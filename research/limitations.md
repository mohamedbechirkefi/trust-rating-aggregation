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
