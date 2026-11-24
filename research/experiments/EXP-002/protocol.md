<!-- SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0 -->
# EXP-002 protocol: reporting selection and quality-dependent missingness

**Status: v1.0, FROZEN 2026-11-24 by the owner (G-FREEZE, round 2), not yet run.** Amended before the freeze (protocol section 13): MovieLens-calibrated base `mu ~ 1 + 4 Beta(4.2726, 3.1944)` and NegBin dispersion 0.4909; LCB prior centred on the catalogue mean (A-1); 20 seeds kept (A-3). Hash in `research/freeze.json` and `research/decision_log.md` D-010. Shared definitions are in `research/protocol.md` sections 2 to 5.

1. **Precise question.** When ratings are selectively reported (extreme ratings more likely to be posted) and the number of reviews depends on quality, does the advantage of SHRINK(5) and LCB over MEAN change?
2. **Mechanism.** Under-reporting of moderate ratings shifts and spreads the observed rating distribution. Quality-dependent exposure changes which products are data-poor: with `gamma > 0` data-poor products tend to be poor products, so shrinking them up towards the catalogue mean may hurt; with `gamma < 0` the reverse.
3. **Rationale from verified sources.** Hu, Pavlou and Zhang (2007 working paper, opened) describe purchasing and under-reporting biases that make the mean a biased estimator of quality and give rise to J-shaped distributions. Li and Hitt (2008, abstract opened) describe self-selection of early reviewers. These motivate the selection model; they do not validate its parameter values.
4. **Competing explanations.** (a) Differences could reflect the definition of truth (full-population versus reported expectation; EXP-003 S3). (b) Lower effective sample size under selection, not selection itself; the realised `n_i` distribution is reported per cell to separate the two.
5. **Hypotheses.** H0: `E[D]` is equal across `lambda` levels and across `gamma` levels. H1 (nondirectional): it differs. `D` is as in EXP-001; the same contrast is reported for LCB.
6. **What would contradict H1.** 95% intervals for the paired difference `E[D | lambda = 2] - E[D | lambda = 0]` (same seed, same `gamma`, same `nu`) containing 0 in every stratum. That outcome is "no detected difference", not equivalence.
7. **Estimand.** `E[D | lambda = 2] - E[D | lambda = 0]` averaged over the six (`gamma`, `nu`) strata; analogous contrasts for `gamma`.
8. **Experimental unit.** One catalogue, `N = 200`.
9. **Simulation scope.** As EXP-001 with `sigma = 1.0` fixed.
10. **Independent variables.** `lambda` in {0, 2}; `gamma` in {-0.5, 0, 0.5}; `nu` in {3, 10} (mean potential raters); arm.
11. **Dependent variables.** Same as EXP-001. Ground truth is the full-population `theta_i`.
12. **Treatment and control.** Arms as EXP-001; MEAN is the baseline. `lambda = 0`, `gamma = 0` is the no-selection control cell.
13. **Sampling and seeds.** 12 cells x 20 seeds = 240 catalogues; `SeedSequence([20261124, 2, seed_index])`; common random numbers across cells for the same seed.
14. **Sample-size rationale.** Same planning logic as EXP-001; difference-in-differences are noisier, so the smoke SD is checked against a half-width of 0.03 for the `lambda` contrast before the freeze.
15. **Fixed compute budget.** Under 30 minutes of local CPU.
16. **Metric formulas and units.** As `research/protocol.md` section 5.
17. **Uncertainty method.** Paired (same-seed) bootstrap across seeds within strata; Holm correction across the `lambda` and two `gamma` contrasts.
18. **Exclusion and stopping rules.** As EXP-001.
19. **Anticipated failure modes.** With `lambda = 2` the reporting probability of moderate ratings falls below 1, so realised counts at `nu = 3` are lower than with `lambda = 0` and many products have no review. The realised count distribution is reported per cell, not corrected.
20. **Sensitivity tests.** EXP-003 S1, S3.
21. **Reproducibility commands (planned).** `uv run python -m trust.cli run --exp EXP-002`; `uv run python -m trust.cli report --exp EXP-002`.
