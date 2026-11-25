# SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
"""M6 release checks (master prompt 11.6).

1. Every relative link in the tracked Markdown files resolves (``scripts/check_links.py``), and the
   checker does flag a missing file and a missing heading.
2. Every decimal number and every comma-grouped integer printed in the README and the article
   drafts appears verbatim in ``research/paper/manuscript.md`` (extends the M5 demo check).
"""

from __future__ import annotations

import importlib.util
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
NUMBER = re.compile(r"(?<![\w.])-?\d[\d,]*\.\d+|(?<![\w.])\d{1,3}(?:,\d{3})+")
PUBLIC_TEXTS = ["README.md", "articles/medium.md", "articles/linkedin.md", "articles/README.md"]


def _load_checker():
    spec = importlib.util.spec_from_file_location("check_links", REPO / "scripts" / "check_links.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_repository_links_resolve():
    counts, broken = _load_checker().check(REPO)
    assert counts["files"] > 0 and counts["relative"] > 0
    assert broken == []


def test_checker_flags_broken_links(tmp_path):
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    (tmp_path / "b.md").write_text("# Real heading\n", encoding="utf-8")
    (tmp_path / "a.md").write_text(
        "# Top\n[ok](b.md) [ok2](b.md#real-heading) [self](#top)\n"
        "[gone](missing.md) [bad](b.md#nope) `[code](missing2.md)`\n"
        "```\n[fenced](missing3.md)\n```\n[web](https://example.org)\n", encoding="utf-8")
    subprocess.run(["git", "add", "a.md", "b.md"], cwd=tmp_path, check=True)
    counts, broken = _load_checker().check(tmp_path)
    assert counts == {"files": 2, "relative": 4, "external": 1, "anchor_only": 1}
    assert len(broken) == 2
    assert any("missing.md" in b and "missing file" in b for b in broken)
    assert any("b.md#nope" in b and "no such heading" in b for b in broken)


def test_public_text_numbers_in_manuscript():
    manuscript = (REPO / "research" / "paper" / "manuscript.md").read_text(encoding="utf-8")
    missing = {}
    for rel in PUBLIC_TEXTS:
        tokens = set(NUMBER.findall((REPO / rel).read_text(encoding="utf-8")))
        absent = sorted(t for t in tokens if t not in manuscript)
        if absent:
            missing[rel] = absent
    assert missing == {}
