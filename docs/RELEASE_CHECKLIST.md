# Release Checklist

Use this checklist for every production release and every new long-form report.

## 1. Content Completeness

- Confirm every indexable page has one clear editorial purpose.
- Confirm every page has exactly one `<h1>`.
- Confirm page title, meta description, canonical URL, and localized alternates.
- Confirm all facts, names, roles, dates, organisations, and source links.
- Confirm all external links use the right `rel` attributes.
- Confirm conference reports include overview, day/session reconstruction, images, FAQs, source links, and navigation back to the report hub.

## 2. SEO And AI Discovery

- Update `sitemap.xml`.
- Update localized search indexes.
- Update RSS feeds when long-form content changes.
- Update `llms.txt` and `ai.txt` when the public structure changes.
- Confirm JSON-LD is valid and page-specific.
- Confirm report pages include extractable summaries and source sections for AI answer engines.

## 3. Accessibility

- Run `python3 tools/quality-check.py`.
- Run Pa11y WCAG2AAA on representative English, French, and German pages.
- Manually test keyboard navigation for header, menu, language selector, search, FAQ rows, share controls, and contact form.
- Test 200% and 400% zoom.
- Test visible focus and focus-not-obscured behaviour.
- Run WAVE manually before release.
- Test VoiceOver or another screen reader for new templates.

## 4. Performance

- Run Lighthouse against the production-like local server.
- Keep Lighthouse accessibility, best practices, and SEO at 100.
- Keep report performance in the green band and core pages at 98+.
- Check image waste and LCP element.
- Confirm only the true LCP image is preloaded.
- Confirm CSS/JS remain minified and syntax-valid.

## 5. Reader Mode

- Open key articles in Safari Reader Mode.
- Open key articles in Chrome Reading Mode.
- Confirm title, summary, author/date metadata, headings, paragraphs, figures, and captions are preserved.
- Confirm navigation, footer chrome, search overlays, and share controls are not required to understand the article.

## 6. Print

- Run PDF export with `npm run print:report`.
- Run `npm run assets:articles` after article changes.
- Confirm article pages show the PDF icon beside share controls and that it
  links to the static article PDF.
- Confirm FAQ/disclosure answers are visible in print preview and exported PDF.
- Confirm header navigation, search, language selector, share controls, and CTAs are hidden.
- Confirm A4 pagination, no clipped text, readable type, and preserved figure captions.
- Confirm report images carry 300 DPI metadata.
- Confirm exported and static article PDFs contain a structure tree.
- Run `npm run pdf:audit`.
- Run `npm run pdf:a4f` before describing any PDF as PDF/A-4f.
- Run `npm run pdf:ua2-a4f` before describing any PDF as PDF/UA-2.

## 7. Internationalisation

- Confirm EN/FR/DE pages have reciprocal `hreflang`.
- Confirm localized nav labels, footer labels, search labels, and form labels.
- Confirm translated slugs match `sitemap.xml` and search indexes.
- Confirm localized trust pages exist and are linked.

## 8. Release Commands

```bash
npm test
npm run quality
python3 tools/site-inventory.py > /tmp/site-inventory.json
python3 tools/serve-with-headers.py --port 8081
npm run pa11y:report
npm run pa11y:trust
npm run lighthouse:report
npm run print:report
```

## 9. Evidence To Keep

- Lighthouse JSON.
- Pa11y output.
- PDF export.
- Site inventory JSON.
- Screenshot of changed page templates.
- WAVE manual audit notes.
