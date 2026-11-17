# CHANGELOG (protocol deviations and methodological changes, with reasons)

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

## Revision 1 (after review cycle 1; 10 independent reviewers; see Target_Journal_Submission/REVIEW/review_01.md)
* [Primary analysis changed — deviation from protocol] The honest end-to-end protocol E12 (every
  label-dependent component — BCTS, prior, transitions, tau, conformal quantile — fitted only on the
  calibration half of 50/50 subject-grouped splits, calibration scores cross-fitted inside the calibration
  set) is now the PRIMARY within-cohort analysis. Reason: in the pre-registered analysis the HMM/BCTS were
  cross-fitted on ~80 % of each cohort, including labels of test-half subjects, whereas the comparators used
  only the 50 % calibration half (unequal use of labelled data; reviewers 2, 3, 5, 10). The pre-registered
  cross-fitted analysis (E04/E07) is retained in the supplement. Validity guarantee for cross-fitted scores
  stated as CV+-type (>= 1 - 2 alpha; Barber et al. 2021).
* [Leakage fix] Automatic hypnograms are now evaluated on all analysis-window epochs; the reference
  "unscored" mask is no longer applied to automatic hypnograms (it is label information). Reference unscored
  epochs are treated as wake. All night summaries (E03) and downstream evaluations re-run.
* [Comparators added] Regression-based Bland–Altman limits (`ba_reg`; Bland & Altman 1999) and an exactly
  valid signed-residual distribution-free LoA (`scp_signed`). Parametric LoA now a t-based prediction
  interval (previously z-based). CQR-QR features extended (plug-in, calibrated plug-in, FFBS mean/SD,
  entropy, max-probability) with a quantile-crossing guard.
* [Ablations] Scale-only ablations at a fixed centre (`norm_reg_ind_s`, `norm_reg_ffbs1_s`) added; earlier
  ablations changed centre and scale together.
* [Statistics] Paired tests changed from Wilcoxon signed-rank (tests the pseudo-median) to a two-sided
  sign-flip permutation test of the mean per-subject difference, so that the reported ratio of means,
  its subject-bootstrap CI and the p-value come from the same analysis; Holm within stager x cohort.
  Wilcoxon p kept as a secondary column. LOSO coverage CIs no longer used for claims.
* [Pre-registered items now run] E13: Spearman success criterion, number of posterior samples M, calibration
  size. 50 Hz line-noise corruption NOT run (deviation): YASA band-pass filtering removes it before feature
  extraction, so the test would not exercise the method.
* [New sensitivity analyses] E14 montage sensitivity (YASA with F4-M1 on HMC; source-only SC->HMC);
  E15 clinical decision thresholds (TST < 360, SOL > 30, WASO > 30, REML <= 15 min) and easier/harder-night
  stratification; label-free flag |raw - calibrated plug-in| added to the flagging analysis.
* [Efficiency] E10 extended: one-off costs (source-model fit incl. JIT compilation, first FFBS call), peak
  memory for a 7 x 24 h recording, single-thread setting.
* [Reporting] Subgroups require >= 20 distinct nights; per-parameter coverage ranges reported; non-finite
  conformal scores treated as +inf.
* [Literature] Closest prior art (van Gorp et al. 2023 JBHI/ICASSP; Philips patent application EP4388985A1)
  added; novelty restricted to calibrated (conformal) per-night coverage, transport and local recalibration.
  Misattributed citations corrected. Ethics statement corrected (only HMC documents an approval, METC-19-065).
* [Manuscript, after the E12/E15 results] Title changed to "...compared with limits of agreement"; Abstract,
  Highlights, Results (3.1–3.8), Discussion, Conclusion and cover letter rewritten around the end-to-end protocol.
  Claims NARROWED: the advantage over limits of agreement is specific to TST (significant against distribution-free
  LoA in 6/6 stager-cohort combinations; against regression-based LoA in 3/6); no consistent gain for other
  parameters; WASO-SC significantly worse; the pre-specified regulariser is suboptimal (unregularised score better in
  20/24); regression-based LoA is competitive in interval score but under-covers. Recommendation changed from
  "about ten local nights" to "at least 20 local nights". Cover letter no longer states that no ethics approval was
  required. Fig. 3 no longer plots unbounded distribution-free LoA (n_t = 10). Per-night E12 files (>85 MB) are
  regenerated rather than versioned.
