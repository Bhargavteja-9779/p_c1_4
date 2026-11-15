"""Extract analysis windows + channels for all nights into a compact cache and a metadata table.

python scripts/build_sleep_cache.py --cohorts SC ST HMC [--delete-raw-hmc]
"""
import argparse
import os
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.data import sleep  # noqa: E402
from src.utils import cache_root, data_root  # noqa: E402


def _job(args):
    kind, payload, root, cache, delete_raw = args
    try:
        if kind == "edf":
            psg, hyp, cohort, meta = payload
            n = sleep.load_sleepedf_night(Path(root), psg, hyp, cohort, meta)
            extra = {"condition": meta.get("condition", "")}
        else:
            rec = payload
            n = sleep.load_hmc_night(Path(root), rec)
            extra = {"condition": ""}
            if delete_raw:
                os.remove(Path(root) / "hmc" / "recordings" / f"{rec}.edf")
        sleep.save_night(n, Path(cache))
        lab = n.y[n.y >= 0]
        return dict(cohort=n.cohort, subject=n.subject, night=n.night, age=n.age, sex=n.sex,
                    n_epochs=n.n_epochs, n_scored=int(len(lab)),
                    **{f"n_{s}": int((lab == i).sum()) for i, s in enumerate(sleep.STAGES)}, **extra)
    except Exception as e:  # report and continue; failures are logged, never silently dropped
        return {"error": f"{payload if kind != 'edf' else payload[0]}: {e!r}"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cohorts", nargs="+", default=["SC", "ST", "HMC"])
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--delete-raw-hmc", action="store_true")
    a = ap.parse_args()
    root, cache = data_root(), cache_root()
    jobs = []
    for c in a.cohorts:
        if c in ("SC", "ST"):
            for psg, hyp, meta in sleep.sleepedf_index(root, c):
                jobs.append(("edf", (psg, hyp, c, meta), str(root), str(cache), False))
        elif c == "HMC":
            for rec in sleep.hmc_index(root):
                jobs.append(("hmc", rec, str(root), str(cache), a.delete_raw_hmc))
    with ProcessPoolExecutor(a.workers) as ex:
        rows = list(ex.map(_job, jobs))
    errs = [r["error"] for r in rows if "error" in r]
    rows = [r for r in rows if "error" not in r]
    meta_path = cache / "sleep" / "nights.csv"
    new = pd.DataFrame(rows)
    if meta_path.exists():
        old = pd.read_csv(meta_path)
        old = old[~old.cohort.isin(new.cohort.unique())]
        new = pd.concat([old, new], ignore_index=True)
    new.sort_values(["cohort", "night"]).to_csv(meta_path, index=False)
    print(new.groupby("cohort").agg(nights=("night", "count"), subjects=("subject", "nunique"),
                                    epochs=("n_scored", "sum")))
    if errs:
        print("ERRORS:", *errs, sep="\n  ")


if __name__ == "__main__":
    main()
