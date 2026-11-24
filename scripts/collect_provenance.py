# SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
"""Collect the run-time provenance of the confirmatory runs into one table, and a SHA-256 manifest
of every file under results/confirmatory/ (M3).

    PYTHONPATH=src .venv/bin/python scripts/collect_provenance.py

Reads each results/confirmatory/<config>/run_manifest.json and results.json (written at run time);
adds the frozen config file SHA-256 and the data manifest SHA-256 from research/freeze.json, the
CLI exit status from results/confirmatory/logs/<config>.log, and writes
results/confirmatory/provenance.csv and results/confirmatory/SHA256SUMS.
"""

from __future__ import annotations

import csv
import json
from datetime import datetime, timedelta

from trust.provenance import REPO_ROOT, sha256_file

CONF = REPO_ROOT / "results" / "confirmatory"


def main() -> int:
    freeze = json.loads((REPO_ROOT / "research" / "freeze.json").read_text(encoding="utf-8"))
    dm_sha = freeze["data_manifest"]["sha256"]
    cfg_sha = {p: h for e in freeze["experiments"].values() for p, h in e["configs"].items()}
    rows = []
    for d in sorted(p for p in CONF.iterdir() if p.is_dir() and (p / "run_manifest.json").exists()):
        man = json.loads((d / "run_manifest.json").read_text(encoding="utf-8"))
        res = json.loads((d / "results.json").read_text(encoding="utf-8"))
        status = {r["run_id"]: (r["status"], r["attempts"], r["seed_index"]) for r in res["runs"]}
        cfg_path = f"experiments/{d.name}.json"
        log = (CONF / "logs" / f"{d.name}.log").read_text(encoding="utf-8").splitlines()
        cli_ok = bool(log) and "(0 failed)" in log[-1]
        hw = f"{man['environment']['cpu']}; {man['environment']['os']}"
        for t in man["runs"]:
            start = datetime.fromisoformat(t["start_utc"])
            st, att, seed = status[t["run_id"]]
            rows.append({
                "config": cfg_path, "run_id": t["run_id"], "seed_index": seed,
                "config_file_sha256": cfg_sha[cfg_path], "config_canonical_sha256": man["config_sha256"],
                "frozen_config_sha256_matches_file": sha256_file(REPO_ROOT / cfg_path) == cfg_sha[cfg_path],
                "git_revision": man["git"]["revision"], "git_dirty": man["git"]["dirty"],
                "data_manifest_sha256": dm_sha, "hardware": hw,
                "start_utc": t["start_utc"], "end_utc": (start + timedelta(seconds=t["runtime_s"])).isoformat(),
                "runtime_s": t["runtime_s"], "status": st, "attempts": att,
                "invocation_exit_ok": cli_ok,
            })
    with (CONF / "provenance.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    files = sorted(p for p in CONF.rglob("*") if p.is_file() and p.name != "SHA256SUMS")
    (CONF / "SHA256SUMS").write_text(
        "".join(f"{sha256_file(p)}  {p.relative_to(CONF).as_posix()}\n" for p in files), encoding="utf-8")
    print(f"{len(rows)} runs; {sum(r['status'] == 'ok' for r in rows)} ok; {len(files)} files hashed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
