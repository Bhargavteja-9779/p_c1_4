# Per-night conformal prediction intervals for automatically scored PSG parameters

Code accompanying the manuscript *"Distribution-free per-night prediction intervals for automatically
scored polysomnography: structured posterior sampling, conformal calibration and external validation"*
(submitted to *Sleep Medicine*).

Automatic sleep stagers output an epoch-by-epoch hypnogram, while clinical decisions use night-level
parameters (TST, SOL, WASO, REM latency, stage percentages). This repository turns the epoch
probabilities of **any** stager into a **per-night interval for each parameter** with finite-sample
coverage under exchangeability:

1. calibrate epoch probabilities (bias-corrected temperature scaling);
2. treat them as scaled likelihoods in a hidden Markov model of stage transitions and draw whole
   hypnograms by **forward-filtering backward-sampling (FFBS)**;
3. compute every parameter on every sampled hypnogram -> per-night posterior mean and SD;
4. **conformalise** the normalised residual |ref − mean| / (SD + median SD) on labelled calibration nights.

## Installation
```bash
conda env create -f environment.yml && conda activate psg-conformal   # or:
pip install -r requirements.txt
```
Tested with Python 3.13 on Linux, 4 CPU cores, 15 GB RAM, no GPU (hardware is auto-detected; nothing
requires CUDA or Apple MPS). Exact versions used are in `requirements.txt`.

## Data
All data are public (PhysioNet open access):
* Sleep-EDF Expanded v1.0.0 — https://doi.org/10.13026/C2X676 (ODC-By 1.0)
* HMC Sleep Staging Database v1.1 — https://doi.org/10.13026/t79q-fr32 (CC BY 4.0)
```bash
bash scripts/download_data.sh            # ~24 GB into code/data/raw (checksums verified)
python scripts/build_sleep_cache.py      # analysis windows + channels -> code/data/cache (≈7 GB)
```
Set `LSA_DATA_ROOT` / `LSA_CACHE_ROOT` to use other locations. Raw EDFs may be deleted after caching
(`--delete-raw-hmc`).

## Reproduce everything
```bash
python run_all.py --mode quick --skip-cache   # ~10 min pipeline check -> ../results_quick/
python run_all.py --mode full  --skip-cache   # full study -> ../results/, ../tables/, ../figures/
```
Every number in the manuscript is read from machine-generated files in `../results`, `../tables`
(`manuscript_numbers.json`) — nothing is typed by hand.

| step | script | output |
|---|---|---|
| E01 | `experiments/e01_features_yasa.py` | YASA features; pretrained-YASA epoch probabilities |
| E02 | `experiments/e02_indomain_lgbm.py` | in-domain LightGBM stager (subject-grouped 5-fold on SC; seeds 0–2) |
| E03 | `experiments/e03_night_summaries.py` | per-night FFBS summaries (`results/summaries`) |
| E04 | `experiments/e04_within_cohort.py` | 500 subject-grouped calibration/test splits + LOSO |
| E06 | `experiments/e06_cross_cohort.py` | SC→ST/HMC transfer; few-night target recalibration |
| E07 | `experiments/e07_utility_and_stats.py` | Wilcoxon/Holm, cluster bootstrap, AUROC, Bland–Altman, ICC |
| E09 | `experiments/e09_robustness.py` | robustness to EEG/EOG corruption |
| E10 | `experiments/e10_efficiency.py` | run time and memory |
| – | `scripts/make_tables.py`, `scripts/make_figures.py` | tables (CSV/Markdown) and figures (PNG/PDF) |

## Using the method on your own stager
```python
from src.uncertainty.night_summary import fit_source_model, summarise_night
sm = fit_source_model(list_of_P_train, list_of_y_train)       # labelled nights (P: n_epochs x 5, W,N1,N2,N3,R)
rec = summarise_night(P_new, y_dummy_or_minus1, sm, "night_id", "tag")   # FFBS summaries per parameter
# then src.evaluation.conformal_eval.make_interval("norm_reg_ffbs", cal_frame, test_frame, alpha=0.10)
```

## Tests
```bash
python -m pytest -q tests
```

## Design safeguards
Subject-grouped splitting everywhere; label-free analysis windows; HMM parameters never fitted on the
evaluated night; pre-registered protocol (`../supplementary/PREREGISTERED_PROTOCOL.md`) and change log
(`../../CHANGELOG.md`).

## Licence
Code: MIT. YASA pretrained classifiers are distributed with the `yasa` package (BSD-3-Clause).
