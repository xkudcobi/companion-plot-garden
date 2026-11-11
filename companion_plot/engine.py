"""Scoring engine: how happy are the plants in a bed, and what should go where."""

import math

from .data import COLS, CROPS, FOES, FRIENDS, ROWS

FRIEND_BONUS = 2
FOE_PENALTY = -3
SAME_CROP_PENALTY = -1
OFF_SEASON_PENALTY = -2
DIVERSITY_CAP = 6


class BedError(ValueError):
  """Raised for malformed beds; the message is an i18n key."""


def neighbors(index, rows=ROWS, cols=COLS):
  """Indices of the up/down/left/right squares around a square."""
  r, c = divmod(index, cols)
  out = []
  if r > 0:
    out.append(index - cols)
  if r < rows - 1:
    out.append(index + cols)
  if c > 0:
    out.append(index - 1)
  if c < cols - 1:
    out.append(index + 1)
  return out


def pair_effect(a, b):
  if a == b:
    return SAME_CROP_PENALTY
  if b in FRIENDS[a]:
    return FRIEND_BONUS
  if b in FOES[a]:
    return FOE_PENALTY
  return 0


def clean_cells(cells, rows=ROWS, cols=COLS):
  """Validate and normalise a list of crop ids (empty squares become None)."""
  if not isinstance(cells, list) or len(cells) != rows * cols:
    raise BedError("error.bad_bed")
  cleaned = []
  for item in cells:
    if item in (None, ""):
      cleaned.append(None)
    elif isinstance(item, str) and item in CROPS:
      cleaned.append(item)
    else:
      raise BedError("error.unknown_crop")
  return cleaned


def clean_month(month):
  if isinstance(month, bool) or not isinstance(month, int) or not 1 <= month <= 12:
    raise BedError("error.bad_month")
  return month


def harvest_month(crop, month):
  """Month in which a crop sown in `month` is ready."""
  return (month - 1 + math.ceil(CROPS[crop]["days"] / 30)) % 12 + 1


def in_season(crop, month):
  return month in CROPS[crop]["sow"]


def _net_score(cells, month, rows, cols):
  net = 0
  for i, crop in enumerate(cells):
    if crop is None:
      continue
    if not in_season(crop, month):
      net += OFF_SEASON_PENALTY
    for j in neighbors(i, rows, cols):
      if j > i and cells[j] is not None:
        net += pair_effect(crop, cells[j])
  planted = {c for c in cells if c}
  return net + min(len(planted), DIVERSITY_CAP) if planted else 0


def _verdict(percent, planted):
  if planted == 0:
    return "empty"
  if percent < 35:
    return "rough"
  if percent < 60:
    return "okay"
  if percent < 80:
    return "good"
  return "great"


def analyze(cells, month, rows=ROWS, cols=COLS):
  cells = clean_cells(cells, rows, cols)
  month = clean_month(month)
  mood = [0] * len(cells)
  pairs = []
  for i, crop in enumerate(cells):
    if crop is None:
      continue
    for j in neighbors(i, rows, cols):
      other = cells[j]
      if other is None:
        continue
      effect = pair_effect(crop, other)
      mood[i] += effect
      if j > i and effect != 0:
        pairs.append({"a": i, "b": j, "effect": effect})
  planted_count = sum(1 for c in cells if c)
  net = _net_score(cells, month, rows, cols)
  percent = 0
  if planted_count:
    percent = round(max(0, min(100, 50 + 12.5 * net / planted_count)))
  crops_in_bed = sorted({c for c in cells if c})
  return {
    "mood": mood,
    "pairs": pairs,
    "off_season": [i for i, c in enumerate(cells) if c and not in_season(c, month)],
    "net": net,
    "percent": percent,
    "planted": planted_count,
    "verdict": _verdict(percent, planted_count),
    "harvest": {c: harvest_month(c, month) for c in crops_in_bed},
  }


def suggest(cells, month, index, rows=ROWS, cols=COLS):
  """Best crop for one square, judged by the score of the whole bed."""
  cells = clean_cells(cells, rows, cols)
  month = clean_month(month)
  if not isinstance(index, int) or isinstance(index, bool) or not 0 <= index < len(cells):
    raise BedError("error.bad_square")
  # FIXME: suggest() tries one square at a time; a swap of two squares can beat it.
  current = _net_score(cells, month, rows, cols)
  best_crop, best_net = cells[index], current
  for crop in sorted(CROPS):
    trial = cells[:index] + [crop] + cells[index + 1:]
    net = _net_score(trial, month, rows, cols)
    if net > best_net:
      best_crop, best_net = crop, net
  return {"crop": best_crop, "gain": best_net - current}
