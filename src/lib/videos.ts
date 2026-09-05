import {
  EPISODES,
  VIDEO_SERIES,
  VIDEO_SERIES_ORDER,
  type VideoEpisode,
  type VideoSeries,
  type VideoSeriesId,
} from "@/content/videos";

/*
 * Helpers over the video content model. Published episodes are the public
 * record; drafts build (for preview at their future URL) but stay out of
 * every listing, index and feed.
 */

export const SITE_URL = "https://haoqian.co";

export function getPublishedEpisodes(): VideoEpisode[] {
  return EPISODES.filter((e) => e.status === "published").sort(
    (a, b) => b.sequence - a.sequence
  );
}

export function getAllEpisodes(): VideoEpisode[] {
  return EPISODES;
}

export function getEpisode(slug: string): VideoEpisode | undefined {
  return EPISODES.find((e) => e.slug === slug);
}

export function getSeries(episode: VideoEpisode): VideoSeries {
  return VIDEO_SERIES[episode.series];
}

/** Every series, in display order. */
export function getSeriesList(): VideoSeries[] {
  return VIDEO_SERIES_ORDER.map((id) => VIDEO_SERIES[id]);
}

/** Published episodes of one series, latest first. */
export function getPublishedEpisodesBySeries(id: VideoSeriesId): VideoEpisode[] {
  return getPublishedEpisodes().filter((e) => e.series === id);
}

/** Series that actually have published episodes — listings never show an empty shelf. */
export function getLiveSeries(): VideoSeries[] {
  return getSeriesList().filter(
    (s) => getPublishedEpisodesBySeries(s.id).length > 0
  );
}

/** The home-index meta line — computed, so the count is always honest. */
export function videosIndexMeta(): string {
  const live = getLiveSeries();
  const n = getPublishedEpisodes().length;
  if (n === 0) return "in production";
  const series = live.length === 1 ? live[0].name : `${live.length} series`;
  return `${series} · ${n} episode${n === 1 ? "" : "s"}`;
}

/** Where the episode was distributed after publishing here — LinkedIn or 小红书. */
export function getDistributionUrl(episode: VideoEpisode): string | undefined {
  return episode.platformPublishedUrl ?? episode.linkedinPublishedUrl;
}

/** Previous/next within the same series, published episodes only. */
export function getNeighbours(episode: VideoEpisode): {
  earlier?: VideoEpisode;
  later?: VideoEpisode;
} {
  const inSeries = EPISODES.filter(
    (e) => e.series === episode.series && e.status === "published"
  ).sort((a, b) => a.sequence - b.sequence);
  const i = inSeries.findIndex((e) => e.slug === episode.slug);
  if (i === -1) return {};
  return { earlier: inSeries[i - 1], later: inSeries[i + 1] };
}

export function episodeCanonicalUrl(episode: VideoEpisode): string {
  return `${SITE_URL}/videos/${episode.slug}`;
}

/** 372 → "6:12" */
export function formatDuration(seconds: number): string {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m}:${String(s).padStart(2, "0")}`;
}

/** 372 → "PT6M12S" (schema.org duration) */
export function isoDuration(seconds: number): string {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `PT${m}M${s}S`;
}

export function isFileVideo(url: string): boolean {
  return /\.(mp4|webm|mov|m4v)(\?|#|$)/i.test(url) || url.startsWith("/");
}

export function isEmbedVideo(url: string): boolean {
  return /youtube\.com|youtu\.be|vimeo\.com/i.test(url);
}
