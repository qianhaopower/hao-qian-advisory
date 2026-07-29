import type { Metadata } from "next";
import {
  SiteShell,
  Container,
  Kicker,
  PageTitle,
  Lede,
} from "@/components/site/Chrome";
import { IDEAS } from "@/content/garden";

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
          {IDEAS.map((idea) => (
            <div
              key={idea.no}
              className="border-b border-hairline py-10 first:border-t first:border-t-ink"
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
            </div>
          ))}
        </section>

        <p className="mt-10 max-w-[640px] text-[14.5px] leading-[1.65] text-ink-2">
          Ideas link to the works they grow into — essays, projects, books.
          Those <span className="text-connect">connections</span> become
          visible as the library fills.
        </p>
      </Container>
    </SiteShell>
  );
}
