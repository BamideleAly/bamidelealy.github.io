#!/usr/bin/env python3
"""Generate a machine-readable site inventory for release reviews."""

from __future__ import annotations

import json
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class InventoryParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self._in_title = False
        self.description = ""
        self.lang = ""
        self.canonical = ""
        self.h1_count = 0
        self.images = 0
        self.reader_content = False
        self.article = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {key: value or "" for key, value in attrs}
        classes = set(data.get("class", "").split())
        if tag == "html":
            self.lang = data.get("lang", "")
        if tag == "title":
            self._in_title = True
        if tag == "meta" and data.get("name") == "description":
            self.description = data.get("content", "")
        if tag == "link" and data.get("rel") == "canonical":
            self.canonical = data.get("href", "")
        if tag == "h1":
            self.h1_count += 1
        if tag == "img":
            self.images += 1
        if "reader-content" in classes:
            self.reader_content = True
        if tag == "article" and data.get("role") == "article":
            self.article = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data.strip()


def page_inventory(path: Path) -> dict[str, object]:
    parser = InventoryParser()
    parser.feed(path.read_text(errors="replace"))
    rel = path.relative_to(ROOT).as_posix()
    return {
        "path": rel,
        "lang": parser.lang,
        "title": parser.title,
        "description": parser.description,
        "canonical": parser.canonical,
        "h1_count": parser.h1_count,
        "image_count": parser.images,
        "reader_content": parser.reader_content,
        "article": parser.article,
    }


def main() -> int:
    pages = [
        page_inventory(path)
        for path in sorted(ROOT.rglob("*.html"))
        if ".git" not in path.parts and ".lighthouseci" not in path.parts
    ]
    inventory = {
        "html_pages": len(pages),
        "languages": sorted({str(page["lang"]) for page in pages if page["lang"]}),
        "pages": pages,
    }
    print(json.dumps(inventory, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
