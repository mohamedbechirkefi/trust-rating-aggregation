# SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
"""Write the fixture that the demo's vitest compares the JavaScript sandbox port against (M5).

Two parts, both exploratory and simulated:

1. ``catalogues``: two EXP-001 catalogues regenerated read-only by the Python engine
   (``trust.simulate``) with their frozen seeds, together with the engine's scores, nominal
   intervals and metrics for MEAN, SHRINK_5 and LCB. The port must reproduce every score, interval,
   truth value and metric from the same counts and qualities to 1e-12.
2. ``cells``: per-cell means and SDs over the 20 committed seeds of tau-b (MEAN, SHRINK_5), D and
   the share of unreviewed products, read from ``results/confirmatory/EXP-001/results.json``. The
   port's own random generator differs from numpy's, so this part is a distributional check.

The regenerated catalogues must reproduce the committed tau-b exactly (the script stops
otherwise). Compute: two catalogues, well under one second, one process.

Usage: .venv/bin/python scripts/make_sandbox_fixture.py
"""

from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from trust.config import expand_cells  # noqa: E402
from trust.estimators import intervals  # noqa: E402
from trust.runner import arm_scores, evaluate_catalogue  # noqa: E402
from trust.simulate import seed_streams, simulate_catalogue  # noqa: E402

OUT = ROOT / "demo" / "src" / "fixtures" / "sandbox_fixture.json"
RESULTS = "results/confirmatory/EXP-001/results.json"
PICK = (("c04", 0), ("c00", 1))  # (cell, seed index): nu 10 sigma 1.0, and nu 3 sigma 0.5
ARMS = ("MEAN", "SHRINK_5", "LCB")


def main() -> int:
    cfg = json.loads((ROOT / "experiments" / "EXP-001.json").read_text(encoding="utf-8"))
    committed = json.loads((ROOT / RESULTS).read_text(encoding="utf-8"))
    by_run = {(r["cell_id"], r["seed_index"]): r for r in committed["runs"]}
    cells = {c.cell_id: c for c in expand_cells(cfg)}
    arms = {a["name"]: a for a in cfg["arms"]}
    z = cfg["evaluation"]["interval_z"]

    cats = []
    for cid, seed in PICK:
        cell = cells[cid]
        cat = simulate_catalogue(cell.params, seed_streams(cfg["seed_root"], cfg["exp_number"], seed))
        metrics, diag = evaluate_catalogue(cfg, cat)
        for a in ARMS:
            if metrics[a]["tau_b"] != by_run[(cid, seed)]["arms"][a]["tau_b"]:
                raise SystemExit(f"regenerated tau-b differs from the committed run {cid} seed {seed} arm {a}")
        out_arms = {}
        for a in ARMS:
            spec = arms[a]
            lo, hi = intervals(spec["type"], cat.counts, z, spec.get("kappa"), 0.0, spec.get("prior", "uniform"))
            out_arms[a] = {
                "scores": arm_scores(spec, cat).tolist(),
                "lo": lo.tolist(),
                "hi": hi.tolist(),
                "tau_b": metrics[a]["tau_b"],
                "precision_at_k": metrics[a]["precision_at_k"],
                "regret_at_k": metrics[a]["regret_at_k"],
                "rmse": metrics[a]["rmse"],
            }
        cats.append({
            "cell_id": cid,
            "seed_index": seed,
            "nu": cell.params.nu,
            "sigma": cell.params.sigma,
            "mu": cat.mu.tolist(),
            "counts": cat.counts.tolist(),
            "theta": cat.theta.tolist(),
            "share_zero_reviews": diag["share_zero_reviews"],
            "arms": out_arms,
        })

    summary = []
    for c in committed["cells"]:
        runs = [r for r in committed["runs"] if r["cell_id"] == c["cell_id"] and r["status"] == "ok"]
        tm = [r["arms"]["MEAN"]["tau_b"] for r in runs]
        ts = [r["arms"]["SHRINK_5"]["tau_b"] for r in runs]
        d = [b - a for a, b in zip(tm, ts)]
        zr = [r["diagnostics"]["share_zero_reviews"] for r in runs]
        summary.append({
            "cell_id": c["cell_id"],
            "nu": c["values"]["nu"],
            "sigma": c["values"]["sigma"],
            "n_seeds": len(runs),
            "tau_b_mean": {"mean": statistics.fmean(tm), "sd": statistics.stdev(tm)},
            "tau_b_shrink5": {"mean": statistics.fmean(ts), "sd": statistics.stdev(ts)},
            "D": {"mean": statistics.fmean(d), "sd": statistics.stdev(d)},
            "share_zero_reviews": {"mean": statistics.fmean(zr), "sd": statistics.stdev(zr)},
        })

    fixture = {
        "label": "exploratory fixture for the demo sandbox test (simulated)",
        "generator": "scripts/make_sandbox_fixture.py",
        "config": "experiments/EXP-001.json",
        "committed_results": RESULTS,
        "params": {
            "n_products": cfg["n_products"],
            "quality_beta": cfg["base"]["quality"][1:],
            "nb_dispersion": cfg["base"]["nb_dispersion"],
            "kappa": arms["SHRINK_5"]["kappa"],
            "lcb_z": arms["LCB"]["z"],
            "interval_z": z,
            "top_k": cfg["evaluation"]["top_k"],
        },
        "catalogues": cats,
        "cells": summary,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(fixture, indent=None, separators=(",", ":")) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size} bytes); committed tau-b reproduced for {len(cats)} catalogues")
    return 0


if __name__ == "__main__":
    sys.exit(main())
