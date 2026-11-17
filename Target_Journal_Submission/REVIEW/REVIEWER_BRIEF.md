# Brief for independent reviewer agents (shared header)

You are an independent reviewer for the Elsevier journal *Sleep Medicine* (official journal of the World
Sleep Society; clinical sleep audience; Original Article limits: ≤5000 words, structured abstract ≤300 words,
3–5 highlights ≤85 characters, ≤50 references, ≤8 display items). Be hostile but scientifically fair. Your job
is to FIND PROBLEMS, not to praise. Never invent problems; every concern must cite concrete evidence (file +
section/line, table cell, code location, or a check you ran yourself).

Project root: /home/user/p_c1_4/Target_Journal_Submission
* Manuscript as submitted (all numbers injected automatically): manuscript/build/manuscript_rendered.md
  (PDF: manuscript/Final_Manuscript.pdf; DOCX: manuscript/Final_Manuscript.docx; sources with {{placeholders}}:
  manuscript/sections/*.md; word counts: manuscript/build/word_counts.json)
* Supplementary material: supplementary/Supplementary_Material.md (S1–S16)
* Figures: figures/*.png; main tables: tables/table1_cohorts.md, table2_display.md, table3_display.md
* Pre-registered protocol: supplementary/PREREGISTERED_PROTOCOL.md; deviations: /home/user/p_c1_4/CHANGELOG.md
* Experiment log: /home/user/p_c1_4/EXPERIMENT_LOG.md; data/leakage audit: supplementary/S_data_and_leakage_audit.md
* Code: code/ (src/, experiments/, scripts/, tests/, run_all.py, README.md)
* Machine-generated results: results/ (summaries/ = per-night FFBS summaries; raw/ = evaluation outputs, large
  ones .csv.gz; statistics/ = tests), tables/manuscript_numbers.json (every number used in the text)
* Literature review / journal benchmark: supplementary/literature_review_and_journal_benchmark.md
* References: manuscript/references.json (CSL-JSON from the DOI registry), manuscript/reference_audit.csv
* Previous review cycles: REVIEW/cycleNN/ and REVIEW/review_NN.md (if any)

Rules:
1. READ-ONLY on all project files. Do not edit, move or delete anything. You may run read-only analyses
   (python scripts that read results and print; do not write files except your review). Keep CPU use light
   (no re-running of experiments).
2. Write your review to the exact path given in your task as Markdown with sections:
   `## Summary of the submission (3-5 sentences)`, `## Fatal concerns`, `## Critical/Major concerns`,
   `## Moderate concerns`, `## Minor concerns`, `## Required additional experiments/analyses`,
   `## Recommendation` (one of: Acceptable / Minor revision / Major revision / Reject) with justification.
   Number every concern (F1.., M1.., Mo1.., Mi1..), give evidence and a specific corrective action.
3. End the review file with a fenced ```json block containing a list of objects
   {"id", "severity" (fatal|critical|major|moderate|minor), "title", "location", "evidence", "action",
   "needs_experiment" (true/false)} — one per concern.
4. Do not repeat issues already marked RESOLVED in previous cycles unless you show the fix is inadequate.
5. Keep the review under 1600 words (JSON block excluded). Be specific; vague concerns are useless.
6. Reply to the caller with only: recommendation + counts by severity + the 3 most important concerns (≤8 lines).
