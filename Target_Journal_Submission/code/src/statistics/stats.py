"""Statistical utilities. Unit of analysis = subject (nights of one subject are not independent)."""
from __future__ import annotations

import numpy as np
from scipy import stats


def clopper_pearson(k: int, n: int, conf: float = 0.95):
    a = 1 - conf
    lo = stats.beta.ppf(a / 2, k, n - k + 1) if k > 0 else 0.0
    hi = stats.beta.ppf(1 - a / 2, k + 1, n - k) if k < n else 1.0
    return float(lo), float(hi)


def cluster_bootstrap(values_by_cluster: dict, stat_fn, B: int = 2000, seed: int = 0):
    """values_by_cluster: {cluster: payload}; stat_fn(list_of_payloads) -> float.
    Returns (estimate, lo95, hi95) by percentile bootstrap over clusters."""
    keys = list(values_by_cluster)
    est = stat_fn([values_by_cluster[k] for k in keys])
    rng = np.random.default_rng(seed)
    bs = []
    for _ in range(B):
        idx = rng.integers(0, len(keys), len(keys))
        bs.append(stat_fn([values_by_cluster[keys[i]] for i in idx]))
    bs = np.asarray(bs, float)
    bs = bs[np.isfinite(bs)]
    if len(bs) < 0.5 * B:  # statistic undefined in most resamples (e.g. no events): report no CI
        return float(est), np.nan, np.nan
    return float(est), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))


def wilcoxon_paired(a: np.ndarray, b: np.ndarray):
    """Two-sided Wilcoxon signed-rank on paired per-subject values; returns p, median difference
    (a - b) and matched-pairs rank-biserial correlation r = (W+ - W-) / (W+ + W-)."""
    d = np.asarray(a, float) - np.asarray(b, float)
    d = d[np.isfinite(d)]
    nz = d[d != 0]
    if len(nz) < 5:
        return dict(p=np.nan, median_diff=float(np.median(d)) if len(d) else np.nan, r_rb=np.nan, n=len(d))
    res = stats.wilcoxon(nz, zero_method="wilcox", alternative="two-sided")
    ranks = stats.rankdata(np.abs(nz))
    wp, wm = ranks[nz > 0].sum(), ranks[nz < 0].sum()
    return dict(p=float(res.pvalue), median_diff=float(np.median(d)), r_rb=float((wp - wm) / (wp + wm)), n=len(d))


def perm_mean_paired(a: np.ndarray, b: np.ndarray, B: int = 20000, seed: int = 0):
    """Two-sided paired sign-flip permutation test of the MEAN difference (a - b) over clusters
    (subjects).  Tests exactly the quantity reported (difference of mean interval scores), unlike the
    Wilcoxon signed-rank test, which targets the pseudo-median.  Returns p, mean difference and a
    percentile-bootstrap 95% CI of the ratio mean(a)/mean(b)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    a, b = a[ok], b[ok]
    d = a - b
    n = len(d)
    if n < 5 or np.all(d == 0):
        return dict(p=np.nan, mean_diff=float(d.mean()) if n else np.nan, ratio=np.nan, ratio_lo=np.nan, ratio_hi=np.nan, n=n)
    rng = np.random.default_rng(seed)
    obs = abs(d.mean())
    signs = rng.choice([-1.0, 1.0], size=(B, n))
    null = np.abs((signs * d).mean(1))
    p = (1 + np.sum(null >= obs - 1e-12)) / (B + 1)
    idx = rng.integers(0, n, size=(2000, n))
    rat = a[idx].mean(1) / b[idx].mean(1)
    return dict(p=float(p), mean_diff=float(d.mean()), ratio=float(a.mean() / b.mean()),
                ratio_lo=float(np.percentile(rat, 2.5)), ratio_hi=float(np.percentile(rat, 97.5)), n=n)


def holm(pvals):
    p = np.asarray(pvals, float)
    out = np.full_like(p, np.nan)
    ok = np.isfinite(p)
    idx = np.argsort(p[ok])
    m = ok.sum()
    adj = np.empty(m)
    run = 0.0
    for rank, i in enumerate(idx):
        run = max(run, (m - rank) * p[ok][i])
        adj[i] = min(1.0, run)
    out[ok] = adj
    return out


def auroc(score: np.ndarray, label: np.ndarray) -> float:
    label = np.asarray(label, bool)
    if label.all() or (~label).all():
        return np.nan
    r = stats.rankdata(score)
    n1 = label.sum()
    n0 = len(label) - n1
    return float((r[label].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def bland_altman(ref, est):
    d = np.asarray(est, float) - np.asarray(ref, float)
    b, s = d.mean(), d.std(ddof=1)
    return dict(bias=float(b), loa_lo=float(b - 1.96 * s), loa_hi=float(b + 1.96 * s),
                mae=float(np.abs(d).mean()))


def icc_a1(ref, est):
    """ICC(A,1): two-way, absolute agreement, single measurement (McGraw & Wong 1996)."""
    Y = np.stack([np.asarray(ref, float), np.asarray(est, float)], 1)
    n, k = Y.shape
    gm = Y.mean()
    msr = k * ((Y.mean(1) - gm) ** 2).sum() / (n - 1)
    msc = n * ((Y.mean(0) - gm) ** 2).sum() / (k - 1)
    sse = ((Y - Y.mean(1, keepdims=True) - Y.mean(0, keepdims=True) + gm) ** 2).sum()
    mse = sse / ((n - 1) * (k - 1))
    return float((msr - mse) / (msr + (k - 1) * mse + k * (msc - mse) / n))
