#!/usr/bin/env bash
# Direct-upload deploy to Cloudflare Pages (free plan). Needs CLOUDFLARE_API_TOKEN (Pages Edit) and CLOUDFLARE_ACCOUNT_ID.
# Deploys the site WITHOUT tools/, DEPLOY.md, README.md, and the www -> apex redirect project.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$(mktemp -d)"
python3 "$ROOT/tools/build.py"
(cd "$ROOT" && tar --exclude=.git --exclude=./tools --exclude=./DEPLOY.md --exclude=./README.md -cf - . | tar -xf - -C "$OUT")
npx wrangler pages deploy "$OUT" --project-name oye-buddy-site --branch main --commit-dirty=true
npx wrangler pages deploy "$ROOT/tools/www-redirect" --project-name oye-buddy-www --branch main --commit-dirty=true
rm -rf "$OUT"
