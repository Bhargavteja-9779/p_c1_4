# Reviewer #4 (Statistics), cycle 1

## Summary of the submission (3-5 sentences)
The authors conformally calibrate the spread of FFBS hypnogram posteriors to give per-night intervals for eight sleep parameters. They evaluate them over 500 within-cohort splits and LOSO, cross-cohort transfer, few-night recalibration, corruption, AUROC flagging and point-estimate agreement. Inference uses Wilcoxon signed-rank tests on per-subject mean LOSO interval scores (IS), Holm-adjusted within cohort × stager, plus cluster-bootstrap CIs. However, the main test does not test the claimed estimand, and some significance marks point the opposite way to the tested effect. The coverage evidence is largely guaranteed by construction, and some of its uncertainty statements are meaningless.

**Verified against result files (all match):** coverage 89.0–92.1 % and 89.9–92.0 %; BA/DF-LoA minima 83.0/83.8 and 85.2/87.1 %; factorial counts 23/18/20, 21/18/19, 13/12/13 vs 0/1/2, 14/10/10 vs 1/4/2; 9/4 vs DF-LoA; TST ratios 0.85/0.59/0.71; few-night 91.0/86.2/89.3, 89.4/83.1/86.5 %, 11/19/24/38 %, 88.1 %; transfer 38/54/46/83 % and 50 %; AUROC 0.74/0.57, 0.68/0.49; quartile 81–85/92–96 %; Mondrian 84–89 % (5/6); HMC TST bias −38.3, MAE 40.2, ICC 0.81 (recomputed independently; the ICC(A,1) formula in stats.py L78–87 is correct); robustness 32/7 %, 71→108 min, 85/48 %; error analysis 0.75/0.81, 10/24, 9/24, ρ 0.79; seed range 1.9 pp; τ 0.10–0.15. There were no zero paired differences (0/2007).

## Fatal concerns
None.

## Critical/Major concerns
**M1. The Wilcoxon signed-rank test does not test the reported quantity, and significance marks contradict the test direction.** The claims and ratios concern *mean* IS, a proper scoring rule. The signed-rank test addresses the pseudo-median of the paired differences. These differences are extremely skewed because of the 2/α = 20 miss penalty. make_tables.py L122–129 and L249–250 take the *direction* from the mean and the *significance* from the Wilcoxon test. Among significant tests, the sign of r_rb contradicts the mean-IS sign in 7/126 (YASA) and 10/138 (LightGBM) cases (e07_paired_tests_*.csv).
- Table 2, YASA HMC SOL vs BA-LoA: "1.39*" is counted as a significant loss, but r_rb = −0.64 (p_holm = 5.6e-10) *favours the proposed method*: 87 % of subjects do better, and one subject contributes +2448. A sign-flip permutation test of the mean difference gives p = 0.25.
- LightGBM HMC SOL "1.21*" behaves the same way (r_rb = −0.62).
- Factorial, LightGBM: 3 of the 7 "significant increases" (HMC N1 % and REML with the calibrated centre; HMC N2 % with the posterior-mean centre) are rank-significant in the *opposite* direction.

*Action:* test mean differences (sign-flip permutation on per-subject mean IS, or subject-bootstrap CIs of the IS ratio, as pre-specified in S1 L70). Take direction and significance from the same statistic and recount every "significant" count, including those in the abstract.

**M2. Table 2 mixes estimands.** Ratios come from 50/50 splits (make_tables.py L106), while stars come from LOSO with n−1 calibration nights. In several cells the two point in different directions. Example: LightGBM ST SOL vs constant width has a split ratio of 0.97, but the LOSO ratio is 1.13 with r_rb = +0.82 (p_holm = 0.02). Calibrated centre: HMC REML has split ratio 1.01 and r_rb −0.55; SC N3 % has split ratio 0.99, LOSO 1.01 and r_rb −0.44. *Action:* take ratio, CI and test from one design.

**M3. The within-cohort coverage evidence is guaranteed by construction, and its uncertainty is mis-stated.**
- LOSO conformal coverage is a rank identity. It equals 136/151 = 0.9007 in HMC and 138/153 in SC for the proposed method and the constant-width conformal comparators (e07_loso_coverage_*.csv). The S7 cluster-bootstrap CIs (0.85–0.95; stats.py L15 resamples indicators without re-calibrating) therefore describe no real sampling variability.
- Mean coverage over random splits equals k/(n_cal+1) under within-cohort randomisation: about 0.909 for SC/HMC and 0.913 for ST, matching Table 2 to within Monte-Carlo and grouping error.
- So the ±3 pp criterion could not fail for any exact conformal method, and all met it. Yet the abstract ("89.0–92.1 %") and Conclusions ("verified average coverage") present this as validation, with no spread or CI; the deployment-relevant SD across splits is 0.045 (S2).

*Action:* call within-cohort coverage an implementation check; report the split distribution (e.g. P(coverage < 0.85)); remove or replace the S7 CIs; reserve "verified" for external analyses.

**M4. Conditional and subgroup coverage are pooled over the 8 parameters and mislabelled.** e07 L153 and e11 L83 group by cohort × quartile across all parameters: "81–85 %" in the worst quartile is n = 304 rows = 38 nights × 8 parameters. Per parameter, worst-quartile coverage falls to 67.5 % (SC N1 %), 73.7 % (HMC WASO), 75 % (SC TST, N2 %) and 72.7 % (ST, 11 nights). "Subgroups with ≥40 nights" (Results 3.2) actually applies `count ≥ 40` to night × parameter rows (make_tables.py L282), so subgroups of 6 nights (ST ≥60 y) and 14 nights (ST 40–59 y) are included. No CIs are given. *Action:* report per-parameter conditional coverage with cluster CIs, correct the "≥40 nights" statement, and redo the E11 (Mondrian) summary per parameter.

**M5. Pre-registered analyses are omitted without being declared as deviations (selective reporting).**
- The protocol (S1 L77–80) made superiority conditional also on a positive width–error Spearman correlation whose CI excludes 0. Methods 2.8 silently drops this, and CHANGELOG does not record the change. Mean Spearman is negative for N2 % in ST and HMC for both stagers (−0.06 to −0.16; tableS_all_methods_within), yet N2 % is cited among the "largest gains" (HMC 0.76*). That gain comes from the centre, not from adaptivity.
- Also pre-registered, unreported and absent from CHANGELOG: width-ratio CIs; M ∈ {100, 300, 1000} and calibration-size sensitivity; 50 Hz line noise.

*Action:* report these analyses or list them as deviations with reasons.

## Moderate concerns
**Mo1. The "23 of 24" vote counts are over-interpreted.** They count point ratios below 1 regardless of size or significance (median 0.946; only 13 are significant). The 24 combinations are strongly dependent: the stage percentages sum to 100, TST/SOL/WASO share a window, and all use the same nights. The abstract also picks the most favourable centre (23 vs 18 and 20). *Action:* give a pooled per-cohort geometric-mean IS ratio with a subject-bootstrap CI, and show all three centres in the abstract.

**Mo2. Multiplicity.** Holm is applied per cohort × stager (6 families of 80 tests, plus factorial families) and never across stagers or cohorts, even though claims pool them. Table 3 shows 48 unadjusted Wilcoxon p-values (31 < 0.05), printed as "0.000" and "1.000". The error-analysis vote count (Mann–Whitney 10/24) is unadjusted and rests on about 4–15 missed nights per test. *Action:* declare primary comparisons (vs BA-LoA and constant width, per protocol) and define the families. Adjust Table 3 and print p < 0.001.

**Mo3. Dependence in the paired tests.** LOSO intervals share n−2 calibration nights, so the test conditions on one realised quantile and ignores calibration variability; it is anti-conservative for "method A beats B", especially in ST (22 subjects). *Action:* use the 500 splits with a corrected resampled t-test (Nadeau–Bengio) or a subject bootstrap that re-runs calibration.

**Mo4. AUROC comparisons are untested.** "Better than mean epoch entropy" rests on point estimates:
- SC REML: CIs 0.65–0.82 vs 0.46–0.69 overlap.
- N3 % "modestly better": the HMC CI of the proposed method includes 0.5 (0.49–0.67).
- TST is worse than entropy in HMC (0.68 vs 0.73) and ST (0.80 vs 0.84), yet is described as "comparable".

B = 1000 resamples were used, against 2000 pre-specified. *Action:* paired cluster bootstrap of AUROC differences, with CIs.

**Mo5. Few-night recalibration is partly a theoretical identity, and the risk metric is confounded.**
- With n = 10 and α = 0.1, k = n, so the interval uses the maximum score. Mean coverage is then 10/11 = 0.909 by construction ("91 %"), and P(C < 0.8) = 0.8¹⁰ = 0.107 under exchangeability. That is exactly the reported 11 % (HMC).
- "Realised coverage" adds test-set binomial noise (about 34 ST test nights; theory ≈14 %), so 19 % is not a site-level probability; the median over parameters hides the worst one.

*Action:* report calibration-conditional (PAC-type) coverage per parameter, and state the n needed for P(C < 0.8) ≤ 5 %.

**Mo6. The parametric BA comparator is handicapped.** It uses bias ± z·SD (conformal_eval.py L86), not ±t₍ₙ₋₁₎·SD·√(1+1/n): about 7 % too narrow at n = 22 and 17 % at n = 10, inflating BA under-coverage (83 % in ST; "twice as often" below 80 %). *Action:* use t-based prediction-interval limits of agreement and re-run.

## Minor concerns
**Mi1.** Table 3 ("Bland–Altman analysis", 2.7) gives no limits of agreement and no CIs for bias or ICC (TST heteroscedasticity is weak, ρ = 0.06).
**Mi2.** Methods says "1000–2000" bootstrap resamples, but the code uses B = 1000 throughout (e07 L87, L112).
**Mi3.** Robustness results (200 splits, pooled over cohorts) carry no uncertainty; "degraded less" is untested.
**Mi4.** make_tables.py L466–469 merges into the old manuscript_numbers.json, so stale keys can persist; regenerate it from scratch.
**Mi5.** The abstract says "significantly better in 9 and worse in 4" without naming the test or adjustment. Revise once M1 is fixed.

## Required additional experiments/analyses
1. Mean-based paired inference with ratio CIs, then recounts (M1, M2).
2. Per-parameter conditional coverage with CIs; split-coverage distribution (M3, M4).
3. Pre-registered analyses or declared deviations (M5).
4. AUROC-difference CIs, PAC few-night coverage, t-based BA (Mo4–Mo6).

## Recommendation
**Major revision.** Every number I checked reproduces. But the efficiency inference uses a test whose direction contradicts some reported "significant losses", and Table 2 combines two designs. Headline coverage is guaranteed by construction and carries meaningless CIs, and pooled conditional coverage hides 67–75 % coverage for individual parameters. Pre-registered criteria were dropped without declaration. All of this can be fixed by re-analysing existing outputs.

```json
[
{"id":"M1","severity":"major","title":"Wilcoxon signed-rank does not test mean interval score; significance stars contradict test direction","location":"Methods 2.8; Table 2; Results 3.3; Abstract; code/scripts/make_tables.py L122-129, L249-250; results/statistics/e07_paired_tests_*.csv, e07_factorial_tests_*.csv","evidence":"Sign of r_rb contradicts mean-IS sign in 7/126 (YASA) and 10/138 (LightGBM) significant tests. YASA HMC SOL vs BA '1.39*' counted as a loss, but r_rb=-0.64 favours the proposed method (p_holm=5.6e-10); a sign-flip permutation test of the mean gives p=0.25 (one subject +2448). 3 of 7 LightGBM factorial 'significant increases' are rank-significant in the opposite direction.","action":"Use mean-based paired inference (sign-flip permutation or subject-bootstrap CI of the IS ratio, as pre-specified); take direction and significance from the same statistic; recount all significant counts.","needs_experiment":false},
{"id":"M2","severity":"major","title":"Table 2 combines 50/50-split ratios with LOSO significance","location":"Table 2; make_tables.py L106-109","evidence":"LightGBM ST SOL vs constant: split ratio 0.97, LOSO ratio 1.13, r_rb +0.82, p_holm 0.02; HMC REML (calibrated centre) split ratio 1.01 vs r_rb -0.55.","action":"Report ratio, CI and test from one design.","needs_experiment":false},
{"id":"M3","severity":"major","title":"Within-cohort coverage is guaranteed by construction; S7 bootstrap CIs are meaningless; no CIs in main text","location":"Abstract; Results 3.2; Conclusions; Supplementary S7; stats.py L15-29","evidence":"LOSO coverage = 136/151 = 0.9007 (HMC) and 138/153 (SC) for the proposed and constant-width conformal methods (rank identity); split means about k/(n_cal+1) = 0.909/0.913; the ±3 pp criterion cannot fail for exact conformal methods; split SD 0.045 not reported in the main text.","action":"Present within-cohort coverage as an implementation check; report the split coverage distribution and P(coverage<0.85); remove or replace the S7 CIs; temper 'verified coverage'.","needs_experiment":false},
{"id":"M4","severity":"major","title":"Conditional and subgroup coverage pooled over parameters; '≥40 nights' is really ≥40 rows","location":"Results 3.2; Discussion limitation (i); e07 L153; e11 L83; make_tables.py L282","evidence":"Worst-quartile 81-85 % pools 8 parameters (n=304 = 38 nights x 8); per parameter coverage falls to 67.5 % (SC N1%), 73.7 % (HMC WASO), 75 % (SC TST). Subgroups with 6 and 14 nights (ST age) are included under '≥40 nights'.","action":"Report per-parameter conditional coverage with cluster CIs; fix the threshold statement; redo E11 per parameter.","needs_experiment":false},
{"id":"M5","severity":"major","title":"Pre-registered criteria and analyses omitted without declaration","location":"Methods 2.8 vs Supplementary S1 L49-80; CHANGELOG.md","evidence":"Spearman (width vs error) success criterion dropped; mean Spearman negative for N2% in ST/HMC for both stagers (-0.06 to -0.16) while HMC N2% is cited as a 'largest gain'. Width-ratio CIs, M sensitivity, calibration-size sensitivity and 50 Hz line noise not reported and not in CHANGELOG.","action":"Report these analyses or declare them as deviations with reasons.","needs_experiment":true},
{"id":"Mo1","severity":"moderate","title":"'23 of 24' vote counts over-interpreted","location":"Abstract; Results 3.3; Highlights","evidence":"Counts point ratios below 1 regardless of significance (13 significant; median ratio 0.946) across 24 dependent combinations; the abstract shows the most favourable centre (23 vs 18/20).","action":"Pooled per-cohort geometric-mean ratio with subject-bootstrap CI; show all centres.","needs_experiment":false},
{"id":"Mo2","severity":"moderate","title":"Multiplicity scope and unadjusted Table 3 / error-analysis tests","location":"Methods 2.8; Table 3; Results 3.6","evidence":"Holm within cohort x stager only (6 families of 80 tests); Table 3 has 48 unadjusted p-values (31 < 0.05) printed as 0.000/1.000; Mann-Whitney vote count 10/24 on about 4-15 missed nights.","action":"Define primary comparisons and families, adjust Table 3, report p<0.001.","needs_experiment":false},
{"id":"Mo3","severity":"moderate","title":"Paired LOSO tests ignore calibration-set dependence","location":"Methods 2.8; e07 paired_tests","evidence":"LOSO intervals share n-2 calibration nights; the test conditions on one realised quantile; ST has 22 subjects.","action":"Corrected resampled t-test over the 500 splits, or a subject bootstrap that re-runs calibration.","needs_experiment":false},
{"id":"Mo4","severity":"moderate","title":"AUROC superiority claims untested","location":"Results 3.8; Fig. 3d; S14","evidence":"SC REML CIs overlap (0.65-0.82 vs 0.46-0.69); HMC N3% proposed CI includes 0.5; TST proposed below entropy in HMC (0.68 vs 0.73) and ST, called 'comparable'; B=1000 vs pre-specified 2000.","action":"Paired cluster bootstrap of AUROC differences with CIs.","needs_experiment":false},
{"id":"Mo5","severity":"moderate","title":"Few-night recalibration statistics partly theoretical identity; risk metric confounded by test noise","location":"Results 3.5; Discussion 'Clinical use'; S17","evidence":"n=10, alpha=0.1 gives k=n: mean coverage 10/11=0.909 and P(C<0.8)=0.8^10=0.107, which equals the reported 11 %; ST 19 % includes binomial noise from about 34 test nights (theory about 14 %); median over parameters hides the worst.","action":"Report calibration-conditional (PAC) coverage per parameter and the n needed for P(C<0.8)<=5 %.","needs_experiment":false},
{"id":"Mo6","severity":"moderate","title":"Parametric BA comparator uses z instead of a t-based prediction interval","location":"conformal_eval.py L83-86; Results 3.2, 3.5","evidence":"bias ± 1.645·SD is about 7 % too narrow at n=22 and 17 % at n=10 versus t·SD·sqrt(1+1/n), inflating BA under-coverage.","action":"Use prediction-interval limits of agreement and re-run.","needs_experiment":true},
{"id":"Mi1","severity":"minor","title":"Point-estimate agreement lacks LoA and CIs","location":"Table 3; Methods 2.7","evidence":"Only bias, MAE and ICC are given; no LoA or CIs (ICC formula verified correct).","action":"Add LoA and bootstrap CIs.","needs_experiment":false},
{"id":"Mi2","severity":"minor","title":"Bootstrap resample count misreported","location":"Methods 2.8; e07 L87, L112","evidence":"Methods says 1000-2000; code uses B=1000.","action":"Correct the text or use 2000.","needs_experiment":false},
{"id":"Mi3","severity":"minor","title":"Robustness results without uncertainty","location":"Results 3.7; S12","evidence":"200 splits pooled over cohorts; 'degraded less' untested.","action":"Add split SDs or CIs.","needs_experiment":false},
{"id":"Mi4","severity":"minor","title":"Stale keys can persist in manuscript_numbers.json","location":"code/scripts/make_tables.py L466-469","evidence":"old.update(NUM) keeps keys no longer generated.","action":"Regenerate the file from scratch.","needs_experiment":false},
{"id":"Mi5","severity":"minor","title":"'Significantly' in the abstract without the test named","location":"Abstract Results","evidence":"'significantly better in 9 and worse in 4' depends on the flawed direction logic (M1).","action":"Revise after M1; name the test and adjustment.","needs_experiment":false}
]
```
