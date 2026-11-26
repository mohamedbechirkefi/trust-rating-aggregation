// SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
// The key result as a test-lab verdict label: SHRINK_5 minus MEAN in Kendall
// tau-b at each rating-noise level (EXP-001, A-2), with its 95% interval, on a
// shared zero axis. Every number and string comes from the exported results.
import { fmtEstimate, fmtInterval, type Estimate, type Results } from "./results";
import { useReveal } from "./useReveal";

const LEVELS = [
  { label: "D_sigma at sigma 0.5 stars (A-2)", name: "Precise ratings", noise: "noise 0.5 stars" },
  { label: "D_sigma at sigma 1.0 stars (A-2)", name: "Moderate noise", noise: "noise 1.0 stars" },
  { label: "D_sigma at sigma 1.5 stars (A-2)", name: "Noisy ratings", noise: "noise 1.5 stars" },
];

export function Verdict({ r }: { r: Results }) {
  const exp = r.experiments.find((e) => e.id === "EXP-001");
  const rows = LEVELS.map((l) => ({ ...l, x: exp?.estimates.find((e) => e.label === l.label) })).filter(
    (row): row is typeof row & { x: Estimate } => row.x !== undefined && row.x.ci_low !== null && row.x.ci_high !== null,
  );
  const [ref, reveal] = useReveal<HTMLDivElement>();
  if (rows.length !== LEVELS.length) return null;
  const m = Math.max(...rows.map((row) => Math.max(Math.abs(row.x.ci_low as number), Math.abs(row.x.ci_high as number)))) * 1.1;
  const pos = (v: number) => 50 + (v / m) * 50; // percent across the bar track

  return (
    <section id="verdict" aria-labelledby="h-verdict" className="verdict-sec">
      <div className={`verdict reveal-${reveal}`} ref={ref}>
        <div className="verdict-strip">
          <h2 id="h-verdict">Test verdict</h2>
          <p>Shrinkage (SHRINK_5) against the plain average (MEAN), EXP-001</p>
        </div>
        <p className="verdict-lede">
          Difference in Kendall tau-b, SHRINK_5 minus MEAN, at each rating-noise level, with 95% intervals. Right of zero: shrinkage recovers
          the true order better. Left of zero: the plain average does.
        </p>
        <ul className="verdict-rows">
          {rows.map((row, i) => {
            const v = row.x.estimate;
            const left = Math.min(pos(0), pos(v));
            const width = Math.abs(pos(v) - pos(0));
            return (
              <li key={row.label}>
                <span className="vr-name">
                  <strong>{row.name}</strong> <span>{row.noise}</span>
                </span>
                <span className="vr-track" aria-hidden="true">
                  <span className="vr-zero" />
                  <span
                    className={`vr-bar ${v < 0 ? "neg" : "pos"}`}
                    style={{ left: `${left}%`, width: `${width}%`, transitionDelay: `${i * 70}ms` }}
                  />
                  <span
                    className="vr-ci"
                    style={{ left: `${pos(row.x.ci_low as number)}%`, width: `${pos(row.x.ci_high as number) - pos(row.x.ci_low as number)}%`, transitionDelay: `${i * 70 + 200}ms` }}
                  />
                </span>
                <span className="vr-num">
                  <strong>{fmtEstimate(row.x)}</strong> <span>({fmtInterval(row.x)})</span>
                </span>
              </li>
            );
          })}
        </ul>
        <p className="verdict-foot">
          Measured in the preregistered simulation; 95% bootstrap intervals over seeds. The advantage also reverses when the shrinkage centre is
          off by half a star or the quality distribution changes shape (EXP-003, below).
        </p>
      </div>
    </section>
  );
}
