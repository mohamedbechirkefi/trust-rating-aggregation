# SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
"""Ranking and metrics (protocol sections 3 and 5). Pure functions; no I/O."""

from __future__ import annotations

import math

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.stats import kendalltau, spearmanr


class MetricError(ValueError):
    """Raised for malformed metric inputs."""


def _vec(x: ArrayLike, name: str) -> NDArray[np.float64]:
    a = np.asarray(x, dtype=float)
    if a.ndim != 1 or a.size == 0:
        raise MetricError(f"{name} must be a non-empty vector")
    if not np.all(np.isfinite(a)):
        raise MetricError(f"{name} must be finite")
    return a


def _pair(s: ArrayLike, t: ArrayLike) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    s, t = _vec(s, "scores"), _vec(t, "truth")
    if s.shape != t.shape:
        raise MetricError("scores and truth must have the same length")
    return s, t


def rank_order(scores: ArrayLike) -> NDArray[np.int64]:
    """Product indices sorted by score descending, ties broken by product id ascending."""
    s = _vec(scores, "scores")
    return np.lexsort((np.arange(s.size), -s)).astype(np.int64)


def top_k(scores: ArrayLike, k: int) -> NDArray[np.int64]:
    s = _vec(scores, "scores")
    if int(k) != k or k < 1 or k > s.size:
        raise MetricError(f"k must be an integer in [1, {s.size}]")
    return rank_order(s)[: int(k)]


def kendall_tau_b(scores: ArrayLike, truth: ArrayLike) -> float:
    """Kendall tau-b; NaN when either vector is constant (undefined)."""
    s, t = _pair(scores, truth)
    if s.size < 2 or np.all(s == s[0]) or np.all(t == t[0]):
        return float("nan")
    return float(kendalltau(s, t, variant="b").statistic)


def kendall_tau_b_reference(scores: ArrayLike, truth: ArrayLike) -> float:
    """O(N^2) textbook tau-b, used only as a differential reference in tests."""
    s, t = _pair(scores, truth)
    nc = nd = ts = tt = 0
    n = s.size
    for i in range(n):
        for j in range(i + 1, n):
            ds, dt = np.sign(s[i] - s[j]), np.sign(t[i] - t[j])
            if ds == 0 and dt == 0:
                continue
            if ds == 0:
                ts += 1
            elif dt == 0:
                tt += 1
            elif ds == dt:
                nc += 1
            else:
                nd += 1
    denom = math.sqrt((nc + nd + ts) * (nc + nd + tt))
    return float("nan") if denom == 0 else (nc - nd) / denom


def spearman_rho(scores: ArrayLike, truth: ArrayLike) -> float:
    s, t = _pair(scores, truth)
    if np.all(s == s[0]) or np.all(t == t[0]):
        return float("nan")
    return float(spearmanr(s, t).statistic)


def precision_at_k(scores: ArrayLike, truth: ArrayLike, k: int) -> float:
    s, t = _pair(scores, truth)
    return len(set(top_k(s, k).tolist()) & set(top_k(t, k).tolist())) / k


def regret_at_k(scores: ArrayLike, truth: ArrayLike, k: int) -> float:
    """Mean truth of the true top k minus mean truth of the arm's top k (stars, >= 0)."""
    s, t = _pair(scores, truth)
    return float(t[top_k(t, k)].mean() - t[top_k(s, k)].mean())


def rmse(scores: ArrayLike, truth: ArrayLike) -> float:
    s, t = _pair(scores, truth)
    return float(np.sqrt(np.mean((s - t) ** 2)))


def coverage(lower: ArrayLike, upper: ArrayLike, truth: ArrayLike, mask: ArrayLike) -> float:
    """Share of masked products whose truth lies in [lower, upper]; NaN if the mask is empty
    or any masked bound is not finite."""
    lo, hi, t = (np.asarray(a, dtype=float) for a in (lower, upper, truth))
    mk = np.asarray(mask, dtype=bool)
    if not (lo.shape == hi.shape == t.shape == mk.shape):
        raise MetricError("coverage inputs must have the same shape")
    if mk.sum() == 0 or not (np.all(np.isfinite(lo[mk])) and np.all(np.isfinite(hi[mk]))):
        return float("nan")
    return float(np.mean((lo[mk] <= t[mk]) & (t[mk] <= hi[mk])))
