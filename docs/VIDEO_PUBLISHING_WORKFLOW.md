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

- `poster.jpg` — the designed 1080×1920 thumbnail (also used for social
  cards): a clean face frame + title in the caption style + HAOQIAN.CO line,
  made by `scripts/video-pipeline/thumbnail.py`. It is the SAME file that
  goes to LinkedIn as «Title - EpN - thumbnail.jpg». Do not use the
  raw frame `publish-video.sh` cuts — it's a fallback only (rule since
  2026-08-22, when Eps 1–3 were switched from frames to thumbnails).
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
   line. Make it with
   `python3 scripts/video-pipeline/thumbnail.py <frame.jpg> "LINE ONE" "LINE TWO." out.jpg`
   (cut the frame with `ffmpeg -ss <sec> -i <raw> -frames:v 1`, mouth
   **HDR sources need a tone-map for every STILL (Hao's rule, 2026-09-02
   — the washed-out thumbnail happened twice):** direct camera MOVs
   (IMG_*.MOV) are HLG/BT.2020 10-bit; a plain ffmpeg PNG grab reads as
   sRGB and comes out 惨白 (washed grey). Teleprompter-app MP4s are SDR
   and unaffected. For any poster/thumbnail from an HDR take:
   `ffmpeg -ss <t> -i <src> -frames:v 1 -vf "scale=...:in_color_matrix=bt2020"
   -pix_fmt rgb48be raw.png` then
   `scripts/video-pipeline/hlg2sdr.py raw.png sdr.png` (inverse HLG OETF,
   highlight rolloff, BT.2020→709, sRGB encode) and build the card on the
   SDR image. Check the JPEG against the playing video before shipping.
   **And the VIDEO itself must be converted, not just stills (2026-09-03,
   after a washed LinkedIn playback):** LinkedIn's transcoder ignores the
   HLG transfer tag — locally the file looks right (Apple players honor
   HLG), then plays out grey after upload. HDR sources go through
   `lut3d=hlg709.cube` at encode pass 1 with explicit bt709 output tags
   (recipe in scripts/video-pipeline/encode_v2.py). The x264 flags alone
   do NOT retag (frame props win) — finish with the two-step retag:
   `-c copy -bsf:v h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1:video_full_range_flag=0`
   then `-c copy -color_primaries bt709 -color_trc bt709 -colorspace bt709
   -movflags +write_colr` (VUI + container colr). Verify with ffprobe:
   the final must read bt709/bt709/bt709.
   Frame choice for the standalone thumbnail: head level, mouth closed,
   eyes open — it need not be frame 0 (only the BAKED cover must be).
   no burnt captions). **The opening recipe (final, after four rounds on
   Ep. 8 — every earlier variant produced a visible jump):**

   1. The video starts AT the first word — the lead trim runs to ~0.06 s
      before speech; pre-speech "settling" footage never survives (the
      speaker is still moving into position there).
   2. The card's background is FRAME 0 of the edited cut itself — never
      a tail or mid-take frame (different pose ⇒ body jump even at one
      frame).
   3. Compose freezes frame 0 for 0.30 s (`tpad=start_mode=clone`,
      audio `adelay`), and ONLY the text layer melts out over it
      (`fade=t=out:st=0.14:d=0.15:alpha=1`). Text dissolving over LIVE
      video ghosts (the speaker moves); over the frozen frame nothing
      can move. The reel reads: cover → type melts → the frame comes
      alive speaking. Caption/insert times shift by the freeze.

   Frame 0 sits at speech onset, so the cover's mouth may be slightly
   open — acceptable; the pose match is what matters. The same file is
   the site poster (`public/videos/<slug>/poster.jpg`); try "Edit
   thumbnail" anyway, it costs nothing.
3. `«Title» - EpN - caption.txt` — the LinkedIn caption (written at
   script stage, stored on the `linkedinCaption` field). Hook line
   first, canonical URL, two tags max. **Blunt and boilerplate-free
   (Hao, 2026-09-05): no "Ep. N of Working Theory, on camera
   (unscripted):" framing, no "Full episode + transcript:" prefix —
   hook, one or two plain sentences of substance, the bare link, tags.
   Meta-talk about the format is filler.**

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

## The second series (live since 2026-09-05)

`VIDEO_SERIES` now holds two lines — `working-theory` (English, LinkedIn)
and `friends-intelligence` (中文, 小红书). `/videos` renders one shelf per
series with published episodes (an empty series never shows), the home
index counts across both, and episode pages read language, platform and
origin from the series config. Adding a third line = one more entry in
`VIDEO_SERIES` + `VIDEO_SERIES_ORDER`; page code needs no change.

Publishing a Friends Intelligence episode (the cutting thread's steps
after Hao exports from CapCut):

1. Compress the export if it is HEVC (`ffmpeg … libx264 crf 22`, 1080×1920,
   `+faststart`); the crf22 `上传版.mp4` is already fine — just remux with
   `-movflags +faststart`. Upload: `gh release upload media <slug>.mp4
   --clobber`. Slugs carry the `fi-` prefix.
2. Poster = frame 1 of the export (the baked cover: brush title + corner
   mark): `ffmpeg -ss 0.05 -i <export> -frames:v 1 -q:v 4
   public/videos/<slug>/poster.jpg`.
3. Captions: read the `captions` text track from the final CapCut draft
   (`~/Movies/CapCut/User Data/Projects/com.lveditor.draft/<name>/
   draft_content.json`) → WebVTT at `public/videos/<slug>/captions.vtt`.
   The transcript on the entry is those captions with punctuation and
   paragraphs added — nothing reworded.
4. Entry in `src/content/videos.ts`: `series: "friends-intelligence"`,
   `language: "zh-Hans"`, Chinese `title` + English `titleEn`, `topic`
   (pillar), `platformCaption`/`platformTags` from the posting package;
   `platformPublishedUrl` once the note is live. Add the edge to
   `book:friends-intelligence` in connections.ts.
5. `npm run build`, commit, push. Then Hao posts the note on 小红书.
