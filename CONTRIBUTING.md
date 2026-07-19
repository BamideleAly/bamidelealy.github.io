# Contributing

This repository is a professional static publishing site. Changes must preserve
SEO, accessibility, performance, translation consistency, reader-mode support,
and print quality.

## Required Before Pull Request

```bash
npm test
npm run quality
python3 tools/site-inventory.py > /tmp/site-inventory.json
```

For article/report changes, also run:

```bash
python3 tools/serve-with-headers.py --port 8081
npm run pa11y:report
npm run lighthouse:report
npm run print:report
```

## Page Rules

- One `<main>` per page.
- One `<h1>` per page.
- Use `reader-content` on readable content.
- Use `<article role="article">` for long-form notes and reports.
- Keep navigation and footer patterns consistent.
- Preserve language selector coverage.
- Preserve localized `hreflang` alternates.
- Update search, RSS, sitemap, `llms.txt`, and `ai.txt` when public structure changes.

## Image Rules

- Do not add report images without explicit dimensions.
- Keep Commercialising Quantum report masters at `2048×1365`.
- Keep print assets at 300 DPI metadata.
- Prefer SVG for icons and interface graphics.

## Documentation Rules

- Update `README.md` when commands, page counts, content types, or release checks change.
- Update `CHANGELOG.md` for user-facing changes.
- Update `docs/RELEASE_CHECKLIST.md` if release gates change.
