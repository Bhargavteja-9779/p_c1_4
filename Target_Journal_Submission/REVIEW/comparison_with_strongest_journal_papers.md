# Comparison with the strongest comparable papers in *Sleep Medicine* (Global Update 7)

Benchmark papers (all verified via PubMed; details in `supplementary/literature_review_and_journal_benchmark.md`):
B1 Baumert et al. 2023 (doi:10.1016/j.sleep.2023.04.002) — age bias of deep-learning staging, 7,777 PSGs;
B2 Svensson et al. 2024 (doi:10.1016/j.sleep.2024.01.020) — Oura Gen3 vs multi-night ambulatory PSG, 96 subjects;
B3 Rohrscheib et al. 2026 (doi:10.1016/j.sleep.2026.108828) — HSAT AI scoring, multi-scorer, 95% CIs on LoA;
B4 Thiesse et al. 2022 (doi:10.1016/j.sleep.2022.04.013) — cardiac-based staging vs 5 scoring centres;
B5 Yook et al. 2024 (doi:10.1016/j.sleep.2024.01.015) — respiratory-event detection with SHHS external validation.

| Dimension | This study | Comparison | Verdict |
|---|---|---|---|
| Novelty | First per-night conformal intervals for PSG parameters; FFBS-based adaptive scale; factorial separation of centre and scale | B1–B5 are validation/bias studies of specific algorithms or devices; none provides per-night uncertainty in clinical units | **Stronger** (methodological novelty), but the gain over bias-corrected limits of agreement is parameter-specific |
| Clinical significance | Reliability statement per night; local recalibration recommendation | B1 (age bias) and B3 (HSAT deployment) have direct clinical populations and larger clinical impact | **Weaker/comparable**: our cohorts are smaller and partly non-clinical (SC healthy) |
| Sample size | 348 nights / 251 subjects / 3 cohorts | B1 7,777 PSGs; B5 SHHS 5,804; B2 96 subjects (421k epochs) | **Weaker** than B1/B5, **stronger** than B2–B4 |
| External validation | Pretrained stager external to all cohorts; cross-cohort transfer + recalibration | B1 cross-age; B4 multi-centre; B5 SHHS | **Comparable/stronger** (explicit transport analysis) |
| Baselines | BA-LoA, distribution-free LoA, 3 constant-width centres, 2 CQR variants, entropy scaling, raw posterior, ablations | Most benchmark papers compare against PSG only (no competing uncertainty method) | **Stronger** |
| Statistical rigour | Pre-registered protocol, 500 subject-grouped splits, LOSO paired Wilcoxon with Holm, cluster bootstrap, exact binomial/bootstrap CIs | B3 reports CIs on LoA; most report BA ± paired tests | **Stronger** |
| Robustness | Signal corruption, montage shift, subgroup coverage, seeds, α | B1 age; B5 hypopnea-dominant subgroups | **Comparable/stronger** |
| Generalisation | Two stagers (one external), three cohorts | B1 one model family; B5 one model | **Comparable** |
| Efficiency | ≈ seconds per night on one CPU core (Supplementary S15) | rarely reported | **Stronger** (reported) |
| Reproducibility | Public data, full code, one-command pipeline, machine-generated numbers | Code availability rare (1 of 25 benchmark papers) | **Stronger** |
| Writing/clinical framing | Methods-heavy; must keep clinical message explicit | Benchmark papers are clinically framed | **Risk**: needs clear clinical take-home messages |

Direct quantitative comparison with B1–B5 is impossible (different tasks, outcomes and cohorts); no superiority over these papers is claimed.
