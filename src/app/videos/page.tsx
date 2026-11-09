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
  groupEpisodesByTopic,
  getLiveSeries,
  formatDuration,
} from "@/lib/videos";
import { formatDate } from "@/lib/essays";

/* The piano line joins the page copy only once it has a published film —
 * same honesty rule as the shelves. */
const pianoLive = getLiveSeries().some((s) => s.id === "piano");

export const metadata: Metadata = {
  title: "Videos",
  description: `Short films, published here first: Friends Intelligence in Chinese, Working Theory in English${
    pianoLive ? ", and one series without words — Hao at the piano" : ""
  }.`,
};

/* 2026-11-09: shelves became poster grids (the Chinese line passed forty
 * episodes — a row per episode no longer read as a shelf), grouped by the
 * episode's topic: the book's pillar for Friends Intelligence, the theory
 * for Working Theory. Groups are computed from the data; nothing hand-sorted. */
function EpisodeCard({ e, series }: { e: VideoEpisode; series: VideoSeries }) {
  return (
    <li>
      <Link
        href={`/videos/${e.slug}`}
        lang={series.language}
        className="group block"
      >
        <div className="aspect-[4/5] overflow-hidden rounded-[2px] border border-line bg-surface transition-colors duration-[250ms] group-hover:border-faint">
          {e.poster && (
            /* eslint-disable-next-line @next/next/no-img-element */
            <img
              src={e.poster}
              alt={`${e.title} — poster`}
              className="block h-full w-full object-cover object-[50%_40%]"
              loading="lazy"
            />
          )}
        </div>
        <div className="meta mt-3 !text-[10.5px]" lang="en">
          Ep. {e.sequence}
          {e.publishedAt ? ` · ${formatDate(e.publishedAt)}` : ""}
          {e.durationSeconds ? ` · ${formatDuration(e.durationSeconds)}` : ""}
        </div>
        <div className="mt-1 font-serif text-[17px] leading-[1.3] transition-colors duration-[250ms] group-hover:text-accent">
          {e.title}
        </div>
        {e.titleEn && (
          <div
            lang="en"
            className="mt-0.5 font-serif text-[13px] italic leading-[1.45] text-faint"
          >
            {e.titleEn}
          </div>
        )}
      </Link>
    </li>
  );
}

function SeriesShelf({ series }: { series: VideoSeries }) {
  const episodes = getPublishedEpisodesBySeries(series.id);
  const groups = groupEpisodesByTopic(series.id);
  const grouped = groups.length > 1;
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

      {groups.map((g, i) => (
        <div
          key={g.topic ?? "untitled"}
          className={grouped ? (i === 0 ? "mt-10" : "mt-12") : "mt-8"}
        >
          {grouped && (
            <div className="meta flex items-baseline gap-x-4 border-t border-line pt-4 !text-[11px]">
              <span lang={series.language}>{g.topic ?? "Other"}</span>
              <span className="text-faint">
                {g.episodes.length} episode{g.episodes.length === 1 ? "" : "s"}
              </span>
            </div>
          )}
          <ul
            className={`grid grid-cols-2 gap-x-5 gap-y-8 min-[700px]:grid-cols-3 min-[900px]:grid-cols-4 ${
              grouped ? "mt-6" : "border-t border-line pt-8"
            }`}
          >
            {g.episodes.map((e) => (
              <EpisodeCard key={e.slug} e={e} series={series} />
            ))}
          </ul>
        </div>
      ))}
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
            Short films, one idea each. Friends Intelligence in Chinese — the
            book, one everyday practice at a time; Working Theory in English —
            the theories, face to camera.
            {pianoLive &&
              " And one series without words: at the piano, one unbroken take per film."}{" "}
            Every episode lives here first, with its captions and transcript;
            小红书 and LinkedIn are where it travels.
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
