// SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
// Browser port of the TRUST engine (src/trust/model.py, simulate.py, estimators.py, metrics.py).
// The truth, estimators, intervals and metrics follow the Python code line by line and are checked
// against a Python fixture to 1e-12 (engine.test.ts). The random generator is NOT numpy's PCG64:
// the same seed gives a different catalogue than the research engine, so the generator is checked
// only in distribution against the committed EXP-001 runs.

export const LEVELS = [1, 2, 3, 4, 5] as const;
const SCALE_MIDPOINT = 3.0;
const PRIOR_STRENGTH = 5.0;

// ---------- random numbers (sfc32 seeded by splitmix32) ----------

export type Rng = { uniform: () => number; normal: () => number };

export function makeRng(seed: number): Rng {
  let s = seed >>> 0;
  const split = () => {
    s = (s + 0x9e3779b9) | 0;
    let z = s;
    z = Math.imul(z ^ (z >>> 16), 0x85ebca6b);
    z = Math.imul(z ^ (z >>> 13), 0xc2b2ae35);
    return (z ^ (z >>> 16)) >>> 0;
  };
  let a = split(), b = split(), c = split(), d = split();
  const u32 = () => {
    const t = (((a + b) | 0) + d) | 0;
    d = (d + 1) | 0;
    a = b ^ (b >>> 9);
    b = (c + (c << 3)) | 0;
    c = (c << 21) | (c >>> 11);
    c = (c + t) | 0;
    return t >>> 0;
  };
  for (let i = 0; i < 12; i++) u32();
  const uniform = () => ((u32() >>> 5) * 67108864 + (u32() >>> 6)) / 9007199254740992; // 53 bits, [0, 1)
  let spare: number | null = null;
  const normal = () => {
    if (spare !== null) {
      const v = spare;
      spare = null;
      return v;
    }
    let x: number, y: number, r: number;
    do {
      x = 2 * uniform() - 1;
      y = 2 * uniform() - 1;
      r = x * x + y * y;
    } while (r >= 1 || r === 0);
    const f = Math.sqrt((-2 * Math.log(r)) / r);
    spare = y * f;
    return x * f;
  };
  return { uniform, normal };
}

export function gamma(rng: Rng, shape: number): number {
  if (shape < 1) return gamma(rng, shape + 1) * Math.pow(1 - rng.uniform(), 1 / shape);
  const d = shape - 1 / 3, c = 1 / Math.sqrt(9 * d);
  for (;;) {
    let x: number, v: number;
    do {
      x = rng.normal();
      v = 1 + c * x;
    } while (v <= 0);
    v = v * v * v;
    const u = 1 - rng.uniform();
    if (u < 1 - 0.0331 * x ** 4) return d * v;
    if (Math.log(u) < 0.5 * x * x + d * (1 - v + Math.log(v))) return d * v;
  }
}

export function beta(rng: Rng, a: number, b: number): number {
  const x = gamma(rng, a), y = gamma(rng, b);
  return x / (x + y);
}

function lgamma(x: number): number {
  // Lanczos approximation (g = 7, n = 9), adequate for the Poisson acceptance test.
  const g = 7;
  const c = [0.99999999999980993, 676.5203681218851, -1259.1392167224028, 771.32342877765313, -176.61502916214059,
    12.507343278686905, -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7];
  if (x < 0.5) return Math.log(Math.PI / Math.abs(Math.sin(Math.PI * x))) - lgamma(1 - x);
  x -= 1;
  let a = c[0];
  const t = x + g + 0.5;
  for (let i = 1; i < 9; i++) a += c[i] / (x + i);
  return 0.5 * Math.log(2 * Math.PI) + (x + 0.5) * Math.log(t) - t + Math.log(a);
}

export function poisson(rng: Rng, lam: number): number {
  if (lam <= 0) return 0;
  if (lam < 10) {
    const L = Math.exp(-lam);
    let k = 0, p = rng.uniform();
    while (p > L) {
      k++;
      p *= rng.uniform();
    }
    return k;
  }
  // PTRS (Hoermann 1993), the method numpy uses for lam >= 10.
  const slam = Math.sqrt(lam), loglam = Math.log(lam);
  const b = 0.931 + 2.53 * slam, a = -0.059 + 0.02483 * b;
  const invalpha = 1.1239 + 1.1328 / (b - 3.4), vr = 0.9277 - 3.6224 / (b - 2);
  for (;;) {
    const U = rng.uniform() - 0.5, V = rng.uniform();
    const us = 0.5 - Math.abs(U);
    const k = Math.floor(((2 * a) / us + b) * U + lam + 0.43);
    if (us >= 0.07 && V <= vr) return k;
    if (k < 0 || (us < 0.013 && V > us)) continue;
    if (Math.log(V) + Math.log(invalpha) - Math.log(a / (us * us) + b) <= -lam + k * loglam - lgamma(k + 1)) return k;
  }
}

/** Negative binomial with the given mean and shape r, as a gamma-Poisson mixture (as numpy). */
export function negBin(rng: Rng, r: number, mean: number): number {
  return poisson(rng, (gamma(rng, r) * mean) / r);
}

// ---------- model ----------

function erfc(x: number): number {
  if (x < 0) return 2 - erfc(-x);
  if (x < 2.5) {
    // erf(x) = 2/sqrt(pi) exp(-x^2) sum_n 2^n x^(2n+1) / (2n+1)!!, all terms positive.
    let term = x, sum = x;
    const x2 = x * x;
    for (let n = 1; n < 200; n++) {
      term *= (2 * x2) / (2 * n + 1);
      sum += term;
      if (term < sum * 1e-17) break;
    }
    return 1 - (2 / Math.sqrt(Math.PI)) * Math.exp(-x2) * sum;
  }
  // Continued fraction (modified Lentz) for x >= 2.5.
  const tiny = 1e-300;
  let f = x, C = x, D = 0;
  for (let n = 1; n < 300; n++) {
    const an = n / 2;
    D = x + an * D;
    D = Math.abs(D) < tiny ? tiny : D;
    C = x + an / C;
    C = Math.abs(C) < tiny ? tiny : C;
    D = 1 / D;
    const delta = C * D;
    f *= delta;
    if (Math.abs(delta - 1) < 1e-16) break;
  }
  return Math.exp(-x * x) / (f * Math.sqrt(Math.PI));
}

export function normCdf(z: number): number {
  return 0.5 * erfc(-z / Math.SQRT2);
}

/** theta = E[r | mu, sigma] in stars (model.true_quality). */
export function trueQuality(mu: number, sigma: number): number {
  const cuts = [1.5, 2.5, 3.5, 4.5];
  const cdf = cuts.map((c) => normCdf((c - mu) / sigma));
  const lower = [0, ...cdf], upper = [...cdf, 1];
  let t = 0;
  for (let k = 0; k < 5; k++) t += Math.min(Math.max(upper[k] - lower[k], 0), 1) * LEVELS[k];
  return t;
}

export type Quality = { kind: "beta"; a: number; b: number } | { kind: "mixture"; a1: number; b1: number; a2: number; b2: number };

export interface CellParams {
  nProducts: number;
  nu: number;
  sigma: number;
  nbDispersion: number;
  quality: Quality;
}

export interface Catalogue {
  mu: number[];
  theta: number[];
  counts: number[][];
}

export function simulateCatalogue(p: CellParams, rng: Rng): Catalogue {
  const mu: number[] = [];
  for (let i = 0; i < p.nProducts; i++) {
    const q = p.quality;
    const b = q.kind === "beta" ? beta(rng, q.a, q.b) : rng.uniform() < 0.5 ? beta(rng, q.a1, q.b1) : beta(rng, q.a2, q.b2);
    mu.push(1 + 4 * b);
  }
  const counts = mu.map((m) => {
    const row = [0, 0, 0, 0, 0];
    const nstar = negBin(rng, p.nbDispersion, p.nu); // lambda = 0, gamma = 0: every potential rating is reported
    for (let j = 0; j < nstar; j++) {
      const r = Math.min(Math.max(Math.floor(m + p.sigma * rng.normal() + 0.5), 1), 5);
      row[r - 1]++;
    }
    return row;
  });
  return { mu, theta: mu.map((m) => trueQuality(m, p.sigma)), counts };
}

// ---------- estimators ----------

export interface Summary {
  n: number[];
  xbar: number[]; // NaN where n == 0
  m: number;
  sPool: number;
}

export function summarise(counts: number[][]): Summary {
  const n = counts.map((c) => c.reduce((s, x) => s + x, 0));
  const sums = counts.map((c) => c.reduce((s, x, k) => s + x * LEVELS[k], 0));
  const sq = counts.map((c) => c.reduce((s, x, k) => s + x * LEVELS[k] * LEVELS[k], 0));
  const xbar = n.map((ni, i) => (ni > 0 ? sums[i] / ni : NaN));
  const total = n.reduce((s, x) => s + x, 0);
  const m = total > 0 ? sums.reduce((s, x) => s + x, 0) / total : SCALE_MIDPOINT;
  let ssSum = 0, df = 0;
  n.forEach((ni, i) => {
    if (ni >= 2) {
      ssSum += Math.max(sq[i] - ni * xbar[i] ** 2, 0);
      df += ni - 1;
    }
  });
  return { n, xbar, m, sPool: df > 0 ? Math.sqrt(ssSum / df) : NaN };
}

export function meanScore(counts: number[][]): number[] {
  const s = summarise(counts);
  return s.n.map((ni, i) => (ni > 0 ? s.xbar[i] : s.m));
}

export function shrinkScore(counts: number[][], kappa: number, centreOffset = 0): number[] {
  const s = summarise(counts);
  const centre = s.m + centreOffset;
  return s.n.map((ni, i) => (ni * (ni > 0 ? s.xbar[i] : 0) + kappa * centre) / (ni + kappa));
}

export function dirichletPosterior(counts: number[][]): { mean: number[]; variance: number[] } {
  const tot = [0, 0, 0, 0, 0];
  counts.forEach((c) => c.forEach((x, k) => (tot[k] += x)));
  const all = tot.reduce((s, x) => s + x, 0);
  const prior = all === 0 ? [1, 1, 1, 1, 1] : tot.map((t) => (PRIOR_STRENGTH * t) / all);
  const mean: number[] = [], variance: number[] = [];
  for (const c of counts) {
    const alpha = c.map((x, k) => x + prior[k]);
    const a0 = alpha.reduce((s, x) => s + x, 0);
    const mu = alpha.reduce((s, x, k) => s + x * LEVELS[k], 0) / a0;
    const second = alpha.reduce((s, x, k) => s + x * LEVELS[k] ** 2, 0) / a0;
    mean.push(mu);
    variance.push(Math.max(second - mu ** 2, 0) / (a0 + 1));
  }
  return { mean, variance };
}

export function lcbScore(counts: number[][], z: number): number[] {
  const { mean, variance } = dirichletPosterior(counts);
  return mean.map((m, i) => m - z * Math.sqrt(variance[i]));
}

export type ArmType = "mean" | "shrink" | "lcb";

export function intervals(arm: ArmType, counts: number[][], z: number, kappa = 5, centreOffset = 0): { lo: number[]; hi: number[] } {
  const s = summarise(counts);
  let centre: number[], half: number[];
  if (arm === "mean") {
    centre = meanScore(counts);
    half = s.n.map((ni) => (z * s.sPool) / Math.sqrt(Math.max(ni, 1)));
  } else if (arm === "shrink") {
    centre = shrinkScore(counts, kappa, centreOffset);
    half = s.n.map((ni) => (z * s.sPool) / Math.sqrt(ni + kappa));
  } else {
    const p = dirichletPosterior(counts);
    centre = p.mean;
    half = p.variance.map((v) => z * Math.sqrt(v));
  }
  return { lo: centre.map((c, i) => c - half[i]), hi: centre.map((c, i) => c + half[i]) };
}

// ---------- metrics ----------

/** Indices by score descending, ties broken by product id ascending (metrics.rank_order). */
export function rankOrder(scores: number[]): number[] {
  return scores.map((_, i) => i).sort((i, j) => scores[j] - scores[i] || i - j);
}

/** Kendall tau-b, O(N^2) definition (metrics.kendall_tau_b_reference). NaN if undefined. */
export function kendallTauB(s: number[], t: number[]): number {
  let nc = 0, nd = 0, ts = 0, tt = 0;
  for (let i = 0; i < s.length; i++) {
    for (let j = i + 1; j < s.length; j++) {
      const ds = Math.sign(s[i] - s[j]), dt = Math.sign(t[i] - t[j]);
      if (ds === 0 && dt === 0) continue;
      if (ds === 0) ts++;
      else if (dt === 0) tt++;
      else if (ds === dt) nc++;
      else nd++;
    }
  }
  const denom = Math.sqrt((nc + nd + ts) * (nc + nd + tt));
  return denom === 0 ? NaN : (nc - nd) / denom;
}

export function precisionAtK(s: number[], t: number[], k: number): number {
  const a = new Set(rankOrder(s).slice(0, k));
  return rankOrder(t).slice(0, k).filter((i) => a.has(i)).length / k;
}

export function regretAtK(s: number[], t: number[], k: number): number {
  const mean = (idx: number[]) => idx.reduce((acc, i) => acc + t[i], 0) / idx.length;
  return mean(rankOrder(t).slice(0, k)) - mean(rankOrder(s).slice(0, k));
}

export function rmse(s: number[], t: number[]): number {
  return Math.sqrt(s.reduce((acc, x, i) => acc + (x - t[i]) ** 2, 0) / s.length);
}
