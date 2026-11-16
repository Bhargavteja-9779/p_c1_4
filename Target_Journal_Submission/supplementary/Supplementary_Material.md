---
title: "Supplementary Material"
---

Supplementary material for: *Per-night prediction intervals for automatically scored polysomnography: conformal calibration of posterior hypnogram samples with external validation*.

All tables were generated automatically from the result files of the analysis code (`code/run_all.py`).

# S1. Pre-registered protocol and deviations

## Pre-specified study protocol (written 2026-11-15, BEFORE any interval/coverage result was computed)

Only base-stager accuracies (E01, E02) had been inspected when this protocol was fixed. Any later
deviation is logged in CHANGELOG.md with its reason.

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


## Deviations and additions (chronological change log)

## 2026-11-15
* [Topic] ECG label-shift direction abandoned after negative DS1 pilot (EXPERIMENT_LOG E0); topic
  re-targeted to night-level uncertainty for automated sleep scoring (journal: Sleep Medicine).
* [Protocol, before any interval result] Emission-temperature grid extended from [0.10, 1.50] to
  [0.02, 1.50]. Reason: in a 12-night/cohort smoke test the fitted tau was at the lower boundary (0.10–0.15),
  i.e. the original grid could not contain the optimum. tau is fitted only on labelled source nights.
* [Protocol extension, after first E04/E07 results] Added comparators to separate *local calibration*
  from *posterior averaging*: (i) plug-in of the locally calibrated probabilities ("plugc") and (ii)
  plug-in of HMM-smoothed marginals ("plugh") as point estimates; (iii) constant-width split conformal
  around the calibrated plug-in ("scp_abs_cal"). Reason: the FFBS posterior mean uses within-cohort
  calibration, whereas the original plug-in uses raw stager output, so the TST improvement could be
  partly attributable to calibration alone (anticipated reviewer objection). Primary method unchanged.
* [Statistics] cluster_bootstrap now returns no CI when the statistic is undefined in >50% of resamples
  (e.g. AUROC with zero events); AUROCs with <10 events are flagged as not interpretable.
* [Comparators, after calibrated-plug-in results] The calibrated plug-in reproduced most of the TST
  bias reduction attributed earlier to the posterior mean, showing that the original constant-width
  comparators (centred on the raw, biased plug-in) conflated calibration with adaptivity. Added
  (i) `scp_abs_bc`: bias-corrected constant-width split conformal (distribution-free analogue of
  Bland–Altman LoA; strongest simple competitor) and (ii) a centre × scale factorial
  (`norm_reg_plug`, `norm_reg_plugc` = FFBS-SD scale with raw/calibrated plug-in centres). Manuscript
  claims about point estimates and efficiency rewritten accordingly. Primary method unchanged.
* [Method correction for exact validity] The regulariser of normalised scores (median scale) is now
  computed from calibration AND test nights (label-free), making the score a symmetric function of all
  nights' features so that the finite-sample guarantee is exact (previously calibration-only;
  numerically negligible difference). All E04/E06/E07/E09 conformal evaluations re-run.
* [Exploratory experiment E11, added after E07] LOSO coverage of the proposed intervals was 81–85 % in the
  quartile of nights with the lowest plug-in accuracy (marginal coverage nominal). Added Mondrian
  (group-conditional) conformal calibration with K=2 bins defined by label-free difficulty proxies (mean epoch
  entropy; FFBS SD) to test whether conditional coverage of difficult nights can be improved. Reported as
  exploratory; the pre-specified method is unchanged.
* [Reporting] Few-night recalibration: report the probability that a site's realised coverage falls below
  0.80 (variability across repetitions), not only mean coverage.


# S2. All interval methods within cohorts (α = 0.10; mean ± SD over 500 splits)

| stager     | cohort   | param   | method           |   coverage_mean |   coverage_std |   mean_width_mean |   interval_score_mean |   spearman_mean |
|:-----------|:---------|:--------|:-----------------|----------------:|---------------:|------------------:|----------------------:|----------------:|
| yasa       | HMC      | N1%     | ba_loa           |           0.918 |          0.043 |            25.177 |                38.984 |           0     |
| yasa       | HMC      | N1%     | bayes_pct        |           0.397 |          0.039 |             5.444 |                66.603 |           0.222 |
| yasa       | HMC      | N1%     | cqr_ffbs         |           0.907 |          0.045 |            21.717 |                35.588 |           0.256 |
| yasa       | HMC      | N1%     | cqr_qr           |           0.923 |          0.054 |            26.898 |                35.574 |           0.237 |
| yasa       | HMC      | N1%     | ind_pct          |           0.286 |          0.036 |             3.576 |                64.954 |           0.147 |
| yasa       | HMC      | N1%     | norm_entropy_reg |           0.905 |          0.045 |            21.471 |                34.517 |           0.322 |
| yasa       | HMC      | N1%     | norm_ffbs        |           0.906 |          0.045 |            22.156 |                35.348 |           0.244 |
| yasa       | HMC      | N1%     | norm_reg_ffbs    |           0.906 |          0.046 |            21.564 |                35.305 |           0.277 |
| yasa       | HMC      | N1%     | norm_reg_ffbs1   |           0.907 |          0.048 |            21.566 |                35.191 |           0.246 |
| yasa       | HMC      | N1%     | norm_reg_ind     |           0.907 |          0.046 |            21.118 |                33.407 |           0.129 |
| yasa       | HMC      | N1%     | norm_reg_plug    |           0.909 |          0.045 |            22.738 |                39.152 |           0.221 |
| yasa       | HMC      | N1%     | norm_reg_plugc   |           0.909 |          0.045 |            22.394 |                39.495 |           0.221 |
| yasa       | HMC      | N1%     | scp_abs          |           0.908 |          0.045 |            23.297 |                41.992 |           0.069 |
| yasa       | HMC      | N1%     | scp_abs_bc       |           0.905 |          0.047 |            24.189 |                39.237 |           0.019 |
| yasa       | HMC      | N1%     | scp_abs_cal      |           0.907 |          0.045 |            22.38  |                41.832 |           0.126 |
| yasa       | HMC      | N1%     | scp_abs_mu       |           0.906 |          0.045 |            21.709 |                36.323 |           0.233 |
| yasa       | HMC      | N2%     | ba_loa           |           0.919 |          0.047 |            32.714 |                47.283 |          -0.013 |
| yasa       | HMC      | N2%     | bayes_pct        |           0.514 |          0.043 |            12.273 |                59.514 |          -0.089 |
| yasa       | HMC      | N2%     | cqr_ffbs         |           0.909 |          0.047 |            27.69  |                35.217 |          -0.089 |
| yasa       | HMC      | N2%     | cqr_qr           |           0.912 |          0.056 |            33.854 |                42.726 |           0.054 |
| yasa       | HMC      | N2%     | ind_pct          |           0.238 |          0.034 |             4.636 |                74.612 |           0.131 |
| yasa       | HMC      | N2%     | norm_entropy_reg |           0.91  |          0.045 |            27.985 |                34.818 |          -0.076 |
| yasa       | HMC      | N2%     | norm_ffbs        |           0.909 |          0.047 |            28.929 |                35.162 |          -0.092 |
| yasa       | HMC      | N2%     | norm_reg_ffbs    |           0.909 |          0.047 |            27.961 |                35.31  |          -0.092 |
| yasa       | HMC      | N2%     | norm_reg_ffbs1   |           0.909 |          0.046 |            30.185 |                38.068 |          -0.087 |
| yasa       | HMC      | N2%     | norm_reg_ind     |           0.905 |          0.048 |            23.497 |                33.886 |           0.125 |
| yasa       | HMC      | N2%     | norm_reg_plug    |           0.907 |          0.048 |            44.563 |                59.682 |           0.356 |
| yasa       | HMC      | N2%     | norm_reg_plugc   |           0.906 |          0.048 |            36.844 |                51.614 |           0.445 |
| yasa       | HMC      | N2%     | scp_abs          |           0.907 |          0.048 |            48.133 |                64.776 |          -0.16  |
| yasa       | HMC      | N2%     | scp_abs_bc       |           0.904 |          0.048 |            30.653 |                46.714 |          -0.004 |
| yasa       | HMC      | N2%     | scp_abs_cal      |           0.907 |          0.048 |            38.465 |                54.484 |          -0.016 |
| yasa       | HMC      | N2%     | scp_abs_mu       |           0.907 |          0.046 |            27.342 |                35.944 |           0.078 |
| yasa       | HMC      | N3%     | ba_loa           |           0.897 |          0.048 |            24.111 |                33.879 |          -0.101 |
| yasa       | HMC      | N3%     | bayes_pct        |           0.438 |          0.041 |             9.625 |                73.33  |           0.112 |
| yasa       | HMC      | N3%     | cqr_ffbs         |           0.908 |          0.048 |            30.324 |                36.204 |           0.121 |
| yasa       | HMC      | N3%     | cqr_qr           |           0.912 |          0.055 |            30.679 |                40.648 |           0.074 |
| yasa       | HMC      | N3%     | ind_pct          |           0.168 |          0.031 |             3.104 |                90.747 |           0.278 |
| yasa       | HMC      | N3%     | norm_entropy_reg |           0.908 |          0.048 |            30.549 |                36.602 |           0.121 |
| yasa       | HMC      | N3%     | norm_ffbs        |           0.91  |          0.045 |            30.283 |                36.212 |           0.126 |
| yasa       | HMC      | N3%     | norm_reg_ffbs    |           0.908 |          0.047 |            30.245 |                35.983 |           0.123 |
| yasa       | HMC      | N3%     | norm_reg_ffbs1   |           0.909 |          0.048 |            28.292 |                35.224 |           0.253 |
| yasa       | HMC      | N3%     | norm_reg_ind     |           0.907 |          0.047 |            26.156 |                33.29  |           0.265 |
| yasa       | HMC      | N3%     | norm_reg_plug    |           0.905 |          0.047 |            30.295 |                40.478 |           0.014 |
| yasa       | HMC      | N3%     | norm_reg_plugc   |           0.907 |          0.048 |            27.16  |                35.729 |           0.156 |
| yasa       | HMC      | N3%     | scp_abs          |           0.905 |          0.049 |            29.15  |                39.865 |          -0.133 |
| yasa       | HMC      | N3%     | scp_abs_bc       |           0.901 |          0.051 |            24.551 |                34.044 |          -0.11  |
| yasa       | HMC      | N3%     | scp_abs_cal      |           0.906 |          0.048 |            26.563 |                34.964 |          -0.065 |
| yasa       | HMC      | N3%     | scp_abs_mu       |           0.908 |          0.047 |            30.811 |                38.183 |           0.038 |
| yasa       | HMC      | REM%    | ba_loa           |           0.908 |          0.042 |            18.075 |                25.386 |          -0.127 |
| yasa       | HMC      | REM%    | bayes_pct        |           0.411 |          0.042 |             8.714 |                50.422 |           0.185 |
| yasa       | HMC      | REM%    | cqr_ffbs         |           0.909 |          0.045 |            21.812 |                27.225 |           0.176 |
| yasa       | HMC      | REM%    | cqr_qr           |           0.927 |          0.05  |            21.709 |                26.951 |           0.043 |
| yasa       | HMC      | REM%    | ind_pct          |           0.271 |          0.037 |             2.913 |                56.632 |           0.148 |
| yasa       | HMC      | REM%    | norm_entropy_reg |           0.908 |          0.046 |            21.705 |                27.083 |           0.064 |
| yasa       | HMC      | REM%    | norm_ffbs        |           0.909 |          0.045 |            23.37  |                27.85  |           0.167 |
| yasa       | HMC      | REM%    | norm_reg_ffbs    |           0.91  |          0.044 |            22.025 |                26.971 |           0.173 |
| yasa       | HMC      | REM%    | norm_reg_ffbs1   |           0.907 |          0.047 |            20.759 |                27.338 |           0.104 |
| yasa       | HMC      | REM%    | norm_reg_ind     |           0.911 |          0.046 |            17.302 |                22.524 |           0.143 |
| yasa       | HMC      | REM%    | norm_reg_plug    |           0.907 |          0.045 |            16.33  |                23.641 |           0.127 |
| yasa       | HMC      | REM%    | norm_reg_plugc   |           0.91  |          0.044 |            16.453 |                22.607 |           0.189 |
| yasa       | HMC      | REM%    | scp_abs          |           0.908 |          0.046 |            18.011 |                25.302 |          -0.132 |
| yasa       | HMC      | REM%    | scp_abs_bc       |           0.905 |          0.046 |            17.869 |                25.427 |          -0.119 |
| yasa       | HMC      | REM%    | scp_abs_cal      |           0.911 |          0.045 |            17.231 |                23.761 |          -0.115 |
| yasa       | HMC      | REM%    | scp_abs_mu       |           0.909 |          0.044 |            21.867 |                28.46  |          -0.032 |
| yasa       | HMC      | REML    | ba_loa           |           0.902 |          0.043 |           188.724 |               318.122 |          -0.209 |
| yasa       | HMC      | REML    | bayes_pct        |           0.886 |          0.026 |           137.904 |               289.241 |           0.455 |
| yasa       | HMC      | REML    | cqr_ffbs         |           0.908 |          0.045 |           156.5   |               291.485 |           0.535 |
| yasa       | HMC      | REML    | cqr_qr           |           0.914 |          0.057 |           238.318 |               329.299 |           0.415 |
| yasa       | HMC      | REML    | ind_pct          |           0.568 |          0.042 |            75.552 |               883.488 |           0.261 |
| yasa       | HMC      | REML    | norm_entropy_reg |           0.907 |          0.047 |           204.608 |               342.352 |           0.335 |
| yasa       | HMC      | REML    | norm_ffbs        |           0.908 |          0.046 |           179.834 |               298.509 |           0.667 |
| yasa       | HMC      | REML    | norm_reg_ffbs    |           0.909 |          0.046 |           183.879 |               314.075 |           0.612 |
| yasa       | HMC      | REML    | norm_reg_ffbs1   |           0.907 |          0.048 |           194.268 |               283.114 |           0.473 |
| yasa       | HMC      | REML    | norm_reg_ind     |           0.91  |          0.045 |           251.604 |               422.962 |           0.254 |
| yasa       | HMC      | REML    | norm_reg_plug    |           0.906 |          0.045 |           179.214 |               289.831 |           0.211 |
| yasa       | HMC      | REML    | norm_reg_plugc   |           0.906 |          0.047 |           191.859 |               315.074 |           0.223 |
| yasa       | HMC      | REML    | scp_abs          |           0.906 |          0.043 |           179.538 |               313.623 |          -0.167 |
| yasa       | HMC      | REML    | scp_abs_bc       |           0.905 |          0.043 |           190.065 |               318.31  |          -0.206 |
| yasa       | HMC      | REML    | scp_abs_cal      |           0.908 |          0.046 |           196.924 |               370.054 |          -0.199 |
| yasa       | HMC      | REML    | scp_abs_mu       |           0.908 |          0.046 |           210.108 |               358.071 |           0.186 |
| yasa       | HMC      | SOL     | ba_loa           |           0.918 |          0.035 |            24.695 |                47.966 |           0.121 |
| yasa       | HMC      | SOL     | bayes_pct        |           0.935 |          0.021 |            19.062 |                54.274 |           0.714 |
| yasa       | HMC      | SOL     | cqr_ffbs         |           0.935 |          0.028 |            19.459 |                54.575 |           0.705 |
| yasa       | HMC      | SOL     | cqr_qr           |           0.92  |          0.052 |            26.832 |                49.374 |           0.501 |
| yasa       | HMC      | SOL     | ind_pct          |           0.618 |          0.039 |             8.017 |               112.943 |           0.519 |
| yasa       | HMC      | SOL     | norm_entropy_reg |           0.91  |          0.046 |            28.285 |                74.209 |           0.023 |
| yasa       | HMC      | SOL     | norm_ffbs        |           0.908 |          0.049 |            19.101 |                60.796 |           0.701 |
| yasa       | HMC      | SOL     | norm_reg_ffbs    |           0.909 |          0.047 |            21.973 |                66.667 |           0.427 |
| yasa       | HMC      | SOL     | norm_reg_ffbs1   |           0.91  |          0.047 |            20.771 |                30.241 |           0.589 |
| yasa       | HMC      | SOL     | norm_reg_ind     |           0.909 |          0.047 |            25.322 |                72.833 |           0.37  |
| yasa       | HMC      | SOL     | norm_reg_plug    |           0.906 |          0.045 |            27.621 |                50.22  |           0.365 |
| yasa       | HMC      | SOL     | norm_reg_plugc   |           0.908 |          0.047 |            17.148 |                48.828 |           0.319 |
| yasa       | HMC      | SOL     | scp_abs          |           0.907 |          0.046 |            32.286 |                58.194 |           0.027 |
| yasa       | HMC      | SOL     | scp_abs_bc       |           0.906 |          0.046 |            22.543 |                49.852 |           0.188 |
| yasa       | HMC      | SOL     | scp_abs_cal      |           0.91  |          0.046 |            19.592 |                53.724 |          -0.067 |
| yasa       | HMC      | SOL     | scp_abs_mu       |           0.909 |          0.047 |            29.305 |                74.714 |          -0.119 |
| yasa       | HMC      | TST     | ba_loa           |           0.931 |          0.041 |           131.433 |               209.448 |          -0.009 |
| yasa       | HMC      | TST     | bayes_pct        |           0.577 |          0.041 |            28.72  |               208.164 |           0.527 |
| yasa       | HMC      | TST     | cqr_ffbs         |           0.91  |          0.047 |            94.678 |               152.859 |           0.527 |
| yasa       | HMC      | TST     | cqr_qr           |           0.92  |          0.051 |           115.525 |               155.356 |           0.362 |
| yasa       | HMC      | TST     | ind_pct          |           0.154 |          0.029 |            10.618 |               363.971 |           0.592 |
| yasa       | HMC      | TST     | norm_entropy_reg |           0.911 |          0.047 |            98.852 |               155.274 |           0.422 |
| yasa       | HMC      | TST     | norm_ffbs        |           0.909 |          0.049 |            81.728 |               129.09  |           0.517 |
| yasa       | HMC      | TST     | norm_reg_ffbs    |           0.91  |          0.048 |            88.433 |               143.933 |           0.517 |
| yasa       | HMC      | TST     | norm_reg_ffbs1   |           0.907 |          0.049 |            85.156 |               144.287 |           0.561 |
| yasa       | HMC      | TST     | norm_reg_ind     |           0.908 |          0.046 |           108.412 |               163.149 |           0.592 |
| yasa       | HMC      | TST     | norm_reg_plug    |           0.909 |          0.048 |           146.813 |               226.975 |           0.428 |
| yasa       | HMC      | TST     | norm_reg_plugc   |           0.908 |          0.049 |            89.521 |               143.859 |           0.527 |
| yasa       | HMC      | TST     | scp_abs          |           0.911 |          0.046 |           162.938 |               260.891 |         nan     |
| yasa       | HMC      | TST     | scp_abs_bc       |           0.909 |          0.049 |           107.84  |               203.591 |          -0.02  |
| yasa       | HMC      | TST     | scp_abs_cal      |           0.911 |          0.048 |           106.884 |               170.425 |         nan     |
| yasa       | HMC      | TST     | scp_abs_mu       |           0.911 |          0.047 |           107.633 |               169.668 |           0.007 |
| yasa       | HMC      | WASO    | ba_loa           |           0.926 |          0.048 |           102.139 |               176.244 |           0.197 |
| yasa       | HMC      | WASO    | bayes_pct        |           0.657 |          0.038 |            35.477 |               177.738 |           0.493 |
| yasa       | HMC      | WASO    | cqr_ffbs         |           0.912 |          0.046 |            81.598 |               147.693 |           0.289 |
| yasa       | HMC      | WASO    | cqr_qr           |           0.922 |          0.051 |           102.912 |               142.69  |           0.389 |
| yasa       | HMC      | WASO    | ind_pct          |           0.147 |          0.03  |            14.586 |               337.834 |           0.441 |
| yasa       | HMC      | WASO    | norm_entropy_reg |           0.911 |          0.048 |            82.355 |               152.046 |           0.177 |
| yasa       | HMC      | WASO    | norm_ffbs        |           0.909 |          0.048 |            81.311 |               136.754 |           0.433 |
| yasa       | HMC      | WASO    | norm_reg_ffbs    |           0.911 |          0.047 |            81.572 |               147.237 |           0.326 |
| yasa       | HMC      | WASO    | norm_reg_ffbs1   |           0.909 |          0.046 |            77.242 |               130.531 |           0.259 |
| yasa       | HMC      | WASO    | norm_reg_ind     |           0.909 |          0.048 |            99.944 |               156.299 |           0.278 |
| yasa       | HMC      | WASO    | norm_reg_plug    |           0.91  |          0.048 |           128.646 |               210.764 |           0.171 |
| yasa       | HMC      | WASO    | norm_reg_plugc   |           0.909 |          0.046 |            81.446 |               135.95  |           0.16  |
| yasa       | HMC      | WASO    | scp_abs          |           0.911 |          0.046 |           134.581 |               224.697 |          -0.036 |
| yasa       | HMC      | WASO    | scp_abs_bc       |           0.909 |          0.046 |            91.875 |               176.781 |           0.286 |
| yasa       | HMC      | WASO    | scp_abs_cal      |           0.912 |          0.048 |            88.736 |               149.922 |          -0.17  |
| yasa       | HMC      | WASO    | scp_abs_mu       |           0.911 |          0.047 |            86.952 |               159.208 |           0.009 |
| yasa       | SC       | N1%     | ba_loa           |           0.923 |          0.04  |            29.28  |                43.012 |          -0.092 |
| yasa       | SC       | N1%     | bayes_pct        |           0.441 |          0.043 |             7.509 |                89.685 |           0.271 |
| yasa       | SC       | N1%     | cqr_ffbs         |           0.907 |          0.05  |            27.052 |                41.087 |           0.218 |
| yasa       | SC       | N1%     | cqr_qr           |           0.915 |          0.055 |            30.8   |                39.392 |           0.264 |
| yasa       | SC       | N1%     | ind_pct          |           0.149 |          0.029 |             3.498 |                96.843 |           0.256 |
| yasa       | SC       | N1%     | norm_entropy_reg |           0.906 |          0.053 |            26.824 |                40.972 |           0.313 |
| yasa       | SC       | N1%     | norm_ffbs        |           0.907 |          0.049 |            26.895 |                38.535 |           0.297 |
| yasa       | SC       | N1%     | norm_reg_ffbs    |           0.907 |          0.05  |            26.872 |                40.071 |           0.261 |
| yasa       | SC       | N1%     | norm_reg_ffbs1   |           0.905 |          0.048 |            28.695 |                43.935 |           0.399 |
| yasa       | SC       | N1%     | norm_reg_ind     |           0.905 |          0.053 |            22.868 |                37.189 |           0.251 |
| yasa       | SC       | N1%     | norm_reg_plug    |           0.906 |          0.054 |            27.61  |                44.036 |           0.093 |
| yasa       | SC       | N1%     | norm_reg_plugc   |           0.905 |          0.053 |            27.319 |                43.923 |           0.169 |
| yasa       | SC       | N1%     | scp_abs          |           0.906 |          0.054 |            28.727 |                46.048 |          -0.042 |
| yasa       | SC       | N1%     | scp_abs_bc       |           0.903 |          0.056 |            27.074 |                43.5   |          -0.055 |
| yasa       | SC       | N1%     | scp_abs_cal      |           0.905 |          0.054 |            28.067 |                45.071 |           0.056 |
| yasa       | SC       | N1%     | scp_abs_mu       |           0.906 |          0.052 |            27.391 |                42.113 |           0.186 |
| yasa       | SC       | N2%     | ba_loa           |           0.905 |          0.038 |            38.695 |                56.334 |           0.007 |
| yasa       | SC       | N2%     | bayes_pct        |           0.451 |          0.042 |            11.477 |                74.279 |           0.239 |
| yasa       | SC       | N2%     | cqr_ffbs         |           0.907 |          0.051 |            33.306 |                43.578 |           0.239 |
| yasa       | SC       | N2%     | cqr_qr           |           0.911 |          0.061 |            42.132 |                53.499 |           0.125 |
| yasa       | SC       | N2%     | ind_pct          |           0.15  |          0.028 |             4.03  |               116.744 |           0.171 |
| yasa       | SC       | N2%     | norm_entropy_reg |           0.907 |          0.05  |            32.183 |                42.583 |           0.216 |
| yasa       | SC       | N2%     | norm_ffbs        |           0.907 |          0.052 |            33.716 |                42.226 |           0.244 |
| yasa       | SC       | N2%     | norm_reg_ffbs    |           0.907 |          0.051 |            33.134 |                42.876 |           0.244 |
| yasa       | SC       | N2%     | norm_reg_ffbs1   |           0.911 |          0.043 |            40.473 |                53.096 |           0.157 |
| yasa       | SC       | N2%     | norm_reg_ind     |           0.904 |          0.047 |            32.985 |                44.717 |           0.165 |
| yasa       | SC       | N2%     | norm_reg_plug    |           0.904 |          0.054 |            41.202 |                57.894 |           0.276 |
| yasa       | SC       | N2%     | norm_reg_plugc   |           0.903 |          0.057 |            39.91  |                58.669 |           0.395 |
| yasa       | SC       | N2%     | scp_abs          |           0.905 |          0.053 |            42.74  |                61.089 |          -0.057 |
| yasa       | SC       | N2%     | scp_abs_bc       |           0.903 |          0.053 |            39.272 |                57.422 |           0     |
| yasa       | SC       | N2%     | scp_abs_cal      |           0.902 |          0.058 |            41.553 |                61.877 |          -0.024 |
| yasa       | SC       | N2%     | scp_abs_mu       |           0.906 |          0.051 |            34.02  |                46.241 |           0.011 |
| yasa       | SC       | N3%     | ba_loa           |           0.917 |          0.053 |            15.948 |                25.538 |           0.136 |
| yasa       | SC       | N3%     | bayes_pct        |           0.377 |          0.041 |             6.796 |                40.834 |           0.32  |
| yasa       | SC       | N3%     | cqr_ffbs         |           0.911 |          0.052 |            16.969 |                23.225 |           0.025 |
| yasa       | SC       | N3%     | cqr_qr           |           0.919 |          0.058 |            20.804 |                26.962 |           0.182 |
| yasa       | SC       | N3%     | ind_pct          |           0.157 |          0.032 |             2.177 |                64.6   |           0.499 |
| yasa       | SC       | N3%     | norm_entropy_reg |           0.911 |          0.05  |            17.761 |                24.467 |          -0.073 |
| yasa       | SC       | N3%     | norm_ffbs        |           0.912 |          0.052 |            15.478 |                21.519 |           0.207 |
| yasa       | SC       | N3%     | norm_reg_ffbs    |           0.912 |          0.052 |            16.48  |                22.76  |           0.075 |
| yasa       | SC       | N3%     | norm_reg_ffbs1   |           0.916 |          0.048 |            21.215 |                30.145 |           0.171 |
| yasa       | SC       | N3%     | norm_reg_ind     |           0.911 |          0.051 |            17.208 |                23.697 |           0.113 |
| yasa       | SC       | N3%     | norm_reg_plug    |           0.912 |          0.051 |            23.269 |                32.672 |           0.163 |
| yasa       | SC       | N3%     | norm_reg_plugc   |           0.912 |          0.053 |            16.935 |                24.254 |           0.151 |
| yasa       | SC       | N3%     | scp_abs          |           0.913 |          0.052 |            24.301 |                35.19  |          -0.082 |
| yasa       | SC       | N3%     | scp_abs_bc       |           0.91  |          0.053 |            15.734 |                25.694 |           0.142 |
| yasa       | SC       | N3%     | scp_abs_cal      |           0.911 |          0.051 |            18.432 |                25.979 |          -0.141 |
| yasa       | SC       | N3%     | scp_abs_mu       |           0.912 |          0.051 |            18.244 |                24.739 |          -0.212 |
| yasa       | SC       | REM%    | ba_loa           |           0.927 |          0.06  |            21.756 |                34.416 |          -0.037 |
| yasa       | SC       | REM%    | bayes_pct        |           0.372 |          0.041 |             8.528 |                65.672 |           0.237 |
| yasa       | SC       | REM%    | cqr_ffbs         |           0.906 |          0.056 |            25.323 |                35.133 |           0.247 |
| yasa       | SC       | REM%    | cqr_qr           |           0.917 |          0.059 |            23.553 |                32.025 |           0.268 |
| yasa       | SC       | REM%    | ind_pct          |           0.261 |          0.036 |             2.657 |                60.804 |           0.289 |
| yasa       | SC       | REM%    | norm_entropy_reg |           0.908 |          0.055 |            25.267 |                35.241 |           0.156 |
| yasa       | SC       | REM%    | norm_ffbs        |           0.909 |          0.055 |            25.114 |                31.845 |           0.244 |
| yasa       | SC       | REM%    | norm_reg_ffbs    |           0.907 |          0.056 |            24.989 |                34.187 |           0.24  |
| yasa       | SC       | REM%    | norm_reg_ffbs1   |           0.906 |          0.06  |            18.69  |                27.543 |           0.262 |
| yasa       | SC       | REM%    | norm_reg_ind     |           0.906 |          0.057 |            16.884 |                28.586 |           0.285 |
| yasa       | SC       | REM%    | norm_reg_plug    |           0.902 |          0.058 |            17.492 |                30.687 |           0.293 |
| yasa       | SC       | REM%    | norm_reg_plugc   |           0.904 |          0.059 |            17.4   |                29.499 |           0.272 |
| yasa       | SC       | REM%    | scp_abs          |           0.903 |          0.06  |            19.051 |                33.155 |          -0.082 |
| yasa       | SC       | REM%    | scp_abs_bc       |           0.901 |          0.059 |            18.69  |                33.208 |          -0.044 |
| yasa       | SC       | REM%    | scp_abs_cal      |           0.903 |          0.06  |            18.132 |                31.333 |          -0.022 |
| yasa       | SC       | REM%    | scp_abs_mu       |           0.905 |          0.055 |            25.97  |                37.202 |          -0     |
| yasa       | SC       | REML    | ba_loa           |           0.884 |          0.043 |           131.356 |               234.944 |          -0.234 |
| yasa       | SC       | REML    | bayes_pct        |           0.917 |          0.023 |           107.632 |               137.231 |           0.621 |
| yasa       | SC       | REML    | cqr_ffbs         |           0.918 |          0.046 |           107.176 |               137.861 |           0.622 |
| yasa       | SC       | REML    | cqr_qr           |           0.918 |          0.054 |           146.823 |               204.122 |           0.5   |
| yasa       | SC       | REML    | ind_pct          |           0.762 |          0.042 |            77.466 |               289.831 |           0.578 |
| yasa       | SC       | REML    | norm_entropy_reg |           0.91  |          0.042 |           121.407 |               188.658 |           0.22  |
| yasa       | SC       | REML    | norm_ffbs        |           0.912 |          0.042 |            86.665 |               141.995 |           0.686 |
| yasa       | SC       | REML    | norm_reg_ffbs    |           0.91  |          0.045 |            94.492 |               155.394 |           0.665 |
| yasa       | SC       | REML    | norm_reg_ffbs1   |           0.911 |          0.044 |            97.328 |               170.305 |           0.623 |
| yasa       | SC       | REML    | norm_reg_ind     |           0.911 |          0.048 |           145.142 |               230.512 |           0.202 |
| yasa       | SC       | REML    | norm_reg_plug    |           0.912 |          0.043 |           130.791 |               198.858 |           0.17  |
| yasa       | SC       | REML    | norm_reg_plugc   |           0.911 |          0.042 |           125.52  |               193.425 |           0.163 |
| yasa       | SC       | REML    | scp_abs          |           0.909 |          0.043 |           143.481 |               225.294 |          -0.215 |
| yasa       | SC       | REML    | scp_abs_bc       |           0.905 |          0.044 |           144.235 |               228.682 |          -0.244 |
| yasa       | SC       | REML    | scp_abs_cal      |           0.91  |          0.042 |           141.377 |               222.23  |          -0.257 |
| yasa       | SC       | REML    | scp_abs_mu       |           0.911 |          0.041 |           120.636 |               186.993 |           0.21  |
| yasa       | SC       | SOL     | ba_loa           |           0.937 |          0.037 |            34.384 |                67.047 |          -0.025 |
| yasa       | SC       | SOL     | bayes_pct        |           0.908 |          0.023 |            26.957 |                33.229 |           0.647 |
| yasa       | SC       | SOL     | cqr_ffbs         |           0.92  |          0.038 |            27.748 |                33.512 |           0.642 |
| yasa       | SC       | SOL     | cqr_qr           |           0.931 |          0.052 |            39.672 |                66.973 |           0.442 |
| yasa       | SC       | SOL     | ind_pct          |           0.559 |          0.043 |            11.417 |               139.556 |           0.636 |
| yasa       | SC       | SOL     | norm_entropy_reg |           0.909 |          0.049 |            30.727 |                83.887 |           0.035 |
| yasa       | SC       | SOL     | norm_ffbs        |           0.906 |          0.048 |            28.863 |                43.8   |           0.627 |
| yasa       | SC       | SOL     | norm_reg_ffbs    |           0.908 |          0.047 |            26.916 |                57.08  |           0.507 |
| yasa       | SC       | SOL     | norm_reg_ffbs1   |           0.904 |          0.049 |            27.052 |                43.863 |           0.572 |
| yasa       | SC       | SOL     | norm_reg_ind     |           0.906 |          0.053 |            35.674 |                97.241 |           0.292 |
| yasa       | SC       | SOL     | norm_reg_plug    |           0.904 |          0.046 |            32.816 |                53.117 |           0.413 |
| yasa       | SC       | SOL     | norm_reg_plugc   |           0.908 |          0.045 |            28.771 |                54.263 |           0.353 |
| yasa       | SC       | SOL     | scp_abs          |           0.91  |          0.047 |            33.407 |                71.414 |           0.023 |
| yasa       | SC       | SOL     | scp_abs_bc       |           0.909 |          0.047 |            26.73  |                67.445 |           0.139 |
| yasa       | SC       | SOL     | scp_abs_cal      |           0.912 |          0.045 |            30.83  |                72.613 |          -0.073 |
| yasa       | SC       | SOL     | scp_abs_mu       |           0.908 |          0.049 |            30.739 |                83.635 |          -0.044 |
| yasa       | SC       | TST     | ba_loa           |           0.903 |          0.053 |           111.289 |               171.435 |          -0.004 |
| yasa       | SC       | TST     | bayes_pct        |           0.532 |          0.043 |            31.408 |               207.748 |           0.4   |
| yasa       | SC       | TST     | cqr_ffbs         |           0.907 |          0.049 |            89.606 |               150.054 |           0.4   |
| yasa       | SC       | TST     | cqr_qr           |           0.922 |          0.053 |           136.102 |               172.999 |           0.222 |
| yasa       | SC       | TST     | ind_pct          |           0.197 |          0.032 |            12.267 |               405.094 |           0.422 |
| yasa       | SC       | TST     | norm_entropy_reg |           0.906 |          0.05  |            89.222 |               151.238 |           0.392 |
| yasa       | SC       | TST     | norm_ffbs        |           0.908 |          0.048 |            79.972 |               137.574 |           0.384 |
| yasa       | SC       | TST     | norm_reg_ffbs    |           0.907 |          0.049 |            85.281 |               145.628 |           0.384 |
| yasa       | SC       | TST     | norm_reg_ffbs1   |           0.908 |          0.048 |           107.709 |               170.724 |           0.509 |
| yasa       | SC       | TST     | norm_reg_ind     |           0.912 |          0.042 |           112.336 |               167.101 |           0.43  |
| yasa       | SC       | TST     | norm_reg_plug    |           0.909 |          0.05  |           114.992 |               172.264 |           0.296 |
| yasa       | SC       | TST     | norm_reg_plugc   |           0.907 |          0.048 |            93.476 |               151.715 |           0.387 |
| yasa       | SC       | TST     | scp_abs          |           0.907 |          0.049 |           131.56  |               199.028 |         nan     |
| yasa       | SC       | TST     | scp_abs_bc       |           0.902 |          0.052 |           109.199 |               171.818 |           0.004 |
| yasa       | SC       | TST     | scp_abs_cal      |           0.907 |          0.048 |           109.462 |               168.941 |         nan     |
| yasa       | SC       | TST     | scp_abs_mu       |           0.906 |          0.049 |            98.195 |               161.35  |          -0     |
| yasa       | SC       | WASO    | ba_loa           |           0.917 |          0.045 |           115.33  |               208.156 |           0.18  |
| yasa       | SC       | WASO    | bayes_pct        |           0.575 |          0.042 |           124.428 |               355.813 |           0.735 |
| yasa       | SC       | WASO    | cqr_ffbs         |           0.907 |          0.047 |           202.891 |               271.145 |           0.701 |
| yasa       | SC       | WASO    | cqr_qr           |           0.911 |          0.061 |           113.805 |               149.857 |           0.373 |
| yasa       | SC       | WASO    | ind_pct          |           0.04  |          0.016 |            57.068 |              1460     |           0.141 |
| yasa       | SC       | WASO    | norm_entropy_reg |           0.907 |          0.048 |           257.317 |               338.637 |           0.126 |
| yasa       | SC       | WASO    | norm_ffbs        |           0.903 |          0.049 |           226.792 |               302.304 |           0.782 |
| yasa       | SC       | WASO    | norm_reg_ffbs    |           0.907 |          0.049 |           230.586 |               310.634 |           0.731 |
| yasa       | SC       | WASO    | norm_reg_ffbs1   |           0.907 |          0.044 |           104.819 |               168.415 |           0.353 |
| yasa       | SC       | WASO    | norm_reg_ind     |           0.908 |          0.05  |           359.226 |               446.448 |           0.675 |
| yasa       | SC       | WASO    | norm_reg_plug    |           0.908 |          0.048 |           158.511 |               267.242 |           0.224 |
| yasa       | SC       | WASO    | norm_reg_plugc   |           0.907 |          0.047 |           157.683 |               255.048 |           0.185 |
| yasa       | SC       | WASO    | scp_abs          |           0.908 |          0.046 |           155.716 |               271.674 |          -0.01  |
| yasa       | SC       | WASO    | scp_abs_bc       |           0.902 |          0.051 |           108.392 |               211.613 |           0.218 |
| yasa       | SC       | WASO    | scp_abs_cal      |           0.906 |          0.047 |           156.752 |               263.717 |          -0.025 |
| yasa       | SC       | WASO    | scp_abs_mu       |           0.906 |          0.05  |           250.868 |               329.858 |           0.323 |
| yasa       | ST       | N1%     | ba_loa           |           0.846 |          0.115 |            14.524 |                21.505 |           0.054 |
| yasa       | ST       | N1%     | bayes_pct        |           0.5   |          0.073 |             5.008 |                44.381 |           0.376 |
| yasa       | ST       | N1%     | cqr_ffbs         |           0.91  |          0.107 |            17.552 |                24.825 |           0.202 |
| yasa       | ST       | N1%     | cqr_qr           |           0.898 |          0.117 |            21.675 |                30.966 |           0.233 |
| yasa       | ST       | N1%     | ind_pct          |           0.368 |          0.057 |             2.657 |                42.616 |           0.61  |
| yasa       | ST       | N1%     | norm_entropy_reg |           0.913 |          0.103 |            17.38  |                24.549 |           0.273 |
| yasa       | ST       | N1%     | norm_ffbs        |           0.914 |          0.102 |            16.183 |                23.248 |           0.286 |
| yasa       | ST       | N1%     | norm_reg_ffbs    |           0.913 |          0.103 |            16.945 |                24.341 |           0.249 |
| yasa       | ST       | N1%     | norm_reg_ffbs1   |           0.901 |          0.098 |            17.549 |                24.667 |           0.371 |
| yasa       | ST       | N1%     | norm_reg_ind     |           0.914 |          0.081 |            14.569 |                16.986 |           0.538 |
| yasa       | ST       | N1%     | norm_reg_plug    |           0.912 |          0.091 |            16.968 |                21.384 |           0.217 |
| yasa       | ST       | N1%     | norm_reg_plugc   |           0.911 |          0.093 |            15.817 |                20.982 |           0.335 |
| yasa       | ST       | N1%     | scp_abs          |           0.906 |          0.097 |            17.747 |                22.285 |           0.147 |
| yasa       | ST       | N1%     | scp_abs_bc       |           0.886 |          0.096 |            15.975 |                20.519 |           0.09  |
| yasa       | ST       | N1%     | scp_abs_cal      |           0.911 |          0.093 |            16.667 |                21.019 |           0.229 |
| yasa       | ST       | N1%     | scp_abs_mu       |           0.909 |          0.109 |            18.016 |                25.372 |           0.137 |
| yasa       | ST       | N2%     | ba_loa           |           0.83  |          0.127 |            30.731 |                45.599 |          -0.005 |
| yasa       | ST       | N2%     | bayes_pct        |           0.362 |          0.093 |            10.251 |                87.289 |          -0.142 |
| yasa       | ST       | N2%     | cqr_ffbs         |           0.889 |          0.109 |            32.777 |                40.331 |          -0.142 |
| yasa       | ST       | N2%     | cqr_qr           |           0.871 |          0.13  |            53.861 |                73.753 |          -0.092 |
| yasa       | ST       | N2%     | ind_pct          |           0.067 |          0.037 |             3.575 |               126.404 |          -0.102 |
| yasa       | ST       | N2%     | norm_entropy_reg |           0.895 |          0.11  |            32.241 |                39.124 |          -0.102 |
| yasa       | ST       | N2%     | norm_ffbs        |           0.899 |          0.108 |            35.386 |                40.913 |          -0.145 |
| yasa       | ST       | N2%     | norm_reg_ffbs    |           0.89  |          0.109 |            33.315 |                40.339 |          -0.145 |
| yasa       | ST       | N2%     | norm_reg_ffbs1   |           0.889 |          0.106 |            42.097 |                53.905 |           0.051 |
| yasa       | ST       | N2%     | norm_reg_ind     |           0.89  |          0.107 |            33.481 |                41.377 |          -0.152 |
| yasa       | ST       | N2%     | norm_reg_plug    |           0.894 |          0.107 |            35.941 |                42.913 |          -0.136 |
| yasa       | ST       | N2%     | norm_reg_plugc   |           0.901 |          0.104 |            37.653 |                45.666 |          -0.031 |
| yasa       | ST       | N2%     | scp_abs          |           0.893 |          0.101 |            34.496 |                42.836 |           0.163 |
| yasa       | ST       | N2%     | scp_abs_bc       |           0.852 |          0.121 |            32.785 |                45.478 |           0.025 |
| yasa       | ST       | N2%     | scp_abs_cal      |           0.904 |          0.107 |            36.349 |                44.246 |           0.182 |
| yasa       | ST       | N2%     | scp_abs_mu       |           0.888 |          0.111 |            32.315 |                40.74  |          -0.126 |
| yasa       | ST       | N3%     | ba_loa           |           0.839 |          0.112 |            23.704 |                34.938 |           0.171 |
| yasa       | ST       | N3%     | bayes_pct        |           0.445 |          0.105 |             7.541 |                72.547 |           0.274 |
| yasa       | ST       | N3%     | cqr_ffbs         |           0.913 |          0.085 |            26.602 |                29.877 |           0.211 |
| yasa       | ST       | N3%     | cqr_qr           |           0.887 |          0.125 |            39.645 |                54.359 |           0.139 |
| yasa       | ST       | N3%     | ind_pct          |           0.157 |          0.064 |             2.401 |               105.605 |           0.466 |
| yasa       | ST       | N3%     | norm_entropy_reg |           0.908 |          0.092 |            26.71  |                29.376 |           0.208 |
| yasa       | ST       | N3%     | norm_ffbs        |           0.907 |          0.096 |            26.108 |                29.53  |           0.259 |
| yasa       | ST       | N3%     | norm_reg_ffbs    |           0.913 |          0.087 |            26.141 |                29.065 |           0.247 |
| yasa       | ST       | N3%     | norm_reg_ffbs1   |           0.897 |          0.103 |            32.19  |                36.151 |           0.129 |
| yasa       | ST       | N3%     | norm_reg_ind     |           0.911 |          0.087 |            25.181 |                28.008 |           0.375 |
| yasa       | ST       | N3%     | norm_reg_plug    |           0.902 |          0.102 |            31.014 |                36.462 |           0.156 |
| yasa       | ST       | N3%     | norm_reg_plugc   |           0.901 |          0.1   |            25.922 |                29.401 |           0.277 |
| yasa       | ST       | N3%     | scp_abs          |           0.908 |          0.098 |            31.91  |                38.876 |          -0.043 |
| yasa       | ST       | N3%     | scp_abs_bc       |           0.881 |          0.1   |            26.393 |                33.748 |           0.157 |
| yasa       | ST       | N3%     | scp_abs_cal      |           0.907 |          0.092 |            26.012 |                28.659 |           0.16  |
| yasa       | ST       | N3%     | scp_abs_mu       |           0.912 |          0.09  |            27.175 |                31.236 |          -0.053 |
| yasa       | ST       | REM%    | ba_loa           |           0.864 |          0.105 |            17.28  |                28.137 |           0.025 |
| yasa       | ST       | REM%    | bayes_pct        |           0.275 |          0.063 |             6.69  |                60.286 |           0.129 |
| yasa       | ST       | REM%    | cqr_ffbs         |           0.9   |          0.103 |            23.861 |                28.52  |           0.148 |
| yasa       | ST       | REM%    | cqr_qr           |           0.886 |          0.124 |            31.004 |                41.451 |           0.147 |
| yasa       | ST       | REM%    | ind_pct          |           0.182 |          0.062 |             2.242 |                65.053 |           0.01  |
| yasa       | ST       | REM%    | norm_entropy_reg |           0.9   |          0.1   |            24.353 |                29.817 |          -0.118 |
| yasa       | ST       | REM%    | norm_ffbs        |           0.913 |          0.113 |            25.263 |                30.089 |           0.173 |
| yasa       | ST       | REM%    | norm_reg_ffbs    |           0.898 |          0.102 |            24.017 |                28.702 |           0.144 |
| yasa       | ST       | REM%    | norm_reg_ffbs1   |           0.903 |          0.097 |            21.865 |                27.998 |           0.157 |
| yasa       | ST       | REM%    | norm_reg_ind     |           0.902 |          0.104 |            23.275 |                31.607 |           0.046 |
| yasa       | ST       | REM%    | norm_reg_plug    |           0.905 |          0.098 |            21.981 |                29.897 |          -0.155 |
| yasa       | ST       | REM%    | norm_reg_plugc   |           0.903 |          0.103 |            23.34  |                30.869 |          -0.15  |
| yasa       | ST       | REM%    | scp_abs          |           0.906 |          0.096 |            21.263 |                28.773 |           0.142 |
| yasa       | ST       | REM%    | scp_abs_bc       |           0.889 |          0.105 |            19.842 |                28.781 |           0.063 |
| yasa       | ST       | REM%    | scp_abs_cal      |           0.904 |          0.1   |            22.328 |                29.438 |           0.094 |
| yasa       | ST       | REM%    | scp_abs_mu       |           0.907 |          0.094 |            23.648 |                27.993 |           0.1   |
| yasa       | ST       | REML    | ba_loa           |           0.848 |          0.083 |           122.65  |               235.529 |           0.066 |
| yasa       | ST       | REML    | bayes_pct        |           0.954 |          0.031 |           126.629 |               134.126 |           0.385 |
| yasa       | ST       | REML    | cqr_ffbs         |           0.908 |          0.09  |           127.375 |               138.255 |           0.389 |
| yasa       | ST       | REML    | cqr_qr           |           0.899 |          0.111 |           174.499 |               231.524 |           0.203 |
| yasa       | ST       | REML    | ind_pct          |           0.634 |          0.078 |            96.201 |               439.6   |           0.162 |
| yasa       | ST       | REML    | norm_entropy_reg |           0.92  |          0.099 |           162.847 |               215.347 |          -0.013 |
| yasa       | ST       | REML    | norm_ffbs        |           0.92  |          0.1   |           146.363 |               200.065 |           0.66  |
| yasa       | ST       | REML    | norm_reg_ffbs    |           0.921 |          0.098 |           148.082 |               199.274 |           0.64  |
| yasa       | ST       | REML    | norm_reg_ffbs1   |           0.91  |          0.094 |           151.282 |               217.639 |           0.484 |
| yasa       | ST       | REML    | norm_reg_ind     |           0.915 |          0.088 |           197.432 |               241.021 |          -0.021 |
| yasa       | ST       | REML    | norm_reg_plug    |           0.905 |          0.095 |           157.515 |               207.678 |           0.063 |
| yasa       | ST       | REML    | norm_reg_plugc   |           0.907 |          0.091 |           156.029 |               205.72  |           0.001 |
| yasa       | ST       | REML    | scp_abs          |           0.907 |          0.095 |           168.973 |               215.41  |          -0.285 |
| yasa       | ST       | REML    | scp_abs_bc       |           0.898 |          0.095 |           157.288 |               213.2   |           0.119 |
| yasa       | ST       | REML    | scp_abs_cal      |           0.906 |          0.092 |           169.658 |               215.422 |          -0.434 |
| yasa       | ST       | REML    | scp_abs_mu       |           0.92  |          0.099 |           151.704 |               196.982 |           0.301 |
| yasa       | ST       | SOL     | ba_loa           |           0.905 |          0.101 |            11.308 |                17.93  |          -0.047 |
| yasa       | ST       | SOL     | bayes_pct        |           0.977 |          0.023 |            17.92  |                28.321 |           0.528 |
| yasa       | ST       | SOL     | cqr_ffbs         |           0.959 |          0.083 |            17.712 |                28.896 |           0.527 |
| yasa       | ST       | SOL     | cqr_qr           |           0.883 |          0.131 |            19.572 |                29.845 |           0.119 |
| yasa       | ST       | SOL     | ind_pct          |           0.659 |          0.091 |             8.648 |                53.844 |           0.632 |
| yasa       | ST       | SOL     | norm_entropy_reg |           0.898 |          0.106 |            24.941 |                45.449 |           0.245 |
| yasa       | ST       | SOL     | norm_ffbs        |           0.919 |          0.095 |            16.912 |                31.848 |           0.563 |
| yasa       | ST       | SOL     | norm_reg_ffbs    |           0.896 |          0.108 |            18.889 |                37.311 |           0.605 |
| yasa       | ST       | SOL     | norm_reg_ffbs1   |           0.909 |          0.086 |            13.603 |                17.788 |           0.443 |
| yasa       | ST       | SOL     | norm_reg_ind     |           0.913 |          0.107 |            23.673 |                52.382 |           0.339 |
| yasa       | ST       | SOL     | norm_reg_plug    |           0.905 |          0.091 |            16.817 |                20.662 |           0.18  |
| yasa       | ST       | SOL     | norm_reg_plugc   |           0.909 |          0.085 |            14.173 |                34.696 |           0.427 |
| yasa       | ST       | SOL     | scp_abs          |           0.915 |          0.078 |            19.534 |                26.658 |           0.189 |
| yasa       | ST       | SOL     | scp_abs_bc       |           0.902 |          0.096 |            12.371 |                19.335 |           0.08  |
| yasa       | ST       | SOL     | scp_abs_cal      |           0.915 |          0.083 |            15.086 |                36.788 |          -0.082 |
| yasa       | ST       | SOL     | scp_abs_mu       |           0.901 |          0.104 |            25.016 |                46.149 |           0.074 |
| yasa       | ST       | TST     | ba_loa           |           0.896 |          0.098 |            55.671 |                96.331 |          -0.005 |
| yasa       | ST       | TST     | bayes_pct        |           0.862 |          0.057 |            22.393 |                53.473 |           0.401 |
| yasa       | ST       | TST     | cqr_ffbs         |           0.914 |          0.077 |            38.786 |                57.603 |           0.401 |
| yasa       | ST       | TST     | cqr_qr           |           0.915 |          0.108 |            72.883 |                94.09  |           0.074 |
| yasa       | ST       | TST     | ind_pct          |           0.295 |          0.073 |             8.093 |               117.3   |           0.589 |
| yasa       | ST       | TST     | norm_entropy_reg |           0.907 |          0.09  |            39.127 |                59.603 |           0.355 |
| yasa       | ST       | TST     | norm_ffbs        |           0.91  |          0.087 |            36.992 |                54.944 |           0.415 |
| yasa       | ST       | TST     | norm_reg_ffbs    |           0.908 |          0.092 |            38.884 |                58.6   |           0.415 |
| yasa       | ST       | TST     | norm_reg_ffbs1   |           0.905 |          0.092 |            36.6   |                51.328 |           0.489 |
| yasa       | ST       | TST     | norm_reg_ind     |           0.908 |          0.104 |            40.354 |                50.208 |           0.602 |
| yasa       | ST       | TST     | norm_reg_plug    |           0.915 |          0.099 |            88.689 |               113.926 |           0.49  |
| yasa       | ST       | TST     | norm_reg_plugc   |           0.916 |          0.08  |            33.292 |                40.62  |           0.475 |
| yasa       | ST       | TST     | scp_abs          |           0.904 |          0.091 |           108.606 |               144.244 |         nan     |
| yasa       | ST       | TST     | scp_abs_bc       |           0.902 |          0.095 |            63.07  |                98.657 |          -0.012 |
| yasa       | ST       | TST     | scp_abs_cal      |           0.921 |          0.081 |            34.288 |                42.513 |         nan     |
| yasa       | ST       | TST     | scp_abs_mu       |           0.907 |          0.091 |            41.413 |                63.009 |           0.1   |
| yasa       | ST       | WASO    | ba_loa           |           0.903 |          0.111 |            37.079 |                71.352 |           0.365 |
| yasa       | ST       | WASO    | bayes_pct        |           0.794 |          0.068 |            30.577 |                78.276 |           0.591 |
| yasa       | ST       | WASO    | cqr_ffbs         |           0.913 |          0.088 |            52.408 |                78.917 |           0.368 |
| yasa       | ST       | WASO    | cqr_qr           |           0.904 |          0.118 |            58.971 |                87.294 |           0.003 |
| yasa       | ST       | WASO    | ind_pct          |           0.208 |          0.069 |            14.734 |               140.908 |           0.663 |
| yasa       | ST       | WASO    | norm_entropy_reg |           0.903 |          0.09  |            58.414 |                95.002 |           0.069 |
| yasa       | ST       | WASO    | norm_ffbs        |           0.915 |          0.08  |            51.588 |                73.501 |           0.563 |
| yasa       | ST       | WASO    | norm_reg_ffbs    |           0.911 |          0.087 |            53.189 |                82.146 |           0.415 |
| yasa       | ST       | WASO    | norm_reg_ffbs1   |           0.915 |          0.084 |            36.939 |                52.083 |           0.244 |
| yasa       | ST       | WASO    | norm_reg_ind     |           0.915 |          0.075 |            48.025 |                64.083 |           0.499 |
| yasa       | ST       | WASO    | norm_reg_plug    |           0.902 |          0.097 |            68.733 |                94.717 |           0.215 |
| yasa       | ST       | WASO    | norm_reg_plugc   |           0.917 |          0.08  |            34.429 |                46.725 |           0.206 |
| yasa       | ST       | WASO    | scp_abs          |           0.902 |          0.095 |            70.167 |               104.308 |           0.015 |
| yasa       | ST       | WASO    | scp_abs_bc       |           0.899 |          0.095 |            34.939 |                69.111 |           0.413 |
| yasa       | ST       | WASO    | scp_abs_cal      |           0.912 |          0.08  |            35.376 |                49.831 |           0.027 |
| yasa       | ST       | WASO    | scp_abs_mu       |           0.902 |          0.093 |            59.453 |                96.742 |           0.066 |
| lgbm_sc_s0 | HMC      | N1%     | ba_loa           |           0.916 |          0.04  |            28.287 |                43.043 |           0.409 |
| lgbm_sc_s0 | HMC      | N1%     | bayes_pct        |           0.389 |          0.041 |             5.77  |                68.47  |           0.125 |
| lgbm_sc_s0 | HMC      | N1%     | cqr_ffbs         |           0.905 |          0.045 |            22.52  |                39.847 |           0.113 |
| lgbm_sc_s0 | HMC      | N1%     | cqr_qr           |           0.921 |          0.057 |            28.535 |                39.47  |           0.245 |
| lgbm_sc_s0 | HMC      | N1%     | ind_pct          |           0.211 |          0.033 |             3.675 |                80.268 |           0.203 |
| lgbm_sc_s0 | HMC      | N1%     | norm_entropy_reg |           0.906 |          0.045 |            22.201 |                38.683 |           0.184 |
| lgbm_sc_s0 | HMC      | N1%     | norm_ffbs        |           0.907 |          0.047 |            23.303 |                40.552 |           0.147 |
| lgbm_sc_s0 | HMC      | N1%     | norm_reg_ffbs    |           0.905 |          0.046 |            22.755 |                39.957 |           0.139 |
| lgbm_sc_s0 | HMC      | N1%     | norm_reg_ffbs1   |           0.907 |          0.046 |            24.429 |                41.478 |           0.212 |
| lgbm_sc_s0 | HMC      | N1%     | norm_reg_ind     |           0.907 |          0.046 |            21.004 |                37.334 |           0.175 |
| lgbm_sc_s0 | HMC      | N1%     | norm_reg_plug    |           0.911 |          0.047 |            39.647 |                50.744 |           0.474 |
| lgbm_sc_s0 | HMC      | N1%     | norm_reg_plugc   |           0.905 |          0.048 |            23.4   |                42.617 |           0.179 |
| lgbm_sc_s0 | HMC      | N1%     | scp_abs          |           0.911 |          0.047 |            41.357 |                53.911 |           0.407 |
| lgbm_sc_s0 | HMC      | N1%     | scp_abs_bc       |           0.908 |          0.048 |            27.728 |                43.657 |           0.402 |
| lgbm_sc_s0 | HMC      | N1%     | scp_abs_cal      |           0.903 |          0.049 |            22.905 |                41.77  |           0.183 |
| lgbm_sc_s0 | HMC      | N1%     | scp_abs_mu       |           0.905 |          0.045 |            22.291 |                39.924 |           0.094 |


# S3. Paired comparisons (leave-one-subject-out; Wilcoxon signed-rank on per-subject mean interval score; Holm within cohort and stager)

| stager     | cohort   | param   | baseline         |   n_subjects |   mean_is_proposed |   mean_is_baseline |   r_rb |     p |   p_holm |
|:-----------|:---------|:--------|:-----------------|-------------:|-------------------:|-------------------:|-------:|------:|---------:|
| yasa       | HMC      | N1%     | ba_loa           |          151 |             34.469 |             38.088 | -0.688 | 0     |    0     |
| yasa       | HMC      | N1%     | scp_abs          |          151 |             34.469 |             41.659 | -0.289 | 0.002 |    0.053 |
| yasa       | HMC      | N1%     | scp_abs_bc       |          151 |             34.469 |             39.601 | -0.543 | 0     |    0     |
| yasa       | HMC      | N1%     | scp_abs_cal      |          151 |             34.469 |             40.93  | -0.215 | 0.022 |    0.396 |
| yasa       | HMC      | N1%     | scp_abs_mu       |          151 |             34.469 |             36.389 | -0.263 | 0.005 |    0.101 |
| yasa       | HMC      | N1%     | norm_reg_plugc   |          151 |             34.469 |             39.156 | -0.367 | 0     |    0.003 |
| yasa       | HMC      | N1%     | cqr_ffbs         |          151 |             34.469 |             34.628 | -0.331 | 0     |    0.011 |
| yasa       | HMC      | N1%     | cqr_qr           |          151 |             34.469 |             30.911 | -0.127 | 0.175 |    1     |
| yasa       | HMC      | N1%     | norm_entropy_reg |          151 |             34.469 |             33.684 | -0.167 | 0.076 |    0.985 |
| yasa       | HMC      | N1%     | norm_ffbs        |          151 |             34.469 |             34.713 | -0.144 | 0.124 |    1     |
| yasa       | HMC      | N2%     | ba_loa           |          151 |             34.491 |             46.201 | -0.811 | 0     |    0     |
| yasa       | HMC      | N2%     | scp_abs          |          151 |             34.491 |             65.293 | -0.855 | 0     |    0     |
| yasa       | HMC      | N2%     | scp_abs_bc       |          151 |             34.491 |             45.439 | -0.751 | 0     |    0     |
| yasa       | HMC      | N2%     | scp_abs_cal      |          151 |             34.491 |             52.749 | -0.828 | 0     |    0     |
| yasa       | HMC      | N2%     | scp_abs_mu       |          151 |             34.491 |             35.114 | -0.182 | 0.052 |    0.783 |
| yasa       | HMC      | N2%     | norm_reg_plugc   |          151 |             34.491 |             51.348 | -0.827 | 0     |    0     |
| yasa       | HMC      | N2%     | cqr_ffbs         |          151 |             34.491 |             34.617 | -0.077 | 0.411 |    1     |
| yasa       | HMC      | N2%     | cqr_qr           |          151 |             34.491 |             35.913 |  0.266 | 0.005 |    0.101 |
| yasa       | HMC      | N2%     | norm_entropy_reg |          151 |             34.491 |             34.284 | -0.123 | 0.19  |    1     |
| yasa       | HMC      | N2%     | norm_ffbs        |          151 |             34.491 |             34.709 | -0.374 | 0     |    0.002 |
| yasa       | HMC      | N3%     | ba_loa           |          151 |             35.559 |             33.113 |  0.731 | 0     |    0     |
| yasa       | HMC      | N3%     | scp_abs          |          151 |             35.559 |             39.527 |  0.146 | 0.12  |    1     |
| yasa       | HMC      | N3%     | scp_abs_bc       |          151 |             35.559 |             33.006 |  0.742 | 0     |    0     |
| yasa       | HMC      | N3%     | scp_abs_cal      |          151 |             35.559 |             34.39  |  0.646 | 0     |    0     |
| yasa       | HMC      | N3%     | scp_abs_mu       |          151 |             35.559 |             37.266 | -0.208 | 0.027 |    0.456 |
| yasa       | HMC      | N3%     | norm_reg_plugc   |          151 |             35.559 |             34.765 |  0.706 | 0     |    0     |
| yasa       | HMC      | N3%     | cqr_ffbs         |          151 |             35.559 |             35.611 | -0.131 | 0.162 |    1     |
| yasa       | HMC      | N3%     | cqr_qr           |          151 |             35.559 |             42.174 |  0.176 | 0.061 |    0.856 |
| yasa       | HMC      | N3%     | norm_entropy_reg |          151 |             35.559 |             36.804 | -0.266 | 0.005 |    0.101 |
| yasa       | HMC      | N3%     | norm_ffbs        |          151 |             35.559 |             35.736 |  0.006 | 0.951 |    1     |
| yasa       | HMC      | REM%    | ba_loa           |          151 |             26.661 |             25.05  |  0.598 | 0     |    0     |
| yasa       | HMC      | REM%    | scp_abs          |          151 |             26.661 |             25.379 |  0.654 | 0     |    0     |
| yasa       | HMC      | REM%    | scp_abs_bc       |          151 |             26.661 |             25.42  |  0.668 | 0     |    0     |
| yasa       | HMC      | REM%    | scp_abs_cal      |          151 |             26.661 |             23.33  |  0.74  | 0     |    0     |
| yasa       | HMC      | REM%    | scp_abs_mu       |          151 |             26.661 |             27.448 |  0.207 | 0.028 |    0.456 |
| yasa       | HMC      | REM%    | norm_reg_plugc   |          151 |             26.661 |             22.255 |  0.814 | 0     |    0     |
| yasa       | HMC      | REM%    | cqr_ffbs         |          151 |             26.661 |             26.784 |  0.538 | 0     |    0     |
| yasa       | HMC      | REM%    | cqr_qr           |          151 |             26.661 |             22.236 |  0.827 | 0     |    0     |
| yasa       | HMC      | REM%    | norm_entropy_reg |          151 |             26.661 |             26.708 |  0.154 | 0.101 |    1     |
| yasa       | HMC      | REM%    | norm_ffbs        |          151 |             26.661 |             27.328 | -0.417 | 0     |    0     |
| yasa       | HMC      | REML    | ba_loa           |          150 |            309.681 |            312.025 | -0.369 | 0     |    0.003 |
| yasa       | HMC      | REML    | scp_abs          |          150 |            309.681 |            310.983 | -0.087 | 0.356 |    1     |
| yasa       | HMC      | REML    | scp_abs_bc       |          150 |            309.681 |            310.925 | -0.285 | 0.002 |    0.062 |
| yasa       | HMC      | REML    | scp_abs_cal      |          150 |            309.681 |            360.653 | -0.405 | 0     |    0.001 |
| yasa       | HMC      | REML    | scp_abs_mu       |          150 |            309.681 |            374.685 | -0.74  | 0     |    0     |
| yasa       | HMC      | REML    | norm_reg_plugc   |          150 |            309.681 |            315.455 | -0.392 | 0     |    0.001 |
| yasa       | HMC      | REML    | cqr_ffbs         |          150 |            309.681 |            290.379 |  0.701 | 0     |    0     |
| yasa       | HMC      | REML    | cqr_qr           |          150 |            309.681 |            270.377 | -0.558 | 0     |    0     |
| yasa       | HMC      | REML    | norm_entropy_reg |          150 |            309.681 |            347.455 | -0.633 | 0     |    0     |
| yasa       | HMC      | REML    | norm_ffbs        |          150 |            309.681 |            303.496 |  0.462 | 0     |    0     |
| yasa       | HMC      | SOL     | ba_loa           |          151 |             71.259 |             47.328 | -0.637 | 0     |    0     |
| yasa       | HMC      | SOL     | scp_abs          |          151 |             71.259 |             59.629 | -0.683 | 0     |    0     |
| yasa       | HMC      | SOL     | scp_abs_bc       |          151 |             71.259 |             51.057 | -0.277 | 0.003 |    0.074 |
| yasa       | HMC      | SOL     | scp_abs_cal      |          151 |             71.259 |             54.142 | -0.109 | 0.243 |    1     |
| yasa       | HMC      | SOL     | scp_abs_mu       |          151 |             71.259 |             76.77  | -0.785 | 0     |    0     |
| yasa       | HMC      | SOL     | norm_reg_plugc   |          151 |             71.259 |             49.552 |  0.712 | 0     |    0     |
| yasa       | HMC      | SOL     | cqr_ffbs         |          151 |             71.259 |             55.501 |  0.644 | 0     |    0     |
| yasa       | HMC      | SOL     | cqr_qr           |          151 |             71.259 |             33.841 |  0.584 | 0     |    0     |
| yasa       | HMC      | SOL     | norm_entropy_reg |          151 |             71.259 |             78.347 | -0.811 | 0     |    0     |
| yasa       | HMC      | SOL     | norm_ffbs        |          151 |             71.259 |             62.587 |  0.808 | 0     |    0     |
| yasa       | HMC      | TST     | ba_loa           |          151 |            144.878 |            206.14  | -0.769 | 0     |    0     |
| yasa       | HMC      | TST     | scp_abs          |          151 |            144.878 |            253.318 | -0.838 | 0     |    0     |
| yasa       | HMC      | TST     | scp_abs_bc       |          151 |            144.878 |            203.642 | -0.761 | 0     |    0     |
| yasa       | HMC      | TST     | scp_abs_cal      |          151 |            144.878 |            162.371 | -0.589 | 0     |    0     |
| yasa       | HMC      | TST     | scp_abs_mu       |          151 |            144.878 |            161.002 | -0.724 | 0     |    0     |
| yasa       | HMC      | TST     | norm_reg_plugc   |          151 |            144.878 |            141.218 | -0.773 | 0     |    0     |
| yasa       | HMC      | TST     | cqr_ffbs         |          151 |            144.878 |            148.999 | -0.601 | 0     |    0     |
| yasa       | HMC      | TST     | cqr_qr           |          151 |            144.878 |            124.596 |  0.116 | 0.215 |    1     |
| yasa       | HMC      | TST     | norm_entropy_reg |          151 |            144.878 |            149.861 | -0.547 | 0     |    0     |
| yasa       | HMC      | TST     | norm_ffbs        |          151 |            144.878 |            125.989 |  0.613 | 0     |    0     |
| yasa       | HMC      | WASO    | ba_loa           |          151 |            146.908 |            171.391 | -0.758 | 0     |    0     |
| yasa       | HMC      | WASO    | scp_abs          |          151 |            146.908 |            228.844 | -0.825 | 0     |    0     |
| yasa       | HMC      | WASO    | scp_abs_bc       |          151 |            146.908 |            175.576 | -0.478 | 0     |    0     |
| yasa       | HMC      | WASO    | scp_abs_cal      |          151 |            146.908 |            156.957 | -0.713 | 0     |    0     |
| yasa       | HMC      | WASO    | scp_abs_mu       |          151 |            146.908 |            155.581 | -0.458 | 0     |    0     |
| yasa       | HMC      | WASO    | norm_reg_plugc   |          151 |            146.908 |            133.018 | -0.565 | 0     |    0     |
| yasa       | HMC      | WASO    | cqr_ffbs         |          151 |            146.908 |            146.936 | -0.22  | 0.019 |    0.366 |
| yasa       | HMC      | WASO    | cqr_qr           |          151 |            146.908 |            125.085 |  0.155 | 0.098 |    1     |
| yasa       | HMC      | WASO    | norm_entropy_reg |          151 |            146.908 |            150.394 | -0.269 | 0.004 |    0.095 |
| yasa       | HMC      | WASO    | norm_ffbs        |          151 |            146.908 |            133.982 |  0.343 | 0     |    0.007 |
| yasa       | SC       | N1%     | ba_loa           |           78 |             39.561 |             42.097 | -0.474 | 0     |    0.007 |
| yasa       | SC       | N1%     | scp_abs          |           78 |             39.561 |             45.618 | -0.544 | 0     |    0.001 |
| yasa       | SC       | N1%     | scp_abs_bc       |           78 |             39.561 |             41.39  |  0.044 | 0.733 |    1     |
| yasa       | SC       | N1%     | scp_abs_cal      |           78 |             39.561 |             44.039 | -0.479 | 0     |    0.007 |
| yasa       | SC       | N1%     | scp_abs_mu       |           78 |             39.561 |             42.019 | -0.464 | 0     |    0.009 |
| yasa       | SC       | N1%     | norm_reg_plugc   |           78 |             39.561 |             43.909 | -0.471 | 0     |    0.008 |
| yasa       | SC       | N1%     | cqr_ffbs         |           78 |             39.561 |             40.028 | -0.079 | 0.545 |    1     |
| yasa       | SC       | N1%     | cqr_qr           |           78 |             39.561 |             38.303 | -0.035 | 0.786 |    1     |
| yasa       | SC       | N1%     | norm_entropy_reg |           78 |             39.561 |             40.493 |  0.115 | 0.377 |    1     |
| yasa       | SC       | N1%     | norm_ffbs        |           78 |             39.561 |             38.834 | -0.108 | 0.407 |    1     |
| yasa       | SC       | N2%     | ba_loa           |           78 |             42.529 |             55.023 | -0.887 | 0     |    0     |
| yasa       | SC       | N2%     | scp_abs          |           78 |             42.529 |             59.471 | -0.9   | 0     |    0     |
| yasa       | SC       | N2%     | scp_abs_bc       |           78 |             42.529 |             54.885 | -0.772 | 0     |    0     |
| yasa       | SC       | N2%     | scp_abs_cal      |           78 |             42.529 |             62.428 | -0.95  | 0     |    0     |
| yasa       | SC       | N2%     | scp_abs_mu       |           78 |             42.529 |             44.058 | -0.083 | 0.525 |    1     |
| yasa       | SC       | N2%     | norm_reg_plugc   |           78 |             42.529 |             58.804 | -0.91  | 0     |    0     |
| yasa       | SC       | N2%     | cqr_ffbs         |           78 |             42.529 |             42.52  |  0.378 | 0.004 |    0.074 |
| yasa       | SC       | N2%     | cqr_qr           |           78 |             42.529 |             44.431 | -0.073 | 0.575 |    1     |
| yasa       | SC       | N2%     | norm_entropy_reg |           78 |             42.529 |             41.296 |  0.526 | 0     |    0.002 |
| yasa       | SC       | N2%     | norm_ffbs        |           78 |             42.529 |             41.089 |  0.435 | 0.001 |    0.02  |
| yasa       | SC       | N3%     | ba_loa           |           78 |             22.395 |             25.212 | -0.218 | 0.095 |    1     |
| yasa       | SC       | N3%     | scp_abs          |           78 |             22.395 |             34.856 | -0.815 | 0     |    0     |
| yasa       | SC       | N3%     | scp_abs_bc       |           78 |             22.395 |             25.149 |  0.102 | 0.436 |    1     |
| yasa       | SC       | N3%     | scp_abs_cal      |           78 |             22.395 |             27.623 | -0.877 | 0     |    0     |
| yasa       | SC       | N3%     | scp_abs_mu       |           78 |             22.395 |             25.869 | -0.886 | 0     |    0     |
| yasa       | SC       | N3%     | norm_reg_plugc   |           78 |             22.395 |             23.878 | -0.279 | 0.032 |    0.584 |
| yasa       | SC       | N3%     | cqr_ffbs         |           78 |             22.395 |             22.616 | -0.698 | 0     |    0     |
| yasa       | SC       | N3%     | cqr_qr           |           78 |             22.395 |             23.549 | -0.133 | 0.306 |    1     |
| yasa       | SC       | N3%     | norm_entropy_reg |           78 |             22.395 |             24.057 | -0.644 | 0     |    0     |
| yasa       | SC       | N3%     | norm_ffbs        |           78 |             22.395 |             21.995 |  0.516 | 0     |    0.002 |
| yasa       | SC       | REM%    | ba_loa           |           78 |             32.7   |             33.183 |  0.098 | 0.45  |    1     |
| yasa       | SC       | REM%    | scp_abs          |           78 |             32.7   |             31.719 |  0.728 | 0     |    0     |
| yasa       | SC       | REM%    | scp_abs_bc       |           78 |             32.7   |             31.764 |  0.779 | 0     |    0     |
| yasa       | SC       | REM%    | scp_abs_cal      |           78 |             32.7   |             30.06  |  0.784 | 0     |    0     |
| yasa       | SC       | REM%    | scp_abs_mu       |           78 |             32.7   |             35.626 | -0.537 | 0     |    0.001 |
| yasa       | SC       | REM%    | norm_reg_plugc   |           78 |             32.7   |             28.237 |  0.807 | 0     |    0     |
| yasa       | SC       | REM%    | cqr_ffbs         |           78 |             32.7   |             34.729 | -0.786 | 0     |    0     |
| yasa       | SC       | REM%    | cqr_qr           |           78 |             32.7   |             29.593 |  0.209 | 0.108 |    1     |
| yasa       | SC       | REM%    | norm_entropy_reg |           78 |             32.7   |             35.062 | -0.569 | 0     |    0.001 |
| yasa       | SC       | REM%    | norm_ffbs        |           78 |             32.7   |             30.938 |  0.074 | 0.572 |    1     |
| yasa       | SC       | REML    | ba_loa           |           78 |            152.473 |            226.735 | -0.717 | 0     |    0     |
| yasa       | SC       | REML    | scp_abs          |           78 |            152.473 |            222.119 | -0.736 | 0     |    0     |
| yasa       | SC       | REML    | scp_abs_bc       |           78 |            152.473 |            220.325 | -0.698 | 0     |    0     |
| yasa       | SC       | REML    | scp_abs_cal      |           78 |            152.473 |            219.167 | -0.692 | 0     |    0     |
| yasa       | SC       | REML    | scp_abs_mu       |           78 |            152.473 |            183.357 | -0.657 | 0     |    0     |
| yasa       | SC       | REML    | norm_reg_plugc   |           78 |            152.473 |            188.851 | -0.672 | 0     |    0     |
| yasa       | SC       | REML    | cqr_ffbs         |           78 |            152.473 |            137.157 | -0.205 | 0.116 |    1     |
| yasa       | SC       | REML    | cqr_qr           |           78 |            152.473 |            167.665 | -0.331 | 0.011 |    0.212 |
| yasa       | SC       | REML    | norm_entropy_reg |           78 |            152.473 |            183.725 | -0.673 | 0     |    0     |
| yasa       | SC       | REML    | norm_ffbs        |           78 |            152.473 |            139.325 |  0.531 | 0     |    0.002 |
| yasa       | SC       | SOL     | ba_loa           |           78 |             56.109 |             65.031 | -0.712 | 0     |    0     |
| yasa       | SC       | SOL     | scp_abs          |           78 |             56.109 |             69.513 | -0.675 | 0     |    0     |
| yasa       | SC       | SOL     | scp_abs_bc       |           78 |             56.109 |             64.925 | -0.401 | 0.002 |    0.046 |
| yasa       | SC       | SOL     | scp_abs_cal      |           78 |             56.109 |             73.054 | -0.671 | 0     |    0     |
| yasa       | SC       | SOL     | scp_abs_mu       |           78 |             56.109 |             81.022 | -0.677 | 0     |    0     |
| yasa       | SC       | SOL     | norm_reg_plugc   |           78 |             56.109 |             52.635 | -0.518 | 0     |    0.002 |
| yasa       | SC       | SOL     | cqr_ffbs         |           78 |             56.109 |             32.719 |  0.387 | 0.003 |    0.063 |
| yasa       | SC       | SOL     | cqr_qr           |           78 |             56.109 |             50.256 | -0.224 | 0.085 |    1     |
| yasa       | SC       | SOL     | norm_entropy_reg |           78 |             56.109 |             82.246 | -0.727 | 0     |    0     |
| yasa       | SC       | SOL     | norm_ffbs        |           78 |             56.109 |             42.493 |  0.136 | 0.297 |    1     |
| yasa       | SC       | TST     | ba_loa           |           78 |            142.74  |            168.673 | -0.757 | 0     |    0     |
| yasa       | SC       | TST     | scp_abs          |           78 |            142.74  |            200.513 | -0.811 | 0     |    0     |
| yasa       | SC       | TST     | scp_abs_bc       |           78 |            142.74  |            168.505 | -0.711 | 0     |    0     |
| yasa       | SC       | TST     | scp_abs_cal      |           78 |            142.74  |            165.859 | -0.724 | 0     |    0     |
| yasa       | SC       | TST     | scp_abs_mu       |           78 |            142.74  |            158.067 | -0.711 | 0     |    0     |
| yasa       | SC       | TST     | norm_reg_plugc   |           78 |            142.74  |            148.782 | -0.674 | 0     |    0     |
| yasa       | SC       | TST     | cqr_ffbs         |           78 |            142.74  |            147.237 | -0.601 | 0     |    0     |
| yasa       | SC       | TST     | cqr_qr           |           78 |            142.74  |            150.532 | -0.517 | 0     |    0.002 |
| yasa       | SC       | TST     | norm_entropy_reg |           78 |            142.74  |            146.902 | -0.422 | 0.001 |    0.027 |
| yasa       | SC       | TST     | norm_ffbs        |           78 |            142.74  |            135.643 |  0.542 | 0     |    0.001 |
| yasa       | SC       | WASO    | ba_loa           |           78 |            324.384 |            214.399 |  0.751 | 0     |    0     |
| yasa       | SC       | WASO    | scp_abs          |           78 |            324.384 |            282.125 |  0.529 | 0     |    0.002 |
| yasa       | SC       | WASO    | scp_abs_bc       |           78 |            324.384 |            229.564 |  0.641 | 0     |    0     |
| yasa       | SC       | WASO    | scp_abs_cal      |           78 |            324.384 |            267.33  |  0.509 | 0     |    0.003 |
| yasa       | SC       | WASO    | scp_abs_mu       |           78 |            324.384 |            329.684 | -0.513 | 0     |    0.003 |
| yasa       | SC       | WASO    | norm_reg_plugc   |           78 |            324.384 |            260.785 |  0.592 | 0     |    0     |
| yasa       | SC       | WASO    | cqr_ffbs         |           78 |            324.384 |            277.864 |  0.786 | 0     |    0     |
| yasa       | SC       | WASO    | cqr_qr           |           78 |            324.384 |            127.554 |  0.879 | 0     |    0     |
| yasa       | SC       | WASO    | norm_entropy_reg |           78 |            324.384 |            335.318 | -0.498 | 0     |    0.004 |
| yasa       | SC       | WASO    | norm_ffbs        |           78 |            324.384 |            307.663 |  0.257 | 0.048 |    0.821 |
| yasa       | ST       | N1%     | ba_loa           |           22 |             24.272 |             20.173 |  0.107 | 0.679 |    1     |
| yasa       | ST       | N1%     | scp_abs          |           22 |             24.272 |             20.743 | -0.162 | 0.524 |    1     |
| yasa       | ST       | N1%     | scp_abs_bc       |           22 |             24.272 |             19.223 |  0.099 | 0.702 |    1     |
| yasa       | ST       | N1%     | scp_abs_cal      |           22 |             24.272 |             19.249 |  0.059 | 0.824 |    1     |
| yasa       | ST       | N1%     | scp_abs_mu       |           22 |             24.272 |             24.668 | -0.573 | 0.017 |    0.74  |
| yasa       | ST       | N1%     | norm_reg_plugc   |           22 |             24.272 |             20.005 |  0.549 | 0.023 |    0.917 |
| yasa       | ST       | N1%     | cqr_ffbs         |           22 |             24.272 |             24.536 | -0.51  | 0.036 |    1     |
| yasa       | ST       | N1%     | cqr_qr           |           22 |             24.272 |             22.356 | -0.407 | 0.098 |    1     |
| yasa       | ST       | N1%     | norm_entropy_reg |           22 |             24.272 |             23.129 | -0.099 | 0.702 |    1     |
| yasa       | ST       | N1%     | norm_ffbs        |           22 |             24.272 |             23.215 |  0.755 | 0.001 |    0.071 |
| yasa       | ST       | N2%     | ba_loa           |           22 |             37.558 |             42.05  | -0.296 | 0.235 |    1     |
| yasa       | ST       | N2%     | scp_abs          |           22 |             37.558 |             42.699 | -0.589 | 0.014 |    0.634 |
| yasa       | ST       | N2%     | scp_abs_bc       |           22 |             37.558 |             43.87  | -0.644 | 0.007 |    0.339 |
| yasa       | ST       | N2%     | scp_abs_cal      |           22 |             37.558 |             40.094 | -0.573 | 0.017 |    0.74  |
| yasa       | ST       | N2%     | scp_abs_mu       |           22 |             37.558 |             39.208 | -0.051 | 0.849 |    1     |
| yasa       | ST       | N2%     | norm_reg_plugc   |           22 |             37.558 |             43.318 | -0.684 | 0.004 |    0.217 |
| yasa       | ST       | N2%     | cqr_ffbs         |           22 |             37.558 |             38.296 |  0.186 | 0.463 |    1     |
| yasa       | ST       | N2%     | cqr_qr           |           22 |             37.558 |             63.28  | -0.897 | 0     |    0.003 |
| yasa       | ST       | N2%     | norm_entropy_reg |           22 |             37.558 |             36.608 |  0.273 | 0.276 |    1     |
| yasa       | ST       | N2%     | norm_ffbs        |           22 |             37.558 |             38.788 | -0.51  | 0.036 |    1     |
| yasa       | ST       | N3%     | ba_loa           |           22 |             27.815 |             33.2   | -0.059 | 0.824 |    1     |
| yasa       | ST       | N3%     | scp_abs          |           22 |             27.815 |             36.29  | -0.953 | 0     |    0.001 |
| yasa       | ST       | N3%     | scp_abs_bc       |           22 |             27.815 |             32.583 | -0.47  | 0.054 |    1     |
| yasa       | ST       | N3%     | scp_abs_cal      |           22 |             27.815 |             27.402 |  0.209 | 0.406 |    1     |
| yasa       | ST       | N3%     | scp_abs_mu       |           22 |             27.815 |             29.429 | -0.107 | 0.679 |    1     |
| yasa       | ST       | N3%     | norm_reg_plugc   |           22 |             27.815 |             29.992 | -0.502 | 0.039 |    1     |
| yasa       | ST       | N3%     | cqr_ffbs         |           22 |             27.815 |             29.343 | -0.739 | 0.001 |    0.093 |
| yasa       | ST       | N3%     | cqr_qr           |           22 |             27.815 |             38.96  | -0.652 | 0.006 |    0.308 |
| yasa       | ST       | N3%     | norm_entropy_reg |           22 |             27.815 |             29.027 | -0.597 | 0.013 |    0.585 |
| yasa       | ST       | N3%     | norm_ffbs        |           22 |             27.815 |             27.747 |  0.138 | 0.588 |    1     |
| yasa       | ST       | REM%    | ba_loa           |           22 |             28.043 |             27.696 |  0.502 | 0.039 |    1     |
| yasa       | ST       | REM%    | scp_abs          |           22 |             28.043 |             27.751 |  0.478 | 0.05  |    1     |
| yasa       | ST       | REM%    | scp_abs_bc       |           22 |             28.043 |             28.83  |  0.478 | 0.05  |    1     |
| yasa       | ST       | REM%    | scp_abs_cal      |           22 |             28.043 |             26.893 |  0.478 | 0.05  |    1     |
| yasa       | ST       | REM%    | scp_abs_mu       |           22 |             28.043 |             27.131 |  0.083 | 0.75  |    1     |
| yasa       | ST       | REM%    | norm_reg_plugc   |           22 |             28.043 |             30.103 | -0.423 | 0.085 |    1     |
| yasa       | ST       | REM%    | cqr_ffbs         |           22 |             28.043 |             27.497 |  0.273 | 0.276 |    1     |
| yasa       | ST       | REM%    | cqr_qr           |           22 |             28.043 |             34.283 | -0.455 | 0.063 |    1     |
| yasa       | ST       | REM%    | norm_entropy_reg |           22 |             28.043 |             28.145 | -0.067 | 0.799 |    1     |
| yasa       | ST       | REM%    | norm_ffbs        |           22 |             28.043 |             30.907 | -0.771 | 0.001 |    0.054 |
| yasa       | ST       | REML    | ba_loa           |           22 |            191.409 |            231.427 | -0.202 | 0.424 |    1     |
| yasa       | ST       | REML    | scp_abs          |           22 |            191.409 |            206.818 | -0.66  | 0.005 |    0.28  |
| yasa       | ST       | REML    | scp_abs_bc       |           22 |            191.409 |            202.025 | -0.589 | 0.014 |    0.634 |
| yasa       | ST       | REML    | scp_abs_cal      |           22 |            191.409 |            212.83  | -0.794 | 0.001 |    0.035 |
| yasa       | ST       | REML    | scp_abs_mu       |           22 |            191.409 |            201.984 | -0.621 | 0.009 |    0.445 |
| yasa       | ST       | REML    | norm_reg_plugc   |           22 |            191.409 |            202.321 | -0.7   | 0.003 |    0.177 |
| yasa       | ST       | REML    | cqr_ffbs         |           22 |            191.409 |            137.427 |  0.281 | 0.262 |    1     |
| yasa       | ST       | REML    | cqr_qr           |           22 |            191.409 |            169.723 | -0.352 | 0.156 |    1     |
| yasa       | ST       | REML    | norm_entropy_reg |           22 |            191.409 |            213.746 | -0.85  | 0     |    0.011 |
| yasa       | ST       | REML    | norm_ffbs        |           22 |            191.409 |            176.602 |  0.794 | 0.001 |    0.035 |
| yasa       | ST       | SOL     | ba_loa           |           22 |             39.042 |             17.955 |  0.692 | 0.003 |    0.194 |
| yasa       | ST       | SOL     | scp_abs          |           22 |             39.042 |             25.17  |  0.281 | 0.262 |    1     |
| yasa       | ST       | SOL     | scp_abs_bc       |           22 |             39.042 |             17.867 |  0.684 | 0.004 |    0.217 |
| yasa       | ST       | SOL     | scp_abs_cal      |           22 |             39.042 |             36.398 |  0.644 | 0.007 |    0.339 |
| yasa       | ST       | SOL     | scp_abs_mu       |           22 |             39.042 |             45.03  | -0.834 | 0     |    0.015 |
| yasa       | ST       | SOL     | norm_reg_plugc   |           22 |             39.042 |             33.589 |  0.676 | 0.004 |    0.237 |
| yasa       | ST       | SOL     | cqr_ffbs         |           22 |             39.042 |             28.461 |  0.913 | 0     |    0.002 |
| yasa       | ST       | SOL     | cqr_qr           |           22 |             39.042 |             16.79  |  0.557 | 0.021 |    0.855 |
| yasa       | ST       | SOL     | norm_entropy_reg |           22 |             39.042 |             43.455 | -0.518 | 0.033 |    1     |
| yasa       | ST       | SOL     | norm_ffbs        |           22 |             39.042 |             31.26  |  1     | 0     |    0     |
| yasa       | ST       | TST     | ba_loa           |           22 |             56.841 |             93.421 | -0.802 | 0     |    0.03  |
| yasa       | ST       | TST     | scp_abs          |           22 |             56.841 |            138.318 | -0.992 | 0     |    0     |
| yasa       | ST       | TST     | scp_abs_bc       |           22 |             56.841 |             92.955 | -0.842 | 0     |    0.013 |
| yasa       | ST       | TST     | scp_abs_cal      |           22 |             56.841 |             39.591 |  0.676 | 0.004 |    0.237 |
| yasa       | ST       | TST     | scp_abs_mu       |           22 |             56.841 |             58.497 | -0.249 | 0.321 |    1     |
| yasa       | ST       | TST     | norm_reg_plugc   |           22 |             56.841 |             37.406 |  0.85  | 0     |    0.011 |
| yasa       | ST       | TST     | cqr_ffbs         |           22 |             56.841 |             56.588 | -0.059 | 0.824 |    1     |
| yasa       | ST       | TST     | cqr_qr           |           22 |             56.841 |             58.214 | -0.202 | 0.424 |    1     |
| yasa       | ST       | TST     | norm_entropy_reg |           22 |             56.841 |             58.832 | -0.225 | 0.371 |    1     |
| yasa       | ST       | TST     | norm_ffbs        |           22 |             56.841 |             55.39  |  0.241 | 0.337 |    1     |
| yasa       | ST       | WASO    | ba_loa           |           22 |             82.357 |             69.138 |  0.644 | 0.007 |    0.339 |
| yasa       | ST       | WASO    | scp_abs          |           22 |             82.357 |             99.148 | -0.668 | 0.005 |    0.253 |
| yasa       | ST       | WASO    | scp_abs_bc       |           22 |             82.357 |             64.057 |  0.676 | 0.004 |    0.237 |
| yasa       | ST       | WASO    | scp_abs_cal      |           22 |             82.357 |             47.795 |  0.763 | 0.001 |    0.062 |
| yasa       | ST       | WASO    | scp_abs_mu       |           22 |             82.357 |             86.342 | -0.383 | 0.121 |    1     |
| yasa       | ST       | WASO    | norm_reg_plugc   |           22 |             82.357 |             48.614 |  0.7   | 0.003 |    0.177 |
| yasa       | ST       | WASO    | cqr_ffbs         |           22 |             82.357 |             85.065 | -0.826 | 0     |    0.018 |
| yasa       | ST       | WASO    | cqr_qr           |           22 |             82.357 |             78.475 |  0.431 | 0.079 |    1     |
| yasa       | ST       | WASO    | norm_entropy_reg |           22 |             82.357 |             88.586 | -0.613 | 0.01  |    0.485 |
| yasa       | ST       | WASO    | norm_ffbs        |           22 |             82.357 |             76.838 |  0.731 | 0.002 |    0.105 |
| lgbm_sc_s0 | HMC      | N1%     | ba_loa           |          151 |             38.797 |             42.57  | -0.675 | 0     |    0     |
| lgbm_sc_s0 | HMC      | N1%     | scp_abs          |          151 |             38.797 |             54.722 | -0.769 | 0     |    0     |
| lgbm_sc_s0 | HMC      | N1%     | scp_abs_bc       |          151 |             38.797 |             43.142 | -0.503 | 0     |    0     |
| lgbm_sc_s0 | HMC      | N1%     | scp_abs_cal      |          151 |             38.797 |             41.396 | -0.212 | 0.024 |    0.43  |
| lgbm_sc_s0 | HMC      | N1%     | scp_abs_mu       |          151 |             38.797 |             39.113 |  0.148 | 0.115 |    1     |
| lgbm_sc_s0 | HMC      | N1%     | norm_reg_plugc   |          151 |             38.797 |             41.999 | -0.043 | 0.644 |    1     |
| lgbm_sc_s0 | HMC      | N1%     | cqr_ffbs         |          151 |             38.797 |             40.06  | -0.058 | 0.537 |    1     |
| lgbm_sc_s0 | HMC      | N1%     | cqr_qr           |          151 |             38.797 |             37.534 | -0.225 | 0.016 |    0.31  |
| lgbm_sc_s0 | HMC      | N1%     | norm_entropy_reg |          151 |             38.797 |             38.328 |  0.187 | 0.046 |    0.65  |
| lgbm_sc_s0 | HMC      | N1%     | norm_ffbs        |          151 |             38.797 |             39.607 | -0.23  | 0.014 |    0.287 |
| lgbm_sc_s0 | HMC      | N2%     | ba_loa           |          151 |             46.488 |             52.509 | -0.72  | 0     |    0     |
| lgbm_sc_s0 | HMC      | N2%     | scp_abs          |          151 |             46.488 |             52.551 | -0.707 | 0     |    0     |
| lgbm_sc_s0 | HMC      | N2%     | scp_abs_bc       |          151 |             46.488 |             52.22  | -0.729 | 0     |    0     |
| lgbm_sc_s0 | HMC      | N2%     | scp_abs_cal      |          151 |             46.488 |             48.5   | -0.698 | 0     |    0     |
| lgbm_sc_s0 | HMC      | N2%     | scp_abs_mu       |          151 |             46.488 |             46.361 | -0.357 | 0     |    0.004 |
| lgbm_sc_s0 | HMC      | N2%     | norm_reg_plugc   |          151 |             46.488 |             48.052 | -0.728 | 0     |    0     |
| lgbm_sc_s0 | HMC      | N2%     | cqr_ffbs         |          151 |             46.488 |             46.512 | -0.661 | 0     |    0     |
| lgbm_sc_s0 | HMC      | N2%     | cqr_qr           |          151 |             46.488 |             35.523 |  0.643 | 0     |    0     |
| lgbm_sc_s0 | HMC      | N2%     | norm_entropy_reg |          151 |             46.488 |             45.151 | -0.545 | 0     |    0     |
| lgbm_sc_s0 | HMC      | N2%     | norm_ffbs        |          151 |             46.488 |             50.055 | -0.764 | 0     |    0     |
| lgbm_sc_s0 | HMC      | N3%     | ba_loa           |          151 |             56.827 |             46.527 |  0.419 | 0     |    0     |
| lgbm_sc_s0 | HMC      | N3%     | scp_abs          |          151 |             56.827 |             49.538 | -0.11  | 0.239 |    1     |
| lgbm_sc_s0 | HMC      | N3%     | scp_abs_bc       |          151 |             56.827 |             46.397 |  0.282 | 0.003 |    0.061 |
| lgbm_sc_s0 | HMC      | N3%     | scp_abs_cal      |          151 |             56.827 |             57.684 | -0.038 | 0.684 |    1     |
| lgbm_sc_s0 | HMC      | N3%     | scp_abs_mu       |          151 |             56.827 |             57.288 |  0.067 | 0.478 |    1     |
| lgbm_sc_s0 | HMC      | N3%     | norm_reg_plugc   |          151 |             56.827 |             54.498 | -0.019 | 0.837 |    1     |
| lgbm_sc_s0 | HMC      | N3%     | cqr_ffbs         |          151 |             56.827 |             57.401 | -0.394 | 0     |    0.001 |
| lgbm_sc_s0 | HMC      | N3%     | cqr_qr           |          151 |             56.827 |             39.831 |  0.599 | 0     |    0     |
| lgbm_sc_s0 | HMC      | N3%     | norm_entropy_reg |          151 |             56.827 |             58.298 | -0.158 | 0.092 |    1     |
| lgbm_sc_s0 | HMC      | N3%     | norm_ffbs        |          151 |             56.827 |             56.078 | -0.442 | 0     |    0     |
| lgbm_sc_s0 | HMC      | REM%    | ba_loa           |          151 |             26.408 |             25.143 |  0.625 | 0     |    0     |
| lgbm_sc_s0 | HMC      | REM%    | scp_abs          |          151 |             26.408 |             27.152 | -0.209 | 0.026 |    0.44  |
| lgbm_sc_s0 | HMC      | REM%    | scp_abs_bc       |          151 |             26.408 |             24.929 |  0.675 | 0     |    0     |
| lgbm_sc_s0 | HMC      | REM%    | scp_abs_cal      |          151 |             26.408 |             23.118 |  0.715 | 0     |    0     |
| lgbm_sc_s0 | HMC      | REM%    | scp_abs_mu       |          151 |             26.408 |             28.957 | -0.632 | 0     |    0     |
| lgbm_sc_s0 | HMC      | REM%    | norm_reg_plugc   |          151 |             26.408 |             22.686 |  0.709 | 0     |    0     |
| lgbm_sc_s0 | HMC      | REM%    | cqr_ffbs         |          151 |             26.408 |             26.641 |  0.249 | 0.008 |    0.173 |
| lgbm_sc_s0 | HMC      | REM%    | cqr_qr           |          151 |             26.408 |             21.593 |  0.764 | 0     |    0     |
| lgbm_sc_s0 | HMC      | REM%    | norm_entropy_reg |          151 |             26.408 |             27.12  | -0.318 | 0.001 |    0.017 |
| lgbm_sc_s0 | HMC      | REM%    | norm_ffbs        |          151 |             26.408 |             26.002 |  0.232 | 0.013 |    0.28  |
| lgbm_sc_s0 | HMC      | REML    | ba_loa           |          150 |            387.815 |            308.233 |  0.056 | 0.555 |    1     |
| lgbm_sc_s0 | HMC      | REML    | scp_abs          |          150 |            387.815 |            313.563 |  0.326 | 0.001 |    0.013 |
| lgbm_sc_s0 | HMC      | REML    | scp_abs_bc       |          150 |            387.815 |            307.299 |  0.176 | 0.062 |    0.803 |
| lgbm_sc_s0 | HMC      | REML    | scp_abs_cal      |          150 |            387.815 |            379.67  | -0.552 | 0     |    0     |
| lgbm_sc_s0 | HMC      | REML    | scp_abs_mu       |          150 |            387.815 |            401.828 | -0.639 | 0     |    0     |
| lgbm_sc_s0 | HMC      | REML    | norm_reg_plugc   |          150 |            387.815 |            380.52  | -0.428 | 0     |    0     |
| lgbm_sc_s0 | HMC      | REML    | cqr_ffbs         |          150 |            387.815 |            397.55  |  0.637 | 0     |    0     |
| lgbm_sc_s0 | HMC      | REML    | cqr_qr           |          150 |            387.815 |            273.066 |  0.21  | 0.026 |    0.44  |
| lgbm_sc_s0 | HMC      | REML    | norm_entropy_reg |          150 |            387.815 |            376.696 | -0.463 | 0     |    0     |
| lgbm_sc_s0 | HMC      | REML    | norm_ffbs        |          150 |            387.815 |            376.996 | -0.042 | 0.659 |    1     |
| lgbm_sc_s0 | HMC      | SOL     | ba_loa           |          151 |             72.716 |             59.095 | -0.615 | 0     |    0     |
| lgbm_sc_s0 | HMC      | SOL     | scp_abs          |          151 |             72.716 |             64.023 | -0.161 | 0.086 |    1     |
| lgbm_sc_s0 | HMC      | SOL     | scp_abs_bc       |          151 |             72.716 |             59.457 |  0.532 | 0     |    0     |
| lgbm_sc_s0 | HMC      | SOL     | scp_abs_cal      |          151 |             72.716 |             51.887 |  0.617 | 0     |    0     |
| lgbm_sc_s0 | HMC      | SOL     | scp_abs_mu       |          151 |             72.716 |             82.52  | -0.751 | 0     |    0     |
| lgbm_sc_s0 | HMC      | SOL     | norm_reg_plugc   |          151 |             72.716 |             50.3   |  0.686 | 0     |    0     |
| lgbm_sc_s0 | HMC      | SOL     | cqr_ffbs         |          151 |             72.716 |             68.888 |  0.825 | 0     |    0     |
| lgbm_sc_s0 | HMC      | SOL     | cqr_qr           |          151 |             72.716 |             49.493 |  0.446 | 0     |    0     |
| lgbm_sc_s0 | HMC      | SOL     | norm_entropy_reg |          151 |             72.716 |             84.754 | -0.803 | 0     |    0     |
| lgbm_sc_s0 | HMC      | SOL     | norm_ffbs        |          151 |             72.716 |             68.295 |  0.813 | 0     |    0     |
| lgbm_sc_s0 | HMC      | TST     | ba_loa           |          151 |            159.486 |            238.345 | -0.875 | 0     |    0     |
| lgbm_sc_s0 | HMC      | TST     | scp_abs          |          151 |            159.486 |            258.411 | -0.758 | 0     |    0     |
| lgbm_sc_s0 | HMC      | TST     | scp_abs_bc       |          151 |            159.486 |            238.634 | -0.87  | 0     |    0     |
| lgbm_sc_s0 | HMC      | TST     | scp_abs_cal      |          151 |            159.486 |            223.583 | -0.925 | 0     |    0     |
| lgbm_sc_s0 | HMC      | TST     | scp_abs_mu       |          151 |            159.486 |            193.243 | -0.951 | 0     |    0     |
| lgbm_sc_s0 | HMC      | TST     | norm_reg_plugc   |          151 |            159.486 |            175.758 | -0.824 | 0     |    0     |
| lgbm_sc_s0 | HMC      | TST     | cqr_ffbs         |          151 |            159.486 |            167.4   | -0.853 | 0     |    0     |
| lgbm_sc_s0 | HMC      | TST     | cqr_qr           |          151 |            159.486 |            147.912 | -0.134 | 0.154 |    1     |
| lgbm_sc_s0 | HMC      | TST     | norm_entropy_reg |          151 |            159.486 |            176.894 | -0.918 | 0     |    0     |
| lgbm_sc_s0 | HMC      | TST     | norm_ffbs        |          151 |            159.486 |            147.09  |  0.794 | 0     |    0     |
| lgbm_sc_s0 | HMC      | WASO    | ba_loa           |          151 |            142.258 |            177.183 | -0.68  | 0     |    0     |
| lgbm_sc_s0 | HMC      | WASO    | scp_abs          |          151 |            142.258 |            218.593 | -0.736 | 0     |    0     |
| lgbm_sc_s0 | HMC      | WASO    | scp_abs_bc       |          151 |            142.258 |            178.349 | -0.631 | 0     |    0     |
| lgbm_sc_s0 | HMC      | WASO    | scp_abs_cal      |          151 |            142.258 |            160.864 | -0.752 | 0     |    0     |
| lgbm_sc_s0 | HMC      | WASO    | scp_abs_mu       |          151 |            142.258 |            150.497 | -0.755 | 0     |    0     |
| lgbm_sc_s0 | HMC      | WASO    | norm_reg_plugc   |          151 |            142.258 |            148.888 | -0.711 | 0     |    0     |
| lgbm_sc_s0 | HMC      | WASO    | cqr_ffbs         |          151 |            142.258 |            140.927 |  0.199 | 0.034 |    0.504 |
| lgbm_sc_s0 | HMC      | WASO    | cqr_qr           |          151 |            142.258 |            129.732 |  0.441 | 0     |    0     |
| lgbm_sc_s0 | HMC      | WASO    | norm_entropy_reg |          151 |            142.258 |            144.397 | -0.537 | 0     |    0     |
| lgbm_sc_s0 | HMC      | WASO    | norm_ffbs        |          151 |            142.258 |            125.868 |  0.928 | 0     |    0     |
| lgbm_sc_s0 | SC       | N1%     | ba_loa           |           78 |             39.258 |             42.489 | -0.461 | 0     |    0.011 |
| lgbm_sc_s0 | SC       | N1%     | scp_abs          |           78 |             39.258 |             47.42  | -0.595 | 0     |    0     |
| lgbm_sc_s0 | SC       | N1%     | scp_abs_bc       |           78 |             39.258 |             42.747 | -0.542 | 0     |    0.001 |
| lgbm_sc_s0 | SC       | N1%     | scp_abs_cal      |           78 |             39.258 |             44.602 | -0.65  | 0     |    0     |
| lgbm_sc_s0 | SC       | N1%     | scp_abs_mu       |           78 |             39.258 |             41.679 | -0.421 | 0.001 |    0.027 |
| lgbm_sc_s0 | SC       | N1%     | norm_reg_plugc   |           78 |             39.258 |             41.002 | -0.324 | 0.013 |    0.209 |
| lgbm_sc_s0 | SC       | N1%     | cqr_ffbs         |           78 |             39.258 |             40.502 | -0.626 | 0     |    0     |
| lgbm_sc_s0 | SC       | N1%     | cqr_qr           |           78 |             39.258 |             33.351 |  0.045 | 0.729 |    1     |
| lgbm_sc_s0 | SC       | N1%     | norm_entropy_reg |           78 |             39.258 |             41.166 | -0.537 | 0     |    0.001 |
| lgbm_sc_s0 | SC       | N1%     | norm_ffbs        |           78 |             39.258 |             37.787 |  0.45  | 0.001 |    0.014 |
| lgbm_sc_s0 | SC       | N2%     | ba_loa           |           78 |             40.823 |             43.831 | -0.26  | 0.046 |    0.599 |
| lgbm_sc_s0 | SC       | N2%     | scp_abs          |           78 |             40.823 |             45.003 | -0.596 | 0     |    0     |
| lgbm_sc_s0 | SC       | N2%     | scp_abs_bc       |           78 |             40.823 |             43.586 | -0.049 | 0.707 |    1     |
| lgbm_sc_s0 | SC       | N2%     | scp_abs_cal      |           78 |             40.823 |             53.173 | -0.921 | 0     |    0     |
| lgbm_sc_s0 | SC       | N2%     | scp_abs_mu       |           78 |             40.823 |             41.812 | -0.15  | 0.251 |    1     |
| lgbm_sc_s0 | SC       | N2%     | norm_reg_plugc   |           78 |             40.823 |             50.858 | -0.952 | 0     |    0     |
| lgbm_sc_s0 | SC       | N2%     | cqr_ffbs         |           78 |             40.823 |             40.761 |  0.334 | 0.01  |    0.187 |
| lgbm_sc_s0 | SC       | N2%     | cqr_qr           |           78 |             40.823 |             41.495 | -0.16  | 0.22  |    1     |
| lgbm_sc_s0 | SC       | N2%     | norm_entropy_reg |           78 |             40.823 |             41.451 |  0.027 | 0.836 |    1     |
| lgbm_sc_s0 | SC       | N2%     | norm_ffbs        |           78 |             40.823 |             39.028 |  0.207 | 0.113 |    1     |
| lgbm_sc_s0 | SC       | N3%     | ba_loa           |           78 |             17.464 |             18.373 | -0.338 | 0.01  |    0.181 |
| lgbm_sc_s0 | SC       | N3%     | scp_abs          |           78 |             17.464 |             18.894 | -0.562 | 0     |    0.001 |
| lgbm_sc_s0 | SC       | N3%     | scp_abs_bc       |           78 |             17.464 |             18.238 | -0.535 | 0     |    0.001 |
| lgbm_sc_s0 | SC       | N3%     | scp_abs_cal      |           78 |             17.464 |             17.22  | -0.441 | 0.001 |    0.018 |
| lgbm_sc_s0 | SC       | N3%     | scp_abs_mu       |           78 |             17.464 |             17.914 | -0.459 | 0     |    0.012 |
| lgbm_sc_s0 | SC       | N3%     | norm_reg_plugc   |           78 |             17.464 |             16.116 |  0.102 | 0.433 |    1     |
| lgbm_sc_s0 | SC       | N3%     | cqr_ffbs         |           78 |             17.464 |             17.632 | -0.479 | 0     |    0.007 |
| lgbm_sc_s0 | SC       | N3%     | cqr_qr           |           78 |             17.464 |             20.885 | -0.616 | 0     |    0     |
| lgbm_sc_s0 | SC       | N3%     | norm_entropy_reg |           78 |             17.464 |             18.131 | -0.573 | 0     |    0     |
| lgbm_sc_s0 | SC       | N3%     | norm_ffbs        |           78 |             17.464 |             16.468 |  0.361 | 0.006 |    0.113 |
| lgbm_sc_s0 | SC       | REM%    | ba_loa           |           78 |             30.393 |             29.024 |  0.762 | 0     |    0     |
| lgbm_sc_s0 | SC       | REM%    | scp_abs          |           78 |             30.393 |             28.114 |  0.681 | 0     |    0     |
| lgbm_sc_s0 | SC       | REM%    | scp_abs_bc       |           78 |             30.393 |             28.219 |  0.685 | 0     |    0     |
| lgbm_sc_s0 | SC       | REM%    | scp_abs_cal      |           78 |             30.393 |             28.107 |  0.735 | 0     |    0     |
| lgbm_sc_s0 | SC       | REM%    | scp_abs_mu       |           78 |             30.393 |             32.858 | -0.287 | 0.028 |    0.39  |
| lgbm_sc_s0 | SC       | REM%    | norm_reg_plugc   |           78 |             30.393 |             26.881 |  0.804 | 0     |    0     |
| lgbm_sc_s0 | SC       | REM%    | cqr_ffbs         |           78 |             30.393 |             31.346 | -0.068 | 0.603 |    1     |
| lgbm_sc_s0 | SC       | REM%    | cqr_qr           |           78 |             30.393 |             28.884 |  0.466 | 0     |    0.01  |
| lgbm_sc_s0 | SC       | REM%    | norm_entropy_reg |           78 |             30.393 |             31.23  | -0.187 | 0.152 |    1     |
| lgbm_sc_s0 | SC       | REM%    | norm_ffbs        |           78 |             30.393 |             29.023 |  0.412 | 0.002 |    0.033 |
| lgbm_sc_s0 | SC       | REML    | ba_loa           |           78 |            141.837 |            194.824 | -0.674 | 0     |    0     |
| lgbm_sc_s0 | SC       | REML    | scp_abs          |           78 |            141.837 |            209.147 | -0.641 | 0     |    0     |
| lgbm_sc_s0 | SC       | REML    | scp_abs_bc       |           78 |            141.837 |            194.657 | -0.603 | 0     |    0     |
| lgbm_sc_s0 | SC       | REML    | scp_abs_cal      |           78 |            141.837 |            242.41  | -0.709 | 0     |    0     |
| lgbm_sc_s0 | SC       | REML    | scp_abs_mu       |           78 |            141.837 |            192.028 | -0.806 | 0     |    0     |
| lgbm_sc_s0 | SC       | REML    | norm_reg_plugc   |           78 |            141.837 |            190.13  | -0.764 | 0     |    0     |
| lgbm_sc_s0 | SC       | REML    | cqr_ffbs         |           78 |            141.837 |            133.947 | -0.329 | 0.012 |    0.198 |
| lgbm_sc_s0 | SC       | REML    | cqr_qr           |           78 |            141.837 |            154.758 | -0.557 | 0     |    0.001 |
| lgbm_sc_s0 | SC       | REML    | norm_entropy_reg |           78 |            141.837 |            183.74  | -0.783 | 0     |    0     |
| lgbm_sc_s0 | SC       | REML    | norm_ffbs        |           78 |            141.837 |            129.072 |  0.543 | 0     |    0.001 |
| lgbm_sc_s0 | SC       | SOL     | ba_loa           |           78 |             54.231 |             62.509 | -0.761 | 0     |    0     |
| lgbm_sc_s0 | SC       | SOL     | scp_abs          |           78 |             54.231 |             61.564 | -0.438 | 0.001 |    0.018 |
| lgbm_sc_s0 | SC       | SOL     | scp_abs_bc       |           78 |             54.231 |             59.793 | -0.685 | 0     |    0     |
| lgbm_sc_s0 | SC       | SOL     | scp_abs_cal      |           78 |             54.231 |             57.625 | -0.561 | 0     |    0.001 |
| lgbm_sc_s0 | SC       | SOL     | scp_abs_mu       |           78 |             54.231 |             80.702 | -0.908 | 0     |    0     |
| lgbm_sc_s0 | SC       | SOL     | norm_reg_plugc   |           78 |             54.231 |             48.648 | -0.435 | 0.001 |    0.02  |
| lgbm_sc_s0 | SC       | SOL     | cqr_ffbs         |           78 |             54.231 |             33.498 |  0.172 | 0.186 |    1     |
| lgbm_sc_s0 | SC       | SOL     | cqr_qr           |           78 |             54.231 |             56.173 | -0.631 | 0     |    0     |
| lgbm_sc_s0 | SC       | SOL     | norm_entropy_reg |           78 |             54.231 |             78.139 | -0.813 | 0     |    0     |
| lgbm_sc_s0 | SC       | SOL     | norm_ffbs        |           78 |             54.231 |             42.442 |  0.046 | 0.725 |    1     |
| lgbm_sc_s0 | SC       | TST     | ba_loa           |           78 |            110.442 |            135.258 | -0.677 | 0     |    0     |
| lgbm_sc_s0 | SC       | TST     | scp_abs          |           78 |            110.442 |            143.821 | -0.683 | 0     |    0     |
| lgbm_sc_s0 | SC       | TST     | scp_abs_bc       |           78 |            110.442 |            136.152 | -0.722 | 0     |    0     |
| lgbm_sc_s0 | SC       | TST     | scp_abs_cal      |           78 |            110.442 |            139.09  | -0.774 | 0     |    0     |
| lgbm_sc_s0 | SC       | TST     | scp_abs_mu       |           78 |            110.442 |            124.459 | -0.679 | 0     |    0     |
| lgbm_sc_s0 | SC       | TST     | norm_reg_plugc   |           78 |            110.442 |            131.385 | -0.778 | 0     |    0     |
| lgbm_sc_s0 | SC       | TST     | cqr_ffbs         |           78 |            110.442 |            114.201 | -0.683 | 0     |    0     |
| lgbm_sc_s0 | SC       | TST     | cqr_qr           |           78 |            110.442 |            120.403 | -0.6   | 0     |    0     |
| lgbm_sc_s0 | SC       | TST     | norm_entropy_reg |           78 |            110.442 |            113.981 | -0.574 | 0     |    0     |
| lgbm_sc_s0 | SC       | TST     | norm_ffbs        |           78 |            110.442 |            112.83  | -0.152 | 0.245 |    1     |
| lgbm_sc_s0 | SC       | WASO    | ba_loa           |           78 |            259.607 |            181.123 |  0.712 | 0     |    0     |
| lgbm_sc_s0 | SC       | WASO    | scp_abs          |           78 |            259.607 |            194.827 |  0.618 | 0     |    0     |
| lgbm_sc_s0 | SC       | WASO    | scp_abs_bc       |           78 |            259.607 |            181.355 |  0.637 | 0     |    0     |
| lgbm_sc_s0 | SC       | WASO    | scp_abs_cal      |           78 |            259.607 |            198.151 |  0.622 | 0     |    0     |
| lgbm_sc_s0 | SC       | WASO    | scp_abs_mu       |           78 |            259.607 |            294.106 | -0.719 | 0     |    0     |
| lgbm_sc_s0 | SC       | WASO    | norm_reg_plugc   |           78 |            259.607 |            199.494 |  0.631 | 0     |    0     |
| lgbm_sc_s0 | SC       | WASO    | cqr_ffbs         |           78 |            259.607 |            219.157 |  0.737 | 0     |    0     |
| lgbm_sc_s0 | SC       | WASO    | cqr_qr           |           78 |            259.607 |            121.108 |  0.884 | 0     |    0     |
| lgbm_sc_s0 | SC       | WASO    | norm_entropy_reg |           78 |            259.607 |            314.425 | -0.858 | 0     |    0     |
| lgbm_sc_s0 | SC       | WASO    | norm_ffbs        |           78 |            259.607 |            252.739 |  0.301 | 0.021 |    0.315 |


# S4. Centre × scale factorial and ablations (median ratio of interval score to the proposed method over cohorts; >1 = worse than proposed)

| stager     | param   |   cqr_ffbs |   norm_entropy_reg |   norm_ffbs |   norm_reg_ffbs1 |   norm_reg_ind |   norm_reg_plug |   norm_reg_plugc |   scp_abs |   scp_abs_bc |   scp_abs_cal |   scp_abs_mu |
|:-----------|:--------|-----------:|-------------------:|------------:|-----------------:|---------------:|----------------:|-----------------:|----------:|-------------:|--------------:|-------------:|
| lgbm_sc_s0 | N1%     |       1.01 |               0.99 |        0.97 |             1.05 |           0.9  |            1.09 |             1.05 |      1.17 |         1.08 |          1.05 |         1.03 |
| lgbm_sc_s0 | N2%     |       1    |               0.99 |        1.03 |             1.21 |           0.97 |            1.05 |             1.17 |      1.09 |         1.1  |          1.15 |         1.01 |
| lgbm_sc_s0 | N3%     |       1.02 |               1.04 |        0.96 |             1.15 |           0.98 |            1    |             0.97 |      1.07 |         1.07 |          1.01 |         1.06 |
| lgbm_sc_s0 | REM%    |       1.01 |               1.02 |        0.98 |             0.92 |           0.9  |            0.98 |             0.89 |      1.02 |         0.95 |          0.95 |         1.08 |
| lgbm_sc_s0 | REML    |       0.94 |               1.2  |        0.91 |             1.04 |           1.78 |            1.21 |             1.3  |      1.45 |         1.37 |          1.58 |         1.15 |
| lgbm_sc_s0 | SOL     |       0.8  |               1.17 |        0.94 |             0.73 |           1.3  |            0.95 |             0.88 |      1.03 |         1    |          1.04 |         1.21 |
| lgbm_sc_s0 | TST     |       1.01 |               1.02 |        0.9  |             1.05 |           1.03 |            1.29 |             1.1  |      1.41 |         1.36 |          1.24 |         1.11 |
| lgbm_sc_s0 | WASO    |       0.95 |               1.06 |        0.93 |             0.83 |           1.19 |            1    |             0.98 |      1    |         0.81 |          1.02 |         1.11 |
| yasa       | N1%     |       1.02 |               1.01 |        0.96 |             1.01 |           0.93 |            1.1  |             1.1  |      1.15 |         1.09 |          1.12 |         1.04 |
| yasa       | N2%     |       1    |               0.99 |        1    |             1.24 |           1.03 |            1.35 |             1.37 |      1.42 |         1.32 |          1.44 |         1.02 |
| yasa       | N3%     |       1.02 |               1.02 |        1.01 |             1.24 |           0.96 |            1.25 |             1.01 |      1.34 |         1.13 |          0.99 |         1.07 |
| yasa       | REM%    |       1.01 |               1.03 |        1.03 |             0.98 |           0.84 |            0.9  |             0.86 |      0.97 |         0.97 |          0.92 |         1.06 |
| yasa       | REML    |       0.89 |               1.09 |        0.95 |             1.09 |           1.35 |            1.04 |             1.03 |      1.08 |         1.07 |          1.18 |         1.14 |
| yasa       | SOL     |       0.77 |               1.22 |        0.85 |             0.48 |           1.4  |            0.75 |             0.93 |      0.87 |         0.75 |          0.99 |         1.24 |
| yasa       | TST     |       1.03 |               1.04 |        0.94 |             1    |           1.13 |            1.58 |             1    |      1.81 |         1.41 |          1.16 |         1.11 |
| yasa       | WASO    |       0.96 |               1.09 |        0.93 |             0.63 |           1.06 |            1.15 |             0.82 |      1.27 |         0.84 |          0.85 |         1.08 |


**Paired factorial tests: FFBS-SD scale versus constant width with the centre held fixed (LOSO; Wilcoxon; Holm within cohort and stager)**


| stager     | cohort   | param   | centre             |   n_subjects |   mean_is_scaled |   mean_is_constant |   ratio |   r_rb |     p |   p_holm |
|:-----------|:---------|:--------|:-------------------|-------------:|-----------------:|-------------------:|--------:|-------:|------:|---------:|
| yasa       | HMC      | N1%     | raw plug-in        |          151 |           38.562 |             41.659 |   0.926 |  0.014 | 0.882 |    0.924 |
| yasa       | HMC      | N1%     | calibrated plug-in |          151 |           39.156 |             40.93  |   0.957 |  0.145 | 0.123 |    0.403 |
| yasa       | HMC      | N1%     | FFBS mean          |          151 |           34.469 |             36.389 |   0.947 | -0.263 | 0.005 |    0.04  |
| yasa       | HMC      | N2%     | raw plug-in        |          151 |           59.116 |             65.293 |   0.905 | -0.766 | 0     |    0     |
| yasa       | HMC      | N2%     | calibrated plug-in |          151 |           51.348 |             52.749 |   0.973 | -0.365 | 0     |    0.001 |
| yasa       | HMC      | N2%     | FFBS mean          |          151 |           34.491 |             35.114 |   0.982 | -0.182 | 0.052 |    0.261 |
| yasa       | HMC      | N3%     | raw plug-in        |          151 |           39.54  |             39.527 |   1     |  0.43  | 0     |    0     |
| yasa       | HMC      | N3%     | calibrated plug-in |          151 |           34.765 |             34.39  |   1.011 |  0.069 | 0.462 |    0.924 |
| yasa       | HMC      | N3%     | FFBS mean          |          151 |           35.559 |             37.266 |   0.954 | -0.208 | 0.027 |    0.188 |
| yasa       | HMC      | REM%    | raw plug-in        |          151 |           23.252 |             25.379 |   0.916 | -0.714 | 0     |    0     |
| yasa       | HMC      | REM%    | calibrated plug-in |          151 |           22.255 |             23.33  |   0.954 | -0.413 | 0     |    0     |
| yasa       | HMC      | REM%    | FFBS mean          |          151 |           26.661 |             27.448 |   0.971 |  0.207 | 0.028 |    0.188 |
| yasa       | HMC      | REML    | raw plug-in        |          150 |          294.444 |            310.983 |   0.947 | -0.154 | 0.101 |    0.403 |
| yasa       | HMC      | REML    | calibrated plug-in |          150 |          315.455 |            360.653 |   0.875 | -0.294 | 0.002 |    0.016 |
| yasa       | HMC      | REML    | FFBS mean          |          150 |          309.681 |            374.685 |   0.827 | -0.74  | 0     |    0     |
| yasa       | HMC      | SOL     | raw plug-in        |          151 |           49.188 |             59.629 |   0.825 | -0.714 | 0     |    0     |
| yasa       | HMC      | SOL     | calibrated plug-in |          151 |           49.552 |             54.142 |   0.915 | -0.662 | 0     |    0     |
| yasa       | HMC      | SOL     | FFBS mean          |          151 |           71.259 |             76.77  |   0.928 | -0.785 | 0     |    0     |
| yasa       | HMC      | TST     | raw plug-in        |          151 |          230.268 |            253.318 |   0.909 | -0.519 | 0     |    0     |
| yasa       | HMC      | TST     | calibrated plug-in |          151 |          141.218 |            162.371 |   0.87  | -0.578 | 0     |    0     |
| yasa       | HMC      | TST     | FFBS mean          |          151 |          144.878 |            161.002 |   0.9   | -0.724 | 0     |    0     |
| yasa       | HMC      | WASO    | raw plug-in        |          151 |          214.292 |            228.844 |   0.936 | -0.508 | 0     |    0     |
| yasa       | HMC      | WASO    | calibrated plug-in |          151 |          133.018 |            156.957 |   0.847 | -0.847 | 0     |    0     |
| yasa       | HMC      | WASO    | FFBS mean          |          151 |          146.908 |            155.581 |   0.944 | -0.458 | 0     |    0     |
| yasa       | SC       | N1%     | raw plug-in        |           78 |           43.062 |             45.618 |   0.944 | -0.502 | 0     |    0.001 |
| yasa       | SC       | N1%     | calibrated plug-in |           78 |           43.909 |             44.039 |   0.997 | -0.216 | 0.097 |    0.32  |
| yasa       | SC       | N1%     | FFBS mean          |           78 |           39.561 |             42.019 |   0.942 | -0.464 | 0     |    0.002 |
| yasa       | SC       | N2%     | raw plug-in        |           78 |           55.8   |             59.471 |   0.938 | -0.69  | 0     |    0     |
| yasa       | SC       | N2%     | calibrated plug-in |           78 |           58.804 |             62.428 |   0.942 | -0.718 | 0     |    0     |
| yasa       | SC       | N2%     | FFBS mean          |           78 |           42.529 |             44.058 |   0.965 | -0.083 | 0.525 |    0.525 |
| yasa       | SC       | N3%     | raw plug-in        |           78 |           32.666 |             34.856 |   0.937 | -0.565 | 0     |    0     |
| yasa       | SC       | N3%     | calibrated plug-in |           78 |           23.878 |             27.623 |   0.864 | -0.896 | 0     |    0     |
| yasa       | SC       | N3%     | FFBS mean          |           78 |           22.395 |             25.869 |   0.866 | -0.886 | 0     |    0     |
| yasa       | SC       | REM%    | raw plug-in        |           78 |           29.609 |             31.719 |   0.933 | -0.566 | 0     |    0     |
| yasa       | SC       | REM%    | calibrated plug-in |           78 |           28.237 |             30.06  |   0.939 | -0.387 | 0.003 |    0.015 |
| yasa       | SC       | REM%    | FFBS mean          |           78 |           32.7   |             35.626 |   0.918 | -0.537 | 0     |    0     |
| yasa       | SC       | REML    | raw plug-in        |           78 |          197.746 |            222.119 |   0.89  | -0.631 | 0     |    0     |
| yasa       | SC       | REML    | calibrated plug-in |           78 |          188.851 |            219.167 |   0.862 | -0.685 | 0     |    0     |
| yasa       | SC       | REML    | FFBS mean          |           78 |          152.473 |            183.357 |   0.832 | -0.657 | 0     |    0     |
| yasa       | SC       | SOL     | raw plug-in        |           78 |           51.666 |             69.513 |   0.743 | -0.531 | 0     |    0     |
| yasa       | SC       | SOL     | calibrated plug-in |           78 |           52.635 |             73.054 |   0.72  | -0.65  | 0     |    0     |
| yasa       | SC       | SOL     | FFBS mean          |           78 |           56.109 |             81.022 |   0.693 | -0.677 | 0     |    0     |
| yasa       | SC       | TST     | raw plug-in        |           78 |          168.624 |            200.513 |   0.841 | -0.847 | 0     |    0     |
| yasa       | SC       | TST     | calibrated plug-in |           78 |          148.782 |            165.859 |   0.897 | -0.675 | 0     |    0     |
| yasa       | SC       | TST     | FFBS mean          |           78 |          142.74  |            158.067 |   0.903 | -0.711 | 0     |    0     |
| yasa       | SC       | WASO    | raw plug-in        |           78 |          277.132 |            282.125 |   0.982 | -0.178 | 0.172 |    0.343 |
| yasa       | SC       | WASO    | calibrated plug-in |           78 |          260.785 |            267.33  |   0.976 |  0.228 | 0.08  |    0.32  |
| yasa       | SC       | WASO    | FFBS mean          |           78 |          324.384 |            329.684 |   0.984 | -0.513 | 0     |    0.001 |
| yasa       | ST       | N1%     | raw plug-in        |           22 |           19.915 |             20.743 |   0.96  | -0.478 | 0.05  |    0.651 |
| yasa       | ST       | N1%     | calibrated plug-in |           22 |           20.005 |             19.249 |   1.039 | -0.099 | 0.702 |    1     |
| yasa       | ST       | N1%     | FFBS mean          |           22 |           24.272 |             24.668 |   0.984 | -0.573 | 0.017 |    0.292 |
| yasa       | ST       | N2%     | raw plug-in        |           22 |           42.937 |             42.699 |   1.006 |  0.462 | 0.059 |    0.704 |
| yasa       | ST       | N2%     | calibrated plug-in |           22 |           43.318 |             40.094 |   1.08  |  0.7   | 0.003 |    0.057 |
| yasa       | ST       | N2%     | FFBS mean          |           22 |           37.558 |             39.208 |   0.958 | -0.051 | 0.849 |    1     |
| yasa       | ST       | N3%     | raw plug-in        |           22 |           37.849 |             36.29  |   1.043 |  0.518 | 0.033 |    0.461 |
| yasa       | ST       | N3%     | calibrated plug-in |           22 |           29.992 |             27.402 |   1.095 |  0.7   | 0.003 |    0.057 |
| yasa       | ST       | N3%     | FFBS mean          |           22 |           27.815 |             29.429 |   0.945 | -0.107 | 0.679 |    1     |
| yasa       | ST       | REM%    | raw plug-in        |           22 |           31.419 |             27.751 |   1.132 |  0.984 | 0     |    0     |
| yasa       | ST       | REM%    | calibrated plug-in |           22 |           30.103 |             26.893 |   1.119 |  0.945 | 0     |    0     |
| yasa       | ST       | REM%    | FFBS mean          |           22 |           28.043 |             27.131 |   1.034 |  0.083 | 0.75  |    1     |
| yasa       | ST       | REML    | raw plug-in        |           22 |          196.807 |            206.818 |   0.952 | -0.447 | 0.068 |    0.704 |
| yasa       | ST       | REML    | calibrated plug-in |           22 |          202.321 |            212.83  |   0.951 | -0.462 | 0.059 |    0.704 |
| yasa       | ST       | REML    | FFBS mean          |           22 |          191.409 |            201.984 |   0.948 | -0.621 | 0.009 |    0.167 |
| yasa       | ST       | SOL     | raw plug-in        |           22 |           21.232 |             25.17  |   0.844 | -0.115 | 0.656 |    1     |
| yasa       | ST       | SOL     | calibrated plug-in |           22 |           33.589 |             36.398 |   0.923 | -0.573 | 0.017 |    0.292 |
| yasa       | ST       | SOL     | FFBS mean          |           22 |           39.042 |             45.03  |   0.867 | -0.834 | 0     |    0.004 |
| yasa       | ST       | TST     | raw plug-in        |           22 |          117.257 |            138.318 |   0.848 | -0.866 | 0     |    0.002 |
| yasa       | ST       | TST     | calibrated plug-in |           22 |           37.406 |             39.591 |   0.945 | -0.557 | 0.021 |    0.313 |
| yasa       | ST       | TST     | FFBS mean          |           22 |           56.841 |             58.497 |   0.972 | -0.249 | 0.321 |    1     |
| yasa       | ST       | WASO    | raw plug-in        |           22 |           95.135 |             99.148 |   0.96  |  0.249 | 0.321 |    1     |
| yasa       | ST       | WASO    | calibrated plug-in |           22 |           48.614 |             47.795 |   1.017 |  0.012 | 0.975 |    1     |
| yasa       | ST       | WASO    | FFBS mean          |           22 |           82.357 |             86.342 |   0.954 | -0.383 | 0.121 |    1     |
| lgbm_sc_s0 | HMC      | N1%     | raw plug-in        |          151 |           50.046 |             54.722 |   0.915 | -0.636 | 0     |    0     |
| lgbm_sc_s0 | HMC      | N1%     | calibrated plug-in |          151 |           41.999 |             41.396 |   1.015 | -0.271 | 0.004 |    0.023 |
| lgbm_sc_s0 | HMC      | N1%     | FFBS mean          |          151 |           38.797 |             39.113 |   0.992 |  0.148 | 0.115 |    0.442 |
| lgbm_sc_s0 | HMC      | N2%     | raw plug-in        |          151 |           54.859 |             52.551 |   1.044 |  0.29  | 0.002 |    0.014 |
| lgbm_sc_s0 | HMC      | N2%     | calibrated plug-in |          151 |           48.052 |             48.5   |   0.991 | -0.44  | 0     |    0     |
| lgbm_sc_s0 | HMC      | N2%     | FFBS mean          |          151 |           46.488 |             46.361 |   1.003 | -0.357 | 0     |    0.001 |
| lgbm_sc_s0 | HMC      | N3%     | raw plug-in        |          151 |           46.992 |             49.538 |   0.949 |  0.201 | 0.032 |    0.161 |
| lgbm_sc_s0 | HMC      | N3%     | calibrated plug-in |          151 |           54.498 |             57.684 |   0.945 | -0.15  | 0.111 |    0.442 |
| lgbm_sc_s0 | HMC      | N3%     | FFBS mean          |          151 |           56.827 |             57.288 |   0.992 |  0.067 | 0.478 |    0.541 |
| lgbm_sc_s0 | HMC      | REM%    | raw plug-in        |          151 |           26.322 |             27.152 |   0.969 | -0.313 | 0.001 |    0.007 |
| lgbm_sc_s0 | HMC      | REM%    | calibrated plug-in |          151 |           22.686 |             23.118 |   0.981 | -0.433 | 0     |    0     |
| lgbm_sc_s0 | HMC      | REM%    | FFBS mean          |          151 |           26.408 |             28.957 |   0.912 | -0.632 | 0     |    0     |
| lgbm_sc_s0 | HMC      | REML    | raw plug-in        |          150 |          297.589 |            313.563 |   0.949 | -0.104 | 0.27  |    0.541 |
| lgbm_sc_s0 | HMC      | REML    | calibrated plug-in |          150 |          380.52  |            379.67  |   1.002 | -0.355 | 0     |    0.001 |
| lgbm_sc_s0 | HMC      | REML    | FFBS mean          |          150 |          387.815 |            401.828 |   0.965 | -0.639 | 0     |    0     |
| lgbm_sc_s0 | HMC      | SOL     | raw plug-in        |          151 |           58.995 |             64.023 |   0.921 | -0.773 | 0     |    0     |
| lgbm_sc_s0 | HMC      | SOL     | calibrated plug-in |          151 |           50.3   |             51.887 |   0.969 | -0.686 | 0     |    0     |
| lgbm_sc_s0 | HMC      | SOL     | FFBS mean          |          151 |           72.716 |             82.52  |   0.881 | -0.751 | 0     |    0     |
| lgbm_sc_s0 | HMC      | TST     | raw plug-in        |          151 |          244.466 |            258.411 |   0.946 | -0.452 | 0     |    0     |
| lgbm_sc_s0 | HMC      | TST     | calibrated plug-in |          151 |          175.758 |            223.583 |   0.786 | -0.977 | 0     |    0     |
| lgbm_sc_s0 | HMC      | TST     | FFBS mean          |          151 |          159.486 |            193.243 |   0.825 | -0.951 | 0     |    0     |
| lgbm_sc_s0 | HMC      | WASO    | raw plug-in        |          151 |          209.563 |            218.593 |   0.959 | -0.499 | 0     |    0     |
| lgbm_sc_s0 | HMC      | WASO    | calibrated plug-in |          151 |          148.888 |            160.864 |   0.926 | -0.795 | 0     |    0     |
| lgbm_sc_s0 | HMC      | WASO    | FFBS mean          |          151 |          142.258 |            150.497 |   0.945 | -0.755 | 0     |    0     |
| lgbm_sc_s0 | SC       | N1%     | raw plug-in        |           78 |           42.502 |             47.42  |   0.896 | -0.867 | 0     |    0     |
| lgbm_sc_s0 | SC       | N1%     | calibrated plug-in |           78 |           41.002 |             44.602 |   0.919 | -0.804 | 0     |    0     |
| lgbm_sc_s0 | SC       | N1%     | FFBS mean          |           78 |           39.258 |             41.679 |   0.942 | -0.421 | 0.001 |    0.012 |
| lgbm_sc_s0 | SC       | N2%     | raw plug-in        |           78 |           42.032 |             45.003 |   0.934 | -0.538 | 0     |    0     |
| lgbm_sc_s0 | SC       | N2%     | calibrated plug-in |           78 |           50.858 |             53.173 |   0.956 | -0.635 | 0     |    0     |
| lgbm_sc_s0 | SC       | N2%     | FFBS mean          |           78 |           40.823 |             41.812 |   0.976 | -0.15  | 0.251 |    0.871 |
| lgbm_sc_s0 | SC       | N3%     | raw plug-in        |           78 |           17.2   |             18.894 |   0.91  | -0.733 | 0     |    0     |
| lgbm_sc_s0 | SC       | N3%     | calibrated plug-in |           78 |           16.116 |             17.22  |   0.936 | -0.606 | 0     |    0     |
| lgbm_sc_s0 | SC       | N3%     | FFBS mean          |           78 |           17.464 |             17.914 |   0.975 | -0.459 | 0     |    0.005 |
| lgbm_sc_s0 | SC       | REM%    | raw plug-in        |           78 |           27.59  |             28.114 |   0.981 |  0.294 | 0.024 |    0.167 |
| lgbm_sc_s0 | SC       | REM%    | calibrated plug-in |           78 |           26.881 |             28.107 |   0.956 |  0.119 | 0.361 |    0.871 |
| lgbm_sc_s0 | SC       | REM%    | FFBS mean          |           78 |           30.393 |             32.858 |   0.925 | -0.287 | 0.028 |    0.167 |
| lgbm_sc_s0 | SC       | REML    | raw plug-in        |           78 |          173.912 |            209.147 |   0.832 | -0.659 | 0     |    0     |
| lgbm_sc_s0 | SC       | REML    | calibrated plug-in |           78 |          190.13  |            242.41  |   0.784 | -0.54  | 0     |    0     |
| lgbm_sc_s0 | SC       | REML    | FFBS mean          |           78 |          141.837 |            192.028 |   0.739 | -0.806 | 0     |    0     |
| lgbm_sc_s0 | SC       | SOL     | raw plug-in        |           78 |           52.916 |             61.564 |   0.86  | -0.357 | 0.006 |    0.055 |
| lgbm_sc_s0 | SC       | SOL     | calibrated plug-in |           78 |           48.648 |             57.625 |   0.844 | -0.355 | 0.006 |    0.055 |
| lgbm_sc_s0 | SC       | SOL     | FFBS mean          |           78 |           54.231 |             80.702 |   0.672 | -0.908 | 0     |    0     |
| lgbm_sc_s0 | SC       | TST     | raw plug-in        |           78 |          136.791 |            143.821 |   0.951 | -0.161 | 0.218 |    0.871 |
| lgbm_sc_s0 | SC       | TST     | calibrated plug-in |           78 |          131.385 |            139.09  |   0.945 | -0.503 | 0     |    0.001 |
| lgbm_sc_s0 | SC       | TST     | FFBS mean          |           78 |          110.442 |            124.459 |   0.887 | -0.679 | 0     |    0     |
| lgbm_sc_s0 | SC       | WASO    | raw plug-in        |           78 |          187.876 |            194.827 |   0.964 |  0.043 | 0.74  |    0.871 |
| lgbm_sc_s0 | SC       | WASO    | calibrated plug-in |           78 |          199.494 |            198.151 |   1.007 |  0.185 | 0.156 |    0.782 |
| lgbm_sc_s0 | SC       | WASO    | FFBS mean          |           78 |          259.607 |            294.106 |   0.883 | -0.719 | 0     |    0     |
| lgbm_sc_s0 | ST       | N1%     | raw plug-in        |           22 |           29.13  |             27.394 |   1.063 |  0.051 | 0.849 |    1     |
| lgbm_sc_s0 | ST       | N1%     | calibrated plug-in |           22 |           23.833 |             23.996 |   0.993 |  0.059 | 0.824 |    1     |
| lgbm_sc_s0 | ST       | N1%     | FFBS mean          |           22 |           23.346 |             24.096 |   0.969 | -0.581 | 0.016 |    0.234 |
| lgbm_sc_s0 | ST       | N2%     | raw plug-in        |           22 |           37.694 |             41.083 |   0.918 | -0.407 | 0.098 |    1     |
| lgbm_sc_s0 | ST       | N2%     | calibrated plug-in |           22 |           45.27  |             41.792 |   1.083 |  0.692 | 0.003 |    0.055 |
| lgbm_sc_s0 | ST       | N2%     | FFBS mean          |           22 |           35.218 |             34.921 |   1.009 |  0.423 | 0.085 |    1     |
| lgbm_sc_s0 | ST       | N3%     | raw plug-in        |           22 |           34.986 |             37.711 |   0.928 | -0.265 | 0.29  |    1     |
| lgbm_sc_s0 | ST       | N3%     | calibrated plug-in |           22 |           32.972 |             34.742 |   0.949 | -0.542 | 0.025 |    0.352 |
| lgbm_sc_s0 | ST       | N3%     | FFBS mean          |           22 |           35.267 |             35.667 |   0.989 |  0.028 | 0.924 |    1     |
| lgbm_sc_s0 | ST       | REM%    | raw plug-in        |           22 |           36.725 |             33.558 |   1.094 |  0.889 | 0     |    0.001 |
| lgbm_sc_s0 | ST       | REM%    | calibrated plug-in |           22 |           30.372 |             28.13  |   1.08  |  0.794 | 0.001 |    0.011 |
| lgbm_sc_s0 | ST       | REM%    | FFBS mean          |           22 |           26.479 |             25.931 |   1.021 | -0.146 | 0.566 |    1     |
| lgbm_sc_s0 | ST       | REML    | raw plug-in        |           22 |          193.457 |            225.193 |   0.859 | -0.708 | 0.003 |    0.045 |
| lgbm_sc_s0 | ST       | REML    | calibrated plug-in |           22 |          228.473 |            228.58  |   1     | -0.107 | 0.679 |    1     |
| lgbm_sc_s0 | ST       | REML    | FFBS mean          |           22 |          157.974 |            166.41  |   0.949 | -0.375 | 0.129 |    1     |
| lgbm_sc_s0 | ST       | SOL     | raw plug-in        |           22 |           39.269 |             36.989 |   1.062 |  0.455 | 0.063 |    0.824 |
| lgbm_sc_s0 | ST       | SOL     | calibrated plug-in |           22 |           39.242 |             35.523 |   1.105 |  0.787 | 0.001 |    0.011 |
| lgbm_sc_s0 | ST       | SOL     | FFBS mean          |           22 |           41.876 |             48.963 |   0.855 | -0.794 | 0.001 |    0.011 |
| lgbm_sc_s0 | ST       | TST     | raw plug-in        |           22 |           89.45  |             90.273 |   0.991 |  0.304 | 0.222 |    1     |
| lgbm_sc_s0 | ST       | TST     | calibrated plug-in |           22 |           62.063 |             70.182 |   0.884 | -0.652 | 0.006 |    0.095 |
| lgbm_sc_s0 | ST       | TST     | FFBS mean          |           22 |           56.175 |             66.128 |   0.849 | -0.81  | 0     |    0.008 |
| lgbm_sc_s0 | ST       | WASO    | raw plug-in        |           22 |           82.998 |             82.636 |   1.004 |  0.328 | 0.187 |    1     |
| lgbm_sc_s0 | ST       | WASO    | calibrated plug-in |           22 |           76.315 |             80.352 |   0.95  | -0.407 | 0.098 |    1     |
| lgbm_sc_s0 | ST       | WASO    | FFBS mean          |           22 |           81.191 |             88.338 |   0.919 | -0.794 | 0.001 |    0.011 |


# S5. Seed variability of the in-domain stager (seeds 0, 1, 2)

| cohort   | param   | method        |   cov_mean |   cov_range |   width_mean |   width_cv |
|:---------|:--------|:--------------|-----------:|------------:|-------------:|-----------:|
| HMC      | N1%     | ba_loa        |     0.9134 |      0.0093 |      28.2087 |     0.0056 |
| HMC      | N1%     | norm_reg_ffbs |     0.9054 |      0.0006 |      22.7329 |     0.0057 |
| HMC      | N1%     | scp_abs       |     0.9106 |      0.0013 |      40.6825 |     0.0147 |
| HMC      | N1%     | scp_abs_bc    |     0.9077 |      0.0014 |      27.835  |     0.0246 |
| HMC      | N2%     | ba_loa        |     0.8949 |      0.0129 |      38.3668 |     0.01   |
| HMC      | N2%     | norm_reg_ffbs |     0.9058 |      0.0006 |      36.8146 |     0.0016 |
| HMC      | N2%     | scp_abs       |     0.9073 |      0.0009 |      42.903  |     0.0165 |
| HMC      | N2%     | scp_abs_bc    |     0.9034 |      0.001  |      39.9374 |     0.0172 |
| HMC      | N3%     | ba_loa        |     0.8932 |      0.0097 |      32.8362 |     0.0113 |
| HMC      | N3%     | norm_reg_ffbs |     0.9044 |      0.0004 |      37.1175 |     0.0102 |
| HMC      | N3%     | scp_abs       |     0.9079 |      0.0006 |      37.332  |     0.0052 |
| HMC      | N3%     | scp_abs_bc    |     0.9044 |      0.0018 |      34.6069 |     0.0212 |
| HMC      | REM%    | ba_loa        |     0.9043 |      0.0166 |      19.0357 |     0.0269 |
| HMC      | REM%    | norm_reg_ffbs |     0.9086 |      0.0015 |      22.2425 |     0.0108 |
| HMC      | REM%    | scp_abs       |     0.9076 |      0.0009 |      21.4361 |     0.0071 |
| HMC      | REM%    | scp_abs_bc    |     0.902  |      0.0045 |      18.786  |     0.0138 |
| HMC      | REML    | ba_loa        |     0.8965 |      0.0182 |     190.04   |     0.0213 |
| HMC      | REML    | norm_reg_ffbs |     0.9079 |      0.0005 |     219.599  |     0.0066 |
| HMC      | REML    | scp_abs       |     0.908  |      0.0004 |     188.417  |     0.052  |
| HMC      | REML    | scp_abs_bc    |     0.907  |      0.0019 |     202.223  |     0.048  |
| HMC      | SOL     | ba_loa        |     0.94   |      0.0054 |      30.2615 |     0.0107 |
| HMC      | SOL     | norm_reg_ffbs |     0.9104 |      0.0004 |      25.632  |     0.0073 |
| HMC      | SOL     | scp_abs       |     0.9115 |      0.0026 |      25.3728 |     0.0053 |
| HMC      | SOL     | scp_abs_bc    |     0.9089 |      0.0027 |      22.0243 |     0.0311 |
| HMC      | TST     | ba_loa        |     0.8955 |      0.0035 |     158.981  |     0.0161 |
| HMC      | TST     | norm_reg_ffbs |     0.9104 |      0.0021 |     115.492  |     0.0145 |
| HMC      | TST     | scp_abs       |     0.9096 |      0.0015 |     203.143  |     0.0058 |
| HMC      | TST     | scp_abs_bc    |     0.9074 |      0.0011 |     170.76   |     0.0167 |
| HMC      | WASO    | ba_loa        |     0.8997 |      0.0026 |     113.676  |     0.0148 |
| HMC      | WASO    | norm_reg_ffbs |     0.9108 |      0.0003 |      96.1954 |     0.0096 |
| HMC      | WASO    | scp_abs       |     0.9086 |      0.0015 |     166.403  |     0.0054 |
| HMC      | WASO    | scp_abs_bc    |     0.9042 |      0.0017 |     116.363  |     0.0235 |
| SC       | N1%     | ba_loa        |     0.894  |      0.0079 |      26.7449 |     0.0053 |
| SC       | N1%     | norm_reg_ffbs |     0.9067 |      0.0007 |      26.092  |     0.0028 |
| SC       | N1%     | scp_abs       |     0.9053 |      0.0007 |      33.7756 |     0.005  |
| SC       | N1%     | scp_abs_bc    |     0.9024 |      0.0022 |      27.9485 |     0.013  |
| SC       | N2%     | ba_loa        |     0.892  |      0.009  |      30.3742 |     0.0035 |
| SC       | N2%     | norm_reg_ffbs |     0.9066 |      0.0006 |      30.9741 |     0.0059 |
| SC       | N2%     | scp_abs       |     0.9073 |      0.0011 |      34.117  |     0.0102 |
| SC       | N2%     | scp_abs_bc    |     0.9005 |      0.0022 |      33.0477 |     0.0138 |
| SC       | N3%     | ba_loa        |     0.8889 |      0.0107 |      11.3852 |     0.012  |
| SC       | N3%     | norm_reg_ffbs |     0.9144 |      0.0007 |      12.0363 |     0.0217 |
| SC       | N3%     | scp_abs       |     0.9093 |      0.0014 |      12.6701 |     0.0243 |
| SC       | N3%     | scp_abs_bc    |     0.908  |      0.0012 |      12.4967 |     0.0226 |
| SC       | REM%    | ba_loa        |     0.9252 |      0.003  |      19.0877 |     0.0154 |
| SC       | REM%    | norm_reg_ffbs |     0.9081 |      0.0001 |      22.9327 |     0.0073 |
| SC       | REM%    | scp_abs       |     0.903  |      0.0009 |      16.6219 |     0.0139 |
| SC       | REM%    | scp_abs_bc    |     0.8995 |      0.0014 |      16.5244 |     0.014  |
| SC       | REML    | ba_loa        |     0.9173 |      0.0104 |     125.228  |     0.0749 |
| SC       | REML    | norm_reg_ffbs |     0.9069 |      0.0017 |      79.7085 |     0.0089 |
| SC       | REML    | scp_abs       |     0.914  |      0.002  |     130.921  |     0.0326 |
| SC       | REML    | scp_abs_bc    |     0.914  |      0.0015 |     123.488  |     0.0471 |
| SC       | SOL     | ba_loa        |     0.9493 |      0.0074 |      35.3282 |     0.008  |
| SC       | SOL     | norm_reg_ffbs |     0.9058 |      0.0015 |      23.0824 |     0.0068 |
| SC       | SOL     | scp_abs       |     0.9075 |      0.0059 |      23.335  |     0.0447 |
| SC       | SOL     | scp_abs_bc    |     0.9048 |      0.0015 |      26.2834 |     0.0403 |
| SC       | TST     | ba_loa        |     0.9066 |      0.0048 |      86.9762 |     0.0111 |
| SC       | TST     | norm_reg_ffbs |     0.9075 |      0.0011 |      70.3997 |     0.0014 |
| SC       | TST     | scp_abs       |     0.9073 |      0.0024 |      97.1733 |     0.0282 |
| SC       | TST     | scp_abs_bc    |     0.9033 |      0.0012 |      87.2267 |     0.0294 |
| SC       | WASO    | ba_loa        |     0.9432 |      0.0105 |     100.007  |     0.0124 |
| SC       | WASO    | norm_reg_ffbs |     0.9066 |      0.0018 |     180.583  |     0.0047 |
| SC       | WASO    | scp_abs       |     0.9072 |      0.0004 |      76.7119 |     0.0536 |
| SC       | WASO    | scp_abs_bc    |     0.9063 |      0.0008 |      73.4393 |     0.0512 |
| ST       | N1%     | ba_loa        |     0.8847 |      0.0059 |      14.8623 |     0.0157 |
| ST       | N1%     | norm_reg_ffbs |     0.9134 |      0.0035 |      18.2743 |     0.009  |
| ST       | N1%     | scp_abs       |     0.9003 |      0.0057 |      20.4133 |     0.0163 |
| ST       | N1%     | scp_abs_bc    |     0.8802 |      0.0056 |      14.5338 |     0.0114 |
| ST       | N2%     | ba_loa        |     0.8355 |      0.0063 |      31.118  |     0.0071 |
| ST       | N2%     | norm_reg_ffbs |     0.8995 |      0.0015 |      31.3074 |     0.0096 |
| ST       | N2%     | scp_abs       |     0.9003 |      0.0004 |      35.2813 |     0.0068 |
| ST       | N2%     | scp_abs_bc    |     0.8671 |      0.0088 |      33.8369 |     0.0024 |
| ST       | N3%     | ba_loa        |     0.8558 |      0.0047 |      22.8639 |     0.0061 |
| ST       | N3%     | norm_reg_ffbs |     0.9042 |      0.0005 |      25.6513 |     0.0009 |
| ST       | N3%     | scp_abs       |     0.8991 |      0.005  |      29.4216 |     0.0085 |
| ST       | N3%     | scp_abs_bc    |     0.8869 |      0.005  |      26.3615 |     0.0072 |
| ST       | REM%    | ba_loa        |     0.8703 |      0.0092 |      17.1178 |     0.0143 |
| ST       | REM%    | norm_reg_ffbs |     0.8977 |      0.0032 |      23.1622 |     0.001  |
| ST       | REM%    | scp_abs       |     0.9018 |      0.0014 |      24.9911 |     0.0257 |
| ST       | REM%    | scp_abs_bc    |     0.8931 |      0.0032 |      20.4291 |     0.0215 |
| ST       | REML    | ba_loa        |     0.8519 |      0.0141 |     137.278  |     0.0374 |
| ST       | REML    | norm_reg_ffbs |     0.9136 |      0.0144 |     126.674  |     0.0225 |
| ST       | REML    | scp_abs       |     0.9197 |      0.0009 |     190.766  |     0.0093 |
| ST       | REML    | scp_abs_bc    |     0.9083 |      0.0042 |     174.168  |     0.0559 |
| ST       | SOL     | ba_loa        |     0.9002 |      0.0124 |      19.5923 |     0.0029 |
| ST       | SOL     | norm_reg_ffbs |     0.9006 |      0.0005 |      21.4348 |     0.0062 |
| ST       | SOL     | scp_abs       |     0.9173 |      0.0155 |      16.115  |     0.1083 |
| ST       | SOL     | scp_abs_bc    |     0.9007 |      0.0193 |      15.7596 |     0.0609 |
| ST       | TST     | ba_loa        |     0.8584 |      0.0137 |      60.4372 |     0.0014 |
| ST       | TST     | norm_reg_ffbs |     0.9168 |      0.0049 |      46.9938 |     0.0107 |
| ST       | TST     | scp_abs       |     0.9248 |      0.0017 |      77.9587 |     0.0616 |
| ST       | TST     | scp_abs_bc    |     0.8862 |      0.0169 |      65.1437 |     0.0258 |
| ST       | WASO    | ba_loa        |     0.8676 |      0.0105 |      43.9881 |     0.0028 |
| ST       | WASO    | norm_reg_ffbs |     0.9048 |      0.0017 |      57.5225 |     0.0048 |
| ST       | WASO    | scp_abs       |     0.921  |      0.0033 |      70.2101 |     0.0398 |
| ST       | WASO    | scp_abs_bc    |     0.8961 |      0.0122 |      49.5466 |     0.0201 |


# S6. Sensitivity to the miscoverage level α

| stager     |   alpha | cohort   | param   | method        |   coverage_mean |   mean_width_mean |   interval_score_mean |
|:-----------|--------:|:---------|:--------|:--------------|----------------:|------------------:|----------------------:|
| yasa       |    0.05 | HMC      | N1%     | ba_loa        |           0.946 |            28.696 |                49.872 |
| yasa       |    0.05 | HMC      | N1%     | cqr_ffbs      |           0.959 |            28.59  |                43.299 |
| yasa       |    0.05 | HMC      | N1%     | norm_reg_ffbs |           0.958 |            28.284 |                43.149 |
| yasa       |    0.05 | HMC      | N1%     | scp_abs_bc    |           0.959 |            31.841 |                49.796 |
| yasa       |    0.05 | HMC      | N2%     | ba_loa        |           0.95  |            38.981 |                60.63  |
| yasa       |    0.05 | HMC      | N2%     | cqr_ffbs      |           0.961 |            34.161 |                39.993 |
| yasa       |    0.05 | HMC      | N2%     | norm_reg_ffbs |           0.962 |            34.174 |                40.302 |
| yasa       |    0.05 | HMC      | N2%     | scp_abs_bc    |           0.957 |            45.644 |                64.733 |
| yasa       |    0.05 | HMC      | N3%     | ba_loa        |           0.937 |            28.466 |                40.643 |
| yasa       |    0.05 | HMC      | N3%     | cqr_ffbs      |           0.96  |            37.039 |                40.861 |
| yasa       |    0.05 | HMC      | N3%     | norm_reg_ffbs |           0.961 |            36.571 |                40.485 |
| yasa       |    0.05 | HMC      | N3%     | scp_abs_bc    |           0.957 |            32.348 |                41.176 |
| yasa       |    0.05 | HMC      | REM%    | ba_loa        |           0.948 |            21.367 |                31.245 |
| yasa       |    0.05 | HMC      | REM%    | cqr_ffbs      |           0.96  |            26.615 |                29.886 |
| yasa       |    0.05 | HMC      | REM%    | norm_reg_ffbs |           0.96  |            26.479 |                30.178 |
| yasa       |    0.05 | HMC      | REM%    | scp_abs_bc    |           0.959 |            22.596 |                31.252 |
| yasa       |    0.05 | HMC      | REML    | ba_loa        |           0.931 |           216.038 |               413.653 |
| yasa       |    0.05 | HMC      | REML    | cqr_ffbs      |           0.96  |           209.493 |               327.77  |
| yasa       |    0.05 | HMC      | REML    | norm_reg_ffbs |           0.959 |           250.215 |               354.43  |
| yasa       |    0.05 | HMC      | REML    | scp_abs_bc    |           0.96  |           269.883 |               396.881 |
| yasa       |    0.05 | HMC      | SOL     | ba_loa        |           0.934 |            28.803 |                66.011 |
| yasa       |    0.05 | HMC      | SOL     | cqr_ffbs      |           0.967 |            30.135 |                77.002 |
| yasa       |    0.05 | HMC      | SOL     | norm_reg_ffbs |           0.963 |            34.265 |                87.53  |
| yasa       |    0.05 | HMC      | SOL     | scp_abs_bc    |           0.96  |            38.998 |                62.269 |
| yasa       |    0.05 | HMC      | TST     | ba_loa        |           0.949 |           156.613 |               286.286 |
| yasa       |    0.05 | HMC      | TST     | cqr_ffbs      |           0.961 |           164.485 |               204.226 |
| yasa       |    0.05 | HMC      | TST     | norm_reg_ffbs |           0.96  |           145.7   |               175.093 |
| yasa       |    0.05 | HMC      | TST     | scp_abs_bc    |           0.96  |           178.91  |               285.262 |
| yasa       |    0.05 | HMC      | WASO    | ba_loa        |           0.945 |           118.193 |               238.731 |
| yasa       |    0.05 | HMC      | WASO    | cqr_ffbs      |           0.961 |           140.228 |               175.77  |
| yasa       |    0.05 | HMC      | WASO    | norm_reg_ffbs |           0.96  |           133.629 |               169.855 |
| yasa       |    0.05 | HMC      | WASO    | scp_abs_bc    |           0.959 |           131.817 |               230.642 |
| yasa       |    0.05 | SC       | N1%     | ba_loa        |           0.944 |            33.252 |                53.333 |
| yasa       |    0.05 | SC       | N1%     | cqr_ffbs      |           0.956 |            34.08  |                48.195 |
| yasa       |    0.05 | SC       | N1%     | norm_reg_ffbs |           0.956 |            32.855 |                46.649 |
| yasa       |    0.05 | SC       | N1%     | scp_abs_bc    |           0.955 |            37.338 |                53.33  |
| yasa       |    0.05 | SC       | N2%     | ba_loa        |           0.928 |            46.096 |                69.419 |
| yasa       |    0.05 | SC       | N2%     | cqr_ffbs      |           0.954 |            43.942 |                52.806 |
| yasa       |    0.05 | SC       | N2%     | norm_reg_ffbs |           0.955 |            42.93  |                51.584 |
| yasa       |    0.05 | SC       | N2%     | scp_abs_bc    |           0.955 |            53.756 |                69.364 |
| yasa       |    0.05 | SC       | N3%     | ba_loa        |           0.942 |            18.737 |                32.963 |
| yasa       |    0.05 | SC       | N3%     | cqr_ffbs      |           0.962 |            21.862 |                25.884 |
| yasa       |    0.05 | SC       | N3%     | norm_reg_ffbs |           0.962 |            21.474 |                25.699 |
| yasa       |    0.05 | SC       | N3%     | scp_abs_bc    |           0.958 |            23.049 |                33.122 |
| yasa       |    0.05 | SC       | REM%    | ba_loa        |           0.949 |            25.733 |                46.701 |
| yasa       |    0.05 | SC       | REM%    | cqr_ffbs      |           0.956 |            35.22  |                44.358 |
| yasa       |    0.05 | SC       | REM%    | norm_reg_ffbs |           0.955 |            33.155 |                40.371 |
| yasa       |    0.05 | SC       | REM%    | scp_abs_bc    |           0.95  |            26.266 |                46.887 |
| yasa       |    0.05 | SC       | REML    | ba_loa        |           0.918 |           151.272 |               307.98  |
| yasa       |    0.05 | SC       | REML    | cqr_ffbs      |           0.963 |           135.661 |               189.705 |
| yasa       |    0.05 | SC       | REML    | norm_reg_ffbs |           0.962 |           137.721 |               204.513 |
| yasa       |    0.05 | SC       | REML    | scp_abs_bc    |           0.958 |           191.211 |               286.679 |
| yasa       |    0.05 | SC       | SOL     | ba_loa        |           0.949 |            39.828 |                96.129 |
| yasa       |    0.05 | SC       | SOL     | cqr_ffbs      |           0.966 |            30.953 |                35.787 |
| yasa       |    0.05 | SC       | SOL     | norm_reg_ffbs |           0.958 |            35.7   |                71.593 |
| yasa       |    0.05 | SC       | SOL     | scp_abs_bc    |           0.96  |            52.916 |                99.207 |
| yasa       |    0.05 | SC       | TST     | ba_loa        |           0.936 |           132.609 |               221.907 |
| yasa       |    0.05 | SC       | TST     | cqr_ffbs      |           0.961 |           138.401 |               200.423 |
| yasa       |    0.05 | SC       | TST     | norm_reg_ffbs |           0.96  |           134.604 |               196.961 |
| yasa       |    0.05 | SC       | TST     | scp_abs_bc    |           0.961 |           161.667 |               225.923 |
| yasa       |    0.05 | SC       | WASO    | ba_loa        |           0.939 |           134.001 |               280.916 |
| yasa       |    0.05 | SC       | WASO    | cqr_ffbs      |           0.961 |           229.392 |               305.644 |
| yasa       |    0.05 | SC       | WASO    | norm_reg_ffbs |           0.957 |           272.781 |               342.832 |
| yasa       |    0.05 | SC       | WASO    | scp_abs_bc    |           0.961 |           167.962 |               270.727 |
| yasa       |    0.05 | ST       | N1%     | ba_loa        |           0.9   |            16.899 |                24.453 |
| yasa       |    0.05 | ST       | N1%     | cqr_ffbs      |           0.933 |            19.716 |                27.88  |
| yasa       |    0.05 | ST       | N1%     | norm_reg_ffbs |           0.933 |            19.478 |                28.36  |
| yasa       |    0.05 | ST       | N1%     | scp_abs_bc    |           0.949 |            18.828 |                22.481 |
| yasa       |    0.05 | ST       | N2%     | ba_loa        |           0.893 |            36.618 |                51.83  |
| yasa       |    0.05 | ST       | N2%     | cqr_ffbs      |           0.945 |            39.294 |                46.148 |
| yasa       |    0.05 | ST       | N2%     | norm_reg_ffbs |           0.945 |            39.118 |                45.205 |
| yasa       |    0.05 | ST       | N2%     | scp_abs_bc    |           0.915 |            39.177 |                52.135 |
| yasa       |    0.05 | ST       | N3%     | ba_loa        |           0.897 |            27.776 |                38.898 |
| yasa       |    0.05 | ST       | N3%     | cqr_ffbs      |           0.956 |            29.225 |                31.802 |
| yasa       |    0.05 | ST       | N3%     | norm_reg_ffbs |           0.956 |            28.45  |                30.77  |
| yasa       |    0.05 | ST       | N3%     | scp_abs_bc    |           0.94  |            30.478 |                36.873 |
| yasa       |    0.05 | ST       | REM%    | ba_loa        |           0.898 |            20.549 |                35.442 |
| yasa       |    0.05 | ST       | REM%    | cqr_ffbs      |           0.954 |            28.643 |                32.667 |
| yasa       |    0.05 | ST       | REM%    | norm_reg_ffbs |           0.952 |            29.89  |                34.671 |
| yasa       |    0.05 | ST       | REM%    | scp_abs_bc    |           0.948 |            25.801 |                34.352 |
| yasa       |    0.05 | ST       | REML    | ba_loa        |           0.868 |           142.611 |               307.698 |
| yasa       |    0.05 | ST       | REML    | cqr_ffbs      |           0.953 |           159.268 |               171.704 |
| yasa       |    0.05 | ST       | REML    | norm_reg_ffbs |           0.94  |           186.383 |               261.005 |
| yasa       |    0.05 | ST       | REML    | scp_abs_bc    |           0.93  |           181.569 |               229.554 |
| yasa       |    0.05 | ST       | SOL     | ba_loa        |           0.93  |            13.314 |                23.511 |
| yasa       |    0.05 | ST       | SOL     | cqr_ffbs      |           0.977 |            30.082 |                45.998 |
| yasa       |    0.05 | ST       | SOL     | norm_reg_ffbs |           0.945 |            30.657 |                58.714 |
| yasa       |    0.05 | ST       | SOL     | scp_abs_bc    |           0.96  |            17.454 |                23.784 |
| yasa       |    0.05 | ST       | TST     | ba_loa        |           0.909 |            66.336 |               131.145 |
| yasa       |    0.05 | ST       | TST     | cqr_ffbs      |           0.959 |            61.671 |                81.029 |
| yasa       |    0.05 | ST       | TST     | norm_reg_ffbs |           0.959 |            57.398 |                76.84  |
| yasa       |    0.05 | ST       | TST     | scp_abs_bc    |           0.95  |            98.609 |               134.651 |
| yasa       |    0.05 | ST       | WASO    | ba_loa        |           0.921 |            43.399 |               100.126 |
| yasa       |    0.05 | ST       | WASO    | cqr_ffbs      |           0.957 |            71.521 |                94.781 |
| yasa       |    0.05 | ST       | WASO    | norm_reg_ffbs |           0.958 |            69.05  |                93.543 |
| yasa       |    0.05 | ST       | WASO    | scp_abs_bc    |           0.947 |            64.576 |               108.28  |
| yasa       |    0.2  | HMC      | N1%     | ba_loa        |           0.862 |            20.499 |                30.449 |
| yasa       |    0.2  | HMC      | N1%     | cqr_ffbs      |           0.803 |            15.498 |                28.506 |
| yasa       |    0.2  | HMC      | N1%     | norm_reg_ffbs |           0.802 |            15.724 |                28.429 |
| yasa       |    0.2  | HMC      | N1%     | scp_abs_bc    |           0.797 |            16.952 |                30.028 |
| yasa       |    0.2  | HMC      | N2%     | ba_loa        |           0.853 |            25.489 |                36.611 |
| yasa       |    0.2  | HMC      | N2%     | cqr_ffbs      |           0.803 |            21.888 |                29.322 |
| yasa       |    0.2  | HMC      | N2%     | norm_reg_ffbs |           0.802 |            22.167 |                29.531 |
| yasa       |    0.2  | HMC      | N2%     | scp_abs_bc    |           0.796 |            21.63  |                35.934 |
| yasa       |    0.2  | HMC      | N3%     | ba_loa        |           0.812 |            18.964 |                27.607 |
| yasa       |    0.2  | HMC      | N3%     | cqr_ffbs      |           0.804 |            23.116 |                31.679 |
| yasa       |    0.2  | HMC      | N3%     | norm_reg_ffbs |           0.804 |            23.267 |                31.478 |
| yasa       |    0.2  | HMC      | N3%     | scp_abs_bc    |           0.796 |            18.31  |                27.629 |
| yasa       |    0.2  | HMC      | REM%    | ba_loa        |           0.835 |            14.193 |                20.26  |
| yasa       |    0.2  | HMC      | REM%    | cqr_ffbs      |           0.806 |            16.765 |                22.772 |
| yasa       |    0.2  | HMC      | REM%    | norm_reg_ffbs |           0.805 |            16.745 |                22.725 |
| yasa       |    0.2  | HMC      | REM%    | scp_abs_bc    |           0.796 |            13.017 |                20.155 |
| yasa       |    0.2  | HMC      | REML    | ba_loa        |           0.862 |           152.97  |               243.067 |
| yasa       |    0.2  | HMC      | REML    | cqr_ffbs      |           0.803 |           111.581 |               226.772 |
| yasa       |    0.2  | HMC      | REML    | norm_reg_ffbs |           0.802 |           120.491 |               251.875 |
| yasa       |    0.2  | HMC      | REML    | scp_abs_bc    |           0.798 |           112.619 |               240.187 |
| yasa       |    0.2  | HMC      | SOL     | ba_loa        |           0.897 |            19.725 |                34.826 |
| yasa       |    0.2  | HMC      | SOL     | cqr_ffbs      |           0.839 |            15.282 |                38.858 |
| yasa       |    0.2  | HMC      | SOL     | norm_reg_ffbs |           0.803 |            13.079 |                45.893 |
| yasa       |    0.2  | HMC      | SOL     | scp_abs_bc    |           0.8   |            11.084 |                34.234 |
| yasa       |    0.2  | HMC      | TST     | ba_loa        |           0.9   |           102.404 |               152.296 |
| yasa       |    0.2  | HMC      | TST     | cqr_ffbs      |           0.807 |            57.466 |               111.592 |
| yasa       |    0.2  | HMC      | TST     | norm_reg_ffbs |           0.807 |            55.911 |               108.619 |
| yasa       |    0.2  | HMC      | TST     | scp_abs_bc    |           0.802 |            63.968 |               136.887 |
| yasa       |    0.2  | HMC      | WASO    | ba_loa        |           0.882 |            82.66  |               131.606 |
| yasa       |    0.2  | HMC      | WASO    | cqr_ffbs      |           0.809 |            51.395 |               104.492 |
| yasa       |    0.2  | HMC      | WASO    | norm_reg_ffbs |           0.806 |            51.399 |               105.013 |
| yasa       |    0.2  | HMC      | WASO    | scp_abs_bc    |           0.802 |            58.613 |               128.805 |
| yasa       |    0.2  | SC       | N1%     | ba_loa        |           0.864 |            23.451 |                33.459 |
| yasa       |    0.2  | SC       | N1%     | cqr_ffbs      |           0.804 |            21.935 |                35.012 |
| yasa       |    0.2  | SC       | N1%     | norm_reg_ffbs |           0.803 |            21.934 |                34.913 |
| yasa       |    0.2  | SC       | N1%     | scp_abs_bc    |           0.791 |            20.503 |                32.92  |
| yasa       |    0.2  | SC       | N2%     | ba_loa        |           0.845 |            30.148 |                43.831 |
| yasa       |    0.2  | SC       | N2%     | cqr_ffbs      |           0.803 |            23.338 |                35.691 |
| yasa       |    0.2  | SC       | N2%     | norm_reg_ffbs |           0.803 |            23.405 |                35.644 |
| yasa       |    0.2  | SC       | N2%     | scp_abs_bc    |           0.791 |            26.886 |                43.373 |
| yasa       |    0.2  | SC       | N3%     | ba_loa        |           0.847 |            12.588 |                19.796 |
| yasa       |    0.2  | SC       | N3%     | cqr_ffbs      |           0.809 |            11.92  |                18.729 |
| yasa       |    0.2  | SC       | N3%     | norm_reg_ffbs |           0.81  |            11.882 |                18.614 |
| yasa       |    0.2  | SC       | N3%     | scp_abs_bc    |           0.812 |            11.207 |                19.895 |
| yasa       |    0.2  | SC       | REM%    | ba_loa        |           0.881 |            17.04  |                25.359 |
| yasa       |    0.2  | SC       | REM%    | cqr_ffbs      |           0.802 |            18.679 |                27.969 |
| yasa       |    0.2  | SC       | REM%    | norm_reg_ffbs |           0.804 |            18.76  |                27.645 |
| yasa       |    0.2  | SC       | REM%    | scp_abs_bc    |           0.8   |            12.388 |                23.903 |
| yasa       |    0.2  | SC       | REML    | ba_loa        |           0.86  |           105.312 |               176.891 |
| yasa       |    0.2  | SC       | REML    | cqr_ffbs      |           0.819 |            74.192 |               101.463 |
| yasa       |    0.2  | SC       | REML    | norm_reg_ffbs |           0.811 |            71.99  |               122.11  |
| yasa       |    0.2  | SC       | REML    | scp_abs_bc    |           0.809 |            61.821 |               173.726 |
| yasa       |    0.2  | SC       | SOL     | ba_loa        |           0.913 |            27.782 |                47.494 |
| yasa       |    0.2  | SC       | SOL     | cqr_ffbs      |           0.853 |            22.454 |                32.091 |
| yasa       |    0.2  | SC       | SOL     | norm_reg_ffbs |           0.803 |            19.246 |                43.457 |
| yasa       |    0.2  | SC       | SOL     | scp_abs_bc    |           0.796 |            15.683 |                46.289 |
| yasa       |    0.2  | SC       | TST     | ba_loa        |           0.851 |            86.709 |               130.897 |
| yasa       |    0.2  | SC       | TST     | cqr_ffbs      |           0.807 |            58.021 |               108.526 |
| yasa       |    0.2  | SC       | TST     | norm_reg_ffbs |           0.806 |            57.597 |               107.383 |
| yasa       |    0.2  | SC       | TST     | scp_abs_bc    |           0.8   |            69.528 |               128.023 |
| yasa       |    0.2  | SC       | WASO    | ba_loa        |           0.875 |            92.881 |               155.889 |
| yasa       |    0.2  | SC       | WASO    | cqr_ffbs      |           0.803 |           167.682 |               249.913 |
| yasa       |    0.2  | SC       | WASO    | norm_reg_ffbs |           0.805 |           190.655 |               266.401 |
| yasa       |    0.2  | SC       | WASO    | scp_abs_bc    |           0.799 |            70.086 |               158.572 |
| yasa       |    0.2  | ST       | N1%     | ba_loa        |           0.759 |            11.469 |                17.988 |
| yasa       |    0.2  | ST       | N1%     | cqr_ffbs      |           0.824 |            13.401 |                21.216 |
| yasa       |    0.2  | ST       | N1%     | norm_reg_ffbs |           0.825 |            13.19  |                20.681 |
| yasa       |    0.2  | ST       | N1%     | scp_abs_bc    |           0.795 |            12.719 |                18.044 |
| yasa       |    0.2  | ST       | N2%     | ba_loa        |           0.722 |            23.944 |                38.207 |
| yasa       |    0.2  | ST       | N2%     | cqr_ffbs      |           0.803 |            26.876 |                34.449 |
| yasa       |    0.2  | ST       | N2%     | norm_reg_ffbs |           0.806 |            27.552 |                34.982 |
| yasa       |    0.2  | ST       | N2%     | scp_abs_bc    |           0.763 |            26.3   |                38.022 |
| yasa       |    0.2  | ST       | N3%     | ba_loa        |           0.74  |            18.673 |                29.549 |
| yasa       |    0.2  | ST       | N3%     | cqr_ffbs      |           0.814 |            21.905 |                27.278 |
| yasa       |    0.2  | ST       | N3%     | norm_reg_ffbs |           0.812 |            22.059 |                27.185 |
| yasa       |    0.2  | ST       | N3%     | scp_abs_bc    |           0.774 |            20.531 |                29.693 |
| yasa       |    0.2  | ST       | REM%    | ba_loa        |           0.79  |            13.492 |                21.733 |
| yasa       |    0.2  | ST       | REM%    | cqr_ffbs      |           0.82  |            19.486 |                24.621 |
| yasa       |    0.2  | ST       | REM%    | norm_reg_ffbs |           0.824 |            19.98  |                25.157 |
| yasa       |    0.2  | ST       | REM%    | scp_abs_bc    |           0.811 |            14.377 |                22.206 |
| yasa       |    0.2  | ST       | REML    | ba_loa        |           0.832 |            97.333 |               173.485 |
| yasa       |    0.2  | ST       | REML    | cqr_ffbs      |           0.829 |            97.801 |               125.802 |
| yasa       |    0.2  | ST       | REML    | norm_reg_ffbs |           0.835 |           106.027 |               145.606 |
| yasa       |    0.2  | ST       | REML    | scp_abs_bc    |           0.835 |           103.596 |               187.646 |
| yasa       |    0.2  | ST       | SOL     | ba_loa        |           0.853 |             8.915 |                13.502 |
| yasa       |    0.2  | ST       | SOL     | cqr_ffbs      |           0.885 |            14.587 |                21.797 |
| yasa       |    0.2  | ST       | SOL     | norm_reg_ffbs |           0.816 |            14.175 |                27.936 |
| yasa       |    0.2  | ST       | SOL     | scp_abs_bc    |           0.813 |             8.046 |                13.249 |
| yasa       |    0.2  | ST       | TST     | ba_loa        |           0.859 |            43.375 |                69.719 |
| yasa       |    0.2  | ST       | TST     | cqr_ffbs      |           0.833 |            24.923 |                41.565 |
| yasa       |    0.2  | ST       | TST     | norm_reg_ffbs |           0.821 |            24.598 |                42.848 |
| yasa       |    0.2  | ST       | TST     | scp_abs_bc    |           0.819 |            37.136 |                68.219 |
| yasa       |    0.2  | ST       | WASO    | ba_loa        |           0.86  |            29.499 |                51.225 |
| yasa       |    0.2  | ST       | WASO    | cqr_ffbs      |           0.82  |            35.093 |                59.609 |
| yasa       |    0.2  | ST       | WASO    | norm_reg_ffbs |           0.815 |            37.323 |                63.28  |
| yasa       |    0.2  | ST       | WASO    | scp_abs_bc    |           0.791 |            24.608 |                48.749 |
| lgbm_sc_s0 |    0.05 | HMC      | N1%     | ba_loa        |           0.943 |            32.52  |                53.092 |
| lgbm_sc_s0 |    0.05 | HMC      | N1%     | cqr_ffbs      |           0.959 |            31.216 |                47.869 |
| lgbm_sc_s0 |    0.05 | HMC      | N1%     | norm_reg_ffbs |           0.96  |            31.287 |                49.235 |
| lgbm_sc_s0 |    0.05 | HMC      | N1%     | scp_abs_bc    |           0.959 |            36.197 |                52.371 |
| lgbm_sc_s0 |    0.05 | HMC      | N2%     | ba_loa        |           0.934 |            45.22  |                62.883 |
| lgbm_sc_s0 |    0.05 | HMC      | N2%     | cqr_ffbs      |           0.96  |            47.846 |                57.103 |
| lgbm_sc_s0 |    0.05 | HMC      | N2%     | norm_reg_ffbs |           0.959 |            47.978 |                57.091 |
| lgbm_sc_s0 |    0.05 | HMC      | N2%     | scp_abs_bc    |           0.958 |            53.237 |                64.442 |
| lgbm_sc_s0 |    0.05 | HMC      | N3%     | ba_loa        |           0.93  |            38.303 |                56.019 |
| lgbm_sc_s0 |    0.05 | HMC      | N3%     | cqr_ffbs      |           0.959 |            52.81  |                74.875 |
| lgbm_sc_s0 |    0.05 | HMC      | N3%     | norm_reg_ffbs |           0.959 |            52.613 |                72.172 |
| lgbm_sc_s0 |    0.05 | HMC      | N3%     | scp_abs_bc    |           0.958 |            43.847 |                54.808 |
| lgbm_sc_s0 |    0.05 | HMC      | REM%    | ba_loa        |           0.946 |            21.73  |                31.015 |
| lgbm_sc_s0 |    0.05 | HMC      | REM%    | cqr_ffbs      |           0.962 |            26.902 |                31.222 |
| lgbm_sc_s0 |    0.05 | HMC      | REM%    | norm_reg_ffbs |           0.962 |            26.647 |                31.417 |
| lgbm_sc_s0 |    0.05 | HMC      | REM%    | scp_abs_bc    |           0.958 |            24.036 |                31.915 |
| lgbm_sc_s0 |    0.05 | HMC      | REML    | ba_loa        |           0.929 |           219.107 |               395.023 |
| lgbm_sc_s0 |    0.05 | HMC      | REML    | cqr_ffbs      |           0.96  |           298.41  |               434.157 |
| lgbm_sc_s0 |    0.05 | HMC      | REML    | norm_reg_ffbs |           0.961 |           307.75  |               425.587 |
| lgbm_sc_s0 |    0.05 | HMC      | REML    | scp_abs_bc    |           0.96  |           270.873 |               381.757 |
| lgbm_sc_s0 |    0.05 | HMC      | SOL     | ba_loa        |           0.95  |            35.423 |                83.304 |
| lgbm_sc_s0 |    0.05 | HMC      | SOL     | cqr_ffbs      |           0.963 |            40.303 |                90.069 |
| lgbm_sc_s0 |    0.05 | HMC      | SOL     | norm_reg_ffbs |           0.963 |            41.023 |                92.511 |
| lgbm_sc_s0 |    0.05 | HMC      | SOL     | scp_abs_bc    |           0.959 |            43.892 |                83.448 |
| lgbm_sc_s0 |    0.05 | HMC      | TST     | ba_loa        |           0.928 |           185.687 |               306.759 |
| lgbm_sc_s0 |    0.05 | HMC      | TST     | cqr_ffbs      |           0.961 |           169.426 |               203.226 |
| lgbm_sc_s0 |    0.05 | HMC      | TST     | norm_reg_ffbs |           0.961 |           152.126 |               185.835 |
| lgbm_sc_s0 |    0.05 | HMC      | TST     | scp_abs_bc    |           0.959 |           231.215 |               312.127 |
| lgbm_sc_s0 |    0.05 | HMC      | WASO    | ba_loa        |           0.934 |           128.402 |               230.096 |
| lgbm_sc_s0 |    0.05 | HMC      | WASO    | cqr_ffbs      |           0.962 |           133.275 |               158.243 |
| lgbm_sc_s0 |    0.05 | HMC      | WASO    | norm_reg_ffbs |           0.961 |           127.733 |               154.902 |
| lgbm_sc_s0 |    0.05 | HMC      | WASO    | scp_abs_bc    |           0.956 |           145.369 |               222.615 |
| lgbm_sc_s0 |    0.05 | SC       | N1%     | ba_loa        |           0.921 |            30.664 |                54.151 |
| lgbm_sc_s0 |    0.05 | SC       | N1%     | cqr_ffbs      |           0.957 |            34.344 |                46.682 |
| lgbm_sc_s0 |    0.05 | SC       | N1%     | norm_reg_ffbs |           0.958 |            33.298 |                45.508 |
| lgbm_sc_s0 |    0.05 | SC       | N1%     | scp_abs_bc    |           0.957 |            39.58  |                48.123 |
| lgbm_sc_s0 |    0.05 | SC       | N2%     | ba_loa        |           0.922 |            36.039 |                54.846 |
| lgbm_sc_s0 |    0.05 | SC       | N2%     | cqr_ffbs      |           0.957 |            42.02  |                51.639 |
| lgbm_sc_s0 |    0.05 | SC       | N2%     | norm_reg_ffbs |           0.957 |            41.045 |                50.231 |
| lgbm_sc_s0 |    0.05 | SC       | N2%     | scp_abs_bc    |           0.957 |            45.229 |                54.219 |
| lgbm_sc_s0 |    0.05 | SC       | N3%     | ba_loa        |           0.923 |            13.617 |                23.051 |
| lgbm_sc_s0 |    0.05 | SC       | N3%     | cqr_ffbs      |           0.96  |            16.459 |                19.634 |
| lgbm_sc_s0 |    0.05 | SC       | N3%     | norm_reg_ffbs |           0.962 |            16.002 |                19.448 |
| lgbm_sc_s0 |    0.05 | SC       | N3%     | scp_abs_bc    |           0.959 |            17.297 |                21.944 |
| lgbm_sc_s0 |    0.05 | SC       | REM%    | ba_loa        |           0.949 |            22.161 |                41.134 |
| lgbm_sc_s0 |    0.05 | SC       | REM%    | cqr_ffbs      |           0.959 |            31.796 |                42.598 |
| lgbm_sc_s0 |    0.05 | SC       | REM%    | norm_reg_ffbs |           0.959 |            30.335 |                39.998 |
| lgbm_sc_s0 |    0.05 | SC       | REM%    | scp_abs_bc    |           0.95  |            24.393 |                42.348 |
| lgbm_sc_s0 |    0.05 | SC       | REML    | ba_loa        |           0.936 |           138.341 |               264.941 |
| lgbm_sc_s0 |    0.05 | SC       | REML    | cqr_ffbs      |           0.963 |           120.31  |               129.367 |
| lgbm_sc_s0 |    0.05 | SC       | REML    | norm_reg_ffbs |           0.961 |           124.876 |               199.284 |
| lgbm_sc_s0 |    0.05 | SC       | REML    | scp_abs_bc    |           0.959 |           170.734 |               260.778 |
| lgbm_sc_s0 |    0.05 | SC       | SOL     | ba_loa        |           0.962 |            39.956 |                90.767 |
| lgbm_sc_s0 |    0.05 | SC       | SOL     | cqr_ffbs      |           0.961 |            28.937 |                35.39  |
| lgbm_sc_s0 |    0.05 | SC       | SOL     | norm_reg_ffbs |           0.959 |            34.868 |                65.522 |
| lgbm_sc_s0 |    0.05 | SC       | SOL     | scp_abs_bc    |           0.958 |            43.476 |                95.679 |
| lgbm_sc_s0 |    0.05 | SC       | TST     | ba_loa        |           0.929 |           105.269 |               175.573 |
| lgbm_sc_s0 |    0.05 | SC       | TST     | cqr_ffbs      |           0.957 |           120.53  |               159.047 |
| lgbm_sc_s0 |    0.05 | SC       | TST     | norm_reg_ffbs |           0.958 |           117.654 |               153.608 |
| lgbm_sc_s0 |    0.05 | SC       | TST     | scp_abs_bc    |           0.961 |           140.986 |               176.172 |
| lgbm_sc_s0 |    0.05 | SC       | WASO    | ba_loa        |           0.953 |           116.97  |               254.178 |
| lgbm_sc_s0 |    0.05 | SC       | WASO    | cqr_ffbs      |           0.958 |           179.149 |               234.128 |
| lgbm_sc_s0 |    0.05 | SC       | WASO    | norm_reg_ffbs |           0.956 |           214.811 |               310.102 |
| lgbm_sc_s0 |    0.05 | SC       | WASO    | scp_abs_bc    |           0.962 |           130.412 |               250.074 |
| lgbm_sc_s0 |    0.05 | ST       | N1%     | ba_loa        |           0.935 |            17.249 |                31.023 |
| lgbm_sc_s0 |    0.05 | ST       | N1%     | cqr_ffbs      |           0.934 |            19.395 |                31.556 |
| lgbm_sc_s0 |    0.05 | ST       | N1%     | norm_reg_ffbs |           0.934 |            19.213 |                32.281 |
| lgbm_sc_s0 |    0.05 | ST       | N1%     | scp_abs_bc    |           0.941 |            21.737 |                34.83  |
| lgbm_sc_s0 |    0.05 | ST       | N2%     | ba_loa        |           0.895 |            36.787 |                51.898 |
| lgbm_sc_s0 |    0.05 | ST       | N2%     | cqr_ffbs      |           0.948 |            38.064 |                45.916 |
| lgbm_sc_s0 |    0.05 | ST       | N2%     | norm_reg_ffbs |           0.949 |            37.928 |                45.222 |
| lgbm_sc_s0 |    0.05 | ST       | N2%     | scp_abs_bc    |           0.907 |            38.294 |                50.902 |
| lgbm_sc_s0 |    0.05 | ST       | N3%     | ba_loa        |           0.9   |            26.749 |                45.816 |
| lgbm_sc_s0 |    0.05 | ST       | N3%     | cqr_ffbs      |           0.953 |            31.045 |                35.556 |
| lgbm_sc_s0 |    0.05 | ST       | N3%     | norm_reg_ffbs |           0.952 |            29.035 |                32.971 |
| lgbm_sc_s0 |    0.05 | ST       | N3%     | scp_abs_bc    |           0.948 |            32.799 |                42.157 |
| lgbm_sc_s0 |    0.05 | ST       | REM%    | ba_loa        |           0.899 |            20.635 |                35.223 |
| lgbm_sc_s0 |    0.05 | ST       | REM%    | cqr_ffbs      |           0.952 |            27.198 |                30.842 |
| lgbm_sc_s0 |    0.05 | ST       | REM%    | norm_reg_ffbs |           0.954 |            27.724 |                31.59  |
| lgbm_sc_s0 |    0.05 | ST       | REM%    | scp_abs_bc    |           0.948 |            25.642 |                31.78  |
| lgbm_sc_s0 |    0.05 | ST       | REML    | ba_loa        |           0.88  |           164.436 |               309.449 |
| lgbm_sc_s0 |    0.05 | ST       | REML    | cqr_ffbs      |           0.953 |           157.172 |               164.6   |
| lgbm_sc_s0 |    0.05 | ST       | REML    | norm_reg_ffbs |           0.945 |           145.101 |               175.892 |
| lgbm_sc_s0 |    0.05 | ST       | REML    | scp_abs_bc    |           0.949 |           205.365 |               241.876 |
| lgbm_sc_s0 |    0.05 | ST       | SOL     | ba_loa        |           0.911 |            22.556 |                70.586 |
| lgbm_sc_s0 |    0.05 | ST       | SOL     | cqr_ffbs      |           0.954 |            31.612 |                54.311 |
| lgbm_sc_s0 |    0.05 | ST       | SOL     | norm_reg_ffbs |           0.947 |            33.601 |                61.042 |
| lgbm_sc_s0 |    0.05 | ST       | SOL     | scp_abs_bc    |           0.928 |            36.053 |                79.439 |
| lgbm_sc_s0 |    0.05 | ST       | TST     | ba_loa        |           0.915 |            71.978 |               108.941 |
| lgbm_sc_s0 |    0.05 | ST       | TST     | cqr_ffbs      |           0.929 |            63.733 |                98.746 |
| lgbm_sc_s0 |    0.05 | ST       | TST     | norm_reg_ffbs |           0.928 |            59.113 |                91.133 |
| lgbm_sc_s0 |    0.05 | ST       | TST     | scp_abs_bc    |           0.953 |            88.399 |               114.355 |
| lgbm_sc_s0 |    0.05 | ST       | WASO    | ba_loa        |           0.898 |            50.667 |                81.732 |
| lgbm_sc_s0 |    0.05 | ST       | WASO    | cqr_ffbs      |           0.96  |            66.826 |                87.559 |
| lgbm_sc_s0 |    0.05 | ST       | WASO    | norm_reg_ffbs |           0.945 |            72.973 |               105.515 |
| lgbm_sc_s0 |    0.05 | ST       | WASO    | scp_abs_bc    |           0.935 |            56.306 |                73.818 |
| lgbm_sc_s0 |    0.2  | HMC      | N1%     | ba_loa        |           0.85  |            23.041 |                34.559 |
| lgbm_sc_s0 |    0.2  | HMC      | N1%     | cqr_ffbs      |           0.803 |            15.486 |                30.357 |
| lgbm_sc_s0 |    0.2  | HMC      | N1%     | norm_reg_ffbs |           0.802 |            15.48  |                30.555 |
| lgbm_sc_s0 |    0.2  | HMC      | N1%     | scp_abs_bc    |           0.798 |            20.693 |                34.803 |
| lgbm_sc_s0 |    0.2  | HMC      | N2%     | ba_loa        |           0.811 |            29.648 |                43.13  |
| lgbm_sc_s0 |    0.2  | HMC      | N2%     | cqr_ffbs      |           0.803 |            25.294 |                38.095 |
| lgbm_sc_s0 |    0.2  | HMC      | N2%     | norm_reg_ffbs |           0.802 |            25.494 |                38.257 |
| lgbm_sc_s0 |    0.2  | HMC      | N2%     | scp_abs_bc    |           0.8   |            28.928 |                43.151 |
| lgbm_sc_s0 |    0.2  | HMC      | N3%     | ba_loa        |           0.83  |            26.011 |                38.234 |
| lgbm_sc_s0 |    0.2  | HMC      | N3%     | cqr_ffbs      |           0.799 |            26.658 |                44.369 |
| lgbm_sc_s0 |    0.2  | HMC      | N3%     | norm_reg_ffbs |           0.8   |            26.8   |                44.368 |
| lgbm_sc_s0 |    0.2  | HMC      | N3%     | scp_abs_bc    |           0.795 |            23.65  |                38.244 |
| lgbm_sc_s0 |    0.2  | HMC      | REM%    | ba_loa        |           0.798 |            14.51  |                21.018 |
| lgbm_sc_s0 |    0.2  | HMC      | REM%    | cqr_ffbs      |           0.803 |            17.889 |                23.328 |
| lgbm_sc_s0 |    0.2  | HMC      | REM%    | norm_reg_ffbs |           0.802 |            17.821 |                23.344 |
| lgbm_sc_s0 |    0.2  | HMC      | REM%    | scp_abs_bc    |           0.793 |            14.393 |                21.022 |
| lgbm_sc_s0 |    0.2  | HMC      | REML    | ba_loa        |           0.842 |           155.411 |               243.625 |
| lgbm_sc_s0 |    0.2  | HMC      | REML    | cqr_ffbs      |           0.803 |           131.099 |               326.108 |
| lgbm_sc_s0 |    0.2  | HMC      | REML    | norm_reg_ffbs |           0.8   |           143.946 |               320.847 |
| lgbm_sc_s0 |    0.2  | HMC      | REML    | scp_abs_bc    |           0.802 |           131.482 |               243.808 |
| lgbm_sc_s0 |    0.2  | HMC      | SOL     | ba_loa        |           0.918 |            25.016 |                42.057 |
| lgbm_sc_s0 |    0.2  | HMC      | SOL     | cqr_ffbs      |           0.825 |            14.24  |                49.851 |
| lgbm_sc_s0 |    0.2  | HMC      | SOL     | norm_reg_ffbs |           0.807 |            13.593 |                53.726 |
| lgbm_sc_s0 |    0.2  | HMC      | SOL     | scp_abs_bc    |           0.802 |            12.318 |                40.35  |
| lgbm_sc_s0 |    0.2  | HMC      | TST     | ba_loa        |           0.847 |           121.414 |               185.635 |
| lgbm_sc_s0 |    0.2  | HMC      | TST     | cqr_ffbs      |           0.808 |            72.892 |               132.58  |
| lgbm_sc_s0 |    0.2  | HMC      | TST     | norm_reg_ffbs |           0.805 |            71.169 |               129.705 |
| lgbm_sc_s0 |    0.2  | HMC      | TST     | scp_abs_bc    |           0.803 |           101.802 |               183.377 |
| lgbm_sc_s0 |    0.2  | HMC      | WASO    | ba_loa        |           0.843 |            91.276 |               144.949 |
| lgbm_sc_s0 |    0.2  | HMC      | WASO    | cqr_ffbs      |           0.809 |            68.425 |               114.118 |
| lgbm_sc_s0 |    0.2  | HMC      | WASO    | norm_reg_ffbs |           0.808 |            68.126 |               113.046 |
| lgbm_sc_s0 |    0.2  | HMC      | WASO    | scp_abs_bc    |           0.803 |            78.918 |               147.826 |
| lgbm_sc_s0 |    0.2  | SC       | N1%     | ba_loa        |           0.833 |            21.494 |                34.276 |
| lgbm_sc_s0 |    0.2  | SC       | N1%     | cqr_ffbs      |           0.803 |            21.102 |                34.725 |
| lgbm_sc_s0 |    0.2  | SC       | N1%     | norm_reg_ffbs |           0.804 |            21.245 |                34.386 |
| lgbm_sc_s0 |    0.2  | SC       | N1%     | scp_abs_bc    |           0.796 |            19.087 |                34.723 |
| lgbm_sc_s0 |    0.2  | SC       | N2%     | ba_loa        |           0.822 |            23.565 |                35.375 |
| lgbm_sc_s0 |    0.2  | SC       | N2%     | cqr_ffbs      |           0.802 |            19.671 |                32.852 |
| lgbm_sc_s0 |    0.2  | SC       | N2%     | norm_reg_ffbs |           0.802 |            19.575 |                32.69  |
| lgbm_sc_s0 |    0.2  | SC       | N2%     | scp_abs_bc    |           0.798 |            21.897 |                35.468 |
| lgbm_sc_s0 |    0.2  | SC       | N3%     | ba_loa        |           0.819 |             9.129 |                14.94  |
| lgbm_sc_s0 |    0.2  | SC       | N3%     | cqr_ffbs      |           0.806 |             8.678 |                14.122 |
| lgbm_sc_s0 |    0.2  | SC       | N3%     | norm_reg_ffbs |           0.806 |             8.606 |                14.094 |
| lgbm_sc_s0 |    0.2  | SC       | N3%     | scp_abs_bc    |           0.8   |             8.618 |                15.175 |
| lgbm_sc_s0 |    0.2  | SC       | REM%    | ba_loa        |           0.876 |            14.578 |                22.041 |
| lgbm_sc_s0 |    0.2  | SC       | REM%    | cqr_ffbs      |           0.806 |            17.318 |                25.892 |
| lgbm_sc_s0 |    0.2  | SC       | REM%    | norm_reg_ffbs |           0.806 |            17.143 |                25.54  |
| lgbm_sc_s0 |    0.2  | SC       | REM%    | scp_abs_bc    |           0.801 |            10.68  |                20.955 |
| lgbm_sc_s0 |    0.2  | SC       | REML    | ba_loa        |           0.882 |            93.698 |               145.954 |
| lgbm_sc_s0 |    0.2  | SC       | REML    | cqr_ffbs      |           0.818 |            68.833 |                97.028 |
| lgbm_sc_s0 |    0.2  | SC       | REML    | norm_reg_ffbs |           0.804 |            56.856 |               113.413 |
| lgbm_sc_s0 |    0.2  | SC       | REML    | scp_abs_bc    |           0.81  |            52.364 |               137.591 |
| lgbm_sc_s0 |    0.2  | SC       | SOL     | ba_loa        |           0.93  |            28.798 |                45.261 |
| lgbm_sc_s0 |    0.2  | SC       | SOL     | cqr_ffbs      |           0.835 |            19.989 |                29.625 |
| lgbm_sc_s0 |    0.2  | SC       | SOL     | norm_reg_ffbs |           0.804 |            16.744 |                40.669 |
| lgbm_sc_s0 |    0.2  | SC       | SOL     | scp_abs_bc    |           0.805 |            15.269 |                41.97  |
| lgbm_sc_s0 |    0.2  | SC       | TST     | ba_loa        |           0.855 |            68.832 |               104.168 |
| lgbm_sc_s0 |    0.2  | SC       | TST     | cqr_ffbs      |           0.809 |            43.188 |                83.107 |
| lgbm_sc_s0 |    0.2  | SC       | TST     | norm_reg_ffbs |           0.804 |            43.359 |                83.349 |
| lgbm_sc_s0 |    0.2  | SC       | TST     | scp_abs_bc    |           0.804 |            53.906 |               101.581 |
| lgbm_sc_s0 |    0.2  | SC       | WASO    | ba_loa        |           0.915 |            81.981 |               131.035 |
| lgbm_sc_s0 |    0.2  | SC       | WASO    | cqr_ffbs      |           0.803 |           133.655 |               190.413 |
| lgbm_sc_s0 |    0.2  | SC       | WASO    | norm_reg_ffbs |           0.801 |           158.322 |               213.932 |
| lgbm_sc_s0 |    0.2  | SC       | WASO    | scp_abs_bc    |           0.802 |            48.132 |               123.479 |
| lgbm_sc_s0 |    0.2  | ST       | N1%     | ba_loa        |           0.79  |            12.063 |                19.328 |
| lgbm_sc_s0 |    0.2  | ST       | N1%     | cqr_ffbs      |           0.821 |            13.235 |                20.591 |
| lgbm_sc_s0 |    0.2  | ST       | N1%     | norm_reg_ffbs |           0.82  |            13.141 |                20.235 |
| lgbm_sc_s0 |    0.2  | ST       | N1%     | scp_abs_bc    |           0.774 |            11.856 |                19.21  |
| lgbm_sc_s0 |    0.2  | ST       | N2%     | ba_loa        |           0.75  |            24.053 |                37.621 |
| lgbm_sc_s0 |    0.2  | ST       | N2%     | cqr_ffbs      |           0.799 |            26.404 |                33.025 |
| lgbm_sc_s0 |    0.2  | ST       | N2%     | norm_reg_ffbs |           0.799 |            26.679 |                33.322 |
| lgbm_sc_s0 |    0.2  | ST       | N2%     | scp_abs_bc    |           0.789 |            27.075 |                38.357 |
| lgbm_sc_s0 |    0.2  | ST       | N3%     | ba_loa        |           0.777 |            17.982 |                29.503 |
| lgbm_sc_s0 |    0.2  | ST       | N3%     | cqr_ffbs      |           0.811 |            19.256 |                27.502 |
| lgbm_sc_s0 |    0.2  | ST       | N3%     | norm_reg_ffbs |           0.81  |            18.874 |                26.778 |
| lgbm_sc_s0 |    0.2  | ST       | N3%     | scp_abs_bc    |           0.782 |            18.403 |                29.739 |
| lgbm_sc_s0 |    0.2  | ST       | REM%    | ba_loa        |           0.798 |            13.549 |                21.691 |
| lgbm_sc_s0 |    0.2  | ST       | REM%    | cqr_ffbs      |           0.807 |            19.956 |                24.977 |
| lgbm_sc_s0 |    0.2  | ST       | REM%    | norm_reg_ffbs |           0.803 |            19.263 |                24.452 |
| lgbm_sc_s0 |    0.2  | ST       | REM%    | scp_abs_bc    |           0.79  |            13.891 |                22.447 |
| lgbm_sc_s0 |    0.2  | ST       | REML    | ba_loa        |           0.806 |           114.596 |               195.679 |
| lgbm_sc_s0 |    0.2  | ST       | REML    | cqr_ffbs      |           0.83  |           103.441 |               111.222 |
| lgbm_sc_s0 |    0.2  | ST       | REML    | norm_reg_ffbs |           0.835 |           103.461 |               131.36  |
| lgbm_sc_s0 |    0.2  | ST       | REML    | scp_abs_bc    |           0.822 |           128.435 |               203.615 |
| lgbm_sc_s0 |    0.2  | ST       | SOL     | ba_loa        |           0.86  |            15.792 |                29.696 |
| lgbm_sc_s0 |    0.2  | ST       | SOL     | cqr_ffbs      |           0.875 |            15.121 |                26.756 |
| lgbm_sc_s0 |    0.2  | ST       | SOL     | norm_reg_ffbs |           0.812 |            15.862 |                33.041 |
| lgbm_sc_s0 |    0.2  | ST       | SOL     | scp_abs_bc    |           0.82  |            10.431 |                25.32  |
| lgbm_sc_s0 |    0.2  | ST       | TST     | ba_loa        |           0.775 |            47.064 |                73.217 |
| lgbm_sc_s0 |    0.2  | ST       | TST     | cqr_ffbs      |           0.84  |            32.627 |                47.163 |
| lgbm_sc_s0 |    0.2  | ST       | TST     | norm_reg_ffbs |           0.829 |            32.297 |                47.567 |
| lgbm_sc_s0 |    0.2  | ST       | TST     | scp_abs_bc    |           0.791 |            49.618 |                73.861 |
| lgbm_sc_s0 |    0.2  | ST       | WASO    | ba_loa        |           0.785 |            35.404 |                57.587 |
| lgbm_sc_s0 |    0.2  | ST       | WASO    | cqr_ffbs      |           0.818 |            41.858 |                62.436 |
| lgbm_sc_s0 |    0.2  | ST       | WASO    | norm_reg_ffbs |           0.817 |            43.17  |                64.948 |
| lgbm_sc_s0 |    0.2  | ST       | WASO    | scp_abs_bc    |           0.815 |            38.486 |                58.309 |


# S7. Leave-one-subject-out coverage with subject-level cluster-bootstrap 95% CIs

| stager     | cohort   | param   | method        |   n_nights |   coverage |   cov_lo95 |   cov_hi95 |   mean_width |
|:-----------|:---------|:--------|:--------------|-----------:|-----------:|-----------:|-----------:|-------------:|
| yasa       | HMC      | N1%     | ba_loa        |        151 |      0.921 |      0.874 |      0.96  |       25.634 |
| yasa       | HMC      | N1%     | cqr_ffbs      |        151 |      0.901 |      0.854 |      0.947 |       21.196 |
| yasa       | HMC      | N1%     | norm_reg_ffbs |        151 |      0.901 |      0.854 |      0.947 |       20.987 |
| yasa       | HMC      | N1%     | scp_abs       |        151 |      0.901 |      0.854 |      0.947 |       21.49  |
| yasa       | HMC      | N1%     | scp_abs_bc    |        151 |      0.901 |      0.848 |      0.947 |       23.173 |
| yasa       | HMC      | N2%     | ba_loa        |        151 |      0.934 |      0.894 |      0.974 |       33.15  |
| yasa       | HMC      | N2%     | cqr_ffbs      |        151 |      0.901 |      0.848 |      0.947 |       26.361 |
| yasa       | HMC      | N2%     | norm_reg_ffbs |        151 |      0.901 |      0.848 |      0.947 |       26.409 |
| yasa       | HMC      | N2%     | scp_abs       |        151 |      0.901 |      0.854 |      0.947 |       47.884 |
| yasa       | HMC      | N2%     | scp_abs_bc    |        151 |      0.901 |      0.854 |      0.947 |       29.575 |
| yasa       | HMC      | N3%     | ba_loa        |        151 |      0.907 |      0.854 |      0.954 |       24.364 |
| yasa       | HMC      | N3%     | cqr_ffbs      |        151 |      0.901 |      0.848 |      0.947 |       29.867 |
| yasa       | HMC      | N3%     | norm_reg_ffbs |        151 |      0.901 |      0.848 |      0.947 |       29.689 |
| yasa       | HMC      | N3%     | scp_abs       |        151 |      0.901 |      0.848 |      0.947 |       27.72  |
| yasa       | HMC      | N3%     | scp_abs_bc    |        151 |      0.894 |      0.841 |      0.94  |       23.571 |
| yasa       | HMC      | REM%    | ba_loa        |        151 |      0.907 |      0.861 |      0.954 |       18.24  |
| yasa       | HMC      | REM%    | cqr_ffbs      |        151 |      0.901 |      0.854 |      0.947 |       20.453 |
| yasa       | HMC      | REM%    | norm_reg_ffbs |        151 |      0.901 |      0.854 |      0.947 |       20.888 |
| yasa       | HMC      | REM%    | scp_abs       |        151 |      0.901 |      0.854 |      0.947 |       17.598 |
| yasa       | HMC      | REM%    | scp_abs_bc    |        151 |      0.901 |      0.854 |      0.947 |       17.413 |
| yasa       | HMC      | REML    | ba_loa        |        150 |      0.913 |      0.867 |      0.953 |      191.62  |
| yasa       | HMC      | REML    | cqr_ffbs      |        150 |      0.9   |      0.853 |      0.94  |      144.132 |
| yasa       | HMC      | REML    | norm_reg_ffbs |        150 |      0.9   |      0.847 |      0.947 |      177.533 |
| yasa       | HMC      | REML    | scp_abs       |        150 |      0.9   |      0.847 |      0.947 |      171.65  |
| yasa       | HMC      | REML    | scp_abs_bc    |        150 |      0.9   |      0.853 |      0.947 |      184.565 |
| yasa       | HMC      | SOL     | ba_loa        |        151 |      0.907 |      0.861 |      0.947 |       24.993 |
| yasa       | HMC      | SOL     | cqr_ffbs      |        151 |      0.934 |      0.894 |      0.974 |       19.024 |
| yasa       | HMC      | SOL     | norm_reg_ffbs |        151 |      0.901 |      0.854 |      0.947 |       20.134 |
| yasa       | HMC      | SOL     | scp_abs       |        151 |      0.901 |      0.854 |      0.947 |       29.695 |
| yasa       | HMC      | SOL     | scp_abs_bc    |        151 |      0.901 |      0.854 |      0.947 |       20.242 |
| yasa       | HMC      | TST     | ba_loa        |        151 |      0.934 |      0.894 |      0.974 |      135.967 |
| yasa       | HMC      | TST     | cqr_ffbs      |        151 |      0.901 |      0.854 |      0.94  |       83.313 |
| yasa       | HMC      | TST     | norm_reg_ffbs |        151 |      0.901 |      0.854 |      0.94  |       80.648 |
| yasa       | HMC      | TST     | scp_abs       |        151 |      0.901 |      0.854 |      0.94  |      150.801 |
| yasa       | HMC      | TST     | scp_abs_bc    |        151 |      0.901 |      0.854 |      0.947 |      100.529 |
| yasa       | HMC      | WASO    | ba_loa        |        151 |      0.934 |      0.894 |      0.974 |      105.99  |
| yasa       | HMC      | WASO    | cqr_ffbs      |        151 |      0.901 |      0.854 |      0.941 |       73.767 |
| yasa       | HMC      | WASO    | norm_reg_ffbs |        151 |      0.901 |      0.854 |      0.941 |       73.867 |
| yasa       | HMC      | WASO    | scp_abs       |        151 |      0.901 |      0.854 |      0.947 |      130.5   |
| yasa       | HMC      | WASO    | scp_abs_bc    |        151 |      0.901 |      0.854 |      0.947 |       82.505 |
| yasa       | SC       | N1%     | ba_loa        |        153 |      0.928 |      0.882 |      0.968 |       29.739 |
| yasa       | SC       | N1%     | cqr_ffbs      |        153 |      0.902 |      0.851 |      0.948 |       25.991 |
| yasa       | SC       | N1%     | norm_reg_ffbs |        153 |      0.902 |      0.854 |      0.948 |       26.135 |
| yasa       | SC       | N1%     | scp_abs       |        153 |      0.902 |      0.851 |      0.948 |       27.618 |
| yasa       | SC       | N1%     | scp_abs_bc    |        153 |      0.895 |      0.84  |      0.947 |       25.096 |
| yasa       | SC       | N2%     | ba_loa        |        153 |      0.908 |      0.859 |      0.954 |       39.187 |
| yasa       | SC       | N2%     | cqr_ffbs      |        153 |      0.902 |      0.85  |      0.948 |       32.284 |
| yasa       | SC       | N2%     | norm_reg_ffbs |        153 |      0.902 |      0.85  |      0.948 |       32.859 |
| yasa       | SC       | N2%     | scp_abs       |        153 |      0.902 |      0.851 |      0.947 |       41.74  |
| yasa       | SC       | N2%     | scp_abs_bc    |        153 |      0.902 |      0.852 |      0.947 |       35.973 |
| yasa       | SC       | N3%     | ba_loa        |        153 |      0.928 |      0.871 |      0.974 |       16.053 |
| yasa       | SC       | N3%     | cqr_ffbs      |        153 |      0.902 |      0.845 |      0.954 |       15.852 |
| yasa       | SC       | N3%     | norm_reg_ffbs |        153 |      0.902 |      0.845 |      0.948 |       15.369 |
| yasa       | SC       | N3%     | scp_abs       |        153 |      0.902 |      0.842 |      0.949 |       23.006 |
| yasa       | SC       | N3%     | scp_abs_bc    |        153 |      0.895 |      0.83  |      0.948 |       14.582 |
| yasa       | SC       | REM%    | ba_loa        |        153 |      0.941 |      0.89  |      0.981 |       22.554 |
| yasa       | SC       | REM%    | cqr_ffbs      |        153 |      0.895 |      0.837 |      0.948 |       24.389 |
| yasa       | SC       | REM%    | norm_reg_ffbs |        153 |      0.895 |      0.837 |      0.948 |       23.069 |
| yasa       | SC       | REM%    | scp_abs       |        153 |      0.902 |      0.84  |      0.954 |       18.311 |
| yasa       | SC       | REM%    | scp_abs_bc    |        153 |      0.902 |      0.841 |      0.954 |       18.246 |
| yasa       | SC       | REML    | ba_loa        |        153 |      0.869 |      0.816 |      0.922 |      134.423 |
| yasa       | SC       | REML    | cqr_ffbs      |        153 |      0.902 |      0.851 |      0.948 |      106.435 |
| yasa       | SC       | REML    | norm_reg_ffbs |        153 |      0.902 |      0.857 |      0.947 |       90.305 |
| yasa       | SC       | REML    | scp_abs       |        153 |      0.895 |      0.843 |      0.942 |      143.48  |
| yasa       | SC       | REML    | scp_abs_bc    |        153 |      0.895 |      0.849 |      0.941 |      141.6   |
| yasa       | SC       | SOL     | ba_loa        |        153 |      0.948 |      0.91  |      0.974 |       35.155 |
| yasa       | SC       | SOL     | cqr_ffbs      |        153 |      0.908 |      0.862 |      0.954 |       26.848 |
| yasa       | SC       | SOL     | norm_reg_ffbs |        153 |      0.902 |      0.855 |      0.948 |       26.365 |
| yasa       | SC       | SOL     | scp_abs       |        153 |      0.902 |      0.855 |      0.942 |       31.712 |
| yasa       | SC       | SOL     | scp_abs_bc    |        153 |      0.895 |      0.85  |      0.935 |       24.333 |
| yasa       | SC       | TST     | ba_loa        |        153 |      0.922 |      0.876 |      0.961 |      112.276 |
| yasa       | SC       | TST     | cqr_ffbs      |        153 |      0.902 |      0.845 |      0.954 |       79.823 |
| yasa       | SC       | TST     | norm_reg_ffbs |        153 |      0.902 |      0.845 |      0.954 |       78.622 |
| yasa       | SC       | TST     | scp_abs       |        153 |      0.895 |      0.843 |      0.942 |      124.569 |
| yasa       | SC       | TST     | scp_abs_bc    |        153 |      0.902 |      0.854 |      0.948 |      102.799 |
| yasa       | SC       | WASO    | ba_loa        |        153 |      0.928 |      0.887 |      0.967 |      117.12  |
| yasa       | SC       | WASO    | cqr_ffbs      |        153 |      0.902 |      0.856 |      0.947 |      198.483 |
| yasa       | SC       | WASO    | norm_reg_ffbs |        153 |      0.902 |      0.851 |      0.948 |      223.006 |
| yasa       | SC       | WASO    | scp_abs       |        153 |      0.902 |      0.854 |      0.948 |      151.686 |
| yasa       | SC       | WASO    | scp_abs_bc    |        153 |      0.895 |      0.842 |      0.942 |      108.737 |
| yasa       | ST       | N1%     | ba_loa        |         44 |      0.841 |      0.705 |      0.955 |       14.743 |
| yasa       | ST       | N1%     | cqr_ffbs      |         44 |      0.909 |      0.795 |      1     |       17.536 |
| yasa       | ST       | N1%     | norm_reg_ffbs |         44 |      0.909 |      0.795 |      1     |       16.85  |
| yasa       | ST       | N1%     | scp_abs       |         44 |      0.886 |      0.773 |      0.977 |       17.098 |
| yasa       | ST       | N1%     | scp_abs_bc    |         44 |      0.886 |      0.795 |      0.955 |       15.22  |
| yasa       | ST       | N2%     | ba_loa        |         44 |      0.886 |      0.75  |      0.977 |       31.739 |
| yasa       | ST       | N2%     | cqr_ffbs      |         44 |      0.909 |      0.795 |      1     |       31.585 |
| yasa       | ST       | N2%     | norm_reg_ffbs |         44 |      0.909 |      0.795 |      1     |       32.288 |
| yasa       | ST       | N2%     | scp_abs       |         44 |      0.909 |      0.795 |      1     |       34.746 |
| yasa       | ST       | N2%     | scp_abs_bc    |         44 |      0.909 |      0.795 |      1     |       32.98  |
| yasa       | ST       | N3%     | ba_loa        |         44 |      0.886 |      0.795 |      0.955 |       24.317 |
| yasa       | ST       | N3%     | cqr_ffbs      |         44 |      0.909 |      0.818 |      0.977 |       26.301 |
| yasa       | ST       | N3%     | norm_reg_ffbs |         44 |      0.909 |      0.818 |      0.977 |       25.778 |
| yasa       | ST       | N3%     | scp_abs       |         44 |      0.909 |      0.841 |      0.977 |       29.932 |
| yasa       | ST       | N3%     | scp_abs_bc    |         44 |      0.909 |      0.818 |      0.977 |       27.95  |
| yasa       | ST       | REM%    | ba_loa        |         44 |      0.886 |      0.773 |      0.977 |       17.631 |
| yasa       | ST       | REM%    | cqr_ffbs      |         44 |      0.886 |      0.773 |      0.977 |       22.903 |
| yasa       | ST       | REM%    | norm_reg_ffbs |         44 |      0.909 |      0.795 |      1     |       23.366 |
| yasa       | ST       | REM%    | scp_abs       |         44 |      0.909 |      0.795 |      1     |       20.636 |
| yasa       | ST       | REM%    | scp_abs_bc    |         44 |      0.886 |      0.773 |      0.977 |       20.606 |
| yasa       | ST       | REML    | ba_loa        |         44 |      0.841 |      0.727 |      0.932 |      125.937 |
| yasa       | ST       | REML    | cqr_ffbs      |         44 |      0.909 |      0.795 |      1     |      125.859 |
| yasa       | ST       | REML    | norm_reg_ffbs |         44 |      0.909 |      0.795 |      1     |      130.378 |
| yasa       | ST       | REML    | scp_abs       |         44 |      0.909 |      0.795 |      1     |      179.091 |
| yasa       | ST       | REML    | scp_abs_bc    |         44 |      0.909 |      0.795 |      1     |      168.551 |
| yasa       | ST       | SOL     | ba_loa        |         44 |      0.932 |      0.818 |      1     |       11.489 |
| yasa       | ST       | SOL     | cqr_ffbs      |         44 |      0.977 |      0.932 |      1     |       18.018 |
| yasa       | ST       | SOL     | norm_reg_ffbs |         44 |      0.909 |      0.795 |      1     |       19.491 |
| yasa       | ST       | SOL     | scp_abs       |         44 |      0.909 |      0.795 |      1     |       16.534 |
| yasa       | ST       | SOL     | scp_abs_bc    |         44 |      0.909 |      0.795 |      1     |       10.086 |
| yasa       | ST       | TST     | ba_loa        |         44 |      0.909 |      0.795 |      1     |       57.239 |
| yasa       | ST       | TST     | cqr_ffbs      |         44 |      0.886 |      0.773 |      0.977 |       36.599 |
| yasa       | ST       | TST     | norm_reg_ffbs |         44 |      0.886 |      0.773 |      0.977 |       36.211 |
| yasa       | ST       | TST     | scp_abs       |         44 |      0.909 |      0.795 |      1     |      103.545 |
| yasa       | ST       | TST     | scp_abs_bc    |         44 |      0.909 |      0.795 |      1     |       58.182 |
| yasa       | ST       | WASO    | ba_loa        |         44 |      0.932 |      0.818 |      1     |       38.813 |
| yasa       | ST       | WASO    | cqr_ffbs      |         44 |      0.909 |      0.818 |      0.977 |       49.588 |
| yasa       | ST       | WASO    | norm_reg_ffbs |         44 |      0.909 |      0.818 |      0.977 |       49.797 |
| yasa       | ST       | WASO    | scp_abs       |         44 |      0.886 |      0.75  |      1     |       64.375 |
| yasa       | ST       | WASO    | scp_abs_bc    |         44 |      0.886 |      0.75  |      1     |       29.284 |
| lgbm_sc_s0 | HMC      | N1%     | ba_loa        |        151 |      0.914 |      0.868 |      0.954 |       28.538 |
| lgbm_sc_s0 | HMC      | N1%     | cqr_ffbs      |        151 |      0.901 |      0.854 |      0.947 |       21.887 |
| lgbm_sc_s0 | HMC      | N1%     | norm_reg_ffbs |        151 |      0.901 |      0.854 |      0.947 |       22.239 |
| lgbm_sc_s0 | HMC      | N1%     | scp_abs       |        151 |      0.901 |      0.854 |      0.947 |       39.748 |
| lgbm_sc_s0 | HMC      | N1%     | scp_abs_bc    |        151 |      0.901 |      0.854 |      0.947 |       25.445 |
| lgbm_sc_s0 | HMC      | N2%     | ba_loa        |        151 |      0.887 |      0.841 |      0.934 |       38.256 |
| lgbm_sc_s0 | HMC      | N2%     | cqr_ffbs      |        151 |      0.901 |      0.854 |      0.947 |       34.881 |
| lgbm_sc_s0 | HMC      | N2%     | norm_reg_ffbs |        151 |      0.901 |      0.854 |      0.947 |       34.047 |
| lgbm_sc_s0 | HMC      | N2%     | scp_abs       |        151 |      0.901 |      0.854 |      0.947 |       41.105 |
| lgbm_sc_s0 | HMC      | N2%     | scp_abs_bc    |        151 |      0.894 |      0.848 |      0.94  |       39.772 |
| lgbm_sc_s0 | HMC      | N3%     | ba_loa        |        151 |      0.887 |      0.834 |      0.934 |       33.154 |
| lgbm_sc_s0 | HMC      | N3%     | cqr_ffbs      |        151 |      0.901 |      0.854 |      0.947 |       36.191 |
| lgbm_sc_s0 | HMC      | N3%     | norm_reg_ffbs |        151 |      0.901 |      0.854 |      0.947 |       35.659 |
| lgbm_sc_s0 | HMC      | N3%     | scp_abs       |        151 |      0.901 |      0.854 |      0.947 |       36.166 |
| lgbm_sc_s0 | HMC      | N3%     | scp_abs_bc    |        151 |      0.901 |      0.848 |      0.947 |       34.071 |
| lgbm_sc_s0 | HMC      | REM%    | ba_loa        |        151 |      0.914 |      0.868 |      0.954 |       18.637 |
| lgbm_sc_s0 | HMC      | REM%    | cqr_ffbs      |        151 |      0.901 |      0.854 |      0.947 |       21.439 |
| lgbm_sc_s0 | HMC      | REM%    | norm_reg_ffbs |        151 |      0.901 |      0.854 |      0.947 |       21.512 |
| lgbm_sc_s0 | HMC      | REM%    | scp_abs       |        151 |      0.901 |      0.854 |      0.941 |       21.311 |
| lgbm_sc_s0 | HMC      | REM%    | scp_abs_bc    |        151 |      0.894 |      0.841 |      0.94  |       17.766 |
| lgbm_sc_s0 | HMC      | REML    | ba_loa        |        150 |      0.913 |      0.86  |      0.953 |      192.244 |
| lgbm_sc_s0 | HMC      | REML    | cqr_ffbs      |        150 |      0.9   |      0.853 |      0.947 |      172.72  |
| lgbm_sc_s0 | HMC      | REML    | norm_reg_ffbs |        150 |      0.9   |      0.853 |      0.947 |      200.781 |
| lgbm_sc_s0 | HMC      | REML    | scp_abs       |        150 |      0.9   |      0.847 |      0.947 |      176.363 |
| lgbm_sc_s0 | HMC      | REML    | scp_abs_bc    |        150 |      0.9   |      0.847 |      0.94  |      185.725 |
| lgbm_sc_s0 | HMC      | SOL     | ba_loa        |        151 |      0.94  |      0.907 |      0.974 |       31.061 |
| lgbm_sc_s0 | HMC      | SOL     | cqr_ffbs      |        151 |      0.901 |      0.854 |      0.947 |       21.964 |
| lgbm_sc_s0 | HMC      | SOL     | norm_reg_ffbs |        151 |      0.901 |      0.854 |      0.947 |       24.668 |
| lgbm_sc_s0 | HMC      | SOL     | scp_abs       |        151 |      0.901 |      0.854 |      0.94  |       24.023 |
| lgbm_sc_s0 | HMC      | SOL     | scp_abs_bc    |        151 |      0.901 |      0.854 |      0.941 |       21.209 |
| lgbm_sc_s0 | HMC      | TST     | ba_loa        |        151 |      0.894 |      0.848 |      0.94  |      157.546 |
| lgbm_sc_s0 | HMC      | TST     | cqr_ffbs      |        151 |      0.907 |      0.861 |      0.947 |      117.146 |
| lgbm_sc_s0 | HMC      | TST     | norm_reg_ffbs |        151 |      0.901 |      0.848 |      0.947 |      108.567 |
| lgbm_sc_s0 | HMC      | TST     | scp_abs       |        151 |      0.901 |      0.854 |      0.947 |      194.901 |
| lgbm_sc_s0 | HMC      | TST     | scp_abs_bc    |        151 |      0.901 |      0.854 |      0.947 |      165.477 |
| lgbm_sc_s0 | HMC      | WASO    | ba_loa        |        151 |      0.914 |      0.868 |      0.954 |      113.616 |
| lgbm_sc_s0 | HMC      | WASO    | cqr_ffbs      |        151 |      0.901 |      0.854 |      0.941 |       94.652 |
| lgbm_sc_s0 | HMC      | WASO    | norm_reg_ffbs |        151 |      0.901 |      0.854 |      0.941 |       95.274 |
| lgbm_sc_s0 | HMC      | WASO    | scp_abs       |        151 |      0.907 |      0.861 |      0.954 |      160.646 |
| lgbm_sc_s0 | HMC      | WASO    | scp_abs_bc    |        151 |      0.901 |      0.854 |      0.947 |      109.581 |
| lgbm_sc_s0 | SC       | N1%     | ba_loa        |        153 |      0.895 |      0.845 |      0.941 |       26.984 |
| lgbm_sc_s0 | SC       | N1%     | cqr_ffbs      |        153 |      0.902 |      0.849 |      0.954 |       25.991 |
| lgbm_sc_s0 | SC       | N1%     | norm_reg_ffbs |        153 |      0.902 |      0.849 |      0.954 |       25.49  |
| lgbm_sc_s0 | SC       | N1%     | scp_abs       |        153 |      0.902 |      0.857 |      0.942 |       33.338 |
| lgbm_sc_s0 | SC       | N1%     | scp_abs_bc    |        153 |      0.902 |      0.853 |      0.947 |       28.026 |
| lgbm_sc_s0 | SC       | N2%     | ba_loa        |        153 |      0.902 |      0.85  |      0.948 |       30.548 |
| lgbm_sc_s0 | SC       | N2%     | cqr_ffbs      |        153 |      0.902 |      0.844 |      0.949 |       30.017 |
| lgbm_sc_s0 | SC       | N2%     | norm_reg_ffbs |        153 |      0.902 |      0.844 |      0.949 |       30.502 |
| lgbm_sc_s0 | SC       | N2%     | scp_abs       |        153 |      0.902 |      0.854 |      0.948 |       33.332 |
| lgbm_sc_s0 | SC       | N2%     | scp_abs_bc    |        153 |      0.889 |      0.832 |      0.94  |       29.91  |
| lgbm_sc_s0 | SC       | N3%     | ba_loa        |        153 |      0.889 |      0.826 |      0.941 |       11.616 |
| lgbm_sc_s0 | SC       | N3%     | cqr_ffbs      |        153 |      0.902 |      0.848 |      0.948 |       11.234 |
| lgbm_sc_s0 | SC       | N3%     | norm_reg_ffbs |        153 |      0.902 |      0.848 |      0.948 |       11.14  |
| lgbm_sc_s0 | SC       | N3%     | scp_abs       |        153 |      0.902 |      0.843 |      0.954 |       12.832 |
| lgbm_sc_s0 | SC       | N3%     | scp_abs_bc    |        153 |      0.902 |      0.844 |      0.948 |       12.295 |
| lgbm_sc_s0 | SC       | REM%    | ba_loa        |        153 |      0.941 |      0.893 |      0.981 |       19.301 |
| lgbm_sc_s0 | SC       | REM%    | cqr_ffbs      |        153 |      0.895 |      0.835 |      0.947 |       22.08  |
| lgbm_sc_s0 | SC       | REM%    | norm_reg_ffbs |        153 |      0.902 |      0.849 |      0.948 |       22.459 |
| lgbm_sc_s0 | SC       | REM%    | scp_abs       |        153 |      0.902 |      0.84  |      0.949 |       15.624 |
| lgbm_sc_s0 | SC       | REM%    | scp_abs_bc    |        153 |      0.895 |      0.831 |      0.948 |       15.612 |
| lgbm_sc_s0 | SC       | REML    | ba_loa        |        153 |      0.915 |      0.864 |      0.955 |      119.542 |
| lgbm_sc_s0 | SC       | REML    | cqr_ffbs      |        153 |      0.915 |      0.868 |      0.96  |       95.576 |
| lgbm_sc_s0 | SC       | REML    | norm_reg_ffbs |        153 |      0.902 |      0.857 |      0.942 |       76.71  |
| lgbm_sc_s0 | SC       | REML    | scp_abs       |        153 |      0.902 |      0.848 |      0.948 |      121.824 |
| lgbm_sc_s0 | SC       | REML    | scp_abs_bc    |        153 |      0.902 |      0.848 |      0.948 |      105.725 |
| lgbm_sc_s0 | SC       | SOL     | ba_loa        |        153 |      0.961 |      0.928 |      0.987 |       35.758 |
| lgbm_sc_s0 | SC       | SOL     | cqr_ffbs      |        153 |      0.935 |      0.895 |      0.968 |       24.197 |
| lgbm_sc_s0 | SC       | SOL     | norm_reg_ffbs |        153 |      0.902 |      0.851 |      0.948 |       22.064 |
| lgbm_sc_s0 | SC       | SOL     | scp_abs       |        153 |      0.902 |      0.849 |      0.948 |       20.382 |
| lgbm_sc_s0 | SC       | SOL     | scp_abs_bc    |        153 |      0.895 |      0.834 |      0.941 |       24.432 |
| lgbm_sc_s0 | SC       | TST     | ba_loa        |        153 |      0.908 |      0.858 |      0.954 |       88.696 |
| lgbm_sc_s0 | SC       | TST     | cqr_ffbs      |        153 |      0.902 |      0.85  |      0.948 |       67.67  |
| lgbm_sc_s0 | SC       | TST     | norm_reg_ffbs |        153 |      0.902 |      0.851 |      0.948 |       63.72  |
| lgbm_sc_s0 | SC       | TST     | scp_abs       |        153 |      0.902 |      0.852 |      0.947 |       90.719 |
| lgbm_sc_s0 | SC       | TST     | scp_abs_bc    |        153 |      0.902 |      0.85  |      0.948 |       83.663 |
| lgbm_sc_s0 | SC       | WASO    | ba_loa        |        153 |      0.948 |      0.91  |      0.981 |      104.063 |
| lgbm_sc_s0 | SC       | WASO    | cqr_ffbs      |        153 |      0.908 |      0.862 |      0.954 |      152.689 |
| lgbm_sc_s0 | SC       | WASO    | norm_reg_ffbs |        153 |      0.902 |      0.85  |      0.948 |      177.783 |
| lgbm_sc_s0 | SC       | WASO    | scp_abs       |        153 |      0.902 |      0.855 |      0.947 |       76.765 |
| lgbm_sc_s0 | SC       | WASO    | scp_abs_bc    |        153 |      0.895 |      0.848 |      0.941 |       72.121 |
| lgbm_sc_s0 | ST       | N1%     | ba_loa        |         44 |      0.932 |      0.818 |      1     |       15.376 |
| lgbm_sc_s0 | ST       | N1%     | cqr_ffbs      |         44 |      0.909 |      0.795 |      1     |       16.225 |
| lgbm_sc_s0 | ST       | N1%     | norm_reg_ffbs |         44 |      0.909 |      0.795 |      1     |       15.722 |
| lgbm_sc_s0 | ST       | N1%     | scp_abs       |         44 |      0.886 |      0.75  |      1     |       19.948 |
| lgbm_sc_s0 | ST       | N1%     | scp_abs_bc    |         44 |      0.841 |      0.705 |      0.955 |       13.631 |
| lgbm_sc_s0 | ST       | N2%     | ba_loa        |         44 |      0.864 |      0.75  |      0.955 |       31.651 |
| lgbm_sc_s0 | ST       | N2%     | cqr_ffbs      |         44 |      0.909 |      0.818 |      0.977 |       30.052 |
| lgbm_sc_s0 | ST       | N2%     | norm_reg_ffbs |         44 |      0.909 |      0.818 |      0.977 |       30.862 |
| lgbm_sc_s0 | ST       | N2%     | scp_abs       |         44 |      0.909 |      0.818 |      0.977 |       35.506 |
| lgbm_sc_s0 | ST       | N2%     | scp_abs_bc    |         44 |      0.909 |      0.795 |      1     |       36.336 |
| lgbm_sc_s0 | ST       | N3%     | ba_loa        |         44 |      0.886 |      0.773 |      0.977 |       23.448 |
| lgbm_sc_s0 | ST       | N3%     | cqr_ffbs      |         44 |      0.886 |      0.773 |      0.977 |       26.823 |
| lgbm_sc_s0 | ST       | N3%     | norm_reg_ffbs |         44 |      0.886 |      0.773 |      0.977 |       26.39  |
| lgbm_sc_s0 | ST       | N3%     | scp_abs       |         44 |      0.909 |      0.795 |      1     |       25.841 |
| lgbm_sc_s0 | ST       | N3%     | scp_abs_bc    |         44 |      0.886 |      0.773 |      0.977 |       26.669 |
| lgbm_sc_s0 | ST       | REM%    | ba_loa        |         44 |      0.864 |      0.75  |      0.955 |       17.703 |
| lgbm_sc_s0 | ST       | REM%    | cqr_ffbs      |         44 |      0.886 |      0.773 |      0.977 |       23.389 |
| lgbm_sc_s0 | ST       | REM%    | norm_reg_ffbs |         44 |      0.909 |      0.818 |      0.977 |       22.631 |
| lgbm_sc_s0 | ST       | REM%    | scp_abs       |         44 |      0.909 |      0.795 |      1     |       24.342 |
| lgbm_sc_s0 | ST       | REM%    | scp_abs_bc    |         44 |      0.909 |      0.795 |      1     |       19.613 |
| lgbm_sc_s0 | ST       | REML    | ba_loa        |         44 |      0.841 |      0.727 |      0.955 |      144.83  |
| lgbm_sc_s0 | ST       | REML    | cqr_ffbs      |         44 |      0.932 |      0.841 |      1     |      133.549 |
| lgbm_sc_s0 | ST       | REML    | norm_reg_ffbs |         44 |      0.886 |      0.727 |      1     |      125.28  |
| lgbm_sc_s0 | ST       | REML    | scp_abs       |         44 |      0.909 |      0.818 |      0.977 |      184.966 |
| lgbm_sc_s0 | ST       | REML    | scp_abs_bc    |         44 |      0.886 |      0.795 |      0.955 |      170.283 |
| lgbm_sc_s0 | ST       | SOL     | ba_loa        |         44 |      0.955 |      0.864 |      1     |       22.766 |
| lgbm_sc_s0 | ST       | SOL     | cqr_ffbs      |         44 |      0.955 |      0.864 |      1     |       16.64  |
| lgbm_sc_s0 | ST       | SOL     | norm_reg_ffbs |         44 |      0.909 |      0.795 |      1     |       22.596 |
| lgbm_sc_s0 | ST       | SOL     | scp_abs       |         44 |      0.909 |      0.795 |      1     |       13.352 |
| lgbm_sc_s0 | ST       | SOL     | scp_abs_bc    |         44 |      0.909 |      0.795 |      1     |       15.17  |
| lgbm_sc_s0 | ST       | TST     | ba_loa        |         44 |      0.841 |      0.705 |      0.955 |       61.162 |
| lgbm_sc_s0 | ST       | TST     | cqr_ffbs      |         44 |      0.909 |      0.773 |      1     |       40.847 |
| lgbm_sc_s0 | ST       | TST     | norm_reg_ffbs |         44 |      0.909 |      0.773 |      1     |       38.505 |
| lgbm_sc_s0 | ST       | TST     | scp_abs       |         44 |      0.909 |      0.795 |      1     |       66.636 |
| lgbm_sc_s0 | ST       | TST     | scp_abs_bc    |         44 |      0.886 |      0.773 |      0.977 |       65.114 |
| lgbm_sc_s0 | ST       | WASO    | ba_loa        |         44 |      0.886 |      0.773 |      0.977 |       44.505 |
| lgbm_sc_s0 | ST       | WASO    | cqr_ffbs      |         44 |      0.909 |      0.795 |      1     |       48.666 |
| lgbm_sc_s0 | ST       | WASO    | norm_reg_ffbs |         44 |      0.909 |      0.795 |      1     |       51.166 |
| lgbm_sc_s0 | ST       | WASO    | scp_abs       |         44 |      0.909 |      0.795 |      1     |       61.727 |
| lgbm_sc_s0 | ST       | WASO    | scp_abs_bc    |         44 |      0.886 |      0.773 |      0.977 |       50.337 |


# S8. Point estimates, in-domain LightGBM stager

| Stager                  | Parameter   | Cohort   |   Plug-in bias |   Plug-in MAE |   Plug-in ICC |   Calibrated plug-in bias |   Calibrated plug-in MAE |   Calibrated plug-in ICC |   Posterior mean bias |   Posterior mean MAE |   Posterior mean ICC |   p (MAE, posterior mean vs plug-in) |   p (MAE, posterior mean vs calibrated) |
|:------------------------|:------------|:---------|---------------:|--------------:|--------------:|--------------------------:|-------------------------:|-------------------------:|----------------------:|---------------------:|---------------------:|-------------------------------------:|----------------------------------------:|
| LightGBM-SC (in-domain) | TST         | SC       |           10.1 |          19.5 |          0.86 |                      -2.9 |                     17   |                     0.88 |                  -1.6 |                 16.2 |                 0.9  |                                 0.01 |                                    0.32 |
| LightGBM-SC (in-domain) | TST         | ST       |          -12.4 |          18.3 |          0.88 |                      -0.1 |                     13.1 |                     0.93 |                  -3   |                 10.2 |                 0.95 |                                 0    |                                    0.06 |
| LightGBM-SC (in-domain) | TST         | HMC      |          -37.1 |          47.6 |          0.75 |                      -8.6 |                     30   |                     0.86 |                  -2.1 |                 25.2 |                 0.89 |                                 0    |                                    0    |
| LightGBM-SC (in-domain) | SOL         | SC       |           -3.3 |           5.9 |          0.81 |                      -1   |                      5.6 |                     0.84 |                  -2.5 |                  7.2 |                 0.64 |                                 0.49 |                                    0.19 |
| LightGBM-SC (in-domain) | SOL         | ST       |           -1.5 |           3   |          0.64 |                      -2   |                      3.2 |                     0.62 |                  -4.6 |                  5.6 |                 0.28 |                                 0.02 |                                    0.04 |
| LightGBM-SC (in-domain) | SOL         | HMC      |            2.2 |           6.2 |          0.74 |                      -0.5 |                      5.1 |                     0.78 |                  -5.2 |                  7.9 |                 0.13 |                                 0.45 |                                    0    |
| LightGBM-SC (in-domain) | WASO        | SC       |            3.4 |          20.1 |          0.7  |                      11.9 |                     20   |                     0.72 |                  56.9 |                 58.1 |                 0.33 |                                 0    |                                    0    |
| LightGBM-SC (in-domain) | WASO        | ST       |           13   |          17.2 |          0.7  |                       3.9 |                     13   |                     0.73 |                  12.8 |                 15.7 |                 0.74 |                                 0.19 |                                    0.39 |
| LightGBM-SC (in-domain) | WASO        | HMC      |           34.8 |          42   |          0.55 |                      10.8 |                     25.8 |                     0.73 |                   9.9 |                 23.7 |                 0.77 |                                 0    |                                    0.01 |
| LightGBM-SC (in-domain) | REML        | SC       |          -11.2 |          18.2 |          0.66 |                     -13.2 |                     22.8 |                     0.55 |                  -4.8 |                 21.6 |                 0.67 |                                 0.08 |                                    0.41 |
| LightGBM-SC (in-domain) | REML        | ST       |            7.5 |          25   |          0.59 |                      -9.2 |                     35.7 |                     0.4  |                   1.3 |                 30   |                 0.47 |                                 0.35 |                                    0.5  |
| LightGBM-SC (in-domain) | REML        | HMC      |          -20.7 |          36.3 |          0.61 |                     -40.5 |                     52   |                     0.26 |                 -48.9 |                 56.8 |                 0.15 |                                 0    |                                    0.04 |
| LightGBM-SC (in-domain) | N1%         | SC       |            3.8 |           7.1 |          0.49 |                      -4.7 |                      7   |                     0.32 |                  -5.6 |                  6.9 |                 0.31 |                                 0.66 |                                    0.57 |
| LightGBM-SC (in-domain) | N1%         | ST       |            3.3 |           4.6 |          0.6  |                      -3   |                      3.9 |                     0.59 |                  -3   |                  3.7 |                 0.43 |                                 0.85 |                                    0.44 |
| LightGBM-SC (in-domain) | N1%         | HMC      |            8.2 |          10.4 |          0.27 |                      -5.9 |                      7.6 |                     0.2  |                  -3.5 |                  5.5 |                 0.2  |                                 0    |                                    0    |
| LightGBM-SC (in-domain) | N2%         | SC       |           -4.2 |           7.8 |          0.51 |                       4.7 |                      7.7 |                     0.47 |                   0.9 |                  6.6 |                 0.58 |                                 0    |                                    0.02 |
| LightGBM-SC (in-domain) | N2%         | ST       |           -2.8 |           8.1 |          0.38 |                       3   |                      8.5 |                     0.36 |                  -1.3 |                  7.4 |                 0.37 |                                 0.34 |                                    0.23 |
| LightGBM-SC (in-domain) | N2%         | HMC      |            5.2 |          10.2 |          0.21 |                       6.8 |                     10   |                     0.37 |                  -4.6 |                  8   |                 0.4  |                                 0.01 |                                    0.01 |
| LightGBM-SC (in-domain) | N3%         | SC       |            0.5 |           2.9 |          0.9  |                      -0.4 |                      2.7 |                     0.91 |                   0.5 |                  3.1 |                 0.9  |                                 0.24 |                                    0    |
| LightGBM-SC (in-domain) | N3%         | ST       |            2.1 |           5.6 |          0.6  |                       0.1 |                      5.7 |                     0.61 |                   1   |                  5.8 |                 0.58 |                                 0.57 |                                    0.7  |
| LightGBM-SC (in-domain) | N3%         | HMC      |          -10.8 |          12.5 |          0.24 |                      -0.9 |                      8.8 |                     0.36 |                   3.8 |                  8.9 |                 0.37 |                                 0    |                                    0.81 |
| LightGBM-SC (in-domain) | REM%        | SC       |           -0.2 |           3.5 |          0.56 |                       0.4 |                      3.6 |                     0.55 |                   4.3 |                  5.8 |                 0.43 |                                 0    |                                    0    |
| LightGBM-SC (in-domain) | REM%        | ST       |           -2.6 |           4.1 |          0.47 |                      -0.1 |                      4.1 |                     0.46 |                   3.3 |                  5.8 |                 0.31 |                                 0.11 |                                    0.01 |
| LightGBM-SC (in-domain) | REM%        | HMC      |           -2.6 |           4.6 |          0.58 |                       0   |                      3.9 |                     0.63 |                   4.3 |                  5.8 |                 0.45 |                                 0.01 |                                    0    |


# S9. Coverage by subgroup (leave-one-subject-out)

| stager     | cohort   | method        | level      |   coverage |   count | factor       |
|:-----------|:---------|:--------------|:-----------|-----------:|--------:|:-------------|
| yasa       | HMC      | ba_loa        | Q1 (worst) |      0.799 |     304 | acc_quartile |
| yasa       | HMC      | ba_loa        | Q2         |      0.951 |     304 | acc_quartile |
| yasa       | HMC      | ba_loa        | Q3         |      0.953 |     296 | acc_quartile |
| yasa       | HMC      | ba_loa        | Q4 (best)  |      0.977 |     303 | acc_quartile |
| yasa       | HMC      | norm_reg_ffbs | Q1 (worst) |      0.812 |     304 | acc_quartile |
| yasa       | HMC      | norm_reg_ffbs | Q2         |      0.918 |     304 | acc_quartile |
| yasa       | HMC      | norm_reg_ffbs | Q3         |      0.939 |     296 | acc_quartile |
| yasa       | HMC      | norm_reg_ffbs | Q4 (best)  |      0.934 |     303 | acc_quartile |
| yasa       | HMC      | scp_abs       | Q1 (worst) |      0.75  |     304 | acc_quartile |
| yasa       | HMC      | scp_abs       | Q2         |      0.931 |     304 | acc_quartile |
| yasa       | HMC      | scp_abs       | Q3         |      0.956 |     296 | acc_quartile |
| yasa       | HMC      | scp_abs       | Q4 (best)  |      0.967 |     303 | acc_quartile |
| yasa       | HMC      | scp_abs_bc    | Q1 (worst) |      0.757 |     304 | acc_quartile |
| yasa       | HMC      | scp_abs_bc    | Q2         |      0.941 |     304 | acc_quartile |
| yasa       | HMC      | scp_abs_bc    | Q3         |      0.943 |     296 | acc_quartile |
| yasa       | HMC      | scp_abs_bc    | Q4 (best)  |      0.96  |     303 | acc_quartile |
| yasa       | SC       | ba_loa        | Q1 (worst) |      0.828 |     320 | acc_quartile |
| yasa       | SC       | ba_loa        | Q2         |      0.932 |     296 | acc_quartile |
| yasa       | SC       | ba_loa        | Q3         |      0.957 |     304 | acc_quartile |
| yasa       | SC       | ba_loa        | Q4 (best)  |      0.974 |     304 | acc_quartile |
| yasa       | SC       | norm_reg_ffbs | Q1 (worst) |      0.809 |     320 | acc_quartile |
| yasa       | SC       | norm_reg_ffbs | Q2         |      0.912 |     296 | acc_quartile |
| yasa       | SC       | norm_reg_ffbs | Q3         |      0.954 |     304 | acc_quartile |
| yasa       | SC       | norm_reg_ffbs | Q4 (best)  |      0.934 |     304 | acc_quartile |
| yasa       | SC       | scp_abs       | Q1 (worst) |      0.772 |     320 | acc_quartile |
| yasa       | SC       | scp_abs       | Q2         |      0.905 |     296 | acc_quartile |
| yasa       | SC       | scp_abs       | Q3         |      0.961 |     304 | acc_quartile |
| yasa       | SC       | scp_abs       | Q4 (best)  |      0.97  |     304 | acc_quartile |
| yasa       | SC       | scp_abs_bc    | Q1 (worst) |      0.788 |     320 | acc_quartile |
| yasa       | SC       | scp_abs_bc    | Q2         |      0.899 |     296 | acc_quartile |
| yasa       | SC       | scp_abs_bc    | Q3         |      0.951 |     304 | acc_quartile |
| yasa       | SC       | scp_abs_bc    | Q4 (best)  |      0.961 |     304 | acc_quartile |
| yasa       | ST       | ba_loa        | Q1 (worst) |      0.773 |      88 | acc_quartile |
| yasa       | ST       | ba_loa        | Q2         |      0.864 |      88 | acc_quartile |
| yasa       | ST       | ba_loa        | Q3         |      0.943 |      88 | acc_quartile |
| yasa       | ST       | ba_loa        | Q4 (best)  |      0.977 |      88 | acc_quartile |
| yasa       | ST       | norm_reg_ffbs | Q1 (worst) |      0.83  |      88 | acc_quartile |
| yasa       | ST       | norm_reg_ffbs | Q2         |      0.92  |      88 | acc_quartile |
| yasa       | ST       | norm_reg_ffbs | Q3         |      0.932 |      88 | acc_quartile |
| yasa       | ST       | norm_reg_ffbs | Q4 (best)  |      0.943 |      88 | acc_quartile |
| yasa       | ST       | scp_abs       | Q1 (worst) |      0.761 |      88 | acc_quartile |
| yasa       | ST       | scp_abs       | Q2         |      0.909 |      88 | acc_quartile |
| yasa       | ST       | scp_abs       | Q3         |      0.955 |      88 | acc_quartile |
| yasa       | ST       | scp_abs       | Q4 (best)  |      0.989 |      88 | acc_quartile |
| yasa       | ST       | scp_abs_bc    | Q1 (worst) |      0.784 |      88 | acc_quartile |
| yasa       | ST       | scp_abs_bc    | Q2         |      0.864 |      88 | acc_quartile |
| yasa       | ST       | scp_abs_bc    | Q3         |      0.966 |      88 | acc_quartile |
| yasa       | ST       | scp_abs_bc    | Q4 (best)  |      0.989 |      88 | acc_quartile |
| yasa       | SC       | ba_loa        | <40        |      0.942 |     312 | age_group    |
| yasa       | SC       | ba_loa        | 40-59      |      0.948 |     344 | age_group    |
| yasa       | SC       | ba_loa        | >=60       |      0.894 |     568 | age_group    |
| yasa       | SC       | norm_reg_ffbs | <40        |      0.923 |     312 | age_group    |
| yasa       | SC       | norm_reg_ffbs | 40-59      |      0.93  |     344 | age_group    |
| yasa       | SC       | norm_reg_ffbs | >=60       |      0.871 |     568 | age_group    |
| yasa       | SC       | scp_abs       | <40        |      0.942 |     312 | age_group    |
| yasa       | SC       | scp_abs       | 40-59      |      0.922 |     344 | age_group    |
| yasa       | SC       | scp_abs       | >=60       |      0.864 |     568 | age_group    |
| yasa       | SC       | scp_abs_bc    | <40        |      0.923 |     312 | age_group    |
| yasa       | SC       | scp_abs_bc    | 40-59      |      0.942 |     344 | age_group    |
| yasa       | SC       | scp_abs_bc    | >=60       |      0.857 |     568 | age_group    |
| yasa       | ST       | ba_loa        | <40        |      0.896 |     192 | age_group    |
| yasa       | ST       | ba_loa        | 40-59      |      0.875 |     112 | age_group    |
| yasa       | ST       | ba_loa        | >=60       |      0.896 |      48 | age_group    |
| yasa       | ST       | norm_reg_ffbs | <40        |      0.932 |     192 | age_group    |
| yasa       | ST       | norm_reg_ffbs | 40-59      |      0.866 |     112 | age_group    |
| yasa       | ST       | norm_reg_ffbs | >=60       |      0.896 |      48 | age_group    |
| yasa       | ST       | scp_abs       | <40        |      0.927 |     192 | age_group    |
| yasa       | ST       | scp_abs       | 40-59      |      0.866 |     112 | age_group    |
| yasa       | ST       | scp_abs       | >=60       |      0.896 |      48 | age_group    |
| yasa       | ST       | scp_abs_bc    | <40        |      0.906 |     192 | age_group    |
| yasa       | ST       | scp_abs_bc    | 40-59      |      0.893 |     112 | age_group    |
| yasa       | ST       | scp_abs_bc    | >=60       |      0.896 |      48 | age_group    |
| yasa       | SC       | ba_loa        | F          |      0.933 |     656 | sex          |
| yasa       | SC       | ba_loa        | M          |      0.908 |     568 | sex          |
| yasa       | SC       | norm_reg_ffbs | F          |      0.907 |     656 | sex          |
| yasa       | SC       | norm_reg_ffbs | M          |      0.894 |     568 | sex          |
| yasa       | SC       | scp_abs       | F          |      0.905 |     656 | sex          |
| yasa       | SC       | scp_abs       | M          |      0.894 |     568 | sex          |
| yasa       | SC       | scp_abs_bc    | F          |      0.916 |     656 | sex          |
| yasa       | SC       | scp_abs_bc    | M          |      0.877 |     568 | sex          |
| yasa       | ST       | ba_loa        | F          |      0.879 |     240 | sex          |
| yasa       | ST       | ba_loa        | M          |      0.911 |     112 | sex          |
| yasa       | ST       | norm_reg_ffbs | F          |      0.896 |     240 | sex          |
| yasa       | ST       | norm_reg_ffbs | M          |      0.929 |     112 | sex          |
| yasa       | ST       | scp_abs       | F          |      0.896 |     240 | sex          |
| yasa       | ST       | scp_abs       | M          |      0.92  |     112 | sex          |
| yasa       | ST       | scp_abs_bc    | F          |      0.896 |     240 | sex          |
| yasa       | ST       | scp_abs_bc    | M          |      0.911 |     112 | sex          |
| yasa       | ST       | ba_loa        | placebo    |      0.886 |     176 | condition    |
| yasa       | ST       | ba_loa        | temazepam  |      0.892 |     176 | condition    |
| yasa       | ST       | norm_reg_ffbs | placebo    |      0.892 |     176 | condition    |
| yasa       | ST       | norm_reg_ffbs | temazepam  |      0.92  |     176 | condition    |
| yasa       | ST       | scp_abs       | placebo    |      0.903 |     176 | condition    |
| yasa       | ST       | scp_abs       | temazepam  |      0.903 |     176 | condition    |
| yasa       | ST       | scp_abs_bc    | placebo    |      0.892 |     176 | condition    |
| yasa       | ST       | scp_abs_bc    | temazepam  |      0.909 |     176 | condition    |
| lgbm_sc_s0 | HMC      | ba_loa        | Q1 (worst) |      0.816 |     304 | acc_quartile |
| lgbm_sc_s0 | HMC      | ba_loa        | Q2         |      0.911 |     304 | acc_quartile |
| lgbm_sc_s0 | HMC      | ba_loa        | Q3         |      0.925 |     295 | acc_quartile |
| lgbm_sc_s0 | HMC      | ba_loa        | Q4 (best)  |      0.98  |     304 | acc_quartile |
| lgbm_sc_s0 | HMC      | norm_reg_ffbs | Q1 (worst) |      0.836 |     304 | acc_quartile |
| lgbm_sc_s0 | HMC      | norm_reg_ffbs | Q2         |      0.921 |     304 | acc_quartile |
| lgbm_sc_s0 | HMC      | norm_reg_ffbs | Q3         |      0.905 |     295 | acc_quartile |
| lgbm_sc_s0 | HMC      | norm_reg_ffbs | Q4 (best)  |      0.941 |     304 | acc_quartile |
| lgbm_sc_s0 | HMC      | scp_abs       | Q1 (worst) |      0.786 |     304 | acc_quartile |
| lgbm_sc_s0 | HMC      | scp_abs       | Q2         |      0.898 |     304 | acc_quartile |
| lgbm_sc_s0 | HMC      | scp_abs       | Q3         |      0.946 |     295 | acc_quartile |
| lgbm_sc_s0 | HMC      | scp_abs       | Q4 (best)  |      0.977 |     304 | acc_quartile |
| lgbm_sc_s0 | HMC      | scp_abs_bc    | Q1 (worst) |      0.799 |     304 | acc_quartile |
| lgbm_sc_s0 | HMC      | scp_abs_bc    | Q2         |      0.901 |     304 | acc_quartile |
| lgbm_sc_s0 | HMC      | scp_abs_bc    | Q3         |      0.915 |     295 | acc_quartile |
| lgbm_sc_s0 | HMC      | scp_abs_bc    | Q4 (best)  |      0.98  |     304 | acc_quartile |
| lgbm_sc_s0 | SC       | ba_loa        | Q1 (worst) |      0.798 |     312 | acc_quartile |
| lgbm_sc_s0 | SC       | ba_loa        | Q2         |      0.931 |     304 | acc_quartile |
| lgbm_sc_s0 | SC       | ba_loa        | Q3         |      0.974 |     304 | acc_quartile |
| lgbm_sc_s0 | SC       | ba_loa        | Q4 (best)  |      0.98  |     304 | acc_quartile |
| lgbm_sc_s0 | SC       | norm_reg_ffbs | Q1 (worst) |      0.83  |     312 | acc_quartile |
| lgbm_sc_s0 | SC       | norm_reg_ffbs | Q2         |      0.891 |     304 | acc_quartile |
| lgbm_sc_s0 | SC       | norm_reg_ffbs | Q3         |      0.931 |     304 | acc_quartile |
| lgbm_sc_s0 | SC       | norm_reg_ffbs | Q4 (best)  |      0.957 |     304 | acc_quartile |
| lgbm_sc_s0 | SC       | scp_abs       | Q1 (worst) |      0.779 |     312 | acc_quartile |
| lgbm_sc_s0 | SC       | scp_abs       | Q2         |      0.898 |     304 | acc_quartile |
| lgbm_sc_s0 | SC       | scp_abs       | Q3         |      0.957 |     304 | acc_quartile |
| lgbm_sc_s0 | SC       | scp_abs       | Q4 (best)  |      0.977 |     304 | acc_quartile |
| lgbm_sc_s0 | SC       | scp_abs_bc    | Q1 (worst) |      0.756 |     312 | acc_quartile |
| lgbm_sc_s0 | SC       | scp_abs_bc    | Q2         |      0.908 |     304 | acc_quartile |
| lgbm_sc_s0 | SC       | scp_abs_bc    | Q3         |      0.951 |     304 | acc_quartile |
| lgbm_sc_s0 | SC       | scp_abs_bc    | Q4 (best)  |      0.98  |     304 | acc_quartile |
| lgbm_sc_s0 | ST       | ba_loa        | Q1 (worst) |      0.75  |      88 | acc_quartile |
| lgbm_sc_s0 | ST       | ba_loa        | Q2         |      0.909 |      88 | acc_quartile |
| lgbm_sc_s0 | ST       | ba_loa        | Q3         |      0.909 |      88 | acc_quartile |
| lgbm_sc_s0 | ST       | ba_loa        | Q4 (best)  |      0.966 |      88 | acc_quartile |
| lgbm_sc_s0 | ST       | norm_reg_ffbs | Q1 (worst) |      0.852 |      88 | acc_quartile |
| lgbm_sc_s0 | ST       | norm_reg_ffbs | Q2         |      0.92  |      88 | acc_quartile |
| lgbm_sc_s0 | ST       | norm_reg_ffbs | Q3         |      0.92  |      88 | acc_quartile |
| lgbm_sc_s0 | ST       | norm_reg_ffbs | Q4 (best)  |      0.92  |      88 | acc_quartile |
| lgbm_sc_s0 | ST       | scp_abs       | Q1 (worst) |      0.761 |      88 | acc_quartile |
| lgbm_sc_s0 | ST       | scp_abs       | Q2         |      0.955 |      88 | acc_quartile |
| lgbm_sc_s0 | ST       | scp_abs       | Q3         |      0.943 |      88 | acc_quartile |
| lgbm_sc_s0 | ST       | scp_abs       | Q4 (best)  |      0.966 |      88 | acc_quartile |
| lgbm_sc_s0 | ST       | scp_abs_bc    | Q1 (worst) |      0.773 |      88 | acc_quartile |
| lgbm_sc_s0 | ST       | scp_abs_bc    | Q2         |      0.92  |      88 | acc_quartile |
| lgbm_sc_s0 | ST       | scp_abs_bc    | Q3         |      0.92  |      88 | acc_quartile |
| lgbm_sc_s0 | ST       | scp_abs_bc    | Q4 (best)  |      0.943 |      88 | acc_quartile |
| lgbm_sc_s0 | SC       | ba_loa        | <40        |      0.952 |     312 | age_group    |
| lgbm_sc_s0 | SC       | ba_loa        | 40-59      |      0.945 |     344 | age_group    |
| lgbm_sc_s0 | SC       | ba_loa        | >=60       |      0.887 |     568 | age_group    |
| lgbm_sc_s0 | SC       | norm_reg_ffbs | <40        |      0.926 |     312 | age_group    |
| lgbm_sc_s0 | SC       | norm_reg_ffbs | 40-59      |      0.93  |     344 | age_group    |
| lgbm_sc_s0 | SC       | norm_reg_ffbs | >=60       |      0.871 |     568 | age_group    |
| lgbm_sc_s0 | SC       | scp_abs       | <40        |      0.939 |     312 | age_group    |
| lgbm_sc_s0 | SC       | scp_abs       | 40-59      |      0.922 |     344 | age_group    |
| lgbm_sc_s0 | SC       | scp_abs       | >=60       |      0.87  |     568 | age_group    |
| lgbm_sc_s0 | SC       | scp_abs_bc    | <40        |      0.942 |     312 | age_group    |
| lgbm_sc_s0 | SC       | scp_abs_bc    | 40-59      |      0.927 |     344 | age_group    |
| lgbm_sc_s0 | SC       | scp_abs_bc    | >=60       |      0.856 |     568 | age_group    |
| lgbm_sc_s0 | ST       | ba_loa        | <40        |      0.922 |     192 | age_group    |
| lgbm_sc_s0 | ST       | ba_loa        | 40-59      |      0.848 |     112 | age_group    |
| lgbm_sc_s0 | ST       | ba_loa        | >=60       |      0.812 |      48 | age_group    |
| lgbm_sc_s0 | ST       | norm_reg_ffbs | <40        |      0.938 |     192 | age_group    |
| lgbm_sc_s0 | ST       | norm_reg_ffbs | 40-59      |      0.839 |     112 | age_group    |
| lgbm_sc_s0 | ST       | norm_reg_ffbs | >=60       |      0.917 |      48 | age_group    |
| lgbm_sc_s0 | ST       | scp_abs       | <40        |      0.938 |     192 | age_group    |
| lgbm_sc_s0 | ST       | scp_abs       | 40-59      |      0.857 |     112 | age_group    |
| lgbm_sc_s0 | ST       | scp_abs       | >=60       |      0.896 |      48 | age_group    |
| lgbm_sc_s0 | ST       | scp_abs_bc    | <40        |      0.922 |     192 | age_group    |
| lgbm_sc_s0 | ST       | scp_abs_bc    | 40-59      |      0.866 |     112 | age_group    |
| lgbm_sc_s0 | ST       | scp_abs_bc    | >=60       |      0.812 |      48 | age_group    |
| lgbm_sc_s0 | SC       | ba_loa        | F          |      0.933 |     656 | sex          |
| lgbm_sc_s0 | SC       | ba_loa        | M          |      0.905 |     568 | sex          |
| lgbm_sc_s0 | SC       | norm_reg_ffbs | F          |      0.916 |     656 | sex          |
| lgbm_sc_s0 | SC       | norm_reg_ffbs | M          |      0.886 |     568 | sex          |
| lgbm_sc_s0 | SC       | scp_abs       | F          |      0.919 |     656 | sex          |
| lgbm_sc_s0 | SC       | scp_abs       | M          |      0.882 |     568 | sex          |
| lgbm_sc_s0 | SC       | scp_abs_bc    | F          |      0.913 |     656 | sex          |
| lgbm_sc_s0 | SC       | scp_abs_bc    | M          |      0.88  |     568 | sex          |
| lgbm_sc_s0 | ST       | ba_loa        | F          |      0.867 |     240 | sex          |
| lgbm_sc_s0 | ST       | ba_loa        | M          |      0.92  |     112 | sex          |
| lgbm_sc_s0 | ST       | norm_reg_ffbs | F          |      0.904 |     240 | sex          |
| lgbm_sc_s0 | ST       | norm_reg_ffbs | M          |      0.902 |     112 | sex          |
| lgbm_sc_s0 | ST       | scp_abs       | F          |      0.888 |     240 | sex          |
| lgbm_sc_s0 | ST       | scp_abs       | M          |      0.946 |     112 | sex          |
| lgbm_sc_s0 | ST       | scp_abs_bc    | F          |      0.871 |     240 | sex          |
| lgbm_sc_s0 | ST       | scp_abs_bc    | M          |      0.929 |     112 | sex          |
| lgbm_sc_s0 | ST       | ba_loa        | placebo    |      0.875 |     176 | condition    |
| lgbm_sc_s0 | ST       | ba_loa        | temazepam  |      0.892 |     176 | condition    |
| lgbm_sc_s0 | ST       | norm_reg_ffbs | placebo    |      0.92  |     176 | condition    |
| lgbm_sc_s0 | ST       | norm_reg_ffbs | temazepam  |      0.886 |     176 | condition    |
| lgbm_sc_s0 | ST       | scp_abs       | placebo    |      0.903 |     176 | condition    |
| lgbm_sc_s0 | ST       | scp_abs       | temazepam  |      0.909 |     176 | condition    |
| lgbm_sc_s0 | ST       | scp_abs_bc    | placebo    |      0.869 |     176 | condition    |
| lgbm_sc_s0 | ST       | scp_abs_bc    | temazepam  |      0.909 |     176 | condition    |


# S10. Cohort-specific plug-in bias (YASA and LightGBM) and epoch confusion matrices


**yasa: plug-in bias (automatic − reference)**

| cohort   | param   |   plug_bias |   plug_sd |
|:---------|:--------|------------:|----------:|
| SC       | TST     |      -21.74 |     34.14 |
| SC       | SOL     |        4.42 |     14.49 |
| SC       | WASO    |       30.12 |     47.6  |
| SC       | REML    |       -6.39 |     43.86 |
| SC       | N1%     |       -9.12 |      9.31 |
| SC       | N2%     |        3.68 |     11.91 |
| SC       | N3%     |        5.94 |      6.17 |
| SC       | REM%    |       -0.5  |      6.91 |
| ST       | TST     |      -22.68 |     17.43 |
| ST       | SOL     |        3.7  |      3.59 |
| ST       | WASO    |       17.55 |     15.22 |
| ST       | REML    |        5.35 |     38.72 |
| ST       | N1%     |       -4.57 |      4.55 |
| ST       | N2%     |        0.88 |      9.66 |
| ST       | N3%     |        4.01 |      7.7  |
| ST       | REM%    |       -0.32 |      5.39 |
| HMC      | TST     |      -38.28 |     41.34 |
| HMC      | SOL     |        5.72 |     10.83 |
| HMC      | WASO    |       31.42 |     40.36 |
| HMC      | REML    |      -22.23 |     63.42 |
| HMC      | N1%     |       -5.57 |      8.39 |
| HMC      | N2%     |       10.46 |     10.08 |
| HMC      | N3%     |       -4.79 |      7.62 |
| HMC      | REM%    |       -0.1  |      5.67 |


**yasa: row-normalised epoch confusion (reference × predicted)**

| cohort   | reference   |   pred_W |   pred_N1 |   pred_N2 |   pred_N3 |   pred_REM |
|:---------|:------------|---------:|----------:|----------:|----------:|-----------:|
| SC       | W           |    0.945 |     0.022 |     0.023 |     0.002 |      0.007 |
| SC       | N1          |    0.334 |     0.219 |     0.354 |     0.008 |      0.084 |
| SC       | N2          |    0.018 |     0.026 |     0.82  |     0.113 |      0.024 |
| SC       | N3          |    0.009 |     0     |     0.092 |     0.898 |      0.001 |
| SC       | REM         |    0.072 |     0.03  |     0.109 |     0.003 |      0.787 |
| ST       | W           |    0.967 |     0.017 |     0.006 |     0     |      0.01  |
| ST       | N1          |    0.392 |     0.329 |     0.162 |     0.001 |      0.117 |
| ST       | N2          |    0.022 |     0.023 |     0.836 |     0.099 |      0.019 |
| ST       | N3          |    0.008 |     0     |     0.123 |     0.868 |      0     |
| ST       | REM         |    0.026 |     0.017 |     0.126 |     0.001 |      0.831 |
| HMC      | W           |    0.949 |     0.026 |     0.017 |     0     |      0.008 |
| HMC      | N1          |    0.462 |     0.24  |     0.198 |     0.002 |      0.097 |
| HMC      | N2          |    0.069 |     0.061 |     0.809 |     0.032 |      0.029 |
| HMC      | N3          |    0.014 |     0.001 |     0.302 |     0.676 |      0.006 |
| HMC      | REM         |    0.083 |     0.057 |     0.11  |     0.002 |      0.748 |


**lgbm_sc_s0: plug-in bias (automatic − reference)**

| cohort   | param   |   plug_bias |   plug_sd |
|:---------|:--------|------------:|----------:|
| SC       | TST     |       10.14 |     26.97 |
| SC       | SOL     |       -3.35 |     13.66 |
| SC       | WASO    |        3.42 |     39.86 |
| SC       | REML    |      -11.25 |     38.01 |
| SC       | N1%     |        3.82 |      9.17 |
| SC       | N2%     |       -4.16 |      9.29 |
| SC       | N3%     |        0.54 |      4.31 |
| SC       | REM%    |       -0.21 |      5.88 |
| ST       | TST     |      -12.42 |     18.61 |
| ST       | SOL     |       -1.48 |      7.54 |
| ST       | WASO    |       13.01 |     16.22 |
| ST       | REML    |        7.48 |     46.71 |
| ST       | N1%     |        3.29 |      5.54 |
| ST       | N2%     |       -2.76 |      9.63 |
| ST       | N3%     |        2.08 |      7.7  |
| ST       | REM%    |       -2.61 |      5.4  |
| HMC      | TST     |      -37.06 |     47.89 |
| HMC      | SOL     |        2.19 |     13.29 |
| HMC      | WASO    |       34.77 |     41.76 |
| HMC      | REML    |      -20.69 |     64.85 |
| HMC      | N1%     |        8.17 |     10.66 |
| HMC      | N2%     |        5.22 |     11.67 |
| HMC      | N3%     |      -10.83 |     10.33 |
| HMC      | REM%    |       -2.56 |      5.78 |


**lgbm_sc_s0: row-normalised epoch confusion (reference × predicted)**

| cohort   | reference   |   pred_W |   pred_N1 |   pred_N2 |   pred_N3 |   pred_REM |
|:---------|:------------|---------:|----------:|----------:|----------:|-----------:|
| SC       | W           |    0.888 |     0.095 |     0.008 |     0.001 |      0.009 |
| SC       | N1          |    0.128 |     0.565 |     0.219 |     0.005 |      0.084 |
| SC       | N2          |    0.006 |     0.102 |     0.821 |     0.042 |      0.029 |
| SC       | N3          |    0.006 |     0.003 |     0.146 |     0.845 |      0.001 |
| SC       | REM         |    0.013 |     0.074 |     0.056 |     0.002 |      0.856 |
| ST       | W           |    0.871 |     0.122 |     0.002 |     0     |      0.005 |
| ST       | N1          |    0.253 |     0.603 |     0.074 |     0.001 |      0.067 |
| ST       | N2          |    0.023 |     0.076 |     0.81  |     0.076 |      0.014 |
| ST       | N3          |    0.009 |     0.002 |     0.131 |     0.858 |      0     |
| ST       | REM         |    0.025 |     0.07  |     0.121 |     0.002 |      0.782 |
| HMC      | W           |    0.859 |     0.128 |     0.007 |     0.001 |      0.005 |
| HMC      | N1          |    0.426 |     0.39  |     0.108 |     0.008 |      0.068 |
| HMC      | N2          |    0.102 |     0.181 |     0.666 |     0.025 |      0.025 |
| HMC      | N3          |    0.046 |     0.01  |     0.498 |     0.442 |      0.004 |
| HMC      | REM         |    0.07  |     0.178 |     0.101 |     0.002 |      0.649 |


# S11. Error analysis

**Covered vs non-covered nights (proposed method, LOSO; Mann–Whitney p)**


| cohort   | param   | variable     |   n_covered |   n_missed |   median_covered |   median_missed |       p |
|:---------|:--------|:-------------|------------:|-----------:|-----------------:|----------------:|--------:|
| HMC      | N1%     | acc_plugin   |         136 |         15 |            0.757 |           0.682 |   0.002 |
| HMC      | N1%     | mean_entropy |         136 |         15 |            0.636 |           0.717 |   0.052 |
| HMC      | N1%     | age          |           0 |          0 |          nan     |         nan     | nan     |
| HMC      | N1%     | n_scored     |         136 |         15 |          885     |         992     |   0.013 |
| HMC      | N2%     | acc_plugin   |         136 |         15 |            0.752 |           0.741 |   0.958 |
| HMC      | N2%     | mean_entropy |         136 |         15 |            0.643 |           0.633 |   0.835 |
| HMC      | N2%     | age          |           0 |          0 |          nan     |         nan     | nan     |
| HMC      | N2%     | n_scored     |         136 |         15 |          898.5   |         853     |   0.544 |
| HMC      | N3%     | acc_plugin   |         136 |         15 |            0.754 |           0.741 |   0.256 |
| HMC      | N3%     | mean_entropy |         136 |         15 |            0.643 |           0.63  |   0.707 |
| HMC      | N3%     | age          |           0 |          0 |          nan     |         nan     | nan     |
| HMC      | N3%     | n_scored     |         136 |         15 |          888     |         939     |   0.54  |
| HMC      | REM%    | acc_plugin   |         136 |         15 |            0.755 |           0.67  |   0.005 |
| HMC      | REM%    | mean_entropy |         136 |         15 |            0.642 |           0.657 |   0.599 |
| HMC      | REM%    | age          |           0 |          0 |          nan     |         nan     | nan     |
| HMC      | REM%    | n_scored     |         136 |         15 |          898.5   |         898     |   0.394 |
| HMC      | REML    | acc_plugin   |         135 |         15 |            0.754 |           0.719 |   0.387 |
| HMC      | REML    | mean_entropy |         135 |         15 |            0.636 |           0.743 |   0.003 |
| HMC      | REML    | age          |           0 |          0 |          nan     |         nan     | nan     |
| HMC      | REML    | n_scored     |         135 |         15 |          898     |         945     |   0.396 |
| HMC      | SOL     | acc_plugin   |         136 |         15 |            0.751 |           0.783 |   0.396 |
| HMC      | SOL     | mean_entropy |         136 |         15 |            0.64  |           0.727 |   0.136 |
| HMC      | SOL     | age          |           0 |          0 |          nan     |         nan     | nan     |
| HMC      | SOL     | n_scored     |         136 |         15 |          898.5   |         880     |   0.582 |
| HMC      | TST     | acc_plugin   |         136 |         15 |            0.757 |           0.651 |   0.003 |
| HMC      | TST     | mean_entropy |         136 |         15 |            0.636 |           0.807 |   0     |
| HMC      | TST     | age          |           0 |          0 |          nan     |         nan     | nan     |
| HMC      | TST     | n_scored     |         136 |         15 |          893     |         951     |   0.11  |
| HMC      | WASO    | acc_plugin   |         136 |         15 |            0.757 |           0.635 |   0.002 |
| HMC      | WASO    | mean_entropy |         136 |         15 |            0.636 |           0.743 |   0.002 |
| HMC      | WASO    | age          |           0 |          0 |          nan     |         nan     | nan     |
| HMC      | WASO    | n_scored     |         136 |         15 |          887     |         999     |   0.023 |
| SC       | N1%     | acc_plugin   |         138 |         15 |            0.816 |           0.698 |   0     |
| SC       | N1%     | mean_entropy |         138 |         15 |            0.491 |           0.559 |   0.058 |
| SC       | N1%     | age          |         138 |         15 |           56     |          85     |   0.006 |
| SC       | N1%     | n_scored     |         138 |         15 |         1200     |        1200     |   0.528 |
| SC       | N2%     | acc_plugin   |         138 |         15 |            0.816 |           0.698 |   0     |
| SC       | N2%     | mean_entropy |         138 |         15 |            0.488 |           0.604 |   0.002 |
| SC       | N2%     | age          |         138 |         15 |           56     |          89     |   0.001 |
| SC       | N2%     | n_scored     |         138 |         15 |         1200     |        1200     |   0.161 |
| SC       | N3%     | acc_plugin   |         138 |         15 |            0.811 |           0.759 |   0.051 |
| SC       | N3%     | mean_entropy |         138 |         15 |            0.498 |           0.533 |   0.253 |
| SC       | N3%     | age          |         138 |         15 |           56.5   |          67     |   0.409 |
| SC       | N3%     | n_scored     |         138 |         15 |         1200     |        1200     |   0.819 |
| SC       | REM%    | acc_plugin   |         137 |         16 |            0.812 |           0.759 |   0.012 |
| SC       | REM%    | mean_entropy |         137 |         16 |            0.491 |           0.643 |   0.008 |
| SC       | REM%    | age          |         137 |         16 |           57     |          76     |   0.08  |
| SC       | REM%    | n_scored     |         137 |         16 |         1200     |        1200     |   0.589 |
| SC       | REML    | acc_plugin   |         138 |         15 |            0.81  |           0.796 |   0.842 |
| SC       | REML    | mean_entropy |         138 |         15 |            0.494 |           0.524 |   0.729 |
| SC       | REML    | age          |         138 |         15 |           57     |          56     |   0.568 |
| SC       | REML    | n_scored     |         138 |         15 |         1200     |        1200     |   0.642 |
| SC       | SOL     | acc_plugin   |         138 |         15 |            0.81  |           0.807 |   0.648 |
| SC       | SOL     | mean_entropy |         138 |         15 |            0.498 |           0.505 |   0.968 |
| SC       | SOL     | age          |         138 |         15 |           57     |          57     |   0.98  |
| SC       | SOL     | n_scored     |         138 |         15 |         1200     |        1200     |   0.88  |
| SC       | TST     | acc_plugin   |         138 |         15 |            0.816 |           0.732 |   0     |
| SC       | TST     | mean_entropy |         138 |         15 |            0.485 |           0.607 |   0     |
| SC       | TST     | age          |         138 |         15 |           56     |          67     |   0.105 |
| SC       | TST     | n_scored     |         138 |         15 |         1200     |        1200     |   0.991 |
| SC       | WASO    | acc_plugin   |         138 |         15 |            0.808 |           0.838 |   0.058 |
| SC       | WASO    | mean_entropy |         138 |         15 |            0.491 |           0.557 |   0.282 |
| SC       | WASO    | age          |         138 |         15 |           57     |          51     |   0.23  |
| SC       | WASO    | n_scored     |         138 |         15 |         1200     |        1200     |   0.102 |
| ST       | N1%     | acc_plugin   |          40 |          4 |            0.819 |           0.798 |   0.273 |
| ST       | N1%     | mean_entropy |          40 |          4 |            0.45  |           0.542 |   0.062 |
| ST       | N1%     | age          |          40 |          4 |           34.5   |          56     |   0.043 |
| ST       | N1%     | n_scored     |          40 |          4 |          964.5   |         975.5   |   0.87  |
| ST       | N2%     | acc_plugin   |          40 |          4 |            0.825 |           0.742 |   0.019 |
| ST       | N2%     | mean_entropy |          40 |          4 |            0.453 |           0.479 |   0.49  |
| ST       | N2%     | age          |          40 |          4 |           35     |          22     |   0.115 |
| ST       | N2%     | n_scored     |          40 |          4 |          961     |        1000.5   |   0.5   |
| ST       | N3%     | acc_plugin   |          40 |          4 |            0.825 |           0.745 |   0.012 |
| ST       | N3%     | mean_entropy |          40 |          4 |            0.46  |           0.439 |   0.953 |
| ST       | N3%     | age          |          40 |          4 |           35     |          35     |   0.854 |
| ST       | N3%     | n_scored     |          40 |          4 |          964.5   |         975.5   |   0.791 |
| ST       | REM%    | acc_plugin   |          40 |          4 |            0.824 |           0.787 |   0.192 |
| ST       | REM%    | mean_entropy |          40 |          4 |            0.466 |           0.37  |   0.036 |
| ST       | REM%    | age          |          40 |          4 |           35     |          22.5   |   0.379 |
| ST       | REM%    | n_scored     |          40 |          4 |          961     |         995.5   |   0.624 |
| ST       | REML    | acc_plugin   |          40 |          4 |            0.816 |           0.828 |   0.595 |
| ST       | REML    | mean_entropy |          40 |          4 |            0.467 |           0.379 |   0.022 |
| ST       | REML    | age          |          40 |          4 |           35     |          21     |   0.212 |
| ST       | REML    | n_scored     |          40 |          4 |          956.5   |        1012     |   0.136 |
| ST       | SOL     | acc_plugin   |          40 |          4 |            0.816 |           0.843 |   0.331 |
| ST       | SOL     | mean_entropy |          40 |          4 |            0.453 |           0.521 |   0.273 |
| ST       | SOL     | age          |          40 |          4 |           35     |          48     |   0.278 |
| ST       | SOL     | n_scored     |          40 |          4 |          956.5   |         984.5   |   0.307 |
| ST       | TST     | acc_plugin   |          39 |          5 |            0.819 |           0.777 |   0.693 |
| ST       | TST     | mean_entropy |          39 |          5 |            0.449 |           0.557 |   0.023 |
| ST       | TST     | age          |          39 |          5 |           34     |          53     |   0.023 |
| ST       | TST     | n_scored     |          39 |          5 |          966     |         931     |   0.375 |
| ST       | WASO    | acc_plugin   |          40 |          4 |            0.819 |           0.746 |   0.256 |
| ST       | WASO    | mean_entropy |          40 |          4 |            0.45  |           0.533 |   0.068 |
| ST       | WASO    | age          |          40 |          4 |           34.5   |          56.5   |   0.032 |
| ST       | WASO    | n_scored     |          40 |          4 |          964.5   |         948.5   |   0.919 |


**WASO mechanism (YASA): wake after final awakening and late sampled final awakenings**

| cohort   |   nights |   median_post_awakening_wake |   mean_frac_late |   spearman_frac_vs_err |
|:---------|---------:|-----------------------------:|-----------------:|-----------------------:|
| HMC      |      151 |                          0.5 |            0.007 |                  0.135 |
| SC       |      153 |                        116.5 |            0.491 |                  0.786 |
| ST       |       44 |                          4   |            0.019 |                  0.246 |


# S12. Robustness to signal corruption (YASA)

| corruption   | cohort   | param   | method        |   coverage |   mean_width |   interval_score |
|:-------------|:---------|:--------|:--------------|-----------:|-------------:|-----------------:|
| art10        | HMC      | N1%     | ba_loa        |      0.913 |       25.151 |           39.068 |
| art10        | HMC      | N1%     | cqr_ffbs      |      0.925 |       22.685 |           35.762 |
| art10        | HMC      | N1%     | norm_reg_ffbs |      0.93  |       22.834 |           35.838 |
| art10        | HMC      | N1%     | scp_abs_bc    |      0.903 |       24.146 |           39.328 |
| art10        | HMC      | N2%     | ba_loa        |      0.903 |       32.968 |           47.636 |
| art10        | HMC      | N2%     | cqr_ffbs      |      0.95  |       28.894 |           32.642 |
| art10        | HMC      | N2%     | norm_reg_ffbs |      0.952 |       29.288 |           32.869 |
| art10        | HMC      | N2%     | scp_abs_bc    |      0.89  |       30.862 |           47.243 |
| art10        | HMC      | N3%     | ba_loa        |      0.898 |       24.424 |           33.158 |
| art10        | HMC      | N3%     | cqr_ffbs      |      0.93  |       31.345 |           37.816 |
| art10        | HMC      | N3%     | norm_reg_ffbs |      0.935 |       31.855 |           37.4   |
| art10        | HMC      | N3%     | scp_abs_bc    |      0.9   |       24.65  |           33.274 |
| art10        | HMC      | REM%    | ba_loa        |      0.865 |       18.169 |           27.805 |
| art10        | HMC      | REM%    | cqr_ffbs      |      0.937 |       23.111 |           27.801 |
| art10        | HMC      | REM%    | norm_reg_ffbs |      0.939 |       23.452 |           27.8   |
| art10        | HMC      | REM%    | scp_abs_bc    |      0.856 |       17.87  |           27.815 |
| art10        | HMC      | REML    | ba_loa        |      0.874 |      187.516 |          374.19  |
| art10        | HMC      | REML    | cqr_ffbs      |      0.923 |      166.212 |          281.381 |
| art10        | HMC      | REML    | norm_reg_ffbs |      0.91  |      189.348 |          331.387 |
| art10        | HMC      | REML    | scp_abs_bc    |      0.874 |      189.082 |          372.935 |
| art10        | HMC      | SOL     | ba_loa        |      0.894 |       24.911 |           62.274 |
| art10        | HMC      | SOL     | cqr_ffbs      |      0.923 |       20.994 |           56.872 |
| art10        | HMC      | SOL     | norm_reg_ffbs |      0.905 |       23.287 |           69.379 |
| art10        | HMC      | SOL     | scp_abs_bc    |      0.874 |       22.494 |           65.337 |
| art10        | HMC      | TST     | ba_loa        |      0.836 |      133.109 |          261.378 |
| art10        | HMC      | TST     | cqr_ffbs      |      0.888 |       99.779 |          160.619 |
| art10        | HMC      | TST     | norm_reg_ffbs |      0.89  |       96.411 |          153.799 |
| art10        | HMC      | TST     | scp_abs_bc    |      0.781 |      107.739 |          279.53  |
| art10        | HMC      | WASO    | ba_loa        |      0.822 |      118.828 |          249.254 |
| art10        | HMC      | WASO    | cqr_ffbs      |      0.879 |       88.278 |          160.839 |
| art10        | HMC      | WASO    | norm_reg_ffbs |      0.881 |       88.849 |          162.039 |
| art10        | HMC      | WASO    | scp_abs_bc    |      0.788 |      105.635 |          261.865 |
| art10        | SC       | N1%     | ba_loa        |      0.887 |       29.385 |           45.877 |
| art10        | SC       | N1%     | cqr_ffbs      |      0.931 |       29.462 |           39.066 |
| art10        | SC       | N1%     | norm_reg_ffbs |      0.937 |       30.13  |           38.259 |
| art10        | SC       | N1%     | scp_abs_bc    |      0.857 |       26.945 |           47.664 |
| art10        | SC       | N2%     | ba_loa        |      0.9   |       38.626 |           54.246 |
| art10        | SC       | N2%     | cqr_ffbs      |      0.922 |       34.678 |           45.359 |
| art10        | SC       | N2%     | norm_reg_ffbs |      0.927 |       35.183 |           44.986 |
| art10        | SC       | N2%     | scp_abs_bc    |      0.893 |       38.913 |           55.28  |
| art10        | SC       | N3%     | ba_loa        |      0.895 |       15.643 |           24.967 |
| art10        | SC       | N3%     | cqr_ffbs      |      0.903 |       16.906 |           24.585 |
| art10        | SC       | N3%     | norm_reg_ffbs |      0.902 |       16.467 |           24.017 |
| art10        | SC       | N3%     | scp_abs_bc    |      0.89  |       15.376 |           25.318 |
| art10        | SC       | REM%    | ba_loa        |      0.902 |       21.938 |           34.131 |
| art10        | SC       | REM%    | cqr_ffbs      |      0.91  |       27.425 |           36.243 |
| art10        | SC       | REM%    | norm_reg_ffbs |      0.917 |       28.01  |           35.412 |
| art10        | SC       | REM%    | scp_abs_bc    |      0.873 |       18.666 |           33.91  |
| art10        | SC       | REML    | ba_loa        |      0.836 |      129.257 |          276.926 |
| art10        | SC       | REML    | cqr_ffbs      |      0.937 |      134.406 |          164.763 |
| art10        | SC       | REML    | norm_reg_ffbs |      0.844 |      107.896 |          183.273 |
| art10        | SC       | REML    | scp_abs_bc    |      0.862 |      142.601 |          261.59  |
| art10        | SC       | SOL     | ba_loa        |      0.904 |       33.698 |           74.954 |
| art10        | SC       | SOL     | cqr_ffbs      |      0.926 |       29.969 |           40.701 |
| art10        | SC       | SOL     | norm_reg_ffbs |      0.906 |       28.391 |           62.806 |
| art10        | SC       | SOL     | scp_abs_bc    |      0.878 |       26.285 |           79.31  |
| art10        | SC       | TST     | ba_loa        |      0.793 |      109.775 |          249.232 |
| art10        | SC       | TST     | cqr_ffbs      |      0.883 |       98.318 |          193.858 |
| art10        | SC       | TST     | norm_reg_ffbs |      0.886 |       97.889 |          189.894 |
| art10        | SC       | TST     | scp_abs_bc    |      0.784 |      108.573 |          251.547 |
| art10        | SC       | WASO    | ba_loa        |      0.693 |      142.599 |          469.345 |
| art10        | SC       | WASO    | cqr_ffbs      |      0.83  |      207.704 |          335.133 |
| art10        | SC       | WASO    | norm_reg_ffbs |      0.816 |      235.16  |          369.996 |
| art10        | SC       | WASO    | scp_abs_bc    |      0.671 |      133.509 |          493.542 |
| art10        | ST       | N1%     | ba_loa        |      0.861 |       14.707 |           21.304 |
| art10        | ST       | N1%     | cqr_ffbs      |      0.92  |       18.578 |           22.784 |
| art10        | ST       | N1%     | norm_reg_ffbs |      0.92  |       18.378 |           22.143 |
| art10        | ST       | N1%     | scp_abs_bc    |      0.895 |       16.217 |           20.84  |
| art10        | ST       | N2%     | ba_loa        |      0.861 |       30.719 |           42.252 |
| art10        | ST       | N2%     | cqr_ffbs      |      0.907 |       33.73  |           39.145 |
| art10        | ST       | N2%     | norm_reg_ffbs |      0.93  |       34.972 |           38.99  |
| art10        | ST       | N2%     | scp_abs_bc    |      0.874 |       32.746 |           42.546 |
| art10        | ST       | N3%     | ba_loa        |      0.857 |       23.566 |           33.026 |
| art10        | ST       | N3%     | cqr_ffbs      |      0.949 |       26.707 |           28.101 |
| art10        | ST       | N3%     | norm_reg_ffbs |      0.955 |       26.577 |           27.791 |
| art10        | ST       | N3%     | scp_abs_bc    |      0.884 |       26.067 |           32.509 |
| art10        | ST       | REM%    | ba_loa        |      0.878 |       17.392 |           29.667 |
| art10        | ST       | REM%    | cqr_ffbs      |      0.932 |       25.122 |           26.874 |
| art10        | ST       | REM%    | norm_reg_ffbs |      0.944 |       26.119 |           27.42  |
| art10        | ST       | REM%    | scp_abs_bc    |      0.892 |       19.997 |           30.486 |
| art10        | ST       | REML    | ba_loa        |      0.88  |      123.1   |          196.549 |
| art10        | ST       | REML    | cqr_ffbs      |      0.934 |      138.79  |          148.864 |
| art10        | ST       | REML    | norm_reg_ffbs |      0.918 |      154.221 |          188.007 |
| art10        | ST       | REML    | scp_abs_bc    |      0.916 |      157.945 |          186.122 |
| art10        | ST       | SOL     | ba_loa        |      0.867 |       11.138 |           18.761 |
| art10        | ST       | SOL     | cqr_ffbs      |      0.96  |       17.963 |           29.468 |
| art10        | ST       | SOL     | norm_reg_ffbs |      0.888 |       18.916 |           38.811 |
| art10        | ST       | SOL     | scp_abs_bc    |      0.862 |       12.166 |           20.183 |
| art10        | ST       | TST     | ba_loa        |      0.673 |       55.017 |          229.924 |
| art10        | ST       | TST     | cqr_ffbs      |      0.859 |       42.742 |           79.139 |
| art10        | ST       | TST     | norm_reg_ffbs |      0.864 |       42.609 |           81.276 |
| art10        | ST       | TST     | scp_abs_bc    |      0.73  |       62.621 |          217.823 |
| art10        | ST       | WASO    | ba_loa        |      0.619 |       44.847 |          213.825 |
| art10        | ST       | WASO    | cqr_ffbs      |      0.842 |       55.457 |          100.854 |
| art10        | ST       | WASO    | norm_reg_ffbs |      0.842 |       56.44  |          104.788 |
| art10        | ST       | WASO    | scp_abs_bc    |      0.611 |       43.016 |          218.241 |
| art25        | HMC      | N1%     | ba_loa        |      0.922 |       24.876 |           39.508 |
| art25        | HMC      | N1%     | cqr_ffbs      |      0.926 |       23.265 |           35.796 |
| art25        | HMC      | N1%     | norm_reg_ffbs |      0.933 |       23.593 |           35.964 |
| art25        | HMC      | N1%     | scp_abs_bc    |      0.915 |       23.929 |           39.655 |
| art25        | HMC      | N2%     | ba_loa        |      0.856 |       32.968 |           53.071 |
| art25        | HMC      | N2%     | cqr_ffbs      |      0.952 |       29.957 |           33.765 |
| art25        | HMC      | N2%     | norm_reg_ffbs |      0.951 |       30.446 |           34.188 |
| art25        | HMC      | N2%     | scp_abs_bc    |      0.836 |       30.862 |           53.573 |
| art25        | HMC      | N3%     | ba_loa        |      0.885 |       24.426 |           35.469 |
| art25        | HMC      | N3%     | cqr_ffbs      |      0.942 |       32.338 |           37.761 |
| art25        | HMC      | N3%     | norm_reg_ffbs |      0.948 |       33.286 |           38.224 |
| art25        | HMC      | N3%     | scp_abs_bc    |      0.885 |       24.647 |           35.534 |
| art25        | HMC      | REM%    | ba_loa        |      0.827 |       18.106 |           29.706 |
| art25        | HMC      | REM%    | cqr_ffbs      |      0.955 |       23.988 |           28.016 |
| art25        | HMC      | REM%    | norm_reg_ffbs |      0.957 |       24.419 |           28.299 |
| art25        | HMC      | REM%    | scp_abs_bc    |      0.822 |       17.811 |           29.816 |
| art25        | HMC      | REML    | ba_loa        |      0.87  |      188.241 |          405.76  |
| art25        | HMC      | REML    | cqr_ffbs      |      0.909 |      169.832 |          337.372 |
| art25        | HMC      | REML    | norm_reg_ffbs |      0.906 |      194.688 |          365.22  |
| art25        | HMC      | REML    | scp_abs_bc    |      0.874 |      189.875 |          404.287 |
| art25        | HMC      | SOL     | ba_loa        |      0.908 |       25.52  |           60.523 |
| art25        | HMC      | SOL     | cqr_ffbs      |      0.918 |       21.252 |           60.35  |
| art25        | HMC      | SOL     | norm_reg_ffbs |      0.906 |       23.434 |           70.933 |
| art25        | HMC      | SOL     | scp_abs_bc    |      0.888 |       23.089 |           62.808 |
| art25        | HMC      | TST     | ba_loa        |      0.694 |      133.109 |          358.631 |
| art25        | HMC      | TST     | cqr_ffbs      |      0.867 |      103.716 |          174.492 |
| art25        | HMC      | TST     | norm_reg_ffbs |      0.876 |      102.366 |          168.456 |
| art25        | HMC      | TST     | scp_abs_bc    |      0.577 |      107.739 |          413.119 |
| art25        | HMC      | WASO    | ba_loa        |      0.675 |      124.708 |          355.833 |
| art25        | HMC      | WASO    | cqr_ffbs      |      0.839 |       92.534 |          178.55  |
| art25        | HMC      | WASO    | norm_reg_ffbs |      0.844 |       93.429 |          179.289 |
| art25        | HMC      | WASO    | scp_abs_bc    |      0.599 |      109.742 |          385.902 |
| art25        | SC       | N1%     | ba_loa        |      0.896 |       29.33  |           44.393 |
| art25        | SC       | N1%     | cqr_ffbs      |      0.948 |       31.327 |           37.72  |
| art25        | SC       | N1%     | norm_reg_ffbs |      0.959 |       32.571 |           37.393 |
| art25        | SC       | N1%     | scp_abs_bc    |      0.871 |       26.909 |           45.762 |
| art25        | SC       | N2%     | ba_loa        |      0.878 |       38.637 |           60.25  |
| art25        | SC       | N2%     | cqr_ffbs      |      0.9   |       35.788 |           49.075 |
| art25        | SC       | N2%     | norm_reg_ffbs |      0.908 |       36.692 |           48.837 |
| art25        | SC       | N2%     | scp_abs_bc    |      0.877 |       38.923 |           61.316 |
| art25        | SC       | N3%     | ba_loa        |      0.871 |       14.773 |           25.43  |
| art25        | SC       | N3%     | cqr_ffbs      |      0.86  |       16.429 |           29.476 |
| art25        | SC       | N3%     | norm_reg_ffbs |      0.853 |       15.975 |           29.226 |
| art25        | SC       | N3%     | scp_abs_bc    |      0.866 |       14.527 |           25.861 |
| art25        | SC       | REM%    | ba_loa        |      0.875 |       21.831 |           36.371 |
| art25        | SC       | REM%    | cqr_ffbs      |      0.928 |       28.695 |           37.37  |
| art25        | SC       | REM%    | norm_reg_ffbs |      0.929 |       29.658 |           36.85  |
| art25        | SC       | REM%    | scp_abs_bc    |      0.833 |       18.615 |           36.142 |
| art25        | SC       | REML    | ba_loa        |      0.814 |      130.478 |          265.361 |
| art25        | SC       | REML    | cqr_ffbs      |      0.961 |      160.947 |          172.729 |
| art25        | SC       | REML    | norm_reg_ffbs |      0.833 |      118.873 |          200.813 |
| art25        | SC       | REML    | scp_abs_bc    |      0.849 |      144.287 |          247.93  |
| art25        | SC       | SOL     | ba_loa        |      0.913 |       32.902 |           85.431 |
| art25        | SC       | SOL     | cqr_ffbs      |      0.926 |       32.127 |           46.348 |
| art25        | SC       | SOL     | norm_reg_ffbs |      0.904 |       29.82  |           67.901 |
| art25        | SC       | SOL     | scp_abs_bc    |      0.876 |       25.658 |           89.274 |
| art25        | SC       | TST     | ba_loa        |      0.569 |      109.775 |          390.529 |
| art25        | SC       | TST     | cqr_ffbs      |      0.817 |      106.894 |          231.991 |
| art25        | SC       | TST     | norm_reg_ffbs |      0.825 |      108.343 |          227.134 |
| art25        | SC       | TST     | scp_abs_bc    |      0.564 |      108.573 |          395.541 |
| art25        | SC       | WASO    | ba_loa        |      0.439 |      150.877 |          884.969 |
| art25        | SC       | WASO    | cqr_ffbs      |      0.697 |      209.59  |          455.094 |
| art25        | SC       | WASO    | norm_reg_ffbs |      0.687 |      236.228 |          489.856 |
| art25        | SC       | WASO    | scp_abs_bc    |      0.41  |      140.747 |          934.627 |
| art25        | ST       | N1%     | ba_loa        |      0.829 |       14.756 |           21.174 |
| art25        | ST       | N1%     | cqr_ffbs      |      0.949 |       19.678 |           21.503 |
| art25        | ST       | N1%     | norm_reg_ffbs |      0.96  |       19.825 |           21.316 |
| art25        | ST       | N1%     | scp_abs_bc    |      0.896 |       16.309 |           20.529 |
| art25        | ST       | N2%     | ba_loa        |      0.837 |       30.719 |           44.076 |
| art25        | ST       | N2%     | cqr_ffbs      |      0.924 |       34.48  |           39.169 |
| art25        | ST       | N2%     | norm_reg_ffbs |      0.929 |       36.108 |           39.721 |
| art25        | ST       | N2%     | scp_abs_bc    |      0.862 |       32.746 |           43.813 |
| art25        | ST       | N3%     | ba_loa        |      0.841 |       22.904 |           34.245 |
| art25        | ST       | N3%     | cqr_ffbs      |      0.938 |       26.634 |           29.105 |
| art25        | ST       | N3%     | norm_reg_ffbs |      0.939 |       26.712 |           29.22  |
| art25        | ST       | N3%     | scp_abs_bc    |      0.893 |       25.238 |           33.329 |
| art25        | ST       | REM%    | ba_loa        |      0.874 |       17.374 |           30.705 |
| art25        | ST       | REM%    | cqr_ffbs      |      0.947 |       25.881 |           28.371 |
| art25        | ST       | REM%    | norm_reg_ffbs |      0.95  |       27.358 |           29.329 |
| art25        | ST       | REM%    | scp_abs_bc    |      0.892 |       19.962 |           31.439 |
| art25        | ST       | REML    | ba_loa        |      0.822 |      121.599 |          232.247 |
| art25        | ST       | REML    | cqr_ffbs      |      0.956 |      150.177 |          157.103 |
| art25        | ST       | REML    | norm_reg_ffbs |      0.904 |      161.074 |          199.078 |
| art25        | ST       | REML    | scp_abs_bc    |      0.885 |      156.384 |          207.313 |
| art25        | ST       | SOL     | ba_loa        |      0.894 |       11.218 |           17.747 |
| art25        | ST       | SOL     | cqr_ffbs      |      0.958 |       18.233 |           29.751 |
| art25        | ST       | SOL     | norm_reg_ffbs |      0.869 |       18.898 |           40.99  |
| art25        | ST       | SOL     | scp_abs_bc    |      0.892 |       12.198 |           18.92  |
| art25        | ST       | TST     | ba_loa        |      0.225 |       55.017 |          504.958 |
| art25        | ST       | TST     | cqr_ffbs      |      0.831 |       47.353 |           92.942 |
| art25        | ST       | TST     | norm_reg_ffbs |      0.839 |       46.321 |           96.123 |
| art25        | ST       | TST     | scp_abs_bc    |      0.305 |       62.621 |          459.334 |
| art25        | ST       | WASO    | ba_loa        |      0.127 |       47.136 |          573.49  |
| art25        | ST       | WASO    | cqr_ffbs      |      0.794 |       59.539 |          125.475 |
| art25        | ST       | WASO    | norm_reg_ffbs |      0.805 |       60.539 |          129.676 |
| art25        | ST       | WASO    | scp_abs_bc    |      0.117 |       44.999 |          592.431 |
| clean        | HMC      | N1%     | ba_loa        |      0.919 |       25.236 |           38.633 |
| clean        | HMC      | N1%     | cqr_ffbs      |      0.905 |       21.651 |           35.521 |
| clean        | HMC      | N1%     | norm_reg_ffbs |      0.905 |       21.47  |           35.224 |
| clean        | HMC      | N1%     | scp_abs_bc    |      0.907 |       24.237 |           38.924 |
| clean        | HMC      | N2%     | ba_loa        |      0.924 |       32.968 |           46.868 |
| clean        | HMC      | N2%     | cqr_ffbs      |      0.911 |       27.767 |           35.242 |
| clean        | HMC      | N2%     | norm_reg_ffbs |      0.911 |       28.057 |           35.342 |
| clean        | HMC      | N2%     | scp_abs_bc    |      0.907 |       30.862 |           46.259 |
| clean        | HMC      | N3%     | ba_loa        |      0.903 |       24.394 |           33.422 |
| clean        | HMC      | N3%     | cqr_ffbs      |      0.91  |       30.384 |           36.163 |
| clean        | HMC      | N3%     | norm_reg_ffbs |      0.912 |       30.436 |           35.922 |
| clean        | HMC      | N3%     | scp_abs_bc    |      0.905 |       24.619 |           33.565 |
| clean        | HMC      | REM%    | ba_loa        |      0.91  |       18.136 |           25.243 |
| clean        | HMC      | REM%    | cqr_ffbs      |      0.908 |       21.855 |           27.22  |
| clean        | HMC      | REM%    | norm_reg_ffbs |      0.909 |       21.967 |           26.925 |
| clean        | HMC      | REM%    | scp_abs_bc    |      0.905 |       17.835 |           25.278 |
| clean        | HMC      | REML    | ba_loa        |      0.901 |      187.496 |          321.316 |
| clean        | HMC      | REML    | cqr_ffbs      |      0.906 |      156     |          293.69  |
| clean        | HMC      | REML    | norm_reg_ffbs |      0.905 |      182.944 |          316.953 |
| clean        | HMC      | REML    | scp_abs_bc    |      0.903 |      189.058 |          320.932 |
| clean        | HMC      | SOL     | ba_loa        |      0.917 |       24.689 |           48.207 |
| clean        | HMC      | SOL     | cqr_ffbs      |      0.934 |       19.464 |           55.12  |
| clean        | HMC      | SOL     | norm_reg_ffbs |      0.909 |       21.975 |           67.238 |
| clean        | HMC      | SOL     | scp_abs_bc    |      0.903 |       22.294 |           50.236 |
| clean        | HMC      | TST     | ba_loa        |      0.933 |      133.109 |          207.008 |
| clean        | HMC      | TST     | cqr_ffbs      |      0.91  |       94.803 |          151.953 |
| clean        | HMC      | TST     | norm_reg_ffbs |      0.908 |       88.407 |          143.114 |
| clean        | HMC      | TST     | scp_abs_bc    |      0.91  |      107.739 |          200.802 |
| clean        | HMC      | WASO    | ba_loa        |      0.929 |      102.83  |          173.863 |
| clean        | HMC      | WASO    | cqr_ffbs      |      0.912 |       81.809 |          146.897 |
| clean        | HMC      | WASO    | norm_reg_ffbs |      0.911 |       81.718 |          146.639 |
| clean        | HMC      | WASO    | scp_abs_bc    |      0.91  |       91.782 |          174.372 |
| clean        | SC       | N1%     | ba_loa        |      0.92  |       29.167 |           43.242 |
| clean        | SC       | N1%     | cqr_ffbs      |      0.904 |       26.959 |           41.331 |
| clean        | SC       | N1%     | norm_reg_ffbs |      0.903 |       26.806 |           40.266 |
| clean        | SC       | N1%     | scp_abs_bc    |      0.897 |       26.803 |           43.911 |
| clean        | SC       | N2%     | ba_loa        |      0.904 |       38.637 |           56.27  |
| clean        | SC       | N2%     | cqr_ffbs      |      0.905 |       33.187 |           43.678 |
| clean        | SC       | N2%     | norm_reg_ffbs |      0.905 |       33.016 |           42.967 |
| clean        | SC       | N2%     | scp_abs_bc    |      0.901 |       38.925 |           57.259 |
| clean        | SC       | N3%     | ba_loa        |      0.918 |       16.077 |           25.284 |
| clean        | SC       | N3%     | cqr_ffbs      |      0.913 |       17.092 |           23.217 |
| clean        | SC       | N3%     | norm_reg_ffbs |      0.913 |       16.565 |           22.752 |
| clean        | SC       | N3%     | scp_abs_bc    |      0.91  |       15.812 |           25.513 |
| clean        | SC       | REM%    | ba_loa        |      0.93  |       22.051 |           34.046 |
| clean        | SC       | REM%    | cqr_ffbs      |      0.907 |       25.36  |           35.039 |
| clean        | SC       | REM%    | norm_reg_ffbs |      0.908 |       25.045 |           34.094 |
| clean        | SC       | REM%    | scp_abs_bc    |      0.903 |       18.712 |           32.738 |
| clean        | SC       | REML    | ba_loa        |      0.879 |      129.867 |          238.455 |
| clean        | SC       | REML    | cqr_ffbs      |      0.917 |      107.812 |          139.668 |
| clean        | SC       | REML    | norm_reg_ffbs |      0.909 |       94.373 |          157.137 |
| clean        | SC       | REML    | scp_abs_bc    |      0.901 |      143.251 |          231.608 |
| clean        | SC       | SOL     | ba_loa        |      0.935 |       33.965 |           67.857 |
| clean        | SC       | SOL     | cqr_ffbs      |      0.922 |       27.75  |           33.393 |
| clean        | SC       | SOL     | norm_reg_ffbs |      0.912 |       27.058 |           55.974 |
| clean        | SC       | SOL     | scp_abs_bc    |      0.908 |       26.47  |           68.359 |
| clean        | SC       | TST     | ba_loa        |      0.899 |      109.775 |          173.68  |
| clean        | SC       | TST     | cqr_ffbs      |      0.904 |       88.957 |          152.82  |
| clean        | SC       | TST     | norm_reg_ffbs |      0.904 |       84.876 |          148.541 |
| clean        | SC       | TST     | scp_abs_bc    |      0.899 |      108.573 |          174.16  |
| clean        | SC       | WASO    | ba_loa        |      0.918 |      115.404 |          207.352 |
| clean        | SC       | WASO    | cqr_ffbs      |      0.904 |      201.819 |          271.759 |
| clean        | SC       | WASO    | norm_reg_ffbs |      0.903 |      229.532 |          311.473 |
| clean        | SC       | WASO    | scp_abs_bc    |      0.902 |      108.246 |          210.741 |
| clean        | ST       | N1%     | ba_loa        |      0.848 |       14.589 |           21.293 |
| clean        | ST       | N1%     | cqr_ffbs      |      0.909 |       17.51  |           24.877 |
| clean        | ST       | N1%     | norm_reg_ffbs |      0.911 |       16.91  |           24.412 |
| clean        | ST       | N1%     | scp_abs_bc    |      0.888 |       16.014 |           20.371 |
| clean        | ST       | N2%     | ba_loa        |      0.833 |       30.719 |           45.024 |
| clean        | ST       | N2%     | cqr_ffbs      |      0.89  |       32.749 |           40.101 |
| clean        | ST       | N2%     | norm_reg_ffbs |      0.89  |       33.327 |           40.107 |
| clean        | ST       | N2%     | scp_abs_bc    |      0.853 |       32.746 |           45.012 |
| clean        | ST       | N3%     | ba_loa        |      0.839 |       23.693 |           35.094 |
| clean        | ST       | N3%     | cqr_ffbs      |      0.91  |       26.528 |           29.961 |
| clean        | ST       | N3%     | norm_reg_ffbs |      0.91  |       26.065 |           29.137 |
| clean        | ST       | N3%     | scp_abs_bc    |      0.876 |       26.274 |           34.014 |
| clean        | ST       | REM%    | ba_loa        |      0.87  |       17.351 |           27.681 |
| clean        | ST       | REM%    | cqr_ffbs      |      0.901 |       23.883 |           28.328 |
| clean        | ST       | REM%    | norm_reg_ffbs |      0.9   |       24.06  |           28.499 |
| clean        | ST       | REM%    | scp_abs_bc    |      0.895 |       19.964 |           28.286 |
| clean        | ST       | REML    | ba_loa        |      0.85  |      123.23  |          233.074 |
| clean        | ST       | REML    | cqr_ffbs      |      0.911 |      127.009 |          137.625 |
| clean        | ST       | REML    | norm_reg_ffbs |      0.923 |      149.857 |          197.718 |
| clean        | ST       | REML    | scp_abs_bc    |      0.901 |      158.496 |          209.98  |
| clean        | ST       | SOL     | ba_loa        |      0.909 |       11.309 |           17.892 |
| clean        | ST       | SOL     | cqr_ffbs      |      0.96  |       17.84  |           29.333 |
| clean        | ST       | SOL     | norm_reg_ffbs |      0.892 |       18.906 |           37.892 |
| clean        | ST       | SOL     | scp_abs_bc    |      0.903 |       12.341 |           19.364 |
| clean        | ST       | TST     | ba_loa        |      0.893 |       55.017 |           97.818 |
| clean        | ST       | TST     | cqr_ffbs      |      0.916 |       39.128 |           58.092 |
| clean        | ST       | TST     | norm_reg_ffbs |      0.911 |       39.263 |           59.002 |
| clean        | ST       | TST     | scp_abs_bc    |      0.901 |       62.621 |           99.918 |
| clean        | ST       | WASO    | ba_loa        |      0.9   |       36.598 |           72.609 |
| clean        | ST       | WASO    | cqr_ffbs      |      0.909 |       51.704 |           79.896 |
| clean        | ST       | WASO    | norm_reg_ffbs |      0.909 |       52.626 |           82.692 |
| clean        | ST       | WASO    | scp_abs_bc    |      0.898 |       35.126 |           70.391 |
| gauss05      | HMC      | N1%     | ba_loa        |      0.858 |       21.899 |           46.7   |
| gauss05      | HMC      | N1%     | cqr_ffbs      |      0.95  |       25.038 |           30.618 |
| gauss05      | HMC      | N1%     | norm_reg_ffbs |      0.96  |       26.284 |           30.433 |
| gauss05      | HMC      | N1%     | scp_abs_bc    |      0.844 |       21.153 |           47.842 |
| gauss05      | HMC      | N2%     | ba_loa        |      0.596 |       32.74  |          121.805 |
| gauss05      | HMC      | N2%     | cqr_ffbs      |      0.907 |       30.345 |           38.69  |
| gauss05      | HMC      | N2%     | norm_reg_ffbs |      0.909 |       30.861 |           38.931 |
| gauss05      | HMC      | N2%     | scp_abs_bc    |      0.57  |       30.684 |          127.8   |
| gauss05      | HMC      | N3%     | ba_loa        |      0.768 |       23.396 |           61.988 |
| gauss05      | HMC      | N3%     | cqr_ffbs      |      0.944 |       30.859 |           36.27  |
| gauss05      | HMC      | N3%     | norm_reg_ffbs |      0.946 |       31.559 |           36.992 |
| gauss05      | HMC      | N3%     | scp_abs_bc    |      0.772 |       23.597 |           61.778 |
| gauss05      | HMC      | REM%    | ba_loa        |      0.67  |       17.033 |           57.422 |
| gauss05      | HMC      | REM%    | cqr_ffbs      |      0.903 |       23.765 |           29.721 |
| gauss05      | HMC      | REM%    | norm_reg_ffbs |      0.908 |       24.156 |           30.025 |
| gauss05      | HMC      | REM%    | scp_abs_bc    |      0.66  |       16.756 |           58.194 |
| gauss05      | HMC      | REML    | ba_loa        |      0.778 |      191.157 |          609.08  |
| gauss05      | HMC      | REML    | cqr_ffbs      |      0.942 |      187.385 |          301.038 |
| gauss05      | HMC      | REML    | norm_reg_ffbs |      0.927 |      206.799 |          335.561 |
| gauss05      | HMC      | REML    | scp_abs_bc    |      0.783 |      193.046 |          607.764 |
| gauss05      | HMC      | SOL     | ba_loa        |      0.825 |       27.273 |           92.977 |
| gauss05      | HMC      | SOL     | cqr_ffbs      |      0.918 |       22.484 |           57.295 |
| gauss05      | HMC      | SOL     | norm_reg_ffbs |      0.908 |       24.145 |           70.428 |
| gauss05      | HMC      | SOL     | scp_abs_bc    |      0.799 |       24.629 |           98.645 |
| gauss05      | HMC      | TST     | ba_loa        |      0.292 |      133.008 |         1293.8   |
| gauss05      | HMC      | TST     | cqr_ffbs      |      0.631 |      114.454 |          406.934 |
| gauss05      | HMC      | TST     | norm_reg_ffbs |      0.65  |      116.988 |          389.814 |
| gauss05      | HMC      | TST     | scp_abs_bc    |      0.229 |      107.711 |         1450.49  |
| gauss05      | HMC      | WASO    | ba_loa        |      0.312 |      128.123 |         1150.19  |
| gauss05      | HMC      | WASO    | cqr_ffbs      |      0.563 |      104.963 |          431.461 |
| gauss05      | HMC      | WASO    | norm_reg_ffbs |      0.58  |      106.596 |          426.236 |
| gauss05      | HMC      | WASO    | scp_abs_bc    |      0.258 |      111.73  |         1248.34  |
| gauss05      | SC       | N1%     | ba_loa        |      0.861 |       26.632 |           49.888 |
| gauss05      | SC       | N1%     | cqr_ffbs      |      0.951 |       32.844 |           39.776 |
| gauss05      | SC       | N1%     | norm_reg_ffbs |      0.962 |       34.87  |           40.189 |
| gauss05      | SC       | N1%     | scp_abs_bc    |      0.833 |       24.992 |           53.084 |
| gauss05      | SC       | N2%     | ba_loa        |      0.707 |       37.889 |          102.959 |
| gauss05      | SC       | N2%     | cqr_ffbs      |      0.888 |       38.294 |           48.516 |
| gauss05      | SC       | N2%     | norm_reg_ffbs |      0.899 |       40.01  |           48.483 |
| gauss05      | SC       | N2%     | scp_abs_bc    |      0.71  |       38.118 |          103.58  |
| gauss05      | SC       | N3%     | ba_loa        |      0.837 |       13.33  |           38.179 |
| gauss05      | SC       | N3%     | cqr_ffbs      |      0.804 |       15.284 |           41.082 |
| gauss05      | SC       | N3%     | norm_reg_ffbs |      0.8   |       14.738 |           41.49  |
| gauss05      | SC       | N3%     | scp_abs_bc    |      0.83  |       13.085 |           38.715 |
| gauss05      | SC       | REM%    | ba_loa        |      0.838 |       21.456 |           43.818 |
| gauss05      | SC       | REM%    | cqr_ffbs      |      0.787 |       31.859 |           51.748 |
| gauss05      | SC       | REM%    | norm_reg_ffbs |      0.82  |       33.596 |           49.249 |
| gauss05      | SC       | REM%    | scp_abs_bc    |      0.794 |       18.319 |           45.491 |
| gauss05      | SC       | REML    | ba_loa        |      0.757 |      129.827 |          346.404 |
| gauss05      | SC       | REML    | cqr_ffbs      |      0.945 |      163.96  |          170.219 |
| gauss05      | SC       | REML    | norm_reg_ffbs |      0.815 |      119.154 |          200.254 |
| gauss05      | SC       | REML    | scp_abs_bc    |      0.792 |      143.84  |          319.751 |
| gauss05      | SC       | SOL     | ba_loa        |      0.916 |       34.918 |           71.428 |
| gauss05      | SC       | SOL     | cqr_ffbs      |      0.947 |       38.014 |           39.302 |
| gauss05      | SC       | SOL     | norm_reg_ffbs |      0.926 |       32.883 |           60.57  |
| gauss05      | SC       | SOL     | scp_abs_bc    |      0.877 |       27.255 |           73.947 |
| gauss05      | SC       | TST     | ba_loa        |      0.249 |      109.77  |          941.411 |
| gauss05      | SC       | TST     | cqr_ffbs      |      0.452 |      122.655 |          586.165 |
| gauss05      | SC       | TST     | norm_reg_ffbs |      0.483 |      125.711 |          563.267 |
| gauss05      | SC       | TST     | scp_abs_bc    |      0.248 |      108.57  |          950.169 |
| gauss05      | SC       | WASO    | ba_loa        |      0.501 |      147.198 |          669.216 |
| gauss05      | SC       | WASO    | cqr_ffbs      |      0.514 |      239.067 |          623.044 |
| gauss05      | SC       | WASO    | norm_reg_ffbs |      0.584 |      266.505 |          608.028 |
| gauss05      | SC       | WASO    | scp_abs_bc    |      0.459 |      137.561 |          714.216 |
| gauss05      | ST       | N1%     | ba_loa        |      0.754 |       12.483 |           44.568 |
| gauss05      | ST       | N1%     | cqr_ffbs      |      0.971 |       21.864 |           22.631 |
| gauss05      | ST       | N1%     | norm_reg_ffbs |      0.972 |       22.547 |           23.228 |
| gauss05      | ST       | N1%     | scp_abs_bc    |      0.779 |       13.324 |           41.05  |
| gauss05      | ST       | N2%     | ba_loa        |      0.426 |       29.879 |          205.611 |
| gauss05      | ST       | N2%     | cqr_ffbs      |      0.823 |       36.418 |           57.919 |
| gauss05      | ST       | N2%     | norm_reg_ffbs |      0.839 |       38.746 |           56.21  |
| gauss05      | ST       | N2%     | scp_abs_bc    |      0.452 |       31.729 |          196.392 |
| gauss05      | ST       | N3%     | ba_loa        |      0.597 |       19.062 |           81.226 |
| gauss05      | ST       | N3%     | cqr_ffbs      |      0.775 |       24.65  |           41.346 |
| gauss05      | ST       | N3%     | norm_reg_ffbs |      0.76  |       24.639 |           41.587 |
| gauss05      | ST       | N3%     | scp_abs_bc    |      0.645 |       20.905 |           72.488 |
| gauss05      | ST       | REM%    | ba_loa        |      0.588 |       16.351 |           68.816 |
| gauss05      | ST       | REM%    | cqr_ffbs      |      0.907 |       27.36  |           32.303 |
| gauss05      | ST       | REM%    | norm_reg_ffbs |      0.925 |       29.385 |           33.188 |
| gauss05      | ST       | REM%    | scp_abs_bc    |      0.655 |       18.657 |           62.695 |
| gauss05      | ST       | REML    | ba_loa        |      0.651 |      122.288 |          508.97  |
| gauss05      | ST       | REML    | cqr_ffbs      |      0.97  |      192.148 |          194.535 |
| gauss05      | ST       | REML    | norm_reg_ffbs |      0.889 |      178.628 |          228.97  |
| gauss05      | ST       | REML    | scp_abs_bc    |      0.686 |      160.067 |          408.633 |
| gauss05      | ST       | SOL     | ba_loa        |      0.388 |        9.331 |          136.534 |
| gauss05      | ST       | SOL     | cqr_ffbs      |      0.96  |       20.575 |           34.175 |
| gauss05      | ST       | SOL     | norm_reg_ffbs |      0.862 |       20.267 |           43.576 |
| gauss05      | ST       | SOL     | scp_abs_bc    |      0.415 |       10.325 |          132.951 |
| gauss05      | ST       | TST     | ba_loa        |      0.02  |       55.017 |         1671.79  |
| gauss05      | ST       | TST     | cqr_ffbs      |      0.303 |       64.827 |          293.392 |
| gauss05      | ST       | TST     | norm_reg_ffbs |      0.286 |       57.702 |          325.669 |
| gauss05      | ST       | TST     | scp_abs_bc    |      0.034 |       62.621 |         1606.16  |
| gauss05      | ST       | WASO    | ba_loa        |      0.007 |       47.36  |         1628.37  |
| gauss05      | ST       | WASO    | cqr_ffbs      |      0.376 |       79.195 |          319.658 |
| gauss05      | ST       | WASO    | norm_reg_ffbs |      0.353 |       77.038 |          337.089 |
| gauss05      | ST       | WASO    | scp_abs_bc    |      0.007 |       45.203 |         1648.13  |
| gauss10      | HMC      | N1%     | ba_loa        |      0.814 |       19.79  |           49.17  |
| gauss10      | HMC      | N1%     | cqr_ffbs      |      0.945 |       25.168 |           33.7   |
| gauss10      | HMC      | N1%     | norm_reg_ffbs |      0.955 |       26.19  |           33.827 |
| gauss10      | HMC      | N1%     | scp_abs_bc    |      0.796 |       19.111 |           50.696 |
| gauss10      | HMC      | N2%     | ba_loa        |      0.09  |       32.281 |          327.943 |
| gauss10      | HMC      | N2%     | cqr_ffbs      |      0.743 |       30.819 |           63.247 |
| gauss10      | HMC      | N2%     | norm_reg_ffbs |      0.751 |       31.331 |           63.325 |
| gauss10      | HMC      | N2%     | scp_abs_bc    |      0.076 |       30.36  |          344.982 |
| gauss10      | HMC      | N3%     | ba_loa        |      0.586 |       22.526 |           91.378 |
| gauss10      | HMC      | N3%     | cqr_ffbs      |      0.947 |       31.616 |           38.044 |
| gauss10      | HMC      | N3%     | norm_reg_ffbs |      0.948 |       32.54  |           38.83  |
| gauss10      | HMC      | N3%     | scp_abs_bc    |      0.587 |       22.705 |           90.719 |
| gauss10      | HMC      | REM%    | ba_loa        |      0.354 |       13.882 |          114.982 |
| gauss10      | HMC      | REM%    | cqr_ffbs      |      0.825 |       22.335 |           38.48  |
| gauss10      | HMC      | REM%    | norm_reg_ffbs |      0.824 |       22.484 |           39.662 |
| gauss10      | HMC      | REM%    | scp_abs_bc    |      0.348 |       13.678 |          116.664 |


# S13. Cross-cohort transfer (calibration on SC) and few-night recalibration

| stager     | target   | param   | method         |   n_cal |   n_test |   coverage |   mean_width |   interval_score |
|:-----------|:---------|:--------|:---------------|--------:|---------:|-----------:|-------------:|-----------------:|
| yasa       | ST       | TST     | ba_loa         |     153 |       44 |      0.977 |      112.295 |          115.53  |
| yasa       | ST       | TST     | scp_abs_bc     |     153 |       44 |      0.977 |      103.471 |          108.711 |
| yasa       | ST       | TST     | scp_abs_cal    |     153 |       44 |      0.977 |      102     |          104.5   |
| yasa       | ST       | TST     | cqr_ffbs       |     153 |       44 |      0.955 |       71.989 |           86.295 |
| yasa       | ST       | TST     | norm_reg_ffbs  |     153 |       44 |      0.955 |       67.377 |           82.63  |
| yasa       | ST       | TST     | norm_reg_plugc |     153 |       44 |      0.977 |       74.285 |           77.777 |
| yasa       | HMC      | TST     | ba_loa         |     153 |      151 |      0.907 |      112.295 |          214.094 |
| yasa       | HMC      | TST     | scp_abs_bc     |     153 |      151 |      0.881 |      103.471 |          214.924 |
| yasa       | HMC      | TST     | scp_abs_cal    |     153 |      151 |      0.894 |      102     |          193.192 |
| yasa       | HMC      | TST     | cqr_ffbs       |     153 |      151 |      0.854 |       84.043 |          187.335 |
| yasa       | HMC      | TST     | norm_reg_ffbs  |     153 |      151 |      0.861 |       84.574 |          180.568 |
| yasa       | HMC      | TST     | norm_reg_plugc |     153 |      151 |      0.881 |       93.282 |          168.507 |
| yasa       | ST       | SOL     | ba_loa         |     153 |       44 |      1     |       36.644 |           36.644 |
| yasa       | ST       | SOL     | scp_abs_bc     |     153 |       44 |      1     |       26.67  |           26.67  |
| yasa       | ST       | SOL     | scp_abs_cal    |     153 |       44 |      1     |       32.045 |           32.045 |
| yasa       | ST       | SOL     | cqr_ffbs       |     153 |       44 |      0.977 |       22.312 |           22.54  |
| yasa       | ST       | SOL     | norm_reg_ffbs  |     153 |       44 |      1     |       23.937 |           23.937 |
| yasa       | ST       | SOL     | norm_reg_plugc |     153 |       44 |      1     |       26.959 |           26.959 |
| yasa       | HMC      | SOL     | ba_loa         |     153 |      151 |      0.94  |       33.309 |           47.804 |
| yasa       | HMC      | SOL     | scp_abs_bc     |     153 |      151 |      0.907 |       23.13  |           49.751 |
| yasa       | HMC      | SOL     | scp_abs_cal    |     153 |      151 |      0.947 |       27.685 |           52.586 |
| yasa       | HMC      | SOL     | cqr_ffbs       |     153 |      151 |      0.954 |       28.757 |           29.75  |
| yasa       | HMC      | SOL     | norm_reg_ffbs  |     153 |      151 |      0.914 |       26.733 |           41.51  |
| yasa       | HMC      | SOL     | norm_reg_plugc |     153 |      151 |      0.96  |       27.287 |           42.241 |
| yasa       | ST       | WASO    | ba_loa         |     153 |       44 |      1     |       92.091 |           92.091 |
| yasa       | ST       | WASO    | scp_abs_bc     |     153 |       44 |      1     |       86.652 |           86.652 |
| yasa       | ST       | WASO    | scp_abs_cal    |     153 |       44 |      1     |      121.92  |          121.92  |
| yasa       | ST       | WASO    | cqr_ffbs       |     153 |       44 |      1     |       92.678 |           92.678 |
| yasa       | ST       | WASO    | norm_reg_ffbs  |     153 |       44 |      1     |      104.39  |          104.39  |
| yasa       | ST       | WASO    | norm_reg_plugc |     153 |       44 |      1     |       92.701 |           92.701 |
| yasa       | HMC      | WASO    | ba_loa         |     153 |      151 |      0.96  |      122.287 |          172.05  |
| yasa       | HMC      | WASO    | scp_abs_bc     |     153 |      151 |      0.947 |      115.72  |          169.938 |
| yasa       | HMC      | WASO    | scp_abs_cal    |     153 |      151 |      0.954 |      144.752 |          185.745 |
| yasa       | HMC      | WASO    | cqr_ffbs       |     153 |      151 |      0.96  |      121.518 |          161.538 |
| yasa       | HMC      | WASO    | norm_reg_ffbs  |     153 |      151 |      0.974 |      126.438 |          164.31  |
| yasa       | HMC      | WASO    | norm_reg_plugc |     153 |      151 |      0.914 |      106.167 |          162.336 |
| yasa       | ST       | REML    | ba_loa         |     153 |       44 |      0.864 |      143.596 |          216.4   |
| yasa       | ST       | REML    | scp_abs_bc     |     153 |       44 |      0.886 |      152.391 |          212.492 |
| yasa       | ST       | REML    | scp_abs_cal    |     153 |       44 |      0.864 |      152.398 |          203.989 |
| yasa       | ST       | REML    | cqr_ffbs       |     153 |       44 |      0.909 |      119.568 |          129.818 |
| yasa       | ST       | REML    | norm_reg_ffbs  |     153 |       44 |      0.864 |       98.052 |          168.81  |
| yasa       | ST       | REML    | norm_reg_plugc |     153 |       44 |      0.864 |      136.333 |          191.995 |
| yasa       | HMC      | REML    | ba_loa         |     153 |      150 |      0.82  |      134.724 |          341.984 |
| yasa       | HMC      | REML    | scp_abs_bc     |     153 |      150 |      0.827 |      142.308 |          333.071 |
| yasa       | HMC      | REML    | scp_abs_cal    |     153 |      150 |      0.827 |      140.65  |          331.05  |
| yasa       | HMC      | REML    | cqr_ffbs       |     153 |      150 |      0.88  |      135.214 |          222.114 |
| yasa       | HMC      | REML    | norm_reg_ffbs  |     153 |      150 |      0.813 |      103.94  |          282.144 |
| yasa       | HMC      | REML    | norm_reg_plugc |     153 |      150 |      0.833 |      134.618 |          299.046 |
| yasa       | ST       | N1%     | ba_loa         |     153 |       44 |      1     |       28.897 |           28.897 |
| yasa       | ST       | N1%     | scp_abs_bc     |     153 |       44 |      0.977 |       24.973 |           25.132 |
| yasa       | ST       | N1%     | scp_abs_cal    |     153 |       44 |      1     |       24.161 |           24.161 |
| yasa       | ST       | N1%     | cqr_ffbs       |     153 |       44 |      1     |       22.072 |           22.072 |
| yasa       | ST       | N1%     | norm_reg_ffbs  |     153 |       44 |      1     |       21.315 |           21.315 |
| yasa       | ST       | N1%     | norm_reg_plugc |     153 |       44 |      1     |       21.774 |           21.774 |
| yasa       | HMC      | N1%     | ba_loa         |     153 |      151 |      0.94  |       29.67  |           38.275 |
| yasa       | HMC      | N1%     | scp_abs_bc     |     153 |      151 |      0.887 |       25.112 |           38.456 |
| yasa       | HMC      | N1%     | scp_abs_cal    |     153 |      151 |      0.947 |       28.598 |           38.072 |
| yasa       | HMC      | N1%     | cqr_ffbs       |     153 |      151 |      0.98  |       28.867 |           31.737 |
| yasa       | HMC      | N1%     | norm_reg_ffbs  |     153 |      151 |      0.98  |       30.28  |           32.075 |
| yasa       | HMC      | N1%     | norm_reg_plugc |     153 |      151 |      0.98  |       30.639 |           36.521 |
| yasa       | ST       | N2%     | ba_loa         |     153 |       44 |      0.955 |       39.19  |           42.993 |
| yasa       | ST       | N2%     | scp_abs_bc     |     153 |       44 |      0.955 |       36.085 |           41.3   |
| yasa       | ST       | N2%     | scp_abs_cal    |     153 |       44 |      0.955 |       42.499 |           45.354 |
| yasa       | ST       | N2%     | cqr_ffbs       |     153 |       44 |      0.886 |       31.08  |           38.365 |
| yasa       | ST       | N2%     | norm_reg_ffbs  |     153 |       44 |      0.886 |       31.154 |           38.81  |
| yasa       | ST       | N2%     | norm_reg_plugc |     153 |       44 |      0.909 |       37.633 |           43.737 |
| yasa       | HMC      | N2%     | ba_loa         |     153 |      151 |      0.901 |       39.164 |           55.906 |
| yasa       | HMC      | N2%     | scp_abs_bc     |     153 |      151 |      0.868 |       36.069 |           56.342 |
| yasa       | HMC      | N2%     | scp_abs_cal    |     153 |      151 |      0.874 |       42.409 |           66.633 |
| yasa       | HMC      | N2%     | cqr_ffbs       |     153 |      151 |      0.868 |       34.677 |           47.357 |
| yasa       | HMC      | N2%     | norm_reg_ffbs  |     153 |      151 |      0.887 |       36.246 |           46.745 |
| yasa       | HMC      | N2%     | norm_reg_plugc |     153 |      151 |      0.901 |       43.727 |           61.816 |
| yasa       | ST       | N3%     | ba_loa         |     153 |       44 |      0.818 |       19.416 |           32.789 |
| yasa       | ST       | N3%     | scp_abs_bc     |     153 |       44 |      0.773 |       17.616 |           34.847 |
| yasa       | ST       | N3%     | scp_abs_cal    |     153 |       44 |      0.841 |       21.76  |           33.361 |
| yasa       | ST       | N3%     | cqr_ffbs       |     153 |       44 |      0.705 |       17.384 |           35.566 |
| yasa       | ST       | N3%     | norm_reg_ffbs  |     153 |       44 |      0.705 |       16.908 |           36.175 |
| yasa       | ST       | N3%     | norm_reg_plugc |     153 |       44 |      0.795 |       19.337 |           34.916 |
| yasa       | HMC      | N3%     | ba_loa         |     153 |      151 |      0.536 |       17.47  |           79.874 |
| yasa       | HMC      | N3%     | scp_abs_bc     |     153 |      151 |      0.464 |       15.888 |           88.201 |
| yasa       | HMC      | N3%     | scp_abs_cal    |     153 |      151 |      0.47  |       19.751 |           92.525 |
| yasa       | HMC      | N3%     | cqr_ffbs       |     153 |      151 |      0.404 |       17.546 |           94.643 |
| yasa       | HMC      | N3%     | norm_reg_ffbs  |     153 |      151 |      0.377 |       17.311 |           96.927 |
| yasa       | HMC      | N3%     | norm_reg_plugc |     153 |      151 |      0.391 |       18.912 |           98.883 |
| yasa       | ST       | REM%    | ba_loa         |     153 |       44 |      0.955 |       22.57  |           25.081 |
| yasa       | ST       | REM%    | scp_abs_bc     |     153 |       44 |      0.886 |       18.284 |           24.691 |
| yasa       | ST       | REM%    | scp_abs_cal    |     153 |       44 |      0.886 |       17.404 |           25.045 |
| yasa       | ST       | REM%    | cqr_ffbs       |     153 |       44 |      0.932 |       22.509 |           25.36  |
| yasa       | ST       | REM%    | norm_reg_ffbs  |     153 |       44 |      0.818 |       19.901 |           25.657 |
| yasa       | ST       | REM%    | norm_reg_plugc |     153 |       44 |      0.864 |       14.64  |           26.656 |
| yasa       | HMC      | REM%    | ba_loa         |     153 |      151 |      0.96  |       22.107 |           25.968 |
| yasa       | HMC      | REM%    | scp_abs_bc     |     153 |      151 |      0.914 |       18.023 |           24.477 |
| yasa       | HMC      | REM%    | scp_abs_cal    |     153 |      151 |      0.927 |       17.229 |           23.146 |
| yasa       | HMC      | REM%    | cqr_ffbs       |     153 |      151 |      0.934 |       25.805 |           28.308 |
| yasa       | HMC      | REM%    | norm_reg_ffbs  |     153 |      151 |      0.914 |       25.035 |           28.151 |
| yasa       | HMC      | REM%    | norm_reg_plugc |     153 |      151 |      0.96  |       18.113 |           22.871 |
| lgbm_sc_s0 | ST       | TST     | ba_loa         |     153 |       44 |      0.932 |       88.708 |          108.185 |
| lgbm_sc_s0 | ST       | TST     | scp_abs_bc     |     153 |       44 |      0.886 |       84.275 |          107.911 |
| lgbm_sc_s0 | ST       | TST     | scp_abs_cal    |     153 |       44 |      0.909 |       85     |          133.636 |
| lgbm_sc_s0 | ST       | TST     | cqr_ffbs       |     153 |       44 |      0.909 |       67.013 |          105.911 |
| lgbm_sc_s0 | ST       | TST     | norm_reg_ffbs  |     153 |       44 |      0.909 |       62.31  |          103.442 |
| lgbm_sc_s0 | ST       | TST     | norm_reg_plugc |     153 |       44 |      0.864 |       77.178 |          115.605 |
| lgbm_sc_s0 | HMC      | TST     | ba_loa         |     153 |      151 |      0.43  |       88.708 |          467.174 |
| lgbm_sc_s0 | HMC      | TST     | scp_abs_bc     |     153 |      151 |      0.417 |       84.275 |          488.325 |
| lgbm_sc_s0 | HMC      | TST     | scp_abs_cal    |     153 |      151 |      0.411 |       85     |          545.861 |
| lgbm_sc_s0 | HMC      | TST     | cqr_ffbs       |     153 |      151 |      0.51  |       83.796 |          432.822 |
| lgbm_sc_s0 | HMC      | TST     | norm_reg_ffbs  |     153 |      151 |      0.503 |       81.704 |          434.758 |
| lgbm_sc_s0 | HMC      | TST     | norm_reg_plugc |     153 |      151 |      0.477 |      102.291 |          426.564 |
| lgbm_sc_s0 | ST       | SOL     | ba_loa         |     153 |       44 |      0.977 |       37.885 |           46.606 |
| lgbm_sc_s0 | ST       | SOL     | scp_abs_bc     |     153 |       44 |      0.977 |       26.045 |           38.685 |
| lgbm_sc_s0 | ST       | SOL     | scp_abs_cal    |     153 |       44 |      0.977 |       23.284 |           28.284 |
| lgbm_sc_s0 | ST       | SOL     | cqr_ffbs       |     153 |       44 |      0.977 |       22.802 |           23.018 |
| lgbm_sc_s0 | ST       | SOL     | norm_reg_ffbs  |     153 |       44 |      1     |       21.425 |           21.425 |
| lgbm_sc_s0 | ST       | SOL     | norm_reg_plugc |     153 |       44 |      1     |       22.508 |           22.508 |
| lgbm_sc_s0 | HMC      | SOL     | ba_loa         |     153 |      151 |      0.947 |       36.297 |           63.244 |
| lgbm_sc_s0 | HMC      | SOL     | scp_abs_bc     |     153 |      151 |      0.868 |       24.739 |           67.087 |
| lgbm_sc_s0 | HMC      | SOL     | scp_abs_cal    |     153 |      151 |      0.821 |       21.781 |           77.079 |
| lgbm_sc_s0 | HMC      | SOL     | cqr_ffbs       |     153 |      151 |      0.927 |       27.494 |           32.987 |
| lgbm_sc_s0 | HMC      | SOL     | norm_reg_ffbs  |     153 |      151 |      0.848 |       23.65  |           52.218 |
| lgbm_sc_s0 | HMC      | SOL     | norm_reg_plugc |     153 |      151 |      0.848 |       24.119 |           61.849 |
| lgbm_sc_s0 | ST       | WASO    | ba_loa         |     153 |       44 |      1     |       99.981 |           99.981 |
| lgbm_sc_s0 | ST       | WASO    | scp_abs_bc     |     153 |       44 |      0.977 |       72.436 |           75.618 |
| lgbm_sc_s0 | ST       | WASO    | scp_abs_cal    |     153 |       44 |      0.955 |       86.795 |           97.932 |
| lgbm_sc_s0 | ST       | WASO    | cqr_ffbs       |     153 |       44 |      0.932 |       59.123 |           79.339 |
| lgbm_sc_s0 | ST       | WASO    | norm_reg_ffbs  |     153 |       44 |      1     |       90.84  |           90.84  |
| lgbm_sc_s0 | ST       | WASO    | norm_reg_plugc |     153 |       44 |      0.795 |       63.731 |          101.629 |
| lgbm_sc_s0 | HMC      | WASO    | ba_loa         |     153 |      151 |      0.848 |      125.555 |          232.066 |
| lgbm_sc_s0 | HMC      | WASO    | scp_abs_bc     |     153 |      151 |      0.642 |       84.064 |          302.014 |
| lgbm_sc_s0 | HMC      | WASO    | scp_abs_cal    |     153 |      151 |      0.583 |       96.245 |          387.238 |
| lgbm_sc_s0 | HMC      | WASO    | cqr_ffbs       |     153 |      151 |      0.563 |       80.227 |          367.959 |
| lgbm_sc_s0 | HMC      | WASO    | norm_reg_ffbs  |     153 |      151 |      0.702 |      105.543 |          302.14  |
| lgbm_sc_s0 | HMC      | WASO    | norm_reg_plugc |     153 |      151 |      0.291 |       64.252 |          535.474 |
| lgbm_sc_s0 | ST       | REML    | ba_loa         |     153 |       44 |      0.818 |      123.207 |          281.967 |
| lgbm_sc_s0 | ST       | REML    | scp_abs_bc     |     153 |       44 |      0.795 |      109.049 |          295.176 |
| lgbm_sc_s0 | ST       | REML    | scp_abs_cal    |     153 |       44 |      0.864 |      146.08  |          259.034 |
| lgbm_sc_s0 | ST       | REML    | cqr_ffbs       |     153 |       44 |      0.955 |      128.266 |          129.175 |
| lgbm_sc_s0 | ST       | REML    | norm_reg_ffbs  |     153 |       44 |      0.75  |       92.625 |          175.052 |
| lgbm_sc_s0 | ST       | REML    | norm_reg_plugc |     153 |       44 |      0.932 |      155.8   |          198.073 |
| lgbm_sc_s0 | HMC      | REML    | ba_loa         |     153 |      150 |      0.747 |      118.805 |          372.667 |
| lgbm_sc_s0 | HMC      | REML    | scp_abs_bc     |     153 |      150 |      0.74  |      105.899 |          396.894 |
| lgbm_sc_s0 | HMC      | REML    | scp_abs_cal    |     153 |      150 |      0.8   |      137.273 |          366.14  |
| lgbm_sc_s0 | HMC      | REML    | cqr_ffbs       |     153 |      150 |      0.92  |      155.086 |          185.777 |
| lgbm_sc_s0 | HMC      | REML    | norm_reg_ffbs  |     153 |      150 |      0.807 |      104.417 |          266.727 |
| lgbm_sc_s0 | HMC      | REML    | norm_reg_plugc |     153 |      150 |      0.873 |      159.184 |          256.782 |
| lgbm_sc_s0 | ST       | N1%     | ba_loa         |     153 |       44 |      0.977 |       23.091 |           24.721 |
| lgbm_sc_s0 | ST       | N1%     | scp_abs_bc     |     153 |       44 |      0.977 |       24.161 |           25.397 |
| lgbm_sc_s0 | ST       | N1%     | scp_abs_cal    |     153 |       44 |      1     |       24.382 |           24.382 |
| lgbm_sc_s0 | ST       | N1%     | cqr_ffbs       |     153 |       44 |      1     |       22.785 |           22.785 |
| lgbm_sc_s0 | ST       | N1%     | norm_reg_ffbs  |     153 |       44 |      1     |       21.464 |           21.464 |
| lgbm_sc_s0 | ST       | N1%     | norm_reg_plugc |     153 |       44 |      1     |       21.247 |           21.247 |
| lgbm_sc_s0 | HMC      | N1%     | ba_loa         |     153 |      151 |      0.834 |       27.621 |           51.151 |
| lgbm_sc_s0 | HMC      | N1%     | scp_abs_bc     |     153 |      151 |      0.848 |       28.964 |           49.711 |
| lgbm_sc_s0 | HMC      | N1%     | scp_abs_cal    |     153 |      151 |      0.94  |       26.172 |           37.823 |
| lgbm_sc_s0 | HMC      | N1%     | cqr_ffbs       |     153 |      151 |      0.974 |       29.941 |           33.029 |
| lgbm_sc_s0 | HMC      | N1%     | norm_reg_ffbs  |     153 |      151 |      0.974 |       30.675 |           33.314 |
| lgbm_sc_s0 | HMC      | N1%     | norm_reg_plugc |     153 |      151 |      0.94  |       27.129 |           36.041 |
| lgbm_sc_s0 | ST       | N2%     | ba_loa         |     153 |       44 |      0.886 |       30.55  |           39.809 |
| lgbm_sc_s0 | ST       | N2%     | scp_abs_bc     |     153 |       44 |      0.886 |       29.938 |           39.892 |
| lgbm_sc_s0 | ST       | N2%     | scp_abs_cal    |     153 |       44 |      0.909 |       37.968 |           42.164 |
| lgbm_sc_s0 | ST       | N2%     | cqr_ffbs       |     153 |       44 |      0.886 |       29.318 |           36.537 |
| lgbm_sc_s0 | ST       | N2%     | norm_reg_ffbs  |     153 |       44 |      0.886 |       29.46  |           36.855 |
| lgbm_sc_s0 | ST       | N2%     | norm_reg_plugc |     153 |       44 |      0.841 |       33.589 |           41.322 |
| lgbm_sc_s0 | HMC      | N2%     | ba_loa         |     153 |      151 |      0.689 |       30.493 |           73.349 |
| lgbm_sc_s0 | HMC      | N2%     | scp_abs_bc     |     153 |      151 |      0.682 |       29.887 |           74.682 |
| lgbm_sc_s0 | HMC      | N2%     | scp_abs_cal    |     153 |      151 |      0.457 |       37.815 |          120.594 |
| lgbm_sc_s0 | HMC      | N2%     | cqr_ffbs       |     153 |      151 |      0.768 |       34.209 |           59.269 |
| lgbm_sc_s0 | HMC      | N2%     | norm_reg_ffbs  |     153 |      151 |      0.821 |       36.212 |           57.608 |
| lgbm_sc_s0 | HMC      | N2%     | norm_reg_plugc |     153 |      151 |      0.53  |       41.403 |          106.343 |
| lgbm_sc_s0 | ST       | N3%     | ba_loa         |     153 |       44 |      0.705 |       13.729 |           43.822 |
| lgbm_sc_s0 | ST       | N3%     | scp_abs_bc     |     153 |       44 |      0.75  |       14.674 |           42.117 |
| lgbm_sc_s0 | ST       | N3%     | scp_abs_cal    |     153 |       44 |      0.727 |       14.686 |           40.335 |
| lgbm_sc_s0 | ST       | N3%     | cqr_ffbs       |     153 |       44 |      0.614 |       13.007 |           40.407 |
| lgbm_sc_s0 | ST       | N3%     | norm_reg_ffbs  |     153 |       44 |      0.636 |       13.014 |           39.88  |
| lgbm_sc_s0 | ST       | N3%     | norm_reg_plugc |     153 |       44 |      0.705 |       13.795 |           39.731 |
| lgbm_sc_s0 | HMC      | N3%     | ba_loa         |     153 |      151 |      0.278 |       12.99  |          147.26  |
| lgbm_sc_s0 | HMC      | N3%     | scp_abs_bc     |     153 |      151 |      0.298 |       13.825 |          141.141 |
| lgbm_sc_s0 | HMC      | N3%     | scp_abs_cal    |     153 |      151 |      0.265 |       13.622 |          155.802 |
| lgbm_sc_s0 | HMC      | N3%     | cqr_ffbs       |     153 |      151 |      0.291 |       14.963 |          130.56  |
| lgbm_sc_s0 | HMC      | N3%     | norm_reg_ffbs  |     153 |      151 |      0.305 |       15.082 |          131.306 |
| lgbm_sc_s0 | HMC      | N3%     | norm_reg_plugc |     153 |      151 |      0.291 |       15.255 |          146.927 |
| lgbm_sc_s0 | ST       | REM%    | ba_loa         |     153 |       44 |      0.886 |       19.168 |           29.766 |
| lgbm_sc_s0 | ST       | REM%    | scp_abs_bc     |     153 |       44 |      0.864 |       15.617 |           30.562 |
| lgbm_sc_s0 | ST       | REM%    | scp_abs_cal    |     153 |       44 |      0.864 |       16.014 |           31.743 |
| lgbm_sc_s0 | ST       | REM%    | cqr_ffbs       |     153 |       44 |      0.909 |       21.159 |           26.363 |
| lgbm_sc_s0 | ST       | REM%    | norm_reg_ffbs  |     153 |       44 |      0.909 |       20.966 |           26.603 |
| lgbm_sc_s0 | ST       | REM%    | norm_reg_plugc |     153 |       44 |      0.864 |       15.599 |           30.643 |
| lgbm_sc_s0 | HMC      | REM%    | ba_loa         |     153 |      151 |      0.848 |       18.512 |           27.312 |
| lgbm_sc_s0 | HMC      | REM%    | scp_abs_bc     |     153 |      151 |      0.801 |       15.245 |           30.762 |
| lgbm_sc_s0 | HMC      | REM%    | scp_abs_cal    |     153 |      151 |      0.841 |       15.594 |           27.81  |
| lgbm_sc_s0 | HMC      | REM%    | cqr_ffbs       |     153 |      151 |      0.96  |       25.193 |           28.325 |
| lgbm_sc_s0 | HMC      | REM%    | norm_reg_ffbs  |     153 |      151 |      0.954 |       26.486 |           29.004 |
| lgbm_sc_s0 | HMC      | REM%    | norm_reg_plugc |     153 |      151 |      0.907 |       19.459 |           25.421 |


| stager     | target   | strategy   |   n_target | method        | param   |   coverage |   mean_width |   interval_score |
|:-----------|:---------|:-----------|-----------:|:--------------|:--------|-----------:|-------------:|-----------------:|
| yasa       | HMC      | pooled     |         10 | ba_loa        | N1%     |      0.941 |       29.522 |           38.242 |
| yasa       | HMC      | pooled     |         10 | ba_loa        | N2%     |      0.902 |       39.152 |           55.208 |
| yasa       | HMC      | pooled     |         10 | ba_loa        | N3%     |      0.641 |       19.267 |           68.894 |
| yasa       | HMC      | pooled     |         10 | ba_loa        | REM%    |      0.961 |       21.892 |           25.853 |
| yasa       | HMC      | pooled     |         10 | ba_loa        | REML    |      0.826 |      138.7   |          338.337 |
| yasa       | HMC      | pooled     |         10 | ba_loa        | SOL     |      0.941 |       32.814 |           47.769 |
| yasa       | HMC      | pooled     |         10 | ba_loa        | TST     |      0.905 |      113.905 |          214.016 |
| yasa       | HMC      | pooled     |         10 | ba_loa        | WASO    |      0.96  |      121.053 |          172.206 |
| yasa       | HMC      | pooled     |         10 | norm_reg_ffbs | N1%     |      0.98  |       30.007 |           31.913 |
| yasa       | HMC      | pooled     |         10 | norm_reg_ffbs | N2%     |      0.891 |       36.035 |           46.841 |
| yasa       | HMC      | pooled     |         10 | norm_reg_ffbs | N3%     |      0.495 |       20.042 |           81.21  |
| yasa       | HMC      | pooled     |         10 | norm_reg_ffbs | REM%    |      0.915 |       25.017 |           28.172 |
| yasa       | HMC      | pooled     |         10 | norm_reg_ffbs | REML    |      0.812 |      105.403 |          280.513 |
| yasa       | HMC      | pooled     |         10 | norm_reg_ffbs | SOL     |      0.913 |       26.771 |           41.388 |
| yasa       | HMC      | pooled     |         10 | norm_reg_ffbs | TST     |      0.861 |       84.881 |          181.098 |
| yasa       | HMC      | pooled     |         10 | norm_reg_ffbs | WASO    |      0.973 |      126.005 |          164.565 |
| yasa       | HMC      | pooled     |         10 | scp_abs_bc    | N1%     |      0.889 |       25.309 |           38.259 |
| yasa       | HMC      | pooled     |         10 | scp_abs_bc    | N2%     |      0.884 |       37.044 |           55.487 |
| yasa       | HMC      | pooled     |         10 | scp_abs_bc    | N3%     |      0.573 |       17.574 |           75.507 |
| yasa       | HMC      | pooled     |         10 | scp_abs_bc    | REM%    |      0.914 |       17.931 |           24.487 |
| yasa       | HMC      | pooled     |         10 | scp_abs_bc    | REML    |      0.83  |      143.919 |          331.62  |
| yasa       | HMC      | pooled     |         10 | scp_abs_bc    | SOL     |      0.906 |       23.317 |           49.614 |
| yasa       | HMC      | pooled     |         10 | scp_abs_bc    | TST     |      0.885 |      103.864 |          214.303 |
| yasa       | HMC      | pooled     |         10 | scp_abs_bc    | WASO    |      0.944 |      110.781 |          170.255 |
| yasa       | HMC      | pooled     |         20 | ba_loa        | N1%     |      0.94  |       29.383 |           38.202 |
| yasa       | HMC      | pooled     |         20 | ba_loa        | N2%     |      0.903 |       39.112 |           54.591 |
| yasa       | HMC      | pooled     |         20 | ba_loa        | N3%     |      0.71  |       20.61  |           62.248 |
| yasa       | HMC      | pooled     |         20 | ba_loa        | REM%    |      0.961 |       21.703 |           25.728 |
| yasa       | HMC      | pooled     |         20 | ba_loa        | REML    |      0.834 |      142.096 |          335.726 |
| yasa       | HMC      | pooled     |         20 | ba_loa        | SOL     |      0.941 |       32.419 |           47.705 |
| yasa       | HMC      | pooled     |         20 | ba_loa        | TST     |      0.908 |      115.845 |          213.225 |
| yasa       | HMC      | pooled     |         20 | ba_loa        | WASO    |      0.957 |      120.227 |          171.879 |
| yasa       | HMC      | pooled     |         20 | norm_reg_ffbs | N1%     |      0.98  |       29.9   |           31.857 |
| yasa       | HMC      | pooled     |         20 | norm_reg_ffbs | N2%     |      0.892 |       36.02  |           46.881 |
| yasa       | HMC      | pooled     |         20 | norm_reg_ffbs | N3%     |      0.565 |       21.633 |           73.245 |
| yasa       | HMC      | pooled     |         20 | norm_reg_ffbs | REM%    |      0.912 |       25.002 |           28.185 |
| yasa       | HMC      | pooled     |         20 | norm_reg_ffbs | REML    |      0.816 |      107.604 |          277.843 |
| yasa       | HMC      | pooled     |         20 | norm_reg_ffbs | SOL     |      0.912 |       26.688 |           41.376 |
| yasa       | HMC      | pooled     |         20 | norm_reg_ffbs | TST     |      0.864 |       85.925 |          180.519 |
| yasa       | HMC      | pooled     |         20 | norm_reg_ffbs | WASO    |      0.97  |      125.216 |          164.111 |
| yasa       | HMC      | pooled     |         20 | scp_abs_bc    | N1%     |      0.892 |       25.408 |           38.161 |
| yasa       | HMC      | pooled     |         20 | scp_abs_bc    | N2%     |      0.886 |       36.989 |           54.911 |
| yasa       | HMC      | pooled     |         20 | scp_abs_bc    | N3%     |      0.667 |       19.381 |           66.049 |
| yasa       | HMC      | pooled     |         20 | scp_abs_bc    | REM%    |      0.913 |       17.87  |           24.476 |
| yasa       | HMC      | pooled     |         20 | scp_abs_bc    | REML    |      0.837 |      145.391 |          330.907 |
| yasa       | HMC      | pooled     |         20 | scp_abs_bc    | SOL     |      0.906 |       23.271 |           49.558 |
| yasa       | HMC      | pooled     |         20 | scp_abs_bc    | TST     |      0.889 |      103.971 |          212.638 |
| yasa       | HMC      | pooled     |         20 | scp_abs_bc    | WASO    |      0.941 |      108.69  |          170.101 |
| yasa       | HMC      | pooled     |         30 | ba_loa        | N1%     |      0.94  |       29.215 |           38.265 |
| yasa       | HMC      | pooled     |         30 | ba_loa        | N2%     |      0.903 |       38.969 |           54.32  |
| yasa       | HMC      | pooled     |         30 | ba_loa        | N3%     |      0.749 |       21.693 |           57.684 |
| yasa       | HMC      | pooled     |         30 | ba_loa        | REM%    |      0.96  |       21.511 |           25.637 |
| yasa       | HMC      | pooled     |         30 | ba_loa        | REML    |      0.84  |      145.085 |          333.863 |
| yasa       | HMC      | pooled     |         30 | ba_loa        | SOL     |      0.94  |       32.046 |           47.83  |
| yasa       | HMC      | pooled     |         30 | ba_loa        | TST     |      0.91  |      117.214 |          213.003 |
| yasa       | HMC      | pooled     |         30 | ba_loa        | WASO    |      0.955 |      119.42  |          172.011 |
| yasa       | HMC      | pooled     |         30 | norm_reg_ffbs | N1%     |      0.98  |       29.457 |           31.687 |
| yasa       | HMC      | pooled     |         30 | norm_reg_ffbs | N2%     |      0.891 |       35.961 |           47.059 |
| yasa       | HMC      | pooled     |         30 | norm_reg_ffbs | N3%     |      0.621 |       22.752 |           68.168 |
| yasa       | HMC      | pooled     |         30 | norm_reg_ffbs | REM%    |      0.912 |       24.985 |           28.199 |
| yasa       | HMC      | pooled     |         30 | norm_reg_ffbs | REML    |      0.818 |      109.708 |          276.13  |
| yasa       | HMC      | pooled     |         30 | norm_reg_ffbs | SOL     |      0.91  |       26.667 |           41.489 |
| yasa       | HMC      | pooled     |         30 | norm_reg_ffbs | TST     |      0.866 |       86.918 |          180.486 |
| yasa       | HMC      | pooled     |         30 | norm_reg_ffbs | WASO    |      0.968 |      123.721 |          163.839 |
| yasa       | HMC      | pooled     |         30 | scp_abs_bc    | N1%     |      0.895 |       25.508 |           38.182 |
| yasa       | HMC      | pooled     |         30 | scp_abs_bc    | N2%     |      0.887 |       36.854 |           54.636 |
| yasa       | HMC      | pooled     |         30 | scp_abs_bc    | N3%     |      0.724 |       20.777 |           60.118 |
| yasa       | HMC      | pooled     |         30 | scp_abs_bc    | REM%    |      0.912 |       17.821 |           24.517 |
| yasa       | HMC      | pooled     |         30 | scp_abs_bc    | REML    |      0.843 |      146.804 |          330.589 |
| yasa       | HMC      | pooled     |         30 | scp_abs_bc    | SOL     |      0.904 |       23.102 |           49.881 |
| yasa       | HMC      | pooled     |         30 | scp_abs_bc    | TST     |      0.892 |      103.771 |          211.872 |
| yasa       | HMC      | pooled     |         30 | scp_abs_bc    | WASO    |      0.938 |      107.363 |          170.379 |
| yasa       | HMC      | pooled     |         50 | ba_loa        | N1%     |      0.939 |       29.005 |           38.102 |
| yasa       | HMC      | pooled     |         50 | ba_loa        | N2%     |      0.909 |       38.863 |           53.368 |
| yasa       | HMC      | pooled     |         50 | ba_loa        | N3%     |      0.787 |       23.314 |           51.627 |
| yasa       | HMC      | pooled     |         50 | ba_loa        | REM%    |      0.957 |       21.211 |           25.517 |
| yasa       | HMC      | pooled     |         50 | ba_loa        | REML    |      0.853 |      150.465 |          330.259 |
| yasa       | HMC      | pooled     |         50 | ba_loa        | SOL     |      0.94  |       31.372 |           47.757 |
| yasa       | HMC      | pooled     |         50 | ba_loa        | TST     |      0.914 |      120.148 |          211.524 |
| yasa       | HMC      | pooled     |         50 | ba_loa        | WASO    |      0.952 |      118.265 |          171.385 |
| yasa       | HMC      | pooled     |         50 | norm_reg_ffbs | N1%     |      0.98  |       28.797 |           31.279 |
| yasa       | HMC      | pooled     |         50 | norm_reg_ffbs | N2%     |      0.891 |       35.959 |           47.221 |
| yasa       | HMC      | pooled     |         50 | norm_reg_ffbs | N3%     |      0.7   |       24.366 |           62.22  |
| yasa       | HMC      | pooled     |         50 | norm_reg_ffbs | REM%    |      0.911 |       24.899 |           28.217 |
| yasa       | HMC      | pooled     |         50 | norm_reg_ffbs | REML    |      0.824 |      114.008 |          271.805 |
| yasa       | HMC      | pooled     |         50 | norm_reg_ffbs | SOL     |      0.91  |       26.55  |           41.455 |
| yasa       | HMC      | pooled     |         50 | norm_reg_ffbs | TST     |      0.869 |       88.774 |          178.944 |
| yasa       | HMC      | pooled     |         50 | norm_reg_ffbs | WASO    |      0.964 |      120.709 |          161.961 |
| yasa       | HMC      | pooled     |         50 | scp_abs_bc    | N1%     |      0.901 |       25.629 |           37.939 |
| yasa       | HMC      | pooled     |         50 | scp_abs_bc    | N2%     |      0.893 |       36.595 |           53.496 |
| yasa       | HMC      | pooled     |         50 | scp_abs_bc    | N3%     |      0.776 |       22.544 |           53.2   |
| yasa       | HMC      | pooled     |         50 | scp_abs_bc    | REM%    |      0.91  |       17.771 |           24.591 |
| yasa       | HMC      | pooled     |         50 | scp_abs_bc    | REML    |      0.854 |      149.602 |          329.62  |
| yasa       | HMC      | pooled     |         50 | scp_abs_bc    | SOL     |      0.904 |       22.901 |           49.845 |
| yasa       | HMC      | pooled     |         50 | scp_abs_bc    | TST     |      0.898 |      104.188 |          209.344 |
| yasa       | HMC      | pooled     |         50 | scp_abs_bc    | WASO    |      0.934 |      105.332 |          169.8   |
| yasa       | HMC      | target     |         10 | ba_loa        | N1%     |      0.862 |       23.398 |           42.558 |
| yasa       | HMC      | target     |         10 | ba_loa        | N2%     |      0.869 |       31.403 |           51.546 |
| yasa       | HMC      | target     |         10 | ba_loa        | N3%     |      0.851 |       23.112 |           37.502 |
| yasa       | HMC      | target     |         10 | ba_loa        | REM%    |      0.861 |       17.49  |           28.007 |
| yasa       | HMC      | target     |         10 | ba_loa        | REML    |      0.852 |      168.43  |          354.959 |
| yasa       | HMC      | target     |         10 | ba_loa        | SOL     |      0.881 |       21.243 |           52.667 |
| yasa       | HMC      | target     |         10 | ba_loa        | TST     |      0.864 |      110.603 |          225.143 |
| yasa       | HMC      | target     |         10 | ba_loa        | WASO    |      0.859 |       85.5   |          195.15  |
| yasa       | HMC      | target     |         10 | norm_reg_ffbs | N1%     |      0.911 |       22.735 |           31.936 |
| yasa       | HMC      | target     |         10 | norm_reg_ffbs | N2%     |      0.911 |       43.1   |           53.129 |
| yasa       | HMC      | target     |         10 | norm_reg_ffbs | N3%     |      0.908 |       35.621 |           45.096 |
| yasa       | HMC      | target     |         10 | norm_reg_ffbs | REM%    |      0.909 |       25.826 |           30.355 |
| yasa       | HMC      | target     |         10 | norm_reg_ffbs | REML    |      0.913 |      187.316 |          269.015 |
| yasa       | HMC      | target     |         10 | norm_reg_ffbs | SOL     |      0.916 |       29.172 |           44.982 |
| yasa       | HMC      | target     |         10 | norm_reg_ffbs | TST     |      0.906 |      129.364 |          202.967 |
| yasa       | HMC      | target     |         10 | norm_reg_ffbs | WASO    |      0.908 |      108.768 |          178.584 |
| yasa       | HMC      | target     |         10 | scp_abs_bc    | N1%     |      0.892 |       27.816 |           43.798 |
| yasa       | HMC      | target     |         10 | scp_abs_bc    | N2%     |      0.896 |       37.958 |           54.419 |
| yasa       | HMC      | target     |         10 | scp_abs_bc    | N3%     |      0.881 |       26.749 |           38.156 |
| yasa       | HMC      | target     |         10 | scp_abs_bc    | REM%    |      0.888 |       20.755 |           29.566 |
| yasa       | HMC      | target     |         10 | scp_abs_bc    | REML    |      0.895 |      214.14  |          351.743 |
| yasa       | HMC      | target     |         10 | scp_abs_bc    | SOL     |      0.907 |       28.489 |           53.372 |
| yasa       | HMC      | target     |         10 | scp_abs_bc    | TST     |      0.892 |      150.387 |          246.436 |
| yasa       | HMC      | target     |         10 | scp_abs_bc    | WASO    |      0.892 |      109.122 |          199.06  |
| yasa       | HMC      | target     |         20 | ba_loa        | N1%     |      0.893 |       24.28  |           40.391 |
| yasa       | HMC      | target     |         20 | ba_loa        | N2%     |      0.898 |       32.233 |           48.962 |
| yasa       | HMC      | target     |         20 | ba_loa        | N3%     |      0.877 |       23.633 |           35.436 |
| yasa       | HMC      | target     |         20 | ba_loa        | REM%    |      0.89  |       17.888 |           26.567 |
| yasa       | HMC      | target     |         20 | ba_loa        | REML    |      0.878 |      177.874 |          333.717 |
| yasa       | HMC      | target     |         20 | ba_loa        | SOL     |      0.902 |       22.901 |           50.46  |
| yasa       | HMC      | target     |         20 | ba_loa        | TST     |      0.899 |      121.005 |          218.069 |
| yasa       | HMC      | target     |         20 | ba_loa        | WASO    |      0.89  |       93.039 |          186.394 |
| yasa       | HMC      | target     |         20 | norm_reg_ffbs | N1%     |      0.906 |       20.537 |           30.542 |
| yasa       | HMC      | target     |         20 | norm_reg_ffbs | N2%     |      0.907 |       39.754 |           50.195 |
| yasa       | HMC      | target     |         20 | norm_reg_ffbs | N3%     |      0.899 |       34.122 |           44.312 |
| yasa       | HMC      | target     |         20 | norm_reg_ffbs | REM%    |      0.904 |       24.913 |           29.37  |
| yasa       | HMC      | target     |         20 | norm_reg_ffbs | REML    |      0.908 |      167.283 |          253.595 |
| yasa       | HMC      | target     |         20 | norm_reg_ffbs | SOL     |      0.91  |       27.011 |           43.583 |
| yasa       | HMC      | target     |         20 | norm_reg_ffbs | TST     |      0.906 |      111.385 |          187.466 |
| yasa       | HMC      | target     |         20 | norm_reg_ffbs | WASO    |      0.903 |       96.975 |          169.25  |
| yasa       | HMC      | target     |         20 | scp_abs_bc    | N1%     |      0.892 |       24.443 |           40.508 |
| yasa       | HMC      | target     |         20 | scp_abs_bc    | N2%     |      0.897 |       32.545 |           49.227 |
| yasa       | HMC      | target     |         20 | scp_abs_bc    | N3%     |      0.886 |       24.898 |           35.683 |
| yasa       | HMC      | target     |         20 | scp_abs_bc    | REM%    |      0.891 |       18.236 |           26.681 |
| yasa       | HMC      | target     |         20 | scp_abs_bc    | REML    |      0.897 |      193.865 |          330.264 |
| yasa       | HMC      | target     |         20 | scp_abs_bc    | SOL     |      0.9   |       24.513 |           51.936 |
| yasa       | HMC      | target     |         20 | scp_abs_bc    | TST     |      0.9   |      121.528 |          215.908 |
| yasa       | HMC      | target     |         20 | scp_abs_bc    | WASO    |      0.899 |       95.622 |          182.771 |
| yasa       | HMC      | target     |         30 | ba_loa        | N1%     |      0.901 |       24.36  |           39.983 |
| yasa       | HMC      | target     |         30 | ba_loa        | N2%     |      0.903 |       32.066 |           48.334 |
| yasa       | HMC      | target     |         30 | ba_loa        | N3%     |      0.886 |       23.825 |           34.56  |
| yasa       | HMC      | target     |         30 | ba_loa        | REM%    |      0.901 |       17.965 |           25.956 |
| yasa       | HMC      | target     |         30 | ba_loa        | REML    |      0.886 |      181.217 |          327.751 |
| yasa       | HMC      | target     |         30 | ba_loa        | SOL     |      0.907 |       23.361 |           49.728 |
| yasa       | HMC      | target     |         30 | ba_loa        | TST     |      0.912 |      124.378 |          214.678 |
| yasa       | HMC      | target     |         30 | ba_loa        | WASO    |      0.903 |       96.141 |          182.45  |
| yasa       | HMC      | target     |         30 | norm_reg_ffbs | N1%     |      0.901 |       19.789 |           30.383 |
| yasa       | HMC      | target     |         30 | norm_reg_ffbs | N2%     |      0.901 |       38.204 |           49.353 |
| yasa       | HMC      | target     |         30 | norm_reg_ffbs | N3%     |      0.9   |       33.835 |           43.768 |
| yasa       | HMC      | target     |         30 | norm_reg_ffbs | REM%    |      0.904 |       24.756 |           29.072 |
| yasa       | HMC      | target     |         30 | norm_reg_ffbs | REML    |      0.902 |      160.096 |          250.347 |
| yasa       | HMC      | target     |         30 | norm_reg_ffbs | SOL     |      0.904 |       26.35  |           43.401 |
| yasa       | HMC      | target     |         30 | norm_reg_ffbs | TST     |      0.904 |      106.204 |          183.586 |
| yasa       | HMC      | target     |         30 | norm_reg_ffbs | WASO    |      0.902 |       94.687 |          167.261 |
| yasa       | HMC      | target     |         30 | scp_abs_bc    | N1%     |      0.893 |       23.7   |           40     |
| yasa       | HMC      | target     |         30 | scp_abs_bc    | N2%     |      0.892 |       30.861 |           48.29  |
| yasa       | HMC      | target     |         30 | scp_abs_bc    | N3%     |      0.889 |       24.318 |           34.743 |
| yasa       | HMC      | target     |         30 | scp_abs_bc    | REM%    |      0.892 |       17.605 |           25.943 |
| yasa       | HMC      | target     |         30 | scp_abs_bc    | REML    |      0.896 |      186.953 |          326.492 |
| yasa       | HMC      | target     |         30 | scp_abs_bc    | SOL     |      0.896 |       22.282 |           51.615 |
| yasa       | HMC      | target     |         30 | scp_abs_bc    | TST     |      0.899 |      112.834 |          209.526 |
| yasa       | HMC      | target     |         30 | scp_abs_bc    | WASO    |      0.895 |       91.016 |          181.135 |
| yasa       | HMC      | target     |         50 | ba_loa        | N1%     |      0.915 |       25.081 |           39.084 |
| yasa       | HMC      | target     |         50 | ba_loa        | N2%     |      0.915 |       32.591 |           47.367 |
| yasa       | HMC      | target     |         50 | ba_loa        | N3%     |      0.894 |       24.042 |           33.96  |
| yasa       | HMC      | target     |         50 | ba_loa        | REM%    |      0.907 |       18.092 |           25.561 |
| yasa       | HMC      | target     |         50 | ba_loa        | REML    |      0.897 |      185.49  |          321.893 |
| yasa       | HMC      | target     |         50 | ba_loa        | SOL     |      0.916 |       24.082 |           48.599 |
| yasa       | HMC      | target     |         50 | ba_loa        | TST     |      0.926 |      130.121 |          210.875 |
| yasa       | HMC      | target     |         50 | ba_loa        | WASO    |      0.917 |      100.796 |          177.51  |
| yasa       | HMC      | target     |         50 | norm_reg_ffbs | N1%     |      0.899 |       19.157 |           30.215 |
| yasa       | HMC      | target     |         50 | norm_reg_ffbs | N2%     |      0.898 |       37.233 |           48.655 |
| yasa       | HMC      | target     |         50 | norm_reg_ffbs | N3%     |      0.901 |       33.711 |           43.402 |
| yasa       | HMC      | target     |         50 | norm_reg_ffbs | REM%    |      0.901 |       24.518 |           28.799 |
| yasa       | HMC      | target     |         50 | norm_reg_ffbs | REML    |      0.899 |      156.614 |          248.148 |
| yasa       | HMC      | target     |         50 | norm_reg_ffbs | SOL     |      0.904 |       26.201 |           42.964 |
| yasa       | HMC      | target     |         50 | norm_reg_ffbs | TST     |      0.903 |      102.331 |          179.037 |
| yasa       | HMC      | target     |         50 | norm_reg_ffbs | WASO    |      0.904 |       93.928 |          163.293 |
| yasa       | HMC      | target     |         50 | scp_abs_bc    | N1%     |      0.898 |       23.61  |           39.272 |
| yasa       | HMC      | target     |         50 | scp_abs_bc    | N2%     |      0.893 |       29.898 |           46.928 |
| yasa       | HMC      | target     |         50 | scp_abs_bc    | N3%     |      0.893 |       24.08  |           34.132 |
| yasa       | HMC      | target     |         50 | scp_abs_bc    | REM%    |      0.894 |       17.326 |           25.563 |
| yasa       | HMC      | target     |         50 | scp_abs_bc    | REML    |      0.898 |      184.72  |          322.438 |
| yasa       | HMC      | target     |         50 | scp_abs_bc    | SOL     |      0.898 |       21.473 |           50.892 |
| yasa       | HMC      | target     |         50 | scp_abs_bc    | TST     |      0.901 |      105.835 |          203.054 |
| yasa       | HMC      | target     |         50 | scp_abs_bc    | WASO    |      0.901 |       89.735 |          176.561 |
| yasa       | ST       | pooled     |         10 | ba_loa        | N1%     |      1     |       28.37  |           28.37  |
| yasa       | ST       | pooled     |         10 | ba_loa        | N2%     |      0.953 |       38.751 |           42.887 |
| yasa       | ST       | pooled     |         10 | ba_loa        | N3%     |      0.82  |       19.771 |           32.801 |
| yasa       | ST       | pooled     |         10 | ba_loa        | REM%    |      0.951 |       22.289 |           24.963 |
| yasa       | ST       | pooled     |         10 | ba_loa        | REML    |      0.856 |      142.891 |          215.49  |
| yasa       | ST       | pooled     |         10 | ba_loa        | SOL     |      1     |       35.962 |           35.962 |
| yasa       | ST       | pooled     |         10 | ba_loa        | TST     |      0.977 |      109.705 |          113.658 |
| yasa       | ST       | pooled     |         10 | ba_loa        | WASO    |      1     |       90.465 |           90.465 |
| yasa       | ST       | pooled     |         10 | norm_reg_ffbs | N1%     |      1     |       20.937 |           20.937 |
| yasa       | ST       | pooled     |         10 | norm_reg_ffbs | N2%     |      0.877 |       30.934 |           39.319 |
| yasa       | ST       | pooled     |         10 | norm_reg_ffbs | N3%     |      0.76  |       18.092 |           34.634 |
| yasa       | ST       | pooled     |         10 | norm_reg_ffbs | REM%    |      0.842 |       20.228 |           25.599 |
| yasa       | ST       | pooled     |         10 | norm_reg_ffbs | REML    |      0.861 |       98.698 |          166.765 |
| yasa       | ST       | pooled     |         10 | norm_reg_ffbs | SOL     |      1     |       23.179 |           23.179 |
| yasa       | ST       | pooled     |         10 | norm_reg_ffbs | TST     |      0.955 |       66.341 |           82.298 |
| yasa       | ST       | pooled     |         10 | norm_reg_ffbs | WASO    |      1     |      100.278 |          100.278 |
| yasa       | ST       | pooled     |         10 | scp_abs_bc    | N1%     |      0.977 |       24.659 |           24.787 |
| yasa       | ST       | pooled     |         10 | scp_abs_bc    | N2%     |      0.953 |       35.776 |           41.436 |
| yasa       | ST       | pooled     |         10 | scp_abs_bc    | N3%     |      0.769 |       18.007 |           34.853 |
| yasa       | ST       | pooled     |         10 | scp_abs_bc    | REM%    |      0.886 |       18.299 |           24.847 |
| yasa       | ST       | pooled     |         10 | scp_abs_bc    | REML    |      0.886 |      153.554 |          211.292 |
| yasa       | ST       | pooled     |         10 | scp_abs_bc    | SOL     |      1     |       26.425 |           26.425 |
| yasa       | ST       | pooled     |         10 | scp_abs_bc    | TST     |      0.977 |       99.982 |          106.388 |
| yasa       | ST       | pooled     |         10 | scp_abs_bc    | WASO    |      1     |       79.371 |           79.371 |
| yasa       | ST       | pooled     |         20 | ba_loa        | N1%     |      1     |       27.901 |           27.901 |
| yasa       | ST       | pooled     |         20 | ba_loa        | N2%     |      0.952 |       38.427 |           42.708 |
| yasa       | ST       | pooled     |         20 | ba_loa        | N3%     |      0.824 |       20.054 |           32.645 |
| yasa       | ST       | pooled     |         20 | ba_loa        | REM%    |      0.945 |       22.043 |           24.877 |
| yasa       | ST       | pooled     |         20 | ba_loa        | REML    |      0.85  |      142.178 |          214.484 |
| yasa       | ST       | pooled     |         20 | ba_loa        | SOL     |      1     |       35.296 |           35.296 |
| yasa       | ST       | pooled     |         20 | ba_loa        | TST     |      0.977 |      107.325 |          111.934 |
| yasa       | ST       | pooled     |         20 | ba_loa        | WASO    |      1     |       89.338 |           89.338 |
| yasa       | ST       | pooled     |         20 | norm_reg_ffbs | N1%     |      1     |       20.968 |           20.968 |
| yasa       | ST       | pooled     |         20 | norm_reg_ffbs | N2%     |      0.876 |       31.022 |           39.542 |
| yasa       | ST       | pooled     |         20 | norm_reg_ffbs | N3%     |      0.779 |       18.625 |           34.148 |
| yasa       | ST       | pooled     |         20 | norm_reg_ffbs | REM%    |      0.854 |       20.407 |           25.582 |
| yasa       | ST       | pooled     |         20 | norm_reg_ffbs | REML    |      0.864 |       99.555 |          165.22  |
| yasa       | ST       | pooled     |         20 | norm_reg_ffbs | SOL     |      1     |       22.144 |           22.144 |
| yasa       | ST       | pooled     |         20 | norm_reg_ffbs | TST     |      0.955 |       65.829 |           82.06  |
| yasa       | ST       | pooled     |         20 | norm_reg_ffbs | WASO    |      1     |       99.776 |           99.776 |
| yasa       | ST       | pooled     |         20 | scp_abs_bc    | N1%     |      0.977 |       24.133 |           24.29  |
| yasa       | ST       | pooled     |         20 | scp_abs_bc    | N2%     |      0.94  |       34.938 |           41.162 |
| yasa       | ST       | pooled     |         20 | scp_abs_bc    | N3%     |      0.778 |       18.371 |           34.592 |
| yasa       | ST       | pooled     |         20 | scp_abs_bc    | REM%    |      0.889 |       18.351 |           24.9   |
| yasa       | ST       | pooled     |         20 | scp_abs_bc    | REML    |      0.889 |      154.111 |          210.118 |
| yasa       | ST       | pooled     |         20 | scp_abs_bc    | SOL     |      1     |       26.143 |           26.143 |
| yasa       | ST       | pooled     |         20 | scp_abs_bc    | TST     |      0.977 |       98.418 |          104.835 |
| yasa       | ST       | pooled     |         20 | scp_abs_bc    | WASO    |      1     |       78.478 |           78.478 |
| yasa       | ST       | pooled     |         30 | ba_loa        | N1%     |      1     |       27.457 |           27.457 |
| yasa       | ST       | pooled     |         30 | ba_loa        | N2%     |      0.953 |       38.144 |           42.419 |
| yasa       | ST       | pooled     |         30 | ba_loa        | N3%     |      0.833 |       20.306 |           32.194 |
| yasa       | ST       | pooled     |         30 | ba_loa        | REM%    |      0.941 |       21.814 |           25     |
| yasa       | ST       | pooled     |         30 | ba_loa        | REML    |      0.837 |      141.242 |          217.837 |
| yasa       | ST       | pooled     |         30 | ba_loa        | SOL     |      1     |       34.552 |           34.552 |
| yasa       | ST       | pooled     |         30 | ba_loa        | TST     |      0.978 |      105.188 |          110.274 |
| yasa       | ST       | pooled     |         30 | ba_loa        | WASO    |      1     |       88.039 |           88.039 |
| yasa       | ST       | pooled     |         30 | norm_reg_ffbs | N1%     |      1     |       20.488 |           20.488 |
| yasa       | ST       | pooled     |         30 | norm_reg_ffbs | N2%     |      0.877 |       31.098 |           39.525 |
| yasa       | ST       | pooled     |         30 | norm_reg_ffbs | N3%     |      0.794 |       19.048 |           33.807 |
| yasa       | ST       | pooled     |         30 | norm_reg_ffbs | REM%    |      0.855 |       20.488 |           25.844 |
| yasa       | ST       | pooled     |         30 | norm_reg_ffbs | REML    |      0.862 |      100.35  |          170.735 |
| yasa       | ST       | pooled     |         30 | norm_reg_ffbs | SOL     |      1     |       21.154 |           21.154 |
| yasa       | ST       | pooled     |         30 | norm_reg_ffbs | TST     |      0.958 |       65.409 |           81.282 |
| yasa       | ST       | pooled     |         30 | norm_reg_ffbs | WASO    |      1     |       98.71  |           98.71  |
| yasa       | ST       | pooled     |         30 | scp_abs_bc    | N1%     |      0.976 |       23.537 |           23.772 |
| yasa       | ST       | pooled     |         30 | scp_abs_bc    | N2%     |      0.93  |       34.552 |           40.834 |
| yasa       | ST       | pooled     |         30 | scp_abs_bc    | N3%     |      0.793 |       18.733 |           33.953 |
| yasa       | ST       | pooled     |         30 | scp_abs_bc    | REM%    |      0.887 |       18.349 |           25.238 |
| yasa       | ST       | pooled     |         30 | scp_abs_bc    | REML    |      0.886 |      154.463 |          212.283 |
| yasa       | ST       | pooled     |         30 | scp_abs_bc    | SOL     |      1     |       24.765 |           24.765 |
| yasa       | ST       | pooled     |         30 | scp_abs_bc    | TST     |      0.978 |       97.299 |          104.214 |
| yasa       | ST       | pooled     |         30 | scp_abs_bc    | WASO    |      1     |       78.944 |           78.944 |
| yasa       | ST       | target     |         10 | ba_loa        | N1%     |      0.824 |       13.994 |           23.605 |
| yasa       | ST       | target     |         10 | ba_loa        | N2%     |      0.766 |       28.725 |           52.336 |
| yasa       | ST       | target     |         10 | ba_loa        | N3%     |      0.802 |       22.379 |           39.667 |
| yasa       | ST       | target     |         10 | ba_loa        | REM%    |      0.817 |       16.384 |           29.985 |
| yasa       | ST       | target     |         10 | ba_loa        | REML    |      0.841 |      113.969 |          244.194 |
| yasa       | ST       | target     |         10 | ba_loa        | SOL     |      0.858 |       10.67  |           19.014 |
| yasa       | ST       | target     |         10 | ba_loa        | TST     |      0.874 |       52.974 |          102.327 |
| yasa       | ST       | target     |         10 | ba_loa        | WASO    |      0.863 |       34.199 |           76.394 |
| yasa       | ST       | target     |         10 | norm_reg_ffbs | N1%     |      0.9   |       16.155 |           22.588 |
| yasa       | ST       | target     |         10 | norm_reg_ffbs | N2%     |      0.872 |       33.125 |           43.647 |
| yasa       | ST       | target     |         10 | norm_reg_ffbs | N3%     |      0.887 |       25.349 |           32.803 |
| yasa       | ST       | target     |         10 | norm_reg_ffbs | REM%    |      0.896 |       24.333 |           29.852 |
| yasa       | ST       | target     |         10 | norm_reg_ffbs | REML    |      0.897 |      139.877 |          195.593 |
| yasa       | ST       | target     |         10 | norm_reg_ffbs | SOL     |      0.893 |       18.079 |           20.811 |
| yasa       | ST       | target     |         10 | norm_reg_ffbs | TST     |      0.894 |       62.441 |           96.26  |
| yasa       | ST       | target     |         10 | norm_reg_ffbs | WASO    |      0.913 |       42.577 |           64.165 |
| yasa       | ST       | target     |         10 | scp_abs_bc    | N1%     |      0.871 |       15.715 |           22.47  |
| yasa       | ST       | target     |         10 | scp_abs_bc    | N2%     |      0.788 |       30.336 |           51.322 |
| yasa       | ST       | target     |         10 | scp_abs_bc    | N3%     |      0.842 |       25.069 |           38.327 |
| yasa       | ST       | target     |         10 | scp_abs_bc    | REM%    |      0.866 |       19.334 |           30.217 |
| yasa       | ST       | target     |         10 | scp_abs_bc    | REML    |      0.876 |      144.325 |          223.559 |
| yasa       | ST       | target     |         10 | scp_abs_bc    | SOL     |      0.888 |       12.619 |           19.836 |
| yasa       | ST       | target     |         10 | scp_abs_bc    | TST     |      0.898 |       69.47  |          107.266 |
| yasa       | ST       | target     |         10 | scp_abs_bc    | WASO    |      0.892 |       43.743 |           78.355 |
| yasa       | ST       | target     |         20 | ba_loa        | N1%     |      0.839 |       14.414 |           21.87  |
| yasa       | ST       | target     |         20 | ba_loa        | N2%     |      0.828 |       30.682 |           45.645 |
| yasa       | ST       | target     |         20 | ba_loa        | N3%     |      0.837 |       23.603 |           35.188 |
| yasa       | ST       | target     |         20 | ba_loa        | REM%    |      0.863 |       17.254 |           28.133 |
| yasa       | ST       | target     |         20 | ba_loa        | REML    |      0.849 |      122.198 |          235.068 |
| yasa       | ST       | target     |         20 | ba_loa        | SOL     |      0.899 |       11.247 |           18.055 |
| yasa       | ST       | target     |         20 | ba_loa        | TST     |      0.893 |       55.528 |           96.587 |
| yasa       | ST       | target     |         20 | ba_loa        | WASO    |      0.9   |       36.883 |           71.6   |
| yasa       | ST       | target     |         20 | norm_reg_ffbs | N1%     |      0.889 |       15.889 |           22.677 |
| yasa       | ST       | target     |         20 | norm_reg_ffbs | N2%     |      0.896 |       35.579 |           44.457 |
| yasa       | ST       | target     |         20 | norm_reg_ffbs | N3%     |      0.886 |       24.737 |           31.926 |
| yasa       | ST       | target     |         20 | norm_reg_ffbs | REM%    |      0.895 |       22.411 |           27.079 |
| yasa       | ST       | target     |         20 | norm_reg_ffbs | REML    |      0.916 |      138.97  |          190.038 |
| yasa       | ST       | target     |         20 | norm_reg_ffbs | SOL     |      0.909 |       18.476 |           20.802 |
| yasa       | ST       | target     |         20 | norm_reg_ffbs | TST     |      0.894 |       50.873 |           86.048 |
| yasa       | ST       | target     |         20 | norm_reg_ffbs | WASO    |      0.908 |       34.856 |           60.776 |
| yasa       | ST       | target     |         20 | scp_abs_bc    | N1%     |      0.87  |       15.487 |           20.963 |
| yasa       | ST       | target     |         20 | scp_abs_bc    | N2%     |      0.841 |       31.879 |           45.668 |
| yasa       | ST       | target     |         20 | scp_abs_bc    | N3%     |      0.868 |       25.564 |           34.266 |
| yasa       | ST       | target     |         20 | scp_abs_bc    | REM%    |      0.88  |       19.041 |           28.706 |
| yasa       | ST       | target     |         20 | scp_abs_bc    | REML    |      0.892 |      152.979 |          216.298 |
| yasa       | ST       | target     |         20 | scp_abs_bc    | SOL     |      0.89  |       11.663 |           19.068 |
| yasa       | ST       | target     |         20 | scp_abs_bc    | TST     |      0.896 |       60.016 |           98.25  |
| yasa       | ST       | target     |         20 | scp_abs_bc    | WASO    |      0.891 |       33.365 |           68.682 |
| yasa       | ST       | target     |         30 | ba_loa        | N1%     |      0.851 |       14.662 |           20.587 |
| yasa       | ST       | target     |         30 | ba_loa        | N2%     |      0.858 |       31.341 |           43.917 |
| yasa       | ST       | target     |         30 | ba_loa        | N3%     |      0.859 |       24.051 |           33.441 |
| yasa       | ST       | target     |         30 | ba_loa        | REM%    |      0.877 |       17.46  |           28.089 |
| yasa       | ST       | target     |         30 | ba_loa        | REML    |      0.843 |      123.84  |          236.777 |
| yasa       | ST       | target     |         30 | ba_loa        | SOL     |      0.923 |       11.44  |           17.685 |
| yasa       | ST       | target     |         30 | ba_loa        | TST     |      0.909 |       56.75  |           93.735 |
| yasa       | ST       | target     |         30 | ba_loa        | WASO    |      0.916 |       38.138 |           69.433 |
| yasa       | ST       | target     |         30 | norm_reg_ffbs | N1%     |      0.889 |       15.966 |           21.966 |
| yasa       | ST       | target     |         30 | norm_reg_ffbs | N2%     |      0.896 |       34.009 |           42.34  |
| yasa       | ST       | target     |         30 | norm_reg_ffbs | N3%     |      0.888 |       24.264 |           31.081 |
| yasa       | ST       | target     |         30 | norm_reg_ffbs | REM%    |      0.886 |       21.951 |           26.767 |
| yasa       | ST       | target     |         30 | norm_reg_ffbs | REML    |      0.902 |      121.727 |          179.084 |
| yasa       | ST       | target     |         30 | norm_reg_ffbs | SOL     |      0.904 |       17.858 |           20.239 |
| yasa       | ST       | target     |         30 | norm_reg_ffbs | TST     |      0.897 |       46.839 |           80.817 |
| yasa       | ST       | target     |         30 | norm_reg_ffbs | WASO    |      0.906 |       29.691 |           55.459 |
| yasa       | ST       | target     |         30 | scp_abs_bc    | N1%     |      0.883 |       15.51  |           19.827 |
| yasa       | ST       | target     |         30 | scp_abs_bc    | N2%     |      0.864 |       32.551 |           44.97  |
| yasa       | ST       | target     |         30 | scp_abs_bc    | N3%     |      0.884 |       26.31  |           32.932 |
| yasa       | ST       | target     |         30 | scp_abs_bc    | REM%    |      0.879 |       19.067 |           28.873 |
| yasa       | ST       | target     |         30 | scp_abs_bc    | REML    |      0.9   |      160.34  |          211.35  |
| yasa       | ST       | target     |         30 | scp_abs_bc    | SOL     |      0.906 |       10.734 |           18.029 |
| yasa       | ST       | target     |         30 | scp_abs_bc    | TST     |      0.909 |       59.21  |           95.479 |
| yasa       | ST       | target     |         30 | scp_abs_bc    | WASO    |      0.9   |       30.194 |           63.951 |
| lgbm_sc_s0 | HMC      | pooled     |         10 | ba_loa        | N1%     |      0.845 |       27.896 |           49.986 |
| lgbm_sc_s0 | HMC      | pooled     |         10 | ba_loa        | N2%     |      0.731 |       31.827 |           68.623 |
| lgbm_sc_s0 | HMC      | pooled     |         10 | ba_loa        | N3%     |      0.41  |       16.667 |          116.175 |
| lgbm_sc_s0 | HMC      | pooled     |         10 | ba_loa        | REM%    |      0.859 |       18.585 |           27.088 |
| lgbm_sc_s0 | HMC      | pooled     |         10 | ba_loa        | REML    |      0.766 |      124.69  |          363.584 |
| lgbm_sc_s0 | HMC      | pooled     |         10 | ba_loa        | SOL     |      0.945 |       36.107 |           62.921 |
| lgbm_sc_s0 | HMC      | pooled     |         10 | ba_loa        | TST     |      0.553 |      100.636 |          397.392 |
| lgbm_sc_s0 | HMC      | pooled     |         10 | ba_loa        | WASO    |      0.854 |      126.725 |          226.69  |
| lgbm_sc_s0 | HMC      | pooled     |         10 | norm_reg_ffbs | N1%     |      0.973 |       30.535 |           33.265 |
| lgbm_sc_s0 | HMC      | pooled     |         10 | norm_reg_ffbs | N2%     |      0.82  |       36.59  |           57.473 |
| lgbm_sc_s0 | HMC      | pooled     |         10 | norm_reg_ffbs | N3%     |      0.412 |       18.584 |          108.697 |
| lgbm_sc_s0 | HMC      | pooled     |         10 | norm_reg_ffbs | REM%    |      0.954 |       26.348 |           28.963 |
| lgbm_sc_s0 | HMC      | pooled     |         10 | norm_reg_ffbs | REML    |      0.808 |      104.967 |          266.472 |
| lgbm_sc_s0 | HMC      | pooled     |         10 | norm_reg_ffbs | SOL     |      0.859 |       24.165 |           51.481 |
| lgbm_sc_s0 | HMC      | pooled     |         10 | norm_reg_ffbs | TST     |      0.58  |       96.612 |          378.384 |
| lgbm_sc_s0 | HMC      | pooled     |         10 | norm_reg_ffbs | WASO    |      0.719 |      108.936 |          295.19  |
| lgbm_sc_s0 | HMC      | pooled     |         10 | scp_abs_bc    | N1%     |      0.855 |       28.545 |           49.368 |
| lgbm_sc_s0 | HMC      | pooled     |         10 | scp_abs_bc    | N2%     |      0.733 |       32.073 |           68.316 |
| lgbm_sc_s0 | HMC      | pooled     |         10 | scp_abs_bc    | N3%     |      0.39  |       15.927 |          120.402 |
| lgbm_sc_s0 | HMC      | pooled     |         10 | scp_abs_bc    | REM%    |      0.806 |       15.943 |           29.704 |
| lgbm_sc_s0 | HMC      | pooled     |         10 | scp_abs_bc    | REML    |      0.754 |      115.137 |          380.82  |
| lgbm_sc_s0 | HMC      | pooled     |         10 | scp_abs_bc    | SOL     |      0.868 |       24.69  |           66.259 |
| lgbm_sc_s0 | HMC      | pooled     |         10 | scp_abs_bc    | TST     |      0.557 |      101.026 |          398.603 |
| lgbm_sc_s0 | HMC      | pooled     |         10 | scp_abs_bc    | WASO    |      0.697 |       91.973 |          273.624 |
| lgbm_sc_s0 | HMC      | pooled     |         20 | ba_loa        | N1%     |      0.854 |       28.101 |           49.212 |
| lgbm_sc_s0 | HMC      | pooled     |         20 | ba_loa        | N2%     |      0.762 |       32.926 |           65.087 |
| lgbm_sc_s0 | HMC      | pooled     |         20 | ba_loa        | N3%     |      0.519 |       19.244 |           97.582 |
| lgbm_sc_s0 | HMC      | pooled     |         20 | ba_loa        | REM%    |      0.864 |       18.653 |           26.878 |
| lgbm_sc_s0 | HMC      | pooled     |         20 | ba_loa        | REML    |      0.782 |      130.19  |          354.354 |
| lgbm_sc_s0 | HMC      | pooled     |         20 | ba_loa        | SOL     |      0.946 |       35.897 |           62.64  |
| lgbm_sc_s0 | HMC      | pooled     |         20 | ba_loa        | TST     |      0.657 |      109.963 |          356.084 |
| lgbm_sc_s0 | HMC      | pooled     |         20 | ba_loa        | WASO    |      0.86  |      127.708 |          221.581 |
| lgbm_sc_s0 | HMC      | pooled     |         20 | norm_reg_ffbs | N1%     |      0.973 |       30.382 |           33.193 |
| lgbm_sc_s0 | HMC      | pooled     |         20 | norm_reg_ffbs | N2%     |      0.827 |       37.277 |           57.044 |
| lgbm_sc_s0 | HMC      | pooled     |         20 | norm_reg_ffbs | N3%     |      0.492 |       20.64  |           96.918 |
| lgbm_sc_s0 | HMC      | pooled     |         20 | norm_reg_ffbs | REM%    |      0.954 |       26.093 |           28.855 |
| lgbm_sc_s0 | HMC      | pooled     |         20 | norm_reg_ffbs | REML    |      0.814 |      106.59  |          264.507 |
| lgbm_sc_s0 | HMC      | pooled     |         20 | norm_reg_ffbs | SOL     |      0.863 |       24.394 |           51.174 |
| lgbm_sc_s0 | HMC      | pooled     |         20 | norm_reg_ffbs | TST     |      0.646 |      106.827 |          344.73  |
| lgbm_sc_s0 | HMC      | pooled     |         20 | norm_reg_ffbs | WASO    |      0.73  |      112.496 |          287.524 |
| lgbm_sc_s0 | HMC      | pooled     |         20 | scp_abs_bc    | N1%     |      0.861 |       28.551 |           48.9   |
| lgbm_sc_s0 | HMC      | pooled     |         20 | scp_abs_bc    | N2%     |      0.764 |       33.59  |           64.549 |
| lgbm_sc_s0 | HMC      | pooled     |         20 | scp_abs_bc    | N3%     |      0.489 |       18.293 |          102.609 |
| lgbm_sc_s0 | HMC      | pooled     |         20 | scp_abs_bc    | REM%    |      0.812 |       16.394 |           28.938 |
| lgbm_sc_s0 | HMC      | pooled     |         20 | scp_abs_bc    | REML    |      0.768 |      123.374 |          365.504 |
| lgbm_sc_s0 | HMC      | pooled     |         20 | scp_abs_bc    | SOL     |      0.87  |       24.506 |           65.723 |
| lgbm_sc_s0 | HMC      | pooled     |         20 | scp_abs_bc    | TST     |      0.681 |      115.286 |          345.562 |
| lgbm_sc_s0 | HMC      | pooled     |         20 | scp_abs_bc    | WASO    |      0.736 |       94.87  |          259.705 |
| lgbm_sc_s0 | HMC      | pooled     |         30 | ba_loa        | N1%     |      0.861 |       28.206 |           48.735 |
| lgbm_sc_s0 | HMC      | pooled     |         30 | ba_loa        | N2%     |      0.779 |       33.742 |           62.798 |
| lgbm_sc_s0 | HMC      | pooled     |         30 | ba_loa        | N3%     |      0.587 |       21.14  |           86.012 |
| lgbm_sc_s0 | HMC      | pooled     |         30 | ba_loa        | REM%    |      0.865 |       18.696 |           26.72  |
| lgbm_sc_s0 | HMC      | pooled     |         30 | ba_loa        | REML    |      0.794 |      134.543 |          348.239 |
| lgbm_sc_s0 | HMC      | pooled     |         30 | ba_loa        | SOL     |      0.946 |       35.708 |           62.527 |
| lgbm_sc_s0 | HMC      | pooled     |         30 | ba_loa        | TST     |      0.71  |      117.13  |          330.571 |
| lgbm_sc_s0 | HMC      | pooled     |         30 | ba_loa        | WASO    |      0.864 |      128.293 |          217.7   |
| lgbm_sc_s0 | HMC      | pooled     |         30 | norm_reg_ffbs | N1%     |      0.973 |       29.887 |           33.027 |
| lgbm_sc_s0 | HMC      | pooled     |         30 | norm_reg_ffbs | N2%     |      0.831 |       37.837 |           56.916 |
| lgbm_sc_s0 | HMC      | pooled     |         30 | norm_reg_ffbs | N3%     |      0.544 |       22.247 |           88.355 |
| lgbm_sc_s0 | HMC      | pooled     |         30 | norm_reg_ffbs | REM%    |      0.953 |       25.815 |           28.777 |
| lgbm_sc_s0 | HMC      | pooled     |         30 | norm_reg_ffbs | REML    |      0.818 |      108.103 |          263.099 |
| lgbm_sc_s0 | HMC      | pooled     |         30 | norm_reg_ffbs | SOL     |      0.866 |       24.619 |           51.044 |
| lgbm_sc_s0 | HMC      | pooled     |         30 | norm_reg_ffbs | TST     |      0.69  |      113.059 |          327.766 |
| lgbm_sc_s0 | HMC      | pooled     |         30 | norm_reg_ffbs | WASO    |      0.745 |      115.6   |          281.284 |


# S14. Flagging nights with clinically relevant errors (AUROC, 95% cluster-bootstrap CI; suppressed when <10 events)

| stager     | cohort   | param   |   threshold | signal            |   n |   n_events |   auroc |    lo95 |    hi95 |
|:-----------|:---------|:--------|------------:|:------------------|----:|-----------:|--------:|--------:|--------:|
| yasa       | HMC      | TST     |          30 | proposed_width    | 151 |         79 |   0.679 |   0.592 |   0.767 |
| yasa       | HMC      | TST     |          30 | ffbs_sd           | 151 |         79 |   0.685 |   0.598 |   0.772 |
| yasa       | HMC      | TST     |          30 | ind_sd            | 151 |         79 |   0.671 |   0.578 |   0.758 |
| yasa       | HMC      | TST     |          30 | mean_entropy      | 151 |         79 |   0.725 |   0.64  |   0.807 |
| yasa       | HMC      | TST     |          30 | one_minus_maxprob | 151 |         79 |   0.714 |   0.632 |   0.794 |
| yasa       | HMC      | SOL     |          15 | proposed_width    | 151 |         17 |   0.831 |   0.757 |   0.897 |
| yasa       | HMC      | SOL     |          15 | ffbs_sd           | 151 |         17 |   0.879 |   0.815 |   0.931 |
| yasa       | HMC      | SOL     |          15 | ind_sd            | 151 |         17 |   0.537 |   0.386 |   0.682 |
| yasa       | HMC      | SOL     |          15 | mean_entropy      | 151 |         17 |   0.677 |   0.524 |   0.814 |
| yasa       | HMC      | SOL     |          15 | one_minus_maxprob | 151 |         17 |   0.669 |   0.513 |   0.808 |
| yasa       | HMC      | WASO    |          30 | proposed_width    | 151 |         68 |   0.624 |   0.53  |   0.707 |
| yasa       | HMC      | WASO    |          30 | ffbs_sd           | 151 |         68 |   0.626 |   0.534 |   0.713 |
| yasa       | HMC      | WASO    |          30 | ind_sd            | 151 |         68 |   0.549 |   0.453 |   0.645 |
| yasa       | HMC      | WASO    |          30 | mean_entropy      | 151 |         68 |   0.75  |   0.67  |   0.828 |
| yasa       | HMC      | WASO    |          30 | one_minus_maxprob | 151 |         68 |   0.742 |   0.66  |   0.82  |
| yasa       | HMC      | REML    |          30 | proposed_width    | 150 |         49 |   0.682 |   0.585 |   0.765 |
| yasa       | HMC      | REML    |          30 | ffbs_sd           | 150 |         49 |   0.697 |   0.601 |   0.78  |
| yasa       | HMC      | REML    |          30 | ind_sd            | 150 |         49 |   0.463 |   0.363 |   0.567 |
| yasa       | HMC      | REML    |          30 | mean_entropy      | 150 |         49 |   0.488 |   0.385 |   0.583 |
| yasa       | HMC      | REML    |          30 | one_minus_maxprob | 150 |         49 |   0.486 |   0.384 |   0.582 |
| yasa       | HMC      | N1%     |           5 | proposed_width    | 151 |         85 |   0.72  |   0.64  |   0.792 |
| yasa       | HMC      | N1%     |           5 | ffbs_sd           | 151 |         85 |   0.705 |   0.626 |   0.778 |
| yasa       | HMC      | N1%     |           5 | ind_sd            | 151 |         85 |   0.685 |   0.602 |   0.765 |
| yasa       | HMC      | N1%     |           5 | mean_entropy      | 151 |         85 |   0.667 |   0.581 |   0.751 |
| yasa       | HMC      | N1%     |           5 | one_minus_maxprob | 151 |         85 |   0.647 |   0.554 |   0.729 |
| yasa       | HMC      | N2%     |          10 | proposed_width    | 151 |         66 |   0.772 |   0.69  |   0.847 |
| yasa       | HMC      | N2%     |          10 | ffbs_sd           | 151 |         66 |   0.772 |   0.689 |   0.847 |
| yasa       | HMC      | N2%     |          10 | ind_sd            | 151 |         66 |   0.775 |   0.697 |   0.851 |
| yasa       | HMC      | N2%     |          10 | mean_entropy      | 151 |         66 |   0.719 |   0.635 |   0.8   |
| yasa       | HMC      | N2%     |          10 | one_minus_maxprob | 151 |         66 |   0.718 |   0.631 |   0.799 |
| yasa       | HMC      | N3%     |           5 | proposed_width    | 151 |         70 |   0.584 |   0.486 |   0.674 |
| yasa       | HMC      | N3%     |           5 | ffbs_sd           | 151 |         70 |   0.602 |   0.508 |   0.691 |
| yasa       | HMC      | N3%     |           5 | ind_sd            | 151 |         70 |   0.599 |   0.509 |   0.69  |
| yasa       | HMC      | N3%     |           5 | mean_entropy      | 151 |         70 |   0.521 |   0.431 |   0.617 |
| yasa       | HMC      | N3%     |           5 | one_minus_maxprob | 151 |         70 |   0.521 |   0.43  |   0.615 |
| yasa       | HMC      | REM%    |           5 | proposed_width    | 151 |         50 |   0.566 |   0.465 |   0.659 |
| yasa       | HMC      | REM%    |           5 | ffbs_sd           | 151 |         50 |   0.6   |   0.495 |   0.694 |
| yasa       | HMC      | REM%    |           5 | ind_sd            | 151 |         50 |   0.62  |   0.527 |   0.714 |
| yasa       | HMC      | REM%    |           5 | mean_entropy      | 151 |         50 |   0.591 |   0.49  |   0.694 |
| yasa       | HMC      | REM%    |           5 | one_minus_maxprob | 151 |         50 |   0.59  |   0.485 |   0.692 |
| yasa       | SC       | TST     |          30 | proposed_width    | 153 |         50 |   0.62  |   0.525 |   0.709 |
| yasa       | SC       | TST     |          30 | ffbs_sd           | 153 |         50 |   0.633 |   0.538 |   0.723 |
| yasa       | SC       | TST     |          30 | ind_sd            | 153 |         50 |   0.649 |   0.56  |   0.741 |
| yasa       | SC       | TST     |          30 | mean_entropy      | 153 |         50 |   0.581 |   0.488 |   0.682 |
| yasa       | SC       | TST     |          30 | one_minus_maxprob | 153 |         50 |   0.576 |   0.481 |   0.67  |
| yasa       | SC       | SOL     |          15 | proposed_width    | 153 |         23 |   0.859 |   0.793 |   0.916 |
| yasa       | SC       | SOL     |          15 | ffbs_sd           | 153 |         23 |   0.861 |   0.796 |   0.917 |
| yasa       | SC       | SOL     |          15 | ind_sd            | 153 |         23 |   0.726 |   0.614 |   0.827 |
| yasa       | SC       | SOL     |          15 | mean_entropy      | 153 |         23 |   0.667 |   0.566 |   0.77  |
| yasa       | SC       | SOL     |          15 | one_minus_maxprob | 153 |         23 |   0.679 |   0.586 |   0.779 |
| yasa       | SC       | WASO    |          30 | proposed_width    | 153 |         56 |   0.499 |   0.401 |   0.588 |
| yasa       | SC       | WASO    |          30 | ffbs_sd           | 153 |         56 |   0.455 |   0.359 |   0.547 |
| yasa       | SC       | WASO    |          30 | ind_sd            | 153 |         56 |   0.355 |   0.255 |   0.46  |
| yasa       | SC       | WASO    |          30 | mean_entropy      | 153 |         56 |   0.663 |   0.563 |   0.762 |
| yasa       | SC       | WASO    |          30 | one_minus_maxprob | 153 |         56 |   0.662 |   0.56  |   0.764 |
| yasa       | SC       | REML    |          30 | proposed_width    | 153 |         29 |   0.739 |   0.647 |   0.818 |
| yasa       | SC       | REML    |          30 | ffbs_sd           | 153 |         29 |   0.741 |   0.653 |   0.818 |
| yasa       | SC       | REML    |          30 | ind_sd            | 153 |         29 |   0.61  |   0.502 |   0.728 |
| yasa       | SC       | REML    |          30 | mean_entropy      | 153 |         29 |   0.573 |   0.457 |   0.693 |
| yasa       | SC       | REML    |          30 | one_minus_maxprob | 153 |         29 |   0.597 |   0.481 |   0.714 |
| yasa       | SC       | N1%     |           5 | proposed_width    | 153 |         95 |   0.709 |   0.618 |   0.792 |
| yasa       | SC       | N1%     |           5 | ffbs_sd           | 153 |         95 |   0.717 |   0.625 |   0.798 |
| yasa       | SC       | N1%     |           5 | ind_sd            | 153 |         95 |   0.74  |   0.655 |   0.819 |
| yasa       | SC       | N1%     |           5 | mean_entropy      | 153 |         95 |   0.633 |   0.521 |   0.718 |
| yasa       | SC       | N1%     |           5 | one_minus_maxprob | 153 |         95 |   0.617 |   0.503 |   0.709 |
| yasa       | SC       | N2%     |          10 | proposed_width    | 153 |         51 |   0.651 |   0.558 |   0.735 |
| yasa       | SC       | N2%     |          10 | ffbs_sd           | 153 |         51 |   0.69  |   0.6   |   0.768 |
| yasa       | SC       | N2%     |          10 | ind_sd            | 153 |         51 |   0.674 |   0.583 |   0.757 |
| yasa       | SC       | N2%     |          10 | mean_entropy      | 153 |         51 |   0.684 |   0.603 |   0.758 |
| yasa       | SC       | N2%     |          10 | one_minus_maxprob | 153 |         51 |   0.667 |   0.589 |   0.742 |
| yasa       | SC       | N3%     |           5 | proposed_width    | 153 |         86 |   0.651 |   0.55  |   0.749 |
| yasa       | SC       | N3%     |           5 | ffbs_sd           | 153 |         86 |   0.676 |   0.578 |   0.768 |
| yasa       | SC       | N3%     |           5 | ind_sd            | 153 |         86 |   0.663 |   0.561 |   0.756 |
| yasa       | SC       | N3%     |           5 | mean_entropy      | 153 |         86 |   0.528 |   0.428 |   0.646 |
| yasa       | SC       | N3%     |           5 | one_minus_maxprob | 153 |         86 |   0.542 |   0.444 |   0.661 |
| yasa       | SC       | REM%    |           5 | proposed_width    | 153 |         37 |   0.747 |   0.646 |   0.837 |
| yasa       | SC       | REM%    |           5 | ffbs_sd           | 153 |         37 |   0.751 |   0.653 |   0.839 |
| yasa       | SC       | REM%    |           5 | ind_sd            | 153 |         37 |   0.74  |   0.645 |   0.825 |
| yasa       | SC       | REM%    |           5 | mean_entropy      | 153 |         37 |   0.683 |   0.57  |   0.787 |
| yasa       | SC       | REM%    |           5 | one_minus_maxprob | 153 |         37 |   0.688 |   0.573 |   0.789 |
| yasa       | ST       | TST     |          30 | proposed_width    |  44 |         10 |   0.803 |   0.648 |   0.94  |
| yasa       | ST       | TST     |          30 | ffbs_sd           |  44 |         10 |   0.821 |   0.645 |   0.952 |
| yasa       | ST       | TST     |          30 | ind_sd            |  44 |         10 |   0.835 |   0.695 |   0.952 |
| yasa       | ST       | TST     |          30 | mean_entropy      |  44 |         10 |   0.844 |   0.712 |   0.944 |
| yasa       | ST       | TST     |          30 | one_minus_maxprob |  44 |         10 |   0.838 |   0.722 |   0.943 |
| yasa       | ST       | SOL     |          15 | proposed_width    |  44 |          0 | nan     | nan     | nan     |
| yasa       | ST       | SOL     |          15 | ffbs_sd           |  44 |          0 | nan     | nan     | nan     |
| yasa       | ST       | SOL     |          15 | ind_sd            |  44 |          0 | nan     | nan     | nan     |
| yasa       | ST       | SOL     |          15 | mean_entropy      |  44 |          0 | nan     | nan     | nan     |
| yasa       | ST       | SOL     |          15 | one_minus_maxprob |  44 |          0 | nan     | nan     | nan     |
| yasa       | ST       | WASO    |          30 | proposed_width    |  44 |          9 | nan     | nan     | nan     |
| yasa       | ST       | WASO    |          30 | ffbs_sd           |  44 |          9 | nan     | nan     | nan     |
| yasa       | ST       | WASO    |          30 | ind_sd            |  44 |          9 | nan     | nan     | nan     |
| yasa       | ST       | WASO    |          30 | mean_entropy      |  44 |          9 | nan     | nan     | nan     |
| yasa       | ST       | WASO    |          30 | one_minus_maxprob |  44 |          9 | nan     | nan     | nan     |
| yasa       | ST       | REML    |          30 | proposed_width    |  44 |          8 | nan     | nan     | nan     |
| yasa       | ST       | REML    |          30 | ffbs_sd           |  44 |          8 | nan     | nan     | nan     |
| yasa       | ST       | REML    |          30 | ind_sd            |  44 |          8 | nan     | nan     | nan     |
| yasa       | ST       | REML    |          30 | mean_entropy      |  44 |          8 | nan     | nan     | nan     |
| yasa       | ST       | REML    |          30 | one_minus_maxprob |  44 |          8 | nan     | nan     | nan     |
| yasa       | ST       | N1%     |           5 | proposed_width    |  44 |         14 |   0.7   |   0.531 |   0.855 |
| yasa       | ST       | N1%     |           5 | ffbs_sd           |  44 |         14 |   0.75  |   0.556 |   0.893 |
| yasa       | ST       | N1%     |           5 | ind_sd            |  44 |         14 |   0.771 |   0.608 |   0.909 |
| yasa       | ST       | N1%     |           5 | mean_entropy      |  44 |         14 |   0.714 |   0.529 |   0.866 |
| yasa       | ST       | N1%     |           5 | one_minus_maxprob |  44 |         14 |   0.702 |   0.501 |   0.862 |
| yasa       | ST       | N2%     |          10 | proposed_width    |  44 |         14 |   0.369 |   0.192 |   0.59  |
| yasa       | ST       | N2%     |          10 | ffbs_sd           |  44 |         14 |   0.41  |   0.241 |   0.636 |
| yasa       | ST       | N2%     |          10 | ind_sd            |  44 |         14 |   0.402 |   0.211 |   0.654 |
| yasa       | ST       | N2%     |          10 | mean_entropy      |  44 |         14 |   0.39  |   0.179 |   0.637 |
| yasa       | ST       | N2%     |          10 | one_minus_maxprob |  44 |         14 |   0.386 |   0.194 |   0.629 |
| yasa       | ST       | N3%     |           5 | proposed_width    |  44 |         19 |   0.669 |   0.483 |   0.847 |
| yasa       | ST       | N3%     |           5 | ffbs_sd           |  44 |         19 |   0.632 |   0.448 |   0.802 |
| yasa       | ST       | N3%     |           5 | ind_sd            |  44 |         19 |   0.68  |   0.479 |   0.852 |
| yasa       | ST       | N3%     |           5 | mean_entropy      |  44 |         19 |   0.533 |   0.301 |   0.752 |
| yasa       | ST       | N3%     |           5 | one_minus_maxprob |  44 |         19 |   0.539 |   0.313 |   0.748 |
| yasa       | ST       | REM%    |           5 | proposed_width    |  44 |         12 |   0.349 |   0.174 |   0.543 |
| yasa       | ST       | REM%    |           5 | ffbs_sd           |  44 |         12 |   0.401 |   0.237 |   0.583 |
| yasa       | ST       | REM%    |           5 | ind_sd            |  44 |         12 |   0.417 |   0.245 |   0.623 |
| yasa       | ST       | REM%    |           5 | mean_entropy      |  44 |         12 |   0.323 |   0.168 |   0.516 |
| yasa       | ST       | REM%    |           5 | one_minus_maxprob |  44 |         12 |   0.32  |   0.166 |   0.501 |
| lgbm_sc_s0 | HMC      | TST     |          30 | proposed_width    | 151 |         92 |   0.614 |   0.518 |   0.705 |
| lgbm_sc_s0 | HMC      | TST     |          30 | ffbs_sd           | 151 |         92 |   0.615 |   0.519 |   0.705 |
| lgbm_sc_s0 | HMC      | TST     |          30 | ind_sd            | 151 |         92 |   0.614 |   0.519 |   0.709 |
| lgbm_sc_s0 | HMC      | TST     |          30 | mean_entropy      | 151 |         92 |   0.674 |   0.583 |   0.761 |
| lgbm_sc_s0 | HMC      | TST     |          30 | one_minus_maxprob | 151 |         92 |   0.667 |   0.574 |   0.755 |
| lgbm_sc_s0 | HMC      | SOL     |          15 | proposed_width    | 151 |         14 |   0.803 |   0.682 |   0.916 |
| lgbm_sc_s0 | HMC      | SOL     |          15 | ffbs_sd           | 151 |         14 |   0.828 |   0.719 |   0.924 |
| lgbm_sc_s0 | HMC      | SOL     |          15 | ind_sd            | 151 |         14 |   0.544 |   0.386 |   0.7   |
| lgbm_sc_s0 | HMC      | SOL     |          15 | mean_entropy      | 151 |         14 |   0.757 |   0.625 |   0.861 |
| lgbm_sc_s0 | HMC      | SOL     |          15 | one_minus_maxprob | 151 |         14 |   0.735 |   0.582 |   0.856 |
| lgbm_sc_s0 | HMC      | WASO    |          30 | proposed_width    | 151 |         84 |   0.529 |   0.441 |   0.624 |
| lgbm_sc_s0 | HMC      | WASO    |          30 | ffbs_sd           | 151 |         84 |   0.593 |   0.497 |   0.684 |
| lgbm_sc_s0 | HMC      | WASO    |          30 | ind_sd            | 151 |         84 |   0.587 |   0.497 |   0.675 |
| lgbm_sc_s0 | HMC      | WASO    |          30 | mean_entropy      | 151 |         84 |   0.64  |   0.552 |   0.733 |
| lgbm_sc_s0 | HMC      | WASO    |          30 | one_minus_maxprob | 151 |         84 |   0.633 |   0.542 |   0.726 |
| lgbm_sc_s0 | HMC      | REML    |          30 | proposed_width    | 150 |         48 |   0.606 |   0.513 |   0.707 |
| lgbm_sc_s0 | HMC      | REML    |          30 | ffbs_sd           | 150 |         48 |   0.664 |   0.573 |   0.755 |
| lgbm_sc_s0 | HMC      | REML    |          30 | ind_sd            | 150 |         48 |   0.413 |   0.306 |   0.509 |
| lgbm_sc_s0 | HMC      | REML    |          30 | mean_entropy      | 150 |         48 |   0.655 |   0.55  |   0.758 |
| lgbm_sc_s0 | HMC      | REML    |          30 | one_minus_maxprob | 150 |         48 |   0.654 |   0.551 |   0.751 |
| lgbm_sc_s0 | HMC      | N1%     |           5 | proposed_width    | 151 |        102 |   0.678 |   0.591 |   0.77  |
| lgbm_sc_s0 | HMC      | N1%     |           5 | ffbs_sd           | 151 |        102 |   0.691 |   0.606 |   0.775 |
| lgbm_sc_s0 | HMC      | N1%     |           5 | ind_sd            | 151 |        102 |   0.718 |   0.632 |   0.802 |
| lgbm_sc_s0 | HMC      | N1%     |           5 | mean_entropy      | 151 |        102 |   0.684 |   0.591 |   0.773 |
| lgbm_sc_s0 | HMC      | N1%     |           5 | one_minus_maxprob | 151 |        102 |   0.69  |   0.602 |   0.779 |
| lgbm_sc_s0 | HMC      | N2%     |          10 | proposed_width    | 151 |         67 |   0.548 |   0.45  |   0.641 |
| lgbm_sc_s0 | HMC      | N2%     |          10 | ffbs_sd           | 151 |         67 |   0.55  |   0.453 |   0.645 |
| lgbm_sc_s0 | HMC      | N2%     |          10 | ind_sd            | 151 |         67 |   0.539 |   0.441 |   0.629 |
| lgbm_sc_s0 | HMC      | N2%     |          10 | mean_entropy      | 151 |         67 |   0.501 |   0.405 |   0.6   |
| lgbm_sc_s0 | HMC      | N2%     |          10 | one_minus_maxprob | 151 |         67 |   0.487 |   0.391 |   0.584 |
| lgbm_sc_s0 | HMC      | N3%     |           5 | proposed_width    | 151 |        123 |   0.647 |   0.548 |   0.742 |
| lgbm_sc_s0 | HMC      | N3%     |           5 | ffbs_sd           | 151 |        123 |   0.649 |   0.541 |   0.758 |
| lgbm_sc_s0 | HMC      | N3%     |           5 | ind_sd            | 151 |        123 |   0.6   |   0.497 |   0.693 |
| lgbm_sc_s0 | HMC      | N3%     |           5 | mean_entropy      | 151 |        123 |   0.589 |   0.477 |   0.714 |
| lgbm_sc_s0 | HMC      | N3%     |           5 | one_minus_maxprob | 151 |        123 |   0.592 |   0.478 |   0.71  |
| lgbm_sc_s0 | HMC      | REM%    |           5 | proposed_width    | 151 |         50 |   0.604 |   0.503 |   0.7   |
| lgbm_sc_s0 | HMC      | REM%    |           5 | ffbs_sd           | 151 |         50 |   0.617 |   0.521 |   0.71  |
| lgbm_sc_s0 | HMC      | REM%    |           5 | ind_sd            | 151 |         50 |   0.589 |   0.49  |   0.683 |
| lgbm_sc_s0 | HMC      | REM%    |           5 | mean_entropy      | 151 |         50 |   0.641 |   0.537 |   0.734 |
| lgbm_sc_s0 | HMC      | REM%    |           5 | one_minus_maxprob | 151 |         50 |   0.638 |   0.539 |   0.733 |
| lgbm_sc_s0 | SC       | TST     |          30 | proposed_width    | 153 |         32 |   0.768 |   0.683 |   0.849 |
| lgbm_sc_s0 | SC       | TST     |          30 | ffbs_sd           | 153 |         32 |   0.774 |   0.689 |   0.855 |
| lgbm_sc_s0 | SC       | TST     |          30 | ind_sd            | 153 |         32 |   0.753 |   0.643 |   0.85  |
| lgbm_sc_s0 | SC       | TST     |          30 | mean_entropy      | 153 |         32 |   0.741 |   0.634 |   0.832 |
| lgbm_sc_s0 | SC       | TST     |          30 | one_minus_maxprob | 153 |         32 |   0.75  |   0.645 |   0.84  |
| lgbm_sc_s0 | SC       | SOL     |          15 | proposed_width    | 153 |         10 |   0.92  |   0.854 |   0.972 |
| lgbm_sc_s0 | SC       | SOL     |          15 | ffbs_sd           | 153 |         10 |   0.92  |   0.853 |   0.972 |
| lgbm_sc_s0 | SC       | SOL     |          15 | ind_sd            | 153 |         10 |   0.615 |   0.461 |   0.749 |
| lgbm_sc_s0 | SC       | SOL     |          15 | mean_entropy      | 153 |         10 |   0.723 |   0.534 |   0.866 |
| lgbm_sc_s0 | SC       | SOL     |          15 | one_minus_maxprob | 153 |         10 |   0.724 |   0.541 |   0.866 |
| lgbm_sc_s0 | SC       | WASO    |          30 | proposed_width    | 153 |         22 |   0.494 |   0.367 |   0.624 |
| lgbm_sc_s0 | SC       | WASO    |          30 | ffbs_sd           | 153 |         22 |   0.428 |   0.301 |   0.563 |
| lgbm_sc_s0 | SC       | WASO    |          30 | ind_sd            | 153 |         22 |   0.259 |   0.146 |   0.396 |
| lgbm_sc_s0 | SC       | WASO    |          30 | mean_entropy      | 153 |         22 |   0.64  |   0.514 |   0.76  |
| lgbm_sc_s0 | SC       | WASO    |          30 | one_minus_maxprob | 153 |         22 |   0.626 |   0.498 |   0.748 |
| lgbm_sc_s0 | SC       | REML    |          30 | proposed_width    | 153 |         25 |   0.762 |   0.66  |   0.861 |
| lgbm_sc_s0 | SC       | REML    |          30 | ffbs_sd           | 153 |         25 |   0.762 |   0.659 |   0.859 |
| lgbm_sc_s0 | SC       | REML    |          30 | ind_sd            | 153 |         25 |   0.504 |   0.37  |   0.627 |
| lgbm_sc_s0 | SC       | REML    |          30 | mean_entropy      | 153 |         25 |   0.536 |   0.395 |   0.669 |
| lgbm_sc_s0 | SC       | REML    |          30 | one_minus_maxprob | 153 |         25 |   0.542 |   0.404 |   0.676 |
| lgbm_sc_s0 | SC       | N1%     |           5 | proposed_width    | 153 |         77 |   0.715 |   0.631 |   0.792 |
| lgbm_sc_s0 | SC       | N1%     |           5 | ffbs_sd           | 153 |         77 |   0.698 |   0.61  |   0.78  |
| lgbm_sc_s0 | SC       | N1%     |           5 | ind_sd            | 153 |         77 |   0.662 |   0.573 |   0.74  |
| lgbm_sc_s0 | SC       | N1%     |           5 | mean_entropy      | 153 |         77 |   0.71  |   0.632 |   0.776 |
| lgbm_sc_s0 | SC       | N1%     |           5 | one_minus_maxprob | 153 |         77 |   0.714 |   0.634 |   0.779 |
| lgbm_sc_s0 | SC       | N2%     |          10 | proposed_width    | 153 |         45 |   0.649 |   0.543 |   0.749 |
| lgbm_sc_s0 | SC       | N2%     |          10 | ffbs_sd           | 153 |         45 |   0.669 |   0.569 |   0.764 |
| lgbm_sc_s0 | SC       | N2%     |          10 | ind_sd            | 153 |         45 |   0.643 |   0.541 |   0.741 |
| lgbm_sc_s0 | SC       | N2%     |          10 | mean_entropy      | 153 |         45 |   0.709 |   0.607 |   0.799 |
| lgbm_sc_s0 | SC       | N2%     |          10 | one_minus_maxprob | 153 |         45 |   0.717 |   0.62  |   0.803 |
| lgbm_sc_s0 | SC       | N3%     |           5 | proposed_width    | 153 |         32 |   0.754 |   0.646 |   0.843 |
| lgbm_sc_s0 | SC       | N3%     |           5 | ffbs_sd           | 153 |         32 |   0.777 |   0.668 |   0.86  |
| lgbm_sc_s0 | SC       | N3%     |           5 | ind_sd            | 153 |         32 |   0.769 |   0.653 |   0.854 |
| lgbm_sc_s0 | SC       | N3%     |           5 | mean_entropy      | 153 |         32 |   0.587 |   0.476 |   0.693 |
| lgbm_sc_s0 | SC       | N3%     |           5 | one_minus_maxprob | 153 |         32 |   0.585 |   0.478 |   0.692 |
| lgbm_sc_s0 | SC       | REM%    |           5 | proposed_width    | 153 |         30 |   0.608 |   0.486 |   0.712 |
| lgbm_sc_s0 | SC       | REM%    |           5 | ffbs_sd           | 153 |         30 |   0.615 |   0.5   |   0.714 |
| lgbm_sc_s0 | SC       | REM%    |           5 | ind_sd            | 153 |         30 |   0.698 |   0.585 |   0.791 |
| lgbm_sc_s0 | SC       | REM%    |           5 | mean_entropy      | 153 |         30 |   0.63  |   0.48  |   0.751 |
| lgbm_sc_s0 | SC       | REM%    |           5 | one_minus_maxprob | 153 |         30 |   0.629 |   0.481 |   0.752 |
| lgbm_sc_s0 | ST       | TST     |          30 | proposed_width    |  44 |          6 | nan     | nan     | nan     |
| lgbm_sc_s0 | ST       | TST     |          30 | ffbs_sd           |  44 |          6 | nan     | nan     | nan     |
| lgbm_sc_s0 | ST       | TST     |          30 | ind_sd            |  44 |          6 | nan     | nan     | nan     |
| lgbm_sc_s0 | ST       | TST     |          30 | mean_entropy      |  44 |          6 | nan     | nan     | nan     |
| lgbm_sc_s0 | ST       | TST     |          30 | one_minus_maxprob |  44 |          6 | nan     | nan     | nan     |
| lgbm_sc_s0 | ST       | SOL     |          15 | proposed_width    |  44 |          1 | nan     | nan     | nan     |
| lgbm_sc_s0 | ST       | SOL     |          15 | ffbs_sd           |  44 |          1 | nan     | nan     | nan     |
| lgbm_sc_s0 | ST       | SOL     |          15 | ind_sd            |  44 |          1 | nan     | nan     | nan     |
| lgbm_sc_s0 | ST       | SOL     |          15 | mean_entropy      |  44 |          1 | nan     | nan     | nan     |
| lgbm_sc_s0 | ST       | SOL     |          15 | one_minus_maxprob |  44 |          1 | nan     | nan     | nan     |
| lgbm_sc_s0 | ST       | WASO    |          30 | proposed_width    |  44 |          6 | nan     | nan     | nan     |
| lgbm_sc_s0 | ST       | WASO    |          30 | ffbs_sd           |  44 |          6 | nan     | nan     | nan     |
| lgbm_sc_s0 | ST       | WASO    |          30 | ind_sd            |  44 |          6 | nan     | nan     | nan     |
| lgbm_sc_s0 | ST       | WASO    |          30 | mean_entropy      |  44 |          6 | nan     | nan     | nan     |
| lgbm_sc_s0 | ST       | WASO    |          30 | one_minus_maxprob |  44 |          6 | nan     | nan     | nan     |
| lgbm_sc_s0 | ST       | REML    |          30 | proposed_width    |  44 |         12 |   0.745 |   0.534 |   0.905 |
| lgbm_sc_s0 | ST       | REML    |          30 | ffbs_sd           |  44 |         12 |   0.755 |   0.582 |   0.899 |
| lgbm_sc_s0 | ST       | REML    |          30 | ind_sd            |  44 |         12 |   0.286 |   0.113 |   0.49  |
| lgbm_sc_s0 | ST       | REML    |          30 | mean_entropy      |  44 |         12 |   0.607 |   0.344 |   0.828 |
| lgbm_sc_s0 | ST       | REML    |          30 | one_minus_maxprob |  44 |         12 |   0.596 |   0.337 |   0.821 |
| lgbm_sc_s0 | ST       | N1%     |           5 | proposed_width    |  44 |         15 |   0.811 |   0.623 |   0.95  |
| lgbm_sc_s0 | ST       | N1%     |           5 | ffbs_sd           |  44 |         15 |   0.823 |   0.647 |   0.948 |
| lgbm_sc_s0 | ST       | N1%     |           5 | ind_sd            |  44 |         15 |   0.834 |   0.676 |   0.948 |
| lgbm_sc_s0 | ST       | N1%     |           5 | mean_entropy      |  44 |         15 |   0.908 |   0.792 |   0.982 |
| lgbm_sc_s0 | ST       | N1%     |           5 | one_minus_maxprob |  44 |         15 |   0.897 |   0.765 |   0.979 |
| lgbm_sc_s0 | ST       | N2%     |          10 | proposed_width    |  44 |         17 |   0.51  |   0.299 |   0.715 |
| lgbm_sc_s0 | ST       | N2%     |          10 | ffbs_sd           |  44 |         17 |   0.534 |   0.328 |   0.731 |
| lgbm_sc_s0 | ST       | N2%     |          10 | ind_sd            |  44 |         17 |   0.523 |   0.317 |   0.718 |
| lgbm_sc_s0 | ST       | N2%     |          10 | mean_entropy      |  44 |         17 |   0.525 |   0.306 |   0.729 |
| lgbm_sc_s0 | ST       | N2%     |          10 | one_minus_maxprob |  44 |         17 |   0.532 |   0.307 |   0.731 |
| lgbm_sc_s0 | ST       | N3%     |           5 | proposed_width    |  44 |         21 |   0.578 |   0.357 |   0.765 |
| lgbm_sc_s0 | ST       | N3%     |           5 | ffbs_sd           |  44 |         21 |   0.743 |   0.573 |   0.878 |
| lgbm_sc_s0 | ST       | N3%     |           5 | ind_sd            |  44 |         21 |   0.762 |   0.588 |   0.894 |
| lgbm_sc_s0 | ST       | N3%     |           5 | mean_entropy      |  44 |         21 |   0.559 |   0.323 |   0.784 |
| lgbm_sc_s0 | ST       | N3%     |           5 | one_minus_maxprob |  44 |         21 |   0.565 |   0.333 |   0.786 |
| lgbm_sc_s0 | ST       | REM%    |           5 | proposed_width    |  44 |         10 |   0.512 |   0.241 |   0.76  |
| lgbm_sc_s0 | ST       | REM%    |           5 | ffbs_sd           |  44 |         10 |   0.553 |   0.328 |   0.768 |
| lgbm_sc_s0 | ST       | REM%    |           5 | ind_sd            |  44 |         10 |   0.582 |   0.338 |   0.809 |
| lgbm_sc_s0 | ST       | REM%    |           5 | mean_entropy      |  44 |         10 |   0.456 |   0.168 |   0.753 |
| lgbm_sc_s0 | ST       | REM%    |           5 | one_minus_maxprob |  44 |         10 |   0.441 |   0.155 |   0.737 |


# S15. Computational cost (median per night, one CPU core)

|    M |   n_epochs |   t_stager_s |   t_ffbs_s |   t_params_s |   samples_MB |
|-----:|-----------:|-------------:|-----------:|-------------:|-------------:|
|  100 |     1028.5 |       1.4222 |     0.0019 |       0.001  |       0.1028 |
|  300 |     1028.5 |       1.4222 |     0.0044 |       0.0027 |       0.3086 |
| 1000 |     1028.5 |       1.4222 |     0.0132 |       0.0095 |       1.0285 |


# S16. Datasets and data-leakage audit

## Datasets and data-leakage audit (Phases 7–8)

## Datasets
| | Sleep-EDF SC | Sleep-EDF ST | HMC |
|---|---|---|---|
| Source | PhysioNet sleep-edfx v1.0.0 (Kemp et al. 2000) | same | PhysioNet hmc-sleep-staging v1.1 (Alvarez-Estevez & Rijsman 2021) |
| Licence | Open Data Commons Attribution v1.0 | same | CC BY 4.0 |
| Population | Healthy community-dwelling adults 25–101 y, ambulatory home recordings (1987–1991) | 22 adults with mild difficulty falling asleep; in-hospital; placebo and temazepam nights (1994) | Consecutive clinical PSGs at a Dutch sleep centre (2018), mixed sleep disorders |
| Nights / subjects | 153 / 78 (2 nights per subject except 3 subjects) | 44 / 22 (2 nights per subject) | 151 / 151 |
| Scoring | R&K (S3+S4 merged to N3), one scorer per night | R&K | AASM, one scorer per night |
| Signals used | Fpz-Cz EEG, horizontal EOG (100 Hz) | same | C4-M1 EEG, E1-M2 EOG (256 Hz → 100 Hz); F4-M1 and E1–E2 cached for montage analyses |
| Lights-off/on | lights-off in SC-subjects.xls; no lights-on | lights-off in ST-subjects.xls | both annotated |
| Known limitations | old analogue recordings; R&K not AASM; EMG only as 1-Hz envelope; daytime naps in 20-h files | small n; drug condition | no per-subject demographics released; single scorer |

## Leakage audit
| Risk | Assessment | Mitigation implemented |
|---|---|---|
| Subject leakage (two nights of the same person in train and test) | Real for SC and ST | All splits (stager CV, HMM cross-fitting, conformal calibration/test splits, LOSO, few-night recalibration) are grouped by **subject**. |
| Leakage through analysis window | Cropping to "30 min before first / after last sleep epoch" (common in Sleep-EDF papers) uses the reference hypnogram | Windows defined only by lights-off/lights-on metadata and a fixed 10-h SC window; never by labels. |
| Leakage through HMM parameters | Transition matrix, prior, calibration and tau use labels | Fitted only on labelled nights that exclude the evaluated night: within-cohort 5-fold cross-fitting by subject; cross-cohort uses SC only. |
| Leakage into the base stagers | S2 trained on SC | SC predictions are out-of-fold (subject-grouped 5-fold); S1 (YASA) never saw any of the three cohorts. |
| Pre-processing leakage | YASA features normalise within each night | Per-night normalisation uses only that night's signal (unsupervised, test-time permissible); no cross-night statistics. |
| Test contamination via hyper-parameter tuning | Possible if tuned on evaluation nights | Stager hyper-parameters fixed a priori; the only fitted HMM quantity (tau) is fitted on source/training-fold nights; conformal methods and all thresholds pre-specified (PREREGISTERED_PROTOCOL.md). |
| Duplicate / near-duplicate nights | None expected; each PSG file is a distinct night | File-level uniqueness checked via PhysioNet SHA256 manifests. |
| Label leakage via unscored epochs | "?"/movement epochs | Marked −1 and excluded identically from reference and automatic parameters. |
| Temporal leakage | Not applicable (no longitudinal prediction) | – |
| Few-night recalibration | Target calibration nights could share subjects with test nights | Target calibration nights are whole subjects disjoint from test subjects. |


# S17. Conditional coverage by difficulty and exploratory Mondrian calibration (LOSO; quartiles of plug-in accuracy used only for evaluation)

| stager     | cohort   | method           | subset     |   coverage |   mean_width |   interval_score |    n |
|:-----------|:---------|:-----------------|:-----------|-----------:|-------------:|-----------------:|-----:|
| yasa       | HMC      | dfloa            | Q1 (worst) |      0.757 |       59.676 |          184.186 |  304 |
| yasa       | HMC      | dfloa            | Q2         |      0.941 |       60.595 |           82.292 |  304 |
| yasa       | HMC      | dfloa            | Q3         |      0.943 |       60.192 |           90.602 |  296 |
| yasa       | HMC      | dfloa            | Q4 (best)  |      0.96  |       59.912 |           83.98  |  303 |
| yasa       | HMC      | mondrian_entropy | Q1 (worst) |      0.836 |       73.183 |          120.957 |  304 |
| yasa       | HMC      | mondrian_entropy | Q2         |      0.938 |       64.647 |           80.912 |  304 |
| yasa       | HMC      | mondrian_entropy | Q3         |      0.929 |       56.325 |           80.057 |  296 |
| yasa       | HMC      | mondrian_entropy | Q4 (best)  |      0.927 |       50.41  |           90.296 |  303 |
| yasa       | HMC      | mondrian_sd      | Q1 (worst) |      0.839 |       71.319 |          118.207 |  304 |
| yasa       | HMC      | mondrian_sd      | Q2         |      0.928 |       60.574 |           81.345 |  304 |
| yasa       | HMC      | mondrian_sd      | Q3         |      0.932 |       59.585 |           77.878 |  296 |
| yasa       | HMC      | mondrian_sd      | Q4 (best)  |      0.931 |       57.841 |           86.056 |  303 |
| yasa       | HMC      | proposed         | Q1 (worst) |      0.812 |       58.992 |          135.257 |  304 |
| yasa       | HMC      | proposed         | Q2         |      0.918 |       55.45  |           87.352 |  304 |
| yasa       | HMC      | proposed         | Q3         |      0.939 |       55.548 |           82.916 |  296 |
| yasa       | HMC      | proposed         | Q4 (best)  |      0.934 |       54.665 |           95.26  |  303 |
| yasa       | SC       | dfloa            | Q1 (worst) |      0.788 |       60.659 |          130.586 |  320 |
| yasa       | SC       | dfloa            | Q2         |      0.899 |       60.41  |          120.173 |  296 |
| yasa       | SC       | dfloa            | Q3         |      0.951 |       57.3   |           71.749 |  304 |
| yasa       | SC       | dfloa            | Q4 (best)  |      0.96  |       57.262 |           90.245 |  304 |
| yasa       | SC       | mondrian_entropy | Q1 (worst) |      0.844 |       68.645 |          108.046 |  320 |
| yasa       | SC       | mondrian_entropy | Q2         |      0.912 |       66.889 |          103.018 |  296 |
| yasa       | SC       | mondrian_entropy | Q3         |      0.944 |       62.546 |           80.334 |  304 |
| yasa       | SC       | mondrian_entropy | Q4 (best)  |      0.938 |       63.904 |          105.71  |  304 |
| yasa       | SC       | mondrian_sd      | Q1 (worst) |      0.831 |       68.598 |          107.477 |  320 |
| yasa       | SC       | mondrian_sd      | Q2         |      0.895 |       68.208 |          104.946 |  296 |
| yasa       | SC       | mondrian_sd      | Q3         |      0.951 |       64.468 |           78.914 |  304 |
| yasa       | SC       | mondrian_sd      | Q4 (best)  |      0.957 |       66.263 |           93.96  |  304 |
| yasa       | SC       | proposed         | Q1 (worst) |      0.809 |       64.018 |          113.78  |  320 |
| yasa       | SC       | proposed         | Q2         |      0.912 |       64.896 |          103.781 |  296 |
| yasa       | SC       | proposed         | Q3         |      0.954 |       63.552 |           79.876 |  304 |
| yasa       | SC       | proposed         | Q4 (best)  |      0.934 |       65.434 |          106.162 |  304 |
| yasa       | ST       | dfloa            | Q1 (worst) |      0.784 |       45.416 |           89.679 |   88 |
| yasa       | ST       | dfloa            | Q2         |      0.864 |       43.724 |           61.192 |   88 |
| yasa       | ST       | dfloa            | Q3         |      0.966 |       45.703 |           51.656 |   88 |
| yasa       | ST       | dfloa            | Q4 (best)  |      0.989 |       46.586 |           48.177 |   88 |
| yasa       | ST       | mondrian_entropy | Q1 (worst) |      0.864 |       44.692 |           61.857 |   88 |
| yasa       | ST       | mondrian_entropy | Q2         |      0.864 |       40.666 |           60.036 |   88 |
| yasa       | ST       | mondrian_entropy | Q3         |      0.92  |       42.719 |           57.037 |   88 |
| yasa       | ST       | mondrian_entropy | Q4 (best)  |      0.932 |       43.207 |           53.437 |   88 |
| yasa       | ST       | mondrian_sd      | Q1 (worst) |      0.818 |       43.426 |           66.52  |   88 |
| yasa       | ST       | mondrian_sd      | Q2         |      0.92  |       39.742 |           55.81  |   88 |
| yasa       | ST       | mondrian_sd      | Q3         |      0.932 |       41.447 |           61.853 |   88 |
| yasa       | ST       | mondrian_sd      | Q4 (best)  |      0.943 |       42.07  |           53.249 |   88 |
| yasa       | ST       | proposed         | Q1 (worst) |      0.83  |       43.044 |           66.17  |   88 |
| yasa       | ST       | proposed         | Q2         |      0.92  |       40.06  |           61.239 |   88 |
| yasa       | ST       | proposed         | Q3         |      0.932 |       41.412 |           61.521 |   88 |
| yasa       | ST       | proposed         | Q4 (best)  |      0.943 |       42.564 |           54.739 |   88 |
| yasa       | HMC      | dfloa            | all        |      0.9   |       60.094 |          110.417 | 1207 |
| yasa       | HMC      | mondrian_entropy | all        |      0.907 |       61.182 |           93.144 | 1207 |
| yasa       | HMC      | mondrian_sd      | all        |      0.907 |       62.352 |           90.962 | 1207 |
| yasa       | HMC      | proposed         | all        |      0.901 |       56.169 |          100.315 | 1207 |
| yasa       | SC       | dfloa            | all        |      0.898 |       58.921 |          103.435 | 1224 |
| yasa       | SC       | mondrian_entropy | all        |      0.908 |       65.528 |           99.367 | 1224 |
| yasa       | SC       | mondrian_sd      | all        |      0.908 |       66.898 |           96.414 | 1224 |
| yasa       | SC       | proposed         | all        |      0.901 |       64.466 |          101.049 | 1224 |
| yasa       | ST       | dfloa            | all        |      0.901 |       45.357 |           62.676 |  352 |
| yasa       | ST       | mondrian_entropy | all        |      0.895 |       42.821 |           58.092 |  352 |
| yasa       | ST       | mondrian_sd      | all        |      0.903 |       41.671 |           59.358 |  352 |
| yasa       | ST       | proposed         | all        |      0.906 |       41.77  |           60.917 |  352 |
| lgbm_sc_s0 | HMC      | dfloa            | Q1 (worst) |      0.799 |       75.055 |          159.589 |  304 |
| lgbm_sc_s0 | HMC      | dfloa            | Q2         |      0.901 |       74.918 |          117.506 |  304 |
| lgbm_sc_s0 | HMC      | dfloa            | Q3         |      0.915 |       74.527 |          115.813 |  295 |
| lgbm_sc_s0 | HMC      | dfloa            | Q4 (best)  |      0.98  |       74.647 |           81.598 |  304 |
| lgbm_sc_s0 | HMC      | mondrian_entropy | Q1 (worst) |      0.891 |       83.007 |          124.516 |  304 |
| lgbm_sc_s0 | HMC      | mondrian_entropy | Q2         |      0.914 |       73.336 |           97.939 |  304 |
| lgbm_sc_s0 | HMC      | mondrian_entropy | Q3         |      0.915 |       65.325 |           95.662 |  295 |
| lgbm_sc_s0 | HMC      | mondrian_entropy | Q4 (best)  |      0.908 |       57.817 |           86.586 |  304 |
| lgbm_sc_s0 | HMC      | mondrian_sd      | Q1 (worst) |      0.875 |       72.063 |          132.546 |  304 |
| lgbm_sc_s0 | HMC      | mondrian_sd      | Q2         |      0.908 |       67.852 |           88.112 |  304 |
| lgbm_sc_s0 | HMC      | mondrian_sd      | Q3         |      0.912 |       67.402 |           96.94  |  295 |
| lgbm_sc_s0 | HMC      | mondrian_sd      | Q4 (best)  |      0.934 |       72.876 |           89.695 |  304 |
| lgbm_sc_s0 | HMC      | proposed         | Q1 (worst) |      0.836 |       67.656 |          133.683 |  304 |
| lgbm_sc_s0 | HMC      | proposed         | Q2         |      0.921 |       67.087 |          110.877 |  304 |
| lgbm_sc_s0 | HMC      | proposed         | Q3         |      0.905 |       66.874 |          124.489 |  295 |
| lgbm_sc_s0 | HMC      | proposed         | Q4 (best)  |      0.941 |       69.291 |           95.695 |  304 |
| lgbm_sc_s0 | SC       | dfloa            | Q1 (worst) |      0.756 |       47.28  |          104.864 |  312 |
| lgbm_sc_s0 | SC       | dfloa            | Q2         |      0.908 |       47.313 |          103.502 |  304 |
| lgbm_sc_s0 | SC       | dfloa            | Q3         |      0.951 |       45.983 |           57.584 |  304 |
| lgbm_sc_s0 | SC       | dfloa            | Q4 (best)  |      0.98  |       45.295 |           85.852 |  304 |
| lgbm_sc_s0 | SC       | mondrian_entropy | Q1 (worst) |      0.862 |       60.397 |           93.323 |  312 |
| lgbm_sc_s0 | SC       | mondrian_entropy | Q2         |      0.911 |       57.104 |           94.536 |  304 |
| lgbm_sc_s0 | SC       | mondrian_entropy | Q3         |      0.905 |       52.258 |           74.412 |  304 |
| lgbm_sc_s0 | SC       | mondrian_entropy | Q4 (best)  |      0.947 |       50.927 |           80.056 |  304 |
| lgbm_sc_s0 | SC       | mondrian_sd      | Q1 (worst) |      0.856 |       60.851 |           90.222 |  312 |
| lgbm_sc_s0 | SC       | mondrian_sd      | Q2         |      0.895 |       55.628 |           89.214 |  304 |
| lgbm_sc_s0 | SC       | mondrian_sd      | Q3         |      0.928 |       53.916 |           70.514 |  304 |
| lgbm_sc_s0 | SC       | mondrian_sd      | Q4 (best)  |      0.954 |       50.214 |           78.54  |  304 |
| lgbm_sc_s0 | SC       | proposed         | Q1 (worst) |      0.83  |       55.083 |           97.385 |  312 |
| lgbm_sc_s0 | SC       | proposed         | Q2         |      0.891 |       53.231 |           90.206 |  304 |
| lgbm_sc_s0 | SC       | proposed         | Q3         |      0.931 |       53.636 |           72.153 |  304 |
| lgbm_sc_s0 | SC       | proposed         | Q4 (best)  |      0.957 |       52.949 |           83.333 |  304 |
| lgbm_sc_s0 | ST       | dfloa            | Q1 (worst) |      0.773 |       47.666 |           82.282 |   88 |
| lgbm_sc_s0 | ST       | dfloa            | Q2         |      0.92  |       49.52  |           60.283 |   88 |
| lgbm_sc_s0 | ST       | dfloa            | Q3         |      0.92  |       50.543 |           75.608 |   88 |
| lgbm_sc_s0 | ST       | dfloa            | Q4 (best)  |      0.943 |       50.848 |           53.693 |   88 |
| lgbm_sc_s0 | ST       | mondrian_entropy | Q1 (worst) |      0.841 |       43.874 |           69.583 |   88 |
| lgbm_sc_s0 | ST       | mondrian_entropy | Q2         |      0.909 |       39.408 |           52.702 |   88 |
| lgbm_sc_s0 | ST       | mondrian_entropy | Q3         |      0.954 |       44.053 |           52.896 |   88 |
| lgbm_sc_s0 | ST       | mondrian_entropy | Q4 (best)  |      0.886 |       40.853 |           61.47  |   88 |
| lgbm_sc_s0 | ST       | mondrian_sd      | Q1 (worst) |      0.852 |       43.605 |           68.791 |   88 |
| lgbm_sc_s0 | ST       | mondrian_sd      | Q2         |      0.932 |       39.297 |           48.456 |   88 |
| lgbm_sc_s0 | ST       | mondrian_sd      | Q3         |      0.943 |       44.275 |           51.591 |   88 |
| lgbm_sc_s0 | ST       | mondrian_sd      | Q4 (best)  |      0.864 |       39.868 |           57.163 |   88 |
| lgbm_sc_s0 | ST       | proposed         | Q1 (worst) |      0.852 |       43.227 |           65.662 |   88 |
| lgbm_sc_s0 | ST       | proposed         | Q2         |      0.92  |       39.716 |           49.802 |   88 |
| lgbm_sc_s0 | ST       | proposed         | Q3         |      0.92  |       42.572 |           56.994 |   88 |
| lgbm_sc_s0 | ST       | proposed         | Q4 (best)  |      0.92  |       41.06  |           56.306 |   88 |
| lgbm_sc_s0 | HMC      | dfloa            | all        |      0.899 |       74.789 |          118.647 | 1207 |
| lgbm_sc_s0 | HMC      | mondrian_entropy | all        |      0.907 |       69.905 |          101.217 | 1207 |
| lgbm_sc_s0 | HMC      | mondrian_sd      | all        |      0.907 |       70.068 |          101.86  | 1207 |
| lgbm_sc_s0 | HMC      | proposed         | all        |      0.901 |       67.733 |          116.124 | 1207 |
| lgbm_sc_s0 | SC       | dfloa            | all        |      0.898 |       46.473 |           88.061 | 1224 |
| lgbm_sc_s0 | SC       | mondrian_entropy | all        |      0.906 |       55.206 |           85.632 | 1224 |
| lgbm_sc_s0 | SC       | mondrian_sd      | all        |      0.908 |       55.189 |           82.176 | 1224 |
| lgbm_sc_s0 | SC       | proposed         | all        |      0.902 |       53.734 |           85.845 | 1224 |
| lgbm_sc_s0 | ST       | dfloa            | all        |      0.889 |       49.644 |           67.967 |  352 |
| lgbm_sc_s0 | ST       | mondrian_entropy | all        |      0.898 |       42.047 |           59.163 |  352 |
| lgbm_sc_s0 | ST       | mondrian_sd      | all        |      0.898 |       41.761 |           56.5   |  352 |
| lgbm_sc_s0 | ST       | proposed         | all        |      0.903 |       41.644 |           57.191 |  352 |


**Few-night recalibration: probability that realised coverage of the remaining target nights falls below 0.80 (500 repetitions)**



*yasa*

| target   |   n_target | method        | param   |   P(coverage<0.80) |
|:---------|-----------:|:--------------|:--------|-------------------:|
| HMC      |         10 | ba_loa        | N1%     |              0.26  |
| HMC      |         10 | ba_loa        | N2%     |              0.214 |
| HMC      |         10 | ba_loa        | N3%     |              0.282 |
| HMC      |         10 | ba_loa        | REM%    |              0.242 |
| HMC      |         10 | ba_loa        | REML    |              0.276 |
| HMC      |         10 | ba_loa        | SOL     |              0.162 |
| HMC      |         10 | ba_loa        | TST     |              0.23  |
| HMC      |         10 | ba_loa        | WASO    |              0.248 |
| HMC      |         10 | norm_reg_ffbs | N1%     |              0.096 |
| HMC      |         10 | norm_reg_ffbs | N2%     |              0.11  |
| HMC      |         10 | norm_reg_ffbs | N3%     |              0.118 |
| HMC      |         10 | norm_reg_ffbs | REM%    |              0.104 |
| HMC      |         10 | norm_reg_ffbs | REML    |              0.104 |
| HMC      |         10 | norm_reg_ffbs | SOL     |              0.078 |
| HMC      |         10 | norm_reg_ffbs | TST     |              0.12  |
| HMC      |         10 | norm_reg_ffbs | WASO    |              0.114 |
| HMC      |         10 | scp_abs_bc    | N1%     |              0.19  |
| HMC      |         10 | scp_abs_bc    | N2%     |              0.14  |
| HMC      |         10 | scp_abs_bc    | N3%     |              0.194 |
| HMC      |         10 | scp_abs_bc    | REM%    |              0.182 |
| HMC      |         10 | scp_abs_bc    | REML    |              0.132 |
| HMC      |         10 | scp_abs_bc    | SOL     |              0.102 |
| HMC      |         10 | scp_abs_bc    | TST     |              0.154 |
| HMC      |         10 | scp_abs_bc    | WASO    |              0.142 |
| HMC      |         20 | ba_loa        | N1%     |              0.106 |
| HMC      |         20 | ba_loa        | N2%     |              0.092 |
| HMC      |         20 | ba_loa        | N3%     |              0.144 |
| HMC      |         20 | ba_loa        | REM%    |              0.106 |
| HMC      |         20 | ba_loa        | REML    |              0.14  |
| HMC      |         20 | ba_loa        | SOL     |              0.072 |
| HMC      |         20 | ba_loa        | TST     |              0.114 |
| HMC      |         20 | ba_loa        | WASO    |              0.116 |
| HMC      |         20 | norm_reg_ffbs | N1%     |              0.076 |
| HMC      |         20 | norm_reg_ffbs | N2%     |              0.082 |
| HMC      |         20 | norm_reg_ffbs | N3%     |              0.096 |
| HMC      |         20 | norm_reg_ffbs | REM%    |              0.076 |
| HMC      |         20 | norm_reg_ffbs | REML    |              0.054 |
| HMC      |         20 | norm_reg_ffbs | SOL     |              0.052 |
| HMC      |         20 | norm_reg_ffbs | TST     |              0.08  |
| HMC      |         20 | norm_reg_ffbs | WASO    |              0.098 |
| HMC      |         20 | scp_abs_bc    | N1%     |              0.118 |
| HMC      |         20 | scp_abs_bc    | N2%     |              0.098 |
| HMC      |         20 | scp_abs_bc    | N3%     |              0.13  |
| HMC      |         20 | scp_abs_bc    | REM%    |              0.112 |
| HMC      |         20 | scp_abs_bc    | REML    |              0.082 |
| HMC      |         20 | scp_abs_bc    | SOL     |              0.094 |
| HMC      |         20 | scp_abs_bc    | TST     |              0.108 |
| HMC      |         20 | scp_abs_bc    | WASO    |              0.092 |
| HMC      |         30 | ba_loa        | N1%     |              0.07  |
| HMC      |         30 | ba_loa        | N2%     |              0.054 |
| HMC      |         30 | ba_loa        | N3%     |              0.088 |
| HMC      |         30 | ba_loa        | REM%    |              0.046 |
| HMC      |         30 | ba_loa        | REML    |              0.108 |
| HMC      |         30 | ba_loa        | SOL     |              0.038 |
| HMC      |         30 | ba_loa        | TST     |              0.07  |
| HMC      |         30 | ba_loa        | WASO    |              0.066 |
| HMC      |         30 | norm_reg_ffbs | N1%     |              0.068 |
| HMC      |         30 | norm_reg_ffbs | N2%     |              0.06  |
| HMC      |         30 | norm_reg_ffbs | N3%     |              0.048 |
| HMC      |         30 | norm_reg_ffbs | REM%    |              0.054 |
| HMC      |         30 | norm_reg_ffbs | REML    |              0.048 |
| HMC      |         30 | norm_reg_ffbs | SOL     |              0.058 |
| HMC      |         30 | norm_reg_ffbs | TST     |              0.07  |
| HMC      |         30 | norm_reg_ffbs | WASO    |              0.078 |
| HMC      |         30 | scp_abs_bc    | N1%     |              0.094 |
| HMC      |         30 | scp_abs_bc    | N2%     |              0.078 |
| HMC      |         30 | scp_abs_bc    | N3%     |              0.086 |
| HMC      |         30 | scp_abs_bc    | REM%    |              0.072 |
| HMC      |         30 | scp_abs_bc    | REML    |              0.058 |
| HMC      |         30 | scp_abs_bc    | SOL     |              0.08  |
| HMC      |         30 | scp_abs_bc    | TST     |              0.078 |
| HMC      |         30 | scp_abs_bc    | WASO    |              0.078 |
| HMC      |         50 | ba_loa        | N1%     |              0.032 |
| HMC      |         50 | ba_loa        | N2%     |              0.018 |
| HMC      |         50 | ba_loa        | N3%     |              0.034 |
| HMC      |         50 | ba_loa        | REM%    |              0.014 |
| HMC      |         50 | ba_loa        | REML    |              0.034 |
| HMC      |         50 | ba_loa        | SOL     |              0.006 |
| HMC      |         50 | ba_loa        | TST     |              0.022 |
| HMC      |         50 | ba_loa        | WASO    |              0.026 |
| HMC      |         50 | norm_reg_ffbs | N1%     |              0.042 |
| HMC      |         50 | norm_reg_ffbs | N2%     |              0.044 |
| HMC      |         50 | norm_reg_ffbs | N3%     |              0.028 |
| HMC      |         50 | norm_reg_ffbs | REM%    |              0.038 |
| HMC      |         50 | norm_reg_ffbs | REML    |              0.036 |
| HMC      |         50 | norm_reg_ffbs | SOL     |              0.04  |
| HMC      |         50 | norm_reg_ffbs | TST     |              0.048 |
| HMC      |         50 | norm_reg_ffbs | WASO    |              0.044 |
| HMC      |         50 | scp_abs_bc    | N1%     |              0.054 |
| HMC      |         50 | scp_abs_bc    | N2%     |              0.05  |
| HMC      |         50 | scp_abs_bc    | N3%     |              0.044 |
| HMC      |         50 | scp_abs_bc    | REM%    |              0.044 |
| HMC      |         50 | scp_abs_bc    | REML    |              0.03  |
| HMC      |         50 | scp_abs_bc    | SOL     |              0.048 |
| HMC      |         50 | scp_abs_bc    | TST     |              0.036 |
| HMC      |         50 | scp_abs_bc    | WASO    |              0.04  |
| ST       |         10 | ba_loa        | N1%     |              0.406 |
| ST       |         10 | ba_loa        | N2%     |              0.514 |
| ST       |         10 | ba_loa        | N3%     |              0.41  |
| ST       |         10 | ba_loa        | REM%    |              0.37  |
| ST       |         10 | ba_loa        | REML    |              0.386 |
| ST       |         10 | ba_loa        | SOL     |              0.272 |
| ST       |         10 | ba_loa        | TST     |              0.212 |
| ST       |         10 | ba_loa        | WASO    |              0.352 |
| ST       |         10 | norm_reg_ffbs | N1%     |              0.206 |
| ST       |         10 | norm_reg_ffbs | N2%     |              0.258 |
| ST       |         10 | norm_reg_ffbs | N3%     |              0.184 |
| ST       |         10 | norm_reg_ffbs | REM%    |              0.236 |
| ST       |         10 | norm_reg_ffbs | REML    |              0.156 |
| ST       |         10 | norm_reg_ffbs | SOL     |              0.152 |
| ST       |         10 | norm_reg_ffbs | TST     |              0.188 |
| ST       |         10 | norm_reg_ffbs | WASO    |              0.134 |
| ST       |         10 | scp_abs_bc    | N1%     |              0.214 |
| ST       |         10 | scp_abs_bc    | N2%     |              0.494 |
| ST       |         10 | scp_abs_bc    | N3%     |              0.33  |
| ST       |         10 | scp_abs_bc    | REM%    |              0.296 |
| ST       |         10 | scp_abs_bc    | REML    |              0.21  |
| ST       |         10 | scp_abs_bc    | SOL     |              0.214 |
| ST       |         10 | scp_abs_bc    | TST     |              0.188 |
| ST       |         10 | scp_abs_bc    | WASO    |              0.198 |
| ST       |         20 | ba_loa        | N1%     |              0.382 |
| ST       |         20 | ba_loa        | N2%     |              0.36  |
| ST       |         20 | ba_loa        | N3%     |              0.33  |
| ST       |         20 | ba_loa        | REM%    |              0.198 |
| ST       |         20 | ba_loa        | REML    |              0.36  |
| ST       |         20 | ba_loa        | SOL     |              0.16  |
| ST       |         20 | ba_loa        | TST     |              0.176 |
| ST       |         20 | ba_loa        | WASO    |              0.236 |
| ST       |         20 | norm_reg_ffbs | N1%     |              0.234 |
| ST       |         20 | norm_reg_ffbs | N2%     |              0.212 |
| ST       |         20 | norm_reg_ffbs | N3%     |              0.206 |
| ST       |         20 | norm_reg_ffbs | REM%    |              0.17  |
| ST       |         20 | norm_reg_ffbs | REML    |              0.144 |
| ST       |         20 | norm_reg_ffbs | SOL     |              0.154 |
| ST       |         20 | norm_reg_ffbs | TST     |              0.178 |
| ST       |         20 | norm_reg_ffbs | WASO    |              0.16  |
| ST       |         20 | scp_abs_bc    | N1%     |              0.252 |
| ST       |         20 | scp_abs_bc    | N2%     |              0.322 |
| ST       |         20 | scp_abs_bc    | N3%     |              0.266 |
| ST       |         20 | scp_abs_bc    | REM%    |              0.194 |
| ST       |         20 | scp_abs_bc    | REML    |              0.182 |
| ST       |         20 | scp_abs_bc    | SOL     |              0.194 |
| ST       |         20 | scp_abs_bc    | TST     |              0.154 |
| ST       |         20 | scp_abs_bc    | WASO    |              0.206 |
| ST       |         30 | ba_loa        | N1%     |              0.374 |
| ST       |         30 | ba_loa        | N2%     |              0.318 |
| ST       |         30 | ba_loa        | N3%     |              0.28  |
| ST       |         30 | ba_loa        | REM%    |              0.268 |
| ST       |         30 | ba_loa        | REML    |              0.398 |
| ST       |         30 | ba_loa        | SOL     |              0.12  |
| ST       |         30 | ba_loa        | TST     |              0.216 |
| ST       |         30 | ba_loa        | WASO    |              0.132 |
| ST       |         30 | norm_reg_ffbs | N1%     |              0.224 |
| ST       |         30 | norm_reg_ffbs | N2%     |              0.248 |
| ST       |         30 | norm_reg_ffbs | N3%     |              0.238 |
| ST       |         30 | norm_reg_ffbs | REM%    |              0.248 |
| ST       |         30 | norm_reg_ffbs | REML    |              0.254 |
| ST       |         30 | norm_reg_ffbs | SOL     |              0.24  |
| ST       |         30 | norm_reg_ffbs | TST     |              0.19  |
| ST       |         30 | norm_reg_ffbs | WASO    |              0.13  |
| ST       |         30 | scp_abs_bc    | N1%     |              0.252 |
| ST       |         30 | scp_abs_bc    | N2%     |              0.302 |
| ST       |         30 | scp_abs_bc    | N3%     |              0.186 |
| ST       |         30 | scp_abs_bc    | REM%    |              0.236 |
| ST       |         30 | scp_abs_bc    | REML    |              0.246 |
| ST       |         30 | scp_abs_bc    | SOL     |              0.196 |
| ST       |         30 | scp_abs_bc    | TST     |              0.204 |
| ST       |         30 | scp_abs_bc    | WASO    |              0.2   |


*lgbm_sc_s0*

| target   |   n_target | method        | param   |   P(coverage<0.80) |
|:---------|-----------:|:--------------|:--------|-------------------:|
| HMC      |         10 | ba_loa        | N1%     |              0.216 |
| HMC      |         10 | ba_loa        | N2%     |              0.284 |
| HMC      |         10 | ba_loa        | N3%     |              0.258 |
| HMC      |         10 | ba_loa        | REM%    |              0.306 |
| HMC      |         10 | ba_loa        | REML    |              0.324 |
| HMC      |         10 | ba_loa        | SOL     |              0.176 |
| HMC      |         10 | ba_loa        | TST     |              0.268 |
| HMC      |         10 | ba_loa        | WASO    |              0.246 |
| HMC      |         10 | norm_reg_ffbs | N1%     |              0.112 |
| HMC      |         10 | norm_reg_ffbs | N2%     |              0.124 |
| HMC      |         10 | norm_reg_ffbs | N3%     |              0.118 |
| HMC      |         10 | norm_reg_ffbs | REM%    |              0.112 |
| HMC      |         10 | norm_reg_ffbs | REML    |              0.106 |
| HMC      |         10 | norm_reg_ffbs | SOL     |              0.096 |
| HMC      |         10 | norm_reg_ffbs | TST     |              0.132 |
| HMC      |         10 | norm_reg_ffbs | WASO    |              0.138 |
| HMC      |         10 | scp_abs_bc    | N1%     |              0.18  |
| HMC      |         10 | scp_abs_bc    | N2%     |              0.208 |
| HMC      |         10 | scp_abs_bc    | N3%     |              0.184 |
| HMC      |         10 | scp_abs_bc    | REM%    |              0.178 |
| HMC      |         10 | scp_abs_bc    | REML    |              0.182 |
| HMC      |         10 | scp_abs_bc    | SOL     |              0.1   |
| HMC      |         10 | scp_abs_bc    | TST     |              0.16  |
| HMC      |         10 | scp_abs_bc    | WASO    |              0.152 |
| HMC      |         20 | ba_loa        | N1%     |              0.1   |
| HMC      |         20 | ba_loa        | N2%     |              0.14  |
| HMC      |         20 | ba_loa        | N3%     |              0.116 |
| HMC      |         20 | ba_loa        | REM%    |              0.184 |
| HMC      |         20 | ba_loa        | REML    |              0.16  |
| HMC      |         20 | ba_loa        | SOL     |              0.08  |
| HMC      |         20 | ba_loa        | TST     |              0.13  |
| HMC      |         20 | ba_loa        | WASO    |              0.13  |
| HMC      |         20 | norm_reg_ffbs | N1%     |              0.096 |
| HMC      |         20 | norm_reg_ffbs | N2%     |              0.076 |
| HMC      |         20 | norm_reg_ffbs | N3%     |              0.084 |
| HMC      |         20 | norm_reg_ffbs | REM%    |              0.068 |
| HMC      |         20 | norm_reg_ffbs | REML    |              0.066 |
| HMC      |         20 | norm_reg_ffbs | SOL     |              0.068 |
| HMC      |         20 | norm_reg_ffbs | TST     |              0.094 |
| HMC      |         20 | norm_reg_ffbs | WASO    |              0.114 |
| HMC      |         20 | scp_abs_bc    | N1%     |              0.114 |
| HMC      |         20 | scp_abs_bc    | N2%     |              0.124 |
| HMC      |         20 | scp_abs_bc    | N3%     |              0.122 |
| HMC      |         20 | scp_abs_bc    | REM%    |              0.122 |
| HMC      |         20 | scp_abs_bc    | REML    |              0.074 |
| HMC      |         20 | scp_abs_bc    | SOL     |              0.078 |
| HMC      |         20 | scp_abs_bc    | TST     |              0.102 |
| HMC      |         20 | scp_abs_bc    | WASO    |              0.098 |
| HMC      |         30 | ba_loa        | N1%     |              0.066 |
| HMC      |         30 | ba_loa        | N2%     |              0.114 |
| HMC      |         30 | ba_loa        | N3%     |              0.066 |
| HMC      |         30 | ba_loa        | REM%    |              0.142 |
| HMC      |         30 | ba_loa        | REML    |              0.102 |
| HMC      |         30 | ba_loa        | SOL     |              0.04  |
| HMC      |         30 | ba_loa        | TST     |              0.086 |
| HMC      |         30 | ba_loa        | WASO    |              0.104 |
| HMC      |         30 | norm_reg_ffbs | N1%     |              0.086 |
| HMC      |         30 | norm_reg_ffbs | N2%     |              0.076 |
| HMC      |         30 | norm_reg_ffbs | N3%     |              0.05  |
| HMC      |         30 | norm_reg_ffbs | REM%    |              0.064 |
| HMC      |         30 | norm_reg_ffbs | REML    |              0.054 |
| HMC      |         30 | norm_reg_ffbs | SOL     |              0.05  |
| HMC      |         30 | norm_reg_ffbs | TST     |              0.064 |
| HMC      |         30 | norm_reg_ffbs | WASO    |              0.084 |
| HMC      |         30 | scp_abs_bc    | N1%     |              0.094 |
| HMC      |         30 | scp_abs_bc    | N2%     |              0.104 |
| HMC      |         30 | scp_abs_bc    | N3%     |              0.102 |
| HMC      |         30 | scp_abs_bc    | REM%    |              0.084 |
| HMC      |         30 | scp_abs_bc    | REML    |              0.046 |
| HMC      |         30 | scp_abs_bc    | SOL     |              0.066 |
| HMC      |         30 | scp_abs_bc    | TST     |              0.06  |
| HMC      |         30 | scp_abs_bc    | WASO    |              0.076 |
| HMC      |         50 | ba_loa        | N1%     |              0.012 |
| HMC      |         50 | ba_loa        | N2%     |              0.032 |
| HMC      |         50 | ba_loa        | N3%     |              0.028 |
| HMC      |         50 | ba_loa        | REM%    |              0.07  |
| HMC      |         50 | ba_loa        | REML    |              0.044 |
| HMC      |         50 | ba_loa        | SOL     |              0.028 |
| HMC      |         50 | ba_loa        | TST     |              0.028 |
| HMC      |         50 | ba_loa        | WASO    |              0.058 |
| HMC      |         50 | norm_reg_ffbs | N1%     |              0.058 |
| HMC      |         50 | norm_reg_ffbs | N2%     |              0.05  |
| HMC      |         50 | norm_reg_ffbs | N3%     |              0.03  |
| HMC      |         50 | norm_reg_ffbs | REM%    |              0.024 |
| HMC      |         50 | norm_reg_ffbs | REML    |              0.04  |
| HMC      |         50 | norm_reg_ffbs | SOL     |              0.026 |
| HMC      |         50 | norm_reg_ffbs | TST     |              0.044 |
| HMC      |         50 | norm_reg_ffbs | WASO    |              0.046 |
| HMC      |         50 | scp_abs_bc    | N1%     |              0.056 |
| HMC      |         50 | scp_abs_bc    | N2%     |              0.056 |
| HMC      |         50 | scp_abs_bc    | N3%     |              0.056 |
| HMC      |         50 | scp_abs_bc    | REM%    |              0.054 |
| HMC      |         50 | scp_abs_bc    | REML    |              0.03  |
| HMC      |         50 | scp_abs_bc    | SOL     |              0.036 |
| HMC      |         50 | scp_abs_bc    | TST     |              0.04  |
| HMC      |         50 | scp_abs_bc    | WASO    |              0.044 |
| ST       |         10 | ba_loa        | N1%     |              0.402 |
| ST       |         10 | ba_loa        | N2%     |              0.47  |
| ST       |         10 | ba_loa        | N3%     |              0.378 |
| ST       |         10 | ba_loa        | REM%    |              0.31  |
| ST       |         10 | ba_loa        | REML    |              0.348 |
| ST       |         10 | ba_loa        | SOL     |              0.344 |
| ST       |         10 | ba_loa        | TST     |              0.39  |
| ST       |         10 | ba_loa        | WASO    |              0.342 |
| ST       |         10 | norm_reg_ffbs | N1%     |              0.176 |
| ST       |         10 | norm_reg_ffbs | N2%     |              0.27  |
| ST       |         10 | norm_reg_ffbs | N3%     |              0.2   |
| ST       |         10 | norm_reg_ffbs | REM%    |              0.156 |
| ST       |         10 | norm_reg_ffbs | REML    |              0.168 |
| ST       |         10 | norm_reg_ffbs | SOL     |              0.154 |
| ST       |         10 | norm_reg_ffbs | TST     |              0.15  |
| ST       |         10 | norm_reg_ffbs | WASO    |              0.174 |
| ST       |         10 | scp_abs_bc    | N1%     |              0.36  |
| ST       |         10 | scp_abs_bc    | N2%     |              0.416 |
| ST       |         10 | scp_abs_bc    | N3%     |              0.31  |
| ST       |         10 | scp_abs_bc    | REM%    |              0.254 |
| ST       |         10 | scp_abs_bc    | REML    |              0.156 |
| ST       |         10 | scp_abs_bc    | SOL     |              0.186 |
| ST       |         10 | scp_abs_bc    | TST     |              0.288 |
| ST       |         10 | scp_abs_bc    | WASO    |              0.278 |
| ST       |         20 | ba_loa        | N1%     |              0.234 |
| ST       |         20 | ba_loa        | N2%     |              0.378 |
| ST       |         20 | ba_loa        | N3%     |              0.22  |
| ST       |         20 | ba_loa        | REM%    |              0.234 |
| ST       |         20 | ba_loa        | REML    |              0.316 |
| ST       |         20 | ba_loa        | SOL     |              0.324 |
| ST       |         20 | ba_loa        | TST     |              0.328 |
| ST       |         20 | ba_loa        | WASO    |              0.272 |
| ST       |         20 | norm_reg_ffbs | N1%     |              0.2   |
| ST       |         20 | norm_reg_ffbs | N2%     |              0.232 |
| ST       |         20 | norm_reg_ffbs | N3%     |              0.202 |
| ST       |         20 | norm_reg_ffbs | REM%    |              0.17  |
| ST       |         20 | norm_reg_ffbs | REML    |              0.184 |
| ST       |         20 | norm_reg_ffbs | SOL     |              0.168 |
| ST       |         20 | norm_reg_ffbs | TST     |              0.146 |
| ST       |         20 | norm_reg_ffbs | WASO    |              0.174 |
| ST       |         20 | scp_abs_bc    | N1%     |              0.214 |
| ST       |         20 | scp_abs_bc    | N2%     |              0.298 |
| ST       |         20 | scp_abs_bc    | N3%     |              0.236 |
| ST       |         20 | scp_abs_bc    | REM%    |              0.208 |
| ST       |         20 | scp_abs_bc    | REML    |              0.126 |
| ST       |         20 | scp_abs_bc    | SOL     |              0.22  |
| ST       |         20 | scp_abs_bc    | TST     |              0.256 |
| ST       |         20 | scp_abs_bc    | WASO    |              0.218 |
| ST       |         30 | ba_loa        | N1%     |              0.178 |
| ST       |         30 | ba_loa        | N2%     |              0.352 |
| ST       |         30 | ba_loa        | N3%     |              0.25  |
| ST       |         30 | ba_loa        | REM%    |              0.308 |
| ST       |         30 | ba_loa        | REML    |              0.388 |
| ST       |         30 | ba_loa        | SOL     |              0.266 |
| ST       |         30 | ba_loa        | TST     |              0.424 |
| ST       |         30 | ba_loa        | WASO    |              0.284 |
| ST       |         30 | norm_reg_ffbs | N1%     |              0.22  |
| ST       |         30 | norm_reg_ffbs | N2%     |              0.256 |
| ST       |         30 | norm_reg_ffbs | N3%     |              0.15  |
| ST       |         30 | norm_reg_ffbs | REM%    |              0.234 |
| ST       |         30 | norm_reg_ffbs | REML    |              0.24  |
| ST       |         30 | norm_reg_ffbs | SOL     |              0.232 |
| ST       |         30 | norm_reg_ffbs | TST     |              0.196 |
| ST       |         30 | norm_reg_ffbs | WASO    |              0.228 |
| ST       |         30 | scp_abs_bc    | N1%     |              0.31  |
| ST       |         30 | scp_abs_bc    | N2%     |              0.3   |
| ST       |         30 | scp_abs_bc    | N3%     |              0.244 |
| ST       |         30 | scp_abs_bc    | REM%    |              0.256 |
| ST       |         30 | scp_abs_bc    | REML    |              0.218 |
| ST       |         30 | scp_abs_bc    | SOL     |              0.252 |
| ST       |         30 | scp_abs_bc    | TST     |              0.27  |
| ST       |         30 | scp_abs_bc    | WASO    |              0.252 |
