<!-- SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0 -->
<!-- Draft for LinkedIn (master prompt section 8). Not published. Numbers copied from research/paper/manuscript.md. Links are placeholders until the owner releases the repository. -->

Does a Bayesian average rank products better than the plain star average? In a simulation, it depends on how noisy the ratings are.

TRUST is a small, preregistered and reproducible simulation of a catalogue of 200 products whose true quality is known by construction. It compares the arithmetic mean with Bayesian averages and a lower credible bound on the same simulated catalogues; the protocol was frozen by the owner before any confirmatory run, and 1,560 runs executed with none failing.

One defensible finding: the pooled advantage of a five-pseudo-review Bayesian average over the mean is small (0.0046 in Kendall tau-b, 95% interval 0.0030 to 0.0061), and its sign follows rating noise: -0.0198 at 0.5 stars, 0.0250 at 1.5. A half-star error in the shrinkage centre turns it into a larger loss. The lower bound ranked whole lists worse than the mean.

Caveat: everything is simulated, and the results depend on the model's assumptions. They say nothing about any real platform, product or review.

Manuscript (independent research manuscript / preprint draft, not peer-reviewed), experiment reports and an offline interactive demo: `<repository URL: not yet published>`, `<demo URL: not yet published>` (to be added by the owner at release).

Developed with an AI research and development assistant (Claude Code), which is not an author.

*Image (alt text, if the demo screenshot is attached): The TRUST demo page showing the question, the status label and a dot-and-interval chart of the shrinkage-minus-mean difference in Kendall tau-b for nine simulated cells, three noise levels and the pooled estimate.*
