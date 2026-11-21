21 November 2026

To the Editor-in-Chief
*Sleep Medicine*

**Submission of an Original Article: "Per-night prediction intervals for automatic sleep scoring: local calibration, review triage and comparison with limits of agreement"**

Dear Editor,

We submit the above manuscript for consideration as an Original Article in *Sleep Medicine*.

Sleep laboratories are adopting automatic stagers, and the validation of these tools is reported, also in this journal, as population-level agreement: Bland–Altman bias and limits of agreement for total sleep time (TST), WASO and stage percentages. These summaries give every night the same error range, however easy or difficult it was to score. A laboratory deploying a stager therefore has three practical questions: can the stager's own probabilities give a night-specific error range, how many locally scored nights are needed to keep that range valid, and which nights should go back for manual review? We answer them with a procedure that samples complete hypnograms from a hidden Markov posterior over the stager's epoch probabilities and calibrates their spread with conformal prediction on a small set of manually scored nights, and we evaluate it against limits of agreement on three open cohorts ({{nights_total}} nights; two stagers) and on two further cohorts with five scorers each (80 nights).

The main findings are:

- Within cohorts, the per-night 90 % intervals reach their nominal marginal coverage relative to a single scorer, whereas regression-based limits of agreement under-cover.
- For TST the intervals have lower interval scores than every variant of limits of agreement in every cohort, although part of this gain is recalibration of the stager's probabilities. At a 6-h threshold, reviewing the {{w_yasa_pooled_TST_norm_reg_ffbs_review*100:.0f}} % of nights whose interval straddles the threshold catches {{w_yasa_pooled_TST_norm_reg_ffbs_caught*100:.0f}} % of the misclassifications of the recalibrated TST, against {{w_yasa_pooled_TST_scp_abs_cal_review*100:.0f}} % of nights with constant-width intervals around the recalibrated value.
- For the other parameters there is no consistent advantage, and wake after sleep onset intervals are worse in the 10-h Sleep-EDF windows; we report these negative results and their mechanism.
- Calibration does not transfer reliably between cohorts, and ten locally scored nights restore average coverage but not at every site, so we recommend at least 20 local nights and periodic monitoring. On the multi-scorer cohorts, intervals calibrated on a consensus covered individual technologists' values far less often than intervals calibrated on one technologist's own scoring, so the reference scoring must be chosen deliberately.

We believe the work fits the scope of *Sleep Medicine*, which covers new diagnostic technologies and their clinical evaluation, and complements recent articles in the journal on the validation and bias of automatic staging. The manuscript ends with a concrete procedure for laboratories (Table 3): calibrate locally, recalibrate the probabilities, report TST with a per-night interval, review the nights the interval cannot decide, and monitor.

The primary method, the initial comparators and the success criteria were fixed in a protocol before any interval was computed, according to the authors' records; the end-to-end evaluation protocol, the additional comparators and the decision thresholds were added after the first results and made our conclusions more conservative. All deviations are documented, and the pre-specified analysis is reported in the supplement. All data are public, and the code regenerates the numbers, tables and figures.

We confirm that this manuscript is original, has not been published previously, and is not under consideration for publication elsewhere. All authors have approved the submission. The study is a secondary analysis of de-identified, openly licensed datasets; the ethics statement in the manuscript describes the approvals documented for the source data. The authors declare no competing interests, and the work received no funding.

Thank you for considering our manuscript.

Yours sincerely,

P. N. Bhargav Teja (corresponding author) and [Second author name]
[Affiliation, address]
[E-mail]
