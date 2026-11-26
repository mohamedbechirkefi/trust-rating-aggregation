<!-- SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0 -->
# Release checklist

Status (2026-11-25, M6; updated 2026-11-26): release candidate prepared. The repository was pushed and has been public at `https://github.com/mohamedbechirkefi/trust-rating-aggregation` since 2026-11-25; no tag, GitHub release, DOI or preprint exists. The owner's answers of 2026-11-26 (decision sheet) were applied in D-018. The ticked items were verified in the M6 session of 2026-11-25; the evidence follows each item. The release itself (B18) waits for the owner's full-text review and sign-off (B16).

- [x] Every registered experiment has a truthful standalone report (`research/experiments/EXP-NNN/report.md`). Evidence: 3 registered experiments in `research/experiment_registry.csv`, 3 reports; their intervals trace to the frozen analysis (`scripts/audit_evidence.py`: 26, 35 and 34 triples, 0 unmatched) and the re-analysis from raw results gives 0 differences.
- [x] Integrated manuscript complete; PDF built locally and visually inspected. Evidence: `scripts/build_publication.py` built `research/paper/manuscript.pdf` (13 pages), the supplement (6) and three reports (7, 6, 6); all 13 manuscript pages and the first and figure pages of each report inspected as PNG; four builder fixes (`research/publication/reproducibility_report.md` section 4).
- [x] README states verified findings only, with experiment table and status. Evidence: `tests/test_release_checks.py`: all 29 numbers of `README.md` appear verbatim in the manuscript; experiment table lists EXP-001 to EXP-003 with status; status sentence updated for M6.
- [x] Articles (`articles/medium.md`, `articles/linkedin.md`) use the same verified numbers and caveats. Evidence: same test, 40 and 9 numbers, 0 missing; status label "independent research manuscript / preprint draft, not peer-reviewed" in both. Their wording still needs the owner's review (`research/publication/author_review.md`).
- [x] Demo uses the same results, labels and scope; offline after initial load; accessibility checks done. Evidence: clean clone `npm test` 28 passed, `npm run build`, `node tools/a11y_check.mjs dist` `A11Y-CHECK PASS`; `tests/test_demo_export.py` passes; re-export left the clone clean.
- [x] Reproducibility report complete. Evidence: `research/publication/reproducibility_report.md` (clean clone at `a5f3abf`: 173 passed; smoke `results.json` and `metrics.csv` byte-identical).
- [x] Licence files and NOTICE intact; third-party licences listed. Evidence: `git diff a5f3abf -- LICENSE NOTICE.md LICENSE_HISTORY.md CLA.md .github` empty; `research/publication/dependency_licences.md` (13 Python, 53 npm packages; flags: pandoc and Chrome, build tools only).
- [x] No large generated files, secrets or personal identifiers committed. Evidence: scan of the tracked files (236 before M6) plus the new files: 0 e-mail addresses, 0 key or token patterns, 0 private-key headers, 0 `.env` files; absolute home-directory paths in 18 lines of 11 files, of which `CLAUDE.md` (2 lines) was fixed, and the rest are in append-only journals (`progress.md` 3, `research/decision_log.md` 2, with a note appended), the frozen `research/protocol.md` (4) and checksummed run logs (7), left unchanged and listed for the owner. Largest new file: `research/paper/manuscript.pdf`, 219,036 bytes; every PDF under 5 MB. PDF metadata: titles set, no e-mail, no path.
- [ ] Owner sign-off of `research/publication/author_review.md` (the owner only).
- [ ] Owner approval to publish, push or release (G-PUBLIC; the owner only).

## Version and date at the release (B8)

Owner, 2026-11-26, decision sheet: `CITATION.cff` keeps `version: 0.1.0-rc1` and no `date-released` until the release. At the release, the version becomes `0.1.0` and `date-released` is set to the release day. `pyproject.toml` stays at `0.0.0` (changing it would change the lockfile and the recorded environments).

## Release notes (draft)

- External build and check tools are used but not redistributed: pandoc (GPL-2.0-or-later) converts Markdown to Typst and LaTeX, Google Chrome runs the demo accessibility check headless, the numpy and scipy wheels bundle compiled libraries (OpenBLAS and, for scipy, a Fortran runtime from GCC), and lightningcss (MPL-2.0) is a demo build dependency, as listed in `research/publication/dependency_licences.md`.
- No figure of this repository was listed with small or clipped labels (B11); the figures are kept as committed.
- The committed PDFs (manuscript, supplement and three experiment reports) stay in the repository and are attached to the release (B10).
- The access labels of the sources not read in full (for example the efron1975 RAND scan) are accepted as stated in the manuscript and `research/literature_review.md` (B14, owner, 2026-11-26, decision sheet).
