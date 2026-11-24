# SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
"""Integration: config -> runner -> schema-validated results -> manifest -> report; CLI gates."""
import copy
import hashlib
import json
import shutil
from pathlib import Path

import pytest

from trust import cli
from trust.analysis import pooled_stratified, seeds_for_half_width, summarise_diffs
from trust.config import ConfigError, config_hash, expand_cells, validate_config
from trust.provenance import protocol_frozen
from trust.report import build_report
from trust.results import ResultError, build_result, export_result, import_result
from trust.runner import run_experiment

REPO = Path(__file__).resolve().parents[1]


def test_all_shipped_configs_validate():
    files = sorted((REPO / "experiments").glob("*.json"))
    assert len(files) >= 3
    for f in files:
        validate_config(json.loads(f.read_text()))


def test_cell_expansion_counts():
    cfg = json.loads((REPO / "experiments" / "EXP-001.json").read_text())
    assert len(expand_cells(cfg)) == 9
    cfg2 = json.loads((REPO / "experiments" / "EXP-002.json").read_text())
    assert len(expand_cells(cfg2)) == 12


@pytest.mark.parametrize(
    "mutate",
    [
        lambda c: c["arms"].pop(0),  # drops MEAN
        lambda c: c["arms"].append(dict(c["arms"][1])),  # duplicate name
        lambda c: c.__setitem__("n_products", 5),  # top_k > N
        lambda c: c.__setitem__("unknown", 1),
        lambda c: c["base"].__setitem__("sigma", -1.0),
        lambda c: c.__setitem__("label", "final"),
        lambda c: c.__setitem__("primary_contrast", ["SHRINK_99", "MEAN"]),
    ],
)
def test_invalid_configs_rejected(smoke_cfg, mutate):
    mutate(smoke_cfg)
    with pytest.raises(ConfigError):
        validate_config(smoke_cfg)


def test_config_hash_is_order_independent(smoke_cfg):
    reordered = dict(reversed(list(smoke_cfg.items())))
    assert config_hash(reordered) == config_hash(smoke_cfg)


def test_run_is_deterministic_and_oracle_is_perfect(smoke_cfg):
    cells1, runs1, _ = run_experiment(smoke_cfg)
    cells2, runs2, _ = run_experiment(copy.deepcopy(smoke_cfg))
    assert json.dumps(runs1, sort_keys=True) == json.dumps(runs2, sort_keys=True)
    assert all(r["status"] == "ok" for r in runs1)
    assert all(r["arms"]["ORACLE"]["tau_b"] == pytest.approx(1.0, abs=1e-12) for r in runs1)
    assert all(r["arms"]["ORACLE"]["regret_at_k"] == 0.0 for r in runs1)
    assert len(runs1) == smoke_cfg["n_seeds"] * len(cells1)


def test_retry_once_then_record_failure(smoke_cfg):
    calls = {}

    def flaky(cfg, cell, seed):
        calls[(cell.cell_id, seed)] = calls.get((cell.cell_id, seed), 0) + 1
        if seed == 0 and calls[(cell.cell_id, seed)] == 1:
            raise RuntimeError("transient")
        if seed == 1:
            raise RuntimeError("persistent")
        return {}, {}

    _, runs, _ = run_experiment(smoke_cfg, runner=flaky)
    by = {(r["cell_id"], r["seed_index"]): r for r in runs}
    assert by[("c00", 0)]["status"] == "ok" and by[("c00", 0)]["attempts"] == 2
    assert by[("c00", 1)]["status"] == "failed" and by[("c00", 1)]["attempts"] == 2
    assert "persistent" in by[("c00", 1)]["error"]
    assert by[("c00", 2)]["attempts"] == 1
    assert len(runs) == 6  # failed runs are kept, never replaced


def test_degenerate_catalogue_flags_and_nulls(smoke_cfg):
    cfg = copy.deepcopy(smoke_cfg)
    cfg["n_products"] = 12
    cfg["grid"] = {"nu": [0.01]}
    cfg["evaluation"]["min_reviews"] = 5
    _, runs, _ = run_experiment(validate_config(cfg))
    r = runs[0]
    assert r["status"] == "ok"
    assert r["diagnostics"]["degenerate"]
    assert r["arms"]["MEAN"]["tau_b"] is None
    doc = build_result(cfg, [], runs)
    doc["cells"] = []
    json.dumps(doc, allow_nan=False)


def test_all_zero_review_catalogue_gives_undefined_tau(smoke_cfg):
    cfg = copy.deepcopy(smoke_cfg)
    cfg["grid"] = {"nu": [1e-9]}
    _, runs, _ = run_experiment(validate_config(cfg))
    r = runs[0]
    assert r["diagnostics"]["m_fallback"] is True
    assert r["arms"]["MEAN"]["tau_b"] is None
    assert any("constant scores" in d for d in r["diagnostics"]["degenerate"])


def test_export_validates_and_import_fails_closed(smoke_cfg, tmp_path):
    cells, runs, _ = run_experiment(smoke_cfg)
    doc = build_result(smoke_cfg, cells, runs)
    p = tmp_path / "results.json"
    export_result(p, doc)
    assert import_result(p)["exp_id"] == "X-SMOKE"
    bad = json.loads(p.read_text())
    bad["config"]["n_seeds"] = 99
    p.write_text(json.dumps(bad))
    with pytest.raises(ResultError):
        import_result(p)
    bad2 = copy.deepcopy(doc)
    del bad2["runs"][0]["arms"]["MEAN"]["tau_b"]
    with pytest.raises(ResultError):
        export_result(tmp_path / "x.json", bad2)
    bad3 = copy.deepcopy(doc)
    bad3["simulated"] = False
    with pytest.raises(ResultError):
        export_result(tmp_path / "y.json", bad3)


def test_cli_run_and_report_end_to_end(tmp_path):
    out = tmp_path / "smoke"
    rc = cli.main(["run", "--config", str(REPO / "experiments" / "smoke.json"), "--out", str(out), "--quiet"])
    assert rc == 0
    man = json.loads((out / "run_manifest.json").read_text())
    for key in ("config_sha256", "git", "environment", "wall_time_s", "peak_rss_bytes_process", "runs"):
        assert key in man
    assert len(man["runs"]) == 6 and all(t["runtime_s"] > 0 for t in man["runs"])
    assert cli.main(["report", "--dir", str(out)]) == 0
    md = (out / "report.md").read_text()
    assert "EXPLORATORY" in md and "Not a finding" in md
    assert (out / "figures" / "fig_primary_contrast.svg").read_text().startswith("<svg")
    ev = json.loads((out / "evidence_manifest.json").read_text())
    assert ev["results_sha256"] == hashlib.sha256((out / "results.json").read_bytes()).hexdigest()


def test_cli_refuses_unfrozen_confirmatory_config(tmp_path, capsys):
    rc = cli.main(["run", "--config", str(REPO / "experiments" / "EXP-001.json"), "--out", str(tmp_path / "x")])
    assert rc == cli.EXIT_REFUSED
    assert "not frozen" in capsys.readouterr().err
    assert not (tmp_path / "x").exists()


def test_cli_refuses_by_registered_id(tmp_path):
    assert cli.main(["run", "--exp", "EXP-002", "--out", str(tmp_path / "y")]) == cli.EXIT_REFUSED
    assert not (tmp_path / "y").exists()


def test_repository_protocols_are_not_frozen():
    for exp in ("EXP-001", "EXP-002", "EXP-003"):
        assert protocol_frozen(exp)[0] is False


def test_protocol_frozen_detects_a_recorded_hash(tmp_path):
    (tmp_path / "research" / "experiments" / "EXP-009").mkdir(parents=True)
    proto = tmp_path / "research" / "experiments" / "EXP-009" / "protocol.md"
    proto.write_text("frozen text\n")
    h = hashlib.sha256(proto.read_bytes()).hexdigest()
    reg = tmp_path / "research" / "experiment_registry.csv"
    reg.write_text(f"exp_id,protocol_hash\nEXP-009,{h}\n")
    log = tmp_path / "research" / "decision_log.md"
    log.write_text("no hash yet\n")
    assert protocol_frozen("EXP-009", tmp_path)[0] is False
    log.write_text(f"owner froze EXP-009 at {h}\n")
    assert protocol_frozen("EXP-009", tmp_path)[0] is True
    proto.write_text("edited after freeze\n")
    assert protocol_frozen("EXP-009", tmp_path)[0] is False


def test_bootstrap_summaries_hand():
    import numpy as np

    iv = summarise_diffs(np.array([0.01, 0.02, 0.03]))
    assert iv.mean == pytest.approx(0.02) and iv.sd == pytest.approx(0.01)
    assert iv.boot_lo >= 0.01 and iv.boot_hi <= 0.03
    const = summarise_diffs(np.array([0.5, 0.5]))
    assert const.boot_lo == const.boot_hi == 0.5
    pooled = pooled_stratified({"a": np.array([1.0, 1.0]), "b": np.array([3.0, 3.0])})
    assert pooled["dbar"] == 2.0 and pooled["lo95"] == pooled["hi95"] == 2.0
    assert seeds_for_half_width(0.05, 0.02) == 25
    assert seeds_for_half_width(0.0, 0.02) is None
