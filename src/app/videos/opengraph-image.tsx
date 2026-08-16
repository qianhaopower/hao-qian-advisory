import { ogCard, OG_SIZE, OG_CONTENT_TYPE } from "@/lib/og";
import { VIDEO_SERIES } from "@/content/videos";

export const alt = "Working Theory — on camera";
export const size = OG_SIZE;
export const contentType = OG_CONTENT_TYPE;

export default function Image() {
  const series = VIDEO_SERIES["working-theory"];
  return ogCard({
    kicker: "Videos",
    title: `${series.name}, on camera`,
    sub: "One idea per episode — published here first, distributed on LinkedIn",
  });
}
