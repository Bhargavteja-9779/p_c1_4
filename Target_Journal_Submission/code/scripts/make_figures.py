"""Generate all figures from machine-readable results (PNG 300 dpi + PDF)."""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.evaluation.conformal_eval import PARAMS, PROPOSED  # noqa: E402
from src.uncertainty import hmm  # noqa: E402
from src.uncertainty.night_summary import fit_source_model, night_seed  # noqa: E402
from src.evaluation.sleep_params import compute_params  # noqa: E402
from src.utils import FIGURES_DIR, RESULTS_DIR  # noqa: E402

plt.rcParams.update({"font.size": 8, "axes.titlesize": 9, "axes.labelsize": 8, "legend.fontsize": 7,
                     "xtick.labelsize": 7, "ytick.labelsize": 7, "font.family": "DejaVu Sans",
                     "axes.spines.top": False, "axes.spines.right": False})
# colour-blind-safe palette (Okabe–Ito)
C = {"ba_loa": "#999999", "ba_reg": "#661100", "scp_signed": "#E69F00", "scp_abs": "#E69F00", "scp_abs_bc": "#E69F00", "scp_abs_cal": "#882255", "norm_reg_plugc": "#44AA99", "scp_abs_mu": "#F0E442", "cqr_qr": "#56B4E9",
     "cqr_ffbs": "#009E73", "norm_entropy_reg": "#CC79A7", "norm_ffbs": "#D55E00", PROPOSED: "#0072B2",
     "bayes_pct": "#000000", "ind_pct": "#AAAAAA"}
LAB = {"ba_loa": "Bland–Altman LoA", "ba_reg": "Regression-based LoA", "scp_signed": "Distribution-free LoA", "scp_abs": "Conformal, constant (raw centre)",
       "scp_abs_bc": "Distribution-free LoA (bias-corrected constant)", "scp_abs_cal": "Conformal, constant (calibrated centre)",
       "norm_reg_plugc": "FFBS-scaled, calibrated centre", "scp_abs_mu": "Conformal, constant (FFBS centre)",
       "cqr_qr": "CQR (quantile regression)", "cqr_ffbs": "CQR (FFBS quantiles)", "norm_entropy_reg": "Conformal, entropy-scaled",
       "norm_ffbs": "Conformal, FFBS SD (unreg.)", PROPOSED: "Proposed (FFBS-scaled)", "bayes_pct": "FFBS percentiles (uncal.)",
       "ind_pct": "Independent-epoch percentiles (uncal.)"}
STAGE_LAB = ["W", "N1", "N2", "N3", "REM"]
STAGE_Y = {0: 4, 4: 3, 1: 2, 2: 1, 3: 0}   # clinical hypnogram ordering (W top, N3 bottom)
STAGER_LAB = {"yasa": "YASA (external)", "lgbm_sc_s0": "LightGBM-SC (in-domain)"}


def save(fig, name):
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURES_DIR / f"{name}.png", dpi=300, bbox_inches="tight")
    fig.savefig(FIGURES_DIR / f"{name}.pdf", bbox_inches="tight")
    plt.close(fig)


def _hyp_y(h):
    return np.vectorize(STAGE_Y.get)(h)


def fig1_example(night="SN050", cohort="HMC", stager="yasa"):
    """Pipeline illustrated on a real night (HMC): probabilities, reference vs plug-in, FFBS samples,
    TST/REML posterior histograms with the LOSO conformal interval."""
    from experiments_loader import load_preds  # local helper (see below)
    preds = load_preds(stager, cohort)
    if night not in preds:  # quick mode uses a subset of nights
        night = sorted(preds)[0]
    P, y = preds[night]
    folds = pd.read_csv(RESULTS_DIR / "summaries" / f"{stager}_xfit.csv")
    k = int(folds.loc[folds.night == night, "fold"].iloc[0])
    tr = folds[(folds.cohort == cohort) & (folds.fold != k)].night.tolist()
    sm = fit_source_model([preds[n][0] for n in tr], [preds[n][1] for n in tr])
    Pc = sm.cal.transform(np.log(np.clip(P, 1e-12, 1)))
    S = hmm.ffbs_sample(Pc, sm.pi_s, sm.A, sm.p0, sm.tau, 1000, np.random.default_rng(night_seed(night, f"{stager}|xfit")))
    mask = y >= 0
    par = compute_params(S)   # automatic hypnograms use all analysis-window epochs (no reference mask)
    loso = pd.read_csv(RESULTS_DIR / "raw" / f"e04_loso_{stager}.csv")
    L = loso[(loso.night == night) & (loso.method == PROPOSED)].set_index("param")
    Lb = loso[(loso.night == night) & (loso.method == "ba_loa")].set_index("param")
    t = np.arange(len(y)) / 120
    fig = plt.figure(figsize=(7.2, 7.2))
    gs = fig.add_gridspec(5, 2, height_ratios=[1.2, 1, 1, 1, 1.6], hspace=0.95, wspace=0.28)
    ax = fig.add_subplot(gs[0, :])
    cols = ["#F0E442", "#56B4E9", "#0072B2", "#000080", "#D55E00"]
    order = [0, 4, 1, 2, 3]
    ax.stackplot(t, *[Pc[:, i] for i in order], colors=[cols[i] for i in order], labels=[STAGE_LAB[i] for i in order], lw=0)
    ax.set_xlim(0, t[-1]); ax.set_ylim(0, 1); ax.set_ylabel("p(stage)")
    ax.set_title("a  Calibrated epoch probabilities (hypnodensity)", loc="left")
    ax.legend(ncol=5, loc="lower right", bbox_to_anchor=(1.0, 1.0), frameon=False, fontsize=6,
              handlelength=1.2, columnspacing=0.8)
    for r, (h, lab) in enumerate([(np.where(mask, y, 0), "Reference (manual)"), (P.argmax(1), "Stager hypnogram (plug-in)")]):
        ax = fig.add_subplot(gs[1 + r, :])
        ax.step(t, _hyp_y(h), where="post", lw=0.7, color="k" if r == 0 else "#0072B2")
        ax.set_yticks([0, 1, 2, 3, 4]); ax.set_yticklabels(["N3", "N2", "N1", "REM", "W"]); ax.set_xlim(0, t[-1])
        ax.set_title(("b  " if r == 0 else "c  ") + lab, loc="left")
    ax = fig.add_subplot(gs[3, :])
    for j, off in enumerate([0, 6, 12]):
        ax.step(t, _hyp_y(S[j]) + off, where="post", lw=0.5, color=["#009E73", "#CC79A7", "#E69F00"][j])
    ax.set_yticks([2, 8, 14]); ax.set_yticklabels(["sample 1", "sample 2", "sample 3"]); ax.set_xlim(0, t[-1])
    ax.set_xlabel("Time since lights-off (h)")
    ax.set_title("d  Hypnograms drawn from the posterior by forward-filtering backward-sampling", loc="left")
    for c, p in enumerate(["TST", "REML"]):
        ax = fig.add_subplot(gs[4, c])
        v = par[p][np.isfinite(par[p])]
        ax.hist(v, bins=40, color="#BBBBBB", edgecolor="none")
        yl = ax.get_ylim()[1]
        ax.axvline(L.loc[p, "y"], color="k", lw=1.2, label="reference")
        ax.axvline(L.loc[p, "plug"], color="#0072B2", lw=1, ls="--", label="plug-in")
        ax.plot([L.loc[p, "lo"], L.loc[p, "hi"]], [yl * 1.05] * 2, color="#0072B2", lw=3, solid_capstyle="butt", label="90% interval (proposed)")
        ax.plot([Lb.loc[p, "lo"], Lb.loc[p, "hi"]], [yl * 1.15] * 2, color="#999999", lw=3, solid_capstyle="butt", label="Bland–Altman LoA")
        ax.set_ylim(0, yl * 1.25); ax.set_xlabel(f"{p} (min)"); ax.set_yticks([])
        ax.set_title(("e  " if c == 0 else "f  ") + f"Posterior of {p} and intervals", loc="left")
        if c == 0:
            ax.legend(loc="center left", frameon=False, fontsize=6, bbox_to_anchor=(0.0, 0.45))
    save(fig, "fig1_example_night")


def fig2_within(stagers=("yasa", "lgbm_sc_s0")):
    """Honest protocol (E12/E15): mean interval score of each method relative to the distribution-free LoA;
    proposed method with the 95% subject-bootstrap CI of the paired ratio."""
    meths = ["ba_loa", "ba_reg", "scp_abs_cal", "cqr_qr", "cqr_ffbs", "norm_ffbs", PROPOSED]
    summ = pd.read_csv(RESULTS_DIR / "statistics" / "e15_summary.csv")
    pr = pd.read_csv(RESULTS_DIR / "statistics" / "e15_paired.csv")
    fig, axes = plt.subplots(2, 3, figsize=(7.2, 5.0), sharey="row", sharex=True)
    for si, st in enumerate(stagers):
        g = summ[summ.stager == st]
        for ci, c in enumerate(["SC", "ST", "HMC"]):
            ax = axes[si, ci]
            gc = g[g.cohort == c]
            ref = gc[gc.method == "scp_signed"].set_index("param")["interval_score"].reindex(PARAMS)
            for mi, m in enumerate(meths):
                gm = gc[gc.method == m].set_index("param").reindex(PARAMS)
                x = np.arange(len(PARAMS)) + (mi - (len(meths) - 1) / 2) * 0.11
                y = gm["interval_score"] / ref
                if m == PROPOSED:
                    t = pr[(pr.stager == st) & (pr.cohort == c) & (pr.comparator == "scp_signed")].set_index("param").reindex(PARAMS)
                    ax.errorbar(x, t.ratio, yerr=[t.ratio - t.ratio_lo95, t.ratio_hi95 - t.ratio], fmt="D", ms=3.5,
                                color=C[m], label=LAB[m], zorder=4, elinewidth=0.8, capsize=0)
                else:
                    ax.scatter(x, y, s=10, color=C[m], label=LAB[m], zorder=3)
            ax.axhline(1, color="k", lw=0.6, ls=":")
            ax.set_yscale("log")
            ax.set_yticks([0.5, 0.7, 1, 1.4, 2]); ax.set_yticklabels(["0.5", "0.7", "1", "1.4", "2"])
            ax.minorticks_off()
            ax.set_xticks(range(len(PARAMS)))
            if si == len(stagers) - 1:
                ax.set_xticklabels(PARAMS, rotation=45, ha="right")
            ax.set_title(f"{'abcdef'[si * 3 + ci]}  {STAGER_LAB[st]} – {c}", loc="left", fontsize=8)
            if ci == 0:
                ax.set_ylabel("Interval score relative to\ndistribution-free LoA (log scale)")
    h, l = axes[0, 0].get_legend_handles_labels()
    fig.tight_layout(rect=(0, 0, 1, 0.9))
    fig.legend(h, l, loc="upper center", ncol=4, frameon=False, bbox_to_anchor=(0.5, 1.0))
    save(fig, "fig2_within_cohort_efficiency")


def fig5_adaptivity(stager="yasa"):
    """(a-c) interval width vs absolute plug-in error (LOSO, pre-specified summaries); (d) flagging AUROC;
    (e-h) decisions at clinical thresholds (honest protocol): fraction of nights with a confident decision
    (interval entirely on one side of the threshold) and accuracy of those decisions, pooled over cohorts."""
    loso = pd.read_csv(RESULTS_DIR / "raw" / f"e04_loso_{stager}.csv")
    fl = pd.read_csv(RESULTS_DIR / "statistics" / f"e07_flagging_{stager}.csv")
    dec = pd.read_csv(RESULTS_DIR / "statistics" / "e15_decisions.csv")
    fig = plt.figure(figsize=(7.2, 5.2))
    gs = fig.add_gridspec(2, 4, width_ratios=[1, 1, 1, 1.25], hspace=0.95, wspace=0.62)
    for i, p in enumerate(["TST", "REML", "N3%"]):
        ax = fig.add_subplot(gs[0, i])
        d = loso[(loso.param == p) & (loso.method == PROPOSED)]
        for c, mk in zip(["SC", "ST", "HMC"], ["o", "s", "^"]):
            dd = d[d.cohort == c]
            ax.scatter(dd.hi - dd.lo, np.abs(dd.y - dd.plug), s=5, alpha=0.6, marker=mk, label=c, lw=0)
        u = "pp" if p.endswith("%") else "min"
        ax.set_xlabel(f"Interval width ({u})"); ax.set_ylabel(f"|Plug-in error| ({u})")
        ax.set_title(f"{'abc'[i]}  {p}", loc="left")
        if i == 0:
            ax.legend(frameon=False, markerscale=2, fontsize=6)
    ax = fig.add_subplot(gs[0, 3])
    sig = ["proposed_width", "mean_entropy", "abs_raw_minus_calibrated"]
    sl = {"proposed_width": "Interval width (proposed)", "mean_entropy": "Mean epoch entropy",
          "abs_raw_minus_calibrated": "|raw − calibrated plug-in|"}
    sig = [x for x in sig if x in set(fl.signal)]
    f = fl[fl.primary & fl.signal.isin(sig)]
    ylab, yy, seen = [], 0, set()
    for (c, p), g in f.groupby(["cohort", "param"], sort=False):
        for s_i, sg in enumerate(sig):
            r = g[g.signal == sg]
            if len(r) and pd.notna(r.iloc[0].auroc) and r.iloc[0].n_events >= 10:   # < 10 events: not interpretable (as in S14)
                r = r.iloc[0]
                ax.errorbar(r.auroc, yy, xerr=[[r.auroc - r.lo95], [r.hi95 - r.auroc]], fmt="o", ms=3,
                            color=["#0072B2", "#CC79A7", "#999999"][s_i], label=None if sg in seen else sl[sg])
                seen.add(sg)
            yy += 1
        ylab.append((yy - 2, f"{c} {p}"))
        yy += 0.8
    ax.axvline(0.5, color="k", lw=0.6, ls=":")
    ax.set_yticks([a for a, _ in ylab]); ax.set_yticklabels([b for _, b in ylab])
    ax.set_xlabel("AUROC, clinically relevant error"); ax.set_title("d  Flagging nights", loc="left")
    h, l = ax.get_legend_handles_labels()
    ax.legend(h, l, frameon=False, fontsize=5.5, loc="upper left", bbox_to_anchor=(-0.55, -0.27), ncol=1)
    meths = ["ba_loa", "ba_reg", "scp_signed", "cqr_qr", PROPOSED]
    dd = dec[dec.stager == stager]
    YMIN = min(0.8, float(np.floor((dd.groupby("param").apply(lambda g: np.average(g.plugin_accuracy, weights=g.n)).min() - 0.03) * 20) / 20),
               float(np.floor((dd.acc_confident.min() - 0.02) * 20) / 20))
    for j, p in enumerate(["TST", "SOL", "WASO", "REML"]):
        ax = fig.add_subplot(gs[1, j])
        g = dd[dd.param == p]
        thr = g.threshold.iloc[0]
        plug = np.average(g[g.method == PROPOSED].plugin_accuracy, weights=g[g.method == PROPOSED].n)
        for m in meths:
            gm = g[g.method == m]
            if not len(gm):
                continue
            frac = np.average(gm.frac_confident, weights=gm.n)
            ok = gm.acc_confident.notna()
            acc = np.average(gm.acc_confident[ok], weights=(gm.frac_confident * gm.n)[ok]) if ok.any() else np.nan
            ax.scatter(frac, acc, s=22 if m == PROPOSED else 14, color=C[m], marker="D" if m == PROPOSED else "o",
                       label=LAB[m], zorder=3)
        ax.axhline(plug, color="k", lw=0.6, ls=":")
        ax.set_xlim(0, 1); ax.set_ylim(YMIN, 1.01)
        ax.set_xlabel("Fraction of nights decided"); ax.set_ylabel("Accuracy of decisions" if j == 0 else "")
        ax.set_title(f"{'efgh'[j]}  {thr.replace('<=', '≤')} min", loc="left")
    h, l = ax.get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=5, frameon=False, fontsize=6.5, bbox_to_anchor=(0.5, -0.05))
    save(fig, "fig5_adaptivity_decisions")


def fig3_transport(stagers=("yasa", "lgbm_sc_s0")):
    """(a, d) SC-calibrated intervals on ST/HMC (E06 source-only); (b, e) local deployment in which every
    component is fitted on n_t labelled target nights only (E12): mean coverage over parameters (range as band);
    (c, f) probability that a site's realised coverage falls below 0.80 (median over parameters)."""
    loc = pd.read_csv(RESULTS_DIR / "statistics" / "e15_local.csv")
    fig, axes = plt.subplots(2, 3, figsize=(7.2, 5.4))
    meths_src = ["ba_loa", "ba_reg", "scp_signed", "cqr_ffbs", PROPOSED]
    meths_loc = ["ba_loa", "ba_reg", "scp_signed", PROPOSED]
    for si, st in enumerate(stagers):
        so = pd.read_csv(RESULTS_DIR / "raw" / f"e06_source_only_{st}.csv")
        so = so[so.alpha == 0.10]
        ax = axes[si, 0]
        for ti, tgt in enumerate(["ST", "HMC"]):
            for mi, m in enumerate(meths_src):
                v = so[(so.target == tgt) & (so.method == m)].set_index("param").reindex(PARAMS)["coverage"]
                ax.scatter(np.arange(8) + (mi - 2) * 0.13, v, s=10, color=C[m], marker="o" if tgt == "HMC" else "x")
        ax.axhline(0.9, color="k", lw=0.6, ls=":")
        ax.set_xticks(range(8)); ax.set_xticklabels(PARAMS, rotation=45, ha="right"); ax.set_ylim(0.3, 1.02)
        ax.set_ylabel("Coverage"); ax.set_title(f"{'ad'[si]}  {STAGER_LAB[st].split(' ')[0]}: calibrated on SC", loc="left", fontsize=8)
        g = loc[loc.stager == st]
        # settings with unbounded intervals (e.g. distribution-free LoA with < 19 calibration nights) are not plotted
        bad = g[~np.isfinite(g.mean_width)].groupby(["cohort", "n_target", "method"]).size().index
        g = g[~g.set_index(["cohort", "n_target", "method"]).index.isin(bad)]
        for j, (col, ylab) in enumerate((("coverage", "Mean coverage"),
                                         ("p_cov_lt80", "P(realised coverage < 0.80)"))):
            ax = axes[si, 1 + j]
            for m in meths_loc:
                for tgt, ls in (("HMC", "-"), ("ST", "--")):
                    gg = g[(g.method == m) & (g.cohort == tgt)].groupby("n_target")[col]
                    mid = gg.mean() if col == "coverage" else gg.median()
                    ax.plot(mid.index, mid.values, ls, color=C[m], marker="o", ms=3)
                    if col == "coverage" and tgt == "HMC" and m == PROPOSED:
                        ax.fill_between(mid.index, gg.min().values, gg.max().values, color=C[m], alpha=0.10, lw=0)
            if col == "coverage":
                ax.axhline(0.9, color="k", lw=0.6, ls=":")
            ax.set_xlabel("Labelled local nights"); ax.set_ylabel(ylab)
            ax.set_xticks(sorted(g.n_target.unique()))
            ttl = "local coverage" if col == "coverage" else "site-level risk"
            ax.set_title(f"{('be' if j == 0 else 'cf')[si]}  {STAGER_LAB[st].split(' ')[0]}: {ttl}", loc="left", fontsize=8)
    from matplotlib.lines import Line2D
    hs = [Line2D([], [], color=C[m], marker="o", ls="", ms=4, label=LAB[m]) for m in meths_src]
    hs += [Line2D([], [], color="k", marker="o", ls="", ms=4, label="HMC (a, d)"),
           Line2D([], [], color="k", marker="x", ls="", ms=4, label="ST (a, d)"),
           Line2D([], [], color="k", ls="-", label="HMC (b, c, e, f)"),
           Line2D([], [], color="k", ls="--", label="ST (b, c, e, f)")]
    fig.tight_layout(rect=(0, 0.11, 1, 1))
    fig.legend(handles=hs, loc="lower center", ncol=5, frameon=False, fontsize=6, bbox_to_anchor=(0.5, 0.0))
    save(fig, "fig3_transport_local")


def fig4_robust():
    d = pd.read_csv(RESULTS_DIR / "raw" / "e09_robustness.csv.gz")
    g = d.groupby(["corruption", "method", "param"])[["coverage", "mean_width"]].mean().reset_index()
    order = ["clean", "gauss05", "gauss10", "art10", "art25"]
    lab = ["clean", "noise 0.5 SD", "noise 1.0 SD", "artefacts 10%", "artefacts 25%"]
    fig, axes = plt.subplots(2, 3, figsize=(7.2, 3.8))
    for i, p in enumerate(["TST", "WASO", "N3%"]):
        for m in ["ba_loa", "scp_signed", "scp_abs_cal", "cqr_ffbs", PROPOSED]:
            gg = g[(g.param == p) & (g.method == m)].set_index("corruption").reindex(order)
            axes[0, i].plot(range(5), gg.coverage, "-o", ms=3, color=C[m], label=LAB[m])
            axes[1, i].plot(range(5), gg.mean_width, "-o", ms=3, color=C[m])
        axes[0, i].axhline(0.9, color="k", lw=0.6, ls=":")
        axes[0, i].set_title(f"{'abc'[i]}  {p}", loc="left"); axes[0, i].set_ylabel("Coverage" if i == 0 else "")
        axes[1, i].set_ylabel("Mean width" if i == 0 else "")
        for ax in axes[:, i]:
            ax.set_xticks(range(5)); ax.set_xticklabels(lab, rotation=40, ha="right")
    h, l = axes[0, 0].get_legend_handles_labels()
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    fig.legend(h, l, loc="upper center", ncol=4, frameon=False, fontsize=6.5, bbox_to_anchor=(0.5, 1.0))
    save(fig, "fig4_robustness")


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments"))
    import importlib
    globals()["experiments_loader"] = importlib.import_module("e03_night_summaries")
    sys.modules["experiments_loader"] = globals()["experiments_loader"]
    which = sys.argv[1:] or ["1", "2", "3", "4", "5"]
    fns = {"1": fig1_example, "2": fig2_within, "3": fig3_transport, "4": fig4_robust, "5": fig5_adaptivity}
    for w in which:
        try:
            fns[w]()
            print("figure", w, "ok")
        except FileNotFoundError as e:
            print("figure", w, "skipped (missing input):", e)
