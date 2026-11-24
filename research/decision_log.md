<!-- SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0 -->
# Decision log

Append-only. Each entry: id, date, decision, decided by, rationale, consequences.

## D-001: Licence (owner's decision)

- **Date:** 2026-11-24
- **Decided by:** the owner.
- **Decision:** All original material is licensed under the TRUST Source-Available Non-Commercial Research License v1.0 (SPDX `LicenseRef-TRUST-NC-Research-1.0`), with a Contributor License Agreement (`CLA.md`). The licence files were committed at the first commit.
- **Deviation from the master prompt:** section 2 asks for an "owner-approved permissive code license". The owner instead chose this protective, non-commercial, source-available licence for their own protection. It is not an OSI-approved open-source licence.
- **Consequences:** README and CITATION.cff name the custom licence. Third-party data and dependencies keep their own licences (recorded in `data/manifest.json` and `uv.lock`). Sessions do not modify the licence files.

## D-002: Zero-cost publication toolchain

- **Date:** 2026-11-24
- **Decided by:** AI assistant (proposal under the brief); the owner may revise.
- **Decision:** No TeX distribution is installed. Markdown is canonical. PDFs are produced by pandoc 3.6.3 (Markdown to Typst) and compiled with the `typst` Python package 0.15.0. `research/paper/manuscript.tex` is generated from Markdown by pandoc and is not compiled locally.
- **Rationale:** zero cost, already installed, no system changes. A toolchain smoke check (exploratory) succeeded on 2026-11-24; see `progress.md`.
- **Consequences:** PDFs exist only after they are built and visually inspected. LaTeX compilation of `manuscript.tex` is unverified unless a TeX distribution is later approved.

## D-003: Synthetic data as primary evidence; real datasets not used at M0

- **Date:** 2026-11-24
- **Decided by:** AI assistant (proposal); the owner decides on any real dataset.
- **Decision:** Ground truth is only known in simulation, so all confirmatory evidence is synthetic. Candidate real datasets (MovieLens, Amazon Reviews 2023, Yelp Open Dataset) are not downloaded. MovieLens forbids redistribution without permission; Amazon Reviews 2023 has no licence assigned by its maintainers; Yelp terms were not verified. These are recorded as blockers in `data/manifest.json` and need the owner's decision before any use.
- **Consequences:** the optional "licensed review metadata" extension is deferred. Bundled artifacts contain only synthetic data and fixtures.

## D-004: Protocol proposed as DRAFT v0.1

- **Date:** 2026-11-24
- **Decided by:** AI assistant (proposal). Freezing is the owner's decision (G-FREEZE).
- **Decision:** `research/protocol.md` and `research/experiments/EXP-00{1,2,3}/protocol.md` are drafts. Primary metric Kendall tau-b against true quality; baseline arithmetic mean; primary contrast SHRINK(5) minus MEAN; 20 seeds per cell.
- **Consequences:** all runs before the freeze are exploratory. The seed count may be raised before the freeze if the smoke run shows wide intervals.

## D-005: Dependency pinning

- **Date:** 2026-11-24
- **Decided by:** AI assistant.
- **Decision:** Python dependencies are pinned exactly in `pyproject.toml`, and `[tool.uv] exclude-newer = "2026-11-10"` guarantees that every resolved version was released at least two weeks before 2026-11-24. `uv.lock` is committed.
- **Consequences:** upgrades are explicit decisions logged here.

## D-006: Stack sequencing

- **Date:** 2026-11-24
- **Decided by:** AI assistant.
- **Decision:** Python for the engine, experiments and report generation (M2 to M4). The static demo (M5) is planned as TypeScript with Vite; no `package.json` is created at M0 because the demo is not set up yet.
- **Consequences:** the demo consumes precomputed, schema-validated result JSON plus a small in-browser sandbox.
