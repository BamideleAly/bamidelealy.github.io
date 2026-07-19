#!/usr/bin/env python3
"""Create a starter conference-report page from the maintained template."""

from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "tools" / "templates" / "conference-report.html"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug", help="Article slug, for example my-conference-2026")
    parser.add_argument("--title", required=True)
    parser.add_argument("--description", required=True)
    parser.add_argument("--date", required=True, help="YYYY-MM-DD")
    parser.add_argument("--lang", default="en-GB")
    args = parser.parse_args()
    output = ROOT / "notes" / f"{args.slug}.html"
    if output.exists():
        raise SystemExit(f"Refusing to overwrite {output.relative_to(ROOT)}")
    values = {
        "{{LANG}}": args.lang,
        "{{TITLE}}": args.title,
        "{{DESCRIPTION}}": args.description,
        "{{CANONICAL_PATH}}": f"notes/{args.slug}.html",
        "{{SLUG}}": args.slug,
        "{{VERSION}}": "2026071909",
        "{{SOCIAL_ALT}}": args.title,
        "{{DATE}}": args.date,
        "{{KEYWORDS}}": args.title,
        "{{EYEBROW}}": "Field Report",
        "{{DEK}}": args.description,
        "{{READING_TIME}}": "10 min read",
        "{{DISPLAY_DATE}}": args.date,
        "{{AGENDA_HEADING}}": "Programme map",
        "{{AGENDA_INTRO}}": "List the talks, panels, interviews and moderators before the analysis.",
        "{{AGENDA_SUMMARY}}": "View the full session and speaker roster",
        "{{AGENDA_ARIA}}": "Named agenda",
        "{{SESSION_TITLE}}": "Panel. Session title",
        "{{SESSION_SPEAKERS}}": "Speaker names with verified profile links.",
        "{{THESIS_HEADING}}": "The thesis",
        "{{THESIS}}": "Write the central interpretation here.",
        "{{ANALYSIS_HEADING}}": "What matters operationally",
        "{{ANALYSIS}}": "Write the practical analysis here.",
        "{{FAQ_Q}}": "What should readers take away?",
        "{{FAQ_A}}": "Replace this with a specific answer grounded in the report.",
    }
    text = TEMPLATE.read_text()
    for key, value in values.items():
        text = text.replace(key, value)
    output.write_text(text)
    print(output.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
