<!-- SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0 -->
# M4 interpretation: confounders, sensitivity, expected versus observed

**Date:** 2026-11-25. **Milestone:** M4. **Status:** interpretation of the frozen confirmatory results of EXP-001 to EXP-003, plus three exploratory checks (JRN-0010). All numbers are simulated and hold only under the model of `research/protocol.md`. Real product quality is unobserved.

Sources of every number: the generated tables `research/experiments/EXP-00N/results_tables.md`, the frozen analysis `results/confirmatory/analysis/EXP-00N.json`, and, for the rows labelled exploratory, `results/exploratory/m4-sensitivity/m4_exploratory.md` (generator `scripts/m4_exploratory.py`, clean revision `4a2b478`). No exploratory value changes or replaces a frozen verdict.

## 1. Exploratory checks run at M4 (JRN-0010)

| Id | What | Input | Cost |
|---|---|---|---|
| E1 | SHRINK_5 and LCB minus MEAN on all five metrics (tau-b, Spearman, precision at 10, regret at 10, RMSE), pooled and per noise level | committed `results/confirmatory/EXP-001/results.json` | under 1 s |
| E2 | Share of products and pairs tied under MEAN and SHRINK_5, and share of products with one review, per EXP-001 cell | the 180 frozen EXP-001 catalogues regenerated read-only from the frozen config and seeds | under 1 s |
| E3 | Per-cell `D` among products with at least one review | committed `results/confirmatory/EXP-003-S1-min1/results.json` | under 1 s |

E2 recomputed the tau-b of MEAN and SHRINK_5 in all 180 regenerated catalogues; the largest absolute difference from the committed values is 0, so the regeneration reproduces the confirmatory catalogues exactly.

## 2. Competing explanations, conclusion by conclusion

The competing explanations below are those named in `research/protocol.md` section 9 and in the three EXP protocols (item 4 of each).

### C1. EXP-001: H1 supported under the frozen rule; the direction depends on noise

`Dbar = 0.0046` (0.0030 to 0.0061); `D_sigma` -0.0198, 0.0085, 0.0250 at sigma 0.5, 1.0, 1.5.

| Competing explanation (source) | Addressed by | What the evidence says |
|---|---|---|
| Advantage only from scoring zero-review products (protocol 9; EXP-001 item 4a) | EXP-003 S1 (confirmatory) | Not the source: among products with at least one review `Dbar = 0.0068` (0.0041 to 0.0094), larger than the reference. With at least five reviews it is -0.0005 (-0.0019 to 0.0011): the effect lives among products with one to four reviews |
| Prior family matching the generator (protocol 9; EXP-001 item 4b) | EXP-003 S4 (confirmatory) | Confirmed as a real dependence: under Beta(1, 1) and under the two-component mixture `Dbar` reverses to -0.0210 and -0.0265 |
| Prior centre luck | EXP-003 S2 (confirmatory) | Confirmed as a real dependence: a 0.5-star shift of the centre gives -0.0406 and -0.0485 |
| Rank metrics favour any estimator that compresses low-count items (EXP-001 item 4c) | EXP-001 secondary arms; EXP-003 S2 (confirmatory) | Rejected as a sufficient explanation: stronger compression (SHRINK_20, -0.0125) and compression towards a wrong centre (S2) both lose. The gain needs moderate strength and the right target |
| The conclusion is specific to Kendall tau-b (construct) | E1 (exploratory) | Not specific: the same sign pattern holds on Spearman, precision at 10, regret at 10 and RMSE. At sigma 0.5 SHRINK_5 is worse than MEAN on all five metrics; at sigma 1.0 and 1.5 it is better on all five |
| Ties in MEAN scores at small `n` (protocol 9) | E2 (exploratory) | Cannot explain the noise dependence: the share of products tied under MEAN depends on `nu` (about 0.85, 0.67 and 0.45 at `nu` 3, 10, 30) but barely on sigma (0.857, 0.847, 0.849 at `nu = 3`), while the sign of `D` is set by sigma. Ties may still affect the level of `D` |
| Rounding and clipping compress `theta` near 1 and 5 (protocol 9) | not addressed | Not separable from the prior shape in the registered design: S4's Beta(1, 1) puts more products near the ends and also changes the population. Disclosed as open |
| Exploratory pilots informed the amendment A-2 (freeze record, C4 disclosure) | design history | The noise-dependent sign was seen in pilots under the planning generator before the freeze. The confirmatory result therefore replicates a pattern that motivated the reporting rule; it is not an independent prediction made blind to it |

**Change to the conclusion.** None to the frozen verdict. The interpretation is strengthened in one direction and narrowed in another: the noise dependence is not a tau-b or tie artefact (E1, E2), but the positive pooled value remains a property of an equally weighted noise grid and of a correctly specified shrinkage target and population.

### C2. EXP-001: H1b contradicted

| Competing explanation | Addressed by | What the evidence says |
|---|---|---|
| Dilution by zero-review products, which are tied under both arms and are more common at small `nu` (0.381, 0.220, 0.132 at `nu` 3, 10, 30) | E3 (exploratory) | Supported. Among reviewed products, at sigma 1.5 `D` is 0.0426, 0.0414 and 0.0405 at `nu` 3, 10, 30: flat, not increasing. The EXP-001 increase with `nu` at sigma 1.5 (0.0183, 0.0260, 0.0309) is largely explained by dilution. At sigma 0.5 and 1.0 no ordering appears and the intervals overlap |

**Change to the conclusion.** The frozen verdict (contradicted) stands. The M3 sentence "at sigma 1.5 the advantage grows with `nu`, the opposite of the hypothesised direction" is qualified: that pattern is mostly dilution, and among reviewed products the data show no clear dependence on `nu` in either direction.

### C3. EXP-001: H1c not supported (centred LCB worse than MEAN on tau-b)

| Competing explanation | Addressed by | What the evidence says |
|---|---|---|
| Estimand mismatch: LCB deliberately ranks uncertain products low, so it is not designed to recover the whole order of expected ratings | E1 (exploratory) | Supported in part. LCB is worse than MEAN on tau-b, Spearman and RMSE at every noise level, but on the top-of-list metrics it is better at sigma 1.5 (precision at 10 +0.1067, 0.0717 to 0.1417; regret at 10 lower by 0.2245 stars, 0.1947 to 0.2540) and its pooled regret at 10 is lower than MEAN's by 0.0888 stars (0.0732 to 0.1045). At sigma 0.5 it is worse on every metric |
| One LCB variant only (z 1.645, prior strength 5, centred) | not addressed | Disclosed: the verdict concerns this variant |

**Change to the conclusion.** The frozen verdict stands for whole-list rank recovery. The manuscript does not say "LCB ranks worse than the mean" without the metric: on top-10 regret, an exploratory check finds the opposite at sigma 1.0 and 1.5.

### C4. EXP-001 secondary: SHRINK_1 better, SHRINK_20 worse

No competing explanation is named for these contrasts. They support the reading that shrinkage strength matters: SHRINK_20 shows the same sign pattern by noise as SHRINK_5 with larger losses at sigma 0.5 (-0.0478), and SHRINK_1 is null at sigma 0.5 (-0.0001, -0.0017 to 0.0014). Unchanged.

### C5. EXP-002: reporting selection does not change `D` on average

| Competing explanation (EXP-002 item 4) | Addressed by | What the evidence says |
|---|---|---|
| (a) Definition of truth (full population versus reported expectation) | EXP-003 S3 (confirmatory) | Not addressed: S3 is non-diagnostic for rank metrics by construction (D-012, owner-accepted D-013) |
| (b) Lower effective sample size, not selection itself | realised counts; EXP-001 | Cannot be separated. `lambda = 2` cut mean reported counts by about a third (for example 9.92 to 6.32 at `nu = 10`, `gamma = 0`), but at sigma 1.0 `D` depends only weakly on `nu` in EXP-001 (0.0078, 0.0069, 0.0107). A null lambda contrast is therefore expected under either reading, and the experiment cannot tell them apart at sigma 1.0 |

**Change to the conclusion.** Unchanged verdict ("no detected average difference; frozen per-stratum rule not met"), with an added caveat: at sigma 1.0 the design has little power to detect a sample-size-mediated effect.

### C6. EXP-002: quality-dependent exposure lowers `D` in both directions

| Competing explanation | Addressed by | What the evidence says |
|---|---|---|
| Exposure coupling changes which products are data-poor (protocol 9) | the experiment itself | This is the mechanism under test; the protocol's directional prediction (gamma > 0 hurts, gamma < 0 helps) is not borne out for SHRINK_5, while LCB follows it |
| Interaction with noise | not addressed | EXP-002 ran at sigma 1.0 only; given C1, the gamma effects may differ at other noise levels |

Unchanged.

### C7. EXP-003: S1 not invalidating; S2 and S4 invalidating; S3 vacuous

Covered under C1. The S2 and S4 reversals are the main limit on C1. S3 provides no evidence (D-012).

## 3. Expected versus observed (all experiments)

| Experiment | Hypothesis or check | Prediction (frozen) | Observation | Verdict under the frozen rule |
|---|---|---|---|---|
| EXP-001 | H1 | `Dbar > 0`; one-sided 95% lower bound above 0 | `Dbar = 0.0046` (0.0030 to 0.0061), lower bound 0.0032 | supported; direction depends on noise (A-2) |
| EXP-001 | A-2 per noise level | report `D_sigma`; if intervals exclude 0 with opposite signs, state "direction depends on the noise level" | -0.0198, 0.0085, 0.0250 at sigma 0.5, 1.0, 1.5, all excluding 0 | direction depends on the noise level |
| EXP-001 | H1b | `E[D]` decreases with `nu` at every noise level | ordered at 1 of 3 levels; at sigma 1.5 increasing (largely dilution, E3) | contradicted |
| EXP-001 | H1c | LCB minus MEAN > 0 | -0.0647 (-0.0689 to -0.0604), Holm-adjusted p 1.0000 | not supported |
| EXP-001 | Secondary SHRINK_1, SHRINK_20 | > 0 (directional family) | SHRINK_1 0.0075 (0.0066 to 0.0082), Holm p 0.0004; SHRINK_20 -0.0125 (-0.0143 to -0.0106) | SHRINK_1 rejects H0; SHRINK_20 does not |
| EXP-002 | H2 lambda | `E[D]` differs between `lambda` 2 and 0 | average -0.0001 (-0.0015 to 0.0012), Holm p 0.8859; 2 of 6 strata exclude 0, in opposite directions | contradiction rule not met; no detected average difference |
| EXP-002 | H2 gamma | `E[D]` differs across `gamma`; mechanism predicted opposite directions | -0.0112 and -0.0091 for gamma -0.5 and 0.5 against 0, both Holm p 0.0006 | difference detected; mechanism's directions not borne out for SHRINK_5 |
| EXP-003 | S1 (n >= 1) | invalidates if the interval contains or falls below 0 | 0.0068 (0.0041 to 0.0094) | not invalidating |
| EXP-003 | S2 (centre m +/- 0.5) | invalidates on sign reversal | -0.0406 and -0.0485 | invalidation criterion met |
| EXP-003 | S3 (truth definition) | invalidates if signs differ in a majority of cells | 0 of 12, by construction (D-012) | criterion not met, vacuously; non-diagnostic |
| EXP-003 | S4 (quality distribution) | invalidates on sign reversal | -0.0210 and -0.0265 | invalidation criterion met |

## 4. What remains open

- Rounding and clipping near the scale ends, separated from population shape.
- Whether the noise dependence holds under quality-dependent exposure and selection (EXP-002 ran only at sigma 1.0).
- A value-based truth-definition check (S3 as registered cannot discriminate).
- A map over intermediate prior shifts and population shapes (S2 and S4 test single points).

Each would be a new EXP id with the owner's approval.
