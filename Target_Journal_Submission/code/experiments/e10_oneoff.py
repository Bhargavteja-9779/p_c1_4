"""E10 (one-off part only): one-off costs of the uncertainty layer that need no raw recordings.

Source-model fit (cold, with Numba JIT, and warm), first FFBS call (JIT), and peak memory for a 7 x 24 h recording
(M = 100 and 1000). Uses the stored YASA probabilities of the SC nights. Merges the result into
results/raw/e10_efficiency_meta.json (key "one_off") without touching the per-night timings of e10_efficiency.py,
which require the raw PSG files.
"""
import json
import os
import sys
import time
import tracemalloc
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("NUMBA_NUM_THREADS", "1")
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from e03_night_summaries import load_preds  # noqa: E402
from src.evaluation.sleep_params import compute_params  # noqa: E402
from src.uncertainty import hmm  # noqa: E402
from src.uncertainty.night_summary import fit_source_model  # noqa: E402
from src.utils import RESULTS_DIR, hardware_info  # noqa: E402


def main():
    sc = load_preds("yasa", "SC")
    X, Y = [v[0] for v in sc.values()], [v[1] for v in sc.values()]
    one_off = {}
    t0 = time.perf_counter(); sm = fit_source_model(X, Y); one_off["fit_source_model_incl_jit_s"] = time.perf_counter() - t0
    t0 = time.perf_counter(); fit_source_model(X, Y); one_off["fit_source_model_warm_s"] = time.perf_counter() - t0
    one_off["n_source_nights"] = len(sc)
    P0 = X[0]
    t0 = time.perf_counter()
    hmm.ffbs_sample(sm.cal.transform(np.log(P0 + 1e-12)), sm.pi_s, sm.A, sm.p0, sm.tau, 10, np.random.default_rng(0))
    one_off["ffbs_first_call_incl_jit_s"] = time.perf_counter() - t0
    T = 7 * 2880
    Plong = np.tile(P0, (T // len(P0) + 1, 1))[:T]
    for M in (100, 1000):
        tracemalloc.start()
        Pc = sm.cal.transform(np.log(np.clip(Plong, 1e-12, 1)))
        S = hmm.ffbs_sample(Pc, sm.pi_s, sm.A, sm.p0, sm.tau, M, np.random.default_rng(2))
        compute_params(S)
        one_off[f"peak_MB_7x24h_M{M}"] = tracemalloc.get_traced_memory()[1] / 1e6
        tracemalloc.stop(); del S
    f = RESULTS_DIR / "raw" / "e10_efficiency_meta.json"
    meta = json.loads(f.read_text())
    meta["one_off"] = one_off
    meta["one_off_hardware"] = hardware_info()
    f.write_text(json.dumps(meta, indent=1))
    print(json.dumps(one_off, indent=1))


if __name__ == "__main__":
    main()
