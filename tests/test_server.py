import json
import threading
import unittest
import urllib.error
import urllib.request

from companion_plot import data, server


class ServerTests(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.httpd = server.make_server(18765)
    cls.base = f"http://127.0.0.1:{cls.httpd.server_address[1]}"
    cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
    cls.thread.start()

  @classmethod
  def tearDownClass(cls):
    cls.httpd.shutdown()
    cls.httpd.server_close()

  def post(self, path, payload):
    req = urllib.request.Request(
      self.base + path, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
    try:
      with urllib.request.urlopen(req) as res:
        return res.status, json.load(res)
    except urllib.error.HTTPError as err:
      return err.code, json.load(err)

  def test_pages_are_served(self):
    for path in ("/", "/app.js", "/app.css"):
      with urllib.request.urlopen(self.base + path) as res:
        self.assertEqual(res.status, 200)

  def test_bootstrap_has_both_languages(self):
    with urllib.request.urlopen(self.base + "/api/bootstrap") as res:
      payload = json.load(res)
    self.assertEqual(set(payload["strings"]), {"tr", "en"})
    self.assertEqual(len(payload["sample"]["cells"]), data.ROWS * data.COLS)

  def test_analyze_and_suggest(self):
    status, body = self.post("/api/analyze", {"cells": data.SAMPLE_BED, "month": 4})
    self.assertEqual(status, 200)
    self.assertIn("percent", body)
    status, body = self.post("/api/suggest", {"cells": data.SAMPLE_BED, "month": 4, "index": 0})
    self.assertEqual(status, 200)
    self.assertIn("crop", body)

  def test_bad_input_returns_error_key(self):
    status, body = self.post("/api/analyze", {"cells": [], "month": 4})
    self.assertEqual((status, body["error"]), (400, "error.bad_bed"))
    status, body = self.post("/api/nothing", {"x": 1})
    self.assertEqual(status, 404)

  def test_unknown_get_is_404(self):
    with self.assertRaises(urllib.error.HTTPError) as ctx:
      urllib.request.urlopen(self.base + "/secret.txt")
    self.assertEqual(ctx.exception.code, 404)


if __name__ == "__main__":
  unittest.main()
