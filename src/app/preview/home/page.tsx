import type { Metadata } from "next";
import Link from "next/link";
import { SiteShell, Container } from "@/components/site/Chrome";
import { Constellation } from "@/components/site/Constellation";
import { HOME_INDEX, SITE } from "@/content/site";
import { BOOKS } from "@/content/books";
import { getStarData } from "@/lib/constellation";
import { videosIndexMeta } from "@/lib/videos";

/* PREVIEW of a quieter, more personal home page (Hao, 2026-09-21): the
 * flagship is a book, a piano and balloons on the street; work is what
 * LinkedIn is for. Unlinked and noindex — if Hao approves, this replaces
 * src/app/page.tsx and this route is deleted. */
export const metadata: Metadata = {
  title: "Home — preview",
  robots: { index: false, follow: false },
};

type Flagship = {
  href: string;
  label: string;
  title: string;
  line: string;
  img: { src: string; alt: string; fit: string };
};

export default function HomePreviewPage() {
  const stars = getStarData();
  const book = BOOKS.find((b) => b.slug === "friends-intelligence")!;

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
      href: "/videos/piano-passacaglia",
      label: "At the piano",
      title: "Passacaglia",
      line: "Handel–Halvorsen on the upright at home — one unbroken take, and one interruption.",
      img: {
        src: "/home/at-the-piano.jpg",
        alt: "Hao at the upright piano at home",
        fit: "object-cover",
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
              A book, a piano, and balloons on the street.
            </h1>
            <p className="mt-6 max-w-[560px] font-serif text-[19px] leading-[1.55] text-ink-2 min-[900px]:text-[21px] min-[900px]:leading-[1.5]">
              I wrote a book about the patterns behind everyday life, I play
              the piano at home, and I twist balloons at Melbourne&rsquo;s
              markets. On weekdays I lead engineering teams and write down what
              the work teaches me. Everything worth keeping lives here —
              permanently.
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
            . The ideas that survive are kept here as{" "}
            <Link
              href="/writing"
              className="text-accent transition-colors duration-[250ms] hover:text-accent-deep"
            >
              Working Theory
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
