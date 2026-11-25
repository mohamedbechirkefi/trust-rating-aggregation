// SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
// Bounded, cancellable sandbox computation in a Web Worker. Runs the browser port of the TRUST
// engine (engine.ts) on the visitor's settings. Nothing is sent anywhere.
import { runOne, summariseReplicates, type Fixed, type ProductRow, type Settings } from "./sandboxRun";

export type WorkerRequest = { type: "run"; settings: Settings; fixed: Fixed } | { type: "cancel" };

export interface Summary {
  mean: number;
  lo: number | null;
  hi: number | null;
}

export interface SandboxOutput {
  settings: Settings;
  replicates: number;
  tauB: { MEAN: Summary; SHRINK: Summary; LCB: Summary };
  precision: { MEAN: Summary; SHRINK: Summary; LCB: Summary };
  dShrink: Summary;
  dLcb: Summary;
  shareZero: Summary;
  products: ProductRow[];
}

export type WorkerReply =
  | { type: "progress"; fraction: number }
  | { type: "done"; output: SandboxOutput }
  | { type: "cancelled" }
  | { type: "error"; message: string };

// Hard bounds, enforced here as well as in the form.
const LIMITS = { nProducts: [20, 400], nu: [1, 100], sigma: [0.1, 3], kappa: [0.5, 50], centreOffset: [-1.5, 1.5], replicates: [1, 50] } as const;
let cancelled = false;

function checked(s: Settings): Settings {
  for (const [k, [lo, hi]] of Object.entries(LIMITS)) {
    const v = s[k as keyof typeof LIMITS];
    if (!Number.isFinite(v) || v < lo || v > hi) throw new Error(`${k} must lie in [${lo}, ${hi}]`);
  }
  if (!Number.isInteger(s.seed) || s.seed < 1 || s.seed > 1_000_000) throw new Error("seed must be an integer in [1, 1000000]");
  return { ...s, nProducts: Math.round(s.nProducts), replicates: Math.round(s.replicates) };
}

async function simulate(raw: Settings, fixed: Fixed): Promise<SandboxOutput | null> {
  const s = checked(raw);
  const rows: ReturnType<typeof runOne>[] = [];
  for (let r = 0; r < s.replicates; r++) {
    rows.push(runOne(s, fixed, r));
    await new Promise((ok) => setTimeout(ok, 0)); // let a cancel message in
    if (cancelled) return null;
    postMessage({ type: "progress", fraction: (r + 1) / s.replicates } satisfies WorkerReply);
  }
  const by = (f: (x: (typeof rows)[number]) => number) => summariseReplicates(rows.map(f));
  return {
    settings: s,
    replicates: s.replicates,
    tauB: { MEAN: by((x) => x.arms.MEAN.tauB), SHRINK: by((x) => x.arms.SHRINK.tauB), LCB: by((x) => x.arms.LCB.tauB) },
    precision: { MEAN: by((x) => x.arms.MEAN.precision), SHRINK: by((x) => x.arms.SHRINK.precision), LCB: by((x) => x.arms.LCB.precision) },
    dShrink: by((x) => x.arms.SHRINK.tauB - x.arms.MEAN.tauB),
    dLcb: by((x) => x.arms.LCB.tauB - x.arms.MEAN.tauB),
    shareZero: by((x) => x.shareZero),
    products: rows[0].products,
  };
}

onmessage = async (ev: MessageEvent<WorkerRequest>) => {
  const m = ev.data;
  if (m.type === "cancel") {
    cancelled = true;
    return;
  }
  cancelled = false;
  try {
    const output = await simulate(m.settings, m.fixed);
    postMessage((output === null ? { type: "cancelled" } : { type: "done", output }) satisfies WorkerReply);
  } catch (e) {
    postMessage({ type: "error", message: e instanceof Error ? e.message : String(e) } satisfies WorkerReply);
  }
};
