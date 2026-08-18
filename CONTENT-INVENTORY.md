# HaoQian.co — Content Inventory

The verified raw material for the digital library. Gathered 2026-07-29. Companion to [STRATEGY.md](STRATEGY.md).

## Books

### Friends Intelligence (published)
- **Title:** Friends Intelligence — *The Hidden Patterns Connecting Money, Relationships, Health, and Decisions*
- **Published:** 2026 · Paperback & Kindle · [Amazon AU B0H5R5C8B6](https://www.amazon.com.au/dp/B0H5R5C8B6)
- **The seven pillars (F.R.I.E.N.D.S.):** Financial · Relationship · Information · Emotional · Nutrition · Dynamic · Sleep
- **Editions to come:** Audiobook (占位 "to be") · 中文版 Chinese edition (占位 "to be")
- **Cover asset:** `public/friendsintelligence/cover.jpg` (900×1440)
- **Companion app:** https://friendsintelligence.net — full product: auth, payments, DB; 35-question assessment across the 7 pillars; personalised focus-pillar report; daily practices with drift detection; freemium + Plus (A$19 lifetime). Local repos: `~/Documents/fiapp`, `~/Documents/fiappv1`.
- **Draft blog (book's origin):** https://www.friendsintelligence.info — the original book draft, serialised as posts (2025–26). → Archive section + book page "related".
- **Manuscript:** `~/Documents/F.R.I.E.N.D.S Intelligence.pdf` / `.txt`; diagram tooling in `~/Documents/Friends Intelligence Diagram Engine`.
- **Landing page (existing):** `/friendsintelligence` static page in this repo.
- **LinkedIn launch post:** https://www.linkedin.com/posts/hao-qian-9ab0b04b_my-book-is-finally-published-it-feels-good-activity-7474331629511921664-FQIe (2026-06-21) · teaser: https://www.linkedin.com/posts/hao-qian-9ab0b04b_for-those-of-you-who-know-me-here-it-is-activity-7471459486247854080-H9G4

### Fish Fun (published)
- **Title:** Fish Fun · **Authors:** Isabelle Qian (Author), Hao Qian (Author) — cover credit: “by Isabelle Qian, with her dad”
- **Published:** July 24, 2026 · Hardcover, 400 pages · English · [Amazon B0HBVBBBBX](https://www.amazon.com/dp/B0HBVBBBBX) · ISBN-13 979-8188767174 · 8.49 × 1.13 × 11.24 in · ~US$59.89 (list $62.75)
- **About:** Goldie, Zoey, Lulu and Stella — four little fish, best friends; 100+ tiny adventures (fly to the moon, university, haunted hotel elevator, one slice of pizza) without leaving their tank. Every picture drawn by Isabelle (age 6). A keepsake made with love.
- **Production repo:** `~/Documents/Fish Fun` (01-originals → 02-stories → 03-illustrations → 04-print-pages → 05-book; KDP files, dashboard, tools). Front-cover source: `05-book/cover-final/fish-fun-cover-KDP-preview.png` (crop right panel for web cover).
- Also doubles as a **Project**: “the pipeline that turned a six-year-old’s drawings into a 400-page hardcover”.

### Working Theory (in progress)
- The book the LinkedIn essay series is becoming. See Writing below.

## Writing — Working Theory series (LinkedIn)

- **Author profile:** https://www.linkedin.com/in/hao-qian-9ab0b04b/
- **STATUS: COMPLETE.** 2026-07-29, parsed from Hao's saved Activity page: all 52 posts, **#1 (2026-01-31) → #52 (2026-07-25)**, with URLs, exact dates (decoded from activity IDs) and **full text**.
- **Full text archive:** `content-src/working-theory-text/` (52 files, `wt-NN-date-urn.txt`) — the Phase 5 migration source. Other original posts (42, incl. book launch) in `content-src/linkedin-posts/`.
- **Site data:** complete series in `src/content/writing.ts`.
- **Numbering (canonical, per Hao 2026-07-29):** #24 and #27 were skipped — recorded as gaps, no backfill. #48 and #49 were each used twice; the later post keeps a `b` suffix (`48b` “From Software Engineering to Knowledge Engineering”, `49b` “AI Is Fast. Reality Isn’t.”) permanently.
- Early posts (#1, #2) were titled “Working Theories (N/…)” with no essay title; #1 shows as its opening line.

The full 52-entry table lives in [src/content/writing.ts](src/content/writing.ts) — no, title, date, URL for every post.

## Videos — Working Theory on camera (added 2026-08-16)

- **Ep. 1 "Speaker Theory"** (from essay wt-2): filmed by Hao 2026-08-16, edited via the scripted ffmpeg/whisper pipeline. Assets in `public/videos/speaker-theory/` (final.mp4 108s 1080×1920, poster.jpg, captions.vtt); entry in `src/content/videos.ts`; canonical `/videos/speaker-theory`. B-roll: Mixkit free license (IDs 22961, 46680, 45923). Format spec: `docs/VIDEO_FORMAT_REFERENCE.md`. LinkedIn distribution pending (caption stored on the entry).

## Projects (confirmed roster)

| Project | Live | Notes |
|---|---|---|
| Friends Intelligence App | https://friendsintelligence.net | flagship; auth/payments/DB; assessment + practices |
| Content Studio · AI Business Mate | https://aibizmate.co (demo: /demo.html) | daily social content for AU accountants/brokers/advisers; $490–690/mo tiers. The address is the .co — aibizmate.com is unrelated to Hao (confirmed 2026-07-30) |
| World Cup Fighter | /worldcupfighter (this repo) | cartoon fight simulator; React/TS, framer-motion, procedural Web Audio, html2canvas share cards |
| Little Wow Balloons | http://littlewowballoons.com | Hao's balloon business — live twisting + delivery bundles ($180/hr, $240–550 bundles), Melbourne E/SE; repos `~/Documents/lwb`, `lwbv2` |
| ↳ Instagram archive | https://www.instagram.com/qianhaopower/ | @qianhaopower was the studio's shopfront (16 posts, bio "✨ Turning air into WOW moments…", logo saved to `public/projects/balloons/studio-logo.jpg`); account is pivoting to books/leadership. **Ingested 2026-08-17**: all 16 photos (from Hao's official IG export, all posted 2026-02-12 via FB cross-post, captions genuinely empty) live in `public/projects/balloons/` and render at `/balloons` — the balloon room, its own nav tab. Reviewed image-by-image: all clean product shots, safe to publish. Street photos added 2026-08-17 (from Hao's `Photos-1-001 (7).zip`): 6 curated as `street-1..6.jpg` — the stand + sign, Box Hill Twilight Markets (2026-02-14), evening orders, Southbank promenade (2026-03-07), Mario (03-12), Mario & Luigi (03-13). IMG_7004 (three generations at the stall, kids in strollers) included as `street-7.jpg` and leads the section — Hao confirmed the event ticket carries photo consent (2026-08-17); source zip also has 3 videos, unused |
| Charis Mortgage | https://charismortgage.com.au | client site — Charis Fok, Melbourne broker, multilingual EN/中文/粤语; repo `~/Documents/charismortgage.com.au` |
| Local business sites | /sites (this repo) | Calla & Cups, Rolf's Pies, Tianjin Pancake House, Premium Hairstyles |
| Fish Fun production line | `~/Documents/Fish Fun` | drawings → 400-page hardcover pipeline |
| HaoQian.co | this repo | the library itself |
| (candidate) Mowing service site | `~/Documents/mowing-service-marketing-site` | found locally — confirm with Hao whether it shipped |

## Author pages (added 2026-08)

- **Amazon Author Page:** https://www.amazon.com/author/haoqian (store: /stores/Hao-Qian/author/B0HCBGC9N2) — linked from /books and About.
- **Goodreads author:** https://www.goodreads.com/author/show/71572056.Hao_Qian — FI listed (3 editions, 222pp, 2026-06-15). Profile is complete: full bio (born Baoding, China; Melbourne; piano/cubes/balloons/night markets → the FI origin story) and the Website field already points to haoqian.co/books/friends-intelligence. Only gap: Fish Fun isn't on Goodreads (would sit under Isabelle Qian's name).
- **Goodreads book (FI):** https://www.goodreads.com/book/show/254117147-friends-intelligence — linked from the FI book page ("shelve, rate, review").

## GitHub (github.com/qianhaopower — 28 public repos, checked 2026-07-30)

Distribution channel + archive material. Site links live in the footer, About/Elsewhere, project pages and /archive.

| Repo | Maps to |
|---|---|
| `hao-qian-advisory` | this site (haoqian-co project links it) |
| `fiappV1` (+ older `FIAPP`) | Friends Intelligence App project |
| `lwbv2` (+ `littlewowballoonsmarketing`) | Little Wow Balloons project |
| `calla-and-cups-cafe` | Local business sites project |
| `smt-gardening-marketing-site` | the mowing/gardening site found locally — still unconfirmed as shipped |
| 2015–21 back-catalogue (QuickRoster, TradesMate*, RedPill, SchoolRankMap, 23-Design-Patterns…) | /archive "The early repositories" |

Private (not visible/linkable): Fish Fun, Book Publisher, aibizmate.co, charismortgage.com.au, worldcupfightor standalone.

## Digital Garden (seed ideas)

- **#138** — Books are software. Readers compile them.
- **#154** — Managers won't disappear. They'll manage AI.
- **#171** — Specifications become more valuable than implementations.

## Archive (initial holdings)

- Leadership Advisory practice (2026) → keep page at `/advisory`, unlinked, enquiry form stays live (Hao will take clients who find it)
- friendsintelligence.info — the book's draft blog (origin story)
- Old homepage (advisory sales page) — preserved in git history
- Fish Fun production materials · FI manuscript & diagram engine · `~/Documents/Second Draft`, `Book Publisher`, `Pumpking Book` (to catalogue with Hao)

## Design status

DONE — Hao authored the system himself in Claude Design (“Design System Foundations Review”, project `072c5a47-f4f5-45f8-b4d4-6a2b41d04565`) and it is implemented site-wide (see `CLAUDE.md` § Design system). Light-first; dark mode is specced for a later pass.
