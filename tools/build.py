#!/usr/bin/env python3
"""Regenerates the static pages from tools/pages/*.html bodies and tools/legal/*.md.

The site itself needs no build step: the generated .html files are committed and
served as they are. Run this only after editing a source file:

    pip install markdown   # once
    python3 tools/build.py

Legal sources are copies of docs/legal/*.md from the app repo (keep them in sync).
To move to the custom domain, change BASE_URL below, re-run, and commit.
"""
import html, pathlib, re, markdown

BASE_URL = "https://oyebuddy.in"
ROOT = pathlib.Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
SUPPORT = "support@oyebuddy.in"
GRIEVANCE = "grievance@oyebuddy.in"

LEGAL = [  # (md file, output, nav label, meta description)
    ("privacy-policy.md", "privacy.html", "Privacy", "How Oyeteck Innovations collects, uses and protects your personal data in the Oye Buddy dating app, under India's DPDP Act 2023."),
    ("terms-of-service.md", "terms.html", "Terms", "The Terms of Service for Oye Buddy, the Indian dating app for meeting real people nearby."),
    ("community-guidelines.md", "community-guidelines.html", "Community Guidelines", "The rules that keep Oye Buddy kind, real and safe: be real, be respectful, no scams, report and block."),
    ("safety-tips.md", "safety-tips.html", "Safety tips", "Simple habits for meeting someone from Oye Buddy safely, plus India emergency helplines."),
    ("grievance-officer.md", "grievance.html", "Grievance Officer", "Contact the Oye Buddy Grievance Officer under the IT Rules 2021 and DPDP Act 2023. Acknowledged within 24 hours, resolved within 15 days."),
]
DOC_NAV = [(o, l) for _, o, l, _ in LEGAL] + [("delete-account.html", "Delete account")]

PIN = '<img src="assets/img/logo-mark-128.png" width="34" height="34" alt="">'

def head(title, desc, path, extra=""):
    url = f"{BASE_URL}/{'' if path == 'index.html' else path}"
    return f"""<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#070706">
<meta name="color-scheme" content="dark">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Oye Buddy">
<meta property="og:locale" content="en_IN">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE_URL}/assets/img/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Oye Buddy: gold pin logo and app screens on black">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{BASE_URL}/assets/img/og.jpg">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
<link rel="preload" href="assets/fonts/instrument-serif-latin-400-italic.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/outfit-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/site.css">
{extra}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""

def header(home=False):
    p = "" if home else "index.html"
    return f"""<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{p or '#top'}" aria-label="Oye Buddy home">{PIN}<span>Oye Buddy</span></a>
    <nav class="nav" aria-label="Main">
      <a href="{p}#features">Features</a>
      <a href="{p}#safety">Safety</a>
      <a href="{p}#faq">FAQ</a>
      <a class="btn btn-gold btn-sm" href="{p}#waitlist">Join the beta</a>
    </nav>
  </div>
</header>
"""

FOOTER = f"""<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="brand" href="index.html" aria-label="Oye Buddy home">{PIN}<span>Oye Buddy</span></a>
        <p class="muted" style="max-width:30em;margin:16px 0 0">Meet real people nearby. Local, live, unplanned. Strictly 18+.</p>
        <address style="margin-top:16px">
          Oye Buddy is operated by <strong style="color:var(--fg);font-weight:500">Oyeteck Innovations</strong><br>
          Currency Tower, Raipur, Chhattisgarh 492001, India
        </address>
      </div>
      <div>
        <h4>Legal</h4>
        <ul>
          <li><a href="privacy.html">Privacy Policy</a></li>
          <li><a href="terms.html">Terms of Service</a></li>
          <li><a href="community-guidelines.html">Community Guidelines</a></li>
          <li><a href="safety-tips.html">Safety tips</a></li>
          <li><a href="delete-account.html">Delete account</a></li>
          <li><a href="grievance.html">Grievance Officer</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li>Support<br><a href="mailto:{SUPPORT}">{SUPPORT}</a></li>
          <li>Grievance Officer: Mayank Chandravanshi<br><a href="mailto:{GRIEVANCE}">{GRIEVANCE}</a></li>
          <li>Emergency in India: <a href="tel:112">112</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-bottom">
      <span>© 2026 Oyeteck Innovations. Made in India.</span>
      <span>Oye Buddy is for adults 18+ only. Google Play is a trademark of Google LLC.</span>
    </div>
  </div>
</footer>
"""

def doc_nav(current):
    return '<nav class="doc-nav" aria-label="Legal pages">' + "".join(
        f'<a href="{o}"{" aria-current=page" if o == current else ""}>{l}</a>' for o, l in DOC_NAV) + "</nav>"

def linkify(s):
    s = re.sub(r"(?<![\w@/\">])([\w.+-]+@[\w-]+\.[\w.]+\w)", r'<a href="mailto:\1">\1</a>', s)
    s = s.replace("cybercrime.gov.in", '<a href="https://cybercrime.gov.in" rel="noopener">cybercrime.gov.in</a>')
    s = re.sub(r"\*\*(112|181|1930)\*\*", r'<strong><a href="tel:\1">\1</a></strong>', s)
    return s

def build_legal():
    for md, out, label, desc in LEGAL:
        src = (TOOLS / "legal" / md).read_text()
        src = linkify(src)
        body = markdown.markdown(src, extensions=["sane_lists", "nl2br"])
        title_m = re.search(r"<h1>(.*?)</h1>", body)
        title = title_m.group(1)
        body = body.replace(title_m.group(0), "", 1)
        body = re.sub(r"<p><strong>Last updated:</strong>(.*?)</p>", r'<p class="updated">Last updated:\1</p>', body)
        page = (head(f"{title} | Oye Buddy", desc, out) + header() +
                f'<main id="main" class="doc">\n<p class="eyebrow">Oye Buddy · Legal</p>\n<h1>{title}</h1>\n{doc_nav(out)}\n{body}\n</main>\n' + FOOTER + "</body>\n</html>\n")
        (ROOT / out).write_text(page)
        print("wrote", out)

def build_pages():
    for name, title, desc in [
        ("index.html", "Oye Buddy: meet real people nearby | Indian dating app", "Oye Buddy is a premium Indian dating app for meeting real people nearby. Discover, Buddy Feed, an area map that never shows exact locations, selfie-verified badges and strong safety tools. Coming soon on Google Play: join the beta."),
        ("delete-account.html", "Delete your Oye Buddy account", "How to delete your Oye Buddy account and data, in the app or by email, and what is deleted or kept."),
        ("404.html", "Page not found | Oye Buddy", "This page does not exist. Go back to Oye Buddy."),
    ]:
        src = (TOOLS / "pages" / name).read_text()
        extra, _, body = src.partition("<!--BODY-->")
        if name == "delete-account.html":
            body = body.replace("<!--DOCNAV-->", doc_nav(name))
        page = head(title, desc, name, extra.strip() + "\n" if extra.strip() else "") + header(home=name == "index.html") + body.strip() + "\n" + FOOTER + "</body>\n</html>\n"
        if name == "404.html":
            page = page.replace('<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">')
        (ROOT / name).write_text(page)
        print("wrote", name)

def build_sitemap():
    urls = ["", "delete-account.html"] + [o for _, o, _, _ in LEGAL]
    items = "".join(f"  <url><loc>{BASE_URL}/{u}</loc><lastmod>2026-10-04</lastmod></url>\n" for u in urls)
    (ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{items}</urlset>\n')
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n")
    print("wrote sitemap.xml, robots.txt")

if __name__ == "__main__":
    build_pages(); build_legal(); build_sitemap()
