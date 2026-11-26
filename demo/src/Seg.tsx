// SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
// Segmented control: a row of aria-pressed buttons with an indicator that
// slides to the pressed one. The indicator is positioned with a transform
// written directly on its own element (no inherited CSS variable).
import { useLayoutEffect, useRef, useState } from "react";

export interface SegItem<T extends string> {
  value: T;
  label: string;
  id?: string;
}

export function Seg<T extends string>({
  title,
  ariaLabel,
  items,
  value,
  onChange,
  tone = "bench",
}: {
  title: string;
  ariaLabel: string;
  items: SegItem<T>[];
  value: T;
  onChange: (v: T) => void;
  tone?: "bench";
}) {
  const row = useRef<HTMLDivElement>(null);
  const ind = useRef<HTMLSpanElement>(null);
  const [ready, setReady] = useState(false);

  useLayoutEffect(() => {
    const place = () => {
      const r = row.current;
      const i = ind.current;
      if (!r || !i) return;
      const b = r.querySelector<HTMLButtonElement>('button[aria-pressed="true"]');
      if (!b) return;
      i.style.transform = `translateX(${b.offsetLeft}px) scaleX(${b.offsetWidth / 100})`;
      i.style.height = `${b.offsetHeight}px`;
      i.style.top = `${b.offsetTop}px`;
    };
    place();
    if (!ready) requestAnimationFrame(() => setReady(true));
    const ro = typeof ResizeObserver !== "undefined" ? new ResizeObserver(place) : null;
    if (ro && row.current) ro.observe(row.current);
    return () => ro?.disconnect();
  }, [value, ready]);

  return (
    <div className={`seg-wrap tone-${tone}`} role="group" aria-label={ariaLabel}>
      <span className="seg-title">{title}</span>
      <div className={`seg${ready ? " is-ready" : ""}`} ref={row}>
        <span className="seg-ind" ref={ind} aria-hidden="true" />
        {items.map((it) => (
          <button key={it.value} type="button" id={it.id} aria-pressed={value === it.value} onClick={() => onChange(it.value)}>
            {it.label}
          </button>
        ))}
      </div>
    </div>
  );
}
