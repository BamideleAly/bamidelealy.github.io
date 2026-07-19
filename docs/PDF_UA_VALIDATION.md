# PDF/UA and PDF/A Validation

The site generates browser-tagged article PDFs under `assets/pdfs/`. The local
quality gate requires a structure tree, QR/source print information, and static
PDF assets for every article.

## Important Standard Boundary

Chrome exports tagged PDFs via Skia/PDF, then `tools/generate-article-assets.py`
rewrites the committed article PDFs as `%PDF-2.0` containers with a structure
tree, XMP metadata, an sRGB output intent, and PDF/A-4f identifier metadata.
The committed PDFs pass strict `PDF/A-4f` validation in `veraPDF`.

Do not describe a generated PDF as `PDF/UA-2` compliant unless the strict
combined validator command passes. Remaining `PDF/UA-2` failures are semantic
tag-tree issues from browser PDF generation: unartifacted generated content,
non-standard `Strong`/`Em` structure types, figure alternate text, and PDF 2.0
namespace requirements.

## Commands

Fast structural tagged-PDF audit:

```bash
npm run pdf:audit
```

Strict PDF/UA-1 and PDF/UA-2 audit with `verapdf`:

```bash
npm run pdf:ua
```

Strict PDF/A-4f target audit:

```bash
npm run pdf:a4f
```

Strict PDF/UA-2 + PDF/A-4f target audit:

```bash
npm run pdf:ua2-a4f
```

The audit writes `docs/PDF_UA_AUDIT.json` with PDF version, structure-tree
presence and metadata signals. Strict commands add veraPDF conformance results.

## Remediation Path

If strict PDF/UA-2 is required for publication, use a dedicated PDF remediation
toolchain after browser export:

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
