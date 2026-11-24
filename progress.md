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

## 2026-11-24: Session M2 (core implementation while the freeze is pending)

**Milestone:** M2. **Actor:** AI assistant, under the owner's M2 brief. No confirmatory run; no protocol frozen; nothing pushed.

### Starting state

`git status`: on `main`, clean, HEAD `4d78e8c`. Control files, protocol drafts and registry read in the order of `CLAUDE.md`.

### What was implemented

- `src/trust/`: `model.py` (rating probabilities, `theta`, `theta_rep`, reporting probability, exposure weights), `simulate.py` (seeded catalogues, four child streams), `estimators.py` (MEAN baseline first, then SHRINK(kappa) with optional centre offset, LCB with the exact Dirichlet posterior moments, calibration intervals), `metrics.py` (deterministic ranking with id tie-break, tau-b, Spearman, precision and regret at k, RMSE, coverage, O(N^2) reference tau-b), `config.py` and `schemas/config-v1.json`, `runner.py` (one retry, failures kept), `results.py` and `schemas/result-v1.json` (schema 1.0.0, validated at export and import, fails closed on a config-hash mismatch), `provenance.py` (git revision captured before the run, environment, peak RSS, freeze check), `analysis.py` (paired differences, percentile bootstrap 10,000, t interval, stratified pooled bootstrap), `report.py` (metrics.csv, summary.json, evidence_manifest.json, SVG figure with alt text, report.md, report.pdf), `cli.py` (`smoke`, `run`, `report`, `test`).
- `experiments/`: smoke and two pilot configs (exploratory), and confirmatory configs for EXP-001, EXP-002 and the five EXP-003 sub-analyses.
- Implementation choices where the draft is silent: `research/decision_log.md` D-007.

### Commands run and actual outputs

| Command | Output |
|---|---|
| `.venv/bin/python -m pytest -q` (first run) | `1 failed, 137 passed`. The failure was my own hand calculation in `test_tau_b_basic_cases` (pair (1,3) of the example is discordant: nc = 3, nd = 1, so tau-b = 2/5, not 4/5). The code and the O(N^2) reference both gave 0.4. The test was corrected. |
| `PYTHONPATH=src ... trust.cli report --dir results/exploratory/smoke --pdf` (first attempt) | `CalledProcessError` from pandoc: relative paths were resolved twice because of `cwd`. Fixed by resolving to absolute paths. |
| First PDF inspection (PNG at 70 ppi) | Duplicated figure caption and one table row overprinted at a page break. Fixed: caption from the alt text only, one compact table per contrast. Re-inspected: no overprint. |
| `uv run --frozen pytest -q` (final, at `e3abbe7`, which only changes report.py tool-path defaults after the exploratory outputs were produced at `e1ad9bb`) | `139 passed` |
| `trust.cli run --config experiments/smoke.json` | `exploratory: 6 runs (0 failed)` |
| `trust.cli run --config experiments/pilot-exp001-corners.json` | `exploratory: 40 runs (0 failed) in 0.14 s` |
| `trust.cli run --config experiments/pilot-exp002-lambda.json` | `exploratory: 40 runs (0 failed) in 0.14 s` |
| `trust.cli run --config experiments/EXP-001.json` and `run --exp EXP-003-S4` | `refused: ... is confirmatory and its protocol is not frozen ...`, exit 3 |
| `shasum -a 256 results/exploratory/*/results.json` | smoke `8fe78903...`, pilot-001 `52815070...`, pilot-002 `9dfed331...`; identical across three code revisions (determinism check) |
| pypdf on the three `report.pdf` | 3, 5 and 5 pages; page 1 text contains "EXPLORATORY" |

Run manifests were first written with `dirty: true` because the git state was read after outputs existed; fixed in two small commits (capture before the run; ignore `results/`). The committed manifests record revision `e1ad9bb`, `dirty: false`.

### Exploratory measurements (JRN-0002 to JRN-0004; simulated; not findings)

- Runtime per run at N = 200: mean 3.30 ms and 3.46 ms in the two pilots, max 5.03 ms; process peak RSS about 91 to 93 MiB.
- Projected full matrices: 1,560 runs over all registered configs, about 5 to 8 s of simulation; budget of 30 minutes not binding.
- Per-seed SD of `D = tau_b(SHRINK_5) - tau_b(MEAN)`: 0.0064 to 0.0128 across the four EXP-001 corner cells (planning assumption 0.05). Seeds needed for a 0.02 half-width: 1 to 2; 20 seeds is adequate.
- EXP-002 lambda contrast per-seed SD: 0.0073 to 0.0074 (threshold 0.03 met).
- Degenerate cases: none at N = 200. Zero-review share 0.255 at nu = 3 and 0.034 at nu = 30. Degenerate handling (all-zero catalogue, too few evaluable products) is exercised by tests, not by the pilots.
- Planning-relevant observations, not findings: the sign of `D` differed between sigma levels in the corner pilot; LCB scored below MEAN in every pilot cell; SHRINK interval coverage was about 0.51 at sigma 0.5, nu 3.

### Commits (local only)

`05a4c5b` (engine, tests, configs), `8a331fb` and `e1ad9bb` (manifest dirty-flag fixes), `e3abbe7` (tool-path defaults), then one records commit (this entry, exploratory outputs, registry, decision log, roadmap, README).

### Proposed amendments for the owner

See `research/decision_log.md` D-008 (A1 to A6). The protocol text was not changed.

### Files created or changed

Created: `src/trust/*.py`, `src/trust/schemas/*.json`, `tests/conftest.py`, `tests/test_*.py`, `experiments/*.json`, `results/exploratory/{smoke,pilot-exp001-corners,pilot-exp002-lambda}/`. Changed: `pyproject.toml` (pytest config only; no new dependency), `CONTRIBUTING.md` (development commands), `README.md`, `roadmap.md`, `progress.md`, `src/README.md`, `tests/README.md`, `experiments/README.md`, `results/README.md`, `research/decision_log.md` (D-007, D-008), `research/experiment_journal.jsonl` (JRN-0002 to JRN-0004), `research/experiment_registry.csv` (status column).

### Not done, and why

- No confirmatory run and no protocol hash: G-FREEZE.
- No EXP-NNN report: those follow confirmatory runs (M3).
- No demo: M5.
- The CLI requires `PYTHONPATH=src` because `pyproject.toml` has `package = false`; making the project installable would need a build backend, which was not added.

### Outstanding risks

- Pilot output was seen before the freeze; any amendment adopted from D-008 must be labelled pilot-informed.
- The equal-weight `Dbar` may be near zero because of sign heterogeneity across sigma; the primary test may end "not supported".

### Next action

The owner reviews D-008 and freezes the protocols (hash in this log and the registry). Then M3: `trust.cli run --exp EXP-001`, `EXP-002`, `EXP-003-S*`, with reports.
