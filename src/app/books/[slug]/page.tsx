import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { SiteShell, Container, Kicker } from "@/components/site/Chrome";
import { Connections } from "@/components/site/Connections";
import { FishSwim } from "@/components/site/FishSwim";
import { BOOKS, getBook } from "@/content/books";
import { getEssays } from "@/lib/essays";

export function generateStaticParams() {
  return BOOKS.map((b) => ({ slug: b.slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const book = getBook(slug);
  if (!book) return {};
  return {
    title: book.title,
    description: book.oneLiner,
    openGraph: {
      title: `${book.title} — Hao Qian`,
      description: book.oneLiner,
      type: "book",
      images: [book.cover ? book.cover.src : `/books/${book.slug}/opengraph-image`],
    },
  };
}

export default async function BookPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const book = getBook(slug);
  if (!book) notFound();

  const essays = slug === "working-theory" ? getEssays() : null;

  return (
    <SiteShell current="/books">
      <Container>
        {/* Header */}
        <header className="flex flex-col gap-8 pt-16 min-[700px]:flex-row min-[700px]:items-start min-[900px]:pt-20">
          {book.cover ? (
            // eslint-disable-next-line @next/next/no-img-element
            <img
              src={book.cover.src}
              alt={book.cover.alt}
              className="h-[229px] w-[160px] flex-none border border-line object-cover"
            />
          ) : (
            <div className="flex h-[229px] w-[160px] flex-none items-center justify-center border border-line bg-surface p-4 text-center font-mono text-[10px] uppercase tracking-[0.12em] text-faint">
              {book.coverLabel}
            </div>
          )}
          <div className="min-w-0">
            <Kicker>
              <Link
                href="/books"
                className="transition-colors duration-[250ms] hover:text-accent"
              >
                Books
              </Link>{" "}
              · {book.kicker.replace(/^Book · /, "")}
            </Kicker>
            <h1 className="mt-5 font-serif text-[34px] font-normal leading-[1.15] tracking-[-0.01em] min-[900px]:text-[44px]">
              {book.title}
            </h1>
            {book.subtitle && (
              <p className="mt-3 max-w-[560px] font-serif text-[19px] italic leading-[1.5] text-ink-2">
                {book.subtitle}
              </p>
            )}
            {book.byline && (
              <p className="mt-3 font-serif text-[17px] italic text-ink-2">
                {book.byline}
              </p>
            )}
            <div className="meta mt-5 !normal-case !tracking-[0.08em]">
              {book.facts.join(" · ")}
            </div>
            {book.buy && (
              <div className="mt-7 flex flex-wrap items-center gap-5">
                <a
                  href={book.buy.href}
                  className="inline-flex items-center rounded-[2px] bg-ink px-6 py-3 text-[14px] font-medium text-paper transition-colors duration-[250ms] hover:bg-[#3A362F]"
                >
                  {book.buy.label} ↗
                </a>
                <a
                  href="#editions"
                  className="text-[13.5px] text-ink-2 transition-colors duration-[250ms] hover:text-accent"
                >
                  All editions ↓
                </a>
              </div>
            )}
          </div>
        </header>

        {/* Narrative + connections rail */}
        <div className="mt-14 grid grid-cols-1 items-start gap-10 min-[1000px]:grid-cols-[640px_minmax(240px,1fr)]">
        <div className="max-w-[640px]">
          {book.sections.map((s) => (
            <section key={s.heading} className="mb-12">
              <h2 className="mb-4 font-serif text-[26px] font-medium leading-[1.3] min-[900px]:text-[28px]">
                {s.heading}
              </h2>
              <div className="prose-read">
                {s.paras.map((p) => (
                  <p key={p.slice(0, 40)}>{p}</p>
                ))}
              </div>
            </section>
          ))}

          {/* Inside */}
          {book.inside && (
            <section className="mb-12">
              <h2 className="mb-5 font-serif text-[26px] font-medium leading-[1.3] min-[900px]:text-[28px]">
                {book.insideHeading}
              </h2>
              <ul className="border-t border-ink">
                {book.inside.map((item) => (
                  <li
                    key={item.title}
                    className="grid grid-cols-[8.5rem_1fr] items-baseline gap-4 border-b border-hairline py-3"
                  >
                    <span className="font-serif text-[18px]">{item.title}</span>
                    <span className="text-[14px] leading-[1.6] text-ink-2">
                      {item.note}
                    </span>
                  </li>
                ))}
              </ul>
            </section>
          )}

          {/* Working Theory live stats */}
          {essays && (
            <section className="mb-12">
              <h2 className="mb-5 font-serif text-[26px] font-medium leading-[1.3] min-[900px]:text-[28px]">
                The theories so far
              </h2>
              <p className="prose-read mb-6">
                {essays.length} theories and counting, published since January
                2026. The latest three:
              </p>
              <ul className="border-t border-ink">
                {essays.slice(0, 3).map((e) => (
                  <li key={e.slug} className="border-b border-hairline">
                    <Link
                      href={`/writing/${e.slug}`}
                      className="group grid grid-cols-[4.4rem_1fr] items-baseline gap-4 py-3"
                    >
                      <span className="font-mono text-[12px] text-faint">
                        № {e.no}
                      </span>
                      <span className="font-serif text-[17px] leading-[1.4] transition-colors duration-[250ms] group-hover:text-accent">
                        {e.title}
                      </span>
                    </Link>
                  </li>
                ))}
              </ul>
            </section>
          )}

          {/* Figures */}
          {book.figures && (
            <section className="mb-12">
              <h2 className="mb-5 font-serif text-[26px] font-medium leading-[1.3] min-[900px]:text-[28px]">
                {book.figuresHeading}
              </h2>
              <div className="flex flex-col gap-8">
                {book.figures.map((f) => (
                  <figure key={f.src}>
                    <div className="overflow-hidden rounded-[2px] border border-line bg-white">
                      {/* eslint-disable-next-line @next/next/no-img-element */}
                      <img src={f.src} alt={f.caption} className="block w-full" loading="lazy" />
                    </div>
                    <figcaption className="mt-3 text-[13.5px] leading-[1.6] text-ink-2">
                      {f.caption}
                    </figcaption>
                  </figure>
                ))}
              </div>
            </section>
          )}

          {book.slug === "fish-fun" && <FishSwim />}

          {/* Editions */}
          <section id="editions" className="mb-12 scroll-mt-24">
            <h2 className="mb-5 font-serif text-[26px] font-medium leading-[1.3] min-[900px]:text-[28px]">
              Editions
            </h2>
            <ul className="border-t border-ink">
              {book.editions.map((ed) => (
                <li
                  key={ed.label}
                  className="flex items-baseline justify-between gap-4 border-b border-hairline py-3 text-[14.5px]"
                >
                  {ed.href ? (
                    <a
                      href={ed.href}
                      className="text-accent transition-colors duration-[250ms] hover:text-accent-deep"
                    >
                      {ed.label} →
                    </a>
                  ) : (
                    <span>{ed.label}</span>
                  )}
                  <span className="font-mono text-[11px] uppercase tracking-[0.12em] text-faint">
                    {ed.note}
                  </span>
                </li>
              ))}
            </ul>
          </section>

          {/* Related */}
          {book.related && (
            <section className="mb-12">
              <h2 className="mb-5 font-serif text-[26px] font-medium leading-[1.3] min-[900px]:text-[28px]">
                Around the book
              </h2>
              <ul className="border-t border-ink">
                {book.related.map((r) => (
                  <li
                    key={r.label}
                    className="grid grid-cols-[1fr_auto] items-baseline gap-4 border-b border-hairline py-3 text-[14.5px] min-[700px]:grid-cols-[14rem_1fr]"
                  >
                    <a
                      href={r.href}
                      className="text-accent transition-colors duration-[250ms] hover:text-accent-deep"
                    >
                      {r.label} →
                    </a>
                    <span className="text-[13.5px] text-ink-2">{r.note}</span>
                  </li>
                ))}
              </ul>
            </section>
          )}

          {/* History */}
          {book.history && (
            <section className="mb-4">
              <h2 className="mb-6 font-serif text-[26px] font-medium leading-[1.3] min-[900px]:text-[28px]">
                History
              </h2>
              <div className="flex flex-col gap-6 border-l border-btnline pl-8">
                {book.history.map((h, i) => (
                  <div key={h.date + i} className="relative">
                    <div
                      className={`absolute -left-[36.5px] top-1.5 h-2 w-2 rounded-full ${
                        /to come/i.test(h.date) ? "border border-faint bg-paper" : "bg-ink"
                      }`}
                    />
                    <div className="font-mono text-[11.5px] text-faint">{h.date}</div>
                    <div className="mt-1 font-serif text-[17px] leading-[1.5] text-ink-2">
                      {h.note}
                    </div>
                  </div>
                ))}
              </div>
            </section>
          )}
        </div>

        <div className="min-[1000px]:sticky min-[1000px]:top-10">
          <Connections id={`book:${book.slug}`} />
        </div>
        </div>
      </Container>
    </SiteShell>
  );
}
