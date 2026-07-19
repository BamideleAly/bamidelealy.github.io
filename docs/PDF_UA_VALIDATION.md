# PDF/UA and PDF/A Validation

The site generates browser-tagged article PDFs under `assets/pdfs/`. The local
quality gate requires a structure tree, QR/source print information, and static
PDF assets for every article.

## Important Standard Boundary

Chrome exports tagged PDFs via Skia/PDF, then `tools/generate-article-assets.py` rewrites the committed article PDFs as `%PDF-2.0` containers with the structure tree preserved. These files are tagged PDF 2.0 assets, but that does not automatically make them PDF/UA-2 or PDF/A-4f compliant. PDF/UA-2 and PDF/A-4f conformance still requires strict validator evidence.

Do not describe a generated PDF as PDF/UA-2 or PDF/A-4f compliant unless the strict validator command passes.

## Commands

Fast structural tagged-PDF audit:

```bash
npm run pdf:audit
```

Strict PDF/UA-1, PDF/UA-2 and PDF/A-4f audit with `verapdf`:

```bash
npm run pdf:ua
```

Strict PDF/UA-2 + PDF/A-4f target audit:

```bash
npm run pdf:ua2-a4f
```

The audit writes `docs/PDF_UA_AUDIT.json` with PDF version, structure-tree
presence and metadata signals. Strict commands add veraPDF conformance results.

## Remediation Path

If strict PDF/UA-2 + PDF/A-4f is required for publication, use a dedicated PDF
remediation toolchain after browser export:

- PAC for interactive PDF/UA inspection;
- axesPDF for tagged-PDF remediation and verification;
- Adobe Acrobat Preflight for PDF/UA and PDF/A profile checks;
- veraPDF for machine-readable conformance reporting.

Required checks:

- PDF header and conformance metadata match the target profile.
- Document catalog contains valid XMP metadata.
- Reading order follows the article sequence.
- Structure tree root has the correct document element and namespace.
- Images have useful alternate text or are marked decorative.
- Artifacts, headers, footers and generated page numbers are correctly tagged.
- Links expose descriptive text and valid targets.
- Output intent, colour profile and embedded-file requirements pass PDF/A-4f.
