<!-- SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0 -->

# X-PILOT-001 run report (exploratory)

**EXPLORATORY, SIMULATED. Not a finding.** Generated before any protocol freeze. These numbers check the pipeline and inform planning; they are not evidence for any hypothesis.

- Description: Exploratory variance pilot (simulated) at the four corner cells of the EXP-001 grid, N = 200, seed namespace 901 disjoint from every confirmatory seed. Purpose: per-seed SD of D and runtime per run at full catalogue size.
- Config SHA-256: `a28345ec364b1461f66545b2673895137182acc53493c348489d4894ec723c68`
- Results SHA-256: `528150705b63300b6d084740ae983c4c04acd2070f567f9a4f608670871cf492` (`results.json`, schema 1.0.0)
- Code revision: `e1ad9bb780aad7e32b9832aec603ae072fc8a607`
- Environment: Python 3.12.1, numpy 2.3.4, scipy 1.16.2; Apple M1 Pro; Darwin 24.3.0 (macOS-15.3.1-arm64-arm-64bit)
- Catalogue size N = 200; seeds per cell = 10; cells = 4; runs = 40; failed runs = 0
- Truth: `theta`; min reviews for evaluation: 0; top k = 10
- Machine-readable outputs: `results.json`, `run_manifest.json`, `metrics.csv` (240 rows), `summary.json`, `evidence_manifest.json`

## Cells

| Cell | Grid values | Mean potential raters | Mean reported | Share with zero reviews | s_pool (stars) |
|---|---|---|---|---|---|
| c00 | nu=3, sigma=0.5 | 2.96 | 2.96 | 0.255 | 0.553 |
| c01 | nu=3, sigma=1.5 | 2.96 | 2.96 | 0.255 | 1.182 |
| c02 | nu=30, sigma=0.5 | 29.23 | 29.23 | 0.034 | 0.561 |
| c03 | nu=30, sigma=1.5 | 29.23 | 29.23 | 0.034 | 1.192 |

## Mean metric per arm and cell

Means over seeds. tau-b and Spearman are unitless; precision at k and coverage are proportions; regret at k and RMSE are in stars. Coverage is of nominal 90% intervals among products with at least 2 reviews.

| Cell | Arm | tau-b | Spearman | P@k | Regret@k | Coverage | RMSE |
|---|---|---|---|---|---|---|---|
| c00 | MEAN | 0.5895 | 0.7451 | 0.340 | 0.2476 | 0.902 | 0.4785 |
| c00 | SHRINK_1 | 0.5842 | 0.7486 | 0.330 | 0.1797 | 0.877 | 0.4520 |
| c00 | SHRINK_5 | 0.5663 | 0.7394 | 0.270 | 0.2057 | 0.506 | 0.5373 |
| c00 | SHRINK_20 | 0.5533 | 0.7312 | 0.230 | 0.2419 | 0.221 | 0.6325 |
| c00 | LCB | 0.2913 | 0.3969 | 0.150 | 0.3452 | 0.721 | 1.3736 |
| c00 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |
| c01 | MEAN | 0.3757 | 0.5141 | 0.120 | 0.4839 | 0.904 | 0.7380 |
| c01 | SHRINK_1 | 0.3839 | 0.5292 | 0.190 | 0.3013 | 0.928 | 0.5269 |
| c01 | SHRINK_5 | 0.3874 | 0.5364 | 0.210 | 0.2816 | 0.897 | 0.4548 |
| c01 | SHRINK_20 | 0.3822 | 0.5324 | 0.190 | 0.2674 | 0.574 | 0.4957 |
| c01 | LCB | 0.2734 | 0.3838 | 0.170 | 0.3075 | 0.852 | 1.2685 |
| c01 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |
| c02 | MEAN | 0.8302 | 0.9474 | 0.650 | 0.0819 | 0.896 | 0.2266 |
| c02 | SHRINK_1 | 0.8309 | 0.9495 | 0.700 | 0.0486 | 0.898 | 0.2107 |
| c02 | SHRINK_5 | 0.8057 | 0.9391 | 0.600 | 0.0489 | 0.702 | 0.2753 |
| c02 | SHRINK_20 | 0.7521 | 0.9140 | 0.460 | 0.0979 | 0.292 | 0.4120 |
| c02 | LCB | 0.5808 | 0.7252 | 0.430 | 0.1085 | 0.806 | 0.7286 |
| c02 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |
| c03 | MEAN | 0.6415 | 0.8150 | 0.240 | 0.3267 | 0.896 | 0.3981 |
| c03 | SHRINK_1 | 0.6542 | 0.8302 | 0.360 | 0.2132 | 0.904 | 0.3219 |
| c03 | SHRINK_5 | 0.6637 | 0.8444 | 0.450 | 0.1176 | 0.907 | 0.2836 |
| c03 | SHRINK_20 | 0.6470 | 0.8371 | 0.410 | 0.1029 | 0.693 | 0.3374 |
| c03 | LCB | 0.5167 | 0.6791 | 0.370 | 0.1149 | 0.884 | 0.7368 |
| c03 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |

## Paired differences in Kendall tau-b against MEAN

Per cell: mean of per-seed paired differences, SD over seeds, 95% percentile bootstrap (10000 resamples, fixed seed) and t interval, and the standardised paired difference (mean/SD).

### SHRINK_1 minus MEAN

| Cell | Seeds | Mean | SD | Bootstrap 95% | t 95% | Half-width | Mean/SD |
|---|---|---|---|---|---|---|---|
| c00 | 10 | -0.0053 | 0.0047 | -0.0082 to -0.0028 | -0.0087 to -0.0019 | 0.0027 | -1.12 |
| c01 | 10 | 0.0082 | 0.0048 | 0.0052 to 0.0109 | 0.0047 to 0.0116 | 0.0028 | 1.70 |
| c02 | 10 | 0.0007 | 0.0050 | -0.0023 to 0.0037 | -0.0029 to 0.0043 | 0.0030 | 0.14 |
| c03 | 10 | 0.0127 | 0.0054 | 0.0098 to 0.0161 | 0.0089 to 0.0165 | 0.0032 | 2.37 |

### SHRINK_5 minus MEAN

| Cell | Seeds | Mean | SD | Bootstrap 95% | t 95% | Half-width | Mean/SD |
|---|---|---|---|---|---|---|---|
| c00 | 10 | -0.0232 | 0.0064 | -0.0271 to -0.0196 | -0.0278 to -0.0186 | 0.0038 | -3.63 |
| c01 | 10 | 0.0117 | 0.0072 | 0.0075 to 0.0160 | 0.0065 to 0.0169 | 0.0043 | 1.61 |
| c02 | 10 | -0.0245 | 0.0103 | -0.0303 to -0.0183 | -0.0318 to -0.0171 | 0.0060 | -2.37 |
| c03 | 10 | 0.0223 | 0.0128 | 0.0154 to 0.0304 | 0.0131 to 0.0314 | 0.0075 | 1.74 |

### SHRINK_20 minus MEAN

| Cell | Seeds | Mean | SD | Bootstrap 95% | t 95% | Half-width | Mean/SD |
|---|---|---|---|---|---|---|---|
| c00 | 10 | -0.0362 | 0.0078 | -0.0410 to -0.0320 | -0.0418 to -0.0307 | 0.0045 | -4.66 |
| c01 | 10 | 0.0065 | 0.0089 | 0.0012 to 0.0117 | 0.0002 to 0.0129 | 0.0053 | 0.73 |
| c02 | 10 | -0.0781 | 0.0156 | -0.0867 to -0.0685 | -0.0893 to -0.0669 | 0.0091 | -4.99 |
| c03 | 10 | 0.0055 | 0.0204 | -0.0057 to 0.0180 | -0.0090 to 0.0201 | 0.0118 | 0.27 |

### LCB minus MEAN

| Cell | Seeds | Mean | SD | Bootstrap 95% | t 95% | Half-width | Mean/SD |
|---|---|---|---|---|---|---|---|
| c00 | 10 | -0.2982 | 0.0428 | -0.3229 to -0.2728 | -0.3288 to -0.2676 | 0.0251 | -6.97 |
| c01 | 10 | -0.1023 | 0.0449 | -0.1295 to -0.0760 | -0.1345 to -0.0702 | 0.0268 | -2.28 |
| c02 | 10 | -0.2494 | 0.0283 | -0.2641 to -0.2309 | -0.2696 to -0.2292 | 0.0166 | -8.82 |
| c03 | 10 | -0.1248 | 0.0287 | -0.1411 to -0.1079 | -0.1454 to -0.1043 | 0.0166 | -4.34 |

Pooled over cells (equal weight, stratified bootstrap):

| Contrast | Cells | Pooled mean | 95% interval | One-sided 95% lower bound |
|---|---|---|---|---|
| SHRINK_1 minus MEAN | 4 | 0.0041 | 0.0026 to 0.0056 | 0.0029 |
| SHRINK_5 minus MEAN | 4 | -0.0034 | -0.0062 to -0.0005 | -0.0057 |
| SHRINK_20 minus MEAN | 4 | -0.0256 | -0.0296 to -0.0212 | -0.0290 |
| LCB minus MEAN | 4 | -0.1937 | -0.2045 to -0.1827 | -0.2028 |

![X-PILOT-001: tau-b(SHRINK_5) minus tau-b(MEAN) per cell. EXPLORATORY, simulated. Dot-and-interval chart. One row per cell; the dot is the mean paired difference in Kendall tau-b over seeds and the bar its 95% percentile bootstrap interval (10000 resamples). Seeds per cell: 10, 10, 10, 10. The dashed line marks zero.](figures/fig_primary_contrast.svg){fig-alt="EXPLORATORY, simulated. Dot-and-interval chart. One row per cell; the dot is the mean paired difference in Kendall tau-b over seeds and the bar its 95% percentile bootstrap interval (10000 resamples). Seeds per cell: 10, 10, 10, 10. The dashed line marks zero."}

## Checks, failures and degenerate cases

- Minimum ORACLE tau-b over runs: 1.000000000000 (must equal 1).
- Failed runs: 0.
- Degenerate-case flags: 0.
- Runtime per run: mean 3.46 ms, median 3.35 ms, max 5.03 ms; wall time 0.14 s; process peak RSS 92.9 MiB.
