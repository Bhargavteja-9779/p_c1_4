"""Evaluation engine: build intervals for test nights from calibration nights, for many methods.

Methods (all receive identical calibration/test nights):
  ba_loa           Bland–Altman limits of agreement around the plug-in estimate (parametric)
  scp_abs          split conformal, |ref - plug-in|                    (constant width)
  scp_abs_cal      split conformal, |ref - calibrated plug-in|         (constant width, local calibration)
  scp_abs_mu       split conformal, |ref - FFBS mean|                  (constant width, better centre)
  scp_abs_bc       split conformal, |ref - (plug-in + mean calibration bias)|  (distribution-free,
                   bias-corrected limits of agreement; strongest constant-width competitor)
  bayes_pct        raw FFBS posterior percentile interval              (no conformal step)
  ind_pct          raw independent-epoch-sampling percentile interval  (no conformal step)
  cqr_ffbs         conformalised FFBS quantiles (CQR score)
  cqr_qr           CQR with linear quantile regression on night-level features (Romano et al. 2019)
  norm_entropy_reg normalised conformal, scale = mean epoch entropy (+ median)   (simple proxy)
  norm_ffbs        normalised conformal, scale = FFBS SD
  norm_reg_ffbs    normalised conformal, scale = FFBS SD + median_cal(SD)        (PROPOSED)
  norm_reg_ind     as proposed, but independent-epoch sampling SD               (ablation)
  norm_reg_ffbs1   as proposed, but emission temperature tau = 1               (ablation)
  norm_reg_plug    FFBS-SD scale, centred on the raw plug-in                   (centre x scale factorial)
  norm_reg_plugc   FFBS-SD scale, centred on the calibrated plug-in            (centre x scale factorial)
Regularised scales add the median of the label-free scale over calibration AND test nights, so that the
score is a symmetric function of all nights' features and finite-sample validity is exact.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from ..uncertainty.conformal import conformal_quantile, interval_score

PARAMS = ["TST", "SOL", "WASO", "REML", "N1%", "N2%", "N3%", "REM%"]
BOUNDS = {"TST": (0, None), "SOL": (0, None), "WASO": (0, None), "REML": (0, None),
          "N1%": (0, 100), "N2%": (0, 100), "N3%": (0, 100), "REM%": (0, 100)}
METHODS = ["ba_loa", "scp_abs", "scp_abs_bc", "scp_abs_cal", "scp_abs_mu", "bayes_pct", "ind_pct", "cqr_ffbs",
           "cqr_qr", "norm_entropy_reg", "norm_ffbs", "norm_reg_ffbs", "norm_reg_ind", "norm_reg_ffbs1",
           "norm_reg_plug", "norm_reg_plugc"]
PROPOSED = "norm_reg_ffbs"
QK = {0.05: ("q025", "q975"), 0.10: ("q05", "q95"), 0.20: ("q10", "q90")}
ZK = {0.05: 1.959964, 0.10: 1.644854, 0.20: 1.281552}


def param_frame(df: pd.DataFrame, p: str) -> pd.DataFrame:
    """Extract the columns needed for parameter p; drop nights where p is undefined."""
    cols = {"y": f"ref_{p}", "plug": f"plug_{p}", "plugc": f"plugc_{p}", "mu": f"ffbs_mean_{p}", "sd": f"ffbs_sd_{p}",
            "mu_ind": f"ind_mean_{p}", "sd_ind": f"ind_sd_{p}", "mu1": f"ffbs1_mean_{p}",
            "sd1": f"ffbs1_sd_{p}"}
    for a in QK.values():
        for q in a:
            cols[f"f_{q}"] = f"ffbs_{q}_{p}"
            cols[f"i_{q}"] = f"ind_{q}_{p}"
    out = pd.DataFrame({k: df[v].values for k, v in cols.items() if v in df})
    out["entropy"] = df["mean_entropy"].values
    out["maxprob"] = df["mean_maxprob"].values
    out["night"] = df["night"].values
    out["subject"] = df["subject"].values
    ok = np.isfinite(out["y"].values)
    if p == "REML":
        ok &= df["ref_has_rem"].values.astype(bool)
    return out[ok].reset_index(drop=True)


def _qr_fit_predict(cal, test, alpha):
    """Linear quantile regression on night-level features, fitted on half of the calibration nights;
    returns (cal2 index mask, lo/hi for cal2 and test)."""
    from sklearn.linear_model import QuantileRegressor
    feats = ["plug", "mu", "entropy", "maxprob"]
    m_tr = subject_split(cal["subject"].values, seed=12345)   # subject-grouped half split
    idx = np.arange(len(cal))
    tr, c2 = idx[m_tr], idx[~m_tr]
    Xtr, ytr = cal[feats].values[tr], cal["y"].values[tr]
    mu, sdv = Xtr.mean(0), Xtr.std(0) + 1e-9
    z = lambda X: (X - mu) / sdv  # noqa: E731
    preds = {}
    for name, q in (("lo", alpha / 2), ("hi", 1 - alpha / 2)):
        m = QuantileRegressor(quantile=q, alpha=0.0, solver="highs").fit(z(Xtr), ytr)
        preds[name] = (m.predict(z(cal[feats].values[c2])), m.predict(z(test[feats].values)))
    return c2, preds


def make_interval(method, cal, test, alpha):
    y_c = cal["y"].values
    if method == "ba_loa":
        r = y_c - cal["plug"].values
        b, s = r.mean(), r.std(ddof=1)
        return test["plug"].values + b - ZK[alpha] * s, test["plug"].values + b + ZK[alpha] * s
    if method == "scp_abs":
        q = conformal_quantile(np.abs(y_c - cal["plug"].values), alpha)
        return test["plug"].values - q, test["plug"].values + q
    if method == "scp_abs_bc":      # bias-corrected constant width (distribution-free LoA analogue)
        r = y_c - cal["plug"].values
        b = r.mean()
        q = conformal_quantile(np.abs(r - b), alpha)
        return test["plug"].values + b - q, test["plug"].values + b + q
    if method == "scp_abs_cal":     # constant width around the locally calibrated plug-in
        q = conformal_quantile(np.abs(y_c - cal["plugc"].values), alpha)
        return test["plugc"].values - q, test["plugc"].values + q
    if method == "scp_abs_mu":
        q = conformal_quantile(np.abs(y_c - cal["mu"].values), alpha)
        return test["mu"].values - q, test["mu"].values + q
    lo_k, hi_k = QK[alpha]
    if method == "bayes_pct":
        return test[f"f_{lo_k}"].values, test[f"f_{hi_k}"].values
    if method == "ind_pct":
        return test[f"i_{lo_k}"].values, test[f"i_{hi_k}"].values
    if method == "cqr_ffbs":
        s = np.maximum(cal[f"f_{lo_k}"].values - y_c, y_c - cal[f"f_{hi_k}"].values)
        q = conformal_quantile(s, alpha)
        return test[f"f_{lo_k}"].values - q, test[f"f_{hi_k}"].values + q
    if method == "cqr_qr":
        c2, pr = _qr_fit_predict(cal, test, alpha)
        lo_c, hi_c = pr["lo"][0], pr["hi"][0]
        s = np.maximum(lo_c - y_c[c2], y_c[c2] - hi_c)
        q = conformal_quantile(s, alpha)
        return pr["lo"][1] - q, pr["hi"][1] + q
    centre_key, scale_key = {"norm_ffbs": ("mu", "sd"), "norm_reg_ffbs": ("mu", "sd"),
                             "norm_reg_ind": ("mu_ind", "sd_ind"), "norm_reg_ffbs1": ("mu1", "sd1"),
                             "norm_entropy_reg": ("mu", "entropy"), "norm_reg_plug": ("plug", "sd"),
                             "norm_reg_plugc": ("plugc", "sd")}[method]
    sc, st = cal[scale_key].values, test[scale_key].values
    if method != "norm_ffbs":
        c = np.median(np.concatenate([sc, st]))   # label-free, symmetric in all nights -> exact validity
        sc, st = sc + c, st + c
    q = conformal_quantile(np.abs(y_c - cal[centre_key].values) / np.maximum(sc, 1e-9), alpha)
    return test[centre_key].values - q * st, test[centre_key].values + q * st


def clip(p, lo, hi):
    a, b = BOUNDS[p]
    lo = np.maximum(lo, a)
    hi = np.maximum(hi, lo)
    if b is not None:
        hi = np.minimum(hi, b)
        lo = np.minimum(lo, hi)
    return lo, hi


def evaluate(p, method, cal, test, alpha):
    lo, hi = make_interval(method, cal, test, alpha)
    lo, hi = clip(p, lo, hi)
    y = test["y"].values
    w = hi - lo
    cov = (y >= lo) & (y <= hi)
    err = np.abs(y - 0.5 * (lo + hi))
    rho = spearmanr(w, err).statistic if np.std(w) > 0 and len(w) > 2 else np.nan
    return dict(coverage=cov.mean(), mean_width=w.mean(), median_width=np.median(w),
                interval_score=interval_score(y, lo, hi, alpha).mean(), spearman=rho,
                inf_width=np.isinf(w).mean()), lo, hi


def subject_split(subjects: np.ndarray, seed: int, frac: float = 0.5):
    u = np.array(sorted(set(subjects)))
    rng = np.random.default_rng(seed)
    rng.shuffle(u)
    cal_s = set(u[: int(round(frac * len(u)))])
    m = np.array([s in cal_s for s in subjects])
    return m
