"""Load HistData 1-minute bars into a tz-aware DataFrame, cached as pickle.

HistData's index CFD files are stamped in New York local time (DST-aware);
verified empirically: the cash-open volatility spike sits at 09:30 (S&P) and
03:00 (DAX = 09:00 Berlin) in both winter and summer.
"""
import io
import zipfile
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
CACHE = ROOT / "data" / "cache"

INSTRUMENTS = {
    "SPXUSD": dict(name="S&P 500", tz="America/New_York", open="09:30", close="16:00"),
    "GRXEUR": dict(name="DAX", tz="Europe/Berlin", open="09:00", close="17:30"),
}


def _read_zip(path: Path) -> pd.DataFrame:
    z = zipfile.ZipFile(path)
    csv = [n for n in z.namelist() if n.endswith(".csv")][0]
    df = pd.read_csv(io.BytesIO(z.read(csv)), sep=";", header=None,
                     names=["ts", "open", "high", "low", "close", "vol"], usecols=range(5))
    df["ts"] = pd.to_datetime(df["ts"], format="%Y%m%d %H%M%S")
    return df


def load(pair: str, refresh: bool = False) -> pd.DataFrame:
    """Return OHLC bars indexed by tz-aware timestamp in the instrument's local tz."""
    cache = CACHE / f"{pair}.pkl"
    if cache.exists() and not refresh:
        return pd.read_pickle(cache)
    files = sorted(RAW.glob(f"{pair}_*.zip"))
    if not files:
        raise FileNotFoundError(f"no raw files for {pair}; run download_histdata.py")
    df = pd.concat([_read_zip(f) for f in files], ignore_index=True)
    df = df.drop_duplicates("ts").sort_values("ts").set_index("ts")
    idx = df.index.tz_localize("America/New_York", ambiguous="NaT", nonexistent="NaT")
    df.index = idx
    df = df[df.index.notna()]
    df.index = df.index.tz_convert(INSTRUMENTS[pair]["tz"])
    df.index.name = "ts"
    # sanity: drop bars with non-positive prices or inverted high/low
    df = df[(df.low > 0) & (df.high >= df.low)]
    CACHE.mkdir(parents=True, exist_ok=True)
    df.to_pickle(cache)
    return df


if __name__ == "__main__":
    for p in INSTRUMENTS:
        d = load(p, refresh=True)
        print(p, len(d), d.index.min(), d.index.max())
