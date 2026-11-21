# Perspective Review Report (Peer Reviewer 3)

ARS `academic-paper-reviewer`, Phase 1 (Reviewer Panel), Peer Reviewer 3 seat, configured by Reviewer Configuration Card #4 (`phase0_field_analysis.md`). Pipeline run `ars-p_c1_4-2026-11-20-a`, Stage 3 (full review). Written without opening any other reviewer's output. The only file read in `stage3_review/` was the Phase 0 report. The manuscript and the repository were not modified.

Criteria binding: `criteria_binding_unavailable`. No `ReviewCriteriaBindingManifest` or Target Criteria Brief was supplied. The judgements below apply the shared framework (`references/review_criteria_framework.md`) and Card #4 to *Sleep Medicine*, Original Article, as the authors state the target.

**Material read.** `manuscript/build/manuscript_rendered.md` (all 299 lines; `Lnnn` refers to this file); Figs. 1–5 (PNG, viewed); Supplementary S1 in full, plus the S8, S13 and S15 headers and tables and S16; `tables/tableS_decisions.csv`, `tables/tableS_fewshot_risk_yasa.csv`, `results/statistics/e15_local.csv`, `results/summaries/yasa_xfit.csv`; `code/experiments/e09_robustness.py` (corruption generator). I consulted `stage2_5_integrity/reverification_round1.md` only after forming my own view, so as not to repeat resolved items. Its one open MEDIUM, the 97.2 %/61 % figures missing from §3.7, is now fixed: L143 carries them.

**Reviewer's own computations** (marked as such where used; plain pandas, independent of the authors' scripts):
(a) Accuracy at the TST < 6 h threshold when the calibrated plug-in classifies every night. This uses the per-night pre-specified-design summaries (`yasa_xfit.csv`), not the end-to-end protocol, so it is indicative only.
(b) Workload per 1,000 nights, derived from `tableS_decisions.csv`.
(c) The binomial floor of the "site-level risk" metric for the test-set sizes used in ST.
(d) The closed-form distribution of conditional coverage for split conformal under exchangeability (Beta(n+1−l, l), l = ⌊(n+1)α⌋).

---

### Reviewer Identity
Health-informatics and implementation-science researcher. I study how AI-based clinical decision-support and scoring software is introduced and monitored after deployment in hospital diagnostic services, sleep-laboratory workflows among them, and I have worked on performance evaluation of software as a medical device. My focus is what a site must do, at what cost and for whom, to use a method safely, and how clinicians read uncertainty statements. I am not a conformal-prediction theorist or a scoring-rules specialist. Where my comments touch statistics or scoring conventions, I raise them only for their practical consequences and defer to Reviewers 1 and 2 on the technical substance.

### Overall Recommendation
**Major Revision**

### Confidence Score
4 (scope: deployment, workflow, communication and evidence coverage. I did not check the conformal derivations, the HMM construction or the scoring conventions.)

Confidence is an uncertainty/scope disclosure only; it never changes consensus counts, severity, decision bearing, or arbitration.

### Calibration Status
`NOT_CALIBRATED`

### Criterion-Bound Judgements
| Dimension / criterion | Criterion source | Judgement | Evidence anchors | Rationale | Uncertainty or scope limit | Decision bearing? |
|---|---|---|---|---|---|---|
| Significance & Impact (practical value for the stated clinical audience) | Framework §1; Card #4 focus 1, 3 | PARTLY_MEETS | L44; L143; L159; `tableS_decisions.csv`; Table 2 widths | The TST advantage is real against Bland–Altman limits, but it is small against the simpler distribution-free alternative calibrated on the same nights: 59.2 % vs 56.9 % of HMC nights decided at TST < 6 h. The benefit is never expressed as workload. | The size of the workload benefit depends on lab policy, which the paper does not state | yes: the clinical takeaway is the paper's case for a clinical journal |
| Evidence Sufficiency (for the practice recommendation "≥ 20 local nights; review wide/straddling nights") | Framework §1; Card #4 focus 2, 3, "will particularly care about" | DOES_NOT_MEET | L137; L159; L166; Fig. 3c, f; `e15_local.csv` | In ST, the site-risk metric is dominated by binomial noise from small test sets. The HMC curve is flat from 10 to 30 nights. No review rule (width threshold, flag rate) is given. | Rests on the reviewer's computations (c), (d) | yes |
| External validity (populations, settings, devices) | Framework §2.1; Card #4 focus 1 | PARTLY_MEETS | L56; Table 1; L161 (iv); S16 Datasets table | Three cohorts. Two are analogue recordings from 1987–1994; one contemporary clinical cohort has no demographics; no children, no home sleep testing, no wearables, no deep-learning stagers. The limitations section discloses part of this, but the scope of the claims does not narrow to match. | none identified | yes, for the wording of the claims; it does not block the method contribution |
| Conclusion conservatism (title, highlights, abstract, conclusion vs results) | Framework §2.1; Card #1 focus 3 overlap, from the practice angle | PARTLY_MEETS | L22; L35; L44; L166 vs L120–122, L137 | The word "valid" for per-night intervals goes unqualified: coverage is marginal, within cohort and empirical, and 7–17 % of sites fall below 80 %. "With 90 % confidence" (L44) invites a per-night probability reading. Most other framing is commendably narrowed (TST-specific; transport failure stated). | none identified | yes, but text-fixable |
| Writing quality: clinical communicability of the uncertainty statement and figures | Framework §1; Card #4 focus 4 | PARTLY_MEETS | Abstract L31–33; Fig. 1d–f; Fig. 2; Fig. 3c; L108 | Dense jargon (FFBS, CQR, Mondrian, CV+, interval score). Efficiency is reported in a unitless score. Fig. 1e places a posterior histogram beside the conformal interval, which invites a credible-interval reading. | Judged from a clinician-reader standpoint | no on its own; it compounds the significance concern |
| Post-deployment monitoring / drift | Card #4 focus 2 | DOES_NOT_MEET | L135; L137; L159; L161 (ii) | The paper shows silent failure under transport (N3 % coverage 38 %) but gives a site no way to detect loss of validity after start-up. | none identified | yes |
| Robustness realism | Card #4 focus 5 | PARTLY_MEETS | L103; L146; Fig. 4; `e09_robustness.py` `corrupt()` | Artefacts are placed in random epochs, drawn separately for EEG and EOG, independent of stage. Gaussian noise reaches 0 dB SNR. No advice is given for degraded nights. | Read from the code, not from runs | no (secondary analysis), but it carries a safety implication |
| Open science / reproducibility (reader's view) | Framework §1 (Evidence Sufficiency); Card #4 | MEETS | L111; L195; S1 deviations log; S16 | An end-to-end pipeline from public data, a candid deviation log and a leakage audit. Weaknesses: code deposit deferred to acceptance; a 1.4 MB machine-table supplement. | Code not executed by this reviewer | no |
| Stakeholder coverage (who benefits, who pays, who is missing) | Phase 0 Stakeholder Coverage; Card #4 focus 1 | PARTLY_MEETS | L44; L159; L161 (iii), (iv); Table 1 | Labs and clinicians are named as beneficiaries. Scorers' workload, patients exposed to confident-but-wrong decisions, and populations outside the cohorts are not discussed. | none identified | no on its own |

### Summary Assessment
The manuscript asks a question that matters for anyone running an AI scorer in a sleep laboratory: can a single automatically scored night carry an honest error range in clinical units? Its answer is careful and, unusually, self-limiting. The advantage over limits of agreement is confined to TST. The authors state that cross-cohort transport fails, and that local calibration restores coverage only on average. The deviation log (S1) is a model of candour.

From a deployment standpoint the paper stops short of what a laboratory needs in order to act. The recommended workflow (L159) gives no review rule (what counts as "wide"?) and no workload estimate. It does not compare against the simplest credible alternative a lab would actually run: recalibrate, then apply distribution-free limits on the same local nights. The decision baseline is the uncorrected plug-in, not the recalibrated one that the authors' own workflow produces. The "at least 20 nights" recommendation rests partly on ST numbers that mostly reflect the binomial noise of 14–34 test nights rather than calibration quality. No monitoring plan exists for a method whose central finding is that validity is local and can fail silently. The phrase "90 % confidence" for a single night (L44) and the unqualified "valid" (Highlights, Abstract, Conclusion) will be read by clinicians as a per-night probability guarantee, which the design does not provide.

All of this can be fixed from existing results and text, apart from broader population coverage. With those changes the paper would give *Sleep Medicine* readers a usable, correctly scoped practice message.

### Strengths
1. **Honest, narrowed framing of the comparative claim.** The abstract and conclusion state that the gain over limits of agreement is "clear for TST, absent for most others" and that "validity requires local calibration" (L35, L166). WASO's failure in long recordings is analysed mechanistically rather than hidden (L140, L157). This is rare in AI-scoring papers and it protects clinicians from over-generalising. Evidence anchor: `manuscript: L35, L127, L157, L166`.
2. **Deployment-shaped evaluation.** Every label-dependent component is fitted on the calibration nights alone "as a laboratory would deploy the method" (L95). Few-night local calibration and cross-cohort transport are tested explicitly (L99–101, L135–137). The site-level probability of realised coverage below 80 % is reported, not only mean coverage (L137). That metric is exactly the right instinct for implementation, even though its current estimate needs rework (P-3). Evidence anchor: `manuscript: L95, L99, L137; Fig. 3c, f`.
3. **Transparency and reproducibility.** There is a dated deviation log with reasons (S1, items 1–15), including the admission that the repository cannot independently date the protocol. There is a leakage audit (S16), a pipeline that regenerates every number from public data (L111), and explicit disclosure of generative-AI involvement (L111, L171). A reader or a laboratory can audit and reproduce the work. Evidence anchor: `supplement: S1 "Deviations"; S16; manuscript: L111, L195`.
4. **Negligible compute cost.** Sampling and parameter computation take 0.02 s per night against 1.4 s for the stager (L146; S15), so compute is not an adoption barrier. Evidence anchor: `supplement: S15`.

### Weaknesses
1. **The practice workflow is neither operational nor quantified in workload terms** (P-1, P-2, P-10).
   - **Severity**: Major | **Evidence Anchor**: `manuscript: L143, L159; data: tables/tableS_decisions.csv` | **Confidence**: 4. Reading tables and lab workflow is within my competence.
2. **The "≥ 20 local nights" recommendation is not supported by the analysis cited** (P-3).
   - **Severity**: Major | **Evidence Anchor**: `manuscript: L137, L159; data: results/statistics/e15_local.csv` | **Confidence**: 4. Rests on standard binomial and Beta calculations; Reviewer 1 should confirm.
3. **No post-deployment monitoring or drift detection** (P-4).
   - **Severity**: Major | **Evidence Anchor**: `manuscript: L135, L159, L161` | **Confidence**: 5. This is the core of my field.
4. **The 90 % interval is open to clinical misreading, and "valid" is stated more strongly than the evidence supports** (P-5, P-6).
   - **Severity**: Major | **Evidence Anchor**: `manuscript: L22, L35, L44, L166; Fig. 1e` | **Confidence**: 4.
5. **The evidence base is narrow relative to the implied scope, and the under-covered hard nights are uncharacterised** (P-7).
   - **Severity**: Major | **Evidence Anchor**: `manuscript: L56, L122, L161 (iv); Table 1; supplement: S16` | **Confidence**: 4.
6. **The robustness simulation has limited realism, and no guidance is given for degraded recordings** (P-8).
   - **Severity**: Major | **Evidence Anchor**: `manuscript: L103, L146; code: code/experiments/e09_robustness.py corrupt()` | **Confidence**: 4.

---

## Numbered comments

### MAJOR

**P-1 (MAJOR) The recommended workflow has no review rule and no workload figure. The headline decision figure is pooled across cohorts and hides the clinical cohort.**
*Location:* L33 (Abstract Results), L143 (§3.7), L159 ("Implications for practice"), Fig. 5e; `tables/tableS_decisions.csv`.
*Problem and why it matters.* L159 tells a laboratory to "review nights whose interval is wide or straddles a decision threshold". No width threshold is defined, and no expected review rate is given. For a decision to adopt, the relevant quantity is how many nights fall to manual review and how many wrong automatic decisions remain. The abstract's 64 % decided at TST < 6 h is pooled over HMC, SC and ST. ST is a small cohort with 4.9 % prevalence and 92.6 % decided, which inflates the pooled figure.

In HMC, the only contemporary clinical cohort (40.6 % prevalence), the proposed intervals decide 59.2 % of nights (98.9 % correct). Distribution-free limits decide 56.9 % (98.3 %) and Bland–Altman limits 44.6 % (97.4 %) (`tableS_decisions.csv`). Per 1,000 HMC nights (reviewer's computation (b)):

| Method | Nights to review | Wrong automatic decisions |
|---|---|---|
| Proposed | ≈ 408 | ≈ 6.5 |
| Distribution-free limits | ≈ 431 | ≈ 9.7 |
| Bland–Altman limits | ≈ 554 | ≈ 11.6 |

The gain over the method validation studies currently report (Bland–Altman) is substantial: about 146 fewer reviews per 1,000 nights. The gain over the simple alternative calibrated on the same nights is about 23 fewer reviews and 3 fewer errors per 1,000 nights. Readers need both numbers to decide whether the extra machinery (HMM, FFBS, temperature fitting) is worth adopting. Implementation science consistently finds complexity to be a barrier to adoption.

*Fix.*
(i) Report the decision results per cohort in §3.7, and give the HMC figure in the abstract alongside or instead of the pooled one.
(ii) Add a short table, "workload per 1,000 nights", for each threshold, with columns for nights to review, residual wrong decisions, and false-reassurance decisions (a confident "normal" call where the reference is abnormal). Include it for proposed, distribution-free limits, Bland–Altman limits and calibrated plug-in (see P-2).
(iii) Turn L159 into an explicit protocol: how many nights to score, which components to fit, which nights to review (straddling a threshold; width above a stated percentile of the calibration-set widths), and what to report.
`[FIXABLE-IN-REPO]`

**P-2 (MAJOR) The automatic-decision baseline is the uncorrected plug-in, but the authors' own workflow recalibrates first.**
*Location:* L33 ("automatic TST on the same nights 97.2 %, elsewhere 61 %"), L143 ("classifying every night by its plug-in TST was correct for 84.2 %"), Fig. 5 caption, dotted line ("uncorrected automatic value"); S8 caption.
*Problem and why it matters.* Step (ii) of the recommended workflow (L159) recalibrates the stager's probabilities on the local nights, which "by itself removed most of the TST bias" (L132; Table 3: HMC bias −38.3 → −5.2 min). A laboratory that has done step (ii) would compare the intervals against the recalibrated plug-in, not the raw one.

In the per-night pre-specified-design summaries (`results/summaries/yasa_xfit.csv`; reviewer's computation (a), indicative only because it is not the end-to-end protocol), the recalibrated plug-in classifies TST < 6 h correctly in:

| Cohort | Calibrated plug-in | Raw plug-in |
|---|---|---|
| HMC | 90.7 % | 84.1 % |
| SC | 89.5 % | 82.4 % |
| ST | 100 % | 88.6 % |
| All | 91.4 % | 83.9 % |

The 84.2 % baseline therefore overstates the added value of the intervals relative to what a lab following the paper would have. Fig. 5e's visual gap (dotted line at 0.84) will be read as the benefit of the intervals.
*Fix.* Add the calibrated plug-in, fitted on the calibration half under the end-to-end protocol, as a baseline in S8, in Fig. 5e–h (a second dotted line) and in §3.7. State in the abstract which plug-in the 97.2 %/61 % figures refer to. The pipeline already computes `plugc_*` per night (`code/src/uncertainty/night_summary.py`), so this needs a re-run, not new data.
`[FIXABLE-IN-REPO]`

**P-3 (MAJOR) The evidence for "at least 20 locally scored nights" is confounded by test-set size and Monte-Carlo noise. A closed-form answer is available.**
*Location:* L137, L159 ("We therefore suggest at least 20 … even 30 left a risk of 15 % in the small ST cohort"), L166, Fig. 3c, f; `results/statistics/e15_local.csv`.
*Problem and why it matters.* "Realised coverage of the remaining nights" depends on how many nights remain. ST has 44 nights, so n_t = 10/20/30 leaves 34/24/14 test nights. Even with perfect calibration and exactly 90 % true coverage, the probability that observed coverage falls below 80 % is 4.8 %, 8.5 % and 15.8 % for 34, 24 and 14 test nights (reviewer's computation (c), exact binomial). The reported ST risks of 17 %, 15 % and 15 % (L137) therefore largely measure the binomial noise of a tiny audit set, not a property of a site's calibration. The statement that "even 30 left a risk of 15 %" (L159) is mostly this artefact.

In HMC, where 121–141 nights remain and the binomial floor is ≈ 0, the risk is flat: 9 %, 7 %, 7 %. With only 50 repetitions, each estimate has a Monte-Carlo SE of about 4 percentage points, and the per-parameter values behind "up to 26 %" (L159; N2 % in ST at n_t = 10, `e15_local.csv`) carry the same noise.

A laboratory needs the probability that *its* calibration yields long-run coverage below a tolerance. For split conformal under exchangeability this has a known closed form. Conditional coverage follows Beta(n+1−l, l) with l = ⌊(n+1)α⌋. At α = 0.10 this gives P(coverage < 0.80) ≈ 10.7 %, 6.9 %, 4.4 % and 1.8 % for n = 10, 20, 30 and 50 (reviewer's computation (d)). These values closely match the HMC empirical 9 %, 7 % and 7 %. The design here is cross-fitted rather than pure split conformal (L88), so the match is a sanity check, not a guarantee. Reviewer 1 should confirm.
*Fix.*
(i) Base the site-risk estimate on long-run coverage: evaluate on a large held-out set (HMC), or report the analytical Beta curve alongside the empirical HMC curve.
(ii) Drop or caveat the ST-based "15 % at 30 nights" statement.
(iii) Give a small table of n against risk at the 80 % and 85 % tolerances, so a site can choose n for its own risk appetite, and state plainly that at n = 20 roughly 1 site in 14 will run below 80 %.
(iv) Increase the repetitions for the local-deployment curves, or report Monte-Carlo SEs.
`[FIXABLE-IN-REPO]`

**P-4 (MAJOR) No plan for detecting loss of validity after deployment.**
*Location:* L135–137 (transport failure; site variability), L159, L161 (ii), L166.
*Problem and why it matters.* The paper's most clinically important negative result is that validity is local and fails silently. N3 % coverage was 38 % when SC calibration was applied to HMC, and TST coverage was 51 % for LightGBM (L135). A laboratory has no way to know whether it is among the 7–9 % of sites below 80 % at start-up, or when a later change breaks exchangeability: a new referral mix (for example a paediatric or neuromuscular service), a new amplifier or montage, a new scorer, a scoring-rule update, or a stager software update. The paper recommends one-off local calibration but no monitoring. In deployed AI diagnostics, the absence of a monitoring plan is a recognised safety gap: post-market performance monitoring is expected under device-evaluation frameworks.
*Fix.* Add a "Monitoring" paragraph to §4 that specifies:
- an ongoing audit: manually score a random k nights per month, and track running coverage per parameter with a binomial confidence interval or a CUSUM/Shewhart-type chart, by analogy with laboratory-medicine QC rules;
- label-free drift signals the method already produces: the distribution of σ̂, mean epoch entropy, and the |raw − calibrated plug-in| difference (L105, L146);
- explicit recalibration triggers (equipment, montage, scorer, scoring-manual, population or software changes);
- optionally, adaptive or online conformal updating as a future direction.

A pseudo-prospective demonstration is possible from existing data. One option: show whether the label-free signals move when SC-calibrated intervals meet HMC (where coverage is known to collapse). Another, if the HMC record order is chronological `[unverified]`: calibrate on the first n recordings and audit the rest.
`[FIXABLE-IN-REPO]`

**P-5 (MAJOR) How a clinician will read a "90 % interval": per-night probability language, marginal coverage, a single scorer, and multiplicity across eight parameters.**
*Location:* L44 ("for this night, TST lies within [a, b] min with 90 % confidence"), L122 (84.7 % in the hardest quartile), L161 (i), (iii), Fig. 1e, f.
*Problem and why it matters.* The guarantee is marginal and empirical. Across a site's nights, about 90 % of intervals contain the single scorer's value. For the hardest quartile of nights it is about 85 % (L122). For an individual night it is not a 90 % probability. Clinicians, and many informaticians, read "90 % confidence" for a specific night as a Bayesian credible statement ("90 % probability TST is in here").

Fig. 1e/f reinforce this reading by drawing the FFBS posterior histogram next to the conformal interval. In Fig. 1e the histogram spans about 430–460 min while the interval spans about 417–478 min, and nothing in the figure says why they differ. The reference is one scorer's value (L161 (iii)), not "true" TST. A night report would also carry eight intervals. At 90 % marginal coverage each, a reader should expect roughly 0.8 misses per night on average, so "one of the intervals was wrong" will be a common experience that erodes trust unless explained.
*Fix.*
(i) Rewrite L44 to avoid per-night probability language, for example: "an interval that, across nights scored at this laboratory, contains the scorer's value 90 % of the time".
(ii) Add a short plain-language box or paragraph in §4: what the interval means and does not mean; lower coverage on difficult nights; the single-scorer reference; multiplicity across parameters.
(iii) In Fig. 1e/f, label the histogram as "model posterior (uncalibrated)" and say in the caption why the calibrated interval differs.
(iv) Consider "error range" or "90 % prediction interval" consistently, never "confidence".
`[FIXABLE-IN-REPO]`

**P-6 (MAJOR) The headline claims are stronger than the results. Absolute interval widths, which decide clinical usefulness, are missing from the abstract.**
*Location:* Highlight 2 (L22, "gave valid per-night 90 % intervals"); Abstract Conclusions (L35, "give valid per-night error ranges"); Conclusion (L166); compare L120–122, L137, L88 ("validity is therefore an empirical property"); Table 2 widths.
*Problem and why it matters.* "Valid" without qualification will be read clinically as "trustworthy for this night". The results support something narrower:
- marginal, not per-night, coverage;
- within cohort;
- assessed empirically, since the design has no distribution-free guarantee (L88);
- after local calibration, with a 7–17 % chance that a site's realised coverage falls below 80 % (L137);
- under-coverage of the hardest nights (L122).

The abstract never states how wide the intervals are. Table 2 shows mean TST widths of 90 min in SC and 91 min in HMC (±45 min), 39 min in ST, REM-latency widths of 94–178 min, and WASO in SC of 237 min. A ±45-min TST interval leaves every night with TST between about 5¼ and 6¾ h undecided at the 6-h threshold. REM-latency intervals of 2–3 h are practically uninformative for SOREMP decisions (see P-11). Clinicians need these numbers to judge usefulness, and a reader of the abstract alone cannot judge it.
*Fix.* Qualify "valid" in Highlight 2, Abstract Conclusions and §5. For example: "reached nominal average coverage within cohorts when calibrated on local nights". Add median TST width (HMC) to the Abstract Results. Add one sentence to §4 on which parameters have widths narrow enough to support decisions.
`[FIXABLE-IN-REPO]`

**P-7 (MAJOR) Who the evidence covers and who it leaves out; the hardest nights are not characterised.**
*Location:* L56, Table 1, L122, L161 (iv); S16 Datasets table.
*Problem and why it matters.* The three cohorts are:
- SC: healthy adults, analogue ambulatory PSG recorded 1987–1991, R&K scoring.
- ST: 22 adults with mild sleep-onset difficulty, placebo/temazepam nights, recorded 1994.
- HMC: one Dutch clinical centre, 2018, AASM scoring, no demographics or diagnoses released.

All three appear to come from Dutch centres (`[unverified]` for the Sleep-EDF origin). The following are absent: children and adolescents; disease-specific groups with characteristically fragmented or atypical sleep (severe OSA, neurodegenerative disease, narcolepsy, which is the population for the REM-latency threshold); home sleep testing; reduced-montage, wearable or forehead-EEG devices; deep-learning stagers; and stagers whose clinical deployment versions may not export epoch probabilities at all (`[unverified]` for specific commercial products).

The under-covered hardest nights (84.7 % coverage, L122) are plausibly those of the sickest or oldest patients, whose misclassification matters most. The paper does not describe who they are, and HMC subgroup analysis is impossible without demographics. Limitations (iv) lists size, age and stager type, but the claims elsewhere ("for automatically scored sleep parameters", L35, L166) are not scoped to match.
*Fix.*
(i) Add an explicit intended-use and scope statement: adult, laboratory PSG, stagers that output epoch probabilities, EEG+EOG montage.
(ii) Characterise the lowest-accuracy quartile with the variables available: cohort, age and sex in SC/ST, reference TST, sleep efficiency, WASO, N1 %. This shows whether under-coverage concentrates in older or more fragmented sleepers.
(iii) Name home and wearable recordings, paediatrics and disease-specific cohorts as untested.
Broader validation would need new data, and the paper should say so.
`[FIXABLE-IN-REPO]` for (i)–(iii); `[NEEDS-NEW-DATA]` for any claim beyond these cohorts.

**P-8 (MAJOR) The simulated artefacts do not resemble clinical or home-recording artefacts, and nothing tells a lab what to do with degraded nights.**
*Location:* L103, L146, Fig. 4; `code/experiments/e09_robustness.py`, function `corrupt()`.
*Problem and why it matters.* From the code, "movement-artefact drifts" are random-walk drifts (AR coefficient 0.995, 50 µV steps) added to a random 10 % or 25 % of epochs, with the whole signal clipped at ±300 µV. The epochs are chosen uniformly and independently of sleep stage. `corrupt()` is called separately for EEG and EOG with a shared RNG, so the corrupted epochs in EEG and in EOG are drawn independently and generally do not coincide.

Real movement artefacts hit all channels at once and cluster at wake, arousals and position changes, which are exactly the epochs that determine TST, SOL and WASO. Other common clinical failure modes are not represented: electrode detachment and flat-line, sweat sway, ECG contamination, and loss of a channel for part of the night. White Gaussian noise at 1 × robust SD (about 0 dB SNR) is extreme and unlike typical degradation. The claim that adaptive methods lost less coverage "because their width responded to the corrupted signal" (L146) is therefore shown only for an unrealistic generator. Under strong noise, TST coverage of the proposed intervals fell to about 33 % (Fig. 4a) while their width rose only to roughly the width of the limits of agreement. In other words, the method can fail silently on bad recordings, and the paper gives no operational advice.
*Fix.*
(i) Describe the artefact model accurately in §2.7 (independent channels, stage-independent placement) and soften L146 accordingly.
(ii) Recommend a signal-quality gate in the practice section: no interval is reported, or the night is routed to manual review, when a quality check fails.
(iii) Optionally re-run with channel-synchronous, stage-dependent artefacts (for example concentrated in reference wake/arousal epochs) and a channel-dropout scenario. This uses existing data and code.
`[FIXABLE-IN-REPO]`

### MINOR

**P-9 (MINOR) As described, σ̄ cannot be computed prospectively.**
*Location:* L84 (σ̄ is "the median of σ̂ over the calibration and test nights"); S1 item 4.
*Problem.* In routine use, test nights arrive one at a time. A regulariser computed over calibration and test nights would change as nights accumulate, so an already-reported interval could change retroactively, or would differ depending on batch. S1 item 4 says the numerical difference from the calibration-only definition was negligible.
*Fix.* State that a deployed system freezes σ̄ from the calibration nights, and confirm with one line that this changes coverage or width negligibly. `[FIXABLE-IN-REPO]`

**P-10 (MINOR) The flagging result has no operating point, and the simpler flag was better for TST in HMC.**
*Location:* L105, L146, Fig. 5d; L159.
*Problem.* AUROCs of 0.68–0.79 say nothing about how many nights a flag would send to review or what fraction of large errors it would catch. For TST in HMC, the label-free |raw − calibrated plug-in| flag (0.79) beat interval width (0.68), yet the practice section recommends reviewing "wide" intervals.
*Fix.* Report the flag rate and the sensitivity for |ΔTST| > 30 min at one or two fixed review budgets (for example, reviewing the top 20 % of nights). Say which flag the authors recommend for which parameter. `[FIXABLE-IN-REPO]`

**P-11 (MINOR) The clinical thresholds are "chosen by the authors", and the most diagnostic one cannot be served.**
*Location:* L105, L143, Fig. 5h.
*Problem.* TST < 6 h and REM latency ≤ 15 min have recognisable clinical anchors. One example is the minimum nocturnal sleep before an MSLT, and the nocturnal SOREMP counts toward a narcolepsy diagnosis (`[unverified]` exact guideline wording; Reviewer 2's remit for sources). From a workflow angle the key finding is buried: no interval ever lay entirely below 15 min (L143). Every positive SOREMP must therefore go to manual review, so the method cannot reduce workload for the decision where an error has the greatest consequence. The 99 %+ "accuracy" in Fig. 5h is entirely negative decisions at 2.5 % prevalence and should not be presented on the same footing as panel e.
*Fix.* Tie each threshold to a clinical use, and state explicitly in §4 that SOREMP-positive nights remain manual. In Fig. 5h, annotate that all confident decisions are negative. `[FIXABLE-IN-REPO]`

**P-12 (MINOR) No intended-use, clinical-safety or regulatory framing.**
*Location:* §4 "Implications for practice" (L159); Limitations.
*Problem.* The recommended workflow has a site refit the stager's probability calibration, the HMM and the interval quantile. Applied to a regulated scoring product, this amounts to modifying the device's output, which raises questions of responsibility, validation and change control. In the EU and US, frameworks for predetermined change-control of AI-enabled device software apply, though their applicability to this workflow is `[unverified]` and for regulatory experts to judge. YASA itself is research software. Clinicians will ask who is accountable when a "confident" automatic decision is wrong. That is about 1 % of decided nights at TST < 6 h in HMC, which is 6–7 patients per 1,000 nights (P-1).
*Fix.* Add two or three sentences: the method is a research procedure; clinical use needs local validation and governance; residual confident-wrong decisions are expected at about 1 %; and integration with regulated scorers depends on vendors exposing epoch probabilities. `[FIXABLE-IN-REPO]`

**P-13 (MINOR) Hidden assumption: the lab signs off nights without epoch review. Reposition as triage.**
*Location:* L44 ("show when a night can be signed off and when it needs manual review"), L159.
*Problem.* In many accredited laboratories a technologist reviews and edits every autoscored record before a physician reports it (`[unverified]` as a universal rule; practices vary). Under that model the interval's value is in prioritising review effort and quality assurance, and in research cohorts where per-night error bars can be propagated, rather than in removing review. The paper does not consider which deployment model it serves.
*Fix.* Name the use-cases explicitly (triage and QA in clinical labs; uncertainty propagation in research; future home and wearable use, untested) and frame the workload results (P-1) accordingly. `[FIXABLE-IN-REPO]`

**P-14 (MINOR) Communication for a clinical readership.**
*Location:* Abstract L31–33; §2.5–2.8; Figs. 1–3.
*Problem.* The abstract uses "forward-filtering backward-sampling", "interval score", "conformally calibrated" and "cohort–parameter combinations". The 21/23-of-24 sentence (L33) is not meaningful to clinicians, and its space would be better spent on widths and workload. Efficiency is reported only as an interval-score ratio, which has no clinical unit; a width-plus-miss-rate presentation, or "median width at nominal coverage", would be readable.

Figures:
- Fig. 2 plots eight methods in six panels. Its message (TST below 1; others around 1) would be clearer with three comparators in the main figure and the rest in the supplement.
- Fig. 1d's sampled hypnograms have no stage axis labels, so a clinician cannot read them as hypnograms.
- Fig. 3c/f's y-axis label "P(realised coverage < 0.80)" needs plain wording ("chance a site's intervals cover < 80 %").
- Fig. 5 mixes three distinct messages: adaptivity, flagging and decisions.
Section 2.7 interleaves "end-to-end" and "pre-specified design" analyses, which forces the reader to track which design each result comes from (L95).
*Fix.* Simplify the abstract. Add a one-paragraph plain-language method summary at the start of §2. Revise the figures as above. Consider moving the adaptivity and ablation detail (L125) to the supplement to make room for the workload and monitoring content. `[FIXABLE-IN-REPO]`

**P-15 (MINOR) Open science from a reader's viewpoint.**
*Location:* L195; L88; S1 "Deviations"; supplement size.
*Problem.*
- The code is "provided as supplementary material and will be deposited … upon acceptance". A persistent public deposit at submission would let reviewers and laboratories test the method.
- The protocol is "held in the study repository, not externally registered" and, per S1, cannot be independently dated. The manuscript now says "pre-specified" rather than "pre-registered", which is appropriate. Readers should still be able to see the protocol's version history.
- The supplement is about 205,000 words of machine-generated tables, which is hard to navigate.
- No deployment-ready artefact is offered: for example, a script that takes a site's scored nights and outputs the calibrated model plus an audit report.
*Fix.* Deposit the code with a DOI now (it can be embargo-free given public data). Curate the supplement into readable key tables, with the full machine tables as CSV files. Consider releasing a minimal "local calibration and audit" tool to lower the adoption barrier. `[FIXABLE-IN-REPO]`

---

### Detailed Comments

#### Assumption Audit
- **Explicit assumptions.** Exchangeability between calibration and test nights (L48, L88, L161 (ii)) is stated and tested. Its operational meaning for a laboratory (same patient mix, equipment, scorer, rules, software version, *over time*) is not spelled out, and the local-deployment experiment draws calibration nights at random from the same cohort. A real site's first 20 nights after go-live are a convenience sample (season, referral source) and may not be representative of later months. Temporal exchangeability is untested (P-4).
- **Implicit assumptions.**
  - (1) That a per-night interval changes what clinicians do (sign-off vs review). This is not evidenced and depends on the review model (P-13).
  - (2) That more nights decided means better care. The value depends on the cost of the residual confident-wrong decisions and on which parameter is decided (P-1, P-11).
  - (3) That the single scorer's value is the right target. The authors acknowledge it (L161 (iii)), but a clinician reads "error range" as error against truth.
  - (4) That the stager exposes calibrated-able epoch probabilities. This holds for open stagers but not necessarily for clinical products (P-7, P-12).
- **Paradigmatic assumptions.** The paper evaluates a statistical object (coverage, interval score) and infers clinical utility from it. Implementation science would ask for at least a workflow simulation (P-1) and, eventually, a user study of how scorers and physicians act on intervals. A decision-curve or workload framing would connect the statistical result to practice more directly than interval-score ratios do.

#### Cross-Disciplinary Connections
- **Parallel research.** Laboratory medicine has long practice in reporting measurement uncertainty for individual results and in monitoring analytical performance with statistical QC rules (Westgard-type multi-rule charts). Both map directly onto per-night intervals and post-deployment coverage audits (P-4). Metrology's "coverage interval" vocabulary (GUM) offers frequentist wording that avoids "confidence" (P-5).
- **Borrowing opportunities.** Uncertainty-communication research gives evidence on how lay and professional audiences misread numerical ranges, and on formats that reduce misreading (P-5). Reporting guidance for the early clinical evaluation of AI decision support (DECIDE-AI) and for prediction models using AI (TRIPOD+AI) would structure the intended-use, human-factors and monitoring content (P-4, P-12).
- **Methodological borrowing.** The conformal literature itself provides the closed-form conditional-coverage distribution for split conformal (P-3) and adaptive or online conformal methods for drifting data (P-4). These are natural tools for the deployment questions the paper raises.

#### Practical Impact
- **Real-world application.** The clearest practical message is not the intervals themselves. It is that recalibrating the stager on local nights removes most TST bias (L132; Table 3) and that any per-night or population error statement must be calibrated locally (L166). That message is valuable and cheap to implement. The intervals add a modest improvement in TST decision triage over simpler distribution-free limits (P-1).
- **Implementation feasibility.**
  - The compute cost is negligible (S15).
  - The labour cost of manual scoring is modest in absolute terms: 20 nights is about 2 % of a 1,000-study annual volume. It recurs at every relevant change, and the paper is silent on that.
  - The dominant cost is reviewing the roughly 40 % of clinical-cohort nights that remain undecided at TST < 6 h (P-1), and all candidate SOREMP nights (P-11).
  - The implementation complexity (HMM, FFBS, temperature fitting, cross-fitting) is far greater than recalibration plus distribution-free limits, for a small incremental gain outside TST. The paper concedes this (L159), but it should be the centre of the practice recommendation.
  - Unintended consequences: automation bias toward "confident" decisions (about 1 % wrong); erosion of trust when one of eight intervals misses (P-5); silent failure on poor-quality recordings (P-8) and after drift (P-4).
- **Stakeholders.** Beneficiaries are named (clinicians, laboratories). Scorers, who bear the calibration and review burden, are not discussed. Patients exposed to confident-but-wrong calls, particularly in the under-covered hard nights, are not discussed. Populations outside the cohorts (children; home, wearable and limited-montage recordings; disease groups; non-European settings) carry the transport risk the paper itself demonstrates (P-7).

#### Broader Implications
- **Ethical dimensions.** Coverage is lowest on the hardest nights (L122). If difficulty correlates with age, disease severity or recording conditions, the method's reliability is unequally distributed. Characterising those nights (P-7) is the minimum step. The data are public and de-identified, and the ethics statement is appropriate (L187).
- **Social impact.** A well-scoped version of this work could raise the standard of validation reporting: from population limits of agreement to locally audited per-night error statements. An over-read version ("valid per-night intervals") could lend false precision to automated reports, especially if it is transplanted to consumer and wearable settings where the paper offers no evidence.
- **Future directions.** A prospective, temporally ordered deployment study with an ongoing audit. Validation on home sleep testing and wearable data and on paediatric cohorts. Deep-learning stagers. A user study of how scorers and physicians act on intervals. Integration with signal-quality gating.

### Cross-Disciplinary Reading Recommendations
- Westgard JO, Barry PL, Hunt MR, Groth T. A multi-rule Shewhart chart for quality control in clinical chemistry. *Clin Chem* 1981. Template for a coverage-audit chart (P-4).
- Gibbs I, Candès E. Adaptive conformal inference under distribution shift. *NeurIPS* 2021. Online recalibration under drift (P-4).
- Vovk V. Conditional validity of inductive conformal predictors. *ACML* (PMLR 25), 2012. Distribution of conditional coverage for a fixed calibration set (P-3).
- van der Bles AM, van der Linden S, Freeman ALJ, et al. Communicating uncertainty about facts, numbers and science. *R Soc Open Sci* 2019. Formats and misreadings of numerical uncertainty (P-5).
- Vasey B, et al. Reporting guideline for the early-stage clinical evaluation of decision support systems driven by artificial intelligence: DECIDE-AI. *Nat Med* 2022. Structure for intended use, human factors and monitoring (P-4, P-12).
- Collins GS, et al. TRIPOD+AI statement. *BMJ* 2024. Reporting of AI prediction models, including deployment considerations.
- JCGM 100:2008, Evaluation of measurement data: Guide to the expression of uncertainty in measurement (GUM). "Coverage interval" terminology (P-5).
- [UNVERIFIED] Search lead: AASM guidance on MSLT/MWT protocols (2021) for the clinical anchor of the TST threshold before an MSLT (P-11). Exact wording to be checked by the authors.

~~~yaml suggested-references
- title: "A multi-rule Shewhart chart for quality control in clinical chemistry"
  authors: ["Westgard, J.O.", "Barry, P.L.", "Hunt, M.R.", "Groth, T."]
  year: "1981"
  doi: null
  arxiv_id: null
- title: "Adaptive conformal inference under distribution shift"
  authors: ["Gibbs, I.", "Candès, E."]
  year: "2021"
  doi: null
  arxiv_id: null
- title: "Conditional validity of inductive conformal predictors"
  authors: ["Vovk, V."]
  year: "2012"
  doi: null
  arxiv_id: null
- title: "Communicating uncertainty about facts, numbers and science"
  authors: ["van der Bles, A.M.", "van der Linden, S.", "Freeman, A.L.J."]
  year: "2019"
  doi: null
  arxiv_id: null
- title: "Reporting guideline for the early-stage clinical evaluation of decision support systems driven by artificial intelligence: DECIDE-AI"
  authors: ["Vasey, B."]
  year: "2022"
  doi: null
  arxiv_id: null
- title: "TRIPOD+AI statement: updated guidance for reporting clinical prediction models that use regression or machine learning methods"
  authors: ["Collins, G.S."]
  year: "2024"
  doi: null
  arxiv_id: null
- title: "Evaluation of measurement data — Guide to the expression of uncertainty in measurement"
  authors: ["JCGM"]
  year: "2008"
  doi: null
  arxiv_id: null
~~~

### Questions for Authors
1. In HMC, how many nights per 1,000 would a laboratory review under your recommended rule, and how many would it review under recalibration plus distribution-free limits? Is the difference worth the added implementation complexity?
2. What is the TST < 6 h accuracy of the *recalibrated* plug-in under the end-to-end protocol, and how does Fig. 5e change with it as the baseline?
3. How should a site decide, after start-up, that its intervals have lost validity? Which signal, which audit size, which trigger?
4. What do you recommend for a night with poor signal quality: no interval, or an interval with a warning?
5. Who are the nights in the lowest-accuracy quartile (age, sleep efficiency, cohort), and does their 85 % coverage fall further in any identifiable group?
6. Can your recommended n be derived from the closed-form conditional-coverage distribution, so that sites can choose n for their own risk tolerance?

### Minor Issues
- L17: the word-count line (4,965/293) differs from the counts quoted in the Phase 0 record (4,946/297). Please make sure the final title-page numbers match the build. (Journal-fit item; noted only.)
- L105: "illustrative decision thresholds chosen by the authors" sits uneasily with the abstract presenting threshold results as a headline. Either justify the thresholds clinically (P-11) or present them as illustrative in the abstract too.
- L137/Fig. 3: "unbounded" distribution-free limits with fewer than 19 nights is an important practical fact for small sites. Consider stating it in the practice paragraph as a hard minimum.
- Fig. 4 caption: state that artefact epochs are chosen independently for EEG and EOG and uniformly over the night (P-8).
- Fig. 5h: annotate that all confident decisions are negative (P-11).

---

## Recommendation
**Major Revision**, confidence 4/5 within my remit (deployment, workflow, communication, evidence coverage).

**Three issues most likely to cause rejection**
1. The clinical payoff is not demonstrated in workload terms. Against the simple alternative a lab would actually run (recalibrate, then distribution-free limits on the same nights), the TST decision gain is about 2 percentage points of HMC nights, and the decision baseline is the uncorrected rather than the recalibrated plug-in (P-1, P-2).
2. The practice recommendation ("≥ 20 local nights") rests partly on a site-risk metric confounded by tiny ST test sets, and it comes with no post-deployment monitoring, although the paper's own central finding is that validity is local and fails silently (P-3, P-4).
3. "Valid per-night 90 % intervals" and "90 % confidence" for a single night will be read clinically as a per-night probability guarantee, and absolute widths (±45 min for TST; 1.5–3 h for REM latency) are absent from the abstract (P-5, P-6).

**Three strongest points**
1. Candid, narrowed claims: the advantage is TST-specific, transport fails, local calibration is required, and WASO's failure is explained mechanistically (L35, L140, L157, L166).
2. A deployment-shaped evaluation: components are fitted only on calibration nights, local few-night calibration and transport are tested explicitly, and site-level risk is reported rather than only mean coverage (L95–101, L137).
3. Strong transparency: a dated deviation log, a leakage audit, a regeneration pipeline from public data, and disclosed AI involvement (S1, S16, L111).
