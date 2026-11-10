/*
 * The /today deck — client-safe half. Types, the five pillars and the daily
 * pick live here so the client bundle never pulls in the episode transcripts
 * (src/content/videos.ts); the server joins cards to episodes in lib/today.ts.
 */

export type PillarId =
  | "nutrition"
  | "exercise"
  | "sleep"
  | "emotion"
  | "relationship";

export type Pillar = {
  id: PillarId;
  zh: string;
  en: string;
  /** The card's outer colour — the only place colour fills a surface, and only inside a card. */
  tint: string;
  /** The paler wash behind the drawing. */
  wash: string;
};

export const PILLARS: Record<PillarId, Pillar> = {
  nutrition: { id: "nutrition", zh: "营养", en: "Nutrition", tint: "#FFE2A8", wash: "#FFF3D1" },
  exercise: { id: "exercise", zh: "运动", en: "Exercise", tint: "#CDEBD3", wash: "#E6F6E9" },
  sleep: { id: "sleep", zh: "睡眠", en: "Sleep", tint: "#CFDDFB", wash: "#E4ECFF" },
  emotion: { id: "emotion", zh: "情绪", en: "Emotion", tint: "#FFD2C8", wash: "#FFE9E3" },
  relationship: { id: "relationship", zh: "关系", en: "Relationship", tint: "#F3D4E8", wash: "#FBEAF4" },
};

/** The daily rotation: one pillar a day, so the deck never serves food five days running. */
export const PILLAR_ORDER: PillarId[] = [
  "nutrition",
  "exercise",
  "sleep",
  "emotion",
  "relationship",
];

/** One card as written by hand in src/content/today.ts. */
export type TodayCard = {
  /** Slug of the episode the action comes from. */
  episode: string;
  pillar: PillarId;
  /** The one thing to do — short lines split with "\n" (≤ 9 characters a line). */
  do: string;
  /** One or two sentences of why, in the episode's own words. */
  why: string;
  /** The moment to do it — a short sticker on the card. Optional. */
  when?: string;
  /** The same card in English — the /today/en edition. */
  en: CardText;
};

export type Lang = "zh" | "en";

/** The words on one face of a card, in one language. */
export type CardText = {
  do: string;
  why: string;
  when?: string;
};

/** The card's words in the language being shown. */
export function cardText(card: TodayCard, lang: Lang): CardText {
  return lang === "en"
    ? card.en
    : { do: card.do, why: card.why, when: card.when };
}

/** A card joined to its published episode — what pages and the client receive. */
export type DeckCard = TodayCard & {
  /** Episode number in the series. */
  no: number;
  /** "02" */
  noLabel: string;
  /** Episode title. */
  title: string;
  /** "2:45" */
  duration?: string;
  /** /videos/<slug> */
  href: string;
};

/** Local calendar day as yyyy-mm-dd. */
export function dateKey(d: Date): string {
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${d.getFullYear()}-${m}-${day}`;
}

/** Days since the epoch for a yyyy-mm-dd key — the deck's clock. */
export function dayNumber(key: string): number {
  const [y, m, d] = key.split("-").map(Number);
  return Math.floor(Date.UTC(y, m - 1, d) / 86_400_000);
}

/**
 * The card for a given day. Pillars take turns day by day; inside a pillar the
 * cards go round in episode order. Deterministic: everyone gets the same card
 * on the same date.
 */
export function cardForDay(cards: DeckCard[], day: number): DeckCard | null {
  const pillars = PILLAR_ORDER.filter((p) => cards.some((c) => c.pillar === p));
  if (pillars.length === 0) return null;
  const pillar = pillars[((day % pillars.length) + pillars.length) % pillars.length];
  const inPillar = cards
    .filter((c) => c.pillar === pillar)
    .sort((a, b) => a.no - b.no);
  const turn = Math.floor(day / pillars.length);
  return inPillar[((turn % inPillar.length) + inPillar.length) % inPillar.length];
}

const WEEKDAYS = ["周日", "周一", "周二", "周三", "周四", "周五", "周六"];
const WEEKDAYS_EN = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
const MONTHS_EN = [
  "Jan", "Feb", "Mar", "Apr", "May", "Jun",
  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
];

/** "11月10日 · 周二" / "Tue · 10 Nov" */
export function dateLabel(key: string, lang: Lang = "zh"): string {
  const [y, m, d] = key.split("-").map(Number);
  const wd = new Date(y, m - 1, d).getDay();
  return lang === "en"
    ? `${WEEKDAYS_EN[wd]} · ${d} ${MONTHS_EN[m - 1]}`
    : `${m}月${d}日 · ${WEEKDAYS[wd]}`;
}

/** Where the deck lives in each language. */
export function deckPath(lang: Lang): string {
  return lang === "en" ? "/today/en" : "/today";
}
