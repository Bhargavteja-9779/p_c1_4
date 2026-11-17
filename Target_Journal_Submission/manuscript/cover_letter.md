[Date]

To the Editor-in-Chief
*Sleep Medicine*

**Submission of an Original Article: "Per-night prediction intervals for automatically scored sleep parameters: conformal calibration of posterior hypnogram samples compared with limits of agreement"**

Dear Editor,

We submit the above manuscript for consideration as an Original Article in *Sleep Medicine*.

Automatic sleep staging is increasingly used in clinical and research laboratories, and its validation is reported, also in this journal, as population-level agreement—Bland–Altman bias and limits of agreement for total sleep time, sleep efficiency, WASO and stage percentages. These summaries do not tell a clinician how reliable the parameters of the night in front of them are. Our study addresses this gap. We propose a procedure that converts the epoch probabilities of any automatic stager into a per-night interval for each clinical sleep parameter, by sampling complete hypnograms from a hidden Markov posterior and calibrating their spread with conformal prediction on a small set of manually scored nights.

Using a published pretrained stager (YASA) and an in-domain stager on three open cohorts ({{nights_total}} nights; healthy community-dwelling adults, insomnia-complaint/temazepam nights and a clinical sleep-centre cohort), with every component fitted on calibration nights only, we show that:

- the per-night 90 % intervals reach their nominal coverage within cohorts, whereas regression-based limits of agreement under-cover;
- for total sleep time the intervals have lower interval scores than parametric, regression-based and distribution-free limits of agreement in every cohort (significantly so against distribution-free limits), and allow more nights to be classified confidently at a 6-h threshold;
- for the other parameters there is no consistent advantage, and wake after sleep onset intervals are worse in long ambulatory recordings — we report these negative results and their mechanism explicitly;
- neither the intervals nor any limits of agreement transfer between cohorts; ten locally scored nights restore average coverage, but not reliably at every site, which leads us to recommend at least 20 local nights.

We believe the work fits the scope of *Sleep Medicine*, which covers new diagnostic technologies and their clinical evaluation, and complements recent articles in the journal on the validation and age-related bias of automatic staging. The findings translate into practical recommendations for laboratories deploying automatic scoring: calibrate on locally scored nights, report total sleep time with a per-night interval and review nights whose interval straddles a decision threshold.

The primary method, the initial comparators and the success criteria were fixed in a protocol before any interval was computed; the end-to-end evaluation protocol, the additional comparators and the decision thresholds were added after the first results and made our conclusions more conservative. All deviations are documented, and the pre-registered analysis is reported in full in the supplement. All data are public, and the complete code reproduces every number, table and figure.

We confirm that this manuscript is original, has not been published previously, and is not under consideration for publication elsewhere. All authors have approved the submission. The study is a secondary analysis of de-identified, openly licensed datasets; the ethics statement in the manuscript describes the approvals documented for the source data. [AUTHOR ACTION REQUIRED: add your institution's determination.] Generative AI (Claude, Anthropic) was used extensively in literature screening, code development, analysis and drafting; this is disclosed in the manuscript's declaration, and the authors have verified all content and take full responsibility for it. The authors declare no competing interests. [AUTHOR ACTION REQUIRED: confirm all statements in this paragraph.]

Suggested reviewers (optional): [names, affiliations, e-mails, with no conflicts of interest].

Thank you for considering our manuscript.

Yours sincerely,

[Corresponding author name]
[Affiliation, address]
[E-mail, telephone]
