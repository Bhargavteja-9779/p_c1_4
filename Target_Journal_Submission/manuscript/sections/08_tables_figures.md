## Tables

**Table 1.** Cohorts and epoch-level performance of the two stagers. Accuracy and Cohen's κ are means ± SD over nights; pooled κ over all epochs. LightGBM-SC values for SC are out-of-fold (subject-grouped five-fold cross-validation).

<<TABLE:table1_cohorts>>

**Table 2.** Within-cohort performance of the proposed 90 % intervals (α = 0.10). Each cell: coverage | mean width | interval-score ratio versus distribution-free (bias-corrected, constant-width conformal) limits of agreement | interval-score ratio versus Bland–Altman limits of agreement. Coverage and width are means over 500 subject-grouped calibration/test splits; ratios < 1 favour the proposed method; * Holm-adjusted p < 0.05 (Wilcoxon signed-rank test on per-subject mean interval scores, leave-one-subject-out calibration). Width in minutes (TST, SOL, WASO, REML) or percentage points of TST (stage percentages).

<<TABLE:table2_display>>

**Table 3.** Agreement of night-level point estimates with the manual reference (YASA stager): bias (mean absolute error); ICC(A,1). Plug-in: parameter of the stager's own hypnogram; calibrated plug-in: hypnogram from locally recalibrated probabilities; posterior mean: mean over 1000 FFBS hypnogram samples. p: Wilcoxon signed-rank test of per-subject absolute errors, posterior mean versus each plug-in. LightGBM results in Supplementary Table S8.

<<TABLE:table3_display>>

## Figure captions

![**Fig. 1.** The procedure on one HMC night (YASA stager). (a) Calibrated epoch probabilities; (b) manual reference hypnogram; (c) the stager's own hypnogram (plug-in); (d) three hypnograms sampled from the posterior by forward-filtering backward-sampling; (e, f) posterior distributions of TST and REM latency over 1000 samples, with the reference value, the plug-in estimate, the proposed 90 % interval (calibrated leave-one-subject-out on the other HMC nights) and the Bland–Altman limits of agreement.](figures/fig1_example_night.png){width=100%}

![**Fig. 2.** Within-cohort efficiency. Mean interval score (500 splits, α = 0.10) of each interval method relative to distribution-free (bias-corrected constant-width) limits of agreement, for each parameter, cohort and stager; values below 1 indicate better (narrower and/or fewer and smaller misses) intervals. Coverage of all conformal methods was 0.89–0.92 (Supplementary Table S2).](figures/fig2_within_cohort_efficiency.png){width=100%}

![**Fig. 3.** Adaptivity and flagging (YASA). (a–c) Proposed interval width versus absolute error of the plug-in estimate for TST, REM latency and N3 % (leave-one-subject-out). (d) AUROC (95 % subject-level bootstrap CI) for detecting nights with a clinically relevant plug-in error (|ΔTST| > 30 min, |ΔREML| > 30 min, |ΔN3 %| > 5 percentage points) using the proposed interval width, mean epoch entropy or 1 − mean maximum probability.](figures/fig3_adaptivity_flagging.png){width=100%}

![**Fig. 4.** Transportability. (a, d) Coverage on ST (×) and HMC (○) of intervals calibrated on SC, for both stagers. (b, c, e, f) Mean coverage over 500 repetitions after recalibration with n labelled target nights, using target nights only (solid) or SC plus target nights (dashed).](figures/fig4_transport_recalibration.png){width=100%}

![**Fig. 5.** Robustness to signal corruption (YASA; calibration on clean nights, test on corrupted nights). Coverage (top) and mean width (bottom) for TST, WASO and N3 % under additive Gaussian noise (0.5 and 1.0 × robust SD) and movement-artefact drifts in 10 % or 25 % of epochs.](figures/fig5_robustness.png){width=100%}
