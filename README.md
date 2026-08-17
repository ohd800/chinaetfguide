# ChinaEquityHub

Plain-English tools for foreign investors exploring Chinese equities
(ETF comparator · ADR delisting-risk checker · broker/access finder ·
China ticker lookup · Market 101 guides).

Static site — no build step, no backend. Pure HTML/CSS/JS.

## Pages
- `index.html` — portal / home
- `etf.html` — China ETF comparator
- `adr.html` — China ADR delisting-risk checker
- `broker.html` — Broker / access finder
- `symbols.html` — China ticker lookup (A-share / H-share / ADR)
- `learn.html` — China Market 101
- `guides/` — long-tail SEO guide cluster
- `assets/` — shared CSS / JS data + logic
- `sitemap.xml`, `robots.txt` — SEO

## Local preview
```bash
cd stock-web
python -m http.server 8099
# open http://127.0.0.1:8099/
```

## Deploy (GitHub + Vercel) — step by step
1. Create an empty repo on GitHub (e.g. `chinaequityhub`).
2. Push this folder:
   ```bash
   git remote add origin https://github.com/<you>/chinaequityhub.git
   git branch -M main
   git push -u origin main
   ```
3. In Vercel: **Add New → Project → Import Git Repository** → pick the repo.
   - Framework preset: **Other**
   - Build command: leave empty
   - Output directory: `.` (root)
   - Deploy.
4. Vercel gives you `https://chinaequityhub.vercel.app`.

## After deploy — required edits
The site currently uses the brand placeholder `https://chinaequityhub.com`
in `canonical`, `og:url` (6 pages) and `sitemap.xml`. Replace it with your
real domain (Vercel subdomain, or a custom domain once connected):
- 6 × `<link rel="canonical" ...>` + `<meta property="og:url" ...>`
- `sitemap.xml` → all 11 `<loc>` URLs
(Use search-and-replace across the repo; then re-commit & redeploy.)

## Analytics (optional)
`index.html` has a commented GA4 snippet. Replace `G-XXXXXXX` with your
GA4 Measurement ID to start collecting traffic data.

## Notes
- Feedback is collected via `mailto:` to the site owner (see `assets/feedback.js`,
  `EMAIL` constant). Swap to Formspree later if desired.
- Live quotes are best-effort (Stooq public CSV, CORS-fallible) and gracefully
  fall back to verified snapshots. See `assets/live.js`.
- Not financial advice.
