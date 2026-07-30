import { ogCard, OG_SIZE, OG_CONTENT_TYPE } from "@/lib/og";
import { getEssay, formatDate } from "@/lib/essays";

export const alt = "Working Theory essay";
export const size = OG_SIZE;
export const contentType = OG_CONTENT_TYPE;

export default async function Image({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const essay = getEssay(slug);
  if (!essay) {
    return ogCard({ kicker: "Writing", title: "Working Theory" });
  }
  return ogCard({
    kicker: `Working Theory · № ${essay.no}`,
    title: essay.title,
    sub: `${formatDate(essay.date)}${
      essay.topics.length > 0 ? ` · ${essay.topics.slice(0, 3).join(" · ")}` : ""
    }`,
  });
}
