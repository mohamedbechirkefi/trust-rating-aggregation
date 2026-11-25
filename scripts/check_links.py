# SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
"""Check that every relative link in the tracked Markdown files resolves (M6).

A link is ``[text](target)`` or ``![alt](target)`` outside code spans and fenced code blocks.
External links (``http``, ``https``, ``mailto``) are not fetched; they are counted only. A
relative target must name an existing file or directory, relative to the linking file; a
``#fragment`` must match a heading of the target Markdown file (GitHub-style slug).

Usage: .venv/bin/python scripts/check_links.py   (exit status 1 on any broken link)
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"!?\[(?:[^\[\]]|\[[^\]]*\])*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
FENCE = re.compile(r"^\s*(```|~~~)")
CODE_SPAN = re.compile(r"`+[^`]*`+")
EXTERNAL = ("http://", "https://", "mailto:")


def tracked_markdown(root: Path = ROOT) -> list[Path]:
    out = subprocess.run(["git", "ls-files", "*.md"], cwd=root, check=True,
                         capture_output=True, text=True).stdout.split()
    return [root / p for p in out if "node_modules/" not in p]


def slug(heading: str) -> str:
    """GitHub-style anchor: lower case, punctuation removed, spaces to hyphens."""
    text = re.sub(r"[`*_]", "", heading.strip().lower())
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def anchors(md: Path) -> set[str]:
    seen: dict[str, int] = {}
    result: set[str] = set()
    in_fence = False
    for line in md.read_text(encoding="utf-8").splitlines():
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        m = re.match(r"^#{1,6}\s+(.*?)\s*#*\s*$", line)
        if m and not in_fence:
            base = slug(m.group(1))
            n = seen.get(base, 0)
            result.add(base if n == 0 else f"{base}-{n}")
            seen[base] = n + 1
    return result


def links(md: Path) -> list[tuple[int, str]]:
    found: list[tuple[int, str]] = []
    in_fence = False
    for i, line in enumerate(md.read_text(encoding="utf-8").splitlines(), start=1):
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for m in LINK.finditer(CODE_SPAN.sub("", line)):
            found.append((i, m.group(1)))
    return found


def check(root: Path = ROOT) -> tuple[dict[str, int], list[str]]:
    counts = {"files": 0, "relative": 0, "external": 0, "anchor_only": 0}
    broken: list[str] = []
    for md in tracked_markdown(root):
        counts["files"] += 1
        for line, target in links(md):
            where = f"{md.relative_to(root)}:{line}: {target}"
            if target.startswith(EXTERNAL):
                counts["external"] += 1
                continue
            path_part, _, frag = target.partition("#")
            if not path_part:
                counts["anchor_only"] += 1
                if frag and frag not in anchors(md):
                    broken.append(f"{where} (no such heading)")
                continue
            counts["relative"] += 1
            dest = (md.parent / unquote(path_part)).resolve()
            if not dest.exists():
                broken.append(f"{where} (missing file)")
            elif frag and dest.suffix == ".md" and frag not in anchors(dest):
                broken.append(f"{where} (no such heading)")
    return counts, broken


def main() -> int:
    counts, broken = check()
    print(f"{counts['files']} Markdown files; {counts['relative']} relative links, "
          f"{counts['anchor_only']} in-page anchors, {counts['external']} external links (not fetched)")
    for b in broken:
        print("BROKEN", b)
    print("LINK-CHECK PASS" if not broken else f"LINK-CHECK FAIL ({len(broken)})")
    return 0 if not broken else 1


if __name__ == "__main__":
    sys.exit(main())
