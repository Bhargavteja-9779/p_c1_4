# Academic Integrity Verification Report — Stage 2.5, Phases C and E + AI Research Failure Mode Checklist

Manuscript: *Per-night prediction intervals for automatically scored sleep parameters: conformal calibration of posterior hypnogram samples compared with limits of agreement* (target: Sleep Medicine).

| Item | Value |
|---|---|
| Pipeline stage | Stage 2.5 (pre-review integrity), sub-report for Phases C, E and the 7-mode checklist. Phases A, B and D are in `phaseABD_references_citations_originality.md` (separate agent). |
| Spec executed | `academic-pipeline/agents/integrity_verification_agent.md` (Phase C C1–C4, Phase E E1–E5, failure-mode checklist, Mode 1, Verdict Criteria, Gray-Zone rule, Output Format); `references/claim_verification_protocol.md`; `references/ai_research_failure_modes.md`; `references/integrity_review_protocol.md` |
| Draft binding | `manuscript/build/manuscript_rendered.md` sha256 `ce84df25e82ef81975409c4a1b12c3c8be9e3c67cdb1c719da961739a243b138`; `tables/manuscript_numbers.json` sha256 `8410f5bf…acda3c`. A fresh render of `manuscript/sections/*.md` with `build_manuscript.py`'s own `render()`/`word_count()` reproduces the committed rendered file byte-for-byte. Evidence files (code, results, tables, figures, supplement, manuscript) are unchanged between commit `af6aab7` (2026-11-17) and HEAD `f984958`. |
| Run | 2026-11-20 (UTC), single model (Claude). Cross-model verification not run (`ARS_CROSS_MODEL` not set). No repository file was modified; scratch work under the session scratchpad. |
| Line numbers | All `Lnnn` locations refer to `manuscript/build/manuscript_rendered.md`. |

## Verification Mode
Initial Verification (Mode 1, Stage 2.5).

## Verdict
**FAIL** (for the Phase C + Phase E sub-scope): 3 SERIOUS (4 claims rated MAJOR_DISTORTION), 1 MEDIUM, 15 MINOR. No fabricated or untraceable number was found. Every reported number traces to a machine output. The primary analysis re-executes bit-exactly from the shipped code and stager predictions.

**AI Research Failure Mode Checklist: BLOCKS.** Mode 1 is SUSPECTED, scoped to one sensitivity claim (seed variability). The other modes are CLEAR or non-blocking.

| Phase | Verdict | Reason |
|---|---|---|
| C — Data verification | **FAIL** | 1 MEDIUM (C1/C4: seed-variability figure not reproducible from shipped artifacts; built from stale or superseded runs) + MINOR items (C2 word-count margin, C3 Fig. 5d / Fig. 1 / Table 3 caption details). C4: 3 OVERSTATED + 1 NOT_SUPPORTED_BY_PROVENANCE alignment rows. |
| E — Claim verification | **FAIL** | 4 MAJOR_DISTORTION (3 distinct issues), 14 MINOR_DISTORTION, 0 UNVERIFIABLE |
| Failure-mode checklist | **Blocks** | Mode 1 SUSPECTED (stale seed-2 run with empty log; seed-1 file differs from the one used for the table) |

## Verification Summary

| Category | Total | Passed | Issues |
|---|---|---|---|
| Reference Existence | — | — | out of scope (Phase A report) |
| Bibliographic Accuracy | — | — | out of scope (Phase A report) |
| Ghost Citations | -- | -- | out of scope (Phase A report) |
| Citation Context Accuracy | — | — | out of scope (Phase B report) |
| Statistical Data Accuracy (C1) | 522 surfaces: 189 placeholder instances (167 unique expressions) + 288 table cells (Table 1: 48, Table 2: 120, Table 3: 120) + ≈45 hard-coded prose numerals | 521 | 1 (seed variability "≤ 2.5 pp"; shipped files give 2.63 pp; MEDIUM) |
| Internal Consistency (C2) | -- | **Fail** | 4 inconsistencies: Discussion "up to 17 %" vs Results "median over parameters" (per-parameter max 26 %); Abstract drops that qualifier; Methods' list of analyses run on the pre-registered design is incomplete; Fig. 5d plots an AUROC that S14/`make_tables.py` suppress. Plus word-count margin (MINOR). |
| Caption fidelity (C3) | 8 artifacts (Tables 1–3, Figs 1–5) | 5 clean | 3 MINOR (Table 3 caption rationale; Fig. 5d <10-event AUROC plotted; Fig. 1 code still uses the superseded reference mask, with no visible effect). No `figure_table_trace[]` exists → trace-unavailable notes. |
| Experiment provenance (C4) | 14 experiment scripts (e01–e15, no e05), 17 logs, 66 result files (raw 19, statistics 34, summaries 13) + 3 manifests; 16 EA rows (46 % of 35 results claims) | 12 ALIGNED | 3 OVERSTATED, 1 NOT_SUPPORTED_BY_PROVENANCE; D7 not run (no passport) |
| Originality Check (D1) | — | — | out of scope (Phase D report) |
| Self-Plagiarism (D2) | — | — | out of scope (Phase D report) |
| Claim Verification (E) | 95 of 104 registered (Mode 1 #549 tiers: HIGH-IMPACT 92, RANDOM 3, TOP-UP 0; NOT-SELECTED 9). Semantic extraction coverage: `not_machine_detectable`; candidate gaps: E1.1 not run → `E1-COVERAGE-UNRESOLVED` | 77 VERIFIED | 4 MAJOR_DISTORTION, 0 UNVERIFIABLE (+14 MINOR_DISTORTION) |

---

## Phase C: Data Verification

### C1. Statistical data cross-referencing

Adaptation: the spec's C1 is written for numbers cited from external sources (WebSearch the original). This paper's statistics are the authors' own results, so their "original source" is the machine output. Each surface was traced to its `manuscript_numbers.json` key, then to the producing `make_tables.py` block, then to the `results/statistics` or `results/raw` file. The values were then **re-derived with independent pandas code**, not by running `make_tables.py`. Where possible, the raw files were themselves regenerated from code and predictions.

**C1.1 Render and number path.** All 189 placeholders in `manuscript/sections/{00_front,03_results,04_discussion}.md` resolve to `tables/manuscript_numbers.json` keys. The build aborts on a missing key. A fresh render equals the committed `manuscript_rendered.md`.

**C1.2 Independent recomputation (results):**

| Surface group | Source traced | Recomputation | Result |
|---|---|---|---|
| Primary-protocol aggregates (`e15_summary`, `e15_local`, `e15_points`): coverage mean/2.5/97.5 pct, widths, IS, local P(cov<0.80), bias/MAE | `results/raw/e12_honest_*.csv.gz`, `e12_points_*.csv.gz` | regrouped from raw, both stagers | max abs diff ≤ 6e-14 (exact) |
| **Table 2** (YASA) + S4 (LightGBM): 48 rows × coverage, CI, width, 3 IS ratios with CI and stars | e15 recompute + `e15_paired.csv` | 240 cells rebuilt and string-compared | 0 mismatches |
| **Table 3** (YASA): 24 rows × 5 estimators | recomputed points | 120 cells string-compared | 0 mismatches |
| **Table 1**: nights, subjects, epochs, stage %, age, female nights, per-night accuracy/κ, pooled κ, both stagers | `results/predictions/*/*.npz` (P, y) + `results/summaries/yasa_xfit.csv` (nights.csv is not shipped) | recomputed with `sklearn.cohen_kappa_score` | all 48 cells exact; totals 348 / 251 / 362,271 exact |
| Paired permutation tests, Holm, difficulty, worst-quartile coverage, decisions (≈60 manuscript numbers incl. every Table 2 star) | `e15_paired/difficulty/q1coverage/decisions.csv` ← `e12_nights_*.csv.gz` (**not shipped**; gitignored, ~90 MB) | **Re-executed E12 within-cohort for both stagers (300 tasks) from code + shipped predictions**. Then ran `e15_honest_stats.py`'s own `paired()`, `difficulty()`, `decisions()` on the regenerated per-night file. | 14,400/14,400 per-split rows identical (max diff 0.0); 3,600/3,600 point rows identical. 288 paired rows: ratio/CI diff ≤ 4e-16, p and p_holm identical, **0 significance flips** (YASA; LightGBM identical, see C1.4). Difficulty, Q1 coverage (576 rows) and decisions (144 rows) identical for both. |
| Cross-cohort transport (N3 % 38/55/44/46 %, LightGBM TST-HMC 51 %) | `e06_source_only_*.csv` | re-executed `evaluate()` on `yasa_srcSC.csv` for all 8 params × 2 targets × 4 methods | max abs diff 0 |
| Spearman success criterion (30/48; TST 6/6; WASO 1/6; N2 % 2; N1 % 6/6) | `e13_spearman.csv` ← `e04_loso_*.csv` | re-ran with the same bootstrap seed (B = 1000) | ρ and lo95 identical (diff 0.0) |
| Pre-registered/auxiliary: uncalibrated percentiles 30–84 %, Mondrian 5/6, subgroups 87–94 %, non-covered 0.75 vs 0.81, WASO mechanism (116.5 → "116" min, 0.5 min, 49 %, 1 %, ρ 0.79), M = 100 ≤ 1.1 pp, cal25 89.4–93.3 %, robustness 86/70/51 %, AUROC 0.74/0.57/0.79/0.68, cost 0.023 s / 1.42 s, N3 bias +5.9/−4.8, F4-M1 −4.5 / 42 %, τ | `e04_splits_yasa`, `e11_conditional_*`, `e07_*`, `e04_loso_*`, `e08_*`, `e13_*`, `e09_robustness`, `e10_efficiency`, `e14_montage`, `source_models.json` | recomputed from the lowest-level shipped file in each case | all exact **except seed variability** (below) |
| τ ≈ 0.1 | `source_models.json` (pre-registered fits: {0.10, 0.15}) | refitted `fit_source_model` on primary-protocol calibration halves (reps 0, 1; 6 stager × cohort cells) | 0.10–0.15; claim holds for both designs |

In total, 105 + 96 + 31 scripted key-level comparisons against `manuscript_numbers.json` were run: 231 matched exactly and 1 did not.

**C1.3 Hard-coded prose numerals (not from the JSON):** 153/78/25–101 y/44/22/151 (L54; age range and counts from summaries), 10 h window, five-fold, three seeds, τ ∈ [0.02, 1.5], M = 1000, α = 0.10, 50/500/200 splits, n_t ∈ {10, 20, 30}, 0.5/1.0 × robust SD, 10 %/25 % artefacts, thresholds (360/30/30/15 min; 30/30 min/5 pp), 20,000 permutations, 1000 bootstrap resamples, "22 nights" / "22 calibration nights from 11 subjects" (n_cal = n_test = 22 in every ST split), "about 75 nights" (HMC n_cal 75–76), "at least 19 calibration nights" (⌈(n+1)·0.95⌉ ≤ n ⇔ n ≥ 19), 60 min (e08), 348 nights (L48, L159). All are consistent with code and data.

**C1.4 Full regeneration of the unshipped per-night file (both stagers).** E12 within-cohort was re-executed for **all 300 tasks** (2 stagers × 3 cohorts × 50 splits) from `code/experiments/e12_honest_protocol.py` and the shipped predictions; run time ≈ 18 min on 4 cores. Then `e15_honest_stats.py`'s own functions were applied.
- YASA: 14,400/14,400 per-split rows and 3,600/3,600 point rows identical (max diff 0.0). Paired tests 288/288 (ratio/CI diff ≤ 4.4e-16, p and p_holm identical, 0 significance flips); difficulty 48/48, Q1 coverage 576/576, decisions 144/144 identical.
- LightGBM-SC: the same counts, all identical (max diff ≤ 4.4e-16; 0 significance flips).
- Extra facts from the regenerated data: REML ≤ 15 min had **0** positive decisions for either stager ("all as negative" verified). For TST < 6 h, plug-in accuracy on the nights the proposed intervals decided was **97.2 %** (YASA) / 98.2 % (LightGBM), vs 61.1 % / 70.4 % on undecided nights (basis of IL-SERIOUS-3).

**C1 issue:**
- **Seed variability (L144: "varied by at most 2.5 percentage points across 3 stager seeds"; key `seed_max_cov_range` = 0.02509; `tables/tableS_seed_variability.csv`).** Recomputing with `make_tables.py`'s logic on the shipped `results/raw/e04_splits_lgbm_sc_s{0,1,2}.csv.gz` gives **0.0263 (2.6 pp; ST, N2 %, BA-LoA)**. Root cause: the seed-0 and seed-2 files reproduce `tableS_seed_variability_long.csv` exactly, but the shipped **seed-1 file does not** (coverage diff up to 0.023, width up to 7.3 min). It was re-committed at 2026-11-17 17:17 (`af6aab7`), after the last number build at 17:15 (`b3da6cf`). The **seed-2 file** dates from 2026-11-16 09:23 (`d618813`). That is *before* the revision-1 code changes of 2026-11-17 15:23–15:24 (`bcac13d`, `9abf141`: no-mask convention, t-based BA LoA, signed DF-LoA) and before the s1/s2 summaries were regenerated (15:29). It contains only 16 methods (no `ba_reg`, `scp_signed`, `norm_reg_*_s`). `results/experiment_logs/e04_seed2.log` is **empty (0 bytes)**, and `e04_seeds.log` contains only seed 1. `PROJECT_STATE.md` records the rerun chain (whose last steps are "E04 seeds" then E10) as "still running" at the rebuild, and `REPRODUCIBILITY_STATUS.md` marks the post-revision one-command run "PENDING". The reported figure therefore mixes outputs of two code versions (one using the reference-mask convention the CHANGELOG calls a leakage fix) and cannot be regenerated from the shipped files. For the proposed method alone the shipped files give a range of 1.45 pp, so the qualitative conclusion probably survives. → **IL-MEDIUM-1**; Mode 1.

### C2. Internal consistency

| Check | Evidence | Result |
|---|---|---|
| Night/subject/epoch counts across Abstract L29, Intro L48, Methods L54, Results L115, Table 1, Limitations L159 | 348 / 251 / 362,271; per-cohort 153/78, 44/22, 151/151 | consistent |
| Abstract vs Results numbers (coverage 90.2–92.5; reg-LoA 86.0; 21/23 of 24; 0.64–0.86; 38 %; 90.3–92.0; 9–17 %; 64 %/98.7 %/84.2 %) | identical keys in `00_front.md` and `03_results.md` | numerically consistent; abstract L31 drops "median over parameters" (IL-MINOR-1) |
| Results vs Tables (TST ratios, WASO-SC 1.72, coverage ranges, Table 3 biases quoted in §3.4) | Table 2/3 cells = keys | consistent |
| Discussion vs Results | L157 "fell below 80 % in **up to** 17 % of our repetitions" vs L135 "(median over parameters)" and data max 26 % | **inconsistent** (IL-SERIOUS-1) |
| Methods' design statement vs Results | L93 lists analyses run on the pre-registered design as "adaptivity and flagging analyses, the subgroup and robustness analyses and Fig. 1". Also pre-registered but not listed and not labelled where reported: Mondrian (L120), M / calibration-size / seed sensitivity (L144), non-covered analysis (L138), WASO mechanism (L138), τ (L115). | incomplete (IL-MINOR-4) |
| Figure vs supplement rule | Fig. 5d plots ST-REML AUROCs with 8 events. S14 title and `make_tables.py` suppress AUROC when < 10 events. | inconsistent (IL-MINOR-13) |
| Word counts vs limits (5,000 / 300) | Build counter: main 4,946, abstract 297 (`build/word_counts.json`). The counter excludes stand-alone symbol tokens ("%", "<"). A whitespace-token count gives **abstract 301** (305 with the four labels) and main text ≈ 5,015 (headings kept, display equations removed, citations as one token). Highlights ≤ 82 characters (limit 85, per PROJECT_STATE). | within limit only under the script's convention (IL-MINOR-15) |
| Percentages/ratios arithmetic | "halved MAE" 40.05 → 19.55; "29 % wider" = median of per-parameter width ratios 1.13–1.44; "about 5 %" = 1 − 1/1.0545 | correct |

### C3. Figure/table caption fidelity

No Figure Package / `figure_table_trace[]` exists. Per the spec this is the legacy case: **trace-unavailable note (PASS WITH NOTES)** for every figure and table. As a substitute, each caption was checked against the generating code (`code/scripts/make_figures.py`, `make_tables.py`) and the rendered PNG.

| Artifact | Caption vs code / data / image | Outcome |
|---|---|---|
| Table 1 (L208) | means ± SD over nights on scored epochs; pooled κ; LightGBM SC out-of-fold (`e02`: subject-grouped 5-fold) | PASS (note: trace unavailable) |
| Table 2 (L229) | 50 splits; components on calibration half; coverage mean (2.5–97.5 %); per-subject IS ratio with bootstrap CI; * = Holm p < 0.05, family = 10 comparators × 8 params per cohort × stager | PASS (note) |
| Table 3 (L258) | estimators and 10-local-night columns match `e12`/`e15`. "Not applicable to SC, the source of the in-domain stager" is given as the reason for a **YASA** table (E12's local setting simply omits SC for both stagers). | MINOR (IL-MINOR-12) |
| Fig. 1 (L289) | panels a–f match code (HMC night SN050, LOSO pre-registered interval, BA LoA). The code computes histograms with `compute_params(S, mask)`, i.e. the superseded reference-mask convention, but SN050 has 0 unscored epochs, so the image is unaffected. | PASS with note (IL-MINOR-14) |
| Fig. 2 (L291) | comparators: ratio of split-mean IS (`e15_summary`); proposed: per-subject paired ratio + CI (`e15_paired`), as captioned. Image values match Table 2 (e.g. YASA ST SOL 1.99; SC WASO 1.72). | PASS (note: two ratio estimators share an axis; the caption discloses it) |
| Fig. 3 (L293) | (a, d) `e06` source-only; (b, e) mean over params, HMC band; (c, f) median P(cov < 0.8); DF-LoA dropped where widths are non-finite (n_t = 10). Image: YASA HMC/ST at n = 10: 0.09/0.17. | PASS (note) |
| Fig. 4 (L295) | `e09`, clean + 4 corruptions, TST/WASO/N3 %, coverage and width | PASS (note) |
| Fig. 5 (L297) | (a–c) LOSO width vs \|plug-in error\|; (d) primary-flag AUROC with 1000-resample cluster-bootstrap CI; (e–h) pooled decisions, dotted = uncorrected plug-in accuracy. Panel d includes ST-REML (8 events), which the supplement suppresses. | MINOR (IL-MINOR-13) |

C3 manuscript-claim linkage (reverse check): the substantive uses ("Fig. 2; Table 2" for the TST claim L125; "Fig. 3a, d" transport L133; "Fig. 5e–h" decisions L141; "Fig. 5a–c" Spearman L144; "Fig. 4" robustness L144; "Fig. 5d" flagging L144) were each checked against the plotted data. The figures support them. The over-generalisations in IL-MINOR-9 concern prose, not the plotted values.

### C4. Experiment provenance and claim alignment

**Boundary (verbatim):** "This check verifies disclosure and claim-to-provenance fidelity. It does not judge whether the experiment was correctly designed, run, statistically adequate, or reproducible by ARS."

(The dispatch additionally asked whether the described methods match the code. That code-conformance audit and the selective re-executions are reported separately below and in the failure-mode checklist; they are not an ARS C4 verdict.)

**D7 declaration-anchored anti-skip: NOT RUN.** No ARS passport exists for this manuscript (no `experiment_intake_declaration`, no `experiment_provenance[]`, no `repro_lock`). Read literally, D7 treats a version-unprovable passport as post-#260, and an absent declaration is FAIL condition 1. Per the dispatch instruction this is recorded as *not run (artifact does not exist)*, not as a pass. If the pipeline requires D7, the author must supply the declaration (`status: experiments_declared`).

**Manual provenance inventory (substitute for `experiment_provenance[]`):** code `code/experiments/e01–e15` (no e05; the protocol's planned "E05 ablation" and "E08 sensitivity" were folded into E04/E13, per S1/CHANGELOG). Logs `results/experiment_logs/` (17 files; no Traceback/Error; `e12.log` and `e12_early.log` byte-identical; **`e04_seed2.log` empty**; no logs for e01/e02 inference). Outputs: predictions for all 348 nights × 2 stagers (+ seeds 1/2, corruptions, F4-M1), summaries, raw and statistics files. Exception: `e12_nights_*.csv.gz` is **not shipped** (gitignored). I regenerated it bit-exactly for YASA from code and shipped predictions (C1.2), so this is a note rather than an issue.

**Methods ↔ code conformance (dispatch extension):**

| Methods statement | Code evidence | Conforms? |
|---|---|---|
| "every label-dependent component … fitted on the calibration subjects only; calibration-night scores from five-fold cross-fitting within the calibration half; test-night summaries from the model fitted on the whole calibration half" (L93) | `e12_honest_protocol.py:47–61` (`honest_frames`: K = 5 subject folds within `cal_nights`; `sm_all` fitted on `cal_nights` only); `fit_source_model` (`night_summary.py:34–43`) uses only the passed nights' labels | yes. Bit-exact re-execution confirms the shipped outputs came from this code. |
| subject-grouped splits | `conformal_eval.subject_split` splits unique subjects; `pick_subjects` adds whole subjects | yes |
| 50 splits; 50 reps × n_t ∈ {10, 20, 30} | `e12 --R 50`, `--nt 10 20 30`; raw has 50 reps per cohort / n_t | yes |
| α = 0.10 | `evaluate(..., 0.10)` throughout E12/E15 | yes |
| M = 1000 FFBS samples, exact FFBS | `e12.M = 1000`; `hmm._ffbs`; unit test `test_ffbs_marginals_match_forward_backward` passes | yes |
| σ̄ = median of σ̂ over calibration **and** test nights | `conformal_eval.py:148–150` | yes |
| k = ⌈(n+1)(1−α)⌉; feasible-range clipping | `conformal.py:204–212`; `conformal_eval.clip` | yes |
| BA LoA t-based PI; regression LoA; signed-residual DF-LoA; CQR on half the calibration subjects; entropy scale | `make_interval` branches | yes (entropy scale also carries the σ̄-style regulariser; not stated, trivial) |
| sign-flip permutation test of the mean (20,000), subject-bootstrap CI, Holm within cohort × stager | `stats.perm_mean_paired` (B = 20,000; bootstrap 2,000); `e15.paired` Holm by (stager, cohort, family) | yes, but the two SCALE comparisons form a **separate Holm family of 16** (comparators: 80). Not disclosed (IL-MINOR-5). |
| AUROC CIs: 1000 subject-level cluster-bootstrap resamples | `e07.flagging` `cluster_bootstrap(B = 1000)` | yes. The protocol said 2000; this deviation is not in S1/CHANGELOG (IL-MINOR-5). |
| unscored reference epochs → wake; automatic hypnograms on all epochs | `night_summary.py:67–73` | yes. Leftovers: `sleep_params.py` docstring and Fig. 1 code still describe/apply the mask (IL-MINOR-14). |
| windows, channels, S3 + S4 → N3 | `src/data/sleep.py:3–35, 99–180` | yes |
| robustness: 0.5/1.0 × robust SD; artefacts 10/25 %; 200 splits | `e09.corrupt`; raw has 200 splits | yes |
| "three predefined seeds were run" (L60) with the revision-1 conventions | seed-2 output produced by pre-revision code; seed-1 file used for the table superseded | **no for the seed-variability analysis** (IL-MEDIUM-1) |
| "A single script regenerates every result, table and figure … all numbers … read from machine-generated files" (L109) | `run_all.py` lists all 17 steps, but `REPRODUCIBILITY_STATUS.md`: post-revision run "PENDING"; seed outputs stale; ≈45 numerals typed in prose (all correct) | partially (IL-MINOR-11) |
| Unit tests | `python -m pytest -q -p no:cacheprovider code/tests` → **8 passed** (2.5 s) | — |

**Leakage audit (calibration ↔ test nights):** no test-night label enters any interval in the primary protocol. The only uses of test labels are evaluation-only: coverage, IS, the REML has-REM filter, difficulty strata, decision accuracy. The regulariser uses test-night σ̂, which is label-free and disclosed. In the pre-registered design, HMM components were cross-fitted over the whole cohort, including test-half labels; this is disclosed at L93 and was the reason for the protocol change. One subtlety: the in-domain LightGBM stager's SC predictions are out-of-fold from a fixed 5-fold split (`e02`, seed 2026) that is independent of the E12 halves. So a SC test night's stager was trained on other test-half subjects. The night itself never was, and calibration and test predictions are both OOF and therefore exchangeable. Coverage is unaffected, but the abstract's "every component" wording is too broad (IL-MINOR-3).

**experiment_alignment_results[] (manual rows; rule_version EA-v1; judge = this agent; judge_run_at 2026-11-20; ≥ 30 % sample: 16 of 35 results-section claims):**

| finding_id | claim_id | experiment | result_pointer | manuscript_locator | alignment_verdict |
|---|---|---|---|---|---|
| EA-001 | E07/E40 | E12/E15 | `e15_summary.csv` coverage, method `norm_reg_ffbs` | Abstract L31; §3.2 L118 | ALIGNED |
| EA-002 | E08/E49 | E12/E15 | `e15_paired.csv` comparator `SCALE@FFBS mean` (ratio, p_holm) | Abstract L31; §3.3 L123 | ALIGNED (numbers; label issue in IL-SERIOUS-2) |
| EA-003 | E09/E51 | E12/E15 | `e15_paired.csv` TST × {scp_signed, ba_reg, ba_loa} | Abstract L31; §3.3 L125 | ALIGNED |
| EA-004 | E11/E58 | E06 | `e06_source_only_yasa.csv` HMC N3 % coverage | Abstract L31; §3.5 L133 | ALIGNED |
| EA-005 | E12/E61 | E12/E15 | `e15_local.csv` p_cov_lt80 (median over params) | Abstract L31; §3.5 L135 | ALIGNED (body); abstract qualifier: IL-MINOR-1 |
| EA-006 | E13 | E12/E15 | `e15_decisions.csv` TST < 360 + regenerated per-night file | Abstract L31 | **OVERSTATED** (plug-in accuracy on the same decided nights 97.2 %, not 84.2 %) |
| EA-007 | E45 | E12/E15 | `e15_q1coverage.csv` | §3.2 L120 | ALIGNED |
| EA-008 | E57 | E12/E15 | `e15_points.csv` TST/WASO | §3.4 L130 | ALIGNED |
| EA-009 | E59 | E14 | `e14_montage.csv` N3 % | §3.5 L133 | ALIGNED |
| EA-010 | E63 | E08 | `e08_waso_mechanism_yasa.csv` | §3.6 L138 | ALIGNED |
| EA-011 | E66 | E12/E15 | regenerated `e12_nights_yasa` REML rows: 0 intervals with hi ≤ 15 | §3.7 L141 | ALIGNED |
| EA-012 | E67 | E13 | `e13_spearman.csv` criterion_met | §3.8 L144 | ALIGNED |
| EA-013 | E69 | E04 seeds | `e04_splits_lgbm_sc_s{0,1,2}` coverage range | §3.8 L144 | **OVERSTATED** (shipped provenance: 2.63 pp; s2 superseded) |
| EA-014 | E70 | E09 | `e09_robustness.csv.gz` coverage by corruption × method | §3.8 L144 | **OVERSTATED** ("all methods lost coverage") |
| EA-015 | E81 | E12/E15 | `e15_local.csv` ST n_t = 10 p_cov_lt80 per param (max 0.26, N2 %) | Discussion L157 | **NOT_SUPPORTED_BY_PROVENANCE** |
| EA-016 | E72 | E10 | `e10_efficiency.csv` medians, M = 1000 | §3.8 L144 | ALIGNED |

C4 result: **FAIL** (check-3 verdicts OVERSTATED / NOT_SUPPORTED_BY_PROVENANCE present). Negative results are disclosed (WASO-SC loss, transport failure, suboptimal regulariser, LoA under-coverage, 50 Hz noise test not run) → check-4 visibility satisfied.

---

## Phase E: Claim Verification Results

**Claim Registry coverage sidecar (#737)**
- Status: `not_run`. A `claim-registry/1.0` JSON artifact with byte spans was not produced, and `scripts/claim_registry_coverage.py` was not run in this dispatch. The table below is a rendered view only.
- Registry: not produced as a schema artifact. Draft binding: sha256 `ce84df25…a243b138`.
- Coverage report: none → **`E1-COVERAGE-UNRESOLVED`** (per spec this keeps the checkpoint closed until E1/E1.1 is rerun with the tooling).
- Candidate scope: citation-bearing + quantitative sentences. Candidate-unregistered count: not available.
- Semantic extraction coverage: `not_machine_detectable`.

**Population and tiers.** Registered: 104 claims. **HIGH-IMPACT 92** (every numerical, headline, causal, methods-critical or disputed claim in the Highlights, Abstract, Methods, Results, Discussion, Conclusion and captions) and 12 non-high-impact own-work qualitative claims. **RANDOM sentinel:** ⌈10 % × 12⌉ = 2 → floor 3, drawn with `random.Random(549).sample` → N04, N08, N11. **TOP-UP** 0. **NOT-SELECTED** 9. Literature-cited background claims (Introduction L40–L46, Discussion L151 first two sentences, L157 "as recommended…") are routed to the Phase B citation-context check and are not registered here.

**Source used for E2/E3.** For own-result claims the "cited source" is the machine output named in the row, which was read or recomputed in-session. No external source text was needed, so **E3.1 evidence rows were not built** (`scripts/evidence_rows.py` not run; `phases.E_claims.evidence_source_dir: null`). The checkpoint therefore cannot render evidence-row pages for this sub-report.

| Verdict | Claim Count | Proportion |
|---|---|---|
| VERIFIED | 77 | 81.1 % |
| MINOR_DISTORTION | 14 | 14.7 % |
| MAJOR_DISTORTION | 4 | 4.2 % |
| UNVERIFIABLE | 0 | 0 % |
| UNVERIFIABLE_ACCESS | 0 | 0 % |

### Claim table (selected claims; basis: H = headline, N = numerical, C = causal, M = methods-critical, D = disputed)

| ID | Location | Claim (abridged) | Tier / basis | Evidence (what was checked) | Verdict |
|---|---|---|---|---|---|
| E01 | L20 | conformally calibrated samples gave valid per-night 90 % intervals | HI / H | 48/48 cells within ±3 pp (raw recompute) | VERIFIED |
| E02 | L21 | TST: more efficient than LoA | HI / H | TST IS ratio < 1 vs all 3 LoA in 18/18 stager × cohort cells | VERIFIED |
| E03 | L22 | gains parameter-specific; WASO worse in long recordings | HI / H | WASO-SC only significant loss vs DF-LoA (1.72, p_holm 0.004; 1.50, 0.038) | VERIFIED |
| E04 | L23 | "Coverage did not transfer between cohorts" | HI / H | `e06`: YASA proposed ≥ 0.87 in 9/16 target × param cells; failures concentrate in N3 %, REML (LightGBM also TST-HMC). Results L133 "did not transfer reliably" is accurate. | MINOR_DISTORTION |
| E05 | L29 | 348 nights, 251 subjects | HI / N | npz + summaries | VERIFIED |
| E06 | L29 | "fitting every component on calibration nights only" | HI / H, M | all HMM/calibration/conformal components: yes (code + re-execution). The in-domain stager's SC predictions are OOF from a fixed 5-fold split independent of the halves. | MINOR_DISTORTION |
| E07 | L31 | 90.2–92.5 % (YASA); reg-LoA mean 86.0 % | HI / H, N | raw recompute | VERIFIED |
| E08 | L31 | scale vs constant width at same centre: lower in 21 and 23 of 24, never significantly worse | HI / H, N | `e15_paired` SCALE@FFBS mean: 21/23, sig-worse 0/0; reproduced from regenerated per-night data (YASA) | VERIFIED |
| E09 | L31 | TST lower IS than every LoA in all cohorts; vs DF 0.64–0.86 | HI / H, N | 9/9 YASA ratios < 1; DF ratios 0.640/0.862 | VERIFIED |
| E10 | L31 | other parameters showed no consistent gain; WASO worse in long recordings | HI / H | non-TST mean ratio vs DF 1.07/0.98; 15/24 lower each; WASO-SC significant loss | VERIFIED |
| E11 | L31 | N3 % coverage 38 % in another cohort | HI / H, N | re-executed `e06`: 0.377 | VERIFIED |
| E12 | L31 | with 10 local nights mean coverage 90.3–92.0 %; realised coverage < 80 % in 9–17 % of repetitions | HI / H, N | numbers exact, but 9/17 % are **medians over parameters** (stated at L135, dropped here). Per-parameter range 2–26 %. | MINOR_DISTORTION |
| **E13** | **L31** | "intervals decided 64 % of nights with 98.7 % accuracy (automatic TST alone: 84.2 %)" | HI / H, N | numbers exact. But 84.2 % is plug-in accuracy on **all** nights. On the same 64 % of nights the plug-in was **97.2 %** accurate, and on the undecided 36 % it was 61.1 % (regenerated per-night data, YASA, pooled as in E15). The juxtaposition implies a ≈14-pp accuracy gain where the like-for-like gain is 1.5 pp; the benefit is triage. | **MAJOR_DISTORTION** |
| E14 | L33 | conclusions: valid local intervals; TST-specific advantage; local calibration needed | HI / H | supported within design; scope advisory ADV-E4-P1 | VERIFIED |
| E15 | L164 | Conclusion: nominal coverage within population; TST-specific advantage incl. threshold decisions; local calibration, preferably ≥ 20 nights | HI / H | as E07, E09, E73, E60–E61 (the "≥ 20" recommendation rests on the 19-night DF bound and the risk data; see IL-SERIOUS-1) | VERIFIED |
| E16 | L54 | cohort sizes; ages 25–101 (SC); ST placebo/temazepam | HI / N, M | summaries: SC age 25–101, 75/78 subjects with 2 nights; ST conditions placebo/temazepam × 22 | VERIFIED |
| E17–E23 | L54–L86 | stage merge; windows; unscored → wake; channels; LightGBM OOF/seeds; BCTS/HMM/τ grid/M = 1000/FFBS; score, σ̄, k, clipping, CV+ caveat | HI / M | code lines cited in C4 table; unit tests pass. The 116-feature count is taken from code docstrings; the feature cache is not shipped, so it was not executed. | VERIFIED |
| E24 | L86 | method, score and α fixed in a protocol before any interval was computed | HI / M, D | protocol fixes α, M, "norm_reg". σ̄ was changed from calibration-only to calibration + test median **after first E04 results** (CHANGELOG "Method correction…", stated negligible). Documented in S1 but not in this sentence. | MINOR_DISTORTION |
| E25 | L89 | comparators (a)–(h) | HI / M | `make_interval` | VERIFIED |
| E26 | L89 | "(b)–(d) beyond the pre-specified ones, the factorial and the scale-only ablations were added **during review**" | HI / M, D | `scp_abs_cal`, `scp_abs_bc` and the factorial were added on 2026-11-15/16 "after first E04/E07 results", before review cycle 1 (CHANGELOG; commit `b0689d3`). The cover letter's "after the first results" is accurate. | MINOR_DISTORTION |
| E27 | L93 | primary end-to-end design | HI / M, N | code + bit-exact re-execution (300 tasks, both stagers) | VERIFIED |
| E28 | L93 | pre-registered design used for "adaptivity and flagging, subgroup and robustness analyses and Fig. 1" | HI / M | also used for Mondrian, M / cal-size / seed sensitivity, non-covered and WASO-mechanism analyses, uncalibrated percentiles, τ | MINOR_DISTORTION |
| E29–E33 | L95–L103 | difficulty / Mondrian, local, transport, robustness, thresholds "fixed before the analysis was run" | HI / M | code. Thresholds committed in `e15` code at 15:29 (`a76f7e6`); EXPERIMENT_LOG dates the early E15 run 16:00–16:53. Consistent; git order cannot prove run order. | VERIFIED |
| E34 | L106 | statistical analysis description | HI / M, N | as coded, except the undisclosed separate Holm family for SCALE tests and the AUROC bootstrap 1000 vs protocol 2000 | MINOR_DISTORTION |
| **E35** | **L106** | "Pre-specified success criteria were: … a lower interval score than constant-width intervals (Holm-adjusted p < 0.05); and a positive width–error Spearman correlation…" | HI / M, D | Protocol (`PREREGISTERED_PROTOCOL.md`, S1): "considered better than constant-width intervals **only if** its mean interval score is lower with a Holm-adjusted p < 0.05 **and** its width–error Spearman correlation is positive…". The hypothesis names the constant-width comparators "(Bland–Altman LoA; split-conformal absolute residual)". Listing them as separate criteria drops the conjunction. | **MAJOR_DISTORTION** (with E48) |
| E36 | L109 | software versions; 4-core CPU | HI / N | `requirements.txt`; `e10_efficiency_meta.json` (cpu_count 4, Python 3.13.18) | VERIFIED |
| E37 | L109 | single script regenerates everything; all numbers machine-generated | HI / M | see C4 (post-revision run PENDING; stale seed outputs; numerals typed in prose, all correct) | MINOR_DISTORTION |
| E38–E47 | L115–L120 | §3.1–3.2 numbers (κ, τ, coverage ranges, 48/48, 68 % ST, DF 87.1–92.8 lowest in ST, BA/reg ranges, 30–84 %, Q1 84.7 (72–99) etc., Mondrian 5/6, subgroups 87–94 %) | HI / N | all recomputed exactly (C1.2). The DF-LoA "instability" explanation (L118) is interpretive and untested. | VERIFIED |
| **E48** | **L123** | "*Adaptive scale at a fixed centre (pre-specified criterion).*" | HI / D, M | The fixed-centre comparison (`scp_abs_mu` vs proposed) is a post-hoc operationalisation added with the factorial after first results. Under the protocol's conjunctive rule at this centre: 12/24 (YASA), 10/24 (LightGBM), not the 15/15 shown. Against the protocol-named comparators: BA-LoA 5/24 and 2/24 (primary design); split-conformal around the raw plug-in 8/24 and 2/24 (pre-registered design; `scp_abs` is not run in E12). The re-operationalisation is not recorded as a deviation in S1/CHANGELOG, and `EXPERIMENT_LOG.md` labels it "pre-specified criterion … Met". | **MAJOR_DISTORTION** |
| E49–E55 | L123–L127 | §3.3 counts/ratios (21/23, 0.92, 15/15, 21/21 (12/9), 20/19, 20/20, 1.05; TST 18/18 < 1, all Holm p < 0.05 vs DF, 3/6, 5/6; 15/15; sig list; 1.07/0.98; WASO-SC 1.72/1.50; reg-LoA lower in 13/21 and 11/21 non-TST; 17/19 vs 10/14) | HI / N | `e15_paired`/`e15_difficulty`. YASA reproduced from regenerated per-night data with 0 significance flips. | VERIFIED |
| E56 | L130 | "The stagers' own hypnograms underestimated TST … LightGBM results were similar" | HI / N, C | YASA: −21.4/−22.6/−38.3. LightGBM plug-in **over**estimates TST in SC (+10.8 min; −11.5 ST, −37.6 HMC), and its HMC MAE goes 47.2 → 30.1 (not halved). | MINOR_DISTORTION |
| E57 | L130 | YASA point-estimate numbers | HI / N | Table 3 / `e15_points` | VERIFIED |
| E58–E63 | L133–L138 | transport, montage, local deployment, error analysis, WASO mechanism | HI / N, C | recomputed / re-executed. Causal attributions ("because … N3 bias reversed"; "points to population or scoring rules"; WASO mechanism) are consistent with the data (bias sign flip; F4-M1 does not restore coverage; ρ 0.79 + WASO definition in `sleep_params.py`) and appropriately hedged. | VERIFIED |
| E64 | L141 | TST decisions, "whereas classifying **every** night by its plug-in TST was correct for 84.2 %" | HI / N | exact; denominator stated | VERIFIED |
| E65 | L141 | WASO/SOL decisions | HI / N | `e15_decisions` + regenerated | VERIFIED |
| E66 | L141 | REML ≤ 15: prevalence 2.5 %, 53 % (33 %) decided, "all as negative" | HI / N | regenerated per-night data: 0 intervals with hi ≤ 15 (proposed: 4,599 negative of 8,647 night-reps; DF: 2,856) | VERIFIED |
| E67–E68 | L144 | Spearman 30/48 etc.; M = 100 ≤ 1.1 pp; cal25 89.4–93.3 % | HI / N | re-run bootstrap identical; `e13_*` | VERIFIED |
| E69 | L144 | "varied by at most 2.5 percentage points across 3 stager seeds" | HI / N | shipped files: 2.63 pp; table built from a superseded s1 file and a pre-revision s2 file | MINOR_DISTORTION (+ IL-MEDIUM-1) |
| E70 | L144 | "Under signal corruption of test nights all methods lost coverage … adaptive intervals less so"; "under strong Gaussian noise no method remained valid" | HI / N, C | with artefacts, `norm_entropy_reg` (+1.2/+1.0 pp) and `cqr_ffbs` (+0.3 pp, art10) did not lose coverage. Under 1.0-SD noise the proposed/CQR/entropy intervals still covered ≥ 0.87 for N1 % and SOL; the mean over parameters is ≤ 0.74 for every method. | MINOR_DISTORTION |
| E71–E72 | L144 | AUROC 0.74 vs 0.57, 0.79 vs 0.68; 0.02 s vs 1.4 s | HI / N | recomputed (point estimates; "better" is not tested and the CIs overlap) | VERIFIED |
| E73 | L149 | TST: lower IS than all LoA, significantly vs DF; more confident decisions at 6 h | HI / H | 18/18; 6/6; 64 vs 60 vs 54 % | VERIFIED |
| E74 | L149 | "Neither the intervals nor any limits of agreement transferred between cohorts" | HI / H | as E04 | MINOR_DISTORTION |
| E75 | L151 | "The present procedure adds that guarantee … for any stager" | HI / H | model-agnostic split-conformal property. Methods L86 discloses the CV+ (≥ 1−2α) weakening in the primary design. Novelty: ADV-E5-1. | VERIFIED (note) |
| E76–E79 | L153–L157 | TST 6/6, N2 % 2, WASO 1, N1 % 6/6; SOL: CQR better (ratios 1.02–1.67, 4/6 significant); reg-LoA competitive but under-covers; 55–68 min; HMC problem absent (WASO ratio 0.88, posterior-mean bias +9.9); ≈5 %; calibrated plug-in an equally good centre (ratio within ±5 % in 7–8/24); recalibration removed most TST bias | HI / N, C | `e13_spearman`, `e15_paired`, `e15_points` | VERIFIED |
| E80 | L157 | for non-TST parameters DF-LoA "were a simpler and equally informative alternative" | HI / H | mean ratio excl. TST 1.07/0.98, but the proposed method is significantly better for N2 % (HMC, SC) and REML (SC) and significantly worse for WASO-SC (YASA) | MINOR_DISTORTION |
| **E81** | **L157** | "a site's realised coverage still fell below 80 % in **up to 17 %** of our repetitions" | HI / N | 17 % is the **median over parameters** (ST, n_t = 10). Per parameter, ST reaches **26 %** (N2 %), 22 % (WASO), 20 % (N3 %), and HMC reaches 16 % (SOL) (`e15_local.csv`). The sentence supports the "≥ 20 nights" recommendation; at n_t = 20/30 ST still reaches 20 %/24 % for single parameters. | **MAJOR_DISTORTION** |
| E82–E84 | L157–L159 | 19-night bound; 30 nights 15 %; ≈85 % worst quartile; DF under-coverage in ST; pre-registered analysis "led to the same qualitative conclusions" | HI / N, D | math; `e15_local`; `e15_q1coverage`. Pre-registered (`e07_paired_tests`): TST < 1 vs all LoA in 12/12 cells (significant 2/3 per LoA/stager); WASO-SC the only significant loss vs DF (YASA). | VERIFIED |
| E85–E86, E88–E92 | L208, L229, L289–L297 | Table 1/2 and Fig. 1–5 captions | HI / M | C3 | VERIFIED (notes) |
| E87 | L258 | Table 3 caption, SC "not applicable … source of the in-domain stager" | HI / M | rationale does not apply to the YASA table | MINOR_DISTORTION |
| N04 | L82 | "σ̂ requires no labels" | RANDOM | σ̂ from FFBS samples of BCTS-calibrated probabilities; the night's own labels are unused | VERIFIED |
| N08 | L159 | "both stagers were feature-based" | RANDOM | YASA LightGBM on 116 features; in-domain LightGBM on the same features | VERIFIED |
| N11 | L155 | WASO failure "is a property of the parameter definition as much as of the method" | RANDOM | hedged interpretation. Plug-in (+29.7) and calibrated plug-in (+25.4) are also biased in SC (definition/window effect); the posterior mean adds ≈ +40 min (method effect). Roughly balanced, as stated. | VERIFIED |

(Unlisted VERIFIED rows are covered by the grouped rows above; ID ranges are inclusive.)

**Scope-conformance advisory (#547)** — `[E4-SKIPPED: no scope context]`. No RQ Brief `scope` object exists (manuscript not produced through ARS Stage 1), so E4 was not run per spec. *Non-spec informational proxy*, comparing against the pre-registered protocol's scope (two feature-based stagers; Sleep-EDF SC/ST and HMC adults; 8 PSG parameters):

| ID | Claim location | Effective scope (proxy) | Drafted scope | Broadened axis |
|---|---|---|---|---|
| ADV-E4-P1 | Abstract Conclusions L33; Conclusion L164 | 2 feature-based stagers, 3 adult cohorts, 2 rule sets | "conformal intervals give valid per-night error ranges for automatically scored sleep parameters" (unqualified) | domain/population (Limitations L159 carries the caveat) |
| ADV-E4-P2 | Discussion L151 | 2 stagers tested | "for any stager that outputs epoch probabilities" | domain (theoretical property; empirical scope two stagers) |

**Novelty-claim classification (#548)**

| ID | Claim location | Claim wording | Classification | Nearest prior work / recommended bounded rewording |
|---|---|---|---|---|
| ADV-E5-1 | Discussion L151 (also cover letter "Our study addresses this gap") | "The present procedure adds that guarantee, in the units clinicians use, for any stager…" (implicit primacy) | UNRESOLVED | Nearest prior work is acknowledged (van Gorp et al. 2023 ICASSP/JBHI; Philips patent application, L44). A search is documented (`supplementary/literature_review_and_journal_benchmark.md`, 2026-11-15: PubMed, Crossref, arXiv, Europe PMC; Google Scholar / IEEE Xplore not searched), but there is no Schema 2 `search_strategy` / `last_searched_at`, and the manuscript wording is not search-bounded. Suggested: "To our knowledge (PubMed, Crossref, arXiv and Europe PMC, searched 15 November 2026), no previous study…". |

**Cache staleness advisory (#541)** — not applicable (no citation cache used in Phases C/E).
**Claim-strength drift (#569)** — `[E6-SKIPPED: no revision evidence]` (first ARS pass; no revision-evidence bundle).
**Token-conservation advisory (#570)** — not applicable (no revision round).

---

## Issue List (Sorted by Severity)

### SERIOUS (Must Fix)

| ID | # | Category | Location | Issue Description | Correct Information | Source |
|---|---|---|---|---|---|---|
| IL-SERIOUS-1 | 1 | Claim (E81, MAJOR_DISTORTION); C2 | Discussion L157 (`04_discussion.md` l.11, key `h_loc_p80_yasa_ST_10_norm_reg_ffbs`) | "realised coverage still fell below 80 % in **up to 17 %** of our repetitions": 17 % is the median over the 8 parameters (ST, 10 nights). The maximum is higher, and the Results (L135) say "median over parameters". | Per parameter (YASA, n_t = 10): ST 10–26 % (max N2 % 26 %), HMC 2–16 %. Suggested: "…fell below 80 % in a median of 9 % (HMC) and 17 % (ST) of repetitions across parameters, and in up to 26 % for individual parameters". Consider also reporting the per-parameter maxima at 20/30 nights (ST: 20 %/24 %) beside the "at least 20 nights" recommendation. | `results/statistics/e15_local.csv` (stager yasa, cohort ST, n_target 10, method norm_reg_ffbs, column p_cov_lt80); recomputed from `results/raw/e12_honest_yasa.csv.gz` |
| IL-SERIOUS-2 | 2 | Claim (E48, E35, MAJOR_DISTORTION); protocol fidelity | §3.3 L123 heading "(pre-specified criterion)"; Methods L106 success-criteria sentence | The fixed-centre scale comparison is presented as "the pre-specified criterion". The protocol's criterion was conjunctive ("only if" IS lower with Holm p < 0.05 **and** Spearman CI > 0) and named BA-LoA and split-conformal absolute residual as the constant-width comparators. The fixed-centre comparator was introduced after the first results. The Methods list the components as separate criteria. | Conjunctive criterion at the fixed centre: 12/24 (YASA), 10/24 (LightGBM). Against BA-LoA (primary): 5/24, 2/24. Against raw-centre split conformal (pre-registered design): 8/24, 2/24. Suggested: relabel as "post-hoc operationalisation of the pre-specified efficiency criterion at a fixed centre", restore the "only if … and" wording in Methods, report the conjunctive outcome and the protocol-named comparator outcome, and add the re-operationalisation to S1. | `supplementary/PREREGISTERED_PROTOCOL.md` ("Hypothesis"; "Success criteria"); `CHANGELOG.md` 2026-11-15 entries; `results/statistics/e15_paired.csv`, `e13_spearman.csv`, `e07_paired_tests_*.csv` |
| IL-SERIOUS-3 | 3 | Claim (E13, MAJOR_DISTORTION) | Abstract L31 (`00_front.md` l.31, keys `h_dec_yasa_TST_*`) | "intervals decided 64 % of nights with 98.7 % accuracy (automatic TST alone: 84.2 %)" compares accuracy on the decided subset with plug-in accuracy on all nights. On the same decided nights the plug-in was 97.2 % accurate. | Like-for-like: 98.7 % vs 97.2 % on the 64 % decided; plug-in only 61.1 % on the 36 % left undecided. Suggested: "…decided 64 % of nights with 98.7 % accuracy (automatic TST on the same nights 97.2 %; on the remaining nights 61 %)". Or reframe the value as identifying the nights where automatic TST is unreliable. Make the same point next to L141 and the Fig. 5 dotted line. | regenerated `e12_nights_yasa` (within; TST; norm_reg_ffbs; pooled over cohorts and repetitions as in `e15_honest_stats.decisions`); `results/statistics/e15_decisions.csv` |

### MEDIUM (Must Fix)

| ID | # | Category | Location | Issue Description | Correct Information | Source |
|---|---|---|---|---|---|---|
| IL-MEDIUM-1 | 1 | Data provenance (C1/C4; E69; Mode 1) | §3.8 L144 ("at most 2.5 percentage points across 3 stager seeds"); `tables/tableS_seed_variability*.csv`; Supplementary S10; key `seed_max_cov_range` | The figure cannot be reproduced from shipped artifacts: those give 2.63 pp. The table used a seed-1 file that was superseded after the last build (17:17 vs 17:15). The seed-2 file was produced on 2026-11-16 by pre-revision code (reference-mask convention, z-based BA LoA; 16 methods). `e04_seed2.log` is empty. | Re-run `code/experiments/e04_within_cohort.py --stagers lgbm_sc_s1 lgbm_sc_s2 --no-loso` with the current code (the unfinished last steps of `code/scripts/rerun_revision1.sh`), then `make_tables.py`, `make_supplement.py`, `build_manuscript.py`. Report the regenerated range. With the shipped files: all four methods 2.63 pp; proposed method alone 1.45 pp. | `results/raw/e04_splits_lgbm_sc_s{0,1,2}.csv.gz` (sha256 s1 `e747b27a…`, s2 `a797bc0d…`); `git log` of those files and of `code/src/evaluation/conformal_eval.py`; `results/experiment_logs/e04_seed2.log` (0 bytes); `PROJECT_STATE.md`; `REPRODUCIBILITY_STATUS.md` |

### MINOR (Recommended Fix at Stage 2.5; Must Fix at Stage 4.5)

| ID | # | Category | Location | Issue Description | Suggestion |
|---|---|---|---|---|---|
| IL-MINOR-1 | 1 | C2 / E12 | Abstract L31 | "fell below 80 % in 9–17 % of repetitions" omits "median over parameters" (per-parameter 2–26 %) | add "(median over parameters)" |
| IL-MINOR-2 | 2 | E04, E74 | Highlight L23; Discussion L149 | blanket "did not transfer" / "Neither … transferred". Data: partial transfer (YASA proposed ≥ 0.87 in 9/16 cells), failing for N3 %, REML and LightGBM TST-HMC | "did not transfer reliably (coverage fell to 38 % for N3 %)", matching L133 |
| IL-MINOR-3 | 3 | E06 | Abstract L29 | "fitting every component on calibration nights only" also covers the in-domain stager, whose SC predictions are OOF from a fixed 5-fold split independent of the calibration halves | "every label-dependent uncertainty component" |
| IL-MINOR-4 | 4 | C2 / E28 | Methods L93; Results L115, L120, L138, L144 | the list of analyses using the pre-registered design omits Mondrian, M / calibration-size / seed sensitivity, non-covered and WASO-mechanism analyses, uncalibrated percentiles and τ. These Results sentences do not say which design they use, and the Mondrian sentence sits beside primary-protocol Q1 numbers. | complete the list; tag those sentences "(pre-registered design)" |
| IL-MINOR-5 | 5 | E34 | Methods L106 | SCALE comparisons use a separate Holm family (16) from the comparator tests (80). The AUROC bootstrap uses 1000 resamples vs 2000 in the protocol; this deviation is not in S1. | state both; add the bootstrap change to S1 |
| IL-MINOR-6 | 6 | E26 | Methods L89 | "added during review": `scp_abs_cal`, `scp_abs_bc` and the factorial were added after first results, before review cycle 1 | "added after the first results or during review (Supplementary S1)" |
| IL-MINOR-7 | 7 | E24 | Methods L86 | "its score … fixed in a protocol": the σ̄ definition changed after first results (calibration-only → calibration + test) | add "(one documented correction of the regulariser; Supplementary S1)" |
| IL-MINOR-8 | 8 | E56 | §3.4 L130 | "The stagers' own hypnograms underestimated TST" (plural); "LightGBM results were similar". LightGBM over-estimates TST in SC (+10.8 min), and its HMC MAE 47.2 → 30.1 is not halved. | "YASA's own hypnograms underestimated TST…"; qualify the LightGBM sentence |
| IL-MINOR-9 | 9 | E70 | §3.8 L144 | "all methods lost coverage". Under artefacts, entropy-scaled (+1.0 to +1.2 pp) and CQR-FFBS (+0.3 pp) did not. "No method remained valid" holds on average and for the Fig. 4 parameters but not for N1 %/SOL. | "under Gaussian noise all methods lost coverage…"; "no method remained valid on average" |
| IL-MINOR-10 | 10 | E80 | Discussion L157 | DF-LoA "equally informative" for non-TST parameters. The proposed method was significantly better for N2 % (HMC, SC) and REML (SC) and worse for WASO-SC (YASA). | "similarly informative on average (mean ratio 1.07 and 0.98), with parameter-specific exceptions" |
| IL-MINOR-11 | 11 | E37; C4 | Methods L109; Code availability L193; cover letter | "A single script regenerates every result … all numbers … read from machine-generated files". The post-revision one-command run is PENDING (`REPRODUCIBILITY_STATUS.md`), seed outputs are stale (IL-MEDIUM-1), ≈45 prose numerals are typed by hand (all verified correct), and the `e12_nights` files are not versioned (regenerable; verified). | complete the full `run_all.py` run after IL-MEDIUM-1, then keep or soften the claim; note that per-night E12 files are regenerated |
| IL-MINOR-12 | 12 | C3 / E87 | Table 3 caption L258 | "not applicable to SC, the source of the in-domain stager" given for a YASA table | "local deployment was evaluated on ST and HMC only" |
| IL-MINOR-13 | 13 | C2 / C3 | Fig. 5d (L297); `code/scripts/make_figures.py` `fig5_adaptivity` | plots ST-REML AUROCs with 8 events. S14 and `make_tables.py` suppress AUROC when < 10 events (CHANGELOG: "not interpretable"). | apply the same suppression in the figure, or mark those points |
| IL-MINOR-14 | 14 | C3 / C4 (code hygiene) | `make_figures.py` `fig1_example` (`compute_params(S, mask)`); `code/src/evaluation/sleep_params.py` docstring | the superseded reference-mask convention survives in Fig. 1 code and a docstring. No effect on the published Fig. 1 (SN050 has 0 unscored epochs). | use `compute_params(S)`; update the docstring |
| IL-MINOR-15 | 15 | C2 | front matter L15 | the word counts (4,946 / 297) come from a custom counter that drops stand-alone symbols. A whitespace count gives abstract 301 (305 with labels) and main text ≈ 5,015. | trim ≥ 5 abstract words and ≈ 30 main-text words for margin, or verify with the journal's counting convention |

**Notes (not issues):** E1-COVERAGE-UNRESOLVED (registry tooling not run); C3 trace-unavailable notes for all 8 artifacts; D7 not run (no passport); E3.1 evidence rows not built; E4/E6 skipped; `e12_nights_*.csv.gz` not versioned but regenerated bit-exactly here for both stagers (C1.4); `p_holm = 0.004` recurs because 80 × 1/20,001 is the smallest attainable Holm-adjusted permutation p (resolution floor, not a bug); waso_postwake_SC = 116.5 renders as "116" (round-half-even).

---

## AI Research Failure Mode Checklist

| Mode | Outcome | Evidence | Blocks? |
|---|---|---|---|
| 1. Implementation bug passing AI self-review | **SUSPECTED** (scoped to the seed-variability sensitivity claim) | Detection question "for every numerical result … a saved log?": the seed-2 run has an **empty log**, and its output was produced by superseded code (pre-revision conventions, 16 methods). The seed-1 file used for the table is not the shipped one (IL-MEDIUM-1). Everything else is CLEAR: E12 primary pipeline re-executed **bit-exactly** (all 300 within-cohort tasks, both stagers; C1.4); e06 transport and e13 Spearman bootstrap re-executed exactly; 8/8 unit tests pass (incl. FFBS vs forward–backward marginals); Holm and permutation code inspected; no suspiciously identical CIs; the recurring p_holm = 0.004 is the permutation-resolution floor. Code-hygiene leftovers (Fig. 1 mask, docstring) have no numerical effect. | **yes** (until seeds are rerun or the user overrides) |
| 2. Hallucinated citation | CLEAR (per the parallel Phase A/B report; not re-verified here) | `phaseABD_references_citations_originality.md`: 51/51 references exist (0 NOT_FOUND, 0 MISMATCH, 0 DOI_MISMATCH); bibliographic and context issues are listed there | no |
| 3. Hallucinated experimental result | CLEAR | All 189 placeholder numbers and 288 table cells trace to machine outputs and were recomputed (231/232 key-level matches; the one mismatch is the stale seed figure, assigned to Mode 1). Per-night statistics behind Table 2 stars, decisions and difficulty were regenerated from code + shipped predictions and match exactly. Run counts match claims (50 splits, 500 pre-registered, 200 robustness, 50 local reps, 3 seed files). Boundary: stager inference from raw EDF (E01/E02) was not re-executed (needs the PhysioNet download). Table 1 accuracies were recomputed from the shipped predictions/labels. | no |
| 4. Shortcut reliance | CLEAR (flag-only at 2.5) | The obvious confound (local recalibration vs adaptivity) is ablated by the centre × scale factorial; scale-only ablations exist (pre-registered design). Comparators are strong (DF-LoA, regression LoA, CQR). Subject-grouped splits prevent within-subject leakage. No test-night label enters any interval (leakage audit, C4). Transport failure is reported, not hidden. | no (flag-only) |
| 5. Bug reframed as novel insight | CLEAR | No "surprisingly / unexpectedly / counterintuitively" framing. The main unexpected result (WASO-SC failure) is reported as a failure, with its mechanism traced to the WASO definition (`sleep_params.py`) and the fixed 10-h window (e08: ρ = 0.79). The plug-in is also biased (+25–30 min). τ ≈ 0.1 is an interior optimum of a documented grid. Reviewer-level note, not a bug: the strong emission down-weighting (τ ≈ 0.1) plausibly contributes to spurious late sleep epochs; the attribution at L155 ("as much as of the method") is hedged. | no |
| 6. Methodology fabrication | CLEAR (with notes) | Every Methods number and procedure was found in code (C4 conformance table: windows, channels, BCTS, emissions, τ grid, M, K = 5 cross-fit, σ̄, k, comparators, 20,000 permutations, Holm, 1000 AUROC resamples, 200 robustness splits, thresholds). Description gaps are MINOR (IL-MINOR-4/5/6/7). The one procedure not run as described (seed-2 with current conventions) is the same root cause as Mode 1 and is counted there. | no |
| 7. Frame-lock (pipeline level) | INSUFFICIENT EVIDENCE (needs the author's answer) | Against frame-lock: after review cycle 1 the authors changed the primary analysis, the title and the claims (CHANGELOG "Claims NARROWED"; recommendation changed from ~10 to ≥ 20 nights). Possible residual tell: the efficiency hypothesis was preserved by re-labelling a post-hoc fixed-centre comparison as "the pre-specified criterion" (IL-SERIOUS-2). Detection question for the author: knowing the results, would the HMM/τ objective (smoothed-marginal likelihood) or the posterior-mean centre still be chosen? | no (warning; re-check at 4.5) |

**Block condition:** Mode 1 SUSPECTED blocks at Stage 2.5. User options: (a) confirm and fix (re-run the seed analyses with current code, rebuild); (b) override with recorded reasoning (e.g. the proposed-method seed range is 1.45 pp with the shipped files); (c) revise the passage (drop or soften the seed sentence) and re-run the check.

---

## Not Run / Limitations of this sub-report

- **D7 (C4)** not run: no ARS passport / `experiment_intake_declaration`. A literal reading of the spec would make this a FAIL condition.
- **C3 `figure_table_trace[]`** absent → legacy trace-unavailable notes; a manual caption-vs-code-vs-image check was substituted.
- **E1 registry artifact and E1.1 coverage sidecar** not produced → `E1-COVERAGE-UNRESOLVED`. **E3.1 evidence rows** not built (no external source texts; own-result sources were read in-session).
- **E4** skipped (no RQ Brief scope; only a non-spec proxy is shown). **E6** skipped (first pass). **Cross-model verification** not run.
- Stager inference (raw PSG → epoch probabilities, E01/E02) and the 116-feature count were not re-executed: the raw data and feature cache are not in the repository.
- `results/` data are taken as produced by the code shown; the selective re-executions establish code ↔ output correspondence for the primary protocol, transport and the Spearman criterion, not the truth of the underlying public datasets.

## Verification Audit Trail

Scratch scripts (session scratchpad, may be cleared): `/tmp/claude-0/-home-user-p-c1-4/9c52bd2c-f480-55be-800e-d02a6653c94b/scratchpad/work/`
- `render_check.py`: fresh render == committed rendered file; word counts 4,946 / 297; 189 placeholders listed.
- `wc_check.py`: whitespace counts (abstract 301 / 305 with labels; main ≈ 5,015); highlight lengths 76–82 characters.
- `recompute_e15.py`: e15 summary/local/points from raw e12 (exact); structure (50 reps; n_cal ST 22, HMC 75–76).
- `check_tables23.py`: Table 2 + S4 (240 cells) and Table 3 (120 cells) string-equal; paired-ratio proxy median relative difference 0.44 %.
- `rederive_A.py`, `rederive_B.py`, `rederive_C.py`: 105 + 96 + 31 key re-derivations (1 mismatch: `seed_max_cov_range`); qualitative assertions (18/18 TST ratios < 1; sig-worse lists; min-coverage locations; per-parameter P(cov < 0.8)).
- `seeds.py`, `seeds2.py` + `git log`: seed-file provenance.
- `table1.py`: Table 1 from npz + summaries (exact).
- `transport.py`: e06 re-execution (exact).
- `rerun_e12.py`, `regen_e12_within.py`, `verify_regen.py`: E12 within-cohort re-execution for yasa and lgbm_sc_s0 (env: `LSA_CACHE_ROOT` → scratch `nights.csv` built from `yasa_xfit.csv` night↔subject, `NUMBA_CACHE_DIR` → scratch, `PYTHONDONTWRITEBYTECODE=1`), then E15's own functions on the regenerated per-night data.
- `python -m pytest -q -p no:cacheprovider code/tests` → 8 passed. `git status` clean after all runs.
