# SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
"""Calibration of simulation parameters from real star counts (protocol section 13.1).

Uses only per-movie star counts. It computes no estimator arm and no simulated catalogue, so it
cannot involve the primary contrast.
"""

from __future__ import annotations

import math

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.optimize import minimize
from scipy.special import gammaln, logsumexp
from scipy.stats import beta as beta_dist
from scipy.stats import nbinom

from trust.model import rating_probabilities

SPLIT_SEED = (20261124, 990)
N_GRID = 4000
QUALITY_STARTS = ((4.0, 2.0, 1.0), (2.0, 2.0, 0.5), (1.0, 1.0, 1.5))
QUALITY_BOUNDS = ((math.log(0.5), math.log(100.0)), (math.log(0.5), math.log(100.0)), (math.log(0.05), math.log(5.0)))


def split_movies(movie_ids: ArrayLike) -> tuple[NDArray[np.int64], NDArray[np.int64]]:
    """Fit split F (first floor(M/2) of a seeded permutation of the sorted ids) and check split H."""
    ids = np.sort(np.asarray(movie_ids, dtype=np.int64))
    rng = np.random.default_rng(np.random.SeedSequence(list(SPLIT_SEED)))
    perm = ids[rng.permutation(ids.size)]
    half = ids.size // 2
    return np.sort(perm[:half]), np.sort(perm[half:])


def nb_loglik(n: ArrayLike, mean: float, r: float) -> float:
    n = np.asarray(n, dtype=float)
    p = r / (r + mean)
    return float(np.sum(gammaln(n + r) - gammaln(r) - gammaln(n + 1) + r * np.log(p) + n * np.log1p(-p)))


def fit_negbin(n: ArrayLike) -> dict:
    """ML fit of NegBin(mean, r), var = mean + mean^2/r, to counts (zeros included)."""
    n = np.asarray(n, dtype=float)
    if n.size < 2 or n.mean() <= 0:
        raise ValueError("need at least two counts with a positive mean")
    m0, v0 = n.mean(), n.var(ddof=1)
    r0 = m0**2 / (v0 - m0) if v0 > m0 else 100.0
    res = minimize(
        lambda x: -nb_loglik(n, math.exp(x[0]), math.exp(x[1])),
        x0=[math.log(m0), math.log(r0)],
        method="L-BFGS-B",
    )
    mean, r = (float(math.exp(v)) for v in res.x)
    return {"mean": mean, "r": r, "loglik": -float(res.fun), "converged": bool(res.success),
            "start": {"mean": float(m0), "r": float(r0)}, "n_items": int(n.size)}


def _grid(n_grid: int = N_GRID) -> NDArray[np.float64]:
    return (np.arange(n_grid) + 0.5) / n_grid


def quality_loglik(counts: ArrayLike, a: float, b: float, sigma: float, n_grid: int = N_GRID) -> float:
    """Marginal log-likelihood of star counts under mu = 1 + 4B, B ~ Beta(a, b), noise sigma.

    The multinomial coefficient is omitted (it does not depend on the parameters)."""
    c = np.asarray(counts, dtype=float)
    u = _grid(n_grid)
    logp = np.log(np.maximum(rating_probabilities(1.0 + 4.0 * u, sigma), 1e-300))  # (G, 5)
    logprior = beta_dist.logpdf(u, a, b) - math.log(n_grid)  # midpoint rule weights
    per_movie = logsumexp(c @ logp.T + logprior[None, :], axis=1)
    return float(per_movie.sum())


def fit_quality(counts: ArrayLike, n_grid: int = N_GRID, starts=QUALITY_STARTS) -> dict:
    """ML fit of (a, b, sigma) to per-movie star counts of movies with n >= 1."""
    c = np.asarray(counts, dtype=np.int64)
    c = c[c.sum(axis=1) >= 1]
    if c.shape[0] < 2:
        raise ValueError("need at least two rated items")
    tried = []
    for s in starts:
        res = minimize(
            lambda x: -quality_loglik(c, *np.exp(x), n_grid=n_grid),
            x0=np.log(s),
            method="L-BFGS-B",
            bounds=QUALITY_BOUNDS,
        )
        a, b, sg = (float(v) for v in np.exp(res.x))
        tried.append({"start": list(s), "a": a, "b": b, "sigma": sg, "loglik": -float(res.fun),
                      "converged": bool(res.success)})
    best = max(tried, key=lambda t: t["loglik"])
    return {**{k: best[k] for k in ("a", "b", "sigma", "loglik", "converged")}, "starts": tried,
            "n_items": int(c.shape[0]), "n_ratings": int(c.sum()), "n_grid": n_grid}


def predicted_star_shares(a: float, b: float, sigma: float, n_grid: int = N_GRID) -> NDArray[np.float64]:
    """Star-level shares of a single rating under the fitted population (equal weight per item)."""
    u = _grid(n_grid)
    w = beta_dist.pdf(u, a, b)
    w = w / w.sum()
    return w @ rating_probabilities(1.0 + 4.0 * u, sigma)


def observed_item_star_shares(counts: ArrayLike) -> NDArray[np.float64]:
    """Equal-weight mean over rated items of each item's star shares (unbiased for predicted_star_shares)."""
    c = np.asarray(counts, dtype=float)
    c = c[c.sum(axis=1) >= 1]
    return (c / c.sum(axis=1, keepdims=True)).mean(axis=0)


def nb_quantiles(mean: float, r: float, qs=(0.1, 0.25, 0.5, 0.75, 0.9)) -> list[float]:
    return [float(nbinom.ppf(q, r, r / (r + mean))) for q in qs]
