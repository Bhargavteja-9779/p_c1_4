"""ECG heartbeat datasets (MIT-BIH Arrhythmia, St Petersburg INCART, MIT-BIH Supraventricular).

Protocol (fixed before any test-set evaluation):
* Lead: MLII (mitdb), II (incartdb), ECG1 (svdb).
* Zero-phase 2nd-order Butterworth band-pass 0.5-40 Hz at native rate, then polyphase resampling
  to a common 128 Hz (the lowest native rate among the three databases, svdb).
* Beats are taken at the reference-annotation R-peak positions (standard practice for beat
  classification; detection errors are out of scope).
* AAMI EC57 mapping: N={N,L,R,e,j,n,B}, S={A,a,J,S}, V={V,E}, F={F}; Q-class and non-beat
  annotations are excluded from classification but beat annotations of all types are used to
  compute RR intervals.
* MIT-BIH paced records 102, 104, 107, 217 are excluded (AAMI recommendation).
* Inter-patient split of de Chazal et al. (2004): DS1 (training) / DS2 (testing).
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
from scipy import signal

CLASSES = ["N", "S", "V", "F"]
AAMI_MAP = {**{s: 0 for s in "NLRejnB"}, **{s: 1 for s in "AaJS"}, **{s: 2 for s in "VE"}, "F": 3}
BEAT_SYMBOLS = set("NLRejnBAaJSVEFQ/f")  # all beat-type annotations (for RR computation)
FS = 128
PRE_S, POST_S = 0.25, 0.45
N_PRE, N_POST = int(round(PRE_S * FS)), int(round(POST_S * FS))
WIN = N_PRE + N_POST  # 90 samples

DS1 = ["101", "106", "108", "109", "112", "114", "115", "116", "118", "119", "122", "124",
       "201", "203", "205", "207", "208", "209", "215", "220", "223", "230"]
DS2 = ["100", "103", "105", "111", "113", "117", "121", "123", "200", "202", "210", "212",
       "213", "214", "219", "221", "222", "228", "231", "232", "233", "234"]
PACED = ["102", "104", "107", "217"]
LEAD = {"mitdb": "MLII", "incartdb": "II", "svdb": "ECG1"}


@dataclass
class RecordBeats:
    db: str
    record: str
    subject: str           # subject identifier (INCART: several records per subject)
    beats: np.ndarray      # (n, WIN) float32, amplitude-normalised waveform
    rr: np.ndarray         # (n, 4) [pre, post, local, average] RR in seconds
    y: np.ndarray          # (n,) int AAMI label 0..3
    t: np.ndarray          # (n,) R-peak time (s)


def records_for(db: str, root: Path) -> list[str]:
    recs = (root / db / "RECORDS").read_text().split()
    if db == "mitdb":
        recs = [r for r in recs if r not in PACED]
    return recs


def subject_of(db: str, record: str, root: Path) -> str:
    """INCART's 75 records were extracted from 32 Holter recordings; each header comment carries
    an explicit "patient <k>" field which we use as the subject identifier (needed for
    subject-level statistics). Other databases: one record = one subject.
    """
    if db != "incartdb":
        return f"{db}:{record}"
    import re
    import wfdb
    h = wfdb.rdheader(str(root / db / record))
    txt = " ".join(h.comments or [])
    m = re.search(r"patient\s+(\d+)", txt)
    if m is None:
        raise ValueError(f"no patient id in header of {record}")
    return f"{db}:patient{int(m.group(1)):02d}"


def _bandpass(x: np.ndarray, fs: float) -> np.ndarray:
    b, a = signal.butter(2, [0.5, 40.0], btype="bandpass", fs=fs)
    return signal.filtfilt(b, a, x)


def load_record(db: str, record: str, root: Path) -> RecordBeats:
    import wfdb
    path = str(root / db / record)
    rec = wfdb.rdrecord(path)
    ann = wfdb.rdann(path, "atr")
    lead = LEAD[db]
    ch = rec.sig_name.index(lead)
    x = rec.p_signal[:, ch].astype(np.float64)
    x = np.nan_to_num(x)
    fs0 = float(rec.fs)
    x = _bandpass(x, fs0)
    # polyphase resampling to 128 Hz
    from fractions import Fraction
    frac = Fraction(FS / fs0).limit_denominator(1000)
    x = signal.resample_poly(x, frac.numerator, frac.denominator)
    scale = FS / fs0

    sym = np.array(ann.symbol)
    samp = np.asarray(ann.sample)
    is_beat = np.array([s in BEAT_SYMBOLS for s in sym])
    samp_b = np.round(samp[is_beat] * scale).astype(int)
    sym_b = sym[is_beat]
    t_b = samp_b / FS
    rr = np.diff(t_b)
    n = len(t_b)
    pre = np.r_[np.nan, rr]
    post = np.r_[rr, np.nan]
    pre[0] = pre[1] if n > 1 else 0.8
    post[-1] = post[-2] if n > 1 else 0.8
    # local RR: mean of the 10 RR intervals centred on the beat; average RR: 5-min centred window
    local = np.convolve(np.pad(pre, (5, 4), mode="edge"), np.ones(10) / 10, mode="valid")
    avg = np.empty(n)
    j0 = j1 = 0
    for i in range(n):
        while t_b[j0] < t_b[i] - 150.0:
            j0 += 1
        while j1 < n and t_b[j1] <= t_b[i] + 150.0:
            j1 += 1
        avg[i] = np.mean(pre[j0:j1])
    rr_feat = np.stack([pre, post, local, avg], axis=1)

    keep = np.array([s in AAMI_MAP for s in sym_b])
    keep &= (samp_b - N_PRE >= 0) & (samp_b + N_POST <= len(x))
    idx = np.where(keep)[0]
    seg = np.stack([x[s - N_PRE: s + N_POST] for s in samp_b[idx]]) if len(idx) else np.zeros((0, WIN))
    # per-beat baseline removal (median of window) and record-level robust amplitude scaling
    seg = seg - np.median(seg, axis=1, keepdims=True)
    amp = np.median(np.abs(seg[:, N_PRE - 3:N_PRE + 4]).max(axis=1)) if len(idx) else 1.0
    seg = seg / (amp + 1e-8)
    y = np.array([AAMI_MAP[s] for s in sym_b[idx]], dtype=np.int64)
    return RecordBeats(db=db, record=record, subject=subject_of(db, record, root),
                       beats=seg.astype(np.float32), rr=rr_feat[idx].astype(np.float32), y=y,
                       t=t_b[idx].astype(np.float32))


def load_db(db: str, root: Path, cache: Path, records: list[str] | None = None) -> list[RecordBeats]:
    """Load (with on-disk caching) all records of a database."""
    cache_file = cache / f"ecg_{db}.npz"
    if cache_file.exists():
        out = _from_cache(cache_file)
    else:
        out = [load_record(db, r, root) for r in records_for(db, root)]
        _to_cache(out, cache_file)
    if records is not None:
        keep = set(records)
        out = [r for r in out if r.record in keep]
    return out


def _to_cache(recs: list[RecordBeats], path: Path) -> None:
    d = {}
    for i, r in enumerate(recs):
        for k in ("beats", "rr", "y", "t"):
            d[f"{i}_{k}"] = getattr(r, k)
        d[f"{i}_meta"] = np.array([r.db, r.record, r.subject])
    np.savez_compressed(path, n=len(recs), **d)


def _from_cache(path: Path) -> list[RecordBeats]:
    z = np.load(path, allow_pickle=False)
    out = []
    for i in range(int(z["n"])):
        db, rec, subj = [str(s) for s in z[f"{i}_meta"]]
        out.append(RecordBeats(db, rec, subj, z[f"{i}_beats"], z[f"{i}_rr"], z[f"{i}_y"], z[f"{i}_t"]))
    return out


def handcrafted_features(r: RecordBeats) -> np.ndarray:
    """Feature vector per beat for the classical / GBDT models.

    RR block (8): pre, post, local, avg, pre/avg, post/avg, local/avg, pre/post.
    Morphology block (30 + 6): waveform decimated by 3, plus QRS-region energy, max, min,
    positive/negative area and an approximate QRS width (samples above 30% of peak |amplitude|).
    """
    pre, post, local, avg = r.rr.T
    rr = np.stack([pre, post, local, avg, pre / avg, post / avg, local / avg, pre / post], 1)
    b = r.beats
    dec = b[:, ::3]
    q = b[:, N_PRE - 10:N_PRE + 12]
    absq = np.abs(q)
    width = (absq > 0.3 * absq.max(axis=1, keepdims=True)).sum(1)
    morph = np.stack([(q ** 2).sum(1), q.max(1), q.min(1), np.clip(q, 0, None).sum(1),
                      np.clip(q, None, 0).sum(1), width], 1)
    return np.concatenate([rr, dec, morph], axis=1).astype(np.float32)
