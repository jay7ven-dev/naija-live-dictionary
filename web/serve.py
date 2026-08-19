#!/usr/bin/env python3
"""Serve Live Dictionary UI from project root (required for fetch of data/*.json)."""
from __future__ import annotations

import http.server
import socketserver
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PORT = 8765


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self) -> None:
        if self.path in ("", "/", "/index.html"):
            self.send_response(302)
            self.send_header("Location", "/web/")
            self.end_headers()
            return
        super().do_GET()


class ReuseTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def main() -> None:
    with ReuseTCPServer(("", PORT), Handler) as httpd:
        print(f"Serving {ROOT}")
        print(f"Open http://localhost:{PORT}/web/")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
