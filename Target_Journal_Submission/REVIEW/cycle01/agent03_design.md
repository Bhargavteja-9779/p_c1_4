# Reviewer #3 — Experimental design (cycle 1)

## Summary of the submission (3-5 sentences)
FFBS samples whole hypnograms from an HMM posterior over calibrated stager probabilities, and the per-night spread of eight PSG parameters is conformally calibrated on scored nights. Two stagers (YASA; LightGBM on the same features) and three cohorts are evaluated with 500 subject-grouped splits, LOSO tests, transport, few-night recalibration, corruption and flagging. Within-cohort coverage is nominal by construction; the efficiency claims depend on which comparators are included. Label asymmetry, the untested few-night bias correction, uncorrected BA-LoA, the Beta(10,1) law and dropped analyses are raised by other reviewers. This review covers the remaining design issues and assesses the new E12 protocol.

## Fatal concerns
None.

## Critical/Major concerns

**C1 (critical). Regression-based limits of agreement (Bland & Altman 1999), the standard heteroscedastic comparator, are missing, and the "strongest simple competitor" label is wrong.** The comparative claim is made against LoA (Abstract, Conclusion). Regression-based LoA model the bias and |residual| as linear in the estimate, giving per-night widths from the plug-in alone. My read-only re-analysis used `results/summaries/*_xfit.csv`, 200 subject-grouped splits (paper's `subject_split` seeds) and the same clipping.
- Conformalised regression LoA vs the proposed method: the proposed method had the lower interval score in 14/24 cells for YASA (median comparator/proposed ratio 1.013) and 13/24 for LightGBM (1.023). The parametric version gave 14/24 (1.014) and 12/24 (1.006).
- Regression LoA was clearly better for SC WASO (0.43 and 0.55), HMC SOL (0.55 and 0.75) and HMC REM % (0.81 and 0.87). The proposed method was better for TST (1.12–1.58).
- Conformalised coverage: 0.88–0.91 in SC/HMC, 0.82–0.89 in ST (approximately valid, like DF-LoA). Nonparametric percentile LoA was weaker (median ratio 1.10–1.12).

*Action:* add regression-based LoA around the raw and calibrated plug-in (parametric with t·√(1+1/n); conformalised with split/cross-fitted scale for exact validity) to Table 2, the paired tests, E12 and the few-night analyses; rewrite the abstract and conclusion accordingly.

**M1. CQR-QR is handicapped by the design, yet it competes, and its results are absent from Results and Discussion.** CQR-QR is mentioned only in Methods (d).
- LOSO paired tests (`e07_paired_tests_*.csv`): the proposed method is significantly better than CQR-QR in 2 cells and worse in 4 for YASA (5 vs 7 for LightGBM). Examples of significant losses: YASA SC WASO ratio 2.54, HMC SOL 2.11, HMC REM % 1.20, HMC REML 1.15 (all p_holm < 0.001).
- The direction reverses between the 500 splits (regression on ~25 % of the cohort) and LOSO (~50 %) in 7/24 YASA cells (e.g. HMC REML 0.95 → 1.15): the design starves it of data.
- At α = 0.05 it returns infinite or full-range intervals in all ST cells in every split (`tableS_all_methods_within`), inflating that comparison.
- It degraded far less under corruption (`tableS_robustness`; TST 0.60 vs 0.32 strong noise, 0.72 vs 0.47 mild; WASO 0.55 vs 0.33) and in transport (LightGBM HMC TST 0.95 vs 0.50; N2 % 0.97 vs 0.82).

*Action:* report and discuss CQR-QR; implement it cross-fitted (CV+) on all calibration nights with σ̂ and calibrated-plug-in features; include it in E06, E09 and E12.

**M2. The secondary analyses compare the proposed method only against the comparators it beats.**
- §3.5 and the Discussion contrast ten-night recalibration only with uncorrected BA-LoA and approximately valid DF-LoA. In `e06_fewshot_yasa`, a plain constant width around the raw plug-in (`scp_abs`) reached 0.911 (HMC) and 0.898 (ST) vs 0.910 and 0.894, with median P(coverage < 0.80) of 9.7 % and 17.2 % vs 10.7 % and 18.6 %.
- A t-corrected BA (my re-run) gives 89.4 % and 86.9 %, P < 0.80 of 14.3 % and 24.6 %: "twice as often with Bland–Altman limits" reflects a mis-specified comparator.
- §3.7 compares only with DF-LoA; entropy scaling (same centre) also degraded less under strong noise (N3 % 0.83 vs 0.73; WASO 0.45 vs 0.33), as did CQR-QR.

*Action:* report all methods; state that local coverage reliability is generic to conformal calibration, not to the FFBS scale.

**M3. The flagging design misdefines the target event and omits the obvious label-free competitor.**
- Events are raw plug-in errors (`e07_utility_and_stats.py`, `flagging`), although intervals are centred on μ̂ and the workflow reports a recalibrated estimate. Events are bias-dominated: |ΔTST| > 30 min in 79/151 HMC nights (YASA), 92/151 (LightGBM); |ΔN3 %| > 5 pp in 123/151 (LightGBM).
- The label-free discrepancy |plug-in − calibrated plug-in| beats the width (my plain AUROCs, no CIs): TST 0.79 vs 0.68 (YASA HMC), 0.81 vs 0.61 (LightGBM HMC); WASO 0.87 vs 0.62. With events on the calibrated-plug-in error, FFBS-SD AUROC for HMC TST is 0.83 and 0.87.
- LightGBM HMC REML: entropy beats width (0.66 vs 0.61), undisclosed in the YASA-only text.

*Action:* pre-specify events on the estimate that is actually reported. Add the discrepancy flag and the independent-sampling SD as comparators. Use paired bootstrap CIs for ΔAUROC, report both stagers, and give operating points (sensitivity at a fixed review rate).

**M4. The E12 "honest protocol" (added in cycle 1) needs design fixes before it can serve as the primary analysis.**
- (a) Calibration scores come from five-fold models within the calibration set, test scores from a model refitted on all of it (`e12_honest_protocol.py`, `honest_frames`). This CV+-type construction has a worst-case 1−2α guarantee (Barber et al. 2021), not the exact 1−α of §2.5; use a true split or state the guarantee.
- (b) R = 50 (500 in the primary analysis) gives P(coverage < 0.80) an SE of ~4–5 pp.
- (c) `scp_abs`, CQR-QR and regression LoA are missing, and BA is still uncorrected (ST, n = 10: 0.821).
- (d) Under the honest protocol the advantage over DF-LoA shrinks for YASA: 14/24 cells with a lower interval score (median ratio 0.956), against 16/24 (0.910) under cross-fitting. For LightGBM it is 16/24 (0.935).
- Positively, E12 supports ten-night bias correction for YASA (TST bias −3.8 min HMC, −0.8 ST); less so for LightGBM HMC (−7.1).

*Action:* fix (a)–(c); make E12 primary (Table 2, paired and factorial tests), keep cross-fitting as sensitivity, log the change.

## Moderate concerns

**Mo1. The pre-specified success criterion, applied in full, is met in a minority of cells.** The criterion requires a Holm-significant reduction in interval score and a width–error Spearman correlation whose CI excludes 0. I computed the correlation's CI with a subject-cluster bootstrap on the LOSO intervals.
- vs BA-LoA: 9/24 (YASA) and 8/24 (LightGBM).
- vs split-conformal with absolute residuals: 7/24 and 9/24.

The Spearman CI is not positive for N2 % or most ST cells, yet the abstract leads with post-hoc factorial point counts (23/24). This quantifies Reviewer 4's M5. *Action:* report the pre-specified primary outcome in the abstract, labelled as such.

**Mo2. The transport design is one-directional, and pooling is naive.** SC (healthy, home recordings, R&K) is the only source. HMC→SC/ST and leave-one-cohort-out were not run, so the failure cannot be separated from the choice of source. "Pooled" calibration simply concatenates SC and target nights. The natural comparators are Mondrian-by-cohort and weighted conformal calibration. CQR-QR and entropy scaling are excluded from `FEW_METHODS`. *Action:* add the reverse direction, leave-one-cohort-out, and cohort-Mondrian or weighted pooling.

**Mo3. The protocol cannot be verified as pre-registered, and Methods contradicts itself.**
- `PREREGISTERED_PROTOCOL.md` first appears in commit 8bbf8ce (2026-11-15 16:37), together with the first E04 coverage logs (`e04_yasa.log`). It was never publicly registered.
- §2.5 says "all comparators were fixed in a protocol", while §2.6 lists comparators that were added later.
- `norm_entropy_reg` and `scp_abs_mu` are not in the protocol's comparator list, but they appear in the first E04 run.

*Action:* call it a "pre-specified internal protocol", correct §2.5, and log these additions.

## Minor concerns

**Mi1. The efficiency advantage depends on α.** For YASA vs DF-LoA, the proposed method had the lower interval score in 18/24, 16/24 and 13/24 cells at α = 0.05, 0.10 and 0.20 (median ratios 0.867, 0.910, 0.943). "Stable across α" (§3.3) holds for coverage only. Report efficiency by α.

**Mi2. In ST the scale effect is not shown.** The factorial reductions were Holm-significant in 1, 0 and 1 of 8 parameters (YASA) for the μ̂, calibrated and raw centres. At the calibrated centre the interval score was lower in only 3/8. "For both stagers and all three cohorts" (Discussion) overstates this.

**Mi3. The M sensitivity analysis was computed but not reported.** My check on `yasa_xfit` found that M = 100 vs 1000 changes σ̂ by a median of 4.5–5.5 % (rank correlation 0.97–0.99). Report this; it justifies a smaller M.

**Mi4. Highlight 3 says "narrowed intervals", but the evidence is the interval score.** State the metric, or report widths: at the μ̂ centre the width was lower in 20/24 cells over the 500 splits.

## Required additional experiments/analyses
1. Regression-based LoA (parametric with t-correction, and conformalised with exact validity) and t-corrected BA, in every analysis (C1, M2).
2. A cross-fitted CQR-QR with σ̂ and calibrated plug-in features, in E04, E06, E09 and E12 (M1).
3. A redesigned flagging analysis: events on the reported estimate, a discrepancy flag, paired ΔAUROC, both stagers (M3).
4. E12 with exact split or declared CV+ guarantees, R ≥ 500 and the full comparator set; promote it to the primary analysis (M4).
5. Reverse and leave-one-cohort-out transport, with Mondrian or weighted pooling (Mo2).

## Recommendation
**Major revision.** Validity holds by construction and E12 addresses label asymmetry, but the efficiency claim against LoA was never tested against heteroscedastic LoA (roughly on par in my re-analysis). CQR-QR was handicapped and omitted, and the secondary analyses report only favourable comparators. All of this is fixable cheaply (FFBS ≈ 0.02 s/night).

```json
[
{"id":"C1","severity":"critical","title":"Regression-based (heteroscedastic) limits of agreement missing; 'strongest simple competitor' claim wrong","location":"Methods 2.6(b); Abstract; Conclusion; Table 2","evidence":"Reviewer re-analysis (200 subject-grouped splits, xfit summaries): conformalised regression LoA (bias and |residual| linear in the plug-in) vs proposed: proposed lower interval score in 14/24 (YASA, median ratio 1.013) and 13/24 (LightGBM, 1.023); parametric 14/24 (1.014) and 12/24 (1.006); regression LoA better for SC WASO (0.43/0.55), HMC SOL (0.55/0.75), HMC REM% (0.81/0.87); coverage 0.88-0.91 SC/HMC","action":"Add regression-based LoA (t-corrected parametric; conformalised with split/cross-fitted scale) around raw and calibrated plug-in to all analyses; revise claims","needs_experiment":true},
{"id":"M1","severity":"major","title":"CQR-QR handicapped by design yet competitive; results omitted from text","location":"Methods 2.6(d); conformal_eval.py _qr_fit_predict; Results 3.3/3.5/3.7","evidence":"LOSO: proposed sig. better/worse vs CQR-QR 2/4 (YASA), 5/7 (LightGBM); split-vs-LOSO direction reversals in 7/24 YASA cells; infinite or full-range intervals in all ST cells at alpha=0.05; robustness TST coverage 0.60 vs 0.32 (strong noise); transport LightGBM HMC TST 0.95 vs 0.50","action":"Report CQR-QR; implement a cross-fitted CV+ CQR with sigma-hat and calibrated plug-in features; include in E06/E09/E12","needs_experiment":true},
{"id":"M2","severity":"major","title":"Secondary analyses report only the comparators the method beats","location":"Sec 3.5, 3.7, Discussion 'Clinical use'","evidence":"Few-night n=10: scp_abs 0.911/0.898 coverage and P(cov<0.8) 9.7%/17.2% vs proposed 0.910/0.894 and 10.7%/18.6%; t-corrected BA 89.4%/86.9%, P<0.8 14.3%/24.6% (reviewer re-run); strong noise: entropy scaling N3% 0.83 vs 0.73, WASO 0.45 vs 0.33","action":"Report all methods; attribute local reliability to conformal calibration generally","needs_experiment":false},
{"id":"M3","severity":"major","title":"Flagging events defined on raw plug-in error; label-free discrepancy flag omitted","location":"e07_utility_and_stats.py flagging; Sec 3.8; Fig 3","evidence":"TST events 79/151 (YASA HMC), 92/151 (LightGBM); |plug-in - calibrated plug-in| AUROC TST 0.79/0.81 vs width 0.68/0.61, WASO 0.87 vs 0.62; FFBS SD on calibrated-error events 0.83/0.87; LightGBM HMC REML entropy 0.66 > width 0.61","action":"Define events on the reported estimate; add discrepancy and independent-SD flags; paired bootstrap of delta-AUROC; both stagers; operating points","needs_experiment":true},
{"id":"M4","severity":"major","title":"E12 honest protocol: asymmetric scores, R=50, incomplete comparators; should become the primary analysis","location":"code/experiments/e12_honest_protocol.py honest_frames, main","evidence":"Calibration scores from within-calibration 5-fold models, test scores from a model refitted on all calibration nights (CV+ structure, 1-2alpha guarantee); R=50; omits scp_abs/CQR-QR/regression LoA; BA uncorrected (ST n=10: 0.821); advantage vs DF-LoA 14/24 (median 0.956) vs 16/24 (0.910) under cross-fitting (YASA)","action":"Use an exact split or declare the CV+ guarantee; R>=500; full comparator set; promote to Table 2 and tests; log the change","needs_experiment":true},
{"id":"Mo1","severity":"moderate","title":"Full pre-specified success criterion met in a minority of cells","location":"Methods 2.8; Abstract; Supplementary S1","evidence":"Holm-significant interval-score reduction AND Spearman CI>0 (subject-cluster bootstrap, LOSO): vs BA-LoA 9/24 (YASA), 8/24 (LightGBM); vs split-conformal abs 7/24, 9/24","action":"Report the pre-specified primary outcome in the abstract, labelled as such","needs_experiment":false},
{"id":"Mo2","severity":"moderate","title":"Transport one-directional; naive pooling","location":"e06_cross_cohort.py; Sec 3.5","evidence":"SC is the only source; no HMC->SC/ST or leave-one-cohort-out; pooled = concatenation; FEW_METHODS excludes CQR-QR and entropy scaling","action":"Add reverse direction, leave-one-cohort-out, and cohort-Mondrian/weighted conformal pooling","needs_experiment":true},
{"id":"Mo3","severity":"moderate","title":"'Pre-registered' protocol not independently time-stamped; Methods contradiction","location":"Supplementary S1; Methods 2.5 vs 2.6; git 8bbf8ce","evidence":"Protocol first committed with the first E04 coverage logs (2026-11-15 16:37); not publicly registered; 2.5 says all comparators were fixed; norm_entropy_reg and scp_abs_mu were run but not listed in the protocol","action":"Rename 'pre-specified internal protocol'; correct 2.5; log the additions","needs_experiment":false},
{"id":"Mi1","severity":"minor","title":"Efficiency advantage depends on alpha","location":"Sec 3.3; Supplementary S6","evidence":"vs DF-LoA lower interval score 18/16/13 of 24 at alpha 0.05/0.10/0.20 (median ratios 0.867/0.910/0.943, YASA)","action":"Report efficiency by alpha; qualify 'stable'","needs_experiment":false},
{"id":"Mi2","severity":"minor","title":"Scale benefit not shown in ST","location":"Discussion para 1; tableS_factorial_tests","evidence":"ST: Holm-significant reductions 1/0/1 of 8 (YASA, mu/calibrated/raw centres); calibrated-centre interval score lower in only 3/8","action":"Qualify 'all three cohorts'","needs_experiment":false},
{"id":"Mi3","severity":"minor","title":"M sensitivity computed but not reported","location":"Supplementary S1 sensitivity; summaries ffbsM100","evidence":"M=100 vs 1000 sigma-hat median relative difference 4.5-5.5%, rank correlation 0.97-0.99 (yasa_xfit)","action":"Report it; consider a smaller M","needs_experiment":false},
{"id":"Mi4","severity":"minor","title":"Highlight 3 'narrowed' but metric is interval score","location":"Highlights","evidence":"At the mu centre, width lower in 20/24 cells and interval score lower in 22/24 (500 splits)","action":"Name the metric or report widths","needs_experiment":false}
]
```
