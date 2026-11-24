<!-- SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0 -->
# src/

Python package `trust` (M2). Separate modules with typed, deterministic, seeded functions:

| Module | Role |
|---|---|
| `trust/model.py` | Formal model: rating probabilities, true quality `theta`, reporting probability, `theta_rep`, exposure weights |
| `trust/simulate.py` | Seeded catalogue generation (`SeedSequence([seed_root, exp_number, seed_index])`, four child streams) |
| `trust/estimators.py` | MEAN baseline, SHRINK(kappa), LCB (Dirichlet posterior), calibration intervals |
| `trust/metrics.py` | Deterministic ranking (score descending, id ascending), tau-b, Spearman, precision and regret at k, RMSE, coverage |
| `trust/config.py` | Config schema validation (`schemas/config-v1.json`), hashing, cell expansion, run ids |
| `trust/runner.py` | Runs every (cell, seed); one retry, failures recorded and never replaced |
| `trust/results.py` | Result schema 1.0.0 (`schemas/result-v1.json`), validated at export and import; run manifest |
| `trust/provenance.py` | Git revision, environment, peak memory, protocol freeze check |
| `trust/analysis.py` | Paired differences, percentile bootstrap, t interval, stratified pooled bootstrap |
| `trust/report.py` | The single generator of tables, figures, report.md and report.pdf from result files |
| `trust/cli.py` | `smoke`, `run`, `report`, `test` |

Run with `PYTHONPATH=src uv run --frozen python -m trust.cli <command>` (the project is not installed as a package).
