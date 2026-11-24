<!-- SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0 -->

# EXP-003 run report (confirmatory)

**Simulated.** Results hold only under the model in `research/protocol.md`.

- Description: EXP-003 S2: SHRINK(5) towards m + 0.5 and m - 0.5 on EXP-001 catalogues. Frozen v1.0 (owner-approved 2026-11-24, round 2): MovieLens-calibrated base (protocol 13.1), LCB prior centred on the catalogue mean (13.2 A-1).
- Config SHA-256: `0da06dd7922298095cb91997b2df17e4989176a290966973d58d6d1ffe2c4a42`
- Results SHA-256: `749eefd581ccb1469ad52b23f33f4d04df7b6e5d8f5e3917c9e7f1cf744b768b` (`results.json`, schema 1.0.0)
- Code revision: `bd9e1460e29389def8baa43d6ca7cc553d659ff1`
- Environment: Python 3.12.1, numpy 2.3.4, scipy 1.16.2; Apple M1 Pro; Darwin 24.3.0 (macOS-15.3.1-arm64-arm-64bit)
- Catalogue size N = 200; seeds per cell = 20; cells = 9; runs = 180; failed runs = 0
- Truth: `theta`; min reviews for evaluation: 0; top k = 10
- Machine-readable outputs: `results.json`, `run_manifest.json`, `metrics.csv` (900 rows), `summary.json`, `evidence_manifest.json`

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
| c00 | SHRINK_5 | 0.5076 | 0.6615 | 0.335 | 0.2870 | 0.567 | 0.5382 |
| c00 | SHRINK_5_UP | 0.4613 | 0.6015 | 0.380 | 0.2342 | 0.511 | 0.6626 |
| c00 | SHRINK_5_DOWN | 0.4212 | 0.5496 | 0.280 | 0.3428 | 0.456 | 0.6695 |
| c00 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |
| c01 | MEAN | 0.4003 | 0.5360 | 0.245 | 0.4322 | 0.896 | 0.6387 |
| c01 | SHRINK_5 | 0.4081 | 0.5509 | 0.265 | 0.3033 | 0.801 | 0.5148 |
| c01 | SHRINK_5_UP | 0.3746 | 0.5053 | 0.285 | 0.3282 | 0.722 | 0.6458 |
| c01 | SHRINK_5_DOWN | 0.3579 | 0.4829 | 0.250 | 0.3254 | 0.699 | 0.6480 |
| c01 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |
| c02 | MEAN | 0.3061 | 0.4187 | 0.140 | 0.5500 | 0.893 | 0.7360 |
| c02 | SHRINK_5 | 0.3243 | 0.4441 | 0.235 | 0.3582 | 0.902 | 0.4673 |
| c02 | SHRINK_5_UP | 0.2946 | 0.4038 | 0.205 | 0.4128 | 0.824 | 0.6118 |
| c02 | SHRINK_5_DOWN | 0.2942 | 0.4045 | 0.210 | 0.3533 | 0.836 | 0.6075 |
| c02 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |
| c03 | MEAN | 0.6424 | 0.7964 | 0.545 | 0.1509 | 0.894 | 0.4151 |
| c03 | SHRINK_5 | 0.6190 | 0.7897 | 0.445 | 0.1671 | 0.652 | 0.4466 |
| c03 | SHRINK_5_UP | 0.5573 | 0.7141 | 0.495 | 0.1372 | 0.584 | 0.5589 |
| c03 | SHRINK_5_DOWN | 0.5550 | 0.7081 | 0.395 | 0.1940 | 0.559 | 0.5392 |
| c03 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |
| c04 | MEAN | 0.5294 | 0.6935 | 0.300 | 0.3762 | 0.901 | 0.5333 |
| c04 | SHRINK_5 | 0.5363 | 0.7089 | 0.370 | 0.1922 | 0.831 | 0.4344 |
| c04 | SHRINK_5_UP | 0.4869 | 0.6444 | 0.410 | 0.1910 | 0.771 | 0.5481 |
| c04 | SHRINK_5_DOWN | 0.4894 | 0.6485 | 0.340 | 0.1998 | 0.746 | 0.5302 |
| c04 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |
| c05 | MEAN | 0.4306 | 0.5853 | 0.135 | 0.5375 | 0.900 | 0.6334 |
| c05 | SHRINK_5 | 0.4566 | 0.6209 | 0.325 | 0.2296 | 0.905 | 0.4059 |
| c05 | SHRINK_5_UP | 0.4098 | 0.5581 | 0.320 | 0.2707 | 0.841 | 0.5284 |
| c05 | SHRINK_5_DOWN | 0.4182 | 0.5685 | 0.290 | 0.2233 | 0.863 | 0.5044 |
| c05 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |
| c06 | MEAN | 0.7392 | 0.8775 | 0.635 | 0.1088 | 0.900 | 0.3249 |
| c06 | SHRINK_5 | 0.7140 | 0.8703 | 0.540 | 0.1115 | 0.709 | 0.3514 |
| c06 | SHRINK_5_UP | 0.6702 | 0.8171 | 0.590 | 0.0860 | 0.667 | 0.4328 |
| c06 | SHRINK_5_DOWN | 0.6536 | 0.8012 | 0.490 | 0.1411 | 0.627 | 0.4339 |
| c06 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |
| c07 | MEAN | 0.6393 | 0.8041 | 0.420 | 0.2573 | 0.900 | 0.4309 |
| c07 | SHRINK_5 | 0.6500 | 0.8221 | 0.485 | 0.1154 | 0.859 | 0.3496 |
| c07 | SHRINK_5_UP | 0.6064 | 0.7678 | 0.505 | 0.1141 | 0.818 | 0.4308 |
| c07 | SHRINK_5_DOWN | 0.5977 | 0.7577 | 0.455 | 0.1307 | 0.793 | 0.4332 |
| c07 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |
| c08 | MEAN | 0.5534 | 0.7217 | 0.275 | 0.3467 | 0.899 | 0.5050 |
| c08 | SHRINK_5 | 0.5843 | 0.7626 | 0.440 | 0.1418 | 0.909 | 0.3338 |
| c08 | SHRINK_5_UP | 0.5325 | 0.6961 | 0.425 | 0.1859 | 0.874 | 0.4176 |
| c08 | SHRINK_5_DOWN | 0.5358 | 0.6993 | 0.420 | 0.1375 | 0.869 | 0.4214 |
| c08 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |

## Paired differences in Kendall tau-b against MEAN

Per cell: mean of per-seed paired differences, SD over seeds, 95% percentile bootstrap (10000 resamples, fixed seed) and t interval, and the standardised paired difference (mean/SD).

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

### SHRINK_5_UP minus MEAN

| Cell | Seeds | Mean | SD | Bootstrap 95% | t 95% | Half-width | Mean/SD |
|---|---|---|---|---|---|---|---|
| c00 | 20 | -0.0572 | 0.0238 | -0.0671 to -0.0468 | -0.0684 to -0.0461 | 0.0102 | -2.40 |
| c01 | 20 | -0.0257 | 0.0232 | -0.0352 to -0.0155 | -0.0366 to -0.0149 | 0.0099 | -1.11 |
| c02 | 20 | -0.0114 | 0.0195 | -0.0199 to -0.0033 | -0.0205 to -0.0023 | 0.0083 | -0.58 |
| c03 | 20 | -0.0851 | 0.0309 | -0.0984 to -0.0721 | -0.0996 to -0.0706 | 0.0132 | -2.75 |
| c04 | 20 | -0.0426 | 0.0281 | -0.0543 to -0.0306 | -0.0557 to -0.0294 | 0.0118 | -1.51 |
| c05 | 20 | -0.0208 | 0.0300 | -0.0340 to -0.0084 | -0.0349 to -0.0068 | 0.0128 | -0.69 |
| c06 | 20 | -0.0690 | 0.0381 | -0.0844 to -0.0519 | -0.0869 to -0.0512 | 0.0162 | -1.81 |
| c07 | 20 | -0.0329 | 0.0402 | -0.0502 to -0.0158 | -0.0518 to -0.0141 | 0.0172 | -0.82 |
| c08 | 20 | -0.0209 | 0.0397 | -0.0371 to -0.0036 | -0.0394 to -0.0023 | 0.0168 | -0.53 |

### SHRINK_5_DOWN minus MEAN

| Cell | Seeds | Mean | SD | Bootstrap 95% | t 95% | Half-width | Mean/SD |
|---|---|---|---|---|---|---|---|
| c00 | 20 | -0.0973 | 0.0280 | -0.1091 to -0.0848 | -0.1104 to -0.0842 | 0.0121 | -3.48 |
| c01 | 20 | -0.0424 | 0.0252 | -0.0526 to -0.0309 | -0.0542 to -0.0306 | 0.0108 | -1.68 |
| c02 | 20 | -0.0118 | 0.0276 | -0.0233 to 0.0001 | -0.0247 to 0.0011 | 0.0117 | -0.43 |
| c03 | 20 | -0.0874 | 0.0277 | -0.0988 to -0.0751 | -0.1003 to -0.0744 | 0.0119 | -3.15 |
| c04 | 20 | -0.0400 | 0.0304 | -0.0528 to -0.0270 | -0.0542 to -0.0258 | 0.0129 | -1.32 |
| c05 | 20 | -0.0125 | 0.0305 | -0.0257 to 0.0004 | -0.0267 to 0.0018 | 0.0131 | -0.41 |
| c06 | 20 | -0.0857 | 0.0310 | -0.0991 to -0.0725 | -0.1002 to -0.0711 | 0.0133 | -2.76 |
| c07 | 20 | -0.0416 | 0.0260 | -0.0527 to -0.0307 | -0.0538 to -0.0295 | 0.0110 | -1.60 |
| c08 | 20 | -0.0176 | 0.0283 | -0.0294 to -0.0050 | -0.0308 to -0.0043 | 0.0122 | -0.62 |

Pooled over cells (equal weight, stratified bootstrap):

| Contrast | Cells | Pooled mean | 95% interval | One-sided 95% lower bound |
|---|---|---|---|---|
| SHRINK_5 minus MEAN | 9 | 0.0046 | 0.0030 to 0.0061 | 0.0032 |
| SHRINK_5_UP minus MEAN | 9 | -0.0406 | -0.0449 to -0.0361 | -0.0443 |
| SHRINK_5_DOWN minus MEAN | 9 | -0.0485 | -0.0525 to -0.0444 | -0.0519 |

Per noise level (protocol section 13.2, A-2): equal-weight mean over the cells at each sigma, two-sided 95% stratified bootstrap interval. Descriptive; not in the Holm family.

| Contrast | sigma (stars) | Cells | Mean | 95% interval |
|---|---|---|---|---|
| SHRINK_5 minus MEAN | 0.5 | 3 | -0.0198 | -0.0225 to -0.0172 |
| SHRINK_5 minus MEAN | 1.0 | 3 | 0.0085 | 0.0056 to 0.0113 |
| SHRINK_5 minus MEAN | 1.5 | 3 | 0.0250 | 0.0224 to 0.0277 |
| SHRINK_5_UP minus MEAN | 0.5 | 3 | -0.0705 | -0.0781 to -0.0625 |
| SHRINK_5_UP minus MEAN | 1.0 | 3 | -0.0337 | -0.0416 to -0.0260 |
| SHRINK_5_UP minus MEAN | 1.5 | 3 | -0.0177 | -0.0252 to -0.0100 |
| SHRINK_5_DOWN minus MEAN | 0.5 | 3 | -0.0901 | -0.0971 to -0.0829 |
| SHRINK_5_DOWN minus MEAN | 1.0 | 3 | -0.0414 | -0.0480 to -0.0347 |
| SHRINK_5_DOWN minus MEAN | 1.5 | 3 | -0.0140 | -0.0210 to -0.0068 |

![EXP-003: tau-b(SHRINK_5) minus tau-b(MEAN) per cell. Simulated. Dot-and-interval chart. One row per cell; the dot is the mean paired difference in Kendall tau-b over seeds and the bar its 95% percentile bootstrap interval (10000 resamples). Seeds per cell: 20, 20, 20, 20, 20, 20, 20, 20, 20. The dashed line marks zero.](figures/fig_primary_contrast.svg){fig-alt="Simulated. Dot-and-interval chart. One row per cell; the dot is the mean paired difference in Kendall tau-b over seeds and the bar its 95% percentile bootstrap interval (10000 resamples). Seeds per cell: 20, 20, 20, 20, 20, 20, 20, 20, 20. The dashed line marks zero."}

## Checks, failures and degenerate cases

- Minimum ORACLE tau-b over runs: 1.000000000000 (must equal 1).
- Failed runs: 0.
- Degenerate-case flags: 0.
- Runtime per run: mean 8.44 ms, median 3.18 ms, max 83.92 ms; wall time 1.52 s; process peak RSS 96.6 MiB.
