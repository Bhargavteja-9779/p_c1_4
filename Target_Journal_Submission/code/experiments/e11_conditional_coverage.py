"""E11 (exploratory, added after E04/E07): conditional coverage for difficult nights.

Motivation: LOSO coverage of the proposed intervals was 81-85 % in the quartile of nights with the lowest
plug-in accuracy (marginal 90 %). Hypothesis: Mondrian (group-conditional) conformal calibration that
stratifies nights by a LABEL-FREE difficulty proxy raises coverage of difficult nights, at the cost of wider
intervals for them and narrower intervals for easy nights.

Methods (all leave-one-subject-out within cohort, alpha = 0.10, identical calibration nights):
  proposed          : norm_reg_ffbs (pre-specified)
  dfloa             : scp_abs_bc (bias-corrected constant width)
  mondrian_entropy  : proposed score, conformal quantile computed separately in K=2 bins defined by the median
                      mean epoch entropy over calibration + test nights (label-free)
  mondrian_sd       : as above, bins by the FFBS posterior SD (the scale itself)
Coverage is reported overall and by quartile of plug-in accuracy (a label-based descriptor used ONLY for
evaluation, never for building intervals).
Output: results/raw/e11_conditional_<stager>.csv (per night), results/statistics/e11_conditional_summary.csv
"""
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.evaluation.conformal_eval import PARAMS, clip, make_interval, param_frame  # noqa: E402
from src.uncertainty.conformal import conformal_quantile, interval_score  # noqa: E402
from src.utils import RESULTS_DIR  # noqa: E402

ALPHA = 0.10


def mondrian(cal, test, key, alpha=ALPHA):
    c = np.median(np.concatenate([cal["sd"].values, test["sd"].values]))
    sc, st = cal["sd"].values + c, test["sd"].values + c
    s_cal = np.abs(cal["y"].values - cal["mu"].values) / sc
    allv = np.concatenate([cal[key].values, test[key].values])
    thr = np.median(allv)                               # label-free bin boundary
    b_cal, b_test = cal[key].values > thr, test[key].values > thr
    lo, hi = np.empty(len(test)), np.empty(len(test))
    for b in (False, True):
        q = conformal_quantile(s_cal[b_cal == b], alpha)
        m = b_test == b
        lo[m] = test["mu"].values[m] - q * st[m]
        hi[m] = test["mu"].values[m] + q * st[m]
    return lo, hi


def _task(args):
    stager, cohort, p, f = args
    rows = []
    for s in f["subject"].unique():
        m = f["subject"].values != s
        cal, test = f[m].reset_index(drop=True), f[~m].reset_index(drop=True)
        ints = {"proposed": make_interval("norm_reg_ffbs", cal, test, ALPHA),
                "dfloa": make_interval("scp_abs_bc", cal, test, ALPHA),
                "mondrian_entropy": mondrian(cal, test, "entropy"),
                "mondrian_sd": mondrian(cal, test, "sd")}
        for meth, (lo, hi) in ints.items():
            lo, hi = clip(p, lo, hi)
            for i in range(len(test)):
                rows.append(dict(stager=stager, cohort=cohort, param=p, method=meth, night=test["night"].iloc[i],
                                 subject=s, y=test["y"].iloc[i], lo=lo[i], hi=hi[i]))
    return rows


def main():
    out_rows = []
    for st in ["yasa", "lgbm_sc_s0"]:
        df = pd.read_csv(RESULTS_DIR / "summaries" / f"{st}_xfit.csv")
        tasks = [(st, c, p, param_frame(dc, p)) for c, dc in df.groupby("cohort") for p in PARAMS]
        with ProcessPoolExecutor(4) as ex:
            rows = [r for rs in ex.map(_task, tasks) for r in rs]
        d = pd.DataFrame(rows)
        acc = df[["night", "acc_plugin", "cohort"]].copy()
        acc["acc_quartile"] = acc.groupby("cohort")["acc_plugin"].transform(
            lambda x: pd.qcut(x, 4, labels=["Q1 (worst)", "Q2", "Q3", "Q4 (best)"]))
        d = d.merge(acc[["night", "acc_quartile"]], on="night")
        d.to_csv(RESULTS_DIR / "raw" / f"e11_conditional_{st}.csv", index=False)
        d["cov"] = (d.y >= d.lo) & (d.y <= d.hi)
        d["width"] = d.hi - d.lo
        d["is"] = interval_score(d.y.values, d.lo.values, d.hi.values, ALPHA)
        for (c, meth, q), g in d.groupby(["cohort", "method", "acc_quartile"], observed=True):
            out_rows.append(dict(stager=st, cohort=c, method=meth, subset=str(q), param="all", coverage=g["cov"].mean(),
                                 mean_width=g.width.mean(), interval_score=g["is"].mean(), n=len(g)))
        for (c, meth, q, prm), g in d.groupby(["cohort", "method", "acc_quartile", "param"], observed=True):
            out_rows.append(dict(stager=st, cohort=c, method=meth, subset=str(q), param=prm, coverage=g["cov"].mean(),
                                 mean_width=g.width.mean(), interval_score=g["is"].mean(), n=len(g)))
        for (c, meth), g in d.groupby(["cohort", "method"]):
            out_rows.append(dict(stager=st, cohort=c, method=meth, subset="all", param="all", coverage=g["cov"].mean(),
                                 mean_width=g.width.mean(), interval_score=g["is"].mean(), n=len(g)))
    s = pd.DataFrame(out_rows)
    (RESULTS_DIR / "statistics").mkdir(exist_ok=True)
    s.to_csv(RESULTS_DIR / "statistics" / "e11_conditional_summary.csv", index=False)
    print(s[s.param == "all"].pivot_table(index=["stager", "cohort", "subset"], columns="method", values="coverage").round(3).to_string())


if __name__ == "__main__":
    main()
