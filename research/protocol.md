<!-- SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0 -->
# TRUST research protocol

**Status: DRAFT v0.1, 2026-11-24. NOT FROZEN.** Freezing is the owner's decision (G-FREEZE). Until the owner freezes this protocol and its hash is recorded in `research/decision_log.md`, every run is exploratory and labelled so. Numbers marked "planning assumption" are not measurements.

## 1. Research question

When do average ratings misrank products compared with uncertainty-aware estimators?

Operationally: in simulated catalogues where the true quality of each product is known by construction, how much worse (or better) does ranking by the arithmetic mean of star ratings recover the true quality order than ranking by Bayesian shrinkage or by a lower credible bound, and how does that gap change with review count, rating noise, prior strength, reporting selection and missingness?

## 2. Formal model (simulation, all quantities synthetic)

A catalogue has `N = 200` products, indexed `i`.

- **Latent quality.** `mu_i = 1 + 4 * B_i`, `B_i ~ Beta(4, 2)` (stars, range [1, 5]).
- **Potential rating.** `r_ij = clip(floor(mu_i + sigma * e_ij + 0.5), 1, 5)`, `e_ij ~ N(0, 1)`, integer stars 1..5. `sigma` is rating noise in stars.
- **True quality (ranking target).** `theta_i = E[r_ij | mu_i, sigma] = sum_k k * P(r = k | mu_i, sigma)`, computed exactly from the normal CDF. For fixed `sigma`, `theta_i` is strictly increasing in `mu_i`, so the true order does not depend on the rounding convention.
- **Review count.** Potential raters `n*_i ~ NegBin(mean = nu * w_i, dispersion = 1)`, which allows zero reviews. Exposure weight `w_i = exp(gamma * z_i) / mean_i exp(gamma * z_i)`, `z_i` the standardised `mu_i`. `gamma = 0` means exposure independent of quality.
- **Reporting selection (under-reporting bias, after Hu, Pavlou and Zhang).** A potential rating `r` is reported with probability `pi(r) = (1 + lambda * |r - 3| / 2) / (1 + lambda)`. `lambda = 0` means every potential rating is reported. `lambda > 0` makes extreme ratings more likely to be reported.
- **Observed data.** For each product: reported count `n_i`, mean `xbar_i` (if `n_i >= 1`), counts `n_ik` per star level.
- **Catalogue prior mean.** `m = ` mean of all reported ratings in the catalogue (empirical Bayes, computed from the same catalogue; no held-out information).

## 3. Estimators (arms)

All arms score the same simulated catalogue (paired design, common random numbers).

| Arm | Score `s_i` | Notes |
|---|---|---|
| MEAN (baseline) | `xbar_i` if `n_i >= 1`, else `m` | Simplest baseline and primary comparator |
| SHRINK(kappa) | `(n_i * xbar_i + kappa * m) / (n_i + kappa)` | Bayesian average with `kappa` pseudo-reviews at `m`. `kappa` in {1, 5, 20}; `kappa = 5` is the prespecified primary arm, not tuned |
| LCB | posterior mean minus `z * sqrt(var)` under a Dirichlet(1,...,1) prior on the five star levels (Miller 2014 formula), `z = 1.645` | Lower credible bound; `n_i = 0` gives the prior bound |
| ORACLE (check only) | `theta_i` | Must give Kendall tau-b = 1; not a compared arm |

Ranking: sort by score descending; ties broken by product id ascending. Sorting must be deterministic.

## 4. Hypotheses

- **Primary (EXP-001).** Let `D = tau_b(SHRINK(5)) - tau_b(MEAN)` for one catalogue, and let `Dbar` be the average over the nine EXP-001 cells of the per-cell expected `D`.
  - H0: `Dbar <= 0` (shrinkage does not improve rank recovery over the mean).
  - H1: `Dbar > 0` (directional).
  - Contradiction: the one-sided 95% lower bound of `Dbar` is at or below 0. That outcome is reported as "not supported", and a confidence interval containing 0 is not read as equivalence.
- **Secondary H1b ("when").** `E[D]` decreases as the mean review count `nu` increases (3 > 10 > 30), at every noise level. Contradicted if the per-cell estimates are not ordered this way in the majority of noise levels, or if the 95% intervals of the `nu = 3` and `nu = 30` cells overlap at every noise level.
- **Secondary H1c.** `tau_b(LCB) - tau_b(MEAN) > 0`, pooled as for H1.
- **Exploratory H2 (EXP-002), nondirectional.** The advantage `D` differs between reporting selection `lambda = 2` and `lambda = 0`, and between exposure coupling levels `gamma`.

## 5. Metrics

- **Primary:** Kendall tau-b between scores `s` and true quality `theta` over all `N` products of a catalogue. Range [-1, 1], higher is better. Chosen over top-k precision because it uses the whole ranking, it is defined for every catalogue, and it is less discrete for `N = 200`.
- **Secondary:**
  - Spearman rho between `s` and `theta`.
  - Precision at 10: `|top10(s) ∩ top10(theta)| / 10`.
  - Regret at 10 (stars): mean `theta` of the true top 10 minus mean `theta` of the arm's top 10; non-negative, lower is better.
  - Calibration: empirical coverage of nominal two-sided 90% intervals for `theta_i` among products with `n_i >= 2`. MEAN uses `xbar_i +/- 1.645 * s_pool / sqrt(n_i)`; SHRINK uses `post_mean +/- 1.645 * s_pool / sqrt(n_i + kappa)`; LCB uses the Dirichlet posterior mean `+/- 1.645 * sqrt(var)`. `s_pool` is the pooled within-product standard deviation. Report coverage and `|coverage - 0.90|`.
  - RMSE of `s` against `theta` (stars).

## 6. Design

- **Experimental unit:** one simulated catalogue (one cell, one seed). Products inside a catalogue are not independent units for inference.
- **Seeds:** 20 seeds per cell (well above the minimum of 5). Seeds derive from `numpy.random.SeedSequence([20261124, exp_number, seed_index])` with separate child streams for quality, counts, ratings and reporting. The quality stream depends only on the seed index, so a given seed shares its latent qualities across cells (common random numbers).
- **Sample-size rationale.** Compute is negligible (planning assumption: under one minute for the full EXP-001 matrix on the M1 Pro; to be measured at smoke). The smallest effect of interest is `Dbar = 0.02` tau units (planning assumption). If the between-catalogue SD of `D` is near 0.05 (planning assumption), 9 cells x 20 seeds give a pooled standard error near 0.004, adequate for that effect. The smoke run measures the SD. If a per-cell 95% half-width exceeds 0.02, the seed count is raised to 50 before the freeze, never after.
- **Uncertainty method.** Per cell: mean paired difference with a 95% percentile bootstrap over seeds (10,000 resamples, fixed bootstrap seed) and a t interval as a cross-check. Pooled `Dbar`: stratified bootstrap resampling seeds within each cell. Report effect sizes (mean difference and paired standardised difference) and full per-seed distributions. Secondary contrasts use Holm correction across H1b, H1c and the other `kappa` values, labelled secondary.
- **Exclusions.** No catalogue is excluded. Products with `n_i = 0` stay in the evaluation with the scoring rule above (sensitivity S1 removes them).
- **Stopping rule.** The matrix is fixed and run in full; no optional stopping or peeking at confirmatory results. A run that raises is recorded and retried once with the same seed. A run that fails twice is reported as failed and never replaced by another seed. If a bug is found after confirmatory runs, the whole affected matrix is rerun and the deviation is dated in `research/decision_log.md`.
- **Held-out data.** There is no tuning. `kappa` and `z` are fixed above. No result of the confirmatory matrix may change them.

## 7. Matrices

- **Smoke matrix (exploratory, before freeze):** `N = 50`, `nu` in {3, 30}, `sigma = 1.0`, `kappa` in {5}, `lambda = 0`, `gamma = 0`, 3 seeds. Purpose: check the pipeline, measure runtime and the SD of `D`. Never used as evidence for H1.
- **Full matrices:** see `research/experiment_registry.csv` and each `research/experiments/EXP-NNN/protocol.md`.
  - EXP-001: `nu` in {3, 10, 30} x `sigma` in {0.5, 1.0, 1.5}; `lambda = 0`, `gamma = 0`; arms MEAN, SHRINK(1, 5, 20), LCB; 9 cells x 20 seeds = 180 catalogues.
  - EXP-002: `lambda` in {0, 2} x `gamma` in {-0.5, 0, 0.5} x `nu` in {3, 10}; `sigma = 1.0`; same arms; 12 cells x 20 seeds = 240 catalogues.
  - EXP-003: sensitivity analyses S1 to S4 on regenerated EXP-001 and EXP-002 catalogues (same seeds).

## 8. Sensitivity analyses that could invalidate the main interpretation

The main interpretation of a positive `Dbar` would be "accounting for sample size improves rank recovery". These checks could overturn it:

- **S1, zero-review convention.** Recompute all metrics on products with `n_i >= 1`, and separately with `n_i >= 5`. If the advantage disappears with `n_i >= 1`, it is an artefact of how zero-review products are scored, not of uncertainty awareness.
- **S2, prior misspecification.** Shrink towards `m + 0.5` and `m - 0.5` instead of `m`.
- **S3, definition of truth under selection.** In EXP-002 catalogues, compare rankings against the full-population `theta_i` and against the expected reported rating `theta_rep_i`. If the winner depends on the definition, conclusions are restricted to the stated definition.
- **S4, quality distribution.** Replace Beta(4, 2) by Beta(1, 1) and by a two-component mixture. If the advantage reverses, it depends on the prior matching the population.

## 9. Confounders and competing explanations

- Zero-review imputation (S1).
- Agreement between the prior family and the generating distribution (S4).
- Exposure correlated with quality (`gamma`), which changes which products are data-poor.
- Ties in MEAN scores at small `n`, handled identically by tau-b and by the fixed tie-break.
- Rounding and clipping at the scale ends, which compress `theta` near 1 and 5.

## 10. Compute budget and provenance

Local CPU only (Apple M1 Pro). Fixed budget: each full matrix must run in under 30 minutes; if it does not, the matrix is reduced before the freeze. Each run records: config and its SHA-256, seed, git revision, package versions, OS, CPU, start and end time, runtime and peak memory where feasible, into `run_manifest.json`. Results follow a versioned JSON schema validated at export.

## 11. Claims boundary

All findings are simulated and hold only under the model above. Real product quality is unobserved. Nothing here labels any review as fraudulent, and nothing here describes the internals of any commercial platform.

## 12. Feasibility audit (M0, 2026-11-24)

Commands and actual outputs are in `progress.md`, entry 2026-11-24.

| Item | Observed |
|---|---|
| CPU | Apple M1 Pro, `hw.ncpu` 10 |
| RAM | 17179869184 bytes (16 GiB) |
| OS | macOS 15.3.1 (24D70) |
| Free disk | 128 GiB available on the data volume (`df -h`) |
| Python | 3.12.1 at `/usr/local/bin/python3` |
| uv | 0.9.5 |
| typst (Python package) | 0.15.0, with pypdf 6.20.0 and pillow 11.3.0, in `/Users/bechir/research/labs/.tools/py` |
| pandoc | 3.6.3 at `/Users/bechir/research/labs/.tools/pandoc` |
| Node | v22.23.3 at `/Users/bechir/research/helix/.tools/node/bin` (read-only use) |
| git | 2.42.1 |
| TeX | none installed |

- **Time budget.** Five focused days (planning estimate). The simulation is small; the main time cost is reporting and the demo.
- **Money.** Zero. No paid service is needed.
- **Toolchain decision (D-002).** No TeX: PDFs via pandoc to Typst, compiled with the `typst` Python package; `manuscript.tex` generated from Markdown by pandoc. A toolchain smoke check succeeded (exploratory, see `progress.md`).
- **Data.** Primary evidence is synthetic. Candidate real datasets and their rights are in `data/manifest.json`; none is used or downloaded at M0.
- **Fallback.** If any real dataset stays unclear, the project remains fully synthetic, which already meets the minimum viable release.
- **Exclusions.** No human participants, no scraping, no personal data, no claims about real platforms.
