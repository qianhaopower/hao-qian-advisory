import { ogCard, OG_SIZE, OG_CONTENT_TYPE } from "@/lib/og";
import { IDEAS } from "@/content/garden";

export const alt = "Digital Garden — ideas that are still growing";
export const size = OG_SIZE;
export const contentType = OG_CONTENT_TYPE;

export default function Image() {
  return ogCard({
    kicker: "Digital Garden",
    title: "Ideas that are still growing.",
    sub: IDEAS.map((i) => `№ ${i.no}`).join(" · ") + " · planted, tended, never finished",
  });
}
