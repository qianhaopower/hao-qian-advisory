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

## Friends Intelligence — where the book exists online (verified 2026-09-05)

Sources: Hao's own publishing emails (KDP, Goodreads, BookSirens, StoryOrigin, CraveBooks) plus direct fetches. Store search pages (Kobo, Google Play, Booktopia, B&N, Apple Books, Google Books, Open Library, WorldCat, AbeBooks) were probed by ISBN/title on 2026-09-05: no listing anywhere but Amazon — the book is KDP-only (no Expanded Distribution / aggregator).

| Trace | URL / id | Status |
|---|---|---|
| Amazon Kindle + paperback (same detail page) | https://www.amazon.com/dp/B0H5R5C8B6 (also .com.au) | live; Kindle in KDP Select since 2026-07-31 |
| Amazon hardcover | https://www.amazon.com/dp/B0HCBBY8B3 | live 2026-07-31 |
| Amazon author page | https://www.amazon.com/author/haoqian (→ stores/Hao-Qian/author/B0HCBGC9N2) | live 2026-08-03 |
| Goodreads book | https://www.goodreads.com/book/show/254117147-friends-intelligence | live |
| Goodreads author (Author Program) | https://www.goodreads.com/author/show/71572056.Hao_Qian | approved 2026-08-01 |
| Draft blog / companion app / GitHub | friendsintelligence.info · friendsintelligence.net · github.com/qianhaopower/FIAPP (+ fiappV1) | live |
| 小红书 account 「不内耗的人生」 | https://www.xiaohongshu.com/user/profile/60af86df0000000001007b70 (rednote.com mirrors it) | live; the FI episodes |
| BookSirens | submitted 2026-08-03, no public page yet | in review |
| StoryOrigin | account 2026-08-20 (review-copy tool, private) | — |
| CraveBooks via Armadillo eBooks | promo booked 2026-09-05 for 2026-09-09 | listing page appears on the day |
| Readings Carlton consignment · Boroondara Library title suggestion | emailed 2026-08-01 | no reply recorded |

Everything with a URL is on `/books/friends-intelligence` (Editions + "Around the book"); submissions without pages are in its History timeline. New registrations join the same way.

## Videos — Working Theory on camera (added 2026-08-16)

Video bytes live on the media shelf (GitHub release `media`, per `scripts/publish-video.sh`); the repo keeps only poster.jpg + captions.vtt per episode.

- **Ep. 1 "Speaker Theory"** (from essay wt-2): filmed by Hao 2026-08-16, edited via the scripted ffmpeg/whisper pipeline. 108s 1080×1920 on the media shelf; poster + VTT in `public/videos/speaker-theory/`; entry in `src/content/videos.ts`; canonical `/videos/speaker-theory`. B-roll: Mixkit free license (IDs 22961, 46680, 45923). Format spec: `docs/VIDEO_FORMAT_REFERENCE.md`. Posted to LinkedIn 2026-08-17.
- **Ep. 2 "AI Throughput Shift"** (from essay wt-1): filmed by Hao 2026-08-18, same pipeline. 87s on the media shelf; poster + VTT in `public/videos/ai-throughput-shift/`; canonical `/videos/ai-throughput-shift`. B-roll: Mixkit free license (ID 914). LinkedIn three-piece package (final + designed thumbnail + caption.txt, per workflow §5) delivered to ~/Downloads 2026-08-18.
- **Ep. 3 "Retrain the Model"** (from essay wt-35): filmed by Hao 2026-08-20, same pipeline. 106s on the media shelf; poster + VTT in `public/videos/retrain-the-model/`; canonical `/videos/retrain-the-model`. B-roll: Mixkit free license (ID 4809). Three-piece package delivered to ~/Downloads 2026-08-20.
- **Eps. 4–7** (all 2026-08-22 on the site, media shelf, poster = designed thumbnail, VTT in repo): Ep. 4 "IQ-to-EQ Career Weighting" (video-first, no essay; approved chart; shelf 242/46680/9069), Ep. 5 "The Goldilocks Load" (video-first; reframed 1.25× from 4K; shelf 42899/23285/42655/5537), Ep. 6 "Attention Is Not Cheap" (from wt-38; narrow-passage diagram; shelf 45922/34096/4817), Ep. 7 "HTML Is The New English" (from wt-46; shelf 1746/42650/17446/42649). LinkedIn status table: `docs/VIDEO_SIGNALS_LOG.md`.
- **Ep. 8 "Good Work Doesn't Speak"** (video-first, no essay; first mic-era episode; the opening recipe was finalized here): filmed 2026-08-29, 97s on the media shelf; poster + VTT in `public/videos/good-work-doesnt-speak/`; canonical `/videos/good-work-doesnt-speak`. B-roll: Mixkit 17315/914/8872/46679.
- **Ep. 11 "Self-Assessment"** (first UNSCRIPTED episode, no teleprompter; video-first): filmed 2026-08-31, 135s on the media shelf; poster + VTT in `public/videos/self-assessment/`; canonical `/videos/self-assessment`. B-roll: Mixkit 25426/8925/46685.

## Videos — Friends Intelligence on camera, 中文 · 小红书 (added to the site 2026-09-05)

The second video line (opened 2026-08-30): Hao speaks in Chinese, voice-first, on the book's seven intelligences; edited through `scripts/xhs-pipeline/` → CapCut (draft generator `to_capcut.py`, Hao exports), format law in `docs/XHS_FORMAT_REFERENCE.md`. Series id `friends-intelligence` in `src/content/videos.ts`; each episode connects to `book:friends-intelligence` in connections.ts. Posting packages (titles / 正文 / tags / pinned comment) in `content-src/video-scripts/fi-xhs-ep*.md`. Same shelf rule: mp4 on the `media` release, poster + VTT in `public/videos/<slug>/`. Posters = the designed frame-1 cover baked into each export (brush title + corner mark), so the site poster is that frame, not a raw grab. Chinese captions were extracted from the CapCut caption track of the final draft (proofread there), and the transcripts are those captions with punctuation and paragraphs added. Music in every episode: Kevin MacLeod (incompetech.com), CC-BY — credited in the pinned 小红书 comment.

| Ep | Slug | Title | Pillar | Finished | Length | Source export |
|---|---|---|---|---|---|---|
| 1 | `fi-sleep-daylight` | 晚上睡不着，先改早上这一件事 | 睡眠 Sleep | 2026-08-30 | 244s | CapCut `FI-sleep-v17` |
| 2 | `fi-coffee` | 下午一杯咖啡，晚上凭什么睡不着 | 睡眠 Sleep | 2026-08-31 | 165s | CapCut `FI-咖啡-v1` |
| 3 | `fi-dim-lights` | 晚上总睡不好，睡前一小时先关大灯 | 睡眠 Sleep | 2026-09-02 | 228s | CapCut `FI-睡前调光-v1` |
| 4 | `fi-temperature` | 晚上翻来覆去睡不着，先把卧室调低两度 | 睡眠 Sleep | 2026-09-03 | 207s | CapCut `FI-温度睡眠-v2` |
| 6 | `fi-couple-20min` | 夫妻之间这件事，每天都应该做 | 关系 Relationship | 2026-09-05 | 193s | CapCut `FI-夫妻20分钟-v2` |

Ep. 5 (打印机 vs 买车, 财富 Financial) exists only as a recording skeleton — not filmed. Site pages for Eps 1–4 were backfilled on 2026-09-05; `publishedAt` carries each episode's finish date. **The 小红书 profile URL is not recorded anywhere in the repo** — `SITE.xiaohongshu` in `src/content/site.ts` is empty and the 小红书 links (footer, About, /videos, episode footers) render only once it is filled. Per-note URLs go on each entry's `platformPublishedUrl`.

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
