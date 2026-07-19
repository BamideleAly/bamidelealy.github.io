#!/usr/bin/env python3
"""Generate article PDFs, QR codes, and social preview QA metadata."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

try:
    import qrcode
    import qrcode.image.svg
except Exception:  # pragma: no cover - dependency guidance is tested via CLI use.
    qrcode = None
try:
    import pikepdf
    from pikepdf import Array, Dictionary, Name, String
except Exception:  # pragma: no cover - dependency guidance is tested via CLI use.
    pikepdf = None

ROOT = Path(__file__).resolve().parents[1]
PDF_DIR = ROOT / "assets" / "pdfs"
QR_DIR = ROOT / "assets" / "qr"
QA_PATH = ROOT / "docs" / "SOCIAL_PREVIEW_QA.json"
CANONICAL_HOST = "https://bamidelealy.com"
SRGB_PROFILE_CANDIDATES = [
    Path("/System/Library/ColorSync/Profiles/sRGB Profile.icc"),
    Path("/Library/ColorSync/Profiles/sRGB Profile.icc"),
    Path("/usr/share/color/icc/sRGB.icc"),
    Path("/usr/share/color/icc/colord/sRGB.icc"),
]
CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome",
    "chromium",
    "chromium-browser",
]


class ArticleParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_article = False
        self.in_title = False
        self.in_description = False
        self.title_parts: list[str] = []
        self.description_parts: list[str] = []
        self.canonical = ""
        self.og_image = ""
        self.og_width = ""
        self.og_height = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {key: value or "" for key, value in attrs}
        classes = set(data.get("class", "").split())
        if tag == "article" and data.get("role") == "article":
            self.in_article = True
        if tag == "h1" and "essay-title" in classes:
            self.in_title = True
        if tag == "p" and "essay-dek" in classes:
            self.in_description = True
        if tag == "link" and data.get("rel") == "canonical":
            self.canonical = data.get("href", "")
        if tag == "meta" and data.get("property") == "og:image":
            self.og_image = data.get("content", "")
        if tag == "meta" and data.get("property") == "og:image:width":
            self.og_width = data.get("content", "")
        if tag == "meta" and data.get("property") == "og:image:height":
            self.og_height = data.get("content", "")

    def handle_endtag(self, tag: str) -> None:
        if tag == "h1":
            self.in_title = False
        if tag == "p":
            self.in_description = False
        if tag == "article":
            self.in_article = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)
        if self.in_description:
            self.description_parts.append(data)

    @property
    def title(self) -> str:
        return re.sub(r"\s+", " ", " ".join(self.title_parts)).strip()

    @property
    def description(self) -> str:
        return re.sub(r"\s+", " ", " ".join(self.description_parts)).strip()


def find_chrome() -> str:
    for candidate in CHROME_CANDIDATES:
        path = Path(candidate)
        if path.exists():
            return str(path)
        resolved = shutil.which(candidate)
        if resolved:
            return resolved
    raise SystemExit("Chrome or Chromium is required for PDF generation.")


def article_pages() -> list[Path]:
    pages: list[Path] = []
    for folder in [ROOT / "notes", ROOT / "fr" / "notes", ROOT / "de" / "notizen"]:
        for page in sorted(folder.glob("*.html")):
            if page.name == "index.html":
                continue
            parser = ArticleParser()
            parser.feed(page.read_text(errors="replace"))
            if parser.canonical and parser.title:
                pages.append(page)
    return pages


def asset_stem(page: Path) -> str:
    return "-".join(page.relative_to(ROOT).with_suffix("").parts)


def canonical_path(canonical: str) -> str:
    parsed = urlparse(canonical)
    return parsed.path or "/"


def generate_qr(url: str, output: Path) -> None:
    if qrcode is None:
        raise SystemExit("Install qrcode with `python3 -m pip install 'qrcode[pil]==8.2'` to generate QR assets.")
    output.parent.mkdir(parents=True, exist_ok=True)
    factory = qrcode.image.svg.SvgPathImage
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_Q, border=2, box_size=10, image_factory=factory)
    qr.add_data(url)
    qr.make(fit=True)
    image = qr.make_image(attrib={"class": "print-qr-code", "role": "img", "aria-label": f"QR code for {url}"})
    image.save(output)


def generate_pdf(chrome: str, base_url: str, page: Path, output: Path, article: ArticleParser) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    url = base_url.rstrip("/") + "/" + page.relative_to(ROOT).as_posix()
    command = [
        chrome,
        "--headless",
        "--no-sandbox",
        "--disable-gpu",
        "--no-pdf-header-footer",
        "--force-renderer-accessibility",
        "--export-tagged-pdf",
        "--enable-features=AccessibilityPDFExport",
        f"--print-to-pdf={output}",
        url,
    ]
    last_error: subprocess.CalledProcessError | None = None
    for _ in range(2):
        try:
            subprocess.run(command, check=True)
            last_error = None
            break
        except subprocess.CalledProcessError as error:
            last_error = error
    if last_error is not None:
        raise last_error
    data = output.read_bytes()
    if len(data) < 10_000:
        raise SystemExit(f"PDF export is suspiciously small: {output}")
    if b"/StructTreeRoot" not in data:
        raise SystemExit(f"PDF lacks a structure tree: {output}")
    rewrite_pdf_2(output, article.title)


def rewrite_pdf_2(output: Path, title: str) -> None:
    if pikepdf is None:
        raise SystemExit("Install pikepdf with `python3 -m pip install -r requirements-dev.txt` to write PDF 2.0 assets.")
    srgb_profile = find_srgb_profile()
    with pikepdf.Pdf.open(output, allow_overwriting_input=True) as pdf:
        root = pdf.Root
        metadata = pdf.make_stream(xmp_metadata(title))
        metadata.Type = Name("/Metadata")
        metadata.Subtype = Name("/XML")
        root.Metadata = metadata
        icc = pdf.make_stream(srgb_profile.read_bytes())
        icc.N = 3
        root.OutputIntents = Array(
            [
                Dictionary(
                    {
                        "/Type": Name("/OutputIntent"),
                        "/S": Name("/GTS_PDFA1"),
                        "/OutputConditionIdentifier": String("sRGB IEC61966-2.1"),
                        "/Info": String("sRGB IEC61966-2.1"),
                        "/DestOutputProfile": icc,
                    }
                )
            ]
        )
        default_rgb = Array([Name("/ICCBased"), icc])
        for page in pdf.pages:
            resources = page.get("/Resources", Dictionary())
            page.Resources = resources
            resources.DefaultRGB = default_rgb
        names = root.get("/Names", Dictionary())
        root.Names = names
        names.EmbeddedFiles = Dictionary({"/Names": Array([])})
        try:
            del pdf.trailer["/Info"]
        except KeyError:
            pass
        pdf.save(output, force_version="2.0")
    data = output.read_bytes()
    if not data.startswith(b"%PDF-2.0"):
        raise SystemExit(f"PDF 2.0 rewrite failed: {output}")
    if b"/StructTreeRoot" not in data:
        raise SystemExit(f"PDF 2.0 rewrite removed the structure tree: {output}")


def xmp_metadata(title: str) -> bytes:
    safe_title = (
        title.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )
    return f'''<?xpacket begin="﻿" id="W5M0MpCehiHzreSzNTczkc9d"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="bamidelealy-pdf-remediation">
 <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="" xmlns:pdfaid="http://www.aiim.org/pdfa/ns/id/" xmlns:pdfuaid="http://www.aiim.org/pdfua/ns/id/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:xmp="http://ns.adobe.com/xap/1.0/" xmlns:pdf="http://ns.adobe.com/pdf/1.3/">
   <pdfaid:part>4</pdfaid:part>
   <pdfaid:rev>2020</pdfaid:rev>
   <pdfaid:conformance>F</pdfaid:conformance>
   <pdfuaid:part>2</pdfuaid:part>
   <pdfuaid:rev>2024</pdfuaid:rev>
   <dc:title><rdf:Alt><rdf:li xml:lang="x-default">{safe_title}</rdf:li></rdf:Alt></dc:title>
   <dc:creator><rdf:Seq><rdf:li>Bamidele Aly</rdf:li></rdf:Seq></dc:creator>
   <xmp:CreatorTool>Chromium print pipeline with pikepdf remediation</xmp:CreatorTool>
   <pdf:Producer>Chromium; pikepdf</pdf:Producer>
  </rdf:Description>
 </rdf:RDF>
</x:xmpmeta>
<?xpacket end="w"?>'''.encode("utf-8")


def find_srgb_profile() -> Path:
    configured = os.environ.get("SRGB_ICC_PROFILE")
    candidates = [Path(configured)] if configured else []
    candidates.extend(SRGB_PROFILE_CANDIDATES)
    for candidate in candidates:
        if candidate.exists():
            return candidate
    searched = ", ".join(str(candidate) for candidate in candidates)
    raise SystemExit(f"sRGB ICC profile not found. Set SRGB_ICC_PROFILE or install a profile at one of: {searched}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://127.0.0.1:8081")
    parser.add_argument("--skip-pdf", action="store_true")
    parser.add_argument("--skip-existing", action="store_true")
    args = parser.parse_args()

    PDF_DIR.mkdir(parents=True, exist_ok=True)
    QR_DIR.mkdir(parents=True, exist_ok=True)
    chrome = None if args.skip_pdf else find_chrome()
    qa: list[dict[str, str | bool]] = []

    for page in article_pages():
        html = page.read_text(errors="replace")
        article = ArticleParser()
        article.feed(html)
        stem = asset_stem(page)
        canonical = article.canonical or CANONICAL_HOST + "/" + page.relative_to(ROOT).as_posix()
        pdf_path = PDF_DIR / f"{stem}.pdf"
        qr_path = QR_DIR / f"{stem}.svg"
        generate_qr(canonical, qr_path)
        if chrome and not (args.skip_existing and pdf_path.exists() and pdf_path.stat().st_size > 10_000):
            generate_pdf(chrome, args.base_url, page, pdf_path, article)
        qa.append(
            {
                "page": page.relative_to(ROOT).as_posix(),
                "title": article.title,
                "canonical": canonical,
                "pdf": pdf_path.relative_to(ROOT).as_posix(),
                "qr": qr_path.relative_to(ROOT).as_posix(),
                "og_image": article.og_image,
                "og_width": article.og_width,
                "og_height": article.og_height,
                "social_preview_ok": article.og_width == "1200" and article.og_height == "630" and "/assets/social/" in article.og_image,
            }
        )
    QA_PATH.write_text(json.dumps({"articles": qa}, indent=2, ensure_ascii=False) + "\n")
    print(f"Generated assets for {len(qa)} articles")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
