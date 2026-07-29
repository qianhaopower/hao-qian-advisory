import type { Metadata } from "next";
import {
  SiteShell,
  Container,
  Kicker,
  PageTitle,
  Lede,
} from "@/components/site/Chrome";
import { getEssays, monthLabel } from "@/lib/essays";
import { WritingIndex, type EssayListItem } from "@/components/site/WritingIndex";

export const metadata: Metadata = {
  title: "Writing",
  description:
    "Working Theory — Hao Qian's essay series on AI, engineering, systems and leadership. All 52 essays, readable here.",
};

export default function WritingPage() {
  const essays = getEssays();
  const items: EssayListItem[] = essays.map((e) => ({
    slug: e.slug,
    no: e.no,
    title: e.title,
    date: e.date,
    month: monthLabel(e.date),
    topics: e.topics,
    series: e.series,
    minutes: e.minutes,
  }));

  return (
    <SiteShell current="/writing">
      <Container>
        <section className="pt-16 min-[900px]:pt-20">
          <Kicker>Working Theory · № 1–52 · roughly two a week since Jan 2026</Kicker>
          <PageTitle>One theory at a time.</PageTitle>
          <Lede>
            A numbered essay series on AI, engineering, systems thinking and
            leadership — serialised on LinkedIn, but this library is where
            every theory lives in full.
          </Lede>
        </section>

        <WritingIndex essays={items} />
      </Container>
    </SiteShell>
  );
}
