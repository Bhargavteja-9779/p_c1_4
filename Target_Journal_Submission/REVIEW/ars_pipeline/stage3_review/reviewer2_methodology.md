## Methodology Review Report (Peer Reviewer 1)

Pipeline run `ars-p_c1_4-2026-11-20-a`, Stage 3, Phase 1, Peer Reviewer 1 seat (`methodology_reviewer_agent.md`, Reviewer Configuration Card #2). Standard mode: no sprint contract was supplied. Criteria binding: `criteria_binding_unavailable`. No `ReviewCriteriaBindingManifest` or Target Criteria Brief came with the dispatch, so the judgements below use the ARS review-criteria framework and Card #2.

I wrote this report without opening any other reviewer's output. I read the Phase 0 file. I consulted `stage2_5_integrity/reverification_round1.md` only after forming my own view, and only to avoid repeating numeric items it already resolved. Line numbers `Lnnn` refer to `manuscript/build/manuscript_rendered.md`. Every number marked "recomputed" comes from my own scripts in `/tmp/claude-0/-home-user-p-c1-4/9c52bd2c-f480-55be-800e-d02a6653c94b/scratchpad/rev_method/` (`a2.py` to `a5.py`), run on the shipped `results/raw/*.csv.gz` and `results/statistics/*.csv` files.

### Reviewer Identity
I am a biostatistician working on clinical measurement and prediction methodology. I specialise in distribution-free prediction intervals (split conformal, cross-conformal, CV+/jackknife+) and in method-comparison analysis (parametric and regression-based Bland–Altman, ICC) of clustered, repeated-measures data. I also work on Bayesian computation for state-space models. My question for this paper is whether the stated validity claim and the comparative claims survive the resampling and fitting scheme that was actually run.

### Overall Recommendation
Major Revision

### Confidence Score
4. I read all of the relevant code and recomputed the key quantities from the stored per-night and per-split results. I did not re-run the pipeline. In particular, I did not run a CV+ re-analysis, so the direction of the cross-fitting effect (M-3) is inferred from coverage bounds and has not been measured directly.

Confidence is an uncertainty/scope disclosure only; it never changes consensus counts, severity, decision bearing, or arbitration.

### Calibration Status
`NOT_CALIBRATED`

Seat reports always emit `NOT_CALIBRATED`: the final panel topology is not knowable until every seat has completed.

### Criterion-Bound Judgements
| Dimension / criterion | Criterion source | Judgement | Evidence anchors | Rationale | Uncertainty or scope limit | Decision bearing? |
|---|---|---|---|---|---|---|
| Validity claim matches the design that was run | Card #2 focus 1; framework "Conclusion conservatism" | PARTLY_MEETS | L88; L95; L35; L166; `e12_honest_protocol.py:47-61`; `conformal_eval.py:250-254` | Methods (L88) correctly say there is no finite-sample guarantee. The Abstract and Conclusion still say "valid" with no qualifier. Night-level exchangeability fails in the two-night cohorts (M-2), and the cross-fit asymmetry is untested (M-3). | The direction of the cross-fit effect is inferred, not measured | yes: the paper's central claim |
| Fair comparators (equal information) | Card #2 focus 2 | DOES_NOT_MEET | L91; L127; `e15_paired.csv`; `conformal_eval.py:191-213` | All three LoA variants are centred on the raw plug-in. The proposed interval uses recalibrated probabilities. The TST advantage over LoA is partly a centre (recalibration) effect (M-1). | none identified | yes: headline comparative claim |
| Multiplicity and inference | Card #2 focus 2; statistical_reporting_standards §4.5 | PARTLY_MEETS | L108; `stats.py:198-233`; `e15_honest_stats.py:72-73` | The Holm families match the text: 80 tests per stager×cohort, plus a separate family of 16. Inference ignores calibration-set variability; a corrected test weakens several TST results (M-4). | The Nadeau–Bengio correction is approximate | yes |
| Pre-specification and disclosure | Card #2 focus 3; §4.2 HARKing | PARTLY_MEETS | L88; L161(vi); S1 items 1–15; S9 | The deviation log is unusually complete. Main-text summaries understate it, and the "same qualitative conclusions" claim is only partly supported (M-8). | Protocol timing cannot be verified (S1 says so) | yes |
| Small-sample coverage risk and the "≥ 20 nights" advice | Card #2 focus 4 | DOES_NOT_MEET | L137; L159; L166; Fig. 3c,f; `e15_local.csv` | The risk figures reproduce textbook Beta/binomial behaviour. In ST they mostly measure test-set size (M-5). | none identified | yes: a practice recommendation |
| Decided-subset vs all-night accuracy | Card #2 focus 4 | PARTLY_MEETS | L33; L143; `e15_honest_stats.py:98-117` | The reference line is the uncorrected plug-in. The calibrated plug-in with a simple margin rule matches the interval decisions (M-6). | none identified | yes: claim in the Abstract |
| Posterior construction (τ, BCTS, smoothing, censoring) | Card #2 focus 5 | PARTLY_MEETS | L65-77; `hmm.py:250-278`; `night_summary.py:34-43` | Implemented as described. τ is fitted to epoch-level likelihood, its value in the primary design is not reported, and its interpretation is thin (m-3). | none identified | no |
| Data handling and leakage | Card #2 focus 5; framework "Internal validity" | PARTLY_MEETS | L59; S1 item 9; S16 "Label leakage via unscored epochs"; `night_summary.py:67-73` | The code matches §2.2. S16 contradicts it, and two S16 rows describe the superseded design (m-2). | Few epochs are affected (SC mean 1.9 per night, ST 8.3, HMC 0) | no |
| Reproducibility (code vs Methods) | framework "Statistical reporting completeness" | MEETS | `code/`; `results/` | The code does what §2.5–2.8 say. Stale dead code and thin tests remain (m-8). | Full pipeline not re-run | no |
| Statistical reporting completeness | statistical_reporting_standards §1, §6 | PARTLY_MEETS | Table 2; L108; L143 | Ratios have CIs. Adjusted p-values are shown only as asterisks, decision accuracies have no CIs, and the per-split percentile range rests on 50 values. | none identified | no |

These judgements are not totalled, weighted or mapped mechanically to the recommendation.

### Summary Assessment
The paper proposes conformal calibration of FFBS posterior spreads to obtain per-night intervals for eight sleep parameters, and compares them with three forms of limits of agreement (LoA) on 348 nights. Methodologically it is better than most submissions in this area. It has an end-to-end protocol in which every label-dependent component is fitted on calibration subjects. It states openly (L88) that its cross-fitted design carries no finite-sample guarantee. It runs a centre×scale factorial that isolates the adaptive scale. Its deviation log is detailed. I nevertheless see four problems that bear on the decision.

1. The headline comparison with LoA is not like-for-like. The LoA are centred on the raw stager output, while the proposed interval uses locally recalibrated probabilities. In ST the whole TST advantage disappears against a constant-width interval around the calibrated plug-in.
2. Two nights per subject break the night-level exchangeability that the "exactly valid" and finite-sample statements rely on. I show by resampling that this, not quantile instability, explains the under-coverage of distribution-free LoA in ST.
3. The significance statements condition on the realised calibration sets. A corrected resampled test weakens several TST comparisons, and the pre-specified analysis (S9) finds the TST advantage over distribution-free LoA significant in 4 of 6 combinations, not 6 of 6.
4. The site-level coverage risk behind the "≥ 20 nights" recommendation is what conformal theory predicts analytically. In ST it is driven by the number of test nights left over, not by the number of calibration nights.

All four can be fixed from the stored predictions, without new data. After these fixes the paper would make a narrower but defensible claim: a roughly 10–16 % interval-score gain from the adaptive scale for TST, on top of a larger gain from local recalibration that LoA users could also obtain.

### Strengths
1. **End-to-end fitting of all label-dependent components on calibration subjects only**: BCTS, π_s, A, p0, τ and the conformal quantile are refitted in every split, and splits are grouped by subject [code: `e12_honest_protocol.py:47-61, 123-131`; L95]. This removes the main leakage path of the earlier design (S1 item 7) and mirrors how a laboratory would deploy the method.
2. **Honest statement of the guarantee**: L88 and S1 item 8 say correctly that the K-fold jackknife-type design has no distribution-free guarantee, cite the CV+ bound (≥ 1−2α) correctly, and present validity as an empirical property [L88].
3. **Centre×scale factorial and fixed-centre scale tests**: these separate calibration from adaptivity. The fixed-centre comparisons (SCALE@ rows) give a clean estimate of what the posterior scale adds [L91; L125; `e15_paired.csv`, SCALE@ rows: TST ratios 0.84–0.92].
4. **Unit of analysis and test choice**: per-subject means, a sign-flip test of the mean difference that matches the reported ratio of means, a subject bootstrap, and Holm families that match the text (80 tests plus 16 per stager×cohort, checked in `e15_honest_stats.py:72-73` and in the p_holm floor of 0.0040 = 80 × 1/20001).
5. **Label-free analysis windows, and automatic parameters computed with no reference mask** [L59; `night_summary.py:69-73`].
6. **A detailed, chronological deviation log**, including the admission that repository history cannot date the protocol [S1, "Deviations" ¶1].

### Weaknesses
(Full detail is in "Detailed Comments", M-1 to M-8 and m-1 to m-11.)
1. **Unequal information between the proposed interval and the LoA comparators (M-1).** Severity: Major | Evidence anchor: `table: e15_paired.csv TST rows`; `manuscript: L127, L33, L23` | Confidence: 5. I recomputed the ratios from the stored results.
2. **Night-level exchangeability fails with two nights per subject (M-2).** Severity: Major | Evidence anchor: `manuscript: L120, L91(c), L161(ii)`; `code: a2.py` resampling | Confidence: 5. Direct resampling check.
3. **The cross-fit/full-model asymmetry is not tested and is not neutral (M-3).** Severity: Major | Evidence anchor: `code: e12_honest_protocol.py:55-61`; `table: e15_summary.csv HMC coverage` | Confidence: 3. Inferred from coverage bounds, not measured.
4. **Inference ignores calibration-set variability; the significance counts are fragile (M-4).** Severity: Major | Evidence anchor: `code: stats.py:198-218`; `a5.py`; S9 | Confidence: 4.
5. **Coverage-risk analysis and the "≥ 20 nights" recommendation (M-5).** Severity: Major | Evidence anchor: `manuscript: L137, L159, L166`; Fig. 3c,f; `a3.py` | Confidence: 5.
6. **Decided-subset accuracy is benchmarked against the uncorrected plug-in (M-6).** Severity: Major | Evidence anchor: `manuscript: L33, L143`; `a4.py` | Confidence: 5.
7. **Pre-specification is summarised inaccurately in the main text (M-8).** Severity: Major | Evidence anchor: `manuscript: L88, L161(vi)`; `supplement: S1 items 1, 7, 13; S9` | Confidence: 5.

### Detailed Comments

Each comment gives its severity, location, problem, fix, and a flag: [FIXABLE-IN-REPO] means a text change or a re-analysis from stored predictions and results; [NEEDS-NEW-DATA] means new data are required.

#### Research Questions & Hypotheses
The five research questions (L50) are clear, and the design can answer them. The hypothesis in the protocol (S1) is that the FFBS spread "ranks nights by their actual parameter error" and gives intervals narrower than constant-width intervals "for any base stager". The data falsify this for most parameters, and the paper says so (L127, L151). That is to its credit. The problems below concern how the remaining positive claim (TST) is attributed and tested.

#### Research Design

**M-1. MAJOR. The LoA comparators are denied the locally recalibrated centre, so the TST advantage over LoA mixes recalibration with the conformal scale.** Location: L91 (a)–(c); L127; L151; L159; Abstract L33; Highlight L23; Table 2; `conformal_eval.py:191-213` (all three LoA use `cal["plug"]`, the argmax of the *uncalibrated* probabilities, `night_summary.py:72`).

- *Problem.* The proposed interval is centred on μ̂ from BCTS-recalibrated probabilities fitted on the calibration nights. Recalibration alone halves the TST MAE in HMC (40 to 20 min; Table 3). The LoA can shift by a constant bias but cannot absorb the per-night part of that improvement.
- *What the stored results show* (`e15_paired.csv`, TST; ratio < 1 favours the proposed method):

| Stager / cohort | vs distribution-free LoA (scp_signed) | vs constant width around calibrated plug-in (scp_abs_cal) | fixed-centre scale effect (SCALE@FFBS mean) |
|---|---|---|---|
| YASA SC | 0.86 | 0.86 | 0.90 |
| YASA ST | 0.64 | **1.18** (0.97–1.37), n.s. | 0.92 |
| YASA HMC | 0.73 | 0.84 | 0.84 |
| LightGBM SC | 0.79 | 0.81 | 0.92 |
| LightGBM ST | 0.65 | 0.85 (0.57–1.31), n.s. | 0.90 |
| LightGBM HMC | 0.66 | 0.78 | 0.86 |

  For YASA in ST, the proposed interval is 18 % worse (not significant) than a constant-width interval around the calibrated plug-in. The "0.64" advantage over distribution-free LoA in that cohort is therefore recalibration, not the posterior scale. In HMC roughly half of the log-advantage comes from the centre. The genuine scale effect for TST is the fixed-centre ratio of 0.84–0.92. That is a real but smaller result than "lower interval scores than every LoA variant in all cohorts (ratio 0.64–0.86)".
- *Why it matters.* The Abstract, Highlights, Discussion ¶1 and Conclusion rest the paper's significance on this comparison. A laboratory that recalibrates its stager (step ii in L159, which the paper itself recommends) would compute LoA around the recalibrated output.
- *Fix.*
  - Add the three LoA variants computed around the calibrated plug-in (`plugc` is already stored per night in `e12_nights_*.csv.gz`, and the LoA formulas need only (y, plugc)) to Table 2 and Fig. 2, or replace the raw-centred ones with them.
  - Report the decomposition of the TST advantage into centre and scale.
  - Restate the claims: the scale gain for TST is about 10–16 %; most of the remaining gain is recalibration, which is available to any method.
  - Keep raw-centred LoA as the "current practice" reference, labelled as such.

  [FIXABLE-IN-REPO]

**M-2. MAJOR. Two nights per subject break the night-level exchangeability on which the finite-sample and "exactly valid" statements rest. The ST under-coverage of distribution-free LoA is a clustering effect, not quantile instability.** Location: L88 (finite-sample statement); L91 (c) "exactly valid"; Table 2 caption "exact split-conformal limits"; L120 ("22 calibration nights … make the extreme residual quantiles unstable"); L161 (ii); `conformal_eval.py:280-286` (subject-grouped split) with night-level scores in `conformal_quantile`.

- *Problem.* Splits are grouped by subject, which is correct for leakage, but the conformal quantile is taken over nights. In ST every subject has two nights (placebo and temazepam), and in SC almost every subject does. Random subject-level assignment makes *subjects* exchangeable between calibration and test, not nights. The night-level guarantee P{θ ∈ C} ≥ 1−α therefore does not apply, even for the non-cross-fitted distribution-free LoA. Quantile instability raises the split-to-split variance; it cannot push the *mean* over random splits below nominal. Clustering can.
- *Check* (`a2.py`). I held each cohort's stored (y, plug-in) pairs fixed (YASA), resampled 2,000 random splits, and computed the coverage of distribution-free LoA:

| ST parameter | subject-grouped splits | night-level splits |
|---|---|---|
| TST | 0.900 | 0.912 |
| WASO | 0.888 | 0.912 |
| N2 % | 0.881 | 0.911 |
| N3 % | 0.903 | 0.915 |
| SOL | 0.907 | 0.926 |
| REML | 0.894 | 0.913 |

  In SC the two schemes agree (0.917–0.925), because calibration halves are larger and fewer subjects contribute two very different nights.
- *Why it matters.* Coverage of the proposed method is counted per night under the same clustering. Its apparent robustness may come from the conservatism discussed in M-3, not from validity under clustering. Limitation (ii) L161 mentions the issue but attributes the ST shortfall to small samples.
- *Fix.*
  - Correct L120, L91 (c) and the Table 2 caption. "Exactly valid" holds only for exchangeable units.
  - Either use a cluster-aware calibration, such as one randomly chosen night per calibration subject, or the subject-level pooled-CDF or subsampling procedures for hierarchical data (Dunn, Wasserman & Ramdas, 2022/2023, two-layer hierarchical conformal prediction; please verify the citation), or report coverage as the mean over *subjects* of per-subject coverage.
  - State the effective calibration size in subjects (ST: 11).

  [FIXABLE-IN-REPO]

**M-3. MAJOR. The cross-fit/full-model asymmetry is neither neutral nor tested. Coverage in HMC exceeds the ceiling that exchangeable split conformal allows, which shows that calibration and test scores are not exchangeable.** Location: L88; L95; `e12_honest_protocol.py:55-61` (calibration scores from fold models fitted on about 80 % of the calibration half; test summaries from `sm_all`); `conformal_eval.py:251` (σ̄ over `concatenate([sc, st])`, which mixes fold-model and full-model SDs).

- *Problem.* With continuous scores and exchangeability, split conformal coverage is at most 1−α+1/(n+1). For HMC (no clustering, n_cal = 76) that ceiling is 0.913. The proposed interval's mean coverage in HMC is 0.914–0.920 for 5 of 8 parameters (N2 % 0.914, N3 % 0.915, WASO 0.918, REM % 0.919, SOL 0.920; `e15_summary.csv`). The same holds for the other cross-fitted centre (scp_abs_cal, up to 0.922).
- This suggests that calibration scores, from weaker fold models, are slightly larger than test scores from the full model. The intervals are then mildly conservative, which costs efficiency against the LoA comparators, which are not cross-fitted. The evidence is weak: the Monte-Carlo SE of the 50-split mean is about 0.005, and SOL may have ties [partly unverified].
- The direction is not guaranteed. With a more flexible stager or HMM, the full-half model could overfit and make the intervals anti-conservative. The symmetry argument for σ̄ in L84 ("keeps the score a symmetric function of the data") does not apply in this design, because calibration and test scores already come from different functions.
- *Fix.* Run, as a sensitivity analysis from the stored predictions (`results/predictions/`; FFBS plus summaries cost about 0.02 s per night):
  - (a) CV+: apply each fold model to the test nights and use the CV+ interval, which carries the ≥ 1−2α guarantee the paper cites; and
  - (b) a plain split: fit the HMM and BCTS on one half of the calibration subjects and conformalise on the other half, which carries the exact guarantee.

  Report coverage and interval score next to the primary design. Either result removes the need to rely on L88's "empirical property" caveat. [FIXABLE-IN-REPO]

#### Sampling Strategy

**M-5. MAJOR. The site-level coverage risk, and the "≥ 20 nights" recommendation built on it, restate known Beta/binomial behaviour of split conformal. In ST the metric is dominated by the number of test nights left over.** Location: L33; L137; L159; L166; Fig. 3c,f; `e15_honest_stats.py:41-44` (`p_cov_lt80` over the remaining target nights).

- *Problem.* For exact split conformal, coverage conditional on the calibration set follows Beta(k, n+1−k) with k = ⌈(n+1)(1−α)⌉ (Vovk 2012; Angelopoulos & Bates 2023). This gives P(conditional coverage < 0.80) of 0.107 at n = 10, 0.069 at n = 20 and 0.044 at n = 30 (`a3.py`).
- The reported realised-coverage risk then adds binomial noise from the test nights. In ST the number of test nights shrinks as n_t grows: 34, 24 and then only 14 at n_t = 30. With conditional coverage exactly 0.90, P(realised coverage < 0.80) is already 0.158 for 14 test nights, from test sampling alone. A Beta-binomial combination predicts 0.14, 0.14 and 0.18 for ST and 0.108, 0.077 and 0.056 for HMC.
- The observed values (Fig. 3c: ST 0.17, 0.15, 0.15; HMC 0.09, 0.07, 0.07) match these predictions. So:
  - (i) the statement "even 30 left a risk of 15 % in the small ST cohort" (L159) measures the size of the ST test set, not the calibration set;
  - (ii) the HMC numbers show no excess risk beyond exact conformal theory;
  - (iii) the "≥ 20" threshold is not derived from any stated tolerance.
- *Fix.*
  - Report calibration-conditional coverage separately from test noise, for example from the HMC runs with 121–141 test nights or analytically.
  - Base the recommendation on an explicit rule: choose n so that P(coverage given calibration < 1−α−ε) ≤ δ, using the Beta distribution. Alternatively use the training-conditional (PAC) conformal adjustment, which takes a slightly higher quantile to guarantee such a bound.
  - Delete the ST n_t = 30 statement. The cross-reference to distribution-free LoA "needing 19 nights" is arithmetic (⌈(n+1)·0.95⌉ ≤ n), not evidence.

  [FIXABLE-IN-REPO]

Additional sampling notes:
- The local-deployment ST draws pick whole subjects until there are ≥ n_t nights (`e12_honest_protocol.py:96-107`). Ten nights therefore means five subjects with two nights each, which compounds M-2.
- 348 nights is adequate for marginal coverage but leaves the hard-night quartile (about 87 nights pooled) and the subgroups imprecise. No precision target or power argument is given. Acceptable for a methods paper, but the "concentrated in difficult nights" statement (L129) carries no test (m-6).

#### Data Collection

**m-2. MINOR. Handling of unscored epochs is described inconsistently, and S16 describes the superseded design.** Location: L59; S1 item 9; S16 row "Label leakage via unscored epochs" ("Marked −1 and excluded identically from reference and automatic parameters"); S16 row "Leakage through HMM parameters" ("within-cohort 5-fold cross-fitting"); `night_summary.py:67-73`.

- The code follows §2.2: reference unscored epochs count as wake, and automatic parameters use all epochs. The S16 table contradicts this. The S16 HMM row describes the pre-specified design, not the primary one.
- The number of epochs affected is small (recomputed from `results/summaries/yasa_xfit.csv`: mean unscored epochs per night SC 1.9, ST 8.3, HMC 0; 653 epochs in total). So this is a documentation fault.
- R&K "movement time" counted as wake lowers reference TST slightly in SC and ST. State the size of this effect.
- *Fix:* update the two S16 rows and add the counts. [FIXABLE-IN-REPO]

**m-9. MINOR. The LightGBM stager folds are not nested in the calibration/test splits.** Location: L62; `results/predictions/folds_sc.csv`. The SC predictions for calibration nights come from stager models trained on folds that include test-half subjects. This is a mild dependence between calibration and test nights, not direct leakage, because each night's prediction is out-of-fold. Acknowledge it, or report YASA as the clean case. [FIXABLE-IN-REPO] [unverified magnitude]

#### Analysis Methods

**M-4. MAJOR. Significance ignores calibration-set variability and the dependence it induces across subjects. Several TST "significant" results are fragile.** Location: L108; L127; L151 ("significantly so against distribution-free limits"); `stats.py:198-218`; `e15_honest_stats.py:49-74`.

- *Problem.* Each subject's interval score is averaged over the 50 splits in which it was tested, and the sign-flip test then treats the 78, 22 or 151 subject means as independent. The subject means share calibration sets: any two subjects were tested together in about 25 % of splits under the same conformal quantile. Variability from which subjects end up in the calibration half is not part of the null. This is the known anti-conservatism of repeated-split comparisons (Nadeau & Bengio 2003; Bates, Hastie & Tibshirani 2024).
- *Check* (`a5.py`). A Nadeau–Bengio corrected resampled t on the 50 per-split differences (correction factor 1/J + n_test/n_cal; unadjusted p-values) gives, for TST against distribution-free LoA:

| Stager / cohort | corrected p (unadjusted) |
|---|---|
| YASA SC | 0.014 |
| YASA ST | 0.002 |
| YASA HMC | **0.077** |
| LightGBM SC | 0.035 |
| LightGBM ST | 0.037 |
| LightGBM HMC | 0.004 |

  None of the LightGBM SC/ST values or the YASA HMC value would survive a Holm family of 80. The pre-specified analysis (S9, LOSO) also finds TST against distribution-free LoA significant in only 4 of 6 combinations: YASA HMC 0.71 (0.55–0.92) and LightGBM SC 0.80 (0.67–0.96) are not significant. The text reports 6 of 6.
- The Nadeau–Bengio correction is itself approximate, so I offer this as a sensitivity result, not a verdict.
- The permutation resolution is not a problem: the minimum p is 1/20001 and the Holm floor is 0.004 with m = 80.
- *Fix.*
  - Add a split-aware sensitivity analysis: corrected resampled t, or a two-level bootstrap that resamples subjects and re-draws calibration halves.
  - Report adjusted p-values, not only asterisks.
  - Phrase the TST claim through effect sizes and CIs, and drop "significantly in every cohort" unless it survives.

  [FIXABLE-IN-REPO]

**M-6. MAJOR. The clinical-decision analysis credits the interval with what the recalibrated centre does.** Location: Abstract L33; L143; Fig. 5e–h caption ("Dotted line: … uncorrected automatic value"); `e15_honest_stats.py:98-117`.

- *Problem.* An interval lies entirely on one side of 360 min only when its centre does. So the accuracy of "decided" nights equals the accuracy of the calibrated centre on those nights. I recomputed: on the decided nights the calibrated plug-in is correct in 98.7 %, identical to the interval decisions.
- The comparison offered (raw plug-in, 97.2 % on the same nights, 84.2 % on all nights) uses the *uncorrected* stager. The calibrated plug-in is right on 91.3 % of all night-repetitions.
- A label-free rule that abstains on the nights whose calibrated plug-in lies closest to 360 min decides 64.3 % of nights with 98.4 % accuracy, against 63.9 % and 98.7 % for the proposed interval (`a4.py`). The interval-specific contribution is about 0.3 percentage points.
- The figures pool 8,672 night×repetition rows from three cohorts with different prevalence, and give no CIs.
- *Fix.*
  - Use the calibrated plug-in as the reference line.
  - Add the margin-rule baseline, or a risk–coverage curve comparing interval-based and margin-based abstention.
  - Report per cohort, with subject-bootstrap CIs.
  - Restate the Abstract sentence.

  [FIXABLE-IN-REPO]

**m-1. MINOR. The σ̄ computed over calibration and test nights is batch-dependent, and no deployment rule is given.** Location: L84; `conformal_eval.py:251`. The interval for a night depends on which other test nights were processed with it. In deployment nights arrive one at a time. State the rule (for example σ̄ from the calibration nights plus the current night; S1 item 4 says the numerical difference is negligible) and evaluate that rule. See M-3 on why the symmetry rationale does not hold in the cross-fitted design. [FIXABLE-IN-REPO]

**m-3. MINOR. The τ fitting and its interpretation.** Location: L77; L117; `hmm.py:263-278`.

- τ maximises the epoch-level smoothed log-likelihood, not the calibration of night-level parameters.
- The grid steps from 0.10 straight to 0.15. τ in the pre-specified summaries is 0.10–0.15 (recomputed: HMC mean 0.12; SC and ST all 0.10).
- τ in the primary design is refitted in every split but is neither stored nor reported. L117 reports only the pre-specified value.
- With τ ≈ 0.1 the emissions are flattened tenfold, so much of the posterior spread comes from the population transition prior. That bears on what the "posterior SD" measures and on why it explains TST error but not stage-percentage error (L155).
- *Fix:* report the distribution of τ across splits and local runs, refine the grid, and discuss the meaning of τ. [FIXABLE-IN-REPO]

**m-4. MINOR. REM latency censoring.** Location: L59; `night_summary.py:46-58`. Samples with no REM are given the window end and enter μ̂ and σ̂ as if observed. That inflates σ̂ for nights near the boundary. State this, and the share of nights with censored samples. [FIXABLE-IN-REPO]

**m-5. MINOR. Ratio of means of interval scores.** Location: L108; Table 2. Ratios of means are dominated by subjects with large misses (2/α = 20× penalty). Add the mean per-subject log-ratio, or the median, as a sensitivity analysis, to show the conclusions do not depend on a few nights. [FIXABLE-IN-REPO]

**m-7. MINOR. Regression-based LoA are implemented with z and no prediction-variance term, while parametric LoA get t·√(1+1/n).** Location: L91 (b); `conformal_eval.py:203-213`. Part of the under-coverage (ST 0.75–0.85) is due to this asymmetry. In HMC (n = 76) the shortfall persists (0.85–0.91), so the conclusion probably holds. Treat the comparators alike, or add a conformalised regression-LoA (normalised score with the fitted |residual| line as scale). [FIXABLE-IN-REPO]

#### Results Presentation

**M-8. MAJOR. The main text summarises pre-specification less accurately than S1 does.** Location: L88; L161 (vi); L125; S1 items 1, 7, 13; S9; S10 "Miscoverage level α".

- L88 says the protocol fixed "the method, its score and α" and that "the one later change" was σ̄. S1 also lists:
  - the τ grid extension (item 1), a change to the method;
  - the change of primary design (item 7);
  - dropping n_t = 50 and cutting 500 repetitions to 50 (item 7);
  - a change of test (item 11);
  - the Spearman criterion run late (item 13).
- S1 states that the repository cannot date the protocol, because the first commit contains interval outputs. L88's "written before any interval was computed" should carry that caveat.
- The protocol's joint adaptivity criterion is evaluated with interval scores from the end-to-end design and Spearman correlations from the pre-specified design (L125).
- The pre-specified α ∈ {0.05, 0.1, 0.2} sensitivity analysis is in S10 but is not mentioned in the main text.
- "The pre-specified analysis led to the same qualitative conclusions" (L161) holds in direction, but not for the significance of the TST advantage over distribution-free LoA (4 of 6 in S9 against 6 of 6; see M-4).
- *Fix.* Rewrite the last sentence of L88 to list all changes to the method (σ̄, τ grid) and to the primary analysis, with the dating caveat. Evaluate the joint criterion within one design. Summarise the α sensitivity analysis in §3.8. Qualify the L161 sentence. [FIXABLE-IN-REPO]

**m-6. MINOR.**
- "Advantage concentrated in difficult nights" (L129) compares counts with no test or CI.
- The coverage range from the 2.5th to the 97.5th percentile over 50 splits is the 2nd and 49th order statistic. Use ≥ 200 splits for that summary, or present it as a range.
- Decision accuracies (L143) lack CIs.

[FIXABLE-IN-REPO]

**m-10. MINOR. "Valid" with no qualifier.** Location: Abstract L35; Highlight L22; L166. Write "achieved nominal marginal coverage within cohort when locally calibrated (empirical; no finite-sample guarantee for the design used)". Card #2 asks that "valid" mean what the design guarantees. Here the design guarantees nothing finite-sample (L88). [FIXABLE-IN-REPO]

#### Reproducibility

**m-8. MINOR. Code hygiene and tests.**
- `src/uncertainty/conformal.py:69-100`: `interval()`/`_scale` implement `norm_reg` with the *calibration-only* median, and the module docstring says "median_cal(sigma)". This is dead code that contradicts §2.5. Remove or update it.
- `tests/test_core.py` contains no test of the cross-fitted pipeline, `scp_signed` or `ba_reg`. The coverage test accepts a mean of ≥ 0.88. `test_sleep_params_mask_and_no_rem` exercises a mask path the primary analysis no longer uses.
- Add a simulation test of the cross-fit coverage, and of the subject-clustered case.

[FIXABLE-IN-REPO]

**m-11. MINOR.** The per-night files the statistics depend on (`e12_nights_*.csv.gz`) are git-ignored and regenerated (L111). Deposit them with the code, or a checksum, so readers can check Table 2 without a multi-hour run. [FIXABLE-IN-REPO]

Otherwise reproducibility is good. The code matches the Methods on fitting order, comparator formulas, the conformal quantile rule (⌈(n+1)(1−α)⌉, +∞ when it exceeds n), clipping, the interval score, the permutation test and the Holm families.

#### Methodological Fallacies Detected
- *Confounding of components* (attribution): recalibration effect credited to the interval method (M-1, M-6).
- *Dependence ignored*: clustered nights treated as exchangeable units (M-2), and split-shared calibration ignored in tests (M-4).
- *HARKing risk*: low, because deviations are logged. The main-text summary understates them (M-8).
- *Overfitting*: no evidence; holdout and cross-fitting are used throughout.
- I checked whether the conclusions go beyond the data: the TST and decision claims do, as written (M-1, M-6). The transport and "local calibration needed" conclusions are supported.

### Questions for Authors
1. What fraction of the TST interval-score advantage over each LoA variant remains when the LoA are computed around the calibrated plug-in?
2. What coverage do CV+ and a plain split (HMM on half of the calibration subjects) achieve, and is the primary design conservative or anti-conservative relative to them?
3. What is coverage when one night per calibration subject is used, or when coverage is averaged per subject, in SC and ST?
4. Which tolerance (ε, δ) does "at least 20 nights" satisfy, and does it follow from the Beta distribution of calibration-conditional coverage?
5. What τ values were selected across the 50 splits and the local runs?
6. How should σ̄ be computed when nights arrive one at a time?

### Minor Issues
- L84: "k-th smallest score, where k is (n+1)(1−α) rounded up" — add "and +∞ (unbounded interval) when k > n", as the code does.
- L91: "Comparators (b)–(d) beyond the pre-specified ones" is hard to parse. List which comparators were pre-specified (Bland–Altman, scp_abs, raw percentiles, CQR type).
- L108: give the family sizes (80 and 16 tests per stager×cohort).
- Table 2 caption: replace "exact split-conformal limits" (see M-2).
- Fig. 3 caption: state the number of test nights per n_t for ST (34, 24, 14).

### Recommendation summary
- **Recommendation**: Major Revision (confidence 4/5).
- **Three issues most likely to cause rejection**:
  1. M-1 (+M-6): the TST advantage and the decision results are partly a recalibration effect credited to the interval method.
  2. M-2/M-3: the validity argument does not match the clustered, cross-fitted design.
  3. M-4: significance counts that depend on an inference ignoring calibration variability, and that S9 does not fully reproduce.
- **Three strongest methodological points**:
  1. The end-to-end protocol fits every label-dependent component on calibration subjects.
  2. The fixed-centre factorial isolates the adaptive scale.
  3. The guarantee is stated candidly and the deviation log is detailed.
