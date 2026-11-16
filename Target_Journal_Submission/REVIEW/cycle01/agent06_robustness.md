# Reviewer #6: Robustness & generalisation (cycle 1)

## Summary of the submission (3-5 sentences)
The authors conformally calibrate the per-night spread of eight PSG parameters, computed from FFBS samples of a tempered classifier/HMM posterior. They use two LightGBM-family stagers on Sleep-EDF SC/ST and HMC. Within-cohort marginal coverage is nominal, transport from SC fails, and "ten local nights restore coverage". I tested the transport, recalibration, corruption and subgroup claims with read-only re-analyses of `results/`, including a mixture-corruption re-analysis that uses the authors' summaries and `conformal_eval.py`.

## Fatal concerns
None.

## Critical/Major concerns

**M1. The 10-night experiment never recalibrates the stager, so "a few local nights correct the bias" is not tested.** `e06_cross_cohort.py` reads `<stager>_srcSC.csv`. There, BCTS, π_s, A and τ are fitted on SC, and only the conformal step uses the n_t target nights. The HMC TST bias reduction (−38.3 → −4.8 min, Table 3) comes from the `xfit` summaries, i.e. 5-fold cross-fitting with ≈120 HMC nights (`e03_night_summaries.py`, N_FOLDS = 5). Yet the Highlights (l.22–23), Discussion (l.135, "a few locally scored nights"), Clinical use (l.141, "recalibrate the stager's probabilities and the intervals") and Conclusion (l.148, "A small set … corrected most of the TST bias and restored coverage") merge these two experiments into one deployment claim that was never run. *Action:* refit BCTS (and optionally π_s, A, τ) on n_t ∈ {10, 20, 30, 50} target nights. Report bias, MAE, coverage, width and the risk of low coverage on the remaining nights. Otherwise, restate the claims separately.

**M2. "Ten nights restored coverage" is the generic finite-sample conformal law, and single-site reliability is poor.** With n = 10 and α = 0.1, q̂ is the maximum of the 10 calibration scores, and realised coverage follows ≈ Beta(10, 1): mean 0.909, P(<0.80) = 0.107, P(<0.85) = 0.197.
- HMC matches this exactly. For the proposed method, P(<0.80) is 0.078–0.120 and P(<0.85) is 0.176–0.206 across parameters. A constant-width interval around the calibrated plug-in gives the same (P(<0.80) 0.088–0.124).
- ST is worse because its test sets are small and clustered (17 subjects): P(<0.80) is 0.13–0.26, and mean N2 % coverage is 87.2 % (YASA) and 85.8 % (LightGBM).
- The price is width. HMC TST width at n = 10 is 129 min (5th–95th percentile over repetitions: 53–274 min), against 88 min within-cohort. For LightGBM it is 209 min.
- The comparison "twice as often with Bland–Altman" uses z·SD with n = 10 and no small-sample correction (`make_interval`, `ba_loa`), which is a known anti-conservative strawman.
- Pooling SC with target nights stays below nominal (Fig. 4b: 0.855 → 0.881 at 50 nights; Fig. 4e, LightGBM: 0.77 → 0.83).

*Action:* drop "restored it" from the Highlight. Report P(coverage < 0.85) and the width distribution, and show percentile bands in Fig. 4. Add a t-based Bland–Altman prediction interval, s·t₀.₉₅,ₙ₋₁·√(1+1/n). Give the n needed for training-conditional (PAC) coverage, e.g. P(coverage ≥ 0.85) ≥ 0.9.

**M3. Transport failure is broader than reported, the method is the most fragile under shift, and the "cohort shift" may be a montage/rule artefact.** Source-only YASA results (`e06_source_only_yasa.csv`, α = 0.1):
- The proposed method is the worst or tied-worst method for HMC N3 % (0.377), HMC REML (0.813), ST N3 % (0.705, against 0.818 for Bland–Altman and 0.841 for raw-plug-in conformal) and ST REM % (0.818, against 0.955 for Bland–Altman).
- ST is also over-covered (100 %) for SOL, WASO and N1 %, so "acceptable on ST for most parameters" (§3.5) is generous.
- Intervals around the uncorrected plug-in kept N3 % at 0.834 (scp_abs) and 0.841 (FFBS-SD scale). The within-cohort advantage of correcting the centre therefore becomes a liability under shift. This trade-off belongs in the Abstract and the Conclusion.
- YASA was run on HMC C4-M1, although F4-M1 is cached (`src/data/sleep.py` l.14/179: "frontal, closest available analogue of Fpz-Cz"). AASM N3 is scored on frontal slow-wave amplitude, and 30 % of HMC N3 epochs went to N2 (S10). The N3 "bias reversal" may therefore come from derivation and scoring rules (R&K vs AASM), not from the population.
- LightGBM's HMC failure (TST 0.503, N3 % 0.305) mixes montage shift (Fpz-Cz → C4-M1) with population shift.

*Action:* re-run HMC with F4-M1 for both stagers. The data are cached, and YASA takes ≈1.4 s per night. Qualify "external validation" in the title and abstract.

**M4. The corruption experiment is a stress test whose mechanism is mis-attributed.**
- (a) *Design.* Clean calibration with corrupted test nights violates exchangeability by construction. A deployed laboratory calibrates on a mixture of clean and corrupted nights. I re-ran the analysis with 25 % corrupted nights in both halves (R = 100):
  - Marginal coverage was 0.90–0.93, but coverage of the corrupted nights under strong noise (TST) was only 0.69 (SC), 0.69 (ST) and 0.82 (HMC) for the proposed method, against 0.66, 0.67 and 0.68 for the distribution-free LoA. Clean nights were over-covered (0.95–0.99).
  - With artefacts in 25 % of epochs the proposed method did help: TST 0.86, 0.90 and 0.89 against 0.79, 0.71 and 0.80.
  - Calibrating on corrupted nights restores coverage, but the adaptive advantage reverses. Under strong noise, SC TST width was 356 min against 160 min, and SC WASO 421 min against 128 min.
- (b) *Attribution.* Under strong noise for TST, constant width around the *calibrated* plug-in (scp_abs_cal) matched the proposed method's mean coverage (0.320 vs 0.323) and had a lower interval score (614 vs 732; cohort means from `tableS_robustness.csv`). The FFBS-SD scale around the calibrated plug-in reached 0.485. The claim that intervals "degraded less because their width responded" (§3.7) is therefore confounded with the centre, and Fig. 5 omits these comparators.
- (c) The headline figures (32 %, 7 %, 71 → 108 min, 85 vs 48 %) are unweighted means over SC, ST and HMC, which is not stated. TST coverage under strong noise was 20 % in SC and 15 % in ST.

*Action:* report the mixture design with coverage conditional on corrupted nights, add the centre-matched comparators, report per cohort, and add LightGBM.

**M5. The age subgroup statement is wrong and hides conditional under-coverage.** In S9, "count" is night × parameter pairs pooled over 8 parameters. `make_tables.py` filters `count >= 40`, so "subgroups with ≥40 nights" (l.110) includes ST ≥60 y (48 pairs = 6 nights). Per-parameter LOSO coverage in SC adults ≥60 y (73 nights, YASA) is 0.86 for TST, 0.84 for N1 %, 0.84 for N2 %, 0.86 for N3 % and 0.86 for REM %, against 0.92–0.96 below 60 y. LightGBM is similar (0.84–0.88). The adaptive scale does not help: the distribution-free LoA gives 0.84–0.88 in the same group. This is the known age bias (Baumert 2023), and age is label-free, so it is correctable. *Action:* add a per-parameter subgroup table and fix the wording. Add Mondrian calibration by age, and an age-shift experiment (calibrate on <60 y, test on ≥60 y).

**M6. The supplement silently truncates the tables that the robustness and transport claims cite.** `make_supplement.py` `tbl(max_rows=400)` cuts S12 at 400 of 480 rows: only 16 of the 96 strong-noise rows appear, so the §3.7 headline numbers cannot be verified. S13 few-shot is cut (672 rows), as are S2 (768) and S3 (480). The 18:35 regeneration still contains only 16 strong-noise rows. *Action:* remove the cap or move these tables to CSV files, and state in the text how aggregates are formed.

## Moderate concerns
**Mo1. Mondrian is not adequate yet.** For YASA, worst-quartile coverage with entropy-binned Mondrian calibration is 0.836 (HMC), 0.844 (SC) and 0.864 (ST). This is still below the pre-specified 87 % bound, and width rises in Q1 (HMC 59 → 73). With K = 2 bins, ST bins hold about 21 nights. *Action:* test bins by age plus entropy, or a localized/weighted conformal method, and report bin sizes.

**Mo2. "Two stagers" is one model family.** Both are gradient-boosted trees on the same 116 YASA features, and both fitted τ ≈ 0.10. Deep stagers that use whole-night context (U-Sleep) and give sharper outputs may collapse the FFBS spread. U-Sleep was trained on Sleep-EDF, so it cannot be tested on SC/ST. *Action:* add a raw-signal CNN (e.g. TinySleepNet, CPU-trainable) trained with subject-grouped CV on SC. As a cheap stress test, feed HMM-smoothed marginals in as the stager output.

**Mo3. Corruption realism and a protocol deviation.** The noise is 0 dB white noise applied to EEG and EOG together. The artefact model is an AR(1) drift (stationary SD ≈ 500 µV) clipped at ±300 µV, which saturates the affected epochs. Each night has one fixed realisation. The pre-registered 50 Hz line noise (PREREGISTERED_PROTOCOL l.41) was neither run nor logged in CHANGELOG. *Action:* add line noise, electrode pop or flat-line, single-channel loss, EMG bursts and several corruption seeds, and log the deviation.

**Mo4. Small ST cohort (22 subjects).** The efficiency claims for ST (TST ratio 0.59) and the transport claims rest on 22 subjects, with 44-night test sets in transport. *Action:* give CIs, and hedge the ST-specific statements.

**Mo5. Population scope.** There are no paediatric, OSA-characterised or wearable data, and HMC has no demographics. *Action:* bound the Conclusion. Stratify HMC by a label-free fragmentation index (stage-shift and wake-bout rate of the plug-in hypnogram). Consider ISRUC-Sleep or DOD-O (public, OSA patients, multiple scorers).

## Minor concerns
**Mi1.** Fig. 4 shows means only, and the Fig. 5 caption does not say that values are averaged over cohorts.
**Mi2.** §3.5 "88.1 % with 50 target nights" omits LightGBM pooled (0.83).
**Mi3.** The robustness experiment uses YASA only.

## Required additional experiments/analyses
1. Full few-night recalibration (BCTS ± HMM refit on n_t target nights): bias, coverage, width and P(coverage < 0.85). FFBS takes 0.02 s per night.
2. HMC with F4-M1 for both stagers, with transport re-run.
3. Mixture-corruption design with coverage conditional on corrupted nights, calibration on corrupted nights, centre-matched comparators, realistic artefacts and several seeds, for both stagers.
4. Per-parameter subgroup table, an age-shift experiment, and Mondrian calibration by age.
5. Small-n comparators: a t-based Bland–Altman prediction interval and PAC-style quantiles.
6. One deep raw-signal stager, plus a smoothed-input stress test.
7. Optional: an OSA or multi-scorer public cohort.

## Recommendation
**Major revision.** Within-cohort marginal validity holds, but the deployment claims (few nights fix bias and coverage; adaptive intervals are robust to corruption; coverage is nominal across age) are not tested as stated, or are contradicted by the authors' own result files. All the analyses needed are cheap with the cached data.

```json
[
{"id":"M1","severity":"major","title":"Few-night experiment never recalibrates stager; bias-correction claim conflated","location":"Highlights l.22-23; Discussion l.135,141; Conclusion l.148; code/experiments/e06_cross_cohort.py; e03 xfit","evidence":"e06 uses SC-fitted srcSC summaries (BCTS/HMM from SC), only conformal quantile from n_t nights; TST bias -38->-5 min uses 5-fold xfit (~120 HMC nights)","action":"Refit BCTS(+HMM) on n_t target nights; report bias/coverage/width vs n_t or rephrase claims","needs_experiment":true},
{"id":"M2","severity":"major","title":"'Ten nights restored coverage' is generic Beta(10,1) conformal behaviour; poor site-level reliability and wide intervals","location":"Highlights; Abstract; Sec 3.5; Fig 4; S17","evidence":"Theory P(<0.80)=0.107, P(<0.85)=0.197; HMC observed 0.078-0.120/0.176-0.206, same for scp_abs_cal; ST 0.13-0.26, N2% mean 0.872/0.858; HMC TST width 129 min (53-274) vs 88 within; LightGBM 209; BA uses z without small-n correction; pooled 0.855-0.881","action":"Rephrase; report P(<0.85) and width distribution; t-based BA prediction interval; PAC calibration; percentile bands in Fig 4","needs_experiment":true},
{"id":"M3","severity":"major","title":"Transport failure broader than stated; proposed most fragile; N3 shift likely montage/rule","location":"Sec 3.5; Fig 4a,d; e06_source_only_*.csv; src/data/sleep.py l.14,179","evidence":"YASA proposed worst/tied-worst: HMC N3 0.377, REML 0.813, ST N3 0.705 (BA 0.818, scp_abs 0.841), ST REM% 0.818 (BA 0.955); raw-plugin intervals kept 0.83-0.84; YASA used C4-M1 though F4-M1 cached; HMC N3->N2 30%","action":"Rerun HMC with F4-M1 for both stagers; report the trade-off in Abstract; qualify 'external validation'","needs_experiment":true},
{"id":"M4","severity":"major","title":"Corruption design unrealistic and robustness gain confounded by centre","location":"Sec 3.7; Fig 5; e09_robustness.py; tableS_robustness.csv","evidence":"Mixture re-analysis (25% corrupted both halves): corrupted-night TST coverage under strong noise 0.69/0.69/0.82 vs 0.66/0.67/0.68; calibrating on corrupted nights: SC TST width 356 vs 160, WASO 421 vs 128; strong-noise TST scp_abs_cal coverage 0.320 vs 0.323, IS 614 vs 732; headline numbers are unstated cohort means (SC 20%, ST 15%)","action":"Mixture design with conditional coverage; centre-matched comparators; per-cohort reporting; LightGBM","needs_experiment":true},
{"id":"M5","severity":"major","title":"Age subgroup claim wrong; per-parameter under-coverage in older adults","location":"Sec 3.2 l.110; S9; code/scripts/make_tables.py count>=40","evidence":"count = night x parameter pairs (ST>=60 = 6 nights); SC >=60 y LOSO coverage TST 0.86, N1 0.84, N2 0.84, N3 0.86, REM% 0.86 vs 0.92-0.96 <60; scp_abs_bc similar","action":"Per-parameter subgroup table; fix wording; Mondrian by age; age-shift experiment","needs_experiment":true},
{"id":"M6","severity":"major","title":"Supplementary tables silently truncated at 400 rows","location":"code/scripts/make_supplement.py tbl(max_rows=400); S2,S3,S12,S13","evidence":"S12 480 rows -> 16/96 strong-noise rows shown; S13 few-shot 672, S2 768, S3 480 rows truncated; persists after regeneration","action":"Remove cap or provide full CSVs; state aggregation in text","needs_experiment":false},
{"id":"Mo1","severity":"moderate","title":"Mondrian fix insufficient","location":"Sec 3.2; S17","evidence":"YASA worst-quartile 0.836/0.844/0.864 (<0.87 criterion); Q1 width 59->73 (HMC); ~21-night bins in ST","action":"Age+entropy bins or localized conformal; report bin sizes","needs_experiment":true},
{"id":"Mo2","severity":"moderate","title":"Both stagers are one model family","location":"Sec 2.3; Limitation iv","evidence":"Both LightGBM on the same 116 YASA features; tau 0.10 for both","action":"Add raw-signal CNN trained SC-CV; smoothed-input stress test","needs_experiment":true},
{"id":"Mo3","severity":"moderate","title":"Corruption realism; unlogged deviation (50 Hz)","location":"e09_robustness.py; PREREGISTERED_PROTOCOL l.41","evidence":"0 dB white noise on EEG+EOG jointly; AR(1) drift SD~500 uV clipped; one realisation per night; line noise pre-registered, not run, not in CHANGELOG","action":"Add realistic artefacts and seeds; log deviation","needs_experiment":true},
{"id":"Mo4","severity":"moderate","title":"Small ST cohort drives several claims","location":"Table 2 ST; Sec 3.5","evidence":"22 subjects; transport test 44 nights; few-shot test 34 nights","action":"CIs; hedge ST-specific claims","needs_experiment":false},
{"id":"Mo5","severity":"moderate","title":"Population scope not bounded","location":"Conclusion; Limitations","evidence":"No paediatric/OSA/wearable data; HMC lacks demographics","action":"Bound claims; HMC fragmentation strata; optional ISRUC/DOD-O","needs_experiment":true},
{"id":"Mi1","severity":"minor","title":"Fig 4 means only; Fig 5 cohort averaging unstated","location":"Fig 4, Fig 5 captions","evidence":"No dispersion; Fig 5 = unweighted cohort means","action":"Add bands; state aggregation","needs_experiment":false},
{"id":"Mi2","severity":"minor","title":"LightGBM pooled recalibration omitted","location":"Sec 3.5","evidence":"Fig 4e pooled 0.77-0.83","action":"Report","needs_experiment":false},
{"id":"Mi3","severity":"minor","title":"Robustness for YASA only","location":"Sec 2.7","evidence":"e09 YASA only","action":"Add LightGBM","needs_experiment":true}
]
```
