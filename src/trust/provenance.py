# SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
"""Run-time provenance: environment, git revision, peak memory, protocol freeze status."""

from __future__ import annotations

import csv
import json
import hashlib
import importlib.metadata
import platform
import re
import resource
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PACKAGES = ("numpy", "scipy", "jsonschema")


def git_revision(root: Path = REPO_ROOT) -> dict:
    def _git(*args: str) -> str:
        return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, check=True).stdout.strip()

    try:
        rev = _git("rev-parse", "HEAD")
        # result outputs under results/ do not count: they are what runs produce
        dirty = bool(_git("status", "--porcelain", "--", ".", ":(exclude)results"))
    except (OSError, subprocess.CalledProcessError):
        return {"revision": None, "dirty": None}
    return {"revision": rev, "dirty": dirty}


def cpu_name() -> str:
    if sys.platform == "darwin":
        try:
            return subprocess.run(
                ["sysctl", "-n", "machdep.cpu.brand_string"], capture_output=True, text=True, check=True
            ).stdout.strip()
        except (OSError, subprocess.CalledProcessError):
            pass
    return platform.processor() or platform.machine()


def environment() -> dict:
    versions = {}
    for p in PACKAGES:
        try:
            versions[p] = importlib.metadata.version(p)
        except importlib.metadata.PackageNotFoundError:
            versions[p] = None
    return {
        "python": platform.python_version(),
        "packages": versions,
        "os": f"{platform.system()} {platform.release()} ({platform.platform()})",
        "cpu": cpu_name(),
        "machine": platform.machine(),
    }


def peak_rss_bytes() -> int:
    """Process-level peak resident set size. ru_maxrss is bytes on macOS and KiB on Linux."""
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(r if sys.platform == "darwin" else r * 1024)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def protocol_frozen(exp_id: str, root: Path = REPO_ROOT) -> tuple[bool, str]:
    """An experiment counts as frozen only if all of these hold:
    its registry row carries a 64-hex protocol_hash, that hash equals the SHA-256 of
    research/experiments/<exp_id>/protocol.md, and research/decision_log.md records the hash.
    Freezing is the owner's decision (G-FREEZE); this function only checks the record.
    """
    reg = root / "research" / "experiment_registry.csv"
    proto = root / "research" / "experiments" / exp_id / "protocol.md"
    log = root / "research" / "decision_log.md"
    if not reg.exists() or not proto.exists():
        return False, f"registry or protocol file for {exp_id} missing"
    with reg.open(newline="", encoding="utf-8") as fh:
        rows = {r["exp_id"]: r for r in csv.DictReader(fh)}
    if exp_id not in rows:
        return False, f"{exp_id} is not registered"
    h = rows[exp_id].get("protocol_hash", "").strip().lower()
    if not re.fullmatch(r"[0-9a-f]{64}", h):
        return False, f"{exp_id} protocol_hash is {h!r} (not frozen)"
    if sha256_file(proto) != h:
        return False, f"{exp_id} protocol file no longer matches its recorded hash"
    if not log.exists() or h not in log.read_text(encoding="utf-8"):
        return False, f"{exp_id} freeze hash is not recorded in research/decision_log.md"
    return True, "frozen"


FREEZE_RECORD = Path("research") / "freeze.json"


def config_frozen(exp_id: str, config_path: Path, root: Path = REPO_ROOT) -> tuple[bool, str]:
    """A confirmatory config may run only if all of these hold (round-2 freeze, 2026-11-24):
    protocol_frozen(exp_id) holds; research/freeze.json exists; the SHA-256 of research/protocol.md
    and of data/manifest.json equal the values recorded there; and the config file, as a path
    relative to the repository, is listed under exp_id with a SHA-256 equal to its current bytes.
    A changed, unlisted or out-of-repository config is refused."""
    ok, why = protocol_frozen(exp_id, root)
    if not ok:
        return ok, why
    rec_path = root / FREEZE_RECORD
    if not rec_path.exists():
        return False, "research/freeze.json missing"
    rec = json.loads(rec_path.read_text(encoding="utf-8"))
    study = rec.get("study_protocol", {})
    if sha256_file(root / study.get("path", "research/protocol.md")) != study.get("sha256"):
        return False, "research/protocol.md no longer matches the freeze record"
    dm = rec.get("data_manifest", {})
    if dm and sha256_file(root / dm["path"]) != dm.get("sha256"):
        return False, "data/manifest.json no longer matches the freeze record"
    try:
        rel = Path(config_path).resolve().relative_to(Path(root).resolve()).as_posix()
    except ValueError:
        return False, f"config {config_path} is outside the repository"
    exp = rec.get("experiments", {}).get(exp_id, {})
    expected = exp.get("configs", {}).get(rel)
    if expected is None:
        return False, f"config {rel} is not listed for {exp_id} in the freeze record"
    if sha256_file(root / rel) != expected:
        return False, f"config {rel} has changed since the freeze"
    return True, "frozen"
