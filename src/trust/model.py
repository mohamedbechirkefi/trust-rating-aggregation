# SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
"""Formal model of research/protocol.md section 2: pure, deterministic functions.

Units: latent quality ``mu``, noise ``sigma``, true quality ``theta`` and all ratings are in
stars on the integer scale 1..5. Probabilities are unitless.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.stats import norm

from trust import STAR_LEVELS

LEVELS = np.asarray(STAR_LEVELS, dtype=float)


class ModelError(ValueError):
    """Raised for parameters outside the model's domain."""


def _check_sigma(sigma: float) -> float:
    sigma = float(sigma)
    if not np.isfinite(sigma) or sigma <= 0.0:
        raise ModelError(f"sigma must be a finite positive number of stars, got {sigma!r}")
    return sigma


def rating_probabilities(mu: ArrayLike, sigma: float) -> NDArray[np.float64]:
    """P(r = k | mu, sigma) for k = 1..5, with r = clip(floor(mu + sigma*e + 0.5), 1, 5).

    Returns an array of shape ``mu.shape + (5,)`` whose rows sum to 1.
    r = k for 2 <= k <= 4 iff k - 0.5 <= mu + sigma*e < k + 0.5; r = 1 iff the latent value is
    below 1.5; r = 5 iff it is at least 4.5.
    """
    sigma = _check_sigma(sigma)
    mu = np.asarray(mu, dtype=float)
    if not np.all(np.isfinite(mu)):
        raise ModelError("mu must be finite")
    cuts = np.array([1.5, 2.5, 3.5, 4.5])
    cdf = norm.cdf((cuts - mu[..., None]) / sigma)
    lower = np.concatenate([np.zeros(mu.shape + (1,)), cdf], axis=-1)
    upper = np.concatenate([cdf, np.ones(mu.shape + (1,))], axis=-1)
    return np.clip(upper - lower, 0.0, 1.0)


def true_quality(mu: ArrayLike, sigma: float) -> NDArray[np.float64]:
    """theta = E[r | mu, sigma] in stars (protocol section 2)."""
    return rating_probabilities(mu, sigma) @ LEVELS


def report_probability(r: ArrayLike, lam: float) -> NDArray[np.float64]:
    """pi(r) = (1 + lam*|r - 3|/2) / (1 + lam): reporting probability of a potential rating r."""
    lam = float(lam)
    if not np.isfinite(lam) or lam < 0.0:
        raise ModelError(f"lambda must be finite and non-negative, got {lam!r}")
    r = np.asarray(r, dtype=float)
    if np.any((r < 1) | (r > 5)):
        raise ModelError("ratings must lie in [1, 5]")
    return (1.0 + lam * np.abs(r - 3.0) / 2.0) / (1.0 + lam)


def reported_quality(mu: ArrayLike, sigma: float, lam: float) -> NDArray[np.float64]:
    """theta_rep = E[r | reported, mu, sigma, lam] in stars (EXP-003 S3)."""
    p = rating_probabilities(mu, sigma) * report_probability(LEVELS, lam)
    return (p @ LEVELS) / p.sum(axis=-1)


def exposure_weights(mu: ArrayLike, gamma: float) -> NDArray[np.float64]:
    """w_i = exp(gamma*z_i) / mean(exp(gamma*z_i)), z the standardised mu. Mean of w is 1."""
    mu = np.asarray(mu, dtype=float)
    if mu.ndim != 1 or mu.size == 0:
        raise ModelError("mu must be a non-empty vector")
    sd = mu.std()
    z = (mu - mu.mean()) / sd if sd > 0 else np.zeros_like(mu)
    e = np.exp(float(gamma) * z)
    return e / e.mean()
