#!/usr/bin/env python3
"""Build a conference report page from structured JSON content."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def render(data: dict) -> str:
    sessions = "\n".join(
        f"<article><h3>{esc(item['title'])}</h3><p>{esc(item.get('speakers', ''))}</p></article>"
        for item in data.get("sessions", [])
    )
    chapters = "\n".join(
        f"<section class=\"essay-chapter\" id=\"{esc(item['id'])}\"><h2>{esc(item['heading'])}</h2>" +
        "".join(f"<p>{esc(paragraph)}</p>" for paragraph in item.get("paragraphs", [])) +
        "</section>"
        for item in data.get("chapters", [])
    )
    faqs = "\n".join(
        f"<details><summary>{esc(item['question'])}</summary><p>{esc(item['answer'])}</p></details>"
        for item in data.get("faqs", [])
    )
    return f"""<!DOCTYPE html>
<html lang=\"{esc(data.get('lang', 'en-GB'))}\">
<head>
<meta charset=\"utf-8\">
<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
<title>{esc(data['title'])} | Bamidele Aly</title>
<meta name=\"description\" content=\"{esc(data['description'])}\">
<meta name=\"author\" content=\"Bamidele Aly\">
<meta name=\"robots\" content=\"index, follow, max-image-preview:large\">
<link rel=\"canonical\" href=\"https://bamidelealy.com/{esc(data['canonical_path'])}\">
<meta property=\"og:type\" content=\"article\">
<meta property=\"og:site_name\" content=\"Bamidele Aly\">
<meta property=\"og:title\" content=\"{esc(data['title'])}\">
<meta property=\"og:description\" content=\"{esc(data['description'])}\">
<meta property=\"og:image\" content=\"https://bamidelealy.com/assets/social/{esc(data['slug'])}.jpg?v={esc(data.get('version', '2026071909'))}\">
<meta property=\"og:image:width\" content=\"1200\">
<meta property=\"og:image:height\" content=\"630\">
<meta name=\"twitter:card\" content=\"summary_large_image\">
<meta name=\"twitter:image\" content=\"https://bamidelealy.com/assets/social/{esc(data['slug'])}.jpg?v={esc(data.get('version', '2026071909'))}\">
<link rel=\"stylesheet\" href=\"../styles.min.css?v={esc(data.get('version', '2026071909'))}\">
</head>
<body class=\"essay-snap\">
<a class=\"skip-link\" href=\"#main\">Skip to main content</a>
<main id=\"main\" class=\"reader-content\"><article class=\"reader-content\" role=\"article\">
<section class=\"essay-hero\"><div class=\"container\"><span class=\"essay-eyebrow\">{esc(data.get('eyebrow', 'Field Report'))}</span><h1 class=\"essay-title\">{esc(data['title'])}</h1><p class=\"essay-dek\">{esc(data['dek'])}</p><p class=\"essay-meta\"><span>By Bamidele Aly</span><span class=\"dot\" aria-hidden=\"true\"></span><span>{esc(data.get('reading_time', '10 min read'))}</span><span class=\"dot\" aria-hidden=\"true\"></span><time datetime=\"{esc(data['date'])}\">{esc(data['date'])}</time></p></div></section>
<section class=\"essay-body\"><div class=\"container\">
<section class=\"essay-chapter programme-map no-drop\" id=\"agenda-index\"><h2>Programme map</h2><p>{esc(data.get('agenda_intro', 'Talks, panels and interviews are listed before the analysis.'))}</p><details class=\"programme-details\"><summary>View the full session and speaker roster</summary><div class=\"session-index\" aria-label=\"Named agenda\">{sessions}</div></details></section>
{chapters}
<section class=\"essay-chapter no-drop apple-faq\" id=\"faq\"><h2><span>Questions?</span> <span>Answers.</span></h2><div class=\"faq-list\">{faqs}</div></section>
</div></section></article></main>
<script src=\"../script.min.js?v={esc(data.get('version', '2026071909'))}\" defer></script>
</body></html>\n"""


def validate(data: dict) -> None:
    required = ["slug", "title", "description", "canonical_path", "dek", "date", "sessions", "chapters", "faqs"]
    missing = [key for key in required if not data.get(key)]
    if missing:
        raise SystemExit(f"Missing required fields: {', '.join(missing)}")
    if len(data["faqs"]) < 3:
        raise SystemExit("Conference reports require at least three FAQs")
    if len(data["sessions"]) < 1:
        raise SystemExit("Conference reports require at least one session")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = json.loads(args.source.read_text())
    validate(data)
    html_text = render(data)
    if args.check:
        print(f"Valid conference report source: {args.source}")
    elif args.write:
        output = ROOT / data["canonical_path"]
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(html_text)
        print(output.relative_to(ROOT))
    else:
        print(html_text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
