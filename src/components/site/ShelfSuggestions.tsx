"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

export type Suggestion = { no: string; title: string; slug: string };

/* Three theories pulled at random for the lost visitor — fresh every visit. */
export function ShelfSuggestions({ pool }: { pool: Suggestion[] }) {
  const [picks, setPicks] = useState<Suggestion[] | null>(null);

  useEffect(() => {
    const shuffled = [...pool];
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    setPicks(shuffled.slice(0, 3));
  }, [pool]);

  if (!picks) return <div className="h-[170px]" aria-hidden="true" />;

  return (
    <div className="border-t border-ink">
      {picks.map((p) => (
        <Link
          key={p.slug}
          href={`/writing/${p.slug}`}
          className="group grid grid-cols-[1fr_auto] items-baseline gap-x-6 border-b border-hairline px-1 py-4 transition-colors duration-[250ms] hover:bg-surface min-[700px]:grid-cols-[80px_1fr_auto]"
        >
          <span className="hidden font-mono text-[12px] text-faint min-[700px]:block">
            № {p.no}
          </span>
          <span className="font-serif text-[18px] leading-[1.4] transition-colors duration-[250ms] group-hover:text-accent">
            {p.title}
          </span>
          <span className="text-[13px] text-faint transition-colors duration-[250ms] group-hover:text-accent">
            →
          </span>
        </Link>
      ))}
    </div>
  );
}
