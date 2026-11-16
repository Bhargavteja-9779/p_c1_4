# Reviewer #10 (hostile competing researcher), cycle 1

## Summary of the submission (3-5 sentences)
The authors sample whole hypnograms by FFBS from a tempered hybrid HMM built on a stager's (recalibrated) epoch probabilities, and conformalise the per-night posterior spread to obtain 90 % intervals for eight sleep parameters. The evaluation covers YASA and an in-domain LightGBM stager on Sleep-EDF SC/ST and HMC (348 nights), with 16 interval methods, 500 subject-grouped splits and LOSO tests. Coverage is nominal within cohorts. Relative to constant-width limits of agreement, the headline claim is better efficiency ("more informative"), with gains concentrated in TST. I re-analysed `results/raw/e04_splits_{yasa,lgbm_sc_s0}.csv.gz` (α = 0.10; 2 stagers × 3 cohorts × 8 parameters = 48 combinations), `e07_paired_tests_*.csv` and `results/summaries/*_xfit.csv`. My re-implementation reproduces the published ratios (DF-LoA/proposed geometric mean 1.055 vs 1.057).

## Fatal concerns
None. The validity results are sound and the authors report many negative findings honestly. My concerns are about whether the efficiency gain is real and how large it is.

## Critical/Major concerns

**M1. The pre-specified method does not beat simple or variant competitors overall.** Ratios are competitor IS / proposed IS (mean over 500 splits); values < 1 mean the competitor is better. The LOSO column counts Holm-significant results from `e07_paired_tests`.

| Competitor | geo-mean ratio | arith. mean | competitor better (of 48) | better by ≥5 % | proposed better by ≥5 % | LOSO: proposed sig. better / worse | min coverage |
|---|---|---|---|---|---|---|---|
| scp_abs_bc (DF-LoA) | 1.057 | 1.084 | 17 | 14 | 29 | 19 / 8 | 0.852 |
| scp_abs_cal | 1.056 | 1.078 | 17 | 11 | 24 | 21 / 11 | 0.901 |
| norm_entropy_reg | 1.067 | 1.072 | 10 | 0 | 19 | 21 / 3 | 0.895 |
| cqr_ffbs | **0.953** | 0.960 | 22 | 12 | 3 | 15 / 7 | 0.889 |
| norm_reg_plugc | **0.993** | 1.009 | 24 | 16 | 18 | 14 / **17** | 0.900 |
| norm_ffbs (no σ̄) | **0.951** | 0.952 | **37** | 22 | **0** | 4 / **20** | 0.896 |
| scp_abs_mu | 1.096 | 1.100 | 4 | 0 | 34 | 26 / 1 | 0.886 |

(Minimum coverage of the proposed method: 0.890.)

The simplest competitor, DF-LoA, comes within ~6 % on average and wins in 17 of 48 combinations. An oracle that picks the best of the three constant-width intervals per combination beats the proposed method on average (0.954; 23/48 wins). Three variants dominate the pre-specified configuration: CQR on FFBS quantiles, the calibrated-plug-in centre, and the unregularised score. The unregularised score is never worse by ≥5 % and is significantly better in 20/48 LOSO tests. The manuscript calls this "modestly" (line 115) and keeps σ̄ in the method. *Action:* add this 48-combination summary to the main text. Present the pre-specified method as dominated by its own ablations, and state the effect size (~5 %) in the abstract.

**M2. The headline TST gain is mostly a better point estimate, not better uncertainty.** I decomposed log(IS_prop/IS_DF-LoA) into a centre step (DF-LoA → constant width around μ̂, `scp_abs_mu`) and a scale step (`scp_abs_mu` → proposed). Geometric means over 6 combinations per row:

| Param | DF-LoA/prop | plugc-scaled/prop | cqr_ffbs/prop | prop/DF-LoA | centre part | scale part |
|---|---|---|---|---|---|---|
| TST | 1.377 | 0.978 | 1.026 | 0.726 | **0.813** | 0.893 |
| N2% | 1.192 | 1.221 | 1.002 | 0.839 | 0.856 | 0.979 |
| REML | 1.179 | 1.149 | 0.894 | 0.848 | 0.959 | 0.884 |
| N3% | 1.042 | 0.996 | 1.023 | 0.960 | 1.024 | 0.937 |
| N1% | 1.012 | 1.020 | 1.014 | 0.988 | 1.021 | 0.968 |
| REM% | 0.980 | 0.939 | 1.011 | 1.021 | 1.072 | 0.952 |
| WASO | 0.901 | 0.838 | 0.942 | 1.110 | 1.230 | 0.903 |
| SOL | 0.867 | 0.863 | 0.749 | 1.154 | 1.448 | 0.797 |
| All 48 | 1.057 | 0.993 | 0.953 | 0.946 | **1.037** | **0.912** |

- About two-thirds of the TST gain (in log terms) comes from the centre. Across all parameters the posterior-mean centre is *worse* than plug-in plus bias (1.037).
- The "largest gain" in Table 2, YASA ST TST at 0.59, splits into centre 0.639 × scale 0.930. In that cell, a *constant-width* interval around the calibrated plug-in beats the proposed method (scp_abs_cal/prop = 0.73).
- Gains are not driven by the small ST cohort: DF-LoA/prop is 1.064 without ST. They are driven by TST: without TST the ratio is 1.018 (17/42 wins), i.e. near parity.

*Action:* say that the TST advantage over LoA comes mainly from per-night probability recalibration. Report the centre/scale decomposition, and attribute only ~9 % to adaptivity.

**M3. Labelled data are used asymmetrically (fairness).** Line 89 states "Comparators used the same calibration nights". This is not true:
- BCTS, π_s, A, p₀ and τ, which define μ̂ and the calibrated plug-in, are cross-fitted on a fixed 5-fold split covering ~80 % of the cohort (`e03_night_summaries.py` l.24–68, `FOLD_SEED=2026`). This split is independent of the 500 random 50/50 conformal splits, so it includes labels of the *test* half.
- DF-LoA and BA-LoA estimate their bias from the 50 % calibration half only (`conformal_eval.py` l.83–94).
- CQR-QR is fitted on *half the calibration subjects* (`_qr_fit_predict`, l.63–78): ~25 % of the cohort, ≈11 nights (5–6 subjects) in ST, for an unpenalised 5-coefficient fit at the 0.05/0.95 quantiles. Its features also omit the FFBS SD. It is a strawman (geo-mean ratio 1.137).
- Because calibration scores depend on test labels through the cross-fit, the "exact" finite-sample claim (lines 82, 86) does not strictly hold within cohort.

*Action:* use a nested design in which every learned component is fitted only on the calibration half. Alternatively, give comparators the same 80 % (e.g. bias estimated on the cross-fit folds). Refit CQR-QR with CV+/cross-conformal on all calibration nights and with log σ̂ as a feature.

**M4. "A few / ten local nights corrected the TST bias" was never tested.** In E06 (`e06_cross_cohort.py` l.45), target nights use `srcSC` summaries: BCTS and HMM are fitted on SC, and only the conformal quantile uses the n_t target nights. The within-cohort TST bias reduction (−38 → −5 min, HMC) used BCTS fitted on ~120 HMC nights (~35 in ST). Highlights 2–3, Discussion (line 135, "a few locally scored nights") and Conclusion (line 148, "A small set of locally scored nights corrected most of the stagers' TST bias") conflate the two experiments. *Action:* run BCTS recalibration on n_t ∈ {10, 20, 30} target nights, or reword these claims.

**M5. The advantage depends on large stager errors.** As a proxy for a more accurate stager, I re-ran the conformal comparison within the easier half of nights (plug-in accuracy ≥ cohort median; the SD of plug-in error falls to 0.69×), using SC+HMC, 200 splits and my own implementation of the authors' code:

| Nights | DF-LoA/prop (wins of 32) | TST DF-LoA/prop | scp_abs_mu/prop (pure scale) |
|---|---|---|---|
| All | 1.062 (11) | 1.308 | 1.105 |
| Easier half | **0.905 (21)** | **1.011** | 1.102 |

With smaller errors, DF-LoA beats the proposed method in most combinations and the TST advantage disappears. Only the ~10 % scale gain at a fixed centre survives. The evaluated stagers are weak: YASA per-night κ is 0.63–0.73, and LightGBM on HMC is 0.49, where the largest TST gain (0.67) occurs. The Fpz-Cz montage is not the main issue, since HMC with YASA's preferred C4-M1 montage is the worst cohort. Still, nothing shows that the conclusion holds for modern sequence models (U-Sleep, SleepTransformer). Their long built-in context could also push τ even lower. *Action:* add at least one pretrained deep stager, and report gains as a function of stager accuracy.

**M6. "More informative" is not shown in absolute terms.** I compared the proposed intervals with a null conformal interval around the calibration mean of the reference value, which ignores the recording (200 splits). For REM % (YASA), proposed/null IS is 0.99, 1.09 and 1.05 (HMC/SC/ST), and the proposed widths are *wider* than the null (22.0/25.0/24.0 vs 20.5/21.1/20.4 pp). For YASA SC WASO the ratio is 1.53 (width 230.6 vs 127.5 min). Across all 48 combinations, the proposed method is worse than the null in 8 and within 10 % of it in 17. The median by parameter is 0.91 for N1 % and N2 % and 0.99 for REM %. *Action:* report the null baseline. Restrict "informative" to TST, N3 %, SOL and REML, and qualify the Conclusion accordingly.

## Moderate concerns

**Mo1.** Abstract and highlight 3 report the factorial only at the μ̂ centre (23/24), which is the most favourable centre. At the calibrated-plug-in centre, the FFBS scale lowers IS in 39/48 combinations, by ≥5 % in only 24/48 (geo 0.94). Widths are narrower in 35/48. *Action:* give all three centres and the effect sizes in the abstract.

**Mo2.** Supplementary Table S4 summarises by the *median over cohorts*, which hides heterogeneity: TST scp_abs_cal/prop ranges from 0.73 to 1.30. *Action:* report per-cell ratios with split-bootstrap intervals.

**Mo3.** No method is better for the skewed latencies than the post-hoc CQR-FFBS (SOL 0.749, REML 0.894 relative to the proposed). The protocol already listed `cqr` as a candidate score (S1, RQ3). Pre-specifying a symmetric score was therefore a choice the data contradict. *Action:* discuss this in the Methods rationale, not only as "a post-hoc observation".

## Minor concerns

**Mi1.** In 13 starred cells of S3/S4, the direction of the split-mean ratio disagrees with the significant LOSO direction. Example: LightGBM ST SOL vs scp_abs_cal has split ratio 0.965 but LOSO ratio 1.179 (p_holm = 0.018). Table 2 itself is consistent. *Action:* flag such cells.

**Mi2.** YASA's ST TST bias correction by a single constant (DF-LoA) is far worse than BCTS (scp_abs_cal/DF-LoA = 0.43). DF-LoA also under-covers in ST (minimum 0.852). This makes ST comparisons against DF-LoA a weak test. *Action:* note this in Section 3.3.

**Mi3.** The "model-agnostic" claim (line 137) is supported by two feature-based LightGBM stagers only. *Action:* soften it, or address it through M5.

## Required additional experiments/analyses
1. A nested, label-symmetric design (M3), and a fair CQR-QR.
2. Few-night BCTS recalibration on target cohorts (M4).
3. At least one modern deep stager, with gains reported against stager accuracy (M5).
4. A 48-combination summary (geo-mean ratio, wins, LOSO counts) including norm_ffbs, norm_reg_plugc, cqr_ffbs, the oracle constant width and a no-stager null (M1, M6).
5. The centre/scale decomposition in the main text (M2).

## Recommendation
**Major revision.** The intervals are valid and the reporting is unusually candid. However, my re-analysis shows that the advantage of the pre-specified method over the simplest competitor averages ~5 %, that two-thirds of the TST gain is a recalibrated point estimate, and that three of the authors' own variants match or beat the method. The advantage over LoA disappears when stager errors are smaller. Several comparisons give the proposed pipeline more labelled data than its competitors, and the "ten local nights fix the bias" message was not tested. The abstract, highlights and conclusions overstate the contribution and must be rewritten after the fair experiments are run.

```json
[
 {"id":"M1","severity":"critical","title":"Pre-specified method not better than simple/variant competitors overall","location":"Abstract l.31-33; Sec 3.3 l.113-115; Suppl. S4","evidence":"Own re-analysis of e04_splits (48 combos, alpha 0.10): competitor/proposed geo-mean IS ratio scp_abs_bc 1.057 (17/48 wins), scp_abs_cal 1.056 (17), norm_reg_plugc 0.993 (24), cqr_ffbs 0.953 (22), norm_ffbs 0.951 (37 wins, 0 losses >=5%); oracle best constant width 0.954 (23/48). LOSO e07: norm_ffbs significantly better in 20/48, norm_reg_plugc in 17/48.","action":"Report a 48-combination summary in the main text, state the ~5% effect size in the abstract, acknowledge dominance by ablations (regulariser, CQR-FFBS, calibrated centre).","needs_experiment":false},
 {"id":"M2","severity":"major","title":"TST gain is mainly a better point estimate (centre), not adaptivity","location":"Abstract l.31; Table 2; Sec 3.3; Discussion l.135","evidence":"Decomposition prop/DF-LoA = centre (scp_abs_mu/scp_abs_bc) x scale (prop/scp_abs_mu): TST 0.726 = 0.813 x 0.893; overall 0.946 = 1.037 x 0.912. YASA ST TST 0.59 = 0.639 x 0.930; there constant width around calibrated plug-in beats proposed (0.73). Without TST DF-LoA/prop = 1.018 (17/42 wins). Not ST-driven (1.064 without ST).","action":"Attribute TST gains to probability recalibration; report the centre/scale decomposition; limit adaptivity claim to ~9%.","needs_experiment":false},
 {"id":"M3","severity":"major","title":"Asymmetric use of labelled data; strawman CQR-QR","location":"Methods l.82-89, l.92; code/experiments/e03_night_summaries.py l.24-68; code/src/evaluation/conformal_eval.py l.63-94","evidence":"BCTS/HMM (defining mu and plugc) cross-fitted on fixed 5 folds (~80% of cohort, incl. test-half labels of each random split); DF-LoA/BA bias from 50% calibration half; CQR-QR fitted on half the calibration subjects (~11 nights in ST, unpenalised, quantiles 0.05/0.95) without FFBS-SD feature (geo-mean ratio 1.137). Contradicts 'Comparators used the same calibration nights'; exactness claim not strict within cohort.","action":"Nested design fitting all learned components on the calibration half only (or give comparators the same 80%); CQR-QR via CV+/cross-conformal with log sigma feature.","needs_experiment":true},
 {"id":"M4","severity":"major","title":"'Few/ten local nights corrected TST bias' not tested","location":"Highlights 2-3; Discussion l.135; Conclusion l.148; code/experiments/e06_cross_cohort.py l.45","evidence":"E06 uses srcSC summaries (BCTS/HMM fitted on SC); only the conformal quantile uses n_t target nights. Within-cohort bias reduction (-38 to -5 min HMC) used BCTS on ~120 HMC nights (~35 in ST).","action":"Run BCTS recalibration with n_t in {10,20,30} target nights or reword all claims.","needs_experiment":true},
 {"id":"M5","severity":"major","title":"Advantage over LoA vanishes when stager errors are smaller; no modern deep stager","location":"Sec 2.3, 3.1, Limitations (iv), l.137","evidence":"Re-analysis on easier half of nights (plug-in error SD 0.69x; SC+HMC, 200 splits): DF-LoA/prop 0.905 with 21/32 DF-LoA wins (all nights: 1.062, 11/32); TST 1.011 (all: 1.308); pure scale gain unchanged (1.10). Largest gains occur for weakest stager-cohort (LightGBM HMC, kappa 0.49).","action":"Add a pretrained deep stager (e.g. U-Sleep/SleepTransformer); report gains vs stager accuracy.","needs_experiment":true},
 {"id":"M6","severity":"major","title":"'More informative' not supported in absolute terms for several parameters","location":"Abstract Conclusions l.33; Conclusion l.148","evidence":"Null conformal interval around calibration mean of the reference (ignores the recording): proposed/null IS for REM% (YASA) 0.99/1.09/1.05 (HMC/SC/ST) with wider proposed widths (22.0/25.0/24.0 vs 20.5/21.1/20.4 pp); SC WASO 1.53 (230.6 vs 127.5 min); 8/48 combos worse than null, 17/48 within 10%.","action":"Report null baseline; restrict 'informative' claims to TST, N3%, SOL, REML.","needs_experiment":false},
 {"id":"Mo1","severity":"moderate","title":"Abstract reports factorial only at the most favourable centre","location":"Abstract l.31; Highlight 3","evidence":"At calibrated-plug-in centre FFBS scaling lowers IS in 39/48, by >=5% only in 24/48 (geo 0.94); width narrower in 35/48.","action":"Report all three centres with effect sizes.","needs_experiment":false},
 {"id":"Mo2","severity":"moderate","title":"Median-over-cohorts summary hides heterogeneity","location":"Suppl. S4","evidence":"TST scp_abs_cal/prop ranges 0.73-1.30 across cells while S4 shows 1.16/1.24.","action":"Report per-cell ratios with split-bootstrap intervals.","needs_experiment":false},
 {"id":"Mo3","severity":"moderate","title":"Symmetric score pre-specified although CQR was a protocol candidate and wins for latencies","location":"Suppl. S1 RQ3; Discussion l.139","evidence":"cqr_ffbs/prop SOL 0.749, REML 0.894 (geo-mean over 6 cells).","action":"Discuss as a design limitation; consider parameter-specific score.","needs_experiment":false},
 {"id":"Mi1","severity":"minor","title":"Split-ratio vs LOSO direction disagreements in supplementary starred cells","location":"Suppl. S3/S4","evidence":"13 Holm-significant cells where split-mean ratio and LOSO direction disagree, e.g. LightGBM ST SOL vs scp_abs_cal: split 0.965, LOSO 1.179 (p_holm 0.018).","action":"Flag such cells or use one evaluation basis.","needs_experiment":false},
 {"id":"Mi2","severity":"minor","title":"DF-LoA is a weak comparator in ST","location":"Sec 3.2-3.3; Table 2","evidence":"scp_abs_cal/scp_abs_bc for YASA ST TST = 0.43; DF-LoA min coverage 0.852 in ST.","action":"Note this when interpreting ST ratios.","needs_experiment":false},
 {"id":"Mi3","severity":"minor","title":"Model-agnostic claim rests on two feature-based LightGBM stagers","location":"Discussion l.137; Limitations (iv)","evidence":"Only YASA and LightGBM-SC evaluated.","action":"Soften claim or add deep stager (see M5).","needs_experiment":false}
]
```
