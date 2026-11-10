import Link from "next/link";
import { SiteShell, Container, Kicker, Note } from "@/components/site/Chrome";
import { TodayDeck } from "@/components/today/TodayDeck";
import { getDeck } from "@/lib/today";
import { deckPath, type Lang } from "@/lib/today-deck";
import { SITE } from "@/content/site";

/*
 * The /today room in one of its two editions:
 *   /today     中文 — the original, for the 小红书 audience
 *   /today/en  English — the same deck, for readers who come from LinkedIn
 * Same cards, same drawings, same day's card; the lettering changes. The films
 * the cards point to are in Chinese either way, and the English card says so.
 */
export function TodayRoom({ lang }: { lang: Lang }) {
  const deck = getDeck();
  const en = lang === "en";

  return (
    <SiteShell current="/today">
      <Container>
        <section className="pt-10 min-[900px]:pt-20">
          <Kicker>
            One thing today
            {deck.length > 0
              ? ` · ${deck.length} card${deck.length === 1 ? "" : "s"}`
              : ""}{" "}
            · from{" "}
            <Link
              href="/videos#friends-intelligence"
              className="transition-colors duration-[250ms] hover:text-accent"
            >
              Friends Intelligence on camera
            </Link>
          </Kicker>
          {en ? (
            <h1 className="mt-6 font-serif text-[38px] font-normal leading-[1.12] tracking-[-0.01em] min-[900px]:text-[52px]">
              One thing today.
            </h1>
          ) : (
            <h1
              lang="zh-Hans"
              className="zh-display mt-6 text-[38px] leading-[1.15] min-[900px]:text-[52px]"
            >
              今天只做一件事
            </h1>
          )}
          <p className="mt-4 max-w-[640px] font-serif text-[18px] leading-[1.55] text-ink-2 min-[900px]:mt-5 min-[900px]:text-[22px]">
            Every episode leaves one small action. Each is printed as a card —
            turn one over a day, do it, and that is enough.{" "}
            {!en && (
              <span lang="zh-Hans">
                每集视频留下一个动作，印成一张牌。每天翻一张，做一件。
              </span>
            )}
          </p>
          <p className="mt-4 text-[13.5px]">
            <Link
              href={deckPath(en ? "zh" : "en")}
              lang={en ? "zh-Hans" : "en"}
              className="text-accent transition-colors duration-[250ms] hover:text-accent-deep"
            >
              {en ? "中文版 →" : "The same deck in English →"}
            </Link>
          </p>
        </section>

        {deck.length === 0 ? (
          <div className="mt-14 max-w-[720px]">
            <Note label="Empty · deliberately">
              No cards yet. A card is printed only when an episode really ends
              in something to do.
            </Note>
          </div>
        ) : (
          <TodayDeck cards={deck} handle={SITE.xiaohongshuHandle} lang={lang} />
        )}

        <p className="meta mt-16 max-w-[640px] !normal-case !leading-[1.8] !tracking-[0.04em]">
          What you turn over and tick off is kept only in this browser. Nothing
          is sent anywhere, and nobody is counted.
          {en &&
            " The films behind the cards are in Chinese, with a full transcript on each episode page."}
        </p>
      </Container>
    </SiteShell>
  );
}
