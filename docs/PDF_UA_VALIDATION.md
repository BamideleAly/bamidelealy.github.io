# PDF/UA Validation

The site generates browser-tagged article PDFs as static assets under `assets/pdfs/`.
These files are suitable for the PDF remediation workflow because the generator
requires a PDF structure tree, but browser export alone is not a formal PDF/UA
certificate.

## Automated Local Gate

Run the local static gate after generating PDFs:

```bash
npm run quality
```

The gate checks that every article listed in `docs/SOCIAL_PREVIEW_QA.json` has:

- a static PDF in `assets/pdfs/`;
- a PDF structure tree (`/StructTreeRoot`);
- a canonical QR SVG in `assets/qr/`;
- a 1200×630 Open Graph image in `assets/social/`.

## Formal Certification

Before distributing a PDF as formally PDF/UA compliant, validate it in a
dedicated PDF accessibility tool:

- PAC for PDF/UA checks;
- axesPDF for tagged-PDF remediation and verification;
- Adobe Acrobat Preflight for PDF/UA profile validation.

Required manual checks:

- Document language and title are set correctly.
- Reading order follows the article sequence.
- Headings are nested correctly.
- Images have useful alternate text or are marked decorative.
- Links expose descriptive text and valid targets.
- Tables, lists, footnotes, and captions are tagged correctly.
- The final validator report shows no PDF/UA failures.

Store final certification evidence outside the website build unless it is meant
to be public.
