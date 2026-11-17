# Reviewer 8 — Literature & citation accuracy (cycle 1)

Checks: all DOIs resolved (Crossref 36, DataCite 2). The three DOI-less items were checked against PMLR 119 and the NeurIPS 2019 metadata. Abstracts came from PubMed and OpenAlex, plus full text of YASA and Hardarson 2023 and the PhysioNet pages. The reference list is from the current PDF (2026-11-16 18:35).

## Summary of the submission (3-5 sentences)
The manuscript proposes per-night conformal intervals for PSG sleep parameters, built from FFBS hypnogram samples, and evaluates them on Sleep-EDF and HMC against Bland–Altman limits of agreement. All 41 references exist and are now mostly well formatted. Several attributions are wrong: one "validation study" concerns apnoea scoring, Hardarson 2023 is credited with a mechanism it explicitly did not model, and Baumert 2023 is misread. The closest prior art is uncited: hypnogram posterior sampling for overnight-statistic uncertainty (van Gorp 2023 ×2, Philips patent), plus Vainikka 2026.

## Fatal concerns
None.

## Critical/Major concerns
**M1. Rohrscheib 2026 [8] is miscited.** Intro ¶1 cites [6–8] for validation studies that summarise algorithm–scorer agreement "for these parameters" (TST, SOL, WASO, REML, stage %) with Bland–Altman limits. Rohrscheib (PMID 41671846) evaluates HSAT **AHI/CAI** autoscoring and reports no sleep-staging parameters. The authors' own benchmark file (Table A #22) labels it "AI autoscoring of HSAT (AHI, CAI)". [6] (Oura ring) and [7] (Dreem headband) are consumer-device validations, not PSG autoscoring–scorer comparisons. *Fix:* drop [8]. Cite a PSG-autoscoring validation that reports parameter-level limits of agreement, e.g. Kaneda 2026 (Sleep Adv 7:zpag054, 10.1093/sleepadvances/zpag054; TST limits about ±0.5 h). It is already in `references.json` but uncited. Reword [6,7] as "device validations".

**M2. Hardarson 2023 [11] is credited with the opposite assumption.** Intro ¶2 says high accuracy can give poor parameter estimates "because epoch errors are temporally clustered [11]". Hardarson's Monte Carlo instead "re-assigned each epoch a sleep stage independently of other epochs" and "assumed that the staging error was random in time" (Limitations). It also used wearable-derived confusion matrices, not PSG. *Fix:* attribute only the finding that ~90 % accuracy can still give poor parameter estimates [11]. Present temporal clustering as this paper's own finding (§3.2, independent sampling covered as little as 4 %), and contrast it with Hardarson's independence assumption in the Discussion.

**M3. Directly competing prior work is missing (all verified).**
- van Gorp H et al. *IEEE JBHI* 2023;27:5599–5609 (10.1109/JBHI.2023.3304010). U-Flow models inter-rater disagreement of overnight statistics.
- van Gorp H et al. *ICASSP* 2023:1–5 (10.1109/ICASSP49357.2023.10096894). It does "posterior sampling" of jointly modelled hypnograms and explicitly argues that time-factorised sampling "invalidat[es] posterior sampling of the overnight statistics". This is the paper's own FFBS-versus-independent argument.
- Philips patent EP4388985A1 (van Gorp et al., filed 2023-01-30, published 2024-06-26): "System for estimating uncertainty of overnight sleep parameters through a stochastic neural network".
- Vainikka 2026 [in `references.json`, uncited] proposes an epoch-level "Hypnodensity Interval", which risks a name collision.

The authors' own literature file states that Vainikka "must be cited and contrasted". Without these works, Intro ¶3 ("Monte-Carlo propagation … at the population level [11]") and Discussion "Relation to previous work" overstate the gap. *Fix:* cite them and contrast. The prior work models aleatoric inter-rater uncertainty with generative networks, without conformal calibration, coverage guarantees or local recalibration.

**M4. The submitted Table 2 is corrupted (outside my remit, but verified).** In `Final_Manuscript.docx` Table 2 is 17×5, and row 1 reads `['YASA','TST (min)','0.907','85.3','0.85*']`. The "|"-separated quadruples were split into columns, so the "ST" column shows SC width and the "HMC" column shows SC ratio. Nine of every twelve values are lost. The PDF shows the same. *Fix:* use 12 sub-columns or another separator, then rebuild.

## Moderate concerns
**Mo1. The age claim is not supported as written.** "…and in older patients [9,10]": Baumert's abstract says the main age bias concerns children, and "errors … staging PSG of older people were comparably lower". SLEEPYLAND [10] shows demographic/clinical bias but says nothing on "technically poor recordings". *Fix:* cite YASA's moderator analysis [5] (accuracy falls with age, r = −0.128, and with AHI, r = −0.29). Cite Ganglberger [21] (biosignal-quality features) for signal quality. Restrict [9] to "errors in clinical markers of individual PSGs".

**Mo2. FFBS attribution.** Carter & Kohn [35] and Frühwirth-Schnatter [36] derive FFBS for linear/conditionally Gaussian state-space models. The finite-state HMM sampler of Eq. (3) is from Chib 1996 (*J Econom* 75:79–97, 10.1016/0304-4076(95)01770-4); see also Scott 2002 (*JASA* 97:337–351, 10.1198/016214502753479464). *Fix:* add Chib 1996, and drop [36] if space is needed.

**Mo3. Statistical methods lack citations.**
- (a) "Mondrian calibration" (§3.2, Limitations) is uncited. Add Vovk 2013 (*Mach Learn* 92:349–376, 10.1007/s10994-013-5355-6) and/or the Mondrian chapter of [22].
- (b) The normalised score (4) is locally weighted conformal prediction. Credit Papadopoulos 2011 (*JAIR* 40:815–840, 10.1613/jair.3198) and Lei [23] §5.
- (c) The paper argues that constant limits of agreement cannot follow heteroscedastic error but omits the clinical standard remedy, regression-based limits (Bland & Altman 1999, *Stat Methods Med Res* 8:135–160, 10.1177/096228029900800204). Cite it, and compare against it or justify not doing so.
- (d) "covariate or label shift [25,26]": [25] covers covariate shift and [26] covers drift or non-exchangeability; neither treats label shift. Reword.

**Mo4. Clinical claims lack citations.**
- "score a small set of local nights manually, as recommended for validating any scoring method" (Clinical use) has no source. Cite a guideline that actually says this; check whether the AASM AI position statement (Goldstein 2020, 10.5664/jcsm.8288) does. Otherwise delete "as recommended".
- The TST 6 h and SOREMP REM latency 15 min thresholds need a source, e.g. AASM MSLT guidance (Krahn 2021, 10.5664/jcsm.9620).
- The Rechtschaffen & Kales 1968 manual is uncited.
- Inter-scorer reliability could cite the meta-analysis (Lee 2022, *J Clin Sleep Med* 18:193–202, 10.5664/jcsm.9538).

**Mo5. The Ethics statement is inaccurate.** It says "the original studies obtained the approvals and consents described in their data descriptors [27,29]". But [27] (Kemp 2000) is a physiology paper on the ST cohort, not a data descriptor, and neither it nor the PhysioNet Sleep-EDF page mentions approval. The HMC PhysioNet page does state that reuse was approved by METC Zuid-West Holland (METC-19-065). The licences are correct: Sleep-EDF 1.0.0 is ODC-By v1.0 and HMC 1.1 is CC BY 4.0, matching `code/scripts/download_data.sh`. *Fix:* state what each source actually documents. PhysioNet now also asks users to cite Pollard 2026 (*Nature Health* 1:792–795, 10.1038/s44360-026-00096-z).

## Minor concerns
**Mi1. Residual formatting errors in the current list.**
- [6] "NT H": the author is Hoang NT.
- [18] reads "Sleep 2022;46"; volume 46 is 2023, so it should be 2023;46:zsac154.
- [25] "Tibshirani R" should be RJ. "Foygel Barber R" in [25] and "Barber RF" in [26] should be made consistent.
- [28] "Aeilko Zwinderman" is unparsed. It also needs PhysioNet, v1.0.0 and the [dataset] tag; [30] needs PhysioNet, v1.1 and [dataset].
- [41] lacks pages (e215–20) and the subtitle.
- [33] title is missing ": A Hybrid Approach"; the publisher should be "Boston: Kluwer".
- [20] is a proceedings paper formatted like a journal article.
- Casing is wrong in "Npj" [4,10,12] and "Plos One" [29].
- Use journal-title abbreviations consistently (e.g. Sleep Med), as Elsevier style expects.

**Mi2. The Li 2025 [19] wording needs context.** "Conformal prediction sets … for single epochs" is supported: ConMIL produces conformal set-valued outputs for sleep-stage classification. But the paper's purpose is LLM decision support, and its title does not reveal ConMIL. *Fix:* "conformal prediction sets for sleep-stage classification within an LLM decision-support framework (ConMIL) [19]".

**Mi3. van Gorp 2022 [17] is a theoretical framework on aleatoric and epistemic uncertainty, not a hypnodensity display.** Move it to the uncertainty sentence.

**Mi4. Count and style.** 41 references (limit 50), numbered square brackets in order of first appearance: compliant. After the additions (about 8 new, 1–2 removed) the list still fits.

### Reference verification table
| key | verified? | issue | fix |
|---|---|---|---|
| rohrscheib2026 | yes | apnoea (AHI) study cited for sleep-parameter limits of agreement | replace (M1) |
| svensson2024 / beau2025 | yes | device validations; [6] author "NT H" | reword; Hoang NT |
| hardarson2023 | yes | independence assumption misreported as clustering | M2 |
| baumert2023 / deirossi2025 | yes | "older patients" unsupported | Mo1 |
| carter1994 / fruhwirth1994 | yes | Gaussian state-space FFBS, not the HMM version | add Chib 1996 |
| li2025conmil | yes (ConMIL, sleep staging) | context missing | Mi2 |
| vangorp2022 | yes | misplaced | Mi3 |
| bakker2023 | yes | year 2022, should be 2023 | Mi1 |
| tibshirani2019 / romano2019 / alexandari2020 | yes (pp. 2530–40; 3543–53; PMLR 119:222–32) | initials | Mi1 |
| tibshirani2019 / barber2023 | yes | "label shift" over-attributed | Mo3d |
| sleepedf_data / hmc_data | yes (DataCite) | dataset formatting | Mi1 |
| goldberger2000 | yes | no pages | Mi1 |
| kemp2000 | yes | not a data descriptor; no ethics information | Mo5 |
| bourlard1994 / mikkelsen2020 | yes | title/publisher; proceedings format | Mi1 |
| rosenberg2013, dankerhopfe2009, stephansen2018, perslev2021, vallat2021, kang2021, fiorillo2021, phan2022, heremans2024, bechny2024, ganglberger2024, vovk2005, lei2018, angelopoulos2023, alvarez2021, berry2017 (HMC page confirms AASM v2.4), rabiner1989, bland1986, gneiting2007 (interval score with 2/α correct), mcgraw1996 (ICC(A,1) correct) | yes | none; claims supported | — |
| kaneda2026, vainikka2026 | yes | in bibliography but uncited | cite (M1, M3) |

## Required additional experiments/analyses
None required. Optional: regression-based limits of agreement (Bland & Altman 1999) as a comparator (Mo3c).

## Recommendation
**Major revision.** The bibliography is real, but two attributions are wrong (M1, M2), one is weakly supported (Mo1), and the closest prior art is missing (M3). The corrupted Table 2 (M4) must be fixed before submission.

```json
[
{"id":"M1","severity":"major","title":"Rohrscheib 2026 miscited as sleep-parameter Bland-Altman validation","location":"Introduction para 1, refs [6-8]","evidence":"PMID 41671846 abstract: AHI/CAI autoscoring of HSAT; no TST/SOL/WASO/stage limits of agreement. [6],[7] are Oura/Dreem device validations.","action":"Remove [8]; cite PSG-autoscoring validation with parameter-level limits of agreement (Kaneda 2026, 10.1093/sleepadvances/zpag054, already in references.json); reword [6,7] as device validations.","needs_experiment":false},
{"id":"M2","severity":"major","title":"Hardarson 2023 credited with temporally clustered errors; the paper assumed independent errors","location":"Introduction para 2","evidence":"Hardarson Limitations: resampling 're-assigned each epoch a sleep stage independently of other epochs'; 'assumed that the staging error was random in time'; wearable data.","action":"Attribute only the accuracy-to-parameter-error finding; present temporal clustering as own result and contrast with Hardarson.","needs_experiment":false},
{"id":"M3","severity":"major","title":"Closest prior art on hypnogram posterior sampling for overnight statistics not cited","location":"Introduction para 3; Discussion 'Relation to previous work'","evidence":"van Gorp 2023 IEEE JBHI 27:5599-5609 (10.1109/JBHI.2023.3304010); van Gorp ICASSP 2023:1-5 (10.1109/ICASSP49357.2023.10096894), which argues factorised sampling invalidates overnight statistics; Philips EP4388985A1 (filed 2023-01-30); Vainikka 2026 in references.json but uncited, although the authors' own literature file says it must be contrasted.","action":"Cite and contrast (generative aleatoric models vs conformal calibrated coverage plus local recalibration); temper the novelty wording.","needs_experiment":false},
{"id":"M4","severity":"major","title":"Table 2 corrupted in submitted DOCX/PDF","location":"Final_Manuscript.docx table 2; PDF Table 2","evidence":"python-docx: 17x5 table, row 1 = ['YASA','TST (min)','0.907','85.3','0.85*']; pipe-separated quadruples split into columns, so ST/HMC columns show SC width/ratio.","action":"Restructure Table 2 (sub-columns or other separator) and rebuild.","needs_experiment":false},
{"id":"Mo1","severity":"moderate","title":"Errors 'in older patients' not supported by [9,10]","location":"Introduction para 2","evidence":"Baumert abstract: main bias in children; 'errors ... staging PSG of older people were comparably lower'. SLEEPYLAND: demographic/clinical bias only.","action":"Cite YASA moderator analysis [5] (age r=-0.128, AHI r=-0.29) and Ganglberger [21] (signal quality); restrict [9].","needs_experiment":false},
{"id":"Mo2","severity":"moderate","title":"FFBS for discrete HMM attributed only to Gaussian state-space papers","location":"Methods 2.4, refs [35,36]","evidence":"Carter & Kohn 1994 and Fruhwirth-Schnatter 1994 abstracts: linear/dynamic linear models.","action":"Add Chib 1996 J Econom 75:79-97 (10.1016/0304-4076(95)01770-4).","needs_experiment":false},
{"id":"Mo3","severity":"moderate","title":"Uncited or mis-scoped statistical methods (Mondrian, normalised score, regression limits of agreement, label shift)","location":"Results 3.2; Methods 2.5; Discussion Limitations (ii)","evidence":"'Mondrian calibration' uncited; score (4) is locally weighted conformal; Bland-Altman 1999 regression limits of agreement absent; refs [25,26] do not treat label shift.","action":"Cite Vovk 2013 (10.1007/s10994-013-5355-6), Papadopoulos 2011 (10.1613/jair.3198), Bland & Altman 1999 (10.1177/096228029900800204); reword label shift.","needs_experiment":false},
{"id":"Mo4","severity":"moderate","title":"Clinical statements without citation","location":"Discussion 'Clinical use'; Methods 2.1","evidence":"'as recommended for validating any scoring method', TST 6 h / SOREMP 15 min thresholds, and R&K rules are all uncited.","action":"Cite a guideline that actually makes the validation recommendation or delete it; cite AASM MSLT guidance (10.5664/jcsm.9620) and the R&K manual; optionally Lee 2022 meta-analysis (10.5664/jcsm.9538).","needs_experiment":false},
{"id":"Mo5","severity":"moderate","title":"Ethics statement attributes approvals to sources that do not document them","location":"Ethics statement","evidence":"Kemp 2000 is not a data descriptor and gives no approval; PhysioNet Sleep-EDF page silent; HMC page cites METC-19-065 reuse approval. Licences (ODC-By 1.0, CC BY 4.0) verified correct.","action":"State what each source documents; cite METC-19-065; optionally add Pollard 2026 PhysioNet citation.","needs_experiment":false},
{"id":"Mi1","severity":"minor","title":"Residual reference-format errors","location":"Reference list [4,6,10,12,18,20,25,26,28,29,30,33,41]","evidence":"'NT H'; Sleep 2022;46; 'Tibshirani R'; 'Aeilko Zwinderman'; datasets without PhysioNet/version/[dataset]; Goldberger no pages; 'Npj', 'Plos One'; EMBC as journal; Bourlard subtitle/publisher.","action":"Correct entries; use consistent abbreviated journal titles.","needs_experiment":false},
{"id":"Mi2","severity":"minor","title":"ConMIL citation lacks context","location":"Introduction para 3, ref [19]","evidence":"Abstract: conformal sets for sleep-stage classification feeding LLMs; title does not reveal ConMIL.","action":"Name ConMIL and its LLM decision-support setting.","needs_experiment":false},
{"id":"Mi3","severity":"minor","title":"van Gorp 2022 cited as hypnodensity display","location":"Introduction para 3, ref [17]","evidence":"Abstract: theoretical aleatoric/epistemic framework.","action":"Move to the uncertainty sentence.","needs_experiment":false},
{"id":"Mi4","severity":"minor","title":"Reference count and style compliant; keep at 50 or fewer after additions","location":"References","evidence":"41 references, numbered square brackets in order of first appearance.","action":"After adding about 8 and removing 1-2, verify the total stays at 50 or fewer.","needs_experiment":false}
]
```
