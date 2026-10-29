"""Opening-range breakout (ORB) simulator on 1-minute bars.

Rules (generic, deliberately simple):
  * Opening range = first `or_minutes` of the cash session.
  * entry="breakout": first 1-min bar that CLOSES above the range high -> long,
    below the range low -> short (one trade per day, no re-entry).
  * entry="candle": at the end of the opening range, go in the direction of the
    opening-range candle (close vs open) -- "look at the first candle and trade".
  * Stop: opposite side of the range ("range") or the range midpoint ("half").
  * Exit: take-profit at `target_r` times the initial risk, else market-on-close.
    If a bar touches both stop and target, the stop is assumed to fill first.
  * Gaps through the stop fill at the bar open (worse than the stop level).
  * Costs: a round-trip cost in index points is subtracted from every trade.
    It is applied after simulation so one path serves several cost levels.
"""
from dataclasses import dataclass
from datetime import timedelta

import numpy as np
import pandas as pd

from data import INSTRUMENTS


@dataclass(frozen=True)
class Params:
    or_minutes: int = 15
    entry: str = "breakout"          # breakout | candle
    stop: str = "range"              # range | half
    target_r: float | None = None    # take profit in R multiples; None = hold to close
    last_entry_minute: int | None = None  # no entries after this many minutes past open

    def label(self) -> str:
        tp = "close" if self.target_r is None else f"{self.target_r:g}R"
        le = "" if self.last_entry_minute is None else f" cut{self.last_entry_minute}"
        return f"{self.entry} OR{self.or_minutes} stop={self.stop} exit={tp}{le}"


def split_sessions(df: pd.DataFrame, pair: str, min_fill: float = 0.8) -> list[dict]:
    """Slice the bar series into complete cash sessions, as numpy arrays."""
    inst = INSTRUMENTS[pair]
    oh, om = map(int, inst["open"].split(":"))
    ch, cm = map(int, inst["close"].split(":"))
    session_len = (ch * 60 + cm) - (oh * 60 + om)
    t = df.index
    minute_of_day = t.hour * 60 + t.minute
    in_sess = (minute_of_day >= oh * 60 + om) & (minute_of_day < ch * 60 + cm)
    sub = df[in_sess]
    mins = (sub.index.hour * 60 + sub.index.minute - (oh * 60 + om)).to_numpy()
    dates = sub.index.date
    out = []
    for date, g in sub.groupby(dates, sort=True):
        if len(g) < min_fill * session_len:
            continue
        m = (g.index.hour * 60 + g.index.minute - (oh * 60 + om)).to_numpy()
        if m[0] > 1:  # first bar must be at the open
            continue
        out.append(dict(date=date, m=m, ts=g.index.to_numpy(),
                        o=g.open.to_numpy(), h=g.high.to_numpy(),
                        l=g.low.to_numpy(), c=g.close.to_numpy(),
                        session_len=session_len))
    return out


def simulate(sessions: list[dict], p: Params) -> pd.DataFrame:
    rows = []
    for s in sessions:
        m, o, h, l, c, ts = s["m"], s["o"], s["h"], s["l"], s["c"], s["ts"]
        in_or = m < p.or_minutes
        n_or = in_or.sum()
        if n_or < 0.6 * p.or_minutes:
            continue
        or_high, or_low = h[in_or].max(), l[in_or].min()
        or_open, or_close = o[in_or][0], c[in_or][-1]
        post = np.where(~in_or)[0]
        if len(post) < 2:
            continue

        if p.entry == "breakout":
            cand = post if p.last_entry_minute is None else post[m[post] < p.last_entry_minute]
            up = cand[c[cand] > or_high]
            dn = cand[c[cand] < or_low]
            i_up = up[0] if len(up) else None
            i_dn = dn[0] if len(dn) else None
            if i_up is None and i_dn is None:
                continue
            if i_dn is None or (i_up is not None and i_up < i_dn):
                d, i_entry, entry = 1, i_up, c[i_up]
            else:
                d, i_entry, entry = -1, i_dn, c[i_dn]
            first_exit_bar = i_entry + 1
        elif p.entry == "candle":
            if or_close == or_open:
                continue
            d = 1 if or_close > or_open else -1
            i_entry = post[0]
            entry = o[i_entry]
            first_exit_bar = i_entry
        else:
            raise ValueError(p.entry)

        if p.stop == "range":
            stop = or_low if d == 1 else or_high
        elif p.stop == "half":
            stop = (or_high + or_low) / 2
        else:
            raise ValueError(p.stop)
        risk = d * (entry - stop)
        if risk <= 0:
            continue
        target = entry + d * p.target_r * risk if p.target_r is not None else None

        if first_exit_bar >= len(m):
            continue
        sl = slice(first_exit_bar, None)
        if d == 1:
            stop_hit = l[sl] <= stop
            tgt_hit = h[sl] >= target if target is not None else np.zeros_like(stop_hit)
        else:
            stop_hit = h[sl] >= stop
            tgt_hit = l[sl] <= target if target is not None else np.zeros_like(stop_hit)
        i_stop = np.argmax(stop_hit) if stop_hit.any() else None
        i_tgt = np.argmax(tgt_hit) if tgt_hit.any() else None

        if i_stop is not None and (i_tgt is None or i_stop <= i_tgt):
            j = first_exit_bar + i_stop
            # gap through the stop fills at the open
            exit_px = min(o[j], stop) if d == 1 else max(o[j], stop)
            reason = "stop"
        elif i_tgt is not None:
            j = first_exit_bar + i_tgt
            exit_px, reason = target, "target"
        else:
            j = len(m) - 1
            exit_px, reason = c[j], "close"

        rows.append(dict(date=s["date"], dir=d, entry_time=ts[i_entry], entry=entry,
                         exit_time=ts[j], exit=exit_px, reason=reason, risk_pts=risk,
                         or_width=or_high - or_low, gross_pts=d * (exit_px - entry),
                         hold_min=int(m[j] - m[i_entry])))
    return pd.DataFrame(rows)


def apply_cost(trades: pd.DataFrame, cost_pts: float) -> pd.DataFrame:
    t = trades.copy()
    t["pnl_pts"] = t.gross_pts - cost_pts
    t["ret"] = t.pnl_pts / t.entry          # return on 1x index notional
    t["r"] = t.pnl_pts / t.risk_pts         # R multiple
    return t


def baseline_open_to_close(sessions: list[dict]) -> pd.Series:
    """Long at the open, flat at the close, every session (no cost)."""
    return pd.Series({s["date"]: s["c"][-1] / s["o"][0] - 1 for s in sessions})


def metrics(t: pd.DataFrame, all_dates: list, n_boot: int = 5000, seed: int = 0) -> dict:
    if len(t) == 0:
        return dict(trades=0)
    ret = t.ret.to_numpy()
    wins, losses = ret[ret > 0], ret[ret <= 0]
    daily = pd.Series(0.0, index=pd.Index(all_dates))
    daily.loc[t.date.to_numpy()] = ret  # one trade per day
    eq = daily.cumsum()
    dd = (eq - eq.cummax()).min()
    years = (pd.Timestamp(all_dates[-1]) - pd.Timestamp(all_dates[0])).days / 365.25
    rng = np.random.default_rng(seed)
    boot = rng.choice(ret, size=(n_boot, len(ret)), replace=True).mean(axis=1)
    return dict(
        trades=len(t),
        win_rate=(ret > 0).mean(),
        avg_ret_bp=ret.mean() * 1e4,
        avg_win_bp=wins.mean() * 1e4 if len(wins) else np.nan,
        avg_loss_bp=losses.mean() * 1e4 if len(losses) else np.nan,
        profit_factor=wins.sum() / -losses.sum() if losses.sum() < 0 else np.inf,
        expectancy_r=t.r.mean(),
        total_ret=ret.sum(),
        ann_ret=ret.sum() / years,
        sharpe=daily.mean() / daily.std() * np.sqrt(252) if daily.std() > 0 else np.nan,
        max_dd=dd,
        ci_lo_bp=np.percentile(boot, 2.5) * 1e4,
        ci_hi_bp=np.percentile(boot, 97.5) * 1e4,
        p_le_zero=(boot <= 0).mean(),
        pct_stop=(t.reason == "stop").mean(),
        pct_long=(t.dir == 1).mean(),
    )


def per_year(t: pd.DataFrame) -> pd.DataFrame:
    g = t.assign(year=pd.to_datetime(t.date).dt.year).groupby("year")
    return pd.DataFrame({
        "trades": g.size(),
        "win_rate": g.apply(lambda x: (x.ret > 0).mean()),
        "ret_%": g.ret.sum() * 100,
        "profit_factor": g.apply(lambda x: x.ret[x.ret > 0].sum() / -x.ret[x.ret <= 0].sum()
                                 if (x.ret <= 0).any() else np.inf),
    })
