<!-- SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0 -->
# Second review pass: arguing against the preferred hypothesis

**Date:** 2026-11-25. **Reviewer:** the AI assistant, in the M4 session, after the first full draft of `research/paper/manuscript.md`. This is internal quality control, not peer review; the owner has not yet reviewed it. **Preferred hypothesis under challenge:** H1, "accounting for sample size (SHRINK_5) improves rank recovery over the mean", and the manuscript's reading of it.

The pass looks for the strongest alternative readings, overgeneralisation, stale figures, leakage and missing failed runs. Each item says whether the challenge holds and what changed.

## 1. Strongest alternative readings

| # | Challenge | Holds? | Evidence | Change made |
|---|---|---|---|---|
| A1 | "H1 supported" is a grid artefact: the pooled value is positive only because two of three noise levels favour shrinkage | Yes | `D_sigma` -0.0198, 0.0085, 0.0250; equal weights by design | Already stated in the draft; the abstract's last sentence was rewritten so the positive average is not presented as a general finding (see A2) |
| A2 | "Shrinkage helps ranking **only when** ratings are noisy and the prior matches" claims necessity from three noise levels and two alternative populations | Yes | S2 and S4 test single points; three sigma levels | Abstract now says "in the conditions tested, shrinkage helped ... and hurt it otherwise" |
| A3 | The low-noise loss is a tie artefact: tau-b leaves tied MEAN pairs out, while SHRINK_5 breaks those ties by review count, which is uninformative at `gamma = 0` | No | E2: tie shares depend on `nu`, not sigma; E1: the low-noise loss also appears in RMSE, which has no ties (-0.0281, -0.0338 to -0.0223) | Discussion now names RMSE as the tie-free check and labels the multi-metric evidence exploratory |
| A4 | The noise dependence was not predicted blind: pilots showed it before the freeze | Yes | `research/freeze.json` C4; amendment A-2 was motivated by it | Methods 4.4 and Limitations state that the confirmatory result replicates a pattern seen in pilots |
| A5 | The H1b "reversal" at sigma 1.5 is a measurement artefact of evaluating on all products, including unreviewed ones tied under both arms | Largely | E3: among reviewed products `D` at sigma 1.5 is 0.0426, 0.0414, 0.0405 | Results 5.4 and the EXP-001 report addendum qualify the M3 sentence; E3 is phrased as an interpretation over different product subsets, not a decomposition |
| A6 | "The advantage is confined to products with one to four reviews" overreads S1: evaluating on `n >= 5` removes pairs, it does not localise gains | Yes | S1 `n >= 5` is -0.0005 (-0.0019 to 0.0011) | Discussion rephrased to "arises from orderings that involve products with fewer than five reviews", with the `nu` reading marked untested |
| A7 | H1c's failure says nothing about LCB's purpose, which is to protect the top of the list | Partly | E1: LCB better at sigma 1.5 on precision and regret at 10, worse on whole-list metrics everywhere | Manuscript and CLM-004 restrict the statement to whole-list recovery; the top-of-list gain is labelled a hypothesis (CLM-014) |
| A8 | The favourable exploratory rows are cherry-picked from many intervals | Possible | E1 has 30 uncorrected intervals | Section 5.4 now says isolated favourable rows are hypotheses for a registered follow-up |
| A9 | The null lambda effect in EXP-002 is uninformative about selection versus sample size | Yes | At sigma 1.0, `D` barely depends on `nu` in EXP-001 | Discussion and the EXP-002 addendum say the experiment cannot separate the two |
| A10 | The bias-variance mechanism is asserted, not tested | Yes | No experiment isolates bias and variance | Kept as "model-dependent reading"; the EXP-001 report no longer attributes it to Efron and Morris |
| A11 | Practical advice ("the choice of centre and strength is at least as consequential") leaves the model | Yes | Simulation only | Rephrased as "within this model" |
| A12 | The MovieLens noise estimate (1.05 stars) suggests real catalogues sit in the favourable regime | Risk of misreading | Fit folds rater heterogeneity into noise; movies, not products | Discussion states it does not locate real catalogues |

## 2. Overgeneralisation and wording

- The title asks "when", and the abstract no longer implies a universal benefit (A1, A2).
- "Set by rating noise" in the abstract was softened to "depends on rating noise"; noise is a manipulated factor, but the dependence is shown only on three levels.
- No sentence refers to real products, platforms or reviews beyond the claims boundary. The ethics section says no review is labelled.

## 3. Stale figures and numbers

- The audit (`research/publication/evidence_audit.md`) recomputed the frozen analysis from the raw results with zero differences, and every table, figure and analysis JSON matches the hash in its generator manifest (20 of 20). FIG-001 to FIG-003 are therefore current.
- Every four-decimal interval printed in the manuscript, supplement, reports, claims register and interpretation note equals a triple in the analysis or exploratory JSON.
- Found stale: the README and the experiment registry still said "not yet run" or "report pending"; both were corrected.

## 4. Leakage

- The calibration fit read only MovieLens counts on the fit split; it computed no estimator or contrast (protocol 13.1, JRN-0005).
- The estimators see only reported counts: the catalogue mean `m` and the LCB prior come from reported ratings (`trust.estimators.summarise`), never from `theta` or `mu`.
- The analysis layer was committed before the confirmatory runs (D-011); no frozen file changed afterwards (12 of 12 freeze hashes match).
- Pre-freeze exposure to the contrast is the one leakage-like issue, and it is disclosed (A4).

## 5. Missing failed runs

- 1,560 of 1,560 planned runs are present in the raw result files, all `ok`; none retried (audit, sample counts).
- Exploratory runs are not hidden: smoke, pilots and metric validation are in `results/exploratory/` and the journal; the M4 checks are JRN-0010. The first M4 exploratory output recorded a dirty tree and was regenerated unchanged at a clean revision (journal).

## 6. Challenges that do not hold

- "The positive result is a zero-review artefact": rejected by S1 (`n >= 1`: 0.0068, 0.0041 to 0.0094).
- "Any compression helps rank metrics": rejected by SHRINK_20 and by S2's shifted centres, which compress as much and lose.

## 7. Residual risks the owner should know

- The headline the frozen rule produces ("H1 supported") is technically correct but easy to misquote; any public text (M5) should lead with the conditional statement.
- Rounding and clipping near the scale ends remain unseparated from population shape.
- The literature review is a scoping search, and the ranking-under-uncertainty literature in statistics was not searched, so no novelty is claimed.
