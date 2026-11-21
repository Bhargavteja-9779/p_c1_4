---
title: "Per-night prediction intervals for automatic sleep scoring: local calibration, review triage and comparison with limits of agreement"
---

**Running title:** Per-night intervals for automatic sleep scoring

**Authors:** P. N. Bhargav Teja^a,\*^, [Second author name]^b^

^a^ [Affiliation, address, country]

^b^ [Affiliation, address, country]

^\*^ **Corresponding author:** P. N. Bhargav Teja, [address, e-mail]

**Article type:** Original Article

**Word count:** main text 4,973 words; abstract 289 words

**Highlights**

- Automatic sleep scoring reports no night-specific error range for sleep parameters.
- Per-night 90 % intervals reached nominal marginal coverage within cohorts.
- TST intervals beat limits of agreement; recalibration explains part of the gain.
- Interval-based triage: reviewing 36 % of nights caught 90 % of 6-h TST errors.
- Coverage transferred poorly between sites and depended on whose scoring was used.

**Abstract**

*Objective:* Laboratories adopting automatic scoring usually report population limits of agreement (LoA), which give one error range for all nights. We asked how a laboratory can obtain night-specific error ranges, how many locally scored nights this needs, and which nights to send for manual review.

*Methods:* Recalibrated epoch probabilities were combined with a hidden Markov model; whole hypnograms were sampled by forward-filtering backward-sampling, and the per-night spread of eight parameters, including total sleep time (TST) and wake after sleep onset (WASO), was conformally calibrated on manually scored nights. Two stagers were evaluated against LoA on three public cohorts (348 nights; every label-dependent component fitted on calibration nights only), and we examined transfer between cohorts, calibration on 10–30 local nights, review triage, and two independent cohorts (80 nights) scored by five technologists each.

*Results:* Within cohorts, 90 % intervals covered 90.2–92.5 % (YASA); regression-based LoA covered 86.0 %. For TST, intervals had lower interval scores than every LoA variant (ratio versus distribution-free LoA 0.64–0.86), partly through recalibration (versus recalibrated constant width: 0.86 SC, 0.84 HMC, 1.18 ST); other parameters showed no consistent gain. At TST < 6 h, reviewing the 36 % of nights whose interval straddled the threshold caught 90 % of misclassifications (45 % of nights with recalibrated constant-width intervals). Coverage transferred poorly between cohorts (N3 % coverage 38 %); with ten local nights a site's realised coverage fell below 80 % in 9–17 % of repetitions. In the Dreem cohorts coverage was 91–93 %, but consensus-calibrated intervals covered individual technologists' values in only 73 % of nights.

*Conclusions:* Locally calibrated conformal intervals achieve valid marginal coverage for the scoring used to calibrate them. Their advantage over LoA is clear for TST and absent for most other parameters.

**Keywords:** automatic sleep staging; polysomnography; conformal prediction; uncertainty quantification; sleep parameters; external validation


## 1. Introduction

Automatic sleep staging now reaches epoch-by-epoch agreement with human scorers comparable to the agreement between scorers themselves [@rosenberg2013; @dankerhopfe2009; @stephansen2018; @perslev2021; @vallat2021]. Clinicians, however, do not read hypnograms epoch by epoch: diagnostic and research decisions rest on night-level parameters such as total sleep time (TST), sleep onset latency (SOL), wake after sleep onset (WASO), REM latency and the proportion of each stage. Validation studies therefore summarise algorithm–scorer agreement for these parameters with Bland–Altman bias and limits of agreement across a cohort [@svensson2024; @beau2025; @kaneda2026].

Population limits of agreement give one error range for all nights, although errors in night-level parameters vary between recordings and populations [@baumert2023; @deirossi2025], and modest epoch-level errors can translate into poor estimates of individual parameters [@hardarson2023]. A clinician reviewing an automatically scored study therefore lacks a night-specific range of the form "for this night, TST lies within [a, b] min with 90 % coverage", which would show when a night can be signed off and when it needs manual review.

Uncertainty quantification for automatic staging has mostly addressed single epochs [@vangorp2022]: entropy, Monte-Carlo dropout and confidence networks flag ambiguous epochs for review [@kang2021; @fiorillo2021; @phan2022; @heremans2024; @bechny2024; @vainikka2026], hypnodensity graphs display stage probabilities [@stephansen2018; @bakker2023], conformal prediction sets have been proposed for single epochs [@li2025conmil], and night-level models predict a recording's overall agreement or "scorability" [@mikkelsen2020; @ganglberger2024]. Closest to the present work, van Gorp et al. sampled complete hypnograms from a generative model to obtain distributions of overnight sleep statistics that reflect inter-rater disagreement [@vangorp2023icassp; @vangorp2023jbhi], and a related patent application thresholds the spread of such samples to flag uncertain parameters [@philips2024patent]. This spread is model-based: nothing guarantees that an interval derived from it contains the clinical scorer's value with the stated probability in the laboratory where it is used.

Conformal prediction converts any such heuristic spread into intervals with a finite-sample coverage guarantee, provided that calibration and test cases are exchangeable [@vovk2005; @lei2018; @angelopoulos2023]. Applied with a constant margin it reproduces a distribution-free version of the limits of agreement; scaled by a per-night difficulty measure it can give narrow intervals for easy nights and wide ones for difficult nights. Its guarantee depends on exchangeability, which may fail when an algorithm calibrated in one laboratory is used in another [@tibshirani2019; @barber2023].

A laboratory adopting an automatic stager therefore needs practical answers: can the stager's probabilities give a night-specific error range, how many locally scored nights keep that range valid, and which nights should go back for manual review? We combine posterior sampling of complete hypnograms—implemented post hoc, through a hidden Markov model, for stagers that output epoch probabilities—with conformal calibration on manually scored nights, and test the procedure against limits of agreement within and between three cohorts (348 nights), with few local nights, for review triage at illustrative thresholds, and on two independent cohorts scored by five technologists each.


## 2. Materials and methods

### 2.1. Datasets
We used three openly available polysomnography (PSG) cohorts (Table 1). Sleep-EDF Expanded [@kemp2000; @sleepedf_data] provides 153 ambulatory home recordings from 78 healthy adults aged 25–101 years (SC cohort, mostly two nights per subject) and 44 in-hospital nights from 22 adults with mild difficulty falling asleep, recorded once after placebo and once after temazepam (ST cohort). The Haaglanden Medisch Centrum (HMC) database [@alvarez2021; @hmc_data] contains 151 clinical PSGs of patients referred to a sleep centre for various sleep disorders. SC and ST were scored by Rechtschaffen and Kales rules (stages S3 and S4 merged into N3), HMC by AASM rules [@berry2017]. All data are de-identified and publicly released; this secondary analysis collected no new data.

### 2.2. Analysis windows and night-level parameters
Windows were fixed from recording metadata, not from the reference hypnogram: SC, lights-off to lights-off + 10 h; ST, lights-off to end of recording; HMC, the annotated lights-off and lights-on markers; Dreem, the whole recording (all truncated at the end of the scored part). Within each window we computed eight parameters: total sleep time (TST), sleep onset latency from lights-off (SOL), wake after sleep onset (WASO; wake between sleep onset and the final sleep epoch), REM latency from sleep onset (REML), and the percentages of TST in N1, N2, N3 and REM. Epochs left unscored in the reference were counted as wake in the reference hypnogram, whereas automatic hypnograms used all epochs, so that no reference information enters the automatic parameters. REML was analysed only for nights whose reference contained REM sleep; if an automatic or sampled hypnogram contained none, its REML was right-censored at the window end.

### 2.3. Automatic stagers
The method operates on the epoch-wise stage probabilities of a stager. We studied two. (i) YASA [@vallat2021], an open-source stager trained by its authors on several thousand NSRR recordings, used with its EEG + EOG model and without retraining, so every night is an external test night (SC/ST: Fpz-Cz and horizontal EOG; HMC: C4-M1 and E1-M2; Dreem: C3-M2 and EOG1-EOG2; frontal F4-M1 on HMC as a montage sensitivity analysis). (ii) An in-domain LightGBM model trained on the same 116 YASA features of SC nights (out-of-fold predictions from subject-grouped five-fold cross-validation for SC, a model trained on all SC nights for ST and HMC; three predefined seeds). The stager's own hypnogram (most probable stage per epoch) defines the *plug-in* estimates, i.e. current practice.

### 2.4. Posterior sampling of whole hypnograms
Let $p_t(k)$ be the stager probability of stage $k$ for epoch $t$ of a night with $N$ epochs. Probabilities were first recalibrated by bias-corrected temperature scaling [@alexandari2020],

$$\tilde p_t(k)=\operatorname{softmax}_k\left(\frac{\log p_t(k)}{T}+b_k\right) \qquad (1)$$

fitted by maximum likelihood on labelled source nights; $\pi_s$ denotes the stage distribution of those nights. Following the hybrid classifier/hidden-Markov formulation [@bourlard1994; @rabiner1989], scaled likelihoods

$$e_t(k)=\left[\frac{\tilde p_t(k)}{\pi_s(k)}\right]^{\tau} \qquad (2)$$

serve as emission scores of a first-order Markov chain with transition matrix $A$ and initial distribution $p_0$ estimated from the source hypnograms (add-one smoothing). Given the night's signals, the posterior over complete hypnograms is then

$$P(y_1,\dots,y_N)\propto p_0(y_1)\,e_1(y_1)\prod_{t=2}^{N} A(y_{t-1},y_t)\,e_t(y_t) \qquad (3)$$

Because stagers already use neighbouring epochs as context, the emission temperature $\tau \in [0.02, 1.5]$ down-weights their outputs along the chain; it was fitted on source nights by maximising the smoothed posterior log-likelihood of the reference stages. We drew $M = 1000$ hypnograms per night exactly from (3) by forward-filtering backward-sampling (FFBS) [@carter1994; @fruhwirth1994; @chib1996]: forward probabilities $\alpha_t(k) \propto e_t(k)\sum_j \alpha_{t-1}(j)A(j,k)$, then $y_N \sim \alpha_N$ and, given $y_{t+1}$, $y_t \sim \alpha_t(j)A(j,y_{t+1})$ for $t=N-1,\dots,1$. Every parameter $\theta$ was computed on every sample, giving a per-night posterior mean $\hat\mu$ and standard deviation $\hat\sigma$ (and quantiles). Unlike independent per-epoch sampling, FFBS preserves the temporal correlation of stage errors; posterior sampling of whole hypnograms has been proposed with generative models [@vangorp2023jbhi], and the HMM provides a post-hoc analogue for stagers that output epoch probabilities.

### 2.5. Conformal calibration of per-night intervals
Posterior spreads from (3) are not calibrated: they describe uncertainty given the model, not the stager's systematic errors. We therefore used split conformal prediction [@vovk2005; @lei2018; @angelopoulos2023]. For $n$ labelled calibration nights with reference values $\theta_i$ we computed normalised scores

$$s_i=\frac{|\theta_i-\hat\mu_i|}{\hat\sigma_i+\bar\sigma} \qquad (4)$$

where $\bar\sigma$ is the median of $\hat\sigma$ over the calibration and test nights (a regulariser that stops nights with near-zero posterior spread from dominating; $\hat\sigma$ requires no labels, so computing $\bar\sigma$ over all nights keeps the score a symmetric function of the data). With $\hat q$ the $k$-th smallest score, where $k$ is $(n+1)(1-\alpha)$ rounded up, the interval for a new night is

$$C(x)=\left[\hat\mu-\hat q\,(\hat\sigma+\bar\sigma),\;\hat\mu+\hat q\,(\hat\sigma+\bar\sigma)\right] \qquad (5)$$

intersected with the feasible range (≥ 0 min; 0–100 %). If the score function is fixed independently of the calibration nights and calibration and test nights are exchangeable, $P\{\theta \in C(x)\} \ge 1-\alpha$ in finite samples, whatever the stager or the HMM [@vovk2005; @lei2018]. Our main design departs from this: calibration scores come from models cross-fitted within the calibration set, whereas test nights use the model fitted on all calibration nights, the K-fold analogue of the jackknife of Barber et al. [@barber2021], for which that paper gives no distribution-free guarantee (CV+, which applies the fold models to test nights, guarantees coverage of at least $1-2\alpha$ minus a small term). Validity is therefore an empirical property, and coverage is reported throughout. The method, its score and $\alpha = 0.10$ were fixed in a protocol written before any interval was computed (held in the study repository, not externally registered and not independently datable); later changes are listed in Supplementary S1.

### 2.6. Comparators and ablations
All comparators used the same calibration nights: (a) Bland–Altman limits of agreement around the plug-in [@bland1986], computed as a prediction interval (bias ± $t_{n-1}$·SD·$\sqrt{1+1/n}$); (b) regression-based, heteroscedastic limits after Bland and Altman [@bland1999], with bias and mean absolute residual linear in the automatic value (which replaces the pair mean as regressor because the reference is unknown at prediction time); (c) distribution-free limits of agreement (exact for exchangeable nights): the plug-in plus the conformal $\alpha/2$ and $1-\alpha/2$ quantiles of the signed residual; (d) constant-width conformal intervals [@lei2018] around the raw plug-in, the recalibrated plug-in, or $\hat\mu$; (e) conformalised quantile regression [@romano2019], with linear quantile regression on night-level features or applied to the FFBS percentiles; (f) normalised conformal intervals scaled by mean epoch entropy; (g) FFBS percentile intervals without conformal calibration (Supplementary S1). Crossing the centres in (d) with the FFBS-SD scale separates the effect of the adaptive scale from that of the centre; scale-only ablations kept the centre $\hat\mu$ with other scales or without the regulariser $\bar\sigma$. Comparators (b)–(d), the factorial and the ablations were added after the first results (Supplementary S1).

### 2.7. Evaluation design

*Primary within-cohort analysis (end-to-end protocol).* For each stager and cohort, subjects were split 50 times into calibration and test halves. Every label-dependent component—probability recalibration, $\pi_s$, $A$, $p_0$, $\tau$ and the conformal quantile—was fitted on the calibration subjects only; calibration-night scores came from five-fold cross-fitting within the calibration half and test-night summaries from the model fitted on the whole half, as a laboratory would deploy the method. The pre-specified design (Supplementary S9), with cohort-wide cross-fitting (so that a test night's model could use the labels of other test-half subjects), 500 splits and leave-one-subject-out calibration, was also used for the adaptivity, flagging, subgroup, robustness, sensitivity, error-analysis and emission-temperature results and for Fig. 1; these passages are marked “pre-specified design”. A plain split-conformal sensitivity analysis (calibration subjects halved) is in Supplementary S17.

*Difficult nights.* Coverage was also computed in the quartile of nights with the lowest plug-in epoch accuracy (used only for evaluation), and interval scores were compared above and below the median accuracy.

*Local deployment.* On ST and HMC, $n_t \in \{10, 20, 30\}$ whole-subject nights (50 repetitions) were the only labelled data; all components were fitted on them and the remaining nights tested (coverage, width, probability that a site's realised coverage falls below 80 %, TST bias).

*Transportability.* Intervals calibrated on all SC nights were applied unchanged to ST and HMC, for YASA also with the frontal F4-M1 derivation on HMC to separate montage from population and scoring-rule (R&K versus AASM [@moser2009]) differences.

*Robustness.* Test-night EEG and EOG were corrupted with Gaussian noise (0.5 and 1.0 × the robust SD) or movement-artefact drifts in 10 % or 25 % of epochs; calibration nights stayed clean (YASA; 200 splits of the pre-specified design).

*Independent multi-scorer validation.* We repeated the primary protocol on the Dreem Open Datasets [@guillot2020]: DOD-H (25 healthy volunteers) and DOD-O (55 patients with suspected sleep apnoea), one night each, AASM scoring by five technologists (reference: the consensus hypnogram supplied with the data). YASA was applied unchanged. We also tested intervals calibrated on the consensus against each technologist's own parameter values, calibrated them on one technologist's labels and tested them against every technologist, and applied the SC-calibrated intervals unchanged (Supplementary S18).

*Clinical use and review workload.* For illustrative decision thresholds chosen by the authors (TST < 6 h, SOL > 30 min, WASO > 30 min, REM latency ≤ 15 min; added after the first results and fixed before this analysis was run) we counted the nights whose interval lay entirely on one side of the threshold (“confident decisions”) and their accuracy; undecided nights were taken as the nights to send for manual review, a rule we compared with ranking nights by interval width, by the label-free raw-minus-recalibrated TST difference and at random. We also asked whether interval width identifies nights with clinically relevant plug-in errors (|ΔTST| > 30 min, |ΔREML| > 30 min, |ΔN3 %| > 5 percentage points) and compared point estimates by bias and mean absolute error.

### 2.8. Statistical analysis
Validity was measured by coverage, the fraction of test nights whose interval contained the reference value. Efficiency was measured by the interval score [@gneiting2007], $\mathrm{IS}=(u-l)+\tfrac{2}{\alpha}(l-\theta)\mathbb{1}\{\theta<l\}+\tfrac{2}{\alpha}(\theta-u)\mathbb{1}\{\theta>u\}$ for an interval $[l,u]$, which rewards narrow intervals and penalises misses in proportion to their size (lower is better). Subjects were the unit of analysis. In the primary analysis, each subject's interval scores were averaged over the repetitions in which the subject was tested; the proposed method was compared with each comparator by a two-sided sign-flip permutation test of the mean per-subject difference (20,000 permutations), which tests the reported ratio of mean interval scores, with subject-bootstrap 95 % confidence intervals for the ratio and Holm adjustment across comparators and parameters within each cohort and stager; the tests treat each calibration set as fixed, so p-values are conditional on it. Coverage is reported as the mean over repetitions with the 2.5th–97.5th percentile range. The protocol's success criteria were coverage within ±3 percentage points of nominal and, for adaptivity, a lower interval score than constant-width intervals (Bland–Altman and split-conformal absolute-residual limits; Holm-adjusted p < 0.05) together with a positive width–error Spearman correlation whose 95 % confidence interval excludes zero; both conditions are reported separately and jointly (Section 3.3). Scale comparisons at fixed centres formed a separate Holm family, and the AUROC bootstrap used 1000 instead of 2000 resamples (Supplementary S1).

### 2.9. Software and reproducibility
Analyses used Python 3.13, YASA 0.8.1, LightGBM 4.7, scikit-learn 1.9 and NumPy/Numba on a 4-core CPU without GPU. A pipeline regenerates the results, tables and figures from the public data (large per-night files are regenerated rather than stored), and the numbers in the Results and tables are read from files written by the analysis scripts.


## 3. Results

### 3.1. Cohorts and stagers
The analysis included 348 nights from 251 subjects (362,271 scored epochs; Table 1). Mean per-night Cohen's κ of the external YASA stager was 0.71 (SC), 0.73 (ST) and 0.63 (HMC); the in-domain LightGBM stager reached 0.75 on SC (out-of-fold) but only 0.49 on HMC. The fitted emission temperature was τ ≈ 0.1 (pre-specified design), i.e. strongly down-weighted emissions. Fig. 1 illustrates the procedure on one HMC night.

### 3.2. Validity within cohorts
With every component fitted on the calibration half (Table 2; Supplementary S2), the proposed 90 % intervals covered 90.2–92.5 % of test nights for YASA and 89.0–92.8 % for LightGBM, within the pre-specified ±3 percentage points in 48 of 48 stager–cohort–parameter combinations. In single splits of the smallest cohort (ST; 22 test nights) coverage fell to 68 % (2.5th percentile). Distribution-free limits of agreement covered 87.1–92.8 % (YASA), lowest in ST, where two nights per subject violate the exchangeability these limits assume and 22 calibration nights from 11 subjects leave the extreme quantiles unstable. Bland–Altman limits covered 85.5–94.0 %, and regression-based limits under-covered systematically (mean 86.0 %, minimum 78.5 %). Posterior percentile intervals without conformal calibration covered only 30–84 % for TST, WASO and stage percentages (Supplementary S9).

Coverage was not uniform across nights. In the quartile of nights with the lowest plug-in accuracy it averaged 84.7 % for the proposed intervals (distribution-free limits 82.3 %, Bland–Altman 79.4 %, regression-based 76.3 %) versus 93.4 % in the other quartiles (Supplementary S5). Coverage in age, sex and drug-condition subgroups with ≥20 nights was 87–94 % (pre-specified design; Supplementary S11). A plain split-conformal design with half-sized calibration sets gave coverage of 87.4–93.1 % (within ±3 percentage points in 23 of 24 combinations) and 6 % wider intervals (Supplementary S17).

### 3.3. Efficiency
*Adaptive scale at a fixed centre (comparison added after the first results).* Scaling the width by the posterior standard deviation lowered the mean interval score relative to a constant width around the same posterior-mean centre in 21 of 24 combinations for YASA and 23 for LightGBM (significantly in 15 and 15; never significantly worse; Supplementary S3). Under the protocol's joint criterion (lower interval score with Holm p < 0.05 and a positive width–error correlation) the proposed intervals beat the fixed-centre constant-width intervals in 12 and 10 of 24 combinations and Bland–Altman limits in 5 and 2 (width–error correlations from the pre-specified design, Supplementary S10). The posterior standard deviation was a better scale than mean epoch entropy (proposed lower in 20 and 19 of 24), whereas the pre-specified regulariser $\bar\sigma$ cost efficiency (without it the interval score was lower in 20 and 20 of 24).

*Comparison with limits of agreement.* For TST the proposed intervals had a lower interval score than every form of limits of agreement in every cohort and for both stagers (Fig. 2; Table 2): ratios versus distribution-free limits were 0.64–0.86 (YASA) and 0.65–0.79 (LightGBM; all Holm-adjusted p < 0.05), and versus regression-based limits 0.61–0.89. Recalibration explained none of this gain in SC, about half in HMC and all of it in ST: against a constant width around the recalibrated plug-in the ratio was 0.86 (SC), 0.84 (HMC) and 1.18 (ST; Holm p = 1.00) for YASA, with median TST half-widths of 44 versus 53 min in HMC and 19 versus 19 min in ST. For the other parameters there was no consistent advantage: the proposed intervals had a lower interval score than distribution-free limits in 15 (YASA) and 15 (LightGBM) of 24 combinations (mean ratio excluding TST 1.07 and 0.98) and were significantly worse for WASO in SC (ratios 1.72 and 1.50; Section 3.6).

*Easier and harder nights.* The advantage over distribution-free limits was concentrated in difficult nights (Supplementary S5).

### 3.4. Point estimates
YASA's own hypnograms underestimated TST (bias −21.4, −22.6 and −38.3 min in SC, ST and HMC; Supplementary S4). Recalibrating the epoch probabilities on the calibration nights removed most of this bias (−5.3, −0.2 and −5.2 min) and halved the mean absolute error in HMC (40 to 20 min); with ten local nights the HMC bias was −3.8 min. The posterior mean added little to the recalibrated plug-in for TST and was markedly biased for WASO in SC (+68 versus +25 min). LightGBM results differed in detail (Supplementary S4).

### 3.5. Transport and local deployment
Intervals calibrated on SC did not transfer reliably (Fig. 3a, d; Supplementary S7). On HMC, N3 % coverage fell to 38 % for the proposed intervals and to 55 %, 44 % and 46 % for Bland–Altman, regression-based and distribution-free limits (YASA), because the stager's N3 bias reversed between cohorts (+5.9 percentage points in SC, −4.8 in HMC); for LightGBM, TST coverage on HMC fell to 51 %. A frontal F4-M1 derivation did not repair N3 % coverage (42 % versus 38 % with C4-M1; the bipolar Fpz-Cz of SC and ST could not be tested on HMC), and population, era, equipment, setting and scoring rules (R&K versus AASM) are confounded between the cohorts.

When all components were fitted on a few manually scored nights of the target cohort (Fig. 3b, c, e, f; Supplementary S6), ten nights gave mean coverage over parameters of 92.0 % on HMC and 90.3 % on ST for the proposed intervals (YASA); distribution-free limits need at least 19 calibration nights at α = 0.10. A site's realised coverage fell below 80 % in 9 % (HMC) and 17 % (ST) of repetitions with ten nights and in 7 % and 15 % with 30 (median over parameters). In HMC these risks were close to finite-sample theory for exchangeable data (11, 8 and 6 % predicted for 10, 20 and 30 nights; Supplementary S17); in ST only 14–34 test nights remained, so theory already gives 14–18 %. With ten nights, HMC intervals were 29 % wider than with the full calibration half (Supplementary S6).

### 3.6. Error analysis
Non-covered nights had lower plug-in accuracy (median 0.75 versus 0.81; pre-specified design; Supplementary S12). The WASO failure in SC had a specific mechanism: the 10-h window contains long wake after the final awakening (median 116 min, versus 0.5 min in HMC), and one spurious sleep epoch late in a sampled hypnogram turns this wake into WASO (49 % of samples of an SC night placed the final awakening more than 60 min late, 1 % in HMC; Spearman ρ = 0.79 with the posterior-mean WASO error).

### 3.7. Review workload and clinical decisions
At the threshold TST < 6 h (prevalence 26 % pooled; 61 of 151 HMC nights), the proposed intervals lay entirely on one side of the threshold for 64 % of test nights, and 98.7 % of these decisions agreed with the reference (Fig. 5e–h; YASA, pooled over cohorts; Supplementary S8). The nights an interval leaves undecided are the nights to review: reviewing the 36 % undecided nights caught 90 % of the misclassifications of the recalibrated TST, whereas constant-width intervals around the recalibrated plug-in needed 45 % of nights for 90 %, distribution-free limits 40 % for 90 % and Bland–Altman limits 46 % for 88 % (Fig. 5c; Supplementary S19). The recalibrated plug-in was as accurate on the decided nights (98.7 %) but correct for only 78 % of the undecided ones, whereas classifying every night by its raw plug-in TST was correct for 84.2 % (recalibrated: 91.3 %). Ranking nights by interval width also worked as a triage rule for continuous errors: after reviewing the 20 % widest nights, 51 % of TST errors above 30 min remained (random review: 80 %; Fig. 5a, b). For WASO > 30 min the proposed intervals decided more nights than distribution-free limits (29 % versus 20 %) at lower accuracy (92.7 % versus 95.7 %); a REM latency ≤ 15 min occurred in only 8 of 348 nights, so no interval lay entirely below 15 min. The thresholds are illustrative, not validated cut-offs.

### 3.8. Sensitivity analyses, robustness and flagging
The pre-specified criterion of a positive width–error correlation (95 % CI excluding zero) was met in 30 of 48 stager–cohort–parameter combinations (6 of 6 for TST, 1 of 6 for WASO; Supplementary S10). Coverage was insensitive to the number of posterior samples (at most 1.1 percentage points with M = 100), to using only 25 % of nights for calibration (89.4–93.3 %) and to the stager seed (at most 2.2 percentage points across 3 seeds; pre-specified design; Supplementary S10). Under signal corruption of test nights most methods lost coverage, the adaptive ones less so (movement artefacts in 25 % of epochs: TST coverage 86 % for the proposed intervals versus 70 % for distribution-free and 51 % for Bland–Altman limits; under strong Gaussian noise no method remained valid on average; Fig. 4; Supplementary S13). Interval width flagged nights with large errors better than mean epoch entropy for REM latency in SC, whereas the raw-minus-recalibrated difference was the better flag for TST in HMC (Fig. 5d; Supplementary S14).

### 3.9. Independent validation on two multi-scorer cohorts
On the Dreem Open Datasets (DOD-H and DOD-O pooled; 40 calibration and 40 test nights per split), the proposed 90 % intervals covered 90.8–92.8 % of consensus values, within ±3 percentage points for 8 of 8 parameters. For TST their interval score was 27 % below that of distribution-free limits and 20 % below that of constant-width intervals around the recalibrated TST (mean widths 64, 88 and 76 min). Validity depended on whose scoring was used: intervals calibrated on the consensus covered the values of individual technologists in only 73 % of nights (59 % for TST; worst technologist 70 %), whereas intervals calibrated on one technologist covered that technologist's own values in 91 % and another technologist's in 88 % (80–93 %). The technologists themselves differed in TST by a median SD of 10 min, against an interval half-width of 32 min. Intervals calibrated on SC transferred for some parameters (mean coverage 92 %) but not others (minimum 71 %; 3 of 8 parameters within ±3 percentage points). With ten local DOD-O nights, mean coverage was 92 % and a site's realised coverage fell below 80 % in 8 % of repetitions (5 % with 30 nights; Supplementary S18).


## 4. Discussion

Epoch probabilities of an automatic stager can be turned into per-night intervals for clinical sleep parameters whose marginal coverage, relative to one scorer, reaches its nominal level within a cohort when every component is fitted on the calibration nights alone. Whether they are more informative than limits of agreement depended on the parameter: for TST they had lower interval scores than every form of limits of agreement in every cohort, but much of the gain came from recalibrating the stager's probabilities (against a constant width around the recalibrated plug-in it was modest in SC and HMC and absent in ST), whereas for the other parameters there was no consistent advantage and for WASO in SC they were worse. Every calibration was local: it did not transfer reliably between cohorts and depended on whose scoring was used.

**Relation to previous work.** Epoch-level uncertainty methods [@kang2021; @fiorillo2021; @phan2022; @heremans2024; @bechny2024; @vainikka2026; @li2025conmil] identify epochs to review, and night-level scorability models [@mikkelsen2020; @ganglberger2024] predict whether a recording will be scored well. Posterior sampling of whole hypnograms has been used to describe the uncertainty of overnight statistics, including against several scorers [@vangorp2023icassp; @vangorp2023jbhi], without a coverage guarantee. The present procedure adds a calibrated coverage statement in the units clinicians use, for stagers that output epoch probabilities (here two feature-based stagers sharing YASA's features), and compares it head-to-head with the agreement statistics that validation studies report [@svensson2024; @beau2025; @kaneda2026].

**Why the gain was specific to TST.** At a fixed centre, widths proportional to the posterior spread were more efficient than constant widths in most combinations (significantly in 15 of 24 for YASA), but the protocol's joint criterion was met against Bland–Altman limits in only 5 and 2 of 24 combinations. TST errors accumulate over the whole night from many ambiguous sleep–wake epochs, which is what sampled hypnograms vary; consistent with this, interval width correlated with the plug-in error for TST in 6 of 6 stager–cohort combinations, but for N2 % in only 2 and for WASO in 1 (N1 %, 6 of 6, showed a correlation without consistent gain). Errors in stage percentages are plausibly dominated by systematic differences in how a stager and a scorer draw stage boundaries, which a posterior given the stager's own probabilities cannot see. Latencies depend on single transitions and have skewed error distributions (for SOL, conformalised posterior quantiles beat the symmetric score; Supplementary S3). Regression-based limits were competitive in interval score but did not reach nominal coverage. In SC, the mechanism described in Section 3.6 made the posterior mean over-estimate WASO by 55–68 min and the intervals wide; this is a property of the window and the parameter definition as much as of the method, and the problem was absent in HMC, which ends at lights-on. The pre-specified configuration was not optimal (removing the regulariser lowered the interval score by about 5 %), and we did not tune it on these results.

**Implications for practice.** Table 3 summarises the procedure these results support. A laboratory can score local nights, recalibrate the stager's probabilities (which alone removed most of the TST bias), report TST with a per-night interval and review the nights whose interval straddles a decision threshold (36 % of nights at 6 h; 41 % in HMC) or is widest. A 90 % interval means that the reference value of about 90 % of nights lies inside intervals so constructed, averaged over nights and relative to one scorer; it is not a probability statement about a single night, and it is only as relevant as the scoring used to calibrate it: technologists differed in TST by a median SD of 10 min, and consensus-calibrated intervals under-covered individual technologists. For other parameters, distribution-free limits calibrated on the same local nights were a simpler, on average similarly informative alternative (mean ratio excluding TST 1.07 and 0.98). The site-level risk of low realised coverage followed finite-sample theory (Section 3.5) and falls only slowly with more nights; distribution-free limits need at least 19. We suggest at least 20 locally scored nights and a periodic coverage check on a rolling sample of newly scored nights, because a change of equipment, montage or population would otherwise go unnoticed.

**Limitations.** (i) Coverage is marginal, not conditional: the hardest nights were under-covered (about 85 % in the lowest-accuracy quartile, 84 % for TST in the widest-interval tercile in HMC), although less than with limits of agreement. (ii) Validity requires exchangeability between calibration and test nights; it was not reliably met across cohorts, and weighted conformal methods [@tibshirani2019; @barber2023] are a possible extension. Two nights per subject in Sleep-EDF and small calibration sets also weaken the finite-sample guarantee, and interval-score p-values ignore calibration-set variability and are descriptive. (iii) Each night in the primary cohorts had one scorer, so the intervals cover that scorer's values [@rosenberg2013; @dankerhopfe2009]; the Dreem cohorts show how much this matters. (iv) The primary cohorts were moderate in size (348 nights), adult and scored with two rule sets; both stagers were feature-based and shared the same features; HMC provides no demographics; the simulated artefacts were not matched to real recording failures; deep-learning stagers were not evaluated, although the method needs only epoch probabilities. (v) After an internal review the primary analysis changed from the pre-specified cohort-wide cross-fitting design to the end-to-end protocol, and comparators and decision thresholds were added; the pre-specified analysis (Supplementary S9) led to the same direction of results (the TST advantage over distribution-free limits was significant in 4 of 6 combinations), and all deviations are documented (Supplementary S1).


## 5. Conclusion

Conformally calibrated posterior hypnogram samples give per-night intervals for automatically scored sleep parameters whose coverage, averaged over nights and relative to one scorer, reached its nominal level within cohorts. Their advantage over limits of agreement is parameter-specific: for total sleep time it partly reflects recalibration of the stager (none of the gain in SC, about half in HMC, all in ST) and for most other parameters it is absent. Because coverage did not transfer reliably between cohorts or hold at every site, error statements for automatic scoring should be calibrated on locally scored nights, preferably at least 20, and monitored.


## Declaration of generative AI and AI-assisted technologies in the research and writing process

During the preparation of this work the authors used Claude (Anthropic) in order to search and screen the literature, write and run the analysis code, draft the manuscript text and run simulated peer-review rounds whose reports guided revisions. After using this tool, the authors reviewed and edited the content as needed and take full responsibility for the content of the publication.

## CRediT authorship contribution statement

**P. N. Bhargav Teja:** Conceptualization, Methodology, Software (all code), Validation, Formal analysis, Investigation, Data curation, Writing – original draft, Visualization. **[Second author name]:** Supervision, Writing – review & editing.

## Declaration of competing interest

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

## Funding

This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors.

## Ethics statement

This secondary analysis used only de-identified, openly available PSG recordings distributed through PhysioNet [@goldberger2000; @pollard2026]: Sleep-EDF Expanded (Open Data Commons Attribution Licence v1.0) the HMC Sleep Staging Database (CC BY 4.0) and the Dreem Open Datasets (MIT licence). For the HMC database, the data descriptor and PhysioNet record state that the recordings were acquired in routine clinical care, fully anonymised, and that their reuse was approved by the institutional review board of Zuid-West Holland (METC-19-065) [@alvarez2021; @hmc_data]. The Sleep-EDF Expanded record [@sleepedf_data] does not document the approvals obtained by the original studies [@kemp2000]. The Dreem data descriptor reports approval by the French Committees for the Protection of Persons and written informed consent for DOD-H, and written informed consent at the Stanford Sleep Medicine Center for DOD-O (NCT03657329) [@guillot2020]. No new data were collected and no participants were contacted.

## Data availability

The datasets analysed are publicly available from PhysioNet: Sleep-EDF Expanded [@sleepedf_data] the HMC Sleep Staging Database [@hmc_data] and the Dreem Open Datasets [@guillot2020] (Zenodo, doi:10.5281/zenodo.15900394).

## Code availability

All code needed to regenerate the results, tables and figures (data download with checksum verification, preprocessing, both stagers, posterior sampling, conformal calibration, statistics and figure generation, with unit tests and stepwise scripts) is provided as supplementary material and will be deposited in a public repository with a persistent identifier upon acceptance.

## Acknowledgements

We thank the creators of the Sleep-EDF Expanded and HMC databases and the developers of YASA for making their data and software openly available.


## References

::: {#refs}
:::


## Tables

**Table 1.** Cohorts and epoch-level performance of the two stagers. Accuracy and Cohen's κ are means ± SD over nights; pooled κ over all epochs. LightGBM-SC values for SC are out-of-fold (subject-grouped five-fold cross-validation).

| Characteristic                                    | SC            | ST            | HMC           |
|:--------------------------------------------------|:--------------|:--------------|:--------------|
| Nights                                            | 153           | 44            | 151           |
| Subjects                                          | 78            | 22            | 151           |
| Age, y (mean ± SD)                                | 59.0 ± 22.1   | 40.2 ± 17.9   | not released  |
| Female nights, n                                  | 82            | 30            | not released  |
| Scored epochs                                     | 182852        | 42643         | 136776        |
| W, %                                              | 31.4          | 10.3          | 17.0          |
| N1, %                                             | 10.9          | 8.6           | 11.4          |
| N2, %                                             | 36.7          | 46.6          | 36.6          |
| N3, %                                             | 7.0           | 15.0          | 19.5          |
| REM, %                                            | 14.0          | 19.6          | 15.5          |
| YASA (pretrained, external): accuracy (per night) | 0.794 ± 0.086 | 0.810 ± 0.059 | 0.733 ± 0.105 |
| YASA (pretrained, external): kappa (per night)    | 0.710 ± 0.114 | 0.725 ± 0.089 | 0.632 ± 0.136 |
| YASA (pretrained, external): pooled kappa         | 0.716         | 0.733         | 0.646         |
| LightGBM-SC (in-domain): accuracy (per night)     | 0.820 ± 0.077 | 0.800 ± 0.062 | 0.619 ± 0.106 |
| LightGBM-SC (in-domain): kappa (per night)        | 0.752 ± 0.102 | 0.715 ± 0.093 | 0.491 ± 0.133 |
| LightGBM-SC (in-domain): pooled kappa             | 0.757         | 0.723         | 0.505         |


**Table 2.** Within-cohort validity and efficiency of the proposed 90 % intervals (YASA stager; α = 0.10). Every label-dependent component (probability recalibration, hidden Markov model, emission temperature, conformal quantile) was fitted on the calibration half of 50 subject-grouped 50/50 splits and evaluated on the other half. Coverage: mean over splits (2.5th–97.5th percentile across splits). Width in minutes (TST, SOL, WASO, REML) or percentage points of TST (stage percentages). Interval-score (IS) ratio: proposed/comparator, computed from per-subject mean interval scores, with subject-bootstrap 95 % CI; values < 1 favour the proposed method; * Holm-adjusted p < 0.05 (two-sided sign-flip permutation test of the mean difference; Holm within cohort). Distribution-free LoA: split-conformal limits from signed residuals of the plug-in (exact for exchangeable nights); regression-based LoA: bias and SD modelled as linear functions of the plug-in value; Bland–Altman LoA: t-based prediction interval. In-domain LightGBM stager in Supplementary S4.

| Parameter   | Cohort   | Coverage (2.5–97.5 % over splits)   | Mean width   | IS ratio vs Distribution-free LoA (95% CI)   | IS ratio vs Regression-based LoA (95% CI)   | IS ratio vs Bland–Altman LoA (95% CI)   |
|:-------------------------|:---------------|:------------------------------------|:-------------|:---------------------------------------------|:--------------------------------------------|:----------------------------------------|
| TST (min)   | SC       | 0.907 (0.77–1.00)                   | 90.2         | 0.86 (0.77–0.94)*                            | 0.89 (0.82–0.96)                            | 0.87 (0.80–0.94)*                       |
| TST (min)   | ST       | 0.915 (0.70–1.00)                   | 39.2         | 0.64 (0.56–0.72)*                            | 0.61 (0.54–0.74)*                           | 0.58 (0.52–0.68)*                       |
| TST (min)   | HMC      | 0.913 (0.84–0.98)                   | 91.4         | 0.73 (0.56–0.89)*                            | 0.73 (0.56–0.93)                            | 0.69 (0.52–0.87)*                       |
| SOL (min)   | SC       | 0.905 (0.76–0.98)                   | 27.0         | 0.89 (0.58–1.39)                             | 1.05 (0.75–1.50)                            | 0.88 (0.56–1.35)                        |
| SOL (min)   | ST       | 0.920 (0.74–1.00)                   | 20.5         | 1.99 (1.04–3.74)                             | 1.93 (0.94–3.70)                            | 1.92 (0.93–3.96)                        |
| SOL (min)   | HMC      | 0.920 (0.80–0.99)                   | 22.1         | 1.71 (0.95–3.07)                             | 1.81 (0.98–3.13)                            | 1.37 (0.76–2.36)                        |
| WASO (min)  | SC       | 0.916 (0.83–0.98)                   | 236.9        | 1.72 (1.43–2.19)*                            | 2.25 (1.86–2.71)*                           | 1.41 (1.15–1.84)*                       |
| WASO (min)  | ST       | 0.905 (0.69–1.00)                   | 55.1         | 1.38 (1.03–2.01)                             | 1.41 (1.12–1.78)                            | 1.15 (0.80–1.89)                        |
| WASO (min)  | HMC      | 0.918 (0.84–0.98)                   | 84.9         | 0.88 (0.66–1.14)                             | 1.05 (0.85–1.29)                            | 0.82 (0.61–1.10)                        |
| REML (min)  | SC       | 0.902 (0.81–0.97)                   | 94.3         | 0.68 (0.52–0.84)*                            | 0.74 (0.55–0.96)                            | 0.67 (0.51–0.84)*                       |
| REML (min)  | ST       | 0.925 (0.73–1.00)                   | 165.8        | 0.98 (0.70–1.42)                             | 1.06 (0.72–1.51)                            | 0.94 (0.73–1.15)                        |
| REML (min)  | HMC      | 0.905 (0.78–0.98)                   | 178.3        | 0.92 (0.77–1.07)                             | 0.96 (0.85–1.12)                            | 0.99 (0.87–1.14)                        |
| N1% (pp)    | SC       | 0.914 (0.76–0.99)                   | 27.2         | 0.93 (0.83–1.02)                             | 0.90 (0.84–0.96)                            | 0.92 (0.87–0.98)                        |
| N1% (pp)    | ST       | 0.909 (0.68–1.00)                   | 16.7         | 1.07 (0.76–1.57)                             | 0.95 (0.70–1.31)                            | 1.08 (0.83–1.49)                        |
| N1% (pp)    | HMC      | 0.912 (0.82–0.97)                   | 21.9         | 0.87 (0.75–1.03)                             | 0.91 (0.81–1.02)                            | 0.92 (0.79–1.08)                        |
| N2% (pp)    | SC       | 0.905 (0.75–0.96)                   | 33.3         | 0.77 (0.67–0.89)*                            | 0.94 (0.83–1.03)                            | 0.78 (0.67–0.89)*                       |
| N2% (pp)    | ST       | 0.903 (0.74–1.00)                   | 37.2         | 0.96 (0.87–1.04)                             | 0.98 (0.84–1.13)                            | 1.03 (0.95–1.10)                        |
| N2% (pp)    | HMC      | 0.914 (0.82–0.99)                   | 28.0         | 0.73 (0.61–0.86)*                            | 1.00 (0.85–1.19)                            | 0.75 (0.61–0.92)                        |
| N3% (pp)    | SC       | 0.919 (0.82–0.99)                   | 17.1         | 0.93 (0.81–1.07)                             | 1.02 (0.92–1.14)                            | 0.92 (0.78–1.11)                        |
| N3% (pp)    | ST       | 0.911 (0.69–1.00)                   | 27.6         | 0.89 (0.77–1.02)                             | 0.81 (0.70–0.94)                            | 0.92 (0.80–1.05)                        |
| N3% (pp)    | HMC      | 0.915 (0.82–0.99)                   | 30.0         | 1.05 (0.91–1.20)                             | 1.02 (0.84–1.25)                            | 1.06 (0.89–1.26)                        |
| REM% (pp)   | SC       | 0.915 (0.78–1.00)                   | 25.7         | 1.02 (0.81–1.31)                             | 1.12 (0.89–1.44)                            | 1.01 (0.79–1.33)                        |
| REM% (pp)   | ST       | 0.923 (0.74–1.00)                   | 26.1         | 1.07 (0.97–1.17)                             | 1.12 (0.83–1.64)                            | 1.08 (0.88–1.37)                        |
| REM% (pp)   | HMC      | 0.919 (0.84–0.99)                   | 21.9         | 1.04 (0.90–1.17)                             | 1.23 (1.08–1.40)*                           | 1.05 (0.89–1.21)                        |


**Table 3.** Procedure for a laboratory that adopts an automatic stager, with the supporting evidence from this study (YASA unless stated; pooled or per cohort as indicated; numbers from the primary end-to-end analysis).

| Step | What to do | Evidence from this study |
|:-----------|:----------------------------|:---------------------------------------|
| 1. Calibrate locally | Score at least 20 whole nights from the laboratory's own recordings by hand; fit the probability recalibration, the hidden Markov model and the conformal quantile on them (code supplied). Do not borrow a calibration from another site, montage or scoring rule. | Calibration transferred poorly between cohorts (N3 % coverage 38 % on HMC). With 10 local nights, mean coverage was 90 % (ST) and 92 % (HMC); the site-level risk of coverage below 80 % followed finite-sample theory (11, 8 and 6 % for 10, 20 and 30 nights in HMC); distribution-free limits need at least 19 nights. |
| 2. Recalibrate the probabilities | Read every parameter from the locally recalibrated hypnogram, not from the raw output. | TST error in HMC fell from 40 to 20 min (bias −38 to −5 min). |
| 3. Attach a per-night interval | Report the 90 % interval with TST. For other parameters use distribution-free limits calibrated on the same nights unless the interval is shown to help. | TST intervals had lower interval scores than every limit-of-agreement variant (ratio versus distribution-free limits 0.64–0.86), partly through recalibration; median half-width 44 min. Other parameters: no consistent gain. |
| 4. Send nights to review | Review the nights whose interval straddles the decision threshold, or the widest 20 %. | At 6 h, reviewing 36 % of nights caught 90 % of misclassifications (45 % needed with constant-width intervals around the recalibrated TST). The widest 20 % left 51 % of TST errors above 30 min (random review 80 %). |
| 5. Monitor | Re-score a random sample of nights each quarter (at least 10) and track realised coverage; recalibrate if it falls below 80 % or after a change of equipment, montage, scoring rules or case mix. | Coverage failed silently between cohorts; a site's realised coverage fell below 80 % in 9–17 % of repetitions even after local calibration with 10 nights. |
| 6. Choose the reference scoring | Calibrate on the labels of the scoring you want to reproduce (the technologist or team whose values will be compared), not on a consensus of other scorers. | On Dreem data, intervals calibrated on a five-scorer consensus covered individual technologists' values in only 73 % of nights; calibrated on one technologist, coverage for another was 88 %. Technologists differed in TST by a median SD of 10 min. |

## Figure captions

![**Fig. 1.** The procedure on one HMC night (YASA stager). (a) Calibrated epoch probabilities; (b) manual reference hypnogram; (c) the stager's own hypnogram (plug-in); (d) three hypnograms sampled from the posterior by forward-filtering backward-sampling; (e, f) posterior distributions of TST and REM latency over 1000 samples, with the reference value, the plug-in estimate, the proposed 90 % interval (calibrated leave-one-subject-out on the other HMC nights) and the Bland–Altman limits of agreement.](figures/fig1_example_night.png){width=100%}

![**Fig. 2.** Within-cohort efficiency. Mean interval score of each method relative to distribution-free limits of agreement (LoA; log scale) for each parameter, cohort and stager (50 subject-grouped splits, all components fitted on the calibration half; α = 0.10). Values below 1 indicate better intervals (narrower, or fewer and smaller misses). Proposed method: ratio of per-subject means with subject-bootstrap 95 % CI. Constant (calibrated centre): constant-width conformal interval around the calibrated plug-in; FFBS SD (unreg.): proposed score without the regulariser. Coverage of all methods in Supplementary S2.](figures/fig2_within_cohort_efficiency.png){width=100%}

![**Fig. 3.** Transport and local deployment. (a, d) Coverage on ST (×) and HMC (○) of 90 % intervals calibrated on SC. (b, e) Mean coverage over the eight parameters when every component is fitted only on n manually scored nights of the target cohort and the remaining nights are tested (50 repetitions; shaded: range over parameters for the proposed method on HMC). (c, f) Probability that the realised coverage of the remaining nights falls below 0.80 (median over parameters). Solid: HMC; dashed: ST. Distribution-free LoA are unbounded with fewer than 19 calibration nights (α = 0.10) and are not shown for ten nights.](figures/fig3_transport_local.png){width=100%}

![**Fig. 4.** Robustness to signal corruption (YASA; calibration on clean nights, test on corrupted nights). Coverage (top) and mean width (bottom) for TST, WASO and N3 % under additive Gaussian noise (0.5 and 1.0 × robust SD) and movement-artefact drifts in 10 % or 25 % of epochs.](figures/fig4_robustness.png){width=100%}

![**Fig. 5.** Review workload, flagging and clinical decisions (YASA). (a, b) Triage by ranking nights: share of nights with an absolute error of the recalibrated TST above 30 min that remains after reviewing a given share of nights, ranked by interval width, by the label-free difference between raw and recalibrated TST, at random or by the true error (oracle); all cohorts and HMC. (c) Share of nights that an interval leaves undecided at TST < 6 h (the nights to review) for each method; labels: share of the misclassifications of the recalibrated TST that fall on those nights. (d) AUROC (95 % subject-level bootstrap CI) for detecting nights with a clinically relevant plug-in error (|ΔTST| > 30 min, |ΔREML| > 30 min, |ΔN3 %| > 5 percentage points) from interval width, mean epoch entropy or the raw–calibrated difference (AUROCs based on fewer than 10 events are not shown). (e–h) Decisions at illustrative thresholds (pooled over cohorts): fraction of nights decided and accuracy of these decisions; dotted and dashed lines: accuracy of the raw and the recalibrated automatic value on all nights.](figures/fig5_adaptivity_decisions.png){width=100%}
