# PROJECT_STATE (checkpoint file — update after every significant stage)

_Last update: 2026-11-15, session 1_

## Selected target journal
**Sleep Medicine** (Elsevier, ISSN 1389-9457). JIF 4.1; Q1 Clinical Neurology 68/296 (secondary source, LetPub);
median submission→acceptance 91 d (own PubMed computation, n=400). Details: `Target_Journal_Submission/journal_selection/`.

## Research topic (status: being finalised — Phase 1–5)
Night-level, distribution-free uncertainty for automated sleep scoring: per-night conformal prediction
intervals for clinical PSG parameters (TST, SOL, WASO, REM latency, stage %), using structured posterior
sampling of hypnograms (HMM forward-filtering backward-sampling over epoch probabilities) and external-cohort
validation + few-night site recalibration.

## Abandoned direction (documented negative result)
Subject-level label-shift adaptation (EM / empirical-Bayes Dirichlet / Markov) for inter-patient ECG.
DS1-only development pilot: adaptation reduced macro-F1 (0.429 → 0.35) — conditional shift violates the
label-shift assumption. See EXPERIMENT_LOG.md (E0). Code archived under `archive_abandoned_ecg/`.

## Data (all public, cached at Target_Journal_Submission/code/data/cache/sleep/, not committed)
| cohort | nights | subjects | scored epochs | source |
|---|---|---|---|---|
| Sleep-EDF SC | 153 | 78 | 182,852 | PhysioNet sleep-edfx 1.0.0 |
| Sleep-EDF ST | 44 | 22 | 42,643 | PhysioNet sleep-edfx 1.0.0 |
| HMC | 151 | 151 | 136,776 | PhysioNet hmc-sleep-staging 1.1 |
Raw EDFs were deleted after caching (disk quota); re-download with `code/scripts/download_data.sh`.

## Environment
4 CPU, 15 GB RAM, no GPU; Python 3.13; torch 2.15 CPU; yasa 0.8.1; lightgbm 4.7; numba 0.68.

## Completed
- Phase 0 journal selection (files in journal_selection/)
- Data download + caching (SC, ST, HMC)

## Next exact step
Run YASA pretrained EEG+EOG stager on all cached nights → epoch probabilities (base model 1);
train in-domain LightGBM stager on SC with subject-wise 5-fold CV (base model 2).
