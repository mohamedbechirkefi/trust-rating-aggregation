<!-- SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0 -->

# X-SMOKE run report (exploratory)

**EXPLORATORY, SIMULATED. Not a finding.** Generated before any protocol freeze. These numbers check the pipeline and inform planning; they are not evidence for any hypothesis.

- Description: Smoke matrix of research/protocol.md section 7 (exploratory, simulated): pipeline check, runtime, SD of D.
- Config SHA-256: `8a834b2b3d89d09dd5bd109047a9999f3038031e485ce26920dceb33c80f813f`
- Results SHA-256: `8fe78903201e533d2734e44686c6c4005609b00eb01e1c4611ab1ee25ff3ad40` (`results.json`, schema 1.0.0)
- Code revision: `bd9e1460e29389def8baa43d6ca7cc553d659ff1`
- Environment: Python 3.12.1, numpy 2.3.4, scipy 1.16.2; Apple M1 Pro; Darwin 24.3.0 (macOS-15.3.1-arm64-arm-64bit)
- Catalogue size N = 50; seeds per cell = 3; cells = 2; runs = 6; failed runs = 0
- Truth: `theta`; min reviews for evaluation: 0; top k = 10
- Machine-readable outputs: `results.json`, `run_manifest.json`, `metrics.csv` (24 rows), `summary.json`, `evidence_manifest.json`

## Cells

| Cell | Grid values | Mean potential raters | Mean reported | Share with zero reviews | s_pool (stars) |
|---|---|---|---|---|---|
| c00 | nu=3 | 2.93 | 2.93 | 0.187 | 0.960 |
| c01 | nu=30 | 31.43 | 31.43 | 0.027 | 0.931 |

## Mean metric per arm and cell

Means over seeds. tau-b and Spearman are unitless; precision at k and coverage are proportions; regret at k and RMSE are in stars. Coverage is of nominal 90% intervals among products with at least 2 reviews.

| Cell | Arm | tau-b | Spearman | P@k | Regret@k | Coverage | RMSE |
|---|---|---|---|---|---|---|---|
| c00 | MEAN | 0.5171 | 0.6729 | 0.567 | 0.2118 | 0.948 | 0.5470 |
| c00 | SHRINK_5 | 0.5347 | 0.6904 | 0.633 | 0.1740 | 0.834 | 0.4467 |
| c00 | LCB | 0.3595 | 0.4897 | 0.533 | 0.2687 | 0.788 | 1.3090 |
| c00 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |
| c01 | MEAN | 0.7698 | 0.9138 | 0.700 | 0.0697 | 0.903 | 0.2397 |
| c01 | SHRINK_5 | 0.7748 | 0.9233 | 0.767 | 0.0331 | 0.875 | 0.2122 |
| c01 | LCB | 0.6027 | 0.7648 | 0.600 | 0.1319 | 0.834 | 0.6830 |
| c01 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |

## Paired differences in Kendall tau-b against MEAN

Per cell: mean of per-seed paired differences, SD over seeds, 95% percentile bootstrap (10000 resamples, fixed seed) and t interval, and the standardised paired difference (mean/SD).

### SHRINK_5 minus MEAN

| Cell | Seeds | Mean | SD | Bootstrap 95% | t 95% | Half-width | Mean/SD |
|---|---|---|---|---|---|---|---|
| c00 | 3 | 0.0176 | 0.0065 | 0.0123 to 0.0249 | 0.0013 to 0.0338 | 0.0063 | 2.69 |
| c01 | 3 | 0.0049 | 0.0235 | -0.0219 to 0.0217 | -0.0534 to 0.0633 | 0.0218 | 0.21 |

### LCB minus MEAN

| Cell | Seeds | Mean | SD | Bootstrap 95% | t 95% | Half-width | Mean/SD |
|---|---|---|---|---|---|---|---|
| c00 | 3 | -0.1575 | 0.0323 | -0.1936 to -0.1311 | -0.2378 to -0.0773 | 0.0312 | -4.87 |
| c01 | 3 | -0.1671 | 0.0627 | -0.2147 to -0.0960 | -0.3230 to -0.0113 | 0.0594 | -2.66 |

Pooled over cells (equal weight, stratified bootstrap):

| Contrast | Cells | Pooled mean | 95% interval | One-sided 95% lower bound |
|---|---|---|---|---|
| SHRINK_5 minus MEAN | 2 | 0.0113 | -0.0016 to 0.0206 | 0.0019 |
| LCB minus MEAN | 2 | -0.1623 | -0.1925 to -0.1293 | -0.1885 |

![X-SMOKE: tau-b(SHRINK_5) minus tau-b(MEAN) per cell. EXPLORATORY, simulated. Dot-and-interval chart. One row per cell; the dot is the mean paired difference in Kendall tau-b over seeds and the bar its 95% percentile bootstrap interval (10000 resamples). Seeds per cell: 3, 3. The dashed line marks zero.](figures/fig_primary_contrast.svg){fig-alt="EXPLORATORY, simulated. Dot-and-interval chart. One row per cell; the dot is the mean paired difference in Kendall tau-b over seeds and the bar its 95% percentile bootstrap interval (10000 resamples). Seeds per cell: 3, 3. The dashed line marks zero."}

## Checks, failures and degenerate cases

- Minimum ORACLE tau-b over runs: 1.000000000000 (must equal 1).
- Failed runs: 0.
- Degenerate-case flags: 0.
- Runtime per run: mean 10.59 ms, median 3.98 ms, max 45.40 ms; wall time 0.06 s; process peak RSS 92.5 MiB.
