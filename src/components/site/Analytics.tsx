"use client";

import { useEffect, useSyncExternalStore } from "react";
import { track } from "@/lib/analytics";

/*
 * The counter's two small jobs inside the app (the loader itself is
 * /visits.js — see src/lib/analytics.ts):
 *
 * 1. Any element carrying `data-ga="event_name"` sends that event when it is
 *    clicked, with its `data-ga-*` attributes as parameters — so server
 *    components (book pages, link lists) can mark a link without becoming
 *    client components.
 * 2. `?me=1` / `?me=0` gets an answer on the page, so Hao can see that this
 *    device has stopped (or resumed) being counted.
 */

const noop = () => () => {};
const readMe = () => new URLSearchParams(window.location.search).get("me") ?? "";
const serverMe = () => "";

export function Analytics() {
  const me = useSyncExternalStore(noop, readMe, serverMe);

  useEffect(() => {
    const onClick = (e: MouseEvent) => {
      const el = (e.target as Element | null)?.closest?.("[data-ga]");
      const event = el?.getAttribute("data-ga");
      if (!el || !event) return;
      const params: Record<string, string> = {};
      for (const attr of Array.from(el.attributes)) {
        if (attr.name.startsWith("data-ga-")) {
          params[attr.name.slice(8).replace(/-/g, "_")] = attr.value;
        }
      }
      track(event, params);
    };
    document.addEventListener("click", onClick, true);
    return () => document.removeEventListener("click", onClick, true);
  }, []);

  if (me !== "1" && me !== "0") return null;
  return (
    <div
      role="status"
      className="pointer-events-none fixed bottom-8 left-1/2 z-50 -translate-x-1/2 rounded-[2px] border border-line bg-paper px-5 py-3 font-mono text-[11px] uppercase tracking-[0.14em] text-ink-2"
    >
      {me === "1"
        ? "This device is no longer counted"
        : "This device is counted again"}
    </div>
  );
}
