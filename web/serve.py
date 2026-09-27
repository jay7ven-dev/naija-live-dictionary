#!/usr/bin/env python3
"""Serve Live Dictionary UI + Part II translate API from project root."""
from __future__ import annotations

import json
import sys
from http.server import SimpleHTTPRequestHandler
from pathlib import Path
from socketserver import TCPServer
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
PORT = 8765
sys.path.insert(0, str(ROOT / "data"))


def _api_path(raw: str) -> str:
    path = urlparse(raw).path.rstrip("/") or "/"
    return path


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self) -> None:
        path = _api_path(self.path)
        if path in ("", "/", "/index.html"):
            self.send_response(302)
            self.send_header("Location", "/web/")
            self.end_headers()
            return
        if path == "/api/translate":
            self._json(405, {"error": 'POST English text as JSON {"text":"..."}'})
            return
        super().do_GET()

    def do_POST(self) -> None:
        path = _api_path(self.path)
        sys.stderr.write(f"POST {path}\n")
        if path != "/api/translate":
            self._json(404, {"error": f"unknown API path: {path}"})
            return
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length else b"{}"
        try:
            body = json.loads(raw.decode("utf-8"))
            text = (body.get("text") or "").strip()
        except Exception:
            self._json(400, {"error": "invalid JSON body"})
            return
        if not text:
            self._json(400, {"error": "missing text"})
            return
        try:
            from translate_en_pcm import translate_and_normalize

            result = translate_and_normalize(text)
            self._json(200, result)
        except Exception as e:
            self._json(503, {"error": str(e)})

    def do_OPTIONS(self) -> None:
        # Allow simple CORS preflight if a proxy is involved
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def _json(self, code: int, obj: dict) -> None:
        data = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt: str, *args) -> None:
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


class ReuseTCPServer(TCPServer):
    allow_reuse_address = True


def main() -> None:
    with ReuseTCPServer(("", PORT), Handler) as httpd:
        print(f"Serving {ROOT}")
        print(f"Open http://localhost:{PORT}/web/")
        print(f"English → Pidgin  http://localhost:{PORT}/web/normalize.html")
        print(f"POST /api/translate  {{\"text\": \"...\"}}")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
