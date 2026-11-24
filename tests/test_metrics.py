# SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
"""Metrics and deterministic sorting; differential test of tau-b against an O(N^2) reference."""
import math

import numpy as np
import pytest

from trust.metrics import (
    MetricError,
    coverage,
    kendall_tau_b,
    kendall_tau_b_reference,
    precision_at_k,
    rank_order,
    regret_at_k,
    rmse,
    spearman_rho,
    top_k,
)


def test_rank_order_descending_with_id_tiebreak():
    s = [2.0, 5.0, 2.0, 5.0, 1.0]
    assert rank_order(s).tolist() == [1, 3, 0, 2, 4]


def test_rank_order_is_deterministic_and_permutation_consistent():
    rng = np.random.default_rng(3)
    s = rng.integers(1, 4, size=200).astype(float)  # heavy ties
    a, b = rank_order(s), rank_order(s.copy())
    assert a.tolist() == b.tolist()
    assert sorted(a.tolist()) == list(range(200))
    # within a tie group ids ascend
    for v in np.unique(s):
        grp = [i for i in a.tolist() if s[i] == v]
        assert grp == sorted(grp)


def test_top_k_and_invalid_k():
    assert top_k([1, 3, 2], 2).tolist() == [1, 2]
    for k in (0, 4, 1.5):
        with pytest.raises(MetricError):
            top_k([1, 3, 2], k)


def test_tau_b_basic_cases():
    x = np.arange(10.0)
    assert kendall_tau_b(x, x) == pytest.approx(1.0)
    assert kendall_tau_b(-x, x) == pytest.approx(-1.0)
    assert math.isnan(kendall_tau_b(np.ones(10), x))
    # hand example with ties: s = [1,2,2,3], t = [1,3,2,2]
    # pairs: (01) c, (02) c, (03) c, (12) tie in s, (13) d, (23) tie in t -> nc=3, nd=1, ts=1, tt=1
    assert kendall_tau_b([1, 2, 2, 3], [1, 3, 2, 2]) == pytest.approx(2 / math.sqrt(5 * 5))


@pytest.mark.parametrize("seed", range(25))
def test_tau_b_differential_against_reference(seed):
    rng = np.random.default_rng(seed)
    n = int(rng.integers(5, 60))
    s = rng.integers(1, 6, size=n).astype(float)  # tied scores, as MEAN produces at small n
    t = rng.normal(size=n)
    if np.all(s == s[0]):
        s[0] += 1
    assert kendall_tau_b(s, t) == pytest.approx(kendall_tau_b_reference(s, t), abs=1e-12)


def test_spearman_and_precision_and_regret_hand():
    t = np.array([5.0, 4.0, 3.0, 2.0, 1.0])
    s = np.array([4.0, 5.0, 3.0, 1.0, 2.0])
    assert spearman_rho(t, t) == pytest.approx(1.0)
    assert precision_at_k(s, t, 2) == 1.0
    assert precision_at_k([1, 2, 3, 4, 5], t, 2) == 0.0
    assert regret_at_k(s, t, 2) == pytest.approx(0.0)
    assert regret_at_k([1, 2, 3, 4, 5], t, 2) == pytest.approx(4.5 - 1.5)
    assert math.isnan(spearman_rho(np.ones(5), t))


@pytest.mark.parametrize("seed", range(10))
def test_regret_nonnegative_and_oracle_zero(seed):
    rng = np.random.default_rng(seed)
    t, s = rng.normal(size=50), rng.normal(size=50)
    assert regret_at_k(s, t, 10) >= -1e-12
    assert regret_at_k(t, t, 10) == 0.0
    assert precision_at_k(t, t, 10) == 1.0


def test_rmse_and_coverage_hand():
    assert rmse([1, 2, 3], [1, 2, 5]) == pytest.approx(math.sqrt(4 / 3))
    lo, hi, t = np.array([0, 0, 0, 0]), np.array([1, 1, 1, 1]), np.array([0.5, 2, 1, -1])
    assert coverage(lo, hi, t, [True, True, True, False]) == pytest.approx(2 / 3)
    assert math.isnan(coverage(lo, hi, t, [False] * 4))


@pytest.mark.parametrize(
    "args",
    [([1, 2], [1, 2, 3]), ([], []), ([1, float("nan")], [1, 2]), ([[1, 2]], [[1, 2]])],
)
def test_invalid_metric_inputs(args):
    with pytest.raises(MetricError):
        kendall_tau_b(*args)
