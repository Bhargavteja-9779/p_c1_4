"""E02: base stager 2 = LightGBM trained in-domain on Sleep-EDF SC (YASA feature set).

* SC nights: out-of-fold probabilities from 5-fold cross-validation grouped by SUBJECT (both nights
  of a subject are always in the same fold -> no subject leakage).
* ST and HMC nights: model trained on all SC nights (external application; HMC also differs in
  montage: C4-M1 / E1-M2 instead of Fpz-Cz / horizontal EOG).
* Fixed hyper-parameters (chosen a priori, never tuned on evaluation nights); predefined seeds
  0, 1, 2 (seed 0 is used for the primary analysis, 1-2 for seed-variability analysis).
Outputs: results/predictions/lgbm_sc_s<seed>/<cohort>/<night>.npz with P (n x 5), y
         results/predictions/folds_sc.csv (subject -> fold)
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.utils import RESULTS_DIR, cache_root, set_seed  # noqa: E402

PARAMS = dict(n_estimators=300, learning_rate=0.05, num_leaves=63, colsample_bytree=0.5,
              subsample=0.8, subsample_freq=1, min_child_samples=50, class_weight="balanced",
              n_jobs=4, verbose=-1)
N_FOLDS = 5


def load_features(cohort):
    d = cache_root() / "features" / cohort
    out = {}
    for p in sorted(d.glob("*.npz")):
        z = np.load(p)
        out[p.stem] = (z["X"], z["y"])
    return out


def subject_folds(nights_csv: Path, seed=2026):
    meta = pd.read_csv(nights_csv)
    sc = meta[meta.cohort == "SC"]
    subj = np.array(sorted(sc.subject.unique()))
    rng = np.random.default_rng(seed)
    rng.shuffle(subj)
    fold = {s: i % N_FOLDS for i, s in enumerate(subj)}
    return {r.night: fold[r.subject] for r in sc.itertuples()}, fold


def fit(Xs, ys, seed):
    import lightgbm as lgb
    X = np.concatenate(Xs)
    y = np.concatenate(ys)
    m = y >= 0
    clf = lgb.LGBMClassifier(random_state=seed, **PARAMS)
    clf.fit(X[m], y[m])
    return clf


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    a = ap.parse_args()
    nights_csv = cache_root() / "sleep" / "nights.csv"
    night_fold, subj_fold = subject_folds(nights_csv)
    pd.Series(subj_fold, name="fold").rename_axis("subject").to_csv(RESULTS_DIR / "predictions" / "folds_sc.csv")
    feats = {c: load_features(c) for c in ["SC", "ST", "HMC"]}
    for seed in a.seeds:
        set_seed(seed)
        outdir = RESULTS_DIR / "predictions" / f"lgbm_sc_s{seed}"
        accs = {}
        for k in range(N_FOLDS):
            tr = [n for n in feats["SC"] if night_fold[n] != k]
            te = [n for n in feats["SC"] if night_fold[n] == k]
            clf = fit([feats["SC"][n][0] for n in tr], [feats["SC"][n][1] for n in tr], seed)
            for n in te:
                X, y = feats["SC"][n]
                P = clf.predict_proba(X)
                (outdir / "SC").mkdir(parents=True, exist_ok=True)
                np.savez_compressed(outdir / "SC" / f"{n}.npz", P=P.astype(np.float32), y=y)
                accs.setdefault("SC", []).append(np.mean(P[y >= 0].argmax(1) == y[y >= 0]))
        clf = fit([v[0] for v in feats["SC"].values()], [v[1] for v in feats["SC"].values()], seed)
        for c in ["ST", "HMC"]:
            (outdir / c).mkdir(parents=True, exist_ok=True)
            for n, (X, y) in feats[c].items():
                P = clf.predict_proba(X)
                np.savez_compressed(outdir / c / f"{n}.npz", P=P.astype(np.float32), y=y)
                accs.setdefault(c, []).append(np.mean(P[y >= 0].argmax(1) == y[y >= 0]))
        print(f"seed {seed}: " + ", ".join(f"{c} mean night acc={np.mean(v):.3f} (n={len(v)})" for c, v in accs.items()), flush=True)


if __name__ == "__main__":
    main()
