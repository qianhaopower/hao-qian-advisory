import type { Metadata } from "next";
import { TodayRoom } from "@/components/today/TodayRoom";

export const metadata: Metadata = {
  title: "One thing today · 今天只做一件事",
  description:
    "Every Friends Intelligence episode leaves one small action — to sleep, eat, move, feel and love a little better. Each is printed as a card: turn one over a day, do it, and that is enough. 每集视频留下一个动作，印成一张牌；每天翻一张，做一件。",
  alternates: {
    canonical: "https://haoqian.co/today",
    languages: {
      "zh-Hans": "https://haoqian.co/today",
      en: "https://haoqian.co/today/en",
    },
  },
};

/*
 * /today — 今天只做一件事 (2026-11-10). The Friends Intelligence films, made
 * usable: one action per episode, one card per day. Cards are written by hand
 * in src/content/today.ts; the drawings are in components/today/CardArt.tsx.
 * This is the Chinese edition; /today/en is the same deck in English.
 */
export default function TodayPage() {
  return <TodayRoom lang="zh" />;
}
