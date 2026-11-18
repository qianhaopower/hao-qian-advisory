/*
 * Which build of the house sign is live — the other half of its self-refresh
 * (see src/lib/pingan-fresh.ts). Never cached, anywhere: the page asks on
 * every open so that a phone holding an old copy (WeChat's browser keeps
 * pages for a long time) can tell, and reload itself.
 */
export const dynamic = "force-dynamic";

export function GET() {
  return Response.json(
    { v: process.env.NEXT_PUBLIC_PINGAN_VERSION ?? "" },
    { headers: { "Cache-Control": "no-store, max-age=0" } }
  );
}
