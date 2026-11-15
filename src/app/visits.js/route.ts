import { visitsScript } from "@/lib/analytics";

/* The visitor counter's loader (see src/lib/analytics.ts). A real file at a
 * real URL so the static /friendsintelligence page can load the same script
 * as the library — the Measurement ID lives only in SITE.gaId. */

export const dynamic = "force-static";

export function GET() {
  return new Response(visitsScript(), {
    headers: {
      "content-type": "text/javascript; charset=utf-8",
      "cache-control": "public, max-age=3600",
    },
  });
}
