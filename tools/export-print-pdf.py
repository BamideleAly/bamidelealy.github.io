#!/usr/bin/env python3
"""Export a page to PDF with headless Chrome for print-regression checks."""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome",
    "chromium",
    "chromium-browser",
]


def find_chrome() -> str:
    for candidate in CHROME_CANDIDATES:
        path = Path(candidate)
        if path.exists():
            return str(path)
        resolved = shutil.which(candidate)
        if resolved:
            return resolved
    raise SystemExit("Chrome or Chromium is required for PDF export.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url")
    parser.add_argument("output")
    args = parser.parse_args()
    chrome = find_chrome()
    subprocess.run(
        [
            chrome,
            "--headless",
            "--no-sandbox",
            "--disable-gpu",
            f"--print-to-pdf={args.output}",
            args.url,
        ],
        check=True,
    )
    output = Path(args.output)
    if not output.exists() or output.stat().st_size < 10_000:
        raise SystemExit(f"PDF export failed or produced a suspiciously small file: {output}")
    print(f"Wrote {output} ({output.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
