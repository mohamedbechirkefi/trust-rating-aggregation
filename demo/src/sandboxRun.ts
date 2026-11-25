// SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
// One sandbox run: simulate a catalogue with the ported engine, score it with MEAN, SHRINK(kappa)
// and LCB, and compare each ranking with the known simulated truth. Pure; used by the worker.
import {
  intervals,
  kendallTauB,
  lcbScore,
  makeRng,
  meanScore,
  precisionAtK,
  rankOrder,
  shrinkScore,
  simulateCatalogue,
  summarise,
  type Quality,
} from "./engine";

export const QUALITIES: Record<string, { label: string; q: (a: number, b: number) => Quality }> = {
  calibrated: { label: "Calibrated Beta (MovieLens fit, as in EXP-001)", q: (a, b) => ({ kind: "beta", a, b }) },
  uniform: { label: "Uniform, Beta(1, 1) (as in EXP-003 S4)", q: () => ({ kind: "beta", a: 1, b: 1 }) },
  bimodal: { label: "Bimodal mixture of Beta(2, 6) and Beta(6, 2) (as in EXP-003 S4)", q: () => ({ kind: "mixture", a1: 2, b1: 6, a2: 6, b2: 2 }) },
};

export interface Settings {
  nProducts: number;
  nu: number;
  sigma: number;
  kappa: number;
  centreOffset: number;
  quality: keyof typeof QUALITIES;
  seed: number;
  replicates: number;
}

export interface Fixed {
  qualityBeta: [number, number];
  nbDispersion: number;
  lcbZ: number;
  topK: number;
}

export interface ArmResult {
  tauB: number;
  precision: number;
}

export interface ProductRow {
  id: number;
  n: number;
  theta: number;
  trueRank: number;
  mean: number;
  meanLo: number;
  meanHi: number;
  shrink: number;
  shrinkLo: number;
  shrinkHi: number;
  lcb: number;
}

export interface RunResult {
  arms: { MEAN: ArmResult; SHRINK: ArmResult; LCB: ArmResult };
  shareZero: number;
  products: ProductRow[];
}

export function runOne(s: Settings, f: Fixed, replicate: number): RunResult {
  const rng = makeRng((s.seed * 1009 + replicate) >>> 0);
  const cat = simulateCatalogue(
    {
      nProducts: s.nProducts,
      nu: s.nu,
      sigma: s.sigma,
      nbDispersion: f.nbDispersion,
      quality: QUALITIES[s.quality].q(f.qualityBeta[0], f.qualityBeta[1]),
    },
    rng,
  );
  const mean = meanScore(cat.counts);
  const shrink = shrinkScore(cat.counts, s.kappa, s.centreOffset);
  const lcb = lcbScore(cat.counts, f.lcbZ);
  const k = Math.min(f.topK, s.nProducts);
  const arm = (x: number[]): ArmResult => ({ tauB: kendallTauB(x, cat.theta), precision: precisionAtK(x, cat.theta, k) });
  const mi = intervals("mean", cat.counts, f.lcbZ);
  const si = intervals("shrink", cat.counts, f.lcbZ, s.kappa, s.centreOffset);
  const sum = summarise(cat.counts);
  const trueRank: number[] = [];
  rankOrder(cat.theta).forEach((id, r) => (trueRank[id] = r + 1));
  const products = cat.theta.map((theta, id) => ({
    id,
    n: sum.n[id],
    theta,
    trueRank: trueRank[id],
    mean: mean[id],
    meanLo: mi.lo[id],
    meanHi: mi.hi[id],
    shrink: shrink[id],
    shrinkLo: si.lo[id],
    shrinkHi: si.hi[id],
    lcb: lcb[id],
  }));
  return {
    arms: { MEAN: arm(mean), SHRINK: arm(shrink), LCB: arm(lcb) },
    shareZero: sum.n.filter((n) => n === 0).length / s.nProducts,
    products,
  };
}

/** Mean and two-sided 95% t interval over replicates (null interval for one replicate). */
export function summariseReplicates(x: number[]): { mean: number; lo: number | null; hi: number | null } {
  const v = x.filter((y) => Number.isFinite(y));
  const n = v.length;
  const mean = v.reduce((a, b) => a + b, 0) / n;
  if (n < 2) return { mean, lo: null, hi: null };
  const sd = Math.sqrt(v.reduce((a, b) => a + (b - mean) ** 2, 0) / (n - 1));
  const half = tQuantile975(n - 1) * (sd / Math.sqrt(n));
  return { mean, lo: mean - half, hi: mean + half };
}

const T975 = [12.706, 4.303, 3.182, 2.776, 2.571, 2.447, 2.365, 2.306, 2.262, 2.228, 2.201, 2.179, 2.16, 2.145, 2.131,
  2.12, 2.11, 2.101, 2.093, 2.086, 2.08, 2.074, 2.069, 2.064, 2.06, 2.056, 2.052, 2.048, 2.045, 2.042];

function tQuantile975(df: number): number {
  if (df <= 30) return T975[df - 1];
  return 1.96 + 2.4 / df; // close approximation above 30 degrees of freedom
}
