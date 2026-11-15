"""E10: computational cost per night (CPU wall-clock, single process) of
  (i)  the base stager (YASA feature extraction + LightGBM inference),
  (ii) the proposed uncertainty layer: calibration + FFBS sampling (M draws) + parameter computation,
  (iii) conformal interval construction (given calibration scores),
and the memory footprint of the sampled hypnogram array. 20 nights per cohort (first 20 by name).
Output: results/raw/e10_efficiency.csv
"""
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from e03_night_summaries import load_preds  # noqa: E402
from src.data import sleep  # noqa: E402
from src.evaluation.conformal_eval import evaluate, param_frame  # noqa: E402
from src.evaluation.sleep_params import compute_params  # noqa: E402
from src.models.yasa_stager import yasa_features_and_proba  # noqa: E402
from src.uncertainty import hmm  # noqa: E402
from src.uncertainty.night_summary import fit_source_model  # noqa: E402
from src.utils import RESULTS_DIR, cache_root, hardware_info, save_json  # noqa: E402


def main(n_per=20):
    import os
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    sc = load_preds("yasa", "SC")
    sm = fit_source_model([v[0] for v in sc.values()], [v[1] for v in sc.values()])
    # warm-up numba
    P0, y0 = next(iter(sc.values()))
    hmm.ffbs_sample(sm.cal.transform(np.log(P0 + 1e-12)), sm.pi_s, sm.A, sm.p0, sm.tau, 10, np.random.default_rng(0))
    rows = []
    for c in ["SC", "ST", "HMC"]:
        for p in sleep.cached_nights(cache_root(), c)[:n_per]:
            n = sleep.load_night(p)
            t0 = time.perf_counter()
            _, P, _ = yasa_features_and_proba(n)
            t_stager = time.perf_counter() - t0
            for M in (100, 300, 1000):
                t0 = time.perf_counter()
                Pc = sm.cal.transform(np.log(np.clip(P, 1e-12, 1)))
                S = hmm.ffbs_sample(Pc, sm.pi_s, sm.A, sm.p0, sm.tau, M, np.random.default_rng(1))
                t_ffbs = time.perf_counter() - t0
                t0 = time.perf_counter()
                compute_params(S, n.y >= 0)
                t_params = time.perf_counter() - t0
                rows.append(dict(cohort=c, night=n.night, n_epochs=n.n_epochs, M=M, t_stager_s=t_stager,
                                 t_ffbs_s=t_ffbs, t_params_s=t_params, samples_MB=S.nbytes / 1e6))
    df = pd.DataFrame(rows)
    # conformal step timing (LOSO-sized calibration set)
    summ = pd.read_csv(RESULTS_DIR / "summaries" / "yasa_xfit.csv")
    f = param_frame(summ[summ.cohort == "SC"], "TST")
    t0 = time.perf_counter()
    for _ in range(100):
        evaluate("TST", "norm_reg_ffbs", f.iloc[1:], f.iloc[:1], 0.10)
    t_conf = (time.perf_counter() - t0) / 100
    df.to_csv(RESULTS_DIR / "raw" / "e10_efficiency.csv", index=False)
    save_json({"hardware": hardware_info(), "t_conformal_per_night_s": t_conf,
               "summary": df.groupby("M")[["t_stager_s", "t_ffbs_s", "t_params_s", "samples_MB"]].median().to_dict()},
              RESULTS_DIR / "raw" / "e10_efficiency_meta.json")
    print(df.groupby("M")[["n_epochs", "t_stager_s", "t_ffbs_s", "t_params_s", "samples_MB"]].median())
    print("conformal step per night (s):", t_conf)


if __name__ == "__main__":
    main()
