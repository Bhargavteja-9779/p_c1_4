## Journal-Fit Review Report

ARS `academic-paper-reviewer`, Phase 1 (Reviewer Panel), Stage 3 of pipeline run `ars-p_c1_4-2026-11-20-a`. Seat: Journal-Fit Reviewer (`eic`, Card #1). Standard-mode report (no sprint contract supplied). Criteria binding: `criteria_binding_unavailable`. Venue-limit checks below are made against the author-stated limits in `journal_selection/selected_journal.md` and are not a bound venue-alignment claim.

This report was written without opening any other Stage 3 reviewer output. The only file opened in `stage3_review/` before writing was `phase0_field_analysis.md`. `stage2_5_integrity/reverification_round1.md` was consulted only after the findings below had been drafted, to avoid repeating items it records as resolved.

### Reviewer Identity
Senior Associate Editor of *Sleep Medicine* who handles submissions on automated scoring, device and wearable validation and other sleep-technology work. A sleep physician by training, formerly medical director of an accredited clinical polysomnography laboratory. Judges whether a methods paper gives the journal's clinical readership a usable takeaway.

### Overall Recommendation
Major Revision

### Confidence Score
4. High confidence on journal fit, clinical value and claim–evidence match. I did not check the conformal-validity argument, the resampling design or the HMM/FFBS construction (Card #1 blind spots; Reviewer 1's remit).

Confidence is an uncertainty/scope disclosure only; it never changes consensus counts, severity, decision bearing, or arbitration.

### Calibration Status
`NOT_CALIBRATED`

### Criterion-Bound Judgements
| Dimension / criterion | Criterion source | Judgement | Evidence anchors | Rationale | Uncertainty or scope limit | Decision bearing? |
|---|---|---|---|---|---|---|
| Scope fit | *Sleep Medicine* scope ("new diagnostic and therapeutic technologies"), per `selected_journal.md`; Card #1 | MEETS | text: L42 "Validation studies therefore summarise algorithm–scorer agreement for these parameters with Bland–Altman bias and limits of agreement" | The paper works on the night-level parameters and agreement statistics this journal's validation papers report. Refs [6], [7] and [9] are *Sleep Medicine* validation papers. | Live author guide not checked (the authors' own notes say it returned 403) | no |
| Clinical problem stated in clinician terms (Card #1 focus 1) | Card #1 | MEETS | text: L44 "which would show when a night can be signed off and when it needs manual review" | The sign-off / re-score decision is named in §1 ¶2, and the payoff is given in minutes of TST | — | no |
| Clinical payoff demonstrated (Card #1 focus 1–2) | Card #1; Original Article expectation of a usable practice message | PARTLY_MEETS | J-1, J-2, J-4 | The decision benefit over limits of agreement is small. It is shown only under ~75-night calibration and measured against the uncorrected plug-in. Part of the TST gain comes from recalibration rather than from the intervals. | Decision analysis read from `e15_decisions.csv` and Fig. 5e only | yes: drives the Major recommendation |
| Originality | Universal dimension (quality_rubrics D1) | MEETS | text: L153 "The present procedure calibrates it, in the units clinicians use and for any stager" | My PubMed search (2026-11-21: `conformal[tiab] AND sleep[tiab] AND (staging OR scoring OR polysomnograph*)`, 6 hits) found no prior conformal per-night interval for sleep parameters. The closest work (van Gorp 2023; ConMIL 2025) is cited. | PubMed only; arXiv, IEEE Xplore and medRxiv not searched | no |
| Claim–evidence match: title, highlights, abstract, conclusion (Card #1 focus 3) | Card #1 | PARTLY_MEETS | J-3, J-4 | The numbers match the Results. "Valid" is unqualified in the Abstract Conclusions, Highlight 2 and §5. The 20-night recommendation is not backed by a reported n = 20 result. The supplement title matches the manuscript title (Supplementary_Material.md L5). | — | yes |
| Generalisability to the clinical readership | Universal dimension D7; Card #1 "will particularly care about" | PARTLY_MEETS | J-5 | One clinical cohort with no demographics; single scorer; feature-based stagers only | — | yes |
| Format limits (Card #1 focus 4) | Author-stated limits | MEETS (no headroom) | J-9 | Main text 4,965 (stated). My whitespace count of L40–166 is 4,860 without citation keys and TeX, 5,071 with them. Abstract 293 (stated), my count 289. References 50/50. Display items 8/8. Highlights 76–82 characters. | The count depends on the counting convention; Word's counter was not available | no (it becomes bearing once revision adds text) |
| Declarations (Card #1 focus 4–5) | Elsevier GenAI policy (as of the Aug 2026 update, per search result); Card #1 | PARTLY_MEETS | J-8, J-11 | The AI declaration heading and the Methods description do not follow the updated policy's wording and version requirement. The ethics statement has no institutional determination. | Policy content verified from search-result text, not from the full page | no |
| Revision provenance readable by journal readers (Card #1 focus 5) | Card #1 | PARTLY_MEETS | J-6, J-7 | "during review" remains at L91. The L88 sentence "the one later change" understates the 15-item deviation log. | — | no |

### Summary Assessment
The manuscript turns the epoch probabilities of an automatic stager into per-night 90 % intervals for eight clinical sleep parameters. It does so by sampling hypnograms from an HMM posterior and calibrating their spread conformally, and it compares the result with three forms of limits of agreement on three public cohorts (348 nights). The question fits *Sleep Medicine*: the journal publishes validation papers that report population limits of agreement, and the authors ask what a clinician should believe about tonight's TST. The paper is unusually candid. It reports that the advantage is confined to TST, that WASO intervals are worse in 10-h ambulatory windows, that calibration does not transfer across cohorts, and that sites calibrated on few nights carry a real risk of under-coverage.

The editorial problem is clinical value. The supporting evidence (Table 2, Fig. 5e) shows a TST benefit that is real but modest. Part of it comes from local probability recalibration, which needs no intervals. It was demonstrated with roughly 75 calibration nights per cohort, whereas the recommended deployment uses 10–20 nights, where TST intervals are about 107–132 min wide in HMC. The practice message ("report TST with a per-night interval; ≥ 20 local nights") is therefore stated more firmly than the evidence allows. "Valid" is used in a stronger sense than the empirical, marginal coverage supports. The clinical evidence base is one clinical cohort scored by one scorer. All of this can be fixed, mostly from results already in the repository, but it needs a substantive rewrite of the framing and a few re-analyses. Major Revision.

### Strengths
1. **S1 Honest, parameter-specific scoping of the claim.** The Abstract, Discussion and Conclusion state where the method fails (WASO in long recordings, most non-TST parameters, cross-cohort transfer) rather than burying it. Clinical editors rarely see this in sleep-AI submissions.
   - **Evidence Anchor**: text: L35 "Their advantage over LoA is parameter-specific (clear for TST, absent for most others), and validity requires local calibration."
2. **S2 Comparators that clinicians recognise, run on equal terms.** Parametric, regression-based and distribution-free limits of agreement use the same calibration nights. A proper scoring rule (interval score) and subject-level inference let the comparison speak directly to how validation is reported in this journal.
   - **Evidence Anchor**: table: Table 2 (L231–258)
3. **S3 Site-level deployment risk reported, not only mean coverage.** The probability that a site's realised coverage falls below 80 % is reported along with mean coverage, the quantity a laboratory director actually needs. I have seen this rarely in sleep-scoring validation.
   - **Evidence Anchor**: text: L137 "the realised coverage of the remaining nights fell below 80 % in 9 % (HMC) and 17 % (ST) of repetitions"
4. **S4 Verifiable novelty in the sleep literature.** Per-night, calibrated intervals in clinical units are new relative to epoch-level uncertainty, scorability models and uncalibrated posterior sampling. My PubMed check (above) found no competing per-night conformal work.
   - **Evidence Anchor**: text: §4 "Relation to previous work" (L153) "Posterior sampling of whole hypnograms has been used to describe the uncertainty of overnight statistics"
5. **S5 Open data, a full deviation log and a regenerating pipeline.** Public PhysioNet data, a pipeline that regenerates every number, and a 15-item deviation log make the paper auditable.
   - **Evidence Anchor**: text: L111 "A pipeline regenerates the results, tables and figures from the public data"
6. **S6 Mechanistic explanation of a failure.** The WASO failure is traced to the 10-h SC window: one spurious late sleep epoch moves the final awakening. This gives clinicians a usable rule: per-night uncertainty is meaningful only for parameters that are stable to isolated epoch errors.
   - **Evidence Anchor**: text: L157 "per-night uncertainty is only meaningful for parameters that are stable to isolated epoch errors"

### Weaknesses

#### J-1: The clinical decision benefit is small, is shown only under large calibration sets, and is benchmarked against the uncorrected plug-in
- **Location**: Abstract Results (L33, last sentence); §3.7 (L143); Fig. 5e–h (L299); §4 "Implications for practice" (L159).
- **Problem**: The clinical payoff the paper offers is threshold decisions at TST < 6 h. Three things weaken it.
  - **(a) The margin over limits of agreement is small.** The proposed intervals decide 64 % of nights against 60 % for distribution-free limits and 54 % for Bland–Altman limits, at similar accuracy (98.7 %, 98.3 %, 97.7 %). Fig. 5e shows the methods nearly overlapping.
  - **(b) The analysis uses the wrong calibration size.** It uses the within-cohort protocol with about 75 calibration nights per cohort (Fig. 5 caption: "Table 2 protocol"), not the 10–20 local nights the paper recommends. With 10 local nights the mean TST interval in HMC is 132 min wide, and 107 min with 20 (`results/statistics/e15_local.csv`, `norm_reg_ffbs`, YASA), against 91 min in Table 2. Readers are not told how many nights would be decided under the recommended deployment.
  - **(c) The benchmark is the wrong one.** The dotted line in Fig. 5e–h and the "84.2 %" all-nights figure are for the uncorrected automatic TST. The paper's own practice step (ii) is to recalibrate the probabilities. The clinically relevant comparison is therefore the calibrated plug-in classifying every night, against intervals plus manual review of the undecided nights.
- **Why it matters for acceptance**: Every clinical reader and the handling editor will ask "what does this change in my lab?" As written, the honest answer is "slightly more nights auto-decided, under conditions you will not have". That makes the paper look like a technical contribution, the main desk-rejection risk the authors themselves list (`selected_journal.md`, "KEY REJECTION RISKS" 1).
- **Fix**: (1) Re-run the TST < 6 h decision analysis inside the local-deployment runs (n_t = 10, 20, 30; ST and HMC). If the per-night intervals of the e15 local runs are not stored, re-run e15 from the stored stager probabilities. (2) Add the calibrated plug-in (all nights) as the benchmark line, and report accuracy of the plug-in on undecided nights next to it. (3) Express the result as a workload trade-off: per 100 nights, how many are signed off automatically, with how many expected misclassifications, and how many go to manual review, compared with LoA and with the calibrated plug-in alone. This can replace part of Fig. 5 (see J-13) without adding a display item.
- **Flag**: [FIXABLE-IN-REPO]
- **Severity**: Major | **Evidence Anchor**: text: L143 "classifying every night by its plug-in TST was correct for 84.2 %" | **Confidence**: 4 — numbers read from `e15_decisions.csv`, `e15_local.csv` and Fig. 5; clinical-utility judgement within my competence

#### J-2: Part of the headline TST advantage comes from local recalibration, which a laboratory can get without the interval method; the main text does not show this for TST
- **Location**: §3.3 "Comparison with limits of agreement" (L127); Table 2 (L231–258); §4 ¶1 (L151); §4 "Implications for practice" (L159); Highlight 3 (L23).
- **Problem**: The TST claim ("lower interval score than every LoA variant in every cohort") compares the proposed interval, centred on recalibrated probabilities, with limits of agreement built around the raw plug-in. The authors' own factorial separates the two effects. The constant-width conformal interval around the *calibrated* plug-in is `scp_abs_cal` in `results/statistics/e15_paired.csv` (YASA, TST). Against it, the proposed interval's IS ratio is 0.86 in SC and 0.84 in HMC, and **1.18 in ST (95 % CI 0.97–1.37; proposed worse, not significant)**. Against distribution-free LoA the ratios are 0.86, 0.73 and 0.64. So in ST essentially all of the TST gain, and in HMC about half, comes from recalibration (Table 3: ST TST MAE 22.6 → 7.5 min). Section 3.3 reports the fixed-centre comparison only as counts over 24 combinations. Fig. 2 plots "Constant (calibrated centre)", but the text never says that for TST in ST the simpler calibrated constant-width interval was at least as good.
- **Why it matters for acceptance**: The practice message, "report TST with a per-night interval", should rest on the simplest procedure that delivers the benefit. If "recalibrate on local nights, then use limits of agreement around the calibrated value" captures most of it, editors and clinical reviewers will see the FFBS/HMM layer as added complexity with a 14–16 % efficiency gain in two of three cohorts. That gain is worth reporting, but it is not the headline the abstract implies.
- **Fix**: Add the calibrated-centre constant-width comparator as a column in Table 2 (or a TST row block). State in §3.3, the Abstract Results and §4 how much of the TST gain is attributable to recalibration and how much to the adaptive scale, per cohort, including ST. Rephrase Highlight 3 and §4 step (iii) to match. If it holds, the honest message is "recalibrate first; per-night scaling adds a further ~15 % for TST in two of three cohorts". Clinicians can use that.
- **Flag**: [FIXABLE-IN-REPO]
- **Severity**: Major | **Evidence Anchor**: dataset: results/statistics/e15_paired.csv, rows yasa,{SC,ST,HMC},TST,scp_abs_cal (ratios 0.861, 1.179, 0.836) | **Confidence**: 4 — read directly from the authors' output file; I did not re-run the test

#### J-3: "Valid" is used without qualification for a property that is empirical, marginal and not reliable at the site level
- **Location**: Abstract Conclusions (L35); Highlight 2 (L22); §5 (L166); compare §2.5 (L88), §3.2 (L120–122), §3.5 (L137), §4 Limitations (i) (L161).
- **Problem**: The Methods state correctly that the main design has no distribution-free guarantee, so validity is empirical, and that coverage is marginal. The hardest quartile is covered at about 85 %, and with 10 local nights 9–17 % of sites fall below 80 % realised coverage. Yet the Abstract Conclusions say "Locally calibrated conformal intervals give valid per-night error ranges", and Highlight 2 says "gave valid per-night 90 % intervals". Clinical readers take "valid per-night" to mean "this night's interval contains the truth 90 % of the time", which is the conditional reading the paper itself rules out.
- **Why it matters for acceptance**: The abstract and highlights are what clinicians read and what decision-support vendors quote. Overstated guarantees in a clinical journal are a standard reason for referee objections and for post-publication criticism, and Reviewer 1 will test this exact wording.
- **Fix**: Replace "valid" in the Abstract Conclusions, Highlight 2 and §5 with a precise statement: "reached nominal average (marginal) coverage within cohorts", with "lower on the hardest nights" and "not guaranteed at every site with few calibration nights" in the abstract. One clause each; the word budget allows it if J-9 cuts are made.
- **Flag**: [FIXABLE-IN-REPO]
- **Severity**: Major | **Evidence Anchor**: text: L35 "Locally calibrated conformal intervals give valid per-night error ranges for automatic sleep parameters." | **Confidence**: 4 — wording judgement; the statistical status is taken from the authors' own §2.5

#### J-4: The "at least 20 local nights" recommendation is not backed by a reported n = 20 result and does not remove the site-level risk it is meant to address
- **Location**: §4 "Implications for practice" (L159); §5 (L166); §3.5 (L137); Fig. 3c, f (L295).
- **Problem**: The text reports site-level risk at 10 nights (9 % HMC, 17 % ST) and 30 nights (7 %, 15 %), then recommends 20. The repository gives the n = 20 values (`e15_local.csv`, `norm_reg_ffbs`, YASA): median over parameters 7 % (HMC) and 15 % (ST), maximum 10 % and 20 %. These are the same as at 30 nights. The figure of 20 seems to come mainly from the ≥ 19 nights distribution-free limits need at α = 0.10 (L159), not from the proposed method's risk curve. A laboratory following the recommendation would still face a roughly 1-in-7 chance of under-80 % coverage in an ST-like setting, and the paper gives no procedure for detecting it (no post-deployment monitoring is proposed).
- **Why it matters for acceptance**: The recommended number of nights is the paper's single most quotable clinical recommendation. It must follow from the data shown, and it must say what risk remains.
- **Fix**: Report the n = 20 results in §3.5 and S6. State that the 20-night figure is a minimum driven by the distribution-free comparator, and give the residual risk at 20 nights. Add one sentence on ongoing monitoring: re-score a small rolling sample of nights and check running coverage. If the authors want a firmer number, report the n at which the risk falls below a stated tolerance (the pre-specified n_t grid included 50; S1 L40).
- **Flag**: [FIXABLE-IN-REPO]
- **Severity**: Major | **Evidence Anchor**: text: L159 "We therefore suggest at least 20 locally scored nights (even 30 left a risk of 15 % in the small ST cohort)." | **Confidence**: 4 — values read from `e15_local.csv`

#### J-5: The clinical evidence base is thin for a clinical journal's practice recommendation: one clinical cohort without demographics, single scorers, feature-based stagers only
- **Location**: §2.1 (L56); §2.3 (L62); Table 1 (L210–229); §4 Limitations (iii), (iv) (L161); §1 ¶5 "for any stager" (L50); §4 L153 "for any stager that outputs epoch probabilities".
- **Problem**: Only HMC (151 nights) is a clinical sleep-centre population, and it has no released age, sex or diagnoses. SC is healthy 1989–1994-era home recordings with a 10-h window that produces the WASO failure. ST has 22 subjects. Every night has one scorer, so the intervals cover one scorer's values. Both stagers are feature-based (YASA and a LightGBM model on YASA features). Laboratories mostly run deep-learning or commercial scorers, and many commercial scorers do not export per-epoch probabilities [unverified; general editorial knowledge, not checked against vendor documentation]. The "any stager" and "a laboratory deploying an automatic stager" framing goes beyond this evidence.
- **Why it matters for acceptance**: Clinical referees for *Sleep Medicine* will ask whether the recommendation holds for patients with OSA, insomnia or hypersomnolence, for deep-learning stagers, and against inter-scorer variability. As it stands, only HMC answers any of this.
- **Fix**: Minimum, text only: confine the practice message to "adult clinical PSG similar to HMC", drop "any stager" in favour of "stagers that output epoch probabilities (here, two feature-based stagers)", and state that the clinical deployment pathway needs probability export. Stronger, needs new data: add (a) a multi-scored clinical cohort, so that coverage can be read against scorer disagreement. Examples are the Dreem Open Dataset DOD-O (OSA patients, five scorers; Guillot et al., IEEE TNSRE 2020, doi:10.1109/TNSRE.2020.3011181, verified via Crossref) or ISRUC-Sleep (Khalighi et al., Comput Methods Programs Biomed 2016, doi:10.1016/j.cmpb.2015.10.013, verified via Crossref). Add also (b) one open deep-learning stager that outputs probabilities, e.g. U-Sleep (ref. [4]). Either addition would materially strengthen fit, but it competes with the word and display limits (J-9).
- **Flag**: text tempering [FIXABLE-IN-REPO]; additional cohort or stager [NEEDS-NEW-DATA] (public recordings not in the repository)
- **Severity**: Major | **Evidence Anchor**: text: L161 "The cohorts were moderate in size (348 nights), adult and scored with two rule sets, both stagers were feature-based, and HMC provides no demographics" | **Confidence**: 4 — clinical-population judgement within competence; the vendor-export statement is unverified

#### J-6: The protocol-timing language reads more confirmatory than the record supports
- **Location**: §2.5 last sentence (L88); §2.6 last sentence (L91); §4 Limitations (vi) (L161); cover letter L23; Supplementary S1 L11 and L85.
- **Problem**: L88 says the method, score and α "were fixed in a protocol … written before any interval was computed; the one later change, the definition of σ̄, is documented". S1 records 15 deviations, including a change of the primary analysis after an internal review and comparators and thresholds added after the first results. The phrase "the one later change" is scoped to the method itself, but a journal reader will take it as "one deviation". S1 L85 also concedes that "The repository history cannot date it independently" and that the protocol's precedence "rests on the authors' records". The protocol is dated 2026-11-15 (S1 L11). Many sections are labelled "pre-specified design", which gives that design a confirmatory feel the record cannot establish.
- **Why it matters for acceptance**: It does not change the results, but editors increasingly query pre-specification claims that cannot be verified, and a referee who finds the S1 L85 sentence will discount the paper's confirmatory framing.
- **Fix**: At L88, write "the method, score and α were fixed in an internal, unregistered protocol (S1) before any interval was computed; the primary evaluation design, several comparators and the decision thresholds were changed or added later (S1 items 2–15)." Consider renaming "pre-specified design" to "original (cross-fitted) design". Cover letter L23 should mirror this.
- **Flag**: [FIXABLE-IN-REPO]
- **Severity**: Minor | **Evidence Anchor**: text: L88 "the one later change, the definition of $\bar\sigma$, is documented in Supplementary S1" | **Confidence**: 4 — compared with S1

#### J-7: "during review" and internal pipeline vocabulary remain in reader-facing text
- **Location**: §2.6 L91 ("were added after the first results or during review"); Supplementary headings S2 "Honest end-to-end protocol", S3 "Honest protocol", S16 "(Phases 7–8)".
- **Problem**: A journal reader will take "during review" to mean journal peer review, which suggests an earlier submission. L161 says "internal review", which is clearer. The integrity re-verification lists this item as fixed, but the rendered manuscript still contains it at L91. "Honest" in the supplement headings implies that other analyses are not honest, and "Phases 7–8" is workflow jargon.
- **Fix**: L91: "added after the first results, following an internal review of the first draft". Rename S2/S3 to "End-to-end protocol: …" and drop "(Phases 7–8)".
- **Flag**: [FIXABLE-IN-REPO]
- **Severity**: Minor | **Evidence Anchor**: text: L91 "were added after the first results or during review to separate calibration from adaptivity" | **Confidence**: 5 — direct reading

#### J-8: The generative-AI disclosure does not follow the publisher's current wording and is internally inconsistent
- **Location**: §2.9 (L111); Declaration heading and text (L169–171); cover letter L25.
- **Problem**: Per Elsevier's journal GenAI policy (updated 2026; checked via web search on 2026-11-21, search-result summary only, full page not opened), AI use in the research process is to be described in Methods with the tool's name, version and developer. Writing-process use goes in a separate declaration titled "Declaration of generative AI and AI-assisted technologies in the manuscript preparation process". §2.9 gives "Claude, Anthropic" without a version. The declaration uses the older heading "…in the research and writing process". The three statements also differ in scope: §2.9 "search the literature", the Declaration "search and screen the literature", and the cover letter "used extensively in literature screening, code development, analysis and drafting". For a paper where AI wrote and ran the analysis code, editors will expect precise, consistent wording.
- **Fix**: In §2.9, name the model and version(s) and the dates of use, and list the tasks consistently (literature search and screening, code writing and execution, drafting). State what the human authors verified (e.g. re-ran the pipeline, checked references against sources). Retitle the declaration to the current heading and keep its text to manuscript preparation. Re-check against the live Guide for Authors.
- **Flag**: [FIXABLE-IN-REPO]
- **Severity**: Minor | **Evidence Anchor**: text: L111 "A generative AI system (Claude, Anthropic) was used to search the literature, write and run the analysis code and draft the manuscript" | **Confidence**: 3 — policy content verified only from search-result text

#### J-9: Every format limit is at its ceiling, leaving no room for the revisions above
- **Location**: Title page (L17); main text; reference list (50 entries, PDF pp. ~21–27); Tables 1–3 and Figs. 1–5.
- **Problem**: The stated main text is 4,965/5,000 words; depending on convention it is 4,860–5,071 by my count, and 4,999 math-inclusive per the integrity report. References are 50/50 (the Phase 0 report recorded 49; Pollard 2026 has since been added as [50]). Display items are 8/8 and the abstract is 293/300. Any added comparator column, n = 20 result or cohort will push the paper over a limit.
- **Fix**: Plan the cuts now. Candidates: move Table 3 (point estimates, a secondary question) or Fig. 4 (robustness) to the supplement; compress §2.6 (the comparator list) and §3.8; drop references that support only methodological lineage (e.g. one of [39]–[41] for FFBS; [37]/[38]). State the word-count convention on the title page.
- **Flag**: [FIXABLE-IN-REPO]
- **Severity**: Minor | **Evidence Anchor**: text: L17 "main text 4,965 words; abstract 293 words" | **Confidence**: 4 — own counts; Word's counter not available

#### J-10: The supplement is too large to review and partly machine-formatted
- **Location**: `supplementary/Supplementary_Material.md` (~1.4 MB, ~205,000 words, S2–S14 almost entirely tables).
- **Problem**: Several main-text claims rest only on the supplement: the decision accuracies (S8), the pre-specified analysis "leading to the same qualitative conclusions" (S9) and site-level risk (S6). Referees cannot realistically locate the supporting rows. Machine-generated column names (e.g. `p_cov_lt80`, `scp_abs_cal`) appear without a legend.
- **Fix**: Curate a supplement of about 20–40 pages with the tables that support specific sentences, each cross-referenced from the main text, plus a method-code legend. Deposit the full tables as CSV data files with the code.
- **Flag**: [FIXABLE-IN-REPO]
- **Severity**: Minor | **Evidence Anchor**: absence: Supplementary Material S2–S14 — expected a curated, legend-equipped set of tables cross-referenced to main-text claims; checked S1–S16 headings, S1, S6, S15, S16 and grep for method codes | **Confidence**: 4 — direct inspection

#### J-11: The ethics statement has no determination by the authors' institution
- **Location**: Ethics statement (L185–187).
- **Problem**: The statement documents HMC's original IRB approval and notes that Sleep-EDF approvals are undocumented. It does not say whether the authors' institution judged the secondary analysis exempt. Many Elsevier clinical journals ask for this explicitly. The integrity re-verification notes that the author-action marker for it was removed without a recorded author decision.
- **Fix**: Add one sentence giving the institution's determination (or the regulation under which none is required), to be confirmed by the authors.
- **Flag**: [FIXABLE-IN-REPO] (author attestation)
- **Severity**: Minor | **Evidence Anchor**: text: L187 "The Sleep-EDF Expanded record does not document the approvals obtained by the original studies" | **Confidence**: 3 — journal-specific requirement not checked on the live guide

#### J-12: The title is long and method-led for a clinical readership
- **Location**: Title (L2).
- **Problem**: At 25 words, with "conformal calibration of posterior hypnogram samples", the title signals a statistics paper. The clinical object (an individual night's TST and other parameters) and the main finding (TST-specific benefit) are not visible.
- **Fix**: E.g. "Per-night error ranges for automatically scored sleep parameters: locally calibrated intervals versus limits of agreement". Keep "conformal" in the keywords.
- **Flag**: [FIXABLE-IN-REPO]
- **Severity**: Minor | **Evidence Anchor**: text: L2 "conformal calibration of posterior hypnogram samples compared with limits of agreement" | **Confidence**: 3 — editorial taste

#### J-13: Display space spent on an uninformative threshold, while clinically familiar parameters are missing
- **Location**: §3.7 (L143); Fig. 5h; §2.2 parameter list (L59); cover letter L12 (lists sleep efficiency).
- **Problem**: At REM latency ≤ 15 min the prevalence is 2.5 % and no interval lay entirely below 15 min, so Fig. 5h shows only negative decisions, which is uninformative. Sleep efficiency, which the cover letter itself names as a standard validation parameter, is absent. So is the TST-as-AHI-denominator use, the most common clinical consequence of a TST error in PSG. Both follow directly from the TST interval (SE = TST / time in bed, with a fixed window) and would strengthen the clinical relevance at no extra analysis cost.
- **Fix**: Replace Fig. 5h with the J-1 workload panel, or with sleep efficiency < 85 %. Add one Discussion sentence on propagating the TST interval to SE and AHI.
- **Flag**: [FIXABLE-IN-REPO]
- **Severity**: Minor | **Evidence Anchor**: figure: Fig. 5h (REML ≤ 15 min panel) | **Confidence**: 3 — clinical-relevance judgement

### Detailed Comments

#### Journal Fit
Specific fit: *Sleep Medicine* publishes device and algorithm validation papers that report Bland–Altman agreement for TST, WASO and stage percentages; refs [6], [7] and [9] are from this journal. This manuscript speaks directly to how those papers report error, so the topic is in scope. The writing is clear but dense with statistical vocabulary: interval score, CV+, Mondrian, FFBS, Holm families. §2.4–2.6 and §3.3 will lose the clinical half of the readership. For this venue, the paper should lead with the TST and local-calibration message and move most of the comparator taxonomy to the supplement. Without J-1 to J-4 there is a real desk or referee risk of "technically sound, clinically incremental". If the clinical framing cannot be made convincing, a methods venue such as *Journal of Sleep Research* (methods section), *SLEEP Advances* or *Physiological Measurement* would accept the current framing more readily [suggestion only; scope statements of these journals not verified in this review].

#### Originality
The originality lies in the combination: per-night parameter intervals, conformal calibration against the clinical scorer, a head-to-head comparison with limits of agreement, and a cross-cohort and local-deployment evaluation. The individual components are established: posterior hypnogram sampling (van Gorp 2023, refs [23]–[25]), conformal inference and HMM smoothing. My PubMed check found no prior per-night conformal intervals for sleep parameters. Ref. [20], cited for epoch-level conformal sets, is an LLM/multiple-instance-learning paper. Its abstract (PubMed 41230240) does report conformal set outputs on a sleep-staging task, so the citation is defensible but peripheral. Reviewer 2 is assigned the citation-support check.

#### Significance
If the conclusions hold, the impact is sub-field: validation practice for automatic scoring. The idea of reporting per-night error rather than population limits of agreement could change how validation papers report results, which is timely as autoscoring enters routine PSG review. What the paper actually demonstrates is narrower: a modest gain for TST, partly through recalibration (J-2), and local calibration as a requirement. The recalibration finding (Table 3; TST bias reduced from −38 to −5 min in HMC with ten local nights) may be the most immediately actionable clinical result, and it is under-sold.

#### Structural Coherence
Title → Abstract → §1 research questions (L50) → Results §3.2–3.7 → §5 are consistent, and each research question is answered. The over-promise lies in emphasis rather than content: "valid" (J-3), "for any stager" (J-5), and a practice recommendation of 20 nights not shown in the Results (J-4).

#### Title & Abstract
The abstract numbers match the Results and Tables (90.2–92.5 %; 86.0 %; 21 and 23 of 24; 0.64–0.86; 38 %; 90.3–92.0 %; 9–17 %; 64 %/98.7 %/97.2 %/61 %). The highlights are within 85 characters (76–82). The supplement's opening line repeats the manuscript title exactly. See J-3 and J-12.

#### Conclusion
§5 answers the research questions and keeps the TST-specific, local-calibration scoping. It should drop the unqualified "reach their nominal coverage" in favour of "on average within a cohort" (J-3) and present 20 nights as a minimum with residual risk (J-4).

### Questions for Authors
1. Under the recommended deployment (10 or 20 locally scored nights), what fraction of nights do the TST intervals decide at 6 h, with what accuracy, and how does that compare with the calibrated plug-in classifying all nights?
2. How much of the TST efficiency gain over limits of agreement remains when the limits are centred on the recalibrated plug-in, in each cohort? Why does ST reverse (ratio 1.18 vs `scp_abs_cal`)?
3. Which commercial or clinically deployed scorers export per-epoch probabilities, i.e. what is the practical deployment pathway for a typical sleep laboratory?
4. What monitoring would you advise a site to use to detect loss of coverage after start-up?
5. Has the authors' institution determined that this secondary analysis is exempt from further ethical review?

### Minor Issues
- L17: state the word-count convention (see J-9).
- L91: "during review" (J-7).
- L161 (ii) "it was not reliably met across cohorts": consistent with the abstract; the cover letter (L19) is consistent too.
- §3.3 (L125): the joint-criterion counts combine end-to-end interval-score tests with width–error correlations from the pre-specified design. This is disclosed in parentheses; keep it.
- Fig. 5e–h caption: "Table 2 protocol" should say explicitly "full calibration half (~75 nights in SC/HMC; 22 in ST)".
- Table 1: add recording era and setting (home/hospital) per cohort, since these bear on the transport discussion.
- Code availability (L195): "will be deposited … upon acceptance". Consider depositing at submission with a private reviewer link, since the supplement points readers to the code.
