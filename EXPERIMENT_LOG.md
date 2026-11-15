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
