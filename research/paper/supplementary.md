<!-- SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0 -->
# Supplementary material

Supplement to `research/paper/manuscript.md` (version M4, 2026-11-25). Independent research manuscript / preprint draft, not peer-reviewed. All values are simulated. Every table is copied from a generated file named in its caption; nothing is retyped from memory.

## S1. Complete experimental matrix

| Experiment | Config | Grid | Fixed | Cells | Seeds | Runs | ok | failed |
|---|---|---|---|---|---|---|---|---|
| EXP-001 | `experiments/EXP-001.json` | nu {3, 10, 30} x sigma {0.5, 1.0, 1.5} | lambda 0, gamma 0 | 9 | 20 | 180 | 180 | 0 |
| EXP-002 | `experiments/EXP-002.json` | lambda {0, 2} x gamma {-0.5, 0, 0.5} x nu {3, 10} | sigma 1.0 | 12 | 20 | 240 | 240 | 0 |
| EXP-003 S1-min1 | `experiments/EXP-003-S1-min1.json` | as EXP-001 | metrics on n >= 1 | 9 | 20 | 180 | 180 | 0 |
| EXP-003 S1-min5 | `experiments/EXP-003-S1-min5.json` | as EXP-001 | metrics on n >= 5 | 9 | 20 | 180 | 180 | 0 |
| EXP-003 S2 | `experiments/EXP-003-S2.json` | as EXP-001 | adds SHRINK_5 at m + 0.5 and m - 0.5 | 9 | 20 | 180 | 180 | 0 |
| EXP-003 S3 | `experiments/EXP-003-S3.json` | as EXP-002 | truth theta_rep | 12 | 20 | 240 | 240 | 0 |
| EXP-003 S4 | `experiments/EXP-003-S4.json` | quality {Beta(1, 1), mixture} x nu x sigma | as EXP-001 | 18 | 20 | 360 | 360 | 0 |
| Total | | | | | | 1,560 | 1,560 | 0 |

Arms in every config: MEAN, SHRINK_1, SHRINK_5, SHRINK_20, LCB (centred prior, z 1.645), ORACLE (check). Counts verified against the raw result files by `scripts/audit_evidence.py` (`research/publication/evidence_audit.json`).

## S2. EXP-001 per-cell results

Source: `research/experiments/EXP-001/results_tables.md`. D = tau-b(SHRINK_5) minus tau-b(MEAN).

| Cell | nu | sigma | Seeds | Mean D | SD | Bootstrap 95% | t 95% |
|---|---|---|---|---|---|---|---|
| c00 | 3 | 0.5 | 20 | -0.0109 | 0.0088 | -0.0148 to -0.0074 | -0.0150 to -0.0068 |
| c01 | 3 | 1.0 | 20 | 0.0078 | 0.0105 | 0.0033 to 0.0123 | 0.0029 to 0.0128 |
| c02 | 3 | 1.5 | 20 | 0.0183 | 0.0105 | 0.0138 to 0.0229 | 0.0133 to 0.0232 |
| c03 | 10 | 0.5 | 20 | -0.0234 | 0.0119 | -0.0284 to -0.0183 | -0.0289 to -0.0178 |
| c04 | 10 | 1.0 | 20 | 0.0069 | 0.0089 | 0.0031 to 0.0107 | 0.0027 to 0.0111 |
| c05 | 10 | 1.5 | 20 | 0.0260 | 0.0115 | 0.0210 to 0.0308 | 0.0206 to 0.0314 |
| c06 | 30 | 0.5 | 20 | -0.0253 | 0.0110 | -0.0300 to -0.0206 | -0.0304 to -0.0201 |
| c07 | 30 | 1.0 | 20 | 0.0107 | 0.0146 | 0.0044 to 0.0168 | 0.0038 to 0.0175 |
| c08 | 30 | 1.5 | 20 | 0.0309 | 0.0104 | 0.0264 to 0.0353 | 0.0260 to 0.0358 |

Secondary arms per noise level (descriptive):

| Contrast | sigma 0.5 | sigma 1.0 | sigma 1.5 |
|---|---|---|---|
| SHRINK_1 minus MEAN | -0.0001 (-0.0017 to 0.0014) | 0.0094 (0.0079 to 0.0108) | 0.0131 (0.0119 to 0.0143) |
| SHRINK_20 minus MEAN | -0.0478 (-0.0508 to -0.0447) | -0.0080 (-0.0114 to -0.0045) | 0.0183 (0.0149 to 0.0219) |
| LCB minus MEAN | -0.0953 (-0.1023 to -0.0880) | -0.0581 (-0.0651 to -0.0511) | -0.0406 (-0.0484 to -0.0328) |

## S3. EXP-002 per-cell results

Source: `research/experiments/EXP-002/results_tables.md` and the per-run report `results/confirmatory/EXP-002/report.md` (realised counts).

| Cell | nu | lambda | gamma | Mean reported | Share zero reviews | Mean D (SHRINK_5) | Bootstrap 95% |
|---|---|---|---|---|---|---|---|
| c00 | 3 | 0 | -0.5 | 2.98 | 0.407 | -0.0025 | -0.0055 to 0.0004 |
| c01 | 3 | 0 | 0 | 3.02 | 0.387 | 0.0042 | 0.0006 to 0.0078 |
| c02 | 3 | 0 | 0.5 | 2.98 | 0.406 | 0.0016 | -0.0024 to 0.0054 |
| c03 | 3 | 2 | -0.5 | 1.89 | 0.486 | -0.0015 | -0.0041 to 0.0011 |
| c04 | 3 | 2 | 0 | 1.93 | 0.460 | 0.0034 | -0.0009 to 0.0073 |
| c05 | 3 | 2 | 0.5 | 1.98 | 0.486 | 0.0052 | 0.0017 to 0.0085 |
| c06 | 10 | 0 | -0.5 | 9.91 | 0.239 | -0.0016 | -0.0069 to 0.0036 |
| c07 | 10 | 0 | 0 | 9.92 | 0.221 | 0.0163 | 0.0113 to 0.0212 |
| c08 | 10 | 0 | 0.5 | 9.92 | 0.234 | -0.0046 | -0.0105 to 0.0013 |
| c09 | 10 | 2 | -0.5 | 6.27 | 0.294 | -0.0033 | -0.0083 to 0.0018 |
| c10 | 10 | 2 | 0 | 6.32 | 0.272 | 0.0118 | 0.0066 to 0.0168 |
| c11 | 10 | 2 | 0.5 | 6.53 | 0.289 | -0.0028 | -0.0091 to 0.0033 |

Per-stratum contrasts for SHRINK_5 and LCB are in `research/experiments/EXP-002/results_tables.md`.

## S4. EXP-003 per-noise-level results

Source: `research/experiments/EXP-003/results_tables.md`.

| Condition | sigma 0.5 | sigma 1.0 | sigma 1.5 |
|---|---|---|---|
| S1, n >= 1 | -0.0347 (-0.0394 to -0.0301) | 0.0135 (0.0087 to 0.0183) | 0.0415 (0.0369 to 0.0460) |
| S1, n >= 5 | -0.0128 (-0.0150 to -0.0106) | 0.0003 (-0.0024 to 0.0031) | 0.0111 (0.0083 to 0.0140) |
| S2, centre m + 0.5 | -0.0705 (-0.0781 to -0.0625) | -0.0337 (-0.0416 to -0.0260) | -0.0177 (-0.0252 to -0.0100) |
| S2, centre m - 0.5 | -0.0901 (-0.0971 to -0.0829) | -0.0414 (-0.0480 to -0.0347) | -0.0140 (-0.0210 to -0.0068) |
| S2 check, centre m | -0.0198 (-0.0225 to -0.0172) | 0.0085 (0.0056 to 0.0113) | 0.0250 (0.0224 to 0.0277) |
| S4, Beta(1, 1) | -0.0484 (-0.0511 to -0.0457) | -0.0191 (-0.0223 to -0.0159) | 0.0045 (0.0012 to 0.0078) |
| S4, mixture | -0.0572 (-0.0599 to -0.0546) | -0.0245 (-0.0273 to -0.0217) | 0.0022 (-0.0008 to 0.0052) |

S3: the sign of D differs between truth definitions in 0 of 12 cells (0 of the 6 lambda = 2 cells); per-cell values are identical under both truths (D-012).

## S5. Configurations and hashes

| Config | File SHA-256 (first 12) | Protocol | Protocol SHA-256 (first 12) |
|---|---|---|---|
| `experiments/EXP-001.json` | bb3bec3b8126 | `research/experiments/EXP-001/protocol.md` | 27766885e692 |
| `experiments/EXP-002.json` | 325df0660716 | `research/experiments/EXP-002/protocol.md` | 47459d4b5c8d |
| `experiments/EXP-003-S1-min1.json` | 7e9683ea0e8f | `research/experiments/EXP-003/protocol.md` | cb4568fa37e4 |
| `experiments/EXP-003-S1-min5.json` | 5b948ab09d3f | same | cb4568fa37e4 |
| `experiments/EXP-003-S2.json` | fecaa2f8523f | same | cb4568fa37e4 |
| `experiments/EXP-003-S3.json` | 4385405824d7 | same | cb4568fa37e4 |
| `experiments/EXP-003-S4.json` | e788afa2ac37 | same | cb4568fa37e4 |

Study protocol `research/protocol.md`: 3226e302fb47. Data manifest `data/manifest.json`: ed8fb8eee48b. Full hashes are in `research/freeze.json`; the audit found all twelve equal to the files on disk. The run manifests also carry a canonical-JSON hash of each config (for example 94bbf40b7a37 for EXP-001), a different definition from the file hash above.

## S6. Robustness and exploratory results

Confirmatory robustness: EXP-003 (S4 above, manuscript section 5.3). Exploratory checks made at M4 (JRN-0010; source `results/exploratory/m4-sensitivity/m4_exploratory.md`; they change no frozen verdict):

E1. Arm minus MEAN on all metrics of EXP-001 (positive favours the arm; regret and RMSE in stars, oriented MEAN minus arm).

| Arm | Metric | Pooled | sigma 0.5 | sigma 1.0 | sigma 1.5 |
|---|---|---|---|---|---|
| SHRINK_5 | Spearman | 0.0151 (0.0137 to 0.0166) | -0.0048 (-0.0068 to -0.0028) | 0.0161 (0.0136 to 0.0186) | 0.0340 (0.0309 to 0.0371) |
| SHRINK_5 | precision at 10 | 0.0389 (0.0178 to 0.0600) | -0.0850 (-0.1200 to -0.0500) | 0.0517 (0.0133 to 0.0900) | 0.1500 (0.1133 to 0.1867) |
| SHRINK_5 | regret at 10 | 0.1213 (0.1058 to 0.1373) | -0.0225 (-0.0396 to -0.0051) | 0.1516 (0.1202 to 0.1834) | 0.2349 (0.2050 to 0.2648) |
| SHRINK_5 | RMSE | 0.0986 (0.0940 to 0.1031) | -0.0281 (-0.0338 to -0.0223) | 0.1013 (0.0927 to 0.1100) | 0.2225 (0.2138 to 0.2312) |
| LCB | Spearman | -0.0686 (-0.0737 to -0.0633) | -0.0933 (-0.1015 to -0.0848) | -0.0643 (-0.0727 to -0.0559) | -0.0481 (-0.0579 to -0.0381) |
| LCB | precision at 10 | -0.0139 (-0.0333 to 0.0056) | -0.1600 (-0.1917 to -0.1283) | 0.0117 (-0.0217 to 0.0467) | 0.1067 (0.0717 to 0.1417) |
| LCB | regret at 10 | 0.0888 (0.0732 to 0.1045) | -0.0769 (-0.0981 to -0.0566) | 0.1188 (0.0877 to 0.1498) | 0.2245 (0.1947 to 0.2540) |
| LCB | RMSE | -0.1759 (-0.1838 to -0.1680) | -0.1971 (-0.2099 to -0.1842) | -0.1753 (-0.1899 to -0.1609) | -0.1554 (-0.1693 to -0.1413) |

E2. Share of products tied under MEAN, by cell (means over 20 seeds): 0.857, 0.847, 0.849 at nu 3; 0.673, 0.665, 0.669 at nu 10; 0.452, 0.461, 0.450 at nu 30 (sigma 0.5, 1.0, 1.5 in that order). The regenerated catalogues reproduce the committed tau-b values exactly.

E3. D among reviewed products (S1, n >= 1), per cell:

| sigma | nu = 3 | nu = 10 | nu = 30 |
|---|---|---|---|
| 0.5 | -0.0313 (-0.0403 to -0.0229) | -0.0392 (-0.0474 to -0.0310) | -0.0338 (-0.0403 to -0.0274) |
| 1.0 | 0.0167 (0.0060 to 0.0270) | 0.0101 (0.0041 to 0.0160) | 0.0137 (0.0053 to 0.0218) |
| 1.5 | 0.0426 (0.0325 to 0.0526) | 0.0414 (0.0335 to 0.0488) | 0.0405 (0.0347 to 0.0462) |

## S7. Experiment reports

- EXP-001: `research/experiments/EXP-001/report.md`
- EXP-002: `research/experiments/EXP-002/report.md`
- EXP-003: `research/experiments/EXP-003/report.md`
- M4 interpretation (confounders, expected versus observed): `research/publication/interpretation.md`
- Evidence audit: `research/publication/evidence_audit.md`; second review pass: `research/publication/review_pass_2.md`

## S8. Deviations and owner decisions

| Id | What | Owner decision |
|---|---|---|
| Section 13 amendments | MovieLens calibration (13.1), centred LCB prior (A-1), per-noise reporting (A-2), 20 seeds (A-3), measured SD (A-4), all before the freeze | approved 2026-11-24 ("Approve all"; "yes for all others"), D-009, D-010 |
| D-011 | Holm p-values from the stratified bootstrap; exact form of the EXP-002 contrasts and EXP-003 sign readings, fixed before data | accepted with disclosure, 2026-11-25 (D-013) |
| D-012 | S3 cannot discriminate for rank metrics; analysis manifests first recorded a dirty tree and were regenerated unchanged | accepted with disclosure, 2026-11-25 (D-013) |
| D-013 | Experiment reports written from committed results by the coordinator | owner, 2026-11-25 |
| D-014 | M4: exploratory checks E1 to E3, evidence audit, report corrections listed in `research/publication/evidence_audit.md` | M4 brief (owner, 2026-11-25, "Approve all recommendations, push then next"); no frozen file changed |

No frozen protocol, config or seed changed. No confirmatory run was repeated.
