"""E17: independent multi-scorer validation on the Dreem Open Datasets (DOD-H: 25 healthy volunteers; DOD-O: 55 patients with
suspected sleep apnoea; five scorers per night; Guillot et al. 2020), using the same end-to-end protocol as E12.

Stager: YASA (pretrained, unchanged; C3-M2 EEG and EOG1-EOG2), probabilities extracted by `scripts/extract_dod.py`
(one night per subject; reference = scorer consensus stored in the dataset; individual scorers' hypnograms in `ys`).
Analyses
  within    : subject-grouped 50/50 calibration/test splits (R repetitions), reference = consensus; cohorts DODH, DODO, DOD (pooled).
  scorer    : on the pooled cohort, calibration with the labels of ONE reference (consensus or scorer j), intervals then tested against
              the parameter values of EVERY reference k (consensus and each scorer): does "valid" depend on whose scoring is used?
  local     : few-night deployment on DODO (n_t = 10, 20, 30 labelled nights) and DODH (n_t = 10).
  transport : intervals calibrated on all Sleep-EDF SC nights (YASA; source model fitted on SC) applied unchanged to DODH, DODO, DOD.
  agreement : inter-scorer spread of each night-level parameter (context for the width of the intervals).
Outputs: results/statistics/e17_*.csv ; per-night file results/raw/e17_nights.csv.gz (git-ignored).
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
from e12_honest_protocol import _evaluate, honest_frames, pick_subjects  # noqa: E402
from src.evaluation.conformal_eval import METHODS as ALL_METHODS, PARAMS, evaluate, param_frame, subject_split  # noqa: E402
from src.evaluation.sleep_params import compute_params, has_rem  # noqa: E402
from src.uncertainty.night_summary import fit_source_model, summarise_night  # noqa: E402
from src.utils import RESULTS_DIR  # noqa: E402

STAGER = "yasa"
COHORTS = {"DODH": ["DODH"], "DODO": ["DODO"], "DOD": ["DODH", "DODO"]}
REFS = ["cons", "s1", "s2", "s3", "s4", "s5"]
TEST_METHODS = ["norm_reg_ffbs", "scp_signed", "ba_loa", "scp_abs_cal", "scp_abs_bc"]
S, RAW = RESULTS_DIR / "statistics", RESULTS_DIR / "raw"


def load_dod(cohort):
    """night -> (P, labels by reference dict)"""
    out = {}
    for c in COHORTS[cohort]:
        d = RESULTS_DIR / "predictions" / STAGER / c
        for f in sorted(d.glob("*.npz")):
            z = np.load(f)
            out[f.stem] = (z["P"], {"cons": z["y"], **{f"s{j+1}": z["ys"][j] for j in range(5)}})
    return out


def preds_for(cohort, ref):
    return {n: (P, labs[ref]) for n, (P, labs) in load_dod(cohort).items()}


def ref_params(labs):
    y = np.where(labs >= 0, labs, 0).astype(np.int8)
    p = compute_params(y)
    rem = has_rem(labs, labs >= 0)
    return {k: (float(v) if (k != "REML" or rem) else np.nan) for k, v in p.items()}


def ref_table(cohort):
    rows = []
    for n, (P, labs) in load_dod(cohort).items():
        for r in REFS:
            for p, v in ref_params(labs[r]).items():
                rows.append((n, r, p, v))
    return pd.DataFrame(rows, columns=["night", "ref", "param", "value"])


def _task(a):
    kind, cohort, calref, key, cal_n, test_n = a
    preds = preds_for(cohort, calref)
    meta = pd.DataFrame({"night": list(preds), "subject": list(preds)})        # one night per subject
    cal_df, test_df = honest_frames(cal_n, test_n, preds, meta, f"{STAGER}|{kind}|{cohort}|{calref}|{key}")
    info = dict(stager=STAGER, setting=kind, cohort=cohort, rep=key[0], n_target=key[1], calref=calref)
    rows, pts, pn = _evaluate(cal_df, test_df, info)
    return rows, pts, [t + (calref,) for t in pn]


NIGHT_COLS = ["setting", "cohort", "rep", "n_target", "param", "method", "night", "subject", "interval_score", "width",
              "covered", "y", "lo", "hi", "plug", "plugc", "calref"]


def build_tasks(R, R_scorer):
    tasks = []
    for coh in COHORTS:
        nights = sorted(load_dod(coh))
        subj = np.array(nights)
        for r in range(R):
            m = subject_split(subj, seed=r)
            tasks.append(("within", coh, "cons", (r, 0), [n for n, k in zip(nights, m) if k], [n for n, k in zip(nights, m) if not k]))
        if coh in ("DODO", "DODH"):
            for nt in ([10, 20, 30] if coh == "DODO" else [10]):
                for r in range(R):
                    cal_n, test_n = pick_subjects(nights, subj, nt, np.random.default_rng(r))
                    tasks.append(("local", coh, "cons", (r, nt), cal_n, test_n))
    nights = sorted(load_dod("DOD"))
    subj = np.array(nights)
    for ref in REFS[1:]:                                    # scorer-specific calibration (consensus run = "within" DOD)
        for r in range(R_scorer):
            m = subject_split(subj, seed=r)
            tasks.append(("scorer", "DOD", ref, (r, 0), [n for n, k in zip(nights, m) if k], [n for n, k in zip(nights, m) if not k]))
    return tasks


def scorer_matrix(pn):
    """coverage of the intervals calibrated on reference `calref` against the parameter values of every reference."""
    pn = pn[(pn.setting.isin(["scorer", "within"])) & (pn.cohort == "DOD") & pn.method.isin(TEST_METHODS)]
    rt = ref_table("DOD")
    rows = []
    for tr in REFS:
        v = rt[rt.ref == tr].set_index(["night", "param"]).value
        key = list(zip(pn.night, pn.param))
        val = v.reindex(key).values
        ok = ~np.isnan(val)
        d = pn.assign(val=val, ok=ok)
        d = d[d.ok]
        d = d.assign(cov=(d.lo <= d.val) & (d.val <= d.hi))
        g = d.groupby(["calref", "param", "method"]).agg(coverage=("cov", "mean"), n=("cov", "size")).reset_index()
        g.insert(1, "testref", tr)
        rows.append(g)
    return pd.concat(rows)


def agreement():
    rows = []
    for coh in COHORTS:
        t = ref_table(coh)
        t = t[t.ref != "cons"].pivot_table(index=["night", "param"], columns="ref", values="value")
        for p, g in t.groupby(level="param"):
            a = g.values
            sd = np.nanstd(a, axis=1, ddof=1)
            rng = np.nanmax(a, axis=1) - np.nanmin(a, axis=1)
            rows.append(dict(cohort=coh, param=p, n=len(g), median_scorer_sd=float(np.nanmedian(sd)), median_scorer_range=float(np.nanmedian(rng)),
                             p90_scorer_range=float(np.nanpercentile(rng, 90))))
    return pd.DataFrame(rows)


def transport():
    src_df = pd.read_csv(RESULTS_DIR / "summaries" / f"{STAGER}_xfit.csv")
    src_df = src_df[src_df.cohort == "SC"]
    scp = load_preds(STAGER, "SC")
    sm = fit_source_model([v[0] for v in scp.values()], [v[1] for v in scp.values()])
    out = []
    for coh in COHORTS:
        preds = preds_for(coh, "cons")
        rows = []
        for n, (P, y) in preds.items():
            rows.append({"night": n, "cohort": coh, "subject": n, **summarise_night(P, y, sm, n, f"{STAGER}|srcSC|{coh}", M=1000, ablations=False)})
        t_df = pd.DataFrame(rows)
        for p in PARAMS:
            src, t = param_frame(src_df, p), param_frame(t_df, p)
            for meth in TEST_METHODS:
                res, lo, hi = evaluate(p, meth, src, t, 0.10)
                out.append(dict(target=coh, param=p, method=meth, n_cal=len(src), n_test=len(t), **res))
    return pd.DataFrame(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--R", type=int, default=50)
    ap.add_argument("--R_scorer", type=int, default=30)
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    tasks = build_tasks(a.R, a.R_scorer)
    rows, pts, pn = [], [], []
    with ProcessPoolExecutor(a.workers) as ex:
        for rr, pp, nn in ex.map(_task, tasks, chunksize=2):
            rows += rr; pts += pp; pn += nn
    rows, pts = pd.DataFrame(rows), pd.DataFrame(pts)
    pn = pd.DataFrame(pn, columns=NIGHT_COLS)
    rows.to_csv(RAW / "e17_rows.csv.gz", index=False)
    pts.to_csv(RAW / "e17_points.csv.gz", index=False)
    pn.to_csv(RAW / "e17_nights.csv.gz", index=False)
    summ = rows[rows.setting == "within"].groupby(["cohort", "param", "method"]).agg(
        coverage=("coverage", "mean"), cov_p025=("coverage", lambda x: np.percentile(x, 2.5)), cov_p975=("coverage", lambda x: np.percentile(x, 97.5)),
        mean_width=("mean_width", "mean"), interval_score=("interval_score", "mean"), n_cal=("n_cal", "median"), n_test=("n_test", "median"),
        inf_width=("inf_width", "mean")).reset_index()
    summ.to_csv(S / "e17_within.csv", index=False)
    loc = rows[rows.setting == "local"].assign(lt80=lambda d: d.coverage < 0.8).groupby(["cohort", "n_target", "param", "method"]).agg(
        coverage=("coverage", "mean"), p_cov_lt80=("lt80", "mean"), mean_width=("mean_width", "mean"), n_test=("n_test", "median")).reset_index()
    loc.to_csv(S / "e17_local.csv", index=False)
    pt = pts.groupby(["setting", "cohort", "n_target", "param", "estimator"]).agg(bias=("bias", "mean"), mae=("mae", "mean")).reset_index()
    pt.to_csv(S / "e17_points.csv", index=False)
    scorer_matrix(pn).to_csv(S / "e17_scorer_matrix.csv", index=False)
    agreement().to_csv(S / "e17_agreement.csv", index=False)
    transport().to_csv(S / "e17_transport.csv", index=False)
    print("E17 done")


if __name__ == "__main__":
    main()
