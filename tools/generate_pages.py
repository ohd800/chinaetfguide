# -*- coding: utf-8 -*-
"""
ChinaEquityHub — programmatic SEO page generator.
Generates:
  * guides/how-to-invest-from-<region>.html  (8 region guides)
  * stocks/<company>.html                    (20 company pages)
  * sitemap.xml                              (regenerated with everything)

Data is mirrored from assets/data.js (BROKER_RULES, COMPANIES, ADRs) so the
static output stays consistent with the live tools. Re-run after editing the
DATA block below to refresh all generated pages.

Run:  python tools/generate_pages.py   (from repo root)
"""
import os, re, json, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = "https://chinaequityhub.com"
ASOF = "August 2026"

# ----------------------------------------------------------------------------
# DATA (mirrors assets/data.js)
# ----------------------------------------------------------------------------
REGION_META = {
    "US":    {"slug": "us",             "name": "the United States",        "lead": "The US is the easiest home base for buying Chinese exposure: US brokerages already list the China ETFs and ADRs you need."},
    "EU":    {"slug": "europe",         "name": "Europe (EU/EEA)",          "lead": "EU retail investors hit one special wall: PRIIPs rules block US-domiciled ETFs, so the right China ETF is a UCITS version, not MCHI or KWEB."},
    "UK":    {"slug": "uk",             "name": "the United Kingdom",       "lead": "Post-Brexit the UK largely mirrors EU PRIIPs for retail funds, so a UCITS China ETF is the safe default — ADRs and H-shares are unaffected."},
    "CA":    {"slug": "canada",         "name": "Canada",                   "lead": "Canadian brokers with US-market access open both China ETFs and ADRs; just confirm the specific fund is offered on your platform."},
    "AU":    {"slug": "australia",      "name": "Australia",                "lead": "Australian investors can reach China through international brokers with US access, or trade China ETFs listed on the ASX in AUD to skip FX friction."},
    "SG":    {"slug": "singapore",      "name": "Singapore",                "lead": "Singapore is a regional hub: local brokers give easy HKEX and US access, and Stock Connect makes A-shares reachable too."},
    "HK":    {"slug": "hongkong",       "name": "Hong Kong",                "lead": "Hong Kong is the gateway itself — direct HKEX access and Stock Connect Northbound make every channel (H-shares, A-shares, ADRs) straightforward."},
    "OTHER": {"slug": "other-countries","name": "other countries",          "lead": "For most of the rest of the world, a global broker with US and HK market access covers China ETFs, ADRs and H-shares; check local rules with an adviser."},
}

TARGETS = [
    ("etf",    "China ETFs",            "US-listed: MCHI, FXI, KWEB, ASHR, GXC"),
    ("adr",    "China ADRs",            "US-listed: BABA, JD, PDD, NIO…"),
    ("hshare", "H-shares",              "HK-listed Chinese stocks, e.g. 9988.HK"),
    ("ashare", "A-shares",              "Mainland China stocks"),
]

STATUS_LABEL = {
    "ok":      "Generally accessible",
    "warn":    "Restricted — read notes",
    "limited": "Harder — indirect route",
}

# BROKER_RULES mirrored from assets/data.js (path may contain <b> HTML — trusted)
BROKER_RULES = {
    "etf": {
        "US":    ("ok", "US-listed China ETFs are available through <b>any US brokerage</b>. They are US-domiciled funds, so there is no PRIIPs/KIID obstacle.", ["Schwab","Fidelity","Vanguard","Robinhood","Interactive Brokers"]),
        "EU":    ("warn", "<b>US-domiciled ETFs (MCHI, FXI, KWEB, ASHR, GXC) generally cannot be sold to EU retail</b> under PRIIPs/KIID rules. Use a <b>UCITS</b> China ETF instead (EU-domiciled, KIID-compliant).", ["iShares MSCI China UCITS","Xtrackers CSI 300 UCITS","Interactive Brokers / Saxo / DEGIRO / Trade Republic"]),
        "UK":    ("warn", "Post-Brexit the UK mirrors much of PRIIPs; a <b>UCITS</b> China ETF is the safe route for retail. Some platforms allow US ETFs via specific arrangements — confirm first.", ["iShares MSCI China UCITS","Interactive Brokers / Saxo / Hargreaves Lansdown"]),
        "CA":    ("ok", "Accessible via Canadian brokers with US-market access. Confirm the specific fund is offered (availability varies by platform).", ["Interactive Brokers","Questrade","Wealthsimple","RBC Direct Investing"]),
        "AU":    ("ok", "Via international brokers with US access, or trade <b>ASX-listed</b> China ETFs in AUD to avoid FX/custody friction.", ["Interactive Brokers","Stake","CommSec International","IZZ (iShares China, ASX)"]),
        "SG":    ("ok", "Via local brokers with US access, or SGX-listed China ETFs.", ["Interactive Brokers","POEMS","Tiger","Moomoo"]),
        "HK":    ("ok", "Via US-market access platforms, or buy HKEX-listed China ETFs directly.", ["Interactive Brokers","Futu","Tiger","HKEX-listed China ETFs"]),
        "OTHER": ("ok", "Use a global broker with US-market access. Local rules vary — confirm with a local advisor.", ["Interactive Brokers (most universal)"]),
    },
    "adr": {
        "US":    ("ok", "Any US brokerage. Watch <b>HFCAA delisting &amp; VIE</b> risk — check the name in the ADR Risk Checker.", ["Schwab","Fidelity","Interactive Brokers","Robinhood"]),
        "EU":    ("ok", "Buyable via brokers with US-stock access. ADRs are <b>stocks, not funds</b>, so PRIIPs/KIID does not block them — but HFCAA/VIE risk still applies (see ADR Risk Checker).", ["Interactive Brokers","Saxo","DEGIRO"]),
        "UK":    ("ok", "Via brokers with US-stock access. PRIIPs does not apply to single stocks; mind HFCAA/VIE risk.", ["Interactive Brokers","Saxo","Hargreaves Lansdown"]),
        "CA":    ("ok", "Via Canadian brokers with US-stock access.", ["Interactive Brokers","Questrade","Wealthsimple"]),
        "AU":    ("ok", "Via international brokers with US-stock access.", ["Interactive Brokers","Stake","CommSec International"]),
        "SG":    ("ok", "Via local brokers with US-stock access.", ["Interactive Brokers","POEMS","Tiger","Moomoo"]),
        "HK":    ("ok", "Via US-market access platforms.", ["Interactive Brokers","Futu","Tiger"]),
        "OTHER": ("ok", "Use a global broker with US-stock access. Confirm local rules with an advisor.", ["Interactive Brokers"]),
    },
    "hshare": {
        "US":    ("ok", "Via an international broker that offers the Hong Kong market (e.g. buy the H-share directly as 9988.HK).", ["Interactive Brokers","Saxo"]),
        "EU":    ("ok", "Via an international broker with HK market access, or buy a UCITS China ETF that holds H-shares.", ["Interactive Brokers","Saxo","UCITS China ETFs"]),
        "UK":    ("ok", "Via an international broker with HK market access.", ["Interactive Brokers","Saxo"]),
        "CA":    ("ok", "Via a broker with HK market access (Interactive Brokers is the most common).", ["Interactive Brokers"]),
        "AU":    ("ok", "Via a broker with HK access, or ASX/SGX-listed China products.", ["Interactive Brokers","Stake","CommSec International"]),
        "SG":    ("ok", "Direct HKEX access is easy from Singapore via local brokers.", ["Interactive Brokers","POEMS","Tiger","Moomoo"]),
        "HK":    ("ok", "Direct HKEX access via any local broker — the simplest route of all.", ["Futu","Tiger","HSBC","Standard Chartered","Interactive Brokers"]),
        "OTHER": ("ok", "Use a global broker with HK market access. Confirm local rules with an advisor.", ["Interactive Brokers","Saxo"]),
    },
    "ashare": {
        "US":    ("limited", "Most retail foreigners <b>cannot open a direct A-share account</b>. The easiest route is an <b>A-share ETF listed in the US</b> — <b>ASHR</b> (Xtrackers Harvest CSI 300) tracks the CSI 300. Broader China ETFs (MCHI/FXI) also hold some A-shares via Stock Connect.", ["ASHR (US-listed)","MCHI / FXI (partial A-share via Connect)","Interactive Brokers (ChinaConnect, eligible clients)"]),
        "EU":    ("limited", "ASHR is a US ETF → PRIIPs blocks it for EU retail. Use a <b>UCITS</b> China A-share fund instead.", ["Xtrackers CSI 300 UCITS","Lyxor / Amundi MSCI China A UCITS","Interactive Brokers / Saxo"]),
        "UK":    ("limited", "Prefer a <b>UCITS</b> China A-share fund for retail. Direct A-share access via Stock Connect is limited to qualifying brokers.", ["Xtrackers CSI 300 UCITS","Interactive Brokers (eligible)"]),
        "CA":    ("limited", "Reach A-shares via an A-share ETF (ASHR in the US, or a local UCITS equivalent) or Stock Connect through a qualifying broker.", ["ASHR (via US access)","Interactive Brokers (ChinaConnect)"]),
        "AU":    ("limited", "Via an A-share ETF or Stock Connect through a qualifying international broker.", ["ASHR (via US access)","Interactive Brokers (ChinaConnect)"]),
        "SG":    ("limited", "Singapore is a Stock Connect hub — some brokers offer A-share access; otherwise use an A-share ETF.", ["Interactive Brokers (ChinaConnect)","POEMS (eligible)","A-share ETFs"]),
        "HK":    ("ok", "Hong Kong is the gateway: <b>Stock Connect</b> (Northbound) lets eligible HK accounts trade mainland A-shares directly.", ["Interactive Brokers (ChinaConnect)","Futu","Tiger","via Stock Connect"]),
        "OTHER": ("limited", "For most foreign retail, A-share exposure is best reached <b>indirectly through a broad China ETF</b> rather than individual mainland stocks. Direct access needs Stock Connect / QFII via a qualifying broker.", ["Broad China ETF (MCHI/FXI/UCITS)","Interactive Brokers (eligible)"]),
    },
}

# ADR risk tier (mirrors data.js ADRs)
ADR_RISK = {
    "BABA": "Low", "LI": "Low",
    "JD": "Medium", "BIDU": "Medium", "NTES": "Medium", "NIO": "Medium",
    "XPEV": "Medium", "TCOM": "Medium", "TME": "Medium", "BILI": "Medium",
    "WB": "Medium", "PDD": "High",
}

COMPANIES = [
    {"name":"Tencent","sector":"Internet & gaming","a":None,"h":"0700.HK","adr":None,"note":"Listed in Hong Kong only. No A-share or US ADR. Buy via the H-share (HKEX)."},
    {"name":"Alibaba","sector":"E-commerce & cloud","a":None,"h":"9988.HK","adr":"BABA","note":"Dual-primary listed in Hong Kong and New York. If US delisting ever happened, shares convert to HK (9988)."},
    {"name":"JD.com","sector":"E-commerce","a":None,"h":"9618.HK","adr":"JD","note":"Secondary HK listing alongside the US ADR. Conversion to HK is possible."},
    {"name":"Baidu","sector":"Search & AI","a":None,"h":"9888.HK","adr":"BIDU","note":"Secondary HK listing alongside the US ADR. Conversion to HK is possible."},
    {"name":"NIO","sector":"Electric vehicles","a":None,"h":"9866.HK","adr":"NIO","note":"Secondary HK listing alongside the US ADR. Conversion to HK is possible."},
    {"name":"XPeng","sector":"Electric vehicles","a":None,"h":"9868.HK","adr":"XPEV","note":"Secondary HK listing alongside the US ADR. Conversion to HK is possible."},
    {"name":"Li Auto","sector":"Electric vehicles","a":None,"h":"2015.HK","adr":"LI","note":"Dual-primary listed in Hong Kong and New York — strongest HK safety net of the EV trio."},
    {"name":"PDD Holdings","sector":"E-commerce (Temu)","a":None,"h":None,"adr":"PDD","note":"US-listed ONLY. No Hong Kong listing — the highest delisting-exposure ADR of the group. See the ADR risk tool."},
    {"name":"Meituan","sector":"Food delivery & local services","a":None,"h":"3690.HK","adr":None,"note":"Listed in Hong Kong only. No A-share or US ADR. Buy via the H-share."},
    {"name":"NetEase","sector":"Games & media","a":None,"h":"9999.HK","adr":"NTES","note":"Secondary HK listing alongside the US ADR. Conversion to HK is possible."},
    {"name":"Trip.com","sector":"Online travel","a":None,"h":"9961.HK","adr":"TCOM","note":"Secondary HK listing alongside the US ADR. Conversion to HK is possible."},
    {"name":"Bilibili","sector":"Video & community","a":None,"h":"9626.HK","adr":"BILI","note":"Secondary HK listing alongside the US ADR. Conversion to HK is possible."},
    {"name":"Weibo","sector":"Social media","a":None,"h":"9898.HK","adr":"WB","note":"Secondary HK listing alongside the US ADR. Conversion to HK is possible."},
    {"name":"BYD","sector":"Electric vehicles & batteries","a":"002594.SZ","h":"1211.HK","adr":None,"note":"Rare double listing: mainland A-share (Shenzhen) AND Hong Kong H-share. No US ADR currently. Foreigners usually reach it via the H-share."},
    {"name":"Kweichow Moutai","sector":"Premium liquor","a":"600519.SH","h":None,"adr":None,"note":"Mainland A-share only (Shanghai). No HK or US listing — hardest for foreigners to access directly; usually reached via an A-share ETF."},
    {"name":"ICBC","sector":"Banking","a":"601398.SH","h":"1398.HK","adr":None,"note":"Both A-share (Shanghai) and H-share (Hong Kong). Foreigners typically use the H-share."},
    {"name":"China Mobile","sector":"Telecom","a":"600941.SH","h":"0941.HK","adr":None,"note":"Both A-share and H-share. Its US ADR was delisted in 2021; the H-share is the foreigner-friendly route."},
    {"name":"CNOOC","sector":"Oil & gas","a":"600938.SH","h":"0883.HK","adr":None,"note":"Both A-share and H-share. US ADR was delisted; use the H-share."},
    {"name":"Ping An","sector":"Insurance & finance","a":"601318.SH","h":"2318.HK","adr":None,"note":"Both A-share (Shanghai) and H-share (Hong Kong). Foreigners usually use the H-share."},
    {"name":"China Construction Bank","sector":"Banking","a":"601939.SH","h":"0939.HK","adr":None,"note":"Both A-share and H-share. Foreigners typically use the H-share."},
]

# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def slugify(s):
    s = re.sub(r'\(.*?\)', '', s).strip().lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')

def esc(t):
    return html.escape(str(t))

def header(active, subfolder):
    p = "../" if subfolder else ""
    return f'''<header>
  <div class="wrap nav">
    <a class="brand" href="{p}index.html" style="display:flex;align-items:center;gap:10px;color:inherit">
      <div class="logo">中</div>
      <div>ChinaEquityHub<small>PLAIN-ENGLISH CHINA EQUITY TOOLS</small></div>
    </a>
    <nav class="navlinks">
      <a href="{p}index.html">Home</a>
      <a href="{p}etf.html">ETF</a>
      <a href="{p}adr.html">ADR Risk</a>
      <a href="{p}broker.html">Broker</a>
      <a href="{p}symbols.html">Ticker</a>
      <a href="{p}guides/index.html">Guides</a>
      <a href="{p}learn.html">Market 101</a>
    </nav>
  </div>
</header>'''

EXTRA_STYLE = '''<style>
.acctable{width:100%;border-collapse:collapse;margin:18px 0;font-size:14px}
.acctable th,.acctable td{border:1px solid var(--line);padding:10px 12px;text-align:left;vertical-align:top}
.acctable th{background:var(--line);font-size:13px}
.bstatus{display:inline-block;font-size:12.5px;font-weight:700;padding:3px 9px;border-radius:20px;margin-bottom:8px}
.bstatus.ok{background:#e3f6ec;color:#0a7a43}
.bstatus.warn{background:#fdf0d8;color:#9a6b00}
.bstatus.limited{background:#fbe6e6;color:#a3262b}
.codetable{width:100%;border-collapse:collapse;margin:16px 0;font-size:14px}
.codetable th,.codetable td{border:1px solid var(--line);padding:10px 12px;text-align:left}
.codetable th{background:var(--line);font-size:13px}
.codebig{font-size:18px;font-weight:800;color:var(--brand)}
.na{color:var(--muted)}
.cta{margin-top:14px}
.cta a{display:inline-block;margin:4px 8px 4px 0;color:var(--accent);font-weight:700;font-size:13.5px}
</style>'''

def footer(subfolder):
    return '''<footer>
  <div class="wrap">
    ChinaEquityHub — a plain-English tool for foreign investors exploring Chinese equities. Built as a research prototype. Not affiliated with any issuer, broker, or exchange.
  </div>
</footer>'''

def breadcrumb_json(chain):
    items = [{"@type":"ListItem","position":i+1,"name":n,"item":u} for i,(n,u) in enumerate(chain)]
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":items}

# ----------------------------------------------------------------------------
# Region guide page
# ----------------------------------------------------------------------------
def build_region_page(rk):
    meta = REGION_META[rk]
    slug = meta["slug"]
    fname = f"how-to-invest-from-{slug}.html"
    url = f"{DOMAIN}/guides/{fname}"
    title = f"How to Buy Chinese Stocks from {meta['name'].title()} — Step-by-Step Guide"
    desc = f"Can you buy Chinese stocks from {meta['name']}? Yes — here are the realistic routes for ETFs, ADRs, H-shares and A-shares, plus example brokers for {meta['name']}."
    kw = f"buy Chinese stocks from {meta['name']}, invest in China from {meta['name']}, China stocks broker {meta['name']}"

    # access table rows
    rows = []
    for tk, tlabel, tsub in TARGETS:
        lvl, path, examples = BROKER_RULES[tk][rk]
        cta = {
            "etf": ("Compare China ETFs", "../etf.html"),
            "adr": ("Check ADR delisting risk", "../adr.html"),
            "hshare": ("Look up H-share codes", "../symbols.html"),
            "ashare": ("What is an A-share?", "../learn.html"),
        }[tk]
        rows.append(f'''<tr>
  <td><b>{tlabel}</b><br><span class="na">{tsub}</span></td>
  <td><span class="bstatus {lvl}">{STATUS_LABEL[lvl]}</span></td>
  <td>{path}</td>
  <td>{esc(', '.join(examples))}</td>
  <td><a href="{cta[1]}">{cta[0]} →</a></td>
</tr>''')
    table = ("<table class='acctable'><thead><tr><th>What you want</th><th>Status</th>"
             "<th>How it works from "+esc(meta['name'])+"</th><th>Example platforms</th><th>Tool</th></tr></thead><tbody>"
             + "".join(rows) + "</tbody></table>")

    faq = [
        ("Can I buy Chinese stocks from " + meta['name'] + "?",
         "Yes. The exact route depends on what you want to buy. Use the table above: China ETFs and ADRs are usually reachable through an international or local broker, H-shares need HK market access, and A-shares are the hardest for retail (best reached via an A-share ETF)."),
        ("What is the easiest China exposure for someone in " + meta['name'] + "?",
         "For most beginners, a single broad China ETF is the simplest start — one position gives diversified exposure without picking individual stocks. US residents can use US-listed ETFs (MCHI, FXI, KWEB); EU/UK retail should use a UCITS China ETF instead."),
        ("Do I need a Chinese brokerage account?",
         "No. Almost all foreign retail gets China exposure through US-listed ETFs/ADRs, HK-listed H-shares via an international broker, or UCITS funds on a local exchange. A direct mainland (A-share) account is rarely needed and is restricted for retail foreigners."),
        ("Is this financial advice?",
         "No. This guide is educational only. Confirm access, taxes, PRIIPs/UCITS rules and eligibility with a licensed broker or adviser in your jurisdiction."),
    ]
    faq_html = "<div class='faq'>" + "".join(
        f"<details><summary>{esc(q)}</summary><p>{a}</p></details>" for q,a in faq) + "</div>"
    faq_json = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]}

    crumbs = breadcrumb_json([
        ("Home", f"{DOMAIN}/"),
        ("Guides", f"{DOMAIN}/guides/"),
        ("How to invest from "+meta['name'], url),
    ])

    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}" />
<meta name="keywords" content="{esc(kw)}" />
<meta name="robots" content="index, follow" />
<link rel="canonical" href="{url}" />
<meta property="og:type" content="article" />
<meta property="og:title" content="{esc(title)}" />
<meta property="og:description" content="{esc(desc)}" />
<meta property="og:url" content="{url}" />
<meta property="og:image" content="{DOMAIN}/assets/og.png" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{esc(title)}" />
<meta name="twitter:description" content="{esc(desc)}" />
<link rel="stylesheet" href="../assets/styles.css" />
{EXTRA_STYLE}
<script type="application/ld+json">{json.dumps(crumbs)}</script>
<script type="application/ld+json">{json.dumps(faq_json)}</script>
</head>
<body>
{header('guides', True)}
<div class="wrap">
  <div class="hero">
    <h1>How to Buy Chinese Stocks from {esc(meta['name'].title())}</h1>
    <p>{esc(meta['lead'])} Below is the realistic access map for someone in {esc(meta['name'])} — ETFs, ADRs, H-shares and A-shares — with example platforms.</p>
  </div>

  <section>
    <h2 class="sec-title">Your 4 ways to get China exposure</h2>
    <p class="sec-sub">Pick what you want to own. Status reflects a typical retail investor in {esc(meta['name'])}.</p>
    {table}
    <p class="note">Platform examples are illustrative, not endorsements. Availability of specific China products depends on your account residency and local regulation. <b>Not financial advice.</b></p>
  </section>

  <section style="margin-top:28px">
    <h2 class="sec-title">Recommended starting point</h2>
    <p>If you are new, start with one diversified China ETF rather than individual stocks — it avoids single-company and delisting risk. Then explore ADRs or H-shares once you are comfortable.</p>
    <div class="cta">
      <a href="../etf.html">Compare China ETFs →</a>
      <a href="../broker.html">Open the Broker Finder →</a>
      <a href="../adr.html">Check ADR delisting risk →</a>
      <a href="../learn.html">China Market 101 →</a>
    </div>
  </section>

  <section class="wrap" style="margin-top:28px">
    <h2 class="sec-title">Common questions</h2>
    {faq_html}
  </section>

  <section class="disc" style="margin-top:24px">
    <b>Disclaimer:</b> Educational only, <b>not financial advice</b>. Access rules (especially EU/UK PRIIPs limits on US-domiciled ETFs, and Stock Connect eligibility) change and depend on your residency and account type. Confirm current access and tax treatment with a licensed broker or adviser in your jurisdiction. Data snapshot: {ASOF}.
  </section>
</div>
{footer(True)}
<script src="../assets/feedback.js"></script>
</body>
</html>'''
    return fname, page, url

# ----------------------------------------------------------------------------
# Company page
# ----------------------------------------------------------------------------
def where_to_buy(c):
    a,h,adr = c["a"],c["h"],c["adr"]
    if adr and h:
        return (f"You can reach {c['name']} two ways from outside China: the US-listed ADR <b>{adr}</b> through any normal US brokerage, "
                f"or the Hong Kong H-share <b>{h}</b> through an international broker with HK access. Because it is dual-listed, an ADR holder has a clear "
                f"landing spot in Hong Kong if the US line were ever delisted.")
    if adr and not h:
        return (f"The realistic way for a foreigner to own {c['name']} is the US-listed ADR <b>{adr}</b>, since there is no Hong Kong listing. "
                f"Note: {c['name']} carries the higher delisting exposure among major ADRs — check the ADR risk tool before sizing a position.")
    if h and not adr:
        return (f"{c['name']} trades only in Hong Kong, as the H-share <b>{h}</b>. Buy it through an international broker that offers the HK market "
                f"(Interactive Brokers, Saxo, and many local platforms).")
    if a and h:
        return (f"{c['name']} has both a mainland A-share <b>{a}</b> and a Hong Kong H-share <b>{h}</b>. Foreign retail usually reaches it through the H-share via an "
                f"international broker, because direct A-share accounts are hard to open. An A-share ETF (e.g. ASHR) is an indirect route.")
    if a and not h and not adr:
        return (f"{c['name']} is a mainland A-share only (<b>{a}</b>) — the hardest for a foreigner to buy directly. Most people get exposure indirectly through an "
                f"A-share ETF like ASHR or a broad China fund that holds it via Stock Connect.")
    return c["note"]

def build_company_page(c):
    slug = slugify(c["name"])
    fname = f"{slug}.html"
    url = f"{DOMAIN}/stocks/{fname}"
    title = f"{c['name']} Stock — Ticker, Price & How to Buy from Abroad"
    desc = (f"{c['name']} ({c['sector']}): find its A-share, H-share and US ADR tickers, and see how a foreign investor can actually buy it. "
            f"Codes: " + " / ".join([x for x in [c['a'], c['h'], c['adr']] if x]) + ".")
    kw = f"{c['name']} stock ticker, buy {c['name']} stock, {c['name']} ADR, how to invest in {c['name']}"

    def code_cell(label, code):
        if not code:
            return f"<td><span class='na'>— not listed</span></td>"
        link = f"<a href='../broker.html'>{esc(code)}</a>"
        return f"<td><span class='codebig'>{link}</span><br><span class='na'>{label}</span></td>"

    codetable = ("<table class='codetable'><thead><tr><th>A-share (mainland)</th><th>H-share (Hong Kong)</th><th>US ADR (New York)</th></tr></thead><tbody><tr>"
                 + code_cell("Shanghai / Shenzhen", c["a"])
                 + code_cell("HKEX", c["h"])
                 + code_cell("NYSE / NASDAQ", c["adr"])
                 + "</tr></tbody></table>")

    wtb = where_to_buy(c)

    # ADR risk line
    adr_risk_html = ""
    if c["adr"] and c["adr"] in ADR_RISK:
        tier = ADR_RISK[c["adr"]]
        adr_risk_html = (f"<p><b>ADR delisting risk:</b> {c['name']}'s US line <b>{c['adr']}</b> is rated <b>{tier}</b> in our model "
                         f"(the dominant mitigant is its Hong Kong listing status). See the <a href='../adr.html'>ADR Risk Checker</a> for the full breakdown.</p>")

    faq = [
        (f"What is {c['name']}'s stock ticker?",
         "It depends on the market: " + " / ".join([x for x in [c['a'], c['h'], c['adr']] if x]) + f". {c['name']} trades across " + ("the mainland A-share, Hong Kong H-share and US ADR markets." if (c['a'] and c['h'] and c['adr']) else "multiple markets as listed above.")),
        (f"How do I buy {c['name']} stock from outside China?",
         wtb),
        (f"Is {c['name']} available as an ADR?" if c['adr'] else f"Why is there no {c['name']} ADR?",
         (f"Yes — it trades on US exchanges as <b>{c['adr']}</b>, buyable through any US brokerage (mind HFCAA/VIE risk)." if c['adr']
          else f"{c['name']} has no US-listed ADR. Foreigners reach it via its " + ("H-share" if c['h'] else "A-share / an A-share ETF") + " instead.")),
    ]
    faq_html = "<div class='faq'>" + "".join(
        f"<details><summary>{esc(q)}</summary><p>{a}</p></details>" for q,a in faq) + "</div>"
    faq_json = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":re.sub('<[^>]+>','',a)}} for q,a in faq]}

    crumbs = breadcrumb_json([
        ("Home", f"{DOMAIN}/"),
        ("China Ticker Lookup", f"{DOMAIN}/symbols.html"),
        (c['name'], url),
    ])

    # related tools
    related = []
    if c["adr"]: related.append(("<a href='../adr.html'>Check "+esc(c['adr'])+" delisting risk →</a>"))
    related.append("<a href='../broker.html'>How to buy →</a>")
    if c["a"]: related.append("<a href='../learn.html'>What is an A-share? →</a>")
    related.append("<a href='../etf.html'>Compare China ETFs →</a>")

    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}" />
<meta name="keywords" content="{esc(kw)}" />
<meta name="robots" content="index, follow" />
<link rel="canonical" href="{url}" />
<meta property="og:type" content="article" />
<meta property="og:title" content="{esc(title)}" />
<meta property="og:description" content="{esc(desc)}" />
<meta property="og:url" content="{url}" />
<meta property="og:image" content="{DOMAIN}/assets/og.png" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{esc(title)}" />
<meta name="twitter:description" content="{esc(desc)}" />
<link rel="stylesheet" href="../assets/styles.css" />
{EXTRA_STYLE}
<script type="application/ld+json">{json.dumps(crumbs)}</script>
<script type="application/ld+json">{json.dumps(faq_json)}</script>
</head>
<body>
{header('symbols', True)}
<div class="wrap">
  <div class="hero">
    <h1>{esc(c['name'])} Stock — Ticker &amp; How to Buy</h1>
    <p>{esc(c['sector'])}. One company, up to three tickers across different markets. Here are all of them, and how a foreign investor can actually own it.</p>
  </div>

  <section>
    <h2 class="sec-title">{esc(c['name'])} — all tickers at a glance</h2>
    {codetable}
    <div class="cta">{"".join(related)}</div>
  </section>

  <section style="margin-top:26px">
    <h2 class="sec-title">Where can a foreigner buy {esc(c['name'])}?</h2>
    <p>{wtb}</p>
    {adr_risk_html}
    <p class="note">{esc(c['note'])}</p>
  </section>

  <section class="wrap" style="margin-top:26px">
    <h2 class="sec-title">Common questions</h2>
    {faq_html}
  </section>

  <section class="disc" style="margin-top:24px">
    <b>Disclaimer:</b> Educational only, <b>not financial advice</b>. Tickers and listing status are verified snapshots as of {ASOF} and can change (companies add or switch listings). Always confirm the current ticker with your broker or the exchange before trading.
  </section>

  <section class="back" style="margin-top:14px">
    <a href="../symbols.html">← Back to China Ticker Lookup</a> · <a href="../guides/index.html">All guides →</a>
  </section>
</div>
{footer(True)}
<script src="../assets/feedback.js"></script>
</body>
</html>'''
    return fname, page, url

# ----------------------------------------------------------------------------
# Sitemap
# ----------------------------------------------------------------------------
def build_sitemap(region_urls, company_urls):
    base = [
        ("/", "1.0"),
        ("/etf.html", "0.9"),
        ("/adr.html", "0.9"),
        ("/broker.html", "0.9"),
        ("/symbols.html", "0.9"),
        ("/learn.html", "0.8"),
        ("/guides/index.html", "0.8"),
        ("/guides/how-to-invest.html", "0.8"),
        ("/guides/a-shares-vs-h-shares.html", "0.8"),
        ("/guides/adr-delisting-explained.html", "0.8"),
        ("/guides/best-china-etf.html", "0.8"),
    ]
    urls = [f"  <url><loc>{DOMAIN}{u}</loc><lastmod>{ASOF[:7]}-01</lastmod><changefreq>monthly</changefreq><priority>{p}</priority></url>" for u,p in base]
    urls += [f"  <url><loc>{u}</loc><lastmod>{ASOF[:7]}-01</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>" for u in region_urls]
    urls += [f"  <url><loc>{u}</loc><lastmod>{ASOF[:7]}-01</lastmod><changefreq>monthly</changefreq><priority>0.6</priority></url>" for u in company_urls]
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(urls) + "\n</urlset>\n")

# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------
def main():
    guides_dir = os.path.join(ROOT, "guides")
    stocks_dir = os.path.join(ROOT, "stocks")
    os.makedirs(guides_dir, exist_ok=True)
    os.makedirs(stocks_dir, exist_ok=True)

    region_urls = []
    for rk in REGION_META:
        fname, page, url = build_region_page(rk)
        with open(os.path.join(guides_dir, fname), "w", encoding="utf-8") as f:
            f.write(page)
        region_urls.append(url)
        print("region:", fname)

    company_urls = []
    for c in COMPANIES:
        fname, page, url = build_company_page(c)
        with open(os.path.join(stocks_dir, fname), "w", encoding="utf-8") as f:
            f.write(page)
        company_urls.append(url)
        print("company:", fname)

    sm = build_sitemap(region_urls, company_urls)
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sm)
    print("sitemap.xml:", len(region_urls)+len(company_urls)+11, "URLs")

if __name__ == "__main__":
    main()
