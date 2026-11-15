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
C = {"ba_loa": "#999999", "scp_abs": "#E69F00", "scp_abs_mu": "#F0E442", "cqr_qr": "#56B4E9",
     "cqr_ffbs": "#009E73", "norm_entropy_reg": "#CC79A7", "norm_ffbs": "#D55E00", PROPOSED: "#0072B2",
     "bayes_pct": "#000000", "ind_pct": "#AAAAAA"}
LAB = {"ba_loa": "Bland–Altman LoA", "scp_abs": "Conformal, constant", "scp_abs_mu": "Conformal, constant (FFBS centre)",
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
    P, y = preds[night]
    folds = pd.read_csv(RESULTS_DIR / "summaries" / f"{stager}_xfit.csv")
    k = int(folds.loc[folds.night == night, "fold"].iloc[0])
    tr = folds[(folds.cohort == cohort) & (folds.fold != k)].night.tolist()
    sm = fit_source_model([preds[n][0] for n in tr], [preds[n][1] for n in tr])
    Pc = sm.cal.transform(np.log(np.clip(P, 1e-12, 1)))
    S = hmm.ffbs_sample(Pc, sm.pi_s, sm.A, sm.p0, sm.tau, 1000, np.random.default_rng(night_seed(night, f"{stager}|xfit")))
    mask = y >= 0
    par = compute_params(S, mask)
    loso = pd.read_csv(RESULTS_DIR / "raw" / f"e04_loso_{stager}.csv")
    L = loso[(loso.night == night) & (loso.method == PROPOSED)].set_index("param")
    Lb = loso[(loso.night == night) & (loso.method == "ba_loa")].set_index("param")
    t = np.arange(len(y)) / 120
    fig = plt.figure(figsize=(7.2, 6.4))
    gs = fig.add_gridspec(5, 2, height_ratios=[1.2, 1, 1, 1, 1.6], hspace=0.65, wspace=0.28)
    ax = fig.add_subplot(gs[0, :])
    cols = ["#F0E442", "#56B4E9", "#0072B2", "#000080", "#D55E00"]
    order = [0, 4, 1, 2, 3]
    ax.stackplot(t, *[Pc[:, i] for i in order], colors=[cols[i] for i in order], labels=[STAGE_LAB[i] for i in order], lw=0)
    ax.set_xlim(0, t[-1]); ax.set_ylim(0, 1); ax.set_ylabel("p(stage)")
    ax.set_title("a  Calibrated epoch probabilities of the stager (hypnodensity)", loc="left")
    ax.legend(ncol=5, loc="upper right", bbox_to_anchor=(1, 1.45), frameon=False)
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
            ax.legend(loc="upper left", frameon=False, fontsize=6)
    save(fig, "fig1_example_night")


def fig2_within(stagers=("yasa", "lgbm_sc_s0")):
    meths = ["ba_loa", "scp_abs", "cqr_qr", "cqr_ffbs", "norm_entropy_reg", PROPOSED]
    fig, axes = plt.subplots(2, 3, figsize=(7.2, 4.6), sharey="row")
    for si, st in enumerate(stagers):
        d = pd.read_csv(RESULTS_DIR / "raw" / f"e04_splits_{st}.csv")
        d = d[d.alpha == 0.10]
        g = d.groupby(["cohort", "param", "method"])[["coverage", "interval_score", "mean_width"]].mean().reset_index()
        for ci, c in enumerate(["SC", "ST", "HMC"]):
            ax = axes[si, ci]
            gc = g[g.cohort == c]
            ref = gc[gc.method == "scp_abs"].set_index("param")["interval_score"]
            for mi, m in enumerate(meths):
                gm = gc[gc.method == m].set_index("param").reindex(PARAMS)
                x = np.arange(len(PARAMS)) + (mi - len(meths) / 2) * 0.12
                ax.scatter(x, gm["interval_score"] / ref.reindex(PARAMS), s=12, color=C[m], label=LAB[m], zorder=3,
                           marker="D" if m == PROPOSED else "o")
            ax.axhline(1, color="k", lw=0.6, ls=":")
            ax.set_xticks(range(len(PARAMS))); ax.set_xticklabels(PARAMS, rotation=45, ha="right")
            ax.set_title(f"{STAGER_LAB[st]} – {c}", loc="left")
            if ci == 0:
                ax.set_ylabel("Interval score relative to\nconstant-width conformal")
    axes[0, 0].legend(ncol=3, loc="lower left", bbox_to_anchor=(0, 1.15), frameon=False)
    fig.tight_layout()
    save(fig, "fig2_within_cohort_efficiency")


def fig3_adaptivity(stager="yasa"):
    loso = pd.read_csv(RESULTS_DIR / "raw" / f"e04_loso_{stager}.csv")
    fl = pd.read_csv(RESULTS_DIR / "statistics" / f"e07_flagging_{stager}.csv")
    fig, axes = plt.subplots(1, 4, figsize=(7.2, 2.3), gridspec_kw={"width_ratios": [1, 1, 1, 1.3]})
    for i, p in enumerate(["TST", "REML", "N3%"]):
        ax = axes[i]
        d = loso[(loso.param == p) & (loso.method == PROPOSED)]
        err = np.abs(d.y - d.plug)
        for c, mk in zip(["SC", "ST", "HMC"], ["o", "s", "^"]):
            dd = d[d.cohort == c]
            ax.scatter(dd.hi - dd.lo, np.abs(dd.y - dd.plug), s=5, alpha=0.6, marker=mk, label=c, lw=0)
        ax.set_xlabel(f"{p} interval width"); ax.set_ylabel(f"|plug-in error|" if i == 0 else "")
        ax.set_title(f"{'abc'[i]}  {p}", loc="left")
        if i == 0:
            ax.legend(frameon=False, markerscale=2)
    ax = axes[3]
    sig = ["proposed_width", "mean_entropy", "one_minus_maxprob"]
    sl = {"proposed_width": "Proposed width", "mean_entropy": "Mean entropy", "one_minus_maxprob": "1 − mean max-prob"}
    f = fl[fl.primary & fl.signal.isin(sig)]
    ylab = []
    yy = 0
    for (c, p), g in f.groupby(["cohort", "param"], sort=False):
        for s_i, s in enumerate(sig):
            r = g[g.signal == s].iloc[0]
            ax.errorbar(r.auroc, yy, xerr=[[r.auroc - r.lo95], [r.hi95 - r.auroc]], fmt="o", ms=3,
                        color=["#0072B2", "#CC79A7", "#999999"][s_i], label=sl[s] if yy < 3 else None)
            yy += 1
        ylab.append((yy - 2, f"{c} {p}"))
        yy += 0.8
    ax.axvline(0.5, color="k", lw=0.6, ls=":")
    ax.set_yticks([a for a, _ in ylab]); ax.set_yticklabels([b for _, b in ylab])
    ax.set_xlabel("AUROC for clinically relevant error"); ax.set_title("d  Flagging nights", loc="left")
    ax.legend(frameon=False, loc="lower right", fontsize=6)
    fig.tight_layout()
    save(fig, "fig3_adaptivity_flagging")


def fig4_transport(stagers=("yasa", "lgbm_sc_s0")):
    fig, axes = plt.subplots(2, 3, figsize=(7.2, 4.4))
    for si, st in enumerate(stagers):
        so = pd.read_csv(RESULTS_DIR / "raw" / f"e06_source_only_{st}.csv")
        so = so[so.alpha == 0.10]
        ax = axes[si, 0]
        meths = ["ba_loa", "scp_abs", "cqr_ffbs", PROPOSED]
        for ti, tgt in enumerate(["ST", "HMC"]):
            for mi, m in enumerate(meths):
                v = so[(so.target == tgt) & (so.method == m)].set_index("param").reindex(PARAMS)["coverage"]
                ax.scatter(np.arange(8) + (mi - 1.5) * 0.15, v, s=10, color=C[m], marker="o" if tgt == "HMC" else "x",
                           label=f"{LAB[m]}" if ti == 1 else None)
        ax.axhline(0.9, color="k", lw=0.6, ls=":")
        ax.set_xticks(range(8)); ax.set_xticklabels(PARAMS, rotation=45, ha="right"); ax.set_ylim(0.3, 1.02)
        ax.set_ylabel("Coverage"); ax.set_title(f"{'ad'[si]}  {STAGER_LAB[st]}: SC-calibrated (o HMC, x ST)", loc="left", fontsize=7)
        fs = pd.read_csv(RESULTS_DIR / "raw" / f"e06_fewshot_{st}.csv")
        for j, tgt in enumerate(["HMC", "ST"]):
            ax = axes[si, 1 + j]
            g = fs[fs.target == tgt].groupby(["strategy", "n_target", "method"])["coverage"].mean().reset_index()
            for m in ["ba_loa", "scp_abs", PROPOSED]:
                for strat, ls in (("target", "-"), ("pooled", "--")):
                    gg = g[(g.method == m) & (g.strategy == strat)]
                    ax.plot(gg.n_target, gg.coverage, ls, color=C[m], marker="o", ms=3,
                            label=f"{LAB[m]} ({strat})" if (si == 0 and j == 0) else None)
            ax.axhline(0.9, color="k", lw=0.6, ls=":")
            ax.set_xlabel("Labelled target nights"); ax.set_ylabel("Coverage (mean of 500)")
            ax.set_title(f"{'be'[si] if j == 0 else 'cf'[si]}  Recalibration on {tgt}", loc="left")
    axes[0, 0].legend(frameon=False, fontsize=5.5, loc="lower left")
    axes[0, 1].legend(frameon=False, fontsize=5.5, loc="lower right")
    fig.tight_layout()
    save(fig, "fig4_transport_recalibration")


def fig5_robust():
    d = pd.read_csv(RESULTS_DIR / "raw" / "e09_robustness.csv")
    g = d.groupby(["corruption", "method", "param"])[["coverage", "mean_width"]].mean().reset_index()
    order = ["clean", "gauss05", "gauss10", "art10", "art25"]
    lab = ["clean", "noise 0.5 SD", "noise 1.0 SD", "artefacts 10%", "artefacts 25%"]
    fig, axes = plt.subplots(2, 3, figsize=(7.2, 3.8))
    for i, p in enumerate(["TST", "WASO", "N3%"]):
        for m in ["ba_loa", "scp_abs", "cqr_ffbs", PROPOSED]:
            gg = g[(g.param == p) & (g.method == m)].set_index("corruption").reindex(order)
            axes[0, i].plot(range(5), gg.coverage, "-o", ms=3, color=C[m], label=LAB[m])
            axes[1, i].plot(range(5), gg.mean_width, "-o", ms=3, color=C[m])
        axes[0, i].axhline(0.9, color="k", lw=0.6, ls=":")
        axes[0, i].set_title(f"{'abc'[i]}  {p}", loc="left"); axes[0, i].set_ylabel("Coverage" if i == 0 else "")
        axes[1, i].set_ylabel("Mean width" if i == 0 else "")
        for ax in axes[:, i]:
            ax.set_xticks(range(5)); ax.set_xticklabels(lab, rotation=40, ha="right")
    axes[0, 0].legend(frameon=False, fontsize=6)
    fig.tight_layout()
    save(fig, "fig5_robustness")


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments"))
    import importlib
    globals()["experiments_loader"] = importlib.import_module("e03_night_summaries")
    sys.modules["experiments_loader"] = globals()["experiments_loader"]
    which = sys.argv[1:] or ["1", "2", "3", "4", "5"]
    fns = {"1": fig1_example, "2": fig2_within, "3": fig3_adaptivity, "4": fig4_transport, "5": fig5_robust}
    for w in which:
        try:
            fns[w]()
            print("figure", w, "ok")
        except FileNotFoundError as e:
            print("figure", w, "skipped (missing input):", e)
