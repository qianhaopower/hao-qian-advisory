import type { Metadata } from "next";
import {
  SiteShell,
  Container,
  Kicker,
  PageTitle,
  Lede,
  Note,
} from "@/components/site/Chrome";

export const metadata: Metadata = {
  title: "Books",
  description:
    "The books of Hao Qian: Friends Intelligence, Fish Fun, and Working Theory in progress.",
};

type Book = {
  meta: string;
  title: string;
  summary: string;
  cover?: { src: string; alt: string };
  coverLabel?: string;
  editions: { label: string; note: string; href?: string }[];
};

const BOOKS: Book[] = [
  {
    meta: "Book · 2026",
    title: "Friends Intelligence",
    summary:
      "The hidden patterns connecting money, relationships, health, and decisions. Seven everyday intelligences — F.R.I.E.N.D.S — and how they cluster.",
    cover: {
      src: "/friendsintelligence/cover.jpg",
      alt: "Friends Intelligence cover",
    },
    editions: [
      {
        label: "Paperback & Kindle",
        note: "available",
        href: "https://www.amazon.com.au/dp/B0H5R5C8B6",
      },
      {
        label: "Companion app",
        note: "friendsintelligence.net",
        href: "https://friendsintelligence.net",
      },
      { label: "Audiobook", note: "to come" },
      { label: "中文版 · Chinese edition", note: "to come" },
    ],
  },
  {
    meta: "Book · 2026 · with my daughter",
    title: "Fish Fun",
    summary:
      "By Isabelle Qian, with her dad. Goldie, Zoey, Lulu and Stella — more than a hundred tiny adventures, every picture drawn by a six-year-old.",
    cover: { src: "/books/fish-fun-cover.jpg", alt: "Fish Fun cover" },
    editions: [
      {
        label: "Hardcover · 400 pages",
        note: "available",
        href: "https://www.amazon.com/dp/B0HBVBBBBX",
      },
    ],
  },
  {
    meta: "Book · in progress",
    title: "Working Theory",
    summary:
      "The book the essay series is quietly becoming — compiled from the theories, one per week, as they prove themselves.",
    coverLabel: "manuscript open",
    editions: [{ label: "The series so far", note: "№ 2–52", href: "/writing" }],
  },
];

export default function BooksPage() {
  return (
    <SiteShell current="/books">
      <Container>
        <section className="pt-16 min-[900px]:pt-20">
          <Kicker>Books · 2 published · 1 underway</Kicker>
          <PageTitle>The shelf so far.</PageTitle>
          <Lede>
            Books are the slowest, most permanent thing I make. Each one gets a
            home here: why it exists, what is inside, and every edition it
            grows.
          </Lede>
        </section>

        <section className="mt-14 flex flex-col gap-6">
          {BOOKS.map((book) => (
            <article
              key={book.title}
              className="flex flex-col gap-7 rounded-[2px] border border-line bg-paper p-7 transition-colors duration-[250ms] hover:border-faint min-[700px]:flex-row min-[900px]:p-8"
            >
              {book.cover ? (
                // eslint-disable-next-line @next/next/no-img-element
                <img
                  src={book.cover.src}
                  alt={book.cover.alt}
                  className="h-[172px] w-[120px] flex-none border border-line object-cover"
                  loading="lazy"
                />
              ) : (
                <div className="flex h-[172px] w-[120px] flex-none items-center justify-center border border-line bg-surface p-3 text-center font-mono text-[10px] uppercase tracking-[0.12em] text-faint">
                  {book.coverLabel}
                </div>
              )}
              <div className="flex min-w-0 flex-1 flex-col gap-2.5">
                <div className="meta !text-[11px]">{book.meta}</div>
                <h2 className="font-serif text-[24px] font-normal leading-[1.25]">
                  {book.title}
                </h2>
                <p className="max-w-[560px] text-[14px] leading-[1.6] text-ink-2">
                  {book.summary}
                </p>
                <ul className="mt-2 flex max-w-[560px] flex-col border-t border-hairline">
                  {book.editions.map((ed) => (
                    <li
                      key={ed.label}
                      className="flex items-baseline justify-between gap-4 border-b border-hairline py-2 text-[13.5px]"
                    >
                      {ed.href ? (
                        <a
                          href={ed.href}
                          className="text-accent transition-colors duration-[250ms] hover:text-accent-deep"
                        >
                          {ed.label} →
                        </a>
                      ) : (
                        <span className="text-ink">{ed.label}</span>
                      )}
                      <span className="font-mono text-[11px] uppercase tracking-[0.12em] text-faint">
                        {ed.note}
                      </span>
                    </li>
                  ))}
                </ul>
              </div>
            </article>
          ))}
        </section>

        <div className="mt-10 max-w-[720px]">
          <Note>
            Full book pages — why each was written, contents, previews and
            update history — are the next shelf to be built.
          </Note>
        </div>
      </Container>
    </SiteShell>
  );
}
