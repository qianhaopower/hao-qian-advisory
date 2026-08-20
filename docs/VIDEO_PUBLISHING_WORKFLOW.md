# Video publishing workflow — website first, LinkedIn second

The website is the canonical home; LinkedIn is distribution. One episode =
one entry in [`src/content/videos.ts`](../src/content/videos.ts). No CMS.

Everything below should take minutes once the video file exists.

## 1 · Draft the episode

1. Duplicate an entry in `EPISODES` in `src/content/videos.ts` (the
   `example-episode` placeholder shows every field). Keep `status: "draft"`.
2. Fill in `slug`, `series`, `sequence`, `title`, `hook`, `summary`,
   `transcript` (the full spoken script, one string per paragraph — write it
   here first and read from it when filming; the repo is the home of the raw
   script too), and `keyPoints`.
3. A draft builds at `/videos/<slug>` (noindex, absent from all listings),
   so you can preview the page — and even deploy it — before the video exists.

## 2 · Add the media

**The rule (since 2026-08-20): video bytes never enter git.** Videos live
as assets on the repo's `media` GitHub release — the "media shelf"
(https://github.com/qianhaopower/hao-qian-advisory/releases/tag/media).
Release assets don't bloat the repo or Amplify builds, stream with range
support (seek bar works), and need no account, bucket or API key beyond
the `gh` login that already exists. Raw originals stay in Photos/Downloads
and are never committed either.

One command does compress + poster + upload:

```bash
scripts/publish-video.sh <raw-video> <slug> [poster-at-seconds]
# → uploads  https://github.com/qianhaopower/hao-qian-advisory/releases/download/media/<slug>.mp4
# → leaves   ~/Downloads/<slug>.mp4  and  ~/Downloads/<slug>-poster.jpg
```

(Compression standard, if doing it by hand: 1080p long-edge H.264 CRF 23,
AAC 128k, `+faststart`. Keep a cut under ~100 MB; release assets allow up
to 2 GB but the page should stay light. Manual upload also works — drag
the mp4 onto the `media` release on github.com, or
`gh release upload media <file> --clobber`.)

What still lives in the repo, in `public/videos/<slug>/`:

- `poster.jpg` — the thumbnail (also used for social cards); the script's
  `<slug>-poster.jpg`, copied here.
- `captions.vtt` — WebVTT captions (only used with file URLs).
- optional `figure-1.jpg` … — supporting diagrams/evidence, listed in
  `supportingVisuals` with real `alt` text.

Then set `videoUrl` (the **full release URL**), `poster`, `captions`,
`durationSeconds`, `aspect`. YouTube/Vimeo URLs still render as embeds if
ever needed. The same shelf serves non-episode videos too (e.g. the Fish
Fun flip-through on its book page via `Book.video` in `books.ts`).

## 3 · Preview and validate

```bash
npm run dev      # http://localhost:3000/videos/<slug>
npm run lint
npm run build    # must pass before publishing
```

Check the episode page on a phone-width viewport as well as desktop.

## 4 · Publish on haoqian.co

1. Set `status: "published"` and `publishedAt: "yyyy-mm-dd"`.
   This is the switch that adds the episode to `/videos`, the homepage
   index count, search, the sitemap, and turns on VideoObject structured
   data + canonical/OG metadata.
2. Commit and push to `main` — Amplify deploys automatically.
3. Confirm the canonical URL: `https://haoqian.co/videos/<slug>`.

## 5 · Publish on LinkedIn (manual)

**Delivery rule (since Ep. 3):** every final cut is delivered to
~/Downloads as a three-piece package, ready to post in one sitting:

1. `«Title» - EpN - final.mp4` — the video
2. `«Title» - EpN - thumbnail.jpg` — 1080×1920 designed thumbnail:
   a clean face frame from the episode with the episode title in the
   caption style (Arial Black, lower third) and a small HAOQIAN.CO mono
   line. Upload it via LinkedIn's "Edit thumbnail" on the video.
3. `«Title» - EpN - caption.txt` — the LinkedIn caption (written at
   script stage, stored on the `linkedinCaption` field). Hook line
   first, canonical URL, two tags max.

The LinkedIn package lives on the same episode entry — no second copy:

- **Video file** — the same compressed cut that went to the media shelf
  (`~/Downloads/<slug>.mp4` from the script; upload natively; don't just
  link).
- **Caption** — `linkedinCaption` (write it in the entry so it's kept).
  End with the canonical URL, or add it as the first comment.
- **Hook** — `hook` is the opening line.
- **Tags** — `linkedinTags`.

Checklist:

- [ ] Upload video natively, with the poster frame selected
- [ ] Paste caption, check the canonical haoqian.co link
- [ ] Add captions/subtitles on LinkedIn if it didn't auto-detect
- [ ] After posting, copy the post URL into `linkedinPublishedUrl`
      (adds the "Also published on LinkedIn →" footer on the episode page)

## 6 · Seven days later — record three numbers

Fill in the `signals` field on the episode:

```ts
signals: {
  recordedAt: "yyyy-mm-dd",
  reach: 0,        // impressions/views on LinkedIn
  responses: 0,    // comments + saves + shares
  inbound: "",     // relevant follows, useful DMs, invitations
},
```

These support exactly one weekly decision — what to continue, what to
stop, and the single variable to change next. Don't optimise around likes.

## Adding a second series later

Add an entry to `VIDEO_SERIES` (e.g. a Friends Intelligence line for
Xiaohongshu/Instagram) and give its episodes that `series` id. Page code
reads series config; nothing else changes. Not part of Phase 1.
