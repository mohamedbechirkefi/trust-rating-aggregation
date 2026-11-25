// SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
// Hand-written SVG charts. The SVG is drawn at the measured pixel width of its container (no
// viewBox scaling), so text keeps its size on a phone.
import { useEffect, useRef, useState, type ReactNode } from "react";
import type { Figure } from "./results";
import type { ProductRow } from "./sandboxRun";

export function useWidth<T extends HTMLElement>(): [React.RefObject<T | null>, number] {
  const ref = useRef<T | null>(null);
  const [w, setW] = useState(640);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const update = () => setW(Math.max(260, Math.floor(el.getBoundingClientRect().width)));
    update();
    const ro = new ResizeObserver(update);
    ro.observe(el);
    return () => ro.disconnect();
  }, []);
  return [ref, w];
}

function niceTicks(lo: number, hi: number, n = 5): number[] {
  const span = hi - lo || 1;
  const raw = span / n;
  const mag = 10 ** Math.floor(Math.log10(raw));
  const step = [1, 2, 2.5, 5, 10].map((m) => m * mag).find((s) => span / s <= n) ?? 10 * mag;
  const out: number[] = [];
  for (let t = Math.ceil(lo / step) * step; t <= hi + 1e-12; t += step) out.push(Number(t.toFixed(10)));
  return out;
}

function tickLabel(t: number): string {
  if (t === 0) return "0";
  return Math.abs(t) < 0.1 ? t.toFixed(3).replace(/0+$/, "").replace(/\.$/, "") : t.toFixed(2).replace(/0+$/, "").replace(/\.$/, "");
}

/** Plain-language summary computed from the data shown (no other numbers). */
export function describeIntervals(rows: { ci_low: number | null; ci_high: number | null }[]): string {
  const below = rows.filter((r) => r.ci_high !== null && r.ci_high < 0).length;
  const above = rows.filter((r) => r.ci_low !== null && r.ci_low > 0).length;
  const across = rows.length - below - above;
  const n = (k: number, one: string, many: string) => `${k} ${k === 1 ? one : many}`;
  return `${rows.length} rows: ${n(above, "interval lies", "intervals lie")} entirely above zero (the arm ranks better than MEAN), ${n(below, "lies", "lie")} entirely below zero (worse than MEAN), and ${n(across, "includes", "include")} zero.`;
}

export function ForestChart({ fig }: { fig: Figure }) {
  const [ref, width] = useWidth<HTMLDivElement>();
  const narrow = width < 560;
  const labelW = narrow ? 0 : Math.min(260, Math.round(width * 0.38));
  const rowH = narrow ? 44 : 26;
  const top = 8, axisH = 40, padR = 16;
  const lo = Math.min(0, ...fig.rows.map((r) => r.ci_low as number));
  const hi = Math.max(0, ...fig.rows.map((r) => r.ci_high as number));
  const pad = (hi - lo) * 0.06;
  const x0 = lo - pad, x1 = hi + pad;
  const plotL = labelW + 8, plotR = width - padR;
  const sx = (v: number) => plotL + ((v - x0) / (x1 - x0)) * (plotR - plotL);
  const height = top + fig.rows.length * rowH + axisH;
  const ticks = niceTicks(x0, x1);
  return (
    <div ref={ref} className="chart">
      <svg width={width} height={height} role="img" aria-label={`${fig.id}: ${fig.title}. ${describeIntervals(fig.rows)}`}>
        {ticks.map((t) => (
          <g key={t}>
            <line x1={sx(t)} x2={sx(t)} y1={top} y2={height - axisH} className="grid" />
            <text x={sx(t)} y={height - axisH + 15} textAnchor="middle" className="tick">{tickLabel(t)}</text>
          </g>
        ))}
        <line x1={sx(0)} x2={sx(0)} y1={top} y2={height - axisH} className="zero" />
        <text x={(plotL + plotR) / 2} y={height - 4} textAnchor="middle" className="axis-label">{fig.unit}; dashed line at zero</text>
        {fig.rows.map((r, i) => {
          const yMid = top + i * rowH + (narrow ? 30 : rowH / 2);
          return (
            <g key={r.label} className={`row ${r.kind}`}>
              <text x={narrow ? plotL : labelW} y={narrow ? yMid - 14 : yMid + 4} textAnchor={narrow ? "start" : "end"} className={narrow ? "row-label halo" : "row-label"}>
                {r.label}
              </text>
              <line x1={sx(r.ci_low as number)} x2={sx(r.ci_high as number)} y1={yMid} y2={yMid} className="ci" />
              <line x1={sx(r.ci_low as number)} x2={sx(r.ci_low as number)} y1={yMid - 4} y2={yMid + 4} className="ci" />
              <line x1={sx(r.ci_high as number)} x2={sx(r.ci_high as number)} y1={yMid - 4} y2={yMid + 4} className="ci" />
              {r.kind === "pooled" ? (
                <path d={`M${sx(r.estimate)},${yMid - 6}l6,6l-6,6l-6,-6z`} className="pt" />
              ) : (
                <circle cx={sx(r.estimate)} cy={yMid} r={r.kind === "summary" ? 5 : 3.5} className="pt" />
              )}
            </g>
          );
        })}
      </svg>
    </div>
  );
}

export type OrderBy = "mean" | "shrink" | "lcb" | "theta";

/** Rating explorer: per product, MEAN and SHRINK estimates with nominal 90% intervals, the LCB score and the simulated truth. */
export function ExplorerChart({ rows, kappa, legend }: { rows: ProductRow[]; kappa: number; legend: ReactNode }) {
  const [ref, width] = useWidth<HTMLDivElement>();
  const labelW = width < 480 ? 92 : 120;
  const rowH = 30, top = 6, axisH = 36, padR = 14;
  const plotL = labelW + 6, plotR = width - padR;
  // Domain: the half-star grid around the values shown, within 0.5 to 5.5 stars.
  const vals = rows.flatMap((p) => [p.meanLo, p.meanHi, p.shrinkLo, p.shrinkHi, p.lcb, p.theta, p.mean, p.shrink]).filter(Number.isFinite);
  const d0 = Math.max(0.5, Math.floor(Math.min(...vals) * 2) / 2), d1 = Math.min(5.5, Math.ceil(Math.max(...vals) * 2) / 2);
  const sx = (v: number) => plotL + ((Math.min(Math.max(v, d0), d1) - d0) / (d1 - d0 || 1)) * (plotR - plotL);
  const ticks: number[] = [];
  for (let t = Math.ceil(d0 * 2) / 2; t <= d1 + 1e-9; t += 0.5) ticks.push(t);
  const height = top + rows.length * rowH + axisH;
  return (
    <div ref={ref} className="chart">
      {legend}
      <svg width={width} height={height} role="img"
        aria-label={`Rating explorer for ${rows.length} products: for each product, the average rating and SHRINK_${kappa} estimates with nominal 90% intervals, the LCB score and the simulated true quality, on a scale of stars. The table below lists the same values.`}>
        {ticks.map((t) => (
          <g key={t}>
            <line x1={sx(t)} x2={sx(t)} y1={top} y2={height - axisH} className="grid" />
            <text x={sx(t)} y={height - axisH + 16} textAnchor="middle" className="tick">{Number.isInteger(t) || width >= 480 ? t.toFixed(1) : ""}</text>
          </g>
        ))}
        <text x={(plotL + plotR) / 2} y={height - 4} textAnchor="middle" className="axis-label">{width < 480 ? "stars (sandbox, simulated)" : "stars (sandbox output, simulated)"}</text>
        {rows.map((p, i) => {
          const y = top + i * rowH + rowH / 2;
          return (
            <g key={p.id}>
              <text x={labelW} y={y + 4} textAnchor="end" className="row-label">#{p.id} · n {p.n}</text>
              {Number.isFinite(p.meanLo) && <line x1={sx(p.meanLo)} x2={sx(p.meanHi)} y1={y - 5} y2={y - 5} className="ci mean" />}
              <circle cx={sx(p.mean)} cy={y - 5} r={4} className="pt mean" />
              {Number.isFinite(p.shrinkLo) && <line x1={sx(p.shrinkLo)} x2={sx(p.shrinkHi)} y1={y + 5} y2={y + 5} className="ci shrink" />}
              <path d={`M${sx(p.shrink)},${y + 0.5}l4.5,4.5l-4.5,4.5l-4.5,-4.5z`} className="pt shrink" />
              <path d={`M${sx(p.lcb)},${y - 4}l4,7h-8z`} className="pt lcb" />
              <line x1={sx(p.theta)} x2={sx(p.theta)} y1={y - 11} y2={y + 11} className="truth" />
            </g>
          );
        })}
      </svg>
    </div>
  );
}

/** A details element whose content is rendered only while open, so closed content holds no tab stops. */
export function Disclosure({ summary, children }: { summary: ReactNode; children: ReactNode }) {
  const [open, setOpen] = useState(false);
  return (
    <details onToggle={(e) => setOpen((e.currentTarget as HTMLDetailsElement).open)}>
      <summary>{summary}</summary>
      {open && children}
    </details>
  );
}
