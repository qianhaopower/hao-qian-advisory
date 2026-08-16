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
import { VIDEO_SERIES } from "@/content/videos";
import { getPublishedEpisodes, getSeries, formatDuration } from "@/lib/videos";
import { formatDate } from "@/lib/essays";

const series = VIDEO_SERIES["working-theory"];

export const metadata: Metadata = {
  title: "Videos",
  description: `${series.name} — ${series.description}`,
};

export default function VideosPage() {
  const episodes = getPublishedEpisodes();

  return (
    <SiteShell current="/videos">
      <Container>
        <section className="pt-16 min-[900px]:pt-20">
          <Kicker>
            {series.name} · {series.form}
            {episodes.length > 0 ? ` · ${episodes.length} episode${episodes.length === 1 ? "" : "s"}` : ""}
          </Kicker>
          <PageTitle>The theories, spoken.</PageTitle>
          <Lede>{series.description}</Lede>
        </section>

        {episodes.length === 0 ? (
          <div className="mt-14 max-w-[720px]">
            <Note label="Empty · deliberately">
              The first episode is in production. Episodes appear here only
              once they are finished and published — this shelf never fills
              itself with placeholders.
            </Note>
          </div>
        ) : (
          <div className="mt-14 border-t border-ink">
            {episodes.map((e) => {
              const s = getSeries(e);
              return (
                <Link
                  key={e.slug}
                  href={`/videos/${e.slug}`}
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
                    <div className="meta !text-[11px]">
                      {s.name} · Ep. {e.sequence}
                      {e.publishedAt ? ` · ${formatDate(e.publishedAt)}` : ""}
                      {e.durationSeconds
                        ? ` · ${formatDuration(e.durationSeconds)}`
                        : ""}
                    </div>
                    <div className="mt-2 font-serif text-[24px] leading-[1.3] group-hover:text-accent min-[900px]:text-[26px]">
                      {e.title}
                    </div>
                    <p className="mt-2 max-w-[560px] text-[14.5px] leading-[1.65] text-ink-2">
                      {e.summary}
                    </p>
                  </div>
                </Link>
              );
            })}
          </div>
        )}
      </Container>
    </SiteShell>
  );
}
