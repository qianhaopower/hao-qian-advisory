import { ogCard, OG_SIZE, OG_CONTENT_TYPE } from "@/lib/og";
import { getProject } from "@/content/projects";

export const alt = "A project by Hao Qian";
export const size = OG_SIZE;
export const contentType = OG_CONTENT_TYPE;

export default async function Image({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const project = getProject(slug);
  if (!project) return ogCard({ kicker: "Projects", title: "Software worth keeping." });
  return ogCard({
    kicker: `Project · ${project.years}`,
    title: project.name,
    sub: project.oneLiner,
  });
}
