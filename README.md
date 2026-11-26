<!-- SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0 -->
# TRUST: rating aggregation under uncertainty

Author: Mohamed Bechir Kefi, independent researcher. Repository: <https://github.com/mohamedbechirkefi/trust-rating-aggregation>.

**Question.** When do average ratings misrank products compared with uncertainty-aware estimators?

**Status: protocol v1.0 frozen by the owner on 2026-11-24 (`research/freeze.json`); all three registered experiments ran in full on 2026-11-24 (1,560 of 1,560 simulated runs ok) and have standalone reports. The integrated manuscript is a draft (M4): independent research manuscript / preprint draft, not peer-reviewed. A static, offline interactive demo exists (M5, `demo/`). The owner approved the funding, competing-interest and AI-use statements on 2026-11-25. A release candidate (M6) is prepared and awaits the owner's review; the repository has been public since 2026-11-25, and no tag or release exists yet.** All results are simulated. In this model, shrinkage towards the catalogue mean ranks better than the average rating when ratings are noisy and worse when they are precise, and the advantage reverses under a misspecified shrinkage centre or population shape (`research/paper/manuscript.md`).

## Why it matters

Ranking products by their average star rating lets products with very few reviews reach the top or bottom of a list by chance. Uncertainty-aware estimators (Bayesian shrinkage, lower credible bounds) are known fixes. This project ran a preregistered simulation that maps when the difference is material, with uncertainty and sensitivity checks. All evidence is simulated: real product quality is unobserved, and nothing here labels any review as fraudulent.

## What exists now

- Control files: `CLAUDE.md`, `roadmap.md`, `progress.md`.
- Frozen protocol (v1.0, 2026-11-24): `research/protocol.md`; registered experiments in `research/experiment_registry.csv`. The status lines of the frozen protocols (`research/protocol.md`, `research/experiments/EXP-00N/protocol.md`) still say "not yet run" because frozen files are not edited; the experiment registry and the reports give the current state.
- Literature scoping: `research/literature_review.md`. Data candidates and their licences: `data/manifest.json`.
- Manuscript draft: `research/paper/manuscript.md` and `research/paper/supplementary.md`; experiment reports `research/experiments/EXP-00N/report.md`; evidence audit `research/publication/evidence_audit.md`.

- Engine (M2): `src/trust/` (simulation, MEAN, SHRINK, LCB, metrics, runner, versioned schemas, run manifests, report generator, CLI) and `tests/`.

- Interactive demo (M5): `demo/`, a static page with the published results, effect sizes and intervals, and a rating explorer sandbox. Its numbers come from `demo/public/data/results.json`, written by `scripts/export_demo_data.py` from committed results only; `tests/test_demo_export.py` checks that every number it shows is printed verbatim in the manuscript.

Drafts of the Medium and LinkedIn articles are in `articles/` (not published).

- Release candidate (M6): PDFs of the manuscript, supplement and reports (`research/paper/manuscript.pdf`, `research/paper/supplementary.pdf`, `research/experiments/EXP-00N/report.pdf`, built by `scripts/build_publication.py` and visually inspected), a clean-clone reproduction (`research/publication/reproducibility_report.md`), dependency licences (`research/publication/dependency_licences.md`) and the owner review checklist (`research/publication/author_review.md`). What is not done: the owner's full-text review and sign-off, and the release (tag and GitHub release).

## Key results (simulated, confirmatory)

Numbers as printed in `research/paper/manuscript.md` section 5; intervals are two-sided 95% stratified bootstrap intervals.

- Primary estimand: SHRINK_5 minus MEAN in Kendall tau-b, pooled over nine cells, 0.0046 (0.0030 to 0.0061). H1 is supported under the frozen rule, but the direction depends on the noise level: -0.0198 (-0.0225 to -0.0172) at 0.5 stars, 0.0085 (0.0056 to 0.0113) at 1.0 and 0.0250 (0.0224 to 0.0277) at 1.5.
- H1b (the advantage fades with review count) is contradicted; H1c is not supported: LCB minus MEAN is -0.0647 (-0.0689 to -0.0604).
- Sensitivity: a half-star error in the shrinkage centre gives -0.0406 (-0.0449 to -0.0361) and -0.0485 (-0.0525 to -0.0444); a uniform quality population gives -0.0210 (-0.0228 to -0.0192). Both invalidation criteria are met.
- Disclosed deviations accepted by the owner: Holm p-values from the bootstrap (D-011); the registered S3 check cannot discriminate by design (D-012).

## Experiments

| ID | Title | Status |
|---|---|---|
| EXP-001 | Mean versus uncertainty-aware ranking under random reporting | complete (confirmatory); report in `research/experiments/EXP-001/report.md` |
| EXP-002 | Reporting selection and quality-dependent missingness | complete (confirmatory); report in `research/experiments/EXP-002/report.md` |
| EXP-003 | Sensitivity analyses that could invalidate the main interpretation | complete (confirmatory); report in `research/experiments/EXP-003/report.md` |

## Quick start

```sh
uv sync --frozen
uv run --frozen pytest -q
PYTHONPATH=src uv run --frozen python -m trust.cli smoke     # exploratory, simulated
PYTHONPATH=src uv run --frozen python -m trust.cli report --dir results/exploratory/smoke --pdf
```

`trust.cli run --exp EXP-001` accepts only the frozen configs: a changed config, protocol or data manifest is refused (`research/freeze.json`).

## Interactive demo

![TRUST demo page: the question, the status label, the three value labels (published result, assumption, sandbox output) and FIG-001, a dot-and-interval chart of SHRINK_5 minus MEAN in Kendall tau-b for the nine EXP-001 cells, the three noise levels and the pooled estimate.](docs/demo.png)

The demo is a static page that runs offline after the first load and sends nothing anywhere. Demo URL: <https://trust-rating-aggregation.kefimohamedbechir.workers.dev> (Cloudflare Workers static assets, free plan; see `demo/README.md`).

```sh
cd demo && npm ci && npm run build && npm run preview
```

`npm test` runs the vitest suite, including the check of the browser engine against the Python engine (`scripts/make_sandbox_fixture.py`). `.venv/bin/python scripts/export_demo_data.py` regenerates the results file.

## Data and licences

All evidence is simulated. MovieLens 1M (GroupLens; research use, no redistribution) calibrates two simulation parameters, the review-count dispersion and the quality distribution (`research/protocol.md` section 13). It is never bundled: `python scripts/download_movielens.py` fetches it into the git-ignored `data/raw/` and checks its SHA-256. This work uses the MovieLens data set: F. Maxwell Harper and Joseph A. Konstan, 2015, The MovieLens Datasets: History and Context, ACM TiiS 5(4), doi:10.1145/2827872; no endorsement by GroupLens is implied. See `data/manifest.json`.

## Licence

TRUST Source-Available Non-Commercial Research License v1.0 (`LicenseRef-TRUST-NC-Research-1.0`), see `LICENSE` and `NOTICE.md`. This is a custom source-available licence, not an OSI-approved open-source licence. Third-party material keeps its own terms.

## Citation

See `CITATION.cff`.
