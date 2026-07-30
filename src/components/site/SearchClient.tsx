"use client";

import { useMemo, useState } from "react";
import Link from "next/link";

export type SearchRecord = {
  kind: "Theory" | "Book" | "Project" | "Idea";
  title: string;
  meta: string;
  href: string;
  /** lowercased searchable text (title + tags + full body) */
  hay: string;
};

function score(rec: SearchRecord, tokens: string[]): number {
  let total = 0;
  const title = rec.title.toLowerCase();
  const meta = rec.meta.toLowerCase();
  for (const t of tokens) {
    if (!rec.hay.includes(t) && !title.includes(t) && !meta.includes(t)) {
      return 0; // every token must match somewhere
    }
    if (title.includes(t)) total += 5;
    if (meta.includes(t)) total += 2;
    if (rec.hay.includes(t)) total += 1;
  }
  return total;
}

export function SearchClient({ records }: { records: SearchRecord[] }) {
  const [q, setQ] = useState("");

  const results = useMemo(() => {
    const tokens = q.toLowerCase().split(/\s+/).filter((t) => t.length >= 2);
    if (tokens.length === 0) return null;
    return records
      .map((r) => ({ r, s: score(r, tokens) }))
      .filter((x) => x.s > 0)
      .sort((a, b) => b.s - a.s)
      .slice(0, 30)
      .map((x) => x.r);
  }, [q, records]);

  return (
    <div className="max-w-[640px]">
      <input
        type="search"
        autoFocus
        value={q}
        onChange={(e) => setQ(e.target.value)}
        placeholder="Search theories, books, projects, ideas…"
        className="mt-10 w-full rounded-[2px] border border-btnline bg-paper px-5 py-4 font-serif text-[19px] text-ink placeholder:text-faint focus:border-ink focus:outline-none"
      />

      {results === null ? (
        <p className="mt-8 text-[14.5px] leading-[1.65] text-ink-2">
          The whole library is indexed — every word of every theory, the books,
          the project stories, the garden.
        </p>
      ) : results.length === 0 ? (
        <p className="mt-8 text-[14.5px] leading-[1.65] text-ink-2">
          Nothing on the shelves matches “{q}”. Try fewer or different words.
        </p>
      ) : (
        <div className="mt-8 border-t border-ink">
          <div className="meta border-b border-hairline py-2 !text-[11px]">
            {results.length}
            {results.length === 30 ? "+" : ""} found
          </div>
          {results.map((r) => (
            <Link
              key={r.href}
              href={r.href}
              className="group grid grid-cols-[1fr_auto] items-baseline gap-x-6 border-b border-hairline px-1 py-4 transition-colors duration-[250ms] hover:bg-surface min-[700px]:grid-cols-[100px_1fr]"
            >
              <span className="font-mono text-[10.5px] uppercase tracking-[0.12em] text-faint">
                {r.kind}
              </span>
              <span className="min-w-0">
                <span className="font-serif text-[18px] leading-[1.4] transition-colors duration-[250ms] group-hover:text-accent">
                  {r.title}
                </span>
                <span className="mt-0.5 block text-[13px] leading-[1.55] text-ink-2">
                  {r.meta}
                </span>
              </span>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
