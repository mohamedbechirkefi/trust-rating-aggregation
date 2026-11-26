<!-- SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0 -->
# Owner review checklist

Status (2026-11-25, M6): no box is ticked; only the owner ticks them. No box had been ticked by an agent, so none was unticked. Recorded elsewhere so far: the owner froze the protocol on 2026-11-24 (D-010) and approved the funding, competing-interest and AI-use statements on 2026-11-25 (D-015). A release candidate is prepared (D-017). Updated 2026-11-26: the repository was pushed by the coordinator and has been public at `https://github.com/mohamedbechirkefi/trust-rating-aggregation` since 2026-11-25; no tag, release, DOI or preprint exists. The owner's answers of 2026-11-26 are recorded below and applied in D-018; no box was ticked.

- [ ] Protocol freeze approved (hash recorded in `research/decision_log.md`).
- [ ] Authorship and affiliation metadata approved.
- [ ] AI assistance disclosure reviewed.
- [ ] Claims and limitations reviewed.
- [ ] Any use of an external dataset approved after licence review.
- [ ] Publication, push and release approved (G-PUBLIC).

## Prepared for the owner (M6, 2026-11-25)

### What to read for each item

1. **Protocol freeze.** `research/decision_log.md` D-010 (freeze and its hashes) and `research/freeze.json`; the post-freeze deviations are D-011 and D-012, accepted in D-013. The evidence audit confirms all 12 frozen hashes (`research/publication/evidence_audit.md` section 1).
2. **Authorship and affiliation.** Manuscript front matter (`research/paper/manuscript.md`, line 4, "Mohamed Bechir Kefi, independent researcher"), `CITATION.cff` (`authors`, `abstract`) and the Identification table (section 1) of each experiment report.
3. **AI assistance disclosure.** Manuscript section 11; `articles/medium.md` last line and `articles/linkedin.md` line 14 (both now say "an AI system", as the manuscript does); the Identification table of each report ("Authorship" row).
4. **Claims and limitations.** Manuscript sections 5 to 7; `research/claims_register.csv`; `research/limitations.md`; `research/publication/review_pass_2.md` section 7 (residual risks); `research/publication/evidence_audit.md` sections 4 and 6; the article drafts `articles/medium.md` and `articles/linkedin.md` (they repeat the manuscript's numbers and caveats).
5. **External dataset.** `data/manifest.json` (MovieLens 1M entry, licence summary, never committed), README "Data and licences", decision D-009, manuscript section 4.2.
6. **Publication, push and release.** `research/publication/release_checklist.md`, `research/publication/reproducibility_report.md`, `research/publication/dependency_licences.md`, the PDFs (`research/paper/manuscript.pdf`, `research/paper/supplementary.pdf`, `research/experiments/EXP-00N/report.pdf`) and `CITATION.cff`.

### Open decisions for this repository (as of 2026-11-25; see the 2026-11-26 section below for the answers)

- The owner decides whether and when to release, publish or change a licence. At M6 no session pushed; the coordinator pushed the repository on 2026-11-25 on the owner's word, and it has been public since then.
- The owner ticks the boxes above; no agent ticks them.
- Answered on 2026-11-26: the manuscript title, the `CITATION.cff` title, the AI wording, the repository and demo URLs, the author line, funding and competing interests, the version and `date-released` policy, the frozen "not yet run" status lines, the build-tool licence flags and the remaining absolute paths (section below).

### Remaining owner placeholders (file and line)

None. The six placeholder lines listed at M6 (`research/paper/manuscript.md` 222, `README.md` 57, `demo/README.md` 4, `demo/src/App.tsx` 57, `articles/medium.md` 59, `articles/linkedin.md` 12) were filled on 2026-11-26 with `https://github.com/mohamedbechirkefi/trust-rating-aggregation` and `https://trust-rating-aggregation.kefimohamedbechir.workers.dev` (D-018), and the PDFs were rebuilt with `scripts/build_publication.py`.

## Owner answers recorded (2026-11-26)

Source: owner, 2026-11-26, decision sheet (`labs/_shared/owner-decision-sheet-2026-11-26.md` and `labs/_shared/owner-approvals-2026-11-26.md`, outside this repository). Applied in decision D-018. No box above is ticked.

| Id | Answer | Applied in this repository |
|---|---|---|
| A1 | correct the out-of-date "not pushed / nothing published" sentences | this checklist, `release_checklist.md`, README, `articles/README.md`, `CLAUDE.md` (G-PUBLIC line), `roadmap.md` (M6 status); append-only records unchanged |
| B1 | repository URL `https://github.com/mohamedbechirkefi/trust-rating-aggregation` | manuscript section 10, README, demo footer, both articles; `CITATION.cff` `repository-code` |
| B2 | demo on Cloudflare Workers, free plan, at `https://trust-rating-aggregation.kefimohamedbechir.workers.dev` | README, `demo/README.md`, manuscript section 10, both articles; new `demo/wrangler.jsonc` (assets `./dist`, no Worker script); the coordinator deploys |
| B3 | "Mohamed Bechir Kefi, independent researcher" | manuscript, supplement, the three experiment reports (Identification table), `CITATION.cff` (`affiliation: "Independent researcher"`), README, Medium article byline, demo footer; the frozen `research/freeze.json` (C3, "no affiliation") is not edited |
| B4 | no funding, no competing interests | manuscript section 11: "No funding was received. The author declares no competing interests." |
| B5 | TRUST uses "an AI system" in every file | both articles and the three reports aligned with the manuscript |
| B6, B7 | manuscript title approved; `CITATION.cff` carries it | `CITATION.cff` `title` set to the manuscript title |
| B8 | `0.1.0-rc1` and no `date-released` until the release | recorded in `release_checklist.md` |
| B9 | scrub home paths from editable files, no history rewrite | none found in editable files; 16 remaining lines in 10 append-only, frozen or run-log files listed in `reproducibility_report.md` section 7 |
| B10, B11, B13 | PDFs kept; build-tool licence sentence | "Release notes (draft)" in `release_checklist.md`; no TRUST figure was listed under B11 |
| B12 | leave the frozen "not yet run" status lines; one README sentence | README, "What exists now" |
| B14 | source-level access labels accepted | recorded in `release_checklist.md`; no text change |

### Still open (owner only)

- B15: the article drafts `articles/medium.md` and `articles/linkedin.md` and their titles, before any posting.
- B16: the owner's full-text review of the manuscript, supplement and reports, then the sign-off of this checklist.
- B18: the release (tag, GitHub release with the PDFs attached, optional zero-cost DOI or preprint), with the version `0.1.0` and `date-released` set on that day.
- Freezes: none open in this repository (the protocol was frozen on 2026-11-24, D-010; no new experiment is registered).
