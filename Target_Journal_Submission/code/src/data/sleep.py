"""Polysomnography cohorts: Sleep-EDF Expanded (SC, ST) and Haaglanden Medisch Centrum (HMC).

Pre-specified, label-free analysis windows (no ground-truth hypnogram information is used):
  * SC  (ambulatory 20-h home recordings with daytime naps): [lights-off, lights-off + 10 h]
        (truncated at recording end); lights-off from SC-subjects.xls.
  * ST  (in-hospital nights): [lights-off, end of recording]; lights-off from ST-subjects.xls.
  * HMC (clinical PSG): [annotated "Lights off", annotated "Lights on"].
Window boundaries are snapped to the 30-s scoring grid.  Stage mapping (AASM): W=0, N1=1, N2=2,
N3=3 (R&K S3+S4), REM=4; "Movement time" and "Sleep stage ?" are marked -1 (unscored) and are
excluded from parameter computation for both reference and automatic hypnograms.

Signals cached per night at 100 Hz (float16, microvolts):
  eeg  : SC/ST Fpz-Cz;  HMC C4-M1 (the derivation recommended for YASA)
  eeg2 : SC/ST Pz-Oz;   HMC F4-M1 (frontal, closest available analogue of Fpz-Cz)
  eog  : SC/ST horizontal EOG (bipolar); HMC E1-M2 (single-ended, as used by YASA)
  eog2 : HMC E1-E2 bipolar (horizontal analogue); SC/ST copy of eog
"""
from __future__ import annotations

import datetime as dt
import glob
import os
import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np

STAGES = ["W", "N1", "N2", "N3", "REM"]
EPOCH = 30
FS = 100
SC_WINDOW_H = 10.0
LABEL_MAP = {"Sleep stage W": 0, "Sleep stage 1": 1, "Sleep stage 2": 2, "Sleep stage 3": 3,
             "Sleep stage 4": 3, "Sleep stage R": 4, "Sleep stage N1": 1, "Sleep stage N2": 2,
             "Sleep stage N3": 3, "Movement time": -1, "Sleep stage ?": -1}


@dataclass
class Night:
    cohort: str
    subject: str
    night: str
    age: float
    sex: str
    y: np.ndarray        # (n_epochs,) int8 labels, -1 = unscored
    eeg: np.ndarray      # (n_epochs*3000,) float16 uV
    eeg2: np.ndarray
    eog: np.ndarray
    eog2: np.ndarray

    @property
    def n_epochs(self):
        return len(self.y)

    @property
    def key(self):
        return f"{self.cohort}:{self.night}"


# ----------------------------------------------------------------------------- helpers
def _read(psg: str, picks: list[str]):
    import mne
    mne.set_log_level("ERROR")
    raw = mne.io.read_raw_edf(psg, include=picks, preload=True)
    if raw.info["sfreq"] != FS:
        raw.resample(FS, npad="auto")
    return raw


def _labels_from_annotations(onsets, durations, descs, n_total_epochs):
    y = np.full(n_total_epochs, -1, dtype=np.int8)
    for o, d, s in zip(onsets, durations, descs):
        if s not in LABEL_MAP or d <= 0:
            continue
        i0 = int(round(o / EPOCH))
        n = int(round(d / EPOCH))
        y[i0:min(i0 + n, n_total_epochs)] = LABEL_MAP[s]
    return y


def _cut(raw, ch, e0, e1):
    x = raw.get_data(picks=[ch])[0] * 1e6
    seg = x[e0 * EPOCH * FS: e1 * EPOCH * FS]
    out = np.zeros((e1 - e0) * EPOCH * FS, dtype=np.float32)
    out[:len(seg)] = seg
    return np.clip(out, -6e4, 6e4).astype(np.float16)


def _lights_off_seconds(start: dt.datetime, lo_time: dt.time) -> float:
    lo = dt.datetime.combine(start.date(), lo_time)
    if lo < start - dt.timedelta(hours=2):
        lo += dt.timedelta(days=1)
    return (lo - start).total_seconds()


# ----------------------------------------------------------------------------- Sleep-EDF
def load_sleepedf_night(root: Path, psg: str, hyp: str, cohort: str, meta: dict) -> Night:
    import mne
    raw = _read(psg, ["EEG Fpz-Cz", "EEG Pz-Oz", "EOG horizontal"])
    start = raw.info["meas_date"].replace(tzinfo=None)
    n_total = int(raw.times[-1] // EPOCH)
    ann = mne.read_annotations(hyp)
    y_all = _labels_from_annotations(ann.onset, ann.duration, ann.description, n_total)
    lo_s = _lights_off_seconds(start, meta["lights_off"])
    e0 = int(np.ceil(max(lo_s, 0) / EPOCH))
    if cohort == "SC":
        e1 = min(n_total, e0 + int(SC_WINDOW_H * 3600 / EPOCH))
    else:
        e1 = n_total
    # do not extend beyond the last scored epoch of the file (unscored tail is not part of PSG)
    scored = np.where(y_all >= 0)[0]
    e1 = min(e1, scored[-1] + 1)
    y = y_all[e0:e1]
    eog = _cut(raw, "EOG horizontal", e0, e1)
    return Night(cohort=cohort, subject=meta["subject"], night=meta["night"], age=meta["age"],
                 sex=meta["sex"], y=y, eeg=_cut(raw, "EEG Fpz-Cz", e0, e1),
                 eeg2=_cut(raw, "EEG Pz-Oz", e0, e1), eog=eog, eog2=eog)


def sleepedf_index(root: Path, cohort: str) -> list[tuple[str, str, dict]]:
    import pandas as pd
    base = root / "sleep-edfx"
    out = []
    if cohort == "SC":
        tab = pd.read_excel(base / "SC-subjects.xls")
        for psg in sorted(glob.glob(str(base / "sleep-cassette" / "*PSG.edf"))):
            code = os.path.basename(psg)[:6]
            hyp = glob.glob(str(base / "sleep-cassette" / f"{code}*Hypnogram.edf"))[0]
            s, n = int(code[3:5]), int(code[5])
            row = tab[(tab.subject == s) & (tab.night == n)].iloc[0]
            out.append((psg, hyp, dict(subject=f"SC{s:02d}", night=code, age=float(row["age"]),
                                       sex="F" if int(row["sex (F=1)"]) == 1 else "M",
                                       lights_off=row["LightsOff"])))
    else:
        tab = pd.read_excel(base / "ST-subjects.xls", header=None, skiprows=2)
        tab.columns = ["nr", "age", "sex", "pl_night", "pl_lo", "tz_night", "tz_lo"]
        for psg in sorted(glob.glob(str(base / "sleep-telemetry" / "*PSG.edf"))):
            code = os.path.basename(psg)[:6]
            hyp = glob.glob(str(base / "sleep-telemetry" / f"{code}*Hypnogram.edf"))[0]
            s, n = int(code[3:5]), int(code[5])
            row = tab[tab.nr == s].iloc[0]
            if int(row.pl_night) == n:
                lo, cond = row.pl_lo, "placebo"
            else:
                lo, cond = row.tz_lo, "temazepam"
            out.append((psg, hyp, dict(subject=f"ST{s:02d}", night=code, age=float(row.age),
                                       sex="M" if int(row.sex) == 1 else "F", lights_off=lo,
                                       condition=cond)))
    return out


# ----------------------------------------------------------------------------- HMC
def load_hmc_night(root: Path, rec: str) -> Night:
    base = root / "hmc" / "recordings"
    raw = _read(str(base / f"{rec}.edf"), ["EEG C4-M1", "EEG F4-M1", "EOG E1-M2", "EOG E2-M2"])
    n_total = int(raw.times[-1] // EPOCH)
    on, du, de, lights = [], [], [], {}
    with open(base / f"{rec}_sleepscoring.txt") as f:
        next(f)
        for line in f:
            parts = [p.strip() for p in line.split(",")]
            if len(parts) < 5:
                continue
            o, d, s = float(parts[2]), float(parts[3]), parts[4]
            if s.lower().startswith("lights"):
                lights.setdefault(s.lower(), o)
            else:
                on.append(o); du.append(d); de.append(s)
    y_all = _labels_from_annotations(on, du, de, n_total)
    e0 = int(np.ceil(lights.get("lights off", 0.0) / EPOCH))
    e1 = int(np.floor(lights.get("lights on", n_total * EPOCH) / EPOCH))
    scored = np.where(y_all >= 0)[0]
    e0, e1 = max(e0, 0), min(e1, n_total, scored[-1] + 1)
    eog1 = raw.get_data(picks=["EOG E1-M2"])[0]
    eog2 = raw.get_data(picks=["EOG E2-M2"])[0]
    import mne
    bip = mne.io.RawArray(np.atleast_2d(eog1 - eog2), mne.create_info(["EOG E1-E2"], FS, "eog"))
    return Night(cohort="HMC", subject=rec, night=rec, age=np.nan, sex="NA", y=y_all[e0:e1],
                 eeg=_cut(raw, "EEG C4-M1", e0, e1), eeg2=_cut(raw, "EEG F4-M1", e0, e1),
                 eog=_cut(raw, "EOG E1-M2", e0, e1), eog2=_cut(bip, "EOG E1-E2", e0, e1))


def hmc_index(root: Path) -> list[str]:
    return [os.path.basename(r).replace(".edf", "")
            for r in (root / "hmc" / "RECORDS").read_text().split()]


# ----------------------------------------------------------------------------- cache
def save_night(n: Night, cache: Path) -> Path:
    p = cache / "sleep" / n.cohort / f"{n.night}.npz"
    p.parent.mkdir(parents=True, exist_ok=True)
    eog2 = np.zeros(0, np.float16) if n.eog2 is n.eog else n.eog2  # avoid storing duplicates
    np.savez(p, y=n.y, eeg=n.eeg, eeg2=n.eeg2, eog=n.eog, eog2=eog2,
             meta=np.array([n.cohort, n.subject, n.night, str(n.age), n.sex]))
    return p


def load_night(p: Path) -> Night:
    z = np.load(p, allow_pickle=False)
    c, s, ni, a, sx = [str(v) for v in z["meta"]]
    eog = z["eog"]
    eog2 = z["eog2"] if z["eog2"].size else eog
    return Night(c, s, ni, float(a), sx, z["y"], z["eeg"], z["eeg2"], eog, eog2)


def cached_nights(cache: Path, cohort: str) -> list[Path]:
    return sorted((cache / "sleep" / cohort).glob("*.npz"))
