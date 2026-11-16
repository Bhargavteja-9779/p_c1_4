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
