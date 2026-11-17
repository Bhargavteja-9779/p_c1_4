# Reviewer 2: Methodology and implementation correctness (cycle 1)

## Summary of the submission (3-5 sentences)
Stager probabilities are recalibrated with BCTS (eq. 1). A tempered hybrid HMM (eq. 2–3) is then sampled by FFBS (M = 1000 per night), and the per-night spread is conformalised with a regularised normalised score (eq. 4–5). Evaluation covers cohorts internally (500 subject-grouped splits and leave-one-subject-out, LOSO), transfer between cohorts, and signal corruption. I checked the equations against the code and ran light read-only checks on the shipped predictions and summaries (`pytest`: 8/8 pass). The core numerics are correct:
- **Forward and backward passes:** scaled correctly (`hmm.py:22-62`).
- **FFBS:** draws y_t with weights α_t(j)A(j,y_{t+1}) (`hmm.py:95-109`).
- **Equations:** (1), (2) and (4) match the code. The row-max normalisation of E (`hmm.py:115`) does not change the posterior.
- **LightGBM folds:** the out-of-fold folds and the cross-fitting folds coincide (same seed and algorithm in `e02:37-43` and `e03:37-43`).

The problems are in the validity claims, the ablation design and the "few local nights" claims.

## Fatal concerns
None.

## Critical/Major concerns

**M1. The "exact" finite-sample guarantee does not hold for the design as evaluated.** The manuscript states that the guarantee is exact "whatever the stager or the HMM" (manuscript l.82, l.86; also l.110: "comparators with exact guarantees"). Two mechanisms break this.
- **(a) Cross-fitting.** Each night's μ̂/σ̂ comes from a source model fitted on the other four folds of the same cohort (`e03_night_summaries.py:59-70`, used in `e04:84`, `e11:70`, `e07:168`). A calibration night's score thus depends on test-night labels from other folds, and vice versa. This is the CV+/cross-conformal setting, with only a 1−2α worst-case guarantee.
- **(b) Two nights per subject.** The rank argument needs night-level exchangeability, which subject-grouped splits of correlated nights do not provide (within-subject Spearman correlation of the proposed scores in ST: up to 0.64).
- **My check (ST, YASA, 4000 splits; bound k/(n+1) = 0.913 for a fixed score):** night-level splits gave 0.912–0.917; subject-grouped splits gave 0.899 (N2 %) and 0.902–0.904 (TST, REM %, SOL) even for fixed-score `scp_abs` (SE 0.0016), and 0.896 for the proposed method. S2 shows `cqr_qr` in ST at 0.871–0.887, below 1−α.

*Action:* State the guarantee at subject level, approximate under cross-fitting; use a subject-level procedure (one night per subject, or pooled-CDF weighting, Dunn et al. 2022) or report the deficit; remove "exact".

**M2. The FFBS-vs-independent and τ ablations change the centre as well as the scale, and the Discussion attributes the effects to the scale.** `norm_reg_ind` uses (`mu_ind`, `sd_ind`) and `norm_reg_ffbs1` uses (`mu1`, `sd1`) (`conformal_eval.py:116-119`). I decomposed both in LOSO (YASA; ratios of mean interval score versus the proposed method):
- **REM % with independent sampling:** the gain is entirely the centre. Centre only: 0.80 (HMC), 0.85 (SC). Scale only: 0.99, 1.04.
- **N1 % in ST:** centre only 0.67, scale only 0.98.
- **τ = 1, SC WASO:** centre only 0.52, scale only 0.88.
- **τ = 1, N3 % worsening (1.32, SC):** entirely the centre (scale only 1.00).
- **The FFBS scale does help the latencies:** with the independent scale only, SC SOL 1.26 and REML 1.22.

"Independent-epoch spread was an equally good or better scale" and "temperature … too low for SOL and WASO" (l.139; l.115) are therefore misattributions. *Action:* Run centre-fixed 2×2 ablations and rewrite l.115 and l.139.

**M3. The "few/small set of local nights" claims and the recommended deployment workflow are not what was tested.**
- **(i) Point estimates.** The calibrated plug-in in Table 3 and §3.4 ("recalibrating … on the labelled calibration nights", l.118) uses BCTS cross-fitted on about four fifths of the cohort (around 121 HMC nights; `e07:168`, `e03:61-66`). Yet the Abstract, Discussion (l.135: "a few locally scored nights") and Conclusion (l.148) speak of a small local set.
- **(ii) Coverage restoration.** In the 10-night transport experiment (`e06:139`, `srcSC`) BCTS and the HMM come from SC; only the conformal quantile is local.
- **(iii) Clinical use.** The recommended workflow (l.141, "use them to recalibrate the stager's probabilities and the intervals") was never evaluated.

My checks:
- BCTS fitted on 10 HMC nights removed the TST bias on average (−4.4 min). Across repetitions, however, the site-level bias ranged from −24 to +24 min.
- Refitting the full source model on 10 HMC nights and conformalising on those same nights gave mean coverage 0.885 (N3 % 0.864; 25 repetitions, M = 300). Cross-fitting within the 10 nights gave 0.911.
- E12 (`e12_honest_protocol.py`, results present: 0.90–0.92 mean coverage, per-repetition minimum 0.46–0.72) implements the correct nested protocol but is not reported.

*Action:* Report E12 with per-site spread; specify within-local cross-fitting; restrict "few nights" wording.

**M4. Comparisons within a cohort are not "on the same calibration nights" (l.89).**
- The proposed method, `scp_abs_cal`, `scp_abs_mu` and `norm_reg_plugc` use centres from models trained on about 80 % of the cohort, including test-half labels.
- `scp_abs_bc` and `ba_loa` estimate the bias from the 50 % calibration half only (`conformal_eval.py:84-94`).

This favours the BCTS-based centres in the headline comparison (Table 2, Abstract). *Action:* Base Table 2 on the nested (E12-type) protocol, or show that the conclusions are unchanged under it.

## Moderate concerns

**Mo1. The τ criterion and the "posterior" interpretation.** `fit_tau` maximises a composite likelihood, the summed log-score of smoothed marginals (`hmm.py:150-165`), although the samples serve path functionals (latencies, WASO).
- On all SC nights the marginal criterion peaks at τ = 0.10, but the joint path log-likelihood log P(y_ref | x) peaks at about 0.15–0.20 (−60,316 versus −59,672).
- At τ = 0.1, raw 90 % posterior intervals covered only 54 % (TST), 37 % (REM %) and 39 % (N3 %) in-sample.
- Eq. (2) is a heuristic power-tempered likelihood; at τ ≈ 0.1 samples revert towards the source composition (REM % bias +4.7, Table 3).
- The grid is coarse around the optimum (0.08 / 0.10 / 0.15), and the manuscript presents it as a continuous range "τ ∈ [0.02, 1.5]" (l.75).

*Action:* Call the samples a tempered pseudo-posterior and state the grid. Add a sensitivity analysis selecting τ by a night-level criterion (inner-CV interval score or log P(y_ref | x)), or per parameter.

**Mo2. The "strongest simple competitor" is not exactly valid, and an exactly valid alternative exists.** `scp_abs_bc` estimates its bias from calibration labels (`conformal_eval.py:90-94`), and it under-covers in ST (0.852 for N2 %, S2). Taking two one-sided conformal quantiles of the signed residual y − plug-in (α/2 each) gives an interval that is exactly valid, corrects bias and allows asymmetry.
- In my LOSO check its coverage was 0.86–0.93.
- Against `scp_abs_bc` its interval-score ratio was 0.81 (HMC SOL) and 0.83 (SC WASO).
- The proposed method was worse than it in 8 of 24 YASA combinations (unadjusted p < 0.05) and better in 13.

*Action:* Add it as a comparator.

**Mo3. The regulariser is computed from the test batch, which matters under shift.** σ̄ over calibration plus test nights (`conformal_eval.py:122`) is legitimate under exchangeability, but in E09 half the pool is corrupted. For SC TST under strong noise, median σ̂ is 8.8 (clean) and 24.8 (corrupted), and pooled σ̄ is 16.0. Part of the widening reported at l.127 is thus batch transduction, unavailable when nights are scored one at a time. E06 is affected likewise. *Action:* Recompute E06 and E09 with σ̄ from calibration nights plus one test night at a time.

**Mo4. The windows are not purely "metadata only" (l.57).** The window end is truncated at the last scored epoch of the reference annotation (`sleep.py:110-112`, `173`). This does not reveal stage content, but it is label-derived. *Action:* State this, or use the recording end or lights-on only.

## Minor concerns

**Mi1. Stale code and docstrings contradict the method.** `conformal.py:71` and `_scale` (`conformal.py:90-96`) use a calibration-only median, as does the `conformal_eval.py:16` docstring. The `interval()` function is unused. *Action:* Delete or fix these.

**Mi2. `conformal_quantile` drops non-finite scores before counting n** (`conformal.py:81-83`). This is anti-conservative if a score is ever +inf or NaN. None occur in the current summaries (I checked), but +inf scores should be kept.

**Mi3. `cqr_qr` edge cases.** At α = 0.05 in ST, `cqr_qr` gives infinite width in 50 % of splits (the second calibration half has about 10 nights, so k > n). The S6 summary must say how these are handled. Quantile crossing is not handled either (0.07 % zero-width LOSO intervals, `conformal_eval.py:75-77`).

**Mi4. REML censoring.** Censored REML values are averaged as if they were observed values (`sleep_params.py:47`; `night_summary.py:88`). I found no night where the FFBS 95th percentile or the plug-in REML reached the censoring point, so the effect is immaterial. Say so.

**Mi5. Feasible range.** The upper bounds (window length) for TST, SOL, WASO and REML are not applied (`conformal_eval.py:33-34`). This is conservative, but "intersected with the feasible range" overstates what the code does.

**Mi6. Bootstrap resamples.** The code uses B = 1000 (`e07:87,110`), the protocol specifies 2000, and the text says "1000–2000". Harmonise.

## Required additional experiments/analyses
1. Nested E12 results with per-site coverage and bias spread; Table 2 under it (M3, M4).
2. Subject-level conformal variant or night- vs subject-split coverage (M1).
3. Centre-fixed 2×2 ablations (M2).
4. Signed-residual comparator (Mo2).
5. E06/E09 with a deployment-faithful σ̄ (Mo3).
6. Night- or path-level τ sensitivity (Mo1).

## Recommendation
**Major revision.** The implementation is largely correct, but: the exact, HMM-independent guarantee does not hold for the evaluated design (shipped results show sub-bound coverage); several component conclusions come from ablations confounding centre and scale; and the "few local nights" claims rest on models fitted on about 80 % of each cohort or on SC. Existing code (E12) and modest re-analysis can fix all of these.

```json
[
 {"id":"M1","severity":"major","title":"Claimed exact finite-sample guarantee does not hold under cross-fitting and two nights per subject","location":"manuscript l.82, l.86, l.110; e03_night_summaries.py:59-70; e04_within_cohort.py:84; conformal_eval.py:151-157","evidence":"Scores depend on labels of other-fold nights (CV+ setting). ST, 4000 splits: night-level splits give 0.912-0.917 (bound 0.913); subject-grouped splits give 0.899 (N2%) for fixed-score scp_abs (SE 0.0016) and 0.896 for the proposed method; S2: cqr_qr ST 0.871-0.887.","action":"State the guarantee at subject level and as approximate under cross-fitting; add a subject-level conformal variant (one night per subject or pooled-CDF weighting) or report the deficit; remove 'exact'.","needs_experiment":true},
 {"id":"M2","severity":"major","title":"FFBS-vs-independent and tau ablations confound centre and scale","location":"conformal_eval.py:116-119; manuscript l.115, l.139; Supp. S4","evidence":"LOSO decomposition (YASA): REM% independent gain is centre-only (0.80/0.85; scale-only 0.99/1.04); ST N1% centre 0.67 vs scale 0.98; tau=1 SC WASO centre 0.52 vs scale 0.88; N3% worsening 1.32 entirely centre.","action":"Run centre-fixed 2x2 ablations and rewrite the scale attributions.","needs_experiment":true},
 {"id":"M3","severity":"major","title":"'Few local nights' claims and recommended workflow not tested as stated","location":"manuscript l.118, l.135, l.141, l.148, Abstract; e07_utility_and_stats.py:168; e06_cross_cohort.py:139; e12_honest_protocol.py (unreported)","evidence":"Calibrated plug-in uses BCTS on about 4/5 of the cohort (around 121 HMC nights); the 10-night transport keeps SC-fitted BCTS/HMM. My check: BCTS on 10 HMC nights gives mean bias -4.4 min but range -24 to +24 min; refit plus conformal on the same 10 nights gives coverage 0.885 (N3% 0.864) vs 0.911 with cross-fitting. E12 results exist but are not reported.","action":"Report E12 with per-site variability; specify cross-fitting within local nights; restrict wording.","needs_experiment":true},
 {"id":"M4","severity":"major","title":"Within-cohort comparators do not use the same labelled nights","location":"manuscript l.89; conformal_eval.py:84-94 vs e03 xfit summaries","evidence":"The proposed and calibrated-centre methods use models trained on about 80% of the cohort including test-half labels; scp_abs_bc/ba_loa estimate bias on the 50% calibration half only.","action":"Base Table 2 on the nested protocol or show the conclusions are unchanged.","needs_experiment":true},
 {"id":"Mo1","severity":"moderate","title":"Tau fitted by marginal composite likelihood; samples are a tempered pseudo-posterior","location":"hmm.py:150-165; manuscript l.75","evidence":"SC: marginal optimum 0.10 vs joint path log-likelihood optimum 0.15-0.20; raw 90% posterior coverage at tau=0.1 is 54% TST, 37% REM%, 39% N3%; grid is 0.08/0.10/0.15, not continuous.","action":"Rename as tempered pseudo-posterior, state the grid, add a night-level or path-level tau sensitivity analysis.","needs_experiment":true},
 {"id":"Mo2","severity":"moderate","title":"Approximately valid scp_abs_bc chosen over an exactly valid asymmetric signed-residual conformal comparator","location":"conformal_eval.py:90-94; Table 2","evidence":"Signed-residual LOSO: coverage 0.86-0.93; interval-score ratio vs scp_abs_bc 0.81 (HMC SOL), 0.83 (SC WASO); proposed worse in 8/24 and better in 13/24 YASA combinations (unadjusted p<0.05).","action":"Add the comparator to Table 2 and S3.","needs_experiment":true},
 {"id":"Mo3","severity":"moderate","title":"Regulariser computed from the test batch inflates widths under shift","location":"conformal_eval.py:122; e09_robustness.py; e06_cross_cohort.py; manuscript l.127","evidence":"E09 gauss10 SC TST: median sd 8.8 clean, 24.8 corrupted, pooled regulariser 16.0.","action":"Recompute E06/E09 with the regulariser from calibration nights plus one test night at a time.","needs_experiment":true},
 {"id":"Mo4","severity":"moderate","title":"Analysis window end derived from reference annotation extent","location":"sleep.py:110-112, 173; manuscript l.57","evidence":"e1 = min(e1, last scored epoch + 1) uses the hypnogram file.","action":"Disclose this or use the recording end or lights-on only.","needs_experiment":false},
 {"id":"Mi1","severity":"minor","title":"Stale calibration-only median in docstrings and unused interval()","location":"conformal.py:71, 90-96; conformal_eval.py:16","evidence":"Contradicts conformal_eval.py:122 and the manuscript.","action":"Remove or fix.","needs_experiment":false},
 {"id":"Mi2","severity":"minor","title":"conformal_quantile discards non-finite scores before counting n","location":"conformal.py:81-83","evidence":"+inf scores should rank at the top; no current impact (no non-finite values found).","action":"Keep +inf scores and treat NaN explicitly.","needs_experiment":false},
 {"id":"Mi3","severity":"minor","title":"cqr_qr infinite widths at alpha=0.05 in ST and unhandled quantile crossing","location":"conformal_eval.py:63-78, 110-115; Supp. S6","evidence":"inf_width 0.5 in ST at alpha=0.05; 0.07% zero-width LOSO intervals.","action":"Report the handling and sort lo/hi.","needs_experiment":false},
 {"id":"Mi4","severity":"minor","title":"Censored REML averaged as an observed value","location":"sleep_params.py:47; night_summary.py:88","evidence":"No night reached the censoring point at the FFBS 95th percentile or for the plug-in (checked).","action":"State that the effect is immaterial.","needs_experiment":false},
 {"id":"Mi5","severity":"minor","title":"Feasible-range clipping applies lower bounds only for minute parameters","location":"conformal_eval.py:33-34; manuscript l.86","evidence":"No window-length upper bound for TST/SOL/WASO/REML.","action":"Correct the wording or apply the bounds.","needs_experiment":false},
 {"id":"Mi6","severity":"minor","title":"Bootstrap B=1000 in code vs 2000 in protocol","location":"e07_utility_and_stats.py:87,110; manuscript l.98","evidence":"Protocol specifies 2000 resamples.","action":"Harmonise or log the deviation.","needs_experiment":false}
]
```
