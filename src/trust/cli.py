# SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
"""Command-line interface: smoke, run, report, test.

    PYTHONPATH=src uv run --frozen python -m trust.cli smoke
    PYTHONPATH=src uv run --frozen python -m trust.cli run --config experiments/<file>.json
    PYTHONPATH=src uv run --frozen python -m trust.cli report --dir results/exploratory/<name> [--pdf]
    PYTHONPATH=src uv run --frozen python -m trust.cli test

`run` refuses a confirmatory config unless its protocol and the config file itself are frozen
(G-FREEZE; see trust.provenance.config_frozen and research/freeze.json). Exploratory outputs go to results/exploratory/.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

from trust.config import ConfigError, load_config
from trust.provenance import REPO_ROOT, config_frozen, git_revision
from trust.report import build_report
from trust.results import build_manifest, build_result, export_result, now, write_json
from trust.runner import run_experiment

SMOKE_CONFIG = REPO_ROOT / "experiments" / "smoke.json"
EXIT_REFUSED = 3


def output_dir(cfg: dict, config_path: Path, out: str | None) -> Path:
    if out:
        return Path(out)
    if cfg["label"] == "exploratory":
        return REPO_ROOT / "results" / "exploratory" / config_path.stem
    return REPO_ROOT / "results" / "confirmatory" / config_path.stem


def do_run(config_path: Path, out: str | None, quiet: bool, command: str) -> int:
    try:
        cfg = load_config(config_path)
    except (ConfigError, OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if cfg["label"] == "confirmatory":
        ok, why = config_frozen(cfg["exp_id"], config_path)
        if not ok:
            print(f"refused: {cfg['exp_id']} is confirmatory and is not frozen as given ({why}). "
                  "Freezing is the owner's decision (G-FREEZE). Use an exploratory config.", file=sys.stderr)
            return EXIT_REFUSED
    dest = output_dir(cfg, config_path, out)
    git = git_revision()
    started, t0 = now()
    cells, runs, timings = run_experiment(cfg, progress=None if quiet else print)
    wall = time.perf_counter() - t0
    doc = build_result(cfg, cells, runs)
    export_result(dest / "results.json", doc)
    write_json(dest / "run_manifest.json", build_manifest(cfg, timings, started, wall, command, git))
    n_failed = sum(r["status"] != "ok" for r in runs)
    print(f"{cfg['label']}: {len(runs)} runs ({n_failed} failed) in {wall:.2f} s -> {dest}")
    return 0 if n_failed == 0 else 1


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="trust", description="TRUST simulation study (all data simulated)")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("smoke", help="run the exploratory smoke matrix and build its report")
    s.add_argument("--quiet", action="store_true")
    r = sub.add_parser("run", help="run a config (confirmatory configs need a frozen protocol)")
    g = r.add_mutually_exclusive_group(required=True)
    g.add_argument("--config", help="path to a config JSON")
    g.add_argument("--exp", help="registered id, e.g. EXP-001 (reads experiments/<id>.json)")
    r.add_argument("--out")
    r.add_argument("--quiet", action="store_true")
    rep = sub.add_parser("report", help="build tables, figures and report.md from a result directory")
    rep.add_argument("--dir", required=True)
    rep.add_argument("--pdf", action="store_true", help="also build report.pdf (pandoc to Typst)")
    sub.add_parser("test", help="run the pytest suite")
    a = p.parse_args(argv)
    command = "trust " + " ".join(argv if argv is not None else sys.argv[1:])

    if a.cmd == "smoke":
        rc = do_run(SMOKE_CONFIG, None, a.quiet, command)
        if rc == 0:
            cfg = load_config(SMOKE_CONFIG)
            build_report(output_dir(cfg, SMOKE_CONFIG, None))
        return rc
    if a.cmd == "run":
        path = Path(a.config) if a.config else REPO_ROOT / "experiments" / f"{a.exp}.json"
        return do_run(path, a.out, a.quiet, command)
    if a.cmd == "report":
        summ = build_report(Path(a.dir), pdf=a.pdf)
        print(f"report written for {summ['exp_id']} ({summ['label']}) in {a.dir}")
        return 0
    if a.cmd == "test":
        return subprocess.call([sys.executable, "-m", "pytest", "-q", str(REPO_ROOT / "tests")], cwd=REPO_ROOT)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
