# v0.0.3 Implementation Roadmap

This roadmap maps the ten improvement phases into concrete repository work.

## Phase 1 — Quality Baseline

Status: implemented in v0.0.3.

- Static quality gate.
- Unit tests for quality helpers.
- Production-like local server.
- Browser audit scripts.
- PDF export tooling.
- CI workflow for static checks, unit tests, Pa11y, Lighthouse, and print export.

## Phase 2 — Publishing System

Status: scaffolded.

- Documented content types and required fields.
- Documented image, template, and editorial rules.
- Next: convert pages to front matter and generated HTML.

## Phase 3 — SEO / GEO

Status: partially implemented.

- `sitemap.xml`, `llms.txt`, `ai.txt`, localized search indexes, canonical links, and structured data exist.
- Next: add entity graph, topic hubs, breadcrumbs, source methodology blocks, and answer summaries.

## Phase 4 — Editorial Product

Status: partially implemented.

- Commercialising Quantum Global 2026 has hub, Day 1, Day 2, images, FAQs, share controls, and localized pages.
- Next: add `/reports/`, series pages, sticky desktop table of contents, source notes, and PDF downloads.

## Phase 5 — Performance

Status: partially implemented.

- Static site, minified assets, responsive images, production cache headers.
- Next: critical CSS extraction, AVIF web variants, 480w candidates, page-specific preload manifests, and CSS budget enforcement.

## Phase 6 — Accessibility

Status: implemented for automated baseline; manual release checks documented.

- WCAG2AAA Pa11y scripts.
- AAA contrast token checks.
- Reader hooks and semantic article checks.
- Next: add automated keyboard-flow and visual focus regression tests.

## Phase 7 — Visual System

Status: partially implemented.

- Shared CSS tokens and article system exist.
- Next: create static component gallery and visual regression baselines.

## Phase 8 — Internationalisation

Status: implemented for current pages.

- EN/FR/DE pages, localized search, localized RSS, reciprocal `hreflang`.
- Next: add translation status metadata and glossary.

## Phase 9 — Trust And Authority

Status: partially implemented.

- Accessibility and privacy pages exist in all locales.
- Footer maker credit is enforced.
- Next: add media kit, speaking page, publication citation formats, and newsletter/RSS landing page.

## Phase 10 — Operations

Status: implemented for release discipline.

- Release checklist.
- CI quality workflow.
- Inventory tool.
- Next: add scheduled monthly audits and changelog automation.
