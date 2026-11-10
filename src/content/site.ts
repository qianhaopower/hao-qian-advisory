export const SITE = {
  name: "Hao Qian",
  /* Home h1 + intro since 2026-09-21 (Hao: the flagship is the book, the piano
   * and the street balloons). "Turning ideas into systems." was the 2026-07
   * line; it stays with Working Theory (feed description, STRATEGY.md history). */
  tagline: "A book, a piano, and balloons on the street.",
  intro:
    "I wrote a book about the patterns behind everyday life, I play the piano at home, and I twist balloons at Melbourne’s markets. On weekdays I lead engineering teams and write down what the work teaches me. Everything worth keeping lives here — permanently.",
  principle:
    "Every meaningful thing I create should eventually have a permanent home here.",
  linkedin: "https://www.linkedin.com/in/hao-qian-9ab0b04b/",
  /* 小红书 (Xiaohongshu) — the Friends Intelligence channel, account
   * 「不内耗的人生」 (confirmed by Hao 2026-09-05; rednote.com mirrors the same id). */
  xiaohongshu: "https://www.xiaohongshu.com/user/profile/60af86df0000000001007b70",
  xiaohongshuHandle: "不内耗的人生",
  github: "https://github.com/qianhaopower",
  amazonAuthor: "https://www.amazon.com/author/haoqian",
  goodreads: "https://www.goodreads.com/author/show/71572056.Hao_Qian",
};

export type SectionEntry = {
  href: string;
  label: string;
  meta: string;
  blurb: string;
};

/* Header navigation — six doors (trimmed 2026-11-09: Projects, Talks and
 * the Garden keep their rooms and their place in the home index, but the top
 * bar only carries the shelves that are alive). */
export const NAV: { href: string; label: string }[] = [
  { href: "/books", label: "Books" },
  { href: "/videos", label: "Videos" },
  { href: "/writing", label: "Writing" },
  { href: "/balloons", label: "Balloons" },
  { href: "/about", label: "About" },
  { href: "/search", label: "Search" },
];

/* Home index — every room of the library, with honest counts. Order since
 * 2026-11-09: the living shelves first, the quiet rooms after. */
export const HOME_INDEX: SectionEntry[] = [
  {
    href: "/videos",
    label: "Videos",
    /* meta is computed live on the home page from published episodes */
    meta: "3 series",
    blurb: "Friends Intelligence in Chinese, Working Theory in English, and one film at the piano — published here first.",
  },
  {
    href: "/today",
    label: "One thing today",
    /* meta is computed live on the home page from the deck */
    meta: "one card a day",
    blurb: "今天只做一件事 — every Friends Intelligence episode leaves one small action, printed as a card.",
  },
  {
    href: "/books",
    label: "Books",
    meta: "2 published · 1 planned",
    blurb: "Friends Intelligence, Fish Fun, and the book the essays may one day become.",
  },
  {
    href: "/balloons",
    label: "Balloons",
    meta: "16 works · archived",
    blurb: "Little Wow Balloons — real balloon art, twisted by hand, kept for good.",
  },
  {
    href: "/writing",
    label: "Writing",
    meta: "Working Theory · 52 essays · Jan–Jul 2026",
    blurb: "The numbered essay series on AI, engineering, systems and leadership — complete, and kept in full.",
  },
  {
    href: "/projects",
    label: "Projects",
    meta: "8 kept",
    blurb: "Software worth keeping, with the thinking behind it.",
  },
  {
    href: "/garden",
    label: "Digital Garden",
    meta: "4 ideas · resting",
    blurb: "Numbered ideas, tended over years, never finished.",
  },
  {
    href: "/talks",
    label: "Talks",
    meta: "collecting",
    blurb: "Public thinking — conferences, meetups, podcasts, recordings.",
  },
  {
    href: "/about",
    label: "About",
    meta: "who & why",
    blurb: "Who I am, why I build, and what I am trying to achieve.",
  },
];
