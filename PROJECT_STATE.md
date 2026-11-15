# PROJECT_STATE (checkpoint file — update after every significant stage)

_Last update: 2026-11-15, session 1 (approx. 3 h into session)_

## Selected target journal
**Sleep Medicine** (Elsevier, ISSN 1389-9457). JIF 4.1; Q1 Clinical Neurology 68/296 (secondary source, LetPub);
median submission→acceptance 91 d (own PubMed computation, n=400). Details: `Target_Journal_Submission/journal_selection/`.
Guidelines: ≤5000 words, structured abstract ≤300 w, ≤50 refs, ≤8 display items, highlights, GenAI declaration.

## Research topic (FINAL)
Per-night conformal prediction intervals for automatically scored PSG parameters (TST, SOL, WASO, REML,
N1/N2/N3/REM %) using HMM forward-filtering backward-sampling (FFBS) over stager probabilities +
normalised split-conformal calibration; two stagers (YASA pretrained external; LightGBM in-domain on SC),
three cohorts (Sleep-EDF SC/ST, HMC; 348 nights, 251 subjects). Protocol: `supplementary/PREREGISTERED_PROTOCOL.md`.

## Key results so far (see EXPERIMENT_LOG.md)
* Within-cohort validity achieved (0.89–0.92 coverage) for all conformal methods.
* Efficiency gains vs constant-width/BA-LoA for TST, stage %, REML (SC/ST); not for SOL, REM%, WASO-SC.
* Cross-cohort coverage fails for N3% (bias sign flips SC vs HMC); 10 local nights restore coverage.
* Posterior-mean TST removes plug-in bias (−38 → −4 min in HMC); WASO-SC failure (long post-awakening wake).

## Code / pipeline
`Target_Journal_Submission/code/` — run_all.py (quick/full), experiments e01–e10, scripts make_tables/make_figures,
tests (8 passing). Manuscript sources: `Target_Journal_Submission/manuscript/sections/*.md`, builder build_manuscript.py
(pandoc + python-docx + LibreOffice; numbers injected from tables/manuscript_numbers.json).

## In progress (background)
* Rerun chain E03→E04→E06→E07→E04-seeds after adding calibrated plug-in comparators (CHANGELOG).
* E09 robustness (YASA predictions on corrupted signals; 1 worker).

## Next exact steps
1. After chain: run E08 (error analysis), E10 (efficiency), make_tables, make_figures.
2. Write Results/Discussion/Conclusion/Abstract with placeholders; references; build DOCX/PDF.
3. Ten-agent review cycles (REVIEW/), fixes, reruns.
4. Cover letter, final audits, risk report, decision; commit + push to branch claude/tender-bohr-dljsc0.
