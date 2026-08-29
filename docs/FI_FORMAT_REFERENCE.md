# Friends Intelligence video format — reverse-engineered from Mel Robbins

**Benchmark chosen by Hao, 2026-08-23: Mel Robbins (@melrobbins).** Two
reels analysed frame-by-frame (4 fps contact sheets, full-res pixel
measurements) and by audio (whisper word timestamps, silence detection,
EBU R128 loudness, spectrograms):

| | Reel A | Reel B |
|---|---|---|
| URL | instagram.com/reel/DcMXL6cgfAm | instagram.com/reel/Db_ev0CEb-f |
| Title card | "Your 50s Are a Decade of Reinvention" | "Your 40s Aren't a Finish Line" |
| Posted | 2026-08-18 | 2026-08-13 |
| Length | 65.9 s | 32.7 s |
| Likes / comments (at 2026-08-23) | 42,087 / 1,789 | 66,863 / 1,619 |
| Words / speech rate | 227 words, **208 wpm** | 95 words, **180 wpm** |
| Face vs b-roll | 58 % face / 42 % b-roll | 40 % face / **60 % b-roll** |

We copy the **format** pixel for pixel — set, framing, cuts, captions,
timing, cadence of the voice — never her words, her brand, or her
personality. Content is Hao's, from the book. This file is the rule
book for the FI line (Xiaohongshu first, Instagram later) and is
deliberately separate from the Working Theory bible
(`VIDEO_FORMAT_REFERENCE.md`): the two lines never mix.

---

## 0. The analysis plan (the dimensions we measured)

Every future benchmark or self-review goes through the same list:

| # | Dimension | What we measured | Section |
|---|---|---|---|
| 1 | Container | resolution, fps, bitrate, duration, audio codec | §1 |
| 2 | Set & production context | where it's shot, what's in frame, props | §2 |
| 3 | Camera & framing | number of angles, lens feel, eye line, headroom, face size, where the mic sits | §3 |
| 4 | Lighting & grade | key direction, fill, background brightness, colour temperature, depth of field | §4 |
| 5 | Wardrobe & body | clothes, glasses, jewellery, posture, hands, gestures per sentence | §5 |
| 6 | Gaze & face | where the eyes go, expression range | §5 |
| 7 | Edit timeline | every cut and dissolve to 0.25 s, angle switches, b-roll share | §6 |
| 8 | B-roll grammar | what triggers an insert, clip length, stock style, transitions in/out | §7 |
| 9 | Captions | font, case, size, position, chunk length, timing, punctuation | §8 |
| 10 | Title card | position, shape, font, pin duration, fade | §9 |
| 11 | Brand marks | logo position, size, persistence | §9 |
| 12 | Audio | loudness, dynamic range, music yes/no, room, processing | §10 |
| 13 | Voice & delivery | wpm, pauses, pitch behaviour, energy, filler words | §11 |
| 14 | Editorial structure | beat-by-beat script architecture, hook, CTA, ending | §12 |
| 15 | Language | sentence shapes, pronouns, concreteness, repetition | §12 |
| 16 | Post caption | structure of the text under the video, CTA mechanics | §13 |
| 17 | Cover / 封面 | what the first frame and the feed thumbnail do | §14 |
| 18 | What transfers to Chinese / XHS | adaptation rules | §15 |

---

## 1. Container

| Property | Benchmark (both reels) | Our target |
|---|---|---|
| Aspect / resolution | 9:16, 1080×1920 delivered | 9:16, shoot 4K (for the punch-in), deliver 1080×1920 |
| Frame rate | 29.97 fps | 30 fps (not 24 — this line is video, not film) |
| Video bitrate | 1.5–2.2 Mbit/s VP9 (IG re-encode) | upload H.264 ≥ 8 Mbit/s, let the platform crush it |
| Audio | AAC 48 kHz stereo | same |
| Duration | **33 s and 66 s** | 30–70 s. Shorter reel got more likes (66.9 k vs 42 k). Default to 35–45 s; go to 60+ only when a concrete story needs it |

---

## 2. The set — it's a podcast studio, not a white wall

This is the biggest difference from the Galloway/WT format. Nothing is
"shot for the reel": both clips are **cut from a podcast recording**.
The set itself is the brand:

- **Branded podcast mic in frame, always.** Large dynamic mic on a
  boom arm, capsule sitting just under her chin, a white cube flag on
  it with the show name in black + yellow. It occupies 40–65 % of frame
  height, slightly left of centre. Viewers read "this is a show, she
  has authority" before she says a word.
- **Background:** warm wood slat wall, a framed landscape painting on
  the left, a gold YouTube plaque visible in the wide shot, a cream
  armchair behind her. All **bright, warm and blurred** (shallow depth
  of field). Nothing is dark. (Matches Hao's light-locked taste.)
- **Desk in the wide shot:** papers, a pen, a notebook — the "I've
  prepared" signal.
- Nothing else: no plants, no ring-light reflections, no screen.

**Our equivalent:** one fixed corner at home that becomes "the studio":
a real podcast mic on a boom arm (Shure MV7 / SM7B class — the mic is
the costume), a small flag on it later if we want a mark, a warm wall
with one framed object, bright daylight-balanced soft light, a chair
with a back that shows. Build it once, never move it.

---

## 3. Camera & framing — two angles, fixed

Two locked cameras. Nobody ever pans, zooms or pushes.

| | Cam A — CLOSE (default, ~85 % of face time) | Cam B — WIDE (punctuation) |
|---|---|---|
| Shot | tight medium close-up, head + shoulders | medium shot, head to desk |
| Top of head | ~10 % from top | ~12 % |
| **Eye line** | **~28 % from top** | ~27 % |
| Chin | ~40 % | ~36 % |
| Face height | ~30 % of frame | ~24 % |
| Horizontal | face centred (B) or centre-left (A), mic capsule at x ≈ 35–45 % | face centre-right, boom arm enters from bottom-left |
| What's visible | mic, necklace, shoulders; hands enter from below when she gestures | mic + boom arm, both hands, desk, notes, pen |
| Lens feel | ~50 mm equivalent, shallow DoF, background soft | same lens, camera further back |
| Camera height | **eye level**, dead-on | eye level, ~15° off-axis to her right |

**When the wide shot is used:** as punctuation at a pivot sentence, for
2–6 s, then back to close. Reel A: 3.5–9.25 s (the "everybody I know is
doing something cool" set-up) and 43.25–49.0 s ("he only does three of
them a year… death doula"). Reel B: 5.75–7.5 s ("It's where you can…").
Pattern: **open on close → wide on the second sentence → close for the
body → one wide in the back half.** Never two wides in a row.

**Our equivalent:** phone A on a tripod at eye level for the close;
phone B (or a 4K crop of A) for the wide. Hao shoots 4K on one camera
and the cutting room makes the wide from the full frame and the close
from a ~1.35× crop — same eye-line rule applies to both.

---

## 4. Lighting & grade

- **Key:** large soft source, camera-left, ~30° off axis, slightly above
  eye level. Shadow side of the face is only ~1 stop darker — very
  gentle modelling.
- **Fill:** strong, from camera-right (bright room). No dark side.
- **Background:** lit to about the same brightness as the face —
  bright, warm, no vignette.
- **Grade:** warm (golden) white balance, medium contrast, skin slightly
  lifted, blacks not crushed. Black top reads as deep black without
  losing the necklace.
- **Glasses:** thick black frames, and **no reflections** — the key is
  high enough and soft enough that lenses stay clean. This is a
  checklist item for Hao (who also wears glasses).

---

## 5. Wardrobe, body, gaze

- **Wardrobe:** plain black crew-neck long-sleeve top, every time. One
  long thin gold necklace. Black thick-rimmed glasses. One accent
  (green beaded bracelet). Hair down. High contrast against the warm
  bright background. **One uniform for the whole series.**
- **Posture:** seated, upright, leaning slightly toward the mic. Never
  slouched, never rocking.
- **Hands:** in frame constantly. Reel A: index finger raised on "In
  fact, my husband", hand on glasses on "I'm so proud", counting on
  "three of them", open palm on "how cool is that". Reel B: OK-sign
  pinch held through "Your 40s are the launch pad" (3 s), finger
  pointing down at the desk on "It's where". **Roughly one gesture per
  sentence, held for the sentence**, not fidgeting.
- **Gaze:** straight into the lens for 90 % of the close shot; in the
  wide shot she glances down at the notes and back up. Blinks are
  normal, no staring.
- **Face:** expressive — eyebrows up on "how cool is that", a smile at
  "I'm so proud", a squint-smile on "you're supposed to do your own
  thing". The face does the emphasis that captions don't.

---

## 6. Edit timeline — every cut, to 0.25 s

### Reel B (32.7 s) — the tighter, better-performing one

| Time | Shot | Caption chunk on screen | Transition |
|---|---|---|---|
| 0.00–5.75 | Cam A close, **title card pinned** | Your 40s / aren't a / finish line. / Your 40s are / the launch pad / for the / next decade / of your life. | cold open, no fade-in |
| 5.75–7.50 | Cam B wide, title card still pinned until ~7.0 then fades (~0.3 s) | It's where / you can | hard cut |
| 7.50–10.50 | B-roll 1: woman with coffee walking down stone steps | truly launch / forward in / your career. | **0.75 s dissolve in** from the wide |
| 10.50–12.25 | B-roll 2: meeting, hands on documents | You can do / something new. | hard cut |
| 12.25–15.75 | B-roll 3: woman in headphones, profile, thinking | You can build on / what you've / learned, / the mistakes / that you've made. | hard cut |
| 15.75–16.25 | → Cam A close | That's why | **0.75 s dissolve out** |
| 16.25–21.50 | Cam A close | the 40s / are incredible. / Maybe things / haven't / worked out / because / you're supposed / to do / your own thing. | — |
| 21.50–24.50 | B-roll 4: POV on a motorbike through trees | Maybe your 40s is / where you | hard cut |
| 24.50–26.75 | B-roll 5: photographer from behind | take that interest / that you had, / or that side | hard cut |
| 26.75–28.00 | B-roll 6: laptop, yellow sweater | hustle, / or that thing | hard cut |
| 28.00–30.00 | B-roll 7: piping jam into cupcakes | you've always / imagined doing, | hard cut |
| 30.00–32.70 | B-roll 8: handshake | you actually / launch your / own thing. | hard cut, **video ends on b-roll** — no return to face, no end card |

Face 13.0 s (40 %) · b-roll 19.7 s (60 %) · 8 b-roll clips, mean 2.5 s ·
2 angle switches · 2 dissolves, 8 hard cuts.

### Reel A (65.9 s)

| Time | Shot | Caption chunks | Transition |
|---|---|---|---|
| 0.00–3.50 | Cam A close, title pinned | Your / 50s / are the decade / of reinvention. | cold open |
| 3.50–9.25 | Cam B wide, title pinned to ~8.75 then fades | Everybody / that I know / that's in their 50s / is doing | hard cut |
| 9.25–17.25 | B-roll 1: aerial drone, two red kayaks on green water (8 s!) | something cool / right now. / And if you are / listening / and you have | hard cut in |
| 17.25–23.25 | B-roll 2: woman watering a garden | parents in / their 50s, / please / send this to them. / Please remind / your parents | 0.75 s dissolve |
| 23.25–27.75 | B-roll 3: group of older women taking a selfie with balloons | that they are / super cool / and there are / so many cool / things that they / could be doing, | 0.75 s dissolve |
| 27.75–30.75 | B-roll 4: older woman in yoga class | because everybody / that I know / in their 50s / right now | 0.75 s dissolve |
| 30.75–36.75 | B-roll 5: woman on sofa, hand to temple, thinking | is thinking / about this / like they're either / thinking about it / from the / standpoint of, | 0.75 s dissolve |
| 36.75–43.25 | Cam A close | "What do I want / to do next?" / Or they're / thinking about it / from the / standpoint of, / "All right, / I've taken / care of the kids / and everybody else, / what do / I want to do? / What's / the contribution / I want to make?" / In fact, / my husband, / I'm so / proud of him. / Christopher Robbins, / for the last / five years, / when he was / in his 50s, / he started / a men's retreat | 0.75 s dissolve back to face |
| 43.25–49.00 | Cam B wide | called Soul Degree. / He only does / three of them / a year. / He has also gotten / a certificate / to be a / death doula. | hard cut |
| 49.00–65.90 | Cam A close to the end | He also / is working / on his first book. / I'm so excited / about this book. / I can't tell you / about it. / I'm going to / have to let him / tell you about it / when he's / finished writing, / but he writes / every day / for an hour. / How cool is that? / And the man / is also getting / a master's / in Spiritual / Psychology / right now. | hard cut; **ends mid-thought on her face** (podcast cut) |

Face 38.2 s (58 %) · b-roll 27.7 s (42 %) in **one contiguous block**
(9.25–36.75) of 5 clips, mean 5.5 s · 4 angle switches · 5 dissolves.

### Edit rules extracted

1. **Cold open on the face with the title card already up.** Frame 1
   is her face + title. No logo sting, no fade-in.
2. **Second sentence = wide shot.** The first angle switch lands on the
   second sentence in both reels (3.5 s / 5.75 s).
3. **B-roll arrives at the first "picture noun"** ("doing something
   cool", "launch forward in your career") and stays in b-roll for a
   run — not one insert, a **sequence** of 3–8 clips.
4. **Clip length scales with speech energy:** calm, descriptive
   passages get 5–8 s clips with dissolves (Reel A); a list of
   alternatives ("that interest… side hustle… that thing…") gets
   1.25–3 s clips with hard cuts, one clip per item (Reel B).
5. **Dissolve = entering/leaving a mood; hard cut = next item.**
   Dissolves are always ~0.75 s (22–23 frames).
6. **Come back to the face for the personal part.** In A the husband
   story (the most concrete, most personal material) is 29 s of
   uninterrupted face. Personal = face, general = b-roll.
7. **No end card, no outro, no "follow me".** It just stops. A ends on
   her face mid-list; B ends on b-roll on the last word.
8. **No jump cuts within an angle** — the podcast take is continuous;
   angle switches do the job jump cuts do in the WT format.
9. No zooms, no speed ramps, no text animations, no emoji, no
   sound effects.

---

## 7. B-roll grammar

- **Source:** stock footage (Artgrid/Pexels class), **bright, warm,
  daylight, slightly desaturated**, shallow DoF, people aged 35–65,
  diverse, no faces looking at camera. Every clip has slow motion
  inside it (walking, paddling, watering, piping) — never static.
- **Mapping is literal and gentle:** "career" → woman with briefcase on
  steps; "something new" → meeting; "learned" → woman thinking in
  headphones; "parents" → gardening; "super cool" → older women selfie;
  "interest" → photographer; "side hustle" → laptop; "always imagined
  doing" → baking; "launch your own thing" → handshake. The clip shows
  the *category* of the noun, never the exact thing.
- **Colour continuity:** all clips share the warm grade of the studio,
  so dissolves feel like one world.
- **Captions sit exactly where they sit over the face** — never
  restyled, never moved, logo stays.
- **Share:** 42–60 % of runtime. This is the opposite of WT (10 %).

**Our rule:** library of 30–50 bright warm clips per pillar, graded to
our studio. For personal material (Hao's own story, his kids, his
tank, his balloons) use **his own photos/footage** as the b-roll — that
is the honest version of this grammar and it's what she does with the
husband story: she *doesn't* cut away, because it's hers.

---

## 8. Captions — one chunk at a time, small, centred, sentence case

Measured on 1080×1920 frames:

| Property | Value |
|---|---|
| Style | **One chunk replaces the next.** No karaoke, no accumulation, no word highlighting, no size changes |
| Chunk length | 1–4 words, **mean 2.3 words**; Reel B = 42 chunks in 32.7 s → **0.78 s per chunk**; Reel A ≈ 95 chunks → 0.7 s |
| Chunk boundaries | phrase units, not fixed word counts: "Your 40s / aren't a / finish line." "the mistakes / that you've made." Punctuation and quotes kept ("What do I want / to do next?") |
| Case | **Sentence case**, exactly as written prose. Not ALL CAPS |
| Font | heavy geometric grotesk, round dots, single-storey 'a' (closest free match: **Outfit Bold** or **Poppins SemiBold**; commercial: Sofia Pro Bold). Same family as the title card |
| Size | cap height ≈ 46 px, line box ≈ 60–66 px incl. descenders → **~62 px font on 1080 wide (3.3 % of height)**. Small by reel standards — legible, not shouting |
| Colour | pure white, **soft dark drop shadow** (~6 px blur, ~40 % opacity, offset 0/2). No stroke, no box |
| Position (no title) | horizontally centred (50.0 %); text box **y = 66.5–71.4 %** of frame height; baseline ≈ 70 % |
| Position (title pinned) | pushed down to **y = 72–78 %** so the title sits above it |
| Width | never exceeds ~60 % of frame width (max measured 396–708 px); long phrases wrap to two centred lines ("Christopher / Robbins,", "and everybody / else,") |
| Over b-roll | identical style and position |

Timing: chunk appears on the first phoneme of its first word (whisper
offsets match the frame changes to ±1 frame) and is swapped on the
first phoneme of the next chunk — **no gaps, no flicker**, a chunk is on
screen 100 % of the time speech is happening. Captions end with the last
word; nothing is shown in silence.

---

## 9. Title card and logo

**Title card** (the hook, pinned at the top of the video):

| Property | Value |
|---|---|
| Content | the first sentence, as a claim, 4–7 words, Title Case: "Your 40s Aren't a Finish Line" / "Your 50s Are a Decade of Reinvention" |
| Shape | **white rounded "speech-bubble" label**, one rounded rectangle per line, stacked and merged (the TikTok text-background look), corner radius ≈ 24 px, padding ≈ 20 px, line gap 0 |
| Font | same heavy grotesk, **black**, ~58 px, two lines |
| Position | centred; box spans **y = 57.7–71.3 %** (A) / 58.1–71.3 % (B); width 717–835 px (66–77 % of frame). It sits over her chest/the mic, **below the face, never over it** |
| Duration | pinned from frame 1 for **~7.0 s (B) / ~8.75 s (A)** — i.e. through the first two sentences and across the first angle switch — then **fades out over ~0.3 s** just before the first b-roll |
| Motion | none: no pop-in, no slide |

**Logo:** handwritten "Mel" script + letter-spaced thin "ROBBINS",
white, **top-right**, box x = 739–990, y = 129–222 px (right margin
90 px, top margin 129 px, 250×93 px, ≈ 8.5 % opacity loss over bright
b-roll but never hidden). On screen for 100 % of the runtime including
over b-roll. That is the only brand mark — no lower-third, no handle,
no end card.

**Our marks:** a small white wordmark top-right at the same box
(HAOQIAN.CO in Plex Mono for the site version; the XHS version may
carry the account name instead — decide when the account exists).

---

## 10. Audio

| Property | Measured | Our target |
|---|---|---|
| Integrated loudness | **−14.2 LUFS** both reels | −14 LUFS (IG/XHS normalise to about that) |
| Loudness range | **3.0 LU** — heavily compressed broadcast chain | compress hard: podcast-style chain (HPF 80 Hz → de-esser → compressor 4:1 → limiter) |
| Music | **Reel A: none.** Reel B: spectrogram shows faint sustained tones at ~1.1 k / 1.5 k / 6 k Hz under the whole clip — a **very quiet music bed (~−35 dB under voice)**, felt not heard | none for talking-head-heavy cuts; optional barely-there warm pad under b-roll-heavy cuts, −30 dB or lower. Never a beat. |
| Noise floor in pauses | −37 to −43 dB RMS | ≤ −45 dB: treated room or close mic |
| Mic | large dynamic mic, 5–10 cm from mouth: proximity bass, intimate, zero room | real podcast mic on a boom (also the prop), not the phone mic |
| Silence detection | **zero** silences at −35 dB — there is always room tone | keep room tone, never hard-gate to digital silence |

---

## 11. Voice & delivery

- **Speed:** 180 wpm when stating (B), 208 wpm when enthusing (A).
  Faster than Galloway's 180 flat; she speeds up when she's excited
  and it reads as sincerity, not rush.
- **Pauses:** B has **no pause ≥ 0.35 s in 33 s** — one breath, one
  thought. A has six pauses of 0.4–0.7 s, all after a full stop
  ("reinvention." / "them." / "else." / "year." / "doula." / "that?").
  Pauses mark sentence ends, nothing else.
- **Pitch behaviour:** downward terminals on claims ("finish line."
  "of your life."), rising on the rhetorical questions ("What do I
  want to do?" "How cool is that?"). Emphasis by *stretch* not volume:
  "in-CRED-ible", "super cool".
- **Register:** talking to one person across a table. Contractions
  everywhere. "Like" as a spoken connective ("Like they're either…").
  Repeats small words for rhythm ("cool" ×5 in A; "Your 40s" ×3,
  "maybe" ×2, "launch" ×3 in B).
- **Energy curve:** starts calm and sure (the claim), rises through
  the middle (the list, the husband), peaks on the question ("How cool
  is that?"), never comes back down — the clip ends at the peak.
- **Zero hedging.** No "I think", "maybe you", "for some people"; the
  only "maybe" is the reframe device ("Maybe things haven't worked
  out because…"), which is a claim wearing a maybe.

---

## 12. Editorial structure (the beats)

### Reel B, 33 s — "the claim clip" (5 beats)

1. **0–5.5 s Inversion claim** — "Your 40s aren't a finish line. Your
   40s are the launch pad for the next decade of your life." (also the
   title card)
2. **5.5–12.5 Permission list** — "You can truly launch forward in your
   career. You can do something new. You can build on what you've
   learned, the mistakes that you've made."
3. **12.5–18 Why** — "That's why the 40s are incredible."
4. **18–24.5 Reframe of the listener's failure** — "Maybe things
   haven't worked out because you're supposed to do your own thing."
5. **24.5–32.7 The picture of doing it** — a list of concrete
   alternatives ending on the verb: "…and you actually launch your own
   thing."

### Reel A, 66 s — "the story clip" (6 beats)

1. **0–3.5 Claim** — "Your 50s are the decade of reinvention."
2. **3.5–9 Social proof** — "Everybody that I know in their 50s is
   doing something cool right now."
3. **9–13 Share CTA, early** — "If you have parents in their 50s,
   please send this to them." (a share instruction at 0:09 — the
   distribution mechanic is *inside* the script)
4. **13–34 The inner question** — what 50-somethings are asking
   themselves, quoted in first person: "What do I want to do next?…
   What's the contribution I want to make?"
5. **34–62 One concrete person, four concrete facts** — her husband:
   men's retreat (3 a year), death-doula certificate, first book (writes
   1 h every day), master's in spiritual psychology. Names, numbers,
   specifics.
6. **62–66 Cut at the peak** — "How cool is that? And the man is also
   getting a master's… right now." End.

### Structural rules

- **Hook = a claim about *you* in the first 2 s**, stated as fact,
  often an inversion ("aren't a finish line"). Second person, present
  tense. It is also the title card and the first line of the post.
- **The whole clip is one idea.** No "three reasons", no framework, no
  numbering.
- **Concrete person > concept.** The best-performing minute of either
  reel is a named human with four verifiable facts. For Hao: his own
  life, his wife, his daughter, his friends — with permission, real.
- **A list of alternatives is delivered as b-roll rapid-fire**, one
  clip per item.
- **CTA lives in the script, early, and is a *share* instruction
  aimed at a third party** ("send this to your parents"), not "follow
  me".
- **No conclusion sentence.** Neither reel summarises. They end on the
  most energetic concrete line.
- Reel titles are **decade-specific** ("Your 40s", "Your 50s") — the
  audience self-selects by age in the first word. For FI: pillar- or
  situation-specific ("你四十岁以后的朋友", "睡不好的那一年").

---

## 13. The post caption (text under the video)

Both follow the same template:

1. **Line 1 = the hook, restated** ("You're not running out of time." /
   "Your 50s might be the most exciting decade of your life.")
2. **Blank line. 2–5 short lines expanding the idea**, one sentence
   each, often a list of questions ("What do I want? What do I want to
   learn?…").
3. **A personal line with a number** ("I'm turning 58 this year…").
4. **Social proof / the concrete person again** (husband, tagged).
5. **The CTA**, one of two mechanics:
   - *Share*: "Send this to anyone you know in their 50s – they need
     to hear it!"
   - *Comment-keyword → DM*: "Comment 'Timeline' and I'll DM you the
     link to the full episode." (drives comments, which drives reach;
     1,619 comments on a 33 s clip)
6. No hashtags in either. Tags only for people and the podcast.

For XHS: same template in Chinese; XHS rewards a **title line ≤ 20
字** plus body plus 3–6 topic tags (#话题) — the hashtag rule flips
there. Keep the share-CTA idea; the comment-keyword mechanic works on
XHS too ("评论区扣 1 发你链接" style), but we only use it once we have
something real to send.

---

## 14. Cover / first frame

Instagram shows frame 1 in the feed: **her face, close, title card
already pinned.** There is no separate designed cover — the pinned
title card *is* the cover, and it stays up for 7–9 s so the thumbnail
and the first seconds are the same image.

For Xiaohongshu the cover (封面) is a separate uploaded image and does
more work than on IG: it is what people see in the double-column feed.
Rule for this line: **cover = the same frame-1 composition (face + white
bubble title), exported at 1080×1440 (3:4) for the feed**, with the
title as the XHS hook line. No extra text, no arrows, no red circles.
This keeps the cover and frame 1 identical — the honest version of
what she does. Cover template to be built in the thumbnail pipeline
when the account opens.

---

## 15. What transfers to Chinese / XHS — adaptation rules

- **Everything visual transfers unchanged:** set, mic, two angles,
  eye line at 28 %, warm bright light, black top, 0.75 s dissolves,
  b-roll share, title-bubble, logo box, caption position and size.
- **Captions in Chinese:** chunk = **2–7 字**, one phrase unit, ~0.8 s
  each; font **思源黑体 Heavy / 阿里巴巴普惠体 Bold** (the geometric-
  grotesk equivalent), ~60 px, white, soft shadow, centred at y ≈ 70 %.
  Mixed English words (Hao's natural code-switching: "EQ", "dopamine",
  "side hustle") stay in Latin in the same font weight — do not
  translate his own mouth.
- **Speed:** 180–210 wpm ≈ **260–300 字/分钟** spoken Chinese. Hao's
  natural Chinese speed will be measured on the first recording and
  the target set from that; the rule is "no pause ≥ 0.35 s except after
  a full stop".
- **Title bubble in Chinese:** 6–12 字, two lines max, same white
  bubble, black 思源黑体 Heavy.
- **Script language** (the Chinese AI-flavour kill list, mirrors the WT
  rules): no 排比堆砌, no "不是…而是…" as the hook, no "值得注意的是",
  no 四平八稳 conclusions, no numbered lists aloud, no "今天我们来聊",
  no 鸡汤 abstractions ("成长", "热爱", "遇见更好的自己") without a
  concrete person/number attached. Second person (你), present tense,
  one idea, one named real person with real facts, share-CTA inside
  the script. Every claim traces to the manuscript or Hao's own words.
- **Honest positioning line** is in the post caption, not the video:
  "英文版已出版,中文版在路上" — once per post, plainly.

---

## 16. Production checklist per episode (FI line)

1. **Script:** one claim, 90–200 字, second person, ends on the most
   concrete line. Title bubble text = first sentence. Mark the b-roll
   nouns and the one personal story (face time, no b-roll).
2. **Record:** the fixed studio corner, podcast mic in frame, black
   top, eye level, eye line at 28 %, 4K 30 fps, one continuous take
   per script; teleprompter loop tail trimmed.
3. **Edit (cutting room):** close → wide on sentence 2 → close;
   b-roll run from the first picture noun; dissolves 0.75 s for
   mood, hard cuts for lists; one wide in the back half; **end on the
   last word**, no outro.
4. **Captions:** 2–7 字 chunks swapped on phoneme onset, 60 px,
   centred, y 70 % (78 % while title is up); title bubble pinned
   through sentence 2, 0.3 s fade.
5. **Audio:** −14 LUFS, LRA ≤ 4, no music (or ≤ −30 dB pad under
   b-roll only).
6. **Export:** 1080×1920 H.264 ≥ 8 Mbit/s + **3:4 cover** from frame 1.
7. **Post text:** hook line / 3–5 short lines / personal number /
   share-CTA / 英文版已出版,中文版在路上 / 3–6 tags.

---

## 17. Hao's home setup — the ≤ AU$150 version (agreed 2026-08-23)

No pro gear, **no mic in frame** (Hao's call: the mic must improve the
sound, not play credibility prop — the set stays honest). Seated at a
desk; WT is shot standing, so the two lines never share a posture.

**Buy once (after the current WT batch, ~2026-08-30):** a wireless
lavalier that plugs straight into the phone — Rode Wireless Micro
class (~AU$150, USB-C or Lightning version to match the phone).
Clipped at the centre of the collar one fist below the chin, invisible
on the black top. The camera app records its audio directly; no sync.
Lav sound is thinner/roomier than her dynamic mic → cutting room adds
a low shelf (+3 dB @ 150 Hz), de-ess, compress to LRA ≤ 4, −14 LUFS.
Room: windows shut, no A/C, not next to a hard wall.

**The corner (build once, never move):**
- Desk + chair **with a visible back**; notebook + pen on the desk —
  these replace the mic as the frame's anchor.
- **Window 30–45° to Hao's front-left**, never behind him; diffuse
  daylight. Background = warm wall with one framed object, ≥ 1.5 m
  behind him so it blurs. No window, door or dark area behind.

**Phone:** vertical on the small tripod on the desk, stacked on books
until the **lens is at eye height**; **0.9–1.0 m away on the 1× lens**
(close enough to read the teleprompter). Recorded *through
PromptSmart* (Hao reads; no-teleprompter delivery is a later skill):
max font, narrowest text window so the words sit directly under the
lens, 6–8 字 per line, scroll set to 260–300 字/min.

- If PromptSmart records **4K**: frame the WIDE (top of head ~12 %,
  eyes near the upper quarter, desk edge + hands visible); the cutting
  room crops the CLOSE (~1.35×). Two angles for free.
- If it only records **1080p**: frame the CLOSE (Mel's cam A: head top
  ~10 %, eyes at 28 %, shoulders in); angle switches become subtle
  1.15× punch-ins. Joins still hide; the desk-and-hands wide is lost.

**Wardrobe:** plain black crew-neck long sleeve, no logos, two
identical ones. Glasses on. Nothing else.

**Body:** sit upright, lean slightly forward; hands resting on the
desk at the bottom edge of frame; **one gesture per sentence, held
through the sentence** (index finger / OK pinch / point at desk / open
palm — her whole vocabulary); eyes on the prompter text (= the lens);
face does the emphasis (captions never do); no pause except ~0.5 s
after full stops; **first sentence is the title**, no greeting; after
the last word hold still for 2 s, then reach for the phone.

**Takes:** one continuous read per script, three times; fluffs get
re-entered from the beat, never restarted — the angle switch hides
every join.

**Calibration test before ep. 1:** 30 s of Chinese, phone mic is fine,
set as above → measure eye line, light direction, background blur, and
Hao's real 字/分钟; replace the §15 starting numbers with his own.
