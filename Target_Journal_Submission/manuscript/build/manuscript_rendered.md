---
title: "Per-night prediction intervals for automatically scored polysomnography: conformal calibration of posterior hypnogram samples with external validation"
---

**Running title:** Per-night intervals for automatic sleep scoring

**Authors:** [AUTHOR NAME(S)]^a^

^a^ [Affiliation, address, country]

**Corresponding author:** [Name, address, e-mail]

**Article type:** Original Article

**Word count:** main text 4,437 words; abstract 288 words

**Highlights**

- Automatic sleep scoring gives no per-night error range for clinical sleep parameters.
- Posterior hypnogram sampling plus conformal calibration gives per-night intervals.
- At a fixed centre, posterior-spread scaling narrowed intervals in most settings.
- Recalibrating the stager on locally scored nights removed most sleep-time bias.
- Coverage did not transfer across cohorts; ten locally scored nights restored it.

**Abstract**

*Objective:* Automatic sleep staging is validated with population limits of agreement but gives no error range for the parameters of an individual night. We developed and externally evaluated per-night prediction intervals for automatically scored polysomnography parameters.

*Methods:* Stage probabilities from a stager were combined with a hidden Markov model of stage transitions; whole hypnograms were sampled by forward-filtering backward-sampling, and the per-night spread of total sleep time (TST), sleep onset latency, wake after sleep onset (WASO), REM latency and stage percentages was conformally calibrated on manually scored nights. We evaluated a pretrained external stager (YASA) and an in-domain stager on Sleep-EDF and HMC data (348 nights, 251 subjects) against Bland–Altman limits of agreement and other interval methods, including transfer between cohorts, local recalibration and signal corruption.

*Results:* Within cohorts, 90 % intervals covered 89.0–92.1 % of reference values (YASA). At a fixed centre, scaling widths by the posterior spread lowered the interval score versus constant widths in 23 of 24 cohort–parameter combinations (LightGBM: 21). Against bias-corrected, distribution-free limits of agreement, intervals were significantly better in 9 and worse in 4 combinations, with the largest gains for TST and none for REM %. The nights hardest to score were under-covered (81–85 %). Recalibrating stage probabilities on locally scored nights reduced the TST bias of the stager's hypnogram from -38 to -5 min (HMC). Intervals did not transfer between cohorts (N3 % coverage on HMC: 38 %); calibration on ten local nights restored it to 91 % on average.

*Conclusions:* Automatically scored sleep parameters can be reported with per-night intervals of verified average coverage. Adaptive scaling makes them more informative than limits of agreement for several parameters, and a small set of locally scored nights is needed to correct bias and restore coverage in a new population.

**Keywords:** automatic sleep staging; polysomnography; conformal prediction; uncertainty quantification; sleep parameters; external validation


## 1. Introduction

Automatic sleep staging now reaches epoch-by-epoch agreement with human scorers comparable to the agreement between scorers themselves [@rosenberg2013; @dankerhopfe2009; @stephansen2018; @perslev2021; @vallat2021], and open-source tools make it available to any laboratory [@vallat2021; @perslev2021]. Clinicians, however, do not read hypnograms epoch by epoch: diagnostic and research decisions rest on night-level parameters such as total sleep time (TST), sleep onset latency (SOL), wake after sleep onset (WASO), REM latency and the proportion of each stage. Validation studies, including those published in this journal, therefore summarise algorithm–scorer agreement for these parameters with Bland–Altman bias and limits of agreement across a cohort [@svensson2024; @beau2025; @rohrscheib2026].

Population limits of agreement answer the question "how far off is the algorithm on average?", not "how far off might it be tonight?". Errors in night-level parameters are heteroscedastic: they concentrate in fragmented, pathological or technically poor recordings and in older patients [@baumert2023; @deirossi2025], and even high epoch accuracy can translate into poor estimates of individual parameters because epoch errors are temporally clustered [@hardarson2023]. A clinician reviewing an automatically scored study therefore lacks a statement of the form "for this night, TST lies within the interval [a, b] min with 90 % confidence", which would show when a night can be signed off and when it needs manual review.

Uncertainty quantification for sleep staging has so far been developed at the epoch level. Entropy, Monte-Carlo dropout and dedicated confidence networks flag ambiguous epochs for review [@kang2021; @fiorillo2021; @phan2022; @heremans2024; @bechny2024], hypnodensity graphs display stage probabilities [@stephansen2018; @vangorp2022; @bakker2023], and conformal prediction sets have been proposed for single epochs [@li2025conmil]. Night-level approaches predict a recording's overall agreement or "scorability" [@mikkelsen2020; @ganglberger2024] but not an error range in clinical units, and Monte-Carlo propagation of staging error to sleep parameters has been studied at the population level [@hardarson2023]. Translating epoch probabilities into calibrated intervals for night-level parameters is not straightforward: parameters such as SOL, WASO and REM latency are non-linear functionals of the whole hypnogram, and errors in neighbouring epochs are strongly correlated.

Conformal prediction provides intervals with finite-sample coverage guarantees for any predictive model, provided that calibration and test cases are exchangeable [@vovk2005; @lei2018; @angelopoulos2023]. Applied naively—a constant margin around each estimate—it reproduces an empirical version of the limits of agreement and cannot distinguish easy from difficult nights. Its usefulness therefore depends on a per-night measure of difficulty, and its guarantee depends on exchangeability, which may fail when an algorithm calibrated in one laboratory is used in another [@tibshirani2019; @barber2023].

We propose a model-agnostic procedure that (i) samples complete hypnograms from the posterior implied by a stager's epoch probabilities and a Markov model of stage transitions, using forward-filtering backward-sampling, (ii) computes every clinical parameter on every sample, and (iii) conformally calibrates the resulting per-night spread on a small set of manually scored nights. We evaluated it with two stagers on three cohorts (348 nights), against Bland–Altman limits of agreement and other conformal and regression-based intervals, addressing five questions: are per-night intervals valid within a cohort; are they narrower and better targeted than constant-width intervals; which components matter; does validity transfer across cohorts and how many locally scored nights restore it; and can interval width identify nights with clinically relevant errors.


## 2. Materials and methods

### 2.1. Datasets
We used three openly available polysomnography (PSG) cohorts (Table 1). Sleep-EDF Expanded [@kemp2000; @sleepedf_data] provides 153 ambulatory home recordings from 78 healthy adults aged 25–101 years (SC cohort, mostly two nights per subject) and 44 in-hospital nights from 22 adults with mild difficulty falling asleep, recorded once after placebo and once after temazepam (ST cohort). The Haaglanden Medisch Centrum (HMC) database [@alvarez2021; @hmc_data] contains 151 clinical PSGs of patients referred to a sleep centre for various sleep disorders. SC and ST were scored by Rechtschaffen and Kales rules (stages S3 and S4 merged into N3), HMC by AASM rules [@berry2017]. All data are de-identified and publicly released under open licences; no new data were collected, so no ethics approval was required.

### 2.2. Analysis windows and night-level parameters
To avoid deriving the analysis window from the reference hypnogram, windows were fixed from metadata only: SC, lights-off to lights-off + 10 h (the 20-h SC files contain daytime naps); ST, lights-off to end of recording; HMC, the annotated lights-off and lights-on markers. Within each window we computed eight parameters for a hypnogram *y*: total sleep time (TST), sleep onset latency from lights-off (SOL), wake after sleep onset (WASO), REM latency from sleep onset (REML), and the percentages of TST spent in N1, N2, N3 and REM. Epochs marked as movement or unscored in the reference were excluded from both reference and automatic parameters. REML was analysed only for nights whose reference contained REM sleep; if a sampled or automatic hypnogram contained no REM, its REML was right-censored at the window end.

### 2.3. Automatic stagers
The method operates on the epoch-wise stage probabilities of any stager. We studied two. (i) YASA [@vallat2021], a published open-source stager whose LightGBM classifier was trained by its authors on several thousand NSRR recordings; we used its EEG + EOG model without any retraining, so every night in our cohorts is an external test night for this stager (SC/ST: Fpz-Cz and horizontal EOG; HMC: C4-M1 and E1-M2, the montage recommended by its authors). (ii) An in-domain LightGBM model trained on the same 116 YASA features of SC nights, with out-of-fold SC predictions from subject-grouped five-fold cross-validation and a model trained on all SC nights for ST and HMC (where it additionally faces a montage change). Hyper-parameters were fixed a priori; three predefined seeds were run. The stager's own hypnogram (most probable stage per epoch) defines the *plug-in* parameter estimates, i.e. current practice.

### 2.4. Posterior sampling of whole hypnograms
Let $p(k \mid x_t)$ be the stager probability of stage k for epoch t of a night with N epochs. Probabilities were first recalibrated by bias-corrected temperature scaling [@alexandari2020],

$$\tilde p(k \mid x_t)=\operatorname{softmax}_k\!\left(\frac{\log p(k \mid x_t)}{T}+b_k\right) \qquad (1)$$

fitted by maximum likelihood on labelled source nights; $\pi_s$ denotes the stage distribution of those nights. Following the hybrid classifier/hidden-Markov formulation [@bourlard1994; @rabiner1989], scaled likelihoods

$$e_t(k)=\left[\frac{\tilde p(k \mid x_t)}{\pi_s(k)}\right]^{\tau} \qquad (2)$$

serve as emission scores of a first-order Markov chain with transition matrix $A$ and initial distribution $p_0$ estimated from the source hypnograms (add-one smoothing). The posterior over complete hypnograms is then

$$P(y_1,\dots,y_N \mid x)\;\propto\; p_0(y_1)\,e_1(y_1)\prod_{t=2}^{N} A(y_{t-1},y_t)\,e_t(y_t) \qquad (3)$$

Because most stagers already use neighbouring epochs as context (YASA uses rolling-window features), multiplying their outputs along the chain would count the same evidence repeatedly; the emission temperature $\tau \in [0.02, 1.5]$ absorbs this and was fitted on source nights by maximising the smoothed posterior log-likelihood of the reference stages. We drew $M = 1000$ hypnograms per night exactly from (3) by forward-filtering backward-sampling (FFBS) [@carter1994; @fruhwirth1994]: forward probabilities $\alpha_t(k) \propto e_t(k)\sum_j \alpha_{t-1}(j)A(j,k)$, then $y_N \sim \alpha_N$ and $y_t \mid y_{t+1} \sim \alpha_t(j)A(j,y_{t+1})$ for $t=N-1,\dots,1$. Every parameter $\theta$ was computed on every sample, giving a per-night posterior mean $\hat\mu$ and standard deviation $\hat\sigma$ (and quantiles). Unlike sampling each epoch independently, FFBS preserves the temporal correlation of stage errors, which dominates the uncertainty of sums and latencies.

### 2.5. Conformal calibration of per-night intervals
Posterior spreads from (3) are not calibrated: they describe uncertainty given the model, not the stager's systematic errors. We therefore used split conformal prediction [@vovk2005; @lei2018; @angelopoulos2023]. For $n$ labelled calibration nights with reference values $\theta_i$ we computed normalised scores

$$s_i=\frac{\lvert \theta_i-\hat\mu_i\rvert}{\hat\sigma_i+\bar\sigma} \qquad (4)$$

where $\bar\sigma$ is the median of $\hat\sigma$ over the calibration and test nights (a regulariser that stops nights with near-zero posterior spread from dominating; because $\hat\sigma$ requires no labels, computing $\bar\sigma$ over all nights keeps the score a symmetric function of the data and the guarantee below exact). With $\hat q$ the $\lceil (n+1)(1-\alpha)\rceil$-th smallest score, the interval for a new night is

$$C(x)=\left[\hat\mu-\hat q\,(\hat\sigma+\bar\sigma),\;\hat\mu+\hat q\,(\hat\sigma+\bar\sigma)\right] \qquad (5)$$

intersected with the feasible range (≥ 0 min; 0–100 %). If calibration and test nights are exchangeable, $P\{\theta \in C(x)\} \ge 1-\alpha$ in finite samples, whatever the stager or the HMM [@vovk2005; @lei2018]; the HMM therefore affects only the width and adaptivity of the intervals, never their validity. The method, its score, $\alpha = 0.10$ and all comparators were fixed in a protocol written before any interval was computed (Supplementary S1).

### 2.6. Comparators and ablations
Comparators used the same calibration nights: (a) Bland–Altman limits of agreement around the plug-in estimate [@bland1986] (bias ± z·SD, the usual validation summary); (b) its distribution-free counterpart, a bias-corrected constant-width conformal interval (plug-in + mean calibration residual ± conformal quantile of the centred absolute residuals), the strongest simple competitor; (c) constant-width conformal intervals [@lei2018] around three different centres—the raw plug-in, the plug-in of the locally recalibrated probabilities and $\hat\mu$; (d) conformalised quantile regression (CQR) [@romano2019] with linear quantile regression on night-level features (plug-in value, $\hat\mu$, mean epoch entropy, mean maximum probability) fitted on half of the calibration subjects; (e) CQR applied to the FFBS 5th/95th percentiles; (f) normalised conformal intervals with mean epoch entropy as scale; (g) raw FFBS percentile intervals without conformal calibration. Crossing the three centres in (c) with the FFBS-SD scale of (4) gives a centre × scale factorial that separates the effect of the adaptive scale from that of the centre. Ablations replaced FFBS by independent per-epoch sampling, fixed $\tau = 1$, or removed the $\bar\sigma$ regulariser. Comparators (b) and (c) with calibrated or posterior-mean centres, and the factorial, were added after the first analysis to separate calibration from adaptivity (Supplementary S1).

### 2.7. Evaluation design
*Within-cohort validity and efficiency.* For each stager and cohort, nights were split 500 times at random into calibration and test halves, grouped by subject, and coverage, mean width and the interval score [@gneiting2007] (width plus a $2/\alpha$ penalty per unit of miss) were averaged over test nights. In addition, leave-one-subject-out (LOSO) calibration gave one interval per night for paired comparisons. HMM components (calibration, $\pi_s$, $A$, $p_0$, $\tau$) were fitted by subject-grouped five-fold cross-fitting, so no night contributed to its own model.
*Transportability.* Intervals calibrated on all SC nights (HMM fitted on SC) were applied to ST and HMC. We then simulated local recalibration by labelling $n_t \in \{10, 20, 30, 50\}$ target nights (whole subjects; 500 repetitions) and calibrating on target nights only or on SC plus target nights.
*Robustness.* EEG and EOG of test nights were corrupted with additive Gaussian noise (0.5 and 1.0 × the channel's robust SD) or with high-amplitude movement-artefact drifts in 10 % or 25 % of epochs, while calibration nights stayed clean (YASA stager; 200 splits).
*Clinical utility.* We asked whether a night's interval width identifies nights whose plug-in estimate has a clinically relevant error (pre-specified: |ΔTST| > 30 min, |ΔREML| > 30 min, |ΔN3%| > 5 percentage points), compared with mean epoch entropy and mean maximum probability, and compared the plug-in, the plug-in of locally recalibrated probabilities and the posterior mean as point estimates by Bland–Altman analysis and the intraclass correlation ICC(A,1) [@mcgraw1996].

### 2.8. Statistical analysis
Subjects were the unit of analysis. LOSO interval scores were averaged per subject and compared between the proposed and each comparator with two-sided Wilcoxon signed-rank tests (effect size: matched-pairs rank-biserial correlation r), Holm-adjusted across comparators and parameters within each cohort and stager. Confidence intervals for coverage and AUROC used 1000–2000 subject-level cluster-bootstrap resamples. Pre-specified success criteria were: within-cohort coverage within ±3 percentage points of nominal, and superiority over constant-width intervals only if interval scores were lower with Holm-adjusted p < 0.05.

### 2.9. Software and reproducibility
Analyses used Python 3.13, YASA 0.8.1, LightGBM 4.7, scikit-learn 1.9 and NumPy/Numba on a 4-core CPU without GPU. A single script regenerates every result, table and figure from the public data; all numbers in this article are read from machine-generated files (code availability statement).


## 3. Results

### 3.1. Cohorts and stagers
The analysis included 348 nights from 251 subjects (362,271 scored epochs; Table 1). Mean per-night Cohen's κ of the external YASA stager was 0.71 (SC), 0.73 (ST) and 0.63 (HMC); the in-domain LightGBM stager reached 0.75 on SC (out-of-fold) but only 0.49 on HMC, where it also faced a montage change. The fitted emission temperature was τ = 0.10 (range 0.10–0.15) across folds and stagers, i.e. both stagers' outputs had to be strongly down-weighted along the chain, consistent with their built-in temporal context. Fig. 1 illustrates the procedure on one HMC night.

### 3.2. Within-cohort validity
Within each cohort, the proposed 90 % intervals covered the reference value in 89.0–92.1 % of test nights for YASA and 89.9–92.0 % for LightGBM across all 24 cohort–parameter combinations (500 splits; Table 2), meeting the pre-specified ±3 percentage-point criterion; the other conformal comparators with exact guarantees behaved similarly (Supplementary Table S2). Parametric Bland–Altman limits of agreement fell as low as 83.0 % (YASA) and 83.8 % (LightGBM), and their bias-corrected distribution-free counterpart, whose bias is estimated on the calibration nights, to 85.2 % and 87.1 %, mostly in the small ST cohort. Uncalibrated posterior percentile intervals covered only 27–86 % of reference values for TST, WASO and stage percentages while over-covering the latencies (89–98 %; YASA), and intervals from independent per-epoch sampling covered as little as 4 %: posterior spread alone misstates the error of night-level parameters, and ignoring the temporal correlation of epoch errors makes this much worse. Coverage of the proposed intervals was close to nominal across subgroups of age, sex and drug condition (84–94 % in subgroups with ≥40 nights; Supplementary Table S9) but not across nights of different difficulty: in the quartile of nights with the lowest plug-in accuracy it was 81–85 % (distribution-free limits of agreement: 76–80 %), and in the best quartile 92–96 % (94–99 %). In an exploratory analysis, calibrating separately for nights above and below the median mean epoch entropy—a label-free difficulty proxy (Mondrian calibration)—raised worst-quartile coverage in 5 of 6 cohort–stager combinations (to 84–89 %) with unchanged overall coverage (89.5–90.8 %; Supplementary S17).

### 3.3. Efficiency: the contribution of the centre and of the adaptive scale
Interval efficiency depended on two separable choices, the centre of the interval and its width (Fig. 2; Supplementary Tables S2–S4). *Scale:* holding the centre fixed, scaling the width by the FFBS posterior standard deviation lowered the mean interval score relative to a constant width in 23 of 24 cohort–parameter combinations with the posterior-mean centre, 18 with the calibrated plug-in centre and 20 with the raw plug-in centre for YASA (21, 18 and 19 for LightGBM; median interval-score ratios 0.94–0.96). In the paired leave-one-subject-out analysis these reductions were significant (Holm-adjusted p < 0.05) in 13, 12 and 13 combinations, against 0, 1 and 2 significant increases (YASA; LightGBM: 14, 10, 10 versus 1, 4, 2). *Centre:* in most settings, the posterior mean was the better centre for N1 %, N2 % and REM latency, and the locally calibrated plug-in for REM %, SOL and WASO (Supplementary Table S4; Section 3.6).

Against the strongest constant-width competitor—bias-corrected, distribution-free limits of agreement—the pre-specified method had a significantly lower interval score in 9 and a significantly higher one in 4 of 24 combinations for YASA (10 and 4 for LightGBM; Table 2). The largest gains were for TST (interval-score ratios 0.85, 0.59 and 0.71 in SC, ST and HMC) and N2 %; the significant losses concerned N3 % (HMC), REM % (HMC, SC) and WASO (SC) for YASA and REM % (HMC, SC), SOL (HMC) and WASO (SC) for LightGBM, parameters for which the posterior-mean centre was poor. Parametric Bland–Altman limits performed similarly to their distribution-free counterpart when they were valid (Table 2). The ablations showed that the pre-specified configuration was not the best variant for every parameter (Supplementary Table S4; ratios > 1 favour the pre-specified method). Removing the regulariser $\bar\sigma$ lowered the interval score modestly for most parameters (median ratio 0.95); an emission temperature of τ = 1 instead of the fitted value improved SOL and WASO (median ratios 0.48 and 0.63) but worsened N2 % and N3 % (1.24 and 1.24); conformalised FFBS quantiles (CQR) were better for the skewed latencies (0.77 for SOL, 0.89 for REML); sampling epochs independently instead of by FFBS worsened the latencies (1.35 for REML, 1.40 for SOL) but was as good or better for N1 % and REM % (0.93 and 0.84); and scaling by mean epoch entropy was worse for the latencies (1.22 for SOL, 1.09 for REML) and similar for stage percentages (all YASA; LightGBM in Supplementary Table S4). Results were stable across stager seeds (maximum coverage range 1.9 percentage points across 3 seeds) and α levels (Supplementary Tables S5–S6).

### 3.4. Point estimates
The stagers' own hypnograms systematically underestimated TST (YASA bias -21.7, -22.7 and -38.3 min in SC, ST and HMC; Table 3). Most of this bias was removed by recalibrating the epoch probabilities on the labelled calibration nights (calibrated plug-in: -6.0, -1.3 and -4.8 min), which also halved the mean absolute error in HMC (40 to 19 min). Averaging over posterior hypnograms added little beyond calibration: the posterior-mean TST error was similar to that of the calibrated plug-in in HMC and ST (MAE 19 and 8 min) and somewhat smaller in SC (20 versus 23 min). The posterior mean was worse than the calibrated plug-in for REM %, SOL and REM latency and, markedly, for WASO in SC (bias 68 min). Findings for LightGBM were similar (Supplementary Table S8).

### 3.5. Transportability and local recalibration
Intervals calibrated on SC did not transfer reliably (Fig. 4; Supplementary Table S13). Coverage remained acceptable on ST for most parameters but collapsed for N3 % on HMC (38 % for the proposed method, 54 % for Bland–Altman and 46 % for distribution-free limits of agreement with YASA); the in-domain LightGBM stager, which additionally faced a montage change, lost coverage for several parameters on HMC, including TST (50 %). The cause was a reversal of the stager's N3 bias between cohorts (plug-in bias +5.9 percentage points in SC versus -4.8 in HMC; Supplementary Table S10), which no interval calibrated on SC can anticipate; methods that learn and correct the SC bias were hurt most, whereas a constant-width interval around the uncorrected plug-in kept 83 %. Calibrating instead on a small number of manually scored target nights restored nominal coverage: with ten HMC nights, mean coverage was 91.0 % for the proposed method versus 86.2 % for Bland–Altman and 89.3 % for distribution-free limits, and with ten ST nights 89.4 % versus 83.1 % and 86.5 %. Coverage at an individual site nevertheless varied: with ten calibration nights, the realised coverage of the remaining nights fell below 80 % in 11 % (HMC) and 19 % (ST) of repetitions for the proposed method, versus 24 % and 38 % for Bland–Altman limits (median over parameters; Supplementary S17). Pooling SC and target nights did not fully correct the HMC shift (88.1 % with 50 target nights).

### 3.6. Error analysis
Non-covered nights had lower plug-in accuracy (median 0.75 versus 0.81; Mann–Whitney p < 0.05 in 10 of 24 cohort–parameter comparisons) and higher mean epoch entropy (p < 0.05 in 9 of 24; YASA, Supplementary Table S11). The WASO failure in SC had a specific mechanism: the 10-h SC window contains long periods of wake after the final awakening (median 116 min, versus 0 min in HMC), and a single spurious sleep epoch late in a sampled hypnogram moves the final awakening and converts this wake into WASO. On average 49 % of samples per SC night placed the final awakening more than 60 min after the reference (1 % in HMC), and this fraction correlated with the posterior-mean WASO error (Spearman ρ = 0.79).

### 3.7. Robustness to signal corruption
With calibration on clean nights and corrupted test nights, the coverage of all methods decreased as corruption increased (Fig. 5; Supplementary Table S12). No method remained valid under strong additive noise. The adaptive intervals degraded less because their width responded to the corrupted signal: for TST, coverage under strong noise fell to 32 % for the proposed intervals, which widened from 71 to 108 min, but to 7 % for distribution-free limits of agreement, whose width cannot change; with artefacts in 25 % of epochs, TST coverage was 85 % versus 48 %.

### 3.8. Flagging nights with large errors and computational cost
The width of a night's interval identified nights with clinically relevant plug-in errors in REM latency better than mean epoch entropy (AUROC 0.74 vs 0.57 in SC and 0.68 vs 0.49 in HMC, YASA), was modestly better for N3 % and comparable for TST (Fig. 3; Supplementary Table S14). Overall discrimination was moderate (AUROC mostly 0.6–0.8). Posterior sampling (M = 1000) and parameter computation took a median of 0.02 s per night on one CPU core, compared with 1.4 s for YASA feature extraction and inference, and the conformal step 0.4 ms (Supplementary Table S15).


## 4. Discussion

We have shown that the epoch probabilities of an automatic stager can be turned into per-night intervals for clinical sleep parameters that achieve their nominal coverage within a cohort, for an external pretrained stager and an in-domain stager alike. Three findings have practical consequences. First, the width of a night's interval should depend on the night: scaling by the spread of posterior hypnogram samples was more efficient than a constant width with the same centre in most settings, for both stagers and all three cohorts, and against the strongest constant-width competitor—bias-corrected, distribution-free limits of agreement—it was better for TST and stage percentages, though not for REM % or sleep onset latency. Second, most of the stagers' systematic underestimation of TST was removed by recalibrating their epoch probabilities on a few locally scored nights; averaging over posterior hypnograms added little to the point estimate. Third, neither intervals nor limits of agreement established in one cohort can be assumed to hold in another; a handful of locally scored nights was enough to restore nominal coverage.

**Relation to previous work.** Epoch-level uncertainty methods [@kang2021; @fiorillo2021; @phan2022; @heremans2024; @bechny2024; @li2025conmil] answer which epochs to review; night-level scorability models [@mikkelsen2020; @ganglberger2024] answer whether a recording is likely to be scored well; Hardarson et al. [@hardarson2023] showed, at the population level, how staging errors propagate to sleep parameters. Our contribution is complementary: a per-night interval in the units clinicians use (minutes, percentage of TST) with a coverage statement that is verified empirically and guaranteed under exchangeability. Unlike the parametric limits of agreement routinely reported in validation studies, the intervals require no normality assumption, and unlike independent per-epoch sampling, FFBS respects the temporal structure of hypnograms, which is what makes latencies and WASO uncertain. Because the procedure only consumes epoch probabilities, it can be added to existing stagers without retraining.

**Where the method helps and where it does not.** The centre × scale factorial separates two ingredients that are easily confounded. The adaptive scale was beneficial almost regardless of the centre: nights whose sampled hypnograms disagree are the nights whose parameters are uncertain. Sampling whole hypnograms rather than independent epochs mattered for the latencies, whose uncertainty depends on runs of consecutive epochs, but not for stage percentages, for which independent-epoch spread was an equally good or better scale; and the pre-specified configuration was not optimal for every parameter (an emission temperature tuned for epoch-level likelihood was too low for SOL and WASO, and the median regulariser cost some efficiency). The centre, in contrast, should be chosen per parameter. The posterior mean was a good centre for N1 %, N2 % and REM latency but a biased one for REM %, SOL and long-window WASO; with strongly tempered emissions (τ ≈ 0.1), posterior samples are pulled towards the typical stage composition of the source cohort, which inflates REM % and shortens sleep onset latency. Centring on the locally calibrated plug-in and scaling by the posterior spread, an exploratory variant, avoided these biases (Supplementary Table S4). For the skewed and bounded latencies, conformalised posterior quantiles were better than the symmetric score; we report this as a post-hoc observation to be confirmed. The SC WASO failure illustrates that per-night uncertainty is only as meaningful as the parameter definition: when the analysis window extends far beyond the final awakening, a single spurious late sleep epoch changes WASO by hours, and posterior sampling makes such epochs visible rather than hiding them. In clinical PSG, which ends at lights-on, this situation is rare (HMC), but the same caution applies to long ambulatory recordings.

**Clinical use.** In practice a laboratory deploying an automatic stager would (i) score a small set of local nights manually, as recommended for validating any scoring method, (ii) use them to recalibrate the stager's probabilities and the intervals, and (iii) report each automatically scored parameter with its interval. Nights whose intervals are wide, or whose interval straddles a decision threshold (e.g. a TST of 6 h or a REM latency of 15 min for a sleep-onset REM period), are natural candidates for manual review. Our recalibration experiment suggests that about ten local nights suffice for nominal *average* coverage, but a given site calibrated on ten nights still had a realised coverage below 80 % in roughly 11–19 % of our repetitions (twice as often with Bland–Altman limits), so larger local calibration sets are preferable when available.

**Limitations.** (i) Coverage is marginal over nights, not conditional: the nights hardest to score were under-covered (81–85 % in the lowest accuracy quartile), although less so than with constant-width intervals, and difficulty-stratified (Mondrian) calibration narrowed but did not close this gap in an exploratory analysis. (ii) Validity requires exchangeability; under cohort shift it failed for N3 %, and our recalibration remedy needs local manual scoring. Weighted conformal methods for covariate or label shift [@tibshirani2019; @barber2023] are a possible extension. (iii) Each night had a single human scorer, so the intervals cover that scorer's values; scorer disagreement [@rosenberg2013; @dankerhopfe2009] is part of the "error" the intervals absorb, and a multi-scorer reference would yield different widths. (iv) The cohorts are moderate in size (348 nights), adult, and scored with two rule sets; the in-domain stager was feature-based, and we did not evaluate deep-learning stagers, although the method is model-agnostic. (v) HMC provides no per-subject demographics, so age-related analyses were limited to Sleep-EDF. (vi) The first-order HMM ignores longer-range sleep architecture (e.g. cycle structure); richer posterior models could narrow intervals further. (vii) The bias-corrected and calibrated-centre comparators, the centre × scale factorial and the WASO analysis were added after the first results to separate competing explanations; they made our conclusions more conservative, and all deviations from the protocol are documented (Supplementary S1). (viii) Bias-corrected limits of agreement estimate their bias on the calibration nights and are therefore only approximately valid, which showed as some under-coverage in the small ST cohort.


## 5. Conclusion

Per-night conformal intervals make the uncertainty of automatically scored sleep parameters explicit in clinical units, with verified coverage. Scaling their width by the spread of posterior hypnogram samples made them more efficient than constant-width intervals in most settings, while the best centre was parameter-specific and the gains over bias-corrected limits of agreement were concentrated in TST and stage percentages. A small set of locally scored nights corrected most of the stagers' TST bias and restored coverage after a change of cohort. Reporting automatically scored parameters with locally calibrated intervals, rather than as point values qualified only by population limits of agreement, is a practical step towards safer use of automatic scoring.


## Declaration of generative AI and AI-assisted technologies in the research and writing process

During the preparation of this work the author(s) used Claude (Anthropic), an AI system, to search and screen the literature, design and implement the analysis code, run the experiments and draft the manuscript text. After using this tool, the author(s) reviewed, verified and edited all content, re-ran the analysis pipeline, and take(s) full responsibility for the content of the publication. [AUTHOR ACTION REQUIRED: confirm or edit this statement so that it accurately describes how AI was used, as required by the journal's policy.]

## CRediT authorship contribution statement

[AUTHOR NAME(S)]: Conceptualization, Methodology, Software, Validation, Formal analysis, Data curation, Writing – original draft, Writing – review & editing, Visualization. [Complete according to actual contributions.]

## Declaration of competing interest

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper. [AUTHOR ACTION REQUIRED: confirm.]

## Funding

This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors. [AUTHOR ACTION REQUIRED: confirm.]

## Ethics statement

This secondary analysis used only de-identified, openly available PSG recordings (Sleep-EDF Expanded, Open Data Commons Attribution Licence v1.0; HMC Sleep Staging Database, CC BY 4.0) distributed through PhysioNet [@goldberger2000]. The original studies obtained the approvals and consents described in their data descriptors [@kemp2000; @alvarez2021]. No new data were collected and no additional ethical approval was required.

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

**Table 2.** Within-cohort performance of the proposed 90 % intervals (α = 0.10). Each cell: coverage | mean width | interval-score ratio versus distribution-free (bias-corrected, constant-width conformal) limits of agreement | interval-score ratio versus Bland–Altman limits of agreement. Coverage and width are means over 500 subject-grouped calibration/test splits; ratios < 1 favour the proposed method; * Holm-adjusted p < 0.05 (Wilcoxon signed-rank test on per-subject mean interval scores, leave-one-subject-out calibration). Width in minutes (TST, SOL, WASO, REML) or percentage points of TST (stage percentages).

| Stager      | Parameter   | SC                            | ST                           | HMC                           |
|:------------|:------------|:------------------------------|:-----------------------------|:------------------------------|
| YASA        | TST (min)   | 0.907 | 85.3 | 0.85* | 0.85*  | 0.908 | 38.9 | 0.59* | 0.61* | 0.910 | 88.4 | 0.71* | 0.69*  |
| YASA        | SOL (min)   | 0.908 | 26.9 | 0.85* | 0.85*  | 0.896 | 18.9 | 1.93 | 2.08   | 0.909 | 22.0 | 1.34 | 1.39*   |
| YASA        | WASO (min)  | 0.907 | 230.6 | 1.47* | 1.49* | 0.911 | 53.2 | 1.19 | 1.15   | 0.911 | 81.6 | 0.83* | 0.84*  |
| YASA        | REML (min)  | 0.910 | 94.5 | 0.68* | 0.66*  | 0.921 | 148.1 | 0.93 | 0.85  | 0.909 | 183.9 | 0.99 | 0.99*  |
| YASA        | N1% (pp)    | 0.907 | 26.9 | 0.92 | 0.93*   | 0.913 | 16.9 | 1.19 | 1.13   | 0.906 | 21.6 | 0.90* | 0.91*  |
| YASA        | N2% (pp)    | 0.907 | 33.1 | 0.75* | 0.76*  | 0.890 | 33.3 | 0.89 | 0.88   | 0.909 | 28.0 | 0.76* | 0.75*  |
| YASA        | N3% (pp)    | 0.912 | 16.5 | 0.89 | 0.89    | 0.913 | 26.1 | 0.86 | 0.83   | 0.908 | 30.2 | 1.06* | 1.06*  |
| YASA        | REM% (pp)   | 0.907 | 25.0 | 1.03* | 0.99   | 0.898 | 24.0 | 1.00 | 1.02   | 0.910 | 22.0 | 1.06* | 1.06*  |
| LightGBM-SC | TST (min)   | 0.908 | 70.5 | 0.83* | 0.85*  | 0.920 | 47.1 | 0.74* | 0.74* | 0.910 | 117.5 | 0.67* | 0.67* |
| LightGBM-SC | SOL (min)   | 0.906 | 23.0 | 0.90* | 0.88*  | 0.900 | 21.4 | 1.00 | 0.91   | 0.910 | 25.9 | 1.19* | 1.21*  |
| LightGBM-SC | WASO (min)  | 0.907 | 179.4 | 1.39* | 1.38* | 0.904 | 57.9 | 1.23 | 1.21   | 0.911 | 97.0 | 0.75* | 0.75*  |
| LightGBM-SC | REML (min)  | 0.907 | 79.6 | 0.73* | 0.74*  | 0.904 | 123.4 | 0.65 | 0.60  | 0.908 | 218.2 | 1.25 | 1.26   |
| LightGBM-SC | N1% (pp)    | 0.907 | 26.2 | 0.92* | 0.92*  | 0.912 | 18.3 | 1.12 | 1.09   | 0.905 | 22.8 | 0.92* | 0.93*  |
| LightGBM-SC | N2% (pp)    | 0.906 | 30.7 | 0.92 | 0.93    | 0.900 | 31.3 | 0.84 | 0.83   | 0.906 | 36.8 | 0.91* | 0.91*  |
| LightGBM-SC | N3% (pp)    | 0.915 | 12.4 | 0.94* | 0.93   | 0.904 | 25.6 | 0.85 | 0.86   | 0.905 | 37.2 | 1.22 | 1.22*   |
| LightGBM-SC | REM% (pp)   | 0.908 | 22.8 | 1.06* | 1.03*  | 0.899 | 23.2 | 0.93 | 0.97   | 0.909 | 22.0 | 1.05* | 1.05*  |

**Table 3.** Agreement of night-level point estimates with the manual reference (YASA stager): bias (mean absolute error); ICC(A,1). Plug-in: parameter of the stager's own hypnogram; calibrated plug-in: hypnogram from locally recalibrated probabilities; posterior mean: mean over 1000 FFBS hypnogram samples. p: Wilcoxon signed-rank test of per-subject absolute errors, posterior mean versus each plug-in. LightGBM results in Supplementary Table S8.

| Parameter   | Cohort   | Plug-in            | Calibrated plug-in   | Posterior mean     |   p vs plug-in |   p vs calibrated |
|:------------|:---------|:-------------------|:---------------------|:-------------------|---------------:|------------------:|
| TST         | SC       | -21.7 (29.9); 0.76 | -6.0 (23.2); 0.81    | -0.7 (20.2); 0.83  |          0.000 |             0.000 |
| TST         | ST       | -22.7 (22.7); 0.84 | -1.3 (7.3); 0.98     | -2.2 (7.6); 0.97   |          0.000 |             1.000 |
| TST         | HMC      | -38.3 (40.2); 0.81 | -4.8 (19.5); 0.93    | -3.9 (19.3); 0.93  |          0.000 |             0.640 |
| SOL         | SC       | +4.4 (7.9); 0.81   | +0.9 (7.4); 0.79     | -1.4 (7.8); 0.61   |          0.073 |             0.300 |
| SOL         | ST       | +3.7 (3.8); 0.88   | -0.2 (2.7); 0.65     | -3.3 (4.8); 0.38   |          0.870 |             0.007 |
| SOL         | HMC      | +5.7 (7.1); 0.83   | +0.2 (5.1); 0.77     | -3.7 (7.2); 0.23   |          0.009 |             0.027 |
| WASO        | SC       | +30.1 (36.0); 0.55 | +25.7 (33.1); 0.53   | +68.2 (72.3); 0.19 |          0.000 |             0.000 |
| WASO        | ST       | +17.5 (17.5); 0.73 | +2.0 (7.3); 0.92     | +10.5 (12.4); 0.79 |          0.007 |             0.033 |
| WASO        | HMC      | +31.4 (34.9); 0.66 | +5.4 (17.4); 0.85    | +9.9 (19.4); 0.83  |          0.000 |             0.062 |
| REML        | SC       | -6.4 (21.7); 0.60  | -5.5 (21.1); 0.62    | +3.7 (24.0); 0.65  |          0.100 |             0.085 |
| REML        | ST       | +5.4 (19.8); 0.61  | +1.8 (20.0); 0.65    | +16.0 (30.9); 0.45 |          0.008 |             0.008 |
| REML        | HMC      | -22.2 (35.9); 0.60 | -29.7 (40.3); 0.47   | -29.1 (45.2); 0.39 |          0.003 |             0.004 |
| N1%         | SC       | -9.1 (9.6); 0.10   | -5.1 (7.2); 0.22     | -5.8 (7.0); 0.27   |          0.000 |             0.290 |
| N1%         | ST       | -4.6 (5.0); 0.35   | -3.1 (4.1); 0.52     | -3.4 (4.0); 0.40   |          0.014 |             0.800 |
| N1%         | HMC      | -5.6 (7.0); 0.17   | -5.0 (6.5); 0.20     | -4.0 (5.2); 0.34   |          0.000 |             0.000 |
| N2%         | SC       | +3.7 (9.0); 0.36   | +5.9 (9.2); 0.31     | +0.1 (7.5); 0.41   |          0.054 |             0.013 |
| N2%         | ST       | +0.9 (7.8); 0.31   | +2.7 (8.4); 0.26     | -1.1 (8.0); 0.22   |          0.970 |             0.680 |
| N2%         | HMC      | +10.5 (11.0); 0.30 | +6.1 (7.9); 0.43     | -3.1 (6.7); 0.55   |          0.000 |             0.260 |
| N3%         | SC       | +5.9 (6.6); 0.69   | -0.7 (3.9); 0.80     | +1.0 (4.4); 0.78   |          0.000 |             0.022 |
| N3%         | ST       | +4.0 (6.5); 0.48   | +0.2 (5.9); 0.53     | +1.6 (6.1); 0.50   |          0.610 |             0.660 |
| N3%         | HMC      | -4.8 (6.6); 0.64   | -1.4 (5.8); 0.70     | +3.1 (6.8); 0.66   |          0.860 |             0.005 |
| REM%        | SC       | -0.5 (4.2); 0.43   | -0.0 (4.1); 0.47     | +4.7 (6.2); 0.38   |          0.000 |             0.000 |
| REM%        | ST       | -0.3 (4.0); 0.53   | +0.3 (4.0); 0.46     | +2.9 (5.6); 0.33   |          0.003 |             0.002 |
| REM%        | HMC      | -0.1 (4.2); 0.62   | +0.3 (4.0); 0.62     | +4.0 (5.6); 0.52   |          0.000 |             0.000 |

## Figure captions

![**Fig. 1.** The procedure on one HMC night (YASA stager). (a) Calibrated epoch probabilities; (b) manual reference hypnogram; (c) the stager's own hypnogram (plug-in); (d) three hypnograms sampled from the posterior by forward-filtering backward-sampling; (e, f) posterior distributions of TST and REM latency over 1000 samples, with the reference value, the plug-in estimate, the proposed 90 % interval (calibrated leave-one-subject-out on the other HMC nights) and the Bland–Altman limits of agreement.](figures/fig1_example_night.png){width=100%}

![**Fig. 2.** Within-cohort efficiency. Mean interval score (500 splits, α = 0.10) of each interval method relative to distribution-free (bias-corrected constant-width) limits of agreement, for each parameter, cohort and stager; values below 1 indicate better (narrower and/or fewer and smaller misses) intervals. Coverage of all conformal methods was 0.89–0.92 (Supplementary Table S2).](figures/fig2_within_cohort_efficiency.png){width=100%}

![**Fig. 3.** Adaptivity and flagging (YASA). (a–c) Proposed interval width versus absolute error of the plug-in estimate for TST, REM latency and N3 % (leave-one-subject-out). (d) AUROC (95 % subject-level bootstrap CI) for detecting nights with a clinically relevant plug-in error (|ΔTST| > 30 min, |ΔREML| > 30 min, |ΔN3 %| > 5 percentage points) using the proposed interval width, mean epoch entropy or 1 − mean maximum probability.](figures/fig3_adaptivity_flagging.png){width=100%}

![**Fig. 4.** Transportability. (a, d) Coverage on ST (×) and HMC (○) of intervals calibrated on SC, for both stagers. (b, c, e, f) Mean coverage over 500 repetitions after recalibration with n labelled target nights, using target nights only (solid) or SC plus target nights (dashed).](figures/fig4_transport_recalibration.png){width=100%}

![**Fig. 5.** Robustness to signal corruption (YASA; calibration on clean nights, test on corrupted nights). Coverage (top) and mean width (bottom) for TST, WASO and N3 % under additive Gaussian noise (0.5 and 1.0 × robust SD) and movement-artefact drifts in 10 % or 25 % of epochs.](figures/fig5_robustness.png){width=100%}
