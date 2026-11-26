<!-- SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0 -->
# TRUST: rules for every session

TRUST studies one question: when do average ratings misrank products compared with uncertainty-aware estimators? `master_prompt.md` is the authority. Never edit it. If this file and `master_prompt.md` conflict, `master_prompt.md` wins; record the conflict in `progress.md`.

## 1. Reading order (before modifying anything)

1. `master_prompt.md` (in full at least once per session; sections 2, 3, 10 and 11 are binding).
2. `roadmap.md` (current milestone, acceptance criteria, blockers).
3. `progress.md` (last entry and its next action).
4. `research/protocol.md` (draft or frozen status, hypotheses, metrics).
5. `research/claims_register.csv` (what may be said, and its evidence).

Then run `git status` and inspect existing files. Do not overwrite changes made by the owner. State the current milestone and the next bounded task before working.

## 2. Mandatory requirements (master prompt section 11)

- Maintain the publication tree of section 11.1: `research/experiment_registry.csv`, `research/protocol.md`, `research/claims_register.csv`, `research/paper/` (manuscript.md canonical, manuscript.tex and manuscript.pdf generated), `research/experiments/EXP-NNN/`, `research/publication/`.
- Stable identifiers: EXP-NNN for experiments, RUN-EXP-NNN-<cell>-<seed> for runs, FIG-NNN for figures, CLM-NNN for claims.
- Register every experiment before confirmatory execution. A seed is a run inside an experiment, not a new experiment. A new question or materially different protocol gets a new EXP id.
- Before each experiment: `research/experiments/EXP-NNN/protocol.md` following section 11.2, including what result would contradict the hypothesis.
- After each experiment: a standalone report with the 12 sections of 11.3, generated tables and figures from actual outputs, captions, units, sample sizes and alt text. Failed, null, abandoned and exploratory experiments keep their reports, labelled as such.
- One integrated manuscript (11.4), venue neutral, status "independent research manuscript / preprint draft, not peer-reviewed".
- Evidence pipeline (11.5): one generator for tables and figures, reused by reports, manuscript, demo and articles; a manifest maps every number to experiment, run ids, metric, result path, script, config hash and code revision. A second review pass must challenge the preferred hypothesis.
- Milestone additions (11.6): M0/M1 registry, skeleton, experiment protocols, zero-cost toolchain; M2 versioned schemas, run manifests and report generators beside the core code; M3 reports as experiments finish, provenance captured at run time; M4 evidence audit and synthesis, contradictions included; M5 identical numbers and labels in demo, paper, reports and articles; M6 PDFs compiled and visually inspected, clean-clone smoke reproduction, owner review checklist.
- Toolchain (decision D-002): Markdown is canonical. PDFs are built with pandoc to Typst, compiled by the `typst` Python package. `manuscript.tex` is generated from Markdown with pandoc. No TeX distribution is installed; never claim a PDF exists unless it was built and inspected.

## 3. Gates (the owner decides)

- **G-PUBLIC.** Never push, add a remote, create a GitHub repository, deploy or publish anything. The repository has been public at `https://github.com/mohamedbechirkefi/trust-rating-aggregation` since 2026-11-25 and the demo is hosted at `https://trust-rating-aggregation.kefimohamedbechir.workers.dev`; pushes and deploys are made by the coordinator on the owner's word, never by a session of this repository.
- **No paid service** of any kind. No paid APIs, inference, datasets, hosting or compute. The coding subscription is not an inference backend.
- **G-FREEZE.** Never freeze a protocol yourself. Freezing is the owner's decision, recorded with a hash in `research/decision_log.md`. Until then all runs are exploratory and labelled so.
- No confirmatory experiments before the owner freezes the protocol. Small exploratory smoke checks are allowed and labelled exploratory.

## 4. Scope

- Work only inside this repository. Tools outside it are used read-only: `../.tools/py/bin/` (uv, python with typst, pypdf, pillow), `../.tools/pandoc` (both relative to this repository), and Node at `helix/.tools/node/bin` in the owner's research workspace, two levels above this repository (never modify that folder; the session brief gives the absolute path).
- Do not touch any other folder of the owner's research workspace (the folder two levels above this repository).
- Never kill processes you did not start. Never delete anything you did not create in the current session.

## 5. Truthfulness

- Never fabricate results, citations, test counts or PDFs.
- Record the commands you ran and their actual outputs in `progress.md`.
- A source that was not opened is labelled unverified and is not cited as read.
- Synthetic results are labelled simulated. Real product quality is unobserved. Never label any review as fraudulent from these models.

## 6. Files and style

- New text and code files start with `SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0` as a comment where the format allows. JSON and CSV files are covered by `NOTICE.md`.
- English. No em dashes. Plain, formal register.
- No e-mail address, personal identifier or secret in any committed file (git author metadata excepted).
- Refer to the owner as "the owner" (they/them).
- Do not change the licence files (`LICENSE`, `NOTICE.md`, `LICENSE_HISTORY.md`, `CLA.md`, `.github/`). Development commands may be appended to `CONTRIBUTING.md`.
- Commits are local only, under the owner's git identity (`user.name=mohamedbechirkefi`, with the owner's e-mail passed by `-c user.email=...` as given in the session brief; it is not stored in this file). The message ends with a blank line, then the Co-Authored-By trailer for the AI assistant given in the session brief.

## 7. Session end

Update `progress.md` (dated entry: commands, actual outputs, failures, changed files, risks, next action) and `roadmap.md` statuses. Never mark incomplete work done.
