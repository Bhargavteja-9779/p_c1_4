"""Assemble the Supplementary Material (Markdown -> DOCX) from machine-generated tables.

Numbering (referenced in the manuscript; revision 1):
  S1  Pre-specified protocol and all deviations
  S2  Honest end-to-end protocol: all methods (coverage, width, interval score; 50 splits)
  S3  Honest protocol: paired comparisons (permutation test of mean difference; Holm) incl. scale-at-fixed-centre
  S4  In-domain LightGBM stager: within-cohort table (as Table 2) and point estimates (as Table 3)
  S5  Difficulty: easier vs harder nights; coverage in the lowest-accuracy quartile; exploratory Mondrian (E11)
  S6  Local deployment with few labelled nights (E12) and pooled recalibration (E06)
  S7  Transport of SC-calibrated intervals (E06) and montage sensitivity (E14)
  S8  Clinical decision thresholds
  S9  Pre-specified cross-fitted analysis (E04/E07): all methods, paired tests, point estimates, ablations, LOSO
  S10 Pre-specified sensitivity analyses: Spearman criterion, M, calibration size, alpha, stager seeds
  S11 Subgroup coverage
  S12 Error analysis: cohort-specific bias, confusion, covered vs non-covered nights, WASO mechanism
  S13 Robustness to signal corruption
  S14 Flagging nights with clinically relevant errors
  S15 Computational cost
  S16 Datasets and data-leakage audit
  S17 Sensitivity: plain split-conformal design; site-level coverage risk vs finite-sample theory
"""
import subprocess
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.utils import _QUICK, RESULTS_DIR, ROOT_DIR, TABLES_DIR  # noqa: E402

OUT = (RESULTS_DIR / "supplementary") if _QUICK else (ROOT_DIR / "supplementary")   # never overwrite full results


def tbl(name, query=None, cols=None, round_=3, max_rows=None):
    f = TABLES_DIR / f"{name}.csv"
    if not f.exists() or f.stat().st_size < 2:
        return f"*[{name} not available]*\n"
    d = pd.read_csv(f)
    if query:
        d = d.query(query)
    if cols:
        d = d[[c for c in cols if c in d.columns]]
    d = d.round(round_)
    if max_rows is not None and len(d) > max_rows:
        d = d.head(max_rows)
    return d.to_markdown(index=False) + "\n"


def csv_tbl(path, round_=3):
    f = Path(path)
    if not f.exists():
        return f"*[{f.name} not available]*\n"
    return pd.read_csv(f).round(round_).to_markdown(index=False) + "\n"


def main():
    parts = ["---\ntitle: \"Supplementary Material\"\n---\n",
             "Supplementary material for: *Per-night prediction intervals for automatically scored sleep parameters: "
             "conformal calibration of posterior hypnogram samples compared with limits of agreement*.\n",
             "All tables were generated automatically from the result files of the analysis code "
             "(`code/run_all.py`).\n"]
    parts.append("# S1. Pre-specified protocol and deviations\n")
    parts.append((ROOT_DIR / "supplementary" / "PROTOCOL.md").read_text().replace("# ", "## ", 1))
    parts.append("\n## Deviations from the protocol and additions\n")
    parts.append((ROOT_DIR / "supplementary" / "DEVIATIONS.md").read_text())
    parts.append("\n# S2. Honest end-to-end protocol: all interval methods (α = 0.10; 50 subject-grouped 50/50 splits; "
                 "all label-dependent components fitted on the calibration half)\n")
    parts.append(tbl("tableS_honest_all_methods", None, ["stager", "cohort", "param", "method", "coverage", "cov_p025",
                                                         "cov_p975", "mean_width", "interval_score", "n_cal", "n_test"]))
    parts.append("\n# S3. Honest protocol: paired comparisons of the proposed method with each comparator\n\n"
                 "Per-subject mean interval score (averaged over the splits in which the subject was tested); ratio of means "
                 "(proposed / comparator; < 1 favours the proposed method) with subject-bootstrap 95% CI; two-sided sign-flip "
                 "permutation test of the mean difference; Holm adjustment within stager × cohort (separately for the "
                 "scale-at-fixed-centre family 'SCALE@…', which compares FFBS-SD scaling with a constant width around the same centre).\n\n")
    parts.append(tbl("tableS_honest_paired", None, ["stager", "cohort", "param", "comparator", "n_subjects", "ratio",
                                                    "ratio_lo95", "ratio_hi95", "p", "p_holm"]))
    parts.append("\n# S4. In-domain LightGBM stager\n\n**Within-cohort validity and efficiency (honest protocol; as Table 2)**\n\n")
    parts.append(tbl("tableS_within_cohort_lgbm"))
    parts.append("\n**Point estimates: bias (MAE) on test nights (as Table 3)**\n\n" + tbl("tableS_point_estimates_lgbm"))
    parts.append("\n# S5. Difficulty of nights\n\n**Interval-score ratios on easier and harder nights (median split of plug-in "
                 "accuracy within cohort; honest protocol)**\n\n")
    parts.append(tbl("tableS_honest_difficulty"))
    parts.append("\n**Coverage in the quartile of nights with the lowest plug-in accuracy (Q1) and in the other nights "
                 "(honest protocol; accuracy used only for evaluation)**\n\n")
    parts.append(tbl("tableS_honest_q1coverage", "method in ['ba_loa','ba_reg','scp_signed','cqr_qr','norm_ffbs','norm_reg_ffbs']"))
    parts.append("\n**Exploratory Mondrian calibration by mean epoch entropy (pre-specified cross-fitted summaries, LOSO)**\n\n")
    parts.append(tbl("tableS_conditional_coverage", round_=3))
    parts.append("\n# S6. Local deployment with a few labelled nights\n\n**Every component (BCTS, prior, transitions, τ, conformal "
                 "quantile) fitted only on n_t labelled local nights; 50 repetitions; P(site coverage < 0.80) = fraction of "
                 "repetitions in which the realised coverage of the remaining nights fell below 0.80**\n\n")
    parts.append(tbl("tableS_local_deployment", "method in ['ba_loa','ba_reg','scp_signed','cqr_qr','norm_ffbs','norm_reg_ffbs']"))
    parts.append("\n**Recalibration of the conformal step only, with target nights alone or pooled with SC (HMM fitted on SC; "
                 "500 repetitions)**\n\n")
    parts.append(tbl("tableS_fewshot", "method in ['ba_loa','ba_reg','scp_signed','norm_reg_ffbs']"))
    parts.append("\n# S7. Transport of SC-calibrated intervals and montage sensitivity\n")
    parts.append(tbl("tableS_cross_cohort_source_only", "method in ['ba_loa','ba_reg','scp_signed','scp_abs','scp_abs_cal','cqr_ffbs','norm_reg_ffbs','norm_reg_plugc']",
                     ["stager", "target", "param", "method", "n_cal", "n_test", "coverage", "mean_width", "interval_score"]))
    parts.append("\n**YASA on HMC with the frontal (F4-M1) versus central (C4-M1) EEG derivation; SC-calibrated intervals**\n\n")
    parts.append(tbl("tableS_montage"))
    parts.append("\n# S8. Clinical decision thresholds\n\n**A night's decision is 'confident' when its 90% interval lies "
                 "entirely on one side of the threshold; accuracy of confident decisions against the manual reference; "
                 "plug-in accuracy = agreement of the uncorrected automatic value with the reference, over all nights; plug_acc_confident / plug_acc_unconfident = the same on the nights the method decided / left undecided (honest protocol)**\n\n")
    parts.append(tbl("tableS_decisions", "method in ['ba_loa','ba_reg','scp_signed','cqr_qr','norm_ffbs','norm_reg_ffbs']",
                     ["stager", "cohort", "threshold", "method", "n", "prevalence", "plugin_accuracy", "frac_confident", "acc_confident",
                      "plug_acc_confident", "plug_acc_unconfident"]))
    parts.append("\n**Decisions compared with the recalibrated plug-in and constant-width intervals around it** "
                 "(pooled and per cohort; plug-in accuracy columns give the accuracy of the raw and the recalibrated automatic value "
                 "on all nights, on the nights this method decided and on those it left undecided)\n\n")
    parts.append(tbl("tableS_decisions_calibrated", "param == 'TST'"))
    parts.append("\n# S9. Pre-specified design: cross-fitted analysis\n\nHMM and BCTS cross-fitted within each cohort (5 subject folds), "
                 "conformal calibration on subject-grouped 50/50 splits (500 repetitions) and leave-one-subject-out. Unlike the "
                 "primary analysis, the HMM/BCTS of a test night used labels of other test-half subjects (see S1).\n\n"
                 "**All methods (α = 0.10; mean ± SD over 500 splits)**\n\n")
    parts.append(tbl("tableS_all_methods_within", "alpha == 0.1",
                     ["stager", "cohort", "param", "method", "coverage_mean", "coverage_std", "mean_width_mean",
                      "interval_score_mean", "spearman_mean"]))
    parts.append("\n**Proposed method versus comparators (LOSO; permutation test of mean per-subject difference; Holm)**\n\n")
    parts.append(tbl("tableS_prespecified_within"))
    parts.append("\n" + tbl("tableS_paired_tests", None, ["stager", "cohort", "param", "baseline", "n_subjects", "mean_is_proposed",
                                                          "mean_is_baseline", "ratio", "ratio_lo95", "ratio_hi95", "p", "p_holm", "p_wilcoxon"]))
    parts.append("\n**Point estimates (bias, MAE, ICC)**\n\n" + tbl("tableS_prespecified_point_estimates"))
    parts.append("\n" + tbl("tableS_prespecified_point_estimates_lgbm", round_=2))
    parts.append("\n**Centre × scale factorial and ablations (median ratio of interval score to the proposed method over cohorts; >1 = worse than proposed)**\n\n")
    parts.append(tbl("tableS_ablation_summary", round_=2))
    parts.append("\n**FFBS-SD scale versus constant width with the centre held fixed (LOSO; permutation test; Holm)**\n\n")
    parts.append(tbl("tableS_factorial_tests", None, ["stager", "cohort", "param", "centre", "n_subjects", "mean_is_scaled",
                                                        "mean_is_constant", "ratio", "p", "p_holm"]))
    parts.append("\n**Leave-one-subject-out coverage (descriptive; nominal by construction)**\n\n")
    parts.append(tbl("tableS_loso_coverage", "method in ['ba_loa','scp_signed','scp_abs_bc','cqr_ffbs','norm_reg_ffbs']",
                     ["stager", "cohort", "param", "method", "n_nights", "coverage", "mean_width"]))
    parts.append("\n# S10. Pre-specified sensitivity analyses\n\n**Pre-specified success criterion: Spearman correlation between "
                 "interval width and absolute error of the point estimate > 0 with 95% CI excluding 0**\n\n")
    parts.append(tbl("tableS_spearman_criterion"))
    parts.append("\n**Number of posterior samples M**\n\n" + tbl("tableS_M_sensitivity", round_=4))
    parts.append("\n**Size of the calibration set (fraction of subjects)**\n\n" + tbl("tableS_calsize_sensitivity", round_=4))
    parts.append("\n**Miscoverage level α (pre-specified analysis)**\n\n")
    parts.append(tbl("tableS_all_methods_within", "alpha != 0.1 and method in ['ba_loa','scp_signed','cqr_ffbs','norm_reg_ffbs']",
                     ["stager", "alpha", "cohort", "param", "method", "coverage_mean", "mean_width_mean", "interval_score_mean"]))
    parts.append("\n**Seed variability of the in-domain stager (seeds 0, 1, 2)**\n\n" + tbl("tableS_seed_variability", round_=4))
    parts.append("\n# S11. Coverage by subgroup (pre-specified design, LOSO; subgroups with ≥ 20 nights)\n")
    parts.append(tbl("tableS_subgroup_coverage", "n_nights >= 20"))
    parts.append("\n# S12. Error analysis\n")
    for st in ["yasa", "lgbm_sc_s0"]:
        parts.append(f"\n**{st}: plug-in bias (automatic − reference)**\n\n" + tbl(f"tableS_cohort_bias_{st}", round_=2))
        parts.append(f"\n**{st}: row-normalised epoch confusion (reference × predicted)**\n\n"
                     + csv_tbl(RESULTS_DIR / "statistics" / f"e08_confusion_{st}.csv"))
    parts.append("\n**Covered vs non-covered nights (proposed method, LOSO; Mann–Whitney p)**\n\n")
    parts.append(csv_tbl(RESULTS_DIR / "statistics" / "e08_noncovered_yasa.csv"))
    parts.append("\n**WASO mechanism (YASA): wake after final awakening and late sampled final awakenings**\n\n" + tbl("tableS_waso_mechanism"))
    parts.append("\n# S13. Robustness to signal corruption (YASA; calibration on clean nights, test on corrupted nights)\n")
    parts.append(tbl("tableS_robustness", "method in ['ba_loa','scp_signed','scp_abs_cal','cqr_ffbs','norm_reg_ffbs']"))
    parts.append("\n# S14. Flagging nights with clinically relevant errors (AUROC, 95% cluster-bootstrap CI; suppressed when <10 events)\n")
    parts.append(tbl("tableS_flagging", None, ["stager", "cohort", "param", "threshold", "signal", "n", "n_events", "auroc", "lo95", "hi95"]))
    parts.append("\n# S15. Computational cost (median per night, one CPU core) and one-off costs\n\nPer-night timings: 20 nights per cohort, original timing run. One-off costs were measured in a separate run from the stored SC probabilities (`code/experiments/e10_oneoff.py`); the \"7 × 24 h recording\" is synthetic (one night's probabilities repeated to 20,160 epochs) and memory is the peak traced by `tracemalloc`.\n")
    parts.append(tbl("tableS_efficiency", round_=4))
    parts.append("\n" + tbl("tableS_efficiency_oneoff", round_=3))
    parts.append("\n# S16. Datasets and data-leakage audit\n")
    parts.append((ROOT_DIR / "supplementary" / "S_data_and_leakage_audit.md").read_text().replace("# ", "## ", 1))
    parts.append("\n# S17. Sensitivity: plain split-conformal design and site-level coverage risk\n\n"
                 "**Plain-split design.** Calibration subjects of each of the 50 splits were halved (A, B); all label-dependent "
                 "components were fitted on A, scores computed on B with A's model, and test nights summarised with A's model "
                 "(exact split-conformal construction; calibration set about half the size of the primary design).\n\n")
    parts.append(tbl("tableS_plainsplit", "method in ['norm_reg_ffbs','scp_signed']",
                     ["stager", "cohort", "param", "method", "cov_plain", "cov_primary", "width_plain", "width_primary", "width_ratio",
                      "n_cal_plain", "n_cal_primary"]))
    parts.append("\n**Probability that a site's realised coverage falls below 0.80.** Theory: exchangeable split-conformal "
                 "interval, coverage given the calibration set ~ Beta(n+1-l, l) with l = floor(0.1 (n+1)), test nights binomial; "
                 "observed: 50 repetitions (median over parameters).\n\n")
    parts.append(tbl("tableS_local_risk_theory"))
    md = "\n".join(parts)
    OUT.mkdir(exist_ok=True)
    (OUT / "Supplementary_Material.md").write_text(md)
    subprocess.run(["pandoc", str(OUT / "Supplementary_Material.md"), "-o", str(OUT / "Supplementary_Material.docx"),
                    "-f", "markdown+pipe_tables"], check=True)
    print("written", OUT / "Supplementary_Material.docx")


if __name__ == "__main__":
    main()
