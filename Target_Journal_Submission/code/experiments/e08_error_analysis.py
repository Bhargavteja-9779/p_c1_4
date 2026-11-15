"""E08 (error analysis).

(a) WASO failure mechanism: for each night, FFBS samples are regenerated (same deterministic seeds as
    E03) and the sampled final awakening is compared with the reference; we record the fraction of
    samples whose last sleep epoch lies > 60 min after the reference final awakening, and relate it to
    the posterior-mean WASO error.
(b) Non-covered nights (LOSO, proposed, alpha = 0.10): per-night descriptors of covered vs non-covered
    nights (plug-in accuracy, mean entropy, age, recording length), Mann–Whitney tests.
(c) Cohort shift of stager bias: per-cohort epoch confusion matrices of the plug-in hypnogram and
    per-cohort plug-in bias of each parameter (explains cross-cohort coverage loss).
Outputs: results/statistics/e08_*.csv
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu
from sklearn.metrics import confusion_matrix

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from e03_night_summaries import load_preds, subject_folds  # noqa: E402
from src.evaluation.conformal_eval import PARAMS, PROPOSED  # noqa: E402
from src.uncertainty import hmm  # noqa: E402
from src.uncertainty.night_summary import fit_source_model, night_seed  # noqa: E402
from src.utils import RESULTS_DIR, cache_root  # noqa: E402

OUT = RESULTS_DIR / "statistics"


def waso_mechanism(stager="yasa"):
    meta = pd.read_csv(cache_root() / "sleep" / "nights.csv")
    rows = []
    for c in ["SC", "ST", "HMC"]:
        preds = load_preds(stager, c)
        folds = subject_folds(meta, c)
        for k in range(5):
            tr = [n for n in preds if folds[n] != k]
            sm = fit_source_model([preds[n][0] for n in tr], [preds[n][1] for n in tr])
            for n in [n for n in preds if folds[n] == k]:
                P, y = preds[n]
                mask = y >= 0
                Pc = sm.cal.transform(np.log(np.clip(P, 1e-12, 1)))
                S = hmm.ffbs_sample(Pc, sm.pi_s, sm.A, sm.p0, sm.tau, 1000,
                                    np.random.default_rng(night_seed(n, f"{stager}|xfit")))
                sl_ref = np.where((y > 0) & mask)[0]
                if len(sl_ref) == 0:
                    continue
                last_ref = sl_ref[-1]
                sl = (S > 0) & mask[None, :]
                last = np.where(sl.any(1), len(y) - 1 - sl[:, ::-1].argmax(1), -1)
                post_wake_ref = (len(y) - 1 - last_ref) * 0.5
                rows.append(dict(cohort=c, night=n, post_awakening_wake_min=post_wake_ref,
                                 frac_late_final_awakening=float(np.mean((last - last_ref) * 0.5 > 60)),
                                 median_shift_final_awakening_min=float(np.median((last - last_ref) * 0.5))))
    df = pd.DataFrame(rows)
    summ = pd.read_csv(RESULTS_DIR / "summaries" / f"{stager}_xfit.csv")
    df = df.merge(summ[["night", "ref_WASO", "plug_WASO", "ffbs_mean_WASO"]], on="night")
    df["err_ffbs_WASO"] = df.ffbs_mean_WASO - df.ref_WASO
    df["err_plug_WASO"] = df.plug_WASO - df.ref_WASO
    df.to_csv(OUT / f"e08_waso_mechanism_{stager}.csv", index=False)
    s = df.groupby("cohort").agg(nights=("night", "count"),
                                 median_post_awakening_wake=("post_awakening_wake_min", "median"),
                                 mean_frac_late=("frac_late_final_awakening", "mean"),
                                 spearman_frac_vs_err=("frac_late_final_awakening",
                                                       lambda x: df.loc[x.index, ["frac_late_final_awakening", "err_ffbs_WASO"]].corr("spearman").iloc[0, 1]))
    s.to_csv(OUT / f"e08_waso_mechanism_summary_{stager}.csv")
    return s


def noncovered(stager):
    loso = pd.read_csv(RESULTS_DIR / "raw" / f"e04_loso_{stager}.csv")
    summ = pd.read_csv(RESULTS_DIR / "summaries" / f"{stager}_xfit.csv")
    d = loso[loso.method == PROPOSED].merge(summ[["night", "acc_plugin", "mean_entropy", "age", "n_scored"]], on="night")
    d["covered"] = (d.y >= d.lo) & (d.y <= d.hi)
    rows = []
    for (c, p), g in d.groupby(["cohort", "param"]):
        for v in ["acc_plugin", "mean_entropy", "age", "n_scored"]:
            a, b = g.loc[g.covered, v].dropna(), g.loc[~g.covered, v].dropna()
            pval = mannwhitneyu(a, b).pvalue if len(a) > 2 and len(b) > 2 else np.nan
            rows.append(dict(cohort=c, param=p, variable=v, n_covered=len(a), n_missed=len(b),
                             median_covered=a.median(), median_missed=b.median(), p=pval))
    pd.DataFrame(rows).to_csv(OUT / f"e08_noncovered_{stager}.csv", index=False)
    # nights missed in >=3 parameters
    miss = d[~d.covered].groupby(["cohort", "night"]).size().rename("n_params_missed").reset_index()
    miss = miss.merge(summ[["night", "acc_plugin", "mean_entropy", "age", "condition"]], on="night")
    miss.sort_values("n_params_missed", ascending=False).to_csv(OUT / f"e08_missed_nights_{stager}.csv", index=False)


def cohort_bias(stager):
    rows, cms = [], []
    summ = pd.read_csv(RESULTS_DIR / "summaries" / f"{stager}_xfit.csv")
    for c in ["SC", "ST", "HMC"]:
        preds = load_preds(stager, c)
        y = np.concatenate([v[1] for v in preds.values()])
        yp = np.concatenate([v[0].argmax(1) for v in preds.values()])
        m = y >= 0
        cm = confusion_matrix(y[m], yp[m], labels=range(5), normalize="true")
        for i, s in enumerate(["W", "N1", "N2", "N3", "REM"]):
            cms.append(dict(cohort=c, reference=s, **{f"pred_{t}": cm[i, j] for j, t in enumerate(["W", "N1", "N2", "N3", "REM"])}))
        sc = summ[summ.cohort == c]
        for p in PARAMS:
            dd = sc[sc.ref_has_rem.astype(bool)] if p == "REML" else sc
            e = dd[f"plug_{p}"] - dd[f"ref_{p}"]
            rows.append(dict(cohort=c, param=p, plug_bias=e.mean(), plug_sd=e.std(ddof=1)))
    pd.DataFrame(cms).to_csv(OUT / f"e08_confusion_{stager}.csv", index=False)
    pd.DataFrame(rows).to_csv(OUT / f"e08_cohort_bias_{stager}.csv", index=False)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    print(waso_mechanism("yasa"))
    for s in ["yasa", "lgbm_sc_s0"]:
        noncovered(s)
        cohort_bias(s)
    print("done")
