import { ogCard, OG_SIZE, OG_CONTENT_TYPE } from "@/lib/og";

export const alt = "Videos — two series, spoken";
export const size = OG_SIZE;
export const contentType = OG_CONTENT_TYPE;

/* Latin-only on purpose: the OG fonts carry no CJK glyphs. */
export default function Image() {
  return ogCard({
    kicker: "Videos",
    title: "The ideas, spoken",
    sub: "Working Theory in English, Friends Intelligence in Chinese — published here first",
  });
}
