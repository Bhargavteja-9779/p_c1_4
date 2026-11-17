# Review cycle 1 — consolidated report and author response

Ten independent reviewer agents (roles: REVIEWER_ROLES.md; full reviews: cycle01/agentNN_*.md, each with a JSON
findings block). All ten recommended **Major revision** (the Associate Editor: return before external review).
Findings: 127 (1 fatal, 5 critical, 39 major, 40 moderate, 42 minor). Duplicates were merged below; independent
supporting reviewers are listed. Status codes: FIXED (change made and verified), RERUN (fixed by re-running
experiments in revision 1), REPORTED (documented as limitation/deviation because it cannot be fixed with the
available data), REJECTED (with reason).

## Fatal / critical

| # | Issue (reviewers) | Decision and action | Status |
|---|---|---|---|
| C1 | Table 2 corrupted in DOCX/PDF: '|' inside cells split columns, ST/HMC values lost (9; 8) | Table 2 rebuilt as long-format table without in-cell separators (YASA in main text, LightGBM in supplement); rendered DOCX/PDF inspected | FIXED |
| C2 | Closest prior art uncited: van Gorp et al. 2023 (IEEE JBHI, U-Flow; ICASSP 2023) already sample whole hypnograms for per-night sleep statistics; Philips patent EP4388985A1 (1; 8) | Verified via Crossref/Google Patents; cited; Introduction gap statement rewritten; novelty repositioned to *calibrated* (conformal) coverage, external transfer and local recalibration; claim "posterior hypnogram sampling is new" withdrawn | FIXED |
| C3 | "A few locally scored nights correct TST bias" untested: recalibration used ~80% of each cohort; few-night experiment refitted only the conformal quantile (6; 7; 9; 10; 2; 5) | New end-to-end honest protocol E12: every label-dependent component (BCTS, prior, transitions, τ, conformal quantile) fitted only on 10/20/30 local nights (cross-fitted), 50 repetitions; bias and coverage reported from E12 only | RERUN |
| C4 | Unequal use of labelled data: HMM/BCTS cross-fitted on ~80% of each cohort incl. test-half labels; comparators use 50% (10; 2; 5; 3) | E12 honest protocol (50/50 subject splits, all components fitted on the calibration half) made the PRIMARY within-cohort analysis; pre-registered cross-fitted analysis moved to supplement | RERUN |
| C5 | Pre-specified method not better overall than simple/variant competitors; gain concentrated in TST (10; 3) | Claims narrowed: report mean ratio with and without TST, wins/losses, and that unregularised/CQR variants are better; title/abstract/highlights rewritten | FIXED (text) / RERUN (numbers) |
| C6 | Regression-based (heteroscedastic) Bland–Altman limits missing; "strongest competitor" label wrong (3; 8) | Added `ba_reg` (Bland & Altman 1999) and an exactly valid signed-residual distribution-free LoA (`scp_signed`); parametric LoA now a t-based prediction interval | RERUN |
| C7 | Placeholders/declarations unfilled (9) | Cannot be completed by the AI; listed as AUTHOR ACTION REQUIRED in the final package | REPORTED |

## Major (merged)

| # | Issue (reviewers) | Action | Status |
|---|---|---|---|
| M1 | Wilcoxon tests pseudo-median, not the reported mean; stars contradict ratios; ratios (splits) and stars (LOSO) from different analyses (4; 10) | Sign-flip permutation test of the mean per-subject interval-score difference; ratio, bootstrap CI and p from the same analysis | FIXED |
| M2 | LOSO coverage nominal by construction; bootstrap CIs meaningless (4) | LOSO coverage CIs dropped from claims; coverage reported from repeated splits/E12 with between-split spread | FIXED |
| M3 | Conditional/subgroup coverage pooled over parameters; "≥40 nights" counted rows (4; 6) | Subgroups now ≥20 distinct nights; per-parameter ranges reported (worst-accuracy quartile and ≥60 y) | FIXED |
| M4 | Pre-registered items omitted (Spearman criterion; width-ratio CIs; M; calibration size; 50 Hz noise) (4; 7; 3) | E13 run and reported (criterion met in 30/48 cells — reported as partial failure); M=100 suffices; calibration-size sensitivity; 50 Hz line noise not run: listed as deviation (YASA band-pass removes it) | RERUN / REPORTED |
| M5 | Reference unscored mask applied to automatic hypnograms (label leakage) (5) | Automatic hypnograms evaluated on all window epochs; reference unscored epochs treated as wake | RERUN |
| M6 | Ablations changed centre and scale together; misattribution (2) | Scale-only ablations added (`norm_reg_ind_s`, `norm_reg_ffbs1_s`); Discussion corrected | RERUN |
| M7 | SC→HMC N3 failure possibly montage (YASA also changes montage) or R&K→AASM rules, not population (5; 6) | E14: YASA re-run on HMC with frontal F4-M1; text states YASA montage change; Moser 2009 cited for rule effects | RERUN |
| M8 | "Ten nights restored coverage" is the textbook conformal guarantee; site-level risk and widths understated (6; 9) | Text states this explicitly; reports P(realised coverage < 80%) and widths with n=10; parametric LoA compared at equal n | FIXED |
| M9 | Corruption: calibration clean/test corrupted unrealistic; gain from centre not width (6; 3) | Reported as limitation; comparison includes calibrated-centre constant-width interval; claim restricted | REPORTED |
| M10 | Flagging: label-free |raw − calibrated plug-in| beats width for TST; no operating point (3; 9) | Signal added to E07; operating-point (decision-threshold) analysis from E12 intervals | RERUN |
| M11 | Generative-AI disclosure must appear in Methods (9) | Methods 2.9 now describes AI assistance | FIXED |
| M12 | Misattributed citations: Rohrscheib 2026 (AHI study), Hardarson 2023 (assumed independent errors), Baumert 2023 ("older patients") (8; 1) | Citations corrected (Kaneda 2026 for parameter agreement; Hardarson cited for population-level propagation only; age claim removed/re-sourced) | FIXED |
| M13 | Deployment workflow/one-off costs/memory under-reported (7) | E10 extended: JIT and source-model fitting time, peak memory for 7×24 h, single-thread setting | RERUN |
| M14 | SC window artefacts (start/end in sleep; 116 min morning wake) (5) | Counted and reported; WASO-SC flagged as definition artefact | REPORTED |
| M15 | Advantage vanishes with smaller stager errors; no deep stager (10; 6) | Easier/harder-night stratified comparison reported; absence of a deep stager stated as limitation | REPORTED |
| M16 | Too methodological for readership; which number to report unclear (9) | Clinical framing: a practical reporting recommendation and decision-threshold analysis | FIXED |

## Moderate / minor
All 82 moderate/minor items were triaged. Implemented: non-finite scores treated as +∞; CQR quantile crossing;
CQR-QR given plug-in, calibrated plug-in and FFBS SD features; Chib 1996, Barber et al. 2021 (CV+ guarantee for
cross-fitted scores), Bland & Altman 1999, Moser 2009 cited; ethics wording corrected; figure order; supplement
truncation removed; Holm scope stated; "significant" always with the test named; BA t-based; bootstrap counts
stated as implemented. Reported as limitations: compositional constraint/joint coverage of stage percentages;
censored REML; single-scorer reference; both stagers feature-based; ST small; transport tested one direction;
protocol not independently time-stamped (git history provided instead).

## Rejected
None outright. The request for a modern deep stager is acknowledged but not feasible within this study's
compute budget (CPU only) and is stated as a limitation.
