<!-- SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0 -->
# demo/

Static, offline research page for TRUST (M5, 2026-11-25). Stack: TypeScript, React and Vite, pinned versions from the shared lab template (owner, 2026-11-25, "Next"; decision D-016). Demo URL: <https://trust-rating-aggregation.kefimohamedbechir.workers.dev>. The built page (`dist/`) is hosted as Cloudflare Workers static assets on the free plan, configured by `wrangler.jsonc` (assets only, no Worker script); it is deployed by the coordinator, not by any script of this repository.

## What it shows

- **Overview** with the status label (independent research manuscript / preprint draft, not peer-reviewed; all results simulated) and the three value labels: published result, assumption, sandbox output.
- **Published results**: FIG-001 to FIG-003 redrawn as dot-and-interval charts from the exported data, and one panel per registered experiment (EXP-001 to EXP-003) plus the exploratory M4 checks, each with its status, its verdict under the frozen rule, its estimates with 95% intervals and its claim ids. Every displayed number is the exact text the manuscript prints (`tests/test_demo_export.py`). The disclosed deviations D-011 (bootstrap p-values for Holm) and D-012 (S3 cannot discriminate by design) appear where the affected results are shown.
- **Assumptions**, **method and limitations**, and the source files with their SHA-256.
- **Rating explorer (sandbox)**: a seeded simulation in a Web Worker with scenario presets (the nine EXP-001 cells), sample-size and catalogue-size sliders, rating noise, shrinkage strength and centre offset, quality population, seed, replicates, run, cancel and reset. It shows MEAN and SHRINK estimates with their nominal 90% intervals against the simulated truth, the LCB score, and a top-10 ranking comparison. Its output can be downloaded as JSON.

## Sandbox fidelity

`src/engine.ts` ports the research engine. The truth, estimators, intervals and metrics match the Python engine to 1e-12 on two regenerated EXP-001 catalogues (`src/fixtures/sandbox_fixture.json`, from `scripts/make_sandbox_fixture.py`). The random-number generator is not numpy's, so a seed does not reproduce a study catalogue; in each of the nine EXP-001 cells, the mean tau-b of MEAN and SHRINK_5, their difference and the share of unreviewed products over 100 browser seeds lie within 4 combined standard errors of the 20 committed runs (`src/engine.test.ts`). The sandbox models random reporting only (no selection or exposure coupling). Its output is never a research result.

## Commands

    npm ci && npm test && npm run build && npm run preview
    node tools/a11y_check.mjs dist --screenshots <scratch dir>

The results file `public/data/results.json` is written by `../scripts/export_demo_data.py` from committed results only. The page validates it and fails closed: if any field is missing or malformed, no number is shown and the sandbox does not start. No font, image or script is loaded from another host, no analytics are used, and nothing about visitors is collected, stored or sent.

## Design and brand

The page has its own identity (owner request of 2026-11-26): a consumer test-lab report, with product test labels, bench sheets and an instrument-panel sandbox; stars sharpen as reviews accumulate. The plan, palette, type, motion and review are in `DESIGN.md`. Brand files are in `public/brand/` (mark: a star on a confidence interval; one-colour and reversed variants; wordmark lockups; favicon SVG and 32 px PNG; Open Graph card `og.png`). `tools/make_brand.py` regenerates the SVGs (needs fontTools and a TrueType copy of the Archivo variable font, decompressed from the bundled woff2, for example with the `wawoff2` npm package outside this repository); `tools/og.html` is the source of the Open Graph card (Chrome headless, 1200 by 630). The hero animation is labelled "Illustration, not study data" and prints no numeral; every number on the page still comes from `public/data/results.json`.

## Third-party notes

- Archivo, `@fontsource-variable/archivo` 5.3.0 (variable width and weight; Latin, Latin Extended and Vietnamese subsets bundled, loaded by unicode-range), copyright the Archivo Project Authors (Omnibus-Type), SIL Open Font License 1.1.
- Atkinson Hyperlegible Next, `@fontsource/atkinson-hyperlegible-next` 5.3.0 (weights 400 and 700, Latin subset), copyright the Atkinson Hyperlegible Next Project Authors (Braille Institute), SIL Open Font License 1.1.

Both are bundled by Vite and served from the page's own origin. The licence texts ship in each package's `LICENSE` file under `node_modules/`.
