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

Files live in `public/videos/<slug>/`:

- `final.mp4` — the finished cut. **Keep it small**: 9:16 1080p H.264,
  target well under ~100 MB (the repo and Amplify both carry it). For
  anything bigger, host it elsewhere (YouTube unlisted, a CDN) and put the
  full URL in `videoUrl` instead — the page renders file URLs as a native
  player and YouTube/Vimeo URLs as an embed.
- `poster.jpg` — the thumbnail (also used for social cards).
- `captions.vtt` — WebVTT captions (only used with file URLs).
- optional `figure-1.jpg` … — supporting diagrams/evidence, listed in
  `supportingVisuals` with real `alt` text.

Then set `videoUrl`, `poster`, `captions`, `durationSeconds`, `aspect`.

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

The LinkedIn package lives on the same episode entry — no second copy:

- **Video file** — the same `public/videos/<slug>/final.mp4` (upload
  natively; don't just link).
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
