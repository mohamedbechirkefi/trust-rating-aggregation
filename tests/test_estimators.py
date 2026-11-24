# SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
"""Estimators: empty reviews, one review, bounds, posterior formulas, invalid inputs."""
import math

import numpy as np
import pytest

from trust.estimators import (
    SCALE_MIDPOINT,
    EstimatorError,
    dirichlet_posterior,
    intervals,
    lcb_score,
    mean_score,
    shrink_score,
    summarise,
)

Z = 1.645


def counts_from(ratings_per_product):
    c = np.zeros((len(ratings_per_product), 5), dtype=np.int64)
    for i, rs in enumerate(ratings_per_product):
        for r in rs:
            c[i, r - 1] += 1
    return c


# --- empty reviews --------------------------------------------------------------------------

def test_empty_product_gets_catalogue_mean():
    c = counts_from([[], [5, 4], [2]])  # m = (5 + 4 + 2) / 3
    m = 11 / 3
    s = mean_score(c)
    assert s[0] == pytest.approx(m)
    assert s[1] == pytest.approx(4.5) and s[2] == pytest.approx(2.0)
    assert shrink_score(c, 5)[0] == pytest.approx(m)


def test_empty_product_lcb_is_prior_bound():
    # Dirichlet(1,...,1): mean 3, E[X^2] = 11, var = (11 - 9) / 6 = 1/3
    mean, var = dirichlet_posterior(counts_from([[]]))
    assert mean[0] == pytest.approx(3.0)
    assert var[0] == pytest.approx(1 / 3)
    assert lcb_score(counts_from([[]]), Z)[0] == pytest.approx(3 - Z * math.sqrt(1 / 3))


def test_catalogue_with_no_reviews_falls_back_to_midpoint():
    c = counts_from([[], [], []])
    s = summarise(c)
    assert s.m_fallback and s.m == SCALE_MIDPOINT
    assert np.all(mean_score(c) == SCALE_MIDPOINT)
    assert math.isnan(s.s_pool)
    assert np.all(np.isnan(s.xbar))


# --- one review -----------------------------------------------------------------------------

def test_one_review_hand_computed():
    c = counts_from([[5], [3, 3, 3, 1]])  # m = 15 / 5 = 3
    assert summarise(c).m == pytest.approx(3.0)
    assert mean_score(c)[0] == 5.0
    assert shrink_score(c, 5)[0] == pytest.approx((5 + 5 * 3) / 6)
    # alpha = (1,1,1,1,2), A = 6: mean = 20/6, E[X^2] = 80/6, var = (80/6 - (20/6)^2) / 7
    mean, var = dirichlet_posterior(c)
    assert mean[0] == pytest.approx(20 / 6)
    assert var[0] == pytest.approx((80 / 6 - (20 / 6) ** 2) / 7)
    assert lcb_score(c, Z)[0] == pytest.approx(20 / 6 - Z * math.sqrt((80 / 6 - (20 / 6) ** 2) / 7))


def test_s_pool_hand_computed():
    # product A: [1, 3] -> SS = 2, df 1; product B: [4, 4, 5] -> SS = 2/3, df 2; product C: [5] ignored
    c = counts_from([[1, 3], [4, 4, 5], [5]])
    assert summarise(c).s_pool == pytest.approx(math.sqrt((2 + 2 / 3) / 3))


def test_shrink_hand_example():
    c = counts_from([[5, 5], [1]])  # m = 11/3
    m = 11 / 3
    np.testing.assert_allclose(shrink_score(c, 1), [(10 + m) / 3, (1 + m) / 2])
    np.testing.assert_allclose(shrink_score(c, 1, centre_offset=0.5), [(10 + m + 0.5) / 3, (1 + m + 0.5) / 2])


# --- invariants -----------------------------------------------------------------------------

def random_counts(seed, n=60, max_reviews=12):
    rng = np.random.default_rng(seed)
    return rng.multinomial(1, [0.2] * 5, size=(n, max_reviews)).sum(axis=1) * (rng.random((n, 1)) < 0.8)


@pytest.mark.parametrize("seed", range(20))
def test_scores_bounded_and_shrink_between_mean_and_prior(seed):
    c = random_counts(seed)
    s = summarise(c)
    mean = mean_score(c)
    for kappa in (0.5, 1, 5, 20):
        sh = shrink_score(c, kappa)
        assert np.all((sh >= 1) & (sh <= 5))
        lo, hi = np.minimum(mean, s.m), np.maximum(mean, s.m)
        assert np.all(sh >= lo - 1e-12) and np.all(sh <= hi + 1e-12)
    assert np.all((mean >= 1) & (mean <= 5))
    pm, var = dirichlet_posterior(c)
    assert np.all((pm >= 1) & (pm <= 5)) and np.all(var > 0)
    assert np.all(lcb_score(c, Z) <= pm)
    # stronger prior pulls further towards m
    assert np.all(np.abs(shrink_score(c, 20) - s.m) <= np.abs(shrink_score(c, 1) - s.m) + 1e-12)


def test_shrink_limits():
    c = counts_from([[5, 5, 4], [1], []])
    m = summarise(c).m
    np.testing.assert_allclose(shrink_score(c, 1e9), m, atol=1e-6)
    np.testing.assert_allclose(shrink_score(c, 1e-9)[:2], mean_score(c)[:2], atol=1e-6)


def test_lcb_increases_with_evidence_for_same_mean():
    c = counts_from([[5] * 2, [5] * 20])
    l = lcb_score(c, Z)
    assert l[1] > l[0]


def test_differential_summary_against_raw_lists():
    rng = np.random.default_rng(7)
    raw = [list(rng.integers(1, 6, size=rng.integers(0, 9))) for _ in range(40)]
    c = counts_from(raw)
    s = summarise(c)
    flat = [r for rs in raw for r in rs]
    assert s.m == pytest.approx(np.mean(flat))
    for i, rs in enumerate(raw):
        if rs:
            assert s.xbar[i] == pytest.approx(np.mean(rs))
    ss = sum(np.sum((np.array(rs) - np.mean(rs)) ** 2) for rs in raw if len(rs) >= 2)
    df = sum(len(rs) - 1 for rs in raw if len(rs) >= 2)
    assert s.s_pool == pytest.approx(math.sqrt(ss / df))


def test_intervals_hand():
    c = counts_from([[1, 3], [4, 4, 5], [5]])
    sp = summarise(c).s_pool
    lo, hi = intervals("mean", c, Z)
    assert hi[0] - lo[0] == pytest.approx(2 * Z * sp / math.sqrt(2))
    lo, hi = intervals("shrink", c, Z, kappa=5)
    assert hi[1] - lo[1] == pytest.approx(2 * Z * sp / math.sqrt(8))
    lo, hi = intervals("lcb", c, Z)
    pm, var = dirichlet_posterior(c)
    np.testing.assert_allclose(lo, pm - Z * np.sqrt(var))
    with pytest.raises(EstimatorError):
        intervals("shrink", c, Z)
    with pytest.raises(EstimatorError):
        intervals("oracle", c, Z)


# --- invalid inputs -------------------------------------------------------------------------

@pytest.mark.parametrize(
    "bad",
    [np.zeros((3, 4)), np.zeros(5), np.zeros((0, 5)), np.array([[1, -1, 0, 0, 0]]), np.array([[0.5, 0, 0, 0, 0]])],
)
def test_invalid_counts_raise(bad):
    with pytest.raises(EstimatorError):
        mean_score(bad)


@pytest.mark.parametrize("kappa", [0, -1, float("nan"), float("inf")])
def test_invalid_kappa_raises(kappa):
    with pytest.raises(EstimatorError):
        shrink_score(counts_from([[5]]), kappa)


def test_invalid_z_raises():
    with pytest.raises(EstimatorError):
        lcb_score(counts_from([[5]]), -1)
