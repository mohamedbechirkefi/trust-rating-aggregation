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

## 2026-11-24: Round 2 (real data, amendments, freeze; owner-approved)

**Milestone:** M1 gate. **Actor:** AI assistant, under the round-2 data-freeze brief. No confirmatory run; nothing pushed; no paid service.

### Done

1. **Licence check.** MovieLens 1M page and README opened 2026-11-24: research use allowed, no redistribution, no commercial use, citation and no-endorsement conditions. Matches the approval; adopted (D-009, `data/manifest.json`).
2. **Download.** `scripts/download_movielens.py`: `ml-1m.zip`, 5,917,549 bytes, SHA-256 `a6898adb...4e20` (pinned in the script). `data/raw/` and `data/processed/` git-ignored; `users.dat` not extracted.
3. **Ingestion.** `src/trust/ingest.py` (pure, schema validation, exclusion counts) with a synthetic fixture `tests/fixtures/movielens/`. Real data: 1,000,209 rows, 0 invalid, 0 unknown movie, 0 repeats; 3,883 movies, 177 unrated.
4. **Protocol.** Section 13 written and committed (`2b8d447`) before the fit: calibration of the NegBin dispersion and the quality Beta on split F; no second test; A-1 to A-4 applied, D-008 A6 not applied (not approved).
5. **Fit** (JRN-0005, exploratory, `7ef3853`, 20.8 s): dispersion 0.4909, Beta(4.2726, 3.1944), sigma 1.0521 (reference only). Values written to the seven confirmatory configs (`39392ab`).
6. **Code.** Centred LCB prior (`prior: catalogue`), per-sigma pooled reporting (`analysis.pooled_by_level`), config-level freeze guard (`provenance.config_frozen`, `research/freeze.json`).
7. **Freeze.** `research/freeze.json`, registry hashes, D-010.

### Commands and actual outputs

| Command | Output |
|---|---|
| `../.tools/py/bin/uv sync --frozen --all-groups --all-extras` | `Audited 13 packages` |
| `.venv/bin/python -m pytest -q` (first run of the new ingest tests) | `1 failed, 7 passed`: my hand count of users in the fixture was wrong (5, not 6; user 14 rated only an unknown movie). Test corrected. |
| `.venv/bin/python -m pytest -q` (before the freeze record existed) | `4 failed, 153 passed` (the four tests that read `research/freeze.json`) |
| `.venv/bin/python -m pytest -q` (final) | `157 passed` |
| smoke and EXP-001 corner pilot rerun into the session scratch directory | results.json byte-identical to the committed ones (`8fe78903...`, `52815070...`) |
| `config_frozen` on the seven confirmatory configs | all `(True, 'frozen')` |
| `trust.cli run --config <changed copy of EXP-001.json>` | `refused ... outside the repository`, exit 3 |

### Next action

M3, when the coordinator schedules it: `trust.cli run --exp EXP-001`, `EXP-002`, `EXP-003-S*` with reports, giving `D_sigma` next to `Dbar`.

## 2026-11-25: M3 confirmatory runs (owner: "Start next")

**Milestone:** M3. **Actor:** AI assistant, under the M3 brief. Nothing pushed; no paid service; no download (MovieLens already present).

### Pre-run checks (actual outputs)

| Command | Output |
|---|---|
| `git rev-parse HEAD`; `git status --porcelain` | `6fceabb...`; clean |
| SHA-256 of every file in `research/freeze.json` (study and EXP protocols, 7 configs, data manifest, fit record) | all match |
| SHA-256 of `data/raw/ml-1m.zip` | `a6898adb...4e20`, matches the manifest |
| `../.tools/py/bin/uv sync --frozen --all-groups --all-extras` | `Audited 13 packages` |
| `.venv/bin/python -m pytest -q` | `157 passed` (no editable install; `PYTHONPATH=src` points at this tree) |

### Done

1. Frozen-analysis layer `src/trust/hypotheses.py`, `scripts/analyse_confirmatory.py`, tests `tests/test_hypotheses.py` (8), metric validation `scripts/validate_metrics.py`; choices the protocol left open fixed before data (D-011). Commit `bd9e146`. Suite: `165 passed`.
2. Metric validation: `26 passed, 0 failed`. Smoke (`experiments/smoke.json`, seed namespace 0) into `results/exploratory/smoke-m3/`: 6 runs, 0 failed, results.json byte-identical to the M2 smoke (`8fe78903...`). JRN-0006, exploratory.
3. Confirmatory runs at `bd9e146` (clean), `nice -n 10`, one process, 2026-11-24T23:35:19Z to 23:35:48Z UTC: EXP-001 180 runs in 2.22 s, EXP-002 240 in 2.26 s, S1-min1 180 in 2.51 s, S1-min5 180 in 1.57 s, S2 180 in 1.52 s, S3 240 in 1.97 s, S4 360 in 4.28 s. All exit 0; 1,560 of 1,560 ok, 0 failed, 0 retried. ORACLE tau-b 1 in every run; 0 degenerate flags.
4. Per-run reports (`trust.cli report --pdf`), frozen analysis, provenance table and SHA256SUMS; results total 6.8 MB, committed.
5. Records: journal JRN-0006 to JRN-0009, registry statuses, claims CLM-001 to CLM-011, limitations, D-011, D-012, roadmap.

### Headline (simulated)

`Dbar = 0.0046` (95% 0.0030 to 0.0061; one-sided lower bound 0.0032): H1 supported under the frozen rule, but the direction depends on the noise level: `D_sigma` -0.0198 (-0.0225 to -0.0172), 0.0085 (0.0056 to 0.0113), 0.0250 (0.0224 to 0.0277) at sigma 0.5, 1.0, 1.5. H1b contradicted; H1c not supported (LCB -0.0647). EXP-002: no average lambda effect (-0.0001, -0.0015 to 0.0012); gamma effects negative in both directions. EXP-003: S1 not invalidating; S2 and S4 invalidation criteria met (sign reversal); S3 vacuous by construction (D-012).

### Deviations

None from the frozen protocols, configs or seeds. Analysis details fixed before data (D-011). Analysis manifests first recorded `dirty: true` (the script writes its outputs before reading git state); re-run unchanged after commit, outputs identical (D-012).

### Not done, and why

- Standalone 11.3 reports for EXP-001 to EXP-003: drafted, but the session's file tool refused to write `report.md` files. Generated tables (`research/experiments/EXP-NNN/results_tables.md`) and figures are committed. M3 stays "in progress" until the reports exist.
- Manuscript update: M4.

### Final checks

`.venv/bin/python -m pytest -q`: `165 passed`.

### Next action

Write the three standalone reports from the generated tables, then M4. The owner should look at D-011 (Holm p-value choice), D-012 (S3 non-diagnostic) and the S2 and S4 reversals before any headline is drafted.

## 2026-11-25: M3 done (coordinator)

The owner approved the experiment reports (owner, 2026-11-25, "approve all recommendations, RIGGED A", item 4). Subagents may not write report files, so the reports were composed by the M3 session from committed results only and written by the coordinator: 3 report(s). The coordinator checked that every decimal number in them appears in a committed file. With the complete matrices (or documented failures) recorded above, the M3 gate holds. M3 is **done**. Next: M4 (interpretation), not started.

## 2026-11-25: M4 interpretation, evidence audit and manuscript

**Milestone:** M4. **Actor:** AI assistant, under the M4 brief (owner, 2026-11-25, "Approve all recommendations, push then next"). Nothing pushed; no paid service; no download. The 25b approvals contain no TRUST-specific follow-up.

### Commands and actual outputs

| Command | Output |
|---|---|
| `git status`; `git log -1` | clean; `cad0c35` |
| `PYTHONPATH=src nice -n 10 .venv/bin/python scripts/m4_exploratory.py` (first run) | E1 to E3 written; manifest `dirty: true` (uncommitted script edits) |
| same, after committing the script and outputs | identical result files; manifest clean at `4a2b478` (JRN-0010) |
| `PYTHONPATH=src .venv/bin/python scripts/audit_evidence.py` (final) | freeze hashes 12/12; generated artifacts 20/20; checksums 70/70; re-analysis 0 differences for EXP-001, EXP-002, EXP-003; 1,560/1,560 runs ok; 236 interval triples and 1,464 decimals traced, 0 unmatched |
| WebFetch of miller2014 (free, public page) | confirms "the method here is not exact" and "a normal approximation" |
| `pandoc research/paper/manuscript.md -s -t latex` with SPDX header | `research/paper/manuscript.tex` regenerated (not compiled; no TeX) |
| `.venv/bin/python -m pytest -q` | `165 passed` |

The first version of the audit's number trace was far too permissive (a random four-decimal number matched 63% of the time); it was narrowed, a strict interval-triple trace was added, and the measured chance-match rate is now reported with the audit.

### Done

1. Confounder and sensitivity review per conclusion, expected versus observed table: `research/publication/interpretation.md`.
2. Exploratory checks (`scripts/m4_exploratory.py`, `results/exploratory/m4-sensitivity/`): E1 noise sign pattern holds on all five metrics; LCB better on top-10 metrics at sigma 1.5. E2 ties depend on `nu`, not sigma. E3 H1b increase at sigma 1.5 is mostly dilution.
3. Claims register: new columns; CLM-012 to CLM-026; CLM-003, CLM-004, CLM-009 qualified.
4. Evidence audit (`scripts/audit_evidence.py`, `research/publication/evidence_audit.md` and `.json`, `artifact_manifest.json`); fixes F1 to F9 (citation scope, access status, stale README and registry, addenda).
5. Manuscript and supplement drafted to 11.4 (about 5,300 words); second review pass and revisions (`research/publication/review_pass_2.md`).
6. Records: limitations, D-014, journal JRN-0010 and JRN-0011, literature review audit note, roadmap.

### Deviations

None from frozen protocols, configs or seeds; no confirmatory rerun.

### Risks

- The frozen headline "H1 supported" is easy to misquote; public text should lead with the conditional statement.
- The manuscript's `[@key]` citations are not yet rendered by citeproc; the PDF build is M6.

### Next action

M5 (interactive explorer, identical numbers and labels), when the coordinator schedules it. The owner may want to read `research/publication/review_pass_2.md` section 7.


## 2026-11-25: post-M4 owner decisions (statements)

**Starting state:** `3d4346e`, working tree clean. Authority: owner, 2026-11-25, "Approve all" (post-M4) (`/Users/bechir/research/labs/_shared/owner-approvals-2026-11-25c.md`, item 2; coordinator brief `/Users/bechir/research/labs/_shared/POST-M4-brief.md`, item 2 only).

- Item 2: the funding, competing-interest and AI-use wording in manuscript section 11 is recorded as owner-approved (D-015). No wording changed.
- No frozen protocol, config, seed or result changed. No computation. No manuscript rebuild (the manuscript text did not change).

### Owner placeholders for M5

1. Manuscript section 10: "Repository: `<repository URL: not yet published>`". Only the owner can supply the repository URL, at a release decision (G-PUBLIC).

Section 11 (funding, competing interests, AI assistance) contains no placeholder.

### Tests

`.venv/bin/python -m pytest -q`: 165 passed in 5.68s (after the changes; src/ and tests/ unchanged).

### Next action

M5, with the placeholders above put to the owner.


## 2026-11-25: M5 interactive experience

**Starting state:** `53ce951`, working tree clean. Authority: owner, 2026-11-25, "Next" (`/Users/bechir/research/labs/_shared/owner-approvals-2026-11-25d.md`); brief `/Users/bechir/research/labs/_shared/M5-brief.md`. Decision D-016.

### Done

1. `demo/` from the shared template (TypeScript, React, Vite; pinned versions unchanged, no dependency added). Sections: overview with status label and value labels; published results (FIG-001 to FIG-003 as SVG dot-and-interval charts from the exported data, with data tables; one panel per experiment with status, frozen verdict, estimates, 95% intervals, claim ids and notes, including the exploratory M4 checks, labelled so); assumptions; method and limitations with D-011 and D-012 disclosed; source hashes; rating explorer sandbox.
2. `scripts/export_demo_data.py` writes `demo/public/data/results.json` (deterministic, committed inputs only, sha256 of each source).
3. `tests/test_demo_export.py` (8 tests): byte-identical re-export, every display string verbatim in the manuscript (one documented supplement-only exception, E3 intervals), figure strings in manuscript or supplement, rounding, source hashes, claim ids.
4. Sandbox: `demo/src/engine.ts` port; `scripts/make_sandbox_fixture.py` (exploratory, two regenerated EXP-001 catalogues, committed tau-b reproduced exactly, 0.63 s wall); `demo/src/engine.test.ts`: exact part within 1e-12, generator part within 4 combined standard errors in all nine cells (largest observed 1.53).
5. Text consistency: README, CITATION.cff, `articles/README.md`, `demo/README.md`, `results/README.md`, `research/paper/figures/README.md`, author-review status line, roadmap statuses. `docs/demo.png` (118,563 bytes) with alt text in the README. CONTRIBUTING gains the demo commands.

### Commands and outputs

    .venv/bin/python scripts/export_demo_data.py --check     -> export identical
    .venv/bin/python scripts/make_sandbox_fixture.py         -> wrote demo/src/fixtures/sandbox_fixture.json (88311 bytes); committed tau-b reproduced for 2 catalogues
    .venv/bin/python -m pytest -q                            -> 173 passed in 4.76s (165 before + 8 new)
    cd demo && npm ci --prefer-offline                       -> added 53 packages
    npm test                                                 -> Test Files 2 passed (2); Tests 28 passed (28)
    npm run build                                            -> built (tsc --noEmit clean)
    node tools/a11y_check.mjs dist --screenshots <scratchpad>/trust-rating-aggregation/shots

    PASS results render (no fail-closed panel): 4 experiment panels
    PASS text contrast, light scheme (WCAG AA)
    PASS text contrast, dark scheme (WCAG AA)
    PASS keyboard reaches every focusable element: 25 reached of 25
    PASS visible focus indicator
    PASS no horizontal page scroll at 360 px: overflow 0px
    PASS reduced motion: no running animations: 0 running
    PASS no request leaves the local origin
    PASS offline after first load: results stay, sandbox runs: Sandbox output (seed 1, 1 replicate): tau-b of SHRINK minus MEAN -0.0097 (one re
    PASS with sandbox output: text contrast, light scheme
    PASS with sandbox output: text contrast, dark scheme
    PASS with sandbox output: keyboard reaches every focusable element: 34 reached of 34
    PASS with sandbox output: visible focus indicator
    PASS with sandbox output: no horizontal page scroll at 360 px: overflow 0px
    A11Y-CHECK PASS

Negative control: the same checker on a copy of `dist/` whose results file had one figure interval removed printed `FAIL results render (no fail-closed panel): 0 experiment panels` and `A11Y-CHECK FAIL (2)`. Screenshots (desktop light, desktop dark, mobile, and the sandbox with output) were inspected; fixed during the session: overlapping row labels on narrow charts (halo), squeezed tables on phones (stacked rows), a caption squeezed to one word per line, a literal `{params.top_k}` label, and an explorer axis too compressed on phones (domain now fits the values shown).

### Failures during the session

- First checker run: keyboard 22 of 28 reached. Cause: the checker keys elements by id or text, and identical scroll regions collided; then closed `details` content still counted. Fixed by unique ids and by rendering disclosure content only when open.
- A file named `sandbox.ts` clashed in case with `Sandbox.tsx` under tsc; renamed to `sandboxRun.ts`.

### Gate (master prompt M5)

Offline after initial load, responsive at 360 px, keyboard usable with visible focus, reduced motion respected, no fabricated data (every number exported from committed results and checked verbatim against the manuscript), no runtime service (static files, no foreign request). Holds; M5 marked done.

### Owner items

- Placeholders: repository URL (manuscript section 10 and page footer), demo URL (README, `demo/README.md`).
- The TRUST manuscript title was not in the owner's 2026-11-25 title approvals; it remains for the owner.
- Full-text review of the manuscript and the author-review checklist (M6). No checklist box is ticked.
- Frozen protocols still say "not yet run" in their status lines; left untouched (G-FREEZE).

### Next action

M6 (release candidate), on the owner's word: articles, PDFs, clean-clone reproduction, owner review checklist.

## 2026-11-25: M5 follow-up, article drafts

The M5 commit (d542119) missed one item of the M5 brief, task 6: the article drafts of the master prompt's README paragraph. Written now:

- `articles/medium.md`: title, accessible opening, research question, estimators, method, measured results (pooled estimand, per-noise signs), negative findings (H1b contradicted, H1c not supported, SHRINK_20 loss, S2 and S4 invalidation criteria met, no detected selection effect), limitations, reproducibility section with repository and demo URL placeholders, figure alt text for FIG-001 and `docs/demo.png`, AI-assistance note.
- `articles/linkedin.md`: hook, what was built, one finding (pooled 0.0046 with interval, sign follows noise), caveat, repository and demo placeholders, image alt text.

Status label in both: "independent research manuscript / preprint draft, not peer-reviewed". No link, citation, metric, endorsement or peer-review status was invented; no claim about any real platform.

Number check (shell loop extracting every numeric token from both drafts, excluding the SPDX and comment header lines, and searching each with `grep -F` in `research/paper/manuscript.md`): no token missing. No em dash in either file.

Also changed: `articles/README.md` (drafts exist), `README.md` (status sentence), `roadmap.md` (M5 status line). `research/publication/release_checklist.md` item on articles left unticked for the M6 review.

Tests: `.venv/bin/python -m pytest -q` -> `173 passed in 4.79s`. No demo or Python code changed, so vitest and the checker were not rerun.

Next action: M6 (release candidate) on the owner's word, including the owner's review of the article drafts.

## 2026-11-25: M6 release candidate

**Starting state:** `a5f3abf`, working tree clean. Authority: owner, 2026-11-25, "Next" (second) (`labs/_shared/owner-approvals-2026-11-25e.md`); brief `labs/_shared/M6-brief.md`. Decision D-017. Current milestone M6; bounded task: clean clone, PDFs, checks and the owner review checklist, no publication.

### Commands and actual outputs

Clean clone (session scratch, deleted at the end):

    git clone -q <repository> <scratch>/clone                    -> HEAD a5f3abf
    uv sync --frozen --all-groups --all-extras                   -> locked set installed
    .venv/bin/python -m pytest -q                                -> 173 passed in 74.21s
    PYTHONPATH=src .venv/bin/python -m trust.cli smoke           -> exploratory: 6 runs (0 failed) in 0.02 s
      results.json and metrics.csv byte-identical; 4 files differ in revision, timings, command and an empty per_sigma key only (finding R1)
    cd demo && npm ci --prefer-offline                           -> added 53 packages in 1s
    npm test                                                     -> Test Files 2 passed (2); Tests 28 passed (28)
    npm run build                                                -> built in 359ms
    node tools/a11y_check.mjs dist                               -> 14 PASS lines, A11Y-CHECK PASS
    .venv/bin/python scripts/export_demo_data.py; git status     -> 0 changed files

Working repository:

    PYTHONPATH=src .venv/bin/python scripts/build_publication.py --png-dir <scratch>/png
      -> manuscript.pdf 13 pages (219,036 bytes), supplementary.pdf 6 (140,602), EXP-001 report.pdf 7 (145,206), EXP-002 6 (136,590), EXP-003 6 (124,547); manuscript.tex rewritten
    pypdf metadata                                               -> titles set; no e-mail or path in metadata or text
    .venv/bin/python scripts/check_links.py                      -> 53 Markdown files; 22 relative links ...; LINK-CHECK PASS
    PYTHONPATH=src .venv/bin/python scripts/audit_evidence.py    -> 12 frozen hashes, 20 artifacts, 70 checksums: 0 mismatches; re-analysis 0 differences; all traces 0 unmatched
    artifact_manifest.json paths and hashes                      -> 15 paths, 0 missing; 32 hashes, 0 mismatched
    shasum -a 256 data/raw/ml-1m.zip data/raw/ml-1m/*            -> 4 of 4 equal to data/manifest.json
    CITATION.cff against the CFF 1.2.0 schema (jsonschema)       -> 0 errors
    .venv/bin/python -m pytest -q                                -> 176 passed in 5.62s (173 + 3 new)
    cd demo && npm test; npm run build; node tools/a11y_check.mjs dist -> 28 passed; built; A11Y-CHECK PASS

### Failures and fixes

- First PDF build: Typst error "file not found ... references.bib" (pandoc's Typst writer emits a Typst bibliography call even with citeproc). Fixed by the `typst-citations` writer.
- Inspection of the PNG pages: title rendered as a plain paragraph (the SPDX comment came before the heading), doubled figure numbering ("Figure 1: Figure 1 (FIG-001)"), equal-width table columns with justified, hyphenated cells. Fixed in the builder (D-017); no PDF edited.
- `scripts/audit_evidence.py --help` runs the full audit (it has no argument parser) and rewrote `evidence_audit.json` and `artifact_manifest.json` with `dirty: true`; regenerated after the commit at a clean revision.

### Other changes

References (evidence audit section 6): hu2007wp, li2008 (working paper) and harper2015 (author preprint) opened in full text and their cited statements checked; access statuses updated in the manuscript, EXP-002 report, limitations, literature review, bib and claims register; efron1975 unchanged (RAND version unreadable scan). CITATION.cff: `date-released` removed, version `0.1.0-rc1`. CLAUDE.md: absolute paths replaced. New: `scripts/build_publication.py`, `scripts/check_links.py`, `tests/test_release_checks.py`, `research/publication/dependency_licences.md`. Rewritten: reproducibility report, release checklist, owner review checklist (no box ticked). README, CONTRIBUTING and roadmap updated.

Note on identifiers: earlier entries of this file (lines 18, 257 and 279 as of this entry) and two entries of the decision log contain absolute home-directory paths. They are left as written (append-only) and listed for the owner in `research/publication/author_review.md`.

### Owner items

See `research/publication/author_review.md`, section "Prepared for the owner (M6, 2026-11-25)": G-PUBLIC, the checklist boxes, the manuscript title, the CITATION.cff title, the AI wording in the articles ("Claude Code") against the manuscript ("an AI system"), the repository and demo URLs (6 placeholder lines), the owner-only facts, `date-released` and the version, the frozen "not yet run" status lines, the pandoc and Chrome licence flags and the remaining absolute paths.

### Next action

The owner reviews the release candidate and signs off `research/publication/author_review.md`; any publication waits for G-PUBLIC.

### M6 addendum: fresh-clone re-check (2026-11-25)

Commits `a52eee9` (M6 work) and `86e9984` (evidence audit and artifact manifest regenerated at the clean revision `a52eee9`: `"dirty": false`; demo export refreshed; 176 passed, demo 28 passed, A11Y-CHECK PASS). A fresh clone of `86e9984`: 176 passed in 23.81s; smoke `metrics.csv` and `results.json` byte-identical; export left 0 changed files; LINK-CHECK PASS; npm ci added 53 packages; Tests 28 passed (28); build ok; A11Y-CHECK PASS. Recorded in `research/publication/reproducibility_report.md` section 6. Both clones deleted.

## 2026-11-26: owner answers of 2026-11-26 applied (D-018)

**Starting state:** `39cef21`, working tree clean. Authority: owner, 2026-11-26, decision sheet (`labs/_shared/owner-decision-sheet-2026-11-26.md`, `labs/_shared/owner-approvals-2026-11-26.md`); brief `labs/_shared/OWNER-ANSWERS-brief.md`. Wording and configuration only; no result, analysis, figure, config, seed, frozen protocol, hash or checksummed output changed.

### Changes

A1 (repository public since 2026-11-25; out-of-date sentences corrected), B1 and B2 (repository and demo URLs filled; `CITATION.cff` `repository-code`; new `demo/wrangler.jsonc`, assets `./dist`), B3 (author line "Mohamed Bechir Kefi, independent researcher"; `CITATION.cff` affiliation), B4 ("No funding was received."), B5 ("an AI system" in the articles and reports), B6 and B7 (`CITATION.cff` title = manuscript title), B8, B10, B11, B13, B14 (release checklist: version policy and "Release notes (draft)"), B9 (no home path in editable files; 16 lines in 10 append-only, frozen or run-log files listed in the reproducibility report section 7), B12 (README sentence). Records: decision D-018, `author_review.md` section "Owner answers recorded (2026-11-26)" (no box ticked; placeholder list now empty), `roadmap.md` M6 status.

### Commands and actual outputs

    git ls-files | xargs grep -c "/Users/"                         -> progress.md 3, research/decision_log.md 2, research/protocol.md 4, 7 run logs 1 each; 0 in editable files
    PYTHONPATH=src .venv/bin/python scripts/build_publication.py --png-dir <scratch>/png
      -> manuscript.pdf 219403 bytes (13 pages), supplementary.pdf 140610 (6), EXP-001 report.pdf 145311 (7), EXP-002 136693 (6), EXP-003 124688 (6); manuscript.tex rewritten
    pypdf text scan                                                -> author line on page 1 of manuscript, supplement and reports; URLs and funding sentence on manuscript page 12; no "not yet published" left
    PNG inspection                                                 -> manuscript pages 1 and 12, supplement page 1, EXP-001 report page 1: author line, URLs and statements render correctly
    .venv/bin/python -m pytest -q                                  -> 176 passed in 6.48s
    .venv/bin/python -m pytest -q tests/test_demo_export.py        -> 8 passed in 0.02s
    .venv/bin/python scripts/check_links.py                        -> 54 Markdown files; 22 relative links ...; LINK-CHECK PASS
    cd demo && npm test                                            -> Test Files 2 passed (2); Tests 28 passed (28)
    npm run build                                                  -> built in 136ms (dist/assets/index-96GTScmF.js 249.71 kB)
    node tools/a11y_check.mjs dist                                 -> 14 PASS lines (keyboard 26 of 26, 35 of 35 with sandbox output; no request leaves the local origin), A11Y-CHECK PASS
    built page origins                                             -> index.html loads ./assets only; the only external URL in the bundle besides XML namespaces and react.dev error text is the repository link (not loaded)
    .venv/bin/python scripts/export_demo_data.py; git status       -> results.json unchanged

### Next action

The owner reviews the articles (B15), reviews the full text and signs off `research/publication/author_review.md` (B16), then decides the release (B18). The coordinator pushes and deploys on the owner's word.

## 2026-11-26: demo brand identity, motion and UI redesign (owner request)

Brief: `labs/_shared/DEMO-BRAND-brief.md` (read-only). The demo gets its own identity: a consumer test-lab report (bench white, graphite, label yellow only as label grounds, calibration blue for SHRINK, raw magenta for MEAN). No number, result, exported data, fixture, test expectation, test id or checked accessible name changed. The footer AI-use line keeps the wording "an AI system".

### Changed files

- `demo/DESIGN.md` (new): subject, audience, job, palette, type, layout wireframe, motion plan, memorable thing, review against the generated-page tells and what was revised.
- `demo/public/brand/` (new): `mark.svg`, `mark-mono.svg`, `mark-reversed.svg`, `lockup.svg`, `lockup-mono.svg`, `lockup-reversed.svg`, `favicon.svg`, `favicon-32.png`, `apple-touch-icon.png`, `og.png` (1200 by 630). Generators: `demo/tools/make_brand.py` (fontTools), `demo/tools/og.html` (Chrome headless).
- `demo/src/`: new `Hero.tsx` (two product test labels: reviews drop in, interval narrows, star row sharpens; labelled "Illustration, not study data", no numerals), `Verdict.tsx` (key result: SHRINK_5 minus MEAN at the three noise levels with intervals, from `results.json`), `Seg.tsx` (segmented control with sliding indicator, used for the explorer's ranking order), `useReveal.ts`; `App.tsx` (sticky bar, hero with question and answer, verdict, Reproduce section, footer with repository, manuscript, labs index, licence, AI-use and font credits; the sandbox now sits between the results and the assumptions); `Charts.tsx` (forest rows reveal once on scroll); `Sandbox.tsx` (ranking-order select replaced by a segmented control with the same four options; run feedback); `main.tsx` (font imports); `style.css` rewritten.
- `demo/index.html`: title, description, favicon, theme colour, Open Graph and Twitter card metadata.
- `demo/package.json`, `demo/package-lock.json`: `@fontsource-variable/archivo` 5.3.0 and `@fontsource/atkinson-hyperlegible-next` 5.3.0 (exact, `npm_config_before=2026-11-12`), SIL OFL 1.1.
- `demo/README.md`: design and brand section, third-party font notes.

### Commands and actual outputs

| Command | Output |
|---|---|
| `npm install --save-exact @fontsource-variable/archivo@5.3.0 @fontsource/atkinson-hyperlegible-next@5.3.0` (before 2026-11-12) | `added 2 packages` |
| `python3 tools/make_brand.py <archivo-wdth.ttf>` | `brand written to public/brand` |
| `svg_audit.py mark.svg favicon.svg lockup.svg` | favicon 100/100; mark and lockup 92/100 with one warning: the 72 and 108 degree edges of the regular five-point star (its exact geometry, kept) |
| `npm test` (demo) | `Test Files 2 passed (2)`, `Tests 28 passed (28)` |
| `npm run build` | `tsc --noEmit` clean; JS 261.93 kB (81.42 kB gzip) |
| `node tools/a11y_check.mjs dist` | 14 PASS lines (keyboard 32 of 32, then 44 of 44 with sandbox output; contrast light and dark; 360 px overflow 0; reduced motion 0 running; same origin only; offline sandbox), `A11Y-CHECK PASS` |
| `.venv/bin/python -m pytest -q tests/test_demo_export.py` | `8 passed` |
| `dist/` size | 660,452 bytes (was about 296 kB before; the Archivo package bundles three subsets loaded by unicode-range); a first visit loads about 439 kB |

Screenshots (desktop 1440 and phone 390, full page, after one sandbox run) were taken from a local server on 127.0.0.1:5234 with Chrome DevTools device emulation and reviewed in two critique passes (hero title size reduced, explorer chart clipping its last tick fixed, panel headings narrowed on phones, Open Graph title resized).

### Risks

Forest rows and verdict bars start hidden until scrolled into view; a print rule and a no-IntersectionObserver fallback show them at once. The atkinson zero is slashed by design, which changes the look of every number but not its value.

### Next action

Coordinator: review, push and deploy on the owner's word.
