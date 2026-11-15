"""Empirical-Bayes hyper-priors learned from the population of *training subjects*.

Each training subject s contributes a class-count vector n_s (for the class-proportion prior)
and, for every previous state j, a vector of transition counts n_s[j, :] (for the transition
prior).  We fit Dirichlet-multinomial (Polya) distributions to these count vectors by maximum
marginal likelihood (Minka, 2000, fixed-point iteration).  Working with counts rather than
proportions handles the many exact zeros (e.g. subjects without any S beat) without ad-hoc
smoothing.
"""
from __future__ import annotations

import numpy as np
from scipy.special import digamma, gammaln


def dm_loglik(alpha: np.ndarray, counts: np.ndarray) -> float:
    counts = np.atleast_2d(counts)
    A = alpha.sum()
    n = counts.sum(1)
    return float(np.sum(gammaln(A) - gammaln(n + A)
                        + np.sum(gammaln(counts + alpha) - gammaln(alpha), axis=1)))


def fit_dirichlet_multinomial(counts: np.ndarray, max_iter: int = 5000, tol: float = 1e-10,
                              floor: float = 1e-6) -> np.ndarray:
    """Maximum-likelihood Dirichlet-multinomial parameters (Minka's fixed point)."""
    counts = np.asarray(counts, dtype=np.float64)
    counts = counts[counts.sum(1) > 0]
    if len(counts) == 0:
        raise ValueError("no non-empty count vectors")
    p = (counts / counts.sum(1, keepdims=True)).mean(0)
    alpha = np.maximum(p, floor) * 1.0  # initial concentration 1
    n = counts.sum(1)
    for _ in range(max_iter):
        A = alpha.sum()
        num = np.sum(digamma(counts + alpha) - digamma(alpha), axis=0)
        den = np.sum(digamma(n + A) - digamma(A))
        new = np.maximum(alpha * num / max(den, 1e-300), floor)
        if np.max(np.abs(new - alpha)) < tol * max(1.0, alpha.max()):
            alpha = new
            break
        alpha = new
    return alpha


def class_counts(label_seqs: list[np.ndarray], K: int) -> np.ndarray:
    return np.stack([np.bincount(y, minlength=K) for y in label_seqs])


def transition_counts(label_seqs: list[np.ndarray], K: int) -> np.ndarray:
    """(S, K, K) transition count tensor."""
    out = np.zeros((len(label_seqs), K, K))
    for s, y in enumerate(label_seqs):
        if len(y) > 1:
            np.add.at(out[s], (y[:-1], y[1:]), 1)
    return out


def fit_class_prior(label_seqs: list[np.ndarray], K: int) -> np.ndarray:
    return fit_dirichlet_multinomial(class_counts(label_seqs, K))


def fit_transition_prior(label_seqs: list[np.ndarray], K: int, floor: float = 1e-3) -> np.ndarray:
    """Row-wise Dirichlet-multinomial fit; rows never observed fall back to a weak prior
    concentrated on self-transitions."""
    C = transition_counts(label_seqs, K)
    beta = np.zeros((K, K))
    for j in range(K):
        rows = C[:, j, :]
        rows = rows[rows.sum(1) > 0]
        if len(rows) >= 2:
            beta[j] = fit_dirichlet_multinomial(rows, floor=floor)
        else:
            beta[j] = floor
            beta[j, j] = 1.0
    return beta


def pooled_transition_matrix(label_seqs: list[np.ndarray], K: int, eps: float = 1e-3) -> np.ndarray:
    C = transition_counts(label_seqs, K).sum(0) + eps
    return C / C.sum(1, keepdims=True)
