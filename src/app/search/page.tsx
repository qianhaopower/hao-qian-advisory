import type { Metadata } from "next";
import {
  SiteShell,
  Container,
  Kicker,
  PageTitle,
} from "@/components/site/Chrome";
import { SearchClient, type SearchRecord } from "@/components/site/SearchClient";
import { getEssays, formatDate } from "@/lib/essays";
import { BOOKS } from "@/content/books";
import { PROJECTS } from "@/content/projects";
import { IDEAS } from "@/content/garden";
import { BALLOON_ARCHIVE_ITEMS } from "@/content/balloon-archive";
import { getPublishedEpisodes, getSeries } from "@/lib/videos";

export const metadata: Metadata = {
  title: "Search",
  description: "Search the whole library — every theory, book, project and idea.",
};

function buildRecords(): SearchRecord[] {
  const essays: SearchRecord[] = getEssays().map((e) => ({
    kind: "Theory",
    title: `№ ${e.no} — ${e.title}`,
    meta: `${formatDate(e.date)}${e.topics.length ? ` · ${e.topics.join(" · ")}` : ""}`,
    href: `/writing/${e.slug}`,
    hay: [e.title, e.topics.join(" "), e.series ?? "", e.blocks.flat().join(" ")]
      .join(" ")
      .toLowerCase(),
  }));

  const books: SearchRecord[] = BOOKS.map((b) => ({
    kind: "Book",
    title: b.title,
    meta: b.oneLiner,
    href: `/books/${b.slug}`,
    hay: [
      b.title,
      b.subtitle ?? "",
      b.byline ?? "",
      b.oneLiner,
      b.sections.map((s) => `${s.heading} ${s.paras.join(" ")}`).join(" "),
      (b.inside ?? []).map((i) => `${i.title} ${i.note}`).join(" "),
    ]
      .join(" ")
      .toLowerCase(),
  }));

  const projects: SearchRecord[] = PROJECTS.map((p) => ({
    kind: "Project",
    title: p.name,
    meta: p.oneLiner,
    href: `/projects/${p.slug}`,
    hay: [
      p.name,
      p.oneLiner,
      p.status,
      (p.facts ?? []).join(" "),
      p.sections.map((s) => `${s.heading} ${s.paras.join(" ")}`).join(" "),
    ]
      .join(" ")
      .toLowerCase(),
  }));

  const ideas: SearchRecord[] = IDEAS.map((i) => ({
    kind: "Idea",
    title: i.lines.join(" "),
    meta: `Idea № ${i.no} · planted ${i.planted} · ${i.status}`,
    href: `/garden#idea-${i.no}`,
    hay: i.lines.join(" ").toLowerCase(),
  }));

  const episodes: SearchRecord[] = getPublishedEpisodes().map((e) => ({
    kind: "Video",
    title: `Ep. ${e.sequence} — ${e.title}`,
    meta: `${getSeries(e).name} · ${e.publishedAt ? formatDate(e.publishedAt) : ""}`,
    href: `/videos/${e.slug}`,
    hay: [
      e.title,
      e.hook,
      e.summary,
      (e.keyPoints ?? []).join(" "),
      (e.transcript ?? []).join(" "),
    ]
      .join(" ")
      .toLowerCase(),
  }));

  const balloons: SearchRecord[] = [
    {
      kind: "Balloons",
      title: "Little Wow Balloons — the balloon room",
      meta: `${BALLOON_ARCHIVE_ITEMS.length} works · archived from Instagram`,
      href: "/balloons",
      hay: "balloons balloon art twisting little wow balloons studio markets parties festivals melbourne instagram street box hill twilight southbank mario luigi 气球",
    },
  ];

  return [...essays, ...books, ...projects, ...ideas, ...episodes, ...balloons];
}

export default function SearchPage() {
  const records = buildRecords();
  return (
    <SiteShell current="/search">
      <Container>
        <section className="pt-16 min-[900px]:pt-20">
          <Kicker>Search · {records.length} works indexed</Kicker>
          <PageTitle>Find it on the shelves.</PageTitle>
        </section>
        <SearchClient records={records} />
      </Container>
    </SiteShell>
  );
}
