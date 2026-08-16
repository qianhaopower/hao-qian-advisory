import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import {
  SiteShell,
  Container,
  Kicker,
  Note,
} from "@/components/site/Chrome";
import { Connections } from "@/components/site/Connections";
import type { VideoEpisode } from "@/content/videos";
import {
  getAllEpisodes,
  getEpisode,
  getSeries,
  getNeighbours,
  episodeCanonicalUrl,
  formatDuration,
  isoDuration,
  isFileVideo,
  isEmbedVideo,
  SITE_URL,
} from "@/lib/videos";
import { formatDate } from "@/lib/essays";

/* Drafts build too, so an episode can be previewed at its future URL —
 * but they are noindex and appear in no listing. */
export function generateStaticParams() {
  return getAllEpisodes().map((e) => ({ slug: e.slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const episode = getEpisode(slug);
  if (!episode) return {};
  const series = getSeries(episode);
  const canonical = episodeCanonicalUrl(episode);
  const title = `${series.name} Ep. ${episode.sequence} — ${episode.title}`;

  if (episode.status === "draft") {
    return { title, robots: { index: false, follow: false } };
  }

  return {
    title,
    description: episode.summary,
    alternates: { canonical },
    openGraph: {
      title,
      description: episode.summary,
      url: canonical,
      type: "video.other",
      images: [episode.poster ?? `/videos/${episode.slug}/opengraph-image`],
      ...(episode.publishedAt && {
        videos: episode.videoUrl
          ? [{ url: episode.videoUrl }]
          : undefined,
      }),
    },
  };
}

function VideoBlock({ episode }: { episode: VideoEpisode }) {
  const portrait = (episode.aspect ?? "9:16") === "9:16";
  const frame = portrait
    ? "mx-auto w-full max-w-[380px]"
    : "w-full";
  const ratio = portrait ? "aspect-[9/16]" : "aspect-video";

  if (!episode.videoUrl) {
    return (
      <div className={frame}>
        <div
          className={`${ratio} flex items-center justify-center rounded-[2px] border border-line bg-surface`}
        >
          <span className="meta">Video in production</span>
        </div>
      </div>
    );
  }

  if (isFileVideo(episode.videoUrl)) {
    return (
      <div className={frame}>
        <video
          className={`${ratio} w-full rounded-[2px] border border-line bg-surface object-contain`}
          controls
          playsInline
          preload="metadata"
          poster={episode.poster}
        >
          <source src={episode.videoUrl} />
          {episode.captions && (
            <track
              kind="captions"
              src={episode.captions}
              srcLang={episode.language}
              label="Captions"
              default
            />
          )}
        </video>
      </div>
    );
  }

  if (isEmbedVideo(episode.videoUrl)) {
    return (
      <div className={frame}>
        <iframe
          className={`${ratio} w-full rounded-[2px] border border-line bg-surface`}
          src={episode.videoUrl}
          title={episode.title}
          allow="encrypted-media; picture-in-picture"
          allowFullScreen
        />
      </div>
    );
  }

  return (
    <a
      href={episode.videoUrl}
      className="text-accent transition-colors duration-[250ms] hover:text-accent-deep"
    >
      Watch the episode →
    </a>
  );
}

export default async function EpisodePage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const episode = getEpisode(slug);
  if (!episode) notFound();
  const series = getSeries(episode);
  const { earlier, later } = getNeighbours(episode);
  const canonical = episodeCanonicalUrl(episode);

  /* VideoObject structured data — published episodes only, real fields only */
  const jsonLd =
    episode.status === "published" && episode.publishedAt
      ? {
          "@context": "https://schema.org",
          "@type": "VideoObject",
          name: episode.title,
          description: episode.summary,
          uploadDate: episode.publishedAt,
          url: canonical,
          inLanguage: episode.language,
          ...(episode.poster && {
            thumbnailUrl: `${SITE_URL}${episode.poster.startsWith("/") ? "" : "/"}${episode.poster}`,
          }),
          ...(episode.durationSeconds && {
            duration: isoDuration(episode.durationSeconds),
          }),
          ...(episode.videoUrl &&
            (isEmbedVideo(episode.videoUrl)
              ? { embedUrl: episode.videoUrl }
              : {
                  contentUrl: episode.videoUrl.startsWith("/")
                    ? `${SITE_URL}${episode.videoUrl}`
                    : episode.videoUrl,
                })),
          author: { "@type": "Person", name: "Hao Qian", url: SITE_URL },
        }
      : null;

  return (
    <SiteShell current="/videos">
      {jsonLd && (
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
      )}
      <Container>
        <article className="mx-auto max-w-[640px]">
          <header className="pt-16 min-[900px]:pt-20">
            <Kicker>
              <Link
                href="/videos"
                className="transition-colors duration-[250ms] hover:text-accent"
              >
                {series.name}
              </Link>{" "}
              · {series.form} · Ep. {episode.sequence}
            </Kicker>
            <h1 className="mt-6 font-serif text-[32px] font-normal leading-[1.18] tracking-[-0.01em] min-[900px]:text-[44px] min-[900px]:leading-[1.15]">
              {episode.title}
            </h1>
            <p className="mt-5 max-w-[600px] font-serif text-[20px] italic leading-[1.5] text-ink-2 min-[900px]:text-[22px]">
              {episode.hook}
            </p>
            <div className="meta mt-6 !normal-case !tracking-[0.08em]">
              {episode.publishedAt ? formatDate(episode.publishedAt) : "Draft"}
              {episode.durationSeconds
                ? ` · ${formatDuration(episode.durationSeconds)}`
                : ""}
            </div>
          </header>

          {episode.status === "draft" && (
            <div className="mt-8">
              <Note label="Draft">
                This episode is not published yet. It is invisible everywhere
                except this direct URL.
              </Note>
            </div>
          )}

          <div className="mt-10">
            <VideoBlock episode={episode} />
          </div>

          <div className="prose-read mt-12">
            <p>{episode.summary}</p>
          </div>

          {episode.keyPoints && episode.keyPoints.length > 0 && (
            <div className="mt-10 rounded-[2px] bg-surface px-6 py-5">
              <div className="meta !text-[11px]">The idea to keep</div>
              <ul className="mt-3 flex flex-col gap-2">
                {episode.keyPoints.map((point) => (
                  <li
                    key={point}
                    className="font-serif text-[18px] leading-[1.55] text-ink"
                  >
                    {point}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {episode.supportingVisuals &&
            episode.supportingVisuals.length > 0 && (
              <div className="mt-12 flex flex-col gap-6">
                {episode.supportingVisuals.map((v) => (
                  <figure
                    key={v.src}
                    className="overflow-hidden rounded-[2px] border border-line"
                  >
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    <img
                      src={v.src}
                      alt={v.alt}
                      className="block w-full"
                      loading="lazy"
                    />
                    {v.caption && (
                      <figcaption className="border-t border-hairline px-5 py-3 text-[13px] leading-[1.6] text-ink-2">
                        {v.caption}
                      </figcaption>
                    )}
                  </figure>
                ))}
              </div>
            )}

          {episode.transcript && episode.transcript.length > 0 && (
            <section className="mt-14 border-t border-line pt-8">
              <h2 className="meta">Transcript</h2>
              <div className="prose-read mt-6">
                {episode.transcript.map((para, i) => (
                  <p key={i}>{para}</p>
                ))}
              </div>
            </section>
          )}

          {episode.status === "published" && episode.linkedinPublishedUrl && (
            <footer className="mt-14 border-t border-line pt-6">
              <a
                href={episode.linkedinPublishedUrl}
                className="text-[13.5px] text-accent transition-colors duration-[250ms] hover:text-accent-deep"
              >
                Also published on {series.platform} →
              </a>
            </footer>
          )}
        </article>

        <div className="mx-auto mt-10 max-w-[640px]">
          <Connections id={`video:${episode.slug}`} />
        </div>

        {/* neighbours */}
        {(earlier || later) && (
          <nav className="mx-auto mt-14 grid max-w-[640px] grid-cols-1 gap-4 min-[700px]:grid-cols-2">
            {earlier ? (
              <Link
                href={`/videos/${earlier.slug}`}
                className="group rounded-[2px] border border-line p-5 transition-colors duration-[250ms] hover:border-faint"
              >
                <div className="meta !text-[11px]">
                  ← Earlier · Ep. {earlier.sequence}
                </div>
                <div className="mt-2 font-serif text-[17px] leading-[1.4] group-hover:text-accent">
                  {earlier.title}
                </div>
              </Link>
            ) : (
              <div />
            )}
            {later ? (
              <Link
                href={`/videos/${later.slug}`}
                className="group rounded-[2px] border border-line p-5 text-right transition-colors duration-[250ms] hover:border-faint"
              >
                <div className="meta !text-[11px]">
                  Later · Ep. {later.sequence} →
                </div>
                <div className="mt-2 font-serif text-[17px] leading-[1.4] group-hover:text-accent">
                  {later.title}
                </div>
              </Link>
            ) : (
              <div />
            )}
          </nav>
        )}
      </Container>
    </SiteShell>
  );
}
