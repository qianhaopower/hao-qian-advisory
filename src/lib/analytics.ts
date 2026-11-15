import { SITE } from "@/content/site";

/*
 * The library's visitor counter — Google Analytics 4 (since 2026-11-15).
 *
 * One ID, one place: `SITE.gaId`. While it is empty nothing loads and the
 * footer says nothing. The counter itself is the small script served at
 * /visits.js (built from `visitsScript` below), loaded by the root layout
 * and by the static /friendsintelligence landing page.
 *
 * What it will not do:
 *  - run anywhere but haoqian.co (no localhost, no preview builds);
 *  - count a device that opened any page with `?me=1` (the librarian's own
 *    phone and laptop; `?me=0` turns counting back on);
 *  - put any number it collects on a page. /today still shows no counts of
 *    anybody else — these events are for Hao's eyes only.
 */

export const GA_HOSTS = ["haoqian.co", "www.haoqian.co"];
export const GA_OFF_KEY = "ga-off";

type Params = Record<string, string | number | boolean | undefined>;

declare global {
  interface Window {
    dataLayer?: unknown[];
    gtag?: (...args: unknown[]) => void;
  }
}

/** Send one event. Silent when the counter is not loaded; never throws. */
export function track(event: string, params: Params = {}): void {
  if (typeof window === "undefined") return;
  try {
    window.gtag?.("event", event, params);
  } catch {
    /* counting must never break the page */
  }
}

/** The body of /visits.js. Plain ES5: it also runs on the static pages. */
export function visitsScript(id: string = SITE.gaId): string {
  if (!id) return "/* the library is not counting visits */\n";
  return `(function () {
  var ID = ${JSON.stringify(id)};
  try {
    var me = new URLSearchParams(location.search).get("me");
    if (me === "1") localStorage.setItem(${JSON.stringify(GA_OFF_KEY)}, "1");
    if (me === "0") localStorage.removeItem(${JSON.stringify(GA_OFF_KEY)});
    if (localStorage.getItem(${JSON.stringify(GA_OFF_KEY)}) === "1") return;
  } catch (e) {}
  if (${JSON.stringify(GA_HOSTS)}.indexOf(location.hostname) === -1) return;
  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { window.dataLayer.push(arguments); };
  window.gtag("js", new Date());
  window.gtag("config", ID);
  var s = document.createElement("script");
  s.async = true;
  s.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(ID);
  document.head.appendChild(s);
})();
`;
}
