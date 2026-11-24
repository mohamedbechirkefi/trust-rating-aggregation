<!-- SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0 -->

# X-PILOT-002 run report (exploratory)

**EXPLORATORY, SIMULATED. Not a finding.** Generated before any protocol freeze. These numbers check the pipeline and inform planning; they are not evidence for any hypothesis.

- Description: Exploratory variance pilot (simulated) for the EXP-002 lambda contrast at nu = 3, sigma = 1.0, gamma in {-0.5, 0.5}, N = 200, seed namespace 902 disjoint from every confirmatory seed.
- Config SHA-256: `db3a137c49f52c40104c6889142f9954cb492f0c287348bd47ecbed4bfa732c9`
- Results SHA-256: `9dfed331489712be2e87662ad583e0b041d3b820476a1c2c0d86215baa93a4f9` (`results.json`, schema 1.0.0)
- Code revision: `e1ad9bb780aad7e32b9832aec603ae072fc8a607`
- Environment: Python 3.12.1, numpy 2.3.4, scipy 1.16.2; Apple M1 Pro; Darwin 24.3.0 (macOS-15.3.1-arm64-arm-64bit)
- Catalogue size N = 200; seeds per cell = 10; cells = 4; runs = 40; failed runs = 0
- Truth: `theta`; min reviews for evaluation: 0; top k = 10
- Machine-readable outputs: `results.json`, `run_manifest.json`, `metrics.csv` (240 rows), `summary.json`, `evidence_manifest.json`

## Cells

| Cell | Grid values | Mean potential raters | Mean reported | Share with zero reviews | s_pool (stars) |
|---|---|---|---|---|---|
| c00 | gamma=-0.5, lam=0.0 | 3.13 | 3.13 | 0.271 | 0.962 |
| c01 | gamma=0.5, lam=0.0 | 3.08 | 3.08 | 0.261 | 0.882 |
| c02 | gamma=-0.5, lam=2.0 | 3.13 | 2.05 | 0.344 | 1.046 |
| c03 | gamma=0.5, lam=2.0 | 3.08 | 2.19 | 0.347 | 0.868 |

## Mean metric per arm and cell

Means over seeds. tau-b and Spearman are unitless; precision at k and coverage are proportions; regret at k and RMSE are in stars. Coverage is of nominal 90% intervals among products with at least 2 reviews.

| Cell | Arm | tau-b | Spearman | P@k | Regret@k | Coverage | RMSE |
|---|---|---|---|---|---|---|---|
| c00 | MEAN | 0.3972 | 0.5339 | 0.190 | 0.3994 | 0.908 | 0.6757 |
| c00 | SHRINK_1 | 0.3980 | 0.5408 | 0.180 | 0.3633 | 0.919 | 0.5653 |
| c00 | SHRINK_5 | 0.3873 | 0.5302 | 0.170 | 0.3630 | 0.771 | 0.5908 |
| c00 | SHRINK_20 | 0.3764 | 0.5187 | 0.150 | 0.4208 | 0.395 | 0.6591 |
| c00 | LCB | 0.1143 | 0.1607 | 0.110 | 0.5201 | 0.804 | 1.4090 |
| c00 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |
| c01 | MEAN | 0.4256 | 0.5772 | 0.150 | 0.4623 | 0.894 | 0.6895 |
| c01 | SHRINK_1 | 0.4279 | 0.5858 | 0.300 | 0.2621 | 0.913 | 0.5784 |
| c01 | SHRINK_5 | 0.4256 | 0.5861 | 0.320 | 0.1673 | 0.833 | 0.5933 |
| c01 | SHRINK_20 | 0.4212 | 0.5838 | 0.290 | 0.1829 | 0.485 | 0.6455 |
| c01 | LCB | 0.4047 | 0.5485 | 0.240 | 0.2232 | 0.748 | 1.2672 |
| c01 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |
| c02 | MEAN | 0.3709 | 0.4984 | 0.140 | 0.4920 | 0.887 | 0.7441 |
| c02 | SHRINK_1 | 0.3726 | 0.5038 | 0.190 | 0.3797 | 0.916 | 0.5682 |
| c02 | SHRINK_5 | 0.3607 | 0.4911 | 0.140 | 0.4435 | 0.843 | 0.5596 |
| c02 | SHRINK_20 | 0.3546 | 0.4848 | 0.120 | 0.4655 | 0.422 | 0.6238 |
| c02 | LCB | 0.1821 | 0.2524 | 0.120 | 0.5325 | 0.873 | 1.4538 |
| c02 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |
| c03 | MEAN | 0.3605 | 0.4912 | 0.130 | 0.4992 | 0.832 | 0.8414 |
| c03 | SHRINK_1 | 0.3664 | 0.5018 | 0.280 | 0.2634 | 0.856 | 0.7248 |
| c03 | SHRINK_5 | 0.3754 | 0.5121 | 0.320 | 0.1704 | 0.743 | 0.7396 |
| c03 | SHRINK_20 | 0.3709 | 0.5080 | 0.280 | 0.1816 | 0.548 | 0.7831 |
| c03 | LCB | 0.4202 | 0.5636 | 0.240 | 0.2284 | 0.854 | 1.3149 |
| c03 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |

## Paired differences in Kendall tau-b against MEAN

Per cell: mean of per-seed paired differences, SD over seeds, 95% percentile bootstrap (10000 resamples, fixed seed) and t interval, and the standardised paired difference (mean/SD).

### SHRINK_1 minus MEAN

| Cell | Seeds | Mean | SD | Bootstrap 95% | t 95% | Half-width | Mean/SD |
|---|---|---|---|---|---|---|---|
| c00 | 10 | 0.0007 | 0.0042 | -0.0017 to 0.0033 | -0.0023 to 0.0038 | 0.0025 | 0.17 |
| c01 | 10 | 0.0022 | 0.0041 | -0.0002 to 0.0046 | -0.0007 to 0.0052 | 0.0024 | 0.55 |
| c02 | 10 | 0.0017 | 0.0041 | -0.0006 to 0.0042 | -0.0012 to 0.0046 | 0.0024 | 0.41 |
| c03 | 10 | 0.0059 | 0.0054 | 0.0030 to 0.0093 | 0.0020 to 0.0097 | 0.0032 | 1.09 |

### SHRINK_5 minus MEAN

| Cell | Seeds | Mean | SD | Bootstrap 95% | t 95% | Half-width | Mean/SD |
|---|---|---|---|---|---|---|---|
| c00 | 10 | -0.0099 | 0.0124 | -0.0172 to -0.0027 | -0.0188 to -0.0010 | 0.0073 | -0.80 |
| c01 | 10 | -0.0000 | 0.0073 | -0.0044 to 0.0042 | -0.0053 to 0.0052 | 0.0043 | -0.00 |
| c02 | 10 | -0.0103 | 0.0132 | -0.0182 to -0.0028 | -0.0197 to -0.0009 | 0.0077 | -0.78 |
| c03 | 10 | 0.0149 | 0.0085 | 0.0103 to 0.0203 | 0.0089 to 0.0210 | 0.0050 | 1.77 |

### SHRINK_20 minus MEAN

| Cell | Seeds | Mean | SD | Bootstrap 95% | t 95% | Half-width | Mean/SD |
|---|---|---|---|---|---|---|---|
| c00 | 10 | -0.0208 | 0.0146 | -0.0295 to -0.0126 | -0.0313 to -0.0104 | 0.0085 | -1.43 |
| c01 | 10 | -0.0044 | 0.0107 | -0.0112 to 0.0014 | -0.0121 to 0.0032 | 0.0063 | -0.42 |
| c02 | 10 | -0.0164 | 0.0143 | -0.0249 to -0.0084 | -0.0266 to -0.0062 | 0.0083 | -1.15 |
| c03 | 10 | 0.0104 | 0.0086 | 0.0054 to 0.0157 | 0.0042 to 0.0165 | 0.0052 | 1.20 |

### LCB minus MEAN

| Cell | Seeds | Mean | SD | Bootstrap 95% | t 95% | Half-width | Mean/SD |
|---|---|---|---|---|---|---|---|
| c00 | 10 | -0.2830 | 0.0234 | -0.2961 to -0.2686 | -0.2997 to -0.2663 | 0.0138 | -12.10 |
| c01 | 10 | -0.0209 | 0.0317 | -0.0395 to -0.0025 | -0.0436 to 0.0018 | 0.0185 | -0.66 |
| c02 | 10 | -0.1888 | 0.0305 | -0.2051 to -0.1697 | -0.2106 to -0.1670 | 0.0177 | -6.19 |
| c03 | 10 | 0.0597 | 0.0391 | 0.0367 to 0.0830 | 0.0318 to 0.0877 | 0.0231 | 1.53 |

Pooled over cells (equal weight, stratified bootstrap):

| Contrast | Cells | Pooled mean | 95% interval | One-sided 95% lower bound |
|---|---|---|---|---|
| SHRINK_1 minus MEAN | 4 | 0.0026 | 0.0014 to 0.0040 | 0.0016 |
| SHRINK_5 minus MEAN | 4 | -0.0013 | -0.0044 to 0.0018 | -0.0039 |
| SHRINK_20 minus MEAN | 4 | -0.0078 | -0.0115 to -0.0043 | -0.0109 |
| LCB minus MEAN | 4 | -0.1082 | -0.1172 to -0.0990 | -0.1159 |

![X-PILOT-002: tau-b(SHRINK_5) minus tau-b(MEAN) per cell. EXPLORATORY, simulated. Dot-and-interval chart. One row per cell; the dot is the mean paired difference in Kendall tau-b over seeds and the bar its 95% percentile bootstrap interval (10000 resamples). Seeds per cell: 10, 10, 10, 10. The dashed line marks zero.](figures/fig_primary_contrast.svg){fig-alt="EXPLORATORY, simulated. Dot-and-interval chart. One row per cell; the dot is the mean paired difference in Kendall tau-b over seeds and the bar its 95% percentile bootstrap interval (10000 resamples). Seeds per cell: 10, 10, 10, 10. The dashed line marks zero."}

## Checks, failures and degenerate cases

- Minimum ORACLE tau-b over runs: 1.000000000000 (must equal 1).
- Failed runs: 0.
- Degenerate-case flags: 0.
- Runtime per run: mean 3.30 ms, median 3.25 ms, max 5.03 ms; wall time 0.13 s; process peak RSS 91.2 MiB.
