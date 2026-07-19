<!-- SPDX-License-Identifier: MIT -->

<p align="center">
  <img src="./assets/bamidele-aly-studio.webp" alt="Bamidele Aly" width="128" />
</p>

<h1 align="center">bamidelealy.github.io</h1>

<p align="center">
  Multilingual static website for Bamidele Aly: AI governance, Product
  Control, finance transformation, economic history, creative practice, and
  long-form conference reporting.
</p>

<p align="center">
  <a href="https://github.com/BamideleAly/bamidelealy.github.io/actions"><img src="https://img.shields.io/github/actions/workflow/status/BamideleAly/bamidelealy.github.io/static-quality.yml?style=for-the-badge&label=quality&logo=github" alt="Static quality workflow" /></a>
  <a href="https://bamidelealy.com/"><img src="https://img.shields.io/badge/live-bamidelealy.com-0050a4?style=for-the-badge" alt="Live site" /></a>
  <a href="https://www.w3.org/WAI/WCAG22/quickref/"><img src="https://img.shields.io/badge/WCAG_2.2-AA%2FAAA-1d1d1f?style=for-the-badge" alt="WCAG 2.2 AA / AAA target" /></a>
  <a href="#architecture"><img src="https://img.shields.io/badge/static_site-zero_build-66c2a5?style=for-the-badge&logo=html5&logoColor=white" alt="Static site, zero build" /></a>
  <a href="#license"><img src="https://img.shields.io/badge/license-MIT-545458?style=for-the-badge" alt="License: MIT" /></a>
</p>

---

## Contents

- [Overview](#overview)
- [Current Content](#current-content)
- [Locales](#locales)
- [Commercialising Quantum Global 2026](#commercialising-quantum-global-2026)
- [Architecture](#architecture)
- [Design System](#design-system)
- [Features](#features)
- [SEO and Discovery](#seo-and-discovery)
- [Accessibility](#accessibility)
- [Reader and Print](#reader-and-print)
- [Performance](#performance)
- [Security and Hosting](#security-and-hosting)
- [Development](#development)
- [Publishing Workflow](#publishing-workflow)
- [Quality Checks](#quality-checks)
- [Release Operations](#release-operations)
- [Deployment](#deployment)
- [Repository Metadata](#repository-metadata)
- [License](#license)

---

## Overview

This repository contains the source for `https://bamidelealy.com/`.

The site is deliberately simple operationally: hand-authored HTML, CSS,
vanilla JavaScript, static assets, no build step, and no framework runtime.
It is designed for high-trust professional publishing where accessibility,
SEO, multilingual consistency, and editorial quality matter more than
implementation novelty.

Primary themes:

- AI governance and model risk in regulated finance.
- Product Control, finance transformation, and applied AI systems.
- Economic history, especially West African monetary systems.
- Creative studio practice.
- Long-form conference and field reports, starting with Commercialising
  Quantum Global 2026.

---

## Current Content

### Core English Pages

| Page | Purpose |
|---|---|
| `index.html` | Home page and professional positioning. |
| `projects.html` | Applied AI, Ile Owo, multi-agent architecture, and risk projects. |
| `historian.html` | Economic history, research, publications, and education. |
| `studio.html` | Creative practice across watercolour, Chinese painting, gouache, printmaking, and acrylics. |
| `contact.html` | Advisory, speaking, collaboration, and contact intake. |
| `accessibility.html` | Accessibility statement, WCAG target, testing approach, and feedback route. |
| `privacy.html` | Privacy notice for contact forms, third-party links, and first-party aggregate analytics. |
| `notes/index.html` | Long-form notes and field-report index. |
| `thanks/index.html` | Post-submission confirmation page. |
| `404.html` | Not-found page. |
| `about.html` | Compatibility redirect to `historian.html`. |

### Notes and Reports

| Page | Purpose |
|---|---|
| `notes/commercialising-quantum-global-2026.html` | Main field report on Commercialising Quantum Global 2026. |
| `notes/commercialising-quantum-global-2026-day-1.html` | Day 1 proceedings: promise, platforms, ecosystems, AI, standards, capital, and readiness. |
| `notes/commercialising-quantum-global-2026-day-2.html` | Day 2 proceedings: regulation, Q-Day, post-quantum cryptography, finance, AI convergence, and enterprise adoption. |
| `notes/ile-owo-design.html` | Why Ile Owo uses eight agents rather than one chatbot. |
| `notes/ai-governance-as-road.html` | AI governance as the road to adoption, not a blocker. |
| `notes/bank-of-biafra-project.html` | Bank of Biafra / Central Bank of Nigeria research note. |

The repository currently contains 52 HTML pages across English, French,
German, redirect/compatibility pages, localized notes, and governance pages.

---

## Locales

The site ships in three languages:

- English: canonical root pages.
- French: `/fr/`.
- German: `/de/`.

Each indexable page has reciprocal `hreflang` links for `en-GB`, `fr-FR`,
`de-DE`, and `x-default`. Search indexes and RSS feeds are localized.

| English | French | German |
|---|---|---|
| `/` | `/fr/` | `/de/` |
| `/projects.html` | `/fr/projets.html` | `/de/projekte.html` |
| `/historian.html` | `/fr/historienne.html` | `/de/historikerin.html` |
| `/studio.html` | `/fr/atelier.html` | `/de/atelier.html` |
| `/contact.html` | `/fr/contact.html` | `/de/kontakt.html` |
| `/accessibility.html` | `/fr/accessibilite.html` | `/de/barrierefreiheit.html` |
| `/privacy.html` | `/fr/confidentialite.html` | `/de/datenschutz.html` |
| `/notes/` | `/fr/notes/` | `/de/notizen/` |
| `/notes/commercialising-quantum-global-2026.html` | `/fr/notes/commercialisation-quantique-global-2026.html` | `/de/notizen/commercialising-quantum-global-2026.html` |
| `/notes/commercialising-quantum-global-2026-day-1.html` | `/fr/notes/commercialisation-quantique-global-2026-jour-1.html` | `/de/notizen/commercialising-quantum-global-2026-tag-1.html` |
| `/notes/commercialising-quantum-global-2026-day-2.html` | `/fr/notes/commercialisation-quantique-global-2026-jour-2.html` | `/de/notizen/commercialising-quantum-global-2026-tag-2.html` |
| `/notes/ile-owo-design.html` | `/fr/notes/conception-ile-owo.html` | `/de/notizen/ile-owo-konzept.html` |
| `/notes/ai-governance-as-road.html` | `/fr/notes/gouvernance-ia-comme-route.html` | `/de/notizen/ki-governance-als-strasse.html` |
| `/notes/bank-of-biafra-project.html` | `/fr/notes/projet-banque-biafra.html` | `/de/notizen/projekt-bank-von-biafra.html` |
| `/thanks/` | `/fr/merci/` | `/de/danke/` |
| `/about.html` | `/fr/a-propos.html` | `/de/ueber.html` |

---

## Commercialising Quantum Global 2026

The Commercialising Quantum Global 2026 package is the first full example of
the site’s long-form conference-report model.

It includes:

- A main editorial report.
- Day 1 and Day 2 reconstruction pages.
- French and German localized versions.
- Apple Newsroom-inspired article layout.
- Report navigation near the top of the article.
- Article-specific FAQ sections with expandable `+` rows.
- Social sharing controls for LinkedIn, X, Facebook, email, and copy link.
- Structured metadata for search and social previews.
- Responsive report photography from the provided Word-document source images.

### Report Media

Report images live under:

```text
assets/reports/commercialising-quantum-global-2026/
```

Each photo set has:

- Master JPEG: `2048×1365`.
- Master WebP: `2048×1365`.
- Medium JPEG/WebP: `760×507`.
- Small JPEG/WebP: `600×400`.

The current report image sets are:

- `quantum-commercialisation-hero`
- `uk-quantum-strategy`
- `compute-continuum-panel`
- `post-quantum-cryptography`
- `ai-quantum-convergence`
- `quantum-regulation-strategy`

Images are normalized to a consistent 3:2 editorial ratio and include
embedded Nikon-style metadata supplied for the project.

---

## Architecture

```text
bamidelealy.github.io/
├── index.html
├── projects.html
├── historian.html
├── studio.html
├── contact.html
├── accessibility.html
├── privacy.html
├── about.html
├── 404.html
├── notes/
│   ├── index.html
│   ├── commercialising-quantum-global-2026.html
│   ├── commercialising-quantum-global-2026-day-1.html
│   ├── commercialising-quantum-global-2026-day-2.html
│   ├── ile-owo-design.html
│   ├── ai-governance-as-road.html
│   └── bank-of-biafra-project.html
├── fr/
│   ├── index.html
│   ├── accessibilite.html
│   ├── confidentialite.html
│   ├── notes/
│   ├── rss.xml
│   └── search-data.json
├── de/
│   ├── index.html
│   ├── barrierefreiheit.html
│   ├── datenschutz.html
│   ├── notizen/
│   ├── rss.xml
│   └── search-data.json
├── assets/
│   ├── fonts/
│   ├── icons/
│   ├── diagrams/
│   └── reports/commercialising-quantum-global-2026/
├── styles.css
├── styles.min.css
├── script.js
├── script.min.js
├── search-data.json
├── sitemap.xml
├── rss.xml
├── robots.txt
├── llms.txt
├── ai.txt
├── _headers
├── tools/quality-check.py
└── README.md
```

The production pages can reference minified assets. Source files remain in
the repository for maintainability.

---

## Design System

The visual system is defined in `styles.css` using CSS custom properties and
systematic layout rules.

Key principles:

- Apple-inspired restraint: large whitespace, strong typography, low visual
  noise, and calm interaction states.
- High-contrast colour tokens suitable for AAA normal-text contrast checks.
- Editorial article columns with wider media breaks.
- Native disclosure elements for accessible FAQs.
- Responsive images via `<picture>`, WebP, JPEG fallback, `srcset`, and
  explicit `width`/`height`.
- `prefers-reduced-motion` support for article and UI animations.

Core token groups:

| Token group | Examples |
|---|---|
| Surfaces | `--bg`, `--bg-soft`, `--surface`, `--surface-soft`, `--surface-elev` |
| Text | `--ink`, `--ink-soft`, `--ink-muted` |
| Accent | `--accent`, `--accent-hover`, `--accent-press`, `--accent-soft`, `--accent-ink` |
| Lines | `--line`, `--line-soft` |
| Layout | `--container`, `--article-column`, `--article-media`, `--pad` |
| Typography | `--font-text`, `--font-display` |
| Motion | `--ease-out`, `--ease-in-out` |

---

## Features

### Search

The search palette opens with `Cmd+K`, `Ctrl+K`, or `/`. It lazy-loads the
locale-specific search index:

- English: `search-data.json`
- French: `fr/search-data.json`
- German: `de/search-data.json`

Search supports substring and fuzzy-subsequence matching, keyboard
navigation, translated empty states, and locale-aware URLs.

### Theme

The theme system respects `prefers-color-scheme`, stores a manual override in
`localStorage`, and sets the theme before paint to avoid a flash of the wrong
theme.

### Language Selector

Each standard page has an EN/FR/DE language selector with reciprocal links to
the equivalent localized page. The active locale is marked with
`aria-current="true"`.

### Contact Form

`contact.html` posts to Formspree and falls back gracefully. The thank-you
pages are localized under:

- `thanks/`
- `fr/merci/`
- `de/danke/`

### Article Sharing

Report pages expose professional share actions generated from the canonical
article URL and document title.

---

## SEO and Discovery

The site includes:

- Canonical URLs.
- Open Graph metadata.
- Twitter card metadata.
- JSON-LD structured data.
- Per-locale RSS feeds.
- Per-locale search indexes.
- `sitemap.xml` with localized alternates.
- `robots.txt`.
- `llms.txt`.
- `ai.txt`.
- Public accessibility and privacy notices in English, French, and German.

The Commercialising Quantum pages include article-level metadata for:

- Commercialising Quantum Global 2026.
- Quantum commercialisation.
- Post-quantum cryptography.
- Q-Day.
- Quantum finance.
- AI and quantum convergence.
- Enterprise readiness.
- Standards, regulation, and ecosystem strategy.

---

## Accessibility

Accessibility targets:

- WCAG 2.2 AA for interactive target sizing and usability.
- AAA-level contrast checks for normal body/link text where enforced by
  `tools/quality-check.py`.
- One logical `<h1>` per page.
- Semantic landmarks: `<header>`, `<main>`, `<nav>`, `<footer>`.
- Descriptive image `alt` text.
- Icon-only buttons with `aria-label`.
- Native `<details>/<summary>` for FAQ accordions.
- `prefers-reduced-motion` support.
- Localized language attributes and `hreflang` alternates.

Recent validation:

- Pa11y WCAG2AAA passed on the Day 1 report page during local validation.
- Lighthouse Day 1 accessibility score: `100`.

---

## Reader and Print

Reader-mode and print support are first-class release requirements:

- Every non-redirect page exposes a single `<main>` region with the
  `reader-content` hook.
- Long-form notes, reports, and governance pages use article semantics via
  `<article role="article">`.
- Article pages keep a clear title, description, byline/date metadata, body
  paragraphs, headings, figures, and captions for Safari Reader Mode and
  Chrome Reading Mode.
- Article pages expose a toolbar PDF icon that opens the browser print dialog
  so readers can print or save the article as a PDF.
- The print stylesheet hides navigation, header controls, share controls,
  search, language controls, CTAs, and footer chrome.
- FAQ and disclosure answers are automatically opened for print and restored
  afterward for screen use.
- Print output uses A4 page sizing, inch/point units, high-contrast serif body
  text, sans-serif headings, widow/orphan protection, and forced exact colour
  adjustment where supported.
- Report images include print-specific `<source media="print">` entries that
  point to the 2048×1365 master WebP assets.
- Commercialising Quantum image files carry 300 DPI metadata and remain in
  sRGB for modern printer and browser compatibility.
- PDF export requests Chrome tagged-PDF output and fails if no PDF structure
  tree is produced. Formal PDF/UA certification still requires a specialist
  validator such as PAC because browser-generated PDFs can expose tags without
  guaranteeing every PDF/UA rule.

Chrome PDF print validation:

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --headless \
  --no-sandbox \
  --disable-gpu \
  --print-to-pdf=/tmp/cqg-overview-print.pdf \
  http://127.0.0.1:8081/notes/commercialising-quantum-global-2026.html
```

---

## Performance

The site remains static and low-dependency:

- No client framework.
- No server rendering.
- No build pipeline required to edit content.
- Deferred JavaScript.
- Lazy loading for non-critical imagery.
- Responsive image candidates for report photos.
- Minified CSS/JS committed for static hosting.

Recent Lighthouse Day 1 report:

| Category | Score |
|---|---:|
| Performance | 98 |
| Accessibility | 100 |
| Best Practices | 100 |
| SEO | 100 |

The Lighthouse evidence file is kept in `.lighthouseci/`.

---

## Security and Hosting

The repository includes `_headers` for static hosting platforms that support
Netlify/Cloudflare-style headers.

Header goals:

- Cache static assets aggressively.
- Keep HTML cache shorter.
- Prevent MIME sniffing.
- Reduce unnecessary browser permissions.
- Use strict referrer behavior.

The pages also include a CSP meta tag tailored for this static site and its
contact-form integration.

The site does not ship third-party analytics scripts. The runtime emits
first-party analytics events only, and `workers/analytics-worker.js` provides an
optional privacy-preserving Cloudflare Worker backend. Privacy documentation is
published at `privacy.html`, `fr/confidentialite.html`, and
`de/datenschutz.html`.

---

## Development

Install the lightweight Node metadata used for scripts:

```bash
npm install
python3 -m pip install -r requirements-dev.txt
```

The repository does not persist browser-audit dependencies. Pa11y and
Lighthouse run through pinned `npx` commands so `npm audit` stays clean.

### Serve Locally

```bash
python3 -m http.server 8000
```

For Lighthouse, Pa11y, and print validation, use the production-like local
server with cache/security headers:

```bash
npm run serve
```

Open:

```text
http://localhost:8000/
http://127.0.0.1:8081/
```

Useful report URLs:

```text
http://localhost:8000/notes/commercialising-quantum-global-2026.html
http://localhost:8000/notes/commercialising-quantum-global-2026-day-1.html
http://localhost:8000/notes/commercialising-quantum-global-2026-day-2.html
```

### Edit Content

Edit HTML directly. Keep these synchronized when adding indexable pages:

- Relevant localized HTML pages.
- `search-data.json`
- `fr/search-data.json`
- `de/search-data.json`
- `rss.xml`
- `fr/rss.xml`
- `de/rss.xml`
- `sitemap.xml`

---

## Publishing Workflow

To add a new long-form conference report:

1. Create the English report page under `notes/`.
2. Add day/session pages if the event needs chronological reconstruction.
3. Add French and German localized versions.
4. Add report navigation near the top of the article.
5. Add article-specific FAQs.
6. Add social metadata, canonical URL, Open Graph, Twitter card, and JSON-LD.
7. Process images into the report asset folder with matching 3:2 responsive
   variants.
8. Generate 1200×630 social preview images, QR SVGs, and tagged static PDFs.
9. Add entries to notes indexes, search data, RSS feeds, and sitemap.
10. Update `README.md`, `llms.txt`, and `ai.txt` when site structure changes.
11. Run the static quality check.
12. Validate key pages with accessibility and Lighthouse tooling.

---

## Quality Checks

Run the complete fast local gate:

```bash
npm test
npm run quality
```

Generate a machine-readable inventory:

```bash
npm run inventory
```

Run browser accessibility checks while `npm run serve` is running:

```bash
npm run pa11y:report
npm run pa11y:trust
```

Run Lighthouse while `npm run serve` is running:

```bash
npm run lighthouse:report
```

Export a print PDF while `npm run serve` is running:

```bash
npm run print:report
```

Regenerate article PDFs, QR codes, and social-preview QA while
`npm run serve` is running:

```bash
npm run assets:articles
```

Audit committed article PDFs:

```bash
npm run pdf:audit
```

Strict PDF/A-4f validation is available when `verapdf` is installed:

```bash
npm run pdf:a4f
```

Strict combined PDF/UA-2 + PDF/A-4f validation is also available:

```bash
npm run pdf:ua2-a4f
```

Current article PDFs are tagged, structurally checked, rewritten as `%PDF-2.0` containers, and pass strict `PDF/A-4f` validation in `veraPDF`. They must not be described as `PDF/UA-2` compliant until `npm run pdf:ua2-a4f` passes; remaining failures are semantic tag-tree issues from browser PDF generation.

GitHub Actions runs the v0.0.3 release gate via
`.github/workflows/static-quality.yml`.

The quality gate verifies parseable structured files, local references,
canonical and `hreflang` coverage, image alternatives and dimensions, AAA
contrast-sensitive design tokens, search targets, trust-page discovery,
Commercialising Quantum image dimensions, 1200×630 social previews, static
tagged PDFs, QR assets, print stylesheet requirements, reader-mode hooks,
navigation indicators, governance footer links, and documentation page counts.

---

## Release Operations

Operational documentation:

- `docs/RELEASE_CHECKLIST.md`
- `docs/PUBLISHING.md`
- `docs/PDF_UA_VALIDATION.md`
- `docs/ROADMAP_V0_0_3.md`
- `CONTRIBUTING.md`
- `CHANGELOG.md`

Release-critical tools:

| Command | Purpose |
|---|---|
| `npm test` | Unit tests for quality-check helpers. |
| `npm run quality` | Static HTML/CSS/JS/content/image gate. |
| `npm run inventory` | JSON inventory of pages, languages, titles, descriptions, images, and reader hooks. |
| `npm run serve` | Local server with production-like cache/security headers. |
| `npm run pa11y:report` | WCAG2AAA browser audit for the main report. |
| `npm run pa11y:trust` | WCAG2AAA browser audit for the accessibility page. |
| `npm run lighthouse:report` | Lighthouse JSON audit for the main report. |
| `npm run print:report` | Headless Chrome PDF export for print verification. |
| `npm run assets:articles` | Generates per-article tagged PDFs, QR SVGs, and social-preview QA. |
| `npm run pdf:audit` | Fast structural audit for committed article PDFs. |
| `npm run pdf:a4f` | Strict veraPDF target check for PDF/A-4f. |
| `npm run pdf:ua2-a4f` | Strict veraPDF target check for PDF/UA-2 and PDF/A-4f. |
| `npm run content:example` | Renders the structured conference-report example. |

The v0.0.3 branch is the first operational release branch for scaling from a
hand-authored static site into a controlled publishing system.

---

## Deployment

The site is intended for GitHub Pages or any static host.

Recommended setup:

- Branch: `main`.
- Custom domain: `bamidelealy.com`.
- HTTPS enabled.
- Static headers from `_headers` if the host supports them.

For GitHub Pages with an apex domain, configure the domain in repository
settings and DNS with GitHub Pages-compatible A records or an equivalent
provider-specific `ALIAS`/`ANAME`.

---

## Repository Metadata

Recommended GitHub repository description:

```text
Bamidele Aly’s multilingual professional site for AI governance, Product Control, finance transformation, economic history, and long-form conference reports.
```

Recommended topics:

- `accessibility`
- `ai-governance`
- `conference-report`
- `economic-history`
- `finance-transformation`
- `multilingual`
- `post-quantum-cryptography`
- `product-control`
- `quantum-computing`
- `static-site`

---

## License

MIT. The SPDX header at the top of this file is the canonical declaration.

<p align="right"><a href="#contents">Back to Top</a></p>
