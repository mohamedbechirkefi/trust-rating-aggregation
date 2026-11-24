# SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
"""Frozen confirmatory analysis layer (trust.hypotheses, D-011). Uses hand-built result documents and
small exploratory catalogues in the smoke seed namespace (exp_number 0), never a confirmatory one."""
import copy

import numpy as np
import pytest

from trust.analysis import paired_differences, pooled_stratified
from trust.hypotheses import (
    analyse_exp001,
    analyse_exp002,
    analyse_exp003,
    clean,
    direction_depends_on_sigma,
    holm,
    p_one_sided_greater,
    p_two_sided,
)
from trust.results import build_result
from trust.runner import run_experiment


def test_holm_hand():
    r = holm({"a": 0.01, "b": 0.04, "c": 0.03})
    assert r["a"]["p_holm"] == pytest.approx(0.03) and r["a"]["reject"]
    assert r["c"]["p_holm"] == pytest.approx(0.06) and not r["c"]["reject"]
    assert r["b"]["p_holm"] == pytest.approx(0.06) and not r["b"]["reject"]  # step-down stops, monotone


def test_holm_all_reject():
    r = holm({"a": 0.001, "b": 0.02})
    assert all(v["reject"] for v in r.values())


def test_bootstrap_p_values():
    assert p_one_sided_greater(np.ones(99)) == pytest.approx(1 / 100)
    assert p_one_sided_greater(-np.ones(99)) == pytest.approx(1.0)
    assert p_two_sided(np.ones(99)) == pytest.approx(2 / 100)
    assert p_two_sided(np.r_[np.ones(50), -np.ones(49)]) == pytest.approx(1.0)


def test_direction_depends_on_sigma():
    assert direction_depends_on_sigma({"a": {"lo95": 0.1, "hi95": 0.2}, "b": {"lo95": -0.3, "hi95": -0.1}})
    assert not direction_depends_on_sigma({"a": {"lo95": 0.1, "hi95": 0.2}, "b": {"lo95": -0.3, "hi95": 0.1}})


def _fake_doc(dvals: dict, grid_keys=("nu", "sigma")) -> dict:
    """Result document whose SHRINK_5 minus MEAN tau-b differences per cell are given exactly."""
    cells, runs = [], []
    for i, (vals, ds) in enumerate(dvals.items()):
        cid = f"c{i:02d}"
        cells.append({"cell_id": cid, "values": dict(zip(grid_keys, vals)), "params": {}})
        for s, d in enumerate(ds):
            arms = {"MEAN": {"tau_b": 0.5}, "SHRINK_5": {"tau_b": 0.5 + d}, "LCB": {"tau_b": 0.5 - d},
                    "ORACLE": {"tau_b": 1.0}}
            runs.append({"run_id": f"R-{cid}-{s}", "cell_id": cid, "seed_index": s, "status": "ok", "arms": arms,
                         "diagnostics": {"n_evaluated": 200}})
    cfg = {"arms": [{"name": n} for n in ("MEAN", "SHRINK_5", "LCB", "ORACLE")]}
    return {"exp_id": "X", "cells": cells, "runs": runs, "config": cfg}


def test_exp001_rules_on_hand_built_document():
    rng = np.random.default_rng(1)
    dv = {}
    for nu, shift in ((3, 0.03), (10, 0.02), (30, 0.01)):
        for sigma in (0.5, 1.0, 1.5):
            dv[(nu, sigma)] = list(shift + 0.001 * rng.normal(size=20))
    a = analyse_exp001(_fake_doc(dv))
    assert a["H1"]["verdict"] == "supported"
    assert a["H1"]["Dbar"] == pytest.approx(0.02, abs=1e-3)
    assert a["H1b"]["n_sigma_ordered"] == 3 and a["H1b"]["verdict"] == "supported"
    assert not a["direction_depends_on_sigma"]
    assert set(a["holm"]) == {"H1b (nu 3 minus nu 30)", "H1c (LCB)"}
    assert a["holm"]["H1b (nu 3 minus nu 30)"]["reject"] and not a["holm"]["H1c (LCB)"]["reject"]


def test_exp001_sign_change_and_null():
    dv = {}
    for nu in (3, 10, 30):
        for sigma, d in ((0.5, -0.02), (1.0, 0.0), (1.5, 0.02)):
            dv[(nu, sigma)] = [d + 0.001 * k for k in range(-10, 10)]
    a = analyse_exp001(_fake_doc(dv))
    assert a["direction_depends_on_sigma"]
    assert a["H1"]["verdict"] == "not supported"
    assert a["H1b"]["verdict"] == "contradicted"


def test_exp002_paired_contrasts():
    dv = {}
    for nu in (3, 10):
        for lam in (0.0, 2.0):
            for g in (-0.5, 0.0, 0.5):
                dv[(nu, lam, g)] = [0.01 * lam + 0.001 * k for k in range(20)]
    a = analyse_exp002(_fake_doc(dv, ("nu", "lam", "gamma")))
    e = a["contrasts"]["SHRINK_5 minus MEAN"]
    lam = e["contrasts"]["lambda 2 minus 0"]
    assert lam["estimate"] == pytest.approx(0.02) and lam["n_strata_excluding_zero"] == 6
    assert len(lam["per_stratum"]) == 6 and all(r["n_pairs"] == 20 for r in lam["per_stratum"])
    assert e["contrasts"]["gamma 0.5 minus 0"]["estimate"] == pytest.approx(0.0)
    assert e["H1_lambda_verdict"].startswith("difference detected")
    assert e["holm"]["lambda 2 minus 0"]["reject"]
    assert "note" in a["contrasts"]["LCB minus MEAN"]


def test_end_to_end_on_exploratory_catalogues(smoke_cfg):
    """Runs the full analysis chain on small exploratory catalogues (smoke namespace, N = 50)."""
    def mk(grid, base_extra=None, arms_extra=(), ev=None):
        c = copy.deepcopy(smoke_cfg)
        c["n_seeds"] = 3
        c["base"].pop("sigma", None)
        c["base"]["sigma"] = 1.0
        for k in grid:
            c["base"].pop(k, None)
        c["grid"] = grid
        c["base"].update(base_extra or {})
        c["arms"] += list(arms_extra)
        if ev:
            c["evaluation"].update(ev)
        cells, runs, _ = run_experiment(c)
        return build_result(c, cells, runs)

    g1 = {"nu": [3, 10, 30], "sigma": [0.5, 1.5]}
    g2 = {"nu": [3, 10], "lam": [0.0, 2.0], "gamma": [-0.5, 0.0, 0.5]}
    e1 = mk(g1)
    e2 = mk(g2)
    s2 = mk(g1, arms_extra=[{"name": "SHRINK_5_UP", "type": "shrink", "kappa": 5, "centre_offset": 0.5},
                            {"name": "SHRINK_5_DOWN", "type": "shrink", "kappa": 5, "centre_offset": -0.5}])
    s3 = mk(g2, ev={"truth": "theta_rep"})
    s4 = mk({**g1, "quality": [["beta", 1.0, 1.0], ["mixture", 2.0, 6.0, 6.0, 2.0]]})
    s4["config"]["base"].pop("quality", None)
    a1 = clean(analyse_exp001(e1))
    assert a1["counts"]["ok"] == 18
    a2 = clean(analyse_exp002(e2))
    assert len(a2["D_per_cell"]) == 12
    a3 = clean(analyse_exp003(e1, e2, mk(g1, ev={"min_reviews": 1}), mk(g1, ev={"min_reviews": 5}), s2, s3, s4))
    ref = pooled_stratified(paired_differences(e1, "SHRINK_5", "MEAN"))["dbar"]
    assert a3["EXP-001_Dbar"] == pytest.approx(ref)
    assert a3["S2"]["SHRINK_5 (check, equals EXP-001)"]["Dbar"] == pytest.approx(ref)
    assert len(a3["S4"]["by_quality"]) == 2 and a3["S3"]["n_cells"] == 12
    # lambda = 0 cells: theta_rep equals theta, so the signs agree there.
    assert all(not r["sign_differs"] for r in a3["S3"]["rows"] if r["values"]["lam"] == 0.0)
