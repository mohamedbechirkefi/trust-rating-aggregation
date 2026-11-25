// SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
// Port check: the browser engine against a fixture written by the Python engine
// (scripts/make_sandbox_fixture.py). Tolerances:
//   exact part        |JS - Python| <= 1e-12 for truth, scores, intervals and metrics computed
//                     from the same simulated counts and qualities;
//   generator part    per EXP-001 cell, |JS mean - committed mean| <= 4 combined standard errors
//                     for tau-b (MEAN, SHRINK_5), D and the share of unreviewed products,
//                     with 100 JS seeds against the 20 committed seeds.
import { describe, expect, it } from "vitest";
import { readFileSync } from "node:fs";
import {
  intervals,
  kendallTauB,
  lcbScore,
  makeRng,
  meanScore,
  precisionAtK,
  regretAtK,
  rmse,
  shrinkScore,
  simulateCatalogue,
  trueQuality,
} from "./engine";

const fx = JSON.parse(readFileSync("src/fixtures/sandbox_fixture.json", "utf8"));
const TOL = 1e-12;

function close(a: number[], b: number[], tol = TOL) {
  expect(a.length).toBe(b.length);
  const worst = Math.max(...a.map((x, i) => Math.abs(x - b[i])));
  expect(worst).toBeLessThanOrEqual(tol);
}

describe("exact part: same counts, same numbers (1e-12)", () => {
  for (const c of fx.catalogues) {
    const name = `${c.cell_id} seed ${c.seed_index}`;
    it(`${name}: truth theta`, () => close(c.mu.map((m: number) => trueQuality(m, c.sigma)), c.theta));
    it(`${name}: MEAN, SHRINK_5 and LCB scores and intervals`, () => {
      close(meanScore(c.counts), c.arms.MEAN.scores);
      close(shrinkScore(c.counts, fx.params.kappa), c.arms.SHRINK_5.scores);
      close(lcbScore(c.counts, fx.params.lcb_z), c.arms.LCB.scores);
      const m = intervals("mean", c.counts, fx.params.interval_z);
      close(m.lo, c.arms.MEAN.lo); close(m.hi, c.arms.MEAN.hi);
      const s = intervals("shrink", c.counts, fx.params.interval_z, fx.params.kappa);
      close(s.lo, c.arms.SHRINK_5.lo); close(s.hi, c.arms.SHRINK_5.hi);
      const l = intervals("lcb", c.counts, fx.params.interval_z);
      close(l.lo, c.arms.LCB.lo); close(l.hi, c.arms.LCB.hi);
    });
    it(`${name}: tau-b, precision, regret and RMSE`, () => {
      for (const a of ["MEAN", "SHRINK_5", "LCB"]) {
        const sc = c.arms[a].scores;
        close([kendallTauB(sc, c.theta), precisionAtK(sc, c.theta, fx.params.top_k), regretAtK(sc, c.theta, fx.params.top_k), rmse(sc, c.theta)],
          [c.arms[a].tau_b, c.arms[a].precision_at_k, c.arms[a].regret_at_k, c.arms[a].rmse]);
      }
    });
  }
});

describe("generator part: distribution matches the committed EXP-001 runs (4 SE)", () => {
  const SEEDS = 100;
  for (const cell of fx.cells) {
    it(`${cell.cell_id} (nu ${cell.nu}, sigma ${cell.sigma})`, () => {
      const tm: number[] = [], ts: number[] = [], d: number[] = [], z: number[] = [];
      for (let s = 0; s < SEEDS; s++) {
        const cat = simulateCatalogue(
          { nProducts: fx.params.n_products, nu: cell.nu, sigma: cell.sigma, nbDispersion: fx.params.nb_dispersion,
            quality: { kind: "beta", a: fx.params.quality_beta[0], b: fx.params.quality_beta[1] } },
          makeRng(7919 * (s + 1) + cell.nu * 31 + Math.round(cell.sigma * 10)),
        );
        const a = kendallTauB(meanScore(cat.counts), cat.theta), b = kendallTauB(shrinkScore(cat.counts, fx.params.kappa), cat.theta);
        tm.push(a); ts.push(b); d.push(b - a);
        z.push(cat.counts.filter((r) => r.every((x) => x === 0)).length / cat.counts.length);
      }
      const stat = (x: number[]) => {
        const m = x.reduce((p, q) => p + q, 0) / x.length;
        return { m, sd: Math.sqrt(x.reduce((p, q) => p + (q - m) ** 2, 0) / (x.length - 1)) };
      };
      for (const [js, py] of [[tm, cell.tau_b_mean], [ts, cell.tau_b_shrink5], [d, cell.D], [z, cell.share_zero_reviews]] as const) {
        const j = stat(js as number[]);
        const se = Math.sqrt(py.sd ** 2 / cell.n_seeds + j.sd ** 2 / SEEDS);
        expect(Math.abs(j.m - py.mean)).toBeLessThanOrEqual(4 * se);
      }
    });
  }
});

describe("random generator", () => {
  it("is deterministic for a seed and differs between seeds", () => {
    const a = makeRng(42), b = makeRng(42), c = makeRng(43);
    const xa = [a.uniform(), a.normal()], xb = [b.uniform(), b.normal()], xc = [c.uniform(), c.normal()];
    expect(xa).toEqual(xb);
    expect(xa).not.toEqual(xc);
  });
});
