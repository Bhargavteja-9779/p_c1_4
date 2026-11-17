# Reviewer 5 — Dataset validity & leakage (cycle 1)

## Summary of the submission (3-5 sentences)
The authors turn epoch probabilities from YASA (pretrained) and an in-domain LightGBM into per-night conformal intervals for eight PSG parameters. They evaluate these on Sleep-EDF SC (153 nights/78 subjects), Sleep-EDF ST (44/22) and HMC (151/151), with windows taken from lights-off metadata. I checked loaders, cache, folds, cross-fitting, raw hypnograms and the dataset/YASA documentation.

The core leakage controls are sound:
- Every split is grouped by subject (e02/e03 folds, e04 `subject_split` and LOSO, e06 `pick_subjects`, e09, e11, CQR half-split).
- All 197 Sleep-EDF windows reproduce exactly from the hypnograms plus `SC-subjects.xls`/`ST-subjects.xls`.
- The HMC windows reproduce the released aggregate TIB 7.6 (1.2) h, TST 6.3 h and SE 83 %; I computed 7.55 ± 1.24 h, 6.27 ± 1.46 h and 83.1 %.
- YASA's pretrained classifier does not overlap with the study cohorts. Vallat & Walker (eLife 2021) trained it on 3,163 nights from CCSHS, CFS, CHAT, HomePAP, MESA, MrOS and SHHS, and tested it on 585 held-out NSRR nights and 75 Dreem (DOD) nights; Sleep-EDF and HMC appear nowhere.
- The installed model is `clf_eeg+eog_lgb_0.5.0`. The YASA 0.5.0 changelog dates it to the post-review eLife version, so the "external stager" claim holds.

The remaining problems are a reference-derived mask applied to the automatic hypnograms, a confounded cross-cohort shift, and SC metadata/window artefacts.

## Fatal concerns
None.

## Critical/Major concerns

**M1. A reference-label mask is applied to automatic and sampled hypnograms, so the windows are not label-free.**
- **Where:** `night_summary.summarise_night` sets `mask = y >= 0` and passes it to `compute_params` for the plug-in, the calibrated plug-in, FFBS and the independent-sampling hypnograms. `load_sleepedf_night`/`load_hmc_night` also truncate at `scored[-1]+1`.
- **Effect at sleep onset (ST):** in 8 of 44 ST nights the hypnogram has an unannotated run of 7–43 epochs that ends exactly at the reference sleep onset (ST7041, 7042, 7051, 7161, 7201, 7202, 7241, 7242). The automatic SOL therefore cannot precede the reference onset.
  - For ST7041, the YASA plug-in SOL is 9.5 min with the mask and 6.5 min without it; the reference is 9.0 min.
- **Effect within the night (SC):** SC4762 has 144 masked epochs. Automatic TST is 245.5 min with the mask and 278 min without it.
- **Effect at the window end:** SC4592 and SC4772 are cut at the scorer's last annotated epoch, not at a metadata-defined time.
- **Why it matters:** this contradicts §2.2 ("fixed from metadata only") and the audit row "Label leakage via unscored epochs". It also cannot be reproduced in deployment, where no reference mask exists. It persists in the new E12, which calls `summarise_night`.
- **Likely size:** small (only ST7041 changed for the YASA plug-in), but it is unquantified for the FFBS samples.
- **Action:**
  1. Compute every automatic parameter on all window epochs.
  2. Apply reference exclusions to the reference only, or treat unannotated pre-onset epochs as W.
  3. Re-run E04, E06 and E12 as a sensitivity analysis and report the counts above.
  4. Correct §2.2 and the audit.

**M2. The SC→HMC "transportability" result confounds scoring manual, montage and population, and the montage statement is wrong for YASA.**
- **Scoring manual:** SC/ST were scored by R&K on Fpz-Cz/Pz-Oz (PhysioNet); HMC was scored by AASM v2.4. The YASA N3 bias reverses from +5.9 percentage points (pp) on SC to −4.8 pp on HMC. Moser et al. (Sleep 2009;32:139) found that AASM scores more N3 than R&K S3+S4 (+9 min) and less N2, which is the direction expected from a change of label definition. §3.5 instead calls the reversal something "no interval calibrated on SC can anticipate".
- **Montage:** §3.5 and Table 1 say only LightGBM "additionally faced a montage change". YASA's inputs also change, from Fpz-Cz plus bipolar horizontal EOG to C4-M1/E1-M2, and its SC/ST inputs are outside YASA's documented preference (central EEG; left EOG referenced to the mastoid).
- **Unused controls:** F4-M1 and E1-E2 were cached "for montage analyses" (`sleep.py` docstring; audit table), but no experiment reads `eeg2`/`eog2` (grep of `experiments/`).
- **Action:**
  1. Re-stage HMC with F4-M1 + E1-E2 for both stagers (about 1.4 s per night) and report the N3/TST bias and the source-only coverage.
  2. In §2.1/§3.5/§4, describe SC→HMC as a combined label-definition, montage, era and age shift, and cite Moser 2009.

**M3. SC lights-off metadata and the fixed 10-h window produce artefactual parameter values (not acknowledged).**
- **Asleep at lights-off:** 9 of 153 SC windows begin in sleep, so reference SOL = 0 (SC4121, 4332, 4482, 4612, 4621, 4622, 4651, 4711, 4811). SC4612 begins in REM, giving a reference REML of 0 min, a spurious SOREMP. SC4651 has REML 4 min after 119.5 min of pre-lights-off sleep.
- **Sleep before lights-off:** 48 nights contain reference sleep before lights-off, and in 12 the first sleep is ≤60 min before it.
- **Truncated sleep at the window end:** 7 windows end in sleep, truncating the main sleep period by up to 118.5 min (SC4191 118.5, SC4192 85, SC4501 40, SC4621 39.5, SC4771 25 min). 15 nights have sleep within 2 h after the window.
- **Long morning wake:** wake after the final awakening has median 116.5 min (IQR 73–154), and 72 nights exceed 120 min. This inflates SC W % (31.4 %) and accuracy/κ relative to the literature, and drives the SC WASO failure (width 230.6 min).
- **Why it matters:** SC values are window-defined, not clinical, yet SC is the source for all transport analyses.
- **Action:**
  1. Report these counts.
  2. Run a sensitivity analysis excluding nights that are asleep at lights-off or at the window end.
  3. Add a deployable, label-free end rule (e.g. the stager's own final awakening + 30 min, or an 8–9 h window).
  4. Flag SC WASO in Table 2.

## Moderate concerns

**Mo1. The ethics statement is inaccurate.**
- "The original studies obtained the approvals and consents described in their data descriptors [kemp2000; alvarez2021]": Kemp 2000 (IEEE TBME) is a methods paper and not a data descriptor, and the PhysioNet Sleep-EDF page states no ethics approval.
- For HMC, reuse was approved by METC Zuid-West Holland (METC-19-065) with consent waived, according to PhysioNet and Alvarez-Estevez & Rijsman 2021, so "consents" is wrong.
- The licences are correct: ODC-By 1.0 for Sleep-EDF and CC BY 4.0 for HMC (local `LICENSE.txt`).
- **Action:** state exactly what is documented per dataset, give the HMC approval number, and state the authors' own institutional determination.

**Mo2. Several dataset descriptions are inaccurate.**
- **Table 1, HMC:** age and sex are shown as "not released", but `data_raw/hmc/Subjects_info_aggregated.txt` gives 85 M/66 F, age 53.9 ± 15.4 and AHI 14.6 ± 16.9. Report these, and the AHI to characterise the clinical case mix.
- **HMC recordings:** HMC includes both in-hospital and ambulatory recordings, and patients were "randomly selected" (PhysioNet). The audit's "Consecutive" and the text's implied in-lab-only setting are wrong.
- **HMC version:** state v1.1, which has 151 recordings after SN014, SN064 and SN135 were removed.
- **Undocumented assumptions:** neither source documents "one scorer per night" (audit; Limitation iii) or one HMC recording per patient (the PLoS paper reports 154 recordings and no patient count). Both underpin subject grouping and the scorer-noise interpretation, so label them as assumptions.
- **YASA description:** "several thousand NSRR recordings" should read 3,163 nights from seven NSRR cohorts, and the classifier file (0.5.0) should be named.
- **Ages:** Table 1 ages are per night. Per subject, SC is 58.8 ± 22.1.

## Minor concerns

**Mi1. HMC data quality is not reported.**
- In 69 of 151 HMC windows lights-on occurs during sleep, so the final awakening is unobserved.
- 5 nights have TIB < 5 h (SN033, SN054, SN062, SN130, SN150). SN062 has 465 of 467 epochs asleep and 50 % N3, so it is likely truncated or atypical.
- SN112 has no REM; its correct exclusion from REML should be stated.
- **Action:** report these, and run a sensitivity analysis excluding TIB < 5 h.

**Mi2. Point-estimate claims (partly fixed by E12).**
- Table 3 "calibrated plug-in" still comes from xfit models fitted on about 4/5 of each cohort (about 121 HMC nights).
- E12 now shows that 10 local HMC nights give a calibrated plug-in TST bias of −3.8 min (MAE 20.7 min).
- **Action:** base the claims "a few locally scored nights" (Discussion, Conclusion, Highlights) on E12, not xfit.

**Mi3. Wording of the "external" claim.** It applies to YASA's weights only. Every interval component in the main analyses is fitted in-cohort, and the external transfer failed on HMC, so qualify the title phrase "with external validation".

**Mi4. Two audit rows overstate what was done.**
- "File-level uniqueness checked via SHA256 manifests": checksums verify integrity, not the absence of duplicates.
- "cached for montage analyses": no such analysis exists (see M2).

## Required additional experiments/analyses
1. Parameters without the reference mask on automatic and sampled hypnograms, re-running E04/E06/E12 (M1).
2. Montage-matched HMC (F4-M1 + E1-E2), both stagers: bias and source-only coverage (M2).
3. SC sensitivity analyses: exclude nights asleep at lights-off or at the window end, and apply a label-free automatic end rule (M3).
4. HMC sensitivity analysis excluding TIB < 5 h (Mi1).

## Recommendation
**Major revision.** Subject-level leakage is well controlled and the "external pretrained stager" status of YASA is verified. However:
- a reference-derived mask leaks label information into the automatic parameters;
- the headline transport failure is attributed without disentangling a known R&K→AASM label shift and a montage change that the text misstates;
- SC metadata and window artefacts (spurious SOL = 0 and REML = 0, truncated sleep, about 2 h of morning wake) shape the source cohort.

All four requested analyses are cheap.

```json
[
 {"id":"M1","severity":"major","title":"Reference-label mask applied to automatic/sampled hypnograms; windows truncated at last scored epoch","location":"code/src/uncertainty/night_summary.py summarise_night (mask=y>=0); code/src/data/sleep.py e1=min(...,scored[-1]+1); Methods 2.2; S_data_and_leakage_audit row 'Label leakage via unscored epochs'; also E12","evidence":"8/44 ST nights (ST7041,7042,7051,7161,7201,7202,7241,7242) have unannotated runs (7-43 epochs) ending exactly at reference sleep onset; ST7041 YASA plug-in SOL 9.5 masked vs 6.5 unmasked (ref 9.0); SC4762 automatic TST 245.5 masked vs 278 unmasked; SC4592/SC4772 truncated at scorer's last epoch","action":"Compute automatic parameters on all window epochs; apply exclusions to reference only (or code unannotated pre-onset epochs as W); rerun E04/E06/E12 sensitivity; correct 2.2 and audit","needs_experiment":true},
 {"id":"M2","severity":"major","title":"SC->HMC transfer confounds R&K vs AASM labels and montage (also for YASA); montage controls unused","location":"Results 3.5; Table 1/2.3; code/src/data/sleep.py (eeg2/eog2 never used in experiments/)","evidence":"N3 bias +5.9 pp (SC, R&K on Fpz-Cz) vs -4.8 pp (HMC, AASM v2.4) matches Moser 2009 (AASM N3 +9 min vs R&K S3+S4); YASA input changes Fpz-Cz/bipolar hEOG -> C4-M1/E1-M2 but text says only LightGBM faced a montage change; grep shows no experiment uses F4-M1/E1-E2","action":"Re-stage HMC with F4-M1+E1-E2 for both stagers, report N3/TST bias and source-only coverage; describe shift as label-definition+montage+population; cite Moser 2009","needs_experiment":true},
 {"id":"M3","severity":"major","title":"SC lights-off metadata and fixed 10-h window create artefactual parameters","location":"Methods 2.2; code/src/data/sleep.py load_sleepedf_night; Tables 1-3 SC rows","evidence":"9/153 SC windows start in sleep (SOL=0; SC4612 starts in REM -> REML 0, SC4651 REML 4); 48 nights with sleep before lights-off; 7 windows end in sleep truncating up to 118.5 min (SC4191); 15 with sleep within 2 h after window; post-final-awakening wake median 116.5 min (IQR 73-154), 72 nights >120 min; SC W% 31.4","action":"Report counts; sensitivity excluding sleep-at-lights-off/sleep-at-window-end nights; label-free automatic end rule or 8-9 h window; flag SC WASO","needs_experiment":true},
 {"id":"Mo1","severity":"moderate","title":"Ethics statement inaccurate","location":"Ethics statement; Methods 2.1","evidence":"Kemp 2000 is a methods paper, PhysioNet Sleep-EDF gives no ethics info; HMC reuse approved by METC Zuid-West Holland METC-19-065 with consent waived (PhysioNet; PLoS ONE 2021)","action":"State documented approvals per dataset incl. METC-19-065 and consent waiver; give authors' institutional determination","needs_experiment":false},
 {"id":"Mo2","severity":"moderate","title":"Dataset descriptions inaccurate/unsupported","location":"Table 1; Methods 2.1/2.3; Limitations (iii),(v); S_data_and_leakage_audit","evidence":"Subjects_info_aggregated.txt (downloaded) gives 85M/66F, age 53.9+/-15.4, AHI 14.6+/-16.9 but Table 1 says 'not released'; HMC mixes in-hospital and ambulatory, randomly selected (audit says consecutive); v1.1 removed SN014/SN064/SN135; single scorer and one recording per HMC patient undocumented; YASA trained on 3,163 nights (not 'several thousand'), classifier 0.5.0; ages per night","action":"Correct Table 1 and text; state version, setting and assumptions; name YASA classifier version and training cohorts","needs_experiment":false},
 {"id":"Mi1","severity":"minor","title":"HMC data-quality characteristics unreported","location":"Results 3.1; Table 1","evidence":"69/151 windows end in sleep (lights-on during sleep); 5 nights TIB<5 h (SN033,SN054,SN062,SN130,SN150); SN062 465/467 epochs asleep, 50% N3; SN112 no REM","action":"Report; sensitivity excluding TIB<5 h","needs_experiment":true},
 {"id":"Mi2","severity":"minor","title":"'Few local nights correct bias' must rest on E12, not xfit Table 3","location":"Table 3; Discussion; Conclusion; Highlights","evidence":"Table 3 calibrated plug-in from xfit (~121 HMC nights); E12 local n=10 gives HMC TST bias -3.8 min, MAE 20.7","action":"Report E12 local results as evidence for the few-night claim; label Table 3 calibration size","needs_experiment":false},
 {"id":"Mi3","severity":"minor","title":"'External validation' wording","location":"Title; 2.3; Abstract","evidence":"YASA weights external (verified: NSRR CCSHS/CFS/CHAT/HomePAP/MESA/MrOS/SHHS train; NSRR holdout+DOD test), but all interval components fitted in-cohort; external transfer failed on HMC","action":"Qualify the external claim in title and text","needs_experiment":false},
 {"id":"Mi4","severity":"minor","title":"Audit table overstates checks","location":"supplementary/S_data_and_leakage_audit.md","evidence":"SHA256 verifies integrity, not uniqueness; 'cached for montage analyses' but none run","action":"Rephrase or perform the checks","needs_experiment":false}
]
```
