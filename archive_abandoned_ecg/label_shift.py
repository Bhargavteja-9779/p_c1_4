"""Subject-level label-shift adaptation: baselines and the proposed hierarchical method.

Notation: P (n x K) calibrated source posteriors p_s(y|x) for the n samples (beats / epochs) of
ONE test subject, in temporal order; pi_s (K,) the source prior implied by the calibrated model.
Every estimator returns an `Adaptation` with the estimated subject prior (the quantification
output) and adapted per-sample posteriors.

Baselines (independent re-implementations from the original papers):
  * none      : calibrated source posteriors.
  * MLLS      : EM prior adjustment (Saerens et al., 2002), used with BCTS (Alexandari 2020).
  * BBSE      : black-box shift estimation (Lipton et al., 2018), soft confusion matrix.
  * RLLS      : regularised BBSE (Azizzadenesheli et al., 2019).
  * MAPLS     : MAP label shift with uniform Dirichlet target prior and divergence-based
                shrinkage weight (Ye et al., 2024), following the authors' public algorithm.
  * IM-prior  : prior selected by information maximisation of the adapted posteriors (the
                prior-learning principle used by SPDIM, Li et al., 2025), applied post hoc.
  * HMM-fixed : forward-backward smoothing with a fixed population transition matrix and the
                source prior (hybrid classifier/HMM; no adaptation).
Proposed (HEB-LSA): hierarchical empirical-Bayes label-shift adaptation
  * EB-iid    : variational-Bayes EM for the subject prior pi ~ Dir(alpha_EB).
  * EB-HMM    : variational-Bayes Baum-Welch for a subject-specific Markov chain whose rows
                A_j ~ Dir(beta_EB[j]); emissions are scaled likelihoods p_s(y|x)/pi_s(y).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from numba import njit
from scipy.optimize import minimize
from scipy.special import digamma, softmax

EPS = 1e-12


@dataclass
class Adaptation:
    prior: np.ndarray            # estimated subject class proportions (quantification)
    post: np.ndarray             # adapted posteriors (n x K)
    info: dict = field(default_factory=dict)


def _renorm(M):
    M = np.maximum(M, EPS)
    return M / M.sum(-1, keepdims=True)


def reweight(P, w):
    return _renorm(P * w[None, :])


# --------------------------------------------------------------------------- baselines
def none(P, pi_s, **kw) -> Adaptation:
    return Adaptation(prior=P.mean(0), post=P.copy())


def mlls(P, pi_s, max_iter=1000, tol=1e-8, **kw) -> Adaptation:
    pi = pi_s.copy()
    for it in range(max_iter):
        Q = reweight(P, pi / pi_s)
        new = Q.mean(0)
        if np.abs(new - pi).max() < tol:
            pi = new
            break
        pi = new
    return Adaptation(prior=pi, post=reweight(P, pi / pi_s), info={"iter": it + 1})


def soft_confusion(P_src, y_src, K):
    """Joint p(yhat = i, y = j) estimated with soft predictions on held-out source data."""
    C = np.zeros((K, K))
    for j in range(K):
        m = y_src == j
        if m.any():
            C[:, j] = P_src[m].sum(0)
    return C / len(y_src)


def _w_to_prior(w, pi_s):
    w = np.clip(w, 0, None)
    pi = w * pi_s
    if pi.sum() <= 0:
        return pi_s.copy()
    return pi / pi.sum()


def bbse(P, pi_s, C=None, **kw) -> Adaptation:
    mu = P.mean(0)
    # C is the joint p(yhat, y) = p(yhat|y) pi_s(y); solving C w = mu gives w = pi_t / pi_s
    w = np.linalg.lstsq(C, mu, rcond=None)[0]
    pi = _w_to_prior(w, pi_s)
    return Adaptation(prior=pi, post=reweight(P, pi / pi_s))


def rlls(P, pi_s, C=None, n_src=None, alpha=0.01, delta=0.05, **kw) -> Adaptation:
    K = len(pi_s)
    mu = P.mean(0)
    b = mu - C.sum(1)  # mu_t - mu_s (source predicted marginal)
    rho = 3 * (2 * np.log(2 * K / delta) / (3 * n_src) + np.sqrt(2 * np.log(2 * K / delta) / n_src))
    lam = alpha * rho

    def obj(theta):
        return np.linalg.norm(C @ theta - b) + lam * np.linalg.norm(theta)

    res = minimize(obj, np.zeros(K), method="SLSQP", bounds=[(-1, None)] * K)
    w = 1 + res.x
    pi = _w_to_prior(w, pi_s)
    return Adaptation(prior=pi, post=reweight(P, pi / pi_s))


def _kl(p, q):
    p = np.asarray(p, float)
    q = np.asarray(q, float) + 1e-8
    return float(np.sum(np.where(p > 0, p * np.log(np.maximum(p, 1e-300) / q), 0)))


def mapls(P, pi_s, max_iter=100, **kw) -> Adaptation:
    """MAP label shift (Ye et al., WACV 2024): uniform Dirichlet target prior; shrinkage weight
    lambda derived from KL divergences between the MLLS estimate, the source prior and uniform."""
    K = len(pi_s)
    u = np.ones(K) / K

    def em(lam, prior, n_iter):
        q = pi_s.copy()
        for _ in range(n_iter):
            new = reweight(P, q / pi_s).mean(0)
            q = lam * new + (1 - lam) * prior
            q = q / q.sum()
        return q

    def lam_inv(dpq, lam):
        return (1 / (1 - lam) - 1) / dpq

    def lam_fwd(dpq, g):
        return g * dpq / (1 + g * dpq)

    q_ml = em(1.0, np.zeros(K), max_iter)
    TU, TS, SU = _kl(q_ml, u), _kl(q_ml, pi_s), _kl(pi_s, u)
    SU_conf = 1 - lam_fwd(SU, lam_inv(0.5, 0.2))
    TU_conf = lam_fwd(TU, lam_inv(0.5, SU_conf))
    TS_conf = lam_fwd(TS, lam_inv(0.5, SU_conf))
    lam = float(np.sum(np.array([0.9, 0.1]) * np.array([TU_conf, 1 - TS_conf])))
    q = em(lam, u, max_iter)
    return Adaptation(prior=q, post=reweight(P, q / pi_s), info={"lambda": lam})


def im_prior(P, pi_s, **kw) -> Adaptation:
    """Choose the subject prior that maximises the information-maximisation objective
    H(mean_t q_t) - mean_t H(q_t) of the reweighted posteriors q_t = P_t * pi/pi_s."""
    logP = np.log(np.maximum(P, EPS))
    lps = np.log(pi_s)

    def neg_im(v):
        lw = v - np.log(np.sum(np.exp(v - v.max()))) - v.max() - lps
        Q = softmax(logP + lw[None, :], axis=1)
        m = Q.mean(0)
        H_marg = -np.sum(m * np.log(m + EPS))
        H_cond = -np.mean(np.sum(Q * np.log(Q + EPS), 1))
        return -(H_marg - H_cond)

    res = minimize(neg_im, np.log(pi_s), method="L-BFGS-B")
    pi = softmax(res.x)
    return Adaptation(prior=pi, post=reweight(P, pi / pi_s))


# --------------------------------------------------------------------------- HMM machinery
@njit(cache=True)
def forward_backward(E, A, p0):
    """Scaled forward-backward. E: (T,K) emission scores (any positive scale per row),
    A: (K,K) transition (rows may be sub-normalised, as in VB), p0: (K,).
    Returns smoothed marginals gamma (T,K), expected transition counts xi (K,K), log-lik."""
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
    beta = np.empty((T, K))
    for k in range(K):
        beta[T - 1, k] = 1.0
    for t in range(T - 2, -1, -1):
        for j in range(K):
            acc = 0.0
            for k in range(K):
                acc += A[j, k] * E[t + 1, k] * beta[t + 1, k]
            beta[t, j] = acc / c[t + 1]
    gamma = np.empty((T, K))
    for t in range(T):
        s = 0.0
        for k in range(K):
            gamma[t, k] = alpha[t, k] * beta[t, k]
            s += gamma[t, k]
        for k in range(K):
            gamma[t, k] /= s
    xi = np.zeros((K, K))
    for t in range(T - 1):
        for j in range(K):
            for k in range(K):
                xi[j, k] += alpha[t, j] * A[j, k] * E[t + 1, k] * beta[t + 1, k] / c[t + 1]
    ll = 0.0
    for t in range(T):
        ll += np.log(c[t])
    return gamma, xi, ll


def _emissions(P, pi_s, temp=1.0):
    E = (P / pi_s[None, :]) ** temp
    return E / E.max(1, keepdims=True)


def hmm_fixed(P, pi_s, A_pop=None, temp=1.0, **kw) -> Adaptation:
    E = _emissions(P, pi_s, temp)
    g, _, ll = forward_backward(E, A_pop, pi_s)
    return Adaptation(prior=g.mean(0), post=g, info={"loglik": ll})


# --------------------------------------------------------------------------- proposed
def eb_iid(P, pi_s, alpha_eb=None, lam=1.0, max_iter=1000, tol=1e-8, **kw) -> Adaptation:
    """Variational-Bayes EM for pi ~ Dir(alpha_eb); lam tempers the evidence (lam=1: exact VB)."""
    K = len(pi_s)
    a = alpha_eb + lam * len(P) * pi_s  # initialise q(pi) around the source prior
    for it in range(max_iter):
        elog = digamma(a) - digamma(a.sum())
        Q = reweight(P, np.exp(elog - elog.max()) / pi_s)
        new = alpha_eb + lam * Q.sum(0)
        if np.abs(new - a).max() < tol * len(P):
            a = new
            break
        a = new
    pi = a / a.sum()
    elog = digamma(a) - digamma(a.sum())
    Q = reweight(P, np.exp(elog - elog.max()) / pi_s)
    return Adaptation(prior=pi, post=Q, info={"iter": it + 1, "a": a})


def ml_hmm(P, pi_s, A_pop=None, max_iter=200, tol=1e-6, temp=1.0, **kw) -> Adaptation:
    """Maximum-likelihood Baum-Welch adaptation of the transition matrix (no hyper-prior);
    used as an ablation of the empirical-Bayes prior."""
    E = _emissions(P, pi_s, temp)
    A = A_pop.copy()
    p0 = pi_s.copy()
    prev = -np.inf
    for it in range(max_iter):
        g, xi, ll = forward_backward(E, A, p0)
        A = _renorm(xi + 1e-10)
        p0 = g[0] * 0.5 + 0.5 * g.mean(0)
        if ll - prev < tol * abs(ll):
            break
        prev = ll
    g, _, ll = forward_backward(E, A, p0)
    return Adaptation(prior=g.mean(0), post=g, info={"iter": it + 1, "A": A, "loglik": ll})


def eb_hmm(P, pi_s, beta_eb=None, alpha_eb=None, lam=1.0, max_iter=200, tol=1e-6, temp=1.0,
           **kw) -> Adaptation:
    """Variational-Bayes Baum-Welch with empirical-Bayes Dirichlet row priors beta_eb.

    q(A_j) = Dir(beta_eb[j] + lam * xi_j); the forward-backward pass uses the sub-normalised
    geometric-mean transitions exp(E[log A_jk]) (MacKay, 1997; Beal, 2003).  The initial-state
    distribution uses the EB class prior mean.  Output prior = mean smoothed marginal.
    """
    K = len(pi_s)
    E = _emissions(P, pi_s, temp)
    p0 = alpha_eb / alpha_eb.sum() if alpha_eb is not None else pi_s.copy()
    B = beta_eb.copy()
    Ageo = np.exp(digamma(B) - digamma(B.sum(1, keepdims=True)))
    prev = -np.inf
    for it in range(max_iter):
        g, xi, ll = forward_backward(E, Ageo, p0)
        B = beta_eb + lam * xi
        Ageo = np.exp(digamma(B) - digamma(B.sum(1, keepdims=True)))
        if ll - prev < tol * abs(ll):
            break
        prev = ll
    g, _, ll = forward_backward(E, Ageo, p0)
    A_mean = B / B.sum(1, keepdims=True)
    return Adaptation(prior=g.mean(0), post=g, info={"iter": it + 1, "A": A_mean, "loglik": ll})


METHODS = {
    "none": none, "mlls": mlls, "bbse": bbse, "rlls": rlls, "mapls": mapls, "im_prior": im_prior,
    "hmm_fixed": hmm_fixed, "ml_hmm": ml_hmm, "eb_iid": eb_iid, "eb_hmm": eb_hmm,
}
