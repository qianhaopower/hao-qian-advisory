/*
 * Projects — software worth keeping. Phase 1 carries the roster; the full
 * unified template (Problem / Context / Design / Implementation / Lessons /
 * Status / Future) arrives with the per-project pages.
 */
export type Project = {
  slug: string;
  name: string;
  years: string;
  oneLiner: string;
  href?: string; // live link, if public
};

export const PROJECTS: Project[] = [
  {
    slug: "friends-intelligence-app",
    name: "Friends Intelligence App",
    years: "2026 · ongoing",
    oneLiner:
      "The book as a product — assessment across seven pillars, focus-pillar reports, daily practices. Auth, payments, the lot.",
    href: "https://friendsintelligence.net",
  },
  {
    slug: "content-studio",
    name: "Content Studio · AI Business Mate",
    years: "2026 · ongoing",
    oneLiner:
      "Daily social content in a business's own voice, for accountants, brokers and advisers.",
    href: "https://aibizmate.co",
  },
  {
    slug: "fish-fun-production-line",
    name: "Fish Fun Production Line",
    years: "2026",
    oneLiner:
      "The pipeline that turned a six-year-old's drawings into a 400-page hardcover.",
  },
  {
    slug: "world-cup-fighter",
    name: "World Cup Fighter",
    years: "2026",
    oneLiner:
      "A silly cartoon fight simulator — procedural sound, shareable battle cards.",
    href: "/worldcupfighter",
  },
  {
    slug: "little-wow-balloons",
    name: "Little Wow Balloons",
    years: "2025 · ongoing",
    oneLiner:
      "My balloon studio — live twisting for parties and festivals, delivered bundles across Melbourne.",
    href: "https://littlewowballoons.com",
  },
  {
    slug: "charis-mortgage",
    name: "Charis Mortgage",
    years: "2026",
    oneLiner: "Client site for a Melbourne mortgage broker — EN · 中文 · 粤语.",
    href: "https://charismortgage.com.au",
  },
  {
    slug: "local-business-sites",
    name: "Local Business Sites",
    years: "2025–26",
    oneLiner:
      "A café, a pie shop, a jianbing house, a hair salon — small sites for real neighbours.",
    href: "/sites",
  },
  {
    slug: "haoqian-co",
    name: "HaoQian.co",
    years: "2026 · ongoing",
    oneLiner: "This library itself — strategy, design system, and the shelves.",
    href: "/",
  },
];
