#!/usr/bin/env python3
"""Serve the static site locally with production-like cache/security headers."""

from __future__ import annotations

import argparse
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATIC_EXTENSIONS = {
    ".avif",
    ".css",
    ".gif",
    ".ico",
    ".jpeg",
    ".jpg",
    ".js",
    ".json",
    ".png",
    ".svg",
    ".webmanifest",
    ".webp",
    ".woff2",
    ".xml",
}


class HeaderHandler(SimpleHTTPRequestHandler):
    """Simple static handler with the same header intent as `_headers`."""

    def end_headers(self) -> None:
        path = self.path.split("?", 1)[0]
        suffix = Path(path).suffix.lower()
        if path.startswith("/assets/") or suffix in STATIC_EXTENSIONS:
            self.send_header("Cache-Control", "public, max-age=31536000, immutable")
        elif path == "/" or path.endswith("/") or suffix == ".html":
            self.send_header("Cache-Control", "public, max-age=300, must-revalidate")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        super().end_headers()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8081, type=int)
    args = parser.parse_args()
    os.chdir(ROOT)
    server = ThreadingHTTPServer((args.host, args.port), HeaderHandler)
    print(f"Serving {ROOT} at http://{args.host}:{args.port}/")
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
