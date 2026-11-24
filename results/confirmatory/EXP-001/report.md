<!-- SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0 -->

# EXP-001 run report (confirmatory)

**Simulated.** Results hold only under the model in `research/protocol.md`.

- Description: EXP-001 full matrix (research/experiments/EXP-001/protocol.md). Frozen v1.0 (owner-approved 2026-11-24, round 2): MovieLens-calibrated base (protocol 13.1), LCB prior centred on the catalogue mean (13.2 A-1).
- Config SHA-256: `94bbf40b7a37137c02dc6d1f88657ad1fa24c30b9220f267c10e912f1adbc255`
- Results SHA-256: `4985c4283311180ffd0736d29d4b72b9c9e9ae5f1350ee2c44cc29fe9b1b5fb7` (`results.json`, schema 1.0.0)
- Code revision: `bd9e1460e29389def8baa43d6ca7cc553d659ff1`
- Environment: Python 3.12.1, numpy 2.3.4, scipy 1.16.2; Apple M1 Pro; Darwin 24.3.0 (macOS-15.3.1-arm64-arm-64bit)
- Catalogue size N = 200; seeds per cell = 20; cells = 9; runs = 180; failed runs = 0
- Truth: `theta`; min reviews for evaluation: 0; top k = 10
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
| c00 | MEAN | 0.5185 | 0.6620 | 0.395 | 0.2385 | 0.905 | 0.5119 |
| c00 | SHRINK_1 | 0.5189 | 0.6671 | 0.385 | 0.2328 | 0.894 | 0.4837 |
| c00 | SHRINK_5 | 0.5076 | 0.6615 | 0.335 | 0.2870 | 0.567 | 0.5382 |
| c00 | SHRINK_20 | 0.4961 | 0.6549 | 0.280 | 0.3414 | 0.239 | 0.6089 |
| c00 | LCB | 0.4254 | 0.5585 | 0.270 | 0.3654 | 0.711 | 0.7366 |
| c00 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |
| c01 | MEAN | 0.4003 | 0.5360 | 0.245 | 0.4322 | 0.896 | 0.6387 |
| c01 | SHRINK_1 | 0.4063 | 0.5469 | 0.265 | 0.3670 | 0.920 | 0.5222 |
| c01 | SHRINK_5 | 0.4081 | 0.5509 | 0.265 | 0.3033 | 0.801 | 0.5148 |
| c01 | SHRINK_20 | 0.4033 | 0.5479 | 0.245 | 0.3321 | 0.442 | 0.5656 |
| c01 | LCB | 0.3517 | 0.4773 | 0.240 | 0.3423 | 0.824 | 0.8374 |
| c01 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |
| c02 | MEAN | 0.3061 | 0.4187 | 0.140 | 0.5500 | 0.893 | 0.7360 |
| c02 | SHRINK_1 | 0.3156 | 0.4331 | 0.200 | 0.4526 | 0.920 | 0.5450 |
| c02 | SHRINK_5 | 0.3243 | 0.4441 | 0.235 | 0.3582 | 0.902 | 0.4673 |
| c02 | SHRINK_20 | 0.3231 | 0.4441 | 0.210 | 0.3540 | 0.611 | 0.4896 |
| c02 | LCB | 0.2841 | 0.3918 | 0.210 | 0.3621 | 0.895 | 0.9060 |
| c02 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |
| c03 | MEAN | 0.6424 | 0.7964 | 0.545 | 0.1509 | 0.894 | 0.4151 |
| c03 | SHRINK_1 | 0.6401 | 0.7999 | 0.520 | 0.1358 | 0.887 | 0.3914 |
| c03 | SHRINK_5 | 0.6190 | 0.7897 | 0.445 | 0.1671 | 0.652 | 0.4466 |
| c03 | SHRINK_20 | 0.5907 | 0.7734 | 0.355 | 0.2180 | 0.279 | 0.5370 |
| c03 | LCB | 0.5480 | 0.7044 | 0.365 | 0.2093 | 0.761 | 0.6076 |
| c03 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |
| c04 | MEAN | 0.5294 | 0.6935 | 0.300 | 0.3762 | 0.901 | 0.5333 |
| c04 | SHRINK_1 | 0.5386 | 0.7062 | 0.430 | 0.2150 | 0.912 | 0.4371 |
| c04 | SHRINK_5 | 0.5363 | 0.7089 | 0.370 | 0.1922 | 0.831 | 0.4344 |
| c04 | SHRINK_20 | 0.5197 | 0.6985 | 0.300 | 0.2320 | 0.475 | 0.4998 |
| c04 | LCB | 0.4740 | 0.6334 | 0.325 | 0.2242 | 0.849 | 0.7021 |
| c04 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |
| c05 | MEAN | 0.4306 | 0.5853 | 0.135 | 0.5375 | 0.900 | 0.6334 |
| c05 | SHRINK_1 | 0.4438 | 0.6037 | 0.275 | 0.3546 | 0.917 | 0.4743 |
| c05 | SHRINK_5 | 0.4566 | 0.6209 | 0.325 | 0.2296 | 0.905 | 0.4059 |
| c05 | SHRINK_20 | 0.4511 | 0.6192 | 0.270 | 0.2374 | 0.662 | 0.4353 |
| c05 | LCB | 0.3948 | 0.5414 | 0.290 | 0.2376 | 0.894 | 0.7738 |
| c05 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |
| c06 | MEAN | 0.7392 | 0.8775 | 0.635 | 0.1088 | 0.900 | 0.3249 |
| c06 | SHRINK_1 | 0.7407 | 0.8821 | 0.650 | 0.0751 | 0.898 | 0.3032 |
| c06 | SHRINK_5 | 0.7140 | 0.8703 | 0.540 | 0.1115 | 0.709 | 0.3514 |
| c06 | SHRINK_20 | 0.6700 | 0.8481 | 0.410 | 0.1878 | 0.333 | 0.4444 |
| c06 | LCB | 0.6408 | 0.7931 | 0.460 | 0.1542 | 0.804 | 0.4989 |
| c06 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |
| c07 | MEAN | 0.6393 | 0.8041 | 0.420 | 0.2573 | 0.900 | 0.4309 |
| c07 | SHRINK_1 | 0.6522 | 0.8183 | 0.530 | 0.1388 | 0.911 | 0.3533 |
| c07 | SHRINK_5 | 0.6500 | 0.8221 | 0.485 | 0.1154 | 0.859 | 0.3496 |
| c07 | SHRINK_20 | 0.6220 | 0.8071 | 0.380 | 0.1723 | 0.545 | 0.4159 |
| c07 | LCB | 0.5690 | 0.7299 | 0.435 | 0.1427 | 0.872 | 0.5893 |
| c07 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |
| c08 | MEAN | 0.5534 | 0.7217 | 0.275 | 0.3467 | 0.899 | 0.5050 |
| c08 | SHRINK_1 | 0.5701 | 0.7425 | 0.370 | 0.2367 | 0.909 | 0.3870 |
| c08 | SHRINK_5 | 0.5843 | 0.7626 | 0.440 | 0.1418 | 0.909 | 0.3338 |
| c08 | SHRINK_20 | 0.5709 | 0.7569 | 0.365 | 0.1667 | 0.715 | 0.3651 |
| c08 | LCB | 0.4893 | 0.6483 | 0.370 | 0.1611 | 0.901 | 0.6609 |
| c08 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |

## Paired differences in Kendall tau-b against MEAN

Per cell: mean of per-seed paired differences, SD over seeds, 95% percentile bootstrap (10000 resamples, fixed seed) and t interval, and the standardised paired difference (mean/SD).

### SHRINK_1 minus MEAN

| Cell | Seeds | Mean | SD | Bootstrap 95% | t 95% | Half-width | Mean/SD |
|---|---|---|---|---|---|---|---|
| c00 | 20 | 0.0004 | 0.0045 | -0.0016 to 0.0022 | -0.0018 to 0.0025 | 0.0019 | 0.08 |
| c01 | 20 | 0.0060 | 0.0055 | 0.0036 to 0.0083 | 0.0035 to 0.0086 | 0.0023 | 1.10 |
| c02 | 20 | 0.0095 | 0.0050 | 0.0075 to 0.0117 | 0.0072 to 0.0118 | 0.0021 | 1.92 |
| c03 | 20 | -0.0022 | 0.0068 | -0.0052 to 0.0006 | -0.0054 to 0.0010 | 0.0029 | -0.33 |
| c04 | 20 | 0.0092 | 0.0037 | 0.0076 to 0.0108 | 0.0075 to 0.0109 | 0.0016 | 2.48 |
| c05 | 20 | 0.0132 | 0.0051 | 0.0110 to 0.0153 | 0.0108 to 0.0155 | 0.0022 | 2.59 |
| c06 | 20 | 0.0014 | 0.0069 | -0.0017 to 0.0041 | -0.0018 to 0.0047 | 0.0029 | 0.21 |
| c07 | 20 | 0.0129 | 0.0077 | 0.0096 to 0.0161 | 0.0093 to 0.0165 | 0.0033 | 1.67 |
| c08 | 20 | 0.0167 | 0.0047 | 0.0147 to 0.0187 | 0.0145 to 0.0189 | 0.0020 | 3.58 |

### SHRINK_5 minus MEAN

| Cell | Seeds | Mean | SD | Bootstrap 95% | t 95% | Half-width | Mean/SD |
|---|---|---|---|---|---|---|---|
| c00 | 20 | -0.0109 | 0.0088 | -0.0148 to -0.0074 | -0.0150 to -0.0068 | 0.0037 | -1.25 |
| c01 | 20 | 0.0078 | 0.0105 | 0.0033 to 0.0123 | 0.0029 to 0.0128 | 0.0045 | 0.74 |
| c02 | 20 | 0.0183 | 0.0105 | 0.0138 to 0.0229 | 0.0133 to 0.0232 | 0.0046 | 1.74 |
| c03 | 20 | -0.0234 | 0.0119 | -0.0284 to -0.0183 | -0.0289 to -0.0178 | 0.0050 | -1.97 |
| c04 | 20 | 0.0069 | 0.0089 | 0.0031 to 0.0107 | 0.0027 to 0.0111 | 0.0038 | 0.77 |
| c05 | 20 | 0.0260 | 0.0115 | 0.0210 to 0.0308 | 0.0206 to 0.0314 | 0.0049 | 2.25 |
| c06 | 20 | -0.0253 | 0.0110 | -0.0300 to -0.0206 | -0.0304 to -0.0201 | 0.0047 | -2.29 |
| c07 | 20 | 0.0107 | 0.0146 | 0.0044 to 0.0168 | 0.0038 to 0.0175 | 0.0062 | 0.73 |
| c08 | 20 | 0.0309 | 0.0104 | 0.0264 to 0.0353 | 0.0260 to 0.0358 | 0.0044 | 2.97 |

### SHRINK_20 minus MEAN

| Cell | Seeds | Mean | SD | Bootstrap 95% | t 95% | Half-width | Mean/SD |
|---|---|---|---|---|---|---|---|
| c00 | 20 | -0.0224 | 0.0108 | -0.0272 to -0.0181 | -0.0275 to -0.0174 | 0.0046 | -2.09 |
| c01 | 20 | 0.0030 | 0.0129 | -0.0025 to 0.0084 | -0.0030 to 0.0091 | 0.0055 | 0.24 |
| c02 | 20 | 0.0170 | 0.0130 | 0.0113 to 0.0227 | 0.0109 to 0.0231 | 0.0057 | 1.31 |
| c03 | 20 | -0.0517 | 0.0130 | -0.0572 to -0.0461 | -0.0577 to -0.0456 | 0.0056 | -3.99 |
| c04 | 20 | -0.0097 | 0.0128 | -0.0151 to -0.0042 | -0.0157 to -0.0037 | 0.0054 | -0.76 |
| c05 | 20 | 0.0205 | 0.0161 | 0.0137 to 0.0275 | 0.0130 to 0.0280 | 0.0069 | 1.27 |
| c06 | 20 | -0.0693 | 0.0125 | -0.0746 to -0.0639 | -0.0751 to -0.0634 | 0.0053 | -5.55 |
| c07 | 20 | -0.0173 | 0.0163 | -0.0243 to -0.0104 | -0.0249 to -0.0097 | 0.0069 | -1.06 |
| c08 | 20 | 0.0175 | 0.0130 | 0.0119 to 0.0230 | 0.0114 to 0.0236 | 0.0055 | 1.34 |

### LCB minus MEAN

| Cell | Seeds | Mean | SD | Bootstrap 95% | t 95% | Half-width | Mean/SD |
|---|---|---|---|---|---|---|---|
| c00 | 20 | -0.0931 | 0.0257 | -0.1039 to -0.0816 | -0.1051 to -0.0810 | 0.0111 | -3.62 |
| c01 | 20 | -0.0486 | 0.0247 | -0.0587 to -0.0373 | -0.0601 to -0.0370 | 0.0107 | -1.97 |
| c02 | 20 | -0.0220 | 0.0286 | -0.0340 to -0.0097 | -0.0354 to -0.0086 | 0.0121 | -0.77 |
| c03 | 20 | -0.0943 | 0.0292 | -0.1065 to -0.0815 | -0.1080 to -0.0807 | 0.0125 | -3.24 |
| c04 | 20 | -0.0554 | 0.0317 | -0.0687 to -0.0416 | -0.0702 to -0.0405 | 0.0136 | -1.75 |
| c05 | 20 | -0.0358 | 0.0335 | -0.0503 to -0.0217 | -0.0515 to -0.0202 | 0.0143 | -1.07 |
| c06 | 20 | -0.0984 | 0.0315 | -0.1121 to -0.0854 | -0.1132 to -0.0837 | 0.0134 | -3.13 |
| c07 | 20 | -0.0704 | 0.0277 | -0.0824 to -0.0588 | -0.0833 to -0.0574 | 0.0118 | -2.54 |
| c08 | 20 | -0.0641 | 0.0326 | -0.0779 to -0.0499 | -0.0794 to -0.0489 | 0.0140 | -1.97 |

Pooled over cells (equal weight, stratified bootstrap):

| Contrast | Cells | Pooled mean | 95% interval | One-sided 95% lower bound |
|---|---|---|---|---|
| SHRINK_1 minus MEAN | 9 | 0.0075 | 0.0066 to 0.0082 | 0.0068 |
| SHRINK_5 minus MEAN | 9 | 0.0046 | 0.0030 to 0.0061 | 0.0032 |
| SHRINK_20 minus MEAN | 9 | -0.0125 | -0.0143 to -0.0106 | -0.0141 |
| LCB minus MEAN | 9 | -0.0647 | -0.0689 to -0.0604 | -0.0682 |

Per noise level (protocol section 13.2, A-2): equal-weight mean over the cells at each sigma, two-sided 95% stratified bootstrap interval. Descriptive; not in the Holm family.

| Contrast | sigma (stars) | Cells | Mean | 95% interval |
|---|---|---|---|---|
| SHRINK_1 minus MEAN | 0.5 | 3 | -0.0001 | -0.0017 to 0.0014 |
| SHRINK_1 minus MEAN | 1.0 | 3 | 0.0094 | 0.0079 to 0.0108 |
| SHRINK_1 minus MEAN | 1.5 | 3 | 0.0131 | 0.0119 to 0.0143 |
| SHRINK_5 minus MEAN | 0.5 | 3 | -0.0198 | -0.0225 to -0.0172 |
| SHRINK_5 minus MEAN | 1.0 | 3 | 0.0085 | 0.0056 to 0.0113 |
| SHRINK_5 minus MEAN | 1.5 | 3 | 0.0250 | 0.0224 to 0.0277 |
| SHRINK_20 minus MEAN | 0.5 | 3 | -0.0478 | -0.0508 to -0.0447 |
| SHRINK_20 minus MEAN | 1.0 | 3 | -0.0080 | -0.0114 to -0.0045 |
| SHRINK_20 minus MEAN | 1.5 | 3 | 0.0183 | 0.0149 to 0.0219 |
| LCB minus MEAN | 0.5 | 3 | -0.0953 | -0.1023 to -0.0880 |
| LCB minus MEAN | 1.0 | 3 | -0.0581 | -0.0651 to -0.0511 |
| LCB minus MEAN | 1.5 | 3 | -0.0406 | -0.0484 to -0.0328 |

![EXP-001: tau-b(SHRINK_5) minus tau-b(MEAN) per cell. Simulated. Dot-and-interval chart. One row per cell; the dot is the mean paired difference in Kendall tau-b over seeds and the bar its 95% percentile bootstrap interval (10000 resamples). Seeds per cell: 20, 20, 20, 20, 20, 20, 20, 20, 20. The dashed line marks zero.](figures/fig_primary_contrast.svg){fig-alt="Simulated. Dot-and-interval chart. One row per cell; the dot is the mean paired difference in Kendall tau-b over seeds and the bar its 95% percentile bootstrap interval (10000 resamples). Seeds per cell: 20, 20, 20, 20, 20, 20, 20, 20, 20. The dashed line marks zero."}

## Checks, failures and degenerate cases

- Minimum ORACLE tau-b over runs: 1.000000000000 (must equal 1).
- Failed runs: 0.
- Degenerate-case flags: 0.
- Runtime per run: mean 12.29 ms, median 3.95 ms, max 101.97 ms; wall time 2.22 s; process peak RSS 96.9 MiB.
