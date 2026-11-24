<!-- SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0 -->
# EXP-003 protocol: sensitivity analyses that could invalidate the main interpretation

**Status: DRAFT v0.1, 2026-11-24, awaiting owner freeze (G-FREEZE). Not executed.** Depends on the EXP-001 and EXP-002 generators. Shared definitions are in `research/protocol.md`.

1. **Precise question.** Does the EXP-001 conclusion about `D = tau_b(SHRINK(5)) - tau_b(MEAN)` survive changes to the zero-review convention, the prior centre, the definition of truth and the quality distribution?
2. **Mechanism under test.** The interpretation "uncertainty awareness improves rank recovery" predicts an advantage that persists among reviewed products and degrades gracefully under prior misspecification.
3. **Rationale.** Shrinkage gains depend on the prior (Efron and Morris 1975). Miller (2014) notes the method is approximate. The checks target the assumptions that the main result could silently depend on.
4. **Competing explanations targeted.** Zero-review artefact (S1); prior-centre luck (S2); truth-definition dependence (S3); prior-family match (S4).
5. **Analyses (each a prespecified sub-analysis, not a new question).**
   - **S1.** EXP-001 catalogues regenerated with the same seeds; metrics restricted to products with `n_i >= 1`, and to `n_i >= 5`.
   - **S2.** SHRINK(5) towards `m + 0.5` and `m - 0.5` on EXP-001 catalogues.
   - **S3.** EXP-002 catalogues scored against `theta_i` and against `theta_rep_i = E[r | reported]`.
   - **S4.** EXP-001 matrix rerun with `mu ~ 1 + 4 Beta(1, 1)` and with an equal mixture of `1 + 4 Beta(2, 6)` and `1 + 4 Beta(6, 2)`.
6. **What would contradict the main interpretation.** S1 with `n_i >= 1`: pooled `Dbar` interval containing or below 0 while the EXP-001 pooled `Dbar` is positive. S2: sign reversal of `Dbar` under a 0.5-star shift. S3: the sign of `D` differs between truth definitions in a majority of strata. S4: sign reversal under either alternative distribution. Any of these is reported prominently and limits the claim.
7. **Estimand, unit, seeds, uncertainty, stopping.** As EXP-001 for each sub-analysis; 20 seeds per cell; one-sided intervals are not used here, only two-sided 95% stratified bootstrap intervals.
8. **Fixed compute budget.** Under 60 minutes of local CPU in total.
9. **Anticipated failure modes.** `n_i >= 5` leaves few products at `nu = 3` (counts reported; cells with fewer than 20 qualifying products per catalogue are flagged, not dropped).
10. **Reproducibility commands (planned).** `uv run python -m trust.cli run --exp EXP-003`; `uv run python -m trust.cli report --exp EXP-003`.
