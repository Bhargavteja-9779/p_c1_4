# Academic Integrity Re-verification Report: Stage 2.5, FAIL-loop round 1 (Mode 1)

ARS v3.24.4 `integrity_verification_agent`, re-verification of the corrected items of the first Stage 2.5 pass plus an audit of the text the corrections introduced. Run 2026-11-20 (UTC), single model (Claude). No tracked file was modified; scratch work is under `/tmp/claude-0/-home-user-p-c1-4/9c52bd2c-f480-55be-800e-d02a6653c94b/scratchpad/reverify/`.

| Item | Value |
|---|---|
| Draft checked | repo HEAD `4271473` (commits `c50e13a`, `4271473` on top of first-pass entry `af6aab7`) |
| `manuscript/build/manuscript_rendered.md` | sha256 `1e8c97aa…` (line numbers `Lnnn` below refer to this file unless stated) |
| `manuscript/Final_Manuscript.docx` | sha256 `f22343da…`; DOCX and PDF were built 17:44:44–47, one second after the rendered md, and contain the corrected text (checked: "97.2 %", "joint criterion", "parameter median", "transferred poorly", no "pre-registered") |
| `supplementary/Supplementary_Material.md` | sha256 `4abfeb54…` |
| `tables/manuscript_numbers.json` | sha256 `f0973921…` |
| Method | Corrected items re-verified from the lowest-level shipped file, independent code, not the author's scripts. Where a number is reported, "recomputed" means my own pandas/numpy code. Retrieved web content (arXiv PDF, Crossref, PubMed, DataCite, PhysioNet, Springer and nature.com pages) was treated as data. Requests carried a generic User-Agent and no personal data. |

## Verdict

**FAIL** (round 1 re-verification): 0 SERIOUS, **1 MEDIUM**, 18 MINOR. AI Research Failure Mode Checklist: **Mode 1 no longer blocks** (stale-seed concern resolved), Mode 7 still INSUFFICIENT EVIDENCE (author answer pending).

All four first-pass SERIOUS issues and the three MEDIUM issues are resolved in substance and each number I recomputed matches the shipped value. The one open MEDIUM is a Phase C2 consistency defect created by the CE-SERIOUS-3 fix: the like-for-like accuracy numbers now in the Abstract (97.2 % / 61 %) appear nowhere in the body or in the supplement, while Results 3.7 still sets 98.7 % (decided nights) against 84.2 % (all nights). The first-pass correction list asked for the like-for-like comparison in the Abstract "(+ §3.7)"; only the Abstract was changed. A two-sentence and two-column fix is expected to bring the draft to PASS WITH NOTES.

## 1. Verdicts on the nine re-verification items

### Item 1. ABD-SERIOUS-1 (CV+ claim): **RESOLVED**, with one new MINOR (R1-MINOR-9)

New wording (L88): "Our main design departs from this: calibration scores come from models cross-fitted within the calibration set, whereas test nights use the model fitted on all calibration nights. This is the cross-validation variant of Barber et al., which lacks the distribution-free guarantee of CV+ (≥ 1−2α) because CV+ applies the fold models to test nights [barber2021]; validity is therefore an empirical property, and coverage is reported throughout." Supplement S1 item 8 (Supplementary_Material.md L102): "the design corresponds to the cross-validation variant of Barber et al. (2021), for which no distribution-free guarantee is available. Validity is therefore assessed empirically…".

Source check (arXiv 1905.02928v3, 29 May 2020, the latest arXiv version; PDF read with pdftotext; Crossref confirms Ann Stat 49(1):486–507, doi:10.1214/20-AOS1965):
- CV+ (eq. 11, §3) forms the interval from `μ̂_{−S_k(i)}(X_{n+1}) ± R_i^CV`, i.e. it applies the K fold models at the test point. Theorem 4: `P{Y_{n+1} ∈ C^CV+} ≥ 1 − 2α − min{2(1−1/K)/(n/K+1), (1−K/n)/(K+1)}`. The paper's own summary table (§4) writes "K-fold CV+ (11): ≥ 1−2α coverage". So "CV+ applies the fold models to test nights" and "(≥ 1−2α)" as the headline guarantee are accurate to the source.
- The original jackknife (LOO residuals, full-model prediction at the test point) carries "No guarantee" in the §4 table, and the abstract states "Such guarantees are not possible for the original jackknife and we demonstrate examples where the coverage rate may actually vanish."
- The wording is therefore true in substance: the manuscript no longer claims the CV+ guarantee and states validity is empirical. The sentence "(≥ 1−2α) … because CV+ applies the fold models to test nights" reproduces the paper's explanation of why the jackknife+ modification matters.
- Limits of the source check: I could only read arXiv v3; Project Euclid (the AOS version) returned a bot-wall page (HTTP 200, 1,162 bytes, Incapsula), so differences between v3 and the published text are UNVERIFIABLE by me.

Code check: `code/experiments/e12_honest_protocol.py` L47–61 (`honest_frames`): K = 5 subject-grouped folds inside `cal_nights`; calibration-night summaries come from the K fold models (`sm` fitted on `tr`), test-night summaries from `sm_all` fitted on all calibration nights. `src/evaluation/conformal_eval.py` L142–152: one quantile `q` of `|θ−μ̂|/(σ̂+σ̄)` over the calibration (out-of-fold) scores is applied with the test-night `μ̂`, `σ̂` from the full model; `σ̄` = median of `σ̂` over calibration and test nights (L149). The code matches the described design and the docstring (L4–5). This is the K-fold analogue of the jackknife (full-model prediction at the test point), not CV+.

### Item 2. CE-SERIOUS-1 (realised coverage < 80 %): **RESOLVED**

Discussion L159: "…fell below 80 % in a median over parameters of 9 % (HMC) and 17 % (ST) of our repetitions (up to 26 % for single parameters)". Recomputed from `results/statistics/e15_local.csv` (stager yasa, method norm_reg_ffbs, `p_cov_lt80`):
- n_t = 10: HMC median 0.09 (range 0.02–0.16), ST median 0.17 (range 0.10–0.26; maximum N2 % 0.26). Matches the text and keys `h_loc_p80_yasa_{HMC,ST}_10_norm_reg_ffbs` (0.09, 0.17) and `h_loc_p80max_yasa_ST_10_norm_reg_ffbs` (0.26), all placeholder-driven.
- n_t = 30: HMC median 0.07, ST median 0.15 (L137 "with 30 nights still in 7 % and 15 %") ✔. Bland–Altman at n_t = 10: HMC 0.10, ST 0.28 (L137 "10 % and 28 %") ✔.
- Abstract L33 now says "(parameter median)" ✔ (closes CE-MINOR-1).

### Item 3. CE-SERIOUS-2 ("pre-specified criterion" labelling): **RESOLVED WITH NEW ISSUE** (R1-MINOR-10, -11, -12)

Remaining uses of the fixed-centre comparison as the pre-specified criterion: none. Every occurrence of "pre-specified" in the rendered manuscript (10 lines: L91, 95, 103, 117, 120, 122, 125, 146, 157, 161) was read in context. Each refers to something that is in `PROTOCOL.md` (±3 pp; the Spearman criterion; the regulariser; the pre-specified design) or is qualified ("exploratory"; "pre-specified design"). Abstract (L33) and Discussion (L155, "at a fixed centre, widths proportional to the posterior spread were more efficient … in most combinations (significantly in 15 of 24 for YASA)") do not call it pre-specified. §3.3 heading is now "(comparison added after the first results)" (L125). Methods 2.8 (L108) states the protocol's joint criterion ("a lower interval score … together with a positive width–error Spearman correlation …; both conditions are reported separately and jointly"), the separate Holm family and the 1000-vs-2000 resample deviation. S1 item 12 repeats it.

Protocol comparison (`supplementary/PROTOCOL.md` L66–70, "Success criteria"): "the proposed method is considered better than constant-width intervals only if its mean interval score is lower with a Holm-adjusted p < 0.05 and its width–error Spearman correlation is positive with a CI excluding 0". L108 is faithful ("together with").

Recomputation of the joint counts (`results/statistics/e15_paired.csv` merged with `e13_spearman.csv` on stager × cohort × param; criterion = ratio < 1 and p_holm < 0.05 and Spearman CI > 0; n = 24 per cell), all equal to the keys `conj_*` and to L125:

| comparator | YASA | LightGBM |
|---|---|---|
| fixed-centre constant width (SCALE@FFBS mean) | 12 | 10 (text: "12 and 10 of 24") |
| Bland–Altman (ba_loa) | 5 | 2 (text: "5 and 2") |
| ratio < 1 and p_holm < 0.05 only (no Spearman), SCALE@FFBS mean | 15 | 15 (text: "significantly in 15 and 15") |
| ratio < 1 only | 21 | 23 (text: "21 … 23") |
| SCALE@FFBS mean, ratio > 1 and p_holm < 0.05 | 0 | 0 ("never significantly worse") |

Spearman criterion: 30/48 met, TST 6/6, WASO 1/6 (L146) ✔. Residual points (all MINOR): the joint counts combine paired interval-score tests from the end-to-end protocol with Spearman CIs from the pre-specified-design LOSO analysis (`e13_prespecified_sensitivity.py::spearman_criterion` reads `e04_loso_*.csv`), which §3.3 does not say (R1-MINOR-10); the protocol-named split-conformal absolute-residual comparator (`scp_abs`) is not run in the end-to-end protocol and has no joint count in the paper (R1-MINOR-10); "pre-registered" survives in code comments (R1-MINOR-11); supplement headings S9/S11 and an S16 row over-claim pre-specification (R1-MINOR-12).

### Item 4. CE-SERIOUS-3 (Abstract like-for-like accuracy): **RESOLVED WITH NEW ISSUE** (IL-MEDIUM-1)

Abstract L33: "At TST < 6 h, intervals decided 64 % of nights with 98.7 % accuracy (automatic TST on the same nights 97.2 %, elsewhere 61 %)." Recomputed from `results/raw/e12_nights_yasa.csv.gz` (untracked; first checked that it is the file behind the tracked per-split results: aggregating its rows by cohort × rep × param × method reproduces `e12_honest_yasa.csv.gz` coverage exactly, max |diff| 0.0, width and IS ≤ 7e-13 over 14,400 per-split rows, and its `plug` and `y` for TST equal `yasa_xfit.csv` `plug_TST`, `ref_TST` for all 348 nights). Within setting, param TST, method norm_reg_ffbs, pooled over 8,672 night-splits:

| quantity | recomputed | reported / key |
|---|---|---|
| frac. of nights decided (interval entirely on one side of 360 min) | 0.6394 | 64 % (`h_dec_yasa_TST_norm_reg_ffbs_frac` 0.63941) |
| accuracy of decided nights | 0.9870 | 98.7 % (`..._acc` 0.98702) |
| plug-in accuracy, all nights | 0.8420 | 84.2 % (`h_dec_yasa_TST_plugacc` 0.84202) |
| plug-in accuracy on the decided nights | 0.9724 | 97.2 % (`h_dec_yasa_TST_norm_reg_ffbs_plugacc_conf` 0.97241) |
| plug-in accuracy on the undecided nights | 0.6108 | 61 % (`..._plugacc_unconf` 0.61081) |
| LightGBM, same quantities | 0.5936 / 0.9930 / 0.8691 / 0.9821 / 0.7040 | keys equal |

The numbers are exact and the Abstract no longer implies a 14-point accuracy gain. Why it is not fully resolved: (a) 97.2 % and 61 % appear only in the Abstract. They are not in Results 3.7 (L143), the Fig. 5 caption, or the S8 supplement table, whose columns are `n, prevalence, plugin_accuracy, frac_confident, acc_confident` (Supplementary_Material.md L4783); the new columns `plug_acc_confident` / `plug_acc_unconfident` exist only in `tables/tableS_decisions.csv` / `e15_decisions.csv`. Spec C2: an abstract must state only findings, numbers and scope that the body states (MEDIUM). (b) L143 still reads "…98.7 % of these decisions agreed with the reference …, whereas classifying every night by its plug-in TST was correct for 84.2 %", the subset-versus-all juxtaposition the first pass flagged; the first-pass correction #4 read "L31 (+ §3.7)". The Fig. 5e dotted line (0.84) has the same visual effect, though its caption states its basis ("accuracy when every night is decided from the uncorrected automatic value"), which is accurate.

### Item 5. CE-MEDIUM-1 (seed variability): **RESOLVED**

- Key `seed_max_cov_range` = 0.021545 (was 0.025091); L146 "at most 2.2 percentage points across 3 stager seeds" (2.15 rounds to 2.2). Recomputed following `make_tables.py` L464–482 (alpha 0.10; methods norm_reg_ffbs, scp_abs, scp_abs_bc, ba_loa; mean over 500 splits per cohort × param × method; range over seeds 0, 1, 2): maximum 0.021545 (ST, SOL, scp_abs_bc); per method maximum: norm_reg_ffbs 0.014455, ba_loa 0.018240, scp_abs 0.012909, scp_abs_bc 0.021545. Width CV maximum 0.104833 = key `seed_max_width_cv` ✔. The sentence in §3.8 says "coverage … varied by at most 2.2 pp" and the maximum is over all four methods, so it is conservative for the proposed method (1.45 pp). Only these two numeric keys changed by value between `af6aab7` and HEAD (218 keys added, none removed, none else changed; checked with tolerance 1e-9).
- Provenance: `e04_splits_lgbm_sc_s1/s2.csv.gz` have all 20 methods, as do s0. I re-executed `e04_within_cohort._split_task` (current code, shipped `results/summaries/lgbm_sc_s{1,2}_xfit.csv`) for **all 500 splits** × 3 cohorts × 8 parameters × 3 alphas × 20 methods for seeds 1 and 2: 504,000/504,000 rows each, coverage, width and interval-score differences exactly 0.0. Summaries `lgbm_sc_s{1,2}_xfit.csv` were last written in `a76f7e6` (2026-11-17 15:29), after the revision-1 code changes (`bcac13d` 15:23, `9abf141` 15:24), and the `night_summary.py`, `conformal_eval.py` code is unchanged since. The files are therefore current-code outputs, not the superseded ones.
- Logs: `results/experiment_logs/e04_seeds.log` (13,754 bytes) now contains the 20-method coverage tables for both `lgbm_sc_s1` and `lgbm_sc_s2`; `e03_seeds.log` (734 bytes) holds both seeds' τ (all 0.1). The legacy file `e04_seed2.log` is still 0 bytes and was not removed (R1-MINOR-8).
- §3.8 sentence ✔ (see above).

### Item 6. ABD-MEDIUM-1/2 and MINOR reference items: **RESOLVED** for both MEDIUM, MINOR items per Section 2

Corrected `references.json` entries checked against live sources:
- `goldberger2000` (rendered [49]): "PhysioBank, PhysioToolkit, and PhysioNet: components of a new research resource for complex physiologic signals. Circulation 2000;101:e215–20". Crossref `subtitle` = "Components of a New Research Resource for Complex Physiologic Signals", vol 101 issue 23; PubMed 10851218 "Circulation 2000 Jun 13;101(23):E215-20" ✔ (VERIFIED).
- `bourlard1994` ([37]): "Connectionist Speech Recognition: A Hybrid Approach"; Springer page title "Connectionist Speech Recognition: A Hybrid Approach | Springer Nature Link" (Crossref omits the subtitle) ✔.
- `bakker2023` ([19]): "Sleep 2023;46:zsac154"; Crossref print 2023-02-08, vol 46 issue 2; PubMed "2023 Feb 8" ✔.
- `deirossi2025` ([10]): "npj Digit Med 2026;9:55"; nature.com "Cite this article: npj Digit. Med. 9, 55 (2026)", `citation_online_date` 2025/12/16; PubMed and Crossref carry 2025 Dec 16. Both years are defensible; 2026 follows the publisher (no error).
- `kemp2000` ([31]): "Oberyé JJL" ✔ (PubMed 11008419 authors "Oberyé JJ"); `tibshirani2019` ([29]) now "Tibshirani RJ, Barber RF, Candès EJ, Ramdas A", `romano2019` ([45]) "Candès EJ" ✔ (consistent with [30], [42]); `alvarez2021` ([33]) "PLoS One" (NLM form of Crossref "PLOS ONE"); `sleepedf_data` ([32]) authors now "Zwinderman AH, Kamphuisen HAC, Oberyé JJL" and "(version 1.0.0) 2018" (DataCite year 2018, PhysioNet "Discovery DOI (v1.0.0)", "Published Oct. 24, 2013 · Version 1.0.0").
- `vainikka2026` ([18]): Crossref IEEE TBME 73(6):2144–2154, 2026, no update notice; cited at L46 (with the MC-dropout/epoch-flagging group, where its S2 abstract, "Monte Carlo (MC) dropout … Hypnodensity Interval", fits) and L153.

DOCX reference list (python-docx, 50 entries): no "Npj", "Plos", "®", `&amp;`, `<span`, U+2010/U+2011, no "The …" container artefacts; abbreviated NLM-style journal names throughout. Citation check (rendered md vs `references.json`): 50 distinct keys cited (87 instances), **0 dangling**, 1 uncited key (`rohrscheib2026`, deliberately kept out; not printed). DOCX: citation numbers 1–50 all present in the text and all 50 list entries cited. `vainikka2026` cited ✔.

### Item 7. First-pass MINOR items

See Section 2.

### Item 8. New text introduced by the corrections

See Section 3 (audit of every changed sentence, DEVIATIONS.md against CHANGELOG.md, "pre-registered" → "pre-specified", one-off cost table).

### Item 9. Limits and hygiene

See Section 4.

## 2. Status of every first-pass MINOR item (and notes)

Locations are current (rendered md line, or file).

| First-pass ID | Status | Evidence / location |
|---|---|---|
| ABD-MINOR-1 orphans | **Fixed** for `vainikka2026` (cited L46, L153). `rohrscheib2026`: **deliberately not cited**; still in `references.json`, not printed | 0 dangling, 1 unprinted orphan |
| ABD-MINOR-2 bakker2023 year | **Fixed** | [19] 2023;46 |
| ABD-MINOR-3 deirossi2025 year | **Fixed** (2026 per publisher) | [10] |
| ABD-MINOR-4 sleepedf_data | **Partly fixed**: authors and version added; no "[dataset]" label or repository in the rendered entry | [32] |
| ABD-MINOR-5 Oberyé | **Fixed** | [31] |
| ABD-MINOR-6 Tibshirani/Barber names | **Fixed** | [29] |
| ABD-MINOR-7 Candès EJ | **Fixed** | [45] |
| ABD-MINOR-8 patent format | **Not fixed in output**: applicant added to the JSON `note` only; rendered [25] still "…stochastic neural network. EP4388985A1, 2024." (R1-MINOR-1) | |
| ABD-MINOR-9 format consistency | **Partly fixed**: NLM abbreviations via `container-title-short`; "Npj", "Plos", "®", "The …", U+2010 removed. **Not fixed**: mixed title/sentence case, two conference formats ([21], [23] vs [29], [36], [45]), [34] dataset without version/label, books without place (R1-MINOR-2) | |
| ABD-MINOR-10 Bland–Altman 1999 adapted | **Fixed** | L91 (b) "(which replaces the pair mean as regressor because the reference is unknown at prediction time)" |
| ABD-MINOR-11 vangorp2022 hypnodensity | **Fixed** (moved to opening clause) | L46 |
| ABD-MINOR-12 uncited attributions | **Mostly fixed**: "as recommended" removed (L159); Mondrian now cited [vovk2005] (L97). **Not fixed**: "common clinical decision thresholds" (L105) has no source, although provenance ("added after the first results and fixed before this analysis was run") is now stated (R1-MINOR-3) | |
| ABD notes N-1 (McGraw correction), N-2 ("data descriptor", L187), N-3 (wearable studies, L42) | **Not changed** (notes; never block) | |
| CE-MINOR-1 Abstract "median over parameters" | **Fixed** | L33 "(parameter median)" |
| CE-MINOR-2 blanket "did not transfer" | **Mostly fixed**: Highlight L25, Abstract L33, Discussion L151, Conclusion L166. **Not fixed**: cover letter bullet "neither the intervals nor any limits of agreement transfer between cohorts"; Limitations (ii) L161 "it failed across cohorts" (R1-MINOR-4) | |
| CE-MINOR-3 "every component" | **Partly fixed**: Abstract L31 now "all label-dependent components"; still no "uncertainty" qualifier although the in-domain stager is itself label-dependent and its SC predictions are out-of-fold from a fixed split. Methods L95 enumerates the components (R1-MINOR-6) | |
| CE-MINOR-4 list of pre-registered-design analyses | **Fixed in Methods** (L95 lists adaptivity, flagging, subgroup, robustness, Mondrian, sensitivity (M, calibration size, stager seeds), error analysis, τ, Fig. 1; I confirmed in code that each uses the cross-fitted E03/E04 summaries). Results tagging is **partial** (τ L117, Mondrian/subgroups L122, robustness L103 tagged; §3.2 uncalibrated percentiles, §3.6 error analysis, §3.8 M/size/seeds/flagging rely on the S9/S10/S12 pointers) (R1-MINOR-6) | |
| CE-MINOR-5 Holm family, AUROC 1000 vs 2000 | **Fixed** | L108; S1 item 11; true to code (e15 `paired`: SCALE comparators form their own family, 16 vs 80; `e07` `cluster_bootstrap(B=1000)`) |
| CE-MINOR-6 "added during review" | **Fixed** | L91, L105 |
| CE-MINOR-7 σ̄ change | **Fixed** | L88, S1 item 4; verified against git (Section 3) |
| CE-MINOR-8 §3.4 stagers / LightGBM | **Fixed** | L132 ("YASA's own hypnograms"; LightGBM +10.8 min SC, MAE 47 → 30 min HMC) |
| CE-MINOR-9 "all methods lost coverage" | **Fixed** | L146 "most methods … no method remained valid on average" |
| CE-MINOR-10 DF-LoA "equally informative" | **Fixed** | L159 |
| CE-MINOR-11 "single script … every number" | **Partly fixed**: Methods L111 softened; Code availability L195 ("one-command pipeline"), cover letter ("the complete code reproduces every number, table and figure") unchanged; `REPRODUCIBILITY_STATUS.md` still lists the post-revision one-command run as PENDING; ≈45 prose numerals are still typed by hand and L111 still says "the numbers in the Results and tables are read from machine-generated files"; `make_tables.py` now silently skips Table 1 when the cache is absent (R1-MINOR-5) | |
| CE-MINOR-12 Table 3 caption | **Fixed** | L260 "evaluated on ST and HMC only" |
| CE-MINOR-13 Fig. 5d < 10 events | **Fixed in figure/code** (ST REML row is empty in `fig5_adaptivity_decisions.png`); caption does not mention the suppression (R1-MINOR-7) | |
| CE-MINOR-14 Fig. 1 mask / docstring | **Fixed** in code (`compute_params(S)`, docstring); published image unaffected, as predicted | |
| CE-MINOR-15 word counts | **Fixed** (Section 4) | |

## 3. Audit of the new text (git diff `af6aab7..HEAD`)

### 3a. DEVIATIONS.md against CHANGELOG.md, the protocol and git history

Mapping (CHANGELOG entry → DEVIATIONS item): τ grid → 1 ✔; plug-in comparators → 2 ✔; bias-corrected comparators and factorial → 3 ✔; σ̄ → 4 ✔; Mondrian → 5 ✔; P(coverage < 0.80), bootstrap/AUROC < 10 events → 6 ✔; primary analysis changed → 7 ✔; leakage fix → 9 ✔; comparators added, t-based BA, scale-only ablations → 10 ✔; paired-test change → 11 ✔; E13 and 50 Hz → 13 ✔; E14/E15/label-free flag/subgroups/non-finite scores → 14 ✔; title, claims, recommendation → 15 ✔. Items 8 and 12 are new wording (corrected validity statement; the joint criterion).

Claims checked against evidence:
- Item 4 (σ̄ "originally computed on the calibration nights only"): **TRUE**. `git show 8bbf8ce:…/conformal_eval.py` L109 `c = np.median(sc)`; `b0689d3` (2026-11-16 09:04) `c = np.median(np.concatenate([sc, st]))`. "The numerical difference was negligible": **TRUE for the proposed method**: comparing the shipped first-run `e04_splits_yasa.csv` (`8bbf8ce`) with the post-change file (`b0689d3`) on the same 12,000 (cohort, param, split) cells, mean coverage 0.9079 vs 0.9077, mean relative width difference 0.29 %, mean relative interval-score difference 0.24 % (max single-split coverage difference 0.045; the other changes between those commits did not touch the E03 summaries).
- Item 11 (AUROC bootstrap 1000 vs the protocol's 2000): **TRUE**. Protocol "subject-level cluster bootstrap (2000 resamples) for CIs of width ratios and AUROC"; `e07_utility_and_stats.py` L115 `B=1000` (also `B=1000` in `e13` Spearman CIs, and in the first commit). The ratio CIs use 2000 (`stats.perm_mean_paired`, L63) as the protocol says. Item 11 (scale comparisons as a separate Holm family): **TRUE** (`e15_honest_stats.py` L72: groups by `(stager, cohort, fam)`, `fam = comparator.startswith("SCALE")`; 16 vs 80 tests).
- Item 13 (E13 "run after the first draft"): consistent with git (first draft `d618813` 2026-11-16 09:23; E13 added `50c7a1c` 2026-11-16 18:45).
- Item 1 (τ grid): `hmm.py` L152 comment "0.02–0.10 added after the optimum hit the original 0.10 lower bound". Git cannot show that this preceded any interval result: the first commit that contains interval code (`8bbf8ce`) already contains the extended grid.
- Item 14 (one-off costs measured "from the stored predictions by a separate script; the per-night timings come from the original timing run"): **TRUE** (`e10_oneoff.py`; `e10_efficiency_meta.json` keys `hardware` platform `…fc-v470…` vs `one_off_hardware` `…fc-v726…`). The first-pass S15 showed "*[tableS_efficiency_oneoff not available]*" while the CHANGELOG already listed the one-off costs; the table now exists.

Deviations in the CHANGELOG or protocol that are **missing or incomplete in DEVIATIONS.md** (R1-MINOR-14): (i) local deployment: protocol "R = 500 repetitions per n_t, n_t ∈ {10, 20, 30, 50}" vs the primary analysis 50 repetitions and n_t ∈ {10, 20, 30} (n_t = 50 exists only in the pre-specified-design E06); item 7 mentions only the 50 within-cohort splits; (ii) CHANGELOG: Wilcoxon p kept as a secondary column, LOSO coverage CIs no longer used for claims, CQR quantile-crossing guard; (iii) the abandoned ECG pilot (EXPERIMENT_LOG E0, topic change before the protocol; not a protocol deviation). None changes a reported result.

Contradiction inside the S1 block (R1-MINOR-13): the protocol text printed in S1 says "Any later deviation is logged in CHANGELOG.md with its reason" (Supplementary_Material.md L14; `PROTOCOL.md` L4), but the supplement now carries DEVIATIONS.md instead and `CHANGELOG.md` sits outside `Target_Journal_Submission/`. `code/README.md` L75 still points to `../../CHANGELOG.md`, which (L43–44) still says "Validity guarantee for cross-fitted scores stated as CV+-type (>= 1 - 2 alpha; Barber et al. 2021)", the statement the correction removed.

### 3b. "pre-registered" → "pre-specified"

- Rendered manuscript, cover letter, supplement DOCX/md, PDF, tables and figure scripts: no "pre-registered" left (grep, DOCX text, pdftotext).
- **Remaining in the code that ships with the submission**: `code/experiments/e07_utility_and_stats.py` L26, `e13_prespecified_sensitivity.py` L1 (docstring, file already renamed), `code/run_all.py` L4 and L19 ("complete pre-registered analysis"). Internal files outside the package also keep the word (`CHANGELOG.md` L41–42/58, `EXPERIMENT_LOG.md`, `PROJECT_STATE.md`), and `REVIEW/REVIEWER_BRIEF.md` L15 points to the renamed `PREREGISTERED_PROTOCOL.md` (R1-MINOR-11). The state log says the replacement covered "manuscript/code/supplement"; this is incomplete.
- **Mislabelling that "pre-specified" now makes visible** (R1-MINOR-12). `PROTOCOL.md` contains no subgroup analysis, no clinical decision thresholds (TST < 6 h etc.; only the |error| flag thresholds), no Mondrian calibration, no factorial. Yet: S16 row "Test contamination via hyper-parameter tuning" (Supplementary_Material.md L10832; `S_data_and_leakage_audit.md` L23) says "conformal methods and all thresholds pre-specified (PROTOCOL.md)", contradicting S1 items 2, 3, 10, 14; heading "S11. Coverage by subgroup (pre-specified analysis, …)" (L8442); heading "S9. Pre-specified cross-fitted analysis" (L4931) covers tables that include comparators and the factorial added after the first results (S1 items 2–3). The body text is more careful ("pre-specified design"). The protocol's first heading ("Pre-specified study protocol (written 2026-11-15, BEFORE any interval/coverage result was computed)") is byte-identical to the first-committed version (`8bbf8ce` → HEAD is a pure rename, similarity 100 %).
- **Protocol timing statement ("written before any interval/coverage result was computed", S1 heading; L88 "a protocol written before any interval was computed"): what git shows and does not show.**
  - Shows: `PREREGISTERED_PROTOCOL.md` first appears in commit `8bbf8ce` (2026-11-15 16:37:02 UTC, message "Core uncertainty pipeline, experiments E01-E10, statistics, first results"). The previous commit `c92f764` (15:58:56) contains no protocol and no interval code (`src/uncertainty/`, `conformal_eval.py` first appear in `8bbf8ce`); its `PROJECT_STATE.md` "Next exact step" is to run the stagers (E01/E02). The protocol text has not changed since (rename only).
  - Does not show: the order of writing and computing inside `8bbf8ce`. That commit also first records the first interval/coverage outputs (`results/experiment_logs/e04_yasa.log`, `results/raw/e04_splits_*.csv`, `e04_loso_*`, `e06_*`, `e07_*`) and the CHANGELOG entries that label the τ-grid change "before any interval result" and the comparator additions "after first E04/E07 results". Commit timestamps record when snapshots were committed, not when files were authored.
  - Conclusion: the statement is not contradicted by git, and is not corroborated by it; it rests on the authors' attestation. The manuscript (L161) already says the protocol was "held in the study repository and not registered in an external registry". I recommend one further clause in S1 (R1-MINOR-15).

### 3c. One-off cost table (S15, `e10_oneoff.py`)

- **I found no new Methods, Results or Discussion text on the one-off costs.** `grep` of the rendered manuscript and `sections/*.md` for "one-off", "JIT", "peak", "memory" finds nothing; the only cost sentence is the unchanged one in §3.8 (L146: "Sampling (M = 1000) and parameter computation took 0.02 s per night on one CPU core, against 1.4 s for YASA itself (Supplementary S15)"), which agrees with S15 (t_ffbs 0.0132 + t_params 0.0095 = 0.0227 s; t_stager 1.4222 s). The one-off numbers appear only in S15, S1 item 14 and the code. If new main-text sentences were intended, they are not in the build.
- Table values: I replicated `e10_oneoff.py` in scratch (no write to `results/`): peak memory for the 7 × 24 h input at M = 1000 = 184.02 MB (reported 184.023 ✔); M = 100: 20.76 MB (reported 23.548; run-to-run tracemalloc/JIT allocation difference, same order); `fit_source_model` 3.1–3.3 s here vs 4.295 s cold / 2.826 s warm reported (host- and cache-dependent; UNVERIFIABLE exactly, same order).
- Gaps (R1-MINOR-16): the "7 × 24 h recording" is the first SC night's stored probabilities (1,200 epochs) tiled 16.8 × to 20,160 epochs, not a real recording, which neither S15 nor S1 item 14 says; S15 mixes two hosts (per-night timings `fc-v470`, one-off `fc-v726`) without noting it in S15 itself; `peak_MB_*` are `tracemalloc` Python allocations.

### 3d. Other changed sentences (git diff of the rendered manuscript, every hunk read)

Checked and correct: Abstract and Highlights edits (numbers equal the keys); Methods 2.3, 2.6 (b) (regressor is `cal["plug"]`, code L101–110), 2.7 ("added after the first results … fixed before this analysis was run": thresholds exist only in the revision-1 script `e15_honest_stats.py` L29; the claim "fixed before the analysis was run" is unverifiable by git alone), 2.8, 2.9; Results 3.1–3.5, 3.8; Discussion L151–161; the new Limitations sentence L161; Declaration; Ethics; Table 3 caption.

Findings:
- **Dropped qualifiers and results (spec E6, revision-round claim-strength drift; manual semantic pass, the sidecar tooling was not run; advisory rows, outside the issue counts):**
  - ADV-E6-1, Discussion L155: the clause "(a correlation alone was not sufficient: it held for N1 % in 6 of 6 without a consistent gain)" was deleted. The remaining sentence ("interval width correlated with the plug-in error for TST in 6 of 6 …, but for N2 % in only 2 and for WASO in 1") supports the mechanism more strongly than the data do: the Spearman criterion is met 6/6 for N1 % (recomputed from `e13_spearman.csv`) while the N1 % interval-score ratios against distribution-free limits are not significantly below 1 (Table 2: 0.93, 1.07, 0.87).
  - ADV-E6-2, Discussion L155: the sentence "for sleep onset latency, conformalised posterior quantiles were better than the symmetric score (Supplementary S3)" was deleted. It documented a negative result for the proposed score that still holds: `e15_paired.csv`, comparator `cqr_ffbs`, proposed/comparator ratio for SOL 1.205 (HMC, p_holm 0.004), 1.669 (SC, 0.038), 1.496 (ST, 0.004) for YASA; REML-ST 1.399 (p_holm 0.004). No sentence in the manuscript now mentions this.
  - ADV-E6-3, Methods L95: the parenthetical "(so that a test night's model could use labels of other test-half subjects)" was deleted from the description of the pre-specified design, which still underlies the adaptivity, flagging, robustness, Mondrian, sensitivity and error-analysis results. The fact remains in S1 item 7, the S9 introduction and, partly, Limitations (vi) ("cross-fitted over the whole cohort").
  - No roadmap item authorised these changes (they were presumably word-limit trims). Disposition needed: restore or accept with reason.
- R1-MINOR-17: the Methods comparator list (e) lost the description of the CQR-QR features and that it is "fitted on half of the calibration subjects"; neither the manuscript nor S1 states them now (only the code does). "(Supplementary S1)" is cited for (g), but S1 does not define the raw FFBS percentile comparator either (it names "raw Bayesian percentiles").
- Declarations: all `[AUTHOR ACTION REQUIRED]` markers were removed. Competing interests ("no known competing financial interests") and funding ("did not receive any specific grant") follow the recorded author decision ("No competing interests. No funding."). The ethics-determination marker ("state your institution's determination that this analysis … does not require further ethical review") and the cover-letter marker ("add your institution's determination") were deleted without a recorded author decision, and the cover letter says "All authors have approved the submission" while the second author is still a placeholder; the CRediT roles (L175) were assigned to the first author by the assistant, not confirmed in the decision log. These are attestation items for the author, not Phase A–E defects (notes N-R1, N-R2).

## 4. Limits and hygiene

| Check | Result |
|---|---|
| Main text word count (Introduction to Conclusion, DOCX, python-docx `p.text`, whitespace tokens, headings and citation numbers included; limit 5,000) | **4,954** (paragraphs 20–89). Including the OMML equation text (51 math objects, each concatenated as one token): 4,999. Pandoc plain-text conversion that expands equations as TeX source: 5,094 (not a standard convention). The front-matter claim "4,972" comes from the build script's regex counter; it is not a whitespace count. Limit met under the prescribed method with 46 words to spare; under a math-inclusive count the margin is 1 word; Word's own counter was not available (UNVERIFIABLE). |
| Abstract (four labels included, limit 300) | **292** whitespace tokens (32 + 85 + 143 + 32); front matter says "281" (counter drops stand-alone "%", "<" and the labels). Limit met. |
| Highlights ≤ 85 characters | 82, 77, 77, 76, 81 ✔ |
| References ≤ 50 | 50 printed (limit met exactly); `references.json` holds 51 (`rohrscheib2026` unprinted) |
| Display items ≤ 8 | 3 tables + 5 figures = 8 ✔ (at the limit) |
| Template markers `{{`, `<<`, `>>`, `[AUTHOR …]`, `TODO`, `[Date]` in the three DOCX | **none** |
| Placeholders remaining in `Final_Manuscript.docx` (all intentional) | `[Second author name]` ×2 (author line, CRediT); `[Affiliation, address, country]` ×2 (affiliation a, b); `[address, e-mail]` ×1 (corresponding author); `[roles to be completed]` ×1 (CRediT, second author). (`[a, b]` in the Introduction is a mathematical interval, `[Expanded]` a dataset title.) |
| Placeholders in `manuscript/cover_letter.docx` | `[Affiliation, address]`, `[E-mail]` (signature block) |
| Placeholders in `supplementary/Supplementary_Material.docx` | none (the bracketed `[lights-off, +10 h]` etc. in S1 are window definitions) |

Phase C2 re-run (a correction changed body findings): abstract versus body numbers all consistent except 97.2 %/61 % (IL-MEDIUM-1). All 218 new placeholder keys resolve; the build would abort otherwise; only the two seed keys changed value.

## 5. Issues still open

### SERIOUS: none

### MEDIUM

| ID | Origin | Category | Location | Issue | Correct information / suggested fix |
|---|---|---|---|---|---|
| IL-MEDIUM-1 | CE-SERIOUS-3 (partly fixed) | C2 abstract–body consistency; claim framing | Abstract L33; §3.7 L143; S8 table (Supplementary_Material.md L4783 ff.); Fig. 5 caption | "automatic TST on the same nights 97.2 %, elsewhere 61 %" is stated only in the Abstract; §3.7 still says "…98.7 % of these decisions agreed …, whereas classifying every night by its plug-in TST was correct for 84.2 %"; S8 omits `plug_acc_confident` / `plug_acc_unconfident`. | Add to §3.7: "…; on the same nights the plug-in was correct in 97.2 % (61 % on the remaining 36 % of nights)", move the "84.2 % of all nights" figure after it, add the two columns (already in `tables/tableS_decisions.csv`) to the S8 call in `make_supplement.py`, and optionally a note in the Fig. 5 caption. Values: `h_dec_yasa_TST_norm_reg_ffbs_plugacc_conf` / `_unconf`. |

### MINOR (recommended at 2.5; must be fixed by 4.5)

| ID | Origin | Location | Problem | Suggested fix |
|---|---|---|---|---|
| R1-MINOR-1 | ABD-MINOR-8 | ref [25] | Rendered patent entry still "EP4388985A1, 2024." (applicant is in the unrendered `note`) | Put applicant/document type into `title`/`publisher` fields the CSL prints, e.g. "…; Koninklijke Philips NV. European patent application EP4388985A1. 2024 Jun 26 (withdrawn)." |
| R1-MINOR-2 | ABD-MINOR-4, -9 | refs [21], [23] vs [29], [36], [45]; [32], [34]; many titles | Two conference formats; no "[dataset]" label/version for [34]; books without place; mixed Title/sentence case | Harmonise ("In: …"), add dataset fields, normalise to sentence case, or accept as journal-production work |
| R1-MINOR-3 | ABD-MINOR-12 | L105 | "common clinical decision thresholds (TST < 6 h, SOL > 30 min, WASO > 30 min, REM latency ≤ 15 min)" has no source | Cite a guideline or say "illustrative thresholds chosen by the authors" |
| R1-MINOR-4 | CE-MINOR-2 | cover letter bullet 4; L161 (ii) | "neither the intervals nor any limits of agreement transfer between cohorts"; "it failed across cohorts" | "did not transfer reliably (N3 % coverage fell to 38 %)" |
| R1-MINOR-5 | CE-MINOR-11 | L111, L195, cover letter; `REPRODUCIBILITY_STATUS.md`; `make_tables.py` | "reproduces every number, table and figure" / "one-command pipeline" while the post-revision full run is PENDING and ≈45 prose numerals are typed; Table 1 is skipped silently when the cache is missing | Run `run_all.py` once end to end or soften to "stepwise-executed pipeline"; say per-night E12 files are regenerated and Table 1 needs the raw-data cache |
| R1-MINOR-6 | CE-MINOR-3, -4 | Abstract L31; §3.2 L120, §3.6 L140, §3.8 L146 | "all label-dependent components" lacks "uncertainty" (the in-domain stager is label-dependent); several Results passages that use the pre-specified design are not tagged | "all label-dependent uncertainty components"; add "(pre-specified design)" to those passages |
| R1-MINOR-7 | CE-MINOR-13 | Fig. 5 caption | AUROCs from < 10 events are suppressed in panel d (ST REML row empty) without saying so | Add "(AUROC not shown for < 10 events)" |
| R1-MINOR-8 | IL-MEDIUM-1 follow-up | `results/experiment_logs/e04_seed2.log` | Legacy 0-byte log remains although `e04_seeds.log` now holds both seeds | Delete it or write a pointer line |
| R1-MINOR-9 | new (ABD-SERIOUS-1 fix) | L88; S1 item 8 | "the cross-validation variant of Barber et al." is not a construct that paper names or analyses (arXiv v3): it analyses the LOO jackknife ("No guarantee") and K-fold CV+; "no distribution-free guarantee is available" is stronger than "not proved there". CV+ bound given as ≥ 1−2α without the finite-K term (as in the paper's own §4 table) | "the K-fold analogue of the jackknife of Barber et al. [barber2021], for which that paper gives no distribution-free guarantee (CV+ applies the fold models at test time; Theorem 4: coverage ≥ 1−2α−min{…} ≥ 1−2α−√(2/n))" |
| R1-MINOR-10 | new (CE-SERIOUS-2 fix) | L125; L108 | Joint-criterion counts combine end-to-end-protocol interval-score tests with Spearman CIs from the pre-specified-design LOSO analysis; the protocol-named split-conformal absolute-residual comparator has no joint count | Add "(width–error correlation from the pre-specified design, S10)"; optionally report the pre-specified-design joint count (8/24, 2/24 per the first pass) |
| R1-MINOR-11 | new | `code/experiments/e07_utility_and_stats.py` L26; `e13_prespecified_sensitivity.py` L1; `code/run_all.py` L4, L19; `REVIEW/REVIEWER_BRIEF.md` L15 | "pre-registered" survives in shipped code; brief points to renamed file | Replace with "pre-specified"; fix the path |
| R1-MINOR-12 | new | Supplementary_Material.md L10832 (`S_data_and_leakage_audit.md` L23); L8442 (S11); L4931 (S9) | "conformal methods and all thresholds pre-specified" contradicts S1 items 2, 3, 10, 14; S11 "(pre-specified analysis)" and S9 "Pre-specified … analysis" include analyses not in the protocol | "the primary method, α and the error thresholds were pre-specified; comparators and decision thresholds were added later (S1)"; use "pre-specified design" in S9/S11 headings |
| R1-MINOR-13 | new | Supplementary_Material.md L14 (`PROTOCOL.md` L4); `code/README.md` L75; `CHANGELOG.md` L43–44 | Protocol text refers to CHANGELOG.md, not in the package; CHANGELOG still carries the superseded "CV+-type" statement | Add a bracketed note under the protocol ("deviations are listed in the next section"); do not ship CHANGELOG or correct L43–44; fix README |
| R1-MINOR-14 | new | `supplementary/DEVIATIONS.md` | Omits: local deployment R = 500 → 50 and n_t = 50 dropped from the primary analysis; Wilcoxon kept as secondary; LOSO CIs not used for claims; CQR crossing guard | Add one sentence to item 7/11 |
| R1-MINOR-15 | new | S1 protocol heading; L88; cover letter | "written before any interval was computed" is not corroborated by git (protocol and first interval outputs were committed together in `8bbf8ce`); not contradicted | Add to S1: "The repository history cannot date the protocol independently: its first commit (8bbf8ce, 2026-11-15) also contains the first interval outputs; the statement rests on the authors' records." |
| R1-MINOR-16 | new | S15; S1 item 14 | One-off "7 × 24 h recording" is a tiled single night; two hosts; `tracemalloc` memory | State "synthetic input: one night's probabilities repeated to 20,160 epochs"; note the two measurement hosts |
| R1-MINOR-17 | new | L91 (e), (g); S1 | CQR-QR feature set and "fitted on half of the calibration subjects" no longer described anywhere in text | Restore one clause or place the detail in S1 |
| R1-MINOR-18 | new | front matter L17; DOCX | Stated counts 4,972 / 281 are not whitespace counts (4,954 / 292); math-inclusive count 4,999 | State the counting convention or update the figures; trim ~20 words for margin |

### Advisory rows (outside the issue counts)

| ID | Location | Item | Disposition needed |
|---|---|---|---|
| ADV-E6-1 | Discussion L155 | dropped N1 % "correlation without gain" qualifier | restore / authorise with reason |
| ADV-E6-2 | Discussion L155 | dropped "conformalised posterior quantiles were better for SOL" (CQR-FFBS significantly better in 3/3 YASA cohorts) | restore / authorise with reason |
| ADV-E6-3 | Methods L95 | dropped disclosure that the pre-specified design let test-night models use other test-half labels | restore / authorise with reason |
| N-R1 / N-R2 | declarations, cover letter | ethics-determination marker removed without recorded decision; "All authors have approved" with a placeholder co-author; CRediT roles assigned by assistant | author to confirm |
| N-1…N-3 | unchanged first-pass notes (McGraw correction notice, "data descriptor", wearable validations) | not addressed | optional |

## 6. AI Research Failure Mode Checklist (Mode 1 re-check, Mode 7)

| Mode | Outcome | Evidence | Blocks? |
|---|---|---|---|
| 1 Implementation bug passing self-review | **CLEAR** (was SUSPECTED, scoped to the stale seed runs) | `e04_splits_lgbm_sc_s1/s2.csv.gz` regenerated with current code and reproduced bit-exactly: all 500 splits, 504,000 rows each (coverage, width, IS diff 0.0). The reported 2.2 pp = recomputed 0.021545. `e04_seeds.log` and `e03_seeds.log` now document both seeds. Summaries for s1/s2 post-date the revision-1 code. Unchanged and still CLEAR from first pass: E12 primary pipeline re-executed bit-exactly; per-night file consistent with the tracked per-split results. The stale-seed concern is resolved. Residual: legacy empty `e04_seed2.log` (R1-MINOR-8) and the still-PENDING full-pipeline run (R1-MINOR-5), neither a result error. | no |
| 2 Hallucinated citation | CLEAR | 50/50 printed entries verified in the first pass; the 12 corrected/added entries re-verified against Crossref, PubMed, DataCite, PhysioNet, Springer, nature.com; the Barber et al. guarantee checked against the source text | no |
| 3 Hallucinated experimental result | CLEAR | Every new or changed number recomputed (Sections 1–5); only `seed_max_*` changed value | no |
| 4 Shortcut reliance | CLEAR (flag-only) | unchanged | no |
| 5 Bug reframed as insight | CLEAR | unchanged | no |
| 6 Methodology fabrication | CLEAR | Methods 2.5 verified against code; DEVIATIONS claims checked against git and code. Note R1-MINOR-17 (description trimmed, not fabricated) | no |
| 7 Frame-lock | **INSUFFICIENT EVIDENCE**, still needs the author's answer (pending in `PIPELINE_STATE.md`) | The specific tell found in the first pass (re-labelling a post-hoc comparison as the pre-specified criterion) is removed: the joint criterion now shows 12/10 and 5/2 of 24 against 15/15 for the scale-only comparison. The S1 timing statement rests on author attestation (R1-MINOR-15). | no (warning; re-check at 4.5) |

## 7. Not run

- Cross-model verification (`ARS_CROSS_MODEL` unset); cache-staleness advisory (no cache).
- D7 / C4 passport checks: no ARS Material Passport; the experiment-intake declaration is still PENDING (author has not answered). A literal D7 reading would FAIL condition 1.
- Phase D (originality) and Phase B beyond the changed sentences: not re-run (Mode 1 re-verification covers the corrected items; first pass D = PASS). The new sentences are short, authored text; D2 self-plagiarism remains not checkable (second author and affiliation are placeholders).
- E1 registry artifact and E1.1 coverage sidecar (`E1-COVERAGE-UNRESOLVED` from the first pass is unchanged); E3.1 evidence rows; E4 scope advisory (no RQ Brief); E6 sidecar tooling (the ADV-E6 rows are a manual semantic pass).
- Published AOS text of Barber et al. 2021 (Project Euclid bot-wall); Word's own word counter; wall-clock timings of the one-off table (host-dependent).
- Stager inference from raw PSG (E01/E02) and the 116-feature count (raw data not in the repository); `e12_nights_*.csv.gz` is git-ignored, so its tracked-file consistency (Item 4) rests on the per-split reproduction, not on a versioned artefact.

## Verification audit trail

Scratch scripts and outputs (may be cleared): `/tmp/claude-0/-home-user-p-c1-4/9c52bd2c-f480-55be-800e-d02a6653c94b/scratchpad/reverify/`
- `barber/b.pdf`, `b.txt`: arXiv 1905.02928v3 (eq. 11, Theorem 4, §4 table); `export.arxiv.org` API entry (v3, 2020-05-29); Crossref 10.1214/20-AOS1965.
- `item4.py`: per-night consistency with `e12_honest_*` and `yasa_xfit.csv`; decided/undecided plug-in accuracy (both stagers).
- `seedcheck.py` (+ `seedcheck_s1_full.out`, `seedcheck_s2_full.out`): current-code re-execution of E04 `_split_task` for lgbm_sc_s0 (10 splits), s1 and s2 (10, 50 and 500 splits); seed range recomputation.
- `oneoff_check.py`: replication of `e10_oneoff.py` logic without writing results.
- `cr/*.json`, `src/pm.json`, `src/springer.html`, `src/nat.html`, `src/pn.html`: Crossref, PubMed, Springer, nature.com, PhysioNet, DataCite lookups (generic User-Agent).
- `old_e04.csv`, `new_e04.csv`: `git show` of the first-run and post-σ̄-change E04 splits (σ̄ effect).
- `N_old.json`: numbers JSON at `af6aab7` for the by-value diff.
- Git checks: `git log`, `git show 8bbf8ce`/`c92f764` (protocol and interval-code first appearance), `git diff af6aab7..HEAD` (sections, code, references, rendered md).
- `git status` was clean before and after (no tracked file modified, nothing committed).
