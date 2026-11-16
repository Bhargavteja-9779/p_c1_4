# Reviewer 7 — Computational efficiency & deployment (cycle 1)

## Summary of the submission (3-5 sentences)
The authors turn epoch probabilities of a sleep stager into per-night intervals for 8 clinical parameters. They apply BCTS recalibration and a hybrid HMM with tempered emissions (τ grid), draw M = 1000 hypnograms by numba FFBS, and then split-conformalise a normalised score. Section 3.8 / Table S15 claim the uncertainty layer costs a median 0.02 s per night on one CPU core, against 1.4 s for YASA, plus 0.4 ms for the conformal step. The core speed claim holds: the E10 data support it, and my own single-threaded synthetic micro-benchmark of a scratchpad copy of `hmm.py` reproduced it (warm FFBS, M = 1000, T = 1028: 0.011 s against the reported 0.013 s). The problems lie elsewhere:
- **Untimed one-off costs.** These costs are not reported.
- **Memory.** Memory use is under-reported.
- **Deployment workflow.** The workflow recommended in the Discussion was never evaluated end-to-end.
- **Pre-registration.** The pre-registered M-sensitivity analysis is silently missing.

## Fatal concerns
None.

## Critical/Major concerns
**M1. The recommended deployment workflow ("about ten local nights") was never run end-to-end.**
- **What the manuscript says.** Discussion l.135 says TST bias was removed by recalibrating probabilities "on a few locally scored nights", and l.141 says a site should "(ii) use them to recalibrate the stager's probabilities and the intervals", with "about ten local nights".
- **What was actually done.** Probability recalibration (BCTS, π_s, A, p0, τ) was fitted by 5-fold cross-fitting (`e03_night_summaries.py` l.60–66). Per cohort, the folds in `yasa_xfit.csv` are HMC 30–31 nights, SC 29–32 and ST 8–10, so each model is trained on about 120 HMC/SC nights and 34–36 ST nights.
- **What the few-night experiment did.** E06 reuses the SC-fitted summaries (`*_srcSC.csv`; docstring l.1–8) and re-estimates only the conformal quantile.
- **Consequence.** The bias reduction (−38 → −5 min) and the ten-night coverage restoration come from different calibration regimes. Neither the statistical behaviour nor the cost of refitting BCTS/τ/A on 10 nights is known.
- **Action.** Simulate the real deployment: refit BCTS (and τ, A) plus the conformal step on n_t ∈ {10, 20, 30, 50} target nights. Report bias, coverage, interval score and fit time. Otherwise, restrict l.135/l.141 and the highlights to what was tested.

**M2. The pre-registered M sensitivity analysis is computed but not reported, and is not listed as a deviation.**
- **Evidence.** The protocol (`PREREGISTERED_PROTOCOL.md` l.39; Supplement S1 l.49) specifies "number of samples M ∈ {100, 300, 1000}". `night_summary.py` l.96–99 stores `ffbsM100/ffbsM300` mean/SD. `make_tables.py` l.240 has only the comment `# sample-size sensitivity M ...` with no code. No table exists in `tables/` or the Supplement, and the deviation log in S1 (l.83–117) does not mention it.
- **My check (read-only, proposed score reimplemented, 200 subject-grouped splits, 24 cohort × parameter cells per stager):**
  - Spearman ρ between SD(M=100) and SD(M=1000) had a median of 0.967 (minimum 0.877) for YASA and 0.958 (minimum 0.777, ST N2 %) for LightGBM.
  - The median per-night relative SD difference was 4.7 %.
  - Coverage changed by at most 0.7 percentage points.
  - Interval-score ratios M100/M1000 were 0.92–1.04, and M300/M1000 were 0.96–1.05.
  - The median per-night width change was about 3 %.
- **Caveat.** The M = 100/300 draws are the first draws of the same M = 1000 array, so this agreement is optimistic.
- **Action.** Report the table, declare the omission in S1, and state the Monte-Carlo error of interval endpoints using independent seeds. M = 100–300 appears sufficient.

## Moderate concerns
**Mo1. The timing protocol is incomplete and its "one core" condition is unverified.**
- **One-off costs are untimed.** `fit_source_model` (`e10_efficiency.py` l.31) and the numba warm-up (l.33–34) fall outside the timed region. On this host I measured about 2.5 s of cold JIT compilation (FFBS 1.36 s, forward–backward 1.11 s) and 0.9 s for the 33-point τ grid on 120 nights. BCTS fitting was not measured.
- **Thread count is not controlled.** `os.environ.setdefault("OMP_NUM_THREADS","1")` (l.29) runs after the module-level imports and does not override an inherited value. There is no CPU affinity pinning, and LightGBM/numba thread counts are not recorded. The meta file's `torch_threads: 1` is irrelevant because torch is not used.
- **There is one repetition per night.** FFBS time varies 2.4–6.9-fold (max/min) across nights of similar length.
- **Warm-up is asymmetric.** The stager is timed cold: SC4001 took 13.1 s because of the lazy `import yasa` inside the timed function (`yasa_stager.py` l.25), while FFBS is pre-warmed. EDF loading (`load_night`, l.38) is untimed.
- **Hardware is under-reported.** No CPU model, RAM or numba/NumPy versions are given (Methods l.101 says "NumPy/Numba"). The host reports a virtualised "Intel Xeon @ 2.10GHz".
- **Action.** Time the one-off costs separately. Pin to one core (`taskset`, `NUMBA_NUM_THREADS=1`, LightGBM `num_threads=1`). Use repeated measurements and report median/IQR. Record the CPU model, RAM and library versions in S15.

**Mo2. Memory use is under-reported by about 9×.**
- **Evidence.**
  - The `samples_MB` column is `S.nbytes`, i.e. only the int8 output.
  - `ffbs_sample` also allocates `rng.random((M, T))` in float64 (`hmm.py` l.120), which is 8× larger.
  - `compute_params` creates about 10 boolean M×T temporaries (`sleep_params.py` l.33–51).
  - For T = 20,160 epochs (7×24 h) at M = 1000, I measured a peak RSS increase of 173 MB for FFBS alone, against 20 MB of samples.
- **Action.** Report peak RSS. Draw uniforms inside the kernel (or chunk over M), and accumulate the parameters per sample.

**Mo3. Scaling to long recordings and large cohorts is asserted but not tested.**
- **Timing sample.** The timing nights are the "first 20 by name" per cohort (SC = 10 subjects), all 821–1200 epochs long. Cost is linear (about 0.06 s per 24 h; 0.32 s measured for 20,160 epochs), so throughput is not the issue.
- **The model is built for single nocturnal windows.**
  - p0 and A come from lights-off nocturnal hypnograms, and τ ≈ 0.1 flattens the emissions, so the nocturnal prior dominates.
  - SOL/WASO are defined by the first/last sleep epoch of the whole window (`sleep_params.py` l.37–43).
  - The SC WASO failure (49 % of samples misplacing the final awakening; Results l.124) shows this failure mode, and Discussion l.139 concedes it.
- **Action.** Run the full 20-h SC files (already available) to report cost and per-sleep-period behaviour, or explicitly restrict the scope to single-night PSG windows.

**Mo4. Intervals depend on the test batch, and the code contains a conflicting implementation.**
- **Batch dependence.** σ̄ is the median of σ̂ over calibration and test nights (Methods l.82; `conformal_eval.py` l.122). In the evaluation the test batch is about half a cohort, but in a clinic nights arrive one at a time. A night's interval therefore changes with the composition of the batch, which makes reports non-reproducible and breaks the audit trail.
- **Conflicting code.** `src/uncertainty/conformal.py` `_scale` (l.34–36) still uses the old median over calibration nights only. This is the obvious public API, and it is not the method that was evaluated.
- **Action.** Specify the deployment rule (calibration nights ∪ {this night}, which keeps validity exact), show that the results are unchanged, remove or align the stale function, and provide a single-night inference entry point.

## Minor concerns
**Mi1.** "Median 0.02 s" is computed as a sum of two medians (`03_results.md` template `eff_ffbs_s_M1000+eff_params_s_M1000`). The median of per-night sums is 0.023 s (IQR 0.020–0.028). Report it with its IQR.

**Mi2.** The 0.4 ms conformal time is cited to Table S15, but S15 does not contain it. It also covers one parameter (TST) with n = 152 calibration nights and includes evaluation overhead (`e10` l.55–59). Add it to S15, defined per night for all 8 parameters.

**Mi3.** `@njit(cache=True)` writes to the package's `__pycache__`. In read-only clinical installs, every process start recompiles (about 2.5 s cold). Note this in the deployment guidance, or offer an ahead-of-time or NumPy (vectorised over M) path.

## Required additional experiments/analyses
1. End-to-end local recalibration (M1): refit BCTS/τ/A plus conformal on n_t target nights, and report coverage, bias and fit time.
2. The M ∈ {100, 300, 1000} table (data exist), plus independent-seed Monte-Carlo error of interval endpoints.
3. A repeated, single-core-pinned timing run with one-off costs, peak RSS, full hardware/library metadata, and full 20-h SC recordings.
4. Results under the single-night σ̄ rule (calibration nights ∪ {this night}).

## Recommendation
**Major revision.** Computationally, the method is cheap: about 0.023 s per night, roughly 1.6 % of stager inference, and the one-off costs are a few seconds. Cost is not an argument against it relative to constant-width intervals. The problems are these:
- The deployment workflow the paper recommends (ten local nights to recalibrate probabilities and intervals) was not evaluated as described (M1).
- A pre-registered sensitivity analysis is silently missing (M2).
- Memory, one-off costs, thread control and scaling are incompletely or misleadingly reported (Mo1–Mo4).

All are fixable with light analyses.

```json
[
 {"id":"M1","severity":"major","title":"Deployment workflow (ten local nights recalibrate probabilities + intervals) never evaluated end-to-end","location":"Discussion l.135, l.141; code/experiments/e03_night_summaries.py l.60-66; e06_cross_cohort.py docstring","evidence":"BCTS/pi_s/A/p0/tau fitted by 5-fold cross-fitting on ~120 HMC/SC and 34-36 ST nights (fold sizes in results/summaries/yasa_xfit.csv); E06 few-night recalibration reuses SC-fitted *_srcSC summaries and refits only the conformal quantile","action":"Refit BCTS (+tau, A) and conformal on n_t in {10,20,30,50} target nights; report bias, coverage, interval score and fit time, or restrict claims/highlights","needs_experiment":true},
 {"id":"M2","severity":"major","title":"Pre-registered M in {100,300,1000} sensitivity computed but not reported and not listed as deviation","location":"PREREGISTERED_PROTOCOL.md l.39; Supplement S1 l.49 and deviation log; night_summary.py l.96-99; make_tables.py l.240","evidence":"make_tables.py contains only a comment, no table produced. Reviewer check: Spearman SD(M100) vs SD(M1000) median 0.967/0.958 (min 0.777), coverage change <=0.7 pp, IS ratio M100/M1000 0.92-1.04; draws are nested so agreement is optimistic","action":"Report M-sensitivity table, declare omission in S1, quantify Monte-Carlo error of interval endpoints with independent seeds; consider M=100-300","needs_experiment":false},
 {"id":"Mo1","severity":"moderate","title":"Timing protocol incomplete; single-core condition unverified; hardware under-reported","location":"code/experiments/e10_efficiency.py l.29-46; results/raw/e10_efficiency_meta.json; Methods l.101; Table S15","evidence":"fit_source_model and numba warm-up untimed (reviewer: ~2.5 s cold JIT, 0.9 s tau grid/120 nights); OMP_NUM_THREADS setdefault after imports, no affinity, torch_threads irrelevant; one repetition per night (FFBS max/min 2.4-6.9x); stager cold (13.1 s first night) vs warmed FFBS; EDF loading untimed; no CPU model/RAM/numba version","action":"Time one-off costs separately, pin to one core with explicit thread settings, repeat timings (median/IQR), report CPU model, RAM and library versions","needs_experiment":true},
 {"id":"Mo2","severity":"moderate","title":"Memory footprint under-reported ~9x","location":"Table S15 samples_MB; code/src/uncertainty/hmm.py l.120; sleep_params.py l.33-51","evidence":"samples_MB = int8 output only; ffbs_sample allocates float64 MxT uniforms (8x) and compute_params ~10 boolean MxT temporaries; reviewer measured +173 MB peak RSS for T=20,160, M=1000 vs 20 MB reported","action":"Report peak RSS; generate uniforms in the kernel or chunk over M; accumulate parameters per sample","needs_experiment":false},
 {"id":"Mo3","severity":"moderate","title":"Scaling to 24-h/multi-night recordings and large cohorts untested","location":"e10_efficiency.py l.5,37 (first 20 nights by name, 821-1200 epochs); sleep_params.py l.37-43; Results l.124; Discussion l.139","evidence":"Cost is linear (~0.06 s/24 h; 0.32 s measured for 20,160 epochs) but nocturnal p0/A with tau~0.1 and whole-window first/last-sleep definitions reproduce the SC WASO failure mode","action":"Run full 20-h SC recordings for cost and per-sleep-period behaviour, or restrict scope to single-night PSG windows","needs_experiment":true},
 {"id":"Mo4","severity":"moderate","title":"Batch-dependent regulariser and stale conflicting implementation hinder clinical deployment","location":"Methods l.82; code/src/evaluation/conformal_eval.py l.122; code/src/uncertainty/conformal.py l.34-36","evidence":"sigma-bar = median over calibration AND test nights, so a night's interval depends on test-batch composition; conformal.py _scale still uses calibration-only median (not the evaluated method)","action":"Specify single-night rule (calibration nights plus this night), show results unchanged, remove/align stale function, provide single-night inference API","needs_experiment":false},
 {"id":"Mi1","severity":"minor","title":"'Median 0.02 s' is a sum of two medians without dispersion","location":"Results 3.8 l.130; manuscript/sections/03_results.md template","evidence":"eff_ffbs_s_M1000+eff_params_s_M1000; median of per-night sums 0.023 s (IQR 0.020-0.028)","action":"Report median of per-night totals with IQR","needs_experiment":false},
 {"id":"Mi2","severity":"minor","title":"Conformal-step timing cited to S15 but absent there; scope unclear","location":"Results l.130; Table S15; e10_efficiency.py l.55-59","evidence":"0.4 ms is TST only, n=152 calibration nights, includes evaluation overhead; S15 has no such column","action":"Add to S15, defined per night for all 8 parameters","needs_experiment":false},
 {"id":"Mi3","severity":"minor","title":"Runtime numba JIT/cache is a deployment friction","location":"code/src/uncertainty/hmm.py l.21,49,76","evidence":"cache=True writes to package __pycache__; read-only installs recompile each process (~2.5 s cold measured)","action":"Document, or provide ahead-of-time compiled or NumPy-vectorised FFBS path","needs_experiment":false}
]
```
