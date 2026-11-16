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
- At a fixed centre, posterior-spread scaling narrowed intervals in most settings.
- Recalibrating the stager on locally scored nights removed most sleep-time bias.
- Coverage did not transfer across cohorts; ten locally scored nights restored it.

**Abstract**

*Objective:* Automatic sleep staging is validated with population limits of agreement but gives no error range for the parameters of an individual night. We developed and externally evaluated per-night prediction intervals for automatically scored polysomnography parameters.

*Methods:* Stage probabilities from a stager were combined with a hidden Markov model of stage transitions; whole hypnograms were sampled by forward-filtering backward-sampling, and the per-night spread of total sleep time (TST), sleep onset latency, wake after sleep onset (WASO), REM latency and stage percentages was conformally calibrated on manually scored nights. We evaluated a pretrained external stager (YASA) and an in-domain stager on Sleep-EDF and HMC data ({{nights_total}} nights, {{subjects_total}} subjects) against Bland–Altman limits of agreement and other interval methods, including transfer between cohorts, local recalibration and signal corruption.

*Results:* Within cohorts, 90 % intervals covered {{cov_min_yasa*100:.1f}}–{{cov_max_yasa*100:.1f}} % of reference values (YASA). At a fixed centre, scaling widths by the posterior spread lowered the interval score versus constant widths in {{fact_lower_yasa_mu}} of 24 cohort–parameter combinations (LightGBM: {{fact_lower_lgbm_sc_s0_mu}}). Against bias-corrected, distribution-free limits of agreement, intervals were significantly better in {{n_sig_better_vs_scp_abs_bc_yasa}} and worse in {{n_sig_worse_vs_scp_abs_bc_yasa}} combinations, with the largest gains for TST and none for REM %. The nights hardest to score were under-covered ({{q1cov_min_proposed*100:.0f}}–{{q1cov_max_proposed*100:.0f}} %). Recalibrating stage probabilities on locally scored nights reduced the TST bias of the stager's hypnogram from {{pe_yasa_HMC_TST_plug_in_bias:.0f}} to {{pe_yasa_HMC_TST_plug_in_calibrated_bias:.0f}} min (HMC). Intervals did not transfer between cohorts (N3 % coverage on HMC: {{x_cov_yasa_HMC_N3pct_norm_reg_ffbs*100:.0f}} %); calibration on ten local nights restored it to {{fs_cov_yasa_HMC_target_10_norm_reg_ffbs*100:.0f}} % on average.

*Conclusions:* Automatically scored sleep parameters can be reported with per-night intervals of verified average coverage. Adaptive scaling makes them more informative than limits of agreement for several parameters, and a small set of locally scored nights is needed to correct bias and restore coverage in a new population.

**Keywords:** automatic sleep staging; polysomnography; conformal prediction; uncertainty quantification; sleep parameters; external validation
