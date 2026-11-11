"""Every user-visible text lives here, in Turkish and English."""

import locale
import os

LANGS = ("tr", "en")

_CROP_NAMES = {
  "tr": {
    "tomato": "Domates", "basil": "Fesleğen", "carrot": "Havuç", "onion": "Soğan",
    "lettuce": "Marul", "cucumber": "Salatalık", "pepper": "Biber", "bean": "Fasulye",
    "corn": "Mısır", "potato": "Patates", "garlic": "Sarımsak", "marigold": "Kadife çiçeği",
    "strawberry": "Çilek",
  },
  "en": {
    "tomato": "Tomato", "basil": "Basil", "carrot": "Carrot", "onion": "Onion",
    "lettuce": "Lettuce", "cucumber": "Cucumber", "pepper": "Pepper", "bean": "Bean",
    "corn": "Corn", "potato": "Potato", "garlic": "Garlic", "marigold": "Marigold",
    "strawberry": "Strawberry",
  },
}

_MONTHS = {
  "tr": ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos",
         "Eylül", "Ekim", "Kasım", "Aralık"],
  "en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
}

_TEXT = {
  "tr": {
    "ui.title": "Komşu Tarla",
    "ui.tagline": "Bitkileri tarlaya diz. Dost komşular birbirini büyütür, düşman komşular küstürür.",
    "ui.step1": "1. Aşağıdan bir bitki seç",
    "ui.step2": "2. Tarlada bir kareye dokun",
    "ui.step3": "3. Puanını yükselt",
    "ui.month": "Ekileceği ay",
    "ui.score": "Tarla puanı",
    "ui.planted": "{n} kare dolu",
    "ui.eraser": "Silgi",
    "ui.sample": "Örnek tarla",
    "ui.clear": "Boşalt",
    "ui.help_me": "Seçili kareye öneri ver",
    "ui.legend_happy": "Mutlu",
    "ui.legend_sad": "Huzursuz",
    "ui.legend_cold": "Mevsimi değil",
    "ui.friends_of": "{crop} şunlarla iyi anlaşır:",
    "ui.foes_of": "Şunlardan uzak dursun:",
    "ui.sow_window": "Ekilebilir aylar",
    "ui.calendar": "Hasat takvimi",
    "ui.calendar_note": "Açık yeşil: ekilebilir dönem. 🧺: seçtiğin ayda ekersen hasat ayı.",
    "ui.pairs_good": "En iyi çiftler",
    "ui.pairs_bad": "Kavga edenler",
    "ui.none_yet": "Henüz yok",
    "ui.suggest_pick": "Önce tarlada bir kareye dokun.",
    "ui.suggest_here": "Buraya {crop} dene: {gain} puan artar.",
    "ui.suggest_best": "Bu kare zaten en iyi seçimde.",
    "ui.suggest_fill": "{crop} boş kareye iyi gider.",
    "ui.lang_label": "Dil",
    "ui.pair_line": "{a} + {b}",
    "ui.footer": "Bilgiler genel bahçıvanlık geleneklerinden derlenmiştir; iklimine göre değişebilir.",
    "verdict.empty": "Tarla bomboş. Bir bitki seçip dokunmaya başla!",
    "verdict.rough": "Komşular kavgalı. Kırmızı kareleri değiştir.",
    "verdict.okay": "Fena değil. Biraz daha uyumlu dizebilirsin.",
    "verdict.good": "Güzel bir tarla! Küçük dokunuşlarla mükemmel olur.",
    "verdict.great": "Muhteşem! Komşuların hepsi birbirine bayıldı.",
    "error.bad_bed": "Tarla bilgisi hatalı.",
    "error.unknown_crop": "Bilinmeyen bitki.",
    "error.bad_month": "Ay 1 ile 12 arasında olmalı.",
    "error.bad_square": "Böyle bir kare yok.",
    "error.bad_request": "İstek anlaşılamadı.",
    "error.not_found": "Sayfa bulunamadı.",
    "error.network": "Sunucuya ulaşılamadı. Terminalde program hâlâ açık mı?",
    "cli.description": "Komşu Tarla: bitkileri diz, komşuluk puanını gör.",
    "cli.help_lang": "Arayüz dili (tr veya en)",
    "cli.help_port": "Başlangıç port numarası (varsayılan: 8765)",
    "cli.help_no_browser": "Tarayıcıyı otomatik açma",
    "cli.help_show": "Örnek tarlayı terminalde yazdır ve çık",
    "cli.listening": "Komşu Tarla şurada çalışıyor: {url}",
    "cli.quit_hint": "Kapatmak için Ctrl+C'ye bas.",
    "cli.bye": "Görüşürüz!",
    "cli.no_port": "Boş bir port bulunamadı.",
    "cli.show_score": "Puan: {percent}/100 ({verdict})",
    "cli.show_month": "Ekileceği ay: {month}",
  },
  "en": {
    "ui.title": "Companion Plot",
    "ui.tagline": "Arrange plants in a garden bed. Friendly neighbours help each other grow; rivals sulk.",
    "ui.step1": "1. Pick a plant below",
    "ui.step2": "2. Tap a square in the bed",
    "ui.step3": "3. Push your score up",
    "ui.month": "Sowing month",
    "ui.score": "Bed score",
    "ui.planted": "{n} squares planted",
    "ui.eraser": "Eraser",
    "ui.sample": "Sample bed",
    "ui.clear": "Clear",
    "ui.help_me": "Suggest for selected square",
    "ui.legend_happy": "Happy",
    "ui.legend_sad": "Unhappy",
    "ui.legend_cold": "Wrong season",
    "ui.friends_of": "{crop} gets along with:",
    "ui.foes_of": "Keep it away from:",
    "ui.sow_window": "Sowing months",
    "ui.calendar": "Harvest calendar",
    "ui.calendar_note": "Light green: time to sow. 🧺: harvest month if you sow in the month you picked.",
    "ui.pairs_good": "Best pairs",
    "ui.pairs_bad": "Squabbling pairs",
    "ui.none_yet": "None yet",
    "ui.suggest_pick": "Tap a square in the bed first.",
    "ui.suggest_here": "Try {crop} here: it adds {gain} points.",
    "ui.suggest_best": "This square already has the best choice.",
    "ui.suggest_fill": "{crop} would fit this empty square well.",
    "ui.lang_label": "Language",
    "ui.pair_line": "{a} + {b}",
    "ui.footer": "Pairings follow common gardening folklore; your climate may differ.",
    "verdict.empty": "The bed is empty. Pick a plant and start tapping!",
    "verdict.rough": "The neighbours are fighting. Swap out the red squares.",
    "verdict.okay": "Not bad. A little more harmony would help.",
    "verdict.good": "Lovely bed! A few tweaks and it is perfect.",
    "verdict.great": "Fantastic! Every neighbour adores the others.",
    "error.bad_bed": "The bed data is invalid.",
    "error.unknown_crop": "Unknown plant.",
    "error.bad_month": "Month must be between 1 and 12.",
    "error.bad_square": "No such square.",
    "error.bad_request": "Could not understand the request.",
    "error.not_found": "Page not found.",
    "error.network": "Could not reach the server. Is the program still running in the terminal?",
    "cli.description": "Companion Plot: arrange plants and see how well the neighbours get along.",
    "cli.help_lang": "Interface language (tr or en)",
    "cli.help_port": "Starting port number (default: 8765)",
    "cli.help_no_browser": "Do not open the browser automatically",
    "cli.help_show": "Print the sample bed in the terminal and exit",
    "cli.listening": "Companion Plot is running at {url}",
    "cli.quit_hint": "Press Ctrl+C to stop.",
    "cli.bye": "See you!",
    "cli.no_port": "Could not find a free port.",
    "cli.show_score": "Score: {percent}/100 ({verdict})",
    "cli.show_month": "Sowing month: {month}",
  },
}

# Inserted once so the two month tables and crop names ride along with the text.
for _lang in LANGS:
  for _i, _name in enumerate(_MONTHS[_lang], start=1):
    _TEXT[_lang][f"month.{_i}"] = _name
  for _crop, _name in _CROP_NAMES[_lang].items():
    _TEXT[_lang][f"crop.{_crop}"] = _name

STRINGS = _TEXT


def t(lang, key, **values):
  table = STRINGS.get(lang, STRINGS["en"])
  text = table.get(key, STRINGS["en"].get(key, key))
  return text.format(**values) if values else text


def detect_lang(env=None):
  """Pick tr or en from LANG / LC_ALL or the OS locale; default to en."""
  env = os.environ if env is None else env
  for name in ("LC_ALL", "LC_MESSAGES", "LANG"):
    value = env.get(name, "")
    if value:
      return "tr" if value.lower().startswith("tr") else "en"
  try:
    code = locale.getlocale()[0] or ""
  except (ValueError, TypeError):
    code = ""
  return "tr" if code.lower().startswith("tr") else "en"
