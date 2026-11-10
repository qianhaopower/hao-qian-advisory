import { TODAY_CARDS } from "@/content/today";
import { getEpisode, formatDuration } from "@/lib/videos";
import type { DeckCard } from "@/lib/today-deck";

/*
 * Server half of the /today deck: joins each hand-written card to its episode.
 * Only published episodes carry a card in public; a card pointing at a slug
 * that does not exist fails the build, so the deck can never cite a film that
 * is not there.
 */

export function getDeck(): DeckCard[] {
  const seen = new Set<string>();
  const deck: DeckCard[] = [];
  for (const card of TODAY_CARDS) {
    const episode = getEpisode(card.episode);
    if (!episode) {
      throw new Error(`today.ts: no episode with slug "${card.episode}"`);
    }
    if (seen.has(card.episode)) {
      throw new Error(`today.ts: two cards for "${card.episode}"`);
    }
    seen.add(card.episode);
    if (episode.status !== "published") continue;
    deck.push({
      ...card,
      no: episode.sequence,
      noLabel: String(episode.sequence).padStart(2, "0"),
      title: episode.title,
      duration: episode.durationSeconds
        ? formatDuration(episode.durationSeconds)
        : undefined,
      href: `/videos/${episode.slug}`,
    });
  }
  return deck.sort((a, b) => a.no - b.no);
}

export function getCardForEpisode(slug: string): DeckCard | undefined {
  return getDeck().find((c) => c.episode === slug);
}

/** Home-index meta line — computed, so the count stays honest. */
export function todayIndexMeta(): string {
  const n = getDeck().length;
  return `${n} card${n === 1 ? "" : "s"} · one a day`;
}
