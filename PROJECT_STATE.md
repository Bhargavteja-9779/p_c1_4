# PROJECT_STATE (checkpoint file — update after every significant stage)

_Last update: 2026-11-15, session 1 (after container restart; results saved & pushed at commit 0d41db0)_

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

## In progress (background, started 21:56)
`code/scripts/rerun_conformal_evaluations.sh` = E04 main → E06 → E07 → E08 → E09 (skip-predict; regenerates
corrupted-night summaries with plugc columns) → E04 seeds → E10. Log: results/experiment_logs/.
Review cycle 1 wave A agents (#1 novelty, #2 methodology, #5 dataset/leakage, #8 literature) running;
outputs → REVIEW/cycle01/agentNN_*.md.

## Next exact steps
1. When chain finishes: `python scripts/make_tables.py`, `python scripts/make_figures.py`; rewrite Results 3.3/3.4,
   Abstract, Highlights, Discussion for the calibration finding (use NUM keys n_sig_better_vs_scp_abs_bc_*,
   pe_*_plug_in_calibrated_*); `python manuscript/build_manuscript.py`.
2. Launch cycle-1 wave B agents (#3 design, #4 statistics, #6 robustness, #7 efficiency, #9 AE, #10 competitor).
3. Consolidate cycle-1 reviews → REVIEW/review_01.md; fix; rerun; cycles 2..10 (delta reviews).
4. Cover letter DOCX, final audits, risk report, decision; commit + push (branch claude/tender-bohr-dljsc0).
