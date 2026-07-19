#!/usr/bin/env python3
"""Serve the static site locally with production-like cache/security headers."""

from __future__ import annotations

import argparse
import gzip
import io
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
COMPRESS_EXTENSIONS = {".css", ".html", ".js", ".json", ".svg", ".txt", ".xml"}


class HeaderHandler(SimpleHTTPRequestHandler):
    """Simple static handler with the same header intent as `_headers`."""

    def send_head(self):  # type: ignore[override]
        path = Path(self.translate_path(self.path))
        if path.is_dir():
            for index in ("index.html", "index.htm"):
                index_path = path / index
                if index_path.exists():
                    path = index_path
                    break
            else:
                return super().send_head()
        if not path.exists() or not path.is_file():
            self.send_error(404, "File not found")
            return None
        content_type = self.guess_type(str(path))
        data = path.read_bytes()
        accepts_gzip = "gzip" in self.headers.get("Accept-Encoding", "")
        if accepts_gzip and path.suffix.lower() in COMPRESS_EXTENSIONS:
            data = gzip.compress(data, compresslevel=9)
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Encoding", "gzip")
            self.send_header("Vary", "Accept-Encoding")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            return io.BytesIO(data)
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        return io.BytesIO(data)

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
