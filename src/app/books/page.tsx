import type { Metadata } from "next";
import Link from "next/link";
import {
  SiteShell,
  Container,
  Kicker,
  PageTitle,
  Lede,
} from "@/components/site/Chrome";
import { BOOKS } from "@/content/books";

export const metadata: Metadata = {
  title: "Books",
  description:
    "The books of Hao Qian: Friends Intelligence, Fish Fun, and Working Theory in progress.",
};

export default function BooksPage() {
  return (
    <SiteShell current="/books">
      <Container>
        <section className="pt-16 min-[900px]:pt-20">
          <Kicker>Books · 2 published · 1 underway</Kicker>
          <PageTitle>The shelf so far.</PageTitle>
          <Lede>
            Books are the slowest, most permanent thing I make. Each one has a
            home here: why it exists, what is inside, and every edition it
            grows.
          </Lede>
        </section>

        <section className="mt-14 flex flex-col gap-6">
          {BOOKS.map((book) => (
            <Link
              key={book.slug}
              href={`/books/${book.slug}`}
              className="group flex flex-col gap-7 rounded-[2px] border border-line bg-paper p-7 transition-colors duration-[250ms] hover:border-faint min-[700px]:flex-row min-[900px]:p-8"
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
                <div className="meta !text-[11px]">
                  {book.kicker.replace(/^Book · /, "")}
                </div>
                <h2 className="font-serif text-[24px] font-normal leading-[1.25] transition-colors duration-[250ms] group-hover:text-accent">
                  {book.title}
                </h2>
                {book.byline && (
                  <p className="font-serif text-[15px] italic text-ink-2">
                    {book.byline}
                  </p>
                )}
                <p className="max-w-[560px] text-[14px] leading-[1.6] text-ink-2">
                  {book.oneLiner}
                </p>
                <span className="mt-auto pt-2 text-[13.5px] text-accent">
                  Open the book page →
                </span>
              </div>
            </Link>
          ))}
        </section>
      </Container>
    </SiteShell>
  );
}
