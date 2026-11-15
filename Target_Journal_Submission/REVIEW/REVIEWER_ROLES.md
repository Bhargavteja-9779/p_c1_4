# Ten reviewer perspectives (GLOBAL UPDATE 5)

| # | Role | Focus |
|---|---|---|
| 1 | Novelty & prior-art reviewer | Search for similar work (conformal intervals for sleep parameters, hypnogram sampling, night-level uncertainty, uncertainty propagation in staging, patents). Attempt to invalidate novelty claims. Check differentiation from Hardarson 2023, ConMIL, Ganglberger 2024, Vainikka 2026, Bakker 2023, Kang 2021. |
| 2 | Methodology reviewer | Mathematical correctness of BCTS, hybrid HMM emissions, tau fitting, FFBS, conformal score/quantile, validity argument (exchangeability with 2 nights/subject), clipping, censoring of REML; consistency of equations with code. |
| 3 | Experimental-design reviewer | Fairness of comparators, baselines, splits, hyper-parameter selection, evaluation protocol, whether conclusions follow; pre-registration vs actual; post-hoc additions. |
| 4 | Statistical reviewer | Coverage CIs, split averaging, Wilcoxon on per-subject interval scores, Holm scope, effect sizes, bootstrap, multiplicity across stagers, reporting of non-significant/negative results, interval score properties. |
| 5 | Dataset & leakage reviewer | Data quality, licences, label-free windows, subject leakage, HMM cross-fitting, feature normalisation, YASA training data overlap with cohorts, R&K vs AASM, unscored epochs, ST drug nights. |
| 6 | Robustness & generalisation reviewer | Try to break the central claim: cohort shift, corruption experiment design, small ST, montage shift, subgroup coverage, age, whether recalibration claim is robust (variance across repetitions, n=10 conservativeness). |
| 7 | Computational-efficiency reviewer | Cost of FFBS/parameters vs stager, memory, scaling to long recordings / many nights, deployment feasibility, numba, reproducibility of timings. |
| 8 | Literature & citation reviewer | Verify every reference (references.json, reference_audit.csv) and that claims attributed to them are supported; missing key competing studies; citation formatting per Sleep Medicine (numbered, square brackets); reference count ≤50. |
| 9 | Associate Editor, Sleep Medicine | Scope fit, clinical relevance, novelty level for this journal, author-guideline compliance (word counts, abstract structure, highlights ≤85 chars, display items ≤8, declarations incl. generative-AI statement), desk-rejection risks. |
| 10 | Hostile competing researcher | Show the work is incremental or unnecessary: would a simpler method (constant-width / BA-LoA / entropy scaling / CQR) do as well? Is the TST gain just calibration? Are comparisons unfair? Is the dataset favouring the method? |
