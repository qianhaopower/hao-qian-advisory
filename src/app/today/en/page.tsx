import type { Metadata } from "next";
import { TodayRoom } from "@/components/today/TodayRoom";

export const metadata: Metadata = {
  title: "One thing today",
  description:
    "One small thing a day — to sleep, eat, move, feel and love a little better. An illustrated card from each Friends Intelligence episode: turn one over, do it, and that is enough.",
  alternates: {
    canonical: "https://haoqian.co/today/en",
    languages: {
      "zh-Hans": "https://haoqian.co/today",
      en: "https://haoqian.co/today/en",
    },
  },
};

/* /today/en — the English edition of the deck (2026-11-11), for readers who
 * arrive from LinkedIn. Same cards, same drawings; see TodayRoom. */
export default function TodayEnglishPage() {
  return <TodayRoom lang="en" />;
}
