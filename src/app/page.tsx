import Link from "next/link";
import { SiteShell, Container } from "@/components/site/Chrome";
import { Constellation } from "@/components/site/Constellation";
import { HOME_INDEX, SITE } from "@/content/site";
import { BOOKS } from "@/content/books";
import { getStarData } from "@/lib/constellation";
import {
  getLatestEpisodes,
  getPublishedEpisodesBySeries,
  getSeries,
  videosIndexMeta,
} from "@/lib/videos";
import { VIDEO_SERIES } from "@/content/videos";
import { formatDate } from "@/lib/essays";

/* The home page (Hao, 2026-09-21): the flagship is a book, a piano and
 * balloons on the street; work is what LinkedIn is for. Masthead + sky,
 * one band of three, one line about weekdays, then every room. Quiet on
 * purpose — no new colour, no motion, nothing to click but the work.
 *
 * 2026-11-09: the middle card became the book's video line (Friends
 * Intelligence on 小红书 — the shelf that actually grows every week; the
 * piano film stays on /videos), and a "Latest" strip under the three cards
 * shows the newest episodes across every series, computed from the data. */
type Flagship = {
  href: string;
  label: string;
  title: string;
  line: string;
  img: { src: string; alt: string; fit: string };
};

export default function HomePage() {
  const stars = getStarData();
  const book = BOOKS.find((b) => b.slug === "friends-intelligence")!;

  const fi = VIDEO_SERIES["friends-intelligence"];
  const fiEpisodes = getPublishedEpisodesBySeries("friends-intelligence");
  const fiLatest = fiEpisodes[0];
  const latest = getLatestEpisodes(4);

  const flagships: Flagship[] = [
    {
      href: "/books/friends-intelligence",
      label: "The book",
      title: book.title,
      line: `${book.oneLiner} ${book.heldIn ?? ""}`,
      img: {
        src: book.cover!.src,
        alt: book.cover!.alt,
        fit: "object-contain p-2 min-[800px]:p-7",
      },
    },
    {
      href: "/videos#friends-intelligence",
      label: "On camera",
      title: fi.name,
      line: `The book's seven intelligences, spoken in Chinese — ${fiEpisodes.length} short films so far, published here first and on 小红书 as 「${fi.platformHandle}」.`,
      img: {
        src: fiLatest?.poster ?? "/videos/fi-sleep-daylight/poster.jpg",
        alt: fiLatest
          ? `${fiLatest.title} — the latest Friends Intelligence film`
          : "Friends Intelligence on camera",
        fit: "object-cover object-[50%_40%]",
      },
    },
    {
      href: "/balloons",
      label: "On the street",
      title: "Little Wow Balloons",
      line: "Balloon animals twisted by hand at Melbourne's markets and festivals.",
      img: {
        src: "/projects/balloons/street-2.jpg",
        alt: "Hao at his balloon stand at a Melbourne street market",
        fit: "object-cover object-[28%_50%]",
      },
    },
  ];

  return (
    <SiteShell>
      <Container>
        {/* Masthead: the words and the sky */}
        <section className="grid grid-cols-1 items-center gap-x-12 gap-y-10 pt-14 min-[1000px]:grid-cols-[minmax(380px,44%)_1fr] min-[1000px]:pt-20">
          <div>
            <div className="meta">Hao Qian · Melbourne · A library, not a website</div>
            <h1 className="mt-7 font-serif text-[40px] font-normal leading-[1.1] tracking-[-0.015em] min-[900px]:text-[56px] min-[900px]:leading-[1.08]">
              {SITE.tagline}
            </h1>
            <p className="mt-6 max-w-[560px] font-serif text-[19px] leading-[1.55] text-ink-2 min-[900px]:text-[21px] min-[900px]:leading-[1.5]">
              {SITE.intro}
            </p>
          </div>
          <Constellation data={stars} />
        </section>

        {/* The three things */}
        <section className="mt-14 grid grid-cols-1 gap-x-8 gap-y-10 border-t border-ink pt-8 min-[800px]:grid-cols-3 min-[900px]:mt-20">
          {flagships.map((f) => (
            <Link
              key={f.href}
              href={f.href}
              className="group grid grid-cols-[116px_1fr] items-start gap-x-5 min-[800px]:block"
            >
              <div className="aspect-[4/5] overflow-hidden rounded-[2px] border border-line bg-surface transition-colors duration-[250ms] group-hover:border-faint">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img
                  src={f.img.src}
                  alt={f.img.alt}
                  className={`block h-full w-full ${f.img.fit}`}
                  loading="lazy"
                />
              </div>
              <div>
                <div className="meta !text-[11px] min-[800px]:mt-5">{f.label}</div>
                <div className="mt-2 font-serif text-[22px] leading-[1.25] transition-colors duration-[250ms] group-hover:text-accent min-[800px]:text-[26px]">
                  {f.title}
                </div>
                <p className="mt-2 max-w-[340px] text-[14.5px] leading-[1.65] text-ink-2">
                  {f.line}
                </p>
              </div>
            </Link>
          ))}
        </section>

        {/* Latest — the newest films across every series, straight from the data */}
        {latest.length > 0 && (
          <section className="mt-14 grid grid-cols-1 gap-x-12 gap-y-5 border-t border-line pt-6 min-[900px]:grid-cols-[220px_1fr]">
            <div>
              <div className="meta">Latest</div>
              <Link
                href="/videos"
                className="mt-2 block text-[13.5px] text-accent transition-colors duration-[250ms] hover:text-accent-deep"
              >
                All episodes →
              </Link>
            </div>
            <ul className="grid grid-cols-2 gap-x-5 gap-y-6 min-[700px]:grid-cols-4">
              {latest.map((e) => {
                const series = getSeries(e);
                return (
                  <li key={e.slug}>
                    <Link
                      href={`/videos/${e.slug}`}
                      lang={series.language}
                      className="group block"
                    >
                      {e.poster && (
                        <div className="aspect-[4/5] overflow-hidden rounded-[2px] border border-line bg-surface transition-colors duration-[250ms] group-hover:border-faint">
                          {/* eslint-disable-next-line @next/next/no-img-element */}
                          <img
                            src={e.poster}
                            alt={`${e.title} — poster`}
                            className="block h-full w-full object-cover object-[50%_40%]"
                            loading="lazy"
                          />
                        </div>
                      )}
                      <div className="meta mt-3 !text-[10.5px]" lang="en">
                        {series.name} · Ep. {e.sequence}
                        {e.publishedAt ? ` · ${formatDate(e.publishedAt)}` : ""}
                      </div>
                      <div className="mt-1 font-serif text-[16px] leading-[1.3] transition-colors duration-[250ms] group-hover:text-accent">
                        {e.title}
                      </div>
                    </Link>
                  </li>
                );
              })}
            </ul>
          </section>
        )}

        {/* Work, in one line */}
        <section className="mt-14 grid grid-cols-1 gap-x-12 gap-y-3 border-t border-line pt-6 min-[900px]:grid-cols-[220px_1fr]">
          <div className="meta">On weekdays</div>
          <p className="max-w-[640px] font-serif text-[19px] leading-[1.55] text-ink-2">
            I lead software engineering teams, and I talk about work where work
            is talked about —{" "}
            <a
              href={SITE.linkedin}
              className="text-accent transition-colors duration-[250ms] hover:text-accent-deep"
            >
              on LinkedIn
            </a>
            . The theories that survived the work are kept here as{" "}
            <Link
              href="/writing"
              className="text-accent transition-colors duration-[250ms] hover:text-accent-deep"
            >
              Working Theory
            </Link>
            {" "}— fifty-two essays, and now the{" "}
            <Link
              href="/videos#working-theory"
              className="text-accent transition-colors duration-[250ms] hover:text-accent-deep"
            >
              films
            </Link>
            .
          </p>
        </section>

        {/* Index of the library */}
        <nav className="mt-14 border-t border-ink min-[900px]:mt-16">
          {HOME_INDEX.map((entry) => (
            <Link
              key={entry.href}
              href={entry.href}
              className="group grid grid-cols-[1fr_auto] items-baseline gap-x-6 gap-y-1 border-b border-hairline py-5 transition-colors duration-[250ms] hover:bg-surface min-[900px]:grid-cols-[220px_1fr_auto] min-[900px]:py-6"
            >
              <span className="meta order-2 col-span-2 min-[900px]:order-none min-[900px]:col-span-1">
                {entry.href === "/videos" ? videosIndexMeta() : entry.meta}
              </span>
              <span className="font-serif text-[26px] leading-[1.25] min-[900px]:text-[28px]">
                {entry.label}
                <span className="ml-4 hidden text-[15px] text-ink-2 min-[900px]:inline">
                  {entry.blurb}
                </span>
              </span>
              <span className="text-[15px] text-faint transition-colors duration-[250ms] group-hover:text-accent">
                →
              </span>
            </Link>
          ))}
        </nav>
      </Container>
    </SiteShell>
  );
}
