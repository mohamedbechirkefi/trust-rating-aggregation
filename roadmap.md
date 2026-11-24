<!-- SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0 -->
# TRUST roadmap

Target: five focused development days (planning estimate, never a reason to weaken evidence). Effort is in focused days. Status values: done, in progress, not started, blocked. Last updated 2026-11-24.

| ID | Milestone | Depends on | Priority | Effort | Status | Blockers |
|---|---|---|---|---|---|---|
| M0 | Bootstrap and feasibility | none | P0 | 0.5 | done (pending owner review of this session) | none |
| M1 | Research and preregistration | M0 | P0 | 0.5 | in progress (drafts written; freeze pending) | G-FREEZE: owner must freeze the protocol |
| M2 | Core implementation | M1 drafts (implementation may start before the freeze) | P0 | 1.0 | not started | none |
| M3 | Experiments | M1 freeze, M2 | P0 | 0.5 | not started | protocol freeze |
| M4 | Interpretation | M3 | P0 | 1.0 | not started | M3 |
| M5 | Interactive experience | M3 results (demo shell may start at M2) | P1 | 1.0 | not started | none |
| M6 | Release candidate | M4, M5 | P0 | 0.5 | not started | owner approval for any publication (G-PUBLIC) |

If the five-day target is threatened, cut in this order: optional EXP-003 sub-analysis S4, demo extras, EXP-002 cells. Never cut controls, reports or the evidence audit.

## M0: Bootstrap and feasibility

- Deliverables: control files; feasibility audit (hardware, tools, time, cost, sources, licences); explicit scope, exclusions and fallback; section 11.1 tree initialised; dependency lockfile; zero-cost toolchain confirmed.
- Acceptance: the owner can understand the question, cost (zero) and exclusions from `README.md`, `research/protocol.md` section 12 and `data/manifest.json`. All required files exist. `uv.lock` resolves. A toolchain smoke check is recorded.
- Status: done on 2026-11-24 (see `progress.md`).

## M1: Research and preregistration (with 11.6 additions)

- Deliverables: evidence review completed beyond scoping (ranking-under-uncertainty statistics literature); formal model; baselines; `research/protocol.md`; `research/experiments/EXP-NNN/protocol.md` for every registered experiment; experiment registry; manuscript skeleton; fixture manifest; smoke run measuring runtime and the SD of the primary contrast; seed count confirmed.
- Acceptance: protocol frozen by the owner, with its SHA-256 recorded in `research/decision_log.md` and the registry, before any confirmatory run. Exploratory results visibly separated. Zero-cost toolchain confirmed (done at M0).
- Status: in progress. Drafts v0.1 written 2026-11-24. Smoke run requires the M2 engine.
- Blocker: owner freeze (G-FREEZE).

## M2: Core implementation (with 11.6 additions)

- Deliverables: simulation module; MEAN baseline first, then SHRINK and LCB; metrics; runner; versioned JSON result schema with validation; run manifests (config hash, seed, git revision, package versions, OS, CPU, runtime, peak memory); report generator; CLI commands `smoke`, `run`, `report`, `test`.
- Acceptance: unit tests for empty reviews, one review, bounded ratings, posterior formulas (hand-computed examples), deterministic sorting and tie-breaks; invariant tests (bounds of scores, tau-b of ORACLE equal to 1, shrinkage between mean and prior); differential test of tau-b against a simple reference; integration test config to results. Test counts are reported only from actual runs.
- Status: not started.

## M3: Experiments (with 11.6 additions)

- Deliverables: smoke run; frozen matrices EXP-001 to EXP-003; raw machine-readable results; plots with uncertainty; a standalone report per experiment generated as each finishes.
- Acceptance: complete planned matrix or documented failure; no silently dropped runs; provenance captured at run time.
- Status: not started. Blocked by the protocol freeze.

## M4: Interpretation (with 11.6 additions)

- Deliverables: confounder inspection, sensitivity analyses, expected versus observed, claims register, limitations, finished experiment reports, evidence audit, integrated manuscript including contradictory results.
- Acceptance: every numerical claim maps to result id, config and figure; every external claim maps to a verified source; second review pass challenges the preferred hypothesis.
- Status: not started.

## M5: Interactive experience (with 11.6 additions)

- Deliverables: static rating explorer (uncertainty intervals, sample-size sliders, ranking comparison), playground with reset, seed and scenario controls, results with effect sizes and uncertainty, methodology and limitations panels.
- Acceptance: offline after initial load, responsive, keyboard usable, reduced-motion option, no fabricated data, no runtime service; demo, paper, reports and articles use identical verified numbers and labels.
- Status: not started.

## M6: Release candidate (with 11.6 additions)

- Deliverables: clean-clone reproduction, locked install, tests, smoke reproduction, demo build, manifest and link checks, secret and licence scan, compiled and visually inspected PDFs, owner review checklist.
- Acceptance: actual command outputs recorded; verified facts only; publication only with owner approval.
- Status: not started.
