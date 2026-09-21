import { ogCard, OG_SIZE, OG_CONTENT_TYPE } from "@/lib/og";

export const alt = "Hao Qian — A book, a piano, and balloons on the street";
export const size = OG_SIZE;
export const contentType = OG_CONTENT_TYPE;

export default function Image() {
  return ogCard({
    kicker: "Hao Qian · Melbourne",
    title: "A book, a piano, and balloons on the street.",
    sub: "A library, not a website — books, music, balloons, Working Theory",
  });
}
