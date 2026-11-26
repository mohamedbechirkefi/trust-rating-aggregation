<!-- SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0 -->
# TRUST demo: design plan (owner request 2026-11-26)

## Subject, audience, job

- **Subject.** Star ratings as a measurement problem. A product with three five-star reviews outranks one with three hundred reviews at 4.8 if you sort by the average. Shrinkage (a Bayesian average) and lower credible bounds are the remedies; the study measures, against a known simulated truth, when they recover the order of products better or worse.
- **Audience.** A curious technical reader who has sorted by stars, an admissions committee reading quickly, and a researcher who wants the estimands, intervals and invalidation checks.
- **Primary job.** Ask the question and answer it in one sentence (it depends on rating noise and on the prior being right), then show the answer as a test-lab verdict: the shrinkage advantage at each noise level with its interval, followed by the full forest plots.

## The direction: a consumer test-lab report

Product test labels, bench sheets and calibrated instruments. Ratings are treated as readings with error bars; every number sits on a label or a bench sheet. Stars appear blurred when evidence is thin and sharpen as reviews accumulate.

## Colour (light only)

| Name | Hex | Role |
| --- | --- | --- |
| Bench white | `#F7F8F6` | page field: a clean, cool lab white (not cream) |
| Graphite | `#1F2830` | text, rules, simulated truth |
| Label yellow | `#F2C21B` | test-label grounds behind graphite text, the hero label strip; never text on white |
| Calibration blue | `#1F57B8` | SHRINK (the uncertainty-aware estimate), links, focus |
| Raw magenta | `#A51F5C` | MEAN (the plain average), "worse than MEAN" bars |
| Bench grey | `#E3E7E4` | instrument panels, tracks, table bands |

LCB keeps a third data hue, a verdict green `#1C6B4E`, used only in charts and the ranking table (hits). All text colours pass 4.5:1 on bench white and on bench grey. The brand is light only: a test report is printed on white; a dark variant would add nothing.

## Type

- **Archivo** (Omnibus-Type, SIL OFL 1.1), variable with width and weight axes: display, label headings and the wordmark, set wide (width 112 to 125) and heavy (750 to 850), like the header strip of a test label. Sentence case.
- **Atkinson Hyperlegible Next** (Braille Institute, SIL OFL 1.1), 400 and 700: body, controls, tables. Designed for legibility, which fits a consumer report; tabular figures for every number.
- Scale (1.2 ratio): 14, 16, 17, 20, 24, 29, 35, 50 px; body 17 px, line-height 1.55, measure at most 70 characters.

## Layout

Left-aligned. A bench sheet: content on a 12-column grid with a narrow left margin column on wide screens that carries the evidence label of each section (published, assumption, sandbox) like a lab-sheet margin stamp.

```
+---------------------------------------------------------------+
| [star+interval] Trust     Verdict  Results  Explorer  Method  |  sticky
+===============================================================+
| When do average ratings     | Illustration, not study data    |
| misrank products?           | +-----------------------------+ |
| Answer sentence with the    | | A few reviews   [blur stars] | |
| three noise-level values.   | |  |----o----------◆--|       | |
| author line                 | | Many reviews    [sharp stars]| |
|                             | |  |--o◆--|                   | |
+-----------------------------+-------------------------------+
| TEST VERDICT label (yellow header strip)                      |
|  noise 0.5 stars   [bar left of zero]   -0.0198 (interval)    |
|  noise 1.0 stars   [bar right]           0.0085 (interval)    |
|  noise 1.5 stars   [bar right]           0.0250 (interval)    |
+---------------------------------------------------------------+
| Overview | Published results (forest plots, experiment sheets) |
| Rating explorer (sandbox instrument panel)                    |
| Assumptions | Method and limitations | Reproduce              |
| footer                                                        |
+---------------------------------------------------------------+
```

Experiment panels are bench sheets (graphite header rule, id in Archivo wide); the verdict is a test label with a yellow strip; the sandbox is an instrument panel on bench grey. Radii vary by role: labels 6 px, sheets 2 px, controls 4 px.

## Motion

- **The orchestrated hero moment.** Two product labels. Review ticks drop into each product's strip (40 ms stagger); the interval band narrows (scaleX) as they accumulate; the plain average settles at the end of the scale for the product with few reviews while the shrunk estimate is pulled towards the catalogue centre; the blurred star row crossfades to sharp for the product with many reviews and stays soft for the one with few. About 2.4 s, once. Labelled "Illustration, not study data", with no numerals.
- **Motion that answers actions.** The verdict bars grow from the zero line when the verdict scrolls into view (once); forest-plot rows reveal once on scroll (clip-path wipe from the zero line outward); the explorer's ranking segmented control slides its indicator; a sandbox run shows a progress bar and the result line settles in.
- Curves `cubic-bezier(0.23, 1, 0.32, 1)` (entrances) and `cubic-bezier(0.77, 0, 0.175, 1)` (movement). Transform, opacity and clip-path only. Hover motion only under `(hover: hover) and (pointer: fine)`. Reduced motion: final state at once, or opacity only.

## The one memorable thing

The stars that sharpen with evidence: a blurred star row that comes into focus as reviews accumulate, next to its interval band narrowing. The mark repeats it: a star sitting on a confidence interval, like a point on a forest plot.

## Review against the generated-page tells, and what changed

- First draft put a black hero with a single yellow accent (a "warning label" look). That is the near-black-plus-one-accent default. Changed: the field is bench white; yellow appears only as label grounds behind graphite text.
- First draft used an all-caps tracked "TEST RESULT" eyebrow on every section. Removed. The verdict label keeps one header strip in sentence case ("Test verdict"), because a test label genuinely has one; section evidence labels are short sentence-case stamps.
- First draft used a monospace face for every number. Numbers use the body face with tabular figures; monospace stays only in code and hashes.
- First draft had three identical rounded cards for the noise levels. Replaced by one label with three rows on a shared zero axis, which is the comparison the reader needs.
- First draft paper tone was warm off-white with an amber accent (the old demo). Replaced by a cool lab white with calibration blue and raw magenta that also encode the two estimators.
- Compared with the other studies' directions: PARADOX is slate and chalk in a jury room; MEMORY uses index cards and pencil; FARE a departure board; TRUST is the only white test-lab report with labels and instruments.
