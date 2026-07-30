import { ogCard, OG_SIZE, OG_CONTENT_TYPE } from "@/lib/og";
import { WORKING_THEORY } from "@/content/writing";

export const alt = "Working Theory — the essay series";
export const size = OG_SIZE;
export const contentType = OG_CONTENT_TYPE;

export default function Image() {
  return ogCard({
    kicker: "Writing",
    title: "Working Theory",
    sub: `${WORKING_THEORY.length} essays on AI, engineering, systems and leadership`,
  });
}
