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
