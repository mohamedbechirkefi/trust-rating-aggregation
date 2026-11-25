<!-- SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0 -->
# EXP-002 report: reporting selection and quality-dependent missingness

## 1. Identification

| Field | Value |
|---|---|
| Experiment | EXP-002 (confirmatory; secondary hypothesis H2, nondirectional) |
| Status | Complete. The frozen matrix ran in full: 240 of 240 runs ok, 0 failed, 0 retried |
| Report version | 1.0 (M3), 2026-11-25, written under the owner's approval of 2026-11-25 (D-013) from committed results only |
| Authorship | Mohamed Bechir Kefi (owner-approved, C3). The AI assistant ran the experiment and drafted this report; it is not an author |
| Protocol | `research/experiments/EXP-002/protocol.md` v1.0, SHA-256 `47459d4b5c8d0f9ab2911be068929c6ada9253ec7a601004893c731b0b1fcf27`; study protocol `research/protocol.md` `3226e302fb4758327d50a5f583026d469d7ccbc5ad7c72b458fcd8bf2b702f03` |
| Config | `experiments/EXP-002.json`, file SHA-256 `325df0660716aa3be368cd85ae912184139617bc1b217488a7a98e79bf6b5bd9` (equal to the freeze record) |
| Provenance revision | `bd9e1460e29389def8baa43d6ca7cc553d659ff1`, clean tree |
| Data | Simulated; generator calibrated on MovieLens 1M (protocol section 13.1); `data/manifest.json` `ed8fb8eee48be9a08850c48872883a4299e3e4601b9ac4a371df65e023dd4d30` |

All numbers are simulated and hold only under the model of `research/protocol.md`. Every number is copied from `research/experiments/EXP-002/results_tables.md`, `results/confirmatory/analysis/EXP-002.json` or `results/confirmatory/EXP-002/`.

## 2. Executive summary

**Question.** When extreme ratings are more likely to be posted (`lambda`) and the number of reviews depends on quality (`gamma`), does the advantage `D` of SHRINK_5 (and of LCB) over MEAN change?

**Method.** 12 cells (`lambda` in {0, 2} x `gamma` in {-0.5, 0, 0.5} x `nu` in {3, 10}), sigma 1.0, 20 seeds each. Same-seed paired differences of `D` between factor levels, per stratum of the other factors and averaged over strata with equal weight. Holm across the lambda contrast and the two gamma contrasts.

**Outcome.** Reporting selection does not change `D` on average: lambda 2 minus 0 = -0.0001 (95% -0.0015 to 0.0012), Holm-adjusted p 0.8859. Two of the six per-stratum intervals exclude 0, in opposite directions, so the frozen contradiction rule (every stratum interval contains 0) is not met: H2 for lambda is **not contradicted under the frozen rule**, while the averaged estimand shows no detected difference. Quality-dependent exposure lowers `D` in both directions: gamma -0.5 minus 0 = -0.0112 (-0.0140 to -0.0084) and gamma 0.5 minus 0 = -0.0091 (-0.0123 to -0.0058), both Holm-rejected (adjusted p 0.0006). For LCB, outside the Holm family, all three contrasts are clearly non-zero.

**Principal caveat.** The per-stratum rule is uncorrected across six strata, and the two strata that exclude 0 point in opposite directions; the averaged contrast is the more informative summary. A null average is not equivalence.

## 3. Rationale

Hu, Pavlou and Zhang (2007 working paper, opened) describe purchasing and under-reporting biases that make the mean a biased estimator of quality and produce J-shaped rating distributions. Li and Hitt (2008, abstract opened) describe self-selection of early reviewers. These sources motivate the selection model; they do not validate its parameter values. The gap: whether stylised under-reporting and quality-dependent exposure change the relative ranking performance of shrinkage and lower bounds.

## 4. Hypotheses and operational definitions

- `D = tau_b(SHRINK_5) - tau_b(MEAN)` against the full-population truth `theta_i`; the same contrast is reported for LCB.
- Reporting probability `pi(r) = (1 + lambda |r - 3| / 2) / (1 + lambda)`; exposure weight `w_i = exp(gamma z_i) / mean exp(gamma z)`.
- H0: `E[D]` equal across `lambda` levels and across `gamma` levels. H1 (nondirectional): it differs.
- Estimand: `E[D | lambda = 2] - E[D | lambda = 0]` (same seed, same `gamma`, same `nu`), averaged over the six (`gamma`, `nu`) strata; analogous contrasts for `gamma = -0.5` and `gamma = 0.5`, each minus `gamma = 0`, averaged over the four (`lambda`, `nu`) strata (D-011).
- Frozen contradiction rule: 95% intervals for the lambda contrast contain 0 in every stratum; that outcome is "no detected difference", not equivalence.

## 5. Methodology

- Design: 2 x 3 x 2 factorial, 20 seeds per cell, 240 catalogues; seeds `SeedSequence([20261124, 2, seed_index])`, common across cells, so contrasts are paired by seed.
- Fixed: sigma 1.0; `mu ~ 1 + 4 Beta(4.2726, 3.1944)`; negative binomial dispersion 0.4909.
- Statistics: per stratum, 95% percentile bootstrap over the 20 seed pairs (10,000 resamples, seed 20261124); averaged contrasts by stratified bootstrap; two-sided bootstrap p-values and Holm at alpha 0.05 across the three SHRINK_5 contrasts (D-011, owner-accepted D-013). LCB contrasts are reported outside the Holm family.
- Software and hardware as EXP-001 (Python 3.12.1, numpy 2.3.4, scipy 1.16.2; Apple M1 Pro, macOS 15.3.1). Budget under 30 minutes; 2.26 s used.

## 6. Implementation verification

- Test suite before the runs: 165 passed, 0 failed, including the paired factor-contrast tests in `tests/test_hypotheses.py`.
- Metric validation (JRN-0006): 26 of 26 known-case checks passed, including the reporting probability at `lambda = 2` (1 at r = 1, 1/3 at r = 3).
- ORACLE tau-b = 1 in every run (minimum 1.000000000000); 0 degenerate-case flags.

## 7. Execution record

- Commands: `PYTHONPATH=src nice -n 10 .venv/bin/python -m trust.cli run --config experiments/EXP-002.json` (exit 0); `trust.cli report --dir results/confirmatory/EXP-002 --pdf`; `scripts/analyse_confirmatory.py --exp EXP-002`.
- Start 2026-11-24T23:35:24Z, end 2026-11-24T23:35:27Z (UTC). Wall time 2.26 s; per run mean 9.39 ms, median 3.64 ms, max 111.56 ms; process peak RSS 96.5 MiB.
- Run ids `RUN-EXP-002-c00-s000` to `RUN-EXP-002-c11-s019`: 240 planned, 240 ok, 0 failed, 0 retried. Provenance per run in `results/confirmatory/provenance.csv`.
- Deviations: none from the frozen protocol, config or seeds. The p-value method for Holm and the exact form of the gamma contrasts were fixed before data (D-011) and accepted by the owner with disclosure (owner, 2026-11-25, "approve all recommendations, RIGGED A"; D-013).

## 8. Results

**Realised data per cell** (`results/confirmatory/EXP-002/report.md`, "Cells").

| Cell | nu | lambda | gamma | Mean potential raters | Mean reported | Share zero reviews | Mean D (SHRINK_5) | Bootstrap 95% |
|---|---|---|---|---|---|---|---|---|
| c00 | 3 | 0 | -0.5 | 2.98 | 2.98 | 0.407 | -0.0025 | -0.0055 to 0.0004 |
| c01 | 3 | 0 | 0 | 3.02 | 3.02 | 0.387 | 0.0042 | 0.0006 to 0.0078 |
| c02 | 3 | 0 | 0.5 | 2.98 | 2.98 | 0.406 | 0.0016 | -0.0024 to 0.0054 |
| c03 | 3 | 2 | -0.5 | 2.98 | 1.89 | 0.486 | -0.0015 | -0.0041 to 0.0011 |
| c04 | 3 | 2 | 0 | 3.02 | 1.93 | 0.460 | 0.0034 | -0.0009 to 0.0073 |
| c05 | 3 | 2 | 0.5 | 2.98 | 1.98 | 0.486 | 0.0052 | 0.0017 to 0.0085 |
| c06 | 10 | 0 | -0.5 | 9.91 | 9.91 | 0.239 | -0.0016 | -0.0069 to 0.0036 |
| c07 | 10 | 0 | 0 | 9.92 | 9.92 | 0.221 | 0.0163 | 0.0113 to 0.0212 |
| c08 | 10 | 0 | 0.5 | 9.92 | 9.92 | 0.234 | -0.0046 | -0.0105 to 0.0013 |
| c09 | 10 | 2 | -0.5 | 9.91 | 6.27 | 0.294 | -0.0033 | -0.0083 to 0.0018 |
| c10 | 10 | 2 | 0 | 9.92 | 6.32 | 0.272 | 0.0118 | 0.0066 to 0.0168 |
| c11 | 10 | 2 | 0.5 | 9.92 | 6.53 | 0.289 | -0.0028 | -0.0091 to 0.0033 |

As anticipated (protocol item 19), `lambda = 2` lowers the reported count and raises the zero-review share; the realised distribution is reported, not corrected.

**SHRINK_5 minus MEAN: Holm family.**

| Contrast | Estimate (average over strata) | Two-sided 95% | p (two-sided) | Holm-adjusted p | Rejects H0 | Strata excluding 0 |
|---|---|---|---|---|---|---|
| lambda 2 minus 0 | -0.0001 | -0.0015 to 0.0012 | 0.8859 | 0.8859 | no | 2 of 6 |
| gamma -0.5 minus 0 | -0.0112 | -0.0140 to -0.0084 | 0.0002 | 0.0006 | yes | 3 of 4 |
| gamma 0.5 minus 0 | -0.0091 | -0.0123 to -0.0058 | 0.0002 | 0.0006 | yes | 2 of 4 |

Per stratum (20 pairs each):

| Contrast | Stratum | Mean | Bootstrap 95% |
|---|---|---|---|
| lambda 2 minus 0 | gamma -0.5, nu 3 | 0.0010 | -0.0010 to 0.0030 |
| lambda 2 minus 0 | gamma 0, nu 3 | -0.0008 | -0.0038 to 0.0020 |
| lambda 2 minus 0 | gamma 0.5, nu 3 | 0.0036 | 0.0004 to 0.0067 |
| lambda 2 minus 0 | gamma -0.5, nu 10 | -0.0017 | -0.0055 to 0.0023 |
| lambda 2 minus 0 | gamma 0, nu 10 | -0.0045 | -0.0079 to -0.0014 |
| lambda 2 minus 0 | gamma 0.5, nu 10 | 0.0018 | -0.0023 to 0.0054 |
| gamma -0.5 minus 0 | lambda 0, nu 3 | -0.0067 | -0.0114 to -0.0018 |
| gamma -0.5 minus 0 | lambda 2, nu 3 | -0.0049 | -0.0096 to 0.0000 |
| gamma -0.5 minus 0 | lambda 0, nu 10 | -0.0179 | -0.0246 to -0.0114 |
| gamma -0.5 minus 0 | lambda 2, nu 10 | -0.0151 | -0.0215 to -0.0087 |
| gamma 0.5 minus 0 | lambda 0, nu 3 | -0.0026 | -0.0087 to 0.0032 |
| gamma 0.5 minus 0 | lambda 2, nu 3 | 0.0018 | -0.0036 to 0.0073 |
| gamma 0.5 minus 0 | lambda 0, nu 10 | -0.0209 | -0.0278 to -0.0133 |
| gamma 0.5 minus 0 | lambda 2, nu 10 | -0.0147 | -0.0223 to -0.0072 |

**LCB minus MEAN (outside the Holm family, as the protocol requires).**

| Contrast | Estimate | Two-sided 95% | Strata excluding 0 |
|---|---|---|---|
| lambda 2 minus 0 | 0.0187 | 0.0149 to 0.0225 | 5 of 6 |
| gamma -0.5 minus 0 | -0.0926 | -0.1007 to -0.0846 | 4 of 4 |
| gamma 0.5 minus 0 | 0.0753 | 0.0663 to 0.0841 | 4 of 4 |

Per-stratum LCB values are in `research/experiments/EXP-002/results_tables.md`.

![FIG-002. EXP-002: change in D with lambda and gamma. Dot-and-interval chart of the averaged contrasts (lambda 2 minus 0; gamma -0.5 minus 0; gamma 0.5 minus 0) for SHRINK_5 and LCB. Each row averages six or four strata of 20 same-seed pairs; bars are two-sided 95% stratified bootstrap intervals. Dashed line at zero. Simulated.](figures/FIG-002.svg){fig-alt="Dot-and-interval chart with six rows. The three SHRINK_5 rows lie close to zero: the lambda row straddles zero and both gamma rows sit slightly left of zero near -0.01. The LCB rows are far from zero: lambda about +0.019, gamma -0.5 about -0.093, gamma 0.5 about +0.075."}

## 9. Interpretation

**Expected versus observed.** The protocol (mechanism, item 2) expected that with `gamma > 0` data-poor products tend to be poor, so shrinking them towards the catalogue mean would hurt, with the reverse for `gamma < 0`. Observed for SHRINK_5: `D` fell relative to `gamma = 0` in both directions, mostly at `nu = 10`, so the advantage is largest when exposure does not depend on quality. The directional prediction is not borne out for shrinkage. For LCB, which pushes data-poor products down rather than towards the mean, the pattern matches the mechanism: its relative performance rises with `gamma = 0.5` and falls with `gamma = -0.5`.

**Reporting selection.** On average, under-reporting of moderate ratings did not change the shrinkage advantage. The two strata whose intervals exclude 0 point in opposite directions, with six uncorrected intervals; this pattern is consistent with chance and is not read as a detected effect, though the frozen per-stratum rule is formally not met. For LCB, selection raised its relative performance by 0.0187.

**Competing explanation (b) of the protocol.** Lower effective sample size under selection, rather than selection itself, could drive any lambda effect. The realised counts show that `lambda = 2` reduced mean reported counts by about a third; despite this, the SHRINK_5 average contrast is null.

## 10. Threats to validity

- **Internal.** Seed-paired design across cells; analysis fixed before data (D-011).
- **Statistical.** Per-stratum intervals are uncorrected (the frozen rule uses them as stated); the Holm-adjusted averaged contrasts are the inferential summary. The Holm p-value method is D-011, owner-accepted with disclosure (D-013).
- **Construct.** Truth is the full-population `theta`; EXP-003 S3 was meant to test the alternative `theta_rep` but cannot discriminate for rank metrics (D-012).
- **External.** The selection and exposure functions are stylised assumptions; only sigma 1.0 and `nu` 3 and 10 were run.

## 11. Conclusion and next experiment

Under this model, reporting selection of the form tested does not change the average advantage of shrinkage over the mean (lambda contrast -0.0001, -0.0015 to 0.0012), while quality-dependent exposure in either direction reduces it (-0.0112 and -0.0091). The frozen per-stratum rule for lambda is formally not met because two of six strata exclude 0 in opposite directions. The lower bound reacts strongly to both factors. A follow-up could cross exposure coupling with rating noise, since EXP-001 shows that noise sets the sign of `D`; it would need a new EXP id and the owner's approval.

## 12. Reproduction appendix

```
../.tools/py/bin/uv sync --frozen --all-groups --all-extras
.venv/bin/python -m pytest -q
PYTHONPATH=src .venv/bin/python -m trust.cli run --config experiments/EXP-002.json
PYTHONPATH=src .venv/bin/python -m trust.cli report --dir results/confirmatory/EXP-002 --pdf
PYTHONPATH=src .venv/bin/python scripts/analyse_confirmatory.py --exp EXP-002
```

- Raw results: `results/confirmatory/EXP-002/results.json` (schema 1.0.0), `run_manifest.json`, `metrics.csv`, `summary.json`; checksums `results/confirmatory/SHA256SUMS`; provenance `results/confirmatory/provenance.csv`.
- Analysis: `results/confirmatory/analysis/EXP-002.json` and its manifest; tables `research/experiments/EXP-002/results_tables.md`; figure `figures/FIG-002.svg`.
- Tolerance: as EXP-001.
- References: as in `research/literature_review.md` (Hu, Pavlou and Zhang 2007; Li and Hitt 2008; Harper and Konstan 2015).
