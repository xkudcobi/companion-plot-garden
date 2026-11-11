import unittest

from companion_plot import data, engine


def empty():
  return [None] * (data.ROWS * data.COLS)


class EngineTests(unittest.TestCase):
  def test_neighbors_corner_and_middle(self):
    self.assertEqual(sorted(engine.neighbors(0)), [1, data.COLS])
    self.assertEqual(len(engine.neighbors(data.COLS + 1)), 4)

  def test_pair_effects(self):
    self.assertEqual(engine.pair_effect("tomato", "basil"), engine.FRIEND_BONUS)
    self.assertEqual(engine.pair_effect("tomato", "potato"), engine.FOE_PENALTY)
    self.assertEqual(engine.pair_effect("tomato", "tomato"), engine.SAME_CROP_PENALTY)
    self.assertEqual(engine.pair_effect("carrot", "corn"), 0)

  def test_relations_are_symmetric_and_disjoint(self):
    for a in data.CROPS:
      for b in data.FRIENDS[a]:
        self.assertIn(a, data.FRIENDS[b])
      self.assertFalse(data.FRIENDS[a] & data.FOES[a])

  def test_empty_bed(self):
    result = engine.analyze(empty(), 4)
    self.assertEqual(result["percent"], 0)
    self.assertEqual(result["verdict"], "empty")

  def test_friends_beat_foes(self):
    friends, foes = empty(), empty()
    friends[0], friends[1] = "tomato", "basil"
    foes[0], foes[1] = "tomato", "potato"
    self.assertGreater(engine.analyze(friends, 4)["percent"], engine.analyze(foes, 4)["percent"])

  def test_mood_marks_unhappy_square(self):
    cells = empty()
    cells[0], cells[1] = "tomato", "potato"
    result = engine.analyze(cells, 4)
    self.assertEqual(result["mood"][0], engine.FOE_PENALTY)
    self.assertEqual(result["pairs"], [{"a": 0, "b": 1, "effect": engine.FOE_PENALTY}])

  def test_off_season_is_flagged(self):
    cells = empty()
    cells[3] = "cucumber"
    self.assertEqual(engine.analyze(cells, 1)["off_season"], [3])
    self.assertEqual(engine.analyze(cells, 5)["off_season"], [])

  def test_harvest_month_wraps_year(self):
    self.assertEqual(engine.harvest_month("tomato", 4), 7)
    self.assertEqual(engine.harvest_month("garlic", 10), 6)

  def test_sample_bed_is_good_but_improvable(self):
    result = engine.analyze(data.SAMPLE_BED, data.SAMPLE_MONTH)
    self.assertTrue(55 <= result["percent"] < 95, result["percent"])

  def test_suggest_avoids_foe(self):
    cells = empty()
    cells[0] = "potato"
    best = engine.suggest(cells, 4, 1)
    self.assertNotEqual(best["crop"], "tomato")
    self.assertGreater(best["gain"], 0)

  def test_validation_errors(self):
    with self.assertRaises(engine.BedError):
      engine.analyze([None] * 3, 4)
    with self.assertRaises(engine.BedError):
      engine.analyze(["nope"] + [None] * 23, 4)
    with self.assertRaises(engine.BedError):
      engine.analyze(empty(), 13)
    with self.assertRaises(engine.BedError):
      engine.suggest(empty(), 4, 99)


if __name__ == "__main__":
  unittest.main()
