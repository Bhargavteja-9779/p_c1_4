---
title: "Per-night prediction intervals for automatic sleep scoring: local calibration, review triage and comparison with limits of agreement"
---

**Running title:** Per-night intervals for automatic sleep scoring

**Authors:** P. N. Bhargav Teja^a,\*^, [Second author name]^b^

^a^ [Affiliation, address, country]

^b^ [Affiliation, address, country]

^\*^ **Corresponding author:** P. N. Bhargav Teja, [address, e-mail]

**Article type:** Original Article

**Word count:** main text <<WORDCOUNT>> words; abstract <<ABSTRACTCOUNT>> words

**Highlights**

- Automatic sleep scoring reports no night-specific error range for sleep parameters.
- Per-night 90 % intervals reached nominal marginal coverage within cohorts.
- TST intervals beat limits of agreement; recalibration explains part of the gain.
- Interval-based triage: reviewing {{w_yasa_pooled_TST_norm_reg_ffbs_review*100:.0f}} % of nights caught 90 % of 6-h TST errors.
- Coverage transferred poorly between sites and depended on whose scoring was used.

**Abstract**

*Objective:* Laboratories adopting automatic scoring usually report population limits of agreement (LoA), which give one error range for all nights. We asked how a laboratory can obtain night-specific error ranges, how many locally scored nights this needs, and which nights to send for manual review.

*Methods:* Recalibrated epoch probabilities were combined with a hidden Markov model; whole hypnograms were sampled by forward-filtering backward-sampling, and the per-night spread of eight parameters, including total sleep time (TST) and wake after sleep onset (WASO), was conformally calibrated on manually scored nights. Two stagers were evaluated against LoA on three public cohorts ({{nights_total}} nights; every label-dependent component fitted on calibration nights only), and we examined transfer between cohorts, calibration on 10–30 local nights, review triage, and two independent cohorts (80 nights) scored by five technologists each.

*Results:* Within cohorts, 90 % intervals covered {{h_cov_min_yasa_norm_reg_ffbs*100:.1f}}–{{h_cov_max_yasa_norm_reg_ffbs*100:.1f}} % (YASA); regression-based LoA covered {{h_cov_mean_yasa_ba_reg*100:.1f}} %. For TST, intervals had lower interval scores than every LoA variant (ratio versus distribution-free LoA {{min(h_ratio_yasa_SC_TST_scp_signed, h_ratio_yasa_ST_TST_scp_signed, h_ratio_yasa_HMC_TST_scp_signed):.2f}}–{{max(h_ratio_yasa_SC_TST_scp_signed, h_ratio_yasa_ST_TST_scp_signed, h_ratio_yasa_HMC_TST_scp_signed):.2f}}), partly through recalibration (versus recalibrated constant width: {{h_ratio_yasa_SC_TST_scp_abs_cal:.2f}} SC, {{h_ratio_yasa_HMC_TST_scp_abs_cal:.2f}} HMC, {{h_ratio_yasa_ST_TST_scp_abs_cal:.2f}} ST); other parameters showed no consistent gain. At TST < 6 h, reviewing the {{w_yasa_pooled_TST_norm_reg_ffbs_review*100:.0f}} % of nights whose interval straddled the threshold caught {{w_yasa_pooled_TST_norm_reg_ffbs_caught*100:.0f}} % of misclassifications ({{w_yasa_pooled_TST_scp_abs_cal_review*100:.0f}} % of nights with recalibrated constant-width intervals). Coverage transferred poorly between cohorts (N3 % coverage {{x_cov_yasa_HMC_N3pct_norm_reg_ffbs*100:.0f}} %); with ten local nights a site's realised coverage fell below 80 % in {{h_loc_p80_yasa_HMC_10_norm_reg_ffbs*100:.0f}}–{{h_loc_p80_yasa_ST_10_norm_reg_ffbs*100:.0f}} % of repetitions. In the Dreem cohorts coverage was {{d_cov_min_DOD*100:.0f}}–{{d_cov_max_DOD*100:.0f}} %, but consensus-calibrated intervals covered individual technologists' values in only {{d_sc_cons_to_ind_mean_norm_reg_ffbs*100:.0f}} % of nights.

*Conclusions:* Locally calibrated conformal intervals achieve valid marginal coverage for the scoring used to calibrate them. Their advantage over LoA is clear for TST and absent for most other parameters.

**Keywords:** automatic sleep staging; polysomnography; conformal prediction; uncertainty quantification; sleep parameters; external validation
