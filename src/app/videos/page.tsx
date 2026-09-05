import type { Metadata } from "next";
import Link from "next/link";
import {
  SiteShell,
  Container,
  Kicker,
  PageTitle,
  Lede,
  Note,
} from "@/components/site/Chrome";
import type { VideoEpisode, VideoSeries } from "@/content/videos";
import {
  getPublishedEpisodes,
  getPublishedEpisodesBySeries,
  getLiveSeries,
  formatDuration,
} from "@/lib/videos";
import { formatDate } from "@/lib/essays";

export const metadata: Metadata = {
  title: "Videos",
  description:
    "Two series, spoken: Working Theory in English, Friends Intelligence in Chinese — one idea per episode, published here first.",
};

function EpisodeRow({ e, series }: { e: VideoEpisode; series: VideoSeries }) {
  return (
    <Link
      href={`/videos/${e.slug}`}
      lang={series.language}
      className="group grid grid-cols-1 gap-x-8 gap-y-3 border-b border-hairline py-7 transition-colors duration-[250ms] hover:bg-surface min-[700px]:grid-cols-[140px_1fr]"
    >
      {e.poster ? (
        <div className="overflow-hidden rounded-[2px] border border-line max-[699px]:max-w-[180px]">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={e.poster}
            alt={`${e.title} — poster`}
            className="block w-full"
            loading="lazy"
          />
        </div>
      ) : (
        <div className="hidden min-[700px]:block" />
      )}
      <div>
        <div className="meta !text-[11px]" lang="en">
          Ep. {e.sequence}
          {e.publishedAt ? ` · ${formatDate(e.publishedAt)}` : ""}
          {e.durationSeconds ? ` · ${formatDuration(e.durationSeconds)}` : ""}
          {e.topic ? ` · ${e.topic}` : ""}
        </div>
        <div className="mt-2 font-serif text-[24px] leading-[1.3] group-hover:text-accent min-[900px]:text-[26px]">
          {e.title}
        </div>
        {e.titleEn && (
          <div
            lang="en"
            className="mt-1 font-serif text-[15px] italic leading-[1.5] text-faint"
          >
            {e.titleEn}
          </div>
        )}
        <p className="mt-2 max-w-[560px] text-[14.5px] leading-[1.65] text-ink-2">
          {e.summary}
        </p>
      </div>
    </Link>
  );
}

function SeriesShelf({ series }: { series: VideoSeries }) {
  const episodes = getPublishedEpisodesBySeries(series.id);
  return (
    <section id={series.id} className="mt-16 scroll-mt-10 min-[900px]:mt-20">
      <div className="grid grid-cols-1 gap-x-12 gap-y-4 border-t border-ink pt-6 min-[900px]:grid-cols-[220px_1fr]">
        <div>
          <h2 className="font-serif text-[28px] leading-[1.2] min-[900px]:text-[30px]">
            {series.name}
          </h2>
          <div className="meta mt-3 !text-[11px]">
            {series.form} · {series.languageLabel} · {series.platform}
          </div>
          <div className="meta mt-1 !text-[11px]">
            {episodes.length} episode{episodes.length === 1 ? "" : "s"}
          </div>
        </div>
        <div className="max-w-[640px]">
          <p className="text-[15px] leading-[1.65] text-ink-2">
            {series.description}
          </p>
          {series.nativeDescription && (
            <p
              lang={series.language}
              className="mt-2 font-serif text-[16.5px] leading-[1.65] text-ink-2"
            >
              {series.nativeDescription}
            </p>
          )}
          <div className="mt-4 flex flex-wrap gap-x-6 gap-y-1 text-[13.5px]">
            {series.origin && (
              <Link
                href={series.origin.href}
                className="text-accent transition-colors duration-[250ms] hover:text-accent-deep"
              >
                {series.origin.label} →
              </Link>
            )}
            {series.platformUrl && (
              <a
                href={series.platformUrl}
                className="text-accent transition-colors duration-[250ms] hover:text-accent-deep"
              >
                Also on {series.platform}
                {series.platformHandle ? ` · ${series.platformHandle}` : ""} →
              </a>
            )}
          </div>
        </div>
      </div>

      <div className="mt-8 border-t border-line">
        {episodes.map((e) => (
          <EpisodeRow key={e.slug} e={e} series={series} />
        ))}
      </div>
    </section>
  );
}

export default function VideosPage() {
  const all = getPublishedEpisodes();
  const live = getLiveSeries();

  return (
    <SiteShell current="/videos">
      <Container>
        <section className="pt-16 min-[900px]:pt-20">
          <Kicker>
            Videos
            {live.length > 0 ? ` · ${live.length} series` : ""}
            {all.length > 0
              ? ` · ${all.length} episode${all.length === 1 ? "" : "s"}`
              : ""}
          </Kicker>
          <PageTitle>The ideas, spoken.</PageTitle>
          <Lede>
            Two series in two languages — Working Theory in English, Friends
            Intelligence in Chinese. One idea per episode, face to camera.
            Every episode lives here first, with its captions and transcript;
            LinkedIn and 小红书 are where it travels.
          </Lede>
          {live.length > 1 && (
            <div className="meta mt-8 flex flex-wrap gap-x-6 gap-y-2 !text-[11px]">
              {live.map((s) => (
                <a
                  key={s.id}
                  href={`#${s.id}`}
                  className="transition-colors duration-[250ms] hover:text-accent"
                >
                  {s.name} ↓
                </a>
              ))}
            </div>
          )}
        </section>

        {all.length === 0 ? (
          <div className="mt-14 max-w-[720px]">
            <Note label="Empty · deliberately">
              The first episode is in production. Episodes appear here only
              once they are finished and published — this shelf never fills
              itself with placeholders.
            </Note>
          </div>
        ) : (
          live.map((s) => <SeriesShelf key={s.id} series={s} />)
        )}
      </Container>
    </SiteShell>
  );
}
