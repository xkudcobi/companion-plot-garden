"""Tiny local web server: serves the page and answers scoring requests."""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from . import data, engine
from .strings import STRINGS

WEB_DIR = Path(__file__).parent / "web"
STATIC_FILES = {
  "/": ("index.html", "text/html; charset=utf-8"),
  "/app.css": ("app.css", "text/css; charset=utf-8"),
  "/app.js": ("app.js", "application/javascript; charset=utf-8"),
}
MAX_BODY = 20_000


def bootstrap_payload():
  crops = {}
  for crop_id, info in data.CROPS.items():
    crops[crop_id] = {
      "emoji": info["emoji"],
      "sow": info["sow"],
      "friends": sorted(data.FRIENDS[crop_id]),
      "foes": sorted(data.FOES[crop_id]),
    }
  return {
    "strings": STRINGS,
    "crops": crops,
    "rows": data.ROWS,
    "cols": data.COLS,
    "sample": {"cells": data.SAMPLE_BED, "month": data.SAMPLE_MONTH},
  }


def handle_api(path, body):
  """Return (status, payload) for an API call; errors carry an i18n key."""
  try:
    if path == "/api/analyze":
      return 200, engine.analyze(body.get("cells"), body.get("month"))
    if path == "/api/suggest":
      return 200, engine.suggest(body.get("cells"), body.get("month"), body.get("index"))
  except engine.BedError as exc:
    return 400, {"error": str(exc)}
  return 404, {"error": "error.not_found"}


class Handler(BaseHTTPRequestHandler):
  server_version = "CompanionPlot"

  def log_message(self, fmt, *args):
    pass

  def _send(self, status, body, content_type):
    self.send_response(status)
    self.send_header("Content-Type", content_type)
    self.send_header("Content-Length", str(len(body)))
    self.send_header("Cache-Control", "no-store")
    self.end_headers()
    self.wfile.write(body)

  def _send_json(self, status, payload):
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    self._send(status, body, "application/json; charset=utf-8")

  def do_GET(self):
    path = self.path.split("?", 1)[0]
    if path == "/api/bootstrap":
      return self._send_json(200, bootstrap_payload())
    if path in STATIC_FILES:
      name, ctype = STATIC_FILES[path]
      return self._send(200, (WEB_DIR / name).read_bytes(), ctype)
    self._send_json(404, {"error": "error.not_found"})

  def do_POST(self):
    path = self.path.split("?", 1)[0]
    try:
      length = int(self.headers.get("Content-Length", "0"))
      if not 0 < length <= MAX_BODY:
        raise ValueError
      body = json.loads(self.rfile.read(length).decode("utf-8"))
      if not isinstance(body, dict):
        raise ValueError
    except (ValueError, UnicodeDecodeError):
      return self._send_json(400, {"error": "error.bad_request"})
    status, payload = handle_api(path, body)
    self._send_json(status, payload)


def make_server(start_port=8765, tries=20):
  """Bind to the first free port at or after start_port; None if all are taken."""
  for port in range(start_port, start_port + tries):
    try:
      return ThreadingHTTPServer(("127.0.0.1", port), Handler)
    except OSError:
      continue
  return None
