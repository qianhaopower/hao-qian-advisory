import { NextRequest } from "next/server";

// Anonymous, fire-and-forget analytics. We log a single JSON line per event and
// nothing else — no IP, no user agent, no cookies, no identifiers of any kind.
const ALLOWED_EVENTS = new Set([
  "page_view",
  "fight_started",
  "fight_completed",
  "sound_enabled",
  "result_downloaded",
]);

export async function POST(req: NextRequest) {
  try {
    const body = await req.json().catch(() => null);
    const event = body?.event;

    if (typeof event === "string" && ALLOWED_EVENTS.has(event)) {
      const line: Record<string, string> = {
        type: "wcf_analytics",
        event,
        timestamp: new Date().toISOString(),
      };
      if (body?.teamA) line.teamA = String(body.teamA);
      if (body?.teamB) line.teamB = String(body.teamB);
      if (body?.winner) line.winner = String(body.winner);

      console.log(JSON.stringify(line));
    }
  } catch {
    // Never throw — analytics must not affect the request.
  }

  // Always 204, even for invalid/unknown events.
  return new Response(null, { status: 204 });
}
