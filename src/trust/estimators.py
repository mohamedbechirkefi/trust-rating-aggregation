# SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
"""Estimators (protocol section 3). Inputs are per-product star counts; outputs are scores in stars.

counts has shape (N, 5); counts[i, k-1] is the number of reported ratings equal to k.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike, NDArray

from trust.model import LEVELS

SCALE_MIDPOINT = 3.0  # fallback prior mean when a catalogue has no reported rating at all


class EstimatorError(ValueError):
    """Raised for malformed count matrices or estimator parameters."""


def check_counts(counts: ArrayLike) -> NDArray[np.int64]:
    c = np.asarray(counts)
    if c.ndim != 2 or c.shape[1] != 5 or c.shape[0] < 1:
        raise EstimatorError(f"counts must have shape (N >= 1, 5), got {c.shape}")
    if not np.issubdtype(c.dtype, np.integer):
        if not np.all(np.isfinite(c)) or np.any(c != np.round(c)):
            raise EstimatorError("counts must be integers")
    if np.any(c < 0):
        raise EstimatorError("counts must be non-negative")
    return c.astype(np.int64)


@dataclass(frozen=True)
class Summary:
    n: NDArray[np.int64]
    xbar: NDArray[np.float64]  # NaN where n == 0
    m: float  # catalogue prior mean (stars)
    m_fallback: bool  # True when no rating was reported anywhere and m is the scale midpoint
    s_pool: float  # pooled within-product SD (stars); NaN if no product has n >= 2


def summarise(counts: ArrayLike) -> Summary:
    c = check_counts(counts)
    n = c.sum(axis=1)
    sums = c @ LEVELS
    with np.errstate(invalid="ignore", divide="ignore"):
        xbar = np.where(n > 0, sums / np.maximum(n, 1), np.nan)
    total = n.sum()
    if total > 0:
        m, fb = float(sums.sum() / total), False
    else:
        m, fb = SCALE_MIDPOINT, True
    ss = np.where(n > 0, c @ (LEVELS**2) - n * np.nan_to_num(xbar) ** 2, 0.0)
    ss = np.maximum(ss, 0.0)
    df = np.where(n >= 2, n - 1, 0).sum()
    s_pool = float(np.sqrt(ss[n >= 2].sum() / df)) if df > 0 else float("nan")
    return Summary(n=n, xbar=xbar, m=m, m_fallback=fb, s_pool=s_pool)


def mean_score(counts: ArrayLike) -> NDArray[np.float64]:
    """MEAN baseline: xbar_i if n_i >= 1, else the catalogue mean m."""
    s = summarise(counts)
    return np.where(s.n > 0, np.nan_to_num(s.xbar), s.m)


def shrink_score(counts: ArrayLike, kappa: float, centre_offset: float = 0.0) -> NDArray[np.float64]:
    """SHRINK(kappa): (n*xbar + kappa*(m + offset)) / (n + kappa). offset is EXP-003 S2."""
    kappa = float(kappa)
    if not np.isfinite(kappa) or kappa <= 0:
        raise EstimatorError("kappa must be a positive number of pseudo-reviews")
    if not np.isfinite(centre_offset):
        raise EstimatorError("centre_offset must be finite")
    s = summarise(counts)
    centre = s.m + float(centre_offset)
    return (s.n * np.nan_to_num(s.xbar) + kappa * centre) / (s.n + kappa)


def dirichlet_posterior(counts: ArrayLike) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Posterior mean and variance of sum_k k*p_k under a Dirichlet(1,...,1) prior on p.

    With alpha_k = n_k + 1 and A = sum alpha_k: mean S = sum k alpha_k / A and
    Var = (sum k^2 alpha_k / A - S^2) / (A + 1) (exact Dirichlet moment; Miller 2014).
    """
    c = check_counts(counts)
    alpha = c + 1.0
    a0 = alpha.sum(axis=1)
    mean = (alpha @ LEVELS) / a0
    second = (alpha @ LEVELS**2) / a0
    var = np.maximum(second - mean**2, 0.0) / (a0 + 1.0)
    return mean, var


def lcb_score(counts: ArrayLike, z: float = 1.645) -> NDArray[np.float64]:
    """LCB: Dirichlet posterior mean minus z * posterior SD (stars)."""
    if not np.isfinite(z) or z < 0:
        raise EstimatorError("z must be finite and non-negative")
    mean, var = dirichlet_posterior(counts)
    return mean - float(z) * np.sqrt(var)


def intervals(
    arm_type: str, counts: ArrayLike, z: float = 1.645, kappa: float | None = None, centre_offset: float = 0.0
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Nominal two-sided intervals used for the calibration metric (protocol section 5)."""
    s = summarise(counts)
    if arm_type == "mean":
        centre = mean_score(counts)
        half = z * s.s_pool / np.sqrt(np.maximum(s.n, 1))
    elif arm_type == "shrink":
        if kappa is None:
            raise EstimatorError("shrink intervals need kappa")
        centre = shrink_score(counts, kappa, centre_offset)
        half = z * s.s_pool / np.sqrt(s.n + kappa)
    elif arm_type == "lcb":
        centre, var = dirichlet_posterior(counts)
        half = z * np.sqrt(var)
    else:
        raise EstimatorError(f"no interval rule for arm type {arm_type!r}")
    return centre - half, centre + half
