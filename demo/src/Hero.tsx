// SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
// Hero illustration: two product test labels. Reviews drop in, the interval
// narrows, the plain average and the shrunk estimate settle, and the star row
// comes into focus only where evidence is plentiful. It explains the mechanism
// and is not study data: it prints no numeral and no estimate.
import type { ReactNode } from "react";

const W = 560;
const X0 = 40;
const X1 = 520;
const sx = (u: number) => X0 + u * (X1 - X0); // u in [0, 1] along the rating scale
const CENTRE = 0.62; // catalogue average, illustrative position only

interface Card {
  key: string;
  title: string;
  y: number;
  reviews: number[]; // positions of individual reviews on the scale
  avg: number;
  shrunk: number;
  lo: number;
  hi: number;
  stars: number; // filled share of the star row
  sharp: boolean;
}

const CARDS: Card[] = [
  { key: "few", title: "A few reviews", y: 16, reviews: [0.97, 1, 0.99], avg: 0.985, shrunk: 0.77, lo: 0.42, hi: 1, stars: 0.985, sharp: false },
  {
    key: "many",
    title: "Many reviews",
    y: 210,
    reviews: [0.62, 0.8, 0.71, 0.9, 0.66, 0.78, 0.74, 0.85, 0.69, 0.76, 0.81, 0.58, 0.73, 0.88, 0.7, 0.77, 0.64, 0.83, 0.75, 0.72, 0.79, 0.68, 0.86, 0.74],
    avg: 0.755,
    shrunk: 0.745,
    lo: 0.7,
    hi: 0.81,
    stars: 0.755,
    sharp: true,
  },
];

function starPath(cx: number, cy: number, R: number): string {
  const pts: string[] = [];
  for (let i = 0; i < 10; i++) {
    const r = i % 2 === 0 ? R : R * 0.42;
    const a = (-90 + 36 * i) * (Math.PI / 180);
    pts.push(`${(cx + r * Math.cos(a)).toFixed(2)} ${(cy + r * Math.sin(a)).toFixed(2)}`);
  }
  return `M${pts.join("L")}Z`;
}

function StarRow({ x, y, share, id }: { x: number; y: number; share: number; id: string }) {
  const size = 30;
  const gap = 6;
  const d = Array.from({ length: 5 }, (_, i) => starPath(x + size / 2 + i * (size + gap), y, size / 2)).join("");
  const width = 5 * size + 4 * gap;
  return (
    <g>
      <clipPath id={`clip-${id}`}>
        <rect x={x} y={y - size} width={width * share} height={size * 2} />
      </clipPath>
      <path d={d} className="star-empty" />
      <path d={d} className="star-fill" clipPath={`url(#clip-${id})`} />
    </g>
  );
}

function CardArt({ c }: { c: Card }) {
  const ty = c.y + 112; // scale track
  const bandW = sx(c.hi) - sx(c.lo);
  return (
    <g className={`card card-${c.key}`}>
      <rect className="card-paper" x={8} y={c.y} width={W - 16} height={178} rx={6} />
      <rect className="card-strip" x={8} y={c.y} width={W - 16} height={40} rx={6} />
      <rect className="card-strip" x={8} y={c.y + 20} width={W - 16} height={20} />
      <text className="card-title" x={24} y={c.y + 27}>{c.title}</text>
      <g className={`stars ${c.sharp ? "is-sharp" : "is-soft"}`}>
        <g className="stars-soft" filter="url(#soften)"><StarRow x={X0} y={c.y + 70} share={c.stars} id={`${c.key}-a`} /></g>
        <g className="stars-sharp"><StarRow x={X0} y={c.y + 70} share={c.stars} id={`${c.key}-b`} /></g>
      </g>
      <line className="track" x1={X0} x2={X1} y1={ty} y2={ty} />
      <text className="track-end" x={X0} y={ty + 40}>low</text>
      <text className="track-end" x={X1} y={ty + 40} textAnchor="end">high</text>
      <line className="centre" x1={sx(CENTRE)} x2={sx(CENTRE)} y1={ty - 26} y2={ty + 24} />
      <rect
        className="band"
        x={sx(c.lo)}
        y={ty - 7}
        width={bandW}
        height={14}
        rx={7}
        style={{ animationDelay: `${300 + c.reviews.length * 40}ms` }}
      />
      {c.reviews.map((u, i) => (
        <line
          key={i}
          className="review"
          x1={sx(u) + (i % 3) - 1}
          x2={sx(u) + (i % 3) - 1}
          y1={ty - 30}
          y2={ty - 18}
          style={{ animationDelay: `${200 + i * 40}ms` }}
        />
      ))}
      <circle className="m-avg" cx={sx(c.avg)} cy={ty} r={7} style={{ animationDelay: `${500 + c.reviews.length * 40}ms` }} />
      <path
        className="m-shrunk"
        d={`M${sx(c.shrunk)} ${ty - 9}l9 9l-9 9l-9 -9z`}
        style={{ animationDelay: `${700 + c.reviews.length * 40}ms`, ["--from" as string]: `${(sx(c.avg) - sx(c.shrunk)).toFixed(1)}px` }}
      />
    </g>
  );
}

export function Hero({ children }: { children: ReactNode }) {
  return (
    <header className="hero" id="top">
      <div className="wrap hero-grid">
        <div className="hero-text">{children}</div>
        <figure className="lab">
          <p className="illus-label">Illustration, not study data</p>
          <svg className="lab-svg" viewBox={`0 0 ${W} 404`} role="img" aria-labelledby="lab-title">
            <title id="lab-title">
              Illustration: two products. With a few reviews, the plain average sits at the top of the scale with a wide interval and the
              shrunk estimate is pulled towards the catalogue average. With many reviews, the interval is narrow and both estimates agree.
            </title>
            <defs>
              <filter id="soften" x="-10%" y="-40%" width="120%" height="180%">
                <feGaussianBlur stdDeviation="2.4" />
              </filter>
            </defs>
            {CARDS.map((c) => (
              <CardArt key={c.key} c={c} />
            ))}
          </svg>
          <ul className="lab-legend" aria-label="Illustration legend">
            <li><svg width="16" height="16" aria-hidden="true"><circle cx="8" cy="8" r="6" className="m-avg static" /></svg> Plain average</li>
            <li><svg width="18" height="18" aria-hidden="true"><path d="M9 1l8 8l-8 8l-8 -8z" className="m-shrunk static" /></svg> Shrunk towards the catalogue average</li>
            <li><svg width="26" height="12" aria-hidden="true"><rect x="1" y="1" width="24" height="10" rx="5" className="band static" /></svg> Interval</li>
            <li><svg width="10" height="16" aria-hidden="true"><line x1="5" x2="5" y1="2" y2="14" className="review static" /></svg> One review</li>
          </ul>
        </figure>
      </div>
    </header>
  );
}
