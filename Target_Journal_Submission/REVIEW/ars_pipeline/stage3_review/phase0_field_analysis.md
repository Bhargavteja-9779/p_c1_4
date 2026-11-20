# Field Analysis Report

ARS `academic-paper-reviewer`, Phase 0 (field analysis and persona configuration), run as Stage 3 of pipeline run `ars-p_c1_4-2026-11-20-a`. Agent spec: `academic-paper-reviewer/agents/field_analyst_agent.md`. Date: 2026-11-20.
Phase 1 has not started. It waits for the user to accept the four cards below (Checkpoint Rule 1, #1030).

## Paper Basic Information
- **Title**: Per-night prediction intervals for automatically scored sleep parameters: conformal calibration of posterior hypnogram samples compared with limits of agreement
- **Language**: English
- **Abstract length**: 297 words per the authors' build count (`manuscript/build/word_counts.json`, also stated on the title page). A plain whitespace count of the abstract text without its four labels gives about 301, because tokens such as "90 %" split in two. Either way the abstract is at the 300-word limit. Structured: Objective / Methods / Results / Conclusions.
- **Full text length**: main text 4,946 words per the authors' build count (title page). The whole rendered file, including tables and captions, is about 7,900 words. Supplementary Material is about 205,000 words, almost all machine-generated tables.
- **Number of references**: 49 numbered entries in the reference list (`Final_Manuscript.pdf`). The text cites 49 distinct keys.
- **Display items**: 8 (Tables 1–3, Figs. 1–5)

## Field Analysis

| Dimension | Analysis Result |
|-----------|----------------|
| Primary Discipline | Sleep medicine: clinical polysomnography and the validation of automatic sleep-stage scoring and of night-level sleep parameters |
| Secondary Disciplines | Statistical methodology (distribution-free/conformal predictive inference; method-comparison and agreement statistics), Biomedical engineering / machine learning (EEG-based automatic staging; probabilistic sequence models such as HMMs and forward-filtering backward-sampling), Health informatics (deployment and local validation of AI-based clinical scoring tools) |
| Research Paradigm | Quantitative Research |
| Methodology Type | Statistical Modeling / Machine Learning, combined with a Comparative Study (method comparison against three limits-of-agreement variants and other interval methods). Secondary analysis of three public PSG cohorts (348 nights, 251 subjects) using repeated subject-grouped resampling, cross-cohort transport and few-night local recalibration experiments. |
| Target Journal Tier | Venue: *Sleep Medicine* (Elsevier). Track: none given. Article type: Original Article. |
| Paper Maturity | Pre-submission. The structure is complete: title page, highlights, structured abstract, IMRaD sections 1–5, declarations, a numbered reference list in the PDF, 3 tables and 5 figures. The stated word counts are within the author-stated limits. One internal revision round is logged (Supplementary S1, "Revision 1"). Author-side placeholders remain: author and affiliation fields, CRediT, and five `[AUTHOR ACTION REQUIRED]` markers (AI declaration, competing interests, funding, ethics, code repository). |

## Target Journal
- Venue: *Sleep Medicine* (Elsevier)
- Track: none given
- Article type: Original Article
- Author-stated constraints, as supplied with this dispatch and in `journal_selection/selected_journal.md`: main text ≤5,000 words; structured abstract ≤300 words; ≤50 references; ≤8 display items.
- Criteria binding: no #683 `ReviewTargetContext` object, `ReviewCriteriaBindingManifest` or pointer-only Target Criteria Brief came with this dispatch. This report configures Card #1 for the venue the authors stated. It does not resolve or emit a criteria binding (see Review Strategy Recommendations).

## Coverage

| Part | Status |
|------|--------|
| Title page, running title, article type, word-count line, highlights (5), structured abstract, keywords | read |
| Body: §1 Introduction, §2.1–2.9 Materials and methods (including Equations 1–5), §3.1–3.8 Results, §4 Discussion (including Limitations i–vi), §5 Conclusion | read |
| Declarations: generative-AI use, CRediT, competing interest, funding, ethics, data availability, code availability, acknowledgements | read |
| Reference list (49 entries) | read, from `manuscript/Final_Manuscript.pdf` (reference section, about pp. 22–28). The rendered markdown has only a pandoc placeholder (`::: {#refs}`). I checked that the PDF text matches the markdown on sample passages (word-count line, abstract Results, §3.3, §3.7, §4, §5). |
| Table 1 (cohorts and stager performance) | read (inline; identical to `tables/table1_cohorts.md`) |
| Table 2 (within-cohort validity and efficiency, YASA) | read (inline; identical to `tables/table2_display.md`) |
| Table 3 (bias and MAE of point estimates, YASA) | read (inline; identical to `tables/table3_display.md`) |
| Fig. 1 (example HMC night) | read (PNG viewed) |
| Fig. 2 (within-cohort efficiency) | read (PNG viewed) |
| Fig. 3 (transport and local deployment) | read (PNG viewed) |
| Fig. 4 (robustness to signal corruption) | read (PNG viewed) |
| Fig. 5 (adaptivity, flagging, clinical decisions) | read (PNG viewed) |
| Embedded images other than the five figures | none |
| Appendices inside the manuscript | none |
| Supplementary S1: protocol and deviation log | read |
| Supplementary S2–S14: machine-generated result tables | not read. Headings, captions and the first rows of each were skimmed. |
| Supplementary S15: computational cost | per-night cost table read. One-off cost table is not readable: the supplement shows only the placeholder "*[tableS_efficiency_oneoff not available]*". |
| Supplementary S16: datasets and data-leakage audit | read |
| `supplementary/PREREGISTERED_PROTOCOL.md`, `supplementary/S_data_and_leakage_audit.md` | read. Every non-heading line also appears verbatim in S1 and S16. |
| Analysis code (`code/`), which the manuscript says is supplied as supplementary material | not read |

**Parts not read or not readable**

1. **Supplementary S2–S14** (all-method results, paired tests, LightGBM stager, difficulty strata, local deployment, transport and montage, clinical thresholds, pre-registered cross-fitted analysis, sensitivity analyses, subgroups, error analysis, robustness, flagging). Why: these sections are readable but hold about 200,000 words of tables, so Phase 0 skimmed only their headings, captions and first rows. No card says what these sections contain. Cards name them only as places to check claims the main text makes. **Question for the user:** should Phase 0 be re-run after reading any of these sections in full, or should the reviewers consult them during Phase 1?
2. **Supplementary S15, one-off cost table.** Why: the compiled supplement has a placeholder instead of the table. A file `tables/tableS_efficiency_oneoff.md` exists in the project but was not read, because it is not part of the supplement as compiled. **Request:** please supply the intended table, or confirm whether that file is the content meant for S15.
3. **Analysis code (`code/`).** Why: Phase 0 configures the panel from the manuscript text, and the code was outside that scope. No card makes any statement about the code. **Question for the user:** should Phase 1 include a code check? If so, Reviewer 1 is the natural seat.

Not part of the manuscript under review and not read: `manuscript/cover_letter.*`, `supplementary/literature_review_and_journal_benchmark.md` (an internal working note) and the earlier internal review files under `REVIEW/` (`cycle01/`, `review_01.md`). `journal_selection/selected_journal.md` was read only for the target metadata.

Text aimed at the panel: none found in the manuscript or in the prose lines of the supplement. The `[AUTHOR ACTION REQUIRED]` markers address the authors, not reviewers, and are recorded above only as maturity evidence.

## Reviewer Configuration Cards

### Reviewer Configuration Card #1

**Role**: EIC
**Display role**: Journal-Fit Reviewer
**Identity Description**: Senior Associate Editor of *Sleep Medicine* who handles submissions on automated scoring, device and wearable validation and other sleep-technology work. A sleep physician by training, formerly medical director of an accredited clinical polysomnography laboratory, and used to judging whether a methods paper gives the journal's clinical readership a usable takeaway.
**Review Focus**:
  1. Check whether the clinical problem is stated in terms a sleep clinician acts on: signing off or re-scoring an individual automatically scored night. Check also whether the payoff is expressed in clinical units early and consistently [Abstract Objective; §1 ¶2; §4 "Implications for practice"; §5].
  2. Check whether the contribution, as the manuscript now states it, is significant enough for an Original Article. The stated contribution is valid per-night intervals, an advantage over limits of agreement that is specific to TST, and validity only under local calibration [Abstract Conclusions; §1 ¶5; §4 ¶1; §5].
  3. Check that the title, highlights, abstract and conclusion each match the Results they summarise. Check also that the title quoted at the start of the Supplementary Material matches the manuscript title [title page; Highlights; Abstract; §3.2–3.7; §5; Supplementary Material, opening line].
  4. Check against the author-stated Original Article limits: the stated word counts (main text 4,946; abstract 297) [title page] [unverified], 49 references [Reference list], 8 display items [Tables 1–3; Figs. 1–5]. Check also the completeness of the author, CRediT, competing-interest, funding, ethics and code-availability statements, which carry placeholder or `[AUTHOR ACTION REQUIRED]` markers [title page; Declarations; Ethics statement; Code availability].
  5. Check whether a journal reader can tell what "review" refers to where the text dates design changes: "added during review" [§2.6; §2.7 "Clinical use"] and "after the first review" [§4 Limitations (vi)]. Check also whether the AI-use statements in §2.9 and in the Declaration are consistent and specific enough for an editor to assess [§2.9; Declaration of generative AI].
**Will particularly care about**: Whether a clinician reading the journal leaves with a clear, correctly scoped practice message [§4 "Implications for practice"; §5]. Whether the paper, with its results narrowed to TST [Abstract Conclusions; §4 ¶1], is positioned so that editors would not see it as a purely technical contribution.
**Possible blind spots**: Will not check the conformal validity argument, the resampling design or the permutation tests. May underweight the HMM/FFBS construction. May accept the clinical thresholds and parameter definitions without checking them against scoring conventions (Reviewers 1 and 2 cover these).

### Reviewer Configuration Card #2

**Role**: Peer Reviewer 1
**Display role**: Peer Reviewer 1
**Identity Description**: Biostatistician in clinical measurement and prediction methodology, specialising in distribution-free prediction intervals (split conformal, cross-conformal, CV+/jackknife+) and in method-comparison analysis (parametric and regression-based Bland–Altman limits, ICC) of clustered, repeated-measures data. Also experienced in Bayesian computation for state-space models. Focuses on whether a stated validity guarantee and a comparative claim survive the resampling and fitting scheme actually used.
**Review Focus**:
  1. Check whether the finite-sample and CV+ (≥1−2α) statements match the design that was run. Points to check: calibration scores from models cross-fitted within the calibration half, but test summaries from the model fitted on the whole half; the regulariser σ̄ computed over calibration and test nights; splits grouped by subject while coverage is counted per night in cohorts with two nights per subject [§2.5, Eqs. 4–5; §2.7 "Primary within-cohort analysis"; §4 Limitations (ii)].
  2. Check whether all comparators receive equivalent information. Points to check: the three limits-of-agreement variants and their centre (raw vs recalibrated plug-in); how the interval score is used; the two-sided sign-flip permutation test on per-subject means; the scope of the Holm adjustment across the 24 to 48 cohort–parameter combinations; how counts of "significant" combinations are aggregated in the text [§2.6; §2.8; §3.3; Table 2; Fig. 2; Supplementary S3 caption].
  3. Check whether a reader can verify the timing of the protocol, given the "pre-registered" label. Also check how the switch of the primary analysis and the comparators and thresholds added later are disclosed. Compare the analyses reported in the Results with the protocol and change log, including the α and n_t grids listed in S1. Check whether S9 supports the statement that the pre-registered analysis led to the same qualitative conclusions [§2.5 last sentence; §2.6 last sentence; §2.7; §4 Limitations (vi); Supplementary S1; Supplementary S9].
  4. Check how coverage variability and small samples are summarised and interpreted. Points to check: the mean over splits with the 2.5th–97.5th percentile range in ST (22 test nights); the site-level probability of coverage below 80% behind the "at least 20 nights" recommendation; the hard-night quartile, which is defined by label-dependent plug-in accuracy. Also check how accuracy on the subset of decided nights is set against plug-in accuracy on all nights [§2.7; §3.2; §3.5; §3.7; §4 "Implications for practice"; Abstract Results; Fig. 3c, f; Fig. 5e–h].
  5. Check the posterior construction and the data handling. Points to check: the rationale for the emission temperature (evidence counted repeatedly) and its fitted value τ ≈ 0.1 against the [0.02, 1.5] grid; add-one smoothing; right-censoring of REM latency; whether every label-dependent component is refitted in the local-deployment runs. Check also whether the handling of unscored reference epochs is described the same way in §2.2, in the S1 "Revision 1" log and in the S16 leakage-audit table [§2.2; §2.4, Eqs. 1–3; §2.7 "Local deployment"; §3.1; Supplementary S1; Supplementary S16].
**Will particularly care about**: Whether "valid" in the abstract and conclusion means exactly what the design guarantees (marginal, per-night, CV+-type, within cohort) [Abstract; §2.5; §5]. Whether the efficiency claims rest on comparisons that are fair and correctly adjusted for multiplicity [§2.8; §3.3].
**Possible blind spots**: May treat the scoring-rule, analysis-window and threshold choices as given rather than checking whether they are clinically appropriate (Reviewer 2). May weigh a statistically correct but operationally demanding procedure as acceptable without asking what it costs a laboratory (Reviewer 3).

### Reviewer Configuration Card #3

**Role**: Peer Reviewer 2
**Display role**: Peer Reviewer 2
**Identity Description**: Senior sleep scientist in clinical polysomnography and sleep-scoring standards (Rechtschaffen & Kales and AASM). Has published on inter-scorer reliability, the effect of rule sets on sleep parameters, and the validation of automatic staging algorithms and their derived night-level parameters. Focuses on whether parameter definitions, reference standards and cohort descriptions match how sleep laboratories score and use these parameters.
**Review Focus**:
  1. Check the parameter definitions and analysis windows against scoring conventions. Points to check: SOL from lights-off; REM latency from sleep onset; WASO within a fixed 10-h window for SC versus lights-on for HMC; unscored reference epochs counted as wake; stage percentages relative to TST; merging R&K S3+S4 into N3 [§2.1; §2.2; §3.6; §4 "The WASO failure and the choice of centre"].
  2. Check whether attributing the cross-cohort failure to population or scoring-rule differences, after the F4-M1 montage analysis, is supported by what was examined. Check also whether differences in recording era, equipment and sampling between cohorts are considered [§2.7 "Transportability"; §3.5 ¶1; Fig. 3a, d; Supplementary S7; Supplementary S16 Datasets table].
  3. Check the positioning within the sleep literature: validation of automatic staging, inter-scorer reliability, hypnodensity and multi-scorer ambiguity, and night-level uncertainty and scorability work. Check whether the cited works support the specific claims attributed to them, for example ref. [19], cited for conformal prediction sets for single epochs [§1 ¶1–3; §4 "Relation to previous work"; Reference list].
  4. Check whether the clinical decision thresholds (TST < 6 h, SOL > 30 min, WASO > 30 min, REM latency ≤ 15 min) have a stated clinical source. Check also whether they fit the cohorts studied, given a 2.5% prevalence at the REM-latency threshold [§2.7 "Clinical use"; §3.7; Fig. 5e–h].
  5. Check how the single-scorer reference is interpreted: coverage of "that scorer's values" against inter-scorer variability. Check also how evaluating only feature-based stagers bears on the generality claimed for "any stager" [§1 ¶5; §2.3; §4 "Relation to previous work"; §4 Limitations (iii), (iv)].
**Will particularly care about**: Whether the night-level parameters are defined so that sleep clinicians would recognise and accept them, particularly WASO and the latencies [§2.2]. Whether the novelty is stated in proportion to the existing sleep-field work on posterior hypnogram sampling that the manuscript cites [§1 ¶3; §4 "Relation to previous work"].
**Possible blind spots**: May not check the conformal guarantee or the resampling statistics (Reviewer 1). May take the deployment recommendations at face value without asking what they cost or whom they cover (Reviewer 3).

### Reviewer Configuration Card #4

**Role**: Peer Reviewer 3
**Display role**: Peer Reviewer 3
**Identity Description**: Health-informatics and implementation-science researcher who studies how AI-based clinical decision-support and scoring software is introduced and monitored after deployment in hospital diagnostic services, including sleep-laboratory workflows. Has also worked on performance evaluation of software as a medical device. Focuses on what a site must do, at what cost and for whom, to use a method safely, and on how clinicians read uncertainty statements.
**Review Focus**:
  1. Check who the manuscript assumes will benefit from per-night intervals (clinicians signing off nights, laboratories) and who bears the cost (manual scoring of local calibration nights, review of undecided or wide-interval nights). Check also who is left out of the evidence base: populations, age groups, settings and recording devices not represented in the three cohorts [§1 ¶2; §2.1; Table 1; §4 "Implications for practice"; §4 Limitations (iv)].
  2. Check whether the recommended deployment procedure says how a site would detect loss of validity after start-up. Examples are changes in patient mix, montage, equipment or scorer, read against the site-level risk of realised coverage below 80% and the transport results [§3.5; Fig. 3; §4 "Implications for practice"; §4 Limitations (ii)].
  3. Check what the manuscript says happens to nights the intervals leave undecided at each threshold, and to nights flagged by a wide interval. Check what manual-review workload this implies, and how it compares with the label-free flag that worked better for TST in HMC [§3.7; §3.8; Fig. 5d–h; §4 "Implications for practice"].
  4. Check whether a "90% interval" is explained so that a clinician can act on it correctly. Points to check: marginal rather than conditional coverage; lower coverage on the hardest nights; coverage of a single scorer's values [§1 ¶2; §3.2 ¶2; §4 Limitations (i), (iii); Fig. 1e, f].
  5. Check whether the simulated corruptions (additive Gaussian noise, movement-artefact drifts, calibration on clean nights) correspond to artefacts met in clinical or home recordings. Check also what the manuscript advises when test signals are degraded [§2.7 "Robustness"; §3.8; Fig. 4; Supplementary S13].
**Will particularly care about**: Whether the practice recommendation (recalibrate on at least 20 local nights, report TST with an interval, review wide or threshold-straddling nights) is specified fully enough for a laboratory to adopt and audit [§4 "Implications for practice"; §5].
**Possible blind spots**: Will not check the statistical derivations or the HMM construction (Reviewer 1). May not judge whether parameter definitions and thresholds follow scoring conventions (Reviewer 2). May weigh feasibility over methodological novelty.

## Stakeholder Coverage

Seat: Card #4 (Peer Reviewer 3), Review Focus item 1
Check: Who the manuscript assumes will benefit from per-night intervals (clinicians signing off nights, laboratories), who bears the cost (manual scoring of local calibration nights, review of undecided or wide-interval nights), and who is left out of the evidence base (populations, age groups, settings and recording devices not represented in the three cohorts) [§1 ¶2; §2.1; Table 1; §4 "Implications for practice"; §4 Limitations (iv)].
Competence basis: Card #4's implementation-science and health-informatics expertise in deploying and monitoring AI scoring tools in diagnostic services, including sleep-laboratory workflows and software-as-a-medical-device evaluation. This covers the users, the parties who carry the operating cost, and the populations a deployed tool's evidence does or does not cover.

## Review Strategy Recommendations
- **Highly cross-disciplinary paper.** Coverage across seats is as follows. Sleep medicine (scoring rules, parameter definitions, cohorts, thresholds) [§2.1–2.2; §2.7 "Clinical use"; §3.5–3.7] goes to Reviewer 2. Statistical methodology (conformal guarantee, agreement statistics, resampling, tests) [§2.5–2.8; §3.2–3.3] and the probabilistic sequence model (HMM/FFBS) [§2.4] go to Reviewer 1. Health informatics and deployment (local calibration burden, monitoring, workload, communicating uncertainty) [§3.5; §3.7–3.8; §4 "Implications for practice"] goes to Reviewer 3. Clinical readership fit and significance [Abstract; §1; §4 ¶1; §5] goes to the Journal-Fit Reviewer.
- **A methods contribution aimed at a clinical journal.** Expect tension between the Journal-Fit Reviewer (is the narrowed, TST-specific advantage enough for clinical readers?) and Reviewer 1 (does "valid" hold exactly as claimed under the fitting scheme?). The synthesizer should keep significance and validity separate.
- **The manuscript has already been through one internal revision round** that changed the primary analysis [§2.7; §4 Limitations (vi); Supplementary S1 "Revision 1"]. Reviewers should read the end-to-end protocol as the primary analysis and the pre-registered cross-fitted analysis (S9) as secondary. The cards ask Reviewer 1 to check consistency between them, not to assume it.
- **The supplement is very large and was only skimmed in Phase 0** (S2–S14). Reviewers who rely on a supplementary table should read it themselves. No card carries a statement about its contents.
- **Disclosed AI involvement.** The manuscript states that a generative AI system searched the literature, wrote and ran the analysis code and drafted the text [§2.9; Declaration of generative AI]. Reviewers should anchor claims to the tables and figures they read. Stage 2.5 integrity verification runs separately and is not replaced by this panel.
- **Bibliography source file.** `manuscript/references.json` holds two entries that the text does not cite (`rohrscheib2026`, `vainikka2026`), so they do not appear in the rendered reference list. Whether either belongs in the paper is for Reviewer 2 to judge.
- **Criteria binding.** The venue and article type are author-stated, but no `ReviewCriteriaBindingManifest` or Target Criteria Brief was supplied. Under SKILL.md #684, unless the orchestrator supplies one before Phase 1, each seat discloses `criteria_binding_unavailable`. In that case, Card #1's venue-limit checks stay checks against the author-stated limits and are not a bound venue-alignment claim.
- **Panel composition.** The fifth execution seat is the fixed Devil's Advocate, which receives no configuration card.
