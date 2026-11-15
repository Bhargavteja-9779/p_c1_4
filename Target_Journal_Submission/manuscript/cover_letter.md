[Date]

To the Editor-in-Chief
*Sleep Medicine*

**Submission of an Original Article: "Per-night prediction intervals for automatically scored polysomnography: conformal calibration of posterior hypnogram samples with external validation"**

Dear Editor,

We submit the above manuscript for consideration as an Original Article in *Sleep Medicine*.

Automatic sleep staging is increasingly used in clinical and research laboratories, and its validation is reported, also in this journal, as population-level agreement—Bland–Altman bias and limits of agreement for total sleep time, sleep efficiency, WASO and stage percentages. These summaries do not tell a clinician how reliable the parameters of the night in front of them are. Our study addresses this gap. We propose a procedure that converts the epoch probabilities of any automatic stager into a per-night interval for each clinical sleep parameter, by sampling complete hypnograms from a hidden Markov posterior and calibrating their spread with conformal prediction on a small set of manually scored nights.

Using a published pretrained stager (YASA) and an in-domain stager on three open cohorts ({{nights_total}} nights; healthy community-dwelling adults, insomnia-complaint/temazepam nights and a clinical sleep-centre cohort), we show that:

- the per-night 90 % intervals reach their nominal coverage within cohorts, while parametric limits of agreement under-cover in a small cohort;
- for total sleep time and several stage percentages, the intervals are substantially narrower than constant-width (limits-of-agreement-type) intervals at the same coverage, whereas for REM % and for WASO in long ambulatory recordings they offer no gain — we report these negative results explicitly;
- averaging over posterior hypnograms removes most of the systematic underestimation of total sleep time by the stagers' own hypnograms;
- intervals (and limits of agreement) do not transfer between cohorts, and about ten locally scored nights are sufficient to restore nominal coverage.

We believe the work fits the scope of *Sleep Medicine*, which covers new diagnostic technologies and their clinical evaluation, and complements recent articles in the journal on the validation and age-related bias of automatic staging. The findings translate directly into a recommendation for laboratories deploying automatic scoring: report parameters with locally calibrated intervals and use interval width to prioritise manual review.

The analysis plan, including the primary method, comparators and success criteria, was fixed before any interval was computed; all deviations are documented. All data are public, and the complete code reproduces every number, table and figure.

We confirm that this manuscript is original, has not been published previously, and is not under consideration for publication elsewhere. All authors have approved the submission. The study is a secondary analysis of de-identified, openly licensed datasets, so no ethics approval was required. Generative AI (Claude, Anthropic) was used extensively in literature screening, code development, analysis and drafting; this is disclosed in the manuscript's declaration, and the authors have verified all content and take full responsibility for it. The authors declare no competing interests. [AUTHOR ACTION REQUIRED: confirm all statements in this paragraph.]

Suggested reviewers (optional): [names, affiliations, e-mails, with no conflicts of interest].

Thank you for considering our manuscript.

Yours sincerely,

[Corresponding author name]
[Affiliation, address]
[E-mail, telephone]
