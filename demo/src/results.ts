// SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
// Published results: loaded from public/data/results.json, which
// scripts/export_demo_data.py writes from committed results only.
// Validation fails closed: any missing or malformed field means no numbers are shown.

export const SCHEMA = "lab-demo-results";
export const SCHEMA_MAJOR = 1;

export interface Estimate {
  label: string;
  estimate: number;
  ci_low: number | null;
  ci_high: number | null;
  ci_level: number | null;
  unit: string;
  /** Exact text the manuscript prints for the estimate and interval; shown verbatim when present. */
  display: string | null;
  interval_display: string | null;
}

export interface Experiment {
  id: string;
  title: string;
  status: string;
  verdict: string;
  estimates: Estimate[];
  claim_ids: string[];
  report_path: string;
  notes: string[];
}

export interface Assumption {
  name: string;
  value: string;
  source: string;
}

export interface Source {
  path: string;
  sha256: string;
}

export interface Results {
  schema: string;
  schema_version: string;
  project: string;
  question: string;
  status_label: string;
  code_revision: string;
  sources: Source[];
  experiments: Experiment[];
  assumptions: Assumption[];
  limitations: string[];
  /** TRUST extension: dot-and-interval figures FIG-001 to FIG-003 from the frozen analysis. */
  figures: Figure[];
  /** TRUST extension: frozen EXP-001 parameters used as the sandbox defaults. */
  sandbox: SandboxParams;
}

export interface FigureRow extends Estimate {
  group: string;
  kind: "cell" | "summary" | "pooled";
}

export interface Figure {
  id: string;
  experiment: string;
  title: string;
  unit: string;
  rows: FigureRow[];
}

export interface SandboxParams {
  source: string;
  n_products: number;
  quality_beta: [number, number];
  nb_dispersion: number;
  lcb_z: number;
  lcb_prior: string;
  kappa_primary: number;
  top_k: number;
  nu_grid: number[];
  sigma_grid: number[];
}

export class ResultsError extends Error {}

type Obj = Record<string, unknown>;

function obj(v: unknown, where: string): Obj {
  if (typeof v !== "object" || v === null || Array.isArray(v)) {
    throw new ResultsError(`${where}: expected an object`);
  }
  return v as Obj;
}

function str(o: Obj, k: string, where: string): string {
  const v = o[k];
  if (typeof v !== "string" || v.length === 0) {
    throw new ResultsError(`${where}.${k}: expected a non-empty string`);
  }
  return v;
}

function num(o: Obj, k: string, where: string, nullable = false): number | null {
  const v = o[k];
  if (nullable && v === null) return null;
  if (typeof v !== "number" || !Number.isFinite(v)) {
    throw new ResultsError(`${where}.${k}: expected a finite number`);
  }
  return v;
}

function arr(o: Obj, k: string, where: string): unknown[] {
  const v = o[k];
  if (!Array.isArray(v)) throw new ResultsError(`${where}.${k}: expected an array`);
  return v;
}

function strArr(o: Obj, k: string, where: string): string[] {
  return arr(o, k, where).map((v, i) => {
    if (typeof v !== "string") throw new ResultsError(`${where}.${k}[${i}]: expected a string`);
    return v;
  });
}

function estimate(v: unknown, where: string): Estimate {
  const o = obj(v, where);
  const e: Estimate = {
    label: str(o, "label", where),
    estimate: num(o, "estimate", where) as number,
    ci_low: num(o, "ci_low", where, true),
    ci_high: num(o, "ci_high", where, true),
    ci_level: num(o, "ci_level", where, true),
    unit: typeof o.unit === "string" ? o.unit : "",
    display: typeof o.display === "string" ? o.display : null,
    interval_display: typeof o.interval_display === "string" ? o.interval_display : null,
  };
  if ((e.ci_low === null) !== (e.ci_high === null)) {
    throw new ResultsError(`${where}: interval must have both bounds or neither`);
  }
  if (e.ci_low !== null && e.ci_high !== null && e.ci_low > e.ci_high) {
    throw new ResultsError(`${where}: ci_low exceeds ci_high`);
  }
  return e;
}

export function validateResults(raw: unknown): Results {
  const o = obj(raw, "results");
  if (o.schema !== SCHEMA) throw new ResultsError(`results.schema: expected "${SCHEMA}"`);
  const version = str(o, "schema_version", "results");
  if (Number(version.split(".")[0]) !== SCHEMA_MAJOR) {
    throw new ResultsError(`results.schema_version: unsupported major version ${version}`);
  }
  const experiments = arr(o, "experiments", "results").map((v, i) => {
    const w = `experiments[${i}]`;
    const e = obj(v, w);
    return {
      id: str(e, "id", w),
      title: str(e, "title", w),
      status: str(e, "status", w),
      verdict: str(e, "verdict", w),
      estimates: arr(e, "estimates", w).map((x, j) => estimate(x, `${w}.estimates[${j}]`)),
      claim_ids: strArr(e, "claim_ids", w),
      report_path: str(e, "report_path", w),
      notes: strArr(e, "notes", w),
    };
  });
  if (experiments.length === 0) throw new ResultsError("results.experiments: empty");
  return {
    schema: SCHEMA,
    schema_version: version,
    project: str(o, "project", "results"),
    question: str(o, "question", "results"),
    status_label: str(o, "status_label", "results"),
    code_revision: str(o, "code_revision", "results"),
    sources: arr(o, "sources", "results").map((v, i) => {
      const s = obj(v, `sources[${i}]`);
      const sha = str(s, "sha256", `sources[${i}]`);
      if (!/^[0-9a-f]{64}$/.test(sha)) throw new ResultsError(`sources[${i}].sha256: not a sha256`);
      return { path: str(s, "path", `sources[${i}]`), sha256: sha };
    }),
    experiments,
    assumptions: arr(o, "assumptions", "results").map((v, i) => {
      const a = obj(v, `assumptions[${i}]`);
      return {
        name: str(a, "name", `assumptions[${i}]`),
        value: str(a, "value", `assumptions[${i}]`),
        source: str(a, "source", `assumptions[${i}]`),
      };
    }),
    limitations: strArr(o, "limitations", "results"),
    figures: figures(o),
    sandbox: sandboxParams(o),
  };
}

const KINDS = ["cell", "summary", "pooled"] as const;

function figures(o: Obj): Figure[] {
  const figs = arr(o, "figures", "results").map((v, i) => {
    const w = `figures[${i}]`;
    const f = obj(v, w);
    const rows = arr(f, "rows", w).map((x, j) => {
      const wr = `${w}.rows[${j}]`;
      const r = obj(x, wr);
      const e = estimate(r, wr);
      if (e.ci_low === null || e.display === null || e.interval_display === null) {
        throw new ResultsError(`${wr}: a figure row needs an interval and its display text`);
      }
      const kind = str(r, "kind", wr);
      if (!(KINDS as readonly string[]).includes(kind)) throw new ResultsError(`${wr}.kind: unknown kind`);
      return { ...e, group: str(r, "group", wr), kind: kind as FigureRow["kind"] };
    });
    if (rows.length === 0) throw new ResultsError(`${w}.rows: empty`);
    const id = str(f, "id", w);
    if (!/^FIG-\d{3}$/.test(id)) throw new ResultsError(`${w}.id: not a FIG-NNN id`);
    return { id, experiment: str(f, "experiment", w), title: str(f, "title", w), unit: str(f, "unit", w), rows };
  });
  if (figs.length === 0) throw new ResultsError("results.figures: empty");
  return figs;
}

function numArr(o: Obj, k: string, where: string): number[] {
  const a = arr(o, k, where).map((v, i) => num({ v }, "v", `${where}.${k}[${i}]`) as number);
  if (a.length === 0) throw new ResultsError(`${where}.${k}: empty`);
  return a;
}

function sandboxParams(o: Obj): SandboxParams {
  const w = "sandbox";
  const s = obj(o.sandbox, w);
  const pos = (k: string) => {
    const v = num(s, k, w) as number;
    if (v <= 0) throw new ResultsError(`${w}.${k}: must be positive`);
    return v;
  };
  const qb = numArr(s, "quality_beta", w);
  if (qb.length !== 2 || qb.some((x) => x <= 0)) throw new ResultsError(`${w}.quality_beta: two positive numbers expected`);
  const n = pos("n_products");
  if (!Number.isInteger(n) || n < 2 || n > 1000) throw new ResultsError(`${w}.n_products: integer in [2, 1000] expected`);
  return {
    source: str(s, "source", w),
    n_products: n,
    quality_beta: [qb[0], qb[1]],
    nb_dispersion: pos("nb_dispersion"),
    lcb_z: pos("lcb_z"),
    lcb_prior: str(s, "lcb_prior", w),
    kappa_primary: pos("kappa_primary"),
    top_k: pos("top_k"),
    nu_grid: numArr(s, "nu_grid", w),
    sigma_grid: numArr(s, "sigma_grid", w),
  };
}

export async function loadResults(url = "./data/results.json"): Promise<Results> {
  const res = await fetch(url, { cache: "no-store" });
  if (!res.ok) throw new ResultsError(`could not load ${url} (HTTP ${res.status})`);
  let raw: unknown;
  try {
    raw = await res.json();
  } catch {
    throw new ResultsError(`${url} is not valid JSON`);
  }
  return validateResults(raw);
}

/** Formats a number for display without inventing precision. */
export function fmt(x: number, digits = 3): string {
  if (Number.isInteger(x)) return x.toString();
  return Number(x.toPrecision(digits)).toString();
}

export function fmtEstimate(e: Estimate, digits = 3): string {
  return e.display ?? `${fmt(e.estimate, digits)}${e.unit ? " " + e.unit : ""}`;
}

export function fmtInterval(e: Estimate, digits = 3): string {
  if (e.interval_display !== null) return e.interval_display;
  if (e.ci_low === null || e.ci_high === null) return "no interval";
  const level = e.ci_level === null ? "" : `${Math.round(e.ci_level * 100)}% `;
  return `${level}[${fmt(e.ci_low, digits)}, ${fmt(e.ci_high, digits)}]`;
}
