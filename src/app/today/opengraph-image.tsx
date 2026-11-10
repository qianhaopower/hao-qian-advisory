import { ogCard, OG_SIZE, OG_CONTENT_TYPE } from "@/lib/og";

export const alt = "One thing today — one small action a day, from Friends Intelligence";
export const size = OG_SIZE;
export const contentType = OG_CONTENT_TYPE;

/* Latin-only on purpose: the OG fonts carry no CJK glyphs. */
export default function Image() {
  return ogCard({
    kicker: "One thing today",
    title: "Turn one card over. Do one thing.",
    sub: "Every Friends Intelligence episode leaves one small action — sleep, food, movement, feeling, the people you love",
  });
}
