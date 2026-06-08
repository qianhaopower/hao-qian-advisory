type TrackPayload = {
  teamA?: string;
  teamB?: string;
  winner?: string;
};

// Fire-and-forget anonymous event. Uses sendBeacon when available (survives
// page unload), otherwise a keepalive fetch. All errors are swallowed — this
// must never break the app.
export function trackEvent(event: string, payload: TrackPayload = {}): void {
  if (typeof window === "undefined") return;

  try {
    // Resolve relative to the current page so the deploy basePath is respected.
    const url = new URL("api/track", document.baseURI).toString();
    const body = JSON.stringify({ event, ...payload });

    if (typeof navigator !== "undefined" && navigator.sendBeacon) {
      const blob = new Blob([body], { type: "application/json" });
      if (navigator.sendBeacon(url, blob)) return;
    }

    fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body,
      keepalive: true,
    }).catch(() => {});
  } catch {
    // ignore everything
  }
}
