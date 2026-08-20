#!/usr/bin/env python3
"""Fetch latest delayed quotes from Stooq and write assets/prices.json.

Run by the scheduled GitHub Action so the site's price snapshot stays fresh
without a paid API key. On failure it preserves the previous file (never
overwrites good data with an empty result)."""

import csv
import io
import json
import os
import urllib.request
import datetime

# US-listed China ETFs + ADRs tracked by the site.
TICKERS = [
    # ETFs
    "MCHI", "FXI", "KWEB", "ASHR", "CQQQ", "GXC",
    # ADRs
    "BABA", "LI", "JD", "BIDU", "NTES", "NIO", "XPEV",
    "TCOM", "TME", "BILI", "WB", "PDD",
]
VENUE = "us"

HERE = os.path.abspath(os.path.dirname(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "assets", "prices.json"))


def fetch_csv():
    syms = "+".join(f"{t.lower()}.{VENUE}" for t in TICKERS)
    url = f"https://stooq.com/q/l/?s={syms}&f=sd2t2ohlcv&h&e=csv"
    req = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0 (compatible; ChinaETFGuideBot/1.0)"}
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def parse_prices(txt):
    prices = {}
    reader = csv.reader(io.StringIO(txt))
    rows = list(reader)
    for row in rows[1:]:
        if len(row) < 7:
            continue
        sym = row[0].strip().upper()  # e.g. MCHI.US
        try:
            close = float(row[6])
        except ValueError:
            continue
        if close:
            prices[sym] = round(close, 4)
    return prices


def main():
    try:
        txt = fetch_csv()
        prices = parse_prices(txt)
    except Exception as e:
        print("FETCH FAILED:", e)
        if os.path.exists(OUT):
            print("Keeping previous prices.json (no overwrite with empty data).")
            return
        prices = {}

    if not prices:
        if os.path.exists(OUT):
            print("No prices parsed; keeping previous file.")
            return
        prices = {}

    data = {
        "updated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "Stooq (delayed, key-less)",
        "prices": prices,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Wrote {len(prices)} prices -> {OUT}")


if __name__ == "__main__":
    main()
