# Cycle 2 reviewer prompt (delta review after revision 1)

Common prompt (N = 01..10, ROLE from REVIEWER_ROLES.md):

"You are Reviewer #N (<ROLE>) in an independent 10-reviewer panel, review cycle 2 (revision 1). First read
/home/user/p_c1_4/Target_Journal_Submission/REVIEW/REVIEWER_BRIEF.md and your row in REVIEWER_ROLES.md. Then read YOUR OWN
cycle-1 review (REVIEW/cycle01/agentNN_<role>.md) and the authors' consolidated response (REVIEW/review_01.md).
Read the revised rendered manuscript manuscript/build/manuscript_rendered.md (all numbers injected automatically from
tables/manuscript_numbers.json), the PDF manuscript/Final_Manuscript.pdf if useful, tables/*.csv and
supplementary/Supplementary_Material.md. The primary within-cohort analysis is now the end-to-end ('honest') protocol
(code/experiments/e12_honest_protocol.py, statistics code/experiments/e15_honest_stats.py; results/statistics/e15_*.csv).
Part A — for EACH of your cycle-1 findings: RESOLVED / PARTLY / NOT RESOLVED, with one line of evidence (file/number).
Part B — NEW problems introduced or revealed by the revision (verify numbers against the CSVs yourself; check that every
claim in Abstract, Highlights, Results, Discussion, Conclusion is supported by a table/figure and is not overstated).
Part C — recommendation (accept / minor / major / reject) and the three changes that would most raise acceptance chances.
Write your review to REVIEW/cycle02/agentNN_<role>.md (≤1200 words) ending with a JSON block of findings
[{"id","severity":"fatal|critical|major|moderate|minor","title","location","evidence","action","needs_experiment"}].
Do not modify any other file. Reply with a 5-line summary only."
