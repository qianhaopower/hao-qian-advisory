import { ogCard, OG_SIZE, OG_CONTENT_TYPE } from "@/lib/og";
import { getAllEpisodes, getEpisode, getSeries } from "@/lib/videos";

export const alt = "Video episode";
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
  /* The OG fonts carry no CJK glyphs: a Chinese episode gets its English
   * gloss. (Published episodes point og:image at their poster anyway.) */
  const latin = !series.language.startsWith("zh");
  return ogCard({
    kicker: `${series.name} · ${series.form} · Ep. ${episode.sequence}`,
    title: latin ? episode.title : episode.titleEn ?? series.name,
    sub: latin
      ? episode.hook
      : `${series.name}, spoken in Chinese — episode ${episode.sequence}`,
  });
}
