"""Per-night predictive summaries of clinical parameters for a given base stager.

For one night with stager probabilities P (n x 5) and a fitted 'source model' (BCTS calibrator,
source prior, transition matrix, initial distribution, emission temperature) this produces, for each
parameter: plug-in estimate (stager's argmax hypnogram), FFBS posterior summaries (mean, SD, quantiles),
the same with tau = 1 (ablation) and with independent-epoch sampling (ablation).
"""
from __future__ import annotations

import zlib
from dataclasses import dataclass

import numpy as np

from ..evaluation.sleep_params import PARAMS, compute_params, has_rem
from . import hmm
from .calibration import BCTS

QUANTS = [0.025, 0.05, 0.10, 0.50, 0.90, 0.95, 0.975]
QNAMES = ["q025", "q05", "q10", "q50", "q90", "q95", "q975"]
K = 5


@dataclass
class SourceModel:
    cal: BCTS
    pi_s: np.ndarray
    A: np.ndarray
    p0: np.ndarray
    tau: float
    tau_curve: dict


def fit_source_model(Ps: list[np.ndarray], ys: list[np.ndarray]) -> SourceModel:
    lp = np.log(np.clip(np.concatenate(Ps), 1e-12, 1))
    y = np.concatenate(ys)
    m = y >= 0
    cal = BCTS().fit(lp[m], y[m])
    pi_s = np.bincount(y[m], minlength=K) / m.sum()
    A, p0 = hmm.fit_transition(ys, K)
    Pc = [cal.transform(np.log(np.clip(P, 1e-12, 1))) for P in Ps]
    tau, curve = hmm.fit_tau(Pc, ys, pi_s, A, p0)
    return SourceModel(cal, pi_s, A, p0, tau, curve)


def _summ(samples: dict, prefix: str) -> dict:
    out = {}
    for p in PARAMS:
        v = samples[p].astype(float)
        v = v[np.isfinite(v)]
        if len(v) == 0:
            v = np.array([np.nan])
        out[f"{prefix}_mean_{p}"] = float(np.mean(v))
        out[f"{prefix}_sd_{p}"] = float(np.std(v, ddof=1)) if len(v) > 1 else 0.0
        qs = np.quantile(v, QUANTS)
        for qn, qv in zip(QNAMES, qs):
            out[f"{prefix}_{qn}_{p}"] = float(qv)
    return out


def night_seed(name: str, tag: str) -> int:
    return zlib.crc32(f"{name}|{tag}".encode()) & 0x7FFFFFFF


def summarise_night(P: np.ndarray, y: np.ndarray, sm: SourceModel, name: str, tag: str,
                    M: int = 1000, ablations: bool = True) -> dict:
    mask = y >= 0
    Pc = sm.cal.transform(np.log(np.clip(P, 1e-12, 1)))
    ref = compute_params(np.where(mask, y, 0).astype(np.int8), mask)
    plug_h = P.argmax(1).astype(np.int8)
    plug = compute_params(plug_h, mask)
    rng = np.random.default_rng(night_seed(name, tag))
    S = hmm.ffbs_sample(Pc, sm.pi_s, sm.A, sm.p0, sm.tau, M, rng)
    rec = {"n_epochs": len(y), "n_scored": int(mask.sum()), "ref_has_rem": has_rem(y, mask),
           "acc_plugin": float(np.mean(plug_h[mask] == y[mask])),
           "mean_entropy": float(np.mean(-(Pc * np.log(np.clip(Pc, 1e-12, 1))).sum(1))),
           "mean_maxprob": float(np.mean(Pc.max(1))), "tau": sm.tau}
    g, _ = hmm.smoothed_marginals(Pc, sm.pi_s, sm.A, sm.p0, sm.tau)
    rec["acc_hmm_marginal"] = float(np.mean(g[mask].argmax(1) == y[mask]))
    rec["acc_plugin_cal"] = float(np.mean(Pc[mask].argmax(1) == y[mask]))
    plugc = compute_params(Pc.argmax(1).astype(np.int8), mask)     # locally calibrated plug-in
    plugh = compute_params(g.argmax(1).astype(np.int8), mask)      # HMM-smoothed plug-in
    for p in PARAMS:
        rec[f"ref_{p}"] = float(ref[p])
        rec[f"plug_{p}"] = float(plug[p])
        rec[f"plugc_{p}"] = float(plugc[p])
        rec[f"plugh_{p}"] = float(plugh[p])
    rec.update(_summ(compute_params(S, mask), "ffbs"))
    if ablations:
        rng1 = np.random.default_rng(night_seed(name, tag + "|tau1"))
        S1 = hmm.ffbs_sample(Pc, sm.pi_s, sm.A, sm.p0, 1.0, M, rng1)
        rec.update(_summ(compute_params(S1, mask), "ffbs1"))
        rng2 = np.random.default_rng(night_seed(name, tag + "|ind"))
        S2 = hmm.independent_sample(Pc, M, rng2)
        rec.update(_summ(compute_params(S2, mask), "ind"))
        # sample-size sensitivity: first 100 / 300 FFBS draws
        for m in (100, 300):
            sub = _summ(compute_params(S[:m], mask), f"ffbsM{m}")
            rec.update({k: v for k, v in sub.items() if "_mean_" in k or "_sd_" in k})
    return rec
