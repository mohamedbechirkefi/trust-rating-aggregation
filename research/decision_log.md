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

## D-007: M2 implementation choices where the draft protocol is silent

- **Date:** 2026-11-24
- **Decided by:** AI assistant (implementation choices under the M2 brief); the owner may revise before the freeze.
- **Decisions:**
  1. **Freeze check.** `run` treats an experiment as frozen only when its registry `protocol_hash` is a 64-hex SHA-256 equal to the hash of `research/experiments/<EXP>/protocol.md` and that hash also appears in this log. Otherwise confirmatory configs are refused (exit code 3). This session froze nothing.
  2. **Catalogue with no reported rating at all.** The prior mean `m` falls back to the scale midpoint 3 and the run is flagged `m_fallback`; tau-b is then undefined (constant MEAN scores) and stored as null with a degenerate-case flag, never imputed. Not observed at N = 200 in any pilot.
  3. **Undefined metrics.** Tau-b and Spearman are null when either vector is constant; such runs are excluded from paired differences and counted in the report.
  4. **S1 filter.** `min_reviews` restricts the evaluated products (scores and truth); the catalogue mean `m` and `s_pool` are still computed from the whole catalogue.
  5. **S2.** Implemented as extra arms (`SHRINK_5_UP`, `SHRINK_5_DOWN`) on the same EXP-001 catalogues.
  6. **Seed streams.** `SeedSequence([20261124, exp_number, seed_index]).spawn(4)` for quality, counts, ratings and reporting. EXP-003 configs reuse exp_number 1 (S1, S2, S4) and 2 (S3) so they regenerate the EXP-001 and EXP-002 catalogues, as the EXP-003 draft requires.
  7. **Exploratory seed namespaces.** Pilots use exp_number 901 and 902 so that no confirmatory catalogue is generated before the freeze.
  8. **Figures.** Drawn as hand-written SVG by `trust.report` (no plotting dependency added; D-005 unchanged).
  9. **Peak memory.** Recorded as process-level peak RSS per invocation (getrusage), not per run.
- **Consequences:** these choices are part of the code the owner freezes against; they are listed in `progress.md` and in each run's `results.json` config.

## D-008: Proposed protocol amendments from the exploratory pilots (PROPOSED, not adopted)

- **Date:** 2026-11-24
- **Decided by:** nobody yet. The owner decides at the freeze (G-FREEZE). The protocol text is unchanged.
- **Disclosure:** these proposals are informed by exploratory pilot output (JRN-0002 to JRN-0004, seed namespaces disjoint from the confirmatory ones). Any change adopted because of them must be recorded as pilot-informed, not as a priori.
- **A1, planning SD.** Protocol section 6 assumes a between-catalogue SD of `D` near 0.05. Measured per-seed SD at N = 200: 0.0064 to 0.0128 across the four EXP-001 corner cells (10 seeds each). With 20 seeds the normal-approximation 95% half-width is about 0.003 to 0.006, well under the 0.02 trigger. Proposal: replace the 0.05 assumption with the measured range; 20 seeds is adequate and no increase is required. Because runs are cheap, the owner may still choose 50 seeds (the master prompt allows more seeds when inexpensive).
- **A2, compute budget.** Measured 3.3 to 3.5 ms per run at N = 200 (max 5.03 ms). All registered configs total 1,560 runs (EXP-001 180, EXP-002 240, EXP-003 1,140), projected at about 5 to 8 seconds of simulation plus under 1 second of reporting per experiment. The 30-minute budget is not binding.
- **A3, EXP-002 threshold.** Per-seed SD of the paired lambda contrast about 0.0073 to 0.0074; the 0.03 half-width threshold is met at 20 seeds.
- **A4, sign heterogeneity (for the owner's attention, no change proposed to the analysis).** In the corner pilot `D` was negative at sigma 0.5 and positive at sigma 1.5, at both nu levels, so the equal-weight `Dbar` over the nine cells may sit near zero and depend on grid composition. H1b (ordering by nu) may therefore be less informative than an ordering by sigma. The owner may wish to decide before the freeze whether a sigma-direction secondary hypothesis should be registered; if added now it must be labelled pilot-informed.
- **A5, LCB prior centre (for the owner's attention).** The Dirichlet(1, ..., 1) prior is centred at 3 stars, while the per-catalogue mean `m` averaged 3.60 and 3.65 in the two pilots (range 3.14 to 4.18); LCB minus MEAN was strongly negative in every pilot cell. Keeping the arm as specified is legitimate (it is Miller's published rule). Any catalogue-informed LCB variant would be a new, pilot-informed secondary arm and must not replace the registered one.
- **A6, calibration metric.** The SHRINK interval rule (`post_mean +/- z * s_pool / sqrt(n + kappa)`) ignores shrinkage bias; pilot coverage was about 0.51 at sigma 0.5, nu 3. Interpretation of the calibration metric should say that it evaluates this stated interval rule, not shrinkage in general.
