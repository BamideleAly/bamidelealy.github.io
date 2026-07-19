# Publishing System

This site remains static, but v0.0.3 treats publishing as a controlled system
rather than ad-hoc HTML editing.

## Content Types

### Standard Page

Used for home, projects, historian, studio, contact, privacy, accessibility,
and localized equivalents.

Required fields:

- `title`
- `description`
- `canonical`
- `language`
- `alternate_urls`
- `nav_section`
- `reader_content`

### Note

Used for long-form essays.

Required fields:

- all standard-page fields
- `author`
- `date_published`
- `date_modified`
- `reading_time`
- `tags`
- `summary`
- `article_schema`

### Conference Report

Used for report hubs and day/session pages.

Required fields:

- all note fields
- `event_name`
- `event_url`
- `event_dates`
- `event_location`
- `source_documents`
- `sessions`
- `speakers`
- `organisations`
- `images`
- `faqs`
- `pdf_asset`
- `qr_asset`
- `social_image_1200x630`

## Editorial Rules

- Put reader value before keyword density.
- Keep panel and lecture names exactly as the source agenda records them.
- Link source agendas directly when public URLs exist.
- Use LinkedIn search links only when direct public profile URLs are ambiguous.
- Every report page needs a top-of-page route to the report hub and day pages.
- Every article needs a concise thesis before deep analysis.
- Every FAQ must answer a real reader question specific to the page.

## Image Rules

- Keep master report images at `2048×1365`, 3:2.
- Keep medium variants at `760×507`.
- Keep small variants at `600×400`.
- Use WebP and JPEG.
- Embed 300 DPI metadata for print assets.
- Add `<source media="print">` pointing to the master WebP.
- Use SVG for icons and interface marks wherever possible.
- Make FAQ and disclosure content meaningful when expanded because print export
  opens all `<details>` answers.

## Template Rules

- One `<main>` per page.
- One `<h1>` per page.
- Standard pages use the shared header/footer pattern.
- Article pages use `<article role="article">`.
- Pages must include `reader-content`.
- Pages with navigation must include the language selector.
- Footer must include RSS, sitemap, `llms.txt`, accessibility/privacy, and maker credit where applicable.
- Long-form article pages must expose the share/copy/PDF toolbar so readers
  can share, print, or save the article as a PDF.
- Printable pages must keep FAQ answers, figure captions, and source notes in
  the document flow so tagged PDF export can include them.
- New conference reports should start from
  `tools/templates/conference-report.html` or
  `tools/scaffold-conference-report.py` so agenda maps, FAQs, social previews,
  reader-mode hooks, print support, and article metadata stay consistent.
- Structured reports can also be drafted in
  `content/conference-reports/*.json` and rendered with
  `tools/build-conference-report.py`.
- After publishing or changing an article, run `npm run assets:articles` while
  the local server is running to refresh PDF, QR, and social-preview QA assets.
- Run `npm run pdf:audit` for committed tagged-PDF structure checks. Run
  `npm run pdf:ua2-a4f` only when a PDF 2.0 remediation toolchain has produced
  candidate PDF/UA-2 + PDF/A-4f files.

## Generation Roadmap

The current v0.0.3 branch adds the gates and conventions needed to move to a
generator safely. The next implementation step is to represent each page as
front matter plus body content, then generate HTML, search, RSS, sitemap,
`llms.txt`, and `ai.txt` from one source of truth.
