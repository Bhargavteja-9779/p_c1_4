"""E16 (added after internal review): plain-split sensitivity analysis of the primary (E12 'within') design.

The primary design cross-fits the label-dependent components (BCTS, prior, transitions, tau) WITHIN the calibration
half to obtain out-of-sample calibration scores, but summarises test nights with the model fitted on the whole
calibration half.  Calibration and test scores therefore come from different fitted models (a CV-type construction
without an exact finite-sample guarantee).  This script runs the textbook split-conformal alternative, which has the
exact guarantee for exchangeable units:

  for each of the R subject-grouped 50/50 calibration/test splits of E12 (identical split seeds, subject_split(seed=r)),
    1. split the calibration SUBJECTS at random into halves A and B (subject_split(seed=PLAIN_SEED + r));
    2. fit every label-dependent component (BCTS, source prior, transition matrix, tau) on the nights of A only;
    3. compute night summaries of the nights of B and of the test nights with A's model;
    4. conformalise on B only (n_cal ~ a quarter of the cohort) and evaluate on the test nights.
  The conformal/LoA comparators are computed from exactly the same B / test frames (they use only plug-in values
  and B's labels, so for them the design differs from E12 only in the smaller calibration set).

E12 itself is not modified; its functions are reused.
Output: results/raw/e16_plainsplit_<stager>.csv.gz (one row per split x cohort x parameter x method, columns as
        e12_honest_<stager>.csv.gz) and results/raw/e16_nights_<stager>.csv.gz (per-night, git-ignored).
"""
import argparse
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from e03_night_summaries import load_preds  # noqa: E402
from e12_honest_protocol import _evaluate, _summ  # noqa: E402
from src.evaluation.conformal_eval import subject_split  # noqa: E402
from src.uncertainty.night_summary import fit_source_model  # noqa: E402
from src.utils import RESULTS_DIR, cache_root  # noqa: E402

PLAIN_SEED = 100000
NIGHT_COLS = ["setting", "cohort", "rep", "n_target", "param", "method", "night", "subject", "interval_score", "width",
              "covered", "y", "lo", "hi", "plug", "plugc"]


def plain_frames(cal_nights, test_nights, preds, meta, tag, r):
    subj = meta.set_index("night").loc[cal_nights, "subject"].values
    in_a = subject_split(subj, seed=PLAIN_SEED + r)
    a_n = [n for n, k in zip(cal_nights, in_a) if k]
    b_n = [n for n, k in zip(cal_nights, in_a) if not k]
    sm_a = fit_source_model([preds[n][0] for n in a_n], [preds[n][1] for n in a_n])
    return (_summ(b_n, preds, sm_a, tag + "|B", meta), _summ(test_nights, preds, sm_a, tag + "|test", meta),
            len(a_n), len(b_n))


def _task(args):
    stager, cohort, r, cal_n, test_n = args
    preds = load_preds(stager, cohort)
    meta = pd.read_csv(cache_root() / "sleep" / "nights.csv")
    cal_df, test_df, na, nb = plain_frames(cal_n, test_n, preds, meta, f"{stager}|plainsplit|{cohort}|{(r, 0)}", r)
    info = dict(stager=stager, setting="plainsplit", cohort=cohort, rep=r, n_target=0)
    rows, _, per_night = _evaluate(cal_df, test_df, info)
    for x in rows:
        x["n_fit"] = na
    return rows, per_night


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stagers", nargs="+", default=["yasa", "lgbm_sc_s0"])
    ap.add_argument("--R", type=int, default=50)
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    meta = pd.read_csv(cache_root() / "sleep" / "nights.csv")
    for st in a.stagers:
        tasks = []
        for c in ["SC", "ST", "HMC"]:
            nights = sorted(load_preds(st, c))
            subj = meta.set_index("night").loc[nights, "subject"].values
            for r in range(a.R):
                m = subject_split(subj, seed=r)       # identical calibration/test split to E12 'within'
                tasks.append((st, c, r, [n for n, k in zip(nights, m) if k], [n for n, k in zip(nights, m) if not k]))
        rows, pn = [], []
        with ProcessPoolExecutor(a.workers) as ex:
            for rr, nn in ex.map(_task, tasks, chunksize=2):
                rows += rr
                pn += nn
        out = RESULTS_DIR / "raw"
        pd.DataFrame(rows).to_csv(out / f"e16_plainsplit_{st}.csv.gz", index=False)
        pd.DataFrame(pn, columns=NIGHT_COLS).to_csv(out / f"e16_nights_{st}.csv.gz", index=False)
        d = pd.DataFrame(rows)
        print(st, "\n", d[d.method.isin(["ba_loa", "scp_signed", "norm_reg_ffbs"])]
              .groupby(["cohort", "method"])["coverage"].mean().unstack("method").round(3), flush=True)


if __name__ == "__main__":
    main()
