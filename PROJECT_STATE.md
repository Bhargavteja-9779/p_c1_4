# PROJECT_STATE (checkpoint file — update after every significant stage)

_Last update: 2026-11-17 (revision 1 in progress)_

## Selected target journal
**Sleep Medicine** (Elsevier, ISSN 1389-9457). JIF 4.1; Q1 Clinical Neurology 68/296 (secondary source, LetPub);
median submission→acceptance 91 d (own PubMed computation, n=400). Details: `Target_Journal_Submission/journal_selection/`.
Guidelines: ≤5000 words, structured abstract ≤300 w, ≤50 refs, ≤8 display items, highlights ≤85 chars, GenAI declaration.

## Research topic (FINAL)
Per-night conformal prediction intervals for automatically scored PSG parameters (TST, SOL, WASO, REML,
N1/N2/N3/REM %) using HMM forward-filtering backward-sampling (FFBS) over stager probabilities +
normalised split-conformal calibration; two stagers (YASA pretrained external; LightGBM in-domain on SC),
three cohorts (Sleep-EDF SC/ST, HMC; 348 nights, 251 subjects). Protocol: `supplementary/PREREGISTERED_PROTOCOL.md`.

## Key scientific findings (see EXPERIMENT_LOG.md)
* Within-cohort validity achieved (0.89–0.92 coverage) for all conformal methods.
* IMPORTANT CORRECTION: TST bias removal is mostly due to LOCAL CALIBRATION (calibrated plug-in), not posterior
  averaging (YASA HMC MAE: raw 40.2, calibrated 19.5, FFBS mean 19.3 min, p=0.64). Manuscript must say so.
* Original constant-width comparators were centred on the raw biased plug-in → added bias-corrected
  constant-width conformal (`scp_abs_bc`, distribution-free LoA) and centre×scale factorial (CHANGELOG).
* Cross-cohort coverage fails for N3% (bias sign flips SC vs HMC); 10 local nights restore coverage.

## Status (2026-11-17 ~15:45 UTC) — REVISION 1 in progress
* Review cycle 1 complete (10/10 reviews, all "major revision"); consolidated response REVIEW/review_01.md.
* Revision-1 code changes done: no-mask convention (leakage fix), new comparators (ba_reg, scp_signed, t-based BA),
  honest end-to-end protocol E12 as PRIMARY analysis, E13 (pre-registered sensitivity), E14 (montage), E15 (honest
  stats incl. decision thresholds, difficulty), E10 one-off costs. make_tables (honest_tables, sensitivity_tables;
  manuscript_numbers.json now written fresh, keys h_*), make_figures (Fig2 honest efficiency, Fig3 transport+local,
  Fig4 robustness, Fig5 adaptivity+decisions), make_supplement (S1–S16 renumbered), run_all (E12–E15 added).
* Manuscript: Introduction, Methods, captions, ethics rewritten; Results/Abstract/Highlights/Discussion/Conclusion/
  cover letter STILL OLD (must be rewritten with h_* keys after numbers arrive). 49/50 references cited.
* Running: code/scripts/rerun_revision1.sh (E03→E04→E06→E07→E08→E09→E11→E12→E13→E14→E04 seeds→E10) and an early
  parallel E12+E15 run (results/experiment_logs/e12_early.log, e15.log).

## Next exact steps
1. After E12 early: inspect e15_*.csv; write Results/Abstract/Highlights/Discussion/Conclusion with h_* keys.
2. After chain: run e15 again, make_tables, make_figures, make_supplement, build_manuscript; inspect PDF;
   delete obsolete figure files (fig3_adaptivity_flagging, fig4_transport_recalibration, fig5_robustness).
3. Review cycle 2 (prompt REVIEW/prompts/cycle02.md) → REVIEW/cycle02/, review_02.md; cycles 3–10 delta reviews.
4. Final audits, final_audit.md, rejection-risk report, decision. Commit + push after every step.
