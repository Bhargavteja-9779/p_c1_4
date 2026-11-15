"""Hybrid classifier/HMM posterior over hypnograms and forward-filtering backward-sampling (FFBS).

Given calibrated epoch posteriors p(y_t | x_t) from any stager trained under class prior pi_s,
the scaled likelihoods e_t(k) = [p(k | x_t) / pi_s(k)]^tau act as HMM emission scores
(Bourlard & Morgan hybrid formulation).  With a population transition matrix A and initial
distribution p0 estimated from labelled source nights, the posterior over whole hypnograms is a
Markov chain that can be sampled exactly with FFBS (Carter & Kohn, 1994; Frühwirth-Schnatter, 1994).
Each sampled hypnogram yields every night-level parameter, so arbitrary non-linear parameters (SOL,
WASO, REM latency) inherit uncertainty consistently, including the temporal correlation of errors.
tau (emission temperature) corrects double counting of temporal context already used by the stager
and is fitted on source nights by maximising the smoothed posterior log-likelihood of the true labels.
"""
from __future__ import annotations

import numpy as np
from numba import njit

EPS = 1e-12


@njit(cache=True)
def _forward(E, A, p0):
    T, K = E.shape
    alpha = np.empty((T, K))
    c = np.empty(T)
    s = 0.0
    for k in range(K):
        alpha[0, k] = p0[k] * E[0, k]
        s += alpha[0, k]
    for k in range(K):
        alpha[0, k] /= s
    c[0] = s
    for t in range(1, T):
        s = 0.0
        for k in range(K):
            acc = 0.0
            for j in range(K):
                acc += alpha[t - 1, j] * A[j, k]
            alpha[t, k] = acc * E[t, k]
            s += alpha[t, k]
        if s <= 0.0:
            s = 1e-300
        for k in range(K):
            alpha[t, k] /= s
        c[t] = s
    return alpha, c


@njit(cache=True)
def forward_backward(E, A, p0):
    """Smoothed marginals gamma (T,K) and log-likelihood."""
    T, K = E.shape
    alpha, c = _forward(E, A, p0)
    beta = np.empty((T, K))
    for k in range(K):
        beta[T - 1, k] = 1.0
    for t in range(T - 2, -1, -1):
        for j in range(K):
            acc = 0.0
            for k in range(K):
                acc += A[j, k] * E[t + 1, k] * beta[t + 1, k]
            beta[t, j] = acc / c[t + 1]
    gamma = alpha * beta
    for t in range(T):
        s = 0.0
        for k in range(K):
            s += gamma[t, k]
        for k in range(K):
            gamma[t, k] /= s
    ll = 0.0
    for t in range(T):
        ll += np.log(c[t])
    return gamma, ll


@njit(cache=True)
def _ffbs(E, A, p0, U):
    """U: (M, T) uniforms. Returns (M, T) int8 sampled state paths."""
    T, K = E.shape
    M = U.shape[0]
    alpha, _ = _forward(E, A, p0)
    out = np.empty((M, T), dtype=np.int8)
    w = np.empty(K)
    for m in range(M):
        # last state ~ alpha_T
        u = U[m, T - 1]
        acc = 0.0
        k_sel = K - 1
        for k in range(K):
            acc += alpha[T - 1, k]
            if u <= acc:
                k_sel = k
                break
        out[m, T - 1] = k_sel
        for t in range(T - 2, -1, -1):
            nxt = out[m, t + 1]
            s = 0.0
            for j in range(K):
                w[j] = alpha[t, j] * A[j, nxt]
                s += w[j]
            u = U[m, t] * s
            acc = 0.0
            k_sel = K - 1
            for j in range(K):
                acc += w[j]
                if u <= acc:
                    k_sel = j
                    break
            out[m, t] = k_sel
    return out


def emissions(P: np.ndarray, pi_s: np.ndarray, tau: float = 1.0) -> np.ndarray:
    E = (np.maximum(P, EPS) / pi_s[None, :]) ** tau
    return E / E.max(1, keepdims=True)


def ffbs_sample(P, pi_s, A, p0, tau, M, rng: np.random.Generator) -> np.ndarray:
    E = emissions(P, pi_s, tau)
    U = rng.random((M, len(P)))
    return _ffbs(E, A, p0, U)


def independent_sample(P, M, rng: np.random.Generator) -> np.ndarray:
    """Ablation: sample each epoch independently from its calibrated posterior."""
    C = np.cumsum(P, 1)
    C[:, -1] = 1.0
    U = rng.random((M, len(P)))
    return (U[:, :, None] > C[None, :, :]).sum(2).astype(np.int8)


def smoothed_marginals(P, pi_s, A, p0, tau):
    g, ll = forward_backward(emissions(P, pi_s, tau), A, p0)
    return g, ll


def fit_transition(label_seqs, K=5, eps=1.0):
    """Pooled transition matrix with add-eps smoothing; only transitions between scored epochs."""
    C = np.full((K, K), eps)
    p0 = np.full(K, eps)
    for y in label_seqs:
        ok = (y[:-1] >= 0) & (y[1:] >= 0)
        np.add.at(C, (y[:-1][ok], y[1:][ok]), 1)
        f = y[y >= 0]
        if len(f):
            p0[f[0]] += 1
    return C / C.sum(1, keepdims=True), p0 / p0.sum()


def fit_tau(Ps, ys, pi_s, A, p0, grid=None):
    """Emission temperature maximising sum_t log gamma_t(y_t) over labelled source nights."""
    if grid is None:  # 0.02-0.10 added after the optimum hit the original 0.10 lower bound
        grid = np.round(np.r_[np.arange(0.02, 0.10, 0.02), np.arange(0.10, 1.51, 0.05)], 3)
    best, best_ll = 1.0, -np.inf
    lls = []
    for tau in grid:
        tot = 0.0
        for P, y in zip(Ps, ys):
            g, _ = forward_backward(emissions(P, pi_s, tau), A, p0)
            m = y >= 0
            tot += np.log(np.maximum(g[m, y[m]], EPS)).sum()
        lls.append(tot)
        if tot > best_ll:
            best, best_ll = float(tau), tot
    return best, dict(zip(map(float, grid), lls))
