#!/usr/bin/env python3
"""Static quality checks for bamidelealy.github.io."""

from __future__ import annotations

import json
import re
import struct
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_HREFLANG = {"en-GB", "fr-FR", "de-DE", "x-default"}
REDIRECT_STUBS = {
    ROOT / "about.html",
    ROOT / "fr" / "a-propos.html",
    ROOT / "de" / "ueber.html",
}
REPORT_ASSETS = ROOT / "assets" / "reports" / "commercialising-quantum-global-2026"
REPORT_IMAGE_DIMENSIONS = {
    "master": (2048, 1365),
    "760": (760, 507),
    "600": (600, 400),
}
TRUST_PAGES = {
    "en": ["accessibility.html", "privacy.html"],
    "fr": ["/fr/accessibilite.html", "/fr/confidentialite.html"],
    "de": ["/de/barrierefreiheit.html", "/de/datenschutz.html"],
}
SOCIAL_IMAGE_DIMENSIONS = (1200, 630)


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.lang: str | None = None
        self.refs: list[tuple[str, str, str]] = []
        self.meta_description = 0
        self.viewport = 0
        self.csp = 0
        self.canonical: list[str] = []
        self.alternates: list[tuple[str, str]] = []
        self.images: list[dict[str, str]] = []
        self.buttons: list[dict[str, str]] = []
        self.summaries = 0
        self.nav_links: list[dict[str, str]] = []
        self.footer_links: list[dict[str, str]] = []
        self.main_count = 0
        self.reader_content = 0
        self.article_roles = 0
        self.language_switchers = 0
        self._in_footer = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {key: value or "" for key, value in attrs}
        classes = set(data.get("class", "").split())
        if tag == "html":
            self.lang = data.get("lang")
        if tag == "main":
            self.main_count += 1
            if "reader-content" in classes:
                self.reader_content += 1
        if tag == "article" and data.get("role") == "article":
            self.article_roles += 1
            if "reader-content" in classes:
                self.reader_content += 1
        if "lang-switch" in classes and data.get("data-lang-switch") == "":
            self.language_switchers += 1
        if tag == "footer" and "site-footer" in classes:
            self._in_footer = True
        if tag == "meta" and data.get("name") == "description":
            self.meta_description += 1
        if tag == "meta" and data.get("name") == "viewport":
            self.viewport += 1
        if tag == "meta" and data.get("http-equiv", "").lower() == "content-security-policy":
            self.csp += 1
        if tag == "link" and data.get("rel") == "canonical":
            self.canonical.append(data.get("href", ""))
        if tag == "link" and data.get("rel") == "alternate" and data.get("hreflang"):
            self.alternates.append((data["hreflang"], data.get("href", "")))
        if tag == "img":
            self.images.append(data)
        if tag == "button":
            self.buttons.append(data)
        if tag == "a" and "nav-link" in classes:
            self.nav_links.append(data)
        if tag == "a" and self._in_footer:
            self.footer_links.append(data)
        if tag == "summary":
            self.summaries += 1
        for attr in ("href", "src", "action"):
            if attr in data:
                self.refs.append((tag, attr, data[attr]))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag: str) -> None:
        if tag == "footer":
            self._in_footer = False


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def local_target(page: Path, ref: str) -> Path | None:
    if ref.startswith(("http://", "https://", "mailto:", "tel:", "data:", "#", "//")):
        return None
    parsed = urlparse(ref)
    path = unquote(parsed.path)
    if not path:
        return None
    target = ROOT / path.lstrip("/") if path.startswith("/") else page.parent / path
    return target / "index.html" if path.endswith("/") else target


def check_structured_files() -> None:
    for path in [ROOT / "search-data.json", ROOT / "fr/search-data.json", ROOT / "de/search-data.json", ROOT / "manifest.json"]:
        json.loads(path.read_text())
    for path in [ROOT / "sitemap.xml", ROOT / "rss.xml", ROOT / "fr/rss.xml", ROOT / "de/rss.xml"]:
        ET.parse(path)


def hex_to_rgb(value: str) -> tuple[float, float, float]:
    value = value.strip().lstrip("#")
    if len(value) == 3:
        value = "".join(char * 2 for char in value)
    return tuple(int(value[i : i + 2], 16) / 255 for i in (0, 2, 4))


def linearize(channel: float) -> float:
    return channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4


def luminance(rgb: tuple[float, float, float]) -> float:
    r, g, b = (linearize(channel) for channel in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(foreground: str, background: str) -> float:
    lighter, darker = sorted(
        (luminance(hex_to_rgb(foreground)), luminance(hex_to_rgb(background))),
        reverse=True,
    )
    return (lighter + 0.05) / (darker + 0.05)


def css_vars(block: str) -> dict[str, str]:
    return {
        name: value
        for name, value in re.findall(r"--([a-z-]+):\s*(#[0-9a-fA-F]{3,6})\s*;", block)
    }


def check_contrast_tokens() -> None:
    css = (ROOT / "styles.css").read_text()
    light_match = re.search(r":root,\s*:root\[data-theme=\"light\"\]\s*\{(?P<body>.*?)\n\s*\}", css, re.S)
    dark_match = re.search(r":root\[data-theme=\"dark\"\]\s*\{(?P<body>.*?)\n\s*\}", css, re.S)
    if not light_match or not dark_match:
        fail("styles.css missing light/dark theme variable blocks")
    for theme, values in [("light", css_vars(light_match.group("body"))), ("dark", css_vars(dark_match.group("body")))]:
        for foreground, background in [
            ("ink", "bg"),
            ("ink-soft", "bg"),
            ("ink-muted", "bg"),
            ("accent", "bg"),
            ("ink", "surface"),
            ("ink-soft", "surface"),
            ("ink-muted", "surface"),
            ("accent", "surface"),
        ]:
            ratio = contrast_ratio(values[foreground], values[background])
            if ratio < 7:
                fail(f"{theme} contrast {foreground}/{background} is {ratio:.2f}:1, below WCAG AAA normal text")


def check_html_pages() -> None:
    for page in sorted(ROOT.glob("**/*.html")):
        if ".git" in page.parts or ".lighthouseci" in page.parts or "tools" in page.parts:
            continue
        text = page.read_text(errors="replace")
        parser = PageParser()
        parser.feed(text)
        if not parser.lang:
            fail(f"{page.relative_to(ROOT)} missing html lang")
        if "<title>" not in text:
            fail(f"{page.relative_to(ROOT)} missing title")
        if "sebastienrousseau.com" not in text:
            fail(f"{page.relative_to(ROOT)} missing maker footer credit")
        if page not in REDIRECT_STUBS:
            if parser.meta_description != 1:
                fail(f"{page.relative_to(ROOT)} has {parser.meta_description} meta descriptions")
            if parser.viewport != 1:
                fail(f"{page.relative_to(ROOT)} has {parser.viewport} viewport tags")
            if parser.csp != 1:
                fail(f"{page.relative_to(ROOT)} has {parser.csp} CSP tags")
        if len(parser.canonical) != 1:
            fail(f"{page.relative_to(ROOT)} has {len(parser.canonical)} canonical links")
        if page not in REDIRECT_STUBS and "404.html" not in str(page):
            alternates = {lang for lang, _ in parser.alternates}
            if not EXPECTED_HREFLANG <= alternates:
                fail(f"{page.relative_to(ROOT)} missing hreflang set")
        if page not in REDIRECT_STUBS and parser.main_count != 1:
            fail(f"{page.relative_to(ROOT)} has {parser.main_count} main elements")
        if page not in REDIRECT_STUBS and parser.reader_content < 1:
            fail(f"{page.relative_to(ROOT)} missing reader-content hook")
        h1_count = len(re.findall(r"<h1\b", text, re.I))
        if page not in REDIRECT_STUBS and h1_count != 1:
            fail(f"{page.relative_to(ROOT)} has {h1_count} h1 elements")
        if parser.nav_links and 'id="navToggle"' not in text:
            fail(f"{page.relative_to(ROOT)} navigation toggle missing navToggle id")
        if parser.nav_links and "404.html" not in str(page) and parser.language_switchers != 1:
            fail(f"{page.relative_to(ROOT)} has {parser.language_switchers} language switchers")
        if parser.nav_links and 'class="nav-link active"' not in text and not any(link.get("aria-current") for link in parser.footer_links):
            fail(f"{page.relative_to(ROOT)} missing static current-page indicator")
        footer_hrefs = {link.get("href", "") for link in parser.footer_links}
        if "404.html" not in str(page):
            rel_parts = page.relative_to(ROOT).parts
            if rel_parts[0] == "fr":
                required_footer = {"/fr/accessibilite.html", "/fr/confidentialite.html"}
            elif rel_parts[0] == "de":
                required_footer = {"/de/barrierefreiheit.html", "/de/datenschutz.html"}
            else:
                required_footer = {"/accessibility.html", "/privacy.html"}
            if not required_footer <= footer_hrefs:
                fail(f"{page.relative_to(ROOT)} missing governance footer links")
        for image in parser.images:
            if "alt" not in image:
                fail(f"{page.relative_to(ROOT)} image missing alt: {image.get('src', '')}")
            if not image.get("width") or not image.get("height"):
                fail(f"{page.relative_to(ROOT)} image missing dimensions: {image.get('src', '')}")
        for button_markup in re.findall(r"<button\b(?P<attrs>[^>]*)>(?P<body>.*?)</button>", text, re.I | re.S):
            attrs, body = button_markup
            has_attribute_name = re.search(r"\b(aria-label|aria-labelledby|title)\s*=", attrs, re.I)
            visible_text = re.sub(r"<[^>]+>", " ", body)
            visible_text = re.sub(r"\s+", " ", visible_text).strip()
            if not has_attribute_name and not visible_text:
                fail(f"{page.relative_to(ROOT)} button missing accessible name")
        if "<details" in text and parser.summaries != len(re.findall(r"<details\b", text, re.I)):
            fail(f"{page.relative_to(ROOT)} details element missing summary")
        if "assets/reports/commercialising-quantum-global-2026" in text and '<source media="print"' not in text:
            fail(f"{page.relative_to(ROOT)} report images missing print-resolution source")
        for _, _, ref in parser.refs:
            target = local_target(page, ref)
            if target and not target.exists():
                fail(f"{page.relative_to(ROOT)} broken local ref {ref} -> {target.relative_to(ROOT)}")


def check_search_targets() -> None:
    for search_file, language in [
        (ROOT / "search-data.json", "en"),
        (ROOT / "fr/search-data.json", "fr"),
        (ROOT / "de/search-data.json", "de"),
    ]:
        entries = json.loads(search_file.read_text())["index"][language]
        for entry in entries:
            target = local_target(search_file, entry["u"])
            if target and not target.exists():
                fail(f"{search_file.relative_to(ROOT)} broken search target {entry['u']}")


def jpeg_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if not data.startswith(b"\xff\xd8"):
        fail(f"{path.relative_to(ROOT)} is not a JPEG file")
    offset = 2
    while offset < len(data):
        if data[offset] != 0xFF:
            offset += 1
            continue
        marker = data[offset + 1]
        offset += 2
        if marker in {0xD8, 0xD9}:
            continue
        length = struct.unpack(">H", data[offset : offset + 2])[0]
        if marker in {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}:
            height, width = struct.unpack(">HH", data[offset + 3 : offset + 7])
            return width, height
        offset += length
    fail(f"{path.relative_to(ROOT)} missing JPEG size marker")


def webp_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        fail(f"{path.relative_to(ROOT)} is not a WebP file")
    chunk = data[12:16]
    if chunk == b"VP8X":
        width = int.from_bytes(data[24:27], "little") + 1
        height = int.from_bytes(data[27:30], "little") + 1
        return width, height
    if chunk == b"VP8 ":
        width, height = struct.unpack("<HH", data[26:30])
        return width & 0x3FFF, height & 0x3FFF
    if chunk == b"VP8L":
        bits = int.from_bytes(data[21:25], "little")
        width = (bits & 0x3FFF) + 1
        height = ((bits >> 14) & 0x3FFF) + 1
        return width, height
    fail(f"{path.relative_to(ROOT)} uses unsupported WebP chunk {chunk!r}")


def expected_report_dimensions(path: Path) -> tuple[int, int]:
    stem = path.stem
    if stem.endswith("-760"):
        return REPORT_IMAGE_DIMENSIONS["760"]
    if stem.endswith("-600"):
        return REPORT_IMAGE_DIMENSIONS["600"]
    return REPORT_IMAGE_DIMENSIONS["master"]


def check_report_images() -> None:
    if not REPORT_ASSETS.exists():
        fail("Commercialising Quantum report asset directory is missing")
    images = sorted(path for path in REPORT_ASSETS.iterdir() if path.suffix.lower() in {".jpg", ".webp"})
    if len(images) != 36:
        fail(f"expected 36 Commercialising Quantum report image variants, found {len(images)}")
    base_names: dict[str, set[str]] = {}
    for image in images:
        size = jpeg_dimensions(image) if image.suffix.lower() == ".jpg" else webp_dimensions(image)
        expected = expected_report_dimensions(image)
        if size != expected:
            fail(f"{image.relative_to(ROOT)} is {size[0]}x{size[1]}, expected {expected[0]}x{expected[1]}")
        stem = re.sub(r"-(600|760)$", "", image.stem)
        base_names.setdefault(stem, set()).add(image.suffix.lower())
    if len(base_names) != 6:
        fail(f"expected 6 Commercialising Quantum image sets, found {len(base_names)}")
    for stem, suffixes in base_names.items():
        if suffixes != {".jpg", ".webp"}:
            fail(f"Commercialising Quantum image set {stem} missing JPEG/WebP pair")


def check_print_styles() -> None:
    css = (ROOT / "styles.css").read_text()
    script = (ROOT / "script.js").read_text()
    if "@media print" not in css or "@page" not in css:
        fail("styles.css missing dedicated print stylesheet")
    for token in [
        "size: A4",
        "margin: .7in .65in .75in",
        "font-size: 11pt",
        "font-family: Georgia",
        ".site-header",
        ".site-footer",
        "display: none !important",
        "inline-size: 6.8in",
        "print-color-adjust: exact",
        "counter(page)",
        ".print-source",
        "string-set: article-title",
    ]:
        if token not in css:
            fail(f"styles.css print stylesheet missing {token}")
    minified_css = (ROOT / "styles.min.css").read_text()
    for calc_expression in re.findall(r"calc\([^)]*\)", minified_css):
        if "+" in calc_expression and not re.search(r"\s\+\s", calc_expression):
            fail(f"styles.min.css contains invalid calc() plus spacing: {calc_expression}")
    if "calc(var(--article-column) + (var(--pad) * 2))" not in minified_css:
        fail("styles.min.css missing valid article-column calc() rule")
    if "article-pdf-link" not in script or "window.print()" not in script:
        fail("script.js missing article PDF/print action")
    if "buildArticleToc()" not in script or "injectPrintSource()" not in script:
        fail("script.js missing article TOC or print-source initialization")


def check_article_assets() -> None:
    qa_path = ROOT / "docs" / "SOCIAL_PREVIEW_QA.json"
    if not qa_path.exists():
        fail("docs/SOCIAL_PREVIEW_QA.json is missing")
    qa = json.loads(qa_path.read_text())
    articles = qa.get("articles", [])
    html_articles = []
    for folder in [ROOT / "notes", ROOT / "fr" / "notes", ROOT / "de" / "notizen"]:
        html_articles.extend(page for page in folder.glob("*.html") if page.name != "index.html")
    if len(articles) != len(html_articles):
        fail(f"social preview QA has {len(articles)} articles, expected {len(html_articles)}")
    for entry in articles:
        page = ROOT / entry["page"]
        pdf = ROOT / entry["pdf"]
        qr = ROOT / entry["qr"]
        if not page.exists():
            fail(f"social preview QA references missing page {entry['page']}")
        if not pdf.exists() or pdf.stat().st_size < 10_000:
            fail(f"missing or suspicious static PDF {entry['pdf']}")
        if b"/StructTreeRoot" not in pdf.read_bytes():
            fail(f"static PDF lacks structure tree {entry['pdf']}")
        if not qr.exists() or "<svg" not in qr.read_text(errors="replace"):
            fail(f"missing QR SVG {entry['qr']}")
        if not entry.get("social_preview_ok"):
            fail(f"social preview QA failed for {entry['page']}")
        image_url = entry.get("og_image", "")
        if "/assets/social/" not in image_url:
            fail(f"{entry['page']} og:image does not use assets/social")
        image_path = ROOT / urlparse(image_url).path.lstrip("/")
        if not image_path.exists():
            fail(f"missing social image {image_path.relative_to(ROOT)}")
        if jpeg_dimensions(image_path) != SOCIAL_IMAGE_DIMENSIONS:
            fail(f"{image_path.relative_to(ROOT)} must be 1200x630")
        text = page.read_text(errors="replace")
        og_dimensions: dict[str, str] = {}
        for first_key, first_value, second_value, second_key in re.findall(
            r"<meta\s+[^>]*(?:property=[\"'](og:image:(?:width|height))[\"'][^>]*content=[\"']([^\"']+)[\"']|content=[\"']([^\"']+)[\"'][^>]*property=[\"'](og:image:(?:width|height))[\"'])",
            text,
            re.I,
        ):
            og_dimensions[first_key or second_key] = first_value or second_value
        if og_dimensions.get("og:image:width") != "1200" or og_dimensions.get("og:image:height") != "630":
            fail(f"{entry['page']} missing 1200x630 social metadata")


def check_discovery_indexes() -> None:
    sitemap = ET.parse(ROOT / "sitemap.xml")
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = {loc.text for loc in sitemap.findall(".//sm:loc", ns) if loc.text}
    expected_urls = {
        "https://bamidelealy.com/accessibility.html",
        "https://bamidelealy.com/privacy.html",
        "https://bamidelealy.com/fr/accessibilite.html",
        "https://bamidelealy.com/fr/confidentialite.html",
        "https://bamidelealy.com/de/barrierefreiheit.html",
        "https://bamidelealy.com/de/datenschutz.html",
    }
    missing = expected_urls - urls
    if missing:
        fail(f"sitemap.xml missing trust pages: {', '.join(sorted(missing))}")
    for search_file, language in [
        (ROOT / "search-data.json", "en"),
        (ROOT / "fr/search-data.json", "fr"),
        (ROOT / "de/search-data.json", "de"),
    ]:
        entries = json.loads(search_file.read_text())["index"][language]
        targets = {entry["u"] for entry in entries}
        for target in TRUST_PAGES[language]:
            if target not in targets:
                fail(f"{search_file.relative_to(ROOT)} missing trust target {target}")


def check_documentation() -> None:
    html_count = len([page for page in ROOT.rglob("*.html") if ".git" not in page.parts and ".lighthouseci" not in page.parts])
    readme = (ROOT / "README.md").read_text()
    if f"{html_count} HTML pages" not in readme:
        fail(f"README.md does not report current HTML page count: {html_count}")
    for path in ["accessibility.html", "privacy.html", "fr/accessibilite.html", "fr/confidentialite.html", "de/barrierefreiheit.html", "de/datenschutz.html"]:
        if path not in readme:
            fail(f"README.md missing {path}")
    for doc in [ROOT / "llms.txt", ROOT / "ai.txt"]:
        text = doc.read_text()
        for url in [
            "https://bamidelealy.com/accessibility.html",
            "https://bamidelealy.com/privacy.html",
        ]:
            if url not in text:
                fail(f"{doc.relative_to(ROOT)} missing {url}")


def main() -> int:
    check_structured_files()
    check_contrast_tokens()
    check_html_pages()
    check_search_targets()
    check_report_images()
    check_print_styles()
    check_article_assets()
    check_discovery_indexes()
    check_documentation()
    print("Static quality checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
