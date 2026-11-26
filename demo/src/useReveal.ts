// SPDX-License-Identifier: LicenseRef-TRUST-NC-Research-1.0
// Marks an element as revealed the first time it scrolls into view. If the
// element is already visible at mount, or IntersectionObserver is missing,
// it is revealed at once, so nothing stays hidden.
import { useEffect, useRef, useState } from "react";

export function useReveal<T extends Element>(): [React.RefObject<T | null>, "idle" | "pending" | "shown"] {
  const ref = useRef<T>(null);
  const [state, setState] = useState<"idle" | "pending" | "shown">("idle");
  useEffect(() => {
    const el = ref.current;
    if (!el || typeof IntersectionObserver === "undefined") {
      setState("shown");
      return;
    }
    const r = el.getBoundingClientRect();
    if (r.top < window.innerHeight && r.bottom > 0) {
      setState("shown");
      return;
    }
    setState("pending");
    const io = new IntersectionObserver(
      (es) => {
        if (es.some((e) => e.isIntersecting)) {
          setState("shown");
          io.disconnect();
        }
      },
      { threshold: 0.25 },
    );
    io.observe(el);
    return () => io.disconnect();
  }, []);
  return [ref, state];
}
