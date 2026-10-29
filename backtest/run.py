"""Run the ORB grid on S&P 500 and DAX, write RESULTS.md and equity charts."""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from data import INSTRUMENTS, load
from orb import Params, apply_cost, baseline_open_to_close, metrics, per_year, simulate, split_sessions

OUT = Path(__file__).parent
FIG = OUT / "figures"
FIG.mkdir(exist_ok=True)

# round-trip cost in index points: (label, SPX, DAX)
COSTS = {"gross": (0.0, 0.0), "futures": (0.35, 1.0), "retail CFD": (0.75, 2.5)}
SPLIT_YEAR = 2018  # <= 2017 in-sample, >= 2018 out-of-sample

GRID = [Params(or_minutes=orm, entry=e, target_r=tr)
        for e in ("breakout", "candle")
        for orm in (5, 15, 30, 60)
        for tr in (None, 1.0, 2.0)]


def fmt_table(rows: list[dict]) -> str:
    df = pd.DataFrame(rows)
    return df.to_markdown(index=False, floatfmt=".2f")


def main() -> None:
    md = ["# Opening-range breakout backtest: S&P 500 and DAX\n",
          "Data: histdata.com 1-minute index CFD bars, Nov 2010 to Oct 2026. "
          "One trade per day, cash session only. Returns are on 1x index notional "
          "(no leverage), so 1 bp = 0.01% of the index level per trade.\n",
          f"Costs (round trip, index points): S&P futures {COSTS['futures'][0]}, S&P retail CFD "
          f"{COSTS['retail CFD'][0]}; DAX futures {COSTS['futures'][1]}, DAX retail CFD {COSTS['retail CFD'][1]}.\n"]
    curves = {}
    for k, (pair, inst) in enumerate(INSTRUMENTS.items()):
        df = load(pair)
        sessions = split_sessions(df, pair)
        dates = [s["date"] for s in sessions]
        years = (pd.Timestamp(dates[-1]) - pd.Timestamp(dates[0])).days / 365.25
        base = baseline_open_to_close(sessions)
        md.append(f"\n## {inst['name']} ({pair})\n")
        md.append(f"{len(sessions)} complete sessions, {dates[0]} to {dates[-1]}.\n")
        md.append(f"Baseline, long open-to-close every day, gross: total {base.sum()*100:.1f}%, "
                  f"Sharpe {base.mean()/base.std()*np.sqrt(252):.2f}, mean {base.mean()*1e4:.2f} bp/day.\n")

        results = {}
        rows_full, rows_split = [], []
        for p in GRID:
            tr = simulate(sessions, p)
            results[p] = tr
            row = {"strategy": p.label(), "trades": len(tr)}
            for cl, c in COSTS.items():
                m = metrics(apply_cost(tr, c[k]), dates)
                row[f"{cl} bp/trade"] = m["avg_ret_bp"]
                row[f"{cl} PF"] = m["profit_factor"]
                row[f"{cl} Sharpe"] = m["sharpe"]
            m_cfd = metrics(apply_cost(tr, COSTS["retail CFD"][k]), dates)
            m_gross = metrics(apply_cost(tr, 0.0), dates)
            row["win rate"] = m_gross["win_rate"]
            row["max DD (CFD)"] = m_cfd["max_dd"]
            row["P(edge<=0) gross"] = m_gross["p_le_zero"]
            row["95% CI gross bp"] = f"[{m_gross['ci_lo_bp']:.1f}, {m_gross['ci_hi_bp']:.1f}]"
            rows_full.append(row)

            # in-sample / out-of-sample at futures cost
            tc = apply_cost(tr, COSTS["futures"][k])
            yr = pd.to_datetime(tc.date).dt.year
            ins, oos = tc[yr < SPLIT_YEAR], tc[yr >= SPLIT_YEAR]
            d_in = [d for d in dates if d.year < SPLIT_YEAR]
            d_out = [d for d in dates if d.year >= SPLIT_YEAR]
            mi, mo = metrics(ins, d_in, n_boot=1000), metrics(oos, d_out, n_boot=1000)
            rows_split.append({"strategy": p.label(),
                               "IS bp/trade": mi.get("avg_ret_bp", np.nan), "IS Sharpe": mi.get("sharpe", np.nan),
                               "OOS bp/trade": mo.get("avg_ret_bp", np.nan), "OOS Sharpe": mo.get("sharpe", np.nan)})

        md.append("\n### Full sample, all configurations\n")
        md.append(fmt_table(rows_full) + "\n")

        split_df = pd.DataFrame(rows_split).sort_values("IS Sharpe", ascending=False)
        md.append(f"\n### Overfitting check: pick the best 2010-{SPLIT_YEAR-1}, test on {SPLIT_YEAR}-2026 (futures cost)\n")
        md.append(split_df.to_markdown(index=False, floatfmt=".2f") + "\n")
        best_label = split_df.iloc[0]["strategy"]
        md.append(f"\nBest in-sample: **{best_label}**, IS Sharpe {split_df.iloc[0]['IS Sharpe']:.2f}, "
                  f"OOS Sharpe {split_df.iloc[0]['OOS Sharpe']:.2f}.\n")

        # classic config detail
        classic = Params(or_minutes=30, entry="breakout", target_r=None)
        tc = apply_cost(results[classic], COSTS["futures"][k])
        md.append(f"\n### Year by year: {classic.label()} at futures cost\n")
        md.append(per_year(tc).to_markdown(floatfmt=".2f") + "\n")
        # long vs short
        for name, sub in (("long", tc[tc.dir == 1]), ("short", tc[tc.dir == -1])):
            m = metrics(sub, dates, n_boot=1000)
            md.append(f"- {name} trades only: {m['trades']} trades, {m['avg_ret_bp']:.2f} bp/trade, "
                      f"PF {m['profit_factor']:.2f}, Sharpe {m['sharpe']:.2f}\n")

        # equity curves for the chart
        curves[pair] = {"baseline (long open-to-close)": base.cumsum()}
        for cl, c in COSTS.items():
            t = apply_cost(results[classic], c[k])
            s = pd.Series(0.0, index=pd.Index(dates)); s.loc[t.date.to_numpy()] = t.ret.to_numpy()
            curves[pair][f"ORB30 {cl}"] = s.cumsum()
        # best-in-sample config at CFD cost, for the chart
        pbest = next(p for p in GRID if p.label() == best_label)
        t = apply_cost(results[pbest], COSTS["retail CFD"][k])
        s = pd.Series(0.0, index=pd.Index(dates)); s.loc[t.date.to_numpy()] = t.ret.to_numpy()
        curves[pair][f"best in-sample ({best_label}) retail CFD"] = s.cumsum()

        # save trades of the classic config
        results[classic].to_csv(OUT.parent / "data" / f"trades_{pair}_orb30.csv", index=False)

    fig, axes = plt.subplots(1, 2, figsize=(15, 5.5))
    for ax, (pair, cs) in zip(axes, curves.items()):
        for name, s in cs.items():
            ax.plot(pd.to_datetime(s.index), s.to_numpy() * 100, label=name, lw=1.2)
        ax.axhline(0, color="k", lw=0.5)
        ax.axvline(pd.Timestamp(f"{SPLIT_YEAR}-01-01"), color="grey", ls="--", lw=0.8)
        ax.set_title(f"{INSTRUMENTS[pair]['name']}: cumulative return, 1x notional (%)")
        ax.legend(fontsize=7); ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIG / "equity_curves.png", dpi=130)
    md.append("\n![equity curves](figures/equity_curves.png)\n")
    (OUT / "RESULTS.md").write_text("\n".join(md))
    print("\n".join(md))


if __name__ == "__main__":
    main()
