# Academic Integrity Verification Report — Stage 2.5 (Mode 1, pre-review)

ARS v3.24.4 `integrity_verification_agent`, run as two role-separated passes in one Claude Code session.
Target: `manuscript/build/manuscript_rendered.md` (SHA-256 `ce84df25…a243b138`), repo commit `af6aab7`.
Detailed evidence:
- [phaseABD_references_citations_originality.md](phaseABD_references_citations_originality.md) — Phases A, B, D
- [phaseCE_data_claims_failuremodes.md](phaseCE_data_claims_failuremodes.md) — Phases C, E, AI Research Failure Mode Checklist

## Verdict

**FAIL**: 4 SERIOUS, 3 MEDIUM, 27 MINOR. AI Research Failure Mode Checklist **BLOCKS** (Mode 1 SUSPECTED).

No fabricated reference, no retracted source, no copied text, and no untraceable number was found. All 189 filled-in
numbers and every cell of Tables 1–3 trace to machine outputs, and the primary analysis (E12/E15, both stagers, 300
split tasks) re-executed bit-exactly from the shipped code and stager predictions. The failures are about **what the
text claims**, not about the data.

## Verification summary

| Phase | Scope at Stage 2.5 | Checked | Verdict | Issues |
|---|---|---|---|---|
| A — references | 100 % | 51/51 entries; 0 dangling, 2 orphan | FAIL | 2 MEDIUM, 7 MINOR |
| B — citation context | ≥ 30 % | 62/84 instances (74 %) | FAIL | 1 SERIOUS, 3 MINOR |
| C — data | 100 % of registered surfaces | 189 keys + Tables 1–3; 232 key-level checks, 231 matched | FAIL | 1 MEDIUM, MINOR items |
| D — originality | ≥ 30 % | 19/43 body paragraphs (44 %) | PASS | 0 (self-plagiarism not checkable: author names are placeholders) |
| E — claims | 100 % high-impact + sentinel | all high-impact claims + sentinel | FAIL | 3 SERIOUS (4 MAJOR_DISTORTION), 14 MINOR_DISTORTION, 0 UNVERIFIABLE |

Issue IDs below keep the prefix of the sub-report they come from (ABD- or CE-).

## SERIOUS (must fix)

| ID | Location (rendered md line) | Problem | Verified by orchestrator |
|---|---|---|---|
| ABD-SERIOUS-1 | Methods L86; Supplement L125–126 | Claims the CV+ guarantee (≥ 1 − 2α) of Barber et al. 2021 for a design in which calibration scores are cross-fitted but **test nights use the model refit on all calibration nights**. Barber et al.'s CV+ uses the K fold models at test time; for the refit variant (their CV / jackknife) they give no distribution-free guarantee. | yes — text at L86 and `e12_honest_protocol.py` docstring confirm the refit design |
| CE-SERIOUS-1 | Discussion L157 | "fell below 80 % in **up to** 17 % of our repetitions": 17 % is the median over the 8 parameters (ST, 10 nights); per-parameter maximum is 26 % (N2 %, ST); HMC 2–16 %. | yes — `results/statistics/e15_local.csv` |
| CE-SERIOUS-2 | §3.3 L123 heading; Methods L106 | The fixed-centre scale comparison is labelled "the pre-specified criterion". The protocol's criterion is conjunctive ("better … **only if** IS lower with Holm p < 0.05 **and** Spearman CI excludes 0") and names Bland–Altman LoA and raw-centre split-conformal as the constant-width comparators; the fixed-centre comparator was added after the first results. Judged that way, it holds in 12/24 and 10/24 combinations at the fixed centre and 5/24 and 2/24 against Bland–Altman, vs the 15/24 reported. | yes — `supplementary/PREREGISTERED_PROTOCOL.md` l.67–70 |
| CE-SERIOUS-3 | Abstract L31 | "decided 64 % of nights with 98.7 % accuracy (automatic TST alone: 84.2 %)" compares the decided subset with all nights. On the same decided nights automatic TST was 97.2 % accurate; on the undecided 36 % it was 61 %. | no (from regenerated per-night file; sub-report reports a bit-exact regeneration) |

## MEDIUM (must fix)

| ID | Location | Problem |
|---|---|---|
| ABD-MEDIUM-1 | ref `goldberger2000` | Subtitle and page range e215–e220 missing. |
| ABD-MEDIUM-2 | ref `bourlard1994` | Book subtitle ": A Hybrid Approach" missing. |
| CE-MEDIUM-1 | §3.8 L144; Table S10; key `seed_max_cov_range` | "at most 2.5 pp across 3 stager seeds" is not reproducible from the shipped files (2.63 pp). The seed-1 file was replaced after the last build, the seed-2 file came from pre-revision code, and its log is empty. Fix: re-run E04 for `lgbm_sc_s1`/`lgbm_sc_s2` with current code (predictions are shipped) and rebuild. |

## MINOR (recommended at 2.5; must be fixed by 4.5)

27 items, listed with suggestions in the two sub-reports. Main groups: reference metadata and author-name formats
(Bakker 2023 and Dei Rossi year/volume, patent entry); two orphan references (`rohrscheib2026`, `vainikka2026`);
Bland–Altman 1999 used in adapted form without saying so (L89); van Gorp 2022 cited for "hypnodensity" (L44);
three uncited claims (L95, L103, L157); abstract L31 omits "median over parameters"; σ̄ change after first results
not mentioned at L86; comparators said to be added "during review" (L89) when they were added before review cycle 1;
the list of analyses run on the pre-registered design (L93) is incomplete; undisclosed separate Holm family and
1000 vs 2000 bootstrap resamples (L106); Fig. 5d shows an AUROC with 8 events against the supplement's ≥ 10 rule;
caption details for Fig. 1, Fig. 5d and Table 3; robustness sentence "all methods lost coverage" overstated (L144);
word counts within limits only under the build script's token convention (abstract 301 by whitespace tokens).

## AI Research Failure Mode Checklist

| Mode | Verdict | Blocks at 2.5 |
|---|---|---|
| 1 Implementation bug | SUSPECTED (scoped to the stale seed-variability runs, CE-MEDIUM-1) | **yes** |
| 2 Hallucinated citation | CLEAR | no |
| 3 Hallucinated result | CLEAR | no |
| 4 Shortcut reliance | CLEAR | no (flag-only at 2.5) |
| 5 Bug reframed as insight | CLEAR | no |
| 6 Methodology fabrication | CLEAR (minor notes) | no |
| 7 Frame-lock | INSUFFICIENT EVIDENCE — needs the author's answer | no (warning; re-checked at 4.5) |

Author options for the Mode 1 block: (a) confirm and fix (re-run the seed analysis with current code, rebuild);
(b) override with recorded reasoning; (c) revise the passage (drop or soften the seed sentence) and re-check.

## Not run

Cross-model verification (`ARS_CROSS_MODEL` unset); cache-staleness advisory (no cache); D7 experiment-declaration
check and passport-based checks (no ARS Material Passport; experiment intake question pending with the author);
claim-registry coverage tooling (E1-COVERAGE-UNRESOLVED); E4 scope advisory (no RQ Brief); stager inference from raw
PSG (raw data not in the repo).

## Correction list for the FAIL loop (round 1 of max 3)

1. L86 + Supplement L125–126: replace the CV+ guarantee sentence (reword so validity rests on empirical coverage, or
   implement true CV+ and quote Barber et al. Theorem 4 exactly).
2. L157: "a median of 9 % (HMC) and 17 % (ST) of repetitions across parameters, and up to 26 % for single parameters".
3. L106 + L123: state the pre-registered conjunctive criterion and its result as reported; label the fixed-centre
   comparison as an added (post-hoc) analysis.
4. L31 (+ §3.7): compare like with like (98.7 % vs 97.2 % on decided nights; 61 % on undecided ones).
5. References `goldberger2000`, `bourlard1994`: complete metadata.
6. Seed variability: re-run E04 seeds 1–2 with current code and rebuild (or soften the sentence).
7. MINOR items as listed in the sub-reports.
