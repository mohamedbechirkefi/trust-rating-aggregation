<!-- SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0 -->

# EXP-003 run report (confirmatory)

**Simulated.** Results hold only under the model in `research/protocol.md`.

- Description: EXP-003 S1: EXP-001 catalogues, metrics on products with n >= 1. Frozen v1.0 (owner-approved 2026-11-24, round 2): MovieLens-calibrated base (protocol 13.1), LCB prior centred on the catalogue mean (13.2 A-1).
- Config SHA-256: `1db94739be92b71b8ae7bbfc94473cf68290153ef4a2b1281d8173ff251958a6`
- Results SHA-256: `4b7cc8bf5f7037e110ee757190b6a8dc7ca98297040cc810e87018f2ca7a5241` (`results.json`, schema 1.0.0)
- Code revision: `bd9e1460e29389def8baa43d6ca7cc553d659ff1`
- Environment: Python 3.12.1, numpy 2.3.4, scipy 1.16.2; Apple M1 Pro; Darwin 24.3.0 (macOS-15.3.1-arm64-arm-64bit)
- Catalogue size N = 200; seeds per cell = 20; cells = 9; runs = 180; failed runs = 0
- Truth: `theta`; min reviews for evaluation: 1; top k = 10
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
| c00 | MEAN | 0.7178 | 0.8711 | 0.535 | 0.1610 | 0.905 | 0.3773 |
| c00 | SHRINK_1 | 0.7141 | 0.8816 | 0.525 | 0.1553 | 0.894 | 0.3120 |
| c00 | SHRINK_5 | 0.6865 | 0.8675 | 0.455 | 0.2096 | 0.567 | 0.4326 |
| c00 | SHRINK_20 | 0.6584 | 0.8505 | 0.380 | 0.2640 | 0.239 | 0.5637 |
| c00 | LCB | 0.6323 | 0.8179 | 0.365 | 0.2879 | 0.711 | 0.6079 |
| c00 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |
| c01 | MEAN | 0.5316 | 0.7031 | 0.310 | 0.3709 | 0.896 | 0.6468 |
| c01 | SHRINK_1 | 0.5441 | 0.7296 | 0.355 | 0.3057 | 0.920 | 0.4471 |
| c01 | SHRINK_5 | 0.5483 | 0.7395 | 0.375 | 0.2420 | 0.801 | 0.4335 |
| c01 | SHRINK_20 | 0.5366 | 0.7319 | 0.355 | 0.2709 | 0.442 | 0.5256 |
| c01 | LCB | 0.5082 | 0.6955 | 0.345 | 0.2810 | 0.824 | 0.7190 |
| c01 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |
| c02 | MEAN | 0.3971 | 0.5474 | 0.180 | 0.4959 | 0.893 | 0.8356 |
| c02 | SHRINK_1 | 0.4188 | 0.5832 | 0.265 | 0.3985 | 0.920 | 0.5500 |
| c02 | SHRINK_5 | 0.4397 | 0.6108 | 0.300 | 0.3041 | 0.902 | 0.4192 |
| c02 | SHRINK_20 | 0.4366 | 0.6105 | 0.300 | 0.2999 | 0.611 | 0.4583 |
| c02 | LCB | 0.4072 | 0.5721 | 0.305 | 0.3080 | 0.895 | 0.7999 |
| c02 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |
| c03 | MEAN | 0.7732 | 0.9134 | 0.665 | 0.1109 | 0.894 | 0.3025 |
| c03 | SHRINK_1 | 0.7680 | 0.9189 | 0.650 | 0.0957 | 0.887 | 0.2602 |
| c03 | SHRINK_5 | 0.7340 | 0.9025 | 0.540 | 0.1270 | 0.652 | 0.3562 |
| c03 | SHRINK_20 | 0.6885 | 0.8762 | 0.440 | 0.1780 | 0.279 | 0.4907 |
| c03 | LCB | 0.6713 | 0.8438 | 0.450 | 0.1692 | 0.761 | 0.5066 |
| c03 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |
| c04 | MEAN | 0.6241 | 0.7951 | 0.385 | 0.3447 | 0.901 | 0.5031 |
| c04 | SHRINK_1 | 0.6381 | 0.8158 | 0.525 | 0.1835 | 0.912 | 0.3663 |
| c04 | SHRINK_5 | 0.6342 | 0.8204 | 0.460 | 0.1607 | 0.831 | 0.3633 |
| c04 | SHRINK_20 | 0.6074 | 0.8035 | 0.375 | 0.2005 | 0.475 | 0.4588 |
| c04 | LCB | 0.5756 | 0.7610 | 0.395 | 0.1927 | 0.849 | 0.6084 |
| c04 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |
| c05 | MEAN | 0.4951 | 0.6631 | 0.180 | 0.5095 | 0.900 | 0.6575 |
| c05 | SHRINK_1 | 0.5160 | 0.6932 | 0.360 | 0.3267 | 0.917 | 0.4543 |
| c05 | SHRINK_5 | 0.5365 | 0.7215 | 0.405 | 0.2017 | 0.905 | 0.3605 |
| c05 | SHRINK_20 | 0.5274 | 0.7184 | 0.340 | 0.2095 | 0.662 | 0.4025 |
| c05 | LCB | 0.4839 | 0.6631 | 0.355 | 0.2096 | 0.894 | 0.6867 |
| c05 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |
| c06 | MEAN | 0.8272 | 0.9457 | 0.675 | 0.0935 | 0.900 | 0.2376 |
| c06 | SHRINK_1 | 0.8286 | 0.9516 | 0.705 | 0.0597 | 0.898 | 0.2034 |
| c06 | SHRINK_5 | 0.7935 | 0.9360 | 0.600 | 0.0962 | 0.709 | 0.2784 |
| c06 | SHRINK_20 | 0.7355 | 0.9065 | 0.460 | 0.1724 | 0.333 | 0.4032 |
| c06 | LCB | 0.7268 | 0.8809 | 0.515 | 0.1389 | 0.804 | 0.4165 |
| c06 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |
| c07 | MEAN | 0.7049 | 0.8627 | 0.440 | 0.2452 | 0.900 | 0.3972 |
| c07 | SHRINK_1 | 0.7216 | 0.8815 | 0.580 | 0.1267 | 0.911 | 0.2971 |
| c07 | SHRINK_5 | 0.7186 | 0.8865 | 0.530 | 0.1033 | 0.859 | 0.2922 |
| c07 | SHRINK_20 | 0.6818 | 0.8665 | 0.425 | 0.1601 | 0.545 | 0.3790 |
| c07 | LCB | 0.6477 | 0.8196 | 0.480 | 0.1306 | 0.872 | 0.5107 |
| c07 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |
| c08 | MEAN | 0.6039 | 0.7715 | 0.285 | 0.3360 | 0.899 | 0.5027 |
| c08 | SHRINK_1 | 0.6257 | 0.7991 | 0.395 | 0.2260 | 0.909 | 0.3627 |
| c08 | SHRINK_5 | 0.6443 | 0.8255 | 0.480 | 0.1311 | 0.909 | 0.2957 |
| c08 | SHRINK_20 | 0.6266 | 0.8179 | 0.405 | 0.1560 | 0.715 | 0.3356 |
| c08 | LCB | 0.5634 | 0.7413 | 0.410 | 0.1504 | 0.901 | 0.5860 |
| c08 | ORACLE | 1.0000 | 1.0000 | 1.000 | 0.0000 | n/a | 0.0000 |

## Paired differences in Kendall tau-b against MEAN

Per cell: mean of per-seed paired differences, SD over seeds, 95% percentile bootstrap (10000 resamples, fixed seed) and t interval, and the standardised paired difference (mean/SD).

### SHRINK_1 minus MEAN

| Cell | Seeds | Mean | SD | Bootstrap 95% | t 95% | Half-width | Mean/SD |
|---|---|---|---|---|---|---|---|
| c00 | 20 | -0.0037 | 0.0107 | -0.0083 to 0.0007 | -0.0087 to 0.0013 | 0.0045 | -0.34 |
| c01 | 20 | 0.0126 | 0.0130 | 0.0068 to 0.0180 | 0.0065 to 0.0187 | 0.0056 | 0.96 |
| c02 | 20 | 0.0217 | 0.0111 | 0.0170 to 0.0265 | 0.0165 to 0.0269 | 0.0048 | 1.96 |
| c03 | 20 | -0.0052 | 0.0110 | -0.0099 to -0.0006 | -0.0103 to -0.0001 | 0.0046 | -0.47 |
| c04 | 20 | 0.0140 | 0.0058 | 0.0114 to 0.0164 | 0.0112 to 0.0167 | 0.0025 | 2.39 |
| c05 | 20 | 0.0208 | 0.0081 | 0.0173 to 0.0242 | 0.0170 to 0.0246 | 0.0035 | 2.58 |
| c06 | 20 | 0.0014 | 0.0093 | -0.0028 to 0.0049 | -0.0030 to 0.0057 | 0.0039 | 0.15 |
| c07 | 20 | 0.0167 | 0.0102 | 0.0123 to 0.0209 | 0.0119 to 0.0215 | 0.0043 | 1.63 |
| c08 | 20 | 0.0218 | 0.0062 | 0.0192 to 0.0244 | 0.0189 to 0.0247 | 0.0026 | 3.55 |

### SHRINK_5 minus MEAN

| Cell | Seeds | Mean | SD | Bootstrap 95% | t 95% | Half-width | Mean/SD |
|---|---|---|---|---|---|---|---|
| c00 | 20 | -0.0313 | 0.0205 | -0.0403 to -0.0229 | -0.0409 to -0.0217 | 0.0087 | -1.52 |
| c01 | 20 | 0.0167 | 0.0248 | 0.0060 to 0.0270 | 0.0051 to 0.0283 | 0.0105 | 0.68 |
| c02 | 20 | 0.0426 | 0.0232 | 0.0325 to 0.0526 | 0.0317 to 0.0535 | 0.0101 | 1.83 |
| c03 | 20 | -0.0392 | 0.0194 | -0.0474 to -0.0310 | -0.0482 to -0.0301 | 0.0082 | -2.02 |
| c04 | 20 | 0.0101 | 0.0139 | 0.0041 to 0.0160 | 0.0036 to 0.0166 | 0.0059 | 0.73 |
| c05 | 20 | 0.0414 | 0.0178 | 0.0335 to 0.0488 | 0.0330 to 0.0497 | 0.0077 | 2.32 |
| c06 | 20 | -0.0338 | 0.0150 | -0.0403 to -0.0274 | -0.0408 to -0.0268 | 0.0064 | -2.25 |
| c07 | 20 | 0.0137 | 0.0193 | 0.0053 to 0.0218 | 0.0046 to 0.0228 | 0.0082 | 0.71 |
| c08 | 20 | 0.0405 | 0.0135 | 0.0347 to 0.0462 | 0.0341 to 0.0468 | 0.0058 | 3.00 |

### SHRINK_20 minus MEAN

| Cell | Seeds | Mean | SD | Bootstrap 95% | t 95% | Half-width | Mean/SD |
|---|---|---|---|---|---|---|---|
| c00 | 20 | -0.0594 | 0.0253 | -0.0704 to -0.0489 | -0.0712 to -0.0476 | 0.0108 | -2.35 |
| c01 | 20 | 0.0050 | 0.0305 | -0.0083 to 0.0178 | -0.0092 to 0.0193 | 0.0130 | 0.17 |
| c02 | 20 | 0.0395 | 0.0297 | 0.0264 to 0.0521 | 0.0257 to 0.0534 | 0.0129 | 1.33 |
| c03 | 20 | -0.0847 | 0.0208 | -0.0937 to -0.0759 | -0.0944 to -0.0750 | 0.0089 | -4.08 |
| c04 | 20 | -0.0167 | 0.0207 | -0.0254 to -0.0079 | -0.0264 to -0.0071 | 0.0087 | -0.81 |
| c05 | 20 | 0.0323 | 0.0252 | 0.0216 to 0.0431 | 0.0205 to 0.0441 | 0.0108 | 1.28 |
| c06 | 20 | -0.0917 | 0.0170 | -0.0991 to -0.0846 | -0.0997 to -0.0837 | 0.0073 | -5.38 |
| c07 | 20 | -0.0231 | 0.0216 | -0.0324 to -0.0140 | -0.0332 to -0.0130 | 0.0092 | -1.07 |
| c08 | 20 | 0.0227 | 0.0170 | 0.0154 to 0.0299 | 0.0148 to 0.0307 | 0.0072 | 1.34 |

### LCB minus MEAN

| Cell | Seeds | Mean | SD | Bootstrap 95% | t 95% | Half-width | Mean/SD |
|---|---|---|---|---|---|---|---|
| c00 | 20 | -0.0855 | 0.0206 | -0.0943 to -0.0767 | -0.0952 to -0.0759 | 0.0088 | -4.15 |
| c01 | 20 | -0.0233 | 0.0263 | -0.0351 to -0.0127 | -0.0356 to -0.0110 | 0.0112 | -0.89 |
| c02 | 20 | 0.0101 | 0.0238 | -0.0002 to 0.0203 | -0.0010 to 0.0213 | 0.0102 | 0.43 |
| c03 | 20 | -0.1019 | 0.0299 | -0.1145 to -0.0892 | -0.1159 to -0.0879 | 0.0126 | -3.41 |
| c04 | 20 | -0.0485 | 0.0311 | -0.0616 to -0.0353 | -0.0630 to -0.0339 | 0.0132 | -1.56 |
| c05 | 20 | -0.0112 | 0.0310 | -0.0245 to 0.0016 | -0.0258 to 0.0033 | 0.0130 | -0.36 |
| c06 | 20 | -0.1004 | 0.0207 | -0.1096 to -0.0918 | -0.1102 to -0.0907 | 0.0089 | -4.84 |
| c07 | 20 | -0.0572 | 0.0174 | -0.0647 to -0.0499 | -0.0653 to -0.0491 | 0.0074 | -3.30 |
| c08 | 20 | -0.0404 | 0.0200 | -0.0488 to -0.0315 | -0.0498 to -0.0310 | 0.0087 | -2.02 |

Pooled over cells (equal weight, stratified bootstrap):

| Contrast | Cells | Pooled mean | 95% interval | One-sided 95% lower bound |
|---|---|---|---|---|
| SHRINK_1 minus MEAN | 9 | 0.0111 | 0.0097 to 0.0125 | 0.0100 |
| SHRINK_5 minus MEAN | 9 | 0.0068 | 0.0041 to 0.0094 | 0.0045 |
| SHRINK_20 minus MEAN | 9 | -0.0196 | -0.0228 to -0.0162 | -0.0223 |
| LCB minus MEAN | 9 | -0.0509 | -0.0545 to -0.0474 | -0.0539 |

Per noise level (protocol section 13.2, A-2): equal-weight mean over the cells at each sigma, two-sided 95% stratified bootstrap interval. Descriptive; not in the Holm family.

| Contrast | sigma (stars) | Cells | Mean | 95% interval |
|---|---|---|---|---|
| SHRINK_1 minus MEAN | 0.5 | 3 | -0.0025 | -0.0051 to -0.0000 |
| SHRINK_1 minus MEAN | 1.0 | 3 | 0.0144 | 0.0119 to 0.0168 |
| SHRINK_1 minus MEAN | 1.5 | 3 | 0.0215 | 0.0193 to 0.0236 |
| SHRINK_5 minus MEAN | 0.5 | 3 | -0.0347 | -0.0394 to -0.0301 |
| SHRINK_5 minus MEAN | 1.0 | 3 | 0.0135 | 0.0087 to 0.0183 |
| SHRINK_5 minus MEAN | 1.5 | 3 | 0.0415 | 0.0369 to 0.0460 |
| SHRINK_20 minus MEAN | 0.5 | 3 | -0.0786 | -0.0839 to -0.0732 |
| SHRINK_20 minus MEAN | 1.0 | 3 | -0.0116 | -0.0176 to -0.0057 |
| SHRINK_20 minus MEAN | 1.5 | 3 | 0.0315 | 0.0254 to 0.0376 |
| LCB minus MEAN | 0.5 | 3 | -0.0960 | -0.1020 to -0.0900 |
| LCB minus MEAN | 1.0 | 3 | -0.0430 | -0.0494 to -0.0368 |
| LCB minus MEAN | 1.5 | 3 | -0.0138 | -0.0201 to -0.0078 |

![EXP-003: tau-b(SHRINK_5) minus tau-b(MEAN) per cell. Simulated. Dot-and-interval chart. One row per cell; the dot is the mean paired difference in Kendall tau-b over seeds and the bar its 95% percentile bootstrap interval (10000 resamples). Seeds per cell: 20, 20, 20, 20, 20, 20, 20, 20, 20. The dashed line marks zero.](figures/fig_primary_contrast.svg){fig-alt="Simulated. Dot-and-interval chart. One row per cell; the dot is the mean paired difference in Kendall tau-b over seeds and the bar its 95% percentile bootstrap interval (10000 resamples). Seeds per cell: 20, 20, 20, 20, 20, 20, 20, 20, 20. The dashed line marks zero."}

## Checks, failures and degenerate cases

- Minimum ORACLE tau-b over runs: 1.000000000000 (must equal 1).
- Failed runs: 0.
- Degenerate-case flags: 0.
- Runtime per run: mean 13.88 ms, median 3.91 ms, max 104.90 ms; wall time 2.51 s; process peak RSS 97.9 MiB.
