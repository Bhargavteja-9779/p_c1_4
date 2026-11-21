## Domain Review Report (Peer Reviewer 2)

ARS `academic-paper-reviewer`, Phase 1, seat Peer Reviewer 2 (Domain; Card #3). Pipeline run `ars-p_c1_4-2026-11-20-a`, Stage 3. Review date 2026-11-21.
Criteria binding: `criteria_binding_unavailable`. No ReviewCriteriaBindingManifest or Target Criteria Brief was supplied, so judgements are checked against Card #3 and against field sources named in the text.
Independence: this report was written without opening any other seat's file in `stage3_review/`. Only `phase0_field_analysis.md` was read there. I formed my view first and only then checked `stage2_5_integrity/reverification_round1.md`, so that I would not repeat items it resolved. I did not read `REVIEW/cycle01/` or `REVIEW/review_01.md`.

**What I read.** The full manuscript (`manuscript/build/manuscript_rendered.md`, L1–299; line numbers below refer to it). The reference list (`Final_Manuscript.pdf` via pdftotext, and `references.json`). Fig. 5 (viewed). Supplementary S1 (in full), S7 (montage tables), S16 (in full), and greps of S2/S5/S8/S12. `code/src/evaluation/sleep_params.py` and `code/src/data/sleep.py` (definitions only). I also computed reference-parameter distributions from `results/summaries/yasa_xfit.csv`, labelled "own computation" below. Cited and proposed works were checked against Crossref, PubMed, Semantic Scholar and Google Patents.

### Reviewer Identity
Senior sleep scientist in clinical polysomnography and sleep-scoring standards (Rechtschaffen & Kales and AASM). Background in inter-scorer reliability, the effect of rule sets on sleep parameters, and the validation of automatic staging algorithms and the night-level parameters derived from them (Card #3).

### Overall Recommendation
Major Revision

### Confidence Score
4. My confidence is high on scoring conventions, parameter definitions, cohorts and literature. It is lower on the conformal and statistical machinery, which is Reviewer 1's remit and which I did not audit.

Confidence is an uncertainty/scope disclosure only; it never changes consensus counts, severity, decision bearing, or arbitration.

### Calibration Status
`NOT_CALIBRATED`

### Criterion-Bound Judgements
| Dimension / criterion | Criterion source | Judgement | Evidence anchors | Rationale | Uncertainty or scope limit | Decision bearing? |
|---|---|---|---|---|---|---|
| Parameter definitions and analysis windows match scoring conventions | Card #3 focus 1 | PARTLY_MEETS | `manuscript: L59`; `code: sleep_params.py L6–9, L43`; `own computation: yasa_xfit.csv` | TST, SOL (from lights-off) and REML (from sleep onset) are conventional. The WASO definition (wake between the first and last sleep epoch) is not stated in the text and drives the SC "WASO failure". The 10-h SC window is not a time-in-bed window. | I could not consult the exact wording of the AASM manual's WASO definition, so that point is marked [unverified]. | yes: it feeds the abstract, a highlight and the Discussion |
| Unscored epochs and the N3 merge | Card #3 focus 1 | PARTLY_MEETS | `manuscript: L56, L59`; `supplement: S1 item 9; S16 leakage row "Label leakage via unscored epochs"` | Counting unscored epochs as wake is a defensible convention, but S16 contradicts it. The S3+S4→"N3" relabelling hides the systematic R&K/AASM difference. | Small quantitative effect | no |
| Attribution of the transport failure | Card #3 focus 2 | DOES_NOT_MEET | `manuscript: L101, L135`; `supplement: S7 montage table; S16 Datasets table` | F4-M1 vs C4-M1 tests a montage change inside HMC, not the SC derivation (bipolar Fpz-Cz). Age, recording era and equipment, setting, scorer and rule set are all confounded. | — | yes |
| Positioning and citation accuracy | Card #3 focus 3 | PARTLY_MEETS | `manuscript: L29, L44, L46, L153`; references [12]–[25] | Most of the 20 citations I checked support their sentence. van Gorp et al. is misdescribed at L153. LoA are mischaracterised at L29/L44. The ConMIL citation is loosely characterised. | Full texts not read for some entries (marked) | yes, for novelty framing |
| Clinical thresholds | Card #3 focus 4 | DOES_NOT_MEET | `manuscript: L105, L143, L33, L166`; `figure: Fig. 5e–h` | The thresholds have no source. Sources exist, but these are research-phenotype or narcolepsy cut-offs. Prevalence differs widely between cohorts (pooled). REML ≤ 15 min occurred in 8 of 348 nights. | — | yes: it is in the Abstract and Conclusion |
| Single-scorer reference and generality | Card #3 focus 5 | PARTLY_MEETS | `manuscript: L35, L50, L153, L161 (iii), (iv)` | The limitation is acknowledged, but "valid per-night error ranges" in the Abstract and Conclusion is not scoped to one scorer. "Any stager" is a design property, not a tested result. | — | yes |
| Coverage of recent literature on night-level agreement and uncertainty | Agent Step 1b | PARTLY_MEETS | `references: full list` | The epoch-level UQ and sampling work is well covered. Inter-scorer literature on night-level parameters, multi-scorer datasets and the rule-set/derivation work are thin. | Coverage date = review date (no version date in the manuscript) | no |

### Summary Assessment
The manuscript asks a question that sleep clinicians recognise: how far off might the automatically scored parameters of *this* night be? The answer it reports is honest. Locally calibrated intervals reach nominal marginal coverage, beat limits of agreement clearly only for TST, fail for WASO in SC, and do not transport between cohorts. The authors already narrowed their claims in an internal revision, and the remaining domain problems are mostly ones of framing and attribution rather than of data.

There are six problems. (1) The paper sets its intervals against "population" limits of agreement that supposedly "say nothing about individual nights". Bland–Altman LoA are, by construction, a range for an individual night's difference, and the proposed intervals are also marginal. The real contribution is width that adapts to each night. (2) The cross-cohort failure is attributed to "population or scoring rules" after a montage check that does not reproduce the SC derivation. Age, era, hardware, setting and scorer are left out. (3) "Valid" means coverage of one cohort-specific scorer's values. For stage percentages, that scorer's idiosyncrasy is a large part of the target. (4) The WASO finding depends on an unstated WASO definition and an artificial 10-h window. (5) The clinical thresholds have no source and are inappropriate in part. (6) The prior posterior-sampling work of van Gorp et al. is described as uncalibrated against scorers, which is inaccurate.

All six are fixable in the repository. A multi-scorer check would strengthen the paper considerably but needs new (public) data.

### Strengths
1. **Label-free analysis windows and a leakage-aware parameter pipeline.** Windows come from lights-off/lights-on metadata, never from the reference hypnogram. This avoids the common Sleep-EDF practice of cropping to "30 min before the first and after the last sleep epoch". Automatic parameters never see the reference unscored mask. `manuscript: L59`; `supplement: S16 leakage row "Leakage through analysis window"`.
2. **Honest parameter-specific reporting, including a mechanistic error analysis.** The paper reports that the gain is TST-specific and that WASO intervals fail in SC. It explains the failure (spurious late sleep epochs move the final awakening; 49 % of SC samples vs 1 % in HMC; ρ = 0.79), and the explanation is checkable. `manuscript: L127, L140, L155–157`; `results: e08_waso_mechanism_summary_yasa.csv`.
3. **The clinically useful point-estimate finding.** Recalibrating probabilities on local nights removes most of YASA's TST under-estimation (HMC −38.3 → −5.2 min; with 10 nights −3.8 min). This is a practical, transferable message for laboratories, and the authors correctly separate it from the posterior-sampling contribution. `manuscript: L132`; `table: Table 3`.
4. **Use of three cohorts with two rule sets, plus a montage sensitivity analysis.** These are the right ingredients for a transport question, even if the interpretation overreaches (see W2). `manuscript: L56, L101, L135`.
5. **Grounded citation of the closest prior work, including a withdrawn patent application.** I verified EP4388985A1. Its claim 1 thresholds the uncertainty of sleep parameters estimated from multiple sampled hypnograms, as stated at L46. `reference: [25]`.

### Weaknesses
1. **W1. Limits of agreement are mischaracterised, and the contribution is framed as "per-night vs population" when it is "adaptive vs constant width".** L29 says LoA "say nothing about individual nights". L44 says LoA answer "how far off is the algorithm on average?". Highlight 1 (L21) says automatic scoring "gives no error range for the parameters of a single night". In fact the bias answers the average question, and the 95 % LoA give the range expected to contain an individual night's difference (Bland & Altman 1986, ref. [43]). The authors themselves implement LoA as a prediction interval with √(1+1/n) (L91). Their own intervals are also marginal (L161 (i)). A sleep-medicine reader trained on Bland–Altman will notice the strawman. The defensible novelty is per-night *adaptive* width, with a calibrated per-night centre, compared head-to-head on interval score. Suggested fix: rewrite L21, L29, L44 and L153 accordingly. The Menghini et al. framework for sleep-tracker validation, which places Bland–Altman analysis at its core, is the right field reference for current practice.
   - **Severity**: Major | **Evidence Anchor**: `manuscript: L21, L29, L44, L91, L161` | **Confidence**: 5 — direct definitional point, grounded in ref. [43] and the authors' own Eq./L91.
2. **W2. The transport failure is attributed to "population or scoring rules" without the evidence to separate them.** See D-2. The F4-M1 check does not reproduce SC's bipolar Fpz-Cz. The cohorts differ in age, recording era and hardware, setting and scorer. The size of the R&K→AASM N3 shift reported by Moser et al. (ref. [46]) is too small to explain the observed reversal of N3 bias.
   - **Severity**: Major | **Evidence Anchor**: `manuscript: L101, L135`; `supplement: S7 montage table, S16 Datasets table` | **Confidence**: 4.
3. **W3. "Valid per-night error ranges" are not scoped to one scorer.** See D-3.
   - **Severity**: Major | **Evidence Anchor**: `manuscript: L35, L151, L161 (iii), L166` | **Confidence**: 4. Norm evidence: the inter-scorer literature (Lee et al. 2022; Norman et al. 2000; refs. [1], [2]).
4. **W4. The WASO result depends on an unstated definition and a non-clinical window.** See D-4.
   - **Severity**: Major | **Evidence Anchor**: `manuscript: L24, L59, L140, L157`; `code: sleep_params.py L8` | **Confidence**: 4.
5. **W5. The clinical decision thresholds have no source and are partly unsuited to these cohorts.** See D-5.
   - **Severity**: Major | **Evidence Anchor**: `manuscript: L33, L105, L143, L166`; `figure: Fig. 5e–h` | **Confidence**: 4.
6. **W6. The closest prior work is misdescribed.** See D-6.
   - **Severity**: Major | **Evidence Anchor**: `manuscript: L153`; `reference: [24]` | **Confidence**: 4.

### Detailed Comments (numbered, with fix and flag)

**D-1 (MAJOR): Limits of agreement are mischaracterised, so the contribution is mis-framed.** `[FIXABLE-IN-REPO]`
- *Location*: L21 (Highlight 1), L29 (Abstract Objective), L44 (§1 ¶2), L153 (§4).
- *Problem*: Bland–Altman 95 % LoA are an interval for an individual night's algorithm–scorer difference (ref. [43]). Only the bias is a statement about the average. The paper's own intervals are marginal too (L161 (i)), so "per-night vs population" is not the distinction the data test. What the data test is constant width versus width adapted to each night (plus centre recalibration).
- *Why it matters*: a sleep-medicine referee will read L29 and L44 as a strawman of the field's standard method. That undermines trust in the comparison, which in fact is fair.
- *Fix*: replace "say nothing about individual nights" with wording such as "give the same range for every night, however easy or difficult its scoring". Rewrite Highlight 1, for example: "Limits of agreement give every night the same error range". At L44, keep the "tonight" framing but attribute "on average" to the bias only. Cite Menghini et al. 2021 for current validation practice.

**D-2 (MAJOR): The cross-cohort failure is attributed to "population or scoring rules" without supporting analysis; confounders are not discussed.** `[FIXABLE-IN-REPO]` (rewording and a derivation analysis on cached signals). Optional age-matched analyses are also feasible in the repository.
- *Location*: L101, L135 ("which points to differences in population or scoring rules"), L155 ("for example N3 under different rule sets"), L161 (ii); S7 montage table; S16 Datasets table.
- *Problems*:
  1. The montage check compares F4-M1 with C4-M1 inside HMC (N3 bias −4.5 vs −4.8 pp; N3 coverage 42 % vs 38 %; S7 rows "F4-M1/C4-M1 N3% norm_reg_ffbs"). It does not reproduce the SC derivation, which is a short-distance *bipolar* Fpz-Cz. Slow-wave amplitude, and therefore R&K/AASM slow-wave-sleep scoring against the 75 µV criterion, depends strongly on derivation and inter-electrode distance. So "the montage change did not explain the failure" holds only for frontal vs central referential derivations. A closer analogue is available without new data: F4-C4 = (F4-M1) − (C4-M1), with E1-E2 for horizontal EOG, both from the cached signals (S16).
  2. Other differences between the cohorts are not mentioned in §3.5 or §4. Recording era and equipment: SC 1987–1991 analogue ambulatory recorders at 100 Hz with EMG only as a 1-Hz envelope, vs HMC 2018 digital at 256 Hz (S16). Setting: home vs clinical lab. Scorers and centre. Age: SC mean 59.0 ± 22.1 y, up to 101 y (Table 1), whereas HMC demographics are unreleased.
  3. The magnitudes argue against rule set as the main driver of the N3 swing. Moser et al. (ref. [46]; abstract verified) found SWS higher by about 2.4 % of TST under AASM than under R&K S3+S4. The observed swing in YASA's N3 bias is 10.7 pp (+5.9 → −4.8; L135). Own computation: reference N3 % median 8.2 % in SC (18 of 153 SC nights had 0 % reference S3+S4) vs 23.9 % in HMC (2 of 151 at 0 %). This is consistent with age, derivation and amplitude effects at least as much as with rules.
  4. Moser et al. also found TST, SOL and REM latency unaffected by the rule set. Yet LightGBM TST coverage on HMC fell to 51 % (L135). That failure therefore reflects degradation of the stager (κ 0.49; Table 1) under montage and population shift, not scoring rules.
  5. The authors' own HMC source paper (ref. [33], Alvarez-Estevez & Rijsman) already shows κ falling from 0.80 to 0.54 across databases. The transport result is expected and should be framed against it.
- *Fix*: replace L135's attribution with "montage (frontal vs central) did not explain it; population, recording era and equipment, derivation (bipolar Fpz-Cz vs referential), scorer and rule set are confounded in these cohorts". Add the F4-C4 analysis if feasible. Cite ref. [46] with its effect size and ref. [33] for cross-database degradation. Consider reporting SC N3 bias by age tertile to show whether the bias reversal tracks age.

**D-3 (MAJOR): The single-scorer reference limits what "valid" means; the Abstract and Conclusion overstate it.** `[FIXABLE-IN-REPO]` for wording; `[NEEDS-NEW-DATA]` for the recommended multi-scorer test.
- *Location*: L35 ("valid per-night error ranges"), L151, L161 (iii), L166; Card focus 5.
- *Problem*: each night has one scorer (S16), so coverage is coverage of *that scorer's* value. Inter-scorer agreement is fair for N1 and only moderate for N2 and N3. In the meta-analysis of Lee et al. 2022 (verified) the pooled κ was W 0.70, N1 0.24, N2 0.57, N3 0.57, R 0.69. Night-level differences between centres are well documented (Norman et al. 2000; Kuna et al. 2013; Younes et al. 2016). For stage percentages, therefore, a substantial part of the "error" the intervals cover is scorer idiosyncrasy, and an interval calibrated to scorer A need not cover scorer B. Within each cohort, an unknown number of technicians scored the nights. Exchangeability across scorers is assumed, never examined. The limitation is stated once (L161 (iii)), but the Abstract, Highlights and Conclusion say "valid" without qualification. A clinician will read that as validity against the truth or against any qualified scorer.
- *Fix*: (a) Scope every "valid" in L22, L35, L151 and L166 to "coverage of the reference scorer's values". (b) Recommended: apply locally calibrated intervals to a public multi-scorer dataset, such as the Dreem Open Datasets DOD-H/DOD-O (Guillot et al. 2020, five scorers), and report coverage of each individual scorer and of the consensus. This directly answers what clinicians need, and it would contrast the intervals with van Gorp et al.'s inter-rater distributions. (c) Discuss the scorer-variability argument in "Why the gain was specific to TST" (L155), which currently attributes stage-percentage error to "rule sets" only.

**D-4 (MAJOR): The WASO definition is unstated, and the SC "WASO failure" is largely an artefact of the window.** `[FIXABLE-IN-REPO]`
- *Location*: L24 (Highlight 4), L33, L59, L140, L157; `code/src/evaluation/sleep_params.py` L8 ("WASO = wake epochs between first and last sleep epoch").
- *Problem*: the text never says that WASO excludes wake after the final awakening. Clinical PSG reports compute wake after sleep onset over the recording period up to lights-on [unverified: I could not consult the exact AASM manual wording; reporting definitions vary between laboratories]. SC has no lights-on (S16), so the "10-h" window is not a time in bed. Own computation: under a recording-period definition (window − SOL − TST), median reference WASO would be 168.5 min in SC vs 43 min under the paper's definition. In HMC the two are 44.5 vs 40.5 min. The 116-min median of post-awakening wake in SC (L140) is time that is plausibly out of bed or awake in the morning in an ambulatory recording. The mechanism at L140 is real, but its clinical generalisation ("WASO intervals were worse in long recordings", L24; "long ambulatory recordings", L151) is not supported. Home PSG used clinically has a lights-on or end of time in bed (from a diary or the technician). L157 says this is "a property of the parameter definition as much as of the method"; that is correct, but the abstract and highlights do not reflect it.
- *Fix*: (a) State the WASO definition with a source in §2.2. (b) Reword Highlight 4 and the Abstract, for example "WASO intervals failed in recordings without a lights-on marker". (c) Report HMC WASO under the recording-period definition as a sensitivity analysis. (d) Optionally re-run SC WASO with the window ending at a label-free proxy (for example the last epoch scored as sleep by the *automatic* stager plus a fixed margin), or drop SC WASO from headline counts.

**D-5 (MAJOR): The clinical decision thresholds have no source, are partly unsuited to the cohorts, and the decision results are pooled across very different prevalences.** `[FIXABLE-IN-REPO]`
- *Location*: L33, L105, L143, L151, L166; Fig. 5e–h; S8.
- *Problems*:
  1. L105 calls the thresholds "illustrative ... chosen by the authors". The integrity round left R1-MINOR-3 open on exactly this point; I go further. Each threshold has a recognisable source, and each source belongs to a specific clinical context:
     - TST < 6 h: the short-sleep insomnia phenotype (Vgontzas et al. 2013, verified).
     - SOL and WASO > 30 min: quantitative insomnia criteria, which were derived for sleep diaries (Lichstein et al. 2003; existence verified; content from my knowledge [unverified detail: the ≥31 min criterion]).
     - REM latency ≤ 15 min: the nocturnal sleep-onset REM period criterion for narcolepsy (Andlauer et al. 2013, verified: specificity 99.2 %, sensitivity 50.6 %; also used in ICSD-3).
  2. These are phenotype or screening cut-offs, not the decision a clinician makes when signing off an automatically scored night. The Conclusion's "supported more confident threshold decisions" (L166) therefore overstates clinical utility.
  3. Prevalence differs widely between cohorts (own computation, reference values):
     - TST < 6 h: 40 % HMC, 18 % SC, 4.5 % ST.
     - REM latency ≤ 15 min: 8 nights in total (5 HMC, 3 SC, 0 ST).
     Pooled accuracy (L143, Fig. 5) therefore mixes populations. For REML it is close to trivial: every decision was negative, and accuracy approaches the base rate (Fig. 5h, dotted line ≈ 0.965).
  4. "Plug-in TST correct for 97.2 % of the same nights and 61 % of undecided nights" shows that the intervals mainly separate easy nights from hard ones. That is useful for triage, but it is not a gain in accuracy, and the text should say so.
  5. SOL is measured to the first epoch of any stage (code L6). This is consistent with AASM, but insomnia criteria often use latency to persistent sleep.
- *Fix*: cite the sources and name each clinical context. Report decisions per cohort. Drop REML ≤ 15 min or move it to the supplement as "not evaluable (8 events)". Recast L166 as triage, not decision support.

**D-6 (MAJOR): The closest prior work is misdescribed, which inflates the novelty claim.** `[FIXABLE-IN-REPO]`
- *Location*: L153 ("Posterior sampling of whole hypnograms has been used ... [23, 24] without calibrating it against a scorer"); contrast L46, which is accurate.
- *Problem*: van Gorp et al. 2023 (JBHI, ref. [24]; abstract verified) trained and evaluated U-Flow against six independent scorers on 70 held-out subjects. They report that it "outperforms the other methods in terms of modeling the inter-rater disagreement of overnight sleep statistics". The sampled distributions were therefore compared against scorers, indeed against more than one. What they lack is a finite-sample *coverage* calibration at a target laboratory. L46 says exactly that; L153 does not.
- *Fix*: reword L153, for example "... without a coverage guarantee for the scorer of the laboratory where it is used". Add one sentence on the complementary aims: van Gorp et al. model the spread *between* scorers, whereas this paper covers a *single* local scorer (link to D-3).

**D-7 (MINOR): Treatment of unscored epochs is inconsistent between the text and S16, and its extent is not reported.** `[FIXABLE-IN-REPO]`
- *Location*: L59; S1 item 9; S16 leakage row "Label leakage via unscored epochs" ("Marked −1 and excluded identically from reference and automatic parameters"), which contradicts L59.
- *Domain note*: in R&K, Movement Time is neither sleep nor wake. Counting it as wake in the reference while the automatic hypnogram assigns stages to the same epochs creates a small, systematic difference. Own computation: 290 unscored epochs across 48 SC nights (one night has 144 epochs, 72 min) and 363 across 21 ST nights; none in HMC.
- *Fix*: correct S16. Report these counts in §2.2. Add a sensitivity analysis that excludes the night with 144 unscored epochs, or that gives MT the stage of the neighbouring epoch.

**D-8 (MINOR): The R&K stages are relabelled as AASM stages without caveat.** `[FIXABLE-IN-REPO]`
- *Location*: L56, Table 1, Tables 2–3, Fig. 3.
- *Problem*: "N1/N2/N3" for SC and ST are R&K S1, S2 and S3+S4. Moser et al. (ref. [46]) report systematic differences (S1 vs N1 +2.8 %, S2 vs N2 −4.9 %, SWS +2.4 % of TST, WASO +4 min under AASM), and the paper pools and compares stage percentages across rule sets. With bipolar Fpz-Cz and an elderly cohort, S3+S4 scoring against the amplitude criterion is fragile (18/153 SC nights have 0 %).
- *Fix*: label SC/ST stages "S1/S2/S3+S4 (R&K)" in the tables, or add a footnote. Quote Moser's effect sizes in §2.1.

**D-9 (MINOR): The 10-h SC window can truncate sleep or include out-of-bed time.** `[FIXABLE-IN-REPO]`
- *Location*: L59.
- *Fix*: report how many SC nights have reference sleep in the last 30 min of the window (truncation risk for long sleepers, given ages up to 101), and the distribution of post-awakening wake. State that SOL depends on the accuracy of the lights-off times in the subject sheets.

**D-10 (MINOR): The examples of validation practice are consumer devices, not automatic scoring of PSG.** `[FIXABLE-IN-REPO]`
- *Location*: L42, L153 (refs. [6] Oura, [7] Dreem, [8] Kaneda).
- *Problem*: [6] and [7] (abstracts verified: both use Bland–Altman) validate wearables, where sensor and algorithm error are mixed. Only [8] (verified: LoA for TST about ±0.5 h) is PSG autoscoring.
- *Fix*: add a PSG-autoscoring validation that reports night-level parameter agreement, for example Punjabi et al. 2015 (Somnolyzer). Existence verified; I did not read its content, so this is [unverified: parameter-level reporting].

**D-11 (MINOR): Some citations are loosely characterised.** `[FIXABLE-IN-REPO]`
- *Location*: L46 (ConMIL, ref. [20]; the card calls it ref. [19], but numbering shifted after Vainikka et al. was added as [18]), L44 (Hardarson, ref. [11]).
- *Problems*:
  1. ConMIL (abstract verified) is a multiple-instance-learning + conformal + LLM decision-support framework, with sleep staging as one of two test tasks and set-valued outputs over signal segments. "Conformal prediction sets have been proposed for single epochs" is broadly true but reads as a dedicated sleep-staging method. Suggested: "conformal prediction sets for sleep-stage classification have been used within an LLM-assisted decision-support framework".
  2. Hardarson et al. (abstract verified) is a Monte Carlo simulation based on the classification error of *wearable* studies. It supports "can translate into poor parameter estimates" as a population-level simulation result. Say so (L153 already does).
  3. Vainikka et al. (ref. [18]) introduce an epoch-level "Hypnodensity Interval". Given the name, one sentence distinguishing it from per-night parameter intervals would avoid confusion. The authors' own working notes flag this (`literature_review_and_journal_benchmark.md` L72, L106).

**D-12 (MINOR): The generality of "any stager" is asserted, not tested.** `[FIXABLE-IN-REPO]` for wording.
- *Location*: L50, L62, L153, L161 (iv).
- *Problem*: both stagers use the same 116 YASA features. Deep stagers that output hypnodensity (U-Sleep, ref. [4]; SOMNUS in ref. [10]) have different calibration and temporal context, so the fitted τ ≈ 0.1 (L117) need not carry over. YASA on SC also runs on a derivation (Fpz-Cz) different from the central derivation YASA's authors recommend (L62 notes only the HMC side). Card focus 5.
- *Fix*: say "applicable to any stager that outputs epoch probabilities; evaluated for two feature-based stagers". Note the montage of the SC input to YASA.

**D-13 (MINOR): The AASM version for HMC is unverified.** `[FIXABLE-IN-REPO]`
- *Location*: L56 cites Berry et al. 2017 (v2.4) for HMC scoring. I could not confirm from the abstracts which manual version HMC used [unverified].
- *Fix*: state the version from the HMC descriptor, or cite the AASM manual generically.

**D-14 (MINOR): The clinical context of HMC is under-described.** `[FIXABLE-IN-REPO]`
- *Location*: L56, Table 1.
- *Problem*: "various sleep disorders" without the mix of diagnoses (for example the share with OSA). Respiratory-event arousals fragment sleep and drive the WASO and N1 errors.
- *Fix*: state what the descriptor reports about the case mix, or state that it reports none.

### Detailed Comments (agent template)

#### Literature Review
- **Reference date**: `unknown`. The manuscript states no version date; the protocol in S1 is dated 2026-11-15. Coverage date: 2026-11-21 (review date).
- **Coverage**: Epoch-level UQ, hypnodensity, scorability and posterior sampling are well covered ([12]–[25]). Thin areas: inter-scorer agreement on *night-level parameters* (only [1] and [2], both epoch-level in focus); multi-scorer datasets and consensus scoring; the effects of rule set and derivation on staging (only [46]); and cross-database degradation (ref. [33] is cited only as a data source).
- **Integration quality**: The Introduction is a focused synthesis, not a list. The Discussion contrasts the work with prior work, but compresses the van Gorp contrast inaccurately (D-6).
- **Research gap argument**: Convincing once rephrased as "adaptive, calibrated per-night intervals with empirical coverage at the deploying site" (D-1). It is unconvincing as "LoA say nothing about individual nights".

#### Theoretical Framework
- **Appropriateness**: The scoring-standards framework is used correctly for TST, SOL and REML, and incompletely for WASO, MT and the R&K/AASM mapping (D-4, D-7, D-8).
- **Application depth**: Rule-set and derivation theory is invoked to explain the transport failure without quantitative engagement (D-2).
- **Alternative frameworks**: An inter-scorer (multi-rater) reference framework (van Gorp; Bakker; Guillot) is the natural alternative definition of "truth" and should be discussed (D-3).

#### Academic Argument Quality
- **Factual accuracy**: LoA characterisation (D-1); van Gorp characterisation (D-6); S16 contradicts §2.2 (D-7).
- **Argument logic**: "Montage did not explain → population or rules" is a leap (D-2). The step from "decided nights more accurate" to "decision support" ignores that the plug-in is already 97.2 % accurate on those nights (D-5).
- **Terminology precision**: WASO undefined (D-4); R&K stages labelled N1–N3 (D-8); "valid" unscoped (D-3).

#### Contribution to the Field
- **Incremental contribution**: A practical, stager-agnostic recipe to attach calibrated per-night intervals to TST. A clear demonstration that local recalibration fixes systematic TST bias. A useful negative result: neither LoA nor intervals transport between cohorts.
- **Positioning**: Correct at L46, overstated at L153 (D-6).
- **Overclaiming**: Moderate. "Valid" (D-3), "long recordings" (D-4), "threshold decisions" (D-5). The authors already narrowed the main claims to TST, which is to their credit.

#### Missing Key References
Each existence was checked via Crossref (DOI resolved; first authors, journal and year match). Content checks are noted per item.
- Lee YJ et al. 2022, J Clin Sleep Med 18:193–202. Meta-analysis of inter-rater κ by stage; quantifies the single-scorer issue (D-3). Abstract verified.
- Norman RG et al. 2000, Sleep 23(7). Inter-centre agreement on scoring in a large dataset (D-3). Content from my knowledge; [unverified detail].
- Younes M et al. 2016, J Clin Sleep Med 12:885–894. Sources of inter-scorer variability (D-3). Content from my knowledge; [unverified detail].
- Guillot A et al. 2020, IEEE TNSRE 28:1955–1965. Public multi-scored datasets (DOD-H/DOD-O) that make the D-3 test possible.
- Cesari M et al. 2021, J Clin Sleep Med 17:1237–1247. Two-centre human vs AI agreement; human κ 0.66 between centres. Abstract verified (D-2, D-3).
- Fiorillo L et al. 2023, npj Digit Med 6. U-Sleep's resilience to non-recommended derivations; relevant to the montage argument (D-2, D-12). Abstract verified.
- Menghini L et al. 2021 (online 2020), Sleep 44:zsaa170. Standardised framework for validating sleep parameters, centred on Bland–Altman analysis (D-1). Abstract verified.
- Vgontzas AN et al. 2013, Sleep Med Rev 17:241–254. Source for TST < 6 h (D-5).
- Lichstein KL et al. 2003, Behav Res Ther 41:427–445. Source for the SOL/WASO > 30 min criteria (D-5). Content [unverified detail].
- Andlauer O et al. 2013, JAMA Neurol 70:891. Source for nocturnal REML ≤ 15 min (D-5). Abstract verified.
- Punjabi NM et al. 2015, Sleep 38:1555–1566. Night-level validation of PSG autoscoring (D-10). Content [unverified].
- Search lead, `[UNVERIFIED]`: other conformal approaches to sleep staging beyond ConMIL. My Crossref and PubMed searches returned none that I could confirm.

#### Later Work the Authors May Want to Note
- None

~~~yaml suggested-references
- title: "Interrater reliability of sleep stage scoring: a meta-analysis"
  authors: ["Lee, Y.J.", "Lee, J.Y.", "Cho, J.H.", "Choi, J.H."]
  year: "2022"
  doi: "10.5664/jcsm.9538"
  arxiv_id: null
- title: "Interobserver Agreement Among Sleep Scorers From Different Centers in a Large Dataset"
  authors: ["Norman, R.G.", "Pal, I.", "Stewart, C.", "Walsleben, J.A."]
  year: "2000"
  doi: "10.1093/sleep/23.7.1e"
  arxiv_id: null
- title: "Staging Sleep in Polysomnograms: Analysis of Inter-Scorer Variability"
  authors: ["Younes, M.", "Raneri, J.", "Hanly, P."]
  year: "2016"
  doi: "10.5664/jcsm.5894"
  arxiv_id: null
- title: "Dreem Open Datasets: Multi-Scored Sleep Datasets to Compare Human and Automated Sleep Staging"
  authors: ["Guillot, A.", "Sauvet, F.", "During, E.H.", "Thorey, V."]
  year: "2020"
  doi: "10.1109/tnsre.2020.3011181"
  arxiv_id: null
- title: "Interrater sleep stage scoring reliability between manual scoring from two European sleep centers and automatic scoring performed by the artificial intelligence-based Stanford-STAGES algorithm"
  authors: ["Cesari, M.", "Stefani, A.", "Penzel, T.", "Ibrahim, A."]
  year: "2021"
  doi: "10.5664/jcsm.9174"
  arxiv_id: null
- title: "U-Sleep's resilience to AASM guidelines"
  authors: ["Fiorillo, L.", "Monachino, G.", "van der Meer, J.", "Pesce, M."]
  year: "2023"
  doi: "10.1038/s41746-023-00784-0"
  arxiv_id: null
- title: "A standardized framework for testing the performance of sleep-tracking technology: step-by-step guidelines and open-source code"
  authors: ["Menghini, L.", "Cellini, N.", "Goldstone, A.", "Baker, F.C."]
  year: "2021"
  doi: "10.1093/sleep/zsaa170"
  arxiv_id: null
- title: "Insomnia with objective short sleep duration: The most biologically severe phenotype of the disorder"
  authors: ["Vgontzas, A.N.", "Fernandez-Mendoza, J.", "Liao, D.", "Bixler, E.O."]
  year: "2013"
  doi: "10.1016/j.smrv.2012.09.005"
  arxiv_id: null
- title: "Quantitative criteria for insomnia"
  authors: ["Lichstein, K.L.", "Durrence, H.H.", "Taylor, D.J.", "Bush, A.J."]
  year: "2003"
  doi: "10.1016/s0005-7967(02)00023-2"
  arxiv_id: null
- title: "Nocturnal Rapid Eye Movement Sleep Latency for Identifying Patients With Narcolepsy/Hypocretin Deficiency"
  authors: ["Andlauer, O.", "Moore, H.", "Jouhier, L.", "Drake, C."]
  year: "2013"
  doi: "10.1001/jamaneurol.2013.1589"
  arxiv_id: null
- title: "Computer-Assisted Automated Scoring of Polysomnograms Using the Somnolyzer System"
  authors: ["Punjabi, N.M.", "Shifa, N.", "Dorffner, G.", "Patil, S."]
  year: "2015"
  doi: "10.5665/sleep.5046"
  arxiv_id: null
- title: "Agreement in Computer-Assisted Manual Scoring of Polysomnograms across Sleep Centers"
  authors: ["Kuna, S.T.", "Benca, R.", "Kushida, C.A.", "Walsh, J."]
  year: "2013"
  doi: "10.5665/sleep.2550"
  arxiv_id: null
~~~

### Citation spot-check log (20 checked)
| Ref (rendered no., key) | Sentence (line) | Verdict | Basis |
|---|---|---|---|
| [1] rosenberg2013, [2] dankerhopfe2009 | scorer-level agreement (L42) | supports | titles/known content |
| [3] stephansen2018, [4] perslev2021, [5] vallat2021 | stagers reach scorer-level agreement (L42) | supports | known content |
| [6] svensson2024 | LoA used in validation (L42) | supports (wearable, see D-10) | abstract |
| [7] beau2025 | same | supports (wearable) | abstract |
| [8] kaneda2026 | same | supports | abstract (LoA TST ±0.5 h) |
| [9] baumert2023 | errors vary across populations (L44) | supports | abstract ("significant errors in clinical markers ... individual PSG") |
| [10] deirossi2025 | same | supports (demographic/clinical bias) | abstract |
| [11] hardarson2023 | epoch errors → poor parameter estimates (L44) | supports, with nuance (simulation; wearables) | abstract |
| [18] vainikka2026 | epoch-level UQ (L46) | supports | abstract |
| [19] bakker2023 | hypnodensity display (L46) | supports | abstract |
| [20] li2025conmil | conformal sets for single epochs (L46) | partial (D-11) | abstract |
| [22] ganglberger2024 | night-level scorability (L46) | supports | abstract |
| [24] vangorp2023jbhi | distributions reflecting inter-rater disagreement (L46) | supports | abstract |
| [24] vangorp2023jbhi | "without calibrating it against a scorer" (L153) | does not support (D-6) | abstract |
| [25] philips2024patent | thresholds spread to flag parameters (L46) | supports | Google Patents abstract and claims; status withdrawn |
| [33] alvarez2021 | HMC source (L56) | supports; also relevant to D-2 | abstract |
| [46] moser2009 | R&K vs AASM differences (L101) | supports; effect size argues against L135's attribution | PubMed abstract |

### Questions for Authors
1. What WASO definition was used? Does the SC result survive a recording-period definition, or an SC window ending at a label-free end-of-sleep proxy?
2. How many technicians scored each cohort, and is scorer identity available for HMC?
3. Can YASA be run on F4-C4 (bipolar, derived from cached signals) to approximate SC's Fpz-Cz?
4. Does the SC N3 bias vary with age? How many SC nights with 0 % reference S3+S4 are among the non-covered N3 % nights?
5. Which AASM manual version was used for HMC?

### Minor Issues
- L117: "τ ≈ 0.1 ... strongly down-weighted emissions". A clinical reader needs one sentence on what this means for how sharp the sampled hypnograms are.
- Table 1: stage percentages are of scored window epochs, including wake, whereas the parameters in Tables 2–3 are percentages of TST. Say so in the caption.
- The rendered PDF now lists 50 references ([1]–[50], with Vainikka et al. cited as [18]), not the 49 recorded in Phase 0. This is exactly at the author-stated limit of 50, so any reference added in response to this report must be offset by a removal. `references.json` still contains the uncited `rohrscheib2026` (HSAT apnea scoring). It is not relevant here and need not be added.
- The Phase 0 card cites "ref. [19]" for the conformal claim. In the current PDF that reference is [20], because Vainikka et al. is now cited as [18].

---
### Final summary for the panel
- **Recommendation**: Major Revision (confidence 4/5).
- **Three issues most likely to cause rejection**: (1) LoA mischaracterised as saying "nothing about individual nights", making the central comparison read as a strawman (D-1). (2) The single-scorer reference behind "valid per-night error ranges", without a multi-scorer check (D-3). (3) Transport failure attributed to population or scoring rules on evidence that cannot separate them (D-2).
- **Three strongest domain points**: (1) Label-free, leakage-aware windows and parameter pipeline. (2) Honest, mechanistically explained parameter-specific results, including the WASO failure. (3) A practical finding that local recalibration on about 10 nights removes most of the automatic TST bias.
