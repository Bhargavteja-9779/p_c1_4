"""E12 (added in review cycle 1): honest end-to-end protocol in which EVERY label-dependent component —
probability recalibration (BCTS), source prior, transition matrix, emission temperature tau and the
conformal quantile — is fitted only on the labelled calibration nights, exactly as a laboratory would
deploy the method.  Calibration-night scores are obtained by K-fold cross-fitting WITHIN the calibration
set (so they are out-of-sample); test-night summaries use the model fitted on all calibration nights.

Settings
  within : within-cohort, subject-grouped 50/50 calibration/test splits (R repetitions, seeds 0..R-1).
  local  : few-night local deployment on ST and HMC: n_t in {10, 20, 30} labelled target nights (whole
           subjects) are the ONLY labelled data; the remaining target nights are tested.  This directly
           tests the claim that a few locally scored nights correct bias and restore coverage.
Outputs: results/raw/e12_honest_<stager>.csv.gz (interval metrics), results/raw/e12_points_<stager>.csv.gz
         (point-estimate errors on test nights: raw plug-in, calibrated plug-in, FFBS mean).
"""
import argparse
import sys
import zlib
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from e03_night_summaries import load_preds  # noqa: E402
from src.evaluation.conformal_eval import PARAMS, evaluate, param_frame, subject_split  # noqa: E402
from src.uncertainty.conformal import interval_score  # noqa: E402
from src.uncertainty.night_summary import fit_source_model, summarise_night  # noqa: E402
from src.utils import RESULTS_DIR, cache_root  # noqa: E402

METHODS = ["ba_loa", "ba_reg", "cqr_qr", "scp_signed", "scp_abs_bc", "scp_abs_cal", "scp_abs_mu", "cqr_ffbs", "norm_entropy_reg",
           "norm_ffbs", "norm_reg_ffbs", "norm_reg_plugc"]
M = 1000


def _summ(nights, preds, sm, tag, meta):
    rows = []
    for n in nights:
        P, y = preds[n]
        rec = summarise_night(P, y, sm, n, tag, M=M, ablations=False)
        rows.append({"night": n, **rec})
    d = pd.DataFrame(rows)
    return d.merge(meta[["night", "subject"]], on="night", how="left")


def honest_frames(cal_nights, test_nights, preds, meta, tag, K=5):
    subj = meta.set_index("night").loc[cal_nights, "subject"].values
    us = np.array(sorted(set(subj)))
    rng = np.random.default_rng(zlib.crc32(tag.encode()))
    rng.shuffle(us)
    K = min(K, len(us))
    fold = {s: i % K for i, s in enumerate(us)}
    cal_parts = []
    for k in range(K):
        tr = [n for n, s in zip(cal_nights, subj) if fold[s] != k]
        te = [n for n, s in zip(cal_nights, subj) if fold[s] == k]
        sm = fit_source_model([preds[n][0] for n in tr], [preds[n][1] for n in tr])
        cal_parts.append(_summ(te, preds, sm, tag + f"|cf{k}", meta))
    sm_all = fit_source_model([preds[n][0] for n in cal_nights], [preds[n][1] for n in cal_nights])
    return pd.concat(cal_parts, ignore_index=True), _summ(test_nights, preds, sm_all, tag + "|test", meta)


def _evaluate(cal_df, test_df, info):
    rows, pts, per_night = [], [], []
    for p in PARAMS:
        cal, test = param_frame(cal_df, p), param_frame(test_df, p)
        if len(cal) < 3 or len(test) < 1:
            continue
        for meth in METHODS:
            res, lo, hi = evaluate(p, meth, cal, test, 0.10)
            rows.append(dict(**info, param=p, method=meth, n_cal=len(cal), n_test=len(test), **res))
            y = test["y"].values
            isc = interval_score(y, lo, hi, 0.10)
            for i in range(len(test)):
                per_night.append((info["setting"], info["cohort"], info["rep"], info["n_target"], p, meth,
                                  test["night"].iloc[i], test["subject"].iloc[i], float(isc[i]),
                                  float(hi[i] - lo[i]), bool(lo[i] <= y[i] <= hi[i]), float(y[i]),
                                  float(lo[i]), float(hi[i]), float(test["plug"].iloc[i]), float(test["plugc"].iloc[i])))
        d = test_df if p != "REML" else test_df[test_df.ref_has_rem.astype(bool)]
        for est, col in (("plug_in", f"plug_{p}"), ("plug_in_calibrated", f"plugc_{p}"), ("ffbs_mean", f"ffbs_mean_{p}")):
            e = d[col].values - d[f"ref_{p}"].values
            pts.append(dict(**info, param=p, estimator=est, bias=float(np.mean(e)), mae=float(np.mean(np.abs(e))), n=len(e)))
    return rows, pts, per_night


def _task(args):
    kind, stager, cohort, key, cal_n, test_n = args
    preds = {c: load_preds(stager, c) for c in [cohort]}[cohort]
    meta = pd.read_csv(cache_root() / "sleep" / "nights.csv")
    cal_df, test_df = honest_frames(cal_n, test_n, preds, meta, f"{stager}|{kind}|{cohort}|{key}")
    info = dict(stager=stager, setting=kind, cohort=cohort, rep=key[0], n_target=key[1])
    return _evaluate(cal_df, test_df, info)


def pick_subjects(nights, subj, n_nights, rng):
    us = np.array(sorted(set(subj)))
    rng.shuffle(us)
    chosen, tot = set(), 0
    counts = pd.Series(subj).value_counts()
    for s in us:
        if tot >= n_nights:
            break
        chosen.add(s)
        tot += counts[s]
    m = np.array([s in chosen for s in subj])
    return [n for n, k in zip(nights, m) if k], [n for n, k in zip(nights, m) if not k]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stagers", nargs="+", default=["yasa", "lgbm_sc_s0"])
    ap.add_argument("--R", type=int, default=50)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--nt", type=int, nargs="+", default=[10, 20, 30])
    a = ap.parse_args()
    meta = pd.read_csv(cache_root() / "sleep" / "nights.csv")
    for st in a.stagers:
        tasks = []
        for c in ["SC", "ST", "HMC"]:
            nights = sorted(load_preds(st, c))
            subj = meta.set_index("night").loc[nights, "subject"].values
            for r in range(a.R):
                m = subject_split(subj, seed=r)
                tasks.append(("within", st, c, (r, 0), [n for n, k in zip(nights, m) if k],
                              [n for n, k in zip(nights, m) if not k]))
            if c != "SC":
                for nt in a.nt:
                    for r in range(a.R):
                        cal_n, test_n = pick_subjects(nights, subj, nt, np.random.default_rng(r))
                        tasks.append(("local", st, c, (r, nt), cal_n, test_n))
        rows, pts, pn = [], [], []
        with ProcessPoolExecutor(a.workers) as ex:
            for rr, pp, nn in ex.map(_task, tasks, chunksize=2):
                rows += rr
                pts += pp
                pn += nn
        out = RESULTS_DIR / "raw"
        pd.DataFrame(rows).to_csv(out / f"e12_honest_{st}.csv.gz", index=False)
        pd.DataFrame(pts).to_csv(out / f"e12_points_{st}.csv.gz", index=False)
        pd.DataFrame(pn, columns=["setting", "cohort", "rep", "n_target", "param", "method", "night", "subject",
                                  "interval_score", "width", "covered", "y", "lo", "hi", "plug", "plugc"]).to_csv(out / f"e12_nights_{st}.csv.gz", index=False)
        d = pd.DataFrame(rows)
        print(st, "\n", d[d.method.isin(["ba_loa", "scp_abs_bc", "norm_reg_ffbs", "norm_ffbs"])]
              .groupby(["setting", "cohort", "n_target", "method"])["coverage"].mean().unstack("method").round(3), flush=True)


if __name__ == "__main__":
    main()
