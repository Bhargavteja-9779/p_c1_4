"""E14 (review cycle 1): is the SC->HMC transport failure (N3 %) driven by the EEG montage?

YASA is re-run on HMC with the frontal derivation F4-M1 (closer to Sleep-EDF's Fpz-Cz) instead of the central
C4-M1 used in the main analysis (EOG E1-M2 in both). For both montages: plug-in bias per parameter on HMC, and
coverage/width of SC-calibrated intervals on HMC (HMM source model and conformal calibration on SC nights,
cross-fitted SC summaries taken from E03).  A remaining N3 % failure with the frontal montage would point to
population/scoring-rule differences (R&K in Sleep-EDF vs AASM in HMC) rather than the montage.
Outputs: results/predictions/yasa_f4/HMC/*.npz, results/statistics/e14_montage.csv
"""
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from e03_night_summaries import load_preds  # noqa: E402
from src.data import sleep  # noqa: E402
from src.evaluation.conformal_eval import PARAMS, evaluate, param_frame  # noqa: E402
from src.models.yasa_stager import yasa_features_and_proba  # noqa: E402
from src.uncertainty.night_summary import fit_source_model, summarise_night  # noqa: E402
from src.utils import RESULTS_DIR, cache_root  # noqa: E402


def _pred(p):
    n = sleep.load_night(Path(p))
    _, P, _ = yasa_features_and_proba(n, eeg="eeg2", eog="eog")
    d = RESULTS_DIR / "predictions" / "yasa_f4" / "HMC"
    d.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(d / f"{n.night}.npz", P=P.astype(np.float32), y=n.y)


def _summ(args):
    P, y, sm, n = args
    return n, summarise_night(P, y, sm, n, "e14", M=1000, ablations=False)


def main():
    paths = [str(p) for p in sleep.cached_nights(cache_root(), "HMC")]
    with ProcessPoolExecutor(4) as ex:
        list(ex.map(_pred, paths, chunksize=4))
    meta = pd.read_csv(cache_root() / "sleep" / "nights.csv")
    sc = load_preds("yasa", "SC")
    sm = fit_source_model([v[0] for v in sc.values()], [v[1] for v in sc.values()])
    src = pd.read_csv(RESULTS_DIR / "summaries" / "yasa_xfit.csv")
    src = src[src.cohort == "SC"]
    rows = []
    for mont, stager in (("C4-M1", "yasa"), ("F4-M1", "yasa_f4")):
        preds = load_preds(stager, "HMC")
        with ProcessPoolExecutor(4) as ex:
            recs = list(ex.map(_summ, [(P, y, sm, n) for n, (P, y) in preds.items()]))
        t = pd.DataFrame([{"night": n, **r} for n, r in recs]).merge(meta[["night", "subject"]], on="night")
        acc = float(np.mean(t.acc_plugin))
        for p in PARAMS:
            ft, fs = param_frame(t, p), param_frame(src, p)
            bias = float(np.mean(ft["plug"] - ft["y"]))
            for meth in ("ba_loa", "ba_reg", "scp_signed", "scp_abs", "scp_abs_bc", "norm_reg_ffbs"):
                res, _, _ = evaluate(p, meth, fs, ft, 0.10)
                rows.append(dict(montage=mont, param=p, method=meth, plugin_bias=bias, mean_night_acc=acc, **res))
    out = pd.DataFrame(rows)
    out.to_csv(RESULTS_DIR / "statistics" / "e14_montage.csv", index=False)
    print(out.pivot_table(index=["param"], columns=["montage", "method"], values="coverage").round(3).to_string())
    print(out.groupby(["montage", "param"])[["plugin_bias", "mean_night_acc"]].first().round(3).to_string())


if __name__ == "__main__":
    main()
