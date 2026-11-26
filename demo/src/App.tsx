// SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
import { useEffect, useState } from "react";
import { fmtEstimate, fmtInterval, loadResults, ResultsError, type Results } from "./results";
import { Sandbox } from "./Sandbox";
import { describeIntervals, Disclosure, ForestChart } from "./Charts";

type State = { kind: "loading" } | { kind: "error"; message: string } | { kind: "ready"; results: Results };

export function App() {
  const [state, setState] = useState<State>({ kind: "loading" });

  useEffect(() => {
    loadResults()
      .then((results) => setState({ kind: "ready", results }))
      .catch((e: unknown) =>
        setState({ kind: "error", message: e instanceof ResultsError ? e.message : "results could not be loaded" }),
      );
  }, []);

  return (
    <>
      <a className="skip" href="#main">Skip to content</a>
      <header className="site">
        <div className="wrap">
          <p className="kicker">TRUST · a preregistered simulation study of rating aggregation</p>
          <h1>When do average ratings misrank products compared with uncertainty-aware estimators?</h1>
          <nav aria-label="Sections">
            <a href="#overview">Overview</a>
            <a href="#results">Results</a>
            <a href="#assumptions">Assumptions</a>
            <a href="#method">Method and limitations</a>
            <a href="#sandbox">Rating explorer</a>
          </nav>
        </div>
      </header>
      <main id="main" className="wrap">
        {state.kind === "loading" && <p role="status">Loading the published results.</p>}
        {state.kind === "error" && (
          <div role="alert" className="panel error">
            <h2>Results unavailable</h2>
            <p>The published results file failed validation, so no numbers are shown and the sandbox is not started.</p>
            <p><code>{state.message}</code></p>
          </div>
        )}
        {state.kind === "ready" && (
          <>
            <Published r={state.results} />
            <Sandbox params={state.results.sandbox} />
          </>
        )}
      </main>
      <footer className="site">
        <div className="wrap">
          <p>
            Runs offline after the first load. No data about visitors is collected, stored or sent anywhere. All results
            are simulated; real product quality is unobserved, nothing here describes any real platform, and nothing
            labels any review as fraudulent. Mohamed Bechir Kefi, independent researcher. Repository:{" "}
            <a href="https://github.com/mohamedbechirkefi/trust-rating-aggregation">https://github.com/mohamedbechirkefi/trust-rating-aggregation</a>.
          </p>
        </div>
      </footer>
    </>
  );
}

function Published({ r }: { r: Results }) {
  return (
    <>
      <section id="overview" aria-labelledby="h-overview">
        <h2 id="h-overview">Overview</h2>
        <p className="status-label">{r.status_label}</p>
        <p className="lede">
          In this simulation, shrinking each product's average towards the catalogue mean ranked products better than the
          plain average when individual ratings were noisy, and worse when they were precise. The advantage reversed when
          the shrinkage centre or the shape of the quality population was misspecified. The frozen rule declares the
          primary hypothesis supported, but the informative statement is this conditional one.
        </p>
        <ul className="labels" aria-label="How values are labelled on this page">
          <li><span className="label-chip published-chip">Published result</span> measured in the preregistered simulation, copied from the committed results.</li>
          <li><span className="label-chip assumption-chip">Assumption</span> a model input chosen or calibrated before the runs, not a finding.</li>
          <li><span className="label-chip sandbox-chip">Sandbox output</span> computed in your browser from your settings; never a research result.</li>
        </ul>
      </section>

      <section id="results" aria-labelledby="h-results">
        <p className="label-chip published-chip">Published result</p>
        <h2 id="h-results">Published results</h2>
        <p className="note">
          Numbers come from the committed results of runs at revision <code>{r.code_revision.slice(0, 7)}</code> and are
          printed exactly as in the manuscript. Effects are differences in Kendall tau-b between an arm and MEAN
          (positive: the arm recovers the true order better). Every interval is a two-sided 95% bootstrap interval over
          seeds. Supported, contradicted, null and non-diagnostic results are shown with the same weight.
        </p>
        {r.figures.map((f) => (
          <figure key={f.id} className="panel fig" aria-labelledby={`cap-${f.id}`}>
            <ForestChart fig={f} />
            <figcaption id={`cap-${f.id}`}>
              <strong>{f.id} ({f.experiment}).</strong> {f.title}. Dots are means and bars 95% intervals
              {f.rows.some((x) => x.kind === "pooled") ? "; diamonds mark pooled estimates" : ""}. {describeIntervals(f.rows)} Simulated.
            </figcaption>
            <Disclosure summary={<>Data for {f.id}</>}>
              <div id={`data-${f.id}`} className="table-scroll" role="region" aria-label={`${f.id} data`} tabIndex={0}>
                <table className="stack">
                  <thead><tr><th scope="col">Row</th><th scope="col">Estimate</th><th scope="col">95% interval</th></tr></thead>
                  <tbody>
                    {f.rows.map((x) => (
                      <tr key={x.label}><th scope="row">{x.label}</th><td data-label="Estimate">{fmtEstimate(x)}</td><td data-label="95% interval">{fmtInterval(x)}</td></tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </Disclosure>
          </figure>
        ))}
        {r.experiments.map((e) => (
          <article key={e.id} className={`panel exp ${e.status.startsWith("exploratory") ? "exploratory" : ""}`} aria-labelledby={`h-${e.id}`}>
            <h3 id={`h-${e.id}`}>
              {e.id}: {e.title}
            </h3>
            <p>
              <span className="badge">{e.status}</span>{" "}
              <strong>{e.status.startsWith("exploratory") ? "Verdict:" : "Verdict under the frozen rule:"}</strong> {e.verdict}
            </p>
            {e.estimates.length > 0 && (
              <div id={`est-${e.id}`} className="table-scroll" role="region" aria-label={`${e.id} estimates`} tabIndex={0}>
                <table className="stack">
                  <thead>
                    <tr>
                      <th scope="col">Quantity</th>
                      <th scope="col">Estimate</th>
                      <th scope="col">95% interval</th>
                      <th scope="col">Unit</th>
                    </tr>
                  </thead>
                  <tbody>
                    {e.estimates.map((x) => (
                      <tr key={x.label}>
                        <th scope="row">{x.label}</th>
                        <td data-label="Estimate">{fmtEstimate(x)}</td>
                        <td data-label="95% interval">{x.ci_low === null ? "no interval (a bound or decision quantity)" : fmtInterval(x)}</td>
                        <td data-label="Unit">{x.unit}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
            {e.notes.map((n, i) => (
              <p key={i} className="note">{n}</p>
            ))}
            <p className="meta">
              Report: <code>{e.report_path}</code>
              {e.claim_ids.length > 0 && <> · Claims: {e.claim_ids.join(", ")}</>}
            </p>
          </article>
        ))}
      </section>

      <section id="assumptions" aria-labelledby="h-assumptions">
        <p className="label-chip assumption-chip">Assumption</p>
        <h2 id="h-assumptions">Assumptions</h2>
        <p className="note">Model inputs, fixed before the confirmatory runs. They are not findings.</p>
        <dl className="assumptions">
          {r.assumptions.map((a) => (
            <div key={a.name}>
              <dt>{a.name}</dt>
              <dd>
                {a.value} <span className="meta">({a.source})</span>
              </dd>
            </div>
          ))}
        </dl>
      </section>

      <section id="method" aria-labelledby="h-method">
        <h2 id="h-method">Method and limitations</h2>
        <p>
          Three experiments were registered and their protocols frozen by the owner on 2026-11-24, with file hashes,
          before any confirmatory run. Each simulated catalogue is scored by every arm (paired design), and every arm is
          compared with the simulated truth. All 1,560 runs completed. Two deviations were accepted by the owner with
          disclosure: bootstrap p-values for the Holm families (D-011), and the finding that sensitivity check S3 cannot
          discriminate by design (D-012).
        </p>
        <h3>Limitations</h3>
        <ul>
          {r.limitations.map((l, i) => (
            <li key={i}>{l}</li>
          ))}
        </ul>
        <Disclosure summary={<>Source files and hashes</>}>
          <ul className="meta">
            {r.sources.map((s) => (
              <li key={s.path}>
                <code>{s.path}</code> <code>{s.sha256.slice(0, 12)}</code>
              </li>
            ))}
          </ul>
        </Disclosure>
      </section>
    </>
  );
}
