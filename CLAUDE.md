# HaoQian.co — the library

Hao Qian's personal digital library ("a library, not a website"): books, Working Theory essays, projects, talks, a digital garden. Next.js 16 (App Router) + Tailwind 4, deployed to AWS Amplify on push to `main` (haoqian.co).

## Read these first

- `STRATEGY.md` — the north star: vision, principles, IA, success criteria. Decisions defer to it.
- `CONTENT-INVENTORY.md` — every verified asset (books, app, projects, all recovered Working Theory LinkedIn URLs, what's still missing). Update it when assets are added or confirmed.

## Design system — do not improvise

Source of truth is Hao's own Claude Design project ("Design System Foundations Review", claude.ai/design project `072c5a47-f4f5-45f8-b4d4-6a2b41d04565`, file `Design System.dc.html`). Implemented as tokens in `src/app/globals.css` and fonts in `src/app/layout.tsx`.

- Voices: **Newsreader** (serif — titles + long-form), **Instrument Sans** (UI only), **IBM Plex Mono** (metadata/dates/code, uppercase, 0.14em tracking — use the `.meta` class).
- Palette: paper `#FBFAF7`, surface `#F4F2ED`, line/hairline, ink `#1F1D1A`/`#57534A`/`#8A857A`. Blue accent = links/interactive only; green = connections between works only. Accents never fill surfaces; no gradients; no shadows.
- Layout: 1140px container / 48px margins (24px < 900px), reading columns 640px max, 8px spacing scale, radius 2px.
- Motion: one curve, one speed — 250ms ease; hover = border darkens / surface tints / text takes accent; page fades up 8px (`.fade-up`); everything collapses under `prefers-reduced-motion`.
- **Light-locked.** Hao explicitly rejects dark/murky rendering; dark mode is specced in his design but ships only as a deliberate later pass.

## Architecture

- `src/content/*.ts` — all content as typed data (site nav, `writing.ts` Working Theory links, `garden.ts` ideas, `projects.ts` roster). Adding content = editing these files; no CMS, ever.
- `src/components/site/Chrome.tsx` — SiteShell/Header/Footer + primitives (Container, Kicker, PageTitle, Lede, Note).
- `src/app/{books,writing,projects,talks,garden,about,archive}` — the library rooms.
- `/advisory` — the 2026 advisory practice, archived (noindex, enquiry form still wired to `/api/enquiry` via Resend). Linked only from `/archive`.
- Legacy kept intact: `/sites` + business sites under `public/`, `/worldcupfighter`, `/friendsintelligence` static landing (redirect in `next.config.ts`).
- `content-src/working-theory-cache/` (gitignored) — raw LinkedIn guest-page HTML for the recovered posts; use for full-text migration.

## Roadmap state (2026-07)

Phase 1 shipped (foundation, Home, About, section pages, advisory archived). Phase 2 shipped: all 52 Working Theory essays live on-site at `/writing/wt-<no>` — built from `content-src/working-theory-text/` by `src/lib/essays.ts` (build-time fs loader: strips title header lines, harvests trailing `hashtag#X` into topics, detects series, computes reading time). Adding a new essay = drop the .txt (URL/DATE header) + one entry in `src/content/writing.ts`; figures go in `public/writing/images/` named `<slug>-<n>.jpg` and listed in `src/content/essay-images.json` (42 of 52 essays have their original LinkedIn figures; the rest had none in the export). Phase 3 shipped: full book pages at `/books/[slug]` driven by `src/content/books.ts` (copy sourced from Hao's production repos — `~/Documents/Book Publisher` for Friends Intelligence, `~/Documents/Fish Fun` for Fish Fun, figures from `~/Documents/Friends Intelligence Diagram Engine`), plus RSS at `/feed.xml` (Working Theory) and `sitemap.ts`. Phase 4 shipped: `/projects/[slug]` write-ups (unified template) in `src/content/projects.ts`, facts sourced from each project's own local repo (`~/Documents/fiappv1`, `aibizmate.co`, `lwbv2`, `charismortgage.com.au`, `Fish Fun`) — drafted for Hao's review. Fish Fun pages tell the true arc: real tank → Isabelle's hand drawings (AI = colour/production only, never generative authorship) → 400-page hardcover, with the tank photo + pencil originals beside finished pages. Phase 5 shipped: the connections system — edges declared once in `src/content/connections.ts` (GENUINE relationships only: book↔app, book↔production line, idea↔essays), rendered bidirectionally by `src/components/site/Connections.tsx` as the green Connected panel (right rail on book/project pages, end card on essays, "Grew into" chips + `#idea-<no>` anchors in the garden). Adding an edge = one line in EDGES. Phase 7 (partial) shipped: OG share cards — `src/lib/og.tsx` renders the design system at 1200×630 (fonts committed in `src/assets/og/`); route `opengraph-image.tsx` files cover root/sections/[slug]s; detail pages explicitly point og:image at their own artwork (essay figure / book cover) or their generated card. Site search at `/search` — index built server-side from all content (full essay text included), scored client-side in `SearchClient.tsx`, linked in the header nav. Remaining: talks as they happen, garden growth (new ideas from Hao), dark pass.

## Conventions

- Counts and claims on pages must stay honest — empty sections say so plainly ("Empty · deliberately"), never fake fullness.
- Pre-existing lint errors live in `public/premiumhairstyle/*.jsx` and the enquiry code; don't chase them in unrelated work.
- `npm run dev` / `npm run build` / `npm run lint`. Amplify builds from `amplify.yml`.
