# SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
"""Statistical summaries of result files (protocol section 6): paired differences per seed,
percentile bootstrap over seeds, t interval cross-check, stratified pooled bootstrap."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.stats import t as t_dist

BOOTSTRAP_SEED = 20261124
N_BOOT = 10_000


@dataclass(frozen=True)
class Interval:
    n: int
    mean: float
    sd: float
    boot_lo: float
    boot_hi: float
    t_lo: float
    t_hi: float
    std_effect: float  # mean / sd of the paired differences

    @property
    def half_width(self) -> float:
        return (self.boot_hi - self.boot_lo) / 2


def paired_differences(doc: dict, arm: str, base: str, metric: str = "tau_b") -> dict[str, np.ndarray]:
    """cell_id -> per-seed differences arm - base, in seed order. Failed or null runs are
    excluded and counted by the caller from the result file, never imputed."""
    out: dict[str, list[float]] = {c["cell_id"]: [] for c in doc["cells"]}
    for r in sorted(doc["runs"], key=lambda r: (r["cell_id"], r["seed_index"])):
        if r["status"] != "ok":
            continue
        a, b = r["arms"][arm][metric], r["arms"][base][metric]
        if a is None or b is None:
            continue
        out[r["cell_id"]].append(a - b)
    return {k: np.asarray(v, dtype=float) for k, v in out.items()}


def summarise_diffs(d: np.ndarray, level: float = 0.95, n_boot: int = N_BOOT, seed: int = BOOTSTRAP_SEED) -> Interval:
    n = int(d.size)
    if n == 0:
        nan = float("nan")
        return Interval(0, nan, nan, nan, nan, nan, nan, nan)
    mean = float(d.mean())
    sd = float(d.std(ddof=1)) if n > 1 else float("nan")
    rng = np.random.default_rng(seed)
    boots = d[rng.integers(0, n, size=(n_boot, n))].mean(axis=1)
    a = (1 - level) / 2
    blo, bhi = (float(x) for x in np.quantile(boots, [a, 1 - a]))
    if n > 1 and sd > 0:
        q = float(t_dist.ppf(1 - a, n - 1))
        tlo, thi = mean - q * sd / math.sqrt(n), mean + q * sd / math.sqrt(n)
        eff = mean / sd
    else:
        tlo = thi = eff = float("nan")
    return Interval(n, mean, sd, blo, bhi, tlo, thi, eff)


def pooled_stratified(diffs: dict[str, np.ndarray], n_boot: int = N_BOOT, seed: int = BOOTSTRAP_SEED) -> dict:
    """Equal-weight mean over cells of per-cell mean differences, with a stratified bootstrap
    (seeds resampled within each cell). Returns the point estimate, the two-sided 95% interval
    and the one-sided 95% lower bound."""
    cells = [d for d in diffs.values() if d.size > 0]
    if not cells:
        return {"n_cells": 0, "dbar": None, "lo95": None, "hi95": None, "lower_one_sided_95": None}
    rng = np.random.default_rng(seed)
    acc = np.zeros(n_boot)
    for d in cells:
        acc += d[rng.integers(0, d.size, size=(n_boot, d.size))].mean(axis=1)
    acc /= len(cells)
    dbar = float(np.mean([d.mean() for d in cells]))
    lo, hi, low1 = (float(x) for x in np.quantile(acc, [0.025, 0.975, 0.05]))
    return {"n_cells": len(cells), "dbar": dbar, "lo95": lo, "hi95": hi, "lower_one_sided_95": low1}


def seeds_for_half_width(sd: float, target_half_width: float, z: float = 1.96) -> int | None:
    """Planning: seeds needed so that z*sd/sqrt(n) <= target (normal approximation)."""
    if not (sd > 0) or not (target_half_width > 0):
        return None
    return int(math.ceil((z * sd / target_half_width) ** 2))


def pooled_by_level(doc: dict, diffs: dict[str, np.ndarray], key: str = "sigma", n_boot: int = N_BOOT,
                    seed: int = BOOTSTRAP_SEED) -> dict[str, dict]:
    """Equal-weight pooled contrast within each level of one grid factor (protocol 13.2, A-2):
    for each value of `key`, the cells holding that value are pooled as in pooled_stratified.
    Descriptive; reported with a two-sided 95% interval. Empty if `key` is not a grid factor."""
    groups: dict[str, dict[str, np.ndarray]] = {}
    for c in doc["cells"]:
        if key not in c["values"]:
            return {}
        groups.setdefault(repr(c["values"][key]), {})[c["cell_id"]] = diffs[c["cell_id"]]
    out = {}
    for level, sub in groups.items():
        p = pooled_stratified(sub, n_boot=n_boot, seed=seed)
        out[level] = {"n_cells": p["n_cells"], "mean": p["dbar"], "lo95": p["lo95"], "hi95": p["hi95"]}
    return out
