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

Then add this before `script.min.js` on production pages or through an injected
snippet at the hosting layer:

```html
<script>window.BA_ANALYTICS_ENDPOINT = 'https://analytics.bamidelealy.com/';</script>
```

The repository intentionally does not hard-code a `workers.dev` endpoint. The
runtime sends analytics only when `window.BA_ANALYTICS_ENDPOINT` is configured,
and the CSP allows the intended first-party endpoint
`https://analytics.bamidelealy.com`.

The Team Rousseau / sebastienrousseau Worker and KV namespace created during
testing were deleted on 19 July 2026. The available Wrangler login can list the
non-Sebastien account but currently receives Cloudflare API authentication error
`10000` when creating resources there, so final Cloudflare deployment requires a
Bamidele-owned Wrangler session or refreshed permissions.
