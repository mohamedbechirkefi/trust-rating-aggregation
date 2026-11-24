# SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
"""Experiment configuration: loading, schema validation, hashing and cell expansion."""

from __future__ import annotations

import copy
import hashlib
import itertools
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import jsonschema

from trust.simulate import CellParams

SCHEMA_DIR = Path(__file__).parent / "schemas"
GRID_KEYS = ("nu", "sigma", "lam", "gamma", "quality")


class ConfigError(ValueError):
    """Raised for invalid configurations."""


def load_schema(name: str) -> dict:
    return json.loads((SCHEMA_DIR / name).read_text(encoding="utf-8"))


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def config_hash(cfg: dict) -> str:
    return hashlib.sha256(canonical_json(cfg).encode("utf-8")).hexdigest()


def validate_config(cfg: dict) -> dict:
    try:
        jsonschema.validate(cfg, load_schema("config-v1.json"))
    except jsonschema.ValidationError as exc:
        raise ConfigError(f"invalid config: {exc.message} at {list(exc.absolute_path)}") from exc
    names = [a["name"] for a in cfg["arms"]]
    if len(set(names)) != len(names):
        raise ConfigError("arm names must be unique")
    if "MEAN" not in names:
        raise ConfigError("the MEAN baseline arm is mandatory")
    for a, b in [cfg["primary_contrast"]]:
        if a not in names or b not in names:
            raise ConfigError("primary_contrast must name configured arms")
    if cfg["evaluation"]["top_k"] > cfg["n_products"]:
        raise ConfigError("top_k must not exceed n_products")
    for key in cfg.get("grid", {}):
        if key in cfg["base"]:
            raise ConfigError(f"grid key {key!r} is also fixed in base")
    for c in expand_cells(cfg):
        c.params.validate()
    return cfg


def load_config(path: str | Path) -> dict:
    cfg = json.loads(Path(path).read_text(encoding="utf-8"))
    return validate_config(cfg)


@dataclass(frozen=True)
class Cell:
    cell_id: str
    values: dict  # the grid values of this cell, JSON-serialisable
    params: CellParams


def expand_cells(cfg: dict) -> list[Cell]:
    """Cartesian product of grid values in a fixed key order; cells are numbered c00, c01, ..."""
    grid = cfg.get("grid", {})
    keys = [k for k in GRID_KEYS if k in grid]
    combos = list(itertools.product(*[grid[k] for k in keys])) if keys else [()]
    cells = []
    for i, combo in enumerate(combos):
        vals = dict(zip(keys, combo))
        merged = copy.deepcopy(cfg["base"])
        merged.update(vals)
        q = merged.get("quality", ["beta", 4.0, 2.0])
        params = CellParams(
            n_products=int(cfg["n_products"]),
            nu=float(merged["nu"]),
            sigma=float(merged["sigma"]),
            lam=float(merged.get("lam", 0.0)),
            gamma=float(merged.get("gamma", 0.0)),
            nb_dispersion=float(merged.get("nb_dispersion", 1.0)),
            quality=(q[0], *[float(x) for x in q[1:]]),
        )
        cells.append(Cell(cell_id=f"c{i:02d}", values=vals, params=params))
    return cells


def run_id(exp_id: str, cell_id: str, seed_index: int) -> str:
    return f"RUN-{exp_id}-{cell_id}-s{seed_index:03d}"
