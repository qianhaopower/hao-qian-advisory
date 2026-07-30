import { BOOKS } from "@/content/books";
import { PROJECTS } from "@/content/projects";
import { IDEAS } from "@/content/garden";
import { getEssays } from "@/lib/essays";

/*
 * The home constellation is the library's REAL graph — every node is a work,
 * every solid edge a genuine relationship (the same registry the green
 * Connected panels use, plus series chains). Nothing decorative.
 */

export type StarNode = {
  id: string;
  kind: "book" | "project" | "essay" | "idea";
  label: string; // hover chip title
  tag: string; // mono type line
  href: string;
  /** essays in the same series share a cluster so their chain reads as a small constellation */
  cluster?: number;
};

export type StarData = {
  nodes: StarNode[];
  /** indexes into nodes */
  edges: [number, number][];
  counts: { books: number; essays: number; projects: number; ideas: number };
};

/* mirror of the genuine EDGES in content/connections.ts, by node id */
const REAL_EDGES: [string, string][] = [
  ["book:friends-intelligence", "project:friends-intelligence-app"],
  ["project:friends-intelligence-app", "idea:138"],
  ["book:fish-fun", "project:fish-fun-production-line"],
  ["book:working-theory", "idea:138"],
  ["idea:154", "essay:wt-32"],
  ["idea:171", "essay:wt-46"],
  ["idea:171", "essay:wt-49"],
];

export function getStarData(): StarData {
  const nodes: StarNode[] = [];

  for (const b of BOOKS) {
    nodes.push({
      id: `book:${b.slug}`,
      kind: "book",
      label: b.title,
      tag: b.status === "published" ? "Book · 2026" : "Book · in progress",
      href: `/books/${b.slug}`,
    });
  }
  for (const p of PROJECTS) {
    nodes.push({
      id: `project:${p.slug}`,
      kind: "project",
      label: p.name,
      tag: `Project · ${p.years}`,
      href: `/projects/${p.slug}`,
    });
  }
  for (const i of IDEAS) {
    nodes.push({
      id: `idea:${i.no}`,
      kind: "idea",
      label: i.lines.join(" "),
      tag: `Idea · № ${i.no}`,
      href: `/garden#idea-${i.no}`,
    });
  }
  const essays = getEssays();
  const seriesIndex = new Map<string, number>();
  for (const e of essays) {
    let cluster: number | undefined;
    if (e.series) {
      if (!seriesIndex.has(e.series)) seriesIndex.set(e.series, seriesIndex.size);
      cluster = seriesIndex.get(e.series);
    }
    nodes.push({
      id: `essay:${e.slug}`,
      kind: "essay",
      label: e.title,
      tag: `Theory · № ${e.no}`,
      href: `/writing/${e.slug}`,
      cluster,
    });
  }

  const indexOf = new Map(nodes.map((n, i) => [n.id, i]));
  const edges: [number, number][] = [];
  const push = (a: string, b: string) => {
    const ia = indexOf.get(a);
    const ib = indexOf.get(b);
    if (ia !== undefined && ib !== undefined) edges.push([ia, ib]);
  };

  for (const [a, b] of REAL_EDGES) push(a, b);

  // series chains — consecutive parts genuinely belong together
  const bySeries = new Map<string, string[]>();
  for (const e of essays) {
    if (!e.series) continue;
    const list = bySeries.get(e.series) ?? [];
    list.push(`essay:${e.slug}`);
    bySeries.set(e.series, list);
  }
  for (const list of bySeries.values()) {
    // essays arrive newest-first; chain them in published order
    const ordered = [...list].reverse();
    for (let i = 0; i < ordered.length - 1; i++) push(ordered[i], ordered[i + 1]);
  }

  return {
    nodes,
    edges,
    counts: {
      books: BOOKS.length,
      essays: essays.length,
      projects: PROJECTS.length,
      ideas: IDEAS.length,
    },
  };
}
