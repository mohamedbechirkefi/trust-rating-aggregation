# SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
"""Simulation: determinism, common random numbers, bounded ratings, invalid parameters."""
import numpy as np
import pytest

from trust.model import ModelError, true_quality
from trust.simulate import CellParams, draw_quality, seed_streams, simulate_catalogue


def cat(seed=0, **kw):
    p = CellParams(**{"n_products": 200, "nu": 10.0, "sigma": 1.0, **kw})
    return simulate_catalogue(p, seed_streams(20261124, 1, seed))


def test_deterministic_given_seed():
    a, b = cat(4), cat(4)
    np.testing.assert_array_equal(a.counts, b.counts)
    np.testing.assert_array_equal(a.mu, b.mu)
    assert not np.array_equal(cat(5).counts, a.counts)


def test_quality_shared_across_cells_for_same_seed():
    np.testing.assert_array_equal(cat(2, nu=3.0, sigma=0.5).mu, cat(2, nu=30.0, sigma=1.5, lam=2.0).mu)


def test_shapes_bounds_and_truth():
    c = cat(1)
    assert c.counts.shape == (200, 5) and c.counts.dtype == np.int64
    assert np.all(c.counts >= 0)
    assert np.all((c.mu >= 1) & (c.mu <= 5))
    np.testing.assert_allclose(c.theta, true_quality(c.mu, 1.0))
    np.testing.assert_allclose(c.theta_rep, c.theta)  # lambda = 0


def test_no_selection_reports_every_rating():
    c = cat(3, lam=0.0)
    np.testing.assert_array_equal(c.n, c.potential_raters)


def test_selection_reduces_reported_counts():
    a, b = cat(3, lam=0.0), cat(3, lam=2.0)
    np.testing.assert_array_equal(a.potential_raters, b.potential_raters)
    assert np.all(b.n <= b.potential_raters)
    assert b.n.sum() < a.n.sum()


def test_mean_review_count_roughly_nu():
    # NegBin with mean nu: catalogue average over 5 seeds should be near nu (loose bound)
    m = np.mean([cat(s, nu=10.0).potential_raters.mean() for s in range(5)])
    assert 8.0 < m < 12.0


def test_zero_reviews_occur_at_small_nu():
    assert (cat(0, nu=0.5).n == 0).sum() > 50


def test_mixture_quality_is_bimodal_and_bounded():
    rng = np.random.default_rng(0)
    mu = draw_quality(rng, 5000, ("mixture", 2.0, 6.0, 6.0, 2.0))
    assert np.all((mu >= 1) & (mu <= 5))
    assert np.mean(np.abs(mu - 3) < 0.25) < np.mean(np.abs(mu - 2) < 0.25)


@pytest.mark.parametrize(
    "kw",
    [{"n_products": 1}, {"nu": 0.0}, {"sigma": -1.0}, {"lam": -0.5}, {"gamma": float("nan")},
     {"nb_dispersion": 0.0}, {"quality": ("gamma", 1.0, 1.0)}, {"quality": ("beta", 0.0, 1.0)}],
)
def test_invalid_params_raise(kw):
    with pytest.raises(ModelError):
        cat(0, **kw)


def test_invalid_seed_components_raise():
    with pytest.raises(ModelError):
        seed_streams(-1, 0, 0)
