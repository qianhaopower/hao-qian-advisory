import { BattleResult } from "@wcf/types";

export type ShareTarget = "x" | "whatsapp" | "facebook" | "reddit" | "telegram";

// A clean link to this app that pre-selects the same matchup via ?a=&b=.
// Built from origin + pathname so it preserves the deploy basePath and never
// stacks query params from an already-shared link.
export function getShareUrl(aId: string, bId: string): string {
  if (typeof window === "undefined") return "";
  const { origin, pathname } = window.location;
  const params = new URLSearchParams({ a: aId, b: bId });
  return `${origin}${pathname}?${params.toString()}`;
}

export function getShareText(result: BattleResult): string {
  const { winner, loser } = result;
  return `${winner.flag} ${winner.name} beat ${loser.flag} ${loser.name} in the World Cup Fight Simulator! ${result.oneLiner}`;
}

// One-click intent links — no SDKs, no tracking pixels, just plain share URLs.
export function getSocialUrl(target: ShareTarget, text: string, url: string): string {
  const t = encodeURIComponent(text);
  const u = encodeURIComponent(url);
  const tu = encodeURIComponent(`${text} ${url}`);
  switch (target) {
    case "x":
      return `https://twitter.com/intent/tweet?text=${t}&url=${u}`;
    case "whatsapp":
      return `https://wa.me/?text=${tu}`;
    case "facebook":
      return `https://www.facebook.com/sharer/sharer.php?u=${u}`;
    case "reddit":
      return `https://www.reddit.com/submit?url=${u}&title=${t}`;
    case "telegram":
      return `https://t.me/share/url?url=${u}&text=${t}`;
  }
}

export function canNativeShare(): boolean {
  return typeof navigator !== "undefined" && typeof navigator.share === "function";
}

// Returns true if the native share sheet completed, false if unavailable or
// the user dismissed it (so the caller can fall back to explicit buttons).
export async function nativeShare(text: string, url: string): Promise<boolean> {
  if (!canNativeShare()) return false;
  try {
    await navigator.share({ title: "World Cup Fight Simulator", text, url });
    return true;
  } catch {
    return false;
  }
}

export function openShareWindow(url: string): void {
  if (typeof window !== "undefined") {
    window.open(url, "_blank", "noopener,noreferrer,width=600,height=540");
  }
}
