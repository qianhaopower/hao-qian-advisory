export const SITE = {
  name: "Hao Qian",
  tagline: "Turning ideas into systems.",
  intro:
    "I build software, books, systems and ideas that help people think better. Everything worth keeping lives here — permanently.",
  principle:
    "Every meaningful thing I create should eventually have a permanent home here.",
  linkedin: "https://www.linkedin.com/in/hao-qian-9ab0b04b/",
};

export type SectionEntry = {
  href: string;
  label: string;
  meta: string;
  blurb: string;
};

/* Header navigation — order mirrors the shelf order of the library. */
export const NAV: { href: string; label: string }[] = [
  { href: "/books", label: "Books" },
  { href: "/writing", label: "Writing" },
  { href: "/projects", label: "Projects" },
  { href: "/talks", label: "Talks" },
  { href: "/garden", label: "Garden" },
  { href: "/about", label: "About" },
  { href: "/search", label: "Search" },
];

/* Home index — every room of the library, with honest counts. */
export const HOME_INDEX: SectionEntry[] = [
  {
    href: "/books",
    label: "Books",
    meta: "2 published · 1 underway",
    blurb: "Friends Intelligence, Fish Fun, and the book the essays are becoming.",
  },
  {
    href: "/writing",
    label: "Writing",
    meta: "Working Theory · 52 essays",
    blurb: "An essay series on AI, engineering, systems and leadership.",
  },
  {
    href: "/projects",
    label: "Projects",
    meta: "8 kept",
    blurb: "Software worth keeping, with the thinking behind it.",
  },
  {
    href: "/talks",
    label: "Talks",
    meta: "collecting",
    blurb: "Public thinking — conferences, meetups, podcasts, recordings.",
  },
  {
    href: "/garden",
    label: "Digital Garden",
    meta: "3 ideas growing",
    blurb: "Numbered ideas, tended over years, never finished.",
  },
  {
    href: "/about",
    label: "About",
    meta: "who & why",
    blurb: "Who I am, why I build, and what I am trying to achieve.",
  },
];
