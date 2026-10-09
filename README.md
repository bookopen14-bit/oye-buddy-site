# OyeBuddy website

Static marketing site for **OyeBuddy** (Oyeteck Innovations, Raipur). Plain HTML + CSS, no framework,
no build step needed to serve it: every `.html` file in this folder is the final page.

- Preview (GitHub Pages, `main` branch, root): https://bookopen14-bit.github.io/oye-buddy-site/
- Play Console "Delete account" URL (keep working): https://bookopen14-bit.github.io/oye-buddy-site/delete-account.html
- Future home: **https://oyebuddy.in** on Cloudflare Pages (see [DEPLOY.md](DEPLOY.md))

## Pages

| File | What |
| --- | --- |
| `index.html` | Landing: hero, features (Discover, Buddy Feed, Nearby, Chats, Verified), safety & privacy, 18+ notice, beta waitlist (mailto, no backend), FAQ |
| `privacy.html`, `terms.html`, `community-guidelines.html`, `safety-tips.html`, `grievance.html` | Generated from `tools/legal/*.md` (copies of `docs/legal/` in the app repo) |
| `delete-account.html` | Account deletion page for Google Play (same content as `site/delete-account.html` in the app repo) |
| `404.html` | Not found page (GitHub Pages and Cloudflare Pages both use it) |

## Editing

Sources live in `tools/`: page bodies in `tools/pages/`, legal markdown in `tools/legal/`, shared head/header/footer
in `tools/build.py`. After editing a source:

```bash
pip install markdown        # once
python3 tools/build.py      # rewrites the .html files, sitemap.xml and robots.txt
python3 -m http.server 8090 # preview at http://localhost:8090/
```

Small text fixes can also be made straight in the `.html` files, but they will be overwritten by the next build.

## Assets

Only the app's own material: real app screenshots (`assets/shots/`, from the app's QA screenshot runs; profiles shown are
the app's demo/seed profiles), the Gold Pin logo and app icon (`oye-buddy-native/mobile/assets`, rendered by
`scripts/render-brand-assets.mjs`), and the login background (`src/assets/login/login-bg.jpg`, AI-generated, fictional people;
see its `SOURCES.md`). Fonts: Instrument Serif and Outfit (SIL OFL 1.1, self-hosted, licences in `assets/fonts/`).
No stock photos, no third-party scripts, no cookies, no analytics.

## Custom domain (not active yet)

There is deliberately **no `CNAME` file**. The domain oyebuddy.in will be served by Cloudflare Pages, not GitHub Pages.
If you ever want GitHub Pages on the domain instead, add a `CNAME` file containing `oyebuddy.in` and set DNS as GitHub
documents. Either way, when the domain goes live, set `BASE_URL = "https://oyebuddy.in"` in `tools/build.py`, run the
build and push (canonical URLs, Open Graph image URLs, sitemap and robots.txt use it).
