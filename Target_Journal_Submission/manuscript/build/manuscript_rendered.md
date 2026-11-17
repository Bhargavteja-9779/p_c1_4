---
title: "Per-night prediction intervals for automatically scored sleep parameters: conformal calibration of posterior hypnogram samples compared with limits of agreement"
---

**Running title:** Per-night intervals for automatic sleep scoring

**Authors:** [AUTHOR NAME(S)]^a^

^a^ [Affiliation, address, country]

**Corresponding author:** [Name, address, e-mail]

**Article type:** Original Article

**Word count:** main text 4,946 words; abstract 297 words

**Highlights**

- Automatic sleep scoring gives no error range for the parameters of a single night.
- Conformally calibrated hypnogram samples gave valid per-night 90 % intervals.
- For total sleep time, intervals were more efficient than limits of agreement.
- Gains were parameter-specific; WASO intervals were worse in long recordings.
- Coverage did not transfer between cohorts; local nights restored it on average.

**Abstract**

*Objective:* Automatic sleep staging is validated with population limits of agreement (LoA), which give no error range for an individual night. We developed per-night prediction intervals for automatically scored sleep parameters and compared them with LoA.

*Methods:* Recalibrated epoch probabilities of a stager were combined with a hidden Markov model; whole hypnograms were sampled by forward-filtering backward-sampling, and the per-night spread of eight parameters, including total sleep time (TST) and wake after sleep onset (WASO), was conformally calibrated on manually scored nights. We evaluated an external pretrained stager (YASA) and an in-domain stager on three public cohorts (348 nights, 251 subjects), fitting every component on calibration nights only (50 subject-grouped splits), against parametric, regression-based and distribution-free LoA, and examined transfer between cohorts, calibration on 10–30 local nights and clinical threshold decisions.

*Results:* Within cohorts, 90 % intervals covered 90.2–92.5 % of reference values (YASA), whereas regression-based LoA under-covered (mean 86.0 %). Scaling width by the posterior spread lowered the interval score relative to a constant width around the same centre in 21 (YASA) and 23 (in-domain) of 24 cohort–parameter combinations, never significantly worse. For TST, intervals had lower interval scores than every LoA variant in all cohorts (ratio versus distribution-free LoA 0.64–0.86); other parameters showed no consistent gain, and WASO intervals were worse in long recordings. Intervals calibrated in one cohort did not transfer (N3 % coverage 38 % in another); with ten local nights mean coverage was 90.3–92.0 %, but a site's realised coverage fell below 80 % in 9–17 % of repetitions. At TST < 6 h, intervals decided 64 % of nights with 98.7 % accuracy (automatic TST alone: 84.2 %).

*Conclusions:* Locally calibrated conformal intervals give valid per-night error ranges for automatically scored sleep parameters. Their advantage over LoA is parameter-specific—clear for TST, absent for most others—and validity requires local calibration.

**Keywords:** automatic sleep staging; polysomnography; conformal prediction; uncertainty quantification; sleep parameters; external validation


## 1. Introduction

Automatic sleep staging now reaches epoch-by-epoch agreement with human scorers comparable to the agreement between scorers themselves [@rosenberg2013; @dankerhopfe2009; @stephansen2018; @perslev2021; @vallat2021], and open-source tools make it available to any laboratory [@vallat2021; @perslev2021]. Clinicians, however, do not read hypnograms epoch by epoch: diagnostic and research decisions rest on night-level parameters such as total sleep time (TST), sleep onset latency (SOL), wake after sleep onset (WASO), REM latency and the proportion of each stage. Validation studies therefore summarise algorithm–scorer agreement for these parameters with Bland–Altman bias and limits of agreement across a cohort [@svensson2024; @beau2025; @kaneda2026].

Population limits of agreement answer the question "how far off is the algorithm on average?", not "how far off might it be tonight?". Errors in night-level parameters vary between recordings and populations [@baumert2023; @deirossi2025], and modest epoch-level errors can translate into poor estimates of individual parameters [@hardarson2023]. A clinician reviewing an automatically scored study therefore lacks a statement of the form "for this night, TST lies within [a, b] min with 90 % confidence", which would show when a night can be signed off and when it needs manual review.

Uncertainty quantification for automatic staging has mostly addressed single epochs: entropy, Monte-Carlo dropout and confidence networks flag ambiguous epochs for review [@kang2021; @fiorillo2021; @phan2022; @heremans2024; @bechny2024], hypnodensity graphs display stage probabilities [@stephansen2018; @bakker2023; @vangorp2022], conformal prediction sets have been proposed for single epochs [@li2025conmil], and night-level models predict a recording's overall agreement or "scorability" [@mikkelsen2020; @ganglberger2024]. Closest to the present work, van Gorp et al. sampled complete hypnograms from a generative model to obtain distributions of overnight sleep statistics that reflect inter-rater disagreement [@vangorp2023icassp; @vangorp2023jbhi], and a related patent application describes thresholding the spread of such samples to flag uncertain parameters [@philips2024patent]. The spread of sampled hypnograms, however, is a model-based quantity: nothing guarantees that an interval derived from it contains the clinical scorer's value with the stated probability, in the laboratory where it is used.

Conformal prediction converts any such heuristic spread into intervals with a finite-sample coverage guarantee, provided that calibration and test cases are exchangeable [@vovk2005; @lei2018; @angelopoulos2023]. Applied with a constant margin it reproduces a distribution-free version of the limits of agreement; scaled by a per-night measure of difficulty it can, in principle, give narrow intervals for easy nights and wide ones for difficult nights. Its guarantee depends on exchangeability, which may fail when an algorithm calibrated in one laboratory is used in another [@tibshirani2019; @barber2023].

Here we combine posterior sampling of complete hypnograms—implemented post hoc for any stager through a hidden Markov model—with conformal calibration on manually scored nights, and evaluate whether the resulting per-night intervals are valid, whether they are more informative than limits of agreement, and what a laboratory must do to keep them valid. Using two stagers and three cohorts (348 nights), we asked: (i) are the intervals valid within a cohort when every component is fitted on the calibration nights only; (ii) are they narrower or better targeted than parametric, regression-based and distribution-free limits of agreement; (iii) which components matter; (iv) does validity transfer across cohorts, and can a few locally scored nights restore it; and (v) do the intervals support clinical decisions at common thresholds.


## 2. Materials and methods

### 2.1. Datasets
We used three openly available polysomnography (PSG) cohorts (Table 1). Sleep-EDF Expanded [@kemp2000; @sleepedf_data] provides 153 ambulatory home recordings from 78 healthy adults aged 25–101 years (SC cohort, mostly two nights per subject) and 44 in-hospital nights from 22 adults with mild difficulty falling asleep, recorded once after placebo and once after temazepam (ST cohort). The Haaglanden Medisch Centrum (HMC) database [@alvarez2021; @hmc_data] contains 151 clinical PSGs of patients referred to a sleep centre for various sleep disorders. SC and ST were scored by Rechtschaffen and Kales rules (stages S3 and S4 merged into N3), HMC by AASM rules [@berry2017]. All data are de-identified and publicly released under open licences (Sleep-EDF: Open Data Commons Attribution v1.0; HMC: CC BY 4.0); this secondary analysis collected no new data.

### 2.2. Analysis windows and night-level parameters
To avoid deriving the analysis window from the reference hypnogram, windows were fixed from recording metadata: SC, lights-off to lights-off + 10 h (the 20-h SC files contain daytime naps); ST, lights-off to end of recording; HMC, the annotated lights-off and lights-on markers (all truncated at the end of the scored part of the file). Within each window we computed eight parameters for a hypnogram *y*: total sleep time (TST), sleep onset latency from lights-off (SOL), wake after sleep onset (WASO), REM latency from sleep onset (REML), and the percentages of TST spent in N1, N2, N3 and REM. Epochs left unscored in the reference (movement, unknown) were counted as wake in the reference hypnogram, whereas automatic hypnograms were evaluated on all epochs, so that no reference information enters the automatic parameters. REML was analysed only for nights whose reference contained REM sleep; if a sampled or automatic hypnogram contained no REM, its REML was right-censored at the window end.

### 2.3. Automatic stagers
The method operates on the epoch-wise stage probabilities of any stager. We studied two. (i) YASA [@vallat2021], a published open-source stager whose LightGBM classifier was trained by its authors on several thousand NSRR recordings; we used its EEG + EOG model without any retraining, so every night in our cohorts is an external test night for this stager (SC/ST: Fpz-Cz and horizontal EOG; HMC: C4-M1 and E1-M2, the montage recommended by its authors; YASA therefore also faces a montage change between cohorts, examined in a sensitivity analysis with frontal F4-M1). (ii) An in-domain LightGBM model trained on the same 116 YASA features of SC nights, with out-of-fold SC predictions from subject-grouped five-fold cross-validation and a model trained on all SC nights for ST and HMC (where it additionally faces a montage change). Hyper-parameters were fixed a priori; three predefined seeds were run. The stager's own hypnogram (most probable stage per epoch) defines the *plug-in* parameter estimates, i.e. current practice.

### 2.4. Posterior sampling of whole hypnograms
Let $p_t(k)$ be the stager probability of stage $k$ for epoch $t$ of a night with $N$ epochs. Probabilities were first recalibrated by bias-corrected temperature scaling [@alexandari2020],

$$\tilde p_t(k)=\operatorname{softmax}_k\left(\frac{\log p_t(k)}{T}+b_k\right) \qquad (1)$$

fitted by maximum likelihood on labelled source nights; $\pi_s$ denotes the stage distribution of those nights. Following the hybrid classifier/hidden-Markov formulation [@bourlard1994; @rabiner1989], scaled likelihoods

$$e_t(k)=\left[\frac{\tilde p_t(k)}{\pi_s(k)}\right]^{\tau} \qquad (2)$$

serve as emission scores of a first-order Markov chain with transition matrix $A$ and initial distribution $p_0$ estimated from the source hypnograms (add-one smoothing). Given the night's signals, the posterior over complete hypnograms is then

$$P(y_1,\dots,y_N)\propto p_0(y_1)\,e_1(y_1)\prod_{t=2}^{N} A(y_{t-1},y_t)\,e_t(y_t) \qquad (3)$$

Because most stagers already use neighbouring epochs as context (YASA uses rolling-window features), multiplying their outputs along the chain would count the same evidence repeatedly; the emission temperature $\tau \in [0.02, 1.5]$ absorbs this and was fitted on source nights by maximising the smoothed posterior log-likelihood of the reference stages. We drew $M = 1000$ hypnograms per night exactly from (3) by forward-filtering backward-sampling (FFBS) [@carter1994; @fruhwirth1994; @chib1996]: forward probabilities $\alpha_t(k) \propto e_t(k)\sum_j \alpha_{t-1}(j)A(j,k)$, then $y_N \sim \alpha_N$ and, given $y_{t+1}$, $y_t \sim \alpha_t(j)A(j,y_{t+1})$ for $t=N-1,\dots,1$. Every parameter $\theta$ was computed on every sample, giving a per-night posterior mean $\hat\mu$ and standard deviation $\hat\sigma$ (and quantiles). Unlike sampling each epoch independently, FFBS preserves the temporal correlation of stage errors; posterior sampling of whole hypnograms to describe overnight-statistic uncertainty has been proposed with generative models [@vangorp2023jbhi], and the HMM provides a post-hoc analogue for any stager.

### 2.5. Conformal calibration of per-night intervals
Posterior spreads from (3) are not calibrated: they describe uncertainty given the model, not the stager's systematic errors. We therefore used split conformal prediction [@vovk2005; @lei2018; @angelopoulos2023]. For $n$ labelled calibration nights with reference values $\theta_i$ we computed normalised scores

$$s_i=\frac{|\theta_i-\hat\mu_i|}{\hat\sigma_i+\bar\sigma} \qquad (4)$$

where $\bar\sigma$ is the median of $\hat\sigma$ over the calibration and test nights (a regulariser that stops nights with near-zero posterior spread from dominating; $\hat\sigma$ requires no labels, so computing $\bar\sigma$ over all nights keeps the score a symmetric function of the data). With $\hat q$ the $k$-th smallest score, where $k$ is $(n+1)(1-\alpha)$ rounded up, the interval for a new night is

$$C(x)=\left[\hat\mu-\hat q\,(\hat\sigma+\bar\sigma),\;\hat\mu+\hat q\,(\hat\sigma+\bar\sigma)\right] \qquad (5)$$

intersected with the feasible range (≥ 0 min; 0–100 %). If the score function is fixed independently of the calibration nights and calibration and test nights are exchangeable, $P\{\theta \in C(x)\} \ge 1-\alpha$ in finite samples, whatever the stager or the HMM [@vovk2005; @lei2018]. When, as in our main design, the calibration scores come from models cross-fitted within the calibration set while test nights use the model fitted on all calibration nights, the guarantee weakens to that of CV+ ($\ge 1-2\alpha$) [@barber2021]; empirical coverage is reported throughout. The method, its score and $\alpha = 0.10$ were fixed in a protocol written before any interval was computed (Supplementary S1).

### 2.6. Comparators and ablations
All comparators used the same calibration nights: (a) Bland–Altman limits of agreement around the plug-in estimate [@bland1986], computed as a prediction interval (bias ± $t_{n-1}$·SD·$\sqrt{1+1/n}$); (b) regression-based, heteroscedastic limits of agreement in which bias and mean absolute residual are linear in the automatic value [@bland1999]; (c) exactly valid distribution-free limits of agreement: the plug-in plus conformal lower and upper quantiles (each at $\alpha/2$) of the signed residual; (d) constant-width conformal intervals [@lei2018] around the raw plug-in, the plug-in of the locally recalibrated probabilities, or $\hat\mu$; (e) conformalised quantile regression (CQR) [@romano2019] with linear quantile regression on night-level features (plug-in and recalibrated plug-in values, $\hat\mu$, $\hat\sigma$, mean epoch entropy and maximum probability) fitted on half of the calibration subjects; (f) CQR applied to the FFBS 5th/95th percentiles; (g) normalised conformal intervals with mean epoch entropy as scale; (h) raw FFBS percentile intervals without conformal calibration. Crossing the centres in (d) with the FFBS-SD scale of (4) separates the effect of the adaptive scale from that of the centre. Scale-only ablations kept the centre $\hat\mu$ and replaced the scale by the SD of independent per-epoch samples or of FFBS samples with $\tau = 1$; a further variant removed the regulariser $\bar\sigma$. Comparators (b)–(d) beyond the pre-specified ones, the factorial and the scale-only ablations were added during review to separate calibration from adaptivity (Supplementary S1).

### 2.7. Evaluation design
*Primary within-cohort analysis (end-to-end protocol).* For each stager and cohort, subjects were split 50 times into calibration and test halves. Every label-dependent component—probability recalibration, $\pi_s$, $A$, $p_0$, $\tau$ and the conformal quantile—was fitted on the calibration subjects only; calibration-night scores came from five-fold cross-fitting within the calibration half, and test-night summaries from the model fitted on the whole calibration half. This mirrors how a laboratory would deploy the method. The pre-registered design, in which HMM components were cross-fitted over the whole cohort (so that a test night's model could use labels of other test-half subjects) and 500 splits plus leave-one-subject-out calibration were drawn, is reported in Supplementary S9; it was used for the adaptivity and flagging analyses, the subgroup and robustness analyses and Fig. 1.
*Difficult nights.* Because marginal coverage can hide under-coverage of hard recordings, coverage was also computed in the quartile of nights with the lowest plug-in epoch accuracy (a label-dependent quantity used only for evaluation), and interval scores were compared separately for nights above and below the median accuracy. An exploratory Mondrian (group-conditional) variant calibrated separately above and below the median mean epoch entropy, a label-free difficulty proxy.
*Local deployment with few nights.* On ST and HMC, $n_t \in \{10, 20, 30\}$ nights (whole subjects; 50 repetitions) were the only labelled data: all components were fitted on them as above and the remaining nights were tested. We report coverage, width, the probability that a site's realised coverage falls below 80 %, and the TST bias of the recalibrated plug-in.
*Transportability.* Intervals calibrated on all SC nights were applied unchanged to ST and HMC; for YASA this was repeated with the frontal F4-M1 derivation on HMC to separate montage from population and scoring-rule (R&K versus AASM [@moser2009]) differences.
*Robustness.* EEG and EOG of test nights were corrupted with additive Gaussian noise (0.5 and 1.0 × the channel's robust SD) or with high-amplitude movement-artefact drifts in 10 % or 25 % of epochs, while calibration nights stayed clean (YASA; 200 splits of the pre-registered design).
*Clinical use.* For common clinical decision thresholds (TST < 6 h, SOL > 30 min, WASO > 30 min, REM latency ≤ 15 min; added during review and fixed before the analysis was run) we counted the nights whose interval lay entirely on one side of the threshold ("confident decisions") and the accuracy of these decisions against the reference. We also asked whether interval width identifies nights with clinically relevant plug-in errors (|ΔTST| > 30 min, |ΔREML| > 30 min, |ΔN3 %| > 5 percentage points), compared with label-free alternatives (mean epoch entropy, mean maximum probability, and the absolute difference between raw and recalibrated plug-in estimates), and compared point estimates by bias and mean absolute error (ICC(A,1) [@mcgraw1996] in Supplementary S9).

### 2.8. Statistical analysis
Validity was measured by coverage, the fraction of test nights whose interval contained the reference value. Efficiency was measured by the interval score [@gneiting2007], $\mathrm{IS}=(u-l)+\tfrac{2}{\alpha}(l-\theta)\mathbb{1}\{\theta<l\}+\tfrac{2}{\alpha}(\theta-u)\mathbb{1}\{\theta>u\}$ for an interval $[l,u]$, which rewards narrow intervals and penalises misses in proportion to their size (lower is better). Subjects were the unit of analysis. In the primary analysis, each subject's interval scores were averaged over the repetitions in which the subject was tested; the proposed method was compared with each comparator by a two-sided sign-flip permutation test of the mean per-subject difference (20,000 permutations), which tests the reported ratio of mean interval scores, with subject-bootstrap 95 % confidence intervals for the ratio and Holm adjustment across comparators and parameters within each cohort and stager. Coverage is reported as the mean over repetitions with the 2.5th–97.5th percentile range. AUROC confidence intervals used 1000 subject-level cluster-bootstrap resamples. Pre-specified success criteria were: coverage within ±3 percentage points of nominal; a lower interval score than constant-width intervals (Holm-adjusted p < 0.05); and a positive width–error Spearman correlation whose 95 % confidence interval excludes zero.

### 2.9. Software, reproducibility and use of AI
Analyses used Python 3.13, YASA 0.8.1, LightGBM 4.7, scikit-learn 1.9 and NumPy/Numba on a 4-core CPU without GPU. A single script regenerates every result, table and figure from the public data, and all numbers in this article are read from machine-generated files. A generative AI system (Claude, Anthropic) was used to search the literature, write and run the analysis code and draft the manuscript; all analyses are reproducible from the released code, and the authors verified the content (see Declaration).


## 3. Results

### 3.1. Cohorts and stagers
The analysis included 348 nights from 251 subjects (362,271 scored epochs; Table 1). Mean per-night Cohen's κ of the external YASA stager was 0.71 (SC), 0.73 (ST) and 0.63 (HMC); the in-domain LightGBM stager reached 0.75 on SC (out-of-fold) but only 0.49 on HMC. The fitted emission temperature was τ ≈ 0.1, i.e. both stagers' outputs were strongly down-weighted along the chain. Fig. 1 illustrates the procedure on one HMC night.

### 3.2. Validity within cohorts
With every component fitted on the calibration half (Table 2; Supplementary S2), the proposed 90 % intervals covered 90.2–92.5 % of test nights for YASA and 89.0–92.8 % for LightGBM, within the pre-specified ±3 percentage points in 48 of 48 stager–cohort–parameter combinations. The coverage realised in a single split varied considerably in the smallest cohort (2.5th percentile across splits down to 68 % in ST, where each test half had 22 nights). Distribution-free limits of agreement covered 87.1–92.8 % (YASA), with the lowest values in the small ST cohort, where 22 calibration nights from 11 subjects make the extreme residual quantiles these limits rely on unstable. Parametric Bland–Altman limits covered 85.5–94.0 %, and regression-based limits under-covered systematically (mean 86.0 %, minimum 78.5 % for YASA; 86.0 % and 74.5 % for LightGBM). Posterior percentile intervals without conformal calibration covered only 30–84 % for TST, WASO and stage percentages (Supplementary S9): the posterior spread alone misstates the error of night-level parameters.

Coverage was not uniform across nights. In the quartile of nights with the lowest plug-in accuracy it averaged 84.7 % for the proposed intervals (range over cohorts, parameters and stagers 72–99 %), versus 82.3 % for distribution-free, 79.4 % for Bland–Altman and 76.3 % for regression-based limits; in the other three quartiles it was 93.4 % (Supplementary S5). Calibration stratified by mean epoch entropy (exploratory) raised worst-quartile coverage in 5 of 6 cohort–stager combinations (Supplementary S5); coverage in age, sex and drug-condition subgroups with ≥20 nights was 87–94 % (pre-registered design; Supplementary S11).

### 3.3. Efficiency
*Adaptive scale at a fixed centre (pre-specified criterion).* Scaling the width by the posterior standard deviation lowered the mean interval score relative to a constant width around the same posterior-mean centre in 21 of 24 combinations for YASA and 23 for LightGBM (mean ratio 0.92 and 0.92), significantly in 15 and 15, and was never significantly worse; with the calibrated plug-in as centre the corresponding counts were 21 and 21 (significant: 12 and 9; Supplementary S3). The posterior standard deviation was a better scale than mean epoch entropy (proposed lower in 20 and 19 of 24), whereas the pre-specified regulariser $\bar\sigma$ cost efficiency: without it the interval score was lower in 20 and 20 of 24 combinations (mean ratio of the pre-specified to the unregularised score 1.05 and 1.05).

*Comparison with limits of agreement.* For TST the proposed intervals had a lower interval score than every form of limits of agreement in every cohort and for both stagers (Fig. 2; Table 2): interval-score ratios versus distribution-free limits were 0.64–0.86 (YASA) and 0.65–0.79 (LightGBM; all Holm-adjusted p < 0.05), and versus regression-based limits 0.61–0.89 (significant in 3 of 6 stager–cohort combinations; versus Bland–Altman limits in 5 of 6). For the other parameters there was no consistent advantage. Across all 24 combinations the proposed intervals had a lower interval score than distribution-free limits in 15 (YASA) and 15 (LightGBM), significantly so for N2 % (HMC, SC), TST (HMC, SC, ST) and REML (SC) (YASA); excluding TST, the mean ratio was 1.07 and 0.98. The proposed intervals were significantly worse for WASO in SC (ratio 1.72 for YASA and 1.50 for LightGBM; Section 3.6). Regression-based limits achieved lower interval scores than the proposed intervals for most parameters other than TST (mean ratio excluding TST 1.16 and 1.07), but with the under-coverage reported above.

*Easier and harder nights.* The advantage was concentrated in difficult nights. On nights below the median plug-in accuracy of their cohort, the interval score of the proposed method was lower than that of distribution-free limits in 17 (YASA) and 19 (LightGBM) of 24 combinations (mean ratio 0.93 and 0.88); on easier nights it was lower in 10 and 14 (mean ratio 1.14 and 1.03; Supplementary S5).

### 3.4. Point estimates
The stagers' own hypnograms underestimated TST (YASA bias −21.4, −22.6 and −38.3 min in SC, ST and HMC; Table 3). Recalibrating the epoch probabilities on the calibration nights removed most of this bias (−5.3, −0.2 and −5.2 min) and halved the mean absolute error in HMC (40 to 20 min); with only ten local nights the HMC bias was −3.8 min (MAE 21 min). The posterior mean added little to the calibrated plug-in for TST (MAE 19 min in HMC) and was markedly biased for WASO in SC (+68 min versus +25 min for the calibrated plug-in). LightGBM results were similar (Supplementary S4).

### 3.5. Transport and local deployment
Intervals calibrated on SC did not transfer reliably (Fig. 3a, d; Supplementary S7). On HMC, coverage for N3 % fell to 38 % for the proposed intervals and to 55 %, 44 % and 46 % for Bland–Altman, regression-based and distribution-free limits (YASA), because the stager's N3 bias reversed between cohorts (+5.9 percentage points in SC, −4.8 in HMC); for LightGBM, TST coverage on HMC fell to 51 %. With the frontal F4-M1 derivation on HMC the YASA N3 bias was −4.5 percentage points (C4-M1: −4.8) and N3 % coverage of the proposed intervals 42 % (C4-M1: 38 %): the montage change did not explain the failure, which points to differences in population or scoring rules (R&K versus AASM).

When all components were fitted on a few manually scored nights of the target cohort (Fig. 3b, c, e, f; Supplementary S6), ten nights gave mean coverage over parameters of 92.0 % on HMC and 90.3 % on ST for the proposed intervals (YASA), versus 89.8 % and 86.0 % for Bland–Altman and 76.7 % and 72.4 % for regression-based limits; distribution-free limits require at least 19 calibration nights at α = 0.10 and were unbounded. Average coverage hid between-site variability: the realised coverage of the remaining nights fell below 80 % in 9 % (HMC) and 17 % (ST) of repetitions (median over parameters; Bland–Altman 10 % and 28 %), and with 30 nights still in 7 % and 15 %. With ten nights, intervals on HMC were 29 % wider than with the full calibration half of about 75 nights (median over parameters; Supplementary S6).

### 3.6. Error analysis
Non-covered nights had lower plug-in accuracy (median 0.75 versus 0.81; Supplementary S12). The WASO failure in SC had a specific mechanism: the 10-h SC window contains long wake after the final awakening (median 116 min, versus 0.5 min in HMC), and one spurious sleep epoch late in a sampled hypnogram moves the final awakening and converts this wake into WASO. On average 49 % of the samples of an SC night placed the final awakening more than 60 min after the reference (1 % in HMC), and this fraction correlated with the posterior-mean WASO error (Spearman ρ = 0.79).

### 3.7. Clinical decisions
At the threshold TST < 6 h (prevalence 26 %), the proposed intervals lay entirely on one side of the threshold for 64 % of test nights, and 98.7 % of these decisions agreed with the reference (Fig. 5e–h; YASA, pooled over cohorts; Supplementary S8); distribution-free limits decided 60 % (98.3 % correct) and Bland–Altman limits 54 % (97.7 %), whereas classifying every night by its plug-in TST was correct for 84.2 %. For WASO > 30 min the proposed intervals decided more nights (29 % versus 20 %) at lower accuracy (92.7 % versus 95.7 %); for SOL > 30 min the two were similar (73 % and 74 % decided, 98.0 % and 96.9 % correct). For a REM latency ≤ 15 min (prevalence 2.5 %), 53 % of nights were decided (33 % with distribution-free limits), all as negative: no interval lay entirely below 15 min.

### 3.8. Sensitivity analyses, robustness, flagging and cost
The pre-specified criterion of a positive width–error correlation (95 % CI excluding zero) was met in 30 of 48 stager–cohort–parameter combinations (6 of 6 for TST, 1 of 6 for WASO; Fig. 5a–c; Supplementary S10). Coverage changed by at most 1.1 percentage points with M = 100 instead of 1000 samples, remained 89.4–93.3 % when only 25 % of nights were used for calibration, and varied by at most 2.5 percentage points across 3 stager seeds (Supplementary S10). Under signal corruption of test nights all methods lost coverage (Fig. 4; Supplementary S13), but adaptive intervals less so because their width responded to the corrupted signal: with movement artefacts in 25 % of epochs, TST coverage was 86 % for the proposed intervals versus 70 % for distribution-free and 51 % for Bland–Altman limits; under strong Gaussian noise no method remained valid. Interval width identified nights with REM-latency errors > 30 min better than mean epoch entropy (AUROC 0.74 versus 0.57 in SC), but for TST the label-free difference between raw and recalibrated plug-in was the better flag in HMC (0.79 versus 0.68; Fig. 5d; Supplementary S14). Sampling (M = 1000) and parameter computation took 0.02 s per night on one CPU core, against 1.4 s for YASA itself (Supplementary S15).


## 4. Discussion

Epoch probabilities of an automatic stager can be turned into per-night intervals for clinical sleep parameters that reach their nominal coverage within a cohort when every component is fitted on the calibration nights alone, for an external pretrained stager and an in-domain stager. Whether such intervals are more informative than the limits of agreement already used in validation studies depended on the parameter. For TST they had lower interval scores than parametric, regression-based and distribution-free limits in every cohort, significantly so against distribution-free limits, and they allowed more nights to be classified confidently at a 6-h threshold. For the other parameters they offered no consistent advantage, and for WASO in long ambulatory recordings they were worse. Neither the intervals nor any limits of agreement transferred between cohorts; calibration on locally scored nights restored average coverage, but not reliably at every site with ten nights.

**Relation to previous work.** Epoch-level uncertainty methods [@kang2021; @fiorillo2021; @phan2022; @heremans2024; @bechny2024; @li2025conmil] identify epochs to review, night-level scorability models [@mikkelsen2020; @ganglberger2024] predict whether a recording will be scored well, and Hardarson et al. [@hardarson2023] showed at the population level how staging errors propagate to sleep parameters. Posterior sampling of whole hypnograms has been used to describe the uncertainty of overnight statistics [@vangorp2023icassp; @vangorp2023jbhi], without a guarantee that the resulting ranges contain the clinical scorer's value. The present procedure adds that guarantee, in the units clinicians use, for any stager that outputs epoch probabilities, and compares it head-to-head with the agreement statistics that validation studies report [@svensson2024; @beau2025; @kaneda2026].

**Why the gain was specific to TST.** The adaptive scale did what it was designed to do: at a fixed centre, widths proportional to the posterior spread were more efficient than constant widths for almost every parameter, and the advantage over limits of agreement was largest on the nights that were hardest to score. Whether this translated into an advantage over limits of agreement depended on how much of a parameter's error the posterior spread explains. TST errors accumulate over the whole night from many ambiguous sleep–wake epochs, which is what sampled hypnograms vary; consistent with this, interval width correlated with the plug-in error for TST in 6 of 6 stager–cohort combinations, but for N2 % in only 2 and for WASO in 1 (a correlation alone was not sufficient: it held for N1 % in 6 of 6 without a consistent gain). Errors in stage percentages are plausibly dominated by systematic differences in how a stager and a scorer draw stage boundaries (for example N3 under different rule sets), which a posterior given the stager's own probabilities cannot see; the posterior spread then adds little to a well-chosen constant width. Latencies depend on single transitions and have skewed error distributions; for sleep onset latency, conformalised posterior quantiles were better than the symmetric score (Supplementary S3). Regression-based limits of agreement, which model level-dependent bias, achieved competitive interval scores for these parameters but did not reach nominal coverage.

**The WASO failure and the choice of centre.** In the SC recordings the fixed 10-h window extends far beyond the final awakening; a single spurious sleep epoch late in a sampled hypnogram converts this wake into WASO, so the posterior mean over-estimated WASO by 55–68 min and the intervals became wide. This is a property of the parameter definition as much as of the method: per-night uncertainty is only meaningful for parameters that are stable to isolated epoch errors, and in clinical PSG ending at lights-on (HMC) the problem was absent. More generally, the pre-specified configuration was not optimal: removing the regulariser of the score lowered the interval score by about 5 % on average, and the calibrated plug-in was an equally good centre for several parameters. We did not tune the method on these results; parameter-specific choices would need confirmation in independent data.

**Implications for practice.** A laboratory deploying an automatic stager can (i) score a set of local nights manually, as recommended for validating any scoring method; (ii) use them to recalibrate the stager's probabilities, which by itself removed most of the TST bias; and (iii) report TST with a per-night interval, reviewing nights whose interval is wide or straddles a decision threshold. For parameters other than TST, distribution-free limits of agreement, calibrated on the same local nights, were a simpler and equally informative alternative. Ten local nights restored average coverage, but a site's realised coverage still fell below 80 % in up to 17 % of our repetitions, and distribution-free limits need at least 19 nights at α = 0.10. We therefore suggest at least 20 locally scored nights, recognising that even 30 nights left a non-negligible risk of low realised coverage in the small ST cohort (15 % of repetitions).

**Limitations.** (i) Coverage is marginal, not conditional: the hardest nights were under-covered (about 85 % in the lowest-accuracy quartile), although less than with limits of agreement. (ii) Validity requires exchangeability between calibration and test nights; it failed across cohorts, and weighted conformal methods for distribution shift [@tibshirani2019; @barber2023] are a possible extension. Within-subject correlation (two nights per subject in Sleep-EDF) combined with small calibration sets also weakens the finite-sample guarantee, which showed as some under-coverage of distribution-free limits in ST. (iii) Each night had one human scorer, so the intervals cover that scorer's values, including scorer-specific disagreement [@rosenberg2013; @dankerhopfe2009]. (iv) The cohorts were moderate in size (348 nights), adult and scored with two rule sets, both stagers were feature-based, and HMC provides no demographics; deep-learning stagers were not evaluated, although the method only needs epoch probabilities. (v) The first-order HMM ignores longer-range sleep architecture. (vi) The primary analysis changed after the first review from the pre-registered design, in which hidden Markov components were cross-fitted over the whole cohort, to the end-to-end protocol reported here; comparators and decision thresholds were added at the same time. The pre-registered analysis, reported in full in Supplementary S9, led to the same qualitative conclusions, and all deviations are documented (Supplementary S1).


## 5. Conclusion

Conformally calibrated posterior hypnogram samples give per-night intervals for automatically scored sleep parameters that reach their nominal coverage when calibrated on nights from the same population. Their advantage over limits of agreement is parameter-specific: clear for total sleep time, where they also supported more confident threshold decisions, and absent for most other parameters. Validity did not transfer between cohorts, so any per-night or population error statement for automatic scoring should be calibrated on locally scored nights, preferably at least 20.


## Declaration of generative AI and AI-assisted technologies in the research and writing process

During the preparation of this work the author(s) used Claude (Anthropic), an AI system, to search and screen the literature, design and implement the analysis code, run the experiments and draft the manuscript text. After using this tool, the author(s) reviewed, verified and edited all content, re-ran the analysis pipeline, and take(s) full responsibility for the content of the publication. [AUTHOR ACTION REQUIRED: confirm or edit this statement so that it accurately describes how AI was used, as required by the journal's policy.]

## CRediT authorship contribution statement

[AUTHOR NAME(S)]: Conceptualization, Methodology, Software, Validation, Formal analysis, Data curation, Writing – original draft, Writing – review & editing, Visualization. [Complete according to actual contributions.]

## Declaration of competing interest

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper. [AUTHOR ACTION REQUIRED: confirm.]

## Funding

This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors. [AUTHOR ACTION REQUIRED: confirm.]

## Ethics statement

This secondary analysis used only de-identified, openly available PSG recordings distributed through PhysioNet [@goldberger2000; @pollard2026]: Sleep-EDF Expanded (Open Data Commons Attribution Licence v1.0) and the HMC Sleep Staging Database (CC BY 4.0). For the HMC database, the data descriptor and PhysioNet record state that the recordings were acquired in routine clinical care, fully anonymised, and that their reuse was approved by the institutional review board of Zuid-West Holland (METC-19-065) [@alvarez2021; @hmc_data]. The Sleep-EDF Expanded record [@sleepedf_data] does not document the approvals obtained by the original studies [@kemp2000]. No new data were collected and no one was contacted. [AUTHOR ACTION REQUIRED: state your institution's determination that this analysis of public, de-identified data does not require further ethical review, as required by the journal.]

## Data availability

The datasets analysed are publicly available from PhysioNet: Sleep-EDF Expanded [@sleepedf_data] and the HMC Sleep Staging Database [@hmc_data].

## Code availability

All code needed to reproduce every result, table and figure (data download with checksum verification, preprocessing, both stagers, posterior sampling, conformal calibration, statistics and figure generation, with unit tests and a one-command pipeline) is provided as supplementary material and will be deposited in a public repository with a persistent identifier upon acceptance [AUTHOR ACTION REQUIRED: insert repository URL/DOI].

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

**Table 2.** Within-cohort validity and efficiency of the proposed 90 % intervals (YASA stager; α = 0.10). Every label-dependent component (probability recalibration, hidden Markov model, emission temperature, conformal quantile) was fitted on the calibration half of 50 subject-grouped 50/50 splits and evaluated on the other half. Coverage: mean over splits (2.5th–97.5th percentile across splits). Width in minutes (TST, SOL, WASO, REML) or percentage points of TST (stage percentages). Interval-score (IS) ratio: proposed/comparator, computed from per-subject mean interval scores, with subject-bootstrap 95 % CI; values < 1 favour the proposed method; * Holm-adjusted p < 0.05 (two-sided sign-flip permutation test of the mean difference; Holm within cohort). Distribution-free LoA: exact split-conformal limits from signed residuals of the plug-in; regression-based LoA: bias and SD modelled as linear functions of the plug-in value; Bland–Altman LoA: t-based prediction interval. In-domain LightGBM stager in Supplementary S4.

| Parameter   | Cohort   | Coverage (2.5–97.5 % over splits)   | Mean width   | IS ratio vs Distribution-free LoA (95% CI)   | IS ratio vs Regression-based LoA (95% CI)   | IS ratio vs Bland–Altman LoA (95% CI)   |
|:------------|:---------|:------------------------------------|:-------------|:---------------------------------------------|:--------------------------------------------|:----------------------------------------|
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

**Table 3.** Bias (mean absolute error) of night-level point estimates on test nights (YASA stager). Within cohort: same 50 splits as Table 2. Plug-in: parameter of the stager's own hypnogram (no labels used); calibrated plug-in: hypnogram of the probabilities recalibrated on the calibration nights; posterior mean: mean over 1000 sampled hypnograms. Ten local nights: all components fitted on ten manually scored nights of the same cohort, remaining nights tested (50 repetitions; not applicable to SC, the source of the in-domain stager). Units as in Table 2. In-domain LightGBM stager in Supplementary S4.

| Parameter   | Cohort   | Plug-in      | Calibrated plug-in   | Posterior mean   | Calibrated plug-in, 10 local nights   | Posterior mean, 10 local nights   |
|:------------|:---------|:-------------|:---------------------|:-----------------|:--------------------------------------|:----------------------------------|
| TST (min)   | SC       | −21.4 (29.7) | −5.3 (23.4)          | +0.1 (20.4)      | –                                     | –                                 |
| TST (min)   | ST       | −22.6 (22.6) | −0.2 (7.5)           | −0.6 (8.1)       | −0.3 (7.9)                            | −1.0 (8.4)                        |
| TST (min)   | HMC      | −38.3 (40.1) | −5.2 (19.6)          | −4.9 (19.4)      | −3.8 (20.7)                           | −3.2 (20.4)                       |
| SOL (min)   | SC       | +4.4 (7.9)   | +1.0 (7.5)           | −1.8 (7.9)       | –                                     | –                                 |
| SOL (min)   | ST       | +3.8 (4.0)   | +0.2 (2.3)           | −4.2 (5.0)       | +0.2 (2.5)                            | −3.4 (4.7)                        |
| SOL (min)   | HMC      | +5.7 (7.0)   | +0.3 (5.0)           | −3.3 (7.0)       | −0.2 (5.4)                            | −3.6 (7.3)                        |
| WASO (min)  | SC       | +29.7 (35.9) | +25.4 (33.6)         | +68.5 (72.5)     | –                                     | –                                 |
| WASO (min)  | ST       | +17.4 (17.4) | +0.6 (7.3)           | +10.8 (13.8)     | +0.8 (7.6)                            | +9.4 (12.8)                       |
| WASO (min)  | HMC      | +31.1 (34.5) | +5.5 (17.1)          | +9.9 (19.1)      | +5.2 (18.1)                           | +8.9 (19.8)                       |
| REML (min)  | SC       | −6.3 (22.4)  | −6.0 (21.9)          | +4.0 (24.8)      | –                                     | –                                 |
| REML (min)  | ST       | +5.1 (19.5)  | +0.5 (22.5)          | +17.9 (31.2)     | −1.0 (26.3)                           | +16.6 (31.0)                      |
| REML (min)  | HMC      | −23.0 (36.2) | −29.1 (40.0)         | −28.2 (44.3)     | −27.8 (40.4)                          | −29.1 (45.8)                      |
| N1% (pp)    | SC       | −9.1 (9.6)   | −5.1 (7.3)           | −5.7 (7.1)       | –                                     | –                                 |
| N1% (pp)    | ST       | −4.5 (4.9)   | −3.0 (4.0)           | −3.2 (3.9)       | −2.8 (4.0)                            | −3.2 (4.0)                        |
| N1% (pp)    | HMC      | −5.5 (7.0)   | −4.8 (6.4)           | −4.1 (5.3)       | −4.8 (6.6)                            | −4.1 (5.5)                        |
| N2% (pp)    | SC       | +3.8 (9.0)   | +5.9 (9.3)           | +0.1 (7.6)       | –                                     | –                                 |
| N2% (pp)    | ST       | +1.1 (7.8)   | +3.1 (8.9)           | −0.8 (8.5)       | +2.3 (8.8)                            | −1.6 (8.8)                        |
| N2% (pp)    | HMC      | +10.4 (11.0) | +6.0 (7.9)           | −3.0 (6.7)       | +5.6 (8.1)                            | −3.3 (7.1)                        |
| N3% (pp)    | SC       | +5.9 (6.6)   | −0.8 (3.8)           | +0.9 (4.4)       | –                                     | –                                 |
| N3% (pp)    | ST       | +3.7 (6.3)   | −0.5 (6.4)           | +0.9 (6.5)       | −0.0 (6.6)                            | +1.8 (6.7)                        |
| N3% (pp)    | HMC      | −4.8 (6.6)   | −1.3 (5.8)           | +3.2 (6.9)       | −1.1 (6.0)                            | +3.6 (7.3)                        |
| REM% (pp)   | SC       | −0.5 (4.2)   | −0.1 (4.1)           | +4.6 (6.3)       | –                                     | –                                 |
| REM% (pp)   | ST       | −0.2 (3.9)   | +0.5 (4.1)           | +3.1 (5.7)       | +0.5 (4.5)                            | +3.0 (5.8)                        |
| REM% (pp)   | HMC      | −0.1 (4.2)   | +0.2 (4.0)           | +3.9 (5.4)       | +0.2 (4.3)                            | +3.8 (5.6)                        |

## Figure captions

![**Fig. 1.** The procedure on one HMC night (YASA stager). (a) Calibrated epoch probabilities; (b) manual reference hypnogram; (c) the stager's own hypnogram (plug-in); (d) three hypnograms sampled from the posterior by forward-filtering backward-sampling; (e, f) posterior distributions of TST and REM latency over 1000 samples, with the reference value, the plug-in estimate, the proposed 90 % interval (calibrated leave-one-subject-out on the other HMC nights) and the Bland–Altman limits of agreement.](figures/fig1_example_night.png){width=100%}

![**Fig. 2.** Within-cohort efficiency. Mean interval score of each method relative to distribution-free limits of agreement (LoA; log scale) for each parameter, cohort and stager (50 subject-grouped splits, all components fitted on the calibration half; α = 0.10). Values below 1 indicate better intervals (narrower, or fewer and smaller misses). Proposed method: ratio of per-subject means with subject-bootstrap 95 % CI. Constant (calibrated centre): constant-width conformal interval around the calibrated plug-in; FFBS SD (unreg.): proposed score without the regulariser. Coverage of all methods in Supplementary S2.](figures/fig2_within_cohort_efficiency.png){width=100%}

![**Fig. 3.** Transport and local deployment. (a, d) Coverage on ST (×) and HMC (○) of 90 % intervals calibrated on SC. (b, e) Mean coverage over the eight parameters when every component is fitted only on n manually scored nights of the target cohort and the remaining nights are tested (50 repetitions; shaded: range over parameters for the proposed method on HMC). (c, f) Probability that the realised coverage of the remaining nights falls below 0.80 (median over parameters). Solid: HMC; dashed: ST. Distribution-free LoA are unbounded with fewer than 19 calibration nights (α = 0.10) and are not shown for ten nights.](figures/fig3_transport_local.png){width=100%}

![**Fig. 4.** Robustness to signal corruption (YASA; calibration on clean nights, test on corrupted nights). Coverage (top) and mean width (bottom) for TST, WASO and N3 % under additive Gaussian noise (0.5 and 1.0 × robust SD) and movement-artefact drifts in 10 % or 25 % of epochs.](figures/fig4_robustness.png){width=100%}

![**Fig. 5.** Adaptivity, flagging and clinical decisions (YASA). (a–c) Width of the proposed interval versus absolute error of the plug-in estimate (leave-one-subject-out). (d) AUROC (95 % subject-level bootstrap CI) for detecting nights with a clinically relevant plug-in error (|ΔTST| > 30 min, |ΔREML| > 30 min, |ΔN3 %| > 5 percentage points) from the interval width, the mean epoch entropy, or the label-free difference between the raw and the calibrated plug-in estimate. (e–h) Decisions at common thresholds (Table 2 protocol, pooled over cohorts): fraction of test nights whose 90 % interval lay entirely on one side of the threshold, and accuracy of these decisions against the manual reference. Dotted line: accuracy when every night is decided from the uncorrected automatic value.](figures/fig5_adaptivity_decisions.png){width=100%}
