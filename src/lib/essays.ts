import fs from "node:fs";
import path from "node:path";
import { WORKING_THEORY, type WorkingTheoryPost } from "@/content/writing";
import imageMap from "@/content/essay-images.json";

/*
 * Build-time loader for Working Theory essays.
 * Source of truth: content-src/working-theory-text/*.txt (one file per post,
 * harvested from LinkedIn with a URL/DATE header) joined to the canonical
 * numbering in src/content/writing.ts via the activity URN.
 * All pages are statically generated, so fs access happens only at build.
 */

export type Essay = WorkingTheoryPost & {
  slug: string;
  urn: string;
  topics: string[];
  series?: string;
  /** paragraph blocks; each block is a list of lines (soft breaks) */
  blocks: string[][];
  /** public paths of the figures posted with the essay, in order */
  images: string[];
  minutes: number;
  excerpt: string;
};

const TEXT_DIR = path.join(process.cwd(), "content-src", "working-theory-text");

/** hashtags that mark the series itself rather than a topic */
const NON_TOPIC_TAGS = new Set(["workingtheory", "workingtheories"]);

const TAG_DISPLAY: Record<string, string> = {
  AI: "AI",
  DevOps: "DevOps",
  FutureOfWork: "Future of Work",
  SignalVsNoise: "Signal vs Noise",
  MeaningOverOrigin: "Meaning Over Origin",
};

function displayTag(raw: string): string {
  if (TAG_DISPLAY[raw]) return TAG_DISPLAY[raw];
  // PascalCase → spaced words, keeping runs of capitals together (e.g. "AI")
  return raw
    .replace(/([a-z])([A-Z])/g, "$1 $2")
    .replace(/([A-Z]+)([A-Z][a-z])/g, "$1 $2");
}

const SERIES_RULES: [RegExp, string][] = [
  [/octopus manager/i, "The Octopus Manager"],
  [/silicon brain/i, "Silicon Brain"],
  [/ai playbook/i, "AI Playbook"],
  [/desk theory/i, "Desk Theory"],
];

function normalise(s: string): string {
  return s.toLowerCase().replace(/[^a-z0-9]+/g, " ").trim();
}

function parseFile(filePath: string) {
  const raw = fs.readFileSync(filePath, "utf-8");
  const lines = raw.split("\n");
  const urlLine = lines[0] ?? "";
  const urn = urlLine.match(/activity[:/](\d{15,})/)?.[1] ?? "";
  let body = lines.slice(2).join("\n").trim();

  // collect trailing hashtag lines → topics
  const tags: string[] = [];
  const bodyLines = body.split("\n");
  while (bodyLines.length > 0) {
    const last = bodyLines[bodyLines.length - 1].trim();
    if (last === "" || /^(hashtag#\S+\s*)+$/.test(last)) {
      for (const m of last.matchAll(/hashtag#(\S+)/g)) tags.push(m[1]);
      bodyLines.pop();
    } else break;
  }
  body = bodyLines.join("\n").trim();

  return { urn, body, tags };
}

function stripTitleLines(body: string, canonicalTitle: string): string {
  const lines = body.split("\n");
  let i = 0;
  while (i < lines.length && lines[i].trim() === "") i++;
  // drop the "Working Theory #N — …" header line
  if (i < lines.length && /^working\s+theor(y|ies)/i.test(lines[i].trim())) {
    i++;
    while (i < lines.length && lines[i].trim() === "") i++;
    // drop a following line that just repeats the canonical title
    const next = normalise(lines[i] ?? "");
    const title = normalise(canonicalTitle);
    if (next && title && (next === title || next.startsWith(title))) {
      i++;
    }
  }
  return lines.slice(i).join("\n").trim();
}

function toBlocks(body: string): string[][] {
  return body
    .split(/\n\s*\n/)
    .map((block) =>
      block
        .split("\n")
        .map((l) => l.trim())
        .filter((l) => l !== "")
    )
    .filter((b) => b.length > 0);
}

let cache: Essay[] | null = null;

export function getEssays(): Essay[] {
  if (cache) return cache;

  const byUrn = new Map<string, { body: string; tags: string[] }>();
  for (const file of fs.readdirSync(TEXT_DIR)) {
    if (!file.endsWith(".txt")) continue;
    const { urn, body, tags } = parseFile(path.join(TEXT_DIR, file));
    if (urn) byUrn.set(urn, { body, tags });
  }

  cache = WORKING_THEORY.map((post) => {
    const urn = post.url.match(/activity[-:/](\d{15,})/)?.[1] ?? "";
    const parsed = byUrn.get(urn);
    if (!parsed) {
      throw new Error(`No essay text found for Working Theory №${post.no} (urn ${urn})`);
    }
    const body = stripTitleLines(parsed.body, post.title);
    const blocks = toBlocks(body);
    const words = body.split(/\s+/).filter(Boolean).length;
    const topics = Array.from(
      new Set(
        parsed.tags
          .filter((t) => !NON_TOPIC_TAGS.has(t.toLowerCase()))
          .map(displayTag)
      )
    );
    const series = SERIES_RULES.find(([re]) => re.test(post.title))?.[1];
    const firstBlock = blocks[0]?.join(" ") ?? "";
    const excerpt =
      firstBlock.length > 180 ? `${firstBlock.slice(0, 177).trimEnd()}…` : firstBlock;

    const slug = `wt-${post.no.toLowerCase()}`;
    const images = ((imageMap as Record<string, string[]>)[slug] ?? []).map(
      (f) => `/writing/images/${f}`
    );

    return {
      ...post,
      slug,
      urn,
      topics,
      series,
      blocks,
      images,
      minutes: Math.max(1, Math.round(words / 200)),
      excerpt,
    };
  });

  return cache;
}

export function getEssay(slug: string): Essay | undefined {
  return getEssays().find((e) => e.slug === slug);
}

export function formatDate(iso: string): string {
  return new Date(`${iso}T00:00:00Z`).toLocaleDateString("en-AU", {
    day: "numeric",
    month: "long",
    year: "numeric",
    timeZone: "UTC",
  });
}

export function monthLabel(iso: string): string {
  return new Date(`${iso}T00:00:00Z`).toLocaleDateString("en-AU", {
    month: "long",
    year: "numeric",
    timeZone: "UTC",
  });
}
