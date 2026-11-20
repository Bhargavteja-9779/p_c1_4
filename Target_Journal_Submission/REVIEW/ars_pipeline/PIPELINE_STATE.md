# ARS pipeline run — state log

Framework: academic-research-skills (ARS) v3.24.4, commit `bd57330` of github.com/Imbad0202/academic-research-skills
(installed locally as symlinks under `/home/user/p_c1_4/.claude/skills/`; not committed; licence CC BY-NC 4.0).
Orchestrator: `academic-pipeline` (Mode A, orchestrator-driven), run in a Claude Code cloud session.
This file is a lightweight stand-in for the ARS Material Passport (Schema 9); the YAML passport, run ledger
and opt-in features (cross-model audit gate, L3 claim audit, passport reset) are not used in this run.

- run_id: `ars-p_c1_4-2026-11-20-a`
- Started: 2026-11-20
- User request (verbatim): "Academic Research Skills (academic-research-skills) install this repo and run its full pipeline to improve my work"

## Entry point

Mid-entry with an existing manuscript → Stage 2.5 (INTEGRITY), then Stage 3 (REVIEW) if PASS.
Material Passport check: no passport exists → full Stage 2.5 verification required (prior internal review cycle 1 in
`REVIEW/cycle01/` and `REVIEW/review_01.md` is context only, not a substitute).

Input artefacts (SHA-256):

| Artefact | SHA-256 |
|---|---|
| `manuscript/build/manuscript_rendered.md` | `ce84df25e82ef81975409c4a1b12c3c8be9e3c67cdb1c719da961739a243b138` |
| `manuscript/Final_Manuscript.docx` | `e65ba4c158a1f1220b0d64e5d4f4cffb8ed259d17e3cfe65c3471bc5e9dd5f40` |
| `supplementary/Supplementary_Material.md` | `4236f11f166c0bd35343683e4385e216694b4d25cdf5579cbe67ab8ded2560b7` |

Repo commit at entry: `af6aab7`.

## Experiment intake declaration (#925)

- status: PENDING — question to be asked of the author at the Stage 2.5 checkpoint, answer to be recorded verbatim.
- Deviation: the Stage 2.5 evidence-gathering agents were dispatched before the question was asked. No gate
  verdict will be recorded until the author answers.

## Stage log

| Stage | Status | Started | Finished | Deliverables | Decision |
|---|---|---|---|---|---|
| 2.5 INTEGRITY (Mode 1) | FAIL — awaiting author at MANDATORY checkpoint | 2026-11-20 | 2026-11-20 | `stage2_5_integrity/INTEGRITY_REPORT_stage2_5.md` (+ 2 sub-reports) | pending: intake answer; FAIL-loop fixes; Mode 1 block acknowledgement; Mode 7 question |
| 3 REVIEW | Phase 0 done (prepared early, read-only) — cards await author approval | 2026-11-20 | | `stage3_review/phase0_field_analysis.md` | |
| 4 REVISE | pending | | | | |
| 3' RE-REVIEW | pending | | | | |
| 4' RE-REVISE | pending | | | | |
| 4.5 FINAL INTEGRITY | pending | | | | |
| 5 FINALIZE | pending | | | | |
| 6 PROCESS SUMMARY | pending | | | | |

Round-trip count (document revisions): 0
