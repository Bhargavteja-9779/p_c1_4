"""Assemble the Supplementary Material (Markdown -> DOCX) from machine-generated tables.

Numbering (referenced in the manuscript):
  S1  Pre-registered protocol and all deviations (CHANGELOG)          -> supplementary/PREREGISTERED_PROTOCOL.md + CHANGELOG
  S2  Coverage/width/interval score of all methods, all cohorts       -> tables/tableS_all_methods_within (alpha=0.10)
  S3  Paired Wilcoxon tests (LOSO), Holm-adjusted                      -> tables/tableS_paired_tests
  S4  Centre x scale factorial and ablations                          -> tables/tableS_ablation_summary
  S5  Seed variability (LightGBM seeds 0-2)                           -> tables/tableS_seed_variability
  S6  Sensitivity to alpha (0.05, 0.20)                               -> tables/tableS_all_methods_within (alpha!=0.10)
  S7  LOSO coverage with cluster-bootstrap CIs                         -> tables/tableS_loso_coverage
  S8  Point estimates, LightGBM stager                                -> tables/tableS_point_estimates_lgbm
  S9  Subgroup coverage                                                -> tables/tableS_subgroup_coverage
  S10 Cohort-specific plug-in bias and epoch confusion                 -> tables/tableS_cohort_bias_*
  S11 Error analysis: covered vs non-covered nights; WASO mechanism    -> results/statistics/e08_noncovered_*, tableS_waso_mechanism
  S12 Robustness to signal corruption                                  -> tables/tableS_robustness
  S13 Cross-cohort transfer and few-night recalibration                -> tables/tableS_cross_cohort_source_only, tableS_fewshot
  S14 Flagging AUROCs (all parameters, all signals)                    -> tables/tableS_flagging
  S15 Computational cost                                               -> tables/tableS_efficiency
  S16 Data and leakage audit                                           -> supplementary/S_data_and_leakage_audit.md
"""
import subprocess
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.utils import RESULTS_DIR, ROOT_DIR, TABLES_DIR  # noqa: E402

OUT = ROOT_DIR / "supplementary"


def tbl(name, query=None, cols=None, round_=3, max_rows=400):
    f = TABLES_DIR / f"{name}.csv"
    if not f.exists():
        return f"*[{name} not available]*\n"
    d = pd.read_csv(f)
    if query:
        d = d.query(query)
    if cols:
        d = d[[c for c in cols if c in d.columns]]
    d = d.round(round_)
    if len(d) > max_rows:
        d = d.head(max_rows)
    return d.to_markdown(index=False) + "\n"


def csv_tbl(path, round_=3):
    f = Path(path)
    if not f.exists():
        return f"*[{f.name} not available]*\n"
    return pd.read_csv(f).round(round_).to_markdown(index=False) + "\n"


def main():
    parts = ["---\ntitle: \"Supplementary Material\"\n---\n",
             "Supplementary material for: *Per-night prediction intervals for automatically scored polysomnography: "
             "conformal calibration of posterior hypnogram samples with external validation*.\n",
             "All tables were generated automatically from the result files of the analysis code "
             "(`code/run_all.py`).\n"]
    parts.append("# S1. Pre-registered protocol and deviations\n")
    parts.append((ROOT_DIR / "supplementary" / "PREREGISTERED_PROTOCOL.md").read_text().replace("# ", "## ", 1))
    parts.append("\n## Deviations and additions (chronological change log)\n")
    parts.append((ROOT_DIR.parent / "CHANGELOG.md").read_text().split("\n", 2)[2])
    parts.append("\n# S2. All interval methods within cohorts (α = 0.10; mean ± SD over 500 splits)\n")
    parts.append(tbl("tableS_all_methods_within", "alpha == 0.1",
                     ["stager", "cohort", "param", "method", "coverage_mean", "coverage_std", "mean_width_mean",
                      "interval_score_mean", "spearman_mean"]))
    parts.append("\n# S3. Paired comparisons (leave-one-subject-out; Wilcoxon signed-rank on per-subject mean interval score; Holm within cohort and stager)\n")
    parts.append(tbl("tableS_paired_tests", None, ["stager", "cohort", "param", "baseline", "n_subjects", "mean_is_proposed",
                                                     "mean_is_baseline", "r_rb", "p", "p_holm"]))
    parts.append("\n# S4. Centre × scale factorial and ablations (median ratio of interval score to the proposed method over cohorts; >1 = worse than proposed)\n")
    parts.append(tbl("tableS_ablation_summary", round_=2))
    parts.append("\n**Paired factorial tests: FFBS-SD scale versus constant width with the centre held fixed (LOSO; Wilcoxon; Holm within cohort and stager)**\n\n")
    parts.append(tbl("tableS_factorial_tests", None, ["stager", "cohort", "param", "centre", "n_subjects", "mean_is_scaled",
                                                        "mean_is_constant", "ratio", "r_rb", "p", "p_holm"]))
    parts.append("\n# S5. Seed variability of the in-domain stager (seeds 0, 1, 2)\n")
    parts.append(tbl("tableS_seed_variability", round_=4))
    parts.append("\n# S6. Sensitivity to the miscoverage level α\n")
    parts.append(tbl("tableS_all_methods_within", "alpha != 0.1 and method in ['ba_loa','scp_abs_bc','cqr_ffbs','norm_reg_ffbs']",
                     ["stager", "alpha", "cohort", "param", "method", "coverage_mean", "mean_width_mean", "interval_score_mean"]))
    parts.append("\n# S7. Leave-one-subject-out coverage with subject-level cluster-bootstrap 95% CIs\n")
    parts.append(tbl("tableS_loso_coverage", "method in ['ba_loa','scp_abs_bc','scp_abs','cqr_ffbs','norm_reg_ffbs']",
                     ["stager", "cohort", "param", "method", "n_nights", "coverage", "cov_lo95", "cov_hi95", "mean_width"]))
    parts.append("\n# S8. Point estimates, in-domain LightGBM stager\n")
    parts.append(tbl("tableS_point_estimates_lgbm", round_=2))
    parts.append("\n# S9. Coverage by subgroup (leave-one-subject-out)\n")
    parts.append(tbl("tableS_subgroup_coverage", "count >= 10"))
    parts.append("\n# S10. Cohort-specific plug-in bias (YASA and LightGBM) and epoch confusion matrices\n")
    for st in ["yasa", "lgbm_sc_s0"]:
        parts.append(f"\n**{st}: plug-in bias (automatic − reference)**\n\n" + tbl(f"tableS_cohort_bias_{st}", round_=2))
        parts.append(f"\n**{st}: row-normalised epoch confusion (reference × predicted)**\n\n"
                     + csv_tbl(RESULTS_DIR / "statistics" / f"e08_confusion_{st}.csv"))
    parts.append("\n# S11. Error analysis\n\n**Covered vs non-covered nights (proposed method, LOSO; Mann–Whitney p)**\n\n")
    parts.append(csv_tbl(RESULTS_DIR / "statistics" / "e08_noncovered_yasa.csv"))
    parts.append("\n**WASO mechanism (YASA): wake after final awakening and late sampled final awakenings**\n\n" + tbl("tableS_waso_mechanism"))
    parts.append("\n# S12. Robustness to signal corruption (YASA)\n")
    parts.append(tbl("tableS_robustness", "method in ['ba_loa','scp_abs_bc','cqr_ffbs','norm_reg_ffbs']"))
    parts.append("\n# S13. Cross-cohort transfer (calibration on SC) and few-night recalibration\n")
    parts.append(tbl("tableS_cross_cohort_source_only", "method in ['ba_loa','scp_abs_bc','scp_abs_cal','cqr_ffbs','norm_reg_ffbs','norm_reg_plugc']",
                     ["stager", "target", "param", "method", "n_cal", "n_test", "coverage", "mean_width", "interval_score"]))
    parts.append("\n" + tbl("tableS_fewshot", "method in ['ba_loa','scp_abs_bc','norm_reg_ffbs']"))
    parts.append("\n# S14. Flagging nights with clinically relevant errors (AUROC, 95% cluster-bootstrap CI; suppressed when <10 events)\n")
    parts.append(tbl("tableS_flagging", None, ["stager", "cohort", "param", "threshold", "signal", "n", "n_events", "auroc", "lo95", "hi95"]))
    parts.append("\n# S15. Computational cost (median per night, one CPU core)\n")
    parts.append(tbl("tableS_efficiency", round_=4))
    parts.append("\n# S16. Datasets and data-leakage audit\n")
    parts.append((ROOT_DIR / "supplementary" / "S_data_and_leakage_audit.md").read_text().replace("# ", "## ", 1))
    parts.append("\n# S17. Conditional coverage by difficulty and exploratory Mondrian calibration (LOSO; quartiles of plug-in accuracy used only for evaluation)\n")
    parts.append(tbl("tableS_conditional_coverage", round_=3))
    parts.append("\n**Few-night recalibration: probability that realised coverage of the remaining target nights falls below 0.80 (500 repetitions)**\n\n")
    for st in ["yasa", "lgbm_sc_s0"]:
        parts.append(f"\n*{st}*\n\n" + tbl(f"tableS_fewshot_risk_{st}", "method in ['ba_loa','scp_abs_bc','norm_reg_ffbs']", round_=3))
    md = "\n".join(parts)
    OUT.mkdir(exist_ok=True)
    (OUT / "Supplementary_Material.md").write_text(md)
    subprocess.run(["pandoc", str(OUT / "Supplementary_Material.md"), "-o", str(OUT / "Supplementary_Material.docx"),
                    "-f", "markdown+pipe_tables"], check=True)
    print("written", OUT / "Supplementary_Material.docx")


if __name__ == "__main__":
    main()
