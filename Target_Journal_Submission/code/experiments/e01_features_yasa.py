"""E01: YASA features + pretrained-YASA epoch probabilities for every cached night.

Outputs
  data/cache/features/<cohort>/<night>.npz : X (n x 116, float32), y, feature names
  results/predictions/yasa/<cohort>/<night>.npz : P (n x 5), y
Channel configuration per cohort (pre-specified):
  SC/ST: EEG Fpz-Cz, EOG horizontal.  HMC: EEG C4-M1, EOG E1-M2 (YASA's recommended montage).
"""
import argparse
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.data import sleep  # noqa: E402
from src.models.yasa_stager import yasa_features_and_proba  # noqa: E402
from src.utils import RESULTS_DIR, cache_root  # noqa: E402


def _job(p):
    p = Path(p)
    n = sleep.load_night(p)
    F, P, names = yasa_features_and_proba(n)
    fdir = cache_root() / "features" / n.cohort
    pdir = RESULTS_DIR / "predictions" / "yasa" / n.cohort
    fdir.mkdir(parents=True, exist_ok=True)
    pdir.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(fdir / f"{n.night}.npz", X=F.values.astype(np.float32), y=n.y,
                        names=np.array(F.columns.tolist()))
    np.savez_compressed(pdir / f"{n.night}.npz", P=P.astype(np.float32), y=n.y)
    m = n.y >= 0
    return n.cohort, n.night, float(np.mean(P[m].argmax(1) == n.y[m]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cohorts", nargs="+", default=["SC", "ST", "HMC"])
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--limit", type=int, default=0, help="quick mode: nights per cohort")
    a = ap.parse_args()
    paths = []
    for c in a.cohorts:
        ps = sleep.cached_nights(cache_root(), c)
        paths += [str(p) for p in (ps[:a.limit] if a.limit else ps)]
    with ProcessPoolExecutor(a.workers) as ex:
        out = list(ex.map(_job, paths, chunksize=2))
    for c in a.cohorts:
        acc = [x[2] for x in out if x[0] == c]
        print(f"{c}: {len(acc)} nights, mean per-night accuracy (YASA pretrained) = {np.mean(acc):.3f}")


if __name__ == "__main__":
    main()
