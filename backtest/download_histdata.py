"""Download free 1-minute index CFD bars from histdata.com.

Instruments: SPXUSD (S&P 500) and GRXEUR (DAX). Yearly zip files for past
years, monthly files for the current year. Timestamps in the files are in
US Eastern Standard Time (UTC-5) with NO daylight-saving adjustment.
"""
import argparse
import re
import sys
import time
from pathlib import Path

import requests

BASE = "https://www.histdata.com"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) backtest-research"}
FORM_RE = re.compile(r'<input type="hidden" name="(\w+)" id="\w+" value="([^"]*)"')


def page_url(pair: str, year: int, month: int | None) -> str:
    tail = f"{year}" if month is None else f"{year}/{month}"
    return f"{BASE}/download-free-forex-historical-data/?/ascii/1-minute-bar-quotes/{pair.lower()}/{tail}"


def fetch(pair: str, year: int, month: int | None, out_dir: Path, session: requests.Session) -> Path | None:
    name = f"{pair}_{year}" + (f"_{month:02d}" if month else "") + ".zip"
    out = out_dir / name
    if out.exists() and out.stat().st_size > 1000:
        return out
    url = page_url(pair, year, month)
    r = session.get(url, headers=UA, timeout=60)
    r.raise_for_status()
    fields = dict(FORM_RE.findall(r.text))
    if "tk" not in fields:
        print(f"  no download form for {name} (not available yet?)", file=sys.stderr)
        return None
    form = {k: fields[k] for k in ("tk", "date", "datemonth", "platform", "timeframe", "fxpair")}
    rr = session.post(f"{BASE}/get.php", data=form, headers={**UA, "Referer": url}, timeout=180)
    rr.raise_for_status()
    if not rr.content.startswith(b"PK"):
        print(f"  unexpected response for {name}: {rr.content[:80]!r}", file=sys.stderr)
        return None
    out.write_bytes(rr.content)
    print(f"  {name}: {len(rr.content)/1e6:.1f} MB")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pairs", nargs="+", default=["SPXUSD", "GRXEUR"])
    ap.add_argument("--start", type=int, default=2010)
    ap.add_argument("--end-year", type=int, default=2026)
    ap.add_argument("--end-month", type=int, default=10)
    ap.add_argument("--out", default="data/raw")
    a = ap.parse_args()
    out_dir = Path(a.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    s = requests.Session()
    for pair in a.pairs:
        print(pair)
        for y in range(a.start, a.end_year):
            fetch(pair, y, None, out_dir, s)
            time.sleep(1)
        for m in range(1, a.end_month + 1):
            fetch(pair, a.end_year, m, out_dir, s)
            time.sleep(1)


if __name__ == "__main__":
    main()
