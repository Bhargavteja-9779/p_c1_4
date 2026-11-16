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
    """Main within-cohort table: proposed coverage, width, and interval-score ratios (LOSO, Holm)."""
    rows = []
    for st in STAGERS:
        d = _splits(st)
        d = d[d.alpha == 0.10]
        g = d.groupby(["cohort", "param", "method"])[["coverage", "mean_width", "interval_score"]].mean()
        pt = pd.read_csv(RESULTS_DIR / "statistics" / f"e07_paired_tests_{st}.csv")
        for p in PARAMS:
            r = {"Stager": STAGERS[st], "Parameter": f"{p} ({UNIT[p]})"}
            for c in COHORTS:
                pr = g.loc[(c, p, PROPOSED)]
                r[f"{c} coverage"] = round(pr["coverage"], 3)
                r[f"{c} width"] = round(pr["mean_width"], 1)
                for b, lab in (("ba_loa", "vs BA-LoA"), ("scp_abs_bc", "vs DF-LoA"), ("scp_abs", "vs constant"),
                               ("scp_abs_cal", "vs constant-cal")):
                    t = pt[(pt.cohort == c) & (pt.param == p) & (pt.baseline == b)].iloc[0]
                    ratio = g.loc[(c, p, PROPOSED), "interval_score"] / g.loc[(c, p, b), "interval_score"]
                    r[f"{c} IS ratio {lab}"] = f"{ratio:.2f}{'*' if t.p_holm < 0.05 else ''}"
                    NUM[f"isratio_{st}_{c}_{p}_{b}"] = float(ratio)
                    NUM[f"pholm_{st}_{c}_{p}_{b}"] = float(t.p_holm)
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
        for b in ["scp_abs_bc", "scp_abs_cal", "cqr_ffbs", "cqr_qr", "norm_entropy_reg", "norm_reg_plugc"]:
            sb = pt[(pt.baseline == b)]
            NUM[f"n_sig_better_vs_{b}_{st}"] = int(((sb.p_holm < 0.05) & (sb.mean_is_proposed < sb.mean_is_baseline)).sum())
            NUM[f"n_sig_worse_vs_{b}_{st}"] = int(((sb.p_holm < 0.05) & (sb.mean_is_proposed > sb.mean_is_baseline)).sum())
        sig = pt[(pt.baseline == "scp_abs")]
        NUM[f"n_sig_better_vs_const_{st}"] = int(((sig.p_holm < 0.05) & (sig.mean_is_proposed < sig.mean_is_baseline)).sum())
        NUM[f"n_sig_worse_vs_const_{st}"] = int(((sig.p_holm < 0.05) & (sig.mean_is_proposed > sig.mean_is_baseline)).sum())
        sig = pt[(pt.baseline == "ba_loa")]
        NUM[f"n_sig_better_vs_ba_{st}"] = int(((sig.p_holm < 0.05) & (sig.mean_is_proposed < sig.mean_is_baseline)).sum())
        NUM[f"n_sig_worse_vs_ba_{st}"] = int(((sig.p_holm < 0.05) & (sig.mean_is_proposed > sig.mean_is_baseline)).sum())
    t2 = pd.DataFrame(rows)
    md(t2, TABLES_DIR / "table2_within_cohort")
    disp = []
    for _, r in t2.iterrows():
        d = {"Stager": "YASA" if r["Stager"].startswith("YASA") else "LightGBM-SC", "Parameter": r["Parameter"]}
        for c in COHORTS:
            d[c] = f"{r[f'{c} coverage']:.3f} | {r[f'{c} width']:.1f} | {r[f'{c} IS ratio vs DF-LoA']} | {r[f'{c} IS ratio vs BA-LoA']}"
        disp.append(d)
    md(pd.DataFrame(disp), TABLES_DIR / "table2_display")


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
    md(pd.DataFrame(disp), TABLES_DIR / "table3_display")
    md(t[t.Stager != STAGERS["yasa"]], TABLES_DIR / "tableS_point_estimates_lgbm")


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
    pr = sg[sg.method == PROPOSED]
    pr = pr[pr["count"] >= 40]
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
    for fn in (table2, table3, supp_tables, export_manifest_files):
        try:
            fn()
        except FileNotFoundError as e:
            print(fn.__name__, "skipped:", e)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    p = TABLES_DIR / "manuscript_numbers.json"
    old = json.loads(p.read_text()) if p.exists() else {}
    old.update(NUM)
    p.write_text(json.dumps(old, indent=2))
    print(open(TABLES_DIR / "table1_cohorts.md").read())
