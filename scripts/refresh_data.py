#!/usr/bin/env python3
"""Fetch latest delayed quotes from Nasdaq and write assets/prices.json.

Why Nasdaq (not Stooq/Yahoo):
  Stooq and Yahoo's free endpoints block datacenter IPs, so they return
  404/403 from GitHub Actions runners and the weekly refresh never writes
  anything. Nasdaq's public quote API is reachable without a key from CI,
  which is what makes the scheduled refresh actually work.

Key format written to prices.json: "MCHI.US" (uppercase ticker + venue),
matching what assets/live.js expects for its cache fallback.

Failure handling (fixes the old "stuck-empty" bug):
  - Per-symbol failures are skipped, not fatal.
  - If a run fetches nothing BUT a previous good cache exists, the previous
    file is preserved (never overwrite good data with empty).
  - If a run fetches at least one price, it always writes (so an initially
    empty baseline can never freeze the file at empty forever).
"""

import json
import os
import time
import urllib.request

# US-listed China ETFs + ADRs tracked by the site.
# (ticker, Nasdaq assetclass) — ETFs use "etf", everything else "stocks".
TICKERS = [
    # ETFs
    ("MCHI", "etf"), ("FXI", "etf"), ("KWEB", "etf"),
    ("ASHR", "etf"), ("CQQQ", "etf"), ("GXC", "etf"),
    # ADRs
    ("BABA", "stocks"), ("LI", "stocks"), ("JD", "stocks"), ("BIDU", "stocks"),
    ("NTES", "stocks"), ("NIO", "stocks"), ("XPEV", "stocks"), ("TCOM", "stocks"),
    ("TME", "stocks"), ("BILI", "stocks"), ("WB", "stocks"), ("PDD", "stocks"),
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
}

HERE = os.path.abspath(os.path.dirname(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "assets", "prices.json"))


def fetch_one(symbol, assetclass):
    url = f"https://api.nasdaq.com/api/quote/{symbol}/info?assetclass={assetclass}"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as r:
        doc = json.load(r)
    primary = (doc.get("data") or {}).get("primaryData") or {}
    raw = primary.get("lastSalePrice")
    if not raw or raw in ("N/A", "-", "--", ""):
        return None
    return float(raw.replace("$", "").replace(",", "").strip())


def load_previous():
    if not os.path.exists(OUT):
        return {}, None
    try:
        with open(OUT, encoding="utf-8") as f:
            j = json.load(f)
        return (j.get("prices") or {}), j.get("updated")
    except Exception:
        return {}, None


def main():
    previous, prev_updated = load_previous()
    prices = dict(previous)  # start from last good cache
    fetched = 0

    for symbol, assetclass in TICKERS:
        key = f"{symbol}.US"
        try:
            price = fetch_one(symbol, assetclass)
            if price is not None:
                prices[key] = round(price, 4)
                fetched += 1
            else:
                print(f"  {symbol}: no price returned (kept previous if any)")
        except Exception as e:
            print(f"  {symbol}: WARN {repr(e)[:80]}")
        time.sleep(0.4)  # be polite to Nasdaq

    print(f"Fetched {fetched}/{len(TICKERS)} prices this run.")

    if fetched == 0:
        if previous:
            print("No new prices; previous cache preserved, nothing to write.")
            return
        # Nothing fetched and no previous cache -> write an empty-but-flagged file.
        data = {"updated": None, "source": "Nasdaq (delayed, key-less)", "prices": {}}
        with open(OUT, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print("Wrote empty prices.json (no data, no previous cache).")
        return

    data = {
        "updated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "source": "Nasdaq (delayed, key-less)",
        "prices": prices,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Wrote {len(prices)} prices -> {OUT}")


if __name__ == "__main__":
    main()
