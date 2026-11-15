"""E06 (RQ4): transportability of SC-calibrated intervals and few-night target recalibration.

(a) Source-only: calibration = all SC nights, test = all nights of ST / HMC (HMM source model fitted on
    SC; SC calibration nights use cross-fitted summaries so their own labels are never used).
(b) Few-night recalibration: n_t target nights (whole subjects) are labelled and used for calibration,
    the remaining target nights are tested. Strategies: 'target' (target-only calibration) and
    'pooled' (SC + n_t target nights). R repetitions with seeds 0..R-1.
Outputs: results/raw/e06_source_only_<stager>.csv, results/raw/e06_fewshot_<stager>.csv
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.evaluation.conformal_eval import METHODS, PARAMS, evaluate, param_frame  # noqa: E402
from src.utils import RESULTS_DIR  # noqa: E402

NT = {"ST": [10, 20, 30], "HMC": [10, 20, 30, 50]}
FEW_METHODS = ["ba_loa", "scp_abs", "scp_abs_mu", "cqr_ffbs", "norm_reg_ffbs"]


def pick_subjects(f, n_nights, rng):
    subj = np.array(sorted(f["subject"].unique()))
    rng.shuffle(subj)
    chosen, total = [], 0
    counts = f.groupby("subject").size()
    for s in subj:
        if total >= n_nights:
            break
        chosen.append(s)
        total += counts[s]
    return f["subject"].isin(chosen).values


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stagers", nargs="+", default=["yasa", "lgbm_sc_s0"])
    ap.add_argument("--R", type=int, default=500)
    a = ap.parse_args()
    out = RESULTS_DIR / "raw"
    for s in a.stagers:
        df = pd.read_csv(RESULTS_DIR / "summaries" / f"{s}_srcSC.csv")
        src_rows, few_rows = [], []
        for p in PARAMS:
            src = param_frame(df[df.cohort == "SC"], p)
            for tgt in ["ST", "HMC"]:
                t = param_frame(df[df.cohort == tgt], p)
                for alpha in (0.05, 0.10, 0.20):
                    for meth in METHODS:
                        res, lo, hi = evaluate(p, meth, src, t, alpha)
                        src_rows.append(dict(stager=s, target=tgt, param=p, alpha=alpha, method=meth,
                                             n_cal=len(src), n_test=len(t),
                                             n_covered=int(round(res["coverage"] * len(t))), **res))
                for nt in NT[tgt]:
                    for r in range(a.R):
                        rng = np.random.default_rng(r)
                        m = pick_subjects(t, nt, rng)
                        cal_t, test = t[m].reset_index(drop=True), t[~m].reset_index(drop=True)
                        for strat, cal in (("target", cal_t),
                                           ("pooled", pd.concat([src, cal_t], ignore_index=True))):
                            for meth in FEW_METHODS:
                                res, _, _ = evaluate(p, meth, cal, test, 0.10)
                                few_rows.append(dict(stager=s, target=tgt, param=p, n_target=nt,
                                                     n_cal=len(cal), strategy=strat, split=r,
                                                     method=meth, **res))
        so = pd.DataFrame(src_rows)
        so.to_csv(out / f"e06_source_only_{s}.csv", index=False)
        pd.DataFrame(few_rows).to_csv(out / f"e06_fewshot_{s}.csv", index=False)
        print(s, "\n", so[so.alpha == 0.10].pivot_table(index=["target", "param"], columns="method",
                                                          values="coverage").round(3).to_string(), flush=True)


if __name__ == "__main__":
    main()
