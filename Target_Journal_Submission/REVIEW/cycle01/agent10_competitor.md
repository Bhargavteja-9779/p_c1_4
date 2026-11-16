# Reviewer #10 (hostile competing researcher), cycle 1

## Summary of the submission (3-5 sentences)
FFBS hypnogram samples from a tempered HMM on recalibrated stager probabilities are conformalised into per-night 90 % intervals for eight parameters (YASA and LightGBM; SC, ST, HMC; 348 nights). Coverage is nominal within cohorts; the headline claim is greater efficiency than limits of agreement ("more informative"), mainly for TST. I re-analysed `e04_splits_{yasa,lgbm_sc_s0}.csv.gz` (α = 0.10; 48 stager × cohort × parameter combinations), `e07_paired_tests_*.csv` and `summaries/*_xfit.csv`; my re-implementation reproduces the published ratios (DF-LoA/proposed 1.055 vs 1.057).

## Fatal concerns
None. Validity is sound and negative findings are reported candidly; my concerns are about the size and source of the efficiency gain.

## Critical/Major concerns

**M1. The pre-specified method does not beat simple or variant competitors overall.** Ratio = competitor IS / proposed IS (500-split means; < 1 favours the competitor); LOSO = Holm-significant counts from `e07_paired_tests`.

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

DF-LoA is within ~6 % on average and wins 17/48; the best of the three constant-width intervals per cell beats the proposed method (0.954; 23/48). CQR-FFBS, the calibrated-plug-in centre and the unregularised score dominate the pre-specified configuration; dropping σ̄ is never ≥5 % worse and significantly better in 20/48 LOSO tests, yet line 115 calls this "modest". *Action:* add this 48-combination summary to the main text. Present the pre-specified method as dominated by its own ablations, and state the effect size (~5 %) in the abstract.

**M2. The headline TST gain is mostly a better point estimate, not better uncertainty.** Decomposition of prop/DF-LoA into a centre step (DF-LoA → constant width around μ̂, `scp_abs_mu`) and a scale step (`scp_abs_mu` → proposed); geometric means over 6 cells:

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

Two-thirds of the TST gain (log scale) is the centre; over all parameters the μ̂ centre is *worse* than plug-in + bias (1.037). The "largest gain" (YASA ST TST, 0.59) is centre 0.639 × scale 0.930, and there a *constant-width* interval around the calibrated plug-in beats the proposed method (0.73). Gains are TST-driven, not ST-driven: without ST DF-LoA/prop = 1.064; without TST 1.018 (17/42 wins).

*Action:* attribute the TST advantage mainly to probability recalibration, report the decomposition, and credit adaptivity with ~9 %.

**M3. Labelled data are used asymmetrically (fairness).** Line 89 states "Comparators used the same calibration nights". This is not true:
- BCTS, π_s, A, p₀ and τ, which define μ̂ and the calibrated plug-in, are cross-fitted on a fixed 5-fold split covering ~80 % of the cohort (`e03_night_summaries.py` l.24–68, `FOLD_SEED=2026`). This split is independent of the 500 random 50/50 conformal splits, so it includes labels of the *test* half.
- DF-LoA and BA-LoA estimate their bias from the 50 % calibration half only (`conformal_eval.py` l.83–94).
- CQR-QR is fitted on *half the calibration subjects* (`_qr_fit_predict`, l.63–78): ~25 % of the cohort, ≈11 nights (5–6 subjects) in ST, for an unpenalised 5-coefficient fit at the 0.05/0.95 quantiles. Its features also omit the FFBS SD. It is a strawman (geo-mean ratio 1.137).
- Calibration scores depend on test labels via the cross-fit, so the "exact" guarantee (lines 82, 86) does not strictly hold within cohort.

*Action:* nested design fitting every learned component on the calibration half only (or give comparators the same 80 %); CQR-QR via CV+ on all calibration nights with log σ̂ as a feature.

**M4. "A few / ten local nights corrected the TST bias" was never tested.** In E06 (`e06_cross_cohort.py` l.45), target nights use `srcSC` summaries: BCTS and HMM are fitted on SC, and only the conformal quantile uses the n_t target nights. The within-cohort TST bias reduction (−38 → −5 min, HMC) used BCTS fitted on ~120 HMC nights (~35 in ST). Highlights 2–3, Discussion (line 135, "a few locally scored nights") and Conclusion (line 148, "A small set of locally scored nights corrected most of the stagers' TST bias") conflate the two experiments. *Action:* run BCTS recalibration on n_t ∈ {10, 20, 30} target nights, or reword these claims.

**M5. The advantage depends on large stager errors.** As a proxy for a more accurate stager, I re-ran the conformal comparison within the easier half of nights (plug-in accuracy ≥ cohort median; the SD of plug-in error falls to 0.69×), using SC+HMC, 200 splits and my own implementation of the authors' code:

| Nights | DF-LoA/prop (wins of 32) | TST DF-LoA/prop | scp_abs_mu/prop (pure scale) |
|---|---|---|---|
| All | 1.062 (11) | 1.308 | 1.105 |
| Easier half | **0.905 (21)** | **1.011** | 1.102 |

With smaller errors DF-LoA wins most cells and the TST advantage disappears; only the ~10 % fixed-centre scale gain survives. The stagers are weak (YASA κ 0.63–0.73; LightGBM-HMC 0.49, where the largest TST gain, 0.67, occurs). Fpz-Cz is not the main issue (HMC with YASA's preferred C4-M1 is the worst cohort), but nothing shows the conclusion holds for U-Sleep/SleepTransformer, whose longer context may push τ lower still. *Action:* add at least one pretrained deep stager, and report gains as a function of stager accuracy.

**M6. "More informative" is not shown in absolute terms.** Against a null conformal interval around the calibration mean of the reference (ignoring the recording; 200 splits), YASA REM % proposed/null IS is 0.99/1.09/1.05 (HMC/SC/ST) with *wider* proposed widths (22.0/25.0/24.0 vs 20.5/21.1/20.4 pp); SC WASO 1.53 (230.6 vs 127.5 min). Overall the proposed method is worse than the null in 8/48 cells and within 10 % in 17/48 (median N1 %/N2 % 0.91, REM % 0.99). *Action:* report the null baseline. Restrict "informative" to TST, N3 %, SOL and REML, and qualify the Conclusion accordingly.

## Moderate concerns

**Mo1.** Abstract and highlight 3 report the factorial only at the μ̂ centre (23/24), which is the most favourable centre. At the calibrated-plug-in centre, the FFBS scale lowers IS in 39/48 combinations, by ≥5 % in only 24/48 (geo 0.94). Widths are narrower in 35/48. *Action:* give all three centres and the effect sizes in the abstract.

**Mo2.** Supplementary Table S4 summarises by the *median over cohorts*, which hides heterogeneity: TST scp_abs_cal/prop ranges from 0.73 to 1.30. *Action:* report per-cell ratios with split-bootstrap intervals.

**Mo3.** CQR-FFBS, already a protocol candidate (S1, RQ3), beats the symmetric score for latencies (SOL 0.749, REML 0.894). *Action:* discuss as a design limitation, not only "a post-hoc observation".

## Minor concerns

**Mi1.** In 13 Holm-significant S3/S4 cells the split-mean and LOSO directions disagree (e.g. LightGBM ST SOL vs scp_abs_cal: 0.965 vs 1.179, p_holm = 0.018); Table 2 is consistent. *Action:* flag such cells.

**Mi2.** In ST, constant bias correction is far worse than BCTS for YASA TST (scp_abs_cal/DF-LoA 0.43) and DF-LoA under-covers (min 0.852), so ST ratios against DF-LoA are a weak test. *Action:* note in Section 3.3.

**Mi3.** The "model-agnostic" claim (line 137) is supported by two feature-based LightGBM stagers only. *Action:* soften it, or address it through M5.

## Required additional experiments/analyses
1. A nested, label-symmetric design (M3), and a fair CQR-QR.
2. Few-night BCTS recalibration on target cohorts (M4).
3. At least one modern deep stager, with gains reported against stager accuracy (M5).
4. A 48-combination summary (geo-mean ratio, wins, LOSO counts) including norm_ffbs, norm_reg_plugc, cqr_ffbs, the oracle constant width and a no-stager null (M1, M6).
5. The centre/scale decomposition in the main text (M2).

## Recommendation
**Major revision.** The intervals are valid and reporting is candid, but the gain over the simplest competitor averages ~5 %, two-thirds of the TST gain is a recalibrated point estimate, three of the authors' own variants match or beat the method, and the advantage over LoA vanishes with smaller stager errors. Comparisons give the proposed pipeline more labelled data, and "ten local nights fix the bias" was not tested. Abstract, highlights and conclusions must be rewritten after fair experiments.

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
