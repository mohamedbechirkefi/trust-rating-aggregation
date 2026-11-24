<!-- SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0 -->
# EXP-001 protocol: mean versus uncertainty-aware ranking under random reporting

**Status: v1.0, FROZEN 2026-11-24 by the owner (G-FREEZE, round 2), not yet run.** Amended before the freeze (protocol section 13): MovieLens-calibrated base `mu ~ 1 + 4 Beta(4.2726, 3.1944)` and NegBin dispersion 0.4909 (item 9 below reads accordingly); LCB prior centred on the catalogue mean (A-1, so H1c concerns the centred arm); `D_sigma` reported per noise level next to `Dbar` (A-2); 20 seeds kept and the measured SD 0.0064 to 0.0128 replaces the 0.05 planning value (A-3, A-4). Hash in `research/freeze.json` and `research/decision_log.md` D-010. Shared definitions (model, arms, metrics) are in `research/protocol.md` sections 2 to 5; this file states what is specific to EXP-001.

1. **Precise question.** With no reporting selection and exposure independent of quality, does ranking by Bayesian shrinkage (`kappa = 5`) recover the true quality order better than ranking by the arithmetic mean, and how does the gap depend on review count and rating noise?
2. **Mechanism.** The mean of `n` noisy ratings has variance proportional to `sigma^2 / n`. Products with few reviews therefore reach extreme means by chance and occupy the top and bottom of a mean ranking. Shrinkage pulls those means towards the catalogue mean in proportion to `kappa / (n + kappa)`.
3. **Rationale from verified sources.** Efron and Morris (1975) show that Stein-type shrinkage reduces total squared error over the separate means. Miller (2009, 2014) argues that sorting by a raw average promotes items with few ratings and proposes lower bounds (Wilson interval; Dirichlet posterior). These sources support the mechanism, not the size of the effect in this model. See `research/literature_review.md`.
4. **Competing explanations.** (a) An advantage could come only from zero-review scoring (tested by EXP-003 S1). (b) It could depend on the prior family matching the base quality distribution (EXP-003 S4). (c) Rank metrics may favour any estimator that compresses low-count items, whatever their quality.
5. **Hypotheses.** H0: `Dbar <= 0`; H1: `Dbar > 0`, with `D = tau_b(SHRINK(5)) - tau_b(MEAN)` and `Dbar` the equal-weight average over the 9 cells. Secondary H1b: `E[D]` decreases with `nu`. Secondary H1c: `tau_b(LCB) - tau_b(MEAN) > 0`.
6. **What would contradict H1.** A one-sided 95% stratified-bootstrap lower bound of `Dbar` at or below 0. An interval containing 0 is "not supported", not "equivalent".
7. **Estimand.** `Dbar = (1/9) * sum_c E_seed[D_c]` over the simulation population defined below.
8. **Experimental unit.** One catalogue of `N = 200` products (one cell, one seed).
9. **Simulation scope.** `mu ~ 1 + 4 Beta(4.2726, 3.1944)` (MovieLens fit; planning value Beta(4, 2)); `lambda = 0`; `gamma = 0`; NegBin dispersion 0.4909 (MovieLens fit; planning value 1).
10. **Independent variables.** `nu` in {3, 10, 30}; `sigma` in {0.5, 1.0, 1.5} stars; estimator arm; `kappa` in {1, 5, 20} for SHRINK.
11. **Dependent variables.** Kendall tau-b (primary); Spearman rho, precision at 10, regret at 10 (stars), 90% interval coverage, RMSE (stars).
12. **Treatment and control.** Treatment: SHRINK(5) (primary), LCB and SHRINK(1), SHRINK(20) (secondary). Control and baseline: MEAN. ORACLE is a correctness check only.
13. **Sampling and seeds.** 20 seeds per cell; `SeedSequence([20261124, 1, seed_index])`; quality stream shared across cells for the same seed.
14. **Sample-size rationale.** See `research/protocol.md` section 6. 180 catalogues. Measured per-seed SD 0.0064 to 0.0128 (JRN-0003); 20 seeds kept (protocol section 13.2 A-4).
15. **Fixed compute budget.** Under 30 minutes of local CPU for the full matrix.
16. **Metric formulas and units.** As in `research/protocol.md` section 5. Tau-b and rho are unitless; regret and RMSE are in stars; precision and coverage are proportions.
17. **Uncertainty method.** Paired differences per seed; per-cell 95% percentile bootstrap (10,000 resamples) with t-interval cross-check; pooled stratified bootstrap; Holm correction across secondary contrasts.
18. **Exclusion and stopping rules.** No exclusions. Full matrix, no optional stopping; one retry per failed run with the same seed; persistent failures reported, never replaced.
19. **Anticipated failure modes.** Ties at small `n` inflating or deflating tau-b; NegBin draws of zero for most products at `nu = 3` (expected share of zero-review products to be reported); floating-point differences across platforms in tau-b at the 1e-12 level.
20. **Sensitivity tests.** EXP-003 S1, S2, S4 apply to these catalogues.
21. **Reproducibility commands (planned, not yet implemented).** `uv sync --frozen`; `uv run python -m trust.cli smoke`; `uv run python -m trust.cli run --exp EXP-001`; `uv run python -m trust.cli report --exp EXP-001`; `uv run pytest`.
