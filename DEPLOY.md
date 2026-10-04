# Deployment notes: Cloudflare Pages

**Current setup (2026-10-04): Direct Upload, not Git integration.** Run `tools/deploy-cloudflare.sh` after changes
(needs `CLOUDFLARE_API_TOKEN` with Pages Edit and `CLOUDFLARE_ACCOUNT_ID`; wrangler 3 works on Node 20, wrangler 4 needs Node 22).
It uploads the built site without `tools/`, and deploys `tools/www-redirect/` to a separate Pages project `oye-buddy-www`
(bound to `www.oyebuddy.in`) whose `_redirects` sends everything 301 to `https://oyebuddy.in/:splat`. That replaces a
Redirect Rule. GitHub Pages stays on, so the old `bookopen14-bit.github.io/oye-buddy-site/...` URLs keep working.

Two Cloudflare Pages projects on the free plan:

| Project | Source | Domain |
| --- | --- | --- |
| `oye-buddy-site` | public repo `bookopen14-bit/oye-buddy-site` (this repo), branch `main` | `oyebuddy.in` (+ `www.oyebuddy.in` redirect) |
| `oye-buddy-admin` | private repo `bookopen14-bit/oye-buddy`, folder `admin-web/` | `admin.oyebuddy.in` |

Prerequisite for both: the `oyebuddy.in` zone is added to Cloudflare (Dashboard → Add a domain → Free plan) and the
registrar's nameservers are changed to the two Cloudflare nameservers it shows. Wait until the zone shows **Active**.

---

## 1. Marketing site → oyebuddy.in

1. Dashboard → **Workers & Pages → Create → Pages → Connect to Git** → pick `bookopen14-bit/oye-buddy-site`.
2. Build settings:
   - Framework preset: **None**
   - Build command: *(leave empty)*. The HTML is already built and committed.
   - Build output directory: `/`
   - Root directory: *(empty)*
3. Save and Deploy. The preview is at `https://oye-buddy-site.pages.dev` (name may differ).
4. Project → **Custom domains → Set up a custom domain** → `oyebuddy.in`. Because the zone is on Cloudflare, it adds the DNS
   record and the certificate automatically. Add `www.oyebuddy.in` too, then create a redirect
   (Rules → Redirect Rules: `www.oyebuddy.in/*` → `https://oyebuddy.in/${1}`, 301), or use Bulk Redirects.
5. Switch canonical URLs to the domain: in `tools/build.py` set `BASE_URL = "https://oyebuddy.in"`,
   run `python3 tools/build.py`, commit, push. Cloudflare redeploys on every push to `main`.
6. `_headers` in this repo sets security headers and asset caching on Cloudflare (GitHub Pages ignores it).
   `404.html` is used automatically.
7. Do **not** add a `CNAME` file; that is only for GitHub Pages.

### Keep the Play Console deletion URL working

Google Play currently has `https://bookopen14-bit.github.io/oye-buddy-site/delete-account.html`. Leave GitHub Pages enabled
on this repo, so that URL keeps working alongside Cloudflare (both serve the same `main` branch). When the domain is live,
update Play Console → App content → Data safety → Delete account URL to `https://oyebuddy.in/delete-account.html`.
Also use `https://oyebuddy.in/privacy.html` as the Privacy Policy URL in the store listing.
If you later turn GitHub Pages off, update Play Console **first**.

Optional: Cloudflare Pages also supports Direct Upload (`npx wrangler pages deploy . --project-name oye-buddy-site`)
if you don't want the Git integration.

---

## 2. Admin dashboard (admin-web) → admin.oyebuddy.in

The repo is private, which Cloudflare Pages supports (the GitHub app asks for access to just that repo).

1. **Workers & Pages → Create → Pages → Connect to Git** → `bookopen14-bit/oye-buddy`.
2. Production branch: the branch admin-web ships from (for example `main`; the work currently sits on `feat/supabase-phase2`).
3. Build settings:
   - Framework preset: **Vite** (or None)
   - Root directory: `admin-web`
   - Build command: `npm run build` (runs `tsc -b && vite build`)
   - Build output directory: `dist`
4. Environment variables (Settings → Variables and secrets), set for **Production** and **Preview**:

   | Name | Value |
   | --- | --- |
   | `VITE_SUPABASE_URL` | `https://<project-ref>.supabase.co` (the production project) |
   | `VITE_SUPABASE_ANON_KEY` | the **anon / publishable** key only. Never the service_role / secret key; the app refuses to start with one. |
   | `NODE_VERSION` | `22` (Vite 7 needs Node 20.19+ or 22.12+) |
   | `VITE_SENTRY_DSN` | optional, empty = off |
   | `VITE_APP_ENV` | optional, `production` |

   `VITE_*` values are baked in at build time. After changing one, **retry the deployment** (Deployments → ⋯ → Retry).
   They are public in the bundle by design (anon key + RLS + staff-only RPCs), so a plain variable is fine.
5. Custom domains → `admin.oyebuddy.in` (DNS record and certificate are created automatically).
6. Lock it down (recommended, free up to 50 users): **Zero Trust → Access → Applications → Self-hosted**,
   domain `admin.oyebuddy.in`, policy "Allow" with the staff emails (one-time PIN login). Also add the
   `*.oye-buddy-admin.pages.dev` preview hostnames to the same application, or turn off preview deployments,
   so previews are not open to the public either.
7. Supabase: admin-web signs in with email + password (`signInWithPassword`), so no redirect URL is needed.
   If you later add magic links or OAuth to admin-web, add `https://admin.oyebuddy.in` to
   Supabase → Authentication → URL Configuration → Redirect URLs.
8. admin-web is a single page with no client-side routes, so no SPA `_redirects` rule is needed. If routes are added later,
   add `admin-web/public/_redirects` containing `/* /index.html 200`.
9. Keep it out of search engines: it already sets a `robots` noindex meta. Optionally add
   `admin-web/public/_headers` with `/*` + `X-Robots-Tag: noindex` and `X-Frame-Options: DENY`.

Build check before connecting: `cd admin-web && npm ci && npm run build` must finish without type errors,
because Cloudflare runs exactly that.
