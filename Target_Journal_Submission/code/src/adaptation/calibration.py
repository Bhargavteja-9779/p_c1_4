"""Bias-corrected temperature scaling (BCTS; Alexandari et al., ICML 2020).

Calibrated posterior: softmax(z / T + b), with z the base-model log-probabilities.  Parameters
are fit by minimising the negative log-likelihood on out-of-fold (subject-grouped) source
predictions, so that the calibrated model's implied class prior equals the pooled source prior.
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import minimize
from scipy.special import log_softmax


class BCTS:
    def __init__(self, bias: bool = True):
        self.bias = bias
        self.T = 1.0
        self.b = None

    def fit(self, logp: np.ndarray, y: np.ndarray) -> "BCTS":
        K = logp.shape[1]
        z = np.asarray(logp, dtype=np.float64)

        def nll(theta):
            T = np.exp(theta[0])
            b = theta[1:] if self.bias else np.zeros(K)
            lp = log_softmax(z / T + b, axis=1)
            return -lp[np.arange(len(y)), y].mean()

        x0 = np.zeros(1 + (K if self.bias else 0))
        res = minimize(nll, x0, method="L-BFGS-B")
        self.T = float(np.exp(res.x[0]))
        self.b = res.x[1:] if self.bias else np.zeros(K)
        return self

    def transform(self, logp: np.ndarray) -> np.ndarray:
        z = np.asarray(logp, dtype=np.float64)
        return np.exp(log_softmax(z / self.T + self.b, axis=1))
