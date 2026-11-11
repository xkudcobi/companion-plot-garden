import argparse
import sys
import webbrowser

from . import data, engine
from .server import make_server
from .strings import LANGS, detect_lang, t


def parse_args(argv):
  # Pre-parse the language so --help itself is localised.
  pre = argparse.ArgumentParser(add_help=False)
  pre.add_argument("--lang", choices=LANGS)
  known, _ = pre.parse_known_args(argv)
  lang = known.lang or detect_lang()

  parser = argparse.ArgumentParser(prog="companion_plot", description=t(lang, "cli.description"))
  parser.add_argument("--lang", choices=LANGS, default=lang, help=t(lang, "cli.help_lang"))
  parser.add_argument("--port", type=int, default=8765, help=t(lang, "cli.help_port"))
  parser.add_argument("--no-browser", action="store_true", help=t(lang, "cli.help_no_browser"))
  parser.add_argument("--show", action="store_true", help=t(lang, "cli.help_show"))
  return parser.parse_args(argv)


def render_bed(cells, cols=data.COLS):
  rows = [cells[i:i + cols] for i in range(0, len(cells), cols)]
  return "\n".join(
    " ".join((data.CROPS[c]["emoji"] if c else "..") for c in row) for row in rows
  )


def show_sample(lang):
  result = engine.analyze(data.SAMPLE_BED, data.SAMPLE_MONTH)
  print(t(lang, "cli.show_month", month=t(lang, f"month.{data.SAMPLE_MONTH}")))
  print(render_bed(data.SAMPLE_BED))
  print(t(lang, "cli.show_score", percent=result["percent"],
          verdict=t(lang, f"verdict.{result['verdict']}")))


def main(argv=None):
  args = parse_args(sys.argv[1:] if argv is None else argv)
  if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
  if args.show:
    show_sample(args.lang)
    return 0
  server = make_server(args.port)
  if server is None:
    print(t(args.lang, "cli.no_port"), file=sys.stderr)
    return 1
  url = f"http://127.0.0.1:{server.server_address[1]}/"
  print(t(args.lang, "cli.listening", url=url))
  print(t(args.lang, "cli.quit_hint"))
  if not args.no_browser:
    webbrowser.open(url)
  try:
    server.serve_forever()
  except KeyboardInterrupt:
    print("\n" + t(args.lang, "cli.bye"))
  finally:
    server.server_close()
  return 0


if __name__ == "__main__":
  sys.exit(main())
