"""E15 (revision 1): statistics for the honest end-to-end protocol (E12), the primary analysis after review.

Inputs: results/raw/e12_honest_<stager>.csv.gz (per split), e12_nights_<stager>.csv.gz (per night), e12_points_*.
(a) within-cohort summary: coverage (mean and 2.5-97.5% over repetitions), mean width, interval score.
(b) paired comparisons: per-subject mean interval score (averaged over the repetitions in which the subject was a
    test subject); proposed vs each comparator by a two-sided sign-flip permutation test of the mean difference;
    ratio of means with subject-bootstrap 95% CI; Holm within cohort x stager.
(c) scale effect at a fixed centre (same test): norm_reg_plugc vs scp_abs_cal; norm_reg_ffbs vs scp_abs_mu.
(d) easier vs harder nights (median split of plug-in accuracy per cohort): ratio proposed / DF-LoA.
(e) clinical decision thresholds: TST < 360 min, SOL > 30 min, WASO > 30 min, REML <= 15 min. A night's decision
    is "confident" when its interval lies entirely on one side of the threshold; reported: fraction confident and
    accuracy of confident decisions against the reference, per method.
(f) few-night local deployment (n_t = 10/20/30): coverage, width, P(realised coverage < 0.80), TST bias/MAE.
Outputs: results/statistics/e15_*.csv
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.statistics.stats import holm, perm_mean_paired  # noqa: E402
from src.utils import RESULTS_DIR, cache_root  # noqa: E402

PROPOSED = "norm_reg_ffbs"
COMPARATORS = ["ba_loa", "ba_reg", "scp_signed", "scp_abs_bc", "scp_abs_cal", "cqr_qr", "cqr_ffbs",
               "norm_entropy_reg", "norm_ffbs", "norm_reg_plugc"]
THRESH = {"TST": ("<", 360.0), "SOL": (">", 30.0), "WASO": (">", 30.0), "REML": ("<=", 15.0)}
OUT = RESULTS_DIR / "statistics"


def summary(st):
    d = pd.read_csv(RESULTS_DIR / "raw" / f"e12_honest_{st}.csv.gz")
    w = d[d.setting == "within"]
    g = w.groupby(["cohort", "param", "method"]).agg(
        coverage=("coverage", "mean"), cov_p025=("coverage", lambda x: np.percentile(x, 2.5)),
        cov_p975=("coverage", lambda x: np.percentile(x, 97.5)), mean_width=("mean_width", "mean"),
        interval_score=("interval_score", "mean"), n_cal=("n_cal", "mean"), n_test=("n_test", "mean")).reset_index()
    g.insert(0, "stager", st)
    loc = d[d.setting == "local"].groupby(["cohort", "n_target", "param", "method"]).agg(
        coverage=("coverage", "mean"), p_cov_lt80=("coverage", lambda x: float((x < 0.80).mean())),
        mean_width=("mean_width", "mean"), median_width=("mean_width", "median"),
        interval_score=("interval_score", "mean")).reset_index()
    loc.insert(0, "stager", st)
    return g, loc


def subject_means(st):
    n = pd.read_csv(RESULTS_DIR / "raw" / f"e12_nights_{st}.csv.gz")
    w = n[n.setting == "within"]
    return w, w.groupby(["cohort", "param", "method", "subject"])[["interval_score", "width", "covered"]].mean().reset_index()


def paired(sm, st):
    rows = []
    for (c, p), g in sm.groupby(["cohort", "param"]):
        piv = g.pivot_table(index="subject", columns="method", values="interval_score")
        for b in COMPARATORS:
            if b not in piv or PROPOSED not in piv:
                continue
            t = perm_mean_paired(piv[PROPOSED].values, piv[b].values)
            rows.append(dict(stager=st, cohort=c, param=p, comparator=b, n_subjects=t["n"], ratio=t["ratio"],
                             ratio_lo95=t["ratio_lo"], ratio_hi95=t["ratio_hi"], p=t["p"]))
        for centre, const, scaled in (("calibrated plug-in", "scp_abs_cal", "norm_reg_plugc"), ("FFBS mean", "scp_abs_mu", PROPOSED)):
            if const in piv and scaled in piv:
                t = perm_mean_paired(piv[scaled].values, piv[const].values)
                rows.append(dict(stager=st, cohort=c, param=p, comparator=f"SCALE@{centre}", n_subjects=t["n"],
                                 ratio=t["ratio"], ratio_lo95=t["ratio_lo"], ratio_hi95=t["ratio_hi"], p=t["p"]))
    df = pd.DataFrame(rows)
    df["p_holm"] = np.nan
    for (s, c, fam), g in df.assign(fam=df.comparator.str.startswith("SCALE")).groupby(["stager", "cohort", "fam"]):
        df.loc[g.index, "p_holm"] = holm(g.p.values)
    return df


def difficulty(w, st):
    meta_acc = pd.read_csv(RESULTS_DIR / "summaries" / f"{st}_xfit.csv")[["night", "cohort", "acc_plugin"]]
    meta_acc["harder"] = meta_acc.groupby("cohort")["acc_plugin"].transform(lambda x: x < x.median())
    d = w.merge(meta_acc[["night", "harder"]], on="night")
    rows = []
    for (c, p, h), g in d.groupby(["cohort", "param", "harder"]):
        m = g.groupby("method").interval_score.mean()
        if PROPOSED in m and "scp_signed" in m:
            rows.append(dict(stager=st, cohort=c, param=p, subset="harder" if h else "easier",
                             ratio_vs_dfloa=m[PROPOSED] / m["scp_signed"], ratio_vs_ba=m[PROPOSED] / m["ba_loa"]))
    return pd.DataFrame(rows)


def decisions(w, st):
    rows = []
    for p, (op, thr) in THRESH.items():
        g = w[w.param == p]
        ref_pos = {"<": g.y < thr, ">": g.y > thr, "<=": g.y <= thr}[op]
        lo_pos = {"<": g.hi < thr, ">": g.lo > thr, "<=": g.hi <= thr}[op]        # interval entirely positive
        hi_neg = {"<": g.lo >= thr, ">": g.hi <= thr, "<=": g.lo > thr}[op]       # interval entirely negative
        conf = lo_pos | hi_neg
        correct = (lo_pos & ref_pos) | (hi_neg & ~ref_pos)
        plug_pos = {"<": g.plug < thr, ">": g.plug > thr, "<=": g.plug <= thr}[op]
        dd = g.assign(conf=conf.values, correct=correct.values, plug_correct=(plug_pos == ref_pos).values, ref_pos=ref_pos.values)
        for (c, meth), gg in dd.groupby(["cohort", "method"]):
            rows.append(dict(stager=st, cohort=c, param=p, threshold=f"{p} {op} {thr:g}", method=meth,
                             prevalence=gg.ref_pos.mean(), frac_confident=gg.conf.mean(),
                             acc_confident=gg.loc[gg.conf, "correct"].mean() if gg.conf.any() else np.nan,
                             plugin_accuracy=gg.plug_correct.mean(), n=len(gg)))
    return pd.DataFrame(rows)


def points(st):
    p = pd.read_csv(RESULTS_DIR / "raw" / f"e12_points_{st}.csv.gz")
    g = p.groupby(["setting", "cohort", "n_target", "param", "estimator"]).agg(
        bias=("bias", "mean"), bias_p025=("bias", lambda x: np.percentile(x, 2.5)),
        bias_p975=("bias", lambda x: np.percentile(x, 97.5)), mae=("mae", "mean")).reset_index()
    g.insert(0, "stager", st)
    return g


def main():
    OUT.mkdir(exist_ok=True)
    out = {k: [] for k in ["summary", "local", "paired", "difficulty", "decisions", "points"]}
    for st in ["yasa", "lgbm_sc_s0"]:
        g, loc = summary(st)
        out["summary"].append(g)
        out["local"].append(loc)
        w, sm = subject_means(st)
        out["paired"].append(paired(sm, st))
        out["difficulty"].append(difficulty(w, st))
        out["decisions"].append(decisions(w, st))
        out["points"].append(points(st))
    for k, v in out.items():
        pd.concat(v, ignore_index=True).to_csv(OUT / f"e15_{k}.csv", index=False)
    pr = pd.concat(out["paired"])
    pr = pr.assign(win=pr.ratio < 1, sig_b=(pr.ratio < 1) & (pr.p_holm < 0.05), sig_w=(pr.ratio > 1) & (pr.p_holm < 0.05))
    print(pr.groupby(["stager", "comparator"]).agg(mean_ratio=("ratio", "mean"), wins=("win", "sum"),
                                                   sig_better=("sig_b", "sum"), sig_worse=("sig_w", "sum")).round(3))


if __name__ == "__main__":
    main()
