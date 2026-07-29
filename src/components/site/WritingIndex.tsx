"use client";

import { useMemo, useState } from "react";
import Link from "next/link";

export type EssayListItem = {
  slug: string;
  no: string;
  title: string;
  date: string;
  month: string;
  topics: string[];
  series?: string;
  minutes: number;
};

export function WritingIndex({ essays }: { essays: EssayListItem[] }) {
  const [topic, setTopic] = useState<string | null>(null);

  const topics = useMemo(() => {
    const counts = new Map<string, number>();
    for (const e of essays)
      for (const t of e.topics) counts.set(t, (counts.get(t) ?? 0) + 1);
    return Array.from(counts.entries())
      .filter(([, n]) => n >= 3)
      .sort((a, b) => b[1] - a[1]);
  }, [essays]);

  const visible = topic
    ? essays.filter((e) => e.topics.includes(topic))
    : essays;

  let lastMonth = "";

  return (
    <div>
      <div className="mt-10 flex flex-wrap items-baseline gap-x-2 gap-y-2">
        <button
          onClick={() => setTopic(null)}
          className={`rounded-[2px] border px-3 py-1 text-[13px] transition-colors duration-[250ms] ${
            topic === null
              ? "border-ink bg-ink text-paper"
              : "border-btnline text-ink-2 hover:border-ink hover:text-ink"
          }`}
        >
          All · {essays.length}
        </button>
        {topics.map(([t, n]) => (
          <button
            key={t}
            onClick={() => setTopic(topic === t ? null : t)}
            className={`rounded-[2px] border px-3 py-1 text-[13px] transition-colors duration-[250ms] ${
              topic === t
                ? "border-ink bg-ink text-paper"
                : "border-btnline text-ink-2 hover:border-ink hover:text-ink"
            }`}
          >
            {t} · {n}
          </button>
        ))}
      </div>

      <div className="mt-10 border-t border-ink">
        {visible.map((e) => {
          const monthHeader =
            e.month !== lastMonth ? (
              <div className="meta border-b border-hairline pb-2 pt-8">
                {e.month}
              </div>
            ) : null;
          lastMonth = e.month;
          return (
            <div key={e.slug}>
              {monthHeader}
              <Link
                href={`/writing/${e.slug}`}
                className="group grid grid-cols-[1fr_auto] items-baseline gap-x-6 border-b border-hairline px-1 py-[18px] transition-colors duration-[250ms] hover:bg-surface min-[900px]:grid-cols-[110px_1fr_auto]"
              >
                <span className="hidden font-mono text-[12px] text-faint min-[900px]:block">
                  № {e.no}
                </span>
                <span className="min-w-0">
                  <span className="font-serif text-[19px] leading-[1.4] group-hover:text-accent">
                    <span className="mr-3 font-mono text-[12px] text-faint min-[900px]:hidden">
                      № {e.no}
                    </span>
                    {e.title}
                  </span>
                  {e.series ? (
                    <span className="ml-3 font-mono text-[11px] uppercase tracking-[0.12em] text-faint">
                      {e.series}
                    </span>
                  ) : null}
                </span>
                <span className="font-mono text-[12px] text-faint">
                  {e.minutes} min
                </span>
              </Link>
            </div>
          );
        })}
      </div>
    </div>
  );
}
