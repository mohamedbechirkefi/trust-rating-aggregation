<!-- SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0 -->
# EXP-001 report: mean versus uncertainty-aware ranking under random reporting

## 1. Identification

| Field | Value |
|---|---|
| Experiment | EXP-001 (confirmatory; primary hypothesis H1) |
| Status | Complete. The frozen matrix ran in full: 180 of 180 runs ok, 0 failed, 0 retried |
| Report version | 1.0 (M3), 2026-11-25, written under the owner's approval of 2026-11-25 (D-013) from committed results only |
| Authorship | Mohamed Bechir Kefi, independent researcher (owner-approved, C3; owner, 2026-11-26, decision sheet). An AI system, used as a research and development assistant, ran the experiment and drafted this report; it is not an author |
| Protocol | `research/experiments/EXP-001/protocol.md` v1.0, SHA-256 `27766885e692caa61253528fe5d959ab25f4b64db65bfde28c301671df31ce50`; study protocol `research/protocol.md` `3226e302fb4758327d50a5f583026d469d7ccbc5ad7c72b458fcd8bf2b702f03` |
| Config | `experiments/EXP-001.json`, file SHA-256 `bb3bec3b81261bc1c8701c63a26decfe6d229d23db8d90ed7738b7f10e4f0279` (equal to the freeze record) |
| Provenance revision | `bd9e1460e29389def8baa43d6ca7cc553d659ff1`, clean tree |
| Data | Simulated. Generator calibrated on MovieLens 1M (protocol section 13.1); `data/manifest.json` `ed8fb8eee48be9a08850c48872883a4299e3e4601b9ac4a371df65e023dd4d30` |

All numbers below are simulated and hold only under the model of `research/protocol.md`. Real product quality is unobserved. Every number is copied from `research/experiments/EXP-001/results_tables.md`, `results/confirmatory/analysis/EXP-001.json` or `results/confirmatory/EXP-001/` (report, summary, manifest).

## 2. Executive summary

**Question.** In simulated catalogues of 200 products with known true quality, does ranking by Bayesian shrinkage with five pseudo-reviews (SHRINK_5) recover the true order better than ranking by the arithmetic mean (MEAN), and how does the gap depend on review count and rating noise?

**Method.** Nine cells (mean review count `nu` in {3, 10, 30} by rating noise `sigma` in {0.5, 1.0, 1.5} stars), 20 seeds each, all arms scored on the same catalogue. Primary estimand `Dbar`: the equal-weight mean over cells of `D = tau_b(SHRINK_5) - tau_b(MEAN)`.

**Outcome.** `Dbar = 0.0046` (two-sided 95% stratified bootstrap 0.0030 to 0.0061; one-sided 95% lower bound 0.0032). Under the frozen rule, H1 is **supported**. Under amendment A-2 the result must be stated per noise level, and **the direction depends on the noise level**: `D_sigma = -0.0198` (-0.0225 to -0.0172) at sigma 0.5, `0.0085` (0.0056 to 0.0113) at sigma 1.0 and `0.0250` (0.0224 to 0.0277) at sigma 1.5. Shrinkage ranks worse than the mean when ratings are precise and better when they are noisy. The pooled positive value is a property of this grid, not a uniform effect. Secondary H1b is contradicted and H1c is not supported.

**Principal caveat.** The effect is small, and EXP-003 shows that its sign reverses when the shrinkage centre moves by half a star (S2) or when the quality distribution changes (S4).

## 3. Rationale

Efron and Morris (1975) study Stein-type estimators that shrink separate means towards a common value (only the first page was read for this project, so the paper is cited for that general idea, not for a specific result). Miller (2009, 2014) argues that sorting by a raw average promotes items with few ratings and proposes lower bounds. These sources support the mechanism, not the size or sign of a ranking effect in a given population (`research/literature_review.md`). The gap addressed here: whether lower squared error translates into better whole-list rank recovery, and under which review-count and noise conditions.

## 4. Hypotheses and operational definitions

- Truth: `theta_i = E[r | mu_i, sigma]` (stars), with `mu_i = 1 + 4 B_i`, `B_i ~ Beta(4.2726, 3.1944)` and ratings `clip(floor(mu + sigma e + 0.5), 1, 5)`.
- MEAN: `xbar_i`, or the catalogue mean `m` if `n_i = 0`. SHRINK(kappa): `(n_i xbar_i + kappa m) / (n_i + kappa)`. LCB: Dirichlet posterior mean minus 1.645 posterior SD, with the prior `alpha_k = 5 p_k` centred on `m` (A-1).
- Metric: Kendall tau-b between scores and `theta` over all 200 products (unitless).
- H0: `Dbar <= 0`. H1: `Dbar > 0`. Contradiction: a one-sided 95% lower bound of `Dbar` at or below 0.
- H1b: `E[D]` decreases with `nu` (3 > 10 > 30) at every noise level. Contradicted if not so ordered in a majority of noise levels, or if the `nu = 3` and `nu = 30` intervals overlap at every noise level.
- H1c: `tau_b(LCB) - tau_b(MEAN) > 0`, pooled as for H1.
- Secondary Holm family: H1b, H1c, SHRINK_1 and SHRINK_20 against MEAN (D-011).

## 5. Methodology

- Design: full 3 x 3 factorial, 20 seeds per cell, 180 catalogues. Arms are paired on the same catalogue (common random numbers). Seeds `SeedSequence([20261124, 1, seed_index])`; the quality stream depends only on the seed index.
- Review counts: negative binomial with mean `nu` and dispersion 0.4909 (MovieLens fit); `lambda = 0`, `gamma = 0`.
- Statistics (protocol section 6): per cell, the mean paired difference with a 95% percentile bootstrap over seeds (10,000 resamples, seed 20261124) and a t interval as a cross-check; pooled `Dbar` by stratified bootstrap (seeds resampled within cells); `D_sigma` as the equal-weight mean of the three cells at each sigma, with a two-sided stratified bootstrap interval (A-2); Holm at alpha 0.05 over the secondary family, with bootstrap p-values (D-011).
- Software: Python 3.12.1, numpy 2.3.4, scipy 1.16.2, jsonschema 4.25.1, locked by `uv.lock`. Hardware: Apple M1 Pro, 16 GiB, macOS 15.3.1. Budget: under 30 minutes; 2.22 s used.

## 6. Implementation verification

- Full test suite before the runs: 165 passed, 0 failed. It covers hand-computed estimator values, tau-b against an O(N^2) reference, deterministic tie-breaking and the frozen-analysis layer (`tests/test_hypotheses.py`).
- Metric validation on known cases (`scripts/validate_metrics.py`, exploratory, JRN-0006): 26 of 26 checks passed (`results/exploratory/metric-validation/validation.json`).
- Smoke run (exploratory seed namespace 0): 6 runs, 0 failed. Its `results.json` is byte-identical to the M2 smoke output (SHA-256 `8fe78903...`), so no new contrast value was seen before the confirmatory runs.
- In every confirmatory run the ORACLE arm gave tau-b = 1 (minimum over runs 1.000000000000). No degenerate-case flag was raised.
- Faithfulness: the analysis layer (`src/trust/hypotheses.py`) was committed at `bd9e146` before any confirmatory catalogue existed. No protocol, config, seed or analysis code changed afterwards.

## 7. Execution record

- Commands: `PYTHONPATH=src nice -n 10 .venv/bin/python -m trust.cli run --config experiments/EXP-001.json` (exit 0); `trust.cli report --dir results/confirmatory/EXP-001 --pdf`; `scripts/analyse_confirmatory.py --exp EXP-001`.
- Start 2026-11-24T23:35:20Z, end 2026-11-24T23:35:23Z (UTC). Wall time 2.22 s; per run mean 12.29 ms, median 3.95 ms, max 101.97 ms; process peak RSS 96.9 MiB.
- Run ids `RUN-EXP-001-c00-s000` to `RUN-EXP-001-c08-s019`: 180 planned, 180 ok, 0 failed, 0 retried. Per-run provenance (config hash, seed, revision, data manifest hash, hardware, times, status) is in `results/confirmatory/provenance.csv`.
- Deviations: none from the frozen protocol, config or seeds. The Holm p-value method, which the frozen text left open, was fixed before data (D-011) and accepted by the owner with disclosure (owner, 2026-11-25, "approve all recommendations, RIGGED A"; D-013).

## 8. Results

**Primary (H1).**

| Estimand | Estimate | Two-sided 95% | One-sided 95% lower bound | Cells | Verdict (frozen rule) |
|---|---|---|---|---|---|
| Dbar | 0.0046 | 0.0030 to 0.0061 | 0.0032 | 9 | supported |

**Per noise level (A-2, descriptive).**

| sigma (stars) | D_sigma | Two-sided 95% |
|---|---|---|
| 0.5 | -0.0198 | -0.0225 to -0.0172 |
| 1.0 | 0.0085 | 0.0056 to 0.0113 |
| 1.5 | 0.0250 | 0.0224 to 0.0277 |

The intervals exclude 0 with opposite signs, so the frozen wording applies: the direction depends on the noise level.

**Per cell.**

| Cell | nu | sigma | Mean D | SD | Bootstrap 95% | t 95% | Mean/SD |
|---|---|---|---|---|---|---|---|
| c00 | 3 | 0.5 | -0.0109 | 0.0088 | -0.0148 to -0.0074 | -0.0150 to -0.0068 | -1.25 |
| c01 | 3 | 1.0 | 0.0078 | 0.0105 | 0.0033 to 0.0123 | 0.0029 to 0.0128 | 0.74 |
| c02 | 3 | 1.5 | 0.0183 | 0.0105 | 0.0138 to 0.0229 | 0.0133 to 0.0232 | 1.74 |
| c03 | 10 | 0.5 | -0.0234 | 0.0119 | -0.0284 to -0.0183 | -0.0289 to -0.0178 | -1.97 |
| c04 | 10 | 1.0 | 0.0069 | 0.0089 | 0.0031 to 0.0107 | 0.0027 to 0.0111 | 0.77 |
| c05 | 10 | 1.5 | 0.0260 | 0.0115 | 0.0210 to 0.0308 | 0.0206 to 0.0314 | 2.25 |
| c06 | 30 | 0.5 | -0.0253 | 0.0110 | -0.0300 to -0.0206 | -0.0304 to -0.0201 | -2.29 |
| c07 | 30 | 1.0 | 0.0107 | 0.0146 | 0.0044 to 0.0168 | 0.0038 to 0.0175 | 0.73 |
| c08 | 30 | 1.5 | 0.0309 | 0.0104 | 0.0264 to 0.0353 | 0.0260 to 0.0358 | 2.97 |

Every cell has 20 seeds, and every per-cell bootstrap interval excludes 0. The bootstrap and t intervals agree closely.

**H1b (ordering by review count).**

| sigma | E[D] nu=3 | nu=10 | nu=30 | Ordered 3 > 10 > 30 | nu 3 and nu 30 intervals overlap |
|---|---|---|---|---|---|
| 0.5 | -0.0109 | -0.0234 | -0.0253 | yes | no |
| 1.0 | 0.0078 | 0.0069 | 0.0107 | no | yes |
| 1.5 | 0.0183 | 0.0260 | 0.0309 | no | no |

Frozen verdict: **contradicted** (ordered at 1 of 3 noise levels). At sigma 1.5 the advantage grows with `nu`, the opposite of the hypothesised direction. At sigma 0.5 the ordering holds only because `D` becomes more negative as `nu` grows.

**Secondary family (Holm, alpha 0.05; bootstrap p-values, D-011, owner-accepted D-013).**

| Contrast | Estimate | Two-sided 95% | p | Holm-adjusted p | Rejects H0 |
|---|---|---|---|---|---|
| SHRINK_1 minus MEAN | 0.0075 | 0.0066 to 0.0082 | 0.0001 | 0.0004 | yes |
| H1b (nu 3 minus nu 30) | -0.0004 | -0.0042 to 0.0036 | 0.5706 | 1.0000 | no |
| H1c (LCB minus MEAN) | -0.0647 | -0.0689 to -0.0604 | 1.0000 | 1.0000 | no |
| SHRINK_20 minus MEAN | -0.0125 | -0.0143 to -0.0106 | 1.0000 | 1.0000 | no |

Per noise level (descriptive):

| Contrast | sigma 0.5 | sigma 1.0 | sigma 1.5 |
|---|---|---|---|
| SHRINK_1 minus MEAN | -0.0001 (-0.0017 to 0.0014) | 0.0094 (0.0079 to 0.0108) | 0.0131 (0.0119 to 0.0143) |
| SHRINK_20 minus MEAN | -0.0478 (-0.0508 to -0.0447) | -0.0080 (-0.0114 to -0.0045) | 0.0183 (0.0149 to 0.0219) |
| LCB minus MEAN | -0.0953 (-0.1023 to -0.0880) | -0.0581 (-0.0651 to -0.0511) | -0.0406 (-0.0484 to -0.0328) |

H1c is not supported: the centred LCB ranks clearly worse than the mean at every noise level. SHRINK_1 is the only arm that improves on MEAN overall; at sigma 0.5 its difference is null. SHRINK_20 shows the same sign pattern as SHRINK_5 by sigma, with larger losses at low noise.

**Secondary metrics.** Spearman rho, precision at 10, regret at 10 (stars), interval coverage and RMSE (stars) per arm and cell are in `results/confirmatory/EXP-001/report.md`, section "Mean metric per arm and cell". They were not part of any test and are not summarised here.

**Realised data.** Share of products with zero reviews: 0.381 at `nu = 3`, 0.220 at `nu = 10` and 0.132 at `nu = 30`. These are identical across sigma because counts share random numbers across cells (`results/confirmatory/EXP-001/report.md`, "Cells").

![FIG-001. EXP-001: SHRINK_5 minus MEAN in Kendall tau-b. Dot-and-interval chart of D for the nine cells (20 seeds each), the three D_sigma and the pooled Dbar. Dots are means; bars are two-sided 95% stratified bootstrap intervals (10,000 resamples). Dashed line at zero. Simulated.](figures/FIG-001.svg){fig-alt="Dot-and-interval chart. The three sigma 0.5 cells and D_sigma at 0.5 lie left of zero, between about -0.011 and -0.025. The sigma 1.0 and 1.5 rows lie right of zero, up to 0.031. The pooled Dbar sits just right of zero at 0.0046, with an interval from 0.0030 to 0.0061."}

## 9. Interpretation

**Expected versus observed.** The protocol expected a positive `Dbar` that shrinks as reviews accumulate. Observed: a small positive `Dbar` whose sign is set by rating noise, not by review count. Shrinkage loses at sigma 0.5 in every cell and wins at sigma 1.0 and 1.5 in every cell.

**Measured observations.** Under this model, SHRINK_5 ranks slightly better than MEAN on average over the grid, worse when noise is low and better when it is high. The centred LCB ranks worse than MEAN everywhere.

**Model-dependent inference.** At low noise a few ratings already place a product well, so pulling data-poor products towards `m` mainly moves genuinely good or bad products into the middle and costs rank accuracy. At high noise the variance reduction dominates. This fits a bias-variance reading of shrinkage. It does not support the simpler reading "shrinkage always helps with few reviews", but this experiment does not test any source directly.

**Dependence on the grid.** With equal weight on sigma 0.5, 1.0 and 1.5, the two positive levels outweigh the negative one. A grid weighted towards precise ratings would give a negative `Dbar`. The MovieLens reference noise (sigma 1.05, protocol section 13.3) lies near the middle level, but carrying it over to products is an assumption.

**Alternatives.** The advantage could be a zero-review artefact. EXP-003 S1 finds that it survives among reviewed products. It could also depend on the prior matching the population, and EXP-003 S2 and S4 find that it reverses. The failure of H1b is not evidence that review count does not matter: within a noise level, the magnitude of `D` changes with `nu`, in a direction that depends on sigma.

## 10. Threats to validity

- **Internal.** Paired design, fixed seeds and an analysis committed before data. The C4 disclosure in `research/freeze.json` lists the exploratory contrast values seen before the freeze. They showed the same sign pattern by sigma, under the planning generator.
- **Statistical.** 20 seeds per cell. Percentile bootstrap intervals can be slightly narrow at n = 20, but the t intervals in section 8 agree closely. Holm p-values use bootstrap tails resolved to 1/10,001 (D-011, owner-accepted D-013).
- **Construct.** Tau-b weights all pairs equally, while users mostly see the top of a list. Top-of-list metrics are secondary here.
- **External.** Simulation only. The calibration transfers movie-rating dispersion and quality shape to products. Results hold for N = 200 and this grid.

## 11. Conclusion and next experiment

Under the frozen rule, H1 is supported (`Dbar = 0.0046`, one-sided lower bound 0.0032), but the direction depends on rating noise: shrinkage hurts rank recovery at sigma 0.5 and helps at sigma 1.0 and 1.5. H1b is contradicted and H1c is not supported. The supported statement is conditional: under this model, accounting for sample size helps ranking when individual ratings are noisy and can hurt when they are precise. A follow-up that registers a sigma-direction hypothesis would be informed by these results and would need a new EXP id and the owner's approval.

## M4 addendum (2026-11-25, exploratory, D-014)

Three exploratory checks made at M4 (JRN-0010; `results/exploratory/m4-sensitivity/m4_exploratory.md`) qualify sections 8 and 9 without changing any frozen verdict:

- **H1b.** Section 8 says that at sigma 1.5 "the advantage grows with `nu`". Among reviewed products (EXP-003 S1 catalogues) `D` at sigma 1.5 is flat: 0.0426, 0.0414 and 0.0405 at `nu` 3, 10 and 30. The growth seen here is largely dilution by unreviewed products, which both arms score identically and which are more common at small `nu`. The verdict (contradicted) stands.
- **Metric choice.** The sign pattern by noise holds on Spearman, precision at 10, regret at 10 and RMSE as well as tau-b, so it is not a tau-b or tie artefact.
- **H1c.** LCB is worse than MEAN on whole-list metrics at every noise level, but at sigma 1.5 it is better on precision at 10 (+0.1067, 0.0717 to 0.1417) and regret at 10 (lower by 0.2245 stars). "LCB ranks worse" applies to whole-list recovery.

## 12. Reproduction appendix

```
../.tools/py/bin/uv sync --frozen --all-groups --all-extras
.venv/bin/python -m pytest -q
PYTHONPATH=src .venv/bin/python -m trust.cli run --config experiments/EXP-001.json
PYTHONPATH=src .venv/bin/python -m trust.cli report --dir results/confirmatory/EXP-001 --pdf
PYTHONPATH=src .venv/bin/python scripts/analyse_confirmatory.py --exp EXP-001
```

- Raw results: `results/confirmatory/EXP-001/results.json` (schema 1.0.0), `run_manifest.json`, `metrics.csv`, `summary.json`. Checksums: `results/confirmatory/SHA256SUMS`. Per-run provenance: `results/confirmatory/provenance.csv`.
- Analysis: `results/confirmatory/analysis/EXP-001.json` and its manifest; generated tables `research/experiments/EXP-001/results_tables.md`.
- Tolerance: per-run metrics reproduce exactly on the same platform and library versions; across platforms tau-b may differ at the 1e-12 level (protocol item 19).
- Figures: the last command regenerates `figures/FIG-001.svg` and `results_tables.md`.
- References: as in `research/literature_review.md` (Efron and Morris 1975; Miller 2009, 2014; Harper and Konstan 2015 for MovieLens).
