---
title: "Per-night prediction intervals for automatically scored sleep parameters: conformal calibration of posterior hypnogram samples compared with limits of agreement"
---

**Running title:** Per-night intervals for automatic sleep scoring

**Authors:** [AUTHOR NAME(S)]^a^

^a^ [Affiliation, address, country]

**Corresponding author:** [Name, address, e-mail]

**Article type:** Original Article

**Word count:** main text <<WORDCOUNT>> words; abstract <<ABSTRACTCOUNT>> words

**Highlights**

- Automatic sleep scoring gives no error range for the parameters of a single night.
- Conformally calibrated hypnogram samples gave valid per-night 90 % intervals.
- For total sleep time, intervals were more efficient than limits of agreement.
- Gains were parameter-specific; WASO intervals were worse in long recordings.
- Coverage did not transfer between cohorts; local nights restored it on average.

**Abstract**

*Objective:* Automatic sleep staging is validated with population limits of agreement (LoA), which give no error range for an individual night. We developed per-night prediction intervals for automatically scored sleep parameters and compared them with LoA.

*Methods:* Recalibrated epoch probabilities of a stager were combined with a hidden Markov model; whole hypnograms were sampled by forward-filtering backward-sampling, and the per-night spread of eight parameters, including total sleep time (TST) and wake after sleep onset (WASO), was conformally calibrated on manually scored nights. We evaluated an external pretrained stager (YASA) and an in-domain stager on three public cohorts ({{nights_total}} nights, {{subjects_total}} subjects), fitting every component on calibration nights only (50 subject-grouped splits), against parametric, regression-based and distribution-free LoA, and examined transfer between cohorts, calibration on 10–30 local nights and clinical threshold decisions.

*Results:* Within cohorts, 90 % intervals covered {{h_cov_min_yasa_norm_reg_ffbs*100:.1f}}–{{h_cov_max_yasa_norm_reg_ffbs*100:.1f}} % of reference values (YASA), whereas regression-based LoA under-covered (mean {{h_cov_mean_yasa_ba_reg*100:.1f}} %). Scaling width by the posterior spread lowered the interval score relative to a constant width around the same centre in {{h_nlower_yasa_SCALEmu}} (YASA) and {{h_nlower_lgbm_sc_s0_SCALEmu}} (in-domain) of 24 cohort–parameter combinations, never significantly worse. For TST, intervals had lower interval scores than every LoA variant in all cohorts (ratio versus distribution-free LoA {{min(h_ratio_yasa_SC_TST_scp_signed, h_ratio_yasa_ST_TST_scp_signed, h_ratio_yasa_HMC_TST_scp_signed):.2f}}–{{max(h_ratio_yasa_SC_TST_scp_signed, h_ratio_yasa_ST_TST_scp_signed, h_ratio_yasa_HMC_TST_scp_signed):.2f}}); other parameters showed no consistent gain, and WASO intervals were worse in long recordings. Intervals calibrated in one cohort did not transfer (N3 % coverage {{x_cov_yasa_HMC_N3pct_norm_reg_ffbs*100:.0f}} % in another); with ten local nights mean coverage was {{h_loc_cov_yasa_ST_10_norm_reg_ffbs*100:.1f}}–{{h_loc_cov_yasa_HMC_10_norm_reg_ffbs*100:.1f}} %, but a site's realised coverage fell below 80 % in {{h_loc_p80_yasa_HMC_10_norm_reg_ffbs*100:.0f}}–{{h_loc_p80_yasa_ST_10_norm_reg_ffbs*100:.0f}} % of repetitions. At TST < 6 h, intervals decided {{h_dec_yasa_TST_norm_reg_ffbs_frac*100:.0f}} % of nights with {{h_dec_yasa_TST_norm_reg_ffbs_acc*100:.1f}} % accuracy (automatic TST alone: {{h_dec_yasa_TST_plugacc*100:.1f}} %).

*Conclusions:* Locally calibrated conformal intervals give valid per-night error ranges for automatically scored sleep parameters. Their advantage over LoA is parameter-specific—clear for TST, absent for most others—and validity requires local calibration.

**Keywords:** automatic sleep staging; polysomnography; conformal prediction; uncertainty quantification; sleep parameters; external validation
