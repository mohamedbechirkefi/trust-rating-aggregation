<!-- SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0 -->
# Reproducibility report (M6)

Status (2026-11-25, M6): every item below was run in this session; the outputs are the actual outputs. Brief: `labs/_shared/M6-brief.md`; authority: owner, 2026-11-25, "Next" (second). Machine: Apple M1 Pro, macOS 15.3.1 (Darwin 24.3.0), Python 3.12.1, Node v22.23.3. At most two workers; every command here is single-process.

- [x] Clean clone into a separate directory (command and output recorded).
- [x] `uv sync --frozen` from `uv.lock` (output recorded).
- [x] Test suite run (actual counts recorded).
- [x] Smoke reproduction matches committed smoke results within the documented tolerance.
- [x] Demo builds offline.
- [x] Data manifest and links verified.
- [x] Secret and licence scan.

## 1. Clean clone (revision a5f3abf, before any M6 change)

`<scratch>` is the session scratch directory outside the repository; the clone was deleted at the end of the session.

| Command (in `<scratch>/clone` unless stated) | Actual output |
|---|---|
| `git clone -q <repository> <scratch>/clone` | no output; `git log --oneline -1`: `a5f3abf M5 follow-up: Medium and LinkedIn article drafts from verified manuscript numbers` |
| `../.tools/py/bin/uv sync --frozen --all-groups --all-extras` | created `.venv`, installed the locked set (last lines: `+ pytest==8.4.2`, `+ referencing==0.37.0`, `+ rpds-py==2026.9.1`, `+ scipy==1.16.2`, `+ typing-extensions==4.16.0`) |
| `.venv/bin/python -m pytest -q` | `173 passed in 74.21s` (first run in a fresh environment; the working repository runs the same suite in about 5 s) |
| `PYTHONPATH=src .venv/bin/python -m trust.cli smoke` (README quick start) | `exploratory: 6 runs (0 failed) in 0.02 s` |
| `git status --short` after the smoke run | 4 files modified: `results/exploratory/smoke/{evidence_manifest.json, report.md, run_manifest.json, summary.json}`; `metrics.csv` and `results.json` byte-identical |
| `git checkout -q -- results/exploratory/smoke` | restored the clone's committed smoke output |
| `cd demo && npm ci --prefer-offline` | `added 53 packages in 1s` |
| `npm test` | `Test Files 2 passed (2)`, `Tests 28 passed (28)` |
| `npm run build` | `built in 359ms` (`dist/assets/index-B0avgoZT.js 249.57 kB`) |
| `node tools/a11y_check.mjs dist` | 14 PASS lines, then `A11Y-CHECK PASS` (results render: 4 experiment panels; contrast in both schemes; keyboard 25 of 25, 34 of 34 with sandbox output; visible focus; 360 px overflow 0px; 0 running animations; no request leaves the local origin; offline after first load) |
| `.venv/bin/python scripts/export_demo_data.py` | `wrote demo/public/data/results.json`; `git status --short`: 0 lines (deterministic) |

**Smoke tolerance.** The smoke reproduction is exact for every simulated value: `results.json` (all per-run metrics, SHA-256 `8fe78903...`) and `metrics.csv` are byte-identical to the committed files. The differences in the other four files are only provenance and timing: the git revision (`e1ad9bb` committed, `a5f3abf` in the clone), the start and end times, per-run runtimes (mean 2.26 ms committed, 2.57 ms in the clone), peak RSS (89.1 MiB against 92.5 MiB), the recorded command (`trust run --config experiments/smoke.json --quiet` against `trust smoke`) and, in `summary.json`, an empty `"per_sigma": {}` key that the M3 analysis code adds when a config has a single noise level. Every statistic present in both summaries is equal. Finding R1: the committed smoke summary predates the `per_sigma` key; harmless, not changed (exploratory output, regenerating it would only refresh timings).

## 2. Data manifest and artifact manifest

| Check | Command | Result |
|---|---|---|
| MovieLens 1M hashes in `data/manifest.json` | `shasum -a 256 data/raw/ml-1m.zip data/raw/ml-1m/*` (working repository; `data/raw/` is git-ignored and absent from a clean clone, fetched by `scripts/download_movielens.py`) | 4 of 4 equal (zip `a6898adb...`, `ratings.dat` `506d64ca...`, `movies.dat` `0140fc23...`, `README` `2d5ddce8...`) |
| Frozen files | `PYTHONPATH=src .venv/bin/python scripts/audit_evidence.py` | `freeze hashes: 12 files, 0 mismatches`; `generated artifacts: 20 files, 0 mismatches`; `checksums: 70 files, 0 mismatches`; re-analysis of EXP-001, EXP-002 and EXP-003: 0 differences each; run counts 1,560 of 1,560 ok |
| Paths in `research/publication/artifact_manifest.json` | inline Python: every `result_path` and `generator` path exists; every config and protocol SHA-256 recomputed | 15 paths, 0 missing; 32 hashes, 0 mismatched; study protocol SHA-256 equal |

## 3. Links and numbers

| Check | Command | Result |
|---|---|---|
| Relative links in tracked Markdown | `.venv/bin/python scripts/check_links.py` (new; tested by `tests/test_release_checks.py`) | `53 Markdown files; 22 relative links, 0 in-page anchors, 0 external links (not fetched)`, `LINK-CHECK PASS` |
| Paths written in code spans (not links) | one-off scan of 331 backticked repository paths | 14 not found on disk, all intended: `EXP-NNN` patterns (6), git-ignored folders (`data/processed/`, `results/raw/`), paths relative to another folder (`schemas/...` under `src/trust/`, `figures/`), the shared template outside the repository; none needed a change |
| Numbers in README and articles | `tests/test_release_checks.py::test_public_text_numbers_in_manuscript` | every decimal and comma-grouped number in `README.md` (29), `articles/medium.md` (40), `articles/linkedin.md` (9) and `articles/README.md` (1) appears verbatim in the manuscript |
| Numbers in the demo | `tests/test_demo_export.py` (M5) | passes |

## 4. PDFs

Built with `PYTHONPATH=src .venv/bin/python scripts/build_publication.py --png-dir <scratch>/png` (pandoc 3.6.3 to Typst, `typst` Python package 0.15.0; decision D-002). Every manuscript page and the first and figure pages of each report were rendered to PNG at 60 ppi and inspected; the figure pages were also checked at 150 ppi.

| File | Pages | Bytes |
|---|---|---|
| `research/paper/manuscript.pdf` | 13 | 219,036 |
| `research/paper/supplementary.pdf` | 6 | 140,602 |
| `research/experiments/EXP-001/report.pdf` | 7 | 145,206 |
| `research/experiments/EXP-002/report.pdf` | 6 | 136,590 |
| `research/experiments/EXP-003/report.pdf` | 6 | 124,547 |

PDF metadata (pypdf): each title is the document's first heading; no author e-mail, no local path in metadata or text. Fixes found by inspection, all in the builder, none in a PDF: the title rendered as a plain paragraph (the SPDX comment preceded the heading), `[@key]` citations failed (Typst bibliography not found), "Figure 1: Figure 1 (FIG-001)" doubled numbering, and table columns of equal width with justified, hyphenated cells. `research/paper/manuscript.tex` is regenerated by the same script (not compiled; no TeX distribution).

## 5. Scans

See `research/publication/release_checklist.md` (secrets and identifiers) and `research/publication/dependency_licences.md` (licences).
