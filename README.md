<!-- SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0 -->
# TRUST: rating aggregation under uncertainty

**Question.** When do average ratings misrank products compared with uncertainty-aware estimators?

**Status: protocol v1.0 frozen by the owner on 2026-11-24 (`research/freeze.json`); no registered experiment has been run and there are no findings.** Only exploratory, simulated smoke and pilot runs exist (`results/exploratory/`), and they are not evidence.

## Why it matters

Ranking products by their average star rating lets products with very few reviews reach the top or bottom of a list by chance. Uncertainty-aware estimators (Bayesian shrinkage, lower credible bounds) are known fixes. This project plans a preregistered simulation that maps when the difference is material, with uncertainty and sensitivity checks. All evidence will be simulated: real product quality is unobserved, and nothing here labels any review as fraudulent.

## What exists now

- Control files: `CLAUDE.md`, `roadmap.md`, `progress.md`.
- Draft protocol: `research/protocol.md`; registered experiments in `research/experiment_registry.csv`.
- Literature scoping: `research/literature_review.md`. Data candidates and their licences: `data/manifest.json`.
- Manuscript skeleton: `research/paper/manuscript.md`.

- Engine (M2): `src/trust/` (simulation, MEAN, SHRINK, LCB, metrics, runner, versioned schemas, run manifests, report generator, CLI) and `tests/`.

What is not implemented yet: the confirmatory experiments (frozen, scheduled for M3), their reports, the manuscript results and the demo.

## Experiments

| ID | Title | Status |
|---|---|---|
| EXP-001 | Mean versus uncertainty-aware ranking under random reporting | frozen (owner-approved 2026-11-24), not yet run |
| EXP-002 | Reporting selection and quality-dependent missingness | frozen (owner-approved 2026-11-24), not yet run |
| EXP-003 | Sensitivity analyses that could invalidate the main interpretation | frozen (owner-approved 2026-11-24), not yet run |

## Quick start

```sh
uv sync --frozen
uv run --frozen pytest -q
PYTHONPATH=src uv run --frozen python -m trust.cli smoke     # exploratory, simulated
PYTHONPATH=src uv run --frozen python -m trust.cli report --dir results/exploratory/smoke --pdf
```

`trust.cli run --exp EXP-001` accepts only the frozen configs: a changed config, protocol or data manifest is refused (`research/freeze.json`).

## Data and licences

All evidence is simulated. MovieLens 1M (GroupLens; research use, no redistribution) calibrates two simulation parameters, the review-count dispersion and the quality distribution (`research/protocol.md` section 13). It is never bundled: `python scripts/download_movielens.py` fetches it into the git-ignored `data/raw/` and checks its SHA-256. This work uses the MovieLens data set: F. Maxwell Harper and Joseph A. Konstan, 2015, The MovieLens Datasets: History and Context, ACM TiiS 5(4), doi:10.1145/2827872; no endorsement by GroupLens is implied. See `data/manifest.json`.

## Licence

TRUST Source-Available Non-Commercial Research License v1.0 (`LicenseRef-TRUST-NC-Research-1.0`), see `LICENSE` and `NOTICE.md`. This is a custom source-available licence, not an OSI-approved open-source licence. Third-party material keeps its own terms.

## Citation

See `CITATION.cff`.
