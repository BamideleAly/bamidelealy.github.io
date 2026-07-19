# Privacy-Preserving Analytics

The browser runtime emits first-party events only. No third-party analytics script
is required.

## Events

Events are dispatched to:

- `window` as `ba:analytics` custom events;
- `window.dataLayer` for tag-manager compatibility;
- `navigator.sendBeacon(window.BA_ANALYTICS_ENDPOINT, payload)` when an endpoint is configured.

Tracked events cover PDF downloads, print starts, share clicks, copy-link clicks,
FAQ toggles, article TOC clicks, search-result clicks and scroll-depth milestones.

## Backend

`workers/analytics-worker.js` is a minimal Cloudflare Worker that accepts only
aggregate event counters. It stores counts by day, event and path in KV. It does
not store IP addresses, user agents, cookies, referrers or stable identifiers.

Deployment outline:

```bash
cd workers
wrangler kv namespace create ANALYTICS_KV
wrangler deploy --config analytics-wrangler.jsonc
```

Then add this before `script.min.js` on production pages or through an injected
snippet at the hosting layer:

```html
<script>window.BA_ANALYTICS_ENDPOINT = 'https://analytics.bamidelealy.com/';</script>
```
