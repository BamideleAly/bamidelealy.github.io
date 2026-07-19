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

Bamidele account deployment outline:

```bash
cd workers
npx --yes wrangler@latest kv namespace create bamidelealy_analytics \
  --config analytics-wrangler.jsonc \
  --binding ANALYTICS_KV \
  --update-config

./deploy-analytics.sh
```

Production endpoint:

```html
https://analytics.bamidelealy.com/
```

The repository intentionally does not use a `workers.dev` endpoint. The runtime
sends analytics to the first-party endpoint
`https://analytics.bamidelealy.com/`, and it can still be overridden with
`window.BA_ANALYTICS_ENDPOINT` for staged environments.

The Worker is deployed in Team Bamidele Account:

- Account ID: `85025fbd5f99d3e8b5a876155f6d35e7`
- Worker: `bamidelealy-analytics`
- KV namespace ID: `7f2da22c4c6d48949cf7a429a2980888`
- Current deployed version: `766ee31b-4ae7-4825-8b39-707aafb81a59`
