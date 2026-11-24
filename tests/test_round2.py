# SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
"""Round-2 amendments: centred LCB prior (A-1), per-sigma reporting (A-2), calibrated configs and
the config-level freeze guard."""

import hashlib
import json
import shutil
from pathlib import Path

import numpy as np
import pytest

from trust import cli
from trust.analysis import pooled_by_level, pooled_stratified
from trust.config import load_config
from trust.estimators import EstimatorError, dirichlet_posterior, dirichlet_prior, lcb_score, summarise
from trust.provenance import config_frozen

REPO = Path(__file__).resolve().parents[1]
CONFIRMATORY = ["EXP-001", "EXP-002", "EXP-003-S1-min1", "EXP-003-S1-min5", "EXP-003-S2", "EXP-003-S3", "EXP-003-S4"]


def test_catalogue_prior_hand_computed():
    c = np.array([[0, 0, 0, 0, 1], [0, 0, 0, 1, 0]])
    assert dirichlet_prior(c, "catalogue").tolist() == [0, 0, 0, 2.5, 2.5]
    mean, var = dirichlet_posterior(c, "catalogue")
    # product 0: alpha = (0, 0, 0, 2.5, 3.5), A = 6
    assert mean[0] == pytest.approx(27.5 / 6)
    assert var[0] == pytest.approx((127.5 / 6 - (27.5 / 6) ** 2) / 7)


def test_catalogue_prior_is_centred_on_m_with_strength_five():
    rng = np.random.default_rng(0)
    c = rng.integers(0, 6, size=(30, 5))
    a = dirichlet_prior(c, "catalogue")
    assert a.sum() == pytest.approx(5.0)
    assert (a @ np.arange(1, 6)) / a.sum() == pytest.approx(summarise(c).m)
    # a product with no review gets the prior mean m as its posterior mean
    c[0] = 0
    mean, _ = dirichlet_posterior(c, "catalogue")
    assert mean[0] == pytest.approx(summarise(c).m)


def test_catalogue_prior_falls_back_to_uniform_without_ratings():
    c = np.zeros((4, 5), dtype=int)
    assert dirichlet_prior(c, "catalogue").tolist() == [1, 1, 1, 1, 1]
    assert np.allclose(lcb_score(c, prior="catalogue"), lcb_score(c, prior="uniform"))


def test_uniform_prior_unchanged_and_unknown_prior_rejected():
    c = np.array([[1, 0, 0, 0, 0]])
    mean, _ = dirichlet_posterior(c)
    assert mean[0] == pytest.approx((1 * 2 + 2 + 3 + 4 + 5) / 6)
    with pytest.raises(EstimatorError):
        dirichlet_prior(c, "other")


def _doc(values_per_cell, diffs):
    cells = [{"cell_id": f"c{i:02d}", "values": v} for i, v in enumerate(values_per_cell)]
    return {"cells": cells}, {f"c{i:02d}": np.asarray(d, float) for i, d in enumerate(diffs)}


def test_pooled_by_sigma_groups_cells_and_matches_pooled_stratified():
    vals = [{"nu": nu, "sigma": s} for nu in (3, 30) for s in (0.5, 1.5)]
    diffs = [[-0.01, -0.02, -0.03], [0.02, 0.03, 0.04], [-0.02, -0.02, -0.01], [0.01, 0.02, 0.05]]
    doc, d = _doc(vals, diffs)
    out = pooled_by_level(doc, d, "sigma")
    assert set(out) == {"0.5", "1.5"}
    assert out["0.5"]["n_cells"] == 2
    assert out["0.5"]["mean"] == pytest.approx(np.mean([np.mean(diffs[0]), np.mean(diffs[2])]))
    ref = pooled_stratified({"c00": d["c00"], "c02": d["c02"]})
    assert out["0.5"]["lo95"] == ref["lo95"] and out["0.5"]["hi95"] == ref["hi95"]
    assert out["0.5"]["mean"] < 0 < out["1.5"]["mean"]


def test_pooled_by_level_empty_when_factor_absent():
    doc, d = _doc([{"nu": 3}, {"nu": 10}], [[0.1, 0.2], [0.3, 0.1]])
    assert pooled_by_level(doc, d, "sigma") == {}


def test_confirmatory_configs_carry_calibrated_values():
    fit = json.loads((REPO / "data" / "calibration" / "movielens-1m-fit.json").read_text())["fitted_values_for_configs"]
    for name in CONFIRMATORY:
        cfg = load_config(REPO / "experiments" / f"{name}.json")
        assert cfg["label"] == "confirmatory" and cfg["n_seeds"] == 20
        assert cfg["base"]["nb_dispersion"] == fit["nb_dispersion"]
        if name != "EXP-003-S4":
            assert cfg["base"]["quality"] == fit["quality"]
        else:
            assert cfg["grid"]["quality"] == [["beta", 1.0, 1.0], ["mixture", 2.0, 6.0, 6.0, 2.0]]
        for arm in cfg["arms"]:
            if arm["type"] == "lcb":
                assert arm["prior"] == "catalogue"


def test_repository_confirmatory_configs_are_frozen():
    for name in CONFIRMATORY:
        exp = name[:7]
        ok, why = config_frozen(exp, REPO / "experiments" / f"{name}.json")
        assert ok, (name, why)


def _mini_repo(tmp_path):
    root = tmp_path / "repo"
    shutil.copytree(REPO / "research", root / "research")
    shutil.copytree(REPO / "experiments", root / "experiments")
    (root / "data").mkdir()
    shutil.copy(REPO / "data" / "manifest.json", root / "data" / "manifest.json")
    return root


def test_guard_accepts_unchanged_and_refuses_changed_config(tmp_path):
    root = _mini_repo(tmp_path)
    cfg_path = root / "experiments" / "EXP-001.json"
    assert config_frozen("EXP-001", cfg_path, root)[0] is True
    cfg = json.loads(cfg_path.read_text())
    cfg["n_seeds"] = 21
    cfg_path.write_text(json.dumps(cfg, indent=1) + "\n")
    ok, why = config_frozen("EXP-001", cfg_path, root)
    assert ok is False and "changed" in why


def test_guard_refuses_unlisted_config_changed_protocol_or_manifest(tmp_path):
    root = _mini_repo(tmp_path)
    extra = root / "experiments" / "EXP-001-copy.json"
    extra.write_bytes((root / "experiments" / "EXP-001.json").read_bytes())
    assert config_frozen("EXP-001", extra, root)[0] is False
    assert config_frozen("EXP-002", root / "experiments" / "EXP-001.json", root)[0] is False
    (root / "data" / "manifest.json").write_text("{}\n")
    assert "manifest" in config_frozen("EXP-001", root / "experiments" / "EXP-001.json", root)[1]
    root2 = _mini_repo(tmp_path / "b")
    with (root2 / "research" / "protocol.md").open("a") as fh:
        fh.write("\nedited after the freeze\n")
    assert "protocol.md" in config_frozen("EXP-001", root2 / "experiments" / "EXP-001.json", root2)[1]
    root3 = _mini_repo(tmp_path / "c")
    with (root3 / "research" / "experiments" / "EXP-001" / "protocol.md").open("a") as fh:
        fh.write("\nedited\n")
    assert config_frozen("EXP-001", root3 / "experiments" / "EXP-001.json", root3)[0] is False


def test_cli_refuses_a_changed_confirmatory_config(tmp_path, capsys):
    cfg = json.loads((REPO / "experiments" / "EXP-001.json").read_text())
    cfg["n_seeds"] = 2
    p = tmp_path / "EXP-001.json"
    p.write_text(json.dumps(cfg))
    rc = cli.main(["run", "--config", str(p), "--out", str(tmp_path / "x")])
    assert rc == cli.EXIT_REFUSED
    assert "not frozen" in capsys.readouterr().err
    assert not (tmp_path / "x").exists()


def test_freeze_record_hashes_match_files():
    rec = json.loads((REPO / "research" / "freeze.json").read_text())
    h = lambda p: hashlib.sha256((REPO / p).read_bytes()).hexdigest()  # noqa: E731
    assert h(rec["study_protocol"]["path"]) == rec["study_protocol"]["sha256"]
    assert h(rec["data_manifest"]["path"]) == rec["data_manifest"]["sha256"]
    for exp in rec["experiments"].values():
        assert h(exp["protocol_path"]) == exp["protocol_sha256"]
        for p, v in exp["configs"].items():
            assert h(p) == v
