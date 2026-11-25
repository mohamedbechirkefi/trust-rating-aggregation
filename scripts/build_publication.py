# SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
"""Build the publication PDFs and regenerate manuscript.tex (M6).

Outputs (Markdown stays canonical; decision D-002):
  research/paper/manuscript.pdf, research/paper/supplementary.pdf,
  research/experiments/EXP-00N/report.pdf, research/paper/manuscript.tex (not compiled; no TeX).

Usage: PYTHONPATH=src .venv/bin/python scripts/build_publication.py [--png-dir DIR]
``--png-dir`` also renders every page to PNG there (outside the repository, for inspection).
"""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from trust.report import PANDOC, build_pdf, pandoc_publication_args, publication_source

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research"
BIB = RESEARCH / "paper" / "references.bib"
DOCS = [
    ("manuscript", RESEARCH / "paper" / "manuscript.md"),
    ("supplementary", RESEARCH / "paper" / "supplementary.md"),
    ("EXP-001", RESEARCH / "experiments" / "EXP-001" / "report.md"),
    ("EXP-002", RESEARCH / "experiments" / "EXP-002" / "report.md"),
    ("EXP-003", RESEARCH / "experiments" / "EXP-003" / "report.md"),
]
TEX_HEADER = ("% SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0\n"
              "% Generated from research/paper/manuscript.md by pandoc 3.6.3; do not edit by hand.\n")


def build_tex() -> Path:
    md = RESEARCH / "paper" / "manuscript.md"
    out = subprocess.run([PANDOC, "-f", "markdown", "-s", "-t", "latex", *pandoc_publication_args(BIB)],
                         input=publication_source(md), check=True, cwd=md.parent,
                         capture_output=True, text=True).stdout
    tex = md.with_suffix(".tex")
    tex.write_text(TEX_HEADER + out, encoding="utf-8")
    return tex


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--png-dir", type=Path, default=None)
    args = ap.parse_args()
    for _name, md in DOCS:
        pdf = md.with_suffix(".pdf")
        build_pdf(md, pdf, bibliography=BIB, publication=True, root=RESEARCH, png_dir=args.png_dir)
        print(f"built {pdf.relative_to(ROOT)} ({pdf.stat().st_size} bytes)")
    print(f"wrote {build_tex().relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
