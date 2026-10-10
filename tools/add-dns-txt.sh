#!/usr/bin/env bash
# Adds a TXT record on oyebuddy.in (Search Console / Bing verification). Usage: tools/add-dns-txt.sh "google-site-verification=XXXX"
# Needs CLOUDFLARE_DNS_TOKEN in the environment (never print it).
set -euo pipefail
VAL="${1:?usage: add-dns-txt.sh 'google-site-verification=...'}"
ZONE=$(curl -s -H "Authorization: Bearer $CLOUDFLARE_DNS_TOKEN" "https://api.cloudflare.com/client/v4/zones?name=oyebuddy.in" | python3 -c "import sys,json;print(json.load(sys.stdin)['result'][0]['id'])")
curl -s -X POST -H "Authorization: Bearer $CLOUDFLARE_DNS_TOKEN" -H "Content-Type: application/json" \
  "https://api.cloudflare.com/client/v4/zones/$ZONE/dns_records" \
  --data "$(python3 -c "import json,sys;print(json.dumps({'type':'TXT','name':'oyebuddy.in','content':sys.argv[1],'ttl':300}))" "$VAL")" | python3 -c "import sys,json;r=json.load(sys.stdin);print('ok' if r['success'] else r['errors'])"
