# XHS format — 樊登 personal account, reverse-engineered

**Benchmark: 樊登's personal Xiaohongshu account** (user id
`5dbc304a000000000100a1be`), chosen by Hao 2026-08-23. Four real notes
downloaded via share links and analysed frame-by-frame + by audio
(whisper zh transcription, EBU R128, spectrograms, 1–4 fps contact
sheets, pixel measurement):

| Note | Topic (tags) | Length | 字/min | Ending |
|---|---|---|---|---|
| 人生的容错率，远比你以为的要高 | 认知/内耗/自我成长 | 96 s | ~301 | **repeats its own key passage as outro loop** |
| 孩子最大的安全感 来自家庭的托底。 | 育儿/家庭教育 | 69 s | ~270 | stops dead on last phrase |
| 记住你是自由的，别拿任何主义框住自己。 | 爱情观/婚姻/单身 | 68 s | ~287 | stops dead ("不至于") |
| 你超厉害，你的背后是数十代人的生生不息。 | 历史/科普/姓氏 | 156 s | ~303 | "关注我，了解有趣的知识" (rare follow-CTA) |

**Important context:** the official 帆书/樊登讀書 brand accounts use a
completely different black-canvas packaging template (analysed
2026-08-23 from YouTube mirrors, superseded — kept in git history).
The personal account we clone is rawer and better suited to a solo
operator. The Mel Robbins study (`FI_FORMAT_REFERENCE.md`) remains the
spec for the later IG/English line.

---

## 1. The big idea

**One continuous selfie take + kinetic typography.** Zero cuts in all
four videos (60–156 s each). The camera never moves; the *frame*
moves: digital zoom pushes, shrink-to-quote-card moments, and a
constant layer of animated coloured words carry all the visual energy.
The set is his real study. Nothing is staged except the words on
screen. Production = talk once, decorate in post.

## 2. Container & set

| Property | Benchmark | Our target |
|---|---|---|
| Delivered | 720×1280, 30 fps, ~1.7 Mbit/s | shoot 4K, deliver 1080×1920, 30 fps |
| Take | **one continuous selfie take, 0 cuts** | same — fluffs are retaken from the top or absorbed by a zoom |
| Set | wall-to-wall home bookshelf, warm daylight, real and slightly messy | Hao's real bookshelf/study corner. Real books only |
| Camera | phone at ~arm's length, lens slightly **below** eye level looking up a touch; face LARGE (head + shoulders fill the frame, top of head sometimes cropped); he leans in and out naturally | same; tripod at chest height 40–60 cm away, or literally handheld-on-desk |
| Wardrobe | plain grey/dark tee with a small chest print | plain tee, no logo (or his own mark later) |
| Grade | **warm + saturated + mid-bright** — measured across 4 notes: R/B warmth 1.21–1.50, mean saturation 0.28–0.33, mean luma 0.44–0.50. Phone-native warmth, never neutral grey | pipeline `"grade":"fandeng"`: wall pulled to warm white (R/B≈1.15), saturation ×1.6, contrast ×1.07, wall luma ~0.84. Neutral-grey correction is banned — it reads 阴间 (Hao, 2026-08-23) |

## 3. Motion vocabulary — CORRECTED 2026-08-23 night: the frame is STATIC

Measured: frame-to-frame size delta 0.00–0.03 px/0.5 s across all four
notes — **no zoom pulses, no drift, no shake**. Everything that moves is
his body. Our earlier per-phrase zoom/drift/shake was invented and read
as jitter (Hao: 抖来抖去). Pipeline now: static baseline; a slow 1.06–
1.10× push (~1.1 s) only at fx-marked peaks; shake opt-in per punch.

### Superseded (kept for history)

1. **Zoom pushes** — scale steps of ~1.05–1.2× landing on phrase
   starts, both directions, a few per 10 s. Smooth, not snapped.
2. **Shrink-to-card** — for a quotable formula the video shrinks into
   a black canvas with the line as big text beside/above it
   ("能托底的托底，不能托底的不能托底"), 1.5–3 s, then back to full.
3. **Freeze-ish emphasis** — big word cards land ON the video at the
   word's moment (giant red 无效 / 都不对 / 都出错 filling the upper
   frame).
4. No transitions, no b-roll, no jump cuts, no speed ramps.

## 4. Typography system (the format's soul)

Layers, all synced to speech:

| Layer | Style | Role |
|---|---|---|
| Base caption | one line, white, soft shadow, rounded-bold sans, ~44–52 px (on 720 wide), centred at **y ≈ 77 %**, 5–12 字 per line, swaps per phrase (~1–2 s) | verbatim subtitles, always on |
| Gold punch words | larger 斜体/书法感 gold-yellow with glow ("给孩子托底", 威胁/恐吓, 经常庆功, 你就很好, 亮点), often with a sparkle/ding moment | the concept nouns — the episode's keywords |
| Red warning words | bold red ("真的找不着工作", 无效, 都不对, 恐惧), sometimes huge | negatives, dangers, the thing to stop doing |
| Accent colours | blue 3D (天际线), pink (谦虚/爱) — one-off flavour | rare, one per video max |
| Doodles | floating white/yellow "??" around his head during acted confusion | the humour beat, 1–2 per video |

Rules: base caption never moves from y 77 %; punch layers appear ON
their spoken word and hold 1–3 s; at most one punch layer on screen at
a time; everything has a soft shadow; no boxes behind text (except the
shrink-to-card moments).

**Measured density (manual count off 4fps contact sheets, 2026-08-23):**
托底 ≈ 16 effect events/min (one every 3–4 s: coloured caption lines,
quote lines, cards, floats, giant words); 容错率 ≈ 8–9/min. Target:
**10–16 events/min — one visible new element every 4–6 seconds.**

**Anti-突兀 grammar (why his feel produced, ours felt pasted):**
1. Effects are STYLED WORDS, almost never emoji/clipart — emoji only as
   a small accent, never standalone.
2. The workhorse layer is the **topline**: a styled second line just
   above the base caption (gold quotes 「…」, red verdicts) — not
   elements floating in empty wall space.
3. Every element EXITS (fade + slight rise, ~0.3 s) — nothing hard-cuts
   off screen.
4. Elements sit near the head/gesture zone, inside the composition.

**Pipeline vocabulary (v4–v6):** the
compositor (`scripts/xhs-pipeline/render.py`, fx.json per episode) does
baked opening title · gold/red/blue/pink punch pops (easeOutBack) ·
whole-line caption colours (`cap_colors`) · **inline keyword colouring
inside caption lines (`cap_marks`) — every line containing the keyword
colours it, the benchmark's signature** · Apple-emoji stickers ·
floating ?? doodles · small brush floaters (对吧? asides) · **toplines (styled second caption line, the density workhorse)** · universal fade+rise exits ·
shrink-to-quote cards · zoom pushes + phrase-level horizontal drift ·
**screen shake on every 咚** · white-wall auto colour neutralize +
exposure. Density target per minute: ~3 punches, ~2 stickers, ~1
card/floater/doodle, keywords marked throughout.

## 5. Audio

- −9.7 to −15.5 LUFS across notes (inconsistent, raw) → we normalise
  to −14 LUFS, LRA ≤ 5.
- **Grade decision 2026-08-23 night: default is `natural`** (phone WB kept, sat ×1.35, con ×1.04, exp ×1.05) — Hao's wall stays paper-white per his own light-locked brand; copying the benchmark's warm cast onto a white wall reads jaundiced. 6-variant matrix in ~/Downloads/xhs-overnight/grade-matrix.jpg awaits his pick.
- **Light BGM bed** under the whole video, far below the voice;
  sparkle/whoosh SFX accompany gold-word pops (felt, not loud).
  Ours: **real music only** — synthesized pads are banned (Hao: 阴间).
  Library: ~/Video Studio/work/bgm/ — 21 Kevin MacLeod tracks
  (incompetech, CC-BY 4.0: post text must carry one line
  "音乐: Kevin MacLeod (incompetech.com)"). fx "bgm":"auto" uses
  default.mp3 (currently Wholesome); per-episode pick by path. BGM
  branch is loudness-normalised to −36 LUFS (fx "bgm_lufs"), ≈22 dB
  under the voice. Procedural SFX from `gen_sfx.py` (咚/ding/sparkle/
  whoosh/pop) stay — they read as UI sounds, not music.
- Phone-distance voice, small room, no treatment. Lav mic will beat
  the benchmark — fine.

## 6. Delivery & language

- **270–305 字/分钟, zero pauses ≥ 0.35 s.** One breath rolls into the
  next thought. The energy is a friend mid-rant, not a lecturer.
- **He acts both sides of dialogues**, switching voice: the anxious
  parent ("我不给他饭吃"), the inner monologue ("不生气不生气、没有
  没有没有"), then himself answering. 1–2 acted beats per video.
- Rhetorical checks straight to camera: 对吗？ 够了。 就很好。
- Concrete named examples (梅西 and his 毛病 list: 个子低/不会演电影/
  不会做算术/中文都不会/论语也没读过/坐飞机碳排放高 — absurdist
  escalation is the humour engine).
- Colloquial fillers kept: 咱就拿…来说, 烂七八糟, 你就赶紧做饭去吧.
- **Structure:** ① dramatic claim or acted quote in the first 2 s
  (你儿子将来真的找不着工作，我不给他饭吃 / 你不是普通人，你是皇帝
  的后代) ② mechanism in plain talk ③ one vivid example with the
  absurd list ④ turn it on the viewer's real life (孩子/家长/自己)
  ⑤ ending: usually just stops on the strongest line; occasionally
  **repeats the core passage verbatim as an outro loop**; 关注我 CTA
  exists but is rare — we use it never or almost never.

## 7. Cover (封面) — a designed still, same template every time

Same selfie frame as the video + **two big centred text lines in the
lower half (y ≈ 55–85 %)**: white bold + the key phrase in **gold
brush-calligraphy style**, e.g. 人生容错率 / **高到无法想象**;
别拿"**主义**"绑架自己. Cover text is punchier than the note title —
it's written separately. One corner mark possible (有趣的知识). Face
looks straight into the lens.

## 8. Post text

Title = one striking sentence (the claim, with a full stop). The
description body is **nothing but 3–7 topic tags** (#育儿 #认知 …).
No prose, no links, no 中文版在路上 pitch — for our line the honest
positioning line goes in the *comment section* as our own pinned
comment instead, once per episode.

## 9. What Hao does (per episode)

1. Script from his rambles: 250–450 字 (≈ 60–100 s at his pace), one
   claim, one acted beat, one absurd list, mark punch words in the
   text: `{金:关键词}` `{红:警示}` `{??}`.
2. Sit in the study corner, phone below eye level at arm's length,
   plain tee, PromptSmart big-font narrow window; read FAST (native
   pace + 10 %), roll through mistakes, act the dialogue beats.
   One good take of the whole thing (retake whole, it's ≤ 100 s).
3. Cutting room: zoom pushes on phrase starts, base captions from
   whisper (verified against script), punch layers from the markup,
   shrink-card if the script has a quotable formula, faint BGM + SFX,
   −14 LUFS, export 1080×1920 + designed cover (template §7, gold
   calligraphy font: a free-commercial 书法体, e.g. 霞鹜文楷 bold or
   演示系列; decide once, keep forever).
4. Publish: striking one-line title + tags only. Batch-record 3,
   publish ~1/day.

## 10. Integrity rules

- We clone geometry, motion, typography logic, pacing, structure —
  never his wording, his 帆书 marks, his tee print, or his examples.
- Content = Friends Intelligence manuscript + Hao's own words only.
- No fabricated dialogues presented as real events: acted beats are
  obviously theatrical, same as the benchmark.
- Honest positioning (英文版已出版，中文版在路上) lives in a pinned
  comment, not shouted every video.


## 11. Effect atlas

The complete quantified inventory of his overlay language lives in
`docs/xhs-effect-atlas.json` (layers, colours, sizes, positions, motion
and audio rules, TODOs: comment-card, white-flash opening, multi-line
accumulated captions, avatar end watermark, illustration sourcing).
Every pipeline template must trace to an atlas entry — nothing invented.


## Framing rule (2026-08-30)
Headroom ≤ 8%: white space above the head thin, eyes near upper-quarter line. Benchmark head nearly touches frame top. Check before every take; pipeline can rescue old takes via fx reframe_scale/reframe_y.
## Insert rules (2026-08-30, Hao)
- Text-bearing inserts keep the bottom ~28% of the canvas EMPTY (caption safe zone); labels inside the image must never collide with each other.
- While an insert is on screen: base captions stay, but NO toplines/punches/floaters (generator suppresses with a warning).
- Insert grammar (measured): hard cuts in/out, ~3s each, ~1 per 22s; motion = slow push baked into the clip.
- Sources: CapCut built-in library (Hao drags into planned slots) or AI-generated images in ~/Movies/FI-videos/assets/inserts/.

- Base captions ALWAYS carry a black outline (width ~18 in CapCut units) — white-on-white over bright inserts was invisible (2026-08-30).

- Inserts fade in/out ~0.3s via alpha keyframes (hard cuts sting the eye on white-wall footage). Opening = brush white+gold two-liner over the chest (FD style); persistent brush corner mark top-left; end card = book-anchored (endcard fx key), bgm covers it and fades out.


---

# PRODUCTION LAW — locked 2026-08-30 after v1–v17 (every rule was paid for)

**The pipeline**: record → `transcribe.py` (zh) → PROOFREAD captions.json
(whisper tail-hallucination check on long takes; known typo classes: 咒→昼,
偏正→偏振; anchors must be grepped from THIS episode's captions) → fx.json →
`to_capcut.py` → open CapCut → eyeball → export. Backends kept: to_jianying.py
(future JY 5.9/Windows full-auto), render.py (Python fallback).

## Recording (check before EVERY take)
- Headroom ≤8%, eyes near upper-quarter line. Rescue: fx reframe_scale/_y.
- Lav clipped inside collar, transmitter at the SIDE, not centre-chest.
- Lamps bounce off ceiling, never direct; ceiling light on; 1.2–1.5m off the wall.
- Room LF hum + reverb (the 嗡嗡): SOLVED — the WT sound-engineering
  chain landed as `scripts/video-pipeline/audio_master.py`. FI inherits
  it (see Audio chain step 0). The hum is the downstairs fridge; it
  cycles — listen for it before a take, or let the chain kill it.

## Audio chain (order is law)
0. **VOICE MASTER FIRST**: `scripts/video-pipeline/audio_master.py <raw> raw.mp4`
   (bootstraps its own .venv-audio). One command = dereverb (room-fitted
   Lebart, 0.24s -> ~0.18s) + adeclick + HP80 (fridge) + EQ match to the
   Galloway LTAS + de-esser + pause-hiss expander + 1.7:1 comp + loudnorm
   -14. It REPLACES steps 1-2 below for the voice (they live inside it);
   steps 1-2 are kept for legacy/rescue use only. Measured on XHS raws
   IMG_2623/24/32 (2026-09-03): same room, same mic — applies as-is.
   NEVER add afftdn on top (eats >1.6kHz speech detail — WT measured).
   BGM/sfx mixing stays AFTER the master, on the mixed bus, as below.
   EQ curve is fitted to the collar mic position; if the clip position
   changes, ask the WT thread to refit (takes vary: IMG_2623 vs 2624
   showed a 14dB HF swing from mic placement alone — pin the position).
1. declick GENTLE by default: ffmpeg adeclick=w=20:o=75:t=1 ONLY (right
   character, no waveform patching). The patch-repair pass is RESERVED for
   very clicky takes (>2.5 impulses/s) and even then median+20dB max —
   patches on voiced speech cause robotic warble (Ep3, 2026-09-02), and
   the +14dB pass chewed sibilants (2026-08-30). Always export a diff×8
   track when patching; it must contain zero intelligible speech.
2. loudnorm VOICE to −14 (inside source_ready.mp4). Never normalise a mix.
3. BGM ratio: benchmark voice-to-bed = 17–23dB → generator AUTO-GAINS the
   bed to 21 dB under the measured voice (ebur128 on both; fixed 0.20 was
   only right for Bossa — Wallpaper is 10.5 dB hotter, Ep6 v1 shipped ~10 dB
   under). sfx 0.15. BGM track: non-repetitive (autocorr <0.4), longer
   than the video, from ~/Movies/FI-videos/assets/ (CapCut can't read
   ~/Video Studio). Bed extends under the endcard, 2.5s fade-out.

## Picture
- Grade "natural" only: keep phone WB, sat×1.35, con×1.04, exp×1.05.
  Warm-cast or neutral-grey grading = banned (阴间, twice).
- Motion: static baseline. Zoom only at fx-marked peaks (slow, ~1.1s).
  Cards snap 0.2s/0.25s. ALL scale keyframes gathered+sorted+deduped
  (out-of-order anchors caused a 115s slow-shrink).

## Text system (CapCut fonts/sizes locked)
- Captions: 中黑体 bold 8.5 (auto-shrink >13字, floor 5.2), white,
  BLACK BORDER width 18 (white-on-white was invisible), y −0.54.
- Toplines: 俪金黑 10.5 gold/red/white, y −0.33, 弹入+向上溶解.
- Punch: 俪金黑 16, gold rot −4 / red straight, thick borders, 晃动 loop on gold.
- Opening title: 庞门体 16(white)/18(gold), border 70, chest height,
  **NO intro animation — full title on frame 1** (thumbnail rule), outro 溶解.
- Corner mark: 默陌手写 6.5 white, border 45, top-left, full duration.
- Floaters 9.5 brush. Emoji retired. Nothing invented outside the FD atlas.

## Inserts (真视频 b-roll)
- Real footage first: FI shelf ~/Movies/FI-videos/assets/broll/ (Mixkit
  free-commercial, luma-filtered; harvester fetch_life_broll.py) + WT shelf.
  Diagrams (paper-style) only for numbers/mechanisms.
- Faces: Asian preferred, white OK (XHS audience) — enforced at pick time.
- Grammar: ~3s each, ~1 per 22s, 0.3s alpha fade in/out, bottom 28% of
  text-bearing images left empty, toplines/punches auto-suppressed during
  inserts, inserts ≥ hold+0.5s apart (overlap guard drops with a warning).
- Landscape sources: centre-crop 405:720 → 1080×1920 bake into assets/inserts/.

## Head & tail
- Frame 1 = face + full title (the feed thumbnail).
- End card = the BOOK: cover + 今天讲的是·〈pillar〉智慧 + Sleep Intelligence
  等 + 《Friends Intelligence》七种智慧之一 + 英文版已出版·中文版在路上;
  3.5s, fade-in, bgm rides under it. No 关注我 in the video.

## Process law (for the agent)
- After every scripted patch: grep the file for the new symbols BEFORE
  claiming it landed (a silent .replace() no-op shipped an unfixed v8).
- After every draft generation: read the draft JSON and count segments
  per track before telling Hao it's there.
- All media CapCut touches lives under ~/Movies/FI-videos/.
- Old draft versions: tell Hao which to delete; one live version at a time.

- FRAME-1 FACE RULE — STRENGTHENED 2026-09-03 after three published covers shipped squints/glares (frame 0 = the worst instant: post-record-tap blink/tension).
  ① RECORDING: after pressing record, DO NOT SPEAK — look at the lens, relax the brows, give a slight about-to-share smile, HOLD 2 SECONDS, then start. That posed beat exists solely for the cover (every big account poses covers).
  ② PIPELINE: fx "face_frame" is MANDATORY every episode. Selection criteria: eyes fully open, brows relaxed, mouth closed or softly open (never mid-word), head level or slightly tilted, overall friendly-about-to-share — never 瞪/凶. Agent pulls candidates (prefer the posed 2s; else sentence-gap frames where the mouth just closed), shows the pick to Hao for a nod, then freezes it over the first 0.35s.
  ③ The exported cover jpg / XHS cover must be this same frame.

- EXPORT RULE (2026-09-02): CapCut export = 1080p / 30fps / bitrate "recommended" — never 4K, never high-bitrate (XHS re-encodes anyway). Target ≤250MB for ~4min; >300MB means wrong settings. Oversized exports: ffmpeg -crf 22 recompress before phone transfer.

- INSERT MOOD RULE (Hao 2026-09-05): every insert must match the emotional tone of the beat AND the episode (a warm couple episode gets smiling/embracing/talking couples — never crying, clinical, workplace, or odd clips). Mood is checked by eye on a contact sheet at pick time, per clip. Keep the shelf growing (hundreds) so clips are not reused across episodes.
- POSED PRE-ROLL RULE: the 2s cover-face pause is trimmed out of source_ready (keep ~0.8s), face_frame still overlays frame 1; music alone over a silent opening reads as too loud.

## Episode checklist v2 (locked 2026-09-05 — the Ep6 level is the baseline)
1. PROBE LANGUAGE of every new file before touching it (an EN WT take sat next to the zh one).
2. Cover-face candidates from the posed opening → pick eyes-open/smiling → face1.png → fx face_frame.
3. Measure speech onset (per-second RMS); trim source_ready to onset−0.8s; then TRANSCRIBE THE TRIMMED SOURCE.
4. Proofread: known typo classes (腺肝→腺苷, 偏正→偏振, 咒→昼, 退黑素→褪黑素, 脑白筋→脑白金, 泪干见影→立竿见影, 高中屋里→高中物理, English fragments joined) + tail-hallucination strings (未经许可不得翻唱或使用 / 优优独播剧场 / 感谢观看 / 字幕由… / 订阅…) + duplicate-start chunks.
5. fx: density target 1 insert per ~22s, 3-4 punches, 8-12 toplines; anchors copied from THIS captions.json; run the anchor-miss check before generating; re-run it after ANY retranscribe.
6. Inserts: harvest a fresh category batch per episode (shelf keeps growing, no reuse), mood-check on a contact sheet, Asian faces preferred, bake vertical.
7. Per-pillar end card (endcard_sleep / endcard_relationship / … — build the pillar's card the first time it appears).
8. Generate → read draft JSON → count segments per track → only then report.
9. Export (Hao) → agent compresses to 上传版 (~80MB) → phone → title/body/tags/pinned comment from the episode package.

- COMPRESS RULE (Hao 2026-09-05): every CapCut export is compressed by the agent WITHOUT being asked — the moment a new FI-*.mov lands in Downloads, produce <题>-上传版.mp4 (crf22, ~80MB) and hand that name over; the raw export is never what goes to the phone.
