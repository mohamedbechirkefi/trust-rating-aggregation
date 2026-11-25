# SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
"""Evidence audit (master prompt 11.5): checks committed results against the documents.

    PYTHONPATH=src .venv/bin/python scripts/audit_evidence.py

1. Checksums: every line of results/confirmatory/SHA256SUMS matches the file on disk.
2. Re-analysis: the frozen analysis (trust.hypotheses) is recomputed in memory from the committed
   result files and compared with results/confirmatory/analysis/EXP-00N.json (numbers within 1e-12).
3. Sample counts: runs, ok and failed per result file, against the planned matrix (cells x seeds).
4. Number trace: every decimal number in the publication documents must appear, at the printed
   precision, in a committed source (generated tables, generated per-run reports, run manifests,
   analysis JSON, the calibration record, the protocol, the M4 exploratory output).
   Unmatched numbers are listed for manual review; they are not silently accepted. This check is
   weak on its own (many short decimals occur somewhere in the sources by chance; the measured
   chance-match rate is recorded in the output), so it is complemented by check 5.
5. Interval trace (strict): every "estimate (lo to hi)" or "estimate | lo to hi" triple printed at
   four decimals in the documents must equal a (point, lower, upper) triple of the analysis JSON or
   the M4 exploratory JSON, rounded to four decimals.

Writes research/publication/evidence_audit.json. Changes nothing else.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from trust.hypotheses import analyse_exp001, analyse_exp002, analyse_exp003, clean
from trust.provenance import REPO_ROOT, git_revision
from trust.results import import_result

CONF = REPO_ROOT / "results" / "confirmatory"
STEMS = ["EXP-001", "EXP-002", "EXP-003-S1-min1", "EXP-003-S1-min5", "EXP-003-S2", "EXP-003-S3", "EXP-003-S4"]
TARGETS = [
    "research/experiments/EXP-001/report.md",
    "research/experiments/EXP-002/report.md",
    "research/experiments/EXP-003/report.md",
    "research/paper/manuscript.md",
    "research/paper/supplementary.md",
    "research/claims_register.csv",
    "research/limitations.md",
]
TEXT_SOURCES = [
    "research/experiments/EXP-001/results_tables.md",
    "research/experiments/EXP-002/results_tables.md",
    "research/experiments/EXP-003/results_tables.md",
    "results/exploratory/m4-sensitivity/m4_exploratory.md",
    "research/protocol.md",
    "research/experiments/EXP-001/protocol.md",
    "research/experiments/EXP-002/protocol.md",
    "research/experiments/EXP-003/protocol.md",
    "research/freeze.json",
] + [f"results/confirmatory/{s}/report.md" for s in STEMS]
JSON_SOURCES = (
    [f"results/confirmatory/analysis/{e}.json" for e in ("EXP-001", "EXP-002", "EXP-003")]
    + ["data/calibration/movielens-1m-fit.json", "results/exploratory/m4-sensitivity/m4_exploratory.json",
       "results/exploratory/metric-validation/validation.json"]
)
TRIPLE_DOC = [re.compile(r"(-?\d+\.\d{4}) \((?:95% )?(-?\d+\.\d{4}) to (-?\d+\.\d{4})\)"),
              re.compile(r"(-?\d+\.\d{4}) \| (-?\d+\.\d{4}) to (-?\d+\.\d{4})")]
POINT_KEYS = ("Dbar", "dbar", "estimate", "mean")
LO_KEYS = ("lo95", "boot_lo")
HI_KEYS = ("hi95", "boot_hi")
NUM = re.compile(r"(?<![\w.])-?\d+\.\d+(?![\w.])")


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def check_freeze() -> dict:
    """Every frozen file (study and EXP protocols, configs, data manifest) against research/freeze.json."""
    f = json.loads((REPO_ROOT / "research" / "freeze.json").read_text(encoding="utf-8"))
    pairs = [("research/protocol.md", f["study_protocol"]["sha256"]), ("data/manifest.json", f["data_manifest"]["sha256"])]
    for e, v in f["experiments"].items():
        pairs.append((f"research/experiments/{e}/protocol.md", v["protocol_sha256"]))
        pairs += list(v["configs"].items())
    bad = [rel for rel, h in pairs if sha256(REPO_ROOT / rel) != h]
    return {"files": len(pairs), "mismatches": bad}


def check_sums() -> dict:
    bad, n = [], 0
    for line in (CONF / "SHA256SUMS").read_text().splitlines():
        if not line.strip():
            continue
        h, rel = line.split(None, 1)
        n += 1
        if sha256(CONF / rel.strip()) != h:
            bad.append(rel.strip())
    return {"files": n, "mismatches": bad}


def close(a, b, tol=1e-12) -> list[str]:
    diffs: list[str] = []

    def walk(x, y, path):
        if isinstance(x, dict) and isinstance(y, dict):
            for k in set(x) | set(y):
                if k not in x or k not in y:
                    diffs.append(f"{path}/{k}: key missing")
                else:
                    walk(x[k], y[k], f"{path}/{k}")
        elif isinstance(x, list) and isinstance(y, list):
            if len(x) != len(y):
                diffs.append(f"{path}: length {len(x)} != {len(y)}")
            for i, (u, v) in enumerate(zip(x, y)):
                walk(u, v, f"{path}[{i}]")
        elif isinstance(x, bool) or isinstance(y, bool):
            if x != y:
                diffs.append(f"{path}: {x} != {y}")
        elif isinstance(x, (int, float)) and isinstance(y, (int, float)):
            if abs(x - y) > tol:
                diffs.append(f"{path}: {x} != {y}")
        elif x != y:
            diffs.append(f"{path}: {x!r} != {y!r}")

    walk(a, b, "")
    return diffs


def reanalyse() -> tuple[dict, dict]:
    docs = {s: import_result(CONF / s / "results.json") for s in STEMS}
    fresh = {
        "EXP-001": analyse_exp001(docs["EXP-001"]),
        "EXP-002": analyse_exp002(docs["EXP-002"]),
        "EXP-003": analyse_exp003(docs["EXP-001"], docs["EXP-002"], docs["EXP-003-S1-min1"], docs["EXP-003-S1-min5"],
                                  docs["EXP-003-S2"], docs["EXP-003-S3"], docs["EXP-003-S4"]),
    }
    out = {}
    for e, res in fresh.items():
        committed = json.loads((CONF / "analysis" / f"{e}.json").read_text())
        d = close(json.loads(json.dumps(clean(res))), committed)
        out[e] = {"differences": d[:20], "n_differences": len(d)}
    counts = {}
    for s, doc in docs.items():
        planned = len(doc["cells"]) * doc["config"]["n_seeds"]
        ok = sum(r["status"] == "ok" for r in doc["runs"])
        counts[s] = {"planned": planned, "runs": len(doc["runs"]), "ok": ok, "failed": len(doc["runs"]) - ok,
                     "cells": len(doc["cells"]), "seeds": doc["config"]["n_seeds"]}
    return out, counts


def number_forms(x: float) -> set[str]:
    forms = set()
    for d in range(1, 5):
        s = f"{x:.{d}f}"
        forms.add(s)
        forms.add(s.lstrip("-") if s.startswith("-0.") and float(s) == 0 else s)
    return forms


def harvest_json(o, acc: set[str]) -> None:
    if isinstance(o, dict):
        for v in o.values():
            harvest_json(v, acc)
    elif isinstance(o, list):
        for v in o:
            harvest_json(v, acc)
    elif isinstance(o, float) or (isinstance(o, int) and not isinstance(o, bool)):
        acc |= number_forms(float(o))
    elif isinstance(o, str):
        acc.update(NUM.findall(o))


def source_numbers() -> set[str]:
    acc: set[str] = set()
    for rel in TEXT_SOURCES:
        p = REPO_ROOT / rel
        if p.exists():
            acc.update(NUM.findall(p.read_text(encoding="utf-8")))
    for rel in JSON_SOURCES:
        p = REPO_ROOT / rel
        if p.exists():
            harvest_json(json.loads(p.read_text(encoding="utf-8")), acc)
    return acc


def harvest_triples(o, acc: set[tuple[str, str, str]]) -> None:
    if isinstance(o, dict):
        pt = next((o[k] for k in POINT_KEYS if isinstance(o.get(k), (int, float))), None)
        lo = next((o[k] for k in LO_KEYS if isinstance(o.get(k), (int, float))), None)
        hi = next((o[k] for k in HI_KEYS if isinstance(o.get(k), (int, float))), None)
        if None not in (pt, lo, hi):
            acc.add(tuple(f"{x:.4f}" for x in (pt, lo, hi)))
            if isinstance(o.get("sd"), (int, float)):  # per-cell tables print "SD | lo to hi"
                acc.add(tuple(f"{x:.4f}" for x in (o["sd"], lo, hi)))
        for v in o.values():
            harvest_triples(v, acc)
    elif isinstance(o, list):
        for v in o:
            harvest_triples(v, acc)


def norm0(t: str) -> str:
    return "0.0000" if t == "-0.0000" else t


def interval_trace() -> dict:
    acc: set[tuple[str, str, str]] = set()
    for rel in [f"results/confirmatory/analysis/{e}.json" for e in ("EXP-001", "EXP-002", "EXP-003")] + [
            "results/exploratory/m4-sensitivity/m4_exploratory.json"]:
        harvest_triples(json.loads((REPO_ROOT / rel).read_text(encoding="utf-8")), acc)
    acc = {tuple(norm0(x) for x in t) for t in acc}
    out = {}
    for rel in TARGETS:
        p = REPO_ROOT / rel
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        found = [m.groups() for rx in TRIPLE_DOC for m in rx.finditer(text)]
        bad = sorted({" ".join(t) for t in found if tuple(norm0(x) for x in t) not in acc})
        out[rel] = {"triples": len(found), "unmatched": bad}
    return out


def chance_rate(acc: set[str]) -> dict:
    import random
    rng = random.Random(20261124)
    rate = {}
    for d in (2, 3, 4):
        xs = [f"{rng.uniform(-0.1, 0.1):.{d}f}" for _ in range(2000)]
        rate[f"{d}dp"] = sum(x in acc or x.lstrip("-") in acc for x in xs) / 2000
    return rate


def trace(acc: set[str]) -> dict:
    out = {}
    for rel in TARGETS:
        p = REPO_ROOT / rel
        if not p.exists():
            out[rel] = {"missing_file": True}
            continue
        toks = NUM.findall(p.read_text(encoding="utf-8"))
        unmatched = sorted({t for t in toks if t not in acc and t.lstrip("-") not in acc})
        out[rel] = {"decimal_numbers": len(toks), "unmatched": unmatched}
    return out


def main() -> int:
    git = git_revision()
    sums = check_sums()
    frz = check_freeze()
    re_an, counts = reanalyse()
    acc = source_numbers()
    tr = trace(acc)
    it = interval_trace()
    res = {"interval_trace": it, "number_trace_chance_match_rate_in_[-0.1,0.1]": chance_rate(acc), "generator": "scripts/audit_evidence.py", "git": git, "checksums": sums, "freeze_hashes": frz, "reanalysis": re_an,
           "sample_counts": counts, "number_trace": tr}
    out = REPO_ROOT / "research" / "publication" / "evidence_audit.json"
    out.write_text(json.dumps(res, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(f"freeze hashes: {frz['files']} files, {len(frz['mismatches'])} mismatches")
    print(f"checksums: {sums['files']} files, {len(sums['mismatches'])} mismatches")
    for e, v in re_an.items():
        print(f"reanalysis {e}: {v['n_differences']} differences")
    for s, c in counts.items():
        print(f"counts {s}: {c['runs']}/{c['planned']} runs, {c['ok']} ok, {c['failed']} failed")
    for rel, v in tr.items():
        if v.get("missing_file"):
            print(f"trace {rel}: file missing")
        else:
            print(f"trace {rel}: {v['decimal_numbers']} numbers, {len(v['unmatched'])} unmatched {v['unmatched']}")
    for rel, v in it.items():
        print(f"intervals {rel}: {v['triples']} triples, {len(v['unmatched'])} unmatched {v['unmatched']}")
    print(f"number-trace chance match rate: {res['number_trace_chance_match_rate_in_[-0.1,0.1]']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
