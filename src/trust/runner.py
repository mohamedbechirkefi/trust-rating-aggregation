# SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
"""Experiment runner: config -> per-run metrics. Serialisation lives in trust.results."""

from __future__ import annotations

import dataclasses
import math
import time
from datetime import datetime, timezone
from typing import Callable

import numpy as np

from trust.config import Cell, expand_cells, run_id
from trust.estimators import intervals, lcb_score, mean_score, shrink_score, summarise
from trust.metrics import (
    coverage,
    kendall_tau_b,
    precision_at_k,
    regret_at_k,
    rmse,
    spearman_rho,
)
from trust.simulate import Catalogue, seed_streams, simulate_catalogue


def _num(x: float) -> float | None:
    return None if x is None or (isinstance(x, float) and math.isnan(x)) else float(x)


def arm_scores(arm: dict, cat: Catalogue) -> np.ndarray:
    t = arm["type"]
    if t == "mean":
        return mean_score(cat.counts)
    if t == "shrink":
        return shrink_score(cat.counts, arm["kappa"], arm.get("centre_offset", 0.0))
    if t == "lcb":
        return lcb_score(cat.counts, arm.get("z", 1.645), arm.get("prior", "uniform"))
    if t == "oracle":
        return cat.theta.copy()
    raise ValueError(f"unknown arm type {t!r}")


def evaluate_catalogue(cfg: dict, cat: Catalogue) -> tuple[dict, dict]:
    """Metrics per arm and catalogue diagnostics for one simulated catalogue."""
    ev = cfg["evaluation"]
    truth_all = cat.theta if ev["truth"] == "theta" else cat.theta_rep
    n = cat.n
    keep = n >= ev["min_reviews"]
    summ = summarise(cat.counts)
    diag = {
        "n_products": int(n.size),
        "n_evaluated": int(keep.sum()),
        "share_zero_reviews": float(np.mean(n == 0)),
        "mean_reported": float(n.mean()),
        "median_reported": float(np.median(n)),
        "mean_potential": float(cat.potential_raters.mean()),
        "total_reported": int(n.sum()),
        "catalogue_mean_m": float(summ.m),
        "m_fallback": bool(summ.m_fallback),
        "s_pool": _num(summ.s_pool),
        "degenerate": [],
    }
    k = ev["top_k"]
    if keep.sum() < max(k, 2):
        diag["degenerate"].append(f"only {int(keep.sum())} products meet min_reviews; metrics null")
    arms: dict[str, dict] = {}
    for arm in cfg["arms"]:
        s_all = arm_scores(arm, cat)
        res = dict.fromkeys(["tau_b", "spearman", "precision_at_k", "regret_at_k", "coverage", "coverage_abs_err", "rmse"])
        if keep.sum() >= max(k, 2):
            s, tr = s_all[keep], truth_all[keep]
            res["tau_b"] = _num(kendall_tau_b(s, tr))
            res["spearman"] = _num(spearman_rho(s, tr))
            res["precision_at_k"] = precision_at_k(s, tr, k)
            res["regret_at_k"] = regret_at_k(s, tr, k)
            res["rmse"] = rmse(s, tr)
            if res["tau_b"] is None:
                diag["degenerate"].append(f"{arm['name']}: tau_b undefined (constant scores)")
            if arm["type"] != "oracle":
                lo, hi = intervals(
                    arm["type"], cat.counts, ev["interval_z"], arm.get("kappa"), arm.get("centre_offset", 0.0),
                    arm.get("prior", "uniform"),
                )
                mask = keep & (n >= ev["coverage_min_n"])
                cov = _num(coverage(lo, hi, truth_all, mask))
                res["coverage"] = cov
                res["coverage_abs_err"] = None if cov is None else abs(cov - 0.90)
        arms[arm["name"]] = res
    return arms, diag


def run_one(cfg: dict, cell: Cell, seed_index: int) -> tuple[dict, dict]:
    streams = seed_streams(cfg["seed_root"], cfg["exp_number"], seed_index)
    cat = simulate_catalogue(cell.params, streams)
    return evaluate_catalogue(cfg, cat)


def run_experiment(
    cfg: dict, progress: Callable[[str], None] | None = None, runner: Callable = run_one
) -> tuple[list[dict], list[dict], list[dict]]:
    """Run every (cell, seed). A run that raises is retried once with the same seed; a run that
    fails twice is recorded as failed and never replaced (protocol section 6)."""
    cells = expand_cells(cfg)
    runs, timings = [], []
    for cell in cells:
        for seed in range(cfg["n_seeds"]):
            rid = run_id(cfg["exp_id"], cell.cell_id, seed)
            start = datetime.now(timezone.utc)
            t0 = time.perf_counter()
            err, attempts, arms, diag = None, 0, {}, {}
            for attempts in (1, 2):
                try:
                    arms, diag = runner(cfg, cell, seed)
                    err = None
                    break
                except Exception as exc:  # recorded, never swallowed silently
                    err = f"{type(exc).__name__}: {exc}"
            dt = time.perf_counter() - t0
            runs.append(
                {
                    "run_id": rid,
                    "cell_id": cell.cell_id,
                    "seed_index": seed,
                    "status": "ok" if err is None else "failed",
                    "attempts": attempts,
                    "error": err,
                    "diagnostics": diag,
                    "arms": arms,
                }
            )
            timings.append(
                {"run_id": rid, "seed_index": seed, "start_utc": start.isoformat(), "runtime_s": dt}
            )
            if progress:
                progress(f"{rid} {runs[-1]['status']} {dt * 1000:.1f} ms")
    cell_records = [
        {"cell_id": c.cell_id, "values": c.values, "params": _params_json(c)} for c in cells
    ]
    return cell_records, runs, timings


def _params_json(cell: Cell) -> dict:
    d = dataclasses.asdict(cell.params)
    d["quality"] = list(d["quality"])
    return d
