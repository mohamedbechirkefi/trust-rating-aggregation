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

## D-009: MovieLens 1M adopted for calibration (owner-approved, round 2)

- **Date:** 2026-11-24
- **Decided by:** the owner ("Approve all", `owner-approvals-2026-11-24b.md` section 1: "TRUST | MovieLens | Real rating counts and distributions; the misranking test stays simulated on top"). Variant and method chosen by the AI assistant under the round-2 brief.
- **Licence check.** Dataset page https://grouplens.org/datasets/movielens/1m/ ("Stable benchmark dataset. 1 million ratings from 6000 users on 4000 movies. Released 2/2003", `ml-1m.zip` about 6 MB) and README https://files.grouplens.org/datasets/movielens/ml-1m-README.txt opened on 2026-11-24. Usage licence: research use allowed; no endorsement; acknowledge and cite Harper and Konstan 2015; no redistribution without separate permission; no commercial use without permission. This matches the approval, so the data is adopted. Recorded in `data/manifest.json`.
- **Variant.** MovieLens 1M, the smallest standard variant with integer 1 to 5 star ratings at this scale (5,917,549 bytes; SHA-256 `a6898adb50b9ca05aa231689da44c217cb524e7ebd39d264c56e2832f2c54e20`). ML-25M and the half-star "latest" variants were not used.
- **Redistribution and personal data.** `data/raw/` and `data/processed/` are git-ignored; nothing from MovieLens is committed except aggregate fitted parameters and counts (`data/calibration/movielens-1m-fit.json`). `users.dat` (demographics) is never extracted. User ids are pseudonymous and are discarded after the duplicate check.
- **Use.** Calibration of the NegBin dispersion and the latent quality Beta, by the method written into `research/protocol.md` section 13.1 and committed at `2b8d447` before the fit (JRN-0005). No second test. Fitted values: dispersion 0.4909, Beta(4.2726, 3.1944); sigma 1.0521 reference only.
- **Consequences.** Every confirmatory config uses the fitted values. Publications must acknowledge MovieLens and cite Harper and Konstan 2015, and must not imply GroupLens endorsement.

## D-010: Protocol freeze v1.0 (owner-approved, G-FREEZE)

- **Date:** 2026-11-24
- **Decided by:** the owner. Quoted answers: "yes for all others" (`owner-approvals-2026-11-24.md`, TRUST amendments) and "Approve all" (`owner-approvals-2026-11-24b.md`, real data and section 7). Applied by the AI assistant.
- **Amendments applied** (protocol section 13): MovieLens calibration (D-009); A-1 LCB prior centred on the catalogue mean (`alpha_k = 5 * p_k`); A-2 `D_sigma` reported per noise level next to `Dbar`; A-3 20 seeds kept; A-4 measured SD 0.0064 to 0.0128 replaces 0.05. Not applied: D-008 A6 (not approved). D-008 is thereby resolved.
- **Common decisions.** C1 real data as approved (MovieLens calibration), synthetic otherwise; C2 PDFs with pandoc and Typst; C3 authorship "Mohamed Bechir Kefi", no affiliation, AI disclosed as an assistant; C4 the exploratory primary-contrast values seen before the freeze are listed with their paths in `research/freeze.json` (smoke, X-PILOT-001, X-PILOT-002; all under the planning generator and the uncentred LCB).
- **Hashes (SHA-256).**
  - `research/protocol.md` v1.0: `3226e302fb4758327d50a5f583026d469d7ccbc5ad7c72b458fcd8bf2b702f03`
  - `research/experiments/EXP-001/protocol.md`: `27766885e692caa61253528fe5d959ab25f4b64db65bfde28c301671df31ce50`
  - `research/experiments/EXP-002/protocol.md`: `47459d4b5c8d0f9ab2911be068929c6ada9253ec7a601004893c731b0b1fcf27`
  - `research/experiments/EXP-003/protocol.md`: `cb4568fa37e4feaa1bd1a79a71fafa47a96fcad13d8b8b2d6605932c71b19b81`
  - configs: `EXP-001.json` `bb3bec3b...0f4279`, `EXP-002.json` `325df066...5bd9`, `EXP-003-S1-min1.json` `7e9683ea...a564`, `EXP-003-S1-min5.json` `5b948ab0...dc89`, `EXP-003-S2.json` `fecaa2f8...ff18`, `EXP-003-S3.json` `43854058...d4d7`, `EXP-003-S4.json` `e788afa2...4d89` (full values in `research/freeze.json`)
  - `data/manifest.json`: `ed8fb8eee48be9a08850c48872883a4299e3e4601b9ac4a371df65e023dd4d30`
  - git revision of the frozen content: `39392ab5864ae2c398b226409a765808c80eda6e`
- **Guard.** `run` now also checks the config file, the study protocol and the data manifest against `research/freeze.json` (`trust.provenance.config_frozen`); tests cover acceptance of the frozen configs and refusal of changed, unlisted or out-of-repository ones.
- **Consequences.** Every later change to these files is a dated deviation here. M3 (confirmatory runs) is scheduled by the coordinator; none was run in this session.

## D-011: Frozen-analysis layer written at M3, before any confirmatory output

- **Date:** 2026-11-25
- **Decided by:** the AI assistant under the M3 brief (the owner said "Start next" on 2026-11-25). For the owner's review.
- **Context.** The frozen protocols state the estimands, intervals, decision rules and the Holm families, but the M2 report generator computed only per-cell, pooled and per-sigma contrasts against MEAN. The decision rules (H1, A-2 flag, H1b, Holm family, EXP-002 paired factor contrasts, EXP-003 invalidation criteria) had no code.
- **Decision.** `src/trust/hypotheses.py` and `scripts/analyse_confirmatory.py` implement the frozen rules. They were written, tested (`tests/test_hypotheses.py`) and committed before any confirmatory catalogue was generated; no frozen file (protocols, configs, data manifest, freeze record) changed. Where the frozen text leaves a detail open, the choice is fixed here, before data:
  1. **Holm p-values.** The protocol names Holm but no p-value. We use the bootstrap p-value of the same stratified bootstrap that gives the intervals (10,000 resamples, seed 20261124): one-sided `(1 + #{boot <= 0}) / (B + 1)` for the directional EXP-001 secondary family; two-sided `min(1, 2 * smaller tail)` for the nondirectional EXP-002 family. alpha = 0.05.
  2. **EXP-001 Holm family:** H1b, H1c (LCB minus MEAN) and SHRINK_1 and SHRINK_20 minus MEAN, each pooled over the nine cells with equal weight, one-sided (> 0). H1b enters through the contrast mean over sigma of `E[D | nu = 3] - E[D | nu = 30]`, cells resampled independently. The H1b verdict itself uses the frozen ordering and overlap criteria (overlap of the per-cell 95% bootstrap intervals).
  3. **EXP-002:** the lambda contrast and the two gamma contrasts (`gamma = -0.5` and `gamma = 0.5`, each minus `gamma = 0`) are same-seed paired differences of `D` per stratum of the other factors, averaged over strata with equal weight; Holm across these three for SHRINK_5. The same contrasts are reported for LCB outside the Holm family.
  4. **EXP-003:** "the EXP-001 pooled Dbar is positive" (S1) and "sign reversal" (S2, S4) refer to the sign of the EXP-001 point estimate of `Dbar` against the sign of the sub-analysis point estimate. S3 counts sign differences of the per-cell mean `D` over the 12 EXP-002 cells (the six `lambda = 0` cells, where the two truths coincide, are included); the count among the six `lambda = 2` cells is reported alongside.
- **Consequences.** H1 (the primary decision) does not depend on any of these choices. Secondary verdicts are labelled with this decision. Any other analysis is exploratory.

## D-012: M3 confirmatory runs complete; S3 non-diagnostic for rank metrics; reports pending

- **Date:** 2026-11-25
- **Decided by:** the AI assistant under the M3 brief; recorded for the owner. No frozen artifact changed and nothing was rerun.
- **Runs.** Every frozen matrix ran in full at revision `bd9e146` (clean tree), through the run guard, with the frozen configs and seeds: EXP-001 180, EXP-002 240, EXP-003 1,140 (S1-min1 180, S1-min5 180, S2 180, S3 240, S4 360). 1,560 of 1,560 runs ok, 0 failed, 0 retried (JRN-0007 to JRN-0009). Provenance per run in `results/confirmatory/provenance.csv`; checksums in `results/confirmatory/SHA256SUMS`.
- **Finding about the design (not a deviation).** EXP-003 S3 compares rankings against `theta` and `theta_rep`. Within a cell both are strictly increasing functions of `mu` (checked numerically on a 4,001-point grid at sigma 1.0, lambda 0 and 2), so every rank-only metric (tau-b, Spearman, precision at 10) is identical under the two truths; the S3 tau-b values equal the EXP-002 values exactly in all 240 runs. The frozen S3 criterion ("sign of D differs in a majority of strata") is therefore not met by construction and carries no evidence. RMSE, regret and coverage do differ. This is reported as a limitation of the registered S3, not repaired: a value-based S3 would be a new, owner-approved analysis.
- **Frozen verdicts.** H1 supported (`Dbar` 0.0046, one-sided lower bound 0.0032) with direction depending on sigma (A-2); H1b contradicted; H1c not supported; EXP-002 lambda: no average difference, per-stratum rule not met; S1 not invalidating; S2 and S4 invalidation criteria met; S3 vacuous.
- **Analysis provenance note.** The first `scripts/analyse_confirmatory.py` invocations wrote their own outputs (tables and figures under `research/experiments/`) before reading the git state, so their manifests recorded `dirty: true`. The analysis was re-run unchanged after the results were committed; outputs were identical and the manifests then record a clean revision.
- **Reports pending.** The standalone 11.3 reports (`research/experiments/EXP-NNN/report.md`) were drafted but the session's file tool refused to write them; the generated tables and figures they rely on are committed. Writing them is the next task.

## D-013: Owner decisions closing M3 (2026-11-25)

- **Date:** 2026-11-25
- **Decided by:** the owner, 2026-11-25, "approve all recommendations, RIGGED A" (`owner-approvals-2026-11-25.md` in the labs workspace, outside this repository). Applied by the AI assistant.
- **Item 5 (TRUST).** "D-011 (bootstrap p-values for Holm) and D-012 (S3 cannot discriminate by design) are accepted, with both disclosed." Both are owner-accepted deviations, disclosed in each experiment report, in the claims register (CLM-005, CLM-011), in `research/limitations.md` and in the `deviations` list of `research/freeze.json`. Adding that list changes no hash the run guard checks.
- **Item 4 (experiment reports).** "The owner approves writing the missing 11.3/11.6 experiment reports ... They are written from the committed results, tables and figures only." and "Nothing is recomputed and no numbers change." `research/experiments/EXP-001/report.md`, `EXP-002/report.md` and `EXP-003/report.md` are written on that basis; every number in them is copied from committed result files. This repository has no `reproduction.md`; section 12 of each report is its reproduction appendix.
- **Consequences.** No frozen protocol, config, seed or result changes. With the reports written, the M3 gate holds.
