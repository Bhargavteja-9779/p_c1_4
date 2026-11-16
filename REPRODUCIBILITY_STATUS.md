# REPRODUCIBILITY_STATUS

_Last update: 2026-11-16_

| Check | Status | Evidence |
|---|---|---|
| Public data, scripted download with checksums | OK | `code/scripts/download_data.sh` (PhysioNet S3 mirrors; SHA256 verified) |
| Data cache build | OK | `code/scripts/build_sleep_cache.py` (SC 153, ST 44, HMC 151 nights) |
| Pinned environment | OK | `code/requirements.txt`, `code/environment.yml` (Python 3.13; CPU only) |
| Deterministic seeds | OK | stager seeds 0/1/2; split seeds 0..R-1; per-night FFBS seeds = CRC32(night, tag); rerun of E03 reproduced all 273 numeric summary columns exactly (max abs diff 0.0) |
| Unit tests | OK | `python -m pytest -q tests` → 8 passed |
| One-command pipeline, quick mode | OK | `python run_all.py --mode quick --skip-cache` completed all 13 steps (~9 min, 4 CPUs) into `results_quick/` (isolated from full results) |
| One-command pipeline, full mode | OK (stepwise) | all steps were executed individually in this study (logs in `results/experiment_logs/`); full run ≈ 1.5–2.5 h on 4 CPUs |
| Manuscript numbers machine-generated | OK | `tables/manuscript_numbers.json` → `manuscript/build_manuscript.py` aborts on any missing number |
| Tables / figures / supplement generated from results | OK | `scripts/make_tables.py`, `make_figures.py`, `make_supplement.py` |
| Hardware detection | OK | `src/utils.get_device()` (CUDA → MPS → CPU); no GPU needed |
| Known non-determinism | Note | wall-clock timings (E10) vary with hardware/load; LightGBM uses 4 threads (results identical across reruns here) |
| External dependencies | Note | YASA 0.8.1 pretrained classifier (bundled with the package); LibreOffice + libreoffice-math and pandoc needed only to build DOCX/PDF |
