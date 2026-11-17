"""E04 (RQ1, RQ2, RQ3): within-cohort conformal evaluation.

(a) R random subject-grouped 50/50 calibration/test splits per cohort (split seeds 0..R-1), every
    method, every parameter, alpha in {0.05, 0.10, 0.20}.
(b) Leave-one-subject-out (LOSO): each night's interval is calibrated on all other subjects' nights in
    the same cohort; per-night intervals are stored for paired tests and error analysis (alpha = 0.10).
Inputs : results/summaries/<stager>_xfit.csv
Outputs: results/raw/e04_splits_<stager>.csv, results/raw/e04_loso_<stager>.csv
"""
import argparse
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.evaluation.conformal_eval import METHODS, PARAMS, evaluate, param_frame, subject_split  # noqa: E402
from src.utils import RESULTS_DIR  # noqa: E402

ALPHAS = [0.05, 0.10, 0.20]
SKIP_OTHER_ALPHA = ("norm_reg_ind", "norm_reg_ffbs1", "ind_pct", "norm_reg_plug", "norm_reg_plugc",
                    "scp_abs_cal", "scp_abs_mu", "norm_reg_ind_s", "norm_reg_ffbs1_s")


def _split_task(args):
    cohort, p, f, stager, R = args
    rows = []
    for r in range(R):
        m = subject_split(f["subject"].values, seed=r)
        cal, test = f[m].reset_index(drop=True), f[~m].reset_index(drop=True)
        for alpha in ALPHAS:
            for meth in METHODS:
                if alpha != 0.10 and meth in SKIP_OTHER_ALPHA:
                    continue
                res, _, _ = evaluate(p, meth, cal, test, alpha)
                rows.append(dict(stager=stager, cohort=cohort, param=p, split=r, alpha=alpha,
                                 method=meth, n_cal=len(cal), n_test=len(test), **res))
    return rows


def _loso_task(args):
    cohort, p, f, stager, alpha = args
    rows = []
    for s in f["subject"].unique():
        m = f["subject"].values != s
        cal, test = f[m].reset_index(drop=True), f[~m].reset_index(drop=True)
        for meth in METHODS:
            res, lo, hi = evaluate(p, meth, cal, test, alpha)
            for i in range(len(test)):
                rows.append(dict(stager=stager, cohort=cohort, param=p, method=meth,
                                 night=test["night"].iloc[i], subject=s, y=test["y"].iloc[i],
                                 plug=test["plug"].iloc[i], mu=test["mu"].iloc[i], lo=lo[i], hi=hi[i]))
    return rows


def _tasks(df):
    return [(cohort, p, param_frame(dc, p)) for cohort, dc in df.groupby("cohort") for p in PARAMS]


def run_splits(df, stager, R, workers=4):
    with ProcessPoolExecutor(workers) as ex:
        out = ex.map(_split_task, [(c, p, f, stager, R) for c, p, f in _tasks(df)])
        return pd.DataFrame([r for rows in out for r in rows])


def run_loso(df, stager, alpha=0.10, workers=4):
    with ProcessPoolExecutor(workers) as ex:
        out = ex.map(_loso_task, [(c, p, f, stager, alpha) for c, p, f in _tasks(df)])
        return pd.DataFrame([r for rows in out for r in rows])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stagers", nargs="+", default=["yasa", "lgbm_sc_s0", "lgbm_sc_s1", "lgbm_sc_s2"])
    ap.add_argument("--R", type=int, default=500)
    ap.add_argument("--no-loso", action="store_true")
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    out = RESULTS_DIR / "raw"
    out.mkdir(parents=True, exist_ok=True)
    for s in a.stagers:
        df = pd.read_csv(RESULTS_DIR / "summaries" / f"{s}_xfit.csv")
        sp = run_splits(df, s, a.R, a.workers)
        sp.to_csv(out / f"e04_splits_{s}.csv.gz", index=False)
        if not a.no_loso and s in ("yasa", "lgbm_sc_s0"):
            run_loso(df, s, workers=a.workers).to_csv(out / f"e04_loso_{s}.csv", index=False)
        g = sp[sp.alpha == 0.10].groupby(["cohort", "param", "method"])[["coverage", "mean_width"]].mean()
        print(s, "\n", g.unstack("method")["coverage"].round(3).to_string(), flush=True)


if __name__ == "__main__":
    main()
