/*
 * Connections — the green links between works (Design Foundations §05).
 * Edges are declared once and rendered in both directions. Only genuine
 * relationships belong here: a book that became an app, an idea that grew
 * into essays. Never decorate.
 *
 * Node ids: "book:<slug>" · "project:<slug>" · "essay:<slug>" · "idea:<no>"
 *           · "video:<slug>" · "series:working-theory"
 */
import { BOOKS } from "@/content/books";
import { PROJECTS } from "@/content/projects";
import { IDEAS } from "@/content/garden";
import { WORKING_THEORY } from "@/content/writing";
import { EPISODES } from "@/content/videos";

export type ConnectionRef = {
  id: string;
  tag: string; // mono type label, e.g. "BOOK · 2026"
  title: string;
  href: string;
};

const EDGES: [string, string][] = [
  // Friends Intelligence: the book compiled into software
  ["book:friends-intelligence", "project:friends-intelligence-app"],
  ["project:friends-intelligence-app", "idea:138"],
  // Fish Fun: the book and the line that produced it
  ["book:fish-fun", "project:fish-fun-production-line"],
  // Working Theory: the series, the method, the book
  ["book:working-theory", "series:working-theory"],
  ["book:working-theory", "idea:138"],
  // Ideas that grew into theories
  ["idea:154", "essay:wt-32"],
  ["idea:171", "essay:wt-46"],
  ["idea:171", "essay:wt-49"],
  // Theories that stepped in front of the camera
  ["video:speaker-theory", "essay:wt-2"],
  ["video:speaker-theory", "series:working-theory"],
  ["video:ai-throughput-shift", "essay:wt-1"],
  ["video:ai-throughput-shift", "series:working-theory"],
  ["video:retrain-the-model", "essay:wt-35"],
  ["video:retrain-the-model", "series:working-theory"],
  ["video:iq-to-eq", "series:working-theory"],
  ["video:goldilocks-load", "series:working-theory"],
  ["video:attention-is-not-cheap", "essay:wt-38"],
  ["video:attention-is-not-cheap", "series:working-theory"],
  ["video:html-is-the-new-english", "essay:wt-46"],
  ["video:html-is-the-new-english", "series:working-theory"],
  ["video:good-work-doesnt-speak", "series:working-theory"],
  ["video:self-assessment", "series:working-theory"],
];

function resolve(id: string): ConnectionRef | null {
  const [kind, key] = id.split(":", 2);

  if (kind === "book") {
    const b = BOOKS.find((x) => x.slug === key);
    if (!b) return null;
    const year = b.status === "published" ? "2026" : "in progress";
    return { id, tag: `Book · ${year}`, title: b.title, href: `/books/${b.slug}` };
  }
  if (kind === "project") {
    const p = PROJECTS.find((x) => x.slug === key);
    if (!p) return null;
    return { id, tag: `Project · ${p.years}`, title: p.name, href: `/projects/${p.slug}` };
  }
  if (kind === "essay") {
    const e = WORKING_THEORY.find((x) => `wt-${x.no.toLowerCase()}` === key);
    if (!e) return null;
    return {
      id,
      tag: `Theory · № ${e.no}`,
      title: e.title,
      href: `/writing/wt-${e.no.toLowerCase()}`,
    };
  }
  if (kind === "idea") {
    const i = IDEAS.find((x) => String(x.no) === key);
    if (!i) return null;
    return {
      id,
      tag: `Idea · № ${i.no}`,
      title: i.lines.join(" "),
      href: `/garden#idea-${i.no}`,
    };
  }
  if (kind === "video") {
    const v = EPISODES.find((x) => x.slug === key && x.status === "published");
    if (!v) return null;
    return {
      id,
      tag: `Video · Ep. ${v.sequence}`,
      title: v.title,
      href: `/videos/${v.slug}`,
    };
  }
  if (kind === "series" && key === "working-theory") {
    return {
      id,
      tag: `Series · ${WORKING_THEORY.length} essays`,
      title: "Working Theory",
      href: "/writing",
    };
  }
  return null;
}

export function getConnections(id: string): ConnectionRef[] {
  const neighbours: string[] = [];
  for (const [a, b] of EDGES) {
    if (a === id) neighbours.push(b);
    else if (b === id) neighbours.push(a);
  }
  return neighbours
    .map(resolve)
    .filter((r): r is ConnectionRef => r !== null);
}
