# Verified literature check: night-level conformal uncertainty for automated sleep scoring (target: *Sleep Medicine*)

**Sources (2026-11-15):** PubMed E-utilities (10 Sleep Med [ta] queries, 2021–2026, about 250 records screened; about 12 prior-art queries), Crossref, arXiv, Europe PMC (with preprints), OpenReview, NeurIPS/PMLR pages, DataCite. **Limits:** Semantic Scholar was rate-limited (1 query succeeded); OpenAlex and DBLP were blocked; I did not search Google Scholar or IEEE Xplore. Every item has a retrieved record with its DOI or PMID; anything else is marked UNVERIFIED.

**Note:** Sleep Medicine *vols. 100, 115 and 138* contain World Sleep **congress abstracts** that have DOIs, for example Bechny, "Benchmarking reveals shared biases in sleep-staging algorithms" (10.1016/j.sleep.2025.108570) and "SLEEPYLAND" (10.1016/j.sleep.2025.108623). They are not original articles, so I left them out of Table A.

## Table A. *Sleep Medicine* original research, 2021–2026 (all retrieved via PubMed)

EBE = epoch-by-epoch; BA = Bland–Altman; LoA = limits of agreement; NR = not reported in abstract; Ind. = independent test of a frozen algorithm. No code link unless stated.

| # | Paper (PMID; DOI) | Problem → method | Data (n) | Comparator → metrics | Stats/CIs | External/cross-cohort | Limitations (stated) / code |
|---|---|---|---|---|---|---|---|
| 1 | Wang 2025 RimeSleepNet (41038061; 10.1016/j.sleep.2025.106835) | Optimized VMD + CNN + attention + LSTM; 3 classes | Chengdu hospital + Sleep-EDF; n NR | CNN, LSTM → F1 0.94/0.89/0.92, AUC 0.92, κ 0.90 | NR | Yes (cross-dataset) | NR |
| 2 | Follin 2025 (39938170; 10.1016/j.sleep.2025.02.005) | Scoring of 5-s mini-epochs by 3 experts and U-Sleep | 40 PSG × 120 mini-epochs; NT1 patients and siblings | Inter-rater κ 0.50–0.57; stage-shift % | Mean±SD; significance tests | n/a | No mini-epoch scoring rules; small data |
| 3 | Tamburrino 2025 (39673901; 10.1016/j.sleep.2024.12.009) | Actigraphy (Cole-Kripke, UCSD) vs home PSG in bvFTD | 18 | BA, discrepancy analysis, EBE accuracy 84–85%; TST overestimated by 43–60 min; proportional bias in WASO | Yes | Ind. | Biases must be corrected |
| 4 | Silva 2024 (38810479; 10.1016/j.sleep.2024.05.033) | RNN on 23 accelerometer/PPG features (Samsung watch), 4 classes | 1,522 nights; test set 586 | Balanced accuracy 71.6%, κ 0.56; healthy vs OSA | NR | Held-out only | — |
| 5 | Wulterkens 2024 (38547592; 10.1016/j.sleep.2024.03.031) | Multi-night wrist staging, COMISA vs OSA | 117 participants; 13.4±5.2 nights each | Mixed models; within-subject variance; clustering | Yes | n/a (application) | Single-night PSG missed the differences |
| 6 | Svensson 2024 (38382312; 10.1016/j.sleep.2024.01.020) | Oura Gen3 / OSSA 2.0 vs multi-night ambulatory PSG | 96 participants; 421,045 epochs | Paired t-tests, BA, PABAK 0.83–0.84; stage accuracy 75.5–90.6% | Yes | Ind. | A comment and reply were published |
| 7 | Baumert 2023 (37099916; 10.1016/j.sleep.2023.04.002) | Age bias: XSleepNet2 trained on each age group or pooled | 1,232 children, 3,757 adults, 2,788 older adults | DeepSleepNet → accuracy 88.9% vs 78.9% across ages; significant errors in clinical markers for individual PSGs | Yes | Yes (cross-age cohorts) | "Must pay attention to PSG-level performance" |
| 8 | Ding 2022 (35576830; 10.1016/j.sleep.2022.04.010) | Under-mattress device (Sleeptracker-AI) vs PSG; also OSA | 102 | EBE accuracy 79.0%, κ 0.676; TST +6.3 min; WASO −10.2 min | 95% CIs | Ind. | Data supplied by the manufacturer |
| 9 | Thiesse 2022 (35576829; 10.1016/j.sleep.2022.04.013) | Somno-Art (cardiac-based) vs 5 scoring centres | 60 nights (healthy, OSA, insomnia, MDD) | ICC, Wilcoxon; within the inter-scorer range except N3 in OSA | Yes | Yes (multi-centre) | Underestimates N3 in OSA |
| 10 | Xue 2022 (35123148; PMC9539833; 10.1016/j.sleep.2021.12.016) | Actigraphy algorithms for children with CP | 13 CP + 13 controls | Accuracy 72–80% (CP); BA | Yes | No | Small n; overfitting. **Code: github.com/xuebing1234/actigraphy** |
| 11 | de Goederen 2021 (33866298; 10.1016/j.sleep.2021.03.022) | UWB radar + AdaBoost in children | 32 | κ 0.67 / 0.47 / 0.43 (2-, 3-, 4-class) | NR | No | "Not sufficient for clinical use" |
| 12 | Kuzik 2021 (33429290; 10.1016/j.sleep.2020.12.019) | Waist ActiGraph, random forest + HMM, nap/sleep/wake in preschoolers | 89 | Accuracy 96.2%, κ 0.93 | 95% CI | No | Reference is visual inspection, not PSG |
| 13 | Cesari 2021 (33360558; 10.1016/j.sleep.2020.11.033) | Probabilistic 3-s sleep modelling vs manual features for predicting age | 15 train / 79 test | Adjusted R², cross-validated accuracy | Mean±SD | No | — |
| 14 | Ahsan 2026 (42235319; PMC13436844; 10.1016/j.sleep.2026.109044) | Sleep/wake from CPAP flow (ML) | 100 (70/30 split) | Accuracy 0.82, κ 0.51 | NR | No | Lab titration only; home use untested |
| 15 | Liu 2026 (42202499; 10.1016/j.sleep.2026.109036) | **U-Sleep 2.0 stage uncertainty/mixing** as iRBD markers | 104 iRBD, 28 PD+RBD, 50 controls | Correlations with RBDQ-HK, UPDRS-III, MoCA, DOPA-PET | Yes (r, p) | n/a | — |
| 16 | Alhejaili 2026 (42258963; 10.1016/j.sleep.2026.109059) | Apple Watch 7, Fitbit Charge 5 and Polar M2 vs home PSG and actigraphy | 20 / 19 / 15 | ICC, BA; wide LoA | Yes | Ind. | Not clinical grade |
| 17 | Beau 2025 (40712528; 10.1016/j.sleep.2025.106698) | Dreem 3 headband in insomnia disorder | 31 | EBE sensitivity (N1 29.8%); BA for TST, SE, SOL, WASO | Yes | Ind. | TST and SE overestimated |
| 18 | Kim 2025 (40315671; 10.1016/j.sleep.2025.106533) | Sound-based AI staging with two people in the room | 88 | Macro-F1 0.59, κ 0.47 (4 classes); subgroups | NR | Ind. | Demographic gaps |
| 19 | West 2023 (37257366; PMC10344673; 10.1016/j.sleep.2023.04.031) | Consensus scoring protocol in advanced PD (DBS) | 15 patients, 45 nights, 4 scorers | Agreement 83.1% → 96.6% | NR | n/a | — |
| 20 | Montini 2026 (42967379; 10.1016/j.sleep.2026.109334) | New scoring scheme with abnormal stages in PD | 15 PD + 5 controls, 5 raters | κ 0.75 vs 0.73 for AASM | NR | n/a | — |
| 21 | Deguchi 2026 (41990417; 10.1016/j.sleep.2026.108958) | Wrist and waist devices vs portable EEG in older adults | 55 participants; 238/265 nights | BA, multilevel models, ICC for TST 0.60–0.79 | Yes | Ind. | Quiet wake misclassified |
| 22 | Rohrscheib 2026 (41671846; PMC12945445; 10.1016/j.sleep.2026.108828) | AI autoscoring of HSAT (AHI, CAI) | 44 with simultaneous PSG + 139 clinical HSATs from 11 clinics | r 0.90; BA; 3 scorers | **95% CIs on bias and LoA** | Yes (multi-clinic) | "Sample size limited" |
| 23 | Del-Río Camacho 2024 (38704870; 10.1016/j.sleep.2024.04.030) | Automatic vs manual PLM scoring in children | 131 PSGs | Concordance 0.63 [0.51–0.72] | Yes | n/a | Automatic scoring overestimates PLMI |
| 24 | Ülgen 2023 (36459917; 10.1016/j.sleep.2022.11.020) | Actigraphy and aEEG vs direct observation in preterm infants | 17 infants; 11,252 epochs | κ 0.14–0.17, PABAK, BA | Yes | n/a | — |
| 25 | Yook 2024 (38232604; PMC10872216; 10.1016/j.sleep.2024.01.015) | Xception on airflow/SpO2/ECG for respiratory events | Internal PSG set + **SHHS1 (5,804)** | Event accuracy 94%; screening AUC 0.99 | Partial | **Yes (SHHS1)** | Errors in hypopnea-dominant patients |

## What a *Sleep Medicine* paper in this area usually looks like

- **Novelty axis.** Mostly "does it hold up in population or setting X" (insomnia, bvFTD, PD, iRBD, CP, preterm infants, older adults, CPAP). New architectures alone are rare (#1). Among the strongest are papers built on **PSG-level clinical consequences**: #7 (errors in clinical markers for individual PSGs) and #15 (uncertainty as a biomarker).
- **Sample sizes.** Device validations: 17–102 participants. Algorithm development: 100–1,500 nights. Large studies: about 7,800 PSGs (#7) or SHHS1 (#25).
- **Agreement statistics.** Nearly universal: BA (bias, LoA) for TST, SE, SOL, WASO and stage minutes; EBE accuracy, sensitivity/specificity; κ or PABAK; ICC; paired tests. Stronger papers add **95% CIs**, including on the LoA (#8, #12, #22, #23).
- **Validation.** External or cross-cohort testing is rare in method papers (#1, #7, #22, #25). Multi-scorer or multi-centre references (#9, #22) and multi-night designs (#5, #6, #21) set the stronger papers apart.
- **Code** is rarely stated; only #10 links code among the abstracts and PMC full texts I checked.
- **Implications for this study:**
  1. Report standard BA, ICC and κ for the point estimates.
  2. Report **empirical coverage with binomial or bootstrap CIs**, interval width, and coverage by subgroup (age, AHI or diagnosis, HMC vs Sleep-EDF).
  3. Frame results clinically, e.g. nights whose interval crosses SE 85%, REM latency ≤15 min (SOREMP), or TST <6 h.
  4. **Contrast with BA LoA.** A constant-width split-conformal TST interval is essentially an empirical LoA. The added value must come from adaptive per-night width, finite-sample guarantees, robustness to shift, and recalibration.

## Table B. Prior art on uncertainty for sleep scoring (verified)

"Per-night metric PI w/ coverage?" asks whether the work gives a prediction interval for each night's summary metrics with a stated coverage guarantee.

| Work | Venue; DOI/ID | What it does | Per-night metric PI w/ coverage? |
|---|---|---|---|
| Kang et al. 2021 | npj Digit Med 4:142; 10.1038/s41746-021-00515-3 | Entropy flags uncertain epochs for clinician review (κ +0.28) | No |
| Fiorillo et al. 2021 DeepSleepNet-Lite | IEEE TNSRE 29:2076–85; 10.1109/TNSRE.2021.3117970 | MC-dropout uncertainty at epoch level | No |
| Phan et al. 2022 SleepTransformer | IEEE TBME 69(8):2456–67; 10.1109/TBME.2022.3147187 | Entropy-based deferral of epochs | No |
| van Gorp et al. 2022 | Sleep 45(8):zsac134; 10.1093/sleep/zsac134 | Theoretical framework separating aleatoric and epistemic uncertainty | No |
| Bakker et al. 2023 | Sleep 46(2):zsac154; 10.1093/sleep/zsac154 | Hypnodensity vs 6–12 scorers; ambiguity is the rule; ICC 0.91 | No |
| Huijben et al. 2023; Anderer et al. 2023; Fiorillo et al. 2023 | Physiol Meas 44(1) (10.1088/1361-6579/aca641); Front Sleep 2:1163477 (10.3389/frsle.2023.1163477); Sleep 46(5):zsad028 (10.1093/sleep/zsad028) | Huijben: hypnodensity reflects annotator behaviour. Anderer: review of ambiguity and stability metrics. Fiorillo: training on soft labels from multiple scorers | No |
| **Hardarson et al. 2023** | Curr Sleep Med Rep 9(3):140–51; 10.1007/s40675-023-00253-w | **Monte Carlo propagation of staging error to derived sleep parameters** (197 hypnograms). Finds 90% stage accuracy can still give poor parameter estimates | Population-level simulation; **no** per-night PI |
| Heremans et al. 2024 U-PASS | Comput Biol Med 171:108205; 10.1016/j.compbiomed.2024.108205 | Uncertainty-guided pipeline (active learning, deferral) | No |
| Heremans et al. 2025 | J Sleep Res 34(1):e14300; 10.1111/jsr.14300 | U-PASS on wearable EEG; correlates predicted sleep parameters | No |
| Bechny et al. 2024 | Nat Sci Sleep 16:555–72; 10.2147/NSS.S455649 | U-Sleep + "confidence network" (AUROC about 0.83–0.86) to guide physician review; in- and out-of-domain data | No |
| Ganglberger et al. 2024 | Sleep 47(11):zsae202; 10.1093/sleep/zsae202 | Transfer learning plus a **recording-level scorability model** predicting model–expert agreement (R² 0.42) | Night-level QC; no PI |
| Mikkelsen et al. 2020 | IEEE EMBC 2020:645–8; 10.1109/EMBC44109.2020.9175743 | Predicts a night's κ without labels (RMSE 0.078) | Night-level QC; no PI |
| Rusanen et al. 2025 aSAGA | J Sleep Res 34(3):e14362; 10.1111/jsr.14362 | "Grey area" uncertainty for human-in-the-loop scoring | No |
| Dei Rossi et al. 2025 SLEEPYLAND | npj Digit Med 9:55; 10.1038/s41746-025-02237-2 | 24 datasets; ensemble disagreement predicts scorer ambiguity | No |
| Vainikka et al. 2026 | IEEE TBME 73(6):2144–54; 10.1109/TBME.2025.3623380 | MC dropout; **"Hypnodensity Interval"** at the epoch level (name collision risk) | No |
| Kaneda et al. 2026 | Sleep Adv 7(2):zpag054; 10.1093/sleepadvances/zpag054 | Gradient-boosted staging; LoA for TST about ±0.5 h | Population LoA only |
| Liu et al. 2026; Dodet et al. 2025; van der Aar et al. 2025 | Sleep Med (above); NPJ Parkinsons Dis 11:275 (10.1038/s41531-025-01105-w); J Sleep Res e70046 (10.1111/jsr.70046) | Stage uncertainty or mixing used as a disease biomarker | No |
| **Li H et al. 2025 ConMIL** | J Healthc Inform Res 9(4):656–85; 10.1007/s41666-025-00207-7 | **Conformal prediction sets for sleep-stage classification** (and arrhythmia) feeding into LLMs | Epoch-level sets only |
| Amaral et al. 2025 | arXiv:2511.18141 | Conformal regions for Dirichlet regression; applied to a **sleep-stage composition** dataset from covariates | Not from automatic scoring |
| Wei et al. 2026 TMN-LAKDE | IEEE JBHI 30(10):8557–69; 10.1109/JBHI.2026.3677739 | Calibrated KDE prediction intervals on EEG network dynamics (SIESTA, Sleep-EDF); PI width used as an instability marker | Not for sleep metrics |
| Goparaju et al. 2025 | PLoS One 20:e0334950; 10.1371/journal.pone.0334950 | Uncertainty from sampling only a few nights (>35k people) | No |
| Gnassounou et al. 2023 CMMN | NeurIPS 36:10457–76; 10.52202/075280-0459; arXiv:2305.18831 | PSD normalization by optimal transport for cross-subject, session and dataset shift | Accuracy only |
| Gnassounou et al. PSDNorm | arXiv:2503.04582 (2025); ICLR 2026 poster (OpenReview BZMQotjBwW) | Test-time temporal normalization for sleep staging | Accuracy only |
| Li S et al. SPDIM | ICLR 2025 poster (OpenReview CoQw1dXtGb); arXiv:2411.07249 | Source-free adaptation for conditional and **label** shift, including sleep staging | Accuracy only |
| Phan et al. 2020; Arasu & Jahangiri 2025 | Physiol Meas 41:064004 (10.1088/1361-6579/ab921e); arXiv:2509.02982 | Phan: personalization from a single night (KL-regularized fine-tuning, Sleep-EDF). Arasu: test-time adaptation with entropy gates | Accuracy only |
| Adjacent conformal work in EEG | Kumar 2026 J Neural Eng (10.1088/1741-2552/aebe6a); Chatterjee 2026 arXiv:2602.19483; Alqudah 2026 Diagnostics (10.3390/diagnostics16030448) | Kumar: coverage collapses across subjects in fatigue EEG. Chatterjee: personalized calibration fixes seizure CP coverage. Alqudah: conformal sets for OSA severity | Not sleep staging metrics |
| Vallat & Walker 2021 YASA | eLife 10:e70092; 10.7554/eLife.70092 | Open-source staging with stage probabilities | No |

## Novelty conclusion

**Already exists:**
- Epoch-level uncertainty from entropy, MC dropout, confidence networks and ensembles, used for human-in-the-loop deferral.
- Hypnodensity ambiguity and stage mixing as descriptors or biomarkers.
- Recording-level QC or agreement prediction (Mikkelsen 2020; Ganglberger 2024; SLEEPYLAND).
- Monte Carlo propagation of misclassification to sleep parameters at the population level (Hardarson 2023).
- **Epoch-level** conformal sets for sleep stages (ConMIL 2025).
- Conformal regions for stage *composition* from covariates (Amaral 2025).
- Population-level BA LoA for device or algorithm metrics.
- Domain adaptation (CMMN, PSDNorm, SPDIM) and single-night personalization, judged on accuracy only.

**Not found in my searches:**
1. Distribution-free or conformal **per-night prediction intervals** for PSG summary metrics (TST, SE, SOL, WASO, REM latency, %N1/%N2/%N3/%REM) derived from automatic hypnograms, with empirical coverage reported.
2. **Posterior sampling of hypnograms** (HMM forward-filtering backward-sampling over classifier probabilities) used to turn epoch uncertainty into night-level metric distributions or conformal scores.
3. **Cross-cohort coverage evaluation**, for example Sleep-EDF to HMC, and **few-night site recalibration** of intervals.
4. Label-shift-aware conformal methods for sleep metrics.

**Caveats:**
- Semantic Scholar, Google Scholar and IEEE Xplore were not fully searched; EMBC and ICASSP only via PubMed and Crossref.
- Hardarson 2023 and Vainikka 2026 ("Hypnodensity Interval") must be cited and contrasted directly.
- Reviewers will ask how this differs from BA LoA.

## Verified bibliography (record retrieved; DOI shown)

1. Vallat R, Walker MP. An open-source, high-performance tool for automated sleep staging. *eLife* 2021;10:e70092. doi:10.7554/eLife.70092
2. Kemp B, Zwinderman AH, Tuk B, Kamphuisen HAC, et al. *IEEE Trans Biomed Eng* 2000;47(9):1185–1194. doi:10.1109/10.867928
   - Dataset: Sleep-EDF Database [Expanded], PhysioNet. doi:10.13026/C2X676
3. Goldberger AL, Amaral LAN, Glass L, Hausdorff JM, et al. *Circulation* 2000;101(23):e215 (the Crossref record has no page range). doi:10.1161/01.CIR.101.23.e215
4. Alvarez-Estevez D, Rijsman RM. *PLoS ONE* 2021;16(8):e0256111. doi:10.1371/journal.pone.0256111
   - Dataset: HMC sleep staging database, PhysioNet v1.1 (2022), doi:10.13026/t79q-fr32; v1.0.0 (2021), doi:10.13026/gp48-ea60
5. Angelopoulos AN, Bates S. Conformal prediction: a gentle introduction. *Found Trends Mach Learn* 2023;16(4):494–591. doi:10.1561/2200000101
6. Vovk V, Gammerman A, Shafer G. *Algorithmic Learning in a Random World*. Springer, 2005 (doi:10.1007/b106715); 2nd ed. 2022 (doi:10.1007/978-3-031-06649-8)
7. Lei J, G'Sell M, Rinaldo A, Tibshirani RJ, et al. *JASA* 2018;113(523):1094–1111. doi:10.1080/01621459.2017.1307116
8. Romano Y, Patterson E, Candès E. Conformalized quantile regression. *NeurIPS* 2019;32. No DOI; arXiv:1905.03222
9. Tibshirani RJ, Foygel Barber R, Candès E, Ramdas A. Conformal prediction under covariate shift. *NeurIPS* 2019;32. No DOI; arXiv:1904.06019
10. Barber RF, Candès EJ, Ramdas A, Tibshirani RJ. *Ann Stat* 2023;51(2):816–845. doi:10.1214/23-AOS2276
11. AASM scoring manual (Berry RB et al.):
    - The manual itself has no DOI; which edition and version to cite is **UNVERIFIED**, so cite the version you actually use.
    - Verified related record: Berry RB, Brooks R, Gamaldo C, et al. AASM Scoring Manual Updates for 2017 (Version 2.4). *J Clin Sleep Med* 2017;13(5):665–666. doi:10.5664/jcsm.6576
12. Rosenberg RS, Van Hout S. *J Clin Sleep Med* 2013;9(1):81–87. doi:10.5664/jcsm.2350
13. Danker-Hopfe H, Anderer P, Zeitlhofer J, et al. *J Sleep Res* 2009;18(1):74–84. doi:10.1111/j.1365-2869.2008.00700.x
14. Stephansen JB, Olesen AN, Olsen M, et al. *Nat Commun* 2018;9:5229. doi:10.1038/s41467-018-07229-3
15. Perslev M, Darkner S, Kempfner L, et al. U-Sleep. *npj Digit Med* 2021;4:72. doi:10.1038/s41746-021-00440-5
16. Phan H, Andreotti F, Cooray N, Chén OY, et al. SeqSleepNet. *IEEE TNSRE* 2019;27(3):400–410. doi:10.1109/TNSRE.2019.2896659
17. Supratak A, Dong H, Wu C, Guo Y. DeepSleepNet. *IEEE TNSRE* 2017;25(11):1998–2008. doi:10.1109/TNSRE.2017.2721116
18. Rabiner LR. *Proc IEEE* 1989;77(2):257–286. doi:10.1109/5.18626
19. Carter CK, Kohn R. *Biometrika* 1994;81(3):541–553. doi:10.1093/biomet/81.3.541
20. Frühwirth-Schnatter S. *J Time Ser Anal* 1994;15(2):183–202. doi:10.1111/j.1467-9892.1994.tb00184.x
21. Ohayon MM, Carskadon MA, Guilleminault C, Vitiello MV. *Sleep* 2004;27(7):1255–1273. doi:10.1093/sleep/27.7.1255
22. Alexandari A, Kundaje A, Shrikumar A. *ICML* 2020, PMLR 119:222–232. No DOI; arXiv:1901.06852
23. Saerens M, Latinne P, Decaestecker C. *Neural Comput* 2002;14(1):21–41. doi:10.1162/089976602753284446
24. Lipton ZC, Wang Y-X, Smola A. *ICML* 2018, PMLR 80:3122–3130. No DOI; arXiv:1802.03916
25. Ye C, Tsuchida R, Petersson L, Barnes N. *WACV* 2024:1062–1071. doi:10.1109/WACV57701.2024.00111
    - The abstract describes a MAP label-shift model; that it uses the acronym "MAPLS" is **UNVERIFIED**, so check the full text.
26. Prior-art DOIs: see Table B (all retrieved).
