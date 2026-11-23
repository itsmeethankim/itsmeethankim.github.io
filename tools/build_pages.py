"""Writes index.html, 404.html, d/index.html and f/index.html from one template.

Run from the repo root: python3 tools/build_pages.py
Change BASE when the site moves to a custom domain (og:image must be an absolute URL).
"""
import html

BASE = "https://itsmeethankim.github.io"
APP_ID = "6838256868"
STORE = f"https://apps.apple.com/app/id{APP_ID}"

PAGES = {
    "index.html": dict(
        title="Brillion: the daily trivia dive",
        desc="Six prompts a day. Name the answer nobody else thinks of. Duel your friends on Brillion for iPhone.",
        image="og-link.png", url=BASE + "/",
        lead="Six prompts a day. Name the answer nobody else thinks of.",
    ),
    # Served with HTTP 404 for /d/CODE and /f/CODE. Apple's LinkPresentation (iMessage) ignores
    # non-2xx pages, so these tags only help scrapers that accept a 404 body.
    "404.html": dict(
        title="You've been challenged on Brillion",
        desc="A friend sent you a Brillion duel. Six trivia prompts: name the answer nobody else thinks of.",
        image="og-link.png", url=None,
        lead="Six prompts a day. Name the answer nobody else thinks of.",
    ),
    # Served with HTTP 200 for /d/?c=CODE and /d/#CODE.
    "d/index.html": dict(
        title="You've been challenged to a Brillion duel",
        desc="Same six trivia prompts, head to head. Name the answers nobody else thinks of and beat your friend.",
        image="og-duel.png", url=None,
        lead="You've been challenged to a Brillion duel.",
    ),
    "f/index.html": dict(
        title="Join me on Brillion",
        desc="Your friend wants to dive with you. Six trivia prompts a day, a friends leaderboard, and duels.",
        image="og-invite.png", url=None,
        lead="A friend wants to dive with you on Brillion.",
    ),
}

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0b1d40">
<meta name="apple-itunes-app" content="app-id={app_id}">
<meta property="og:site_name" content="Brillion">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
{og_url}<meta property="og:image" content="{base}/img/{image}">
<meta property="og:image:secure_url" content="{base}/img/{image}">
<meta property="og:image:type" content="image/png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="A pink pixel-art brain over a dark-blue ocean, with the word Brillion">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{base}/img/{image}">
<link rel="icon" type="image/png" href="/img/favicon.png">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<link rel="stylesheet" href="/assets/site.css">
</head>
<body>
<main>
  <img class="hero" src="/img/brain.png" width="256" height="224" alt="">
  <h1>BRILLION</h1>
  <div class="tag">DAILY TRIVIA DIVE</div>
  <div class="card" id="card">
    <p class="lead">{lead}</p>
  </div>
  <div class="actions">
    <a class="btn store" href="{store}"><svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2 3 7v10l9 5 9-5V7l-9-5Zm0 2.3 6.6 3.7L12 11.7 5.4 8 12 4.3ZM5 9.7l6 3.4v6.6l-6-3.4V9.7Zm8 10v-6.6l6-3.4v6.6l-6 3.4Z"/></svg><span><small>Download on the</small><b>App Store</b></span></a>
  </div>
  <img class="preview" src="/img/{image}" width="1200" height="630" alt="">
  <footer><a href="/brillion-legal/privacy.html">Privacy policy</a></footer>
</main>
<script src="/assets/link.js"></script>
</body>
</html>
"""

for path, p in PAGES.items():
    e = {k: html.escape(v, quote=True) if isinstance(v, str) else v for k, v in p.items()}
    og_url = f'<meta property="og:url" content="{e["url"]}">\n' if p["url"] else ""
    out = TEMPLATE.format(base=BASE, app_id=APP_ID, store=STORE, og_url=og_url,
                          title=e["title"], desc=e["desc"], image=e["image"], lead=e["lead"])
    with open(path, "w") as f:
        f.write(out)
    print("wrote", path)
