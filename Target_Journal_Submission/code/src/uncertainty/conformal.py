"""Split-conformal prediction intervals for night-level parameters (and baselines).

All interval methods map per-night summaries (point estimate, posterior SD / quantiles) and a set
of labelled calibration nights to intervals for test nights.  Finite-sample marginal coverage
>= 1 - alpha holds for the conformal methods when calibration and test nights are exchangeable
(Vovk et al., 2005; Lei et al., 2018); it is *not* guaranteed under cohort shift, which is why
cross-cohort coverage is evaluated empirically.

Score functions (s = nonconformity of the reference value m):
  abs      : |m - m_hat|                                   (constant width; Lei et al. 2018)
  norm     : |m - mu| / sigma                              (locally weighted)
  norm_reg : |m - mu| / (sigma + median_cal(sigma))        (proposed default; regularised)
  cqr      : max(q_lo - m, m - q_hi)                       (CQR; Romano et al. 2019)
"""
from __future__ import annotations

import numpy as np


def conformal_quantile(scores: np.ndarray, alpha: float) -> float:
    """ceil((n+1)(1-alpha))-th smallest score; +inf if that exceeds n (Lei et al. 2018)."""
    s = np.sort(np.asarray(scores, float))
    s = s[np.isfinite(s)]
    n = len(s)
    k = int(np.ceil((n + 1) * (1 - alpha)))
    if n == 0 or k > n:
        return np.inf
    return float(s[k - 1])


def _scale(cal, test, kind):
    if kind == "norm":
        return cal["sd"], test["sd"]
    if kind == "norm_reg":
        c = np.median(cal["sd"])
        return cal["sd"] + c, test["sd"] + c
    raise ValueError(kind)


def interval(method: str, cal: dict, test: dict, alpha: float, lo_key=None, hi_key=None):
    """cal/test: dicts of arrays with keys among
       y (reference; cal only), plug (plug-in estimate), mu (posterior mean), sd (posterior SD),
       and quantile keys (e.g. 'q05', 'q95').  Returns (lo, hi) arrays for test nights."""
    if method == "ba_loa":                       # Bland-Altman limits of agreement (parametric)
        r = cal["y"] - cal["plug"]
        z = {0.05: 1.959964, 0.1: 1.644854, 0.2: 1.281552}[alpha]
        b, sd = r.mean(), r.std(ddof=1)
        return test["plug"] + b - z * sd, test["plug"] + b + z * sd
    if method == "scp_abs":                      # split conformal, absolute residual of plug-in
        q = conformal_quantile(np.abs(cal["y"] - cal["plug"]), alpha)
        return test["plug"] - q, test["plug"] + q
    if method == "bayes_pct":                    # raw posterior percentile interval (no conformal)
        return test[lo_key], test[hi_key]
    if method in ("norm", "norm_reg"):
        sc, st = _scale(cal, test, method)
        q = conformal_quantile(np.abs(cal["y"] - cal["mu"]) / np.maximum(sc, 1e-9), alpha)
        return test["mu"] - q * st, test["mu"] + q * st
    if method == "cqr":
        s = np.maximum(cal[lo_key] - cal["y"], cal["y"] - cal[hi_key])
        q = conformal_quantile(s, alpha)
        return test[lo_key] - q, test[hi_key] + q
    raise ValueError(method)


def clip_to_range(lo, hi, lower=0.0, upper=None):
    lo = np.maximum(lo, lower)
    if upper is not None:
        hi = np.minimum(hi, upper)
    return lo, hi


def interval_score(y, lo, hi, alpha):
    """Winkler / interval score (lower is better; Gneiting & Raftery 2007)."""
    w = hi - lo
    return w + (2 / alpha) * (lo - y) * (y < lo) + (2 / alpha) * (y - hi) * (y > hi)
