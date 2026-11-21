"""Extract YASA stage probabilities for the Dreem Open Datasets (DOD-H, DOD-O; Guillot et al. 2020, Zenodo 10.5281/zenodo.15900394).

The recordings are streamed one at a time from the Zenodo zip files with parallel HTTP range requests (the two archives are 22 and 36 GB),
staged with the unchanged pretrained YASA classifier (C3-M2 EEG and EOG1-EOG2; resampled from 250 to 100 Hz; signals are stored in uV although
labelled mV), and only the probabilities and labels are kept: results/predictions/yasa/DODH|DODO/<record>.npz with
  P  (n_epochs x 5, order W, N1, N2, N3, R)   y  consensus hypnogram of the dataset (-1 = not scored)   ys  (5 x n_epochs) individual scorers.
Scorer hypnograms come from github.com/Dreem-Organization/dreem-learning-evaluation (folder scorers/<dodh|dodo>/scorer_k/<record>.json), cloned to
SCORERS_DIR; the first n_epochs of each scorer file are used (scorer files are up to ~30 epochs longer than the stored signals).
The DOD-O record without a consensus (5d8e93a5-d26a-436d-bc2c-e9527dc92cbf) is excluded, as in the original cohort of 55 patients.
Usage: python extract_dod.py [SCORERS_DIR] [TMP_DIR]    (about 1.5 h; resumable; needs h5py, remotezip, yasa, mne)
"""
import concurrent.futures as cf
import json
import os
import struct
import sys
import time
import traceback
import types
import zlib
from pathlib import Path

import h5py
import numpy as np
import pandas as pd
import requests
from remotezip import RemoteZip
from scipy.signal import resample_poly

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.models.yasa_stager import yasa_features_and_proba  # noqa: E402
from src.utils import RESULTS_DIR  # noqa: E402


URLS = {"dodh": "https://zenodo.org/api/records/15900394/files/dodh.zip/content",
        "dodo": "https://zenodo.org/api/records/15900394/files/dodo.zip/content"}

def members(ds):
    with RemoteZip(URLS[ds]) as z:
        return [(i.filename, i.header_offset, i.compress_size, i.file_size, i.compress_type) for i in z.infolist()
                if i.filename.endswith(".h5") and not i.filename.startswith("__MACOSX")]

def _range(url, s, e, tries=6):
    for k in range(tries):
        try:
            r = requests.get(url, headers={"Range": f"bytes={s}-{e}"}, timeout=180)
            if r.status_code == 206 and len(r.content) == e - s + 1:
                return r.content
        except Exception:
            pass
        time.sleep(2 * (k + 1))
    raise RuntimeError(f"range {s}-{e} failed")

def fetch_member(ds, name, hdr_off, csize, ctype, out_path, workers=12, chunk=24_000_000):
    url = URLS[ds]
    lh = _range(url, hdr_off, hdr_off + 29)
    nlen, elen = struct.unpack("<HH", lh[26:30])
    start = hdr_off + 30 + nlen + elen
    ranges = [(s, min(s + chunk, start + csize) - 1) for s in range(start, start + csize, chunk)]
    with cf.ThreadPoolExecutor(workers) as ex:
        parts = list(ex.map(lambda r: _range(url, *r), ranges))
    d = zlib.decompressobj(-15) if ctype == 8 else None
    with open(out_path, "wb") as f:
        for p in parts:
            f.write(d.decompress(p) if d else p)
        if d:
            f.write(d.flush())


def stage_record(h5path, eeg_name="C3_M2"):
    with h5py.File(h5path, "r") as f:
        cons = f["hypnogram"][:].astype(np.int8)
        n = len(cons)
        fs = int(f["signals/eeg"].attrs["fs"])
        eeg = f[f"signals/eeg/{eeg_name}"][: n * 30 * fs].astype(np.float64)
        eog = (f["signals/eog/EOG1"][: n * 30 * fs].astype(np.float64) - f["signals/eog/EOG2"][: n * 30 * fs].astype(np.float64))
        rid = f.attrs["record_id"].decode() if isinstance(f.attrs["record_id"], bytes) else str(f.attrs["record_id"])
    up, down = 100, fs
    g = np.gcd(up, down); up //= g; down //= g
    eeg100 = resample_poly(eeg, up, down)            # signals are already in uV (std ~20)
    eog100 = resample_poly(eog, up, down)
    m = n * 3000
    eeg100, eog100 = eeg100[:m], eog100[:m]
    night = types.SimpleNamespace(eeg=eeg100, eog=eog100, n_epochs=n)
    F, P, _ = yasa_features_and_proba(night)
    return P.astype(np.float32), cons, rid


SC = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("dreem-learning-evaluation/scorers")
TMP = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("dod_tmp")
TMP.mkdir(exist_ok=True)
SKIP = {"5d8e93a5-d26a-436d-bc2c-e9527dc92cbf"}
OUT = {"dodh": "DODH", "dodo": "DODO"}
meta_path = RESULTS_DIR / "predictions" / "yasa" / "dod_meta.csv"
def jobs():
    for ds in ("dodh", "dodo"):
        for (name, off, cs, fs, ct) in members(ds):
            stem = Path(name).stem
            if stem in SKIP: continue
            yield ds, stem, name, off, cs, ct

def fetch(j):
    ds, stem, name, off, cs, ct = j
    p = TMP / f"{stem}.h5"
    t = time.time(); fetch_member(ds, name, off, cs, ct, p)
    return p, time.time() - t

def main():
    todo = []
    for j in jobs():
        ds, stem = j[0], j[1]
        d = RESULTS_DIR / "predictions" / "yasa" / OUT[ds]; d.mkdir(parents=True, exist_ok=True)
        if not (d / f"{stem}.npz").exists(): todo.append(j)
    print(len(todo), "recordings to process", flush=True)
    rows = pd.read_csv(meta_path).to_dict("records") if meta_path.exists() else []
    ex = cf.ThreadPoolExecutor(1)
    nxt = ex.submit(fetch, todo[0]) if todo else None
    for i, j in enumerate(todo):
        ds, stem = j[0], j[1]
        try:
            p, dl = nxt.result()
            nxt = ex.submit(fetch, todo[i + 1]) if i + 1 < len(todo) else None
            t = time.time()
            P, y, rid = stage_record(p)
            n = len(y)
            ys = np.full((5, n), -1, np.int8); lens = []
            for s in range(5):
                a = np.array(json.load(open(SC / ds / f"scorer_{s+1}" / f"{stem}.json")), dtype=np.int8)
                lens.append(len(a)); m = min(n, len(a)); ys[s, :m] = a[:m]
            np.savez_compressed(RESULTS_DIR / "predictions" / "yasa" / OUT[ds] / f"{stem}.npz", P=P, y=y, ys=ys)
            rows.append(dict(dataset=ds, night=stem, record_id=rid, n_epochs=n, n_unscored_consensus=int((y < 0).sum()), scorer_lens=json.dumps(lens)))
            pd.DataFrame(rows).to_csv(meta_path, index=False)
            os.remove(p)
            print(f"[{i+1}/{len(todo)}] {ds} {stem} n={n} dl={dl:.0f}s proc={time.time()-t:.0f}s acc={(P.argmax(1)[y>=0]==y[y>=0]).mean():.3f}", flush=True)
        except Exception:
            print("FAILED", ds, stem, traceback.format_exc()[-600:], flush=True)
    print("ALL DONE", flush=True)

if __name__ == "__main__":
    main()
