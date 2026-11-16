# Cycle 1, wave B reviewer prompts (launched after the manuscript was rebuilt with final numbers)

Common preamble: "You are Reviewer #N (<ROLE>) in an independent 10-reviewer panel, review cycle 1. First read
/home/user/p_c1_4/Target_Journal_Submission/REVIEW/REVIEWER_BRIEF.md and your row in REVIEWER_ROLES.md. Read the rendered
manuscript manuscript/build/manuscript_rendered.md (all numbers were injected automatically from
tables/manuscript_numbers.json) and the PDF manuscript/Final_Manuscript.pdf if useful; supplementary tables in tables/ and
supplementary/Supplementary_Material.md. Write your review to REVIEW/cycle01/agentNN_<role>.md (≤1500 words, brief's
format). Do not modify any other file. Reply with a 5-line summary only."

* #3 Experimental design: fairness of comparators (raw vs calibrated vs bias-corrected centres; CQR variants; BA-LoA),
  split design (500 subject-grouped 50/50 splits + LOSO), what was pre-registered vs added later (CHANGELOG), whether
  conclusions follow from the evidence, missing comparators (e.g. regression-based LoA for heteroscedasticity,
  Mondrian/group-conditional conformal), clinical-utility analysis design, thresholds.
* #4 Statistics: coverage CIs, averaging over overlapping splits (not independent), Wilcoxon on per-subject LOSO interval
  scores (paired; zero-handling), Holm scope (within cohort×stager; multiplicity across stagers and α), effect sizes (r_rb),
  cluster bootstrap for AUROC with few events, interval score as primary efficiency metric, reporting of negative results,
  any statistical claim not supported by a table. Verify several manuscript numbers against tables/*.csv and results/.
* #6 Robustness & generalisation: try to break the central claim: cross-cohort failure (N3 % in HMC), montage shift for
  LightGBM, small ST, few-night recalibration variability (probability of site coverage <0.85; conservativeness with n=10),
  corruption design (calibration clean / test corrupted is realistic?), subgroup coverage, age; propose and justify
  additional experiments.
* #7 Computational efficiency: cost of FFBS (M samples) and parameter computation relative to the stager (tables/
  tableS_efficiency.csv, results/raw/e10_efficiency*.{csv,json}), memory, scaling to multi-night/ambulatory recordings,
  sensitivity to M (summaries contain ffbsM100/ffbsM300 SDs), deployment feasibility, reproducibility of timings.
* #9 Associate Editor (Sleep Medicine): scope and clinical relevance, novelty level for this journal, compliance with
  author guidelines (≤5000 words main text — see manuscript/build/word_counts.json; structured abstract ≤300 words; 3–5
  highlights ≤85 characters; ≤8 display items; ≤50 references; numbered square-bracket citations; IMRaD + Conclusion;
  generative-AI declaration; data/code availability), desk-rejection risks, title/abstract quality.
* #10 Hostile competing researcher: show the work is incremental/unnecessary — does the bias-corrected constant-width
  conformal interval (distribution-free LoA) or calibrated-centre constant width do as well? Is any remaining gain due to
  centring rather than scaling? Is YASA on Sleep-EDF a weak stager that favours the method? Would a deep stager change
  conclusions? Re-analyse the CSVs yourself to check claims.
