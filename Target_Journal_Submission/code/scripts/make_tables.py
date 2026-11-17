"""Generate all tables (CSV + Markdown) and manuscript_numbers.json from machine-readable results.
No number is typed by hand: the manuscript renderer reads tables/manuscript_numbers.json.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import cohen_kappa_score

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.evaluation.conformal_eval import PARAMS, PROPOSED  # noqa: E402
from src.utils import RESULTS_DIR, TABLES_DIR, cache_root  # noqa: E402

STAGERS = {"yasa": "YASA (pretrained, external)", "lgbm_sc_s0": "LightGBM-SC (in-domain)"}
METHOD_LABEL = {"ba_loa": "Bland–Altman LoA", "scp_abs": "Split conformal (constant, raw plug-in)",
                "scp_abs_bc": "Distribution-free LoA (bias-corrected constant width)",
                "scp_abs_cal": "Split conformal (constant, calibrated plug-in)",
                "norm_reg_plug": "FFBS-SD scale, raw plug-in centre", "norm_reg_plugc": "FFBS-SD scale, calibrated plug-in centre",
                "scp_abs_mu": "Split conformal (constant, FFBS centre)", "bayes_pct": "FFBS percentiles (uncalibrated)",
                "ind_pct": "Independent-epoch percentiles (uncalibrated)", "cqr_ffbs": "CQR on FFBS quantiles",
                "cqr_qr": "CQR, quantile regression", "norm_entropy_reg": "Normalised by mean entropy",
                "norm_ffbs": "Normalised by FFBS SD (unregularised)", "norm_reg_ffbs": "Proposed (FFBS-normalised)",
                "norm_reg_ind": "Ablation: independent-epoch SD", "norm_reg_ffbs1": "Ablation: tau = 1"}
COHORTS = ["SC", "ST", "HMC"]
NUM = {}


def md(df, path, floatfmt=".3f"):
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(path.with_suffix(".csv"), index=False)
    try:
        path.with_suffix(".md").write_text(df.to_markdown(index=False, floatfmt=floatfmt))
    except ImportError:
        path.with_suffix(".md").write_text(df.to_string(index=False))


def fmt_ms(x, d=1):
    return f"{np.mean(x):.{d}f} ± {np.std(x, ddof=1):.{d}f}"


# ----------------------------------------------------------------------------- Table 1
def table1():
    meta = pd.read_csv(cache_root() / "sleep" / "nights.csv")
    rows = []
    for c in COHORTS:
        m = meta[meta.cohort == c]
        r = {"Cohort": c, "Nights": len(m), "Subjects": m.subject.nunique(),
             "Age, y (mean ± SD)": fmt_ms(m.age.dropna()) if m.age.notna().any() else "not released",
             "Female nights, n": int((m.sex == "F").sum()) if m.sex.notna().any() else "not released",
             "Scored epochs": int(m.n_scored.sum())}
        tot = m[[f"n_{s}" for s in ["W", "N1", "N2", "N3", "REM"]]].sum()
        for s in ["W", "N1", "N2", "N3", "REM"]:
            r[f"{s}, %"] = round(100 * tot[f"n_{s}"] / tot.sum(), 1)
        for st, lab in STAGERS.items():
            accs, kaps, ys, ps = [], [], [], []
            for p in sorted((RESULTS_DIR / "predictions" / st / c).glob("*.npz")):
                z = np.load(p)
                y, yp = z["y"], z["P"].argmax(1)
                k = y >= 0
                accs.append(np.mean(y[k] == yp[k]))
                kaps.append(cohen_kappa_score(y[k], yp[k]))
                ys.append(y[k]); ps.append(yp[k])
            r[f"{lab}: accuracy (per night)"] = fmt_ms(accs, 3)
            r[f"{lab}: kappa (per night)"] = fmt_ms(kaps, 3)
            r[f"{lab}: pooled kappa"] = round(cohen_kappa_score(np.concatenate(ys), np.concatenate(ps)), 3)
            NUM[f"acc_{st}_{c}"] = float(np.mean(accs))
            NUM[f"kappa_{st}_{c}"] = float(np.mean(kaps))
        rows.append(r)
        NUM[f"nights_{c}"] = len(m)
        NUM[f"subjects_{c}"] = int(m.subject.nunique())
    NUM["nights_total"] = int(len(meta))
    NUM["subjects_total"] = int(meta.subject.nunique())
    NUM["epochs_total"] = int(meta.n_scored.sum())
    t = pd.DataFrame(rows).set_index("Cohort").T.reset_index().rename(columns={"index": "Characteristic"})
    md(t, TABLES_DIR / "table1_cohorts")


UNIT = {"TST": "min", "SOL": "min", "WASO": "min", "REML": "min", "N1%": "pp", "N2%": "pp", "N3%": "pp", "REM%": "pp"}
COMP = ["ba_loa", "scp_abs", "scp_abs_bc", "scp_abs_cal", "scp_abs_mu", "cqr_qr", "cqr_ffbs", "norm_entropy_reg", "norm_ffbs"]


def _splits(st):
    d = pd.read_csv(RESULTS_DIR / "raw" / f"e04_splits_{st}.csv.gz")
    return d


def table2():
    """Main within-cohort table. Coverage and width: mean over 500 subject-grouped splits. Interval-score
    ratios, 95% bootstrap CIs and significance: leave-one-subject-out (LOSO), per-subject mean interval
    scores, paired sign-flip permutation test of the mean difference, Holm-adjusted within cohort x stager.
    Ratios and stars therefore come from the same analysis."""
    rows = []
    for st in STAGERS:
        d = _splits(st)
        d = d[d.alpha == 0.10]
        g = d.groupby(["cohort", "param", "method"])[["coverage", "mean_width", "interval_score"]].mean()
        pt = pd.read_csv(RESULTS_DIR / "statistics" / f"e07_paired_tests_{st}.csv")
        for p in PARAMS:
            for c in COHORTS:
                pr = g.loc[(c, p, PROPOSED)]
                r = {"Stager": "YASA" if st == "yasa" else "LightGBM-SC", "Parameter": f"{p} ({UNIT[p]})",
                     "Cohort": c, "Coverage": f"{pr['coverage']:.3f}", "Mean width": f"{pr['mean_width']:.1f}"}
                for b, lab in (("scp_abs_bc", "IS ratio vs DF-LoA (95% CI)"), ("ba_loa", "IS ratio vs BA-LoA (95% CI)")):
                    t = pt[(pt.cohort == c) & (pt.param == p) & (pt.baseline == b)].iloc[0]
                    r[lab] = f"{t.ratio:.2f} ({t.ratio_lo95:.2f}–{t.ratio_hi95:.2f}){'*' if t.p_holm < 0.05 else ''}"
                    NUM[f"isratio_{st}_{c}_{p}_{b}"] = float(t.ratio)
                    NUM[f"pholm_{st}_{c}_{p}_{b}"] = float(t.p_holm)
                for b in ("scp_abs", "scp_abs_cal"):
                    t = pt[(pt.cohort == c) & (pt.param == p) & (pt.baseline == b)].iloc[0]
                    NUM[f"isratio_{st}_{c}_{p}_{b}"] = float(t.ratio)
                NUM[f"cov_{st}_{c}_{p}"] = float(pr["coverage"])
                NUM[f"width_{st}_{c}_{p}"] = float(pr["mean_width"])
                rows.append(r)
        cov_all = g.xs(PROPOSED, level="method")["coverage"]
        NUM[f"cov_min_{st}"] = float(cov_all.min())
        NUM[f"cov_max_{st}"] = float(cov_all.max())
        for m in ["ba_loa", "scp_abs", "scp_abs_bc", "scp_abs_cal", "cqr_qr", "cqr_ffbs", "bayes_pct", "ind_pct"]:
            cm = g.xs(m, level="method")["coverage"]
            NUM[f"cov_min_{st}_{m}"] = float(cm.min())
            NUM[f"cov_max_{st}_{m}"] = float(cm.max())
        for b in ["ba_loa", "scp_abs", "scp_abs_bc", "scp_abs_cal", "cqr_ffbs", "cqr_qr", "norm_entropy_reg",
                  "norm_reg_plugc", "norm_ffbs"]:
            sb = pt[(pt.baseline == b)]
            NUM[f"n_sig_better_vs_{b}_{st}"] = int(((sb.p_holm < 0.05) & (sb.ratio < 1)).sum())
            NUM[f"n_sig_worse_vs_{b}_{st}"] = int(((sb.p_holm < 0.05) & (sb.ratio > 1)).sum())
            NUM[f"n_lower_vs_{b}_{st}"] = int((sb.ratio < 1).sum())
            NUM[f"mean_ratio_vs_{b}_{st}"] = float(sb.ratio.mean())
            NUM[f"mean_ratio_noTST_vs_{b}_{st}"] = float(sb[sb.param != "TST"].ratio.mean())
        NUM[f"n_sig_better_vs_ba_{st}"] = NUM[f"n_sig_better_vs_ba_loa_{st}"]
        NUM[f"n_sig_worse_vs_ba_{st}"] = NUM[f"n_sig_worse_vs_ba_loa_{st}"]
        NUM[f"n_sig_better_vs_const_{st}"] = NUM[f"n_sig_better_vs_scp_abs_{st}"]
        NUM[f"n_sig_worse_vs_const_{st}"] = NUM[f"n_sig_worse_vs_scp_abs_{st}"]
    t2 = pd.DataFrame(rows)
    md(t2, TABLES_DIR / "tableS_preregistered_within")      # pre-registered cross-fitted analysis (supplement)


def table3():
    """Point estimates: bias / MAE / ICC of plug-in (raw), plug-in (locally calibrated), FFBS mean."""
    rows = []
    for st in STAGERS:
        pe = pd.read_csv(RESULTS_DIR / "statistics" / f"e07_point_estimates_{st}.csv")
        for p in PARAMS:
            for c in COHORTS:
                r = {"Stager": STAGERS[st], "Parameter": p, "Cohort": c}
                for est, lab in (("plug_in", "Plug-in"), ("plug_in_calibrated", "Calibrated plug-in"), ("ffbs_mean", "Posterior mean")):
                    e = pe[(pe.cohort == c) & (pe.param == p) & (pe.estimator == est)].iloc[0]
                    r[f"{lab} bias"] = round(e.bias, 1)
                    r[f"{lab} MAE"] = round(e.mae, 1)
                    r[f"{lab} ICC"] = round(e.icc, 2)
                    NUM[f"pe_{st}_{c}_{p}_{est}_bias"] = float(e.bias)
                    NUM[f"pe_{st}_{c}_{p}_{est}_mae"] = float(e.mae)
                    NUM[f"pe_{st}_{c}_{p}_{est}_icc"] = float(e.icc)
                for tname, key in (("test_ffbs_mean_vs_plug_in", "vs plug-in"), ("test_ffbs_mean_vs_plug_in_calibrated", "vs calibrated")):
                    t = pe[(pe.cohort == c) & (pe.param == p) & (pe.estimator == tname)]
                    if len(t):
                        r[f"p (MAE, posterior mean {key})"] = f"{t.iloc[0].p:.2g}"
                        NUM[f"pe_p_{st}_{c}_{p}_{tname}"] = float(t.iloc[0].p)
                rows.append(r)
    t = pd.DataFrame(rows)
    md(t[t.Stager == STAGERS["yasa"]], TABLES_DIR / "table3_point_estimates_yasa")
    disp = []
    for _, r in t[t.Stager == STAGERS["yasa"]].iterrows():
        disp.append({"Parameter": r.Parameter, "Cohort": r.Cohort,
                     "Plug-in": f"{r['Plug-in bias']:+.1f} ({r['Plug-in MAE']:.1f}); {r['Plug-in ICC']:.2f}",
                     "Calibrated plug-in": f"{r['Calibrated plug-in bias']:+.1f} ({r['Calibrated plug-in MAE']:.1f}); {r['Calibrated plug-in ICC']:.2f}",
                     "Posterior mean": f"{r['Posterior mean bias']:+.1f} ({r['Posterior mean MAE']:.1f}); {r['Posterior mean ICC']:.2f}",
                     "p vs plug-in": r.get("p (MAE, posterior mean vs plug-in)", ""),
                     "p vs calibrated": r.get("p (MAE, posterior mean vs calibrated)", "")})
    md(pd.DataFrame(disp), TABLES_DIR / "tableS_preregistered_point_estimates")
    md(t[t.Stager != STAGERS["yasa"]], TABLES_DIR / "tableS_preregistered_point_estimates_lgbm")


# ----------------------------------------------------------------------------- honest protocol (primary; E12/E15)
H_COMP = {"scp_signed": "Distribution-free LoA", "ba_reg": "Regression-based LoA", "ba_loa": "Bland–Altman LoA"}
SCALE_KEY = {"SCALE@calibrated plug-in": "SCALEcal", "SCALE@FFBS mean": "SCALEmu"}


def _star(p):
    return "*" if p < 0.05 else ""


def honest_tables():
    """Primary analysis after review cycle 1: every label-dependent component fitted on the calibration half only
    (E12, 50 subject-grouped 50/50 splits; statistics from E15)."""
    S = RESULTS_DIR / "statistics"
    summ = pd.read_csv(S / "e15_summary.csv")
    pr = pd.read_csv(S / "e15_paired.csv")
    pts = pd.read_csv(S / "e15_points.csv")
    loc = pd.read_csv(S / "e15_local.csv")
    rows = []
    for st in STAGERS:
        g = summ[summ.stager == st].set_index(["cohort", "param", "method"])
        t = pr[pr.stager == st]
        for p in PARAMS:
            for c in COHORTS:
                if (c, p, PROPOSED) not in g.index:
                    continue
                r0 = g.loc[(c, p, PROPOSED)]
                r = {"Stager": "YASA" if st == "yasa" else "LightGBM-SC", "Parameter": f"{p} ({UNIT[p]})", "Cohort": c,
                     "Coverage (2.5–97.5 % over splits)": f"{r0.coverage:.3f} ({r0.cov_p025:.2f}–{r0.cov_p975:.2f})",
                     "Mean width": f"{r0.mean_width:.1f}"}
                for b, lab in H_COMP.items():
                    tb = t[(t.cohort == c) & (t.param == p) & (t.comparator == b)]
                    if len(tb):
                        tb = tb.iloc[0]
                        r[f"IS ratio vs {lab} (95% CI)"] = f"{tb.ratio:.2f} ({tb.ratio_lo95:.2f}–{tb.ratio_hi95:.2f}){_star(tb.p_holm)}"
                rows.append(r)
                for m in g.xs((c, p), level=("cohort", "param")).index:
                    q = g.loc[(c, p, m)]
                    NUM[f"h_cov_{st}_{c}_{p}_{m}"] = float(q.coverage)
                    NUM[f"h_width_{st}_{c}_{p}_{m}"] = float(q.mean_width)
                    NUM[f"h_is_{st}_{c}_{p}_{m}"] = float(q.interval_score)
        gm = summ[summ.stager == st]
        for m, gg in gm.groupby("method"):
            NUM[f"h_cov_min_{st}_{m}"], NUM[f"h_cov_max_{st}_{m}"] = float(gg.coverage.min()), float(gg.coverage.max())
            NUM[f"h_covp025_min_{st}_{m}"] = float(gg.cov_p025.min())
        NUM[f"h_ncal_min_{st}"], NUM[f"h_ncal_max_{st}"] = float(gm.n_cal.min()), float(gm.n_cal.max())
        for _, r in t.iterrows():
            k = SCALE_KEY.get(r.comparator, r.comparator)
            NUM[f"h_ratio_{st}_{r.cohort}_{r.param}_{k}"] = float(r.ratio)
            NUM[f"h_ratiolo_{st}_{r.cohort}_{r.param}_{k}"] = float(r.ratio_lo95)
            NUM[f"h_ratiohi_{st}_{r.cohort}_{r.param}_{k}"] = float(r.ratio_hi95)
            NUM[f"h_pholm_{st}_{r.cohort}_{r.param}_{k}"] = float(r.p_holm)
        for comp, tc in t.groupby("comparator"):
            k = SCALE_KEY.get(comp, comp)
            NUM[f"h_n_{st}_{k}"] = int(len(tc))
            NUM[f"h_nlower_{st}_{k}"] = int((tc.ratio < 1).sum())
            NUM[f"h_nbetter_{st}_{k}"] = int(((tc.ratio < 1) & (tc.p_holm < 0.05)).sum())
            NUM[f"h_nworse_{st}_{k}"] = int(((tc.ratio > 1) & (tc.p_holm < 0.05)).sum())
            NUM[f"h_meanratio_{st}_{k}"] = float(tc.ratio.mean())
            NUM[f"h_medratio_{st}_{k}"] = float(tc.ratio.median())
            NUM[f"h_meanratio_noTST_{st}_{k}"] = float(tc[tc.param != "TST"].ratio.mean())
            NUM[f"h_meanratio_TST_{st}_{k}"] = float(tc[tc.param == "TST"].ratio.mean())
            better = tc[(tc.ratio < 1) & (tc.p_holm < 0.05)]
            worse = tc[(tc.ratio > 1) & (tc.p_holm < 0.05)]
            for nm, sub in (("better", better), ("worse", worse)):
                grp = {}
                for r in sub.itertuples():
                    grp.setdefault(r.param.replace("%", " %"), []).append(r.cohort)
                items = [f"{a} ({', '.join(b)})" for a, b in grp.items()]
                NUM[f"h_list_{nm}_{st}_{k}"] = ((", ".join(items[:-1]) + " and " + items[-1]) if len(items) > 1
                                                else ("".join(items) if items else "none"))
    t2 = pd.DataFrame(rows)
    md(t2, TABLES_DIR / "table2_within_cohort")
    md(t2[t2.Stager == "YASA"].drop(columns="Stager"), TABLES_DIR / "table2_display")
    md(t2[t2.Stager != "YASA"].drop(columns="Stager"), TABLES_DIR / "tableS_within_cohort_lgbm")
    pr_out = pr.copy()
    md(pr_out.round(4), TABLES_DIR / "tableS_honest_paired")
    md(summ.round(4), TABLES_DIR / "tableS_honest_all_methods")

    # ---- Table 3: point estimates (honest within-cohort; local deployment with 10 nights)
    rows = []
    for st in STAGERS:
        q = pts[pts.stager == st]
        for _, r in q.iterrows():
            tag = "w" if r.setting == "within" else f"l{int(r.n_target)}"
            NUM[f"h_pe_{st}_{tag}_{r.cohort}_{r.param}_{r.estimator}_bias"] = float(r.bias)
            NUM[f"h_pe_{st}_{tag}_{r.cohort}_{r.param}_{r.estimator}_mae"] = float(r.mae)
            NUM[f"h_pe_{st}_{tag}_{r.cohort}_{r.param}_{r.estimator}_biaslo"] = float(r.bias_p025)
            NUM[f"h_pe_{st}_{tag}_{r.cohort}_{r.param}_{r.estimator}_biashi"] = float(r.bias_p975)
        qi = q.set_index(["setting", "cohort", "n_target", "param", "estimator"])
        for p in PARAMS:
            for c in COHORTS:
                def cell(setting, nt, est):
                    k = (setting, c, nt, p, est)
                    if k not in qi.index:
                        return "–"
                    e = qi.loc[k]
                    return f"{e.bias:+.1f} ({e.mae:.1f})"
                rows.append({"Stager": STAGERS[st], "Parameter": f"{p} ({UNIT[p]})", "Cohort": c,
                             "Plug-in": cell("within", 0, "plug_in"),
                             "Calibrated plug-in": cell("within", 0, "plug_in_calibrated"),
                             "Posterior mean": cell("within", 0, "ffbs_mean"),
                             "Calibrated plug-in, 10 local nights": cell("local", 10, "plug_in_calibrated"),
                             "Posterior mean, 10 local nights": cell("local", 10, "ffbs_mean")})
    t3 = pd.DataFrame(rows)
    md(t3[t3.Stager == STAGERS["yasa"]].drop(columns="Stager"), TABLES_DIR / "table3_display")
    md(t3[t3.Stager != STAGERS["yasa"]].drop(columns="Stager"), TABLES_DIR / "tableS_point_estimates_lgbm")

    # ---- local deployment (few labelled target nights; everything fitted on them)
    md(loc.round(4), TABLES_DIR / "tableS_local_deployment")
    for (st, c, nt, m), g in loc.groupby(["stager", "cohort", "n_target", "method"]):
        NUM[f"h_loc_cov_{st}_{c}_{nt}_{m}"] = float(g.coverage.mean())
        NUM[f"h_loc_covmin_{st}_{c}_{nt}_{m}"] = float(g.coverage.min())
        NUM[f"h_loc_p80_{st}_{c}_{nt}_{m}"] = float(g.p_cov_lt80.median())
        NUM[f"h_loc_p80max_{st}_{c}_{nt}_{m}"] = float(g.p_cov_lt80.max())
        for _, r in g.iterrows():
            NUM[f"h_loc_cov_{st}_{c}_{nt}_{r.param}_{m}"] = float(r.coverage)
            NUM[f"h_loc_width_{st}_{c}_{nt}_{r.param}_{m}"] = float(r.mean_width)
            NUM[f"h_loc_mwidth_{st}_{c}_{nt}_{r.param}_{m}"] = float(r.median_width)
            NUM[f"h_loc_p80_{st}_{c}_{nt}_{r.param}_{m}"] = float(r.p_cov_lt80)
    for (st, m), g in loc.groupby(["stager", "method"]):
        NUM[f"h_loc_covmin_{st}_{m}"], NUM[f"h_loc_covmax_{st}_{m}"] = float(g.coverage.min()), float(g.coverage.max())
    # width relative to within-cohort width (cost of few local nights), proposed, YASA
    for st in STAGERS:
        for c in ["ST", "HMC"]:
            for nt in sorted(loc.n_target.unique()):
                rr = []
                for p in PARAMS:
                    a = NUM.get(f"h_loc_width_{st}_{c}_{nt}_{p}_{PROPOSED}")
                    b = NUM.get(f"h_width_{st}_{c}_{p}_{PROPOSED}")
                    if a is not None and b:
                        rr.append(a / b)
                if rr:
                    NUM[f"h_loc_widthratio_{st}_{c}_{nt}"] = float(np.median(rr))

    # ---- difficulty, worst-quartile coverage
    dif = pd.read_csv(S / "e15_difficulty.csv")
    md(dif.round(3), TABLES_DIR / "tableS_honest_difficulty")
    for (st, sub), g in dif.groupby(["stager", "subset"]):
        NUM[f"h_diff_{st}_{sub}_meanratio_dfloa"] = float(g.ratio_vs_dfloa.mean())
        NUM[f"h_diff_{st}_{sub}_nlower_dfloa"] = int((g.ratio_vs_dfloa < 1).sum())
        NUM[f"h_diff_{st}_{sub}_n"] = int(len(g))
        NUM[f"h_diff_{st}_{sub}_meanratio_bareg"] = float(g.ratio_vs_bareg.mean())
    q1 = pd.read_csv(S / "e15_q1coverage.csv")
    md(q1.round(3), TABLES_DIR / "tableS_honest_q1coverage")
    for (st, sub, m), g in q1.groupby(["stager", "subset", "method"]):
        NUM[f"h_q1_{st}_{sub}_{m}_min"], NUM[f"h_q1_{st}_{sub}_{m}_max"] = float(g.coverage.min()), float(g.coverage.max())
        NUM[f"h_q1_{st}_{sub}_{m}_mean"] = float(g.coverage.mean())
    for sub in q1.subset.unique():
        for m in q1.method.unique():
            g = q1[(q1.subset == sub) & (q1.method == m)]
            NUM[f"h_q1_all_{sub}_{m}_min"], NUM[f"h_q1_all_{sub}_{m}_max"] = float(g.coverage.min()), float(g.coverage.max())
            NUM[f"h_q1_all_{sub}_{m}_mean"] = float(g.coverage.mean())

    # ---- clinical decision thresholds (pooled over cohorts, weighted by test nights)
    dec = pd.read_csv(S / "e15_decisions.csv")
    md(dec.round(3), TABLES_DIR / "tableS_decisions")
    for (st, p, m), g in dec.groupby(["stager", "param", "method"]):
        w = g.n.values
        NUM[f"h_dec_{st}_{p}_{m}_frac"] = float(np.average(g.frac_confident, weights=w))
        ok = g.acc_confident.notna()
        wc = (g.frac_confident * g.n)[ok]
        NUM[f"h_dec_{st}_{p}_{m}_acc"] = float(np.average(g.acc_confident[ok], weights=wc)) if wc.sum() > 0 else None
        NUM[f"h_dec_{st}_{p}_plugacc"] = float(np.average(g.plugin_accuracy, weights=w))
        NUM[f"h_dec_{st}_{p}_prev"] = float(np.average(g.prevalence, weights=w))
        for _, r in g.iterrows():
            NUM[f"h_dec_{st}_{r.cohort}_{p}_{m}_frac"] = float(r.frac_confident)
            NUM[f"h_dec_{st}_{r.cohort}_{p}_{m}_acc"] = None if pd.isna(r.acc_confident) else float(r.acc_confident)


def sensitivity_tables():
    """Pre-registered sensitivity analyses (E13), montage sensitivity (E14), one-off costs (E10 meta)."""
    S = RESULTS_DIR / "statistics"
    f = S / "e13_spearman.csv"
    if f.exists():
        sp = pd.read_csv(f)
        md(sp.round(3), TABLES_DIR / "tableS_spearman_criterion")
        NUM["e13_spearman_met"], NUM["e13_spearman_n"] = int(sp.criterion_met.sum()), int(len(sp))
        for st, g in sp.groupby("stager"):
            NUM[f"e13_spearman_met_{st}"], NUM[f"e13_spearman_n_{st}"] = int(g.criterion_met.sum()), int(len(g))
        for p, g in sp.groupby("param"):
            NUM[f"e13_spearman_met_{p}"] = int(g.criterion_met.sum())
            NUM[f"e13_spearman_n_{p}"] = int(len(g))
        NUM["e13_spearman_min"], NUM["e13_spearman_max"] = float(sp.spearman.min()), float(sp.spearman.max())
        NUM["e13_spearman_median"] = float(sp.spearman.median())
    f = S / "e13_M.csv"
    if f.exists():
        mm = pd.read_csv(f)
        md(mm.round(4), TABLES_DIR / "tableS_M_sensitivity")
        piv = mm.pivot_table(index=["stager", "cohort", "param"], columns="M", values=["coverage", "interval_score"])
        NUM["e13_M100_maxdiff_cov"] = float((piv[("coverage", 100)] - piv[("coverage", 1000)]).abs().max())
        rat = piv[("interval_score", 100)] / piv[("interval_score", 1000)]
        NUM["e13_M100_isratio_min"], NUM["e13_M100_isratio_max"] = float(rat.min()), float(rat.max())
    f = S / "e13_calsize.csv"
    if f.exists():
        cs = pd.read_csv(f)
        md(cs.round(4), TABLES_DIR / "tableS_calsize_sensitivity")
        for (fr, m), g in cs.groupby(["cal_frac", "method"]):
            key = int(round(fr * 100))
            NUM[f"e13_cal{key}_{m}_covmin"], NUM[f"e13_cal{key}_{m}_covmax"] = float(g.coverage.min()), float(g.coverage.max())
        pv = cs.pivot_table(index=["stager", "cohort", "param", "cal_frac"], columns="method", values="interval_score")
        for fr, g in pv.groupby(level="cal_frac"):
            NUM[f"e13_cal{int(round(fr * 100))}_ratio_dfloa_median"] = float((g[PROPOSED] / g["scp_signed" if "scp_signed" in g else "scp_abs_bc"]).median())
    f = S / "e14_montage.csv"
    if f.exists():
        mo = pd.read_csv(f)
        md(mo.round(4), TABLES_DIR / "tableS_montage")
        for _, r in mo.iterrows():
            mk = r.montage.replace("-", "")
            NUM[f"e14_cov_{mk}_{r.param}_{r.method}"] = float(r.coverage)
            NUM[f"e14_bias_{mk}_{r.param}"] = float(r.plugin_bias)
            NUM[f"e14_acc_{mk}"] = float(r.mean_night_acc)
    f = RESULTS_DIR / "raw" / "e10_efficiency_meta.json"
    if f.exists():
        oo = json.loads(f.read_text()).get("one_off", {})
        for k, v in oo.items():
            NUM[f"eff_oneoff_{k}"] = float(v)
        md(pd.DataFrame([{"quantity": k, "value": v} for k, v in oo.items()]), TABLES_DIR / "tableS_efficiency_oneoff")



def supp_tables():
    # S: all methods coverage/width/interval score (500 splits), both stagers, all alphas
    allm = []
    for st in STAGERS:
        d = _splits(st)
        g = d.groupby(["alpha", "cohort", "param", "method"])[["coverage", "mean_width", "median_width", "interval_score", "spearman"]].agg(["mean", "std"])
        g.columns = [f"{a}_{b}" for a, b in g.columns]
        g = g.reset_index()
        g.insert(0, "stager", st)
        allm.append(g)
    md(pd.concat(allm), TABLES_DIR / "tableS_all_methods_within")
    # paired tests (full)
    pts = []
    for st in STAGERS:
        t = pd.read_csv(RESULTS_DIR / "statistics" / f"e07_paired_tests_{st}.csv")
        t.insert(0, "stager", st)
        pts.append(t)
    md(pd.concat(pts), TABLES_DIR / "tableS_paired_tests")
    # ablation summary (alpha 0.10, interval score ratio vs proposed, mean over cohorts)
    ab = []
    for st in STAGERS:
        d = _splits(st)
        d = d[d.alpha == 0.10]
        g = d.groupby(["cohort", "param", "method"])["interval_score"].mean().unstack("method")
        for m in ["norm_reg_ind", "norm_reg_ffbs1", "norm_ffbs", "norm_entropy_reg", "cqr_ffbs", "scp_abs_mu", "scp_abs_cal",
                  "scp_abs_bc", "norm_reg_plug", "norm_reg_plugc", "scp_abs"]:
            if m not in g:
                continue
            r = (g[m] / g[PROPOSED]).rename("ratio_to_proposed").reset_index()
            r["variant"] = m
            r["stager"] = st
            ab.append(r)
    ab = pd.concat(ab)
    md(ab, TABLES_DIR / "tableS_ablation_long")
    piv = ab.pivot_table(index=["stager", "param"], columns="variant", values="ratio_to_proposed", aggfunc="median").round(2).reset_index()
    md(piv, TABLES_DIR / "tableS_ablation_summary")
    for st in STAGERS:
        for m in ["norm_reg_ind", "norm_reg_ffbs1", "norm_ffbs", "cqr_ffbs", "scp_abs_cal", "scp_abs_mu", "norm_entropy_reg",
                  "scp_abs_bc", "norm_reg_plug", "norm_reg_plugc", "scp_abs"]:
            sub = ab[(ab.stager == st) & (ab.variant == m)]
            if len(sub):
                NUM[f"ablation_median_ratio_{st}_{m}"] = float(sub.ratio_to_proposed.median())
                for p in PARAMS:
                    NUM[f"ablation_ratio_{st}_{m}_{p}"] = float(sub[sub.param == p].ratio_to_proposed.median())
    # seeds variability (LightGBM seeds 0,1,2) for proposed
    sd = []
    for s in [0, 1, 2]:
        f = RESULTS_DIR / "raw" / f"e04_splits_lgbm_sc_s{s}.csv.gz"
        if f.exists():
            d = pd.read_csv(f)
            d = d[(d.alpha == 0.10) & (d.method.isin([PROPOSED, "scp_abs", "scp_abs_bc", "ba_loa"]))]
            g = d.groupby(["cohort", "param", "method"])[["coverage", "mean_width", "interval_score"]].mean().reset_index()
            g["seed"] = s
            sd.append(g)
    if sd:
        sd = pd.concat(sd)
        md(sd, TABLES_DIR / "tableS_seed_variability_long")
        v = sd.groupby(["cohort", "param", "method"]).agg(cov_mean=("coverage", "mean"), cov_range=("coverage", lambda x: x.max() - x.min()),
                                                          width_mean=("mean_width", "mean"), width_cv=("mean_width", lambda x: x.std(ddof=0) / x.mean())).reset_index()
        md(v.round(4), TABLES_DIR / "tableS_seed_variability")
        NUM["seed_max_cov_range"] = float(v.cov_range.max())
        NUM["seed_max_width_cv"] = float(v.width_cv.max())
        NUM["n_seeds"] = int(sd.seed.nunique())
    # sample-size sensitivity M (proposed scale computed from first 100/300/1000 draws)
    # centre x scale factorial (paired LOSO tests, same centre)
    ft = []
    for st in STAGERS:
        f = RESULTS_DIR / "statistics" / f"e07_factorial_tests_{st}.csv"
        if f.exists():
            t = pd.read_csv(f)
            t.insert(0, "stager", st)
            ft.append(t)
            for centre, key in (("raw plug-in", "raw"), ("calibrated plug-in", "cal"), ("FFBS mean", "mu")):
                tc = t[t.centre == centre]
                NUM[f"fact_better_{st}_{key}"] = int(((tc.p_holm < 0.05) & (tc.ratio < 1)).sum())
                NUM[f"fact_worse_{st}_{key}"] = int(((tc.p_holm < 0.05) & (tc.ratio > 1)).sum())
                NUM[f"fact_lower_{st}_{key}"] = int((tc.ratio < 1).sum())
                NUM[f"fact_n_{st}_{key}"] = int(len(tc))
                NUM[f"fact_median_ratio_{st}_{key}"] = float(tc.ratio.median())
                for _, r in tc.iterrows():
                    NUM[f"fact_ratio_{st}_{key}_{r.cohort}_{r.param}"] = float(r.ratio)
    if ft:
        md(pd.concat(ft), TABLES_DIR / "tableS_factorial_tests")
    # LOSO coverage + bootstrap CIs
    lc = []
    for st in STAGERS:
        t = pd.read_csv(RESULTS_DIR / "statistics" / f"e07_loso_coverage_{st}.csv")
        t.insert(0, "stager", st)
        lc.append(t)
    md(pd.concat(lc), TABLES_DIR / "tableS_loso_coverage")
    # flagging (suppress <10 events)
    fl = []
    for st in STAGERS:
        t = pd.read_csv(RESULTS_DIR / "statistics" / f"e07_flagging_{st}.csv")
        t.insert(0, "stager", st)
        t.loc[t.n_events < 10, ["auroc", "lo95", "hi95"]] = np.nan
        fl.append(t)
        for _, r in t[t.primary].iterrows():
            NUM[f"auroc_{st}_{r.cohort}_{r.param}_{r.signal}"] = None if pd.isna(r.auroc) else float(r.auroc)
            NUM[f"auroc_lo_{st}_{r.cohort}_{r.param}_{r.signal}"] = None if pd.isna(r.lo95) else float(r.lo95)
            NUM[f"auroc_hi_{st}_{r.cohort}_{r.param}_{r.signal}"] = None if pd.isna(r.hi95) else float(r.hi95)
    md(pd.concat(fl), TABLES_DIR / "tableS_flagging")
    # subgroup coverage
    sg = []
    for st in STAGERS:
        t = pd.read_csv(RESULTS_DIR / "statistics" / f"e07_subgroup_coverage_{st}.csv")
        t.insert(0, "stager", st)
        sg.append(t[t.method.isin([PROPOSED, "scp_abs", "scp_abs_bc", "ba_loa"])])
    sg = pd.concat(sg)
    md(sg, TABLES_DIR / "tableS_subgroup_coverage")
    pr = sg[(sg.method == PROPOSED) & (sg.param == "all")]
    pr = pr[pr["n_nights"] >= 20].reset_index(drop=True)          # subgroups with >= 20 distinct nights
    pp = sg[(sg.method == PROPOSED) & (sg.param != "all") & (sg["n_nights"] >= 20)]
    for fac in ["age_group", "acc_quartile"]:
        for lev in pp[pp.factor == fac].level.unique():
            v = pp[(pp.factor == fac) & (pp.level == lev)].coverage
            key = str(lev).split(" ")[0].replace(">=", "ge").replace("<", "lt").replace("-", "_")
            NUM[f"sgp_{fac}_{key}_min"], NUM[f"sgp_{fac}_{key}_max"] = float(v.min()), float(v.max())
    prn = pr[pr.factor != "acc_quartile"]
    NUM["subgroup_cov_min_noacc"], NUM["subgroup_cov_max_noacc"] = float(prn.coverage.min()), float(prn.coverage.max())
    NUM["subgroup_cov_min"] = float(pr.coverage.min())
    NUM["subgroup_cov_max"] = float(pr.coverage.max())
    NUM["subgroup_cov_min_level"] = str(pr.loc[pr.coverage.idxmin(), ["stager", "cohort", "factor", "level"]].tolist())
    # cross-cohort
    xs = []
    for st in STAGERS:
        so = pd.read_csv(RESULTS_DIR / "raw" / f"e06_source_only_{st}.csv")
        so = so[so.alpha == 0.10]
        xs.append(so)
        for _, r in so[so.method.isin([PROPOSED, "ba_loa", "scp_abs", "scp_abs_bc", "scp_abs_cal", "cqr_ffbs"])].iterrows():
            NUM[f"x_cov_{st}_{r.target}_{r.param}_{r.method}"] = float(r.coverage)
            NUM[f"x_width_{st}_{r.target}_{r.param}_{r.method}"] = float(r.mean_width)
    md(pd.concat(xs), TABLES_DIR / "tableS_cross_cohort_source_only")
    fs = []
    for st in STAGERS:
        f = pd.read_csv(RESULTS_DIR / "raw" / f"e06_fewshot_{st}.csv.gz")
        g = f.groupby(["target", "strategy", "n_target", "method", "param"])[["coverage", "mean_width", "interval_score"]].mean().reset_index()
        g.insert(0, "stager", st)
        fs.append(g)
        gg = f.groupby(["target", "strategy", "n_target", "method"])[["coverage", "mean_width"]].mean().reset_index()
        for _, r in gg.iterrows():
            NUM[f"fs_cov_{st}_{r.target}_{r.strategy}_{r.n_target}_{r.method}"] = float(r.coverage)
        # probability that coverage over test nights falls below 0.85 (risk for a single site)
        q = f.groupby(["target", "strategy", "n_target", "method"])["coverage"].apply(lambda x: float((x < 0.85).mean())).reset_index()
        for _, r in q.iterrows():
            NUM[f"fs_plow_{st}_{r.target}_{r.strategy}_{r.n_target}_{r.method}"] = float(r.coverage)
    md(pd.concat(fs), TABLES_DIR / "tableS_fewshot")
    # error analysis + cohort bias
    for st in STAGERS:
        f = RESULTS_DIR / "statistics" / f"e08_cohort_bias_{st}.csv"
        if f.exists():
            cb = pd.read_csv(f)
            md(cb, TABLES_DIR / f"tableS_cohort_bias_{st}")
            for _, r in cb.iterrows():
                NUM[f"bias_{st}_{r.cohort}_{r.param}"] = float(r.plug_bias)
    f = RESULTS_DIR / "statistics" / "e08_waso_mechanism_summary_yasa.csv"
    if f.exists():
        w = pd.read_csv(f)
        md(w, TABLES_DIR / "tableS_waso_mechanism")
        for _, r in w.iterrows():
            NUM[f"waso_fraclate_{r.cohort}"] = float(r.mean_frac_late)
            NUM[f"waso_postwake_{r.cohort}"] = float(r.median_post_awakening_wake)
            NUM[f"waso_rho_{r.cohort}"] = float(r.spearman_frac_vs_err)
    # robustness
    f = RESULTS_DIR / "raw" / "e09_robustness.csv.gz"
    if f.exists():
        r9 = pd.read_csv(f)
        g = r9.groupby(["corruption", "cohort", "param", "method"])[["coverage", "mean_width", "interval_score"]].mean().reset_index()
        md(g, TABLES_DIR / "tableS_robustness")
        gg = r9.groupby(["corruption", "method"])[["coverage", "mean_width"]].mean().reset_index()
        for _, r in gg.iterrows():
            NUM[f"rob_cov_{r.corruption}_{r.method}"] = float(r.coverage)
        g2 = r9.groupby(["corruption", "param", "method"])[["coverage", "mean_width"]].mean().reset_index()
        for _, r in g2.iterrows():
            NUM[f"rob_cov_{r.corruption}_{r.param}_{r.method}"] = float(r.coverage)
            NUM[f"rob_width_{r.corruption}_{r.param}_{r.method}"] = float(r.mean_width)
    # efficiency
    f = RESULTS_DIR / "raw" / "e10_efficiency.csv"
    if f.exists():
        e = pd.read_csv(f)
        g = e.groupby("M")[["n_epochs", "t_stager_s", "t_ffbs_s", "t_params_s", "samples_MB"]].median().reset_index()
        md(g.round(4), TABLES_DIR / "tableS_efficiency")
        for _, r in g.iterrows():
            NUM[f"eff_ffbs_s_M{int(r.M)}"] = float(r.t_ffbs_s)
            NUM[f"eff_params_s_M{int(r.M)}"] = float(r.t_params_s)
            NUM[f"eff_mb_M{int(r.M)}"] = float(r.samples_MB)
        NUM["eff_stager_s"] = float(e.t_stager_s.median())
        meta = json.loads((RESULTS_DIR / "raw" / "e10_efficiency_meta.json").read_text())
        NUM["eff_conformal_s"] = float(meta["t_conformal_per_night_s"])
    # E11 conditional coverage (exploratory Mondrian)
    f = RESULTS_DIR / "statistics" / "e11_conditional_summary.csv"
    if f.exists():
        c11a = pd.read_csv(f)
        md(c11a.round(4), TABLES_DIR / "tableS_conditional_coverage")
        pq = c11a[(c11a.param != "all") & (c11a.subset == "Q1 (worst)")]
        for meth in ["proposed", "dfloa", "mondrian_entropy"]:
            v = pq[pq.method == meth].coverage
            NUM[f"q1cov_param_min_{meth}"], NUM[f"q1cov_param_max_{meth}"] = float(v.min()), float(v.max())
        c11 = c11a[c11a.param == "all"]
        w = c11[c11.subset == "Q1 (worst)"]
        for meth in ["proposed", "dfloa", "mondrian_entropy", "mondrian_sd"]:
            v = w[w.method == meth].coverage
            NUM[f"q1cov_min_{meth}"], NUM[f"q1cov_max_{meth}"] = float(v.min()), float(v.max())
            for _, r in w[w.method == meth].iterrows():
                NUM[f"q1cov_{r.stager}_{r.cohort}_{meth}"] = float(r.coverage)
        b = c11[c11.subset == "Q4 (best)"]
        for meth in ["proposed", "dfloa"]:
            v = b[b.method == meth].coverage
            NUM[f"q4cov_min_{meth}"], NUM[f"q4cov_max_{meth}"] = float(v.min()), float(v.max())
        a = c11[c11.subset == "all"]
        for meth in ["mondrian_entropy"]:
            v = a[a.method == meth].coverage
            NUM[f"allcov_min_{meth}"], NUM[f"allcov_max_{meth}"] = float(v.min()), float(v.max())
        gain = (w[w.method == "mondrian_entropy"].set_index(["stager", "cohort"]).coverage
                - w[w.method == "proposed"].set_index(["stager", "cohort"]).coverage)
        NUM["mondrian_gain_min"], NUM["mondrian_gain_max"] = float(gain.min()), float(gain.max())
        NUM["mondrian_n_improved"], NUM["mondrian_n"] = int((gain > 0).sum()), int(len(gain))
    # factorial median ratio range over all centres and stagers
    meds = [v for k, v in NUM.items() if k.startswith("fact_median_ratio_")]
    if meds:
        NUM["fact_median_ratio_min"], NUM["fact_median_ratio_max"] = float(min(meds)), float(max(meds))
    # few-night recalibration: probability that realised coverage < 0.80 (median over parameters)
    for st in STAGERS:
        f = RESULTS_DIR / "raw" / f"e06_fewshot_{st}.csv.gz"
        if f.exists():
            fs6 = pd.read_csv(f)
            q = (fs6[fs6.strategy == "target"].groupby(["target", "n_target", "method", "param"])["coverage"]
                 .apply(lambda x: float((x < 0.80).mean())).reset_index())
            g = q.groupby(["target", "n_target", "method"])["coverage"].median().reset_index()
            for _, r in g.iterrows():
                NUM[f"fs_p80_{st}_{r.target}_{r.n_target}_{r.method}"] = float(r.coverage)
            md(q.rename(columns={"coverage": "P(coverage<0.80)"}), TABLES_DIR / f"tableS_fewshot_risk_{st}")
    # bayes_pct coverage by parameter class (YASA)
    d = _splits("yasa")
    d = d[(d.alpha == 0.10) & (d.method == "bayes_pct")].groupby(["cohort", "param"])["coverage"].mean().reset_index()
    lat = d[d.param.isin(["SOL", "REML"])].coverage
    oth = d[~d.param.isin(["SOL", "REML"])].coverage
    NUM["bayes_lat_min"], NUM["bayes_lat_max"] = float(lat.min()), float(lat.max())
    NUM["bayes_oth_min"], NUM["bayes_oth_max"] = float(oth.min()), float(oth.max())
    # error analysis: covered vs missed
    for st in STAGERS:
        f = RESULTS_DIR / "statistics" / f"e08_noncovered_{st}.csv"
        if f.exists():
            nc = pd.read_csv(f)
            for v in ["acc_plugin", "mean_entropy"]:
                g = nc[nc.variable == v]
                NUM[f"nc_{st}_{v}_nsig"] = int((g.p < 0.05).sum())
                NUM[f"nc_{st}_{v}_ntests"] = int(g.p.notna().sum())
                NUM[f"nc_{st}_{v}_med_cov"] = float(g.median_covered.median())
                NUM[f"nc_{st}_{v}_med_missed"] = float(g.median_missed.median())
    # significant losses vs DF-LoA (list)
    for st in STAGERS:
        t = pd.read_csv(RESULTS_DIR / "statistics" / f"e07_paired_tests_{st}.csv")
        t = t[(t.baseline == "scp_abs_bc") & (t.p_holm < 0.05) & (t.mean_is_proposed > t.mean_is_baseline)]
        groups = {}
        for r in t.itertuples():
            groups.setdefault(r.param.replace("%", " %"), []).append(r.cohort)
        items = [f"{k} ({', '.join(v)})" for k, v in groups.items()]
        NUM[f"losses_vs_dfloa_{st}"] = (", ".join(items[:-1]) + " and " + items[-1]) if len(items) > 1 else "".join(items)
    # tau values
    sm = json.loads((RESULTS_DIR / "summaries" / "source_models.json").read_text())
    taus = [v for st in ["yasa", "lgbm_sc_s0"] for v in sm[st].values()]
    NUM["tau_min"], NUM["tau_max"] = float(min(taus)), float(max(taus))
    NUM["tau_median"] = float(np.median(taus))


def export_manifest_files():
    """results/raw_results.csv (per-night results, both stagers, LOSO intervals of the proposed method),
    results/metrics.json (all manuscript numbers), results/statistics.json (all hypothesis tests)."""
    rows = []
    for st in STAGERS:
        summ = pd.read_csv(RESULTS_DIR / "summaries" / f"{st}_xfit.csv")
        keep = ["night", "subject", "cohort", "age", "sex", "condition", "n_scored", "acc_plugin", "mean_entropy"]
        for p in PARAMS:
            keep += [f"ref_{p}", f"plug_{p}", f"plugc_{p}", f"ffbs_mean_{p}", f"ffbs_sd_{p}"]
        d = summ[[c for c in keep if c in summ.columns]].copy()
        loso = pd.read_csv(RESULTS_DIR / "raw" / f"e04_loso_{st}.csv")
        loso = loso[loso.method == PROPOSED].pivot_table(index="night", columns="param", values=["lo", "hi"])
        loso.columns = [f"interval_{a}_{b}" for a, b in loso.columns]
        d = d.merge(loso.reset_index(), on="night", how="left")
        d.insert(0, "stager", st)
        rows.append(d)
    pd.concat(rows).to_csv(RESULTS_DIR / "raw_results.csv", index=False)
    (RESULTS_DIR / "metrics.json").write_text(json.dumps(NUM, indent=1, default=float))
    stats = {}
    for st in STAGERS:
        for name in ["paired_tests", "factorial_tests", "point_estimates", "flagging", "loso_coverage"]:
            f = RESULTS_DIR / "statistics" / f"e07_{name}_{st}.csv"
            if f.exists():
                stats[f"{name}_{st}"] = json.loads(pd.read_csv(f).to_json(orient="records"))
    (RESULTS_DIR / "statistics.json").write_text(json.dumps(stats, indent=1))


if __name__ == "__main__":
    table1()
    for fn in (table2, table3, honest_tables, sensitivity_tables, supp_tables, export_manifest_files):
        try:
            fn()
        except FileNotFoundError as e:
            print(fn.__name__, "skipped:", e)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    p = TABLES_DIR / "manuscript_numbers.json"
    p.write_text(json.dumps(NUM, indent=2, default=float))   # fresh keys only (no stale numbers)
    print(open(TABLES_DIR / "table1_cohorts.md").read())
