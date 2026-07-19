#!/usr/bin/env bash
set -euo pipefail

if grep -q "REPLACE_WITH_BAMIDELE_ANALYTICS_KV_ID" analytics-wrangler.jsonc; then
  cat >&2 <<'MSG'
Create the KV namespace from Bamidele's Cloudflare account first, then rerun:

  npx --yes wrangler@latest kv namespace create bamidelealy_analytics \
    --config analytics-wrangler.jsonc \
    --binding ANALYTICS_KV \
    --update-config

Do not deploy this Worker from the Team Rousseau / sebastienrousseau account.
MSG
  exit 2
fi

npx --yes wrangler@latest deploy --config analytics-wrangler.jsonc
