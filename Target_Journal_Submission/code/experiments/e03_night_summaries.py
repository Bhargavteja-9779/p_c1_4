"""E03: per-night predictive summaries for every stager x configuration.

Configurations
  xfit  : within-cohort, subject-grouped 5-fold cross-fitting. For nights of fold k of cohort C, the
          source model (calibration, prior, transitions, tau) is fitted on the other 4 folds of C.
  srcSC : cross-cohort. Source model fitted on ALL SC nights, applied to ST and HMC nights. (SC nights
          in this configuration are taken from xfit, i.e. their own labels are never used.)
Output: results/summaries/<stager>_<config>.csv (one row per night) and fitted tau values in
        results/summaries/source_models.json
"""
import argparse
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.uncertainty.night_summary import fit_source_model, summarise_night  # noqa: E402
from src.utils import RESULTS_DIR, cache_root  # noqa: E402

N_FOLDS = 5
FOLD_SEED = 2026


def load_preds(stager, cohort):
    d = RESULTS_DIR / "predictions" / stager / cohort
    out = {}
    for p in sorted(d.glob("*.npz")):
        z = np.load(p)
        out[p.stem] = (z["P"].astype(np.float64), z["y"].astype(np.int64))
    return out


def subject_folds(meta: pd.DataFrame, cohort: str):
    sub = meta[meta.cohort == cohort]
    subj = np.array(sorted(sub.subject.unique()))
    rng = np.random.default_rng(FOLD_SEED)
    rng.shuffle(subj)
    f = {s: i % N_FOLDS for i, s in enumerate(subj)}
    return {r.night: f[r.subject] for r in sub.itertuples()}


def _work(args):
    P, y, sm, name, tag, M = args
    return name, summarise_night(P, y, sm, name, tag, M=M)


def run(stager, cohorts, M, workers, meta, limit=0):
    rows = {"xfit": [], "srcSC": []}
    taus = {}
    preds = {c: load_preds(stager, c) for c in cohorts}
    if limit:
        preds = {c: dict(list(v.items())[:limit]) for c, v in preds.items()}
    mrow = meta.set_index("night")
    with ProcessPoolExecutor(workers) as ex:
        for c in cohorts:
            folds = subject_folds(meta, c)
            for k in range(N_FOLDS):
                tr = [n for n in preds[c] if folds[n] != k]
                te = [n for n in preds[c] if folds[n] == k]
                if not te or not tr:
                    continue
                sm = fit_source_model([preds[c][n][0] for n in tr], [preds[c][n][1] for n in tr])
                taus[f"{c}_xfit_fold{k}"] = sm.tau
                jobs = [(preds[c][n][0], preds[c][n][1], sm, n, f"{stager}|xfit", M) for n in te]
                for name, rec in ex.map(_work, jobs):
                    rows["xfit"].append({"night": name, "cohort": c, "fold": k, **rec})
        if "SC" in preds:
            sm = fit_source_model([v[0] for v in preds["SC"].values()], [v[1] for v in preds["SC"].values()])
            taus["SC_all"] = sm.tau
            for c in [c for c in cohorts if c != "SC"]:
                jobs = [(P, y, sm, n, f"{stager}|srcSC", M) for n, (P, y) in preds[c].items()]
                for name, rec in ex.map(_work, jobs):
                    rows["srcSC"].append({"night": name, "cohort": c, **rec})
            rows["srcSC"] += [dict(r, config_note="xfit") for r in rows["xfit"] if r["cohort"] == "SC"]
    out = RESULTS_DIR / "summaries"
    out.mkdir(parents=True, exist_ok=True)
    for cfg, rs in rows.items():
        df = pd.DataFrame(rs)
        df = df.merge(meta[["night", "subject", "age", "sex", "condition"]], on="night", how="left")
        df.to_csv(out / f"{stager}_{cfg}.csv", index=False)
    return taus


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stagers", nargs="+", default=["yasa", "lgbm_sc_s0", "lgbm_sc_s1", "lgbm_sc_s2"])
    ap.add_argument("--cohorts", nargs="+", default=["SC", "ST", "HMC"])
    ap.add_argument("--M", type=int, default=1000)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    meta = pd.read_csv(cache_root() / "sleep" / "nights.csv")
    meta["condition"] = meta["condition"].fillna("")
    path = RESULTS_DIR / "summaries" / "source_models.json"
    allt = json.loads(path.read_text()) if path.exists() else {}
    for s in a.stagers:
        allt[s] = run(s, a.cohorts, a.M, a.workers, meta, a.limit)
        print(s, "tau:", allt[s], flush=True)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(allt, indent=2))


if __name__ == "__main__":
    main()
