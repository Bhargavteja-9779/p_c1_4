"""Night-level clinical sleep parameters computed from (possibly many sampled) hypnograms.

Definitions (AASM-style, applied identically to reference, plug-in and sampled hypnograms within the
pre-specified analysis window; epochs with an unscored reference label are counted as wake in the reference hypnogram; automatic hypnograms use all epochs):
  TST   total sleep time (min) = #sleep epochs x 0.5
  SOL   sleep onset latency (min) = time from window start to the first sleep epoch
        (window length if no sleep)
  WASO  wake after sleep onset (min) = #wake epochs between first and last sleep epoch x 0.5
  REML  REM latency (min) = time from sleep onset to first REM epoch; if a hypnogram has sleep but
        no REM, REML is right-censored at window end (reference nights without REM are excluded
        from REML analyses)
  N1%, N2%, N3%, REM% = stage minutes / TST x 100 (0 if TST = 0)
"""
from __future__ import annotations

import numpy as np

PARAMS = ["TST", "SOL", "WASO", "REML", "N1%", "N2%", "N3%", "REM%"]
UNITS = {"TST": "min", "SOL": "min", "WASO": "min", "REML": "min",
         "N1%": "% TST", "N2%": "% TST", "N3%": "% TST", "REM%": "% TST"}
EP_MIN = 0.5


def compute_params(H: np.ndarray, mask: np.ndarray | None = None) -> dict[str, np.ndarray]:
    """H: (M, T) or (T,) integer hypnograms (0=W,1=N1,2=N2,3=N3,4=REM). mask: optional (T,) bool of epochs
    to include; used for reference hypnograms only (automatic hypnograms use all epochs). Returns dict param -> (M,) array (scalar if H is 1-D)."""
    one = H.ndim == 1
    H = np.atleast_2d(H)
    M, T = H.shape
    if mask is None:
        mask = np.ones(T, bool)
    idx = np.arange(T)
    sleep = (H > 0) & mask[None, :]
    wake = (H == 0) & mask[None, :]
    rem = (H == 4) & mask[None, :]
    has_sleep = sleep.any(1)
    first = np.where(has_sleep, sleep.argmax(1), T)
    last = np.where(has_sleep, T - 1 - sleep[:, ::-1].argmax(1), -1)
    tst = sleep.sum(1) * EP_MIN
    # SOL: elapsed time (all epochs count as time) from window start to sleep onset
    sol = first * EP_MIN
    in_sp = (idx[None, :] >= first[:, None]) & (idx[None, :] <= last[:, None])
    waso = (wake & in_sp).sum(1) * EP_MIN
    rem_after = rem & (idx[None, :] >= first[:, None])
    has_rem = rem_after.any(1)
    first_rem = np.where(has_rem, rem_after.argmax(1), T)
    reml = np.where(has_sleep, (first_rem - first) * EP_MIN, np.nan)
    out = {"TST": tst, "SOL": sol, "WASO": waso, "REML": reml}
    n_sleep = np.maximum(sleep.sum(1), 1)
    for k, name in [(1, "N1%"), (2, "N2%"), (3, "N3%"), (4, "REM%")]:
        out[name] = ((H == k) & mask[None, :]).sum(1) / n_sleep * 100.0
    if one:
        out = {k: v[0] for k, v in out.items()}
    return out


def has_rem(H: np.ndarray, mask: np.ndarray) -> bool:
    """True if a (reference) hypnogram contains at least one scored REM epoch."""
    return bool(((H == 4) & mask).any())
