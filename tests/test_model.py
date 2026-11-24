# SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
"""Model formulas: hand-computed values, bounds, monotonicity, invalid inputs."""
import numpy as np
import pytest
from scipy.stats import norm

from trust.model import (
    ModelError,
    exposure_weights,
    rating_probabilities,
    report_probability,
    reported_quality,
    true_quality,
)


def test_probabilities_sum_to_one_and_are_bounded():
    mu = np.linspace(1, 5, 41)
    for sigma in (0.05, 0.5, 1.0, 3.0):
        p = rating_probabilities(mu, sigma)
        assert p.shape == (41, 5)
        assert np.all(p >= 0) and np.all(p <= 1)
        np.testing.assert_allclose(p.sum(axis=1), 1.0, atol=1e-12)


def test_hand_computed_probabilities_at_mu_3_sigma_1():
    p = rating_probabilities(3.0, 1.0)
    a, b = norm.cdf(-1.5), norm.cdf(-0.5)
    np.testing.assert_allclose(p, [a, b - a, 1 - 2 * b, b - a, a], atol=1e-12)
    # numeric golden value of P(r = 3) = Phi(0.5) - Phi(-0.5)
    assert p[2] == pytest.approx(0.38292492254802624, abs=1e-12)


def test_theta_symmetric_and_hand_value():
    assert true_quality(3.0, 1.0) == pytest.approx(3.0, abs=1e-12)
    # theta(3 + d) - 3 == 3 - theta(3 - d) by symmetry of the scale around 3
    for d in (0.3, 1.1, 1.9):
        assert true_quality(3 + d, 0.7) - 3 == pytest.approx(3 - true_quality(3 - d, 0.7), abs=1e-12)
    # small sigma: theta is the rounded latent value
    assert true_quality(4.2, 0.01) == pytest.approx(4.0, abs=1e-9)


def test_theta_strictly_increasing_and_in_bounds():
    mu = np.linspace(1, 5, 401)
    for sigma in (0.5, 1.0, 1.5):
        th = true_quality(mu, sigma)
        assert np.all(np.diff(th) > 0)
        assert np.all((th >= 1) & (th <= 5))


@pytest.mark.parametrize("sigma", [0.0, -1.0, float("nan"), float("inf")])
def test_invalid_sigma_raises(sigma):
    with pytest.raises(ModelError):
        rating_probabilities(3.0, sigma)


def test_report_probability_hand_values():
    np.testing.assert_allclose(report_probability([1, 2, 3, 4, 5], 2.0), [1, 2 / 3, 1 / 3, 2 / 3, 1])
    np.testing.assert_allclose(report_probability([1, 3, 5], 0.0), [1, 1, 1])


@pytest.mark.parametrize("bad", [[0], [6], [3.0, 7.0]])
def test_report_probability_rejects_out_of_scale(bad):
    with pytest.raises(ModelError):
        report_probability(bad, 1.0)


def test_report_probability_rejects_negative_lambda():
    with pytest.raises(ModelError):
        report_probability([3], -0.1)


def test_reported_quality_equals_theta_without_selection():
    mu = np.linspace(1, 5, 11)
    np.testing.assert_allclose(reported_quality(mu, 1.0, 0.0), true_quality(mu, 1.0), atol=1e-12)


def test_reported_quality_moves_away_from_3_under_selection():
    # extreme ratings are over-reported, so E[r | reported] is further from 3 than theta
    for mu in (1.8, 4.3):
        th, tr = true_quality(mu, 1.0), reported_quality(mu, 1.0, 2.0)
        assert abs(tr - 3) > abs(th - 3)


def test_exposure_weights():
    mu = np.array([1.0, 2.0, 3.0, 4.0])
    np.testing.assert_allclose(exposure_weights(mu, 0.0), 1.0)
    w = exposure_weights(mu, 0.5)
    assert w.mean() == pytest.approx(1.0)
    assert np.all(np.diff(w) > 0)
    assert np.all(np.diff(exposure_weights(mu, -0.5)) < 0)
    np.testing.assert_allclose(exposure_weights(np.full(3, 2.0), 1.0), 1.0)  # zero variance
    with pytest.raises(ModelError):
        exposure_weights(np.array([]), 0.5)
