# PDF/UA and PDF/A Validation

The site generates browser-tagged article PDFs under `assets/pdfs/`. The local
quality gate requires a structure tree, QR/source print information, and static
PDF assets for every article.

## Important Standard Boundary

Chrome currently exports tagged PDFs as PDF 1.4 (`Skia/PDF`). Those files can be
useful for accessibility remediation, but they are not automatically PDF/UA-2 or
PDF/A-4f. PDF/UA-2 and PDF/A-4f are PDF 2.0-era targets and must be validated
with a PDF standards validator.

Do not describe a generated PDF as PDF/UA-2 or PDF/A-4f compliant unless the
strict validator command passes.

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
