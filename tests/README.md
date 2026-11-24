<!-- SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0 -->
# tests/

pytest suite (M2), run with `uv run --frozen pytest` or `PYTHONPATH=src uv run --frozen python -m trust.cli test`.

- `test_model.py`: rating probabilities and `theta` against hand-computed values, bounds, monotonicity, symmetry, reporting probabilities, invalid parameters.
- `test_estimators.py`: empty reviews, one review, hand-computed posterior formulas (Dirichlet mean and variance, shrinkage, pooled SD), bounds, shrinkage between mean and prior, differential check against raw rating lists, invalid inputs.
- `test_metrics.py`: deterministic sorting and tie-break, tau-b hand example with ties, differential test of tau-b against an O(N^2) reference, precision, regret, RMSE, coverage, invalid inputs.
- `test_simulate.py`: determinism, common random numbers across cells, bounded ratings, selection, invalid parameters.
- `test_pipeline.py`: config validation, run determinism, ORACLE tau-b equal to 1, retry and failure recording, degenerate catalogues, schema validation failing closed, CLI end to end, refusal of unfrozen confirmatory configs, freeze-check logic.
