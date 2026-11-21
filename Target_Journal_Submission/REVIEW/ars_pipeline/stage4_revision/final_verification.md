# Final verification: ARS Stage 3' re-review and Stage 4.5 integrity delta

Scope: revised manuscript at HEAD `7099752` (delta `6b96c5f..HEAD`). ROOT = `Target_Journal_Submission/`. Line numbers refer to `manuscript/build/manuscript_rendered.md` (R-L). No tracked file was edited; this report is the only file written. Recomputations used pandas/numpy on the stored CSVs (`results/raw/e12_nights_yasa.csv.gz`, `e16_plainsplit_*.csv.gz`, `results/statistics/*.csv`); nothing heavy was re-run. Recomputation of every new `r_*` and `conj_*` quantity matched the shipped value.

## Verdict

**Stage 3' (reviewer-comment closure): 12 RESOLVED, 19 PARTLY, 2 DECLINED, 0 NOT ADDRESSED (33 MAJOR/CRITICAL items).** The calibration confound (DA-1/J-2/M-1) is now disclosed in the abstract, highlights, Results and Discussion, and the "valid" wording is qualified everywhere except in §5. No claim is falsified by the data.

**Stage 4.5 (integrity delta): FAIL.** 0 SERIOUS, 4 MEDIUM, 15 MINOR; plus notes. Every number and factual sentence that is new or changed in the delta matches the data. The 4 MEDIUM items are claim-strength or omission defects, not number errors; all are fixable with sentence-level edits (replacement wording below). Under the spec, any MEDIUM, and at Stage 4.5 any MINOR, blocks release; expect PASS WITH NOTES after the edits.

**Single most likely remaining reason for rejection:** limited clinical and incremental value. Once recalibration is credited to the comparators, the TST gain is a modest 14-16 % interval-score reduction in two of three cohorts (none in ST; 1.18 for YASA), there is no consistent gain for the other seven parameters, and the decision gain is 5-9 percentage points more nights decided, at accuracy equal to a recalibrated plug-in on the same nights. It rests on three small public cohorts with one scorer each and two feature-based stagers, and validity fails across cohorts. A *Sleep Medicine* editor can read this as "recalibrate on local nights and use conformal limits", plus a technical method (the authors' own rejection risk 1 in `journal_selection/selected_journal.md`).

---

## Part A. Reviewer-comment closure (MAJOR/CRITICAL only)

Verdicts: RESOLVED / PARTLY / NOT ADDRESSED / DECLINED-WITH-REASON. "Gap" is what is missing.

| ID | Verdict | Where addressed (R-L / supplement) | Gap |
|---|---|---|---|
| J-1 clinical benefit small; wrong baseline; calibration size | PARTLY | R-L143 (recalibrated plug-in 91.3 % all nights, 98.7 % on decided, 78 % undecided; constant-width around recalibrated TST 55 %; HMC 59 vs 57 %); R-L159 (36 % / 41 % of nights to review); S8 second table (TST, pooled and per cohort) | Decision analysis still uses the ~75-night calibration half (not n = 10-20); no workload-per-100 table; Fig. 5e-h dotted line still the raw plug-in; §5 still "supported more confident threshold decisions" (see F-M1) |
| J-2 TST gain partly recalibration | RESOLVED | R-L127 (0.86 / 0.84 / 1.18, Holm p = 1.00, half-widths 44 vs 53 and 19 vs 19 min); Abstract R-L33, R-L35; Highlight R-L23; R-L151; S1 items 3, 17 | Not added as a Table 2 column (Fig. 2 and S3 carry it). The word "largely" is not supported in SC and HMC (see F-M2) |
| J-3 "valid" unqualified | PARTLY | Highlight R-L22, Abstract R-L35 ("marginal coverage, relative to one scorer"), R-L151, R-L159 | §5 (R-L166) unchanged: no "marginal / average / one scorer" (F-M1) |
| J-4 "at least 20 nights" not backed | RESOLVED | R-L137 (theory 11, 8, 6 % at 10, 20, 30; ST n_t = 30 statement removed); R-L159 (20 = distribution-free needs >= 19, risk falls slowly, rolling audit); S17 observed n = 20 (HMC 7 %, ST 15 %) | None material |
| J-5 thin clinical evidence base | PARTLY | R-L153, R-L161(iii)-(iv) (single scorer; both stagers feature-based, same features; no deep-learning stager). NEEDS-NEW-DATA items stated as limitations | No intended-use/scope sentence ("adult laboratory PSG, stagers that export probabilities"); paediatric, home, wearable and disease cohorts not named as untested; "any stager" at R-L50, R-L62, R-L77 and cover letter (F-m6) |
| M-1 LoA denied recalibrated centre | RESOLVED | Same as J-2; `scp_abs_cal` comparator in S3 and Fig. 2; claims restated; raw-centred LoA labelled as current practice | Signed-residual and Bland-Altman LoA around the calibrated plug-in were not computed (symmetric constant-width variant only) |
| M-2 two nights per subject; "exactly valid" | PARTLY | R-L91 "(exact for exchangeable nights)"; R-L120 attributes ST under-coverage to two nights per subject; R-L161(ii) | Table 2 caption (R-L231) still "exact"; cluster-aware calibration or subject-level coverage not done; "from 11 subjects" deleted from R-L120, so effective calibration size in subjects is no longer stated (F-m1, F-m2). The ST plain-split result (mean coverage 89.3 %, S17) supports the clustering reading but is not interpreted |
| M-3 cross-fit asymmetry untested | PARTLY | Plain-split run: S17, S1 item 16, R-L122 (87.4-93.1 %, 23/24 within ±3 pp, +6 % width). Honestly disclosed; stated as the plain-split variant | CV+ variant not run. Methods §2.5/§2.7 never introduce the analysis (first mention is R-L122, F-m4). Plain-split HMC coverage 0.926 matches exact theory (36/39 = 0.923), which weakens the M-3 concern, but the text does not say so |
| M-4 significance ignores calibration-set variability | DECLINED (disclosed; reason not stated) | R-L108 "p-values are conditional on [the calibration set]" | R-L127 still says "all Holm-adjusted p < 0.05"; Limitations carry no entry. The abstract makes no significance claim for TST, which limits the exposure. Suggest one Limitation clause (F-m11) |
| M-5 site risk = known Beta-binomial | RESOLVED, with one wording defect | R-L137, R-L159; S17 theory table (recomputed, identical to 5 decimals) | R-L137 "which alone gives 14-18 %" misattributes the theory (F-M4) |
| M-6 decisions credit the interval with the centre | PARTLY | R-L143 ("equally accurate on these nights (98.7 %)", 78 % undecided); Abstract R-L33 now compares with constant-width around recalibrated TST | Margin-rule baseline, subject-bootstrap CIs and per-cohort table not added (HMC only); Fig. 5 caption unchanged |
| M-8 pre-specification summary | PARTLY | Abstract reports the protocol's joint criterion (5 and 2 of 24); S1 items 16-17 added; R-L161(vi) shortened | R-L88 "the one later change" unchanged although S1 item 1 (τ grid) is also a change; no dating caveat in main text (S1 says git cannot date the protocol); α-sensitivity not summarised; "same qualitative conclusions" holds in direction only (S9: TST vs distribution-free limits Holm-significant in 4 of 6, F-m10) |
| D-1 LoA mischaracterised | RESOLVED | R-L21, R-L29, R-L44, R-L151 ("one error range for all nights") | Cover letter still carries the old framing (F-m7) |
| D-2 cross-cohort attribution | PARTLY | R-L135 ("population, era, equipment, setting and scoring rules are confounded"); rule-set attribution dropped from R-L155 | F4-C4 and age-tertile analyses not done. "The montage change alone did not explain" is shown only for frontal vs central referential derivations; the bipolar Fpz-Cz of SC/ST is untested and not named as a limitation (add a clause, F-m13) |
| D-3 single-scorer reference | RESOLVED (wording); data part DECLINED as limitation | R-L35, R-L151, R-L159 ("relative to one scorer"), R-L161(iii) | Multi-scorer test stated as limitation only. §5 not qualified (F-M1) |
| D-4 WASO definition and window artefact | RESOLVED (text) | R-L59 definition (matches `sleep_params.py` L8, L47-52); Highlight R-L24 "10-h SC windows"; Abstract "worse in SC"; R-L140, R-L157 | Recording-period WASO sensitivity not reported, although the value is in the repo (SC median 168.5 vs 43 min, HMC 44.5 vs 40.5, `r_waso_incl_postwake_median_*`) |
| D-5 thresholds | PARTLY | R-L105, R-L143 ("illustrative, not validated cut-offs"); per-cohort prevalence (61/151, 28/153, 2/44); REML ≤ 15 min now "only 8 of 348" | No sources cited (50-reference ceiling); §5 still "supported more confident threshold decisions"; Fig. 5 caption still "common thresholds" (F-m8) |
| D-6 van Gorp misdescribed | RESOLVED | R-L153 "including against several scorers ... without a coverage guarantee"; verified (Part B-3) | None |
| P-1 no review rule; pooled figure | PARTLY | R-L143 (HMC 59 %), R-L159 ("36 % of nights at 6 h; 41 % in HMC") | No width-based review rule; no per-1,000 table; abstract figure is pooled and not labelled so (F-m9) |
| P-2 raw-plug-in baseline | RESOLVED | R-L143, Abstract, S8 table | Fig. 5e-h still shows only the raw dotted line (caption accurate) |
| P-3 20-night evidence confounded | RESOLVED | R-L137, S17 (Beta-binomial theory; ST statement removed) | No Monte-Carlo SEs; no tolerance table. Minor |
| P-4 no post-deployment monitoring | PARTLY | R-L159 (periodic check of realised coverage on a rolling sample; reason: equipment, montage or population change) | No recalibration triggers or label-free drift signals; no pseudo-prospective demonstration |
| P-5 how to read a 90 % interval | PARTLY | R-L159 ("not a probability statement about a single night", averaged, one scorer); R-L44 | Fig. 1 caption unchanged (histogram not labelled "uncalibrated"); multiplicity over eight parameters not mentioned |
| P-6 headline stronger than results; widths missing | PARTLY | "Valid" qualified (Highlight, Abstract); half-widths in R-L127 | Abstract still gives no absolute width; no sentence on which parameters are narrow enough to support decisions |
| P-7 who is covered | PARTLY (weak) | R-L161(iv) (adult, two rule sets, no HMC demographics) | No intended-use statement; hardest quartile not characterised; home, wearable, paediatric and disease cohorts not named |
| P-8 simulated artefacts | DECLINED (needs new experiments; disclosed) | R-L161(iv) "simulated artefacts were not matched to real recording failures" | §2.7 does not state that EEG and EOG artefacts are independent and stage-independent; no signal-quality-gate advice; R-L146 keeps "because their width responded to the corrupted signal" |
| DA-1 (CRITICAL) TST = recalibration, not posterior sampling | RESOLVED | Title de-emphasises the sampling ("conformal calibration versus limits of agreement"); Highlight R-L23; Abstract R-L33/R-L35; R-L127; R-L151; S1 item 17; cover letter | Wording of "largely" (F-M2) |
| DA-2 "valid per-night" | RESOLVED | R-L22, R-L35, R-L161(i) (84 % in widest HMC tercile, recomputed 84.3 %) | §5 (F-M1) |
| DA-3 forking paths | PARTLY | Abstract now reports the joint criterion (5/24, 2/24); post-hoc additions flagged in R-L91, R-L105, R-L125; S1 | Family size not stated; TST gain not labelled post hoc in the abstract |
| DA-4 simpler alternatives | PARTLY | Entropy-scale and calibrated-centre comparators in R-L125; R-L157 | Regression-based LoA not conformalised; R-L155 still argues from their under-coverage; best simple configuration not named |
| DA-5 clinical gain modest | PARTLY | Recalibrated constant-width comparator in R-L143; Abstract | No downstream clinical endpoint (AHI/REI) and not named as a limitation |
| DA-6 "any stager" | PARTLY | R-L153 and R-L161(iv) qualified | R-L50, R-L62, R-L77 and cover letter L12 unqualified (F-m6) |
| DA-7 transport/usability | PARTLY | Theory beside observed risk; ST n_t = 30 statement dropped | "No temporal or scorer-drift validation; 'local' = random subjects from the same archive" not stated |

**Honesty of the intended choices.** Disclosure is adequate. (i) Items needing new data are stated: single scorer (R-L35, R-L161(iii)), no deep-learning stager (R-L161(iv)), simulated artefacts (R-L161(iv)). The F4-C4 montage point is only implicit (the cross-cohort differences are described as "confounded"). (ii) M-4 is disclosed in one clause in Methods (R-L108); it should also appear in Limitations. (iii) M-3's plain-split run is reported as a range with no purpose statement and no mention that CV+ was not run; neither is dishonest, but both belong in §2.7. Claims stronger than the evidence remain only where listed under F-M1 to F-M4 (§5, "largely recalibration").

---

## Part B. Integrity delta (Stage 4.5)

### B.1 Recomputed vs reported (all new or changed quantities)

| # | Item | Recomputed (source) | Reported (R-L) | Result |
|---|---|---|---|---|
| 1 | TST < 6 h, YASA, pooled, `norm_reg_ffbs`: decided / accuracy / recal. plug-in acc. all, decided, undecided / raw acc. | 0.6394 / 0.9870 / 0.9132, 0.9870, 0.7822 / 0.8420 (`e12_nights_yasa`) | 64 %, 98.7 %, 91.3 %, 98.7 %, 78 %, 84.2 % (R-L33, R-L143) | PASS |
| 2 | Same, `scp_abs_cal`, `scp_signed`, `ba_loa` (pooled) | 0.5475 / 0.9848; 0.6042 / 0.9830; 0.5386 / 0.9773 | 55 % (98.5 %); 60 % (98.3 %); 54 % (97.7 %) | PASS |
| 3 | HMC decided fraction: proposed; distribution-free; `scp_abs_cal` | 0.5917; 0.5685; 0.5040 | 59 %; 57 % (R-L143); 41 % reviewed = 1 - 0.5917 (R-L159) | PASS |
| 4 | Positive nights TST < 360: HMC, SC, ST; REML ≤ 15 | 61/151, 28/153, 2/44 (prev 0.2637 pooled); REML 5 + 3 + 0 = 8 of 347 evaluable | R-L143 identical; "8 of 348 nights" | PASS (note F-m12) |
| 5 | Median TST half-widths `norm_reg_ffbs` vs `scp_abs_cal` | HMC 44.16 vs 52.75; ST 19.27 vs 19.25 | 44 vs 53; 19 vs 19 (R-L127) | PASS |
| 6 | TST coverage by width tercile, HMC (narrow / mid / wide) | 0.957 / 0.938 / 0.843 | "84 %" widest tercile (R-L161(i)) | PASS |
| 7 | `e16_local_risk_theory.csv` `theory_p_lt80`, Beta(n+1-l, l) with l = floor(0.1(n+1)), Beta-binomial over median n_test | HMC 0.1100, 0.0769, 0.0559; ST 0.1404, 0.1395, 0.1753 (all 12 rows identical to CSV and JSON to 5 dp) | 11, 8, 6 % (R-L137); ST n_test 14-34 | PASS. Wording defect F-M4 (test noise alone = 4.8 / 8.5 / 15.8 % at 34 / 24 / 14 nights) |
| 8 | Plain-split YASA `norm_reg_ffbs`: coverage range; within ±3 pp; median width ratio | 0.8736-0.9309; 23 of 24; 1.063 (50 reps; LightGBM 0.8718-0.9307, 23/24, 1.066) | 87.4-93.1 %; 23 of 24; 6 % (R-L122) | PASS |
| 9 | `conj_*` (lower IS, Holm p < 0.05, Spearman CI > 0): YASA / LightGBM | ba_loa 5 / 2; scp_signed 6 / 3; scp_abs_cal 5 / 3; scp_abs_bc 4 / 2; SCALE@FFBS mean 12 / 10 (of 24) | 5 and 2; 12 and 10 (R-L33, R-L125, R-L155) | PASS |
| 10 | `e15_paired.csv` TST ratios | vs `scp_signed` YASA 0.64 / 0.73 / 0.86; LightGBM 0.66 / 0.79 / 0.65; vs `ba_reg` 0.61-0.89, Holm-significant 3 of 6; vs `ba_loa` 5 of 6; vs `scp_abs_cal` YASA 0.86 SC, 0.84 HMC, 1.18 ST (p_holm 1.000) | 0.64-0.86; 0.65-0.79 (all Holm p < 0.05); 0.61-0.89 (3 of 6); 5 of 6; 0.84-1.18 | PASS |
| 11 | Fixed-centre scale counts; Spearman counts | 21 / 23 lower, 15 / 15 significant, 0 significantly worse, mean 0.92; DF lower 15 / 15; noTST mean 1.07 / 0.98; Spearman 30 / 48, TST 6, WASO 1, N2 % 2, N1 % 6 | R-L125, R-L127, R-L146, R-L155 | PASS |
| 12 | Decomposition of TST gain over distribution-free limits attributable to recalibration (log-ratio scale) | SC ≈ 0 % (0.862 vs 0.861), HMC ≈ 44 % (0.726 → 0.836), ST > 100 % (0.640 → 1.179) | "largely" (R-L23, R-L33, R-L35); "much of the TST gain" (R-L127) | FAIL as worded (F-M2) |
| 13 | van Gorp et al. JBHI, DOI 10.1109/JBHI.2023.3304010 (PubMed 37561616 abstract, DOI matches) | "hold-out test set of 70 subjects, each scored by six independent scorers ... outperforms the other methods in modeling the inter-rater disagreement of overnight sleep statistics". ICASSP abstract (OpenAlex) mentions only majority-voted hypnograms | "including against several scorers [23, 24], without a coverage guarantee" (R-L153) | PASS. Support rests on [24]; note only |
| 14 | WASO definition vs `code/src/evaluation/sleep_params.py` | WASO = wake epochs between first and last sleep epoch (L8, L47-52) | R-L59 "wake between sleep onset and the final sleep epoch" | PASS |
| 15 | Supplement: S1 items 16-17; S8 added table; S17 tables | Items 16-17 in `DEVIATIONS.md`, `Supplementary_Material.md` and DOCX (paragraphs 55-56). S8 table: 40 rows (2 stagers × 4 cohorts × 5 methods); S17: 96 plain-split rows + 12 theory rows. DOCX cell values equal the CSVs (max abs diff 0) | S1 items 16-17; S8; S17 as cited in R-L122, R-L137, R-L143 | PASS. S16 is not cited in the main text (pre-existing) |
| 16 | Format limits | Abstract 293 words (four labels counted; 294 with the "Abstract" heading). Highlights 83, 74, 76, 76, 81 characters. Main text: build convention 4,979 (headings and citations counted, equations excluded); python-docx tokens Introduction → Conclusion incl. headings 4,955. References 50. Display items 3 tables + 5 figures = 8. Keywords 6 | ≤ 300; ≤ 85; ≤ 5,000; ≤ 50; ≤ 8 | PASS (headroom 21-45 words; 51 equations are not counted, F-n3) |
| 17 | Citations | 50 keys cited = 50 printed (first-appearance order monotone 1-50); 0 dangling; `rohrscheib2026` in `references.json` is not cited and not printed | — | PASS (note) |
| 18 | "pre-registered" / "valid" / "any stager" / "say nothing about individual nights" | See B.2 | — | See B.2 |

### B.2 Findings: leftover wording and placeholders

**Phrase sweep (all deliverables: rendered manuscript, DOCX, PDF text, supplement, cover letter)**

| Phrase | Result |
|---|---|
| "pre-registered" | None in manuscript, supplement, cover letter or code |
| "say nothing about individual nights" | Removed from manuscript. Equivalent framing remains in the cover letter (F-m7) |
| "valid" unqualified | Abstract R-L35 and Highlight R-L22 now qualified. Acceptable in-context uses: R-L50 (research question), R-L88, R-L119, R-L161(ii), Table 2 caption. Replace R-L166 "Validity did not transfer" and R-L146 "remained valid" with "Coverage" / "kept nominal coverage". §5 otherwise unqualified (F-M1) |
| "any stager" unqualified | R-L50, R-L62, R-L77, cover letter L12 (F-m6). Qualified at R-L153 |

**Placeholders remaining (identical in `Final_Manuscript.docx` and the PDF text; the intentionally open items)**

1. Authors line: `[Second author name]` (R-L7; also CRediT R-L175).
2. Affiliation a: `[Affiliation, address, country]` (first author) and affiliation b `[Affiliation, address, country]` (second author) (R-L9, R-L11).
3. Corresponding author: `[address, e-mail]` (R-L13).
4. CRediT: `[Second author name]: [roles to be completed].` (R-L175).
5. Cover letter (`.md` and `.docx`): signature block `[Affiliation, address]` and `[E-mail]`; the letter says "All authors have approved the submission" while the second author is unnamed; date line is the fixed "20 November 2026".

Nothing else: no `{{ }}`, TODO or `<<` markers in the three DOCX files or the PDF text. The bracketed `[0.10, 1.50]` and `[lights-off, ...]` in the supplement are interval notation. DOCX core properties carry no author or tool metadata.

### B.3 Open issues, sorted by severity, with fixes

**SERIOUS: none.**

**MEDIUM (4)**

**F-M1. §5 Conclusion (R-L166) was not revised and is stronger than the revised abstract.** Unchanged since commit `c50e13a`. It has no "marginal / averaged / one scorer"; it states the TST advantage without the recalibration qualifier; it says the intervals "supported more confident threshold decisions" without naming the comparators (at equal accuracy to the recalibrated plug-in on the same nights); "Validity" is unqualified. S1 item 17 says the conclusions were revised. Fix: replace §5 with (99 words, +18):

> Conformally calibrated posterior hypnogram samples give per-night intervals for automatically scored sleep parameters whose coverage, averaged over nights and relative to one scorer, reached its nominal level within cohorts. Their advantage over limits of agreement is parameter-specific: for total sleep time it was partly due to recalibration of the stager (none in SC, about half in HMC, all in ST), and for most other parameters it was absent. Coverage did not transfer reliably between cohorts or hold at every site, so error statements for automatic scoring should be calibrated on locally scored nights, preferably at least 20, and monitored.

**F-M2. "Largely through (local) recalibration" is not supported for SC and HMC (R-L23 Highlight 3, R-L33, R-L35, R-L127).** Recomputed shares: recalibration explains ≈ 0 % of the TST gain over distribution-free limits in SC (0.86 against both), ≈ 44 % in HMC, > 100 % in ST (1.18, reversed). The tabulated ratios are right; the verb is not. Fixes (abstract stays ≤ 300: 293 → 298 words; Highlight 80 characters):
- Highlight 3: "TST intervals beat limits of agreement; recalibration explains part of the gain."
- Abstract Results: replace "largely through recalibration (versus a constant width around the recalibrated plug-in 0.84–1.18)" with "partly through recalibration (versus a constant width around the recalibrated plug-in: 0.86 SC, 0.84 HMC, 1.18 ST)".
- Abstract Conclusions: "largely reflects recalibration" → "partly reflects recalibration".
- R-L127: "Much of the TST gain came from recalibration: against a constant width ..." → "Recalibration explained none of the TST gain in SC, about half in HMC and all of it in ST: against a constant width ...".

**F-M3. Width cost of local calibration was deleted from §3.5, but §2.7 (R-L99) says width is reported.** The previous draft stated that HMC intervals with ten nights were 29 % wider than with the full calibration half (key `h_loc_widthratio_yasa_HMC_10` still exists; mean TST width 132 min at n = 10, 107 at n = 20, 91 in Table 2). J-1(b) asked for exactly this. Coverage of 92.0 % at n = 10 is partly bought with width. Fix: re-insert after "... and with 30 nights still in 7 % and 15 %." (25 words): "With ten nights, intervals on HMC were {{(h_loc_widthratio_yasa_HMC_10-1)*100:.0f}} % wider than with the full calibration half of about 75 nights (median over parameters; Supplementary S6)."

**F-M4. R-L137 misattributes the ST theoretical risk.** "in ST only 14-34 test nights remained, which alone gives 14-18 %": 14-18 % is the full Beta-binomial theory (calibration-set risk plus test noise). Test-set size alone at 90 % true coverage gives 4.8, 8.5 and 15.8 % for 34, 24 and 14 nights. Fix: "...; in ST only {{r_risk_yasa_ST_30_ntest}}-{{r_risk_yasa_ST_10_ntest}} test nights remained, so theory, which adds the binomial noise of a small test set to the calibration-set risk, already gives {{...}}-{{...}} %."

**MINOR (15)**

- **F-m1.** R-L120: "where two nights per subject and 22 calibration nights violate the exchangeability" (22 nights do not violate exchangeability; clustering does). Replace with "where two nights per subject violate the exchangeability these limits assume and 22 calibration nights from 11 subjects leave the extreme quantiles unstable".
- **F-m2.** "exact" without qualification: Table 2 caption (R-L231) and S1 item 10 ("exactly valid"). Use "split-conformal limits from signed residuals of the plug-in (exact for exchangeable nights)".
- **F-m3.** R-L88 "the one later change, the definition of σ̄" is inconsistent with S1 item 1 (τ grid extended). The main text does not carry S1's caveat that the repository cannot date the protocol, and the cover letter repeats "before any interval was computed". Replace the end of R-L88 with "...written before any interval was computed (the repository history cannot date it independently); later changes to the method, an extended search range for τ and the definition of σ̄, are documented in Supplementary S1". Cover letter: add "according to the authors' records".
- **F-m4.** The plain-split sensitivity analysis is not introduced in Methods (first appears R-L122). Add to §2.7 (≈ 17 words): "A plain split-conformal sensitivity analysis (calibration subjects halved; exact for exchangeable nights; Supplementary S17) was also run."
- **F-m5.** Dangling "Mondrian" in R-L95 (the Mondrian methods and results sentences were removed; it remains in S1 item 5 and S5). Delete ", Mondrian,".
- **F-m6.** "any stager" unqualified: R-L50 → "implemented post hoc, through a hidden Markov model, for stagers that output epoch probabilities"; R-L62 → "of a stager that outputs them"; R-L77 → "a post-hoc analogue for stagers that output epoch probabilities"; cover letter L12 "any automatic stager" → "an automatic stager (here YASA and a feature-based in-domain model)".
- **F-m7.** Cover letter leftovers of D-1 and J-3: "These summaries do not tell a clinician how reliable the parameters of the night in front of them are" → "These summaries give every night the same error range, however easy or difficult it was to score"; bullet 1 "reach their nominal coverage within cohorts" → "reach their nominal marginal coverage within cohorts, relative to a single scorer".
- **F-m8.** Fig. 5 caption "(e-h) Decisions at common thresholds" → "at illustrative thresholds" (R-L143 calls them illustrative).
- **F-m9.** Abstract: "intervals decided 64 % of nights" is pooled (ST contributes 93 % decided, prevalence 4.5 %); HMC is 59 % against 50 % for the recalibrated constant width. Add "(pooled)" (+1 word; abstract 299).
- **F-m10.** R-L161(vi) "led to the same qualitative conclusions": in S9, TST vs distribution-free limits is Holm-significant in 4 of 6 stager-cohort combinations (YASA-HMC p_holm 1.00; LightGBM-SC 0.084). Add "(direction unchanged; the TST advantage over distribution-free limits was significant in 4 of 6 combinations)".
- **F-m11.** M-4 caveat only in Methods. Add to Limitations: "interval-score p-values ignore calibration-set variability and are descriptive".
- **F-m12.** The literal "348" in R-L143 (also R-L50, R-L161): replace by `{{nights_total}}`. REML is defined for 347 nights (one HMC night lacks reference REM), so "8 of 348" is true but not the evaluable denominator.
- **F-m13.** D-2: R-L135 should add "(frontal versus central referential derivations; the bipolar Fpz-Cz derivation of SC and ST could not be tested on HMC)".
- **F-m14.** "internal review" (R-L161(vi); S1 header "internal critical review", item 16 "second internal review") denotes AI-run reviewer panels. The declaration (R-L171, R-L111) lists only literature search, code and drafting. Add to the declaration: "and to run simulated peer-review rounds whose reports guided revisions" (outside the word count), and "AI-assisted internal review" at R-L161.
- **F-m15.** Pre-existing code note: module docstring of `code/src/evaluation/sleep_params.py` (L2-3) says unscored reference epochs are "excluded everywhere", contradicting R-L59 and S1 item 9 (they are counted as wake; the code in `night_summary.py` does this).

**Notes (not issues)**

- F-n1. "The authors verified the content" (R-L111, R-L171) is an attestation by the human author; not verifiable here (UNVERIFIABLE_ACCESS).
- F-n2. `references.json` retains uncited `rohrscheib2026` (not printed). S16 is not cited in the main text.
- F-n3. Word-count headroom is 21 words (build convention 4,979) or 45 (python-docx 4,955). The 51 equations are excluded under both conventions; a counter that includes them (about +51 to +266) would exceed 5,000. The edits above add ≈ +71 words in the main text (F-M1 +18, F-M2 +11, F-M3 +25, F-m4 +17). Offsetting cuts of ≈ 50 words: the cost sentence at the end of §3.8 (24 words; the data are in S15) and the sentence on non-calibrated posterior percentile intervals' coverage in §3.2 (≈ 30 words) are candidates, or the authors' choice. The abstract has 1 word of headroom after F-M2 and F-m9 (293 + 5 + 1 = 299 of 300).
- F-n4. ICASSP abstract does not mention multiple scorers; the claim rests on the JBHI paper.
- F-n5. Verified, no action: all `r_*`/`conj_*` values, the S17/S8 supplement tables, the ratios in the abstract and §3.3, and the WASO definition.

## Reproducibility of this check

All recomputations: `results/raw/e12_nights_yasa.csv.gz` (setting = within), `results/raw/e16_plainsplit_{yasa,lgbm_sc_s0}.csv.gz`, `results/raw/e12_honest_*.csv.gz`, `results/statistics/{e15_paired,e13_spearman,e15_local,e16_*,e07_paired_tests_*}.csv`, `tables/manuscript_numbers.json`. Beta-binomial and binomial tails were computed with `math.lgamma`/`math.comb` (scipy is not installed). External check: PubMed efetch PMID 37561616 (van Gorp JBHI abstract); OpenAlex abstract for the ICASSP record; Crossref carries no abstract for either DOI. No tracked file was modified and nothing was committed.
