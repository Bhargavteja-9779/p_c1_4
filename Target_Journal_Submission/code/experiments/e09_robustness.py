"""E09 (robustness): signal corruption of TEST nights; calibration remains on clean nights.

Corruptions (applied to EEG and EOG of a night, deterministic per night):
  gauss05 / gauss10 : additive white Gaussian noise, SD = 0.5 / 1.0 x the channel's robust SD
                      (median absolute deviation x 1.4826) -> SNR approx. 6 dB / 0 dB
  art10 / art25     : movement-artefact bursts in 10% / 25% of epochs (random-walk drift, SD 50 uV per
                      sample-step low-passed, plus clipping at +-300 uV)
Stager: YASA pretrained (external; no retraining needed).  HMM source models are fitted on CLEAN
nights of the other folds (as in E03 xfit).  Conformal calibration uses clean nights of calibration
subjects; tested on corrupted nights of test subjects (R = 200 subject-grouped 50/50 splits).
Outputs: results/predictions/yasa_<c>/..., results/summaries/yasa_<c>_xfit.csv, results/raw/e09_robustness.csv
"""
import argparse
import sys
from concurrent.futures import ProcessPoolExecutor
from dataclasses import replace
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.signal import lfilter

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from e03_night_summaries import load_preds, subject_folds  # noqa: E402
from src.data import sleep  # noqa: E402
from src.evaluation.conformal_eval import METHODS, PARAMS, evaluate, param_frame, subject_split  # noqa: E402
from src.models.yasa_stager import yasa_features_and_proba  # noqa: E402
from src.uncertainty.night_summary import fit_source_model, night_seed, summarise_night  # noqa: E402
from src.utils import RESULTS_DIR, cache_root  # noqa: E402

CORRUPTIONS = ["gauss05", "gauss10", "art10", "art25"]
EVAL_METHODS = ["ba_loa", "scp_abs", "scp_abs_bc", "scp_abs_cal", "scp_abs_mu", "cqr_ffbs", "cqr_qr", "norm_entropy_reg", "norm_reg_ffbs", "norm_reg_plugc"]


def corrupt(x: np.ndarray, kind: str, rng) -> np.ndarray:
    x = x.astype(np.float32)
    rsd = 1.4826 * np.median(np.abs(x - np.median(x))) + 1e-6
    if kind.startswith("gauss"):
        k = {"gauss05": 0.5, "gauss10": 1.0}[kind]
        return x + rng.normal(0, k * rsd, len(x)).astype(np.float32)
    frac = {"art10": 0.10, "art25": 0.25}[kind]
    n_ep = len(x) // 3000
    eps = rng.choice(n_ep, size=max(1, int(frac * n_ep)), replace=False)
    y = x.copy()
    for e in eps:
        drift = lfilter([1.0], [1.0, -0.995], rng.normal(0, 50.0, 3000)).astype(np.float32)
        y[e * 3000:(e + 1) * 3000] += drift
    return np.clip(y, -300, 300)


def _job(args):
    p, kind = args
    n = sleep.load_night(Path(p))
    rng = np.random.default_rng(night_seed(n.night, kind))
    n2 = replace(n, eeg=corrupt(n.eeg, kind, rng).astype(np.float16),
                 eog=corrupt(n.eog, kind, rng).astype(np.float16))
    _, P, _ = yasa_features_and_proba(n2)
    d = RESULTS_DIR / "predictions" / f"yasa_{kind}" / n.cohort
    d.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(d / f"{n.night}.npz", P=P.astype(np.float32), y=n.y)
    return n.night


def _sum(args):
    P, y, sm, name, tag = args
    return name, summarise_night(P, y, sm, name, tag, M=1000, ablations=False)


def _eval_task(args):
    k, c, p, fc, ft, R = args
    rows = []
    for r in range(R):
        m = subject_split(fc["subject"].values, seed=r)
        cal_subj = set(fc["subject"].values[m])
        cal = fc[m].reset_index(drop=True)
        test = ft[~ft["subject"].isin(cal_subj)].reset_index(drop=True)
        for meth in EVAL_METHODS:
            res, _, _ = evaluate(p, meth, cal, test, 0.10)
            rows.append(dict(corruption=k, cohort=c, param=p, split=r, method=meth, **res))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cohorts", nargs="+", default=["SC", "ST", "HMC"])
    ap.add_argument("--R", type=int, default=200)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--skip-predict", action="store_true")
    a = ap.parse_args()
    meta = pd.read_csv(cache_root() / "sleep" / "nights.csv")
    meta["condition"] = meta["condition"].fillna("")
    with ProcessPoolExecutor(a.workers) as ex:
        if not a.skip_predict:
            jobs = [(str(p), k) for k in CORRUPTIONS for c in a.cohorts for p in sleep.cached_nights(cache_root(), c)]
            list(ex.map(_job, jobs, chunksize=2))
        clean = {c: load_preds("yasa", c) for c in a.cohorts}
        for k in CORRUPTIONS:
            rows = []
            for c in a.cohorts:
                cor = load_preds(f"yasa_{k}", c)
                folds = subject_folds(meta, c)
                for f in range(5):
                    tr = [n for n in clean[c] if folds[n] != f]
                    te = [n for n in cor if folds[n] == f]
                    sm = fit_source_model([clean[c][n][0] for n in tr], [clean[c][n][1] for n in tr])
                    for name, rec in ex.map(_sum, [(cor[n][0], cor[n][1], sm, n, f"yasa_{k}|xfit") for n in te]):
                        rows.append({"night": name, "cohort": c, "fold": f, **rec})
            df = pd.DataFrame(rows).merge(meta[["night", "subject", "age", "sex", "condition"]], on="night")
            df.to_csv(RESULTS_DIR / "summaries" / f"yasa_{k}_xfit.csv", index=False)
    clean_s = pd.read_csv(RESULTS_DIR / "summaries" / "yasa_xfit.csv")
    tasks = []
    for k in ["clean"] + CORRUPTIONS:
        cor_s = clean_s if k == "clean" else pd.read_csv(RESULTS_DIR / "summaries" / f"yasa_{k}_xfit.csv")
        for c in a.cohorts:
            for p in PARAMS:
                tasks.append((k, c, p, param_frame(clean_s[clean_s.cohort == c], p),
                              param_frame(cor_s[cor_s.cohort == c], p), a.R))
    with ProcessPoolExecutor(a.workers) as ex:
        rows = [r for rs in ex.map(_eval_task, tasks) for r in rs]
    out = pd.DataFrame(rows)
    out.to_csv(RESULTS_DIR / "raw" / "e09_robustness.csv.gz", index=False)
    print(out.groupby(["corruption", "method"])[["coverage", "mean_width"]].mean().round(3).to_string())


if __name__ == "__main__":
    main()
