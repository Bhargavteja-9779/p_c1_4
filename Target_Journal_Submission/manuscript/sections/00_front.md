---
title: "Per-night prediction intervals for automatically scored polysomnography: conformal calibration of posterior hypnogram samples with external validation"
---

**Running title:** Per-night intervals for automatic sleep scoring

**Authors:** [AUTHOR NAME(S)]^a^

^a^ [Affiliation, address, country]

**Corresponding author:** [Name, address, e-mail]

**Article type:** Original Article

**Word count:** main text <<WORDCOUNT>> words; abstract <<ABSTRACTCOUNT>> words

**Highlights**

- Automatic sleep scoring gives no per-night error range for clinical sleep parameters.
- Posterior hypnogram sampling plus conformal calibration gives per-night intervals.
- Coverage was nominal within cohorts; TST intervals beat limits of agreement.
- Posterior averaging removed most of the stagers' underestimation of sleep time.
- Coverage did not transfer across cohorts; ten locally scored nights restored it.

**Abstract**

*Objective:* Automatic sleep staging is validated with population limits of agreement, but gives no error range for the parameters of an individual night. We developed and externally evaluated per-night prediction intervals for automatically scored polysomnography parameters.

*Methods:* Epoch probabilities of a stager were combined with a hidden Markov model of stage transitions; complete hypnograms were drawn by forward-filtering backward-sampling, and the resulting per-night spread of total sleep time (TST), sleep onset latency, wake after sleep onset (WASO), REM latency and stage percentages was conformally calibrated on manually scored nights. We applied the method to a pretrained external stager (YASA) and an in-domain stager on Sleep-EDF (SC, ST) and HMC data ({{nights_total}} nights, {{subjects_total}} subjects), compared it with Bland–Altman limits of agreement and other interval methods, and tested transfer between cohorts, local recalibration and robustness to signal corruption.

*Results:* Within cohorts, 90 % intervals covered {{cov_min_yasa*100:.1f}}–{{cov_max_yasa*100:.1f}} % of reference values (YASA). Compared with constant-width intervals, interval scores were significantly lower in {{n_sig_better_vs_const_yasa}} and higher in {{n_sig_worse_vs_const_yasa}} of 24 cohort–parameter combinations, with the largest gains for TST (ratios {{isratio_yasa_ST_TST_scp_abs:.2f}}–{{isratio_yasa_SC_TST_scp_abs:.2f}}) and no gain for REM % or for WASO in ambulatory recordings. Posterior averaging reduced TST bias from {{pe_yasa_HMC_TST_plug_in_bias:.0f}} to {{pe_yasa_HMC_TST_ffbs_mean_bias:.0f}} min (HMC). Intervals calibrated on one cohort did not transfer: N3 % coverage on HMC fell to {{x_cov_yasa_HMC_N3pct_norm_reg_ffbs*100:.0f}} %; calibration on ten local nights restored it to {{fs_cov_yasa_HMC_target_10_norm_reg_ffbs*100:.0f}} %.

*Conclusions:* Automatically scored sleep parameters can be reported with per-night intervals of verified coverage. Gains over limits of agreement are parameter-specific, and local calibration remains necessary when an algorithm is used in a new population.

**Keywords:** automatic sleep staging; polysomnography; conformal prediction; uncertainty quantification; sleep parameters; external validation
