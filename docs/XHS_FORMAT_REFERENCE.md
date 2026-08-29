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
| Grade | none visible — phone auto everything | same. No colour work |

## 3. Motion vocabulary (replaces cutting)

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

**Pipeline vocabulary (v4, per Hao "more, denser" 2026-08-23):** the
compositor (`scripts/xhs-pipeline/render.py`, fx.json per episode) does
baked opening title · gold/red/blue/pink punch pops (easeOutBack) ·
whole-line caption colours (`cap_colors`) · **inline keyword colouring
inside caption lines (`cap_marks`) — every line containing the keyword
colours it, the benchmark's signature** · Apple-emoji stickers ·
floating ?? doodles · small brush floaters (对吧? asides) ·
shrink-to-quote cards · zoom pushes + phrase-level horizontal drift ·
**screen shake on every 咚** · white-wall auto colour neutralize +
exposure. Density target per minute: ~3 punches, ~2 stickers, ~1
card/floater/doodle, keywords marked throughout.

## 5. Audio

- −9.7 to −15.5 LUFS across notes (inconsistent, raw) → we normalise
  to −14 LUFS, LRA ≤ 5.
- **Light BGM bed** under the whole video, far below the voice;
  sparkle/whoosh SFX accompany gold-word pops (felt, not loud).
  Ours: procedural warm-pad loop (`gen_bgm.py` → ~/Video Studio/work/
  bgm/warm_pad.wav, fx "bgm":"auto", −26 dB) and procedural SFX
  (`gen_sfx.py`: 咚 thud / ding / sparkle / whoosh / pop — auto-mapped
  to punch styles, overridable per item). Downloaded packs drop into
  the same dirs.
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
