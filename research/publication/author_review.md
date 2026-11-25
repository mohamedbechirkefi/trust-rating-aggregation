<!-- SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0 -->
# Owner review checklist

Status (2026-11-25, M6): no box is ticked; only the owner ticks them. No box had been ticked by an agent, so none was unticked. Recorded elsewhere so far: the owner froze the protocol on 2026-11-24 (D-010) and approved the funding, competing-interest and AI-use statements on 2026-11-25 (D-015). A release candidate is prepared (D-017); nothing is published.

- [ ] Protocol freeze approved (hash recorded in `research/decision_log.md`).
- [ ] Authorship and affiliation metadata approved.
- [ ] AI assistance disclosure reviewed.
- [ ] Claims and limitations reviewed.
- [ ] Any use of an external dataset approved after licence review.
- [ ] Publication, push and release approved (G-PUBLIC).

## Prepared for the owner (M6, 2026-11-25)

### What to read for each item

1. **Protocol freeze.** `research/decision_log.md` D-010 (freeze and its hashes) and `research/freeze.json`; the post-freeze deviations are D-011 and D-012, accepted in D-013. The evidence audit confirms all 12 frozen hashes (`research/publication/evidence_audit.md` section 1).
2. **Authorship and affiliation.** Manuscript front matter (`research/paper/manuscript.md`, line 4, "Mohamed Bechir Kefi (no affiliation)"), `CITATION.cff` (`authors`, `abstract`) and the Identification table (section 1) of each experiment report.
3. **AI assistance disclosure.** Manuscript section 11; `articles/medium.md` last line and `articles/linkedin.md` line 14; the Identification table of each report ("Authorship" row).
4. **Claims and limitations.** Manuscript sections 5 to 7; `research/claims_register.csv`; `research/limitations.md`; `research/publication/review_pass_2.md` section 7 (residual risks); `research/publication/evidence_audit.md` sections 4 and 6; the article drafts `articles/medium.md` and `articles/linkedin.md` (they repeat the manuscript's numbers and caveats).
5. **External dataset.** `data/manifest.json` (MovieLens 1M entry, licence summary, never committed), README "Data and licences", decision D-009, manuscript section 4.2.
6. **Publication, push and release.** `research/publication/release_checklist.md`, `research/publication/reproducibility_report.md`, `research/publication/dependency_licences.md`, the PDFs (`research/paper/manuscript.pdf`, `research/paper/supplementary.pdf`, `research/experiments/EXP-00N/report.pdf`) and `CITATION.cff`.

### Open decisions for this repository

- The owner decides whether and when to push, release, publish or change a licence; M6 did none of these (G-PUBLIC).
- The owner ticks the boxes above; no agent ticks them.
- The manuscript title ("When does shrinkage beat the average star rating? A preregistered simulation of rank recovery under noise, sparsity and misspecification") was not among the titles the owner approved on 2026-11-25 and needs the owner's approval.
- `CITATION.cff` keeps the project title ("TRUST: when do average ratings misrank products compared with uncertainty-aware estimators?") because it describes the software; the owner decides whether it should instead carry the manuscript title.
- The article drafts name the assistant "Claude Code" while the manuscript says "an AI system"; both were left as they are, and the owner chooses the wording (or keeps the difference).
- The owner supplies the repository URL and the demo URL, which only the owner can know (placeholders listed below).
- The author line, the affiliation ("no affiliation"), the funding statement and the competing-interest statement are owner-only facts; their wording was approved in D-015, and the owner confirms them at release.
- `CITATION.cff` has no `date-released` (removed under the coordinator default of owner-approvals-2026-11-25e); the owner re-adds it with the actual date when a release exists, and confirms the version `0.1.0-rc1` or the final version number.
- The frozen protocols (`research/protocol.md` and `research/experiments/EXP-00N/protocol.md`) still say "not yet run" in their status lines; changing them would touch frozen files (G-FREEZE), so the owner decides whether to leave them, with the registry and reports giving the current state.
- Two build tools fall outside the permissive licence set and are recorded for the owner: pandoc (GPL, used only as a converter, not redistributed) and Google Chrome (used headless by the demo checker, not redistributed) (`research/publication/dependency_licences.md`).
- Absolute paths of the owner's machine remain in append-only or checksummed files (`progress.md`, `research/decision_log.md`, the frozen `research/protocol.md` and the seven run logs under `results/confirmatory/logs/`); the owner decides whether they are acceptable in a public repository, since removing them would rewrite journals, frozen files or checksummed outputs.

### Remaining owner placeholders (file and line)

| File | Line | Placeholder |
|---|---|---|
| `research/paper/manuscript.md` | 222 | `<repository URL: not yet published>` |
| `README.md` | 57 | `<demo URL: not yet published>` |
| `demo/README.md` | 4 | `<demo URL: not yet published>` |
| `demo/src/App.tsx` | 57 | `<repository URL: not yet published>` (page footer) |
| `articles/medium.md` | 59 | `<repository URL: not yet published>` and `<demo URL: not yet published>` |
| `articles/linkedin.md` | 12 | `<repository URL: not yet published>` and `<demo URL: not yet published>` |

The PDFs repeat the manuscript placeholder (manuscript PDF, section 10) and will be rebuilt with `scripts/build_publication.py` once the URL exists.
