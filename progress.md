<!-- SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0 -->
# Progress journal (append-only)

## 2026-11-24: Session M0 (bootstrap, feasibility, M1 drafts)

**Milestone:** M0, plus the M1 drafts M0 asks for. **Actor:** AI assistant, under the owner's brief. No confirmatory work.

### Starting state

`git status`: on branch `main`, "nothing to commit, working tree clean". One commit, `008a17e` (master prompt and the owner's licence package). `master_prompt.md` was read in full and not edited.

### Commands run and actual outputs (feasibility audit)

| Command | Output |
|---|---|
| `sysctl -n machdep.cpu.brand_string hw.ncpu hw.memsize` | `Apple M1 Pro`, `10`, `17179869184` |
| `sw_vers` | macOS 15.3.1, build 24D70 |
| `df -h /Users/bechir/research/labs` | 460Gi size, 311Gi used, 128Gi available |
| `/usr/local/bin/python3 --version` | Python 3.12.1 |
| `.tools/py/bin/uv --version` | uv 0.9.5 (d5f39331a 2025-10-21) |
| `importlib.metadata.version` for typst, pypdf, pillow | 0.15.0, 6.20.0, 11.3.0 (no `typst` CLI binary; Python package only) |
| `.tools/pandoc --version` | pandoc 3.6.3 |
| `helix/.tools/node/bin/node --version` (read-only) | v22.23.3 |
| `git --version` | git version 2.42.1 |
| TeX | none installed (per brief; not searched further) |

### Literature and data search

Web search and page fetches on 2026-11-24. Opened: Miller 2009, 2012, 2014; Efron and Morris 1975 (first page); Hu, Pavlou and Zhang 2007 working paper (title page and abstract); Li and Hitt 2008 abstract; Algolia Bayesian average documentation; MIT News article on Muchnik et al. 2013; MovieLens ML-25M README and dataset page; Hugging Face licence discussion for Amazon Reviews 2023. Failed (HTTP 403 or unreadable): ACM CACM pages, Science page, Taylor and Francis page, PubMed (cookie wall), scanned Wilson 1927 PDF. Those are labelled metadata-only or unverified in `research/literature_review.md`. No dataset was downloaded.

### Toolchain smoke check (exploratory, journal JRN-0001)

1. `pandoc research/paper/manuscript.md -s -t typst` then `typst.compile(...)`: **failed** with `typst.TypstError: font fallback list must not be empty` (pandoc's Typst template emits an empty font list when no main font is set).
2. Retried with `-V mainfont="Libertinus Serif"`: compile succeeded; pypdf reports 1 page with extractable text; page rendered to PNG at 60 ppi and inspected visually (headings render correctly). PDF SHA-256 `44c1f977152aae7008bb0d7dc204519779ab8c99174610872ce70386e964a700`, kept in the session scratch directory only and not committed (it is a skeleton, not a manuscript).
3. `pandoc research/paper/manuscript.md -s -t latex` with an SPDX comment prepended: wrote `research/paper/manuscript.tex` (not compiled; no TeX).

### Dependency lock

- `uv lock --python /usr/local/bin/python3`: "Resolved 15 packages in 186ms". `exclude-newer = 2026-11-10T00:00:00Z`; the newest upload time in `uv.lock` is 2026-10-15T09:50:58Z.
- `uv sync --frozen --python /usr/local/bin/python3`: installed the 15 locked packages into `.venv/` (git-ignored).
- `uv run --frozen python -c "import numpy, scipy, jsonschema"`: printed `2.3.4 1.16.2 4.25.1` (plus a jsonschema deprecation warning about `__version__`).

### Decisions

D-001 licence (owner), D-002 zero-cost toolchain, D-003 synthetic primary data, D-004 protocol draft v0.1, D-005 dependency pinning, D-006 stack sequencing. See `research/decision_log.md`.

### Files created or changed

Created: `CLAUDE.md`, `roadmap.md`, `progress.md`, `README.md`, `CITATION.cff`, `pyproject.toml`, `uv.lock`, `research/{decision_log.md, literature_review.md, protocol.md, limitations.md, claims_register.csv, experiment_journal.jsonl, experiment_registry.csv}`, `research/experiments/EXP-00{1,2,3}/protocol.md`, `research/paper/{manuscript.md, manuscript.tex, references.bib, supplementary.md, figures/README.md}`, `research/publication/{artifact_manifest.json, claims_audit.md, reproducibility_report.md, author_review.md, release_checklist.md}`, `data/manifest.json`, READMEs in `results/`, `src/`, `tests/`, `experiments/`, `demo/`, `articles/`. Changed: `CONTRIBUTING.md` (appended section 6, development commands). Licence files untouched.

### Not done, and why

- No tests: there is no code yet (M2). No test count is claimed.
- No smoke run of the simulation: the engine does not exist yet. The sample-size numbers in the protocol are planning assumptions.
- No `package.json`: the demo is not set up (D-006).
- Wilson 1927, Hu et al. 2009 (CACM) and Muchnik et al. 2013 full texts not read (access blocked); labelled accordingly.

### Outstanding risks

- Protocol freeze pending (G-FREEZE); all later runs are exploratory until then.
- The selection model's form is an assumption; results may be sensitive to it (EXP-003 S3 partly addresses this).
- The literature search is scoping only; novelty is not claimed.
- Real datasets: MovieLens not redistributable, Amazon 2023 licence unassigned, Yelp terms unverified.

### Next action

M2: implement the simulation and the MEAN baseline with tests (empty reviews, one review, bounded ratings), then SHRINK and LCB with hand-computed posterior checks; then the exploratory smoke matrix to measure runtime and the SD of the primary contrast, and report it to the owner before the freeze.
