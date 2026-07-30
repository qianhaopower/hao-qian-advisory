import type { Metadata } from "next";
import Link from "next/link";
import {
  SiteShell,
  Container,
  Kicker,
  PageTitle,
  Lede,
} from "@/components/site/Chrome";
import { IDEAS } from "@/content/garden";
import { getConnections } from "@/content/connections";

export const metadata: Metadata = {
  title: "Digital Garden",
  description:
    "Numbered ideas, tended over years — Hao Qian's digital garden. No publish dates, no finish line.",
};

export default function GardenPage() {
  return (
    <SiteShell current="/garden">
      <Container>
        <section className="pt-16 min-[900px]:pt-20">
          <Kicker>Digital Garden · {IDEAS.length} ideas · growing</Kicker>
          <PageTitle>Ideas that are still growing.</PageTitle>
          <Lede>
            Not a blog. These are working ideas from a private numbered log —
            planted, revised without ceremony, and never declared finished.
            Only the ones worth tending surface here.
          </Lede>
        </section>

        <section className="mt-14 max-w-[640px]">
          {IDEAS.map((idea) => {
            const refs = getConnections(`idea:${idea.no}`);
            return (
              <div
                key={idea.no}
                id={`idea-${idea.no}`}
                className="scroll-mt-24 border-b border-hairline py-10 first:border-t first:border-t-ink"
              >
                <div className="meta !text-[11px]">
                  Idea № {idea.no} · planted {idea.planted} · {idea.status}
                </div>
                <div className="mt-4 border-l-2 border-ink pl-7">
                  {idea.lines.map((line) => (
                    <p
                      key={line}
                      className="font-serif text-[23px] italic leading-[1.5] text-ink"
                    >
                      {line}
                    </p>
                  ))}
                </div>
                {refs.length > 0 && (
                  <div className="mt-5 flex flex-wrap items-baseline gap-x-6 gap-y-2 pl-7">
                    <span className="font-mono text-[10.5px] uppercase tracking-[0.12em] text-connect">
                      Grew into
                    </span>
                    {refs.map((r) => (
                      <Link
                        key={r.id}
                        href={r.href}
                        className="text-[13.5px] text-connect transition-colors duration-[250ms] hover:text-connect-deep"
                      >
                        {r.title} →
                      </Link>
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </section>

        <p className="mt-10 max-w-[640px] text-[14.5px] leading-[1.65] text-ink-2">
          Ideas link to the works they grow into — essays, projects, books.
          Follow the <span className="text-connect">green</span>.
        </p>
      </Container>
    </SiteShell>
  );
}
