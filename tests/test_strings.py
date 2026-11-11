import unittest

from companion_plot import data, strings


class StringsTests(unittest.TestCase):
  def test_same_keys_in_both_languages(self):
    self.assertEqual(set(strings.STRINGS["tr"]), set(strings.STRINGS["en"]))

  def test_no_empty_text(self):
    for lang in strings.LANGS:
      for key, text in strings.STRINGS[lang].items():
        self.assertTrue(text.strip(), f"{lang}:{key}")

  def test_every_crop_and_verdict_is_named(self):
    for lang in strings.LANGS:
      for crop in data.CROPS:
        self.assertIn(f"crop.{crop}", strings.STRINGS[lang])
      for verdict in ("empty", "rough", "okay", "good", "great"):
        self.assertIn(f"verdict.{verdict}", strings.STRINGS[lang])

  def test_placeholders_match(self):
    import re
    for key, en in strings.STRINGS["en"].items():
      tr = strings.STRINGS["tr"][key]
      self.assertEqual(set(re.findall(r"\{(\w+)\}", en)), set(re.findall(r"\{(\w+)\}", tr)), key)

  def test_detect_lang(self):
    self.assertEqual(strings.detect_lang({"LANG": "tr_TR.UTF-8"}), "tr")
    self.assertEqual(strings.detect_lang({"LC_ALL": "en_US.UTF-8", "LANG": "tr_TR"}), "en")

  def test_t_formats_and_falls_back(self):
    self.assertEqual(strings.t("tr", "ui.planted", n=3), "3 kare dolu")
    self.assertEqual(strings.t("xx", "ui.title"), "Companion Plot")


if __name__ == "__main__":
  unittest.main()
