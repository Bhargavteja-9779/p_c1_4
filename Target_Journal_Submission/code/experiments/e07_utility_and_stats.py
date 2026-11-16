"""E07 (RQ2 inference, RQ5): paired tests, clinical utility, point-estimate agreement, error analysis.

Inputs : results/raw/e04_loso_<stager>.csv (per-night LOSO intervals, alpha = 0.10)
         results/summaries/<stager>_xfit.csv
Outputs: results/statistics/e07_paired_tests_<stager>.csv     Wilcoxon (per-subject mean interval score)
         results/statistics/e07_loso_coverage_<stager>.csv     LOSO coverage + cluster-bootstrap CI, width
         results/statistics/e07_flagging_<stager>.csv          AUROC of uncertainty signals for large errors
         results/statistics/e07_point_estimates_<stager>.csv   BA bias/LoA, MAE, ICC: plug-in vs FFBS mean
         results/statistics/e07_subgroup_coverage_<stager>.csv coverage by subgroup (proposed + baselines)
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.evaluation.conformal_eval import PARAMS, PROPOSED  # noqa: E402
from src.statistics.stats import (auroc, bland_altman, cluster_bootstrap, holm, icc_a1,  # noqa: E402
                                  perm_mean_paired, wilcoxon_paired)
from src.uncertainty.conformal import interval_score  # noqa: E402
from src.utils import RESULTS_DIR  # noqa: E402

BASELINES = ["ba_loa", "scp_abs", "scp_abs_bc", "scp_abs_cal", "scp_abs_mu", "norm_reg_plugc", "cqr_ffbs", "cqr_qr", "norm_entropy_reg", "norm_ffbs"]
# clinically relevant error thresholds (pre-registered primary: TST, REML, N3%; others secondary)
THRESH = {"TST": 30, "REML": 30, "N3%": 5, "SOL": 15, "WASO": 30, "N1%": 5, "N2%": 10, "REM%": 5}
PRIMARY_FLAG = ["TST", "REML", "N3%"]


def paired_tests(loso):
    loso = loso.copy()
    loso["is"] = interval_score(loso["y"].values, loso["lo"].values, loso["hi"].values, 0.10)
    loso["width"] = loso["hi"] - loso["lo"]
    rows = []
    for (cohort, p), g in loso.groupby(["cohort", "param"]):
        subj = g.groupby(["method", "subject"])[["is", "width"]].mean().reset_index()
        prop = subj[subj.method == PROPOSED].set_index("subject")
        for b in BASELINES:
            base = subj[subj.method == b].set_index("subject").reindex(prop.index)
            t = perm_mean_paired(prop["is"].values, base["is"].values)
            w = wilcoxon_paired(prop["is"].values, base["is"].values)
            rows.append(dict(cohort=cohort, param=p, baseline=b, n_subjects=t["n"],
                             mean_is_proposed=prop["is"].mean(), mean_is_baseline=base["is"].mean(),
                             ratio=t["ratio"], ratio_lo95=t["ratio_lo"], ratio_hi95=t["ratio_hi"],
                             mean_width_proposed=prop["width"].mean(), mean_width_baseline=base["width"].mean(),
                             mean_diff_is=t["mean_diff"], p=t["p"], p_wilcoxon=w["p"], r_rb=w["r_rb"]))
    df = pd.DataFrame(rows)
    df["p_holm"] = np.nan
    for c, g in df.groupby("cohort"):  # Holm across baselines x parameters within cohort
        df.loc[g.index, "p_holm"] = holm(g["p"].values)
    return df


FACTORIAL = [("raw plug-in", "scp_abs", "norm_reg_plug"),
             ("calibrated plug-in", "scp_abs_cal", "norm_reg_plugc"),
             ("FFBS mean", "scp_abs_mu", "norm_reg_ffbs")]


def factorial_tests(loso):
    """Effect of the FFBS-SD SCALE with the CENTRE held fixed: per centre, FFBS-scaled vs constant-width
    interval (Wilcoxon on per-subject mean LOSO interval scores; Holm across centres x parameters
    within cohort)."""
    loso = loso.copy()
    loso["is"] = interval_score(loso["y"].values, loso["lo"].values, loso["hi"].values, 0.10)
    rows = []
    for (cohort, p), g in loso.groupby(["cohort", "param"]):
        subj = g.groupby(["method", "subject"])["is"].mean().unstack("method")
        for centre, const_m, scaled_m in FACTORIAL:
            if const_m not in subj or scaled_m not in subj:
                continue
            t = perm_mean_paired(subj[scaled_m].values, subj[const_m].values)
            rows.append(dict(cohort=cohort, param=p, centre=centre, constant=const_m, scaled=scaled_m,
                             n_subjects=t["n"], mean_is_scaled=subj[scaled_m].mean(),
                             mean_is_constant=subj[const_m].mean(), ratio=t["ratio"],
                             ratio_lo95=t["ratio_lo"], ratio_hi95=t["ratio_hi"], p=t["p"]))
    df = pd.DataFrame(rows)
    df["p_holm"] = np.nan
    for c, g in df.groupby("cohort"):
        df.loc[g.index, "p_holm"] = holm(g["p"].values)
    return df


def loso_coverage(loso):
    rows = []
    loso = loso.assign(cov=(loso.y >= loso.lo) & (loso.y <= loso.hi), width=loso.hi - loso.lo)
    for (cohort, p, m), g in loso.groupby(["cohort", "param", "method"]):
        by_s = {s: gg["cov"].values for s, gg in g.groupby("subject")}
        est, lo, hi = cluster_bootstrap(by_s, lambda L: np.concatenate(L).mean(), B=1000)
        rows.append(dict(cohort=cohort, param=p, method=m, n_nights=len(g), coverage=est,
                         cov_lo95=lo, cov_hi95=hi, mean_width=g["width"].mean(),
                         median_width=g["width"].median()))
    return pd.DataFrame(rows)


def flagging(summ, loso):
    rows = []
    prop = loso[loso.method == PROPOSED][["night", "param", "lo", "hi"]]
    for cohort, dc in summ.groupby("cohort"):
        for p in PARAMS:
            d = dc.copy()
            if p == "REML":
                d = d[d.ref_has_rem.astype(bool)]
            d = d.merge(prop[prop.param == p], on="night", how="inner")
            err = np.abs(d[f"ref_{p}"] - d[f"plug_{p}"]).values
            lab = err > THRESH[p]
            signals = {"proposed_width": (d["hi"] - d["lo"]).values,
                       "ffbs_sd": d[f"ffbs_sd_{p}"].values, "ind_sd": d[f"ind_sd_{p}"].values,
                       "mean_entropy": d["mean_entropy"].values, "one_minus_maxprob": 1 - d["mean_maxprob"].values}
            for name, sc in signals.items():
                by_s = {s: (sc[d.subject.values == s], lab[d.subject.values == s]) for s in d.subject.unique()}
                est, lo, hi = cluster_bootstrap(
                    by_s, lambda L: auroc(np.concatenate([x[0] for x in L]), np.concatenate([x[1] for x in L])),
                    B=1000)
                rows.append(dict(cohort=cohort, param=p, threshold=THRESH[p], primary=p in PRIMARY_FLAG,
                                 signal=name, n=len(d), n_events=int(lab.sum()), auroc=est, lo95=lo, hi95=hi))
    return pd.DataFrame(rows)


def point_estimates(summ):
    rows = []
    for cohort, dc in summ.groupby("cohort"):
        for p in PARAMS:
            d = dc[dc.ref_has_rem.astype(bool)] if p == "REML" else dc
            ref = d[f"ref_{p}"].values
            for est_name, col in (("plug_in", f"plug_{p}"), ("plug_in_calibrated", f"plugc_{p}"),
                                  ("plug_in_hmm", f"plugh_{p}"), ("ffbs_mean", f"ffbs_mean_{p}"),
                                  ("ffbs_median", f"ffbs_q50_{p}")):
                ba = bland_altman(ref, d[col].values)
                rows.append(dict(cohort=cohort, param=p, estimator=est_name, n=len(d), **ba,
                                 icc=icc_a1(ref, d[col].values)))
            # paired test of absolute error (per-subject mean), FFBS mean vs plug-in
            ae = pd.DataFrame({"s": d.subject.values, "a": np.abs(d[f"ffbs_mean_{p}"].values - ref),
                               "b": np.abs(d[f"plug_{p}"].values - ref)}).groupby("s").mean()
            t = wilcoxon_paired(ae["a"].values, ae["b"].values)
            rows.append(dict(cohort=cohort, param=p, estimator="test_ffbs_mean_vs_plug_in", n=t["n"],
                             p=t["p"], median_diff_abs_err=t["median_diff"], r_rb=t["r_rb"]))
            ae2 = pd.DataFrame({"s": d.subject.values, "a": np.abs(d[f"ffbs_mean_{p}"].values - ref),
                                "b": np.abs(d[f"plugc_{p}"].values - ref)}).groupby("s").mean()
            t2 = wilcoxon_paired(ae2["a"].values, ae2["b"].values)
            rows.append(dict(cohort=cohort, param=p, estimator="test_ffbs_mean_vs_plug_in_calibrated", n=t2["n"],
                             p=t2["p"], median_diff_abs_err=t2["median_diff"], r_rb=t2["r_rb"]))
    return pd.DataFrame(rows)


def subgroup_coverage(summ, loso):
    m = summ[["night", "age", "sex", "condition", "acc_plugin", "cohort"]].copy()
    m["acc_quartile"] = m.groupby("cohort")["acc_plugin"].transform(
        lambda x: pd.qcut(x, 4, labels=["Q1 (worst)", "Q2", "Q3", "Q4 (best)"]))
    m["age_group"] = pd.cut(m["age"], [0, 40, 60, 120], labels=["<40", "40-59", ">=60"])
    d = loso.merge(m.drop(columns="cohort"), on="night")
    d["cov"] = (d.y >= d.lo) & (d.y <= d.hi)
    rows = []
    for col in ["acc_quartile", "age_group", "sex", "condition"]:
        dd = d[d[col].astype(str).str.len() > 0]
        for keys, by in ((["cohort", "method", col], "all"), (["cohort", "method", col, "param"], "param")):
            g = dd.groupby(keys, observed=True)
            r = g.agg(coverage=("cov", "mean"), count=("cov", "size"), n_nights=("night", "nunique")).reset_index()
            r = r.rename(columns={col: "level"})
            r["factor"] = col
            if by == "all":
                r["param"] = "all"
            rows.append(r)
    return pd.concat(rows, ignore_index=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stagers", nargs="+", default=["yasa", "lgbm_sc_s0"])
    a = ap.parse_args()
    out = RESULTS_DIR / "statistics"
    out.mkdir(parents=True, exist_ok=True)
    for s in a.stagers:
        loso = pd.read_csv(RESULTS_DIR / "raw" / f"e04_loso_{s}.csv")
        summ = pd.read_csv(RESULTS_DIR / "summaries" / f"{s}_xfit.csv")
        pt = paired_tests(loso)
        pt.to_csv(out / f"e07_paired_tests_{s}.csv", index=False)
        factorial_tests(loso).to_csv(out / f"e07_factorial_tests_{s}.csv", index=False)
        loso_coverage(loso).to_csv(out / f"e07_loso_coverage_{s}.csv", index=False)
        flagging(summ, loso).to_csv(out / f"e07_flagging_{s}.csv", index=False)
        point_estimates(summ).to_csv(out / f"e07_point_estimates_{s}.csv", index=False)
        subgroup_coverage(summ, loso).to_csv(out / f"e07_subgroup_coverage_{s}.csv", index=False)
        print(s, "done", flush=True)


if __name__ == "__main__":
    main()
