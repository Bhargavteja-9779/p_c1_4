# EXPERIMENT_LOG

All experiments are logged here, including failures and abandoned directions.

## E0 — Development pilot: subject-level label-shift adaptation for inter-patient ECG (ABANDONED)
* Date: 2026-11-15. Purpose: Phase-2 feasibility check of candidate topic "hierarchical empirical-Bayes,
  Markov-aware label-shift adaptation per patient".
* Data: MIT-BIH Arrhythmia DS1 only (22 records; de Chazal split), 11-fold patient-grouped CV. DS2,
  INCART and SVDB were never evaluated (kept untouched).
* Base model: HistGradientBoosting (class-weighted) on RR + morphology features; BCTS calibration fit on
  inner patient-grouped out-of-fold predictions.
* Result (pooled over held-out DS1 patients):

| method | acc | F1 N | F1 S | F1 V | F1 F | macro-F1 | prior MAE S/V/F (pp) |
|---|---|---|---|---|---|---|---|
| raw (balanced) | 0.902 | 0.951 | 0.219 | 0.670 | 0.040 | 0.470 | – |
| calibrated, no adaptation | 0.919 | 0.959 | 0.128 | 0.628 | 0.000 | 0.429 | 2.69/5.04/1.41 |
| MLLS (EM) | 0.789 | 0.892 | 0.162 | 0.344 | 0.004 | 0.351 | 5.39/10.51/7.58 |
| BBSE | 0.475 | 0.646 | 0.054 | 0.482 | 0.031 | 0.303 | 3.12/7.08/45.88 |
| RLLS | 0.864 | 0.931 | 0.094 | 0.429 | 0.000 | 0.363 | 5.02/7.21/1.24 |
| MAPLS | 0.810 | 0.898 | 0.142 | 0.535 | 0.025 | 0.400 | 9.67/9.65/11.14 |
| IM-prior | 0.849 | 0.918 | 0.254 | 0.657 | 0.049 | 0.470 | 15.33/18.90/10.90 |
| HMM fixed | 0.876 | 0.940 | 0.072 | 0.517 | 0.000 | 0.382 | 6.13/5.73/1.26 |
| ML Baum–Welch | 0.793 | 0.892 | 0.159 | 0.405 | 0.024 | 0.370 | 6.30/9.91/4.37 |
| EB-iid (proposed) | 0.790 | 0.892 | 0.162 | 0.344 | 0.004 | 0.350 | 5.37/10.42/7.45 |
| EB-HMM (proposed) | 0.804 | 0.896 | 0.053 | 0.411 | 0.000 | 0.340 | 9.26/10.30/0.66 |

* Interpretation: every label-shift estimator degraded both classification and prevalence estimation
  relative to no adaptation. Patient-specific morphology (conditional shift p(x|y) varies across
  patients) violates the label-shift assumption, and EM amplifies systematic errors. The empirical-Bayes
  prior (total concentration ≈6 vs ≈2,000 beats/patient) is too weak to counteract it.
* Decision: direction abandoned (Phase-2 stress test failed). Additionally, the journal-selection
  process found no Q1 methods journal with verified ≤100-day acceptance; the topic was re-targeted to
  sleep medicine.
* Code: `archive_abandoned_ecg/` (pilot script + modules), not part of the submission package.

## E01 — YASA features + pretrained probabilities (2026-11-15)
* 348 nights processed (SC 153, ST 44, HMC 151). Mean per-night accuracy (pretrained YASA EEG+EOG):
  SC 0.794, ST 0.810, HMC 0.733. ~2–6 s per night on one CPU core.

## E02 — In-domain LightGBM stager (SC, subject-grouped 5-fold)
* Mean per-night accuracy (seeds 0/1/2 essentially identical): SC 0.820, ST 0.800, HMC 0.619 (montage
  shift C4-M1/E1-M2 vs Fpz-Cz/horizontal EOG).

## E03 — FFBS night summaries
* Fitted emission temperature tau = 0.10 in almost all folds (0.15 in two HMC folds) after the grid was
  extended (CHANGELOG). Raw posterior SDs strongly overconfident (e.g. TST SD 4–7 min vs errors 15–35 min).

## E04 — Within-cohort conformal evaluation (500 splits + LOSO) — first run
* Validity: all conformal methods 0.89–0.92 coverage (nominal 0.90) for both stagers, 3 cohorts,
  8 parameters (meets ±3 pp criterion). BA-LoA under-covers in ST (0.83–0.86). Raw FFBS percentiles
  0.28–0.65 for most parameters; independent-epoch percentiles much worse (0.04–0.77).
* Efficiency (interval score vs constant-width conformal): clear gains for TST (0.41–0.80), most stage
  percentages, REML in SC/ST; no gain or losses for SOL (HMC, ST), REM%, WASO in SC (1.14–1.36).
  Part of the TST gain is attributable to centring on the posterior mean (constant-width around FFBS
  mean already 0.44–0.86). CQR on FFBS quantiles better than the pre-registered symmetric score for
  SOL and REML.

## E06 — Cross-cohort (first run, YASA)
* SC-calibrated intervals do not transfer for N3% to HMC (coverage 0.36–0.58 for most methods); TST
  0.84–0.97; REML 0.79–0.88. Target-only recalibration with 10 nights restores ≈0.90–0.91 coverage for
  conformal methods (BA-LoA 0.83–0.86); pooled SC+target does not fully restore HMC coverage.

## E07 — Paired tests / utility / point estimates (first run)
* Posterior-mean TST: bias −38.3 → −3.9 min (YASA HMC), −21.7 → −0.7 (SC), −22.7 → −2.2 (ST); ICC
  0.81 → 0.93 (HMC). WASO in SC: posterior mean badly biased (+68 min) — long post-awakening wake in the
  10-h SC window (see E08). REML/REM%/SOL: posterior mean worse than plug-in.
* Flagging AUROC (width vs mean entropy): REML and N3% better with width; TST similar; WASO worse.
* Led to protocol extension (calibrated plug-in comparators) — rerun scheduled.

## E04/E07 rerun with calibrated-plug-in comparators (16:30–16:52) and container restart
* Calibrated plug-in (BCTS on calibration nights, argmax) explains most of the TST bias removal
  (YASA HMC MAE: raw 40.2, calibrated 19.5, FFBS mean 19.3 min; posterior mean vs calibrated p = 0.64).
  → earlier interpretation ("posterior averaging removes TST bias") was WRONG; corrected in manuscript.
* Container restarted at ~17:08 (E04 seeds interrupted). All results committed and pushed (0d41db0).

## E04 rerun #3 with bias-corrected and factorial comparators (21:56–22:02, parallel)
* New comparators: scp_abs_bc (distribution-free bias-corrected LoA), norm_reg_plug, norm_reg_plugc;
  regulariser now computed on calibration+test nights (exact validity).
* Factorial (same centre, FFBS-SD scale vs constant width): interval score lower in 79–92% of the 24
  cohort×parameter combinations for every centre, both stagers → adaptive scale is the robust contribution.
* Proposed vs scp_abs_bc: better in 62–67% of combinations (TST, N2%, REML), worse for SOL, REM%,
  WASO-SC (posterior-mean centre biased for these). scp_abs_bc coverage min 0.852 (ST; approximate validity).

## Revision 1 — E12 end-to-end ("honest") protocol + E15 statistics (early run, 16:00–16:53, 2026-11-17)
PRIMARY within-cohort analysis after review cycle 1: every label-dependent component fitted on the calibration half
of 50 subject-grouped 50/50 splits (calibration scores K=5 cross-fitted); local deployment n_t=10/20/30 on ST/HMC.
* Validity: proposed coverage 0.902–0.925 (YASA), 0.890–0.928 (LightGBM), within ±3 pp in all 48 cells.
  DF-LoA (scp_signed) 0.871–0.928 (lowest in ST: 2 nights/subject → clustered calibration scores);
  BA-LoA 0.855–0.940; regression-based LoA (ba_reg) under-covers (mean 0.860, min 0.745–0.785).
* Scale at fixed centre (pre-specified criterion): FFBS-SD scale vs constant width around the FFBS mean lower IS in
  21/24 (YASA) and 23/24 (LGBM), significant 15 and 15, never significantly worse (mean ratio 0.92). Met.
* vs LoA family: TST better than all three LoA in every cohort and stager (ratio vs DF-LoA 0.64–0.86, all Holm p<0.05);
  other parameters no consistent gain (mean ratio vs DF-LoA excl. TST 1.07 YASA, 0.98 LGBM); WASO-SC significantly
  WORSE (1.72 YASA, 1.50 LGBM; posterior-mean WASO bias +68/+55 min in SC). ba_reg lower IS for most non-TST
  parameters (mean ratio excl. TST 1.16/1.07) but under-covers.
* Regulariser: unregularised score better in 20/24 (both stagers; ~5 % lower IS) — pre-specified choice not optimal.
* Harder nights (below-median accuracy): proposed lower IS than DF-LoA in 17/24 and 19/24; easier 10/24 and 14/24.
* Q1 (lowest-accuracy quartile) coverage: proposed mean 0.847, DF-LoA ~0.83, BA 0.79, ba_reg 0.76.
* Local deployment (10 nights): proposed mean coverage 0.920 HMC / 0.903 ST (YASA); BA 0.898/0.860; ba_reg 0.767/0.724;
  DF-LoA unbounded (<19 nights). P(realised cov<0.80) median 0.09/0.17 (BA 0.10/0.28); with 30 nights 0.07/0.15.
* Decisions (YASA, pooled): TST<6h decided 64 % with 98.7 % accuracy (DF-LoA 60 %/98.3 %; plug-in 84.2 % overall);
  WASO>30 29 %/92.7 % vs DF-LoA 20 %/95.7 %.
* Determinism: chain E12 (YASA) summary identical to early run to 3 dp (lgbm comparison pending).
* Consequence: claims narrowed — advantage over LoA is parameter-specific (TST), not general. Title changed.
