# Datasets and data-leakage audit (Phases 7–8)

## Datasets
| | Sleep-EDF SC | Sleep-EDF ST | HMC |
|---|---|---|---|
| Source | PhysioNet sleep-edfx v1.0.0 (Kemp et al. 2000) | same | PhysioNet hmc-sleep-staging v1.1 (Alvarez-Estevez & Rijsman 2021) |
| Licence | Open Data Commons Attribution v1.0 | same | CC BY 4.0 |
| Population | Healthy community-dwelling adults 25–101 y, ambulatory home recordings (1987–1991) | 22 adults with mild difficulty falling asleep; in-hospital; placebo and temazepam nights (1994) | Consecutive clinical PSGs at a Dutch sleep centre (2018), mixed sleep disorders |
| Nights / subjects | 153 / 78 (2 nights per subject except 3 subjects) | 44 / 22 (2 nights per subject) | 151 / 151 |
| Scoring | R&K (S3+S4 merged to N3), one scorer per night | R&K | AASM, one scorer per night |
| Signals used | Fpz-Cz EEG, horizontal EOG (100 Hz) | same | C4-M1 EEG, E1-M2 EOG (256 Hz → 100 Hz); F4-M1 and E1–E2 cached for montage analyses |
| Lights-off/on | lights-off in SC-subjects.xls; no lights-on | lights-off in ST-subjects.xls | both annotated |
| Known limitations | old analogue recordings; R&K not AASM; EMG only as 1-Hz envelope; daytime naps in 20-h files | small n; drug condition | no per-subject demographics released; single scorer |

## Leakage audit
| Risk | Assessment | Mitigation implemented |
|---|---|---|
| Subject leakage (two nights of the same person in train and test) | Real for SC and ST | All splits (stager CV, HMM cross-fitting, conformal calibration/test splits, LOSO, few-night recalibration) are grouped by **subject**. |
| Leakage through analysis window | Cropping to "30 min before first / after last sleep epoch" (common in Sleep-EDF papers) uses the reference hypnogram | Windows defined only by lights-off/lights-on metadata and a fixed 10-h SC window; never by labels. |
| Leakage through HMM parameters | Transition matrix, prior, calibration and tau use labels | Fitted only on labelled nights that exclude the evaluated night: within-cohort 5-fold cross-fitting by subject; cross-cohort uses SC only. |
| Leakage into the base stagers | S2 trained on SC | SC predictions are out-of-fold (subject-grouped 5-fold); S1 (YASA) never saw any of the three cohorts. |
| Pre-processing leakage | YASA features normalise within each night | Per-night normalisation uses only that night's signal (unsupervised, test-time permissible); no cross-night statistics. |
| Test contamination via hyper-parameter tuning | Possible if tuned on evaluation nights | Stager hyper-parameters fixed a priori; the only fitted HMM quantity (tau) is fitted on source/training-fold nights; the primary method, α and the error thresholds of the protocol were pre-specified (PROTOCOL.md); comparators and decision thresholds were added later (Supplementary S1). |
| Duplicate / near-duplicate nights | None expected; each PSG file is a distinct night | File-level uniqueness checked via PhysioNet SHA256 manifests. |
| Label leakage via unscored epochs | "?"/movement epochs | Marked −1 and excluded identically from reference and automatic parameters. |
| Temporal leakage | Not applicable (no longitudinal prediction) | – |
| Few-night recalibration | Target calibration nights could share subjects with test nights | Target calibration nights are whole subjects disjoint from test subjects. |
