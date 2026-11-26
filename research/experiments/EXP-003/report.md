<!-- SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0 -->
# EXP-003 report: sensitivity analyses that could invalidate the main interpretation

## 1. Identification

| Field | Value |
|---|---|
| Experiment | EXP-003 (confirmatory sensitivity analyses S1 to S4 of the EXP-001 conclusion) |
| Status | Complete. All five frozen configs ran in full: 1,140 of 1,140 runs ok, 0 failed, 0 retried |
| Report version | 1.0 (M3), 2026-11-25, written under the owner's approval of 2026-11-25 (D-013) from committed results only |
| Authorship | Mohamed Bechir Kefi, independent researcher (owner-approved, C3; owner, 2026-11-26, decision sheet). An AI system, used as a research and development assistant, ran the experiment and drafted this report; it is not an author |
| Protocol | `research/experiments/EXP-003/protocol.md` v1.0, SHA-256 `cb4568fa37e4feaa1bd1a79a71fafa47a96fcad13d8b8b2d6605932c71b19b81`; study protocol `research/protocol.md` `3226e302fb4758327d50a5f583026d469d7ccbc5ad7c72b458fcd8bf2b702f03` |
| Configs (file SHA-256, equal to the freeze record) | `EXP-003-S1-min1.json` `7e9683ea0e8f31689e5846474b0f15175aaaa1cc04dbc7cd20675729fe60a564`; `EXP-003-S1-min5.json` `5b948ab09d3fb99421c487b14ddd1fb644ff71e33d7e49bc75597fbdc69ddc89`; `EXP-003-S2.json` `fecaa2f8523f360fd5270a3481222e47aea88c27dc125a58c44592aefb22ff18`; `EXP-003-S3.json` `4385405824d78de6b48b14392d094df0277c7cf4bfec44dc359668dc2768d4d7`; `EXP-003-S4.json` `e788afa2ac3733cb22ff639d558c285fefea89aa47814025407ccdfcb3054d89` |
| Provenance revision | `bd9e1460e29389def8baa43d6ca7cc553d659ff1`, clean tree |
| Data | Simulated; `data/manifest.json` `ed8fb8eee48be9a08850c48872883a4299e3e4601b9ac4a371df65e023dd4d30` |

All numbers are simulated. Every number is copied from `research/experiments/EXP-003/results_tables.md`, `results/confirmatory/analysis/EXP-003.json` or the per-config directories under `results/confirmatory/`.

## 2. Executive summary

**Question.** Does the EXP-001 conclusion about `D = tau_b(SHRINK_5) - tau_b(MEAN)` (reference `Dbar = 0.0046`) survive changes to the zero-review convention (S1), the prior centre (S2), the definition of truth (S3) and the quality distribution (S4)?

**Outcome.**
- **S1 (zero-review convention): not invalidating.** Among products with at least one review, `Dbar = 0.0068` (0.0041 to 0.0094). With at least five reviews it is -0.0005 (-0.0019 to 0.0011), reported alongside.
- **S2 (prior centre): invalidation criterion met.** Shrinking towards `m + 0.5` gives -0.0406 (-0.0449 to -0.0361) and towards `m - 0.5` gives -0.0485 (-0.0525 to -0.0444): the sign reverses.
- **S3 (truth definition): criterion not met, but vacuously.** The sign of `D` differs in 0 of 12 cells because, for rank metrics, the two truth definitions cannot differ by construction (D-012, owner-accepted with disclosure, D-013). S3 carries no evidence.
- **S4 (quality distribution): invalidation criterion met.** Beta(1, 1) gives -0.0210 (-0.0228 to -0.0192) and the Beta(2, 6)/Beta(6, 2) mixture gives -0.0265 (-0.0281 to -0.0249): the sign reverses.

**Principal caveat.** The small positive EXP-001 effect depends on the shrinkage target and on the population matching the generator. Two of the four prespecified checks overturn it, which strongly limits the main interpretation.

## 3. Rationale

Shrinkage pulls estimates towards a chosen target (Efron and Morris 1975, first page only read), so its gains can depend on that target; and Miller (2014) notes that the lower-bound method is approximate. The checks target the assumptions the EXP-001 result could silently depend on: zero-review imputation, the prior centre, the truth definition under selection and the match between the prior family and the population.

## 4. Hypotheses and operational definitions

The interpretation under test is "uncertainty awareness improves rank recovery", which predicts an advantage that persists among reviewed products and degrades gracefully under prior misspecification. Frozen invalidation criteria (protocol item 6):

- S1, `n_i >= 1`: pooled `Dbar` interval containing or below 0 while the EXP-001 pooled `Dbar` is positive.
- S2: sign reversal of `Dbar` under a 0.5-star shift of the shrinkage centre.
- S3: the sign of `D` differs between `theta` and `theta_rep` in a majority of strata.
- S4: sign reversal under either alternative quality distribution.

"Positive" and "sign reversal" compare point estimates; S3 counts over the 12 EXP-002 cells (D-011, fixed before data). Only two-sided 95% stratified bootstrap intervals are used; no Holm correction applies to EXP-003.

## 5. Methodology

- S1: EXP-001 catalogues regenerated with the same seeds (`exp_number` 1); metrics restricted to products with `n_i >= 1` (S1-min1) and `n_i >= 5` (S1-min5).
- S2: SHRINK_5 towards `m + 0.5` and `m - 0.5` on EXP-001 catalogues; the unshifted SHRINK_5 is included as a check.
- S3: EXP-002 catalogues (`exp_number` 2) scored against `theta_rep = E[r | reported]`, compared with EXP-002 scored against `theta`.
- S4: the EXP-001 matrix with `mu ~ 1 + 4 Beta(1, 1)` and with an equal mixture of `1 + 4 Beta(2, 6)` and `1 + 4 Beta(6, 2)`; 18 cells.
- 20 seeds per cell; stratified bootstrap with 10,000 resamples, seed 20261124; `D_sigma` per noise level for S1, S2 and S4 (A-2).
- Software and hardware as EXP-001. Budget under 60 minutes; about 12 s of wall time in total.

## 6. Implementation verification

- Test suite before the runs: 165 passed, 0 failed; `tests/test_hypotheses.py` checks the EXP-003 chain end to end on exploratory catalogues, including that S2's unshifted arm reproduces the EXP-001 `Dbar` and that S3 signs agree at `lambda = 0`.
- Check observed in the confirmatory data: the S2 unshifted SHRINK_5 gives `Dbar = 0.0046` (0.0030 to 0.0061), identical to EXP-001, as common random numbers require.
- ORACLE tau-b = 1 in every run of every sub-analysis; 0 degenerate-case flags.
- S1-min5: no catalogue had fewer than 20 evaluated products, so no cell was flagged.

## 7. Execution record

| Sub-analysis | Runs (ok / failed) | Wall time | Per run mean / max | Peak RSS |
|---|---|---|---|---|
| S1-min1 | 180 / 0 | 2.51 s | 13.88 / 104.90 ms | 97.9 MiB |
| S1-min5 | 180 / 0 | 1.57 s | 8.71 / 82.32 ms | 97.4 MiB |
| S2 | 180 / 0 | 1.52 s | 8.44 / 83.92 ms | 96.6 MiB |
| S3 | 240 / 0 | 1.97 s | 8.18 / 199.94 ms | 96.9 MiB |
| S4 | 360 / 0 | 4.28 s | 11.87 / 108.02 ms | 95.4 MiB |

- Commands: `PYTHONPATH=src nice -n 10 .venv/bin/python -m trust.cli run --config experiments/EXP-003-<S>.json` for each config (all exit 0); `trust.cli report --dir results/confirmatory/EXP-003-<S> --pdf`; `scripts/analyse_confirmatory.py --exp EXP-003`.
- Runs between 2026-11-24T23:35:28Z and 23:35:48Z (UTC). No run failed or was retried. Provenance per run in `results/confirmatory/provenance.csv`.
- Deviations: none from the frozen protocol, configs or seeds. Two owner-accepted disclosures (owner, 2026-11-25, "approve all recommendations, RIGGED A"; D-013): D-011 (how "positive", "sign reversal" and the S3 strata are read, fixed before data) and D-012 (S3 cannot discriminate by design).

## 8. Results

**Pooled `Dbar` per condition** (EXP-001 reference: 0.0046).

| Condition | Contrast | Cells | Dbar | Two-sided 95% | Frozen invalidation criterion met |
|---|---|---|---|---|---|
| S1, n >= 1 | SHRINK_5 - MEAN | 9 | 0.0068 | 0.0041 to 0.0094 | no |
| S1, n >= 5 | SHRINK_5 - MEAN | 9 | -0.0005 | -0.0019 to 0.0011 | n/a (reported) |
| S2, centre m + 0.5 | SHRINK_5_UP - MEAN | 9 | -0.0406 | -0.0449 to -0.0361 | yes |
| S2, centre m - 0.5 | SHRINK_5_DOWN - MEAN | 9 | -0.0485 | -0.0525 to -0.0444 | yes |
| S2 check, centre m | SHRINK_5 - MEAN | 9 | 0.0046 | 0.0030 to 0.0061 | n/a |
| S3, truth theta_rep (pooled) | SHRINK_5 - MEAN | 12 | 0.0022 | 0.0009 to 0.0035 | see S3 |
| S4, Beta(1, 1) | SHRINK_5 - MEAN | 9 | -0.0210 | -0.0228 to -0.0192 | yes |
| S4, Beta(2, 6)/Beta(6, 2) mixture | SHRINK_5 - MEAN | 9 | -0.0265 | -0.0281 to -0.0249 | yes |

**Per noise level (A-2, descriptive).**

| Condition | sigma 0.5 | sigma 1.0 | sigma 1.5 |
|---|---|---|---|
| S1, n >= 1 | -0.0347 (-0.0394 to -0.0301) | 0.0135 (0.0087 to 0.0183) | 0.0415 (0.0369 to 0.0460) |
| S1, n >= 5 | -0.0128 (-0.0150 to -0.0106) | 0.0003 (-0.0024 to 0.0031) | 0.0111 (0.0083 to 0.0140) |
| S2, centre m + 0.5 | -0.0705 (-0.0781 to -0.0625) | -0.0337 (-0.0416 to -0.0260) | -0.0177 (-0.0252 to -0.0100) |
| S2, centre m - 0.5 | -0.0901 (-0.0971 to -0.0829) | -0.0414 (-0.0480 to -0.0347) | -0.0140 (-0.0210 to -0.0068) |
| S2 check, centre m | -0.0198 (-0.0225 to -0.0172) | 0.0085 (0.0056 to 0.0113) | 0.0250 (0.0224 to 0.0277) |
| S4, Beta(1, 1) | -0.0484 (-0.0511 to -0.0457) | -0.0191 (-0.0223 to -0.0159) | 0.0045 (0.0012 to 0.0078) |
| S4, mixture | -0.0572 (-0.0599 to -0.0546) | -0.0245 (-0.0273 to -0.0217) | 0.0022 (-0.0008 to 0.0052) |

**S3: sign of `D` under the two truth definitions.** For every one of the 12 EXP-002 cells, the mean `D` and its interval against `theta_rep` equal those against `theta` (for example c07: 0.0163, 0.0113 to 0.0212, under both). The sign differs in 0 of 12 cells (0 of the 6 `lambda = 2` cells). As recorded in D-012, `theta_rep` is strictly increasing in `mu` within a cell, as is `theta`, so tau-b, Spearman and precision at 10 cannot differ; the S3 tau-b values equal the EXP-002 values exactly in all 240 runs. RMSE, regret and coverage do differ. The full per-cell table is in `research/experiments/EXP-003/results_tables.md`.

![FIG-003. EXP-003: pooled D under each sensitivity condition. Dot-and-interval chart of the pooled difference in Kendall tau-b against MEAN for each condition, next to the EXP-001 reference. Each row pools 9 or 12 cells of 20 seeds; bars are two-sided 95% stratified bootstrap intervals (10,000 resamples). Dashed line at zero. Simulated.](figures/FIG-003.svg){fig-alt="Dot-and-interval chart. The EXP-001 reference, the S2 check, S1 with at least one review and S3 sit just right of zero. S1 with at least five reviews straddles zero. Both S2 shifted centres lie far left, near -0.04 and -0.05, and both S4 distributions lie left, near -0.02 and -0.03."}

## 9. Interpretation

**Expected versus observed.** If the advantage came from uncertainty awareness in general, it should persist among reviewed products (S1) and degrade gracefully under misspecification (S2, S4). S1 behaves as expected: restricting to reviewed products increases `Dbar` to 0.0068, so the advantage is not an artefact of how zero-review products are scored. S2 and S4 do not: a half-star error in the shrinkage centre turns a +0.0046 advantage into losses of -0.0406 and -0.0485, and a different population shape turns it into -0.0210 and -0.0265. The degradation is not graceful.

**Model-dependent inference.** Shrinkage helps ranking only when its target matches the population: a uniform or bimodal quality distribution places many genuinely extreme products among the data-poor ones, and pulling them towards the centre costs rank accuracy. The noise dependence seen in EXP-001 persists in every condition (negative at sigma 0.5, more favourable at sigma 1.5).

**S1 with n >= 5.** The advantage disappears (-0.0005, -0.0019 to 0.0011) once products with fewer than five reviews are removed, consistent with shrinkage mattering mainly for data-poor products. This is reported; the frozen criterion concerns `n >= 1` only.

**S3.** The registered S3 cannot test the truth-definition explanation for rank metrics. Its "criterion not met" is a property of the design, not evidence that the conclusion is robust to the truth definition. A value-based S3 (for example RMSE or regret) would be a new, owner-approved analysis.

## 10. Threats to validity

- **Internal.** Same seeds and catalogues as EXP-001 and EXP-002; analysis fixed before data (D-011).
- **Statistical.** No multiplicity correction across S1 to S4, as frozen; the reversals in S2 and S4 have intervals far from 0.
- **Construct.** S3 is non-diagnostic for rank metrics (D-012, owner-accepted with disclosure, D-013).
- **External.** The alternative distributions and the 0.5-star shift are single choices; the sensitivity of the conclusion to intermediate misspecification was not mapped.

## 11. Conclusion and next experiment

The EXP-001 advantage of shrinkage survives the zero-review check (S1) but reverses under a half-star shift of the shrinkage centre (S2) and under both alternative quality distributions (S4); both frozen invalidation criteria are met. S3 is uninformative by construction. The main interpretation must therefore be restricted: under this model, SHRINK_5 improves whole-list rank recovery only when rating noise is moderate to high, the shrinkage target is the true catalogue mean and the population shape matches the calibrated Beta. Next, subject to owner approval and a new EXP id: map the advantage over a range of prior shifts and population shapes, and register a value-based truth-definition check.

## 12. Reproduction appendix

```
../.tools/py/bin/uv sync --frozen --all-groups --all-extras
.venv/bin/python -m pytest -q
for S in S1-min1 S1-min5 S2 S3 S4; do
  PYTHONPATH=src .venv/bin/python -m trust.cli run --config experiments/EXP-003-$S.json
  PYTHONPATH=src .venv/bin/python -m trust.cli report --dir results/confirmatory/EXP-003-$S --pdf
done
PYTHONPATH=src .venv/bin/python scripts/analyse_confirmatory.py --exp EXP-003
```

- EXP-003's analysis also reads `results/confirmatory/EXP-001/results.json` and `results/confirmatory/EXP-002/results.json`.
- Raw results: `results/confirmatory/EXP-003-<S>/results.json` (schema 1.0.0) with manifests, metrics and summaries; checksums `results/confirmatory/SHA256SUMS`; provenance `results/confirmatory/provenance.csv`.
- Analysis: `results/confirmatory/analysis/EXP-003.json` and its manifest; tables `research/experiments/EXP-003/results_tables.md`; figure `figures/FIG-003.svg`.
- Tolerance: as EXP-001.
- References: as in `research/literature_review.md` (Efron and Morris 1975; Miller 2014).
