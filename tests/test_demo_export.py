# SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
"""M5 consistency (master prompt 11.6): the demo shows the manuscript's numbers, verbatim.

1. Re-running the export in memory gives the committed ``demo/public/data/results.json`` byte for byte.
2. Every ``display`` and ``interval_display`` string of an experiment estimate appears verbatim in
   ``research/paper/manuscript.md``, except the documented exceptions below, which must then appear
   verbatim in ``research/paper/supplementary.md``.
3. Every figure row's display strings appear in the manuscript or the supplement (per-cell
   intervals are printed only in supplementary Table S2, as the manuscript says).
4. Every source hash in the export matches the file on disk, and every claim id exists.
"""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = (ROOT / "research" / "paper" / "manuscript.md").read_text(encoding="utf-8")
SUPPLEMENT = (ROOT / "research" / "paper" / "supplementary.md").read_text(encoding="utf-8")
COMMITTED = ROOT / "demo" / "public" / "data" / "results.json"

# Documented exceptions: (experiment id, label prefix, field) -> where the string is printed instead.
SUPPLEMENT_ONLY = {
    ("M4-EXPLORATORY", "E3: D among reviewed products", "interval_display"):
        "E3 intervals are printed in supplementary Table S6; the manuscript body gives the point values only.",
}


def _export_module():
    spec = importlib.util.spec_from_file_location("export_demo_data", ROOT / "scripts" / "export_demo_data.py")
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def _committed() -> dict:
    return json.loads(COMMITTED.read_text(encoding="utf-8"))


def test_export_is_reproduced_exactly():
    mod = _export_module()
    assert mod.render(mod.build()) == COMMITTED.read_text(encoding="utf-8")


def test_export_has_no_timestamp_and_the_template_schema():
    data = _committed()
    assert data["schema"] == "lab-demo-results" and data["schema_version"] == "1.0.0"
    text = COMMITTED.read_text(encoding="utf-8")
    assert "generated_at" not in text and "timestamp" not in text
    assert len(data["code_revision"]) == 40


def test_every_registered_experiment_is_exported():
    with (ROOT / "research" / "experiment_registry.csv").open(encoding="utf-8", newline="") as fh:
        registered = [r["exp_id"] for r in csv.DictReader(fh)]
    ids = [e["id"] for e in _committed()["experiments"]]
    assert ids[: len(registered)] == registered
    for e in _committed()["experiments"]:
        assert e["status"] and e["verdict"]


def _exception(exp_id: str, label: str, field: str) -> str | None:
    for (eid, prefix, f), note in SUPPLEMENT_ONLY.items():
        if eid == exp_id and label.startswith(prefix) and f == field:
            return note
    return None


def test_estimate_strings_appear_verbatim_in_the_manuscript():
    missing = []
    for e in _committed()["experiments"]:
        for x in e["estimates"]:
            for field in ("display", "interval_display"):
                s = x[field]
                if s is None or s in MANUSCRIPT:
                    continue
                if _exception(e["id"], x["label"], field) and s in SUPPLEMENT:
                    continue
                missing.append((e["id"], x["label"], field, s))
    assert missing == []


def test_documented_exceptions_are_used():
    used = set()
    for e in _committed()["experiments"]:
        for x in e["estimates"]:
            for key in SUPPLEMENT_ONLY:
                if e["id"] == key[0] and x["label"].startswith(key[1]) and x[key[2]] not in MANUSCRIPT:
                    used.add(key)
    assert used == set(SUPPLEMENT_ONLY)


def test_figure_strings_appear_in_the_manuscript_or_supplement():
    missing = []
    for f in _committed()["figures"]:
        for r in f["rows"]:
            for field in ("display", "interval_display"):
                s = r[field]
                if s not in MANUSCRIPT and s not in SUPPLEMENT:
                    missing.append((f["id"], r["label"], field, s))
    assert missing == []


def test_displayed_values_round_to_the_stored_estimates():
    for e in _committed()["experiments"]:
        for x in e["estimates"]:
            assert float(x["display"]) == round(x["estimate"], 4)
            if x["ci_low"] is not None:
                lo, hi = x["interval_display"].split(" to ")
                assert (float(lo), float(hi)) == (round(x["ci_low"], 4), round(x["ci_high"], 4))


def test_source_hashes_and_claim_ids():
    data = _committed()
    for s in data["sources"]:
        assert hashlib.sha256((ROOT / s["path"]).read_bytes()).hexdigest() == s["sha256"], s["path"]
    with (ROOT / "research" / "claims_register.csv").open(encoding="utf-8", newline="") as fh:
        claims = {r["claim_id"] for r in csv.DictReader(fh)}
    for e in data["experiments"]:
        assert set(e["claim_ids"]) <= claims
