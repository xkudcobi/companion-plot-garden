"""Static garden knowledge: crops, sowing windows and who gets along with whom."""

ROWS = 4
COLS = 6

# TODO: sowing months assume the northern hemisphere; add a hemisphere switch.
# id -> emoji, sowing months (1-12), days from sowing to harvest
CROPS = {
  "tomato": {"emoji": "🍅", "sow": [3, 4, 5], "days": 80},
  "basil": {"emoji": "🌿", "sow": [4, 5, 6], "days": 60},
  "carrot": {"emoji": "🥕", "sow": [3, 4, 5, 6, 7], "days": 75},
  "onion": {"emoji": "🧅", "sow": [2, 3, 4, 9, 10], "days": 120},
  "lettuce": {"emoji": "🥬", "sow": [3, 4, 5, 8, 9], "days": 45},
  "cucumber": {"emoji": "🥒", "sow": [5, 6], "days": 60},
  "pepper": {"emoji": "🌶️", "sow": [3, 4, 5], "days": 90},
  "bean": {"emoji": "🫘", "sow": [5, 6, 7], "days": 60},
  "corn": {"emoji": "🌽", "sow": [5, 6], "days": 90},
  "potato": {"emoji": "🥔", "sow": [3, 4, 5], "days": 100},
  "garlic": {"emoji": "🧄", "sow": [10, 11], "days": 240},
  "marigold": {"emoji": "🌼", "sow": [4, 5, 6], "days": 60},
  "strawberry": {"emoji": "🍓", "sow": [3, 4, 8, 9], "days": 120},
}

_FRIEND_PAIRS = [
  ("tomato", "basil"), ("tomato", "carrot"), ("tomato", "marigold"),
  ("tomato", "onion"), ("tomato", "garlic"), ("carrot", "onion"),
  ("carrot", "lettuce"), ("carrot", "garlic"), ("carrot", "bean"),
  ("lettuce", "strawberry"), ("lettuce", "onion"), ("cucumber", "bean"),
  ("cucumber", "corn"), ("cucumber", "marigold"), ("pepper", "basil"),
  ("pepper", "onion"), ("pepper", "marigold"), ("bean", "corn"),
  ("potato", "bean"), ("potato", "marigold"), ("potato", "corn"),
  ("strawberry", "garlic"), ("strawberry", "bean"), ("strawberry", "onion"),
]

_FOE_PAIRS = [
  ("tomato", "potato"), ("tomato", "corn"), ("tomato", "cucumber"),
  ("tomato", "strawberry"), ("bean", "onion"), ("bean", "garlic"),
  ("bean", "pepper"), ("potato", "cucumber"), ("potato", "strawberry"),
  ("pepper", "potato"),
]


def _build_relations(pairs):
  table = {crop: set() for crop in CROPS}
  for a, b in pairs:
    table[a].add(b)
    table[b].add(a)
  return table


FRIENDS = _build_relations(_FRIEND_PAIRS)
FOES = _build_relations(_FOE_PAIRS)

# A hand-made starter bed: decent, but with a few squares left to improve.
SAMPLE_BED = [
  "tomato", "basil", "tomato", "marigold", "pepper", "basil",
  "carrot", "onion", "carrot", "onion", "onion", "marigold",
  "lettuce", "carrot", "lettuce", "bean", "corn", "bean",
  "strawberry", "lettuce", "strawberry", "cucumber", "corn", "cucumber",
]
SAMPLE_MONTH = 4
