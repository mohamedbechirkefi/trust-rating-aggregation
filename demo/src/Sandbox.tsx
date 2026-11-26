// SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
// Visitor sandbox: the rating explorer. Runs the browser port of the engine in a Web Worker.
// Its output is labelled as sandbox output and never mixed with the published results.
import { useEffect, useMemo, useRef, useState } from "react";
import type { SandboxParams } from "./results";
import { QUALITIES, type Fixed, type ProductRow, type Settings } from "./sandboxRun";
import type { SandboxOutput, Summary, WorkerReply, WorkerRequest } from "./sandbox.worker";
import { Disclosure, ExplorerChart, type OrderBy } from "./Charts";
import { Seg } from "./Seg";

const f3 = (x: number) => (Number.isFinite(x) ? x.toFixed(3) : "undefined");
const f4 = (x: number) => (Number.isFinite(x) ? x.toFixed(4) : "undefined");
const withCi = (s: Summary, f = f3) => (s.lo === null || s.hi === null ? `${f(s.mean)} (one replicate, no interval)` : `${f(s.mean)} (95% t interval ${f(s.lo)} to ${f(s.hi)})`);

const ORDER_LABEL: Record<OrderBy, string> = {
  mean: "average rating (MEAN)",
  shrink: "shrinkage (SHRINK)",
  lcb: "lower credible bound (LCB)",
  theta: "simulated true quality",
};

const ORDER_SHORT: Record<OrderBy, string> = {
  mean: "Average (MEAN)",
  shrink: "Shrinkage (SHRINK)",
  lcb: "Lower bound (LCB)",
  theta: "True quality",
};

function topBy(products: ProductRow[], key: OrderBy, k: number): ProductRow[] {
  return [...products].sort((a, b) => b[key] - a[key] || a.id - b.id).slice(0, k);
}

export function Sandbox({ params }: { params: SandboxParams }) {
  const defaults = useMemo<Settings>(
    () => ({ nProducts: params.n_products, nu: 10, sigma: 1.0, kappa: params.kappa_primary, centreOffset: 0, quality: "calibrated", seed: 1, replicates: 1 }),
    [params],
  );
  const fixed: Fixed = { qualityBeta: params.quality_beta, nbDispersion: params.nb_dispersion, lcbZ: params.lcb_z, topK: params.top_k };
  const worker = useRef<Worker | null>(null);
  const [s, setS] = useState<Settings>(defaults);
  const [running, setRunning] = useState(false);
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState("");
  const [out, setOut] = useState<SandboxOutput | null>(null);
  const [order, setOrder] = useState<OrderBy>("mean");
  const outRef = useRef<HTMLParagraphElement>(null);
  // A returned run settles in: opacity and a short rise, opacity only under reduced motion.
  useEffect(() => {
    const el = outRef.current;
    if (!el || !status || typeof el.animate !== "function") return;
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    el.animate(
      reduce ? [{ opacity: 0 }, { opacity: 1 }] : [{ opacity: 0, transform: "translateY(6px)" }, { opacity: 1, transform: "none" }],
      { duration: 240, easing: "cubic-bezier(0.23, 1, 0.32, 1)" },
    );
  }, [status]);

  useEffect(() => {
    const w = new Worker(new URL("./sandbox.worker.ts", import.meta.url), { type: "module" });
    w.onmessage = (ev: MessageEvent<WorkerReply>) => {
      const m = ev.data;
      if (m.type === "progress") setProgress(m.fraction);
      if (m.type === "done") {
        setOut(m.output);
        const o = m.output;
        setStatus(
          `Sandbox output (seed ${o.settings.seed}, ${o.replicates} replicate${o.replicates === 1 ? "" : "s"}): ` +
            `tau-b of SHRINK minus MEAN ${withCi(o.dShrink, f4)}.`,
        );
      }
      if (m.type === "error") setStatus(`Sandbox run failed: ${m.message}`);
      if (m.type === "cancelled") setStatus("Sandbox run cancelled.");
      if (m.type !== "progress") setRunning(false);
    };
    worker.current = w;
    return () => w.terminate();
  }, []);

  const set = <K extends keyof Settings>(k: K, v: Settings[K]) => setS((p) => ({ ...p, [k]: v }));
  const run = () => {
    setRunning(true);
    setProgress(0);
    setStatus("");
    worker.current?.postMessage({ type: "run", settings: s, fixed } satisfies WorkerRequest);
  };
  const cancel = () => worker.current?.postMessage({ type: "cancel" } satisfies WorkerRequest);
  const reset = () => {
    if (running) cancel();
    setS(defaults);
    setOut(null);
    setOrder("mean");
    setStatus("Settings reset to the defaults.");
  };
  const scenario = params.nu_grid.flatMap((nu) => params.sigma_grid.map((sigma) => ({ nu, sigma })));
  const scenarioValue = scenario.find((c) => c.nu === s.nu && c.sigma === s.sigma && s.kappa === params.kappa_primary && s.centreOffset === 0 && s.quality === "calibrated" && s.nProducts === params.n_products);

  const download = () => {
    if (!out) return;
    const blob = new Blob([JSON.stringify({ label: "TRUST sandbox output (browser, simulated; not a research result)", ...out }, null, 1)], { type: "application/json" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = `trust-sandbox-seed${out.settings.seed}.json`;
    a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 1000);
  };

  const slider = (k: "nProducts" | "nu" | "sigma" | "kappa" | "centreOffset", label: string, min: number, max: number, step: number, unit: string, fmt: (v: number) => string) => (
    <div className="field">
      <label htmlFor={`sb-${k}`}>{label}</label>
      <input id={`sb-${k}`} type="range" min={min} max={max} step={step} value={s[k]}
        aria-valuetext={`${fmt(s[k])} ${unit}`} onChange={(e) => set(k, Number(e.target.value))} />
      <output htmlFor={`sb-${k}`}>{fmt(s[k])} {unit}</output>
    </div>
  );

  const k = out ? Math.min(12, out.products.length) : 0;
  const shown = out ? topBy(out.products, order, k) : [];
  const kappaOut = out?.settings.kappa ?? s.kappa;

  return (
    <section id="sandbox" aria-labelledby="h-sandbox" className="sandbox">
      <p className="label-chip sandbox-chip">Sandbox output</p>
      <h2 id="h-sandbox">Rating explorer (sandbox)</h2>
      <p className="note">
        Everything in this panel is produced in your browser from your settings. It is not a research result, is not
        comparable to the published numbers above, and nothing is sent anywhere. The estimators, intervals, truth and
        metrics are an exact port of the research engine (checked against it to 1e-12); the random-number generator is
        different, so a seed here does not reproduce a catalogue of the study. Its catalogues match the study's in
        distribution (tested on the nine EXP-001 cells). This sandbox models random reporting only (no selection or
        exposure coupling).
      </p>
      <form className="controls" onSubmit={(e) => { e.preventDefault(); run(); }}>
        <div className="field wide">
          <label htmlFor="sb-scenario">Scenario</label>
          <select id="sb-scenario" value={scenarioValue ? `${scenarioValue.nu}|${scenarioValue.sigma}` : "custom"}
            onChange={(e) => {
              if (e.target.value === "custom") return;
              const [nu, sigma] = e.target.value.split("|").map(Number);
              setS((p) => ({ ...p, nu, sigma, kappa: params.kappa_primary, centreOffset: 0, quality: "calibrated", nProducts: params.n_products }));
            }}>
            <option value="custom">Custom (the sliders below)</option>
            {scenario.map((c) => (
              <option key={`${c.nu}|${c.sigma}`} value={`${c.nu}|${c.sigma}`}>
                EXP-001 settings: nu {c.nu}, sigma {c.sigma.toFixed(1)}
              </option>
            ))}
          </select>
        </div>
        {slider("nu", "Mean review count per product (nu)", 1, 100, 1, "reviews", (v) => v.toFixed(0))}
        {slider("nProducts", "Catalogue size", 20, 400, 20, "products", (v) => v.toFixed(0))}
        {slider("sigma", "Rating noise (sigma)", 0.1, 3, 0.05, "stars", (v) => v.toFixed(2))}
        {slider("kappa", "Shrinkage strength (kappa)", 0.5, 50, 0.5, "pseudo-reviews", (v) => v.toFixed(1))}
        {slider("centreOffset", "Shrinkage centre offset", -1.5, 1.5, 0.1, "stars from the catalogue mean", (v) => (v > 0 ? "+" : "") + v.toFixed(1))}
        <div className="field wide">
          <label htmlFor="sb-quality">Quality population</label>
          <select id="sb-quality" value={s.quality} onChange={(e) => set("quality", e.target.value as Settings["quality"])}>
            {Object.entries(QUALITIES).map(([key, v]) => (
              <option key={key} value={key}>{v.label}</option>
            ))}
          </select>
        </div>
        <div className="field">
          <label htmlFor="sb-seed">Seed</label>
          <input id="sb-seed" type="number" min={1} max={1_000_000} step={1} value={s.seed}
            onChange={(e) => set("seed", Math.min(1_000_000, Math.max(1, Math.round(Number(e.target.value) || 1))))} />
        </div>
        <div className="field">
          <label htmlFor="sb-reps">Replicate catalogues</label>
          <input id="sb-reps" type="number" min={1} max={50} step={1} value={s.replicates}
            onChange={(e) => set("replicates", Math.min(50, Math.max(1, Math.round(Number(e.target.value) || 1))))} />
        </div>
        <div className="buttons">
          <button type="submit" className="primary" disabled={running}>Run</button>
          <button type="button" onClick={cancel} disabled={!running}>Cancel</button>
          <button type="button" onClick={reset}>Reset</button>
          <button type="button" onClick={download} disabled={!out || running}>Download output (JSON)</button>
        </div>
      </form>
      {running && <progress max={1} value={progress} aria-label="Sandbox progress" />}
      <p aria-live="polite" className="sandbox-out" ref={outRef}>{status}</p>
      {!out && !running && <p className="note">No sandbox output yet. Choose settings and press Run.</p>}
      {out && (
        <>
          <div id="sb-metrics" className="table-scroll" role="region" aria-label="Sandbox metrics" tabIndex={0}>
            <table className="stack">
              <caption>
                Sandbox output: rank recovery against the simulated truth, {out.replicates} catalogue{out.replicates === 1 ? "" : "s"} of{" "}
                {out.settings.nProducts} products. Share of products with no review: {withCi(out.shareZero)}.
              </caption>
              <thead>
                <tr><th scope="col">Arm</th><th scope="col">Kendall tau-b</th><th scope="col">Precision at {Math.min(params.top_k, out.settings.nProducts)}</th></tr>
              </thead>
              <tbody>
                <tr><th scope="row">MEAN</th><td data-label="Kendall tau-b">{withCi(out.tauB.MEAN)}</td><td data-label={`Precision at ${Math.min(params.top_k, out.settings.nProducts)}`}>{withCi(out.precision.MEAN)}</td></tr>
                <tr><th scope="row">SHRINK (kappa {out.settings.kappa})</th><td data-label="Kendall tau-b">{withCi(out.tauB.SHRINK)}</td><td data-label={`Precision at ${Math.min(params.top_k, out.settings.nProducts)}`}>{withCi(out.precision.SHRINK)}</td></tr>
                <tr><th scope="row">LCB</th><td data-label="Kendall tau-b">{withCi(out.tauB.LCB)}</td><td data-label={`Precision at ${Math.min(params.top_k, out.settings.nProducts)}`}>{withCi(out.precision.LCB)}</td></tr>
                <tr><th scope="row">SHRINK minus MEAN</th><td data-label="Kendall tau-b">{withCi(out.dShrink, f4)}</td><td data-label="Precision">not computed</td></tr>
                <tr><th scope="row">LCB minus MEAN</th><td data-label="Kendall tau-b">{withCi(out.dLcb, f4)}</td><td data-label="Precision">not computed</td></tr>
              </tbody>
            </table>
          </div>

          <h3>Products under the lens</h3>
          <div className="order-row">
            <Seg<OrderBy>
              title={`Show the top ${k} products ranked by`}
              ariaLabel="Rank the products shown by"
              value={order}
              onChange={setOrder}
              items={(Object.keys(ORDER_LABEL) as OrderBy[]).map((o) => ({ value: o, label: ORDER_SHORT[o], id: `sb-order-${o}` }))}
            />
          </div>
          <p className="note">
            First replicate catalogue. Intervals are the nominal 90% intervals of the research engine; an interval reaching past the axis is cut at its edge. With few reviews
            the average rating swings to the ends of the scale; shrinkage pulls it towards the catalogue mean.
          </p>
          <ExplorerChart rows={shown} kappa={kappaOut} legend={
            <ul className="legend" aria-label="Chart legend">
              <li><span className="key mean" aria-hidden="true">●</span> MEAN with interval</li>
              <li><span className="key shrink" aria-hidden="true">◆</span> SHRINK (kappa {kappaOut}) with interval</li>
              <li><span className="key lcb" aria-hidden="true">▲</span> LCB score</li>
              <li><span className="key truth" aria-hidden="true">|</span> simulated true quality</li>
            </ul>
          } />
          <Disclosure summary={<>Table of the products shown</>}>
            <div id="sb-products" className="table-scroll" role="region" aria-label="Products shown" tabIndex={0}>
              <table className="stack">
                <thead>
                  <tr><th scope="col">Product</th><th scope="col">Reviews</th><th scope="col">MEAN (90%)</th><th scope="col">SHRINK (90%)</th><th scope="col">LCB</th><th scope="col">True quality</th><th scope="col">True rank</th></tr>
                </thead>
                <tbody>
                  {shown.map((p) => (
                    <tr key={p.id}>
                      <th scope="row">#{p.id}</th><td data-label="Reviews">{p.n}</td>
                      <td data-label="MEAN (90%)">{f3(p.mean)} ({f3(p.meanLo)} to {f3(p.meanHi)})</td>
                      <td data-label="SHRINK (90%)">{f3(p.shrink)} ({f3(p.shrinkLo)} to {f3(p.shrinkHi)})</td>
                      <td data-label="LCB">{f3(p.lcb)}</td><td data-label="True quality">{f3(p.theta)}</td><td data-label="True rank">{p.trueRank}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Disclosure>

          <h3>Ranking comparison</h3>
          <div id="sb-ranks" className="table-scroll" role="region" aria-label="Ranking comparison" tabIndex={0}>
            <table className="ranks stack">
              <caption>Top 10 under each rule (first replicate). Each cell gives the product and, in brackets, its true rank; 1 to 10 is a correct pick.</caption>
              <thead>
                <tr><th scope="col">Position</th><th scope="col">MEAN</th><th scope="col">SHRINK</th><th scope="col">LCB</th><th scope="col">Truth</th></tr>
              </thead>
              <tbody>
                {Array.from({ length: Math.min(10, out.products.length) }, (_, i) => {
                  const cols = (["mean", "shrink", "lcb", "theta"] as OrderBy[]).map((o) => topBy(out.products, o, 10)[i]);
                  return (
                    <tr key={i}>
                      <th scope="row">{i + 1}</th>
                      {cols.map((p, j) => (
                        <td key={j} data-label={["MEAN", "SHRINK", "LCB", "Truth"][j]} className={p.trueRank <= 10 ? "hit" : "miss"}>
                          #{p.id} [{p.trueRank}]{p.trueRank <= 10 ? "" : " (outside true top 10)"}
                        </td>
                      ))}
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </>
      )}
    </section>
  );
}
