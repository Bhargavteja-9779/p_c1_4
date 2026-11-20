# Pre-specified study protocol (written 2026-11-15, BEFORE any interval/coverage result was computed)

Only base-stager accuracies (E01, E02) had been inspected when this protocol was fixed. Any later
deviation is listed, with its reason, in the deviations section that follows (Supplementary S1).

## Working title
Distribution-free per-night prediction intervals for automatically scored polysomnography parameters:
structured posterior sampling, conformal calibration and external validation.

## Problem and gap
Automatic staging is validated by epoch agreement and population Bland–Altman limits of agreement (LoA),
yet clinical use relies on per-night parameters (TST, SOL, WASO, REM latency, stage percentages).
Existing uncertainty work is epoch-level (entropy, MC-dropout, conformal sets: ConMIL 2025), night-level
quality scores without calibrated units (Ganglberger 2024; Mikkelsen 2020), or population-level error
propagation (Hardarson 2023). No method was found that returns, for an individual night, an interval for
each clinical parameter with a stated, empirically verified coverage, nor any evaluation of such
coverage across cohorts.

## Hypothesis
Propagating epoch-level posteriors through a hybrid classifier/HMM by forward-filtering backward-sampling
(FFBS) yields per-night predictive distributions whose spread ranks nights by their actual parameter
error; conformal calibration of this spread gives intervals with nominal marginal coverage that are, on
average, narrower and more informative than constant-width intervals (Bland–Altman LoA; split-conformal
absolute residual), for any base stager.

## Research questions → experiments
* RQ1 (validity) – within-cohort coverage of 90% intervals for 8 parameters, two stagers, three cohorts → E04.
* RQ2 (efficiency/adaptivity) – width, interval score, and Spearman correlation between width and absolute
  error, vs BA-LoA, split-conformal (abs), raw Bayesian percentiles, CQR-type alternatives → E04.
* RQ3 (components) – FFBS vs independent-epoch sampling; fitted emission temperature tau vs tau=1;
  score function (norm, norm_reg, cqr) → E05 ablation.
* RQ4 (transportability) – SC-calibrated intervals applied to ST and HMC; few-night target recalibration
  with n_t ∈ {10, 20, 30, 50} target nights → E06.
* RQ5 (clinical utility & errors) – (a) detection of nights with clinically relevant error
  (|TST err| > 30 min; |REML err| > 30 min; |N3% err| > 5 pp) by interval width vs epoch-level
  uncertainty summaries (mean entropy, mean max-probability), AUROC with bootstrap CIs;
  (b) Bland–Altman bias/LoA of plug-in vs posterior-mean point estimates; (c) failure analysis of
  non-covered nights → E07.
* Sensitivity – alpha ∈ {0.05, 0.1, 0.2}; number of samples M ∈ {100, 300, 1000}; calibration-set size;
  base-stager seed (LightGBM seeds 0/1/2) → E08.
* Robustness – synthetic EEG/EOG corruption (additive Gaussian noise at fixed SNR; 50 Hz line noise;
  high-amplitude movement-artefact bursts) applied to test nights, coverage and width tracked → E09.
* Efficiency – wall-clock time and memory of FFBS + parameter computation per night vs base stager → E10.

## Fixed design choices
* Stagers: S1 = YASA pretrained EEG+EOG (external to all cohorts); S2 = LightGBM on YASA features trained on
  SC (subject-grouped 5-fold out-of-fold for SC; all-SC model for ST/HMC). Primary S2 seed = 0.
* Analysis windows: SC [lights-off, +10 h]; ST [lights-off, end]; HMC [lights-off, lights-on].
* Parameters: TST, SOL, WASO, REML, N1%, N2%, N3%, REM%. REML analysed only on nights whose reference has REM.
* Plug-in estimate = parameter of the stager's own hypnogram (argmax of uncalibrated probabilities), i.e.
  current clinical practice.
* HMM parameters (BCTS calibration, source prior, transition matrix, initial distribution, tau) are
  estimated on labelled nights that never include the night being evaluated: within-cohort analyses use
  subject-grouped 5-fold cross-fitting; cross-cohort analyses use all SC nights.
* FFBS: M = 1000 samples/night, seeded deterministically per night.
* Primary proposed interval: norm_reg score with FFBS posterior mean and SD; alpha = 0.10 (90% intervals).
* Within-cohort evaluation: R = 500 random subject-grouped 50/50 calibration/test splits per cohort
  (split seeds 0..499).  Coverage, mean width and interval score averaged over test nights then over splits.
* Few-night recalibration: R = 500 repetitions per n_t (seeds 0..499).
* Statistics: subject-level cluster bootstrap (2000 resamples) for CIs of width ratios and AUROC;
  paired comparisons of per-night interval scores between the proposed method and each baseline with the
  Wilcoxon signed-rank test on per-subject mean interval scores (one fixed split: the full-cohort
  leave-one-subject-out calibration, see below), Holm correction across baselines × parameters.
  Exact binomial CIs for coverage of fixed test sets.
* Leave-one-subject-out (LOSO) conformal evaluation (each night's interval calibrated on all other subjects'
  nights in the same cohort) is used for per-night paired comparisons and error analysis.
* Success criteria (stated a priori): coverage within ±3 pp of nominal in within-cohort analyses; the
  proposed method is considered better than constant-width intervals only if its mean interval score is
  lower with a Holm-adjusted p < 0.05 and its width–error Spearman correlation is positive with a CI
  excluding 0.  Failure to meet these criteria will be reported as such.
