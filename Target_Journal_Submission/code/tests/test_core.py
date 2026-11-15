"""Unit tests for the core methodology (run: python -m pytest -q tests)."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.evaluation.conformal_eval import evaluate  # noqa: E402
from src.evaluation.sleep_params import compute_params  # noqa: E402
from src.statistics.stats import auroc, holm, icc_a1  # noqa: E402
from src.uncertainty import hmm  # noqa: E402
from src.uncertainty.calibration import BCTS  # noqa: E402
from src.uncertainty.conformal import conformal_quantile  # noqa: E402


def test_sleep_params_hand_computed():
    h = np.array([0] * 10 + [2] * 20 + [0] * 4 + [4] * 10 + [0] * 6, dtype=np.int8)
    p = compute_params(h)
    assert p["TST"] == 15 and p["SOL"] == 5 and p["WASO"] == 2 and p["REML"] == 12
    assert abs(p["N2%"] - 200 / 3) < 1e-9 and abs(p["REM%"] - 100 / 3) < 1e-9


def test_sleep_params_mask_and_no_rem():
    h = np.array([0, 0, 2, 2, 0, 2, 0], dtype=np.int8)
    mask = np.array([1, 1, 1, 0, 1, 1, 1], bool)  # one unscored epoch excluded
    p = compute_params(h, mask)
    assert p["TST"] == 1.0 and p["WASO"] == 0.5 and p["REML"] == (7 - 2) * 0.5  # censored


def test_sleep_params_vectorised_matches_scalar():
    rng = np.random.default_rng(0)
    H = rng.integers(0, 5, size=(7, 50)).astype(np.int8)
    V = compute_params(H)
    for i in range(7):
        s = compute_params(H[i])
        for k in V:
            assert np.isclose(V[k][i], s[k], equal_nan=True)


def test_ffbs_marginals_match_forward_backward():
    rng = np.random.default_rng(1)
    A = np.full((5, 5), 0.05) + np.eye(5) * 0.75
    A /= A.sum(1, keepdims=True)
    P = rng.dirichlet(np.ones(5) * 2, size=40)
    pi = np.ones(5) / 5
    S = hmm.ffbs_sample(P, pi, A, pi, 1.0, 20000, rng)
    emp = np.stack([(S == k).mean(0) for k in range(5)], 1)
    g, _ = hmm.smoothed_marginals(P, pi, A, pi, 1.0)
    assert np.abs(emp - g).max() < 0.02


def test_ffbs_deterministic_when_certain():
    h = np.array([0, 0, 1, 2, 2, 3, 4, 4, 0], dtype=np.int8)
    P = np.full((len(h), 5), 1e-8)
    P[np.arange(len(h)), h] = 1
    P /= P.sum(1, keepdims=True)
    A = np.full((5, 5), 0.2)
    S = hmm.ffbs_sample(P, np.ones(5) / 5, A, np.ones(5) / 5, 1.0, 50, np.random.default_rng(0))
    assert (S == h).all()


def test_conformal_quantile_and_coverage():
    rng = np.random.default_rng(2)
    assert conformal_quantile(np.arange(1, 10), 0.1) == 9.0         # n=9: ceil(10*0.9)=9 <= 9 -> 9th
    assert conformal_quantile(np.arange(1, 9), 0.1) == np.inf       # n=8: ceil(9*0.9)=9 > 8 -> inf
    covs = []
    for r in range(400):  # exchangeable heteroscedastic data: marginal coverage >= 0.9
        n = 60
        sd = rng.uniform(0.5, 3, n)
        y = 50 + rng.normal(0, sd)          # centred at 50 so [0,100] clipping is inactive
        f = pd.DataFrame(dict(y=y, plug=50.0, mu=50.0, sd=sd, subject=np.arange(n)))
        res, _, _ = evaluate("N2%", "norm_reg_ffbs", f.iloc[:40], f.iloc[40:], 0.10)
        covs.append(res["coverage"])
    assert np.mean(covs) >= 0.88


def test_bcts_recovers_temperature():
    rng = np.random.default_rng(3)
    z = rng.normal(0, 2, size=(5000, 3))
    p = np.exp(z / 2.0)
    p /= p.sum(1, keepdims=True)
    y = np.array([rng.choice(3, p=pi) for pi in p])
    cal = BCTS().fit(np.log(np.exp(z) / np.exp(z).sum(1, keepdims=True)), y)
    assert 1.6 < cal.T < 2.5


def test_stats_helpers():
    assert auroc(np.array([0.1, 0.2, 0.8, 0.9]), np.array([0, 0, 1, 1])) == 1.0
    adj = holm([0.01, 0.04, 0.03])
    assert np.allclose(adj, [0.03, 0.06, 0.06])
    x = np.linspace(0, 10, 50)
    assert icc_a1(x, x) > 0.999
