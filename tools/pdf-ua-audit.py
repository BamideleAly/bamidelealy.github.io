#!/usr/bin/env python3
"""Audit generated PDFs for structure and veraPDF PDF/UA/PDF/A targets."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PDF_DIR = ROOT / "assets" / "pdfs"
REPORT = ROOT / "docs" / "PDF_UA_AUDIT.json"


def structural_status(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    first_line = data.splitlines()[0].decode("ascii", errors="replace") if data else ""
    return {
        "file": path.relative_to(ROOT).as_posix(),
        "bytes": len(data),
        "pdf_header": first_line,
        "is_pdf_2": first_line.startswith("%PDF-2."),
        "has_structure_tree": b"/StructTreeRoot" in data,
        "has_lang": b"/Lang" in data,
        "has_title": b"/Title" in data,
    }


def verapdf_status(path: Path, verapdf: str, flavour: str) -> dict[str, object]:
    result = subprocess.run(
        [verapdf, "--format", "json", "--flavour", flavour, str(path)],
        check=False,
        capture_output=True,
        text=True,
    )
    try:
        data = json.loads(result.stdout)
        validation = data["report"]["jobs"][0]["validationResult"][0]
        details = validation.get("details", {})
        return {
            f"verapdf_{flavour}_exit_code": result.returncode,
            f"{flavour}_compliant": bool(validation.get("isCompliant")),
            f"{flavour}_failed_rules": details.get("failedRules", 0),
            f"{flavour}_failed_checks": details.get("failedChecks", 0),
        }
    except Exception:
        return {
            f"verapdf_{flavour}_exit_code": result.returncode,
            f"{flavour}_compliant": False,
            f"verapdf_{flavour}_error": result.stderr.strip()[:1000],
        }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="Fail when selected veraPDF targets report non-compliance.")
    parser.add_argument("--verapdf", action="store_true", help="Run veraPDF profile checks in addition to structural checks.")
    parser.add_argument(
        "--flavours",
        default="ua1,ua2,4f",
        help="Comma-separated veraPDF flavours to run when veraPDF is installed.",
    )
    args = parser.parse_args()
    verapdf = shutil.which("verapdf") if args.verapdf or args.strict else None
    flavours = [item.strip() for item in args.flavours.split(",") if item.strip()]
    entries = []
    for pdf in sorted(PDF_DIR.glob("*.pdf")):
        entry = structural_status(pdf)
        if verapdf:
            for flavour in flavours:
                entry.update(verapdf_status(pdf, verapdf, flavour))
        entries.append(entry)
    REPORT.write_text(json.dumps({"verapdf_available": bool(verapdf), "flavours": flavours, "pdfs": entries}, indent=2) + "\n")
    structural_failures = [entry for entry in entries if not entry["has_structure_tree"]]
    if structural_failures:
        raise SystemExit("One or more PDFs lack /StructTreeRoot")
    if args.strict:
        failures = [
            entry
            for entry in entries
            for flavour in flavours
            if entry.get(f"{flavour}_compliant") is not True
        ]
        if failures:
            raise SystemExit(f"PDF/UA failures: {len(failures)}; see {REPORT.relative_to(ROOT)}")
    print(f"Audited {len(entries)} PDFs; veraPDF available: {bool(verapdf)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
