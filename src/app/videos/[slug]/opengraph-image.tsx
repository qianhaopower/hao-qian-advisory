import { ogCard, OG_SIZE, OG_CONTENT_TYPE } from "@/lib/og";
import { getAllEpisodes, getEpisode, getSeries } from "@/lib/videos";

export const alt = "Working Theory episode";
export const size = OG_SIZE;
export const contentType = OG_CONTENT_TYPE;

export function generateStaticParams() {
  return getAllEpisodes().map((e) => ({ slug: e.slug }));
}

export default async function Image({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const episode = getEpisode(slug);
  if (!episode) {
    return ogCard({ kicker: "Videos", title: "Working Theory" });
  }
  const series = getSeries(episode);
  return ogCard({
    kicker: `${series.name} · ${series.form} · Ep. ${episode.sequence}`,
    title: episode.title,
    sub: episode.hook,
  });
}
