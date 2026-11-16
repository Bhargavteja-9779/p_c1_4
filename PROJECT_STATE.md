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

## Status (2026-11-16 ~09:45 UTC)
* All experiments complete: E01–E04 (+seeds), E06–E11; tables, figures (5), supplement (S1–S17),
  manuscript DOCX/PDF (4,437 words; abstract 288), cover letter DOCX. Commit d618813 pushed.
* Review cycle 1: 10 independent reviewer agents launched (outputs → REVIEW/cycle01/agentNN_*.md, each ends
  with a JSON findings block). The earlier wave-A agents (cycle 1 attempt) died on the 5-h rate limit.

## Next exact steps
1. When cycle-1 reviews arrive: consolidate → REVIEW/review_01.md (issue list with severity, decision, fix).
   Adversarially verify fatal/critical/major findings (workflow), implement fixes, rerun affected experiments
   (scripts/rerun_conformal_evaluations.sh; make_tables; make_figures; make_supplement; build_manuscript).
2. Cycles 2..10: delta reviews (same 10 roles, new weaknesses only) → review_02..10.md.
3. Final audits (consistency, reproducibility quick-mode run), final_audit.md, rejection-risk report, decision.
4. Commit + push after every cycle (branch claude/tender-bohr-dljsc0).
