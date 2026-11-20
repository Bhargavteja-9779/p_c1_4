# Academic Integrity Verification Report: Phases A, B, D

**Pipeline stage:** ARS Stage 2.5 (pre-review integrity), integrity_verification_agent
**Verification mode:** Initial Verification (Mode 1)
**Scope of this report:** Phase A (reference verification, 100 %), Phase B (citation context, sampled), Phase D (originality, sampled). Phases C and E and the AI Research Failure Mode Checklist are run by a parallel agent and are not covered here.
**Manuscript checked:** `manuscript/build/manuscript_rendered.md` (297 lines; line numbers below refer to this file), bibliography `manuscript/references.json` (51 CSL-JSON entries), `supplementary/Supplementary_Material.md` (ghost-citation check only).
**Target journal:** Sleep Medicine (Elsevier).
**Execution date:** 2026-11-20. All lookups were live; search results and registry metadata can change over time.

---

## Verdict

| Phase | Verdict | Reason |
|---|---|---|
| A: Reference verification | **FAIL** | 51/51 references exist (0 NOT_FOUND, 0 MISMATCH, 0 DOI misdirection, 0 retractions), but 2 MEDIUM bibliographic-accuracy issues (incomplete titles; missing page range) |
| B: Citation context | **FAIL** | 1 SERIOUS misattribution of a theoretical guarantee (L86, Barber et al. 2021, "CV+") |
| D: Originality | **PASS** | 0 CLOSE_MATCH, 0 VERBATIM in 19 sampled paragraphs; D2 self-plagiarism check not executable (author names are placeholders) |
| **Combined (A + B + D)** | **FAIL** | Any SERIOUS or MEDIUM issue blocks under the spec's Verdict Criteria |

Issue counts (this report): **SERIOUS 1, MEDIUM 2, MINOR 12**, plus 4 notes that are not issues.

## Verification Summary

| Category | Total | Passed | Issues |
|----------|-------|--------|--------|
| Reference Existence (A0 + A1) | 51 | 51 | 0 (0 NOT_FOUND, 0 MISMATCH, 0 DOI_MISMATCH) |
| Bibliographic Accuracy (A2) | 51 | 42 | 9 entries: 2 MEDIUM (goldberger2000, bourlard1994), 7 MINOR |
| Retraction / correction check | 47 DOI'd entries (Crossref `update-to`/`updated-by`/`relation`) | 47 | 0 retractions; 1 correction notice (mcgraw1996), recorded as a note |
| Ghost Citations (A3) | -- | -- | 2 orphan (in references.json only; not printed in the rendered list) / 0 dangling |
| Citation Context Accuracy (B1) | 62 of 84 citation instances (73.8 %) | 59 | 3 (1 SERIOUS, 2 MINOR); plus 1 MINOR for uncited attributions met while sampling |
| Citation Format Consistency (B2) | 49 rendered entries | -- | 1 MINOR (aggregate of style inconsistencies) |
| Statistical Data Accuracy (C) | not in scope (parallel agent) | -- | -- |
| Internal Consistency (C2) | not in scope (parallel agent) | -- | -- |
| Originality Check (D1) | 19 of 43 body paragraphs (44.2 %) | 19 | 0 (0 CLOSE_MATCH / 0 VERBATIM) |
| Self-Plagiarism (D2) | not executed | -- | -- (author names are placeholders) |
| Claim Verification (E) | not in scope (parallel agent) | -- | -- |

## Spec steps not run, and why

| Step | Status | Reason |
|---|---|---|
| Cross-Model Verification (optional, v3.0) | `[CROSS-MODEL-SKIPPED]` | `ARS_CROSS_MODEL` is not set in this environment (`env` shows no `ARS_*` variables); no consent gate was reached |
| A0.5 Cache Staleness Advisory | Not applicable | The `verification_gate` cache was not used; every lookup was a live API/web call on 2026-11-20, so no row was served from cache and no `ADV-CACHE-<n>` rows exist |
| A0 via `verification_gate.verify_citation` | Not used | Ran the same S2 batch check directly against the Semantic Scholar Graph API (`POST /graph/v1/paper/batch`), plus Crossref, DataCite and PubMed E-utilities |
| D2 Self-plagiarism | Not executed | The spec's prerequisite ("user provides author name(s)") is not met: the manuscript lists `[AUTHOR NAME(S)]`. Earlier drafts in this repo's git history are unpublished versions of the same manuscript, so text overlap with them is expected and is not self-plagiarism; they were not compared. A title search (Phase D, row D-20) found no public preprint or prior publication of this manuscript |
| Professional plagiarism software (Turnitin/iThenticate) | Not available | WebSearch-based heuristic only (see Tool Limitation Disclaimer) |
| Phases C, E, Failure Mode Checklist | Not in scope | Assigned to the parallel agent |

---

## Phase A: Reference Verification

### Method

1. **A0 (Semantic Scholar batch):** all 45 entries with a Crossref-registered DOI were sent in one S2 batch request (one HTTP 429 at first, then success on retry). Result: 41 `S2_VERIFIED`, 4 `S2_NOT_FOUND` (heremans2024, goldberger2000, vovk2005, bland1986), **0 `DOI_MISMATCH`** (every DOI S2 returned equals the bib DOI). S2 was not queried for the two DataCite dataset DOIs or the four entries without a DOI. No S2 result was `API_UNAVAILABLE`.
2. **Level-1 source for every entry:** Crossref `https://api.crossref.org/works/<DOI>` (45 entries); DataCite `https://api.datacite.org/dois/<DOI>` (2 PhysioNet datasets); primary venue pages for the 4 entries without a DOI (PMLR v119 page; NeurIPS proceedings pages plus `Metadata.json`; Google Patents). A field-by-field comparison script checked title, container, volume, issue, pages/article number, author count, author family names and year against Crossref.
3. **A1 (WebSearch existence check):** run for the 4 `S2_NOT_FOUND` entries and the 4 entries without a DOI, as A0 routing requires. PubMed E-utilities (`esearch` by `[doi]`, then `efetch`) was used as a Level-2 cross-check for 13 entries.
4. **Retractions:** every Crossref record was checked for `update-to`, `updated-by` (this includes Retraction Watch-sourced updates) and `relation`. No retraction or expression of concern was found. One correction notice: mcgraw1996.
5. **Cross-check of similar references (anti-hallucination rule 4):** vangorp2023icassp and vangorp2023jbhi (different DOIs, venues and titles), barber2021 and barber2023, bland1986 and bland1999, kemp2000 and sleepedf_data, alvarez2021 and hmc_data, dankerhopfe2009 and moser2009 (same SIESTA group). Each pair is two distinct, real publications.
6. **The author's `reference_audit.csv`** was treated as a claim. It is a dump of the registry metadata. It did not catch the truncated Goldberger and Bourlard titles, the missing Goldberger pages or the Bakker/Dei Rossi year–volume mismatch, and it describes the patent as "verified against proceedings listing", which cannot apply to a patent.

### Per-reference table

Rendered numbers are the citation-sequence numbers printed by pandoc + `elsevier-vancouver.csl` (reproduced in scratch to view the bibliography; the repo was not modified). "Match" means every compared field equals the Level-1 record.

| # | Key | Rendered | Type | A0 (S2) | Level-1 / Level-2 sources | A1 existence | A2 bibliographic accuracy | Updates / retraction |
|---|---|---|---|---|---|---|---|---|
| 1 | rosenberg2013 | [1] | article | S2_VERIFIED | Crossref; PubMed 23319910 | VERIFIED | Match (2 authors; J Clin Sleep Med 2013;9(1):81–87) | none |
| 2 | dankerhopfe2009 | [2] | article | S2_VERIFIED | Crossref; PubMed 19250176 | VERIFIED | Match (13 authors; J Sleep Res 2009;18(1):74–84). Crossref title has "&amp;"; bib "&" is correct | none |
| 3 | stephansen2018 | [3] | article | S2_VERIFIED | Crossref | VERIFIED | Match (30 authors; Nat Commun 2018;9:5229) | none |
| 4 | perslev2021 | [4] | article | S2_VERIFIED | Crossref | VERIFIED | Match (npj Digit Med 2021;4:72) | none |
| 5 | vallat2021 | [5] | article | S2_VERIFIED | Crossref; Europe PMC PMC8516415 | VERIFIED | Match (eLife 2021;10:e70092) | none (has-preprint relation only) |
| 6 | svensson2024 | [6] | article | S2_VERIFIED | Crossref; PubMed 38382312 | VERIFIED | Match (5 authors; Sleep Med 2024;115:251–263). Third author is recorded as family "NT", given "Hoang" by Crossref and as "Nt H" by PubMed; the rendered "NT H" follows these sources | none (PubMed: "Comment in Sleep Med 2024;117:216", a letter, not a correction) |
| 7 | beau2025 | [7] | article | S2_VERIFIED | Crossref | VERIFIED | Match (Sleep Med 2025;134:106698) | none |
| 8 | kaneda2026 | [8] | article | S2_VERIFIED | Crossref | VERIFIED | Match (SLEEP Adv 2026;7(2):zpag054) | none |
| 9 | baumert2023 | [9] | article | S2_VERIFIED | Crossref | VERIFIED | Match (Sleep Med 2023;107:18–25) | none |
| 10 | deirossi2025 | [10] | article | S2_VERIFIED | Crossref; PubMed 41402410; nature.com page | VERIFIED | Fields match Crossref, but rendered "2025;9:55" does not follow the publisher's own citation "npj Digit. Med. 9, 55 (2026)" (online 2025-12-16, `citation_volume`=9). **MINOR** (IL-MINOR-3) | none |
| 11 | hardarson2023 | [11] | article | S2_VERIFIED | Crossref | VERIFIED | Match (Curr Sleep Med Rep 2023;9(3):140–151) | none |
| 12 | kang2021 | [12] | article | S2_VERIFIED | Crossref | VERIFIED | Match (npj Digit Med 2021;4:142) | none |
| 13 | fiorillo2021 | [13] | article | S2_VERIFIED | Crossref | VERIFIED | Match (IEEE TNSRE 2021;29:2076–2085) | none |
| 14 | phan2022 | [14] | article | S2_VERIFIED | Crossref | VERIFIED | Match (IEEE TBME 2022;69(8):2456–2467) | none |
| 15 | heremans2024 | [15] | article | S2_NOT_FOUND → A1 | Crossref; PubMed 38401452; WebSearch (arXiv 2306.04663 preprint; AMiner record) | VERIFIED | Match (6 authors; Comput Biol Med 2024;171:108205) | none |
| 16 | bechny2024 | [16] | article | S2_VERIFIED | Crossref | VERIFIED | Match (8 authors; Nat Sci Sleep 2024;16:555–572). Crossref volume string is "Volume 16" | none |
| 17 | bakker2023 | [17] | article | S2_VERIFIED | Crossref; PubMed 35780449 | VERIFIED | Fields match Crossref `issued` (2022-07-03, online), but vol 46(2) is the issue published 2023-02-08 (Crossref `published-print`); rendered "Sleep 2022;46:zsac154" pairs the online year with the 2023 issue. **MINOR** (IL-MINOR-2) | none |
| 18 | vangorp2022 | [18] | article | S2_VERIFIED | Crossref; PubMed 35675746; author repository copy of published version | VERIFIED | Match (Sleep 2022;45(8):zsac134) | none |
| 19 | li2025conmil | [19] | article | S2_VERIFIED | Crossref; arXiv 2501.16215 | VERIFIED | Match (11 authors; J Healthc Inform Res 2025;9(4):656–685) | none |
| 20 | mikkelsen2020 | [20] | proc. | S2_VERIFIED | Crossref | VERIFIED | Match (EMBC 2020:645–648) | none |
| 21 | ganglberger2024 | [21] | article | S2_VERIFIED | Crossref | VERIFIED | Match (Sleep 2024;47(11):zsae202) | none |
| 22 | vangorp2023icassp | [22] | proc. | S2_VERIFIED | Crossref | VERIFIED | Match (ICASSP 2023:1–5). Crossref splits the first author as family "Gorp", given "Hans van"; bib "van Gorp" is correct | none |
| 23 | vangorp2023jbhi | [23] | article | S2_VERIFIED | Crossref | VERIFIED | Match (IEEE JBHI 2023;27(11):5599–5609) | none |
| 24 | philips2024patent | [24] | patent | n/a (no DOI) | Google Patents EP4388985A1; WebSearch (Espacenet record, patent PDF) | VERIFIED | Title, number, publication date (2024-06-26) and 5 inventors (order as on Google Patents) match. Applicant (Koninklijke Philips NV) and document type are not rendered; Google Patents gives status "Withdrawn". **MINOR** (IL-MINOR-8) | n/a |
| 25 | vovk2005 | [25] | book | S2_NOT_FOUND → A1 | Crossref (record has no authors); WebSearch (Springer book page 10.1007/b106715; library catalogues) | VERIFIED | Match (Vovk V, Gammerman A, Shafer G; Springer 2005) | none |
| 26 | lei2018 | [26] | article | S2_VERIFIED | Crossref | VERIFIED | Match (JASA 2018;113(523):1094–1111) | none |
| 27 | angelopoulos2023 | [27] | article | S2_VERIFIED | Crossref; arXiv 2107.07511 | VERIFIED | Match (Found Trends Mach Learn 2023;16(4):494–591) | none |
| 28 | tibshirani2019 | [28] | proc. | n/a (no DOI) | NeurIPS proceedings abstract page + `Metadata.json` | VERIFIED | Title, venue, pages 2530–2540, authors ("Ryan J Tibshirani, Rina Foygel Barber, Emmanuel Candes, Aaditya Ramdas") match. Rendered "Tibshirani R" drops the middle initial, and "Foygel Barber R" differs from "Barber RF" in [29] and [41]. **MINOR** (IL-MINOR-6) | n/a |
| 29 | barber2023 | [29] | article | S2_VERIFIED | Crossref | VERIFIED | Match (Ann Stat 2023;51(2):816–845) | none |
| 30 | kemp2000 | [30] | article | S2_VERIFIED | Crossref; PubMed 11008419; PhysioNet "please cite" text | VERIFIED | Match except fifth author "Oberye" (PubMed and PhysioNet: "Oberyé"). **MINOR** (IL-MINOR-5) | none |
| 31 | sleepedf_data | [31] | dataset | n/a (DataCite DOI) | DataCite 10.13026/C2X676; PhysioNet record page | VERIFIED | Title, DOI and year 2018 match DataCite. Creator "Aeilko Zwinderman" is malformed (DataCite itself stores it un-inverted; it is rendered as "Aeilko Zwinderman" among "Kemp B, … Tuk B"). Version (PhysioNet page: "Version 1.0.0, published Oct. 24, 2013", later expanded) and repository are not rendered. **MINOR** (IL-MINOR-4) | n/a |
| 32 | alvarez2021 | [32] | article | S2_VERIFIED | Crossref; PubMed 34398931; Europe PMC PMC8366993 | VERIFIED | Match (PLoS One 2021;16(8):e0256111) | none |
| 33 | hmc_data | [33] | dataset | n/a (DataCite DOI) | DataCite 10.13026/t79q-fr32; PhysioNet record v1.1 | VERIFIED | Match (Alvarez-Estevez D, Rijsman R; 2022; v1.1, published 2022-03-18) | n/a |
| 34 | berry2017 | [34] | article | S2_VERIFIED | Crossref; PubMed 28416048 | VERIFIED | Match (8 authors; J Clin Sleep Med 2017;13(5):665–666) | none |
| 35 | alexandari2020 | [35] | proc. | n/a (no DOI) | PMLR v119 page `alexandari20a` | VERIFIED | Match (Alexandari A, Kundaje A, Shrikumar A; PMLR 119:222–232; 2020) | n/a |
| 36 | bourlard1994 | [36] | book | S2_VERIFIED | Crossref; WebSearch (Springer DOI page; EPFL Infoscience; Springer series vol. 247) | VERIFIED | Authors, year, DOI match; **title omits the subtitle**: the book is *Connectionist Speech Recognition: A Hybrid Approach* (Springer DOI page; Kluwer 1994). **MEDIUM** (IL-MEDIUM-2) | none |
| 37 | rabiner1989 | [37] | article | S2_VERIFIED | Crossref | VERIFIED | Match (Proc IEEE 1989;77(2):257–286) | none |
| 38 | carter1994 | [38] | article | S2_VERIFIED | Crossref | VERIFIED | Match (Biometrika 1994;81(3):541–553) | none |
| 39 | fruhwirth1994 | [39] | article | S2_VERIFIED | Crossref | VERIFIED | Match (J Time Ser Anal 1994;15(2):183–202) | none |
| 40 | chib1996 | [40] | article | S2_VERIFIED | Crossref; author PDF (cs.ubc.ca) | VERIFIED | Match (J Econom 1996;75(1):79–97) | none |
| 41 | barber2021 | [41] | article | S2_VERIFIED | Crossref; arXiv 1905.02928 | VERIFIED | Match (Ann Stat 2021;49(1):486–507) | none |
| 42 | bland1986 | [42] | article | S2_NOT_FOUND → A1 | Crossref; WebSearch (PubMed 2868172; York reprint) | VERIFIED | Match (Lancet 1986;327(8476):307–310, the same issue as "1986;1(8476):307–10"). Crossref's author field is malformed (family "Martin Bland"); the bib "Bland JM" is correct | none |
| 43 | bland1999 | [43] | article | S2_VERIFIED | Crossref; PubMed 10501650 | VERIFIED | Match (Stat Methods Med Res 1999;8(2):135–160) | none |
| 44 | romano2019 | [44] | proc. | n/a (no DOI) | NeurIPS `Metadata.json` (page_first 3543, page_last 3553); mlanthology | VERIFIED | Title, venue and pages match. Rendered "Candès E" should be "Candès EJ" (paper header: "Emmanuel J. Candès"). **MINOR** (IL-MINOR-7) | n/a |
| 45 | moser2009 | [45] | article | S2_VERIFIED | Crossref; PubMed 19238800 | VERIFIED | Match (13 authors; Sleep 2009;32(2):139–149) | none |
| 46 | mcgraw1996 | [46] | article | S2_VERIFIED | Crossref | VERIFIED | Match (Psychol Methods 1996;1(1):30–46) | **Correction**: Crossref `updated-by` → 10.1037/1082-989x.1.4.390 (type "correction"). Note N-1 |
| 47 | gneiting2007 | [47] | article | S2_VERIFIED | Crossref; author PDF | VERIFIED | Match (JASA 2007;102(477):359–378) | none |
| 48 | goldberger2000 | [48] | article | S2_NOT_FOUND → A1 | Crossref (`subtitle` field); PubMed 10851218; WebSearch (PhysioNet suggested citation) | VERIFIED | **Title truncated and pages missing.** Crossref `subtitle`: "Components of a New Research Resource for Complex Physiologic Signals"; PubMed: "Circulation. 2000 Jun 13;101(23):E215-20". Rendered: "PhysioBank, PhysioToolkit, and PhysioNet. Circulation 2000;101." **MEDIUM** (IL-MEDIUM-1) | none |
| 49 | pollard2026 | [49] | article | S2_VERIFIED | Crossref; PhysioNet record pages (current standard PhysioNet citation) | VERIFIED | Match (9 authors; Nature Health 2026;1(8):792–795) | none |
| 50 | rohrscheib2026 | not rendered (orphan) | article | S2_VERIFIED | Crossref | VERIFIED | Match (Sleep Med 2026;141:108828); **never cited** (IL-MINOR-1) | none |
| 51 | vainikka2026 | not rendered (orphan) | article | S2_VERIFIED | Crossref | VERIFIED | Match (IEEE TBME 2026;73(6):2144–2154); **never cited** (IL-MINOR-1) | none |

**Hallucination-pattern screen.** TF: 0 (every entry resolves). PAC: 0 (author lists match the Level-1 record for all 51). IH: the 4 entries without a DOI each have a verified primary record with pages or a patent number. PH/mashup: 0 (all fields of each entry match a single record). SH: no fabricated distortion; the only near-SH findings are the year–volume pairings of bakker2023 and deirossi2025, which follow the online date in Crossref and are not invented. DOI misdirection: 0.

### A3. Ghost citation check

- 49 distinct keys are cited in `manuscript_rendered.md` (84 citation instances). `Supplementary_Material.md` contains **no pandoc citation keys** (its few author-year mentions, e.g. "Barber et al. 2021" at line 126 and "Kemp et al. 2000" at line 10860, all refer to entries present in references.json).
- **Dangling citations:** 0. Every cited key exists in references.json.
- **Orphan entries:** 2: `rohrscheib2026`, `vainikka2026`. Pandoc prints only cited entries, so neither appears in the rendered reference list (49 entries rendered). They are orphans of the bibliography file, not of the printed list (IL-MINOR-1).

---

## Phase B: Citation Context Verification

### Parameters and labels

- Population: 84 citation instances (key × occurrence) in the rendered manuscript. Sample: **62 instances (73.8 %)**, prioritising Introduction gap statements (L40–L46), Methods attributions (L54–L106), the Discussion comparison and limitation citations (L151, L159), and the Ethics/data statements (L185). Repeated identical uses at L151 (the same keys and claims as L40/L44) are covered by the L40/L44 rows.
- Every sampled key has a Phase A verdict of VERIFIED, as the Gray-Zone rule requires.
- **B1 verdict labels** (the spec's B1 severity scale): **ACCURATE** (the source supports the sentence; no issue); **MINOR** (citation correct but could be more precise); **MEDIUM** (citation context deviation); **SERIOUS** (severe misrepresentation). **UNVERIFIABLE_ACCESS** would mark a note where neither abstract nor full text could be read; none was needed in the final sample.
- Evidence basis: abstract (PubMed / S2 / Crossref) unless "full text" is stated.

### B1 sample table

| ID | Line | Claim in manuscript (abridged) | Key(s) | Evidence seen (quoted) | Basis | Verdict |
|---|---|---|---|---|---|---|
| B-01 | 40 | Automatic staging reaches epoch agreement comparable to inter-scorer agreement | rosenberg2013 | "Sleep stage agreement averaged 82.6% … inter-scorer agreement in a large group is approximately 83%" | abstract (PubMed) | ACCURATE |
| B-02 | 40 | (same) | dankerhopfe2009 | "overall agreement was for the AASM standard 82.0% (Cohen's kappa = 0.76) and for the R&K standard 80.6% (Cohen's kappa = 0.68)" | abstract (PubMed) | ACCURATE |
| B-03 | 40 | (same) | stephansen2018 | "The best model performed better than any individual scorer (87% versus consensus)" | abstract (S2) | ACCURATE |
| B-04 | 40 ×2 | (same); open-source tools available to any laboratory | perslev2021 | "performs as accurately as the best of the human experts"; "a publicly available, ready-to-use deep-learning-based system" | abstract (S2) | ACCURATE |
| B-05 | 40 ×2 | (same); open-source tools | vallat2021 | "high sleep-staging accuracy that matches human scoring accuracy and interscorer agreement"; "open source, and free" | abstract (S2) | ACCURATE |
| B-06 | 40 | Validation studies summarise algorithm–scorer agreement for night-level parameters with Bland–Altman bias and LoA | svensson2024 | "Agreement between sleep measures were assessed using Bland-Altman plots" (TST, SOL, WASO, …). Note: a consumer-wearable (Oura ring) validation, not PSG autoscoring | abstract (PubMed) | ACCURATE |
| B-07 | 40 | (same) | beau2025 | "Bland-Altman plots further assessed … total sleep time (TST), sleep efficiency (SE), sleep latency (SL), and wake after sleep onset (WASO)". Note: a wearable (Dreem 3) validation | abstract (S2) | ACCURATE |
| B-08 | 40 | (same) | kaneda2026 | "with limits of agreement for total sleep time of approximately ±0.5 h" (PSG autoscoring) | abstract (S2) | ACCURATE |
| B-09 | 42 | Errors in night-level parameters vary between recordings and populations | baumert2023 | "all systems produced significant errors in clinical markers when considering individual PSG"; accuracy differs by age group | abstract (S2) | ACCURATE |
| B-10 | 42 | (same) | deirossi2025 | Full text: GAMLSS models of "differences … between predicted and (expert-scored) reference hypnogram-derived sleep markers" (TST, WASO, REML, …) with age, gender, AHI, PLMI effects on bias and variability; "Increased AHI and PLMI generally worsen bias and variability" | full text (nature.com) | ACCURATE |
| B-11 | 42 | Modest epoch-level errors can translate into poor estimates of individual parameters | hardarson2023 | "a machine learning model capable of 90% accurate sleep stage classification … may perform worse than a random guess in estimating some sleep parameters" | abstract (S2) | ACCURATE |
| B-12 | 44 | Entropy, MC dropout and confidence networks flag ambiguous epochs for review | kang2021 | "uncertainty information (as quantified using Shannon entropy) … to promote targeted review of uncertain sleep stage classifications on an epoch-by-epoch basis" | abstract (S2) | ACCURATE |
| B-13 | 44 | (same) | fiorillo2021 | "We exploit … the Monte Carlo dropout technique … to also detect the uncertain instances" | abstract (S2) | ACCURATE |
| B-14 | 44 | (same) | phan2022 | uncertainty "based on entropy, can serve as a metric for deferring low-confidence epochs to a human expert" | abstract (S2) | ACCURATE |
| B-15 | 44 | (same) | heremans2024 | "The largest improvement gain is due to the deferral of uncertain epochs to a sleep expert" | abstract (PubMed) | ACCURATE |
| B-16 | 44 | (same) | bechny2024 | "our novel confidence network … examining less than 29.0% of uncertain epochs was required" | abstract (S2) | ACCURATE |
| B-17 | 44 | Hypnodensity graphs display stage probabilities | stephansen2018 | "producing a hypnodensity graph—a probability distribution conveying more information than classical hypnograms" | abstract (S2) | ACCURATE |
| B-18 | 44 | (same) | bakker2023 | "sleep stage probabilities (hypnodensity; i.e. the probability of each sleep stage being assigned to a given epoch)" | abstract (S2) | ACCURATE |
| B-19 | 44 | (same) | vangorp2022 | Full text (27-page repository copy of the published version, "Published: 11/08/2022") contains **no occurrence of "hypnodensity"**; it is a theoretical framework on aleatoric vs epistemic uncertainty. It says it reviews prior work in its online Supplementary Material, which was not accessed | full text (main) | **MINOR** (IL-MINOR-11) |
| B-20 | 44 | Conformal prediction sets have been proposed for single epochs | li2025conmil | "conformal prediction, integrated with MIL to generate calibrated, set-valued outputs"; full text: Sleep-EDF, "30-second epochs"; example prediction set "{N2, REM}" for "sleep stage classification from an EEG" | abstract + full text (arXiv) | ACCURATE |
| B-21 | 44 | Night-level models predict a recording's overall agreement / "scorability" | mikkelsen2020 | "estimate the quality of the automatic sleep scoring … RMSE between estimated and true Cohen's kappa is 0.078" | abstract (S2) | ACCURATE |
| B-22 | 44 | (same) | ganglberger2024 | "A scorability assessment was developed to predict the agreement between the model and human experts … (R²=0.42)" | abstract (S2) | ACCURATE |
| B-23 | 44 | van Gorp et al. sampled complete hypnograms from a generative model for distributions of overnight statistics reflecting inter-rater disagreement | vangorp2023icassp | "estimate this aleatoric uncertainty … by means of posterior sampling … jointly model the sequence of sleep stages … outperforming in terms of uncertainty estimation of the overnight sleep statistics" | abstract (S2) | ACCURATE |
| B-24 | 44 | (same) | vangorp2023jbhi | "conditional generative models based on Normalizing Flows that permits the modeling of the inter-rater disagreement of overnight sleep statistics" | abstract (S2) | ACCURATE |
| B-25 | 44 | A related patent application describes thresholding the spread of such samples to flag uncertain parameters | philips2024patent | Google Patents text: the controller computes an uncertainty estimate across multiple sleep evaluations of a stochastic network and compares it with a threshold; "sigma>tau2 results in 'red light'"; may "repeat the sleep study" or "advise for additional testing" | full text (Google Patents) | ACCURATE |
| B-26 | 46 ×3 | CP gives finite-sample coverage if calibration and test cases are exchangeable | vovk2005; lei2018; angelopoulos2023 | Lei: "guaranteeing finite-sample marginal coverage even when these assumptions do not hold"; Angelopoulos (arXiv abstract): "explicit, non-asymptotic guarantees even without distributional assumptions or model assumptions"; Vovk: Springer listing (conformal prediction monograph) | abstracts | ACCURATE |
| B-27 | 46, 159 | Guarantee depends on exchangeability, may fail across laboratories; weighted conformal methods for shift | tibshirani2019 | "We extend conformal prediction methodology beyond the case of exchangeable data … a weighted version … test and training covariate distributions differ" | NeurIPS Metadata.json abstract | ACCURATE |
| B-28 | 46, 159 | (same) | barber2023 | "exchangeability is often violated when predictive models are deployed in practice … we employ weighted quantiles to introduce robustness against distribution drift" | abstract (S2) | ACCURATE |
| B-29 | 54 | Sleep-EDF Expanded source citation | kemp2000 | PhysioNet: "When using this resource, please cite the original publication: … Kemp … IEEE-BME 47(9):1185-1194 (2000)"; abstract: two nights in 22 subjects, temazepam on one night | PhysioNet page; abstract (PubMed) | ACCURATE |
| B-30 | 54 | 153 SC home recordings, 78 adults 25–101 y; 44 ST in-hospital nights, 22 adults with mild difficulty falling asleep, placebo/temazepam; R&K; ODC-By 1.0 | sleepedf_data | "The 153 SC* files … healthy Caucasians aged 25-101 … at the subjects homes"; "The 44 ST* files … 22 Caucasian males and females … mild difficulty falling asleep … recorded in the hospital during two nights, one of which was after temazepam intake, and the other … after placebo"; R&K 1968 manual; Open Data Commons Attribution v1.0. (The count of 78 subjects is not stated on the page; it follows from the file list) | PhysioNet record | ACCURATE |
| B-31 | 54 ×2 | HMC: 151 clinical PSGs of patients referred for various sleep disorders; CC BY 4.0 | alvarez2021; hmc_data | PhysioNet: 151 recordings of patients "referred for PSG examination in 2018 due to different sleep disorders"; CC BY 4.0. Alvarez 2021 full text: 154 PSGs from the same 2018 population | PhysioNet; full text (Europe PMC) | ACCURATE |
| B-32 | 54 | HMC scored by AASM rules | berry2017 | PhysioNet HMC: scored following the AASM manual "version 2.4"; Berry 2017 = "AASM Scoring Manual Updates for 2017 (Version 2.4)" | PhysioNet; Crossref title | ACCURATE |
| B-33 | 60 | YASA LightGBM trained on several thousand NSRR recordings; C4-M1 recommended | vallat2021 | "3163 unique full-night PSG recordings from seven different datasets … publicly available from the National Sleep Research Resource"; "fitted with a LightGBM classifier"; EEG "preferentially a central derivation such as C4-M1" | full text (PMC8516415) | ACCURATE |
| B-34 | 63 | Bias-corrected temperature scaling | alexandari2020 | §3.1 "No-Bias Vector Scaling and Bias-Corrected Temperature Scaling"; "we observed that Bias-Corrected Temperature Scaling and Vector Scaling work well" | full text (PMLR PDF) | ACCURATE |
| B-35 | 67 | Hybrid classifier/HMM formulation with scaled likelihoods (posterior ÷ prior) | bourlard1994 | Book table of contents §6.4.3 "Prior Class Probabilities and Likelihoods" (EPFL PDF); secondary (ICSI/EPFL reports): network outputs divided by class priors give scaled likelihoods used as HMM emissions. Book text itself not read | TOC + secondary | ACCURATE |
| B-36 | 67 | (same; HMM formulation) | rabiner1989 | Title: "A tutorial on hidden Markov models and selected applications in speech recognition" (cited for the HMM, not for the hybrid step) | Crossref title | ACCURATE |
| B-37 | 75 ×2 | FFBS | carter1994; fruhwirth1994 | Carter–Kohn: draw "the entire state vector in one block" via the Kalman filter; Frühwirth-Schnatter: "proposes a forward-filtering-backward-sampling algorithm" | S2 TLDR + WebSearch summaries of abstracts | ACCURATE |
| B-38 | 75 | FFBS for the finite-state (Markov mixture) case | chib1996 | "the latent variables, one for each observation, can be simulated from their joint distribution given the data and the remaining parameters" | full text (author PDF) | ACCURATE |
| B-39 | 75 | Posterior sampling of whole hypnograms proposed with generative models | vangorp2023jbhi | as B-24 | abstract | ACCURATE |
| B-40 | 86 ×2 | Split conformal: P{θ ∈ C} ≥ 1−α in finite samples under exchangeability with a fixed score | vovk2005; lei2018 | as B-26 | abstracts | ACCURATE |
| B-41 | **86** | "When … calibration scores come from models cross-fitted within the calibration set while test nights use the model fitted on all calibration nights, the guarantee weakens to that of CV+ (≥ 1−2α)" | **barber2021** | Abstract: "the jackknife+ also uses the leave-one-out predictions at the test point … this crucial modification permits rigorous coverage guarantees … **Such guarantees are not possible for the original jackknife and we demonstrate examples where the coverage rate may actually vanish.**" Full text eq. (11): CV+ uses the fold models μ̂₋S_k(i)(X_{n+1}) at the test point; Section 4 summary table: "Jackknife (7) … No guarantee"; Theorem 4: K-fold CV+ ≥ 1 − 2α − min{2(1−1/K)/(n/K+1), (1−K/n)/(K+1)}. The manuscript's construction (CV residuals, test prediction from the refit full model; confirmed by the docstring of `code/experiments/e12_honest_protocol.py`: "test-night summaries use the model fitted on all calibration nights") is the K-fold analogue of the jackknife, not CV+ | abstract + full text (arXiv) | **SERIOUS** (IL-SERIOUS-1) |
| B-42 | 89 | Bland–Altman LoA (computed as a t-based prediction interval) | bland1986 | Bland's York reprint/PubMed: differences against means with limits of agreement. The t·SD·√(1+1/n) form is stated as the authors' own computation | abstract/reprint | ACCURATE |
| B-43 | 89 (and Table 2 caption, L229) | Regression-based LoA "in which bias and mean absolute residual are linear in the automatic value" | bland1999 | Abstract: "a new, more general, regression approach" where "there is a relationship between difference and magnitude". Bland's York page on that method: "Regression of difference on average …"; "regression of these [absolute residuals] on the average glucose". The original regresses on the **average of the two methods**; the manuscript regresses on the automatic (plug-in) value without saying it adapted the method | abstract (PubMed) + author page | **MINOR** (IL-MINOR-10) |
| B-44 | 89 | Constant-width conformal intervals | lei2018 | split conformal framework (abstract); constant-width split conformal with absolute residuals | abstract | ACCURATE |
| B-45 | 89 | CQR | romano2019 | "It combines conformal prediction with classical quantile regression" | NeurIPS Metadata.json abstract | ACCURATE |
| B-46 | 99 | Scoring-rule differences R&K vs AASM | moser2009 | "the time … spent in sleep stage 1 (S1/N1), stage 2 (S2/N2) and slow wave sleep (S3+S4/N3) differed significantly between the R&K and the AASM classification" | abstract (PubMed) | ACCURATE |
| B-47 | 106 | Interval score formula; rewards narrow intervals, penalises misses | gneiting2007 | Eq. (43): "S_α^int(l,u;x) = (u − l) + (2/α)(l − x)1{x < l} + (2/α)(x − u)1{x > u}", "negatively oriented"; "The forecaster is rewarded for narrow prediction intervals, and … incurs a penalty … if the observation misses the interval" | full text (author PDF) | ACCURATE |
| B-48 | 185 | Data distributed through PhysioNet | goldberger2000 | "PhysioNet is an on-line forum for the dissemination and exchange of recorded biomedical signals" | abstract (PubMed) | ACCURATE |
| B-49 | 185 | (same) | pollard2026 | "Twenty-five years after its first public repository was established, the PhysioNet resource …"; PhysioNet record pages list it as the standard PhysioNet citation | abstract (S2) + PhysioNet | ACCURATE |
| B-50 | 185 ×2 | HMC: acquired in routine care, fully anonymised, reuse approved by the Zuid-West Holland IRB (METC-19-065) | alvarez2021; hmc_data | Alvarez 2021: "Data were acquired in the course of common clinical practice … PSGs were anonymized … Study was approved under identification code METC-19-065"; PhysioNet: "Data were fully anonymized …"; "Ethics approval for reuse of this dataset was granted by the Zuid-West Holland institutional review board (METC-19-065)". (The manuscript calls alvarez2021 "the data descriptor"; PhysioNet calls it "the original publication", Note N-2) | full text (Europe PMC) + PhysioNet | ACCURATE |
| B-51 | 159 ×2 | Intervals cover the single scorer's values, including scorer-specific disagreement | rosenberg2013; dankerhopfe2009 | as B-01, B-02 (inter-scorer disagreement documented) | abstracts | ACCURATE |

**Tally (62 instances):** ACCURATE 59; MINOR 2 (B-19, B-43); MEDIUM 0; SERIOUS 1 (B-41).

**Cherry-picking / omission observations (B1).** (i) `vainikka2026` (an epoch-level MC-dropout "Hypnodensity Interval" method; S2 abstract: "enabling targeted manual review of uncertain epochs") sits in the bibliography but is uncited, although it belongs in the L44 list of epoch-level uncertainty methods. The repo's cycle-1 review (`REVIEW/cycle01/agent01_novelty.md`, Mo1) had already asked for it to be cited. This is folded into IL-MINOR-1. (ii) Several issues raised in cycle 1 are now resolved in the current text: the apnoea study `rohrscheib2026` is no longer cited for sleep-parameter LoA; the Hardarson and Baumert attributions (B-09, B-11) are now accurate; Chib 1996 has been added for FFBS; Bland & Altman 1999 has been added.

**Uncited attributions met while sampling (IL-MINOR-12).** These sentences carry no citation where a source is expected: L157 "score a set of local nights manually, **as recommended** for validating any scoring method" (normative claim without a source; the AASM 2020 position statement, Goldstein et al., JCSM 16(4):605–607, asks manufacturers to "aid sleep centers in evaluation of AI-based software performance", but I found no wording that recommends local manual scoring, so a source must be verified or "as recommended" removed); L103 "common clinical decision thresholds (TST < 6 h, SOL > 30 min, WASO > 30 min, REM latency ≤ 15 min)" (no source); L95 "Mondrian (group-conditional) variant" (method named without a citation).

### B2. Citation format consistency

Checked on the bibliography rendered by pandoc 3.1.3 with `manuscript/elsevier-vancouver.csl`, the same command `build_manuscript.py` uses for the DOCX. The style reference was a third-party Sleep Medicine style page: numbered square brackets [1], [1,2], [1–4]; "Nature 2006;444:854–9"; journal abbreviation "Sleep Med".

- **In-text:** numbered, square-bracketed, citation-sequence, ranges with en dash (e.g. "[1–5]", "[4,5]"). Consistent with the journal.
- **"et al." usage:** CSL lists 6 authors, then "et al." Applied consistently.
- **Inconsistencies (aggregated as IL-MINOR-9):**
  1. Journal titles are printed in full, not as NLM abbreviations ("Journal of Clinical Sleep Medicine", not "J Clin Sleep Med"), with capitalisation artefacts: "Npj Digital Medicine" ([4], [10], [12]), "Plos One" ([32]); "The Lancet", "The Annals of Statistics" keep the article; "Foundations and Trends® in Machine Learning" keeps the ® symbol ([27]).
  2. Article titles mix Title Case ([1], [11], [13], [14], [16], [19], [20], [22], [23], [26], [27], [34], [45], [47]) and sentence case (most others).
  3. Author-name forms: "Kemp B, Aeilko Zwinderman, Tuk B, …" ([31]); "Tibshirani R" ([28]; should be RJ); "Foygel Barber R" ([28]) vs "Barber RF" ([29], [41]); "Candès E" ([44]; should be EJ); "Oberye" ([30]) vs "Oberyé" ([31]); non-standard U+2010 hyphen in "Danker‐Hopfe" ([2]) and "Frühwirth‐Schnatter" ([39]).
  4. Conference papers are formatted two ways: "… (EMBC) 2020:645–8." ([20], [22]) vs "… (NeurIPS 2019), 2019, p. 2530–40." ([28], [35], [44]).
  5. Datasets ([31], [33]) carry no "[dataset]" label, repository name or version (the HMC record is v1.1; Sleep-EDF is v1.0.0). The patent ([24]) is printed as "EP4388985A1, 2024." with no applicant or document type. Books ([25], [36]) have no place of publication.
  6. Year–volume pairing: [17] "2022;46" (the issue year is 2023) and [10] "2025;9" (the publisher cites 2026).
  7. Incomplete record: [48] has no issue or pages and a truncated title (IL-MEDIUM-1).

---

## Phase D: Originality Verification Results

### Verification parameters
- Operating mode: Mode 1 (pre-review)
- Total body-text paragraphs: **43** (Introduction 5; Methods 19, counting the short text blocks between equations in §2.4; Results 12; Discussion 6; Conclusion 1). Abstract, highlights, declarations, tables and captions are excluded.
- Paragraphs sampled: **19 (sampling rate 44.2 %)**: Introduction 5/5, Methods 5/19, Results 3/12, Discussion 5/6, Conclusion 1/1. At least one paragraph from every major chapter; Introduction and Discussion prioritised as high-risk.
- Search template: one quoted 8–12-word characteristic fragment per paragraph (WebSearch, standard mode); search engine results reviewed for verbatim or near-verbatim overlap. Where a related idea surfaced, the closest source wording is recorded.
- Author self-plagiarism check: **Not executed** (author information not provided).

### D1 sample table

| ID | Line | Section | Quoted search fragment | Closest match found | Grade |
|---|---|---|---|---|---|
| D-01 | 40 | Intro ¶1 | "Clinicians, however, do not read hypnograms epoch by epoch" | No match; a related idea (experts evaluate hypnogram features, not epochs; PMC9905781) worded differently | ORIGINAL |
| D-02 | 42 | Intro ¶2 | "how far off is the algorithm on average" | No match | ORIGINAL |
| D-03 | 44 | Intro ¶3 | "Uncertainty quantification for automatic staging has mostly addressed single epochs" | No match; topical hits are the cited epoch-level papers (Kang, Phan, Fiorillo, Bechny) | ORIGINAL |
| D-04 | 46 | Intro ¶4 | "Conformal prediction converts any such heuristic spread into intervals" | Angelopoulos & Bates (arXiv 2107.07511): "a method for taking any heuristic notion of uncertainty from any model and converting it to a rigorous one". Same idea, different wording, **cited** at L46 | PARAPHRASE |
| D-05 | 48 | Intro ¶5 | "posterior sampling of complete hypnograms" + HMM + conformal calibration | No match combining these elements (closest: van Gorp ICASSP 2023, cited) | ORIGINAL |
| D-06 | 54 | Methods 2.1 | "153 ambulatory home recordings from 78 healthy adults" | No verbatim match; dataset facts restate the PhysioNet record ("The 153 SC* files … healthy Caucasians aged 25-101 …") in different words, cited | COMMON_KNOWLEDGE |
| D-07 | 75 | Methods 2.4 | "multiplying their outputs along the chain would count the same evidence" | No match | ORIGINAL |
| D-08 | 86 | Methods 2.5 | "If the score function is fixed independently of the calibration" + "in finite samples" | No verbatim match; the standard split-conformal guarantee is stated in many sources in different words, cited | COMMON_KNOWLEDGE |
| D-09 | 89 | Methods 2.6 | "Crossing the centres … separates the effect of the adaptive scale from that of the centre" | No match | ORIGINAL |
| D-10 | 106 | Methods 2.8 | "rewards narrow intervals and penalises misses in proportion to their size" | No verbatim match; Gneiting & Raftery 2007: "The forecaster is rewarded for narrow prediction intervals, and he or she incurs a penalty …", clearly different wording, **cited** | PARAPHRASE |
| D-11 | 118 | Results 3.2 | "the posterior spread alone misstates the error" | No match | ORIGINAL |
| D-12 | 125 | Results 3.3 | "proposed intervals had a lower interval score than every form of limits of agreement" | No match | ORIGINAL |
| D-13 | 138 | Results 3.6 | "one spurious sleep epoch late in a sampled hypnogram" | No textual match; Luna documentation makes a related point ("accepting an outlier sleep epoch as real may lead to excessive estimates of WASO") in different words; the manuscript reports its own result | ORIGINAL |
| D-14 | 151 | Discussion ¶2 | "night-level scorability models predict whether a recording will be scored well" | No match | ORIGINAL |
| D-15 | 153 | Discussion ¶3 | "TST errors accumulate over the whole night from many ambiguous" | No match | ORIGINAL |
| D-16 | 155 | Discussion ¶4 | "per-night uncertainty is only meaningful for parameters that are stable to isolated epoch errors" | No match | ORIGINAL |
| D-17 | 157 | Discussion ¶5 | "A laboratory deploying an automatic stager can" | No match | ORIGINAL |
| D-18 | 159 | Discussion ¶6 | "Coverage is marginal, not conditional" + "hardest nights were under-covered" | No match | ORIGINAL |
| D-19 | 164 | Conclusion | "Conformally calibrated posterior hypnogram samples give per-night intervals" | No match | ORIGINAL |
| D-20 | 2 (title) | (prior-publication check) | "Per-night prediction intervals for automatically scored sleep parameters" | No preprint, publication or online copy of this manuscript found | n/a |

### D1 summary

| Grade | Paragraph Count | Proportion |
|-------|----------------|-----------|
| ORIGINAL | 15 | 78.9 % |
| COMMON_KNOWLEDGE | 2 | 10.5 % |
| PARAPHRASE | 2 | 10.5 % |
| CLOSE_MATCH | 0 | 0 % |
| VERBATIM | 0 | 0 % |

### D2 self-plagiarism check results

| # | Current Paper Paragraph | Existing Publication | Similarity Type | Determination |
|---|---|---|---|---|
| — | — | — | — | Not executed: author names are placeholders (`[AUTHOR NAME(S)]`), so prior publications cannot be identified. Earlier drafts in the git history are unpublished versions of this same manuscript and were not compared, because overlap with them is not self-plagiarism. No public preprint of this manuscript was found (D-20). |

### D3 AI writing characteristic alerts (checklist only, not a determination)

| # | Indicator | Observation |
|---|---|---|
| 1 | Excessive smoothness | Not assessed as triggered; the text is dense and technical, with varied sentence length |
| 2 | Lack of specificity | Not triggered: paragraphs carry specific numbers, cohorts and mechanisms |
| 3 | Formulaic transitions | Not triggered: in 43 body paragraphs, "Furthermore", "Moreover", "Additionally", "Notably", "Importantly" and "It is worth noting" each occur 0 times |
| 4 | Excessive parallelism | Not triggered: the Discussion uses bold run-in headings, which is a journal convention |
| 5 | Hedging overload | Not triggered: "may" 1, "might" 1, "could" 1, "plausibly" 1 |
| 6 | Citation–argument gap | Not triggered: citations are integrated into the argument (see Phase B) |

Indicators triggered: 0 / 6 (below threshold, not flagged). The manuscript discloses generative-AI use (L109, L169).

### Phase D issue list

None (0 CLOSE_MATCH, 0 VERBATIM).

### Tool Limitation Disclaimer

> This originality verification uses WebSearch for heuristic comparison and is not professional plagiarism detection software (such as Turnitin / iThenticate). Coverage is limited to publicly searchable literature, with a sampling rate of 44.2 %, and there is a risk of missed detection. These results serve as preliminary screening; it is recommended to use professional plagiarism detection tools for complete duplicate checking before formal submission.

---

## Issue List (Sorted by Severity)

### SERIOUS (Must Fix)

| ID | # | Category | Location | Issue Description | Correct Information | Source |
|----|---|----------|----------|------------------|--------------------|----|
| IL-SERIOUS-1 | 1 | Citation context (B1): misattributed theoretical guarantee | manuscript_rendered.md **L86** (sentence beginning "When, as in our main design, …"); same claim in `supplementary/Supplementary_Material.md` L125–126 ("Validity guarantee for cross-fitted scores stated as CV+-type (>= 1 - 2 alpha; Barber et al. 2021)"); design described at L93 and in `code/experiments/e12_honest_protocol.py` docstring | The manuscript says that with calibration scores from models cross-fitted within the calibration set **and test nights scored with the model refitted on all calibration nights**, "the guarantee weakens to that of CV+ (≥ 1−2α) [barber2021]". In Barber et al. 2021, CV+ (eq. 11) uses the **K fold models at the test point**, not a refitted full model. The construction described in the manuscript (out-of-fold residuals plus a full-model test prediction) is the K-fold analogue of the jackknife, for which the source states there is **no assumption-free guarantee** ("Such guarantees are not possible for the original jackknife … the coverage rate may actually vanish"; summary table: "Jackknife (7) … No guarantee"). The quoted bound also omits the finite-K term of Theorem 4. The source therefore contradicts the guarantee attributed to it for this design. Mitigation: the sentence goes on to say that empirical coverage is reported, and coverage was met empirically. | Either (a) implement true CV+ (compute each test night's μ̂ and σ̂ under each of the K fold models and form the CV+ interval from the K-fold lower/upper quantiles), then state Theorem 4 exactly: coverage ≥ 1 − 2α − min{2(1−1/K)/(n/K+1), (1−K/n)/(K+1)}; or (b) rewrite, e.g.: "Because test nights use the model refitted on all calibration nights, this construction is the K-fold analogue of the jackknife, which carries no distribution-free guarantee but attains near-nominal coverage when the fitting procedure is stable [barber2021]; validity therefore rests on the empirical coverage reported throughout." Correct the Supplement S1 entry the same way. | Barber et al. 2021, Ann Stat 49:486–507, doi:10.1214/20-AOS1965; arXiv 1905.02928 (abstract; eq. 11; §3.1 Theorem 4; §4 summary table) |

### MEDIUM (Must Fix)

| ID | # | Category | Location | Issue Description | Correct Information | Source |
|----|---|----------|----------|------------------|--------------------|----|
| IL-MEDIUM-1 | 1 | Reference (A2): title imprecision + page-number omission | `goldberger2000` (rendered [48]; cited L185) | Title truncated to "PhysioBank, PhysioToolkit, and PhysioNet"; issue and page range missing (rendered "Circulation 2000;101.") | Goldberger AL, Amaral LAN, Glass L, Hausdorff JM, Ivanov PCh, Mark RG, et al. PhysioBank, PhysioToolkit, and PhysioNet: components of a new research resource for complex physiologic signals. Circulation 2000;101(23):e215–20. doi:10.1161/01.CIR.101.23.e215. In references.json add the subtitle to `title` and `"page": "e215-e220"` | Crossref `subtitle` field; PubMed 10851218 ("Circulation. 2000 Jun 13;101(23):E215-20"); PhysioNet suggested citation |
| IL-MEDIUM-2 | 2 | Reference (A2): title imprecision (subtitle omitted) | `bourlard1994` (rendered [36]; cited L67) | Title given as "Connectionist Speech Recognition"; the book's title is "Connectionist Speech Recognition: A Hybrid Approach". The Crossref record also lacks the subtitle, so this is incomplete metadata, not fabrication | Bourlard HA, Morgan N. Connectionist speech recognition: a hybrid approach. Boston, MA: Kluwer Academic Publishers (Springer); 1994. doi:10.1007/978-1-4615-3210-1 | Springer DOI page (link.springer.com/doi/10.1007/978-1-4615-3210-1); EPFL Infoscience record 192347 |

### MINOR (Recommended Fix at Stage 2.5; Must Fix at Stage 4.5)

| ID | # | Category | Location | Issue Description | Suggestion |
|----|---|----------|----------|------------------|----|
| IL-MINOR-1 | 1 | Ghost citation (A3): orphans | `rohrscheib2026`, `vainikka2026` in references.json | Listed but never cited; not printed (pandoc omits uncited entries). `vainikka2026` is topically relevant (epoch-level MC-dropout "Hypnodensity Interval"), and the cycle-1 review asked for it to be cited | Delete both from references.json, or cite `vainikka2026` in the L44 list of epoch-level uncertainty methods (and at L151). Do not re-cite `rohrscheib2026` for sleep-parameter LoA: it is an AHI/CAI apnoea-scoring study (S2 abstract) |
| IL-MINOR-2 | 2 | Reference (A2): year–volume pairing | `bakker2023` (rendered [17]) | Rendered "Sleep 2022;46:zsac154": the online year (Crossref `issued` 2022-07-03) is paired with vol 46(2), the Feb 2023 issue (Crossref `published-print` 2023-02-08) | Use 2023 (Sleep 2023;46(2):zsac154), e.g. set `issued` to 2023-02 in references.json |
| IL-MINOR-3 | 3 | Reference (A2): year–volume pairing | `deirossi2025` (rendered [10]) | Rendered "2025;9:55"; the publisher's suggested citation is "npj Digit. Med. 9, 55 (2026)" (online 2025-12-16) | Use 2026 for consistency with vol 9 (and consider renaming the key) |
| IL-MINOR-4 | 4 | Reference (A2): malformed creator; missing version | `sleepedf_data` (rendered [31]) | Creator stored as "Aeilko Zwinderman" (copied from malformed DataCite metadata), rendered un-inverted among inverted names; no version or repository; PhysioNet shows "Version 1.0.0, published Oct. 24, 2013" while DataCite gives 2018 | Fix the author to family "Zwinderman", given "Aeilko H"; add version 1.0.0, publisher PhysioNet and a "[dataset]" label; state which year is used (DataCite 2018) |
| IL-MINOR-5 | 5 | Reference (A2): diacritic | `kemp2000` (rendered [30]) | "Oberye" vs "Oberyé" (PubMed 11008419; PhysioNet citation text) | Use "Oberyé JJL" |
| IL-MINOR-6 | 6 | Reference (A2/B2): author initials and name form | `tibshirani2019` (rendered [28]) | "Tibshirani R" should be "Tibshirani RJ" (the given "RJ" is initialised as one name); "Foygel Barber R" is inconsistent with "Barber RF" in [29], [41] for the same author | Encode given names as "Ryan J." and "Rina Foygel" with family "Barber" |
| IL-MINOR-7 | 7 | Reference (A2): initials | `romano2019` (rendered [44]) | "Candès E" should be "Candès EJ" (paper header "Emmanuel J. Candès"; [29], [41] already use "Candès EJ") | Encode given name "Emmanuel J." |
| IL-MINOR-8 | 8 | Reference (A2/B2): patent format | `philips2024patent` (rendered [24]) | Printed as "… stochastic neural network. EP4388985A1, 2024." with no applicant or document type; Google Patents status "Withdrawn" | E.g. "van Gorp H, Fonseca P, van Gilst MM, Overeem S, van Sloun RJG; Koninklijke Philips NV. System for estimating uncertainty of overnight sleep parameters through a stochastic neural network. European patent application EP4388985A1. 2024 Jun 26 (withdrawn)." |
| IL-MINOR-9 | 9 | Citation format consistency (B2) | Rendered reference list (all entries) | Full rather than NLM-abbreviated journal names, with casing artefacts ("Npj", "Plos One", "®", "The …"); mixed Title/sentence case; two conference formats; datasets without label/version; books without place; non-standard U+2010 hyphens (details in B2) | Add `container-title-short` (NLM abbreviations) to the CSL-JSON or use a CSL that abbreviates; normalise titles to sentence case; harmonise conference entries ("In: …"); add dataset/patent fields; replace U+2010 with "-" |
| IL-MINOR-10 | 10 | Citation context (B1): adapted method not flagged as adapted | L89 (b) and Table 2 caption L229 | Bland & Altman (1999) regress differences and absolute residuals on the **average of the two methods**; the manuscript regresses them on the automatic (plug-in) value (the reference is unknown at prediction time) and cites bland1999 as if this were the original method | Write "regression-based limits of agreement adapted from Bland and Altman [bland1999], with the automatic value replacing the pair average as regressor (the reference value is unknown at prediction time)" |
| IL-MINOR-11 | 11 | Citation context (B1): citation placed on a clause it does not support | L44, "hypnodensity graphs display stage probabilities [stephansen2018; bakker2023; vangorp2022]" | The main text of vangorp2022 never mentions hypnodensity (full-text search of the published version); it is a framework paper on aleatoric/epistemic uncertainty. Its online supplement was not accessed | Move vangorp2022 to the opening clause ("Uncertainty quantification for automatic staging has mostly addressed single epochs [vangorp2022]: …"), or keep it here only if its supplement explicitly discusses hypnodensity |
| IL-MINOR-12 | 12 | Citation context (B1): uncited attributions | L157 ("as recommended for validating any scoring method"); L103 (clinical thresholds TST < 6 h, SOL > 30 min, WASO > 30 min, REM latency ≤ 15 min); L95 (Mondrian conformal variant) | Normative or methodological claims without a source | Cite a verified guideline for L157 (e.g. check the AASM position statements: Goldstein et al. 2020, JCSM 16:605–607; Oks et al. 2025, JCSM 21:1953–1955) or delete "as recommended"; cite sources for the thresholds; cite a Mondrian conformal source |

### Notes (not issues; never block)

| ID | Location | Note |
|---|---|---|
| N-1 | `mcgraw1996` | Crossref records a published correction (doi:10.1037/1082-989X.1.4.390, Psychol Methods 1996;1(4):390). Not a retraction. Consider citing the correction as well, since the manuscript uses ICC(A,1) from this paper (L103) |
| N-2 | L185 | alvarez2021 is called "the data descriptor"; it is an original research article that describes the HMC dataset (PhysioNet calls it "the original publication"). The content attributed to it (routine clinical care, anonymisation, METC-19-065) is verified (B-50) |
| N-3 | L40 | Two of the three validation-study examples (svensson2024, beau2025) are consumer-wearable validations rather than PSG autoscoring validations. The sentence is accurate as worded ("algorithm–scorer agreement"); wording such as "device and autoscoring validation studies" would be more precise |
| N-4 | Retractions | No retraction, expression of concern or withdrawal found for any of the 47 DOI'd entries (Crossref `update-to` / `updated-by` / `relation` checked); the patent application's legal status is "Withdrawn", which does not affect its use as prior art |

---

## Verification Audit Trail

**Phase A: registry and API queries (2026-11-20; generic User-Agent, no personal data sent)**
- Crossref: `GET https://api.crossref.org/works/<DOI>` for all 47 entries with a DOI (45 HTTP 200; 2 PhysioNet DOIs returned 404 at Crossref, as expected, because they are DataCite DOIs). Saved responses were compared field by field with references.json (title, container, volume, issue, page/article-number, author count, family names, year), and `subtitle`, `update-to`, `updated-by` and `relation` were inspected.
- DataCite: `GET https://api.datacite.org/dois/10.13026/C2X676` → title "The Sleep-EDF Database [Expanded]", creators [Kemp, Bastiaan; "Aeilko Zwinderman"; Tuk, Bert; Kamphuisen, Hilbert; Oberyé, Josefien], publisher physionet.org, 2018. `GET …/10.13026/t79q-fr32` → "Haaglanden Medisch Centrum sleep staging database", Alvarez-Estevez D, Rijsman R, PhysioNet, 2022, version 1.1, IsVersionOf 10.13026/t4w7-3k21.
- Semantic Scholar: `POST https://api.semanticscholar.org/graph/v1/paper/batch` with 45 `DOI:` ids (fields title, year, venue, authors, externalIds, abstract, journal, tldr, openAccessPdf): 41 found with matching DOI; 4 null (heremans2024, goldberger2000, vovk2005, bland1986).
- PubMed E-utilities: `esearch.fcgi?db=pubmed&term=<DOI>[doi]` then `efetch` (abstract text) for heremans2024 (38401452), rosenberg2013 (23319910), dankerhopfe2009 (19250176), moser2009 (19238800), goldberger2000 (10851218), svensson2024 (38382312), berry2017 (28416048), kemp2000 (11008419), bland1999 (10501650), alvarez2021 (34398931), vangorp2022 (35675746), bakker2023 (35780449), deirossi2025 (41402410); bland1986 returned no hit by DOI (found as PMID 2868172 by WebSearch).
- Entries without a DOI: PMLR `proceedings.mlr.press/v119/alexandari20a.html` (authors, "pp. 222-232", 2020); NeurIPS `…/5103c3584b063c431bd1268e9b5e76fb-Metadata.json` (CQR, page_first 3543, page_last 3553); NeurIPS `…/8fb21ee7a2207526da55a679f0332de2-Metadata.json` and abstract page (covariate shift, 2530–2540; authors "Ryan J Tibshirani, Rina Foygel Barber, Emmanuel Candes, Aaditya Ramdas"); Google Patents `patents.google.com/patent/EP4388985A1/en` (title, assignee Koninklijke Philips NV, 5 inventors, published 2024-06-26, priority 2022-12-23, status Withdrawn).
- A1 WebSearch queries (S2_NOT_FOUND and no-DOI entries): `"Algorithmic Learning in a Random World" Vovk Gammerman Shafer Springer 2005` → link.springer.com/book/10.1007/b106715 (authors and year confirmed); `Bland Altman 1986 Lancet "Statistical methods for assessing agreement …" 327 8476 307-310` → York reprint and PubMed 2868172; `Heremans "U-PASS: …" Computers in Biology and Medicine 2024 171 108205` → arXiv 2306.04663, AMiner; `Goldberger 2000 Circulation "PhysioBank, PhysioToolkit, and PhysioNet: components of …" 101(23) e215` → PhysioNet citation guidance (e215–e220); `EP4388985A1 "uncertainty of overnight sleep parameters" Philips patent` → Espacenet record, patent PDF; `"Conformalized quantile regression" Romano Patterson Candès NeurIPS 2019 proceedings pages` → NeurIPS metadata; `"Conformal prediction under covariate shift" … NeurIPS 2019` → NeurIPS page; `"Connectionist Speech Recognition: A Hybrid Approach" Bourlard Morgan 1994 …` → Springer DOI page, EPFL record (subtitle confirmed).

**Phase B: full texts and pages read**
- arXiv 1905.02928 (Barber et al. 2021) PDF: abstract; §1 ("the original jackknife may even have zero coverage in degenerate examples"); §3 eq. (11) definition of CV+; Theorem 4; §4 summary table.
- arXiv 2501.16215 (ConMIL) PDF; Europe PMC full text PMC8366993 (Alvarez 2021) and PMC8516415 (YASA); nature.com HTML for SLEEPYLAND; PMLR PDF (Alexandari 2020); author PDF of Gneiting & Raftery 2007 (§6.2, eq. 43); author PDF of Chib 1996; hansvangorp.github.io PDF of van Gorp 2022 (published version, 27 pp.; grep for "hypno", "probab", "Stephansen"); PhysioNet pages sleep-edfx/1.0.0 and hmc-sleep-staging/1.1; Bland's York page on regression-based limits (glucose.htm).
- Abstracts: S2 batch and PubMed `efetch`, as listed in the B1 table.

**Phase D: WebSearch queries** (one per sampled paragraph; queries and outcomes listed in the D1 table, rows D-01 to D-20).

**Scratch artefacts** (outside the repo; may be cleared): Crossref/S2/PubMed/DataCite JSON and text files, downloaded PDFs and the pandoc-rendered bibliography are in the session scratchpad (`/tmp/claude-0/-home-user-p-c1-4/9c52bd2c-f480-55be-800e-d02a6653c94b/scratchpad/`).
