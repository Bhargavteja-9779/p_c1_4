# Selected target journal

| Field | Value | Verification status |
|---|---|---|
| TARGET JOURNAL | **Sleep Medicine** (official journal of the World Sleep Society and the International Pediatric Sleep Association) | Verified – Elsevier journal page (shop.elsevier.com/journals/sleep-medicine/1389-9457) |
| PUBLISHER | Elsevier | Verified |
| ISSN | 1389-9457 | Verified |
| JCR STATUS | Indexed in SCIE (Clarivate) | Secondary (LetPub record lists SCIE); Clarivate JCR requires institutional login – not directly verified |
| JCR QUARTILE | **Q1**, Clinical Neurology, rank 68/296 by JIF (JCI rank 54/296) | **Secondary source only** (LetPub, crowdsourced, data year not stated; the self-citation field is labelled 2025-2026, which suggests the JCR 2026 release). Not verified on Clarivate. |
| JOURNAL IMPACT FACTOR | 4.1 (5-year: 4.5) | Elsevier journal page (year label not displayed; the JCR 2026 release, 2025 data, came out 17 June 2026) |
| JCR SUBJECT CATEGORY | Clinical Neurology | Secondary (LetPub) |
| VERIFIED REVIEW/DECISION TIMELINE | First decision ≈2 days (Elsevier "Insights" page, seen only via search-engine index; ScienceDirect returned HTTP 403 to direct fetches). LetPub reports "average 1.6 months" peer review (secondary). | Partially verified |
| VERIFIED ACCEPTANCE TIMELINE | **Median 91 days** submission→acceptance (IQR 60–128 d) computed by us from PubMed "received"/"accepted" history dates of 400 research articles indexed 2025-07-01…2026-11-15 (`code/scripts/journal_timelines_pubmed.py`, output `pubmed_timelines.json`). An independent agent run found 90 d (2026-only subset, n=294) and the indexed Elsevier Insights figure of 94 d. | **Verified (median of accepted papers)**. About 40% of accepted papers took >100 days, so the ≤100-day target is met *in median only*; no individual-manuscript guarantee is possible. |
| APC | USD 4,130 for gold OA; hybrid journal, so the subscription route has no publication fee | Elsevier APC price list (05-Oct-2026) |
| SCOPE FIT | Scope explicitly includes "new diagnostic and therapeutic technologies" and sleep neurophysiology; the journal regularly publishes automated sleep-staging, wearable-validation and algorithm-evaluation studies (e.g., RimeSleepNet 2025, doi:10.1016/j.sleep.2025.106835; age bias in deep-learning staging 2023, doi:10.1016/j.sleep.2023.04.002) | Verified from journal page and PubMed records |
| RESEARCH FIT | Clinical reliability of automated PSG scoring (night-level sleep parameters with calibrated uncertainty, cross-cohort validation) – clinically oriented methods work | See `../manuscript` and topic selection notes |
| KEY AUTHOR GUIDELINES (Original Article) | ≤5,000 words (excl. abstract, references, tables, figures); structured abstract ≤300 words; sections Introduction / Materials and Methods / Results / Discussion / Conclusion; 3–5 highlights; 1–7 keywords; ≤50 references numbered in square brackets in order of appearance; ≤8 display items (figures + tables combined); figures as separate files, tables as editable text; generative-AI use declaration before references; competing interests; data availability | Official ScienceDirect guide returned HTTP 403; rules taken from the official snippet indexed by the search engine plus two secondary guideline aggregators (scraiber.com, livewrite.app) that cite the official guide. **Re-check the live guide before submission.** |
| KEY REJECTION RISKS | (1) Clinical audience: purely technical ML novelty is insufficient; the clinical value must be explicit. (2) Validation must include external cohorts and agreement statistics (Bland–Altman/ICC) familiar to sleep clinicians. (3) Tight 8-display-item and 50-reference limits. (4) Open datasets (Sleep-EDF, HMC) are well known; the contribution must not be "another staging network". (5) Moderate JIF; editors desk-reject out-of-scope engineering papers. |  |

## Constraint satisfaction summary
* Q1 JCR: satisfied according to a secondary source; primary Clarivate verification **not possible** in this environment.
* JIF: 4.1 – moderate. No journal with a higher JIF that fits the scope had a verified median ≤100 days (see `journal_comparison.md`).
* Submission-to-acceptance ≤100 days: satisfied **in median** (91 days, verified by our own PubMed computation).
* ≤60 days / ≈30 days: **not satisfied** by any reputable candidate examined.
* Not MDPI, not IEEE Access, established society journal of a reputable publisher: satisfied.
