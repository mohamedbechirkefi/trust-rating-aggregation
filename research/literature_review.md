<!-- SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0 -->
# Literature review (M0 scoping, not systematic)

Status: initial scoping search on 2026-11-24 with web search and page fetches. This is not a systematic review; no systematic protocol was followed. "Opened" means the page or PDF was fetched and the stated content was read in this session. "Metadata only" means bibliographic details were confirmed from an index page but the full text was not read. "Unverified" means seen only in search results.

## 1. Sources

| Key | Reference | Access | What it supports here |
|---|---|---|---|
| miller2009 | E. Miller, "How Not To Sort By Average Rating", 2009-02-06 (updated 2012, 2016). https://www.evanmiller.org/how-not-to-sort-by-average-rating.html | Opened 2026-11-24 | Sorting by average favours items with few ratings; proposes the Wilson score lower bound for binary ratings |
| miller2014 | E. Miller, "Ranking Items With Star Ratings", 2014-09-16 (update 2015-07-13). https://www.evanmiller.org/ranking-items-with-star-ratings.html | Opened 2026-11-24; re-opened 2026-11-25 (M4 audit) | Dirichlet posterior over star levels with uniform prior; sort by posterior mean minus `z * sqrt(var)`, described as the lower bound of a normal approximation to a Bayesian credible interval; the author states the method "is not exact". Basis of the LCB arm |
| miller2012 | E. Miller, "Bayesian Average Ratings", 2012-11-06. https://evanmiller.org/bayesian-average-ratings.html | Opened 2026-11-24 | Loss-function view: ranking criterion from an asymmetric loss; designer controls risk attitude |
| efron1975 | B. Efron and C. Morris, "Data Analysis Using Stein's Estimator and its Generalizations", JASA 70(350):311-319, 1975. doi:10.1080/01621459.1975.10479864 | Opened 2026-11-24 (first page of a course-hosted PDF: title, authors, journal, volume, pages and DOI confirmed; body not read in detail). M6 (2026-11-25): the free RAND report version (R-1394-OEO, 1974) was located, but its PDF is an encrypted scan whose text could not be extracted with the available tools; not read | Shrinkage of separate means towards a common value; theoretical motivation for SHRINK |
| wilson1927 | E. B. Wilson, "Probable Inference, the Law of Succession, and Statistical Inference", JASA, June 1927. doi:10.1080/01621459.1927.10502953 | Metadata only (MaRDI portal page opened; publisher page returned 403; a scanned PDF had no extractable text) | Origin of the Wilson score interval cited by miller2009. Volume 22(158):209-212 from search results only, unverified |
| hu2007wp | N. Hu, P. A. Pavlou and J. Zhang, "Why do Online Product Reviews have a J-shaped Distribution? Overcoming Biases in Online Word-of-Mouth Communication", working paper submitted to Marketing Science, February 2007. https://archive.nyu.edu/bitstream/2451/14951/2/usedbook1.pdf | Opened 2026-11-24 (title page and abstract read); full text (35 pages) re-opened 2026-11-25 (M6): the abstract (PDF page 2) and introduction (PDF pages 4 and 5) state that purchasing and under-reporting biases produce the J-shaped distribution and make the mean a biased estimator of product quality; the rest not read | Purchasing bias and under-reporting bias; the mean is a biased estimator of quality; J-shaped distributions. Basis of the `lambda` selection model |
| hu2009 | N. Hu, J. Zhang and P. A. Pavlou, "Overcoming the J-shaped Distribution of Product Reviews", Communications of the ACM 52(10):144-147, 2009. doi:10.1145/1562764.1562800 | Unverified (ACM pages returned 403; details from search results only) | Published short version of hu2007wp; cite only after verification |
| li2008 | X. Li and L. M. Hitt, "Self-Selection and Information Role of Online Product Reviews", Information Systems Research 19(4):456-474, 2008. doi:10.1287/isre.1070.0154 | Abstract opened (EconPapers record) 2026-11-24; author-hosted working paper (Wharton faculty page, dated September 2007, 38 pages) opened 2026-11-25 (M6): abstract (page 1) and section 1 (page 2) state that early buyers self-select and may hold different preferences from later consumers. The published version was not read | Early reviewers self-select; uncorrected bias reduces consumer surplus. Motivates quality-dependent exposure and selection |
| muchnik2013 | L. Muchnik, S. Aral and S. J. Taylor, "Social Influence Bias: A Randomized Experiment", Science 341(6146):647-651, 2013. doi:10.1126/science.1240466 | Secondary source opened (MIT News, 2013-08-08); journal page returned 403 | Herding in ratings. Not modelled in M0 scope; listed as a limitation |
| algolia | Algolia documentation, "Bayesian average" how-to. https://www.algolia.com/doc/guides/managing-results/must-do/custom-ranking/how-to/bayesian-average/ | Opened 2026-11-24 | Practitioner form of the Bayesian average `(n * xbar + C * m) / (n + C)`; shows SHRINK is a common practice, not a contribution |
| harper2015 | F. M. Harper and J. A. Konstan, "The MovieLens Datasets: History and Context", ACM TiiS 5(4), 2015. doi:10.1145/2827872 | Metadata only (citation stated in the ML-25M README, opened); author preprint (files.grouplens.org, 20 pages, placeholder article number and DOI) opened 2026-11-25 (M6): Table II (page 13) gives MovieLens 1M as 6,040 users, 3,706 movies and 1,000,209 ratings, 1 to 5 stars. The published version was not read | Required citation if MovieLens were used |

## 2. What is known

- Sorting by the raw mean promotes items with few ratings; lower bounds and Bayesian averages are well-known fixes (miller2009, miller2014, algolia).
- Shrinkage towards a common mean improves aggregate estimation accuracy under exchangeable-means assumptions (efron1975).
- Observed online ratings are shaped by self-selection, so their mean is a biased estimator of quality (hu2007wp, li2008).

## 3. Narrow contribution (proposed, to be checked against a wider search at M1)

The fixes above are standard. The proposed contribution is not a new estimator. It is a transparent, preregistered simulation map of **when** the mean's misranking is material: the size of the rank-recovery gap, with uncertainty, as a function of review count, noise, prior strength, reporting selection and quality-dependent exposure, plus sensitivity checks that could overturn it. No novelty is claimed until the M1 search (Google Scholar-style queries on "ranking by average rating simulation", "empirical Bayes ranking", "posterior expected rank") is completed and recorded here.

## 4. Gaps in this review (to close at M1)

- Literature on ranking under uncertainty from statistics (for example posterior expected ranks and ranking of small-area estimates) was not searched yet.
- No peer-reviewed simulation study comparing these three estimators was located in the scoping search; absence of evidence is not evidence of absence.

## 5. M4 citation audit (2026-11-25)

Every external claim in the manuscript and the experiment reports was checked against the access status above (claims CLM-019 to CLM-026 in `research/claims_register.csv`). Corrections: the EXP-001 report attributed a squared-error result to efron1975, of which only the first page was read; it now cites the paper for the general idea only, as does the EXP-003 report. The EXP-002 report said hu2007wp was "opened"; it now says title page and abstract. miller2014 was re-opened to verify the statement that the method is approximate. Abstract-only and metadata-only sources are marked as such in the manuscript references. wilson1927, hu2009 and muchnik2013 are not cited in the manuscript.
