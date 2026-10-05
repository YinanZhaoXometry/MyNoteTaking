#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ -f .env ]]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

if [[ -z "${VERCEL_TOKEN:-}" ]]; then
  if ! npm exec --package=vercel@47.0.0 -- vercel whoami >/dev/null 2>&1; then
    echo "Not logged in. Run: npm exec --package=vercel@47.0.0 -- vercel login --github --oob"
    exit 1
  fi
  DEPLOY=(npm exec --package=vercel@47.0.0 -- vercel deploy --prod --yes)
else
  DEPLOY=(npm exec --package=vercel@47.0.0 -- vercel deploy --prod --yes --token="$VERCEL_TOKEN")
fi

if [[ ! -d .vercel ]]; then
  echo "Linking project (first time)..."
  if [[ -n "${VERCEL_TOKEN:-}" ]]; then
    npm exec --package=vercel@47.0.0 -- vercel link --yes --token="$VERCEL_TOKEN"
  else
    npm exec --package=vercel@47.0.0 -- vercel link --yes
  fi
fi

echo "Deploying to production..."
"${DEPLOY[@]}"
