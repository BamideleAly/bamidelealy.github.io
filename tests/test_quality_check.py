#!/usr/bin/env python3
"""Unit tests for the static quality-check helpers."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("quality_check", ROOT / "tools" / "quality-check.py")
quality_check = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(quality_check)


class QualityCheckTests(unittest.TestCase):
    def test_contrast_ratio_aaa_black_on_white(self) -> None:
        self.assertGreaterEqual(quality_check.contrast_ratio("#000000", "#ffffff"), 21)

    def test_local_target_resolves_root_relative(self) -> None:
        target = quality_check.local_target(ROOT / "notes" / "index.html", "/privacy.html")
        self.assertEqual(target, ROOT / "privacy.html")

    def test_local_target_resolves_directory_index(self) -> None:
        target = quality_check.local_target(ROOT / "index.html", "notes/")
        self.assertEqual(target, ROOT / "notes" / "index.html")

    def test_report_image_dimension_expectations(self) -> None:
        base = ROOT / "assets" / "reports" / "commercialising-quantum-global-2026"
        self.assertEqual(quality_check.expected_report_dimensions(base / "uk-quantum-strategy.jpg"), (2048, 1365))
        self.assertEqual(quality_check.expected_report_dimensions(base / "uk-quantum-strategy-760.webp"), (760, 507))
        self.assertEqual(quality_check.expected_report_dimensions(base / "uk-quantum-strategy-600.jpg"), (600, 400))

    def test_jpeg_and_webp_dimensions(self) -> None:
        base = ROOT / "assets" / "reports" / "commercialising-quantum-global-2026"
        self.assertEqual(quality_check.jpeg_dimensions(base / "uk-quantum-strategy-600.jpg"), (600, 400))
        self.assertEqual(quality_check.webp_dimensions(base / "uk-quantum-strategy-600.webp"), (600, 400))


if __name__ == "__main__":
    unittest.main()
