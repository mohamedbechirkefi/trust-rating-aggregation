<!-- SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0 -->
<!-- Draft for Medium (master prompt section 8). Not published. Every number is copied from research/paper/manuscript.md. Repository and demo links filled on 2026-11-26 (owner, 2026-11-26, decision sheet). -->

# Does a Bayesian average rank products better than the star average? In a simulation, it depends on rating noise

*By Mohamed Bechir Kefi, independent researcher.*

*Draft. Status: independent research manuscript / preprint draft, not peer-reviewed. All results are simulated and say nothing about any real platform, product or review.*

A product with one five-star review sits above a product with hundreds of reviews averaging 4.8. Anyone who has sorted a catalogue by average rating has seen this, and practitioner guides have long recommended two fixes: a Bayesian average, which adds a few pseudo-reviews at the catalogue mean, and a lower bound that pushes uncertain products down.

These fixes are standard, and this project does not propose a new one. It asks a narrower question: when do they actually improve the order of products, measured against a known truth, and how much does that depend on the assumptions they rest on?

## The question

TRUST asks: when do average ratings misrank products compared with uncertainty-aware estimators?

Real product quality cannot be observed, so the study uses a simulation in which it is known by construction. Each catalogue has 200 products with a latent quality. Ratings are that quality plus noise, rounded and clipped to one to five stars. Review counts are sparse and skewed, so many products have no review at all, and two variants add reporting selection (moderate ratings are under-reported) and exposure that depends on quality. Two simulation parameters, the shape of the quality distribution and the dispersion of review counts, were calibrated on MovieLens 1M, which is used for calibration only and not redistributed.

## The estimators

- **MEAN**, the arithmetic mean of a product's ratings (the baseline);
- **SHRINK_5**, a Bayesian average with five pseudo-reviews at the catalogue mean (the primary arm), with variants using one and twenty pseudo-reviews;
- **LCB**, a Dirichlet lower credible bound in the style of Evan Miller's star-rating formula, with its prior centred on the catalogue mean.

Rank recovery is measured by Kendall tau-b between each estimator's order and the true order. The main quantity is the difference in tau-b between SHRINK_5 and MEAN on the same catalogue.

## How it was tested

The owner froze the protocol, with file hashes, before any confirmatory run. The primary experiment crossed three mean review counts with three rating-noise levels (0.5, 1.0 and 1.5 stars), with 20 seeds per cell. A second experiment varied reporting selection and exposure, and a third ran four prespecified sensitivity analyses designed to invalidate the main interpretation if it was fragile. In total 1,560 runs executed and none failed. Every arm scored the same simulated catalogue, so every comparison is paired, and intervals are 95% stratified bootstrap intervals over seeds.

## What was measured

**The pooled result is small and positive.** Averaged over the nine cells of the primary experiment, SHRINK_5 beat MEAN by 0.0046 in tau-b (95% interval 0.0030 to 0.0061). The one-sided lower bound, 0.0032, is above zero, so the frozen rule declares the primary hypothesis supported.

**The sign depends on rating noise.** By noise level, the difference is -0.0198 (-0.0225 to -0.0172) at 0.5 stars, 0.0085 (0.0056 to 0.0113) at 1.0 and 0.0250 (0.0224 to 0.0277) at 1.5. When individual ratings are precise, shrinking towards the middle moves genuinely good and bad products to the wrong place; when they are noisy, the reduction in variance wins. The pooled positive value is an equal-weight average over three noise levels, two of which favour shrinkage; a grid weighted towards precise ratings would give a negative average. The informative statement is the conditional one.

*Figure 1 (alt text): A dot-and-interval chart of SHRINK_5 minus MEAN in Kendall tau-b for the nine cells of the primary experiment (20 seeds each), the three noise-level means and the pooled estimate. The three sigma 0.5 cells and their mean lie left of zero; the sigma 1.0 and 1.5 rows lie right of zero; the pooled value sits just right of zero at 0.0046. Bars are two-sided 95% stratified bootstrap intervals. Simulated. Source: FIG-001 in the manuscript and the TRUST demo, `docs/demo.png`.*

## The negative findings

- **The predicted decline with review count was contradicted.** The protocol predicted that the advantage would fade as reviews accumulate; it did not.
- **The lower bound ranked whole lists worse than the mean.** LCB minus MEAN was -0.0647 (-0.0689 to -0.0604), negative at every noise level. It penalises uncertainty, so it pushes data-poor products down regardless of their quality.
- **Shrinkage strength matters.** One pseudo-review gained modestly (0.0075, 0.0066 to 0.0082); twenty pseudo-reviews lost (-0.0125, -0.0143 to -0.0106).
- **The advantage is fragile.** Two of the four sensitivity analyses met their invalidation criteria. Moving the shrinkage centre by half a star in either direction gave pooled differences of -0.0406 and -0.0485, and a uniform or bimodal quality population gave -0.0210 and -0.0265. These losses are several times larger in magnitude than the reference gain of 0.0046.
- **Reporting selection showed no detected average effect** on the SHRINK_5 advantage (-0.0001, -0.0015 to 0.0012), which is not the same as showing equivalence.

One sensitivity check supported the result: restricting the metric to products with at least one review gave 0.0068 (0.0041 to 0.0094), so the advantage is not an artefact of scoring unreviewed products. It vanished among products with at least five reviews (-0.0005, -0.0019 to 0.0011), so it lives among products with one to four reviews.

## Limitations

- Everything is simulated. True quality is defined by the model, and no result transfers to real catalogues without further evidence.
- Results depend on the model: the quality distribution, the rounding and clipping rating model, the review-count distribution and the stylised selection and exposure functions. Herding, manipulation and rater heterogeneity are not modelled.
- The calibration comes from movie ratings with many more ratings per item than the 3 to 30 used here, and the single-noise model misfits held-out star shares.
- The pooled estimand weights three noise levels equally, and its sign depends on that choice.
- The effects are small in tau-b units; top-of-list relevance was examined only in secondary and exploratory metrics.
- The noise dependence was already visible in exploratory pilots before the freeze, so it is a confirmatory replication of a pattern seen in pilots, not a blind prediction.

## Reproducibility

The protocols, freeze record, configurations, raw results with checksums, experiment reports, manuscript (independent research manuscript / preprint draft, not peer-reviewed) and an offline interactive demo are in the project repository: <https://github.com/mohamedbechirkefi/trust-rating-aggregation>. Demo: <https://trust-rating-aggregation.kefimohamedbechir.workers.dev>.

*The study was carried out with an AI system used as a research and development assistant under the author's direction; the AI system is not an author.*
