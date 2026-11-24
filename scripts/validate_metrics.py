# SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
"""M3 metric validation on known cases (exploratory; protocol sections 2, 3 and 5).

    PYTHONPATH=src .venv/bin/python scripts/validate_metrics.py [--out results/exploratory/metric-validation/validation.json]

Each check computes a metric or estimator through the production functions on an input whose
value is known by hand or by construction, and compares it with that value. No simulated
catalogue of any confirmatory seed namespace is generated. Exit status 0 only if every check passes.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

from trust.estimators import dirichlet_posterior, intervals, lcb_score, mean_score, shrink_score, summarise
from trust.metrics import coverage, kendall_tau_b, kendall_tau_b_reference, precision_at_k, regret_at_k, rmse, spearman_rho
from trust.model import report_probability, true_quality

TOL = 1e-12


def checks() -> list[dict]:
    out: list[dict] = []

    def add(name: str, got: float, want: float, tol: float = TOL) -> None:
        ok = (math.isnan(got) and math.isnan(want)) or abs(got - want) <= tol
        out.append({"check": name, "got": None if math.isnan(got) else got,
                    "expected": None if math.isnan(want) else want, "tol": tol, "pass": bool(ok)})

    t = np.array([5.0, 4.0, 3.0, 2.0, 1.0])
    # Kendall tau-b: identical order 1, reversed -1, one swapped pair of 5 -> (9 - 1) / 10.
    add("tau_b identical order", kendall_tau_b(t, t), 1.0)
    add("tau_b reversed order", kendall_tau_b(-t, t), -1.0)
    add("tau_b one adjacent swap (n=5)", kendall_tau_b(np.array([4.0, 5.0, 3.0, 2.0, 1.0]), t), 0.8)
    # Ties: scores (1, 1, 2) vs truth (1, 2, 3): nc = 2, nd = 0, ties in s = 1 -> 2 / sqrt(3 * 2).
    add("tau_b with one tie (hand)", kendall_tau_b(np.array([1.0, 1.0, 2.0]), np.array([1.0, 2.0, 3.0])), 2 / math.sqrt(6))
    rng = np.random.default_rng(424242)
    s, tr = rng.integers(1, 6, 40).astype(float), rng.normal(size=40)
    add("tau_b vs O(N^2) reference (ties)", kendall_tau_b(s, tr), kendall_tau_b_reference(s, tr), 1e-12)
    add("tau_b constant scores is undefined", kendall_tau_b(np.ones(5), t), float("nan"))
    # Spearman: one adjacent swap of 5 -> 1 - 6 * 2 / (5 * 24) = 0.9.
    add("spearman one adjacent swap", spearman_rho(np.array([4.0, 5.0, 3.0, 2.0, 1.0]), t), 0.9)
    # Precision and regret at k = 2: arm top 2 = {0, 2}, true top 2 = {0, 1}.
    arm = np.array([5.0, 1.0, 4.0, 2.0, 3.0])
    add("precision@2 (hand)", precision_at_k(arm, t, 2), 0.5)
    add("regret@2 (hand): (5+4)/2 - (5+3)/2", regret_at_k(arm, t, 2), 0.5)
    add("regret@2 of truth is 0", regret_at_k(t, t, 2), 0.0)
    add("rmse (hand): sqrt((0+9+1+0+4)/5)", rmse(arm, t), math.sqrt(14 / 5))
    lo, hi = t - 0.5, t + 0.5
    add("coverage all inside", coverage(lo, hi, t + 0.1, np.ones(5, bool)), 1.0)
    add("coverage 2 of 4 masked inside", coverage(lo, hi, t + np.array([0, 1, 0, 1, 9]), np.array([1, 1, 1, 1, 0], bool)), 0.5)
    # Estimators on a hand catalogue: product 0 has one 5, product 1 has 1,3 (mean 2), product 2 none.
    c = np.array([[0, 0, 0, 0, 1], [1, 0, 1, 0, 0], [0, 0, 0, 0, 0]])
    m = 3.0  # (5 + 1 + 3) / 3
    add("catalogue mean m", summarise(c).m, m)
    add("MEAN zero-review product scores m", float(mean_score(c)[2]), m)
    add("SHRINK(5) one 5-star review: (5 + 15) / 6", float(shrink_score(c, 5)[0]), 20 / 6)
    add("SHRINK(5) offset +0.5, product 1: (4 + 17.5) / 7", float(shrink_score(c, 5, 0.5)[1]), 21.5 / 7)
    # Pooled SD: only product 1 has n >= 2: values 1, 3 -> s = sqrt(2).
    add("s_pool (hand)", summarise(c).s_pool, math.sqrt(2))
    lo, hi = intervals("mean", c, 1.645)
    add("MEAN interval half-width product 1: 1.645 sqrt(2) / sqrt(2)", float(hi[1] - lo[1]) / 2, 1.645)
    # Centred Dirichlet: catalogue shares (1/3, 0, 1/3, 0, 1/3), alpha = 5/3 each on 1, 3, 5; prior mean = m.
    mean0, var0 = dirichlet_posterior(c, "catalogue")
    add("centred LCB prior mean equals m (zero-review product)", float(mean0[2]), m)
    a = np.array([5 / 3, 0, 5 / 3, 0, 5 / 3]) + np.array([0, 0, 0, 0, 1])
    k = np.arange(1, 6)
    pm = float(a @ k / a.sum())
    pv = float((a @ k**2 / a.sum() - pm**2) / (a.sum() + 1))
    add("centred LCB posterior mean product 0 (hand)", float(mean0[0]), pm)
    add("centred LCB score product 0 (hand)", float(lcb_score(c, 1.645, "catalogue")[0]), pm - 1.645 * math.sqrt(pv))
    # Truth theta: symmetric at mu = 3, and sigma -> 0 gives the rounded value.
    add("theta(mu=3, sigma=1) = 3 by symmetry", float(true_quality(np.array([3.0]), 1.0)[0]), 3.0, 1e-12)
    add("theta(mu=4.2, sigma=0.01) ~ 4", float(true_quality(np.array([4.2]), 0.01)[0]), 4.0, 1e-9)
    add("report probability lambda=2 at r=1 is 1", float(report_probability(np.array([1]), 2.0)[0]), 1.0)
    add("report probability lambda=2 at r=3 is 1/3", float(report_probability(np.array([3]), 2.0)[0]), 1 / 3)
    return out


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--out")
    a = p.parse_args()
    res = checks()
    for r in res:
        print(("PASS" if r["pass"] else "FAIL"), r["check"], r["got"], r["expected"])
    n_fail = sum(not r["pass"] for r in res)
    print(f"{len(res) - n_fail} passed, {n_fail} failed")
    if a.out:
        path = Path(a.out)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"label": "exploratory", "kind": "metric-validation", "checks": res,
                                    "n_pass": len(res) - n_fail, "n_fail": n_fail}, indent=1) + "\n", encoding="utf-8")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
