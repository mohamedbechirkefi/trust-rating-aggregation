# SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
"""Result serialisation: versioned JSON schema validated at export and import, run manifest."""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path

import jsonschema

from trust import RESULT_SCHEMA_VERSION, __version__
from trust.config import config_hash, load_schema
from trust.provenance import environment, git_revision, peak_rss_bytes


class ResultError(ValueError):
    """Raised when a result document does not match the schema (fail closed)."""


def validate_result(doc: dict) -> dict:
    try:
        jsonschema.validate(doc, load_schema("result-v1.json"))
    except jsonschema.ValidationError as exc:
        raise ResultError(f"result does not match schema {RESULT_SCHEMA_VERSION}: {exc.message}") from exc
    ids = [r["run_id"] for r in doc["runs"]]
    if len(set(ids)) != len(ids):
        raise ResultError("duplicate run ids")
    if doc["config_sha256"] != config_hash(doc["config"]):
        raise ResultError("config_sha256 does not match the embedded config")
    return doc


def build_result(cfg: dict, cells: list[dict], runs: list[dict]) -> dict:
    return {
        "schema_version": RESULT_SCHEMA_VERSION,
        "exp_id": cfg["exp_id"],
        "label": cfg["label"],
        "simulated": True,
        "config": cfg,
        "config_sha256": config_hash(cfg),
        "cells": cells,
        "runs": runs,
    }


def write_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=1, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")


def export_result(path: Path, doc: dict) -> None:
    validate_result(doc)
    write_json(path, doc)


def import_result(path: Path) -> dict:
    return validate_result(json.loads(Path(path).read_text(encoding="utf-8")))


def build_manifest(cfg: dict, timings: list[dict], started: datetime, wall_s: float, command: str) -> dict:
    """One manifest per invocation, with a per-run entry (run id, seed, start time, runtime)."""
    return {
        "manifest_version": "1.0",
        "exp_id": cfg["exp_id"],
        "label": cfg["label"],
        "config_sha256": config_hash(cfg),
        "seed_root": cfg["seed_root"],
        "exp_number": cfg["exp_number"],
        "n_seeds": cfg["n_seeds"],
        "trust_version": __version__,
        "result_schema_version": RESULT_SCHEMA_VERSION,
        "git": git_revision(),
        "environment": environment(),
        "command": command,
        "start_utc": started.isoformat(),
        "end_utc": datetime.now(timezone.utc).isoformat(),
        "wall_time_s": wall_s,
        "peak_rss_bytes_process": peak_rss_bytes(),
        "peak_memory_note": "process-level peak resident set size from getrusage; not per run",
        "runs": timings,
    }


def now() -> tuple[datetime, float]:
    return datetime.now(timezone.utc), time.perf_counter()
