/*
 * The house sign keeps itself fresh (2026-11-18 — Hao reads it inside WeChat,
 * whose browser holds on to a page long after a new one is live: "怎么加一个
 * 强刷新").
 *
 * Every build of the sign carries a fingerprint of its own source
 * (NEXT_PUBLIC_PINGAN_VERSION, computed in next.config.ts). On every open,
 * and every time the page comes back to the front, it asks /pingan/version
 * which fingerprint is live. If that is not its own, the copy on this phone is
 * old, and it reloads itself at an address the phone has never fetched
 * (?v=<fingerprint>) — a cached page cannot answer for a new address.
 *
 * Nothing is lost by the reload: the badges live in localStorage.
 */

export const PINGAN_VERSION = process.env.NEXT_PUBLIC_PINGAN_VERSION ?? "";

const TRIES = "pingan:fresh";

/** Load the page again at an address no cache has seen. */
export function reloadFresh(tag: string = Date.now().toString(36)) {
  const url = new URL(window.location.href);
  url.searchParams.set("v", tag);
  window.location.replace(url.toString());
}

/** Ask what is live; if this copy is old, replace it. Never loops. */
export async function freshen(): Promise<void> {
  if (!PINGAN_VERSION) return;
  try {
    const res = await fetch(`/pingan/version?t=${Date.now()}`, { cache: "no-store" });
    if (!res.ok) return;
    const live: unknown = (await res.json())?.v;
    if (typeof live !== "string" || !live || live === PINGAN_VERSION) return;

    /* at most three goes at any one new version per visit */
    let goes = 0;
    try {
      const [v, n] = (window.sessionStorage.getItem(TRIES) ?? "").split(":");
      if (v === live) goes = Number(n) || 0;
      if (goes >= 3) return;
      window.sessionStorage.setItem(TRIES, `${live}:${goes + 1}`);
    } catch {
      /* no storage to count in: one go, told by the address itself */
      if (new URLSearchParams(window.location.search).get("v")?.startsWith(live)) return;
    }
    reloadFresh(goes ? `${live}.${goes}` : live);
  } catch {
    /* offline, or the answer never came: keep showing what we have */
  }
}
