<!-- SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0 -->
# Limitations (living document)

Status at M0, 2026-11-24: no experiment has been run, so these are anticipated limitations of the design, not findings.

1. **Simulation only.** True quality is defined by the model. Real product quality is unobserved, so no result transfers to real platforms without further evidence.
2. **Model dependence.** Results depend on the latent quality distribution, the rounding and clipping rating model, the negative binomial review counts and the selection function. EXP-003 probes some of these, not all.
3. **Selection model is stylised.** The under-reporting function is motivated by Hu, Pavlou and Zhang, but its form and parameter values are assumptions, not estimates.
4. **No herding or social influence.** Ratings are independent given quality. Herding effects (for example Muchnik, Aral and Taylor 2013) are not modelled.
5. **No manipulation model.** Nothing in this project detects or labels fraudulent reviews, and no result may be read that way.
6. **Single primary metric.** Kendall tau-b weighs all rank pairs equally; users mainly see the top of a list. Precision and regret at 10 are reported as secondary metrics for that reason.
7. **Estimator scope.** Three estimator families with fixed parameters; no learned or platform-specific ranking.
8. **Exploratory versus confirmatory.** Until the owner freezes the protocol, any result is exploratory.
9. **Toolchain.** `manuscript.tex` is generated but not compiled locally (no TeX distribution).

## Calibration on MovieLens 1M (added 2026-11-24, protocol section 13)

- The review-count dispersion and the quality distribution come from movie ratings, not product reviews; their transfer to product catalogues is an assumption.
- The dispersion was fitted at a mean of about 252 ratings per movie and is applied at mean counts of 3 to 30, assuming the relative heterogeneity of exposure does not depend on the mean.
- The single-noise ordered-probit model misfits the star shares of held-out movies (1-star and 4-star under-predicted, 2-star and 5-star over-predicted; JRN-0005). User leniency is folded into the noise term.

## After the confirmatory runs (M3, 2026-11-25)

- **Direction depends on noise.** Shrinkage ranks worse than the mean at sigma 0.5 and better at sigma 1.0 and 1.5 (EXP-001). The pooled `Dbar > 0` reflects the equal weighting of this grid and must not be read as a uniform effect.
- **Fragile to the prior.** Moving the shrinkage centre by 0.5 stars (S2) or changing the quality distribution (S4) reverses the sign of `Dbar`. The positive result holds only when the prior centre and population shape match the generator.
- **S3 is non-diagnostic for rank metrics.** `theta_rep` is a monotone transform of `mu`, so the two truth definitions give identical rankings (D-012).
- **Small effect.** `Dbar` is 0.0046 tau-b units, small next to the per-cell tau-b of the arms (`results/confirmatory/EXP-001/report.md`); top-of-list metrics were secondary and untested.
- **Holm p-value method** was fixed at M3 before data (D-011), not in the frozen text.
- **Owner-accepted deviations (D-013).** D-011 (bootstrap p-values for the Holm families) and D-012 (S3 non-diagnostic for rank metrics) were accepted by the owner on 2026-11-25 ("approve all recommendations, RIGGED A") and are disclosed wherever the affected results appear.

## After interpretation and the evidence audit (M4, 2026-11-25)

- **Noise dependence seen before the freeze.** The sign change by noise was observed in exploratory pilots under the planning generator (`research/freeze.json`, C4) and motivated amendment A-2. The confirmatory result replicates it; it was not predicted blind.
- **H1b pattern partly a dilution effect.** The increase of `D` with `nu` at sigma 1.5 largely disappears among reviewed products (exploratory E3, JRN-0010). Unreviewed products are tied under both arms and dilute `D` most where they are most common.
- **H1c is about whole-list recovery.** On top-of-list metrics the centred LCB beats MEAN at sigma 1.5 in an exploratory check (E1); that check has 30 uncorrected intervals and is a hypothesis, not a finding.
- **EXP-002 cannot separate selection from sample size** at sigma 1.0, where `D` barely depends on `nu`.
- **Rounding and clipping near the scale ends** are not separated from population shape by any registered or exploratory analysis.
- **Pooled estimand depends on grid weights.** The positive `Dbar` would turn negative under a grid weighted towards precise ratings.
- **Citations.** efron1975 was read on its first page only, hu2007wp and li2008 on their abstracts only, and harper2015 is metadata only; the manuscript cites them for nothing beyond that.
