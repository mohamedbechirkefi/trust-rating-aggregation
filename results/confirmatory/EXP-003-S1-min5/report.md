<!-- SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0 -->

# EXP-003 run report (confirmatory)

**Simulated.** Results hold only under the model in `research/protocol.md`.

- Description: EXP-003 S1: EXP-001 catalogues, metrics on products with n >= 5. Frozen v1.0 (owner-approved 2026-11-24, round 2): MovieLens-calibrated base (protocol 13.1), LCB prior centred on the catalogue mean (13.2 A-1).
- Config SHA-256: `bb6678dec6cf605f5dac42ceede1cafedfbe538508af9c230ab764dc0c3b7eca`
- Results SHA-256: `06a8b632b65a7e31fe50e4c454abef74c39e8fe020ddff61d0231f0540204c25` (`results.json`, schema 1.0.0)
- Code revision: `bd9e1460e29389def8baa43d6ca7cc553d659ff1`
- Environment: Python 3.12.1, numpy 2.3.4, scipy 1.16.2; Apple M1 Pro; Darwin 24.3.0 (macOS-15.3.1-arm64-arm-64bit)
- Catalogue size N = 200; seeds per cell = 20; cells = 9; runs = 180; failed runs = 0
- Truth: `theta`; min reviews for evaluation: 5; top k = 10
- Machine-readable outputs: `results.json`, `run_manifest.json`, `metrics.csv` (1080 rows), `summary.json`, `evidence_manifest.json`

## Cells

| Cell | Grid values | Mean potential raters | Mean reported | Share with zero reviews | s_pool (stars) |
|---|---|---|---|---|---|
| c00 | nu=3, sigma=0.5 | 3.11 | 3.11 | 0.381 | 0.572 |
| c01 | nu=3, sigma=1.0 | 3.11 | 3.11 | 0.381 | 0.967 |
| c02 | nu=3, sigma=1.5 | 3.11 | 3.11 | 0.381 | 1.236 |
| c03 | nu=10, sigma=0.5 | 10.28 | 10.28 | 0.220 | 0.576 |
| c04 | nu=10, sigma=1.0 | 10.28 | 10.28 | 0.220 | 0.962 |
| c05 | nu=10, sigma=1.5 | 10.28 | 10.28 | 0.220 | 1.243 |
| c06 | nu=30, sigma=0.5 | 30.41 | 30.41 | 0.132 | 0.573 |
| c07 | nu=30, sigma=1.0 | 30.41 | 30.41 | 0.132 | 0.960 |
| c08 | nu=30, sigma=1.5 | 30.41 | 30.41 | 0.132 | 1.239 |

## Mean metric per arm and cell

Means over seeds. tau-b and Spearman are unitless; precision at k and coverage are proportions; regret at k and RMSE are in stars. Coverage is of nominal 90% intervals among products with at least 2 reviews.

| Cell | Arm | tau-b | Spearman | P@k | Regret@k | Coverage | RMSE |
|---|---|---|---|---|---|---|---|
| c00 | MEAN | 0.8276 | 0.9494 | 0.790 | 0.0429 | 0.897 | 0.1984 |
| c00 | SHRINK_1 | 0.8261 | 0.9500 | 0.790 | 0.0413 | 0.892 | 0.1938 |
| c00 | SHRINK_5 | 0.8158 | 0.9463 | 0.750 | 0.0579 | 0.600 | 0.2906 |
| c00 | SHRINK_20 | 0.7845 | 0.9328 | 0.720 | 0.0753 | 0.219 | 0.4764 |
| c00 | LCB | 0.7896 | 0.9322 | 0.725 | 0.0761 | 0.736 | 0.4320 |
| c00 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |
| c01 | MEAN | 0.6973 | 0.8684 | 0.685 | 0.1002 | 0.899 | 0.3410 |
| c01 | SHRINK_1 | 0.6972 | 0.8708 | 0.690 | 0.0953 | 0.906 | 0.3081 |
| c01 | SHRINK_5 | 0.6979 | 0.8713 | 0.710 | 0.0929 | 0.815 | 0.3180 |
| c01 | SHRINK_20 | 0.6885 | 0.8657 | 0.695 | 0.0985 | 0.446 | 0.4483 |
| c01 | LCB | 0.6727 | 0.8530 | 0.695 | 0.0947 | 0.832 | 0.5483 |
| c01 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |
| c02 | MEAN | 0.5740 | 0.7537 | 0.595 | 0.1584 | 0.892 | 0.4450 |
| c02 | SHRINK_1 | 0.5761 | 0.7578 | 0.605 | 0.1543 | 0.905 | 0.3945 |
| c02 | SHRINK_5 | 0.5844 | 0.7669 | 0.605 | 0.1517 | 0.898 | 0.3380 |
| c02 | SHRINK_20 | 0.5828 | 0.7662 | 0.620 | 0.1411 | 0.639 | 0.3973 |
| c02 | LCB | 0.5662 | 0.7495 | 0.620 | 0.1304 | 0.893 | 0.6347 |
| c02 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |
| c03 | MEAN | 0.8534 | 0.9658 | 0.770 | 0.0531 | 0.894 | 0.1717 |
| c03 | SHRINK_1 | 0.8525 | 0.9665 | 0.765 | 0.0524 | 0.896 | 0.1633 |
| c03 | SHRINK_5 | 0.8399 | 0.9628 | 0.725 | 0.0636 | 0.693 | 0.2306 |
| c03 | SHRINK_20 | 0.7988 | 0.9464 | 0.620 | 0.1116 | 0.294 | 0.4019 |
| c03 | LCB | 0.8088 | 0.9473 | 0.625 | 0.1028 | 0.793 | 0.3590 |
| c03 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |
| c04 | MEAN | 0.7375 | 0.9009 | 0.600 | 0.1279 | 0.899 | 0.2859 |
| c04 | SHRINK_1 | 0.7398 | 0.9035 | 0.625 | 0.1022 | 0.911 | 0.2617 |
| c04 | SHRINK_5 | 0.7370 | 0.9038 | 0.595 | 0.1066 | 0.846 | 0.2646 |
| c04 | SHRINK_20 | 0.7140 | 0.8926 | 0.530 | 0.1475 | 0.498 | 0.3805 |
| c04 | LCB | 0.7069 | 0.8821 | 0.545 | 0.1396 | 0.861 | 0.4689 |
| c04 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |
| c05 | MEAN | 0.6310 | 0.8153 | 0.470 | 0.1998 | 0.897 | 0.3710 |
| c05 | SHRINK_1 | 0.6334 | 0.8189 | 0.500 | 0.1835 | 0.910 | 0.3342 |
| c05 | SHRINK_5 | 0.6418 | 0.8270 | 0.515 | 0.1548 | 0.902 | 0.2881 |
| c05 | SHRINK_20 | 0.6330 | 0.8243 | 0.475 | 0.1629 | 0.684 | 0.3393 |
| c05 | LCB | 0.6130 | 0.8013 | 0.485 | 0.1630 | 0.893 | 0.5523 |
| c05 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |
| c06 | MEAN | 0.8830 | 0.9779 | 0.790 | 0.0369 | 0.899 | 0.1365 |
| c06 | SHRINK_1 | 0.8834 | 0.9784 | 0.830 | 0.0296 | 0.897 | 0.1312 |
| c06 | SHRINK_5 | 0.8700 | 0.9747 | 0.725 | 0.0574 | 0.739 | 0.1805 |
| c06 | SHRINK_20 | 0.8155 | 0.9540 | 0.560 | 0.1337 | 0.352 | 0.3273 |
| c06 | LCB | 0.8313 | 0.9570 | 0.630 | 0.1002 | 0.816 | 0.2908 |
| c06 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |
| c07 | MEAN | 0.7930 | 0.9352 | 0.630 | 0.1024 | 0.898 | 0.2317 |
| c07 | SHRINK_1 | 0.7960 | 0.9376 | 0.655 | 0.0840 | 0.905 | 0.2141 |
| c07 | SHRINK_5 | 0.7938 | 0.9383 | 0.655 | 0.0727 | 0.868 | 0.2134 |
| c07 | SHRINK_20 | 0.7624 | 0.9252 | 0.520 | 0.1296 | 0.565 | 0.3113 |
| c07 | LCB | 0.7549 | 0.9140 | 0.585 | 0.1001 | 0.877 | 0.3886 |
| c07 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |
| c08 | MEAN | 0.7072 | 0.8762 | 0.520 | 0.1509 | 0.894 | 0.2970 |
| c08 | SHRINK_1 | 0.7116 | 0.8807 | 0.535 | 0.1355 | 0.902 | 0.2719 |
| c08 | SHRINK_5 | 0.7191 | 0.8890 | 0.570 | 0.1044 | 0.908 | 0.2382 |
| c08 | SHRINK_20 | 0.7050 | 0.8842 | 0.490 | 0.1290 | 0.730 | 0.2815 |
| c08 | LCB | 0.6719 | 0.8522 | 0.505 | 0.1233 | 0.899 | 0.4669 |
| c08 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |

## Paired differences in Kendall tau-b against MEAN

Per cell: mean of per-seed paired differences, SD over seeds, 95% percentile bootstrap (10000 resamples, fixed seed) and t interval, and the standardised paired difference (mean/SD).

### SHRINK_1 minus MEAN

| Cell | Seeds | Mean | SD | Bootstrap 95% | t 95% | Half-width | Mean/SD |
|---|---|---|---|---|---|---|---|
| c00 | 20 | -0.0015 | 0.0049 | -0.0036 to 0.0005 | -0.0038 to 0.0008 | 0.0021 | -0.31 |
| c01 | 20 | -0.0001 | 0.0096 | -0.0039 to 0.0043 | -0.0046 to 0.0044 | 0.0041 | -0.01 |
| c02 | 20 | 0.0021 | 0.0054 | -0.0003 to 0.0044 | -0.0004 to 0.0046 | 0.0023 | 0.39 |
| c03 | 20 | -0.0009 | 0.0043 | -0.0026 to 0.0010 | -0.0029 to 0.0011 | 0.0018 | -0.21 |
| c04 | 20 | 0.0023 | 0.0040 | 0.0005 to 0.0040 | 0.0004 to 0.0042 | 0.0017 | 0.58 |
| c05 | 20 | 0.0024 | 0.0034 | 0.0009 to 0.0038 | 0.0008 to 0.0039 | 0.0014 | 0.70 |
| c06 | 20 | 0.0004 | 0.0024 | -0.0006 to 0.0015 | -0.0007 to 0.0015 | 0.0010 | 0.17 |
| c07 | 20 | 0.0030 | 0.0020 | 0.0022 to 0.0038 | 0.0021 to 0.0039 | 0.0008 | 1.52 |
| c08 | 20 | 0.0044 | 0.0026 | 0.0034 to 0.0056 | 0.0032 to 0.0057 | 0.0011 | 1.72 |

### SHRINK_5 minus MEAN

| Cell | Seeds | Mean | SD | Bootstrap 95% | t 95% | Half-width | Mean/SD |
|---|---|---|---|---|---|---|---|
| c00 | 20 | -0.0118 | 0.0101 | -0.0162 to -0.0075 | -0.0166 to -0.0071 | 0.0044 | -1.17 |
| c01 | 20 | 0.0006 | 0.0145 | -0.0054 to 0.0069 | -0.0061 to 0.0074 | 0.0062 | 0.04 |
| c02 | 20 | 0.0104 | 0.0148 | 0.0043 to 0.0170 | 0.0035 to 0.0173 | 0.0064 | 0.70 |
| c03 | 20 | -0.0136 | 0.0097 | -0.0175 to -0.0093 | -0.0181 to -0.0090 | 0.0041 | -1.40 |
| c04 | 20 | -0.0004 | 0.0115 | -0.0053 to 0.0044 | -0.0058 to 0.0049 | 0.0049 | -0.04 |
| c05 | 20 | 0.0108 | 0.0114 | 0.0064 to 0.0161 | 0.0055 to 0.0161 | 0.0048 | 0.95 |
| c06 | 20 | -0.0130 | 0.0061 | -0.0156 to -0.0103 | -0.0159 to -0.0102 | 0.0026 | -2.12 |
| c07 | 20 | 0.0008 | 0.0058 | -0.0017 to 0.0033 | -0.0019 to 0.0036 | 0.0025 | 0.14 |
| c08 | 20 | 0.0120 | 0.0069 | 0.0091 to 0.0150 | 0.0088 to 0.0152 | 0.0029 | 1.74 |

### SHRINK_20 minus MEAN

| Cell | Seeds | Mean | SD | Bootstrap 95% | t 95% | Half-width | Mean/SD |
|---|---|---|---|---|---|---|---|
| c00 | 20 | -0.0431 | 0.0153 | -0.0496 to -0.0364 | -0.0503 to -0.0360 | 0.0066 | -2.83 |
| c01 | 20 | -0.0088 | 0.0214 | -0.0181 to 0.0002 | -0.0188 to 0.0012 | 0.0092 | -0.41 |
| c02 | 20 | 0.0088 | 0.0248 | -0.0018 to 0.0193 | -0.0028 to 0.0204 | 0.0106 | 0.36 |
| c03 | 20 | -0.0547 | 0.0173 | -0.0619 to -0.0472 | -0.0628 to -0.0466 | 0.0073 | -3.16 |
| c04 | 20 | -0.0234 | 0.0191 | -0.0313 to -0.0151 | -0.0324 to -0.0145 | 0.0081 | -1.23 |
| c05 | 20 | 0.0020 | 0.0202 | -0.0064 to 0.0109 | -0.0075 to 0.0114 | 0.0087 | 0.10 |
| c06 | 20 | -0.0675 | 0.0105 | -0.0722 to -0.0630 | -0.0724 to -0.0626 | 0.0046 | -6.42 |
| c07 | 20 | -0.0306 | 0.0117 | -0.0357 to -0.0256 | -0.0361 to -0.0251 | 0.0050 | -2.61 |
| c08 | 20 | -0.0021 | 0.0125 | -0.0074 to 0.0030 | -0.0080 to 0.0037 | 0.0052 | -0.17 |

### LCB minus MEAN

| Cell | Seeds | Mean | SD | Bootstrap 95% | t 95% | Half-width | Mean/SD |
|---|---|---|---|---|---|---|---|
| c00 | 20 | -0.0380 | 0.0180 | -0.0454 to -0.0302 | -0.0464 to -0.0296 | 0.0076 | -2.11 |
| c01 | 20 | -0.0246 | 0.0200 | -0.0330 to -0.0163 | -0.0339 to -0.0152 | 0.0083 | -1.23 |
| c02 | 20 | -0.0078 | 0.0213 | -0.0170 to 0.0010 | -0.0178 to 0.0022 | 0.0090 | -0.37 |
| c03 | 20 | -0.0446 | 0.0111 | -0.0490 to -0.0396 | -0.0498 to -0.0394 | 0.0047 | -4.01 |
| c04 | 20 | -0.0306 | 0.0143 | -0.0363 to -0.0242 | -0.0373 to -0.0239 | 0.0060 | -2.14 |
| c05 | 20 | -0.0180 | 0.0157 | -0.0244 to -0.0110 | -0.0253 to -0.0106 | 0.0067 | -1.15 |
| c06 | 20 | -0.0517 | 0.0122 | -0.0567 to -0.0465 | -0.0574 to -0.0460 | 0.0051 | -4.25 |
| c07 | 20 | -0.0381 | 0.0126 | -0.0432 to -0.0326 | -0.0439 to -0.0322 | 0.0053 | -3.02 |
| c08 | 20 | -0.0352 | 0.0155 | -0.0417 to -0.0286 | -0.0425 to -0.0280 | 0.0066 | -2.28 |

Pooled over cells (equal weight, stratified bootstrap):

| Contrast | Cells | Pooled mean | 95% interval | One-sided 95% lower bound |
|---|---|---|---|---|
| SHRINK_1 minus MEAN | 9 | 0.0013 | 0.0007 to 0.0020 | 0.0008 |
| SHRINK_5 minus MEAN | 9 | -0.0005 | -0.0019 to 0.0011 | -0.0017 |
| SHRINK_20 minus MEAN | 9 | -0.0244 | -0.0269 to -0.0219 | -0.0265 |
| LCB minus MEAN | 9 | -0.0321 | -0.0344 to -0.0298 | -0.0340 |

Per noise level (protocol section 13.2, A-2): equal-weight mean over the cells at each sigma, two-sided 95% stratified bootstrap interval. Descriptive; not in the Holm family.

| Contrast | sigma (stars) | Cells | Mean | 95% interval |
|---|---|---|---|---|
| SHRINK_1 minus MEAN | 0.5 | 3 | -0.0007 | -0.0017 to 0.0003 |
| SHRINK_1 minus MEAN | 1.0 | 3 | 0.0017 | 0.0003 to 0.0033 |
| SHRINK_1 minus MEAN | 1.5 | 3 | 0.0030 | 0.0020 to 0.0039 |
| SHRINK_5 minus MEAN | 0.5 | 3 | -0.0128 | -0.0150 to -0.0106 |
| SHRINK_5 minus MEAN | 1.0 | 3 | 0.0003 | -0.0024 to 0.0031 |
| SHRINK_5 minus MEAN | 1.5 | 3 | 0.0111 | 0.0083 to 0.0140 |
| SHRINK_20 minus MEAN | 0.5 | 3 | -0.0551 | -0.0587 to -0.0515 |
| SHRINK_20 minus MEAN | 1.0 | 3 | -0.0209 | -0.0253 to -0.0165 |
| SHRINK_20 minus MEAN | 1.5 | 3 | 0.0029 | -0.0020 to 0.0079 |
| LCB minus MEAN | 0.5 | 3 | -0.0448 | -0.0482 to -0.0412 |
| LCB minus MEAN | 1.0 | 3 | -0.0311 | -0.0350 to -0.0272 |
| LCB minus MEAN | 1.5 | 3 | -0.0203 | -0.0247 to -0.0159 |

![EXP-003: tau-b(SHRINK_5) minus tau-b(MEAN) per cell. Simulated. Dot-and-interval chart. One row per cell; the dot is the mean paired difference in Kendall tau-b over seeds and the bar its 95% percentile bootstrap interval (10000 resamples). Seeds per cell: 20, 20, 20, 20, 20, 20, 20, 20, 20. The dashed line marks zero.](figures/fig_primary_contrast.svg){fig-alt="Simulated. Dot-and-interval chart. One row per cell; the dot is the mean paired difference in Kendall tau-b over seeds and the bar its 95% percentile bootstrap interval (10000 resamples). Seeds per cell: 20, 20, 20, 20, 20, 20, 20, 20, 20. The dashed line marks zero."}

## Checks, failures and degenerate cases

- Minimum ORACLE tau-b over runs: 1.000000000000 (must equal 1).
- Failed runs: 0.
- Degenerate-case flags: 0.
- Runtime per run: mean 8.71 ms, median 3.55 ms, max 82.32 ms; wall time 1.57 s; process peak RSS 97.4 MiB.
