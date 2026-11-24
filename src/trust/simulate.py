# SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
"""Synthetic catalogue generation (protocol section 2). Seeded, deterministic, no I/O.

All output is simulated. Real product quality is unobserved and is not modelled here.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from trust.model import (
    ModelError,
    exposure_weights,
    report_probability,
    reported_quality,
    true_quality,
)

STREAMS = ("quality", "counts", "ratings", "reporting")


@dataclass(frozen=True)
class CellParams:
    """Parameters of one simulation cell. Units: sigma in stars; nu is a mean count of raters."""

    n_products: int
    nu: float
    sigma: float
    lam: float = 0.0
    gamma: float = 0.0
    nb_dispersion: float = 1.0
    quality: tuple = ("beta", 4.0, 2.0)

    def validate(self) -> None:
        if int(self.n_products) != self.n_products or self.n_products < 2:
            raise ModelError("n_products must be an integer >= 2")
        if not np.isfinite(self.nu) or self.nu <= 0:
            raise ModelError("nu must be positive")
        if not np.isfinite(self.sigma) or self.sigma <= 0:
            raise ModelError("sigma must be positive")
        if not np.isfinite(self.lam) or self.lam < 0:
            raise ModelError("lambda must be non-negative")
        if not np.isfinite(self.gamma):
            raise ModelError("gamma must be finite")
        if not np.isfinite(self.nb_dispersion) or self.nb_dispersion <= 0:
            raise ModelError("nb_dispersion must be positive")
        validate_quality_spec(self.quality)


def validate_quality_spec(spec: tuple) -> None:
    kind = spec[0]
    if kind == "beta":
        if len(spec) != 3 or min(spec[1], spec[2]) <= 0:
            raise ModelError("beta quality spec is ('beta', a > 0, b > 0)")
    elif kind == "mixture":
        # ('mixture', a1, b1, a2, b2): equal-weight mixture of two Beta components
        if len(spec) != 5 or min(spec[1:]) <= 0:
            raise ModelError("mixture quality spec is ('mixture', a1, b1, a2, b2), all > 0")
    else:
        raise ModelError(f"unknown quality family {kind!r}")


@dataclass(frozen=True)
class Catalogue:
    """One simulated catalogue. counts[i, k-1] is the number of reported ratings equal to k."""

    mu: NDArray[np.float64]
    theta: NDArray[np.float64]
    theta_rep: NDArray[np.float64]
    potential_raters: NDArray[np.int64]
    counts: NDArray[np.int64]

    @property
    def n(self) -> NDArray[np.int64]:
        return self.counts.sum(axis=1)


def seed_streams(seed_root: int, exp_number: int, seed_index: int) -> dict[str, np.random.Generator]:
    """Independent child streams from SeedSequence([seed_root, exp_number, seed_index]).

    The cell does not enter the seed, so within an experiment a given seed index shares its
    latent qualities across cells (common random numbers, protocol section 6).
    """
    for v in (seed_root, exp_number, seed_index):
        if int(v) != v or v < 0:
            raise ModelError("seed components must be non-negative integers")
    children = np.random.SeedSequence([int(seed_root), int(exp_number), int(seed_index)]).spawn(len(STREAMS))
    return {name: np.random.default_rng(ss) for name, ss in zip(STREAMS, children)}


def draw_quality(rng: np.random.Generator, n: int, spec: tuple) -> NDArray[np.float64]:
    """mu = 1 + 4*B in stars, B from the quality family."""
    validate_quality_spec(spec)
    if spec[0] == "beta":
        b = rng.beta(spec[1], spec[2], size=n)
    else:
        comp = rng.random(n) < 0.5
        b = np.where(comp, rng.beta(spec[1], spec[2], size=n), rng.beta(spec[3], spec[4], size=n))
    return 1.0 + 4.0 * b


def simulate_catalogue(params: CellParams, streams: dict[str, np.random.Generator]) -> Catalogue:
    """Generate one catalogue. Deterministic given the streams."""
    params.validate()
    n = int(params.n_products)
    mu = draw_quality(streams["quality"], n, params.quality)
    w = exposure_weights(mu, params.gamma)
    mean = params.nu * w
    r = params.nb_dispersion
    nstar = streams["counts"].negative_binomial(r, r / (r + mean)).astype(np.int64)
    idx = np.repeat(np.arange(n), nstar)
    e = streams["ratings"].standard_normal(idx.size)
    ratings = np.clip(np.floor(mu[idx] + params.sigma * e + 0.5), 1, 5).astype(np.int64)
    keep = streams["reporting"].random(idx.size) < report_probability(ratings, params.lam)
    counts = np.bincount(idx[keep] * 5 + (ratings[keep] - 1), minlength=5 * n).reshape(n, 5)
    return Catalogue(
        mu=mu,
        theta=true_quality(mu, params.sigma),
        theta_rep=reported_quality(mu, params.sigma, params.lam),
        potential_raters=nstar,
        counts=counts.astype(np.int64),
    )
