import type { Metadata } from "next";
import Link from "next/link";
import { SiteShell, Container, Kicker, Note } from "@/components/site/Chrome";
import { TodayDeck } from "@/components/today/TodayDeck";
import { getDeck } from "@/lib/today";
import { SITE } from "@/content/site";

export const metadata: Metadata = {
  title: "One thing today · 今天只做一件事",
  description:
    "Every Friends Intelligence episode leaves one small action — to sleep, eat, move, feel and love a little better. Each is printed as a card: turn one over a day, do it, and that is enough. 每集视频留下一个动作，印成一张牌；每天翻一张，做一件。",
  alternates: { canonical: "https://haoqian.co/today" },
};

/*
 * /today — 今天只做一件事 (2026-11-10). The Friends Intelligence films, made
 * usable: one action per episode, one card per day. Cards are written by hand
 * in src/content/today.ts; the drawings are in components/today/CardArt.tsx.
 */
export default function TodayPage() {
  const deck = getDeck();

  return (
    <SiteShell>
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
          <h1
            lang="zh-Hans"
            className="zh-display mt-6 text-[38px] leading-[1.15] min-[900px]:text-[52px]"
          >
            今天只做一件事
          </h1>
          <p className="mt-4 max-w-[640px] font-serif text-[18px] leading-[1.55] text-ink-2 min-[900px]:mt-5 min-[900px]:text-[22px]">
            Every episode leaves one small action. Each is printed as a card —
            turn one over a day, do it, and that is enough.{" "}
            <span lang="zh-Hans">
              每集视频留下一个动作，印成一张牌。每天翻一张，做一件。
            </span>
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
          <TodayDeck cards={deck} handle={SITE.xiaohongshuHandle} />
        )}

        <p className="meta mt-16 max-w-[640px] !normal-case !leading-[1.8] !tracking-[0.04em]">
          What you turn over and tick off is kept only in this browser. Nothing
          is sent anywhere, and nobody is counted.
        </p>
      </Container>
    </SiteShell>
  );
}
