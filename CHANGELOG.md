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
