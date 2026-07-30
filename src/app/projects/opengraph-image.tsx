import { ogCard, OG_SIZE, OG_CONTENT_TYPE } from "@/lib/og";
import { PROJECTS } from "@/content/projects";

export const alt = "Projects by Hao Qian";
export const size = OG_SIZE;
export const contentType = OG_CONTENT_TYPE;

export default function Image() {
  return ogCard({
    kicker: "Projects",
    title: "Software worth keeping.",
    sub: `${PROJECTS.length} kept — each with the full story and the lessons`,
  });
}
