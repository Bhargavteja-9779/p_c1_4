"""E13 (review cycle 1): pre-registered sensitivity analyses that were not reported in the first draft.

(a) Number of posterior samples M in {100, 300, 1000}: the proposed interval recomputed with FFBS mean/SD
    estimated from the first 100 / 300 / all 1000 draws (stored in the E03 summaries).
(b) Calibration-set size: fraction of subjects used for calibration in {0.25, 0.50, 0.75}.
(c) Pre-specified success criterion "width-error Spearman correlation positive with CI excluding 0": per
    stager x cohort x parameter, Spearman between interval width and |reference - plug-in| over LOSO
    intervals, with a subject-level cluster-bootstrap 95% CI.
All: alpha = 0.10, 200 subject-grouped splits (seeds 0..199) for (a)-(b).
Output: results/statistics/e13_M.csv, e13_calsize.csv, e13_spearman.csv
"""
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.evaluation.conformal_eval import PARAMS, PROPOSED, evaluate, param_frame, subject_split  # noqa: E402
from src.statistics.stats import cluster_bootstrap  # noqa: E402
from src.utils import RESULTS_DIR  # noqa: E402

STAGERS = ["yasa", "lgbm_sc_s0"]
R = 200


def frame_with_M(dc, p, m):
    f = param_frame(dc, p)
    if m != 1000:
        sub = dc if p != "REML" else dc[dc.ref_has_rem.astype(bool)]
        sub = sub[np.isfinite(sub[f"ref_{p}"].values)]
        f["mu"] = sub[f"ffbsM{m}_mean_{p}"].values
        f["sd"] = sub[f"ffbsM{m}_sd_{p}"].values
    return f


def _task(args):
    st, c, p, dc = args
    rows_m, rows_c = [], []
    frames = {m: frame_with_M(dc, p, m) for m in (100, 300, 1000)}
    for r in range(R):
        f = frames[1000]
        msk = subject_split(f["subject"].values, seed=r)
        for m, fm in frames.items():
            res, _, _ = evaluate(p, PROPOSED, fm[msk].reset_index(drop=True), fm[~msk].reset_index(drop=True), 0.10)
            rows_m.append(dict(stager=st, cohort=c, param=p, split=r, M=m, **res))
        for frac in (0.25, 0.50, 0.75):
            msk2 = subject_split(f["subject"].values, seed=r, frac=frac)
            for meth in (PROPOSED, "scp_abs_bc", "ba_loa"):
                res, _, _ = evaluate(p, meth, f[msk2].reset_index(drop=True), f[~msk2].reset_index(drop=True), 0.10)
                rows_c.append(dict(stager=st, cohort=c, param=p, split=r, cal_frac=frac, method=meth,
                                   n_cal=int(msk2.sum()), **res))
    return rows_m, rows_c


def spearman_criterion():
    rows = []
    for st in STAGERS:
        loso = pd.read_csv(RESULTS_DIR / "raw" / f"e04_loso_{st}.csv")
        d = loso[loso.method == PROPOSED].copy()
        d["width"], d["err"] = d.hi - d.lo, (d.y - d.plug).abs()
        for (c, p), g in d.groupby(["cohort", "param"]):
            by_s = {s: (gg.width.values, gg.err.values) for s, gg in g.groupby("subject")}
            fn = lambda L: spearmanr(np.concatenate([x[0] for x in L]), np.concatenate([x[1] for x in L])).statistic  # noqa: E731
            est, lo, hi = cluster_bootstrap(by_s, fn, B=1000)
            rows.append(dict(stager=st, cohort=c, param=p, spearman=est, lo95=lo, hi95=hi,
                             criterion_met=bool(lo > 0) if np.isfinite(lo) else False))
    return pd.DataFrame(rows)


def main():
    tasks = []
    for st in STAGERS:
        df = pd.read_csv(RESULTS_DIR / "summaries" / f"{st}_xfit.csv")
        for c, dc in df.groupby("cohort"):
            for p in PARAMS:
                tasks.append((st, c, p, dc))
    rm, rc = [], []
    with ProcessPoolExecutor(4) as ex:
        for a, b in ex.map(_task, tasks):
            rm += a
            rc += b
    out = RESULTS_DIR / "statistics"
    m = pd.DataFrame(rm).groupby(["stager", "cohort", "param", "M"])[["coverage", "mean_width", "interval_score"]].mean().reset_index()
    m.to_csv(out / "e13_M.csv", index=False)
    c = pd.DataFrame(rc).groupby(["stager", "cohort", "param", "cal_frac", "method"])[["coverage", "mean_width", "interval_score", "n_cal"]].mean().reset_index()
    c.to_csv(out / "e13_calsize.csv", index=False)
    s = spearman_criterion()
    s.to_csv(out / "e13_spearman.csv", index=False)
    print(m.pivot_table(index=["stager", "M"], values=["coverage", "interval_score"], aggfunc="mean").round(3))
    print(c[c.method == PROPOSED].groupby(["cal_frac"])[["coverage", "mean_width"]].mean().round(3))
    print("Spearman criterion met:", int(s.criterion_met.sum()), "of", len(s))


if __name__ == "__main__":
    main()
