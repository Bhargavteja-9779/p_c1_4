"""E18: review workload. If a laboratory sends some nights to manual re-scoring, which nights should it pick?

From the per-night outputs of the primary analysis (E12 'within'; regenerated file results/raw/e12_nights_<stager>.csv.gz):
  (a) decisions: for each threshold, the share of the point estimate's (recalibrated plug-in) misclassifications that fall on the nights a method
      leaves undecided (= nights it would send to review), and the share of nights that this requires;
  (b) triage curves for TST: nights ranked by interval width of the proposed method, by the label-free |raw - recalibrated plug-in| difference,
      at random, or by the true error (oracle); remaining share of nights with an absolute error > 30 min after reviewing a given share of nights.
Outputs: results/statistics/e18_workload_decisions.csv, e18_triage_curve.csv
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.utils import RESULTS_DIR  # noqa: E402

S, RAW = RESULTS_DIR / "statistics", RESULTS_DIR / "raw"
THRESH = {"TST": ("<", 360), "SOL": (">", 30), "WASO": (">", 30)}
METHODS = ["norm_reg_ffbs", "scp_signed", "scp_abs_cal", "scp_abs_bc", "ba_loa"]
GRID = np.round(np.arange(0, 1.0001, 0.05), 2)


def side(op, x, thr):
    return {"<": x < thr, ">": x > thr}[op]


def decisions(n, st):
    rows = []
    for p, (op, thr) in THRESH.items():
        g = n[(n.param == p) & n.method.isin(METHODS)]
        ref = side(op, g.y, thr)
        pos = {"<": g.hi < thr, ">": g.lo > thr}[op]
        neg = {"<": g.lo >= thr, ">": g.hi <= thr}[op]
        decided = pos | neg
        wrong = side(op, g.plugc, thr) != ref                # misclassification of the recalibrated point estimate
        d = g.assign(decided=decided, wrong=wrong)
        for coh_label, dd in [("pooled", d)] + list(d.groupby("cohort")):
            for m, x in dd.groupby("method"):
                tot_wrong = x.wrong.sum()
                resid = (x.wrong & x.decided).sum()
                rows.append(dict(stager=st, cohort=coh_label, param=p, method=m, n=len(x), frac_review=1 - x.decided.mean(),
                                 misclass_total=float(x.wrong.mean()), share_caught=(1 - resid / tot_wrong) if tot_wrong else np.nan,
                                 misclass_resid_decided=float(x[x.decided].wrong.mean()) if x.decided.any() else np.nan))
    return pd.DataFrame(rows)


def triage(n, st, cut=30.0):
    t = n[(n.param == "TST") & (n.method == "norm_reg_ffbs")].copy()
    t["err"] = (t.plugc - t.y).abs()
    t["lf"] = (t.plug - t.plugc).abs()
    rows = []
    for coh_label, dd in [("pooled", t)] + list(t.groupby("cohort")):
        for (rep), r in dd.groupby("rep"):
            e = r.err.values
            big = e > cut
            if big.sum() == 0:
                continue
            for pol, key in [("width", r.width.values), ("raw_minus_cal", r.lf.values), ("oracle", e)]:
                order = np.argsort(-key, kind="stable")
                cum = np.cumsum(big[order])
                for f in GRID:
                    k = int(round(f * len(e)))
                    rows.append((st, coh_label, rep, pol, f, 1 - (cum[k - 1] if k > 0 else 0) / big.sum()))
            for f in GRID:
                rows.append((st, coh_label, rep, "random", f, 1 - f))
    d = pd.DataFrame(rows, columns=["stager", "cohort", "rep", "policy", "review_frac", "resid_share_gt30"])
    return d.groupby(["stager", "cohort", "policy", "review_frac"]).resid_share_gt30.mean().reset_index()


def main():
    dec, tri = [], []
    for st in ["yasa", "lgbm_sc_s0"]:
        n = pd.read_csv(RAW / f"e12_nights_{st}.csv.gz")
        n = n[n.setting == "within"]
        dec.append(decisions(n, st))
        tri.append(triage(n, st))
    pd.concat(dec).to_csv(S / "e18_workload_decisions.csv", index=False)
    pd.concat(tri).to_csv(S / "e18_triage_curve.csv", index=False)
    print("E18 done")


if __name__ == "__main__":
    main()
