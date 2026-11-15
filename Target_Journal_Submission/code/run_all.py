"""Reproduce the complete study.

  python run_all.py --mode quick   # pipeline check: few nights, few splits (~10 min on 4 CPUs)
  python run_all.py --mode full    # complete pre-registered analysis (~2-3 h on 4 CPUs, no GPU needed)

Steps (each is an independent script in experiments/ and can be re-run on its own):
  0  data cache   scripts/build_sleep_cache.py   (requires raw data; scripts/download_data.sh)
  1  E01          YASA features + pretrained-YASA probabilities
  2  E02          in-domain LightGBM stager (SC, subject-grouped 5-fold; seeds 0,1,2)
  3  E03          per-night FFBS posterior summaries (xfit, srcSC)
  4  E04          within-cohort conformal evaluation (R splits + LOSO)
  5  E06          cross-cohort transfer and few-night recalibration
  6  E07          paired tests, clinical utility, point estimates, subgroups
  7  E09          robustness to signal corruption
  8  E10          computational cost
  9  tables/figures (scripts/make_tables.py, scripts/make_figures.py) + manuscript numbers
In quick mode results are written to results_quick/ (via LSA_RESULTS_DIR) so that the full results used
by the manuscript are never overwritten.
"""
import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sh(cmd, log):
    print(f"\n>>> {' '.join(cmd)}", flush=True)
    t0 = time.time()
    with open(log, "a") as f:
        f.write(f"\n>>> {' '.join(cmd)}\n")
        f.flush()
        r = subprocess.run(cmd, cwd=HERE, stdout=f, stderr=subprocess.STDOUT)
    print(f"    exit={r.returncode}  {time.time() - t0:.0f}s", flush=True)
    if r.returncode != 0:
        sys.exit(f"step failed: {' '.join(cmd)} (see {log})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["quick", "full"], default="quick")
    ap.add_argument("--skip-cache", action="store_true", help="data cache already built")
    ap.add_argument("--from-step", type=int, default=0)
    a = ap.parse_args()
    py = [sys.executable, "-W", "ignore"]
    q = a.mode == "quick"
    if q:
        os.environ["LSA_RESULTS_DIR"] = str(HERE.parent / "results_quick")
    res = Path(os.environ.get("LSA_RESULTS_DIR", HERE.parent / "results"))
    (res / "experiment_logs").mkdir(parents=True, exist_ok=True)
    (res / "predictions").mkdir(parents=True, exist_ok=True)
    log = res / "experiment_logs" / f"run_all_{a.mode}.log"
    lim = ["--limit", "12"] if q else []
    R = ["--R", "20"] if q else []
    steps = [
        (0, py + ["scripts/build_sleep_cache.py"]),
        (1, py + ["experiments/e01_features_yasa.py"] + (["--limit", "12"] if q else [])),
        (2, py + ["experiments/e02_indomain_lgbm.py"] + (["--seeds", "0"] if q else [])),
        (3, py + ["experiments/e03_night_summaries.py"] + lim + (["--stagers", "yasa", "lgbm_sc_s0"] if q else [])),
        (4, py + ["experiments/e04_within_cohort.py"] + R + (["--stagers", "yasa", "lgbm_sc_s0"] if q else [])),
        (5, py + ["experiments/e06_cross_cohort.py"] + R),
        (6, py + ["experiments/e07_utility_and_stats.py"]),
        (7, py + ["experiments/e09_robustness.py"] + (["--R", "20", "--cohorts", "HMC"] if q else [])),
        (8, py + ["experiments/e10_efficiency.py"]),
        (9, py + ["scripts/make_tables.py"]),
        (10, py + ["scripts/make_figures.py"]),
    ]
    for k, cmd in steps:
        if k < a.from_step or (k == 0 and a.skip_cache):
            continue
        sh(cmd, log)
    print(f"\nDone. Results in {res}")


if __name__ == "__main__":
    main()
