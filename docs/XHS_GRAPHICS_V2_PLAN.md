# XHS graphics v2 — the 小Lin说 study and what FI takes from it

Started 2026-10-31. Hao: 「小林说大家都是在剪辑剪得好……把我小红书那个输出往这个方向靠一靠。不用非常 rigid 地学，但他每次查的那些图表质量非常高。」
Reference films + per-frame sweeps + cut statistics: `~/Movies/reference/xiaolinshuo/` (NOTES.md there has the raw numbers).

## 1. What was measured (4 films, 2-second frame sweeps + scene-score cuts)

| film | length | visual changes / min | median shot | designed graphics : real footage |
|---|---|---|---|---|
| 免税 | 6:18 | 18 | 2.1 s | ~60 : 40 |
| 黄金 | 5:16 | 27 | 1.5 s | ~70 : 30 (one animated gold-line chart recalled 8×) |
| 财富自由 (横屏) | 12:00 | 32 | 1.2 s | ~65 : 35 (one formula card grows all film) |
| AI 芯片 | 5:16 | 40 | 0.9 s | ~45 : 55 (news footage, every clip with PIP) |
| **FI Ep34 水** | 3:05 | 2 (fades are invisible to the detector; ~20 inserts in truth) | 15.6 s | **15 : 85** — 16 stock clips + 3 flat charts |

## 2. Her insert catalogue (what the "high quality" actually is)

Counted on 免税 and AI 芯片. Per film she uses ~8 kinds; every kind obeys one visual family.

| kind | 免税 | AI芯片 | where it sits | notes |
|---|---|---|---|---|
| A. Anchor card (dark info card, recalled, one row changes per recall) | 15+ recalls, 1 card | 12 recalls (H20 芯片 anchor) | bottom third, under her face | THE core device. Viewers learn to read it. |
| B. Held card (a small card appears beside her hand on a noun) | ~8 | ~8 | beside the hand, ~1/4 frame wide, 1.5–2.5 s | 增值税/消费税/关税 tiles; H20 / 旗舰款 / 性能 |
| C. Chapter title card | 6 | 3 | full frame or over face, 1–2 s | metallic gold CJK + small-caps English under it |
| D. Evidence on a desk (screenshot / invoice / table on paper, red circle, zoom-in) | ~8 | ~10 | full frame, she in square or circle PIP | the screenshot is tilted 1–3°, dated, highlighted |
| E. Real footage, letterboxed in a dark textured frame | ~10 | ~30 | 16:9 clip at native res in the middle 60 % of the frame | **never cropped to portrait**; circular PIP top-right |
| F. Data graphic (bar/line/table), progressive | 2 | 5 | full frame, she in PIP | same palette as the card family |
| G. Cluster / diagram (7 bubbles around her, arrows) | 1 scene (10 s) | 1 (美国/中国 tiles) | around her body | bubbles drop out one by one as she dismisses them |
| H. Meme / joke punctuation (colour bars, cutout heads with bubbles, GIF) | 3 | 6 | full frame, 1 s | the humour beat; never more than ~1 per minute |
| I. Phone mockup (app screens inside a phone frame, two-up) | 6 | 0 | beside her | |
| J. Section tag (small red/green label, top-left, this segment's keyword) | 0 | persistent | top-left during footage runs | 势头强劲 / 捉摸不透 / 国产替代水平 |

Composition rules that hold across every kind:
1. **One family per episode**: near-black textured card, thin gold frame or inner glow, white CJK heading, small-caps English under every label, numbers in a coloured pill. 免税 keyed the rows by channel (green/blue/purple/magenta); AI 芯片 is black + gold only.
2. **Three slots, nothing else**: (a) bottom third under the face (anchor card, toplines); (b) beside the hands (held card); (c) full frame with her in a PIP (circle top-right for footage, square for compositions).
3. **She never disappears.** Full-frame graphic ⇒ PIP. Footage ⇒ PIP. The only face-free frames are 1-second title cards and jokes.
4. **Hard cuts only.** Zero dissolves in 4 films. Cards snap in with a 0.2 s scale-pop; footage cuts straight.
5. **Two-step zoom on the face**, 1.0 / ≈1.25, switched on sentence boundaries, instantaneous.
6. **Footage is shown at native aspect** in a letterbox on the dark textured ground; the caption sits below the clip, not on it.
7. **Everything labelled**: a chart has a title + source line; a screenshot has a date tag; a product render has its name card.

## 3. Why ours looks weaker (the honest diagnosis)

- **Stock clips are cropped**: 14 of Ep34's 16 clips are 1280×720 landscape; PORTRAIT LAW centre-crops them to a 405-px column and upscales 2.7×. Soft, badly framed, random people. She shows the same kind of clip at native res in a letterbox and it reads as "a documentary insert".
- **Our charts are flat white slides** (wt_amount.png: cream ground, two outlined boxes, a bottle) — correct but PowerPoint. Hers are product-grade: dark, layered, gold, with English small caps.
- **The face vanishes ~20× per episode**, each time for 2–8 s. Her face never vanishes.
- **Dissolves** make every change soft; the whole cut feels slow at the same density.
- **No recall**: each of our graphics appears once; her anchor card appears 12–15× and does the teaching.

## 4. The FI v2 grammar (not a copy — the FI version)

Keep: the face take, caption sentence law, cover law, pillar badge, end card, no self-footage inserts, flash gate.
Add, in this priority:

1. **Hard cuts + two-step zoom** (1.0 / 1.22 on sentence starts; no ramps).
2. **Speaker PIP** whenever anything full-frame is on: circle, Ø 300 px, top-right (x 0.82, y 0.12), 6-px gold ring, soft shadow. Hao's own take continues inside it — this is not an insert of himself, it is him staying in the room.
3. **Letterboxed footage** on an ink-textured ground (clip at 1080 wide × 608 tall, centred at y 0.42, 2-px gold hairline, caption below).
4. **Anchor card** per episode, recalled: one dark card, up to 4 rows, each recall changes one row/pill. Written in fx as `"anchor": {"title","rows":[...]}` + `"recalls": [{"match","row","value","state"}]`.
5. **Held cards**: `"held": [{"match","zh","en","icon"?,"side":"left|right","hold"}]`, placed in the free hand-side third, 2 s, scale-pop.
6. **Chapter cards**: `"chapters": [{"match","zh","en"}]` — gold CJK + small-caps English on ink, 1.4 s, hard in/out.
7. **Evidence desk**: `"evidence": [{"match","file","circle":[x,y,r]?,"zoom":[x,y,w,h]?,"date"?}]` — screenshot on paper ground, 2° tilt, red circle, second beat zooms to the region.
8. **Data graphics** keep the existing make_*_anim.py engines but re-skinned to the v2 family (ink ground, gold, white; English small caps), and one graphic per episode is recalled, not shown once.

Per-episode budget (3-minute film): ~1 chapter card per minute, 1 anchor card with 6–10 recalls, 4–6 held cards, 6–10 footage inserts (letterboxed, PIP), 1–2 evidence desks, 1 data graphic with 2–3 recalls, 0–1 joke. That is ~30 graphic events ≈ 10/min — her density, FI's content.

## 5. Trial

Episode: **Ep34 水** (already posted → pure A/B, no deadline; full work dir with captions/fx/edl; 4K source so the 1.22 zoom costs nothing).
Build: a standalone PIL+ffmpeg compositor `scripts/xhs-pipeline/compose_v2.py` driven by `fx_v2.json` (new keys above) so Hao can watch an mp4 without CapCut. If he approves, port the same keys into `to_capcut.py` (pycapcut has `add_mask(MaskType.圆形)` for the PIP) so the normal CapCut flow stays.
Audio: unchanged — the posted master's track.
Deliverable: `~/Movies/FI-videos/water-v2/final_v2.mp4` + a side-by-side contact sheet against the posted cut.

## 6. Ep34 v2 试剪的反馈与量化（2026-10-31）

Hao 看完 v2：「跳来跳去、闪一下，和小Lin完全不是一种感觉」。逐帧 + 亮度统计后，原因不在切法（她也是全硬切，小头像也是瞬间出现），在三件事：

| 指标（每帧平均亮度 0–255） | 小Lin 免税 | 小Lin 芯片 | 小Lin 黄金 | 我们 v2 |
|---|---|---|---|---|
| 硬切 / 分钟 | 17.6 | 33.0 | 23.9 | 21.1 |
| 其中整屏亮度跳变 >45 的切 / 分钟 | 4.4 | 6.8 | 6.7 | **12.6（= 每一刀）** |
| 中间亮度带 60–140 的帧占比 | 74 % | 63 % | 44 % | **6 %** |
| 脸镜头亮度 | 87–143 | ≈90 | ≈66 | **147–153** |
| 图形 / 素材亮度 | 42–88 | — | — | 34–59 |

1. **亮度两极**：我们的脸是白墙 ≈150，卡片是墨色 ≈40，每刀全屏翻 100 多级，这就是「闪」。她的脸镜头和图形只差 30–40 级，所以同样是硬切，不闪。→ 脸镜头压暗（墙压到 ≈100，脸保留），墨色底抬到 ≈45–50，让两边进同一亮度带。
2. **乒乓**：我们每 2–3 s 就从图形世界弹回脸，再弹出去；她进了图形世界会连切 2–4 个图形（素材→素材→卡），小头像一直在，再回脸。→ 图形成组（≥6 s 一组），组内只换图形不回脸；脸段 ≥5 s。
3. **一处三连跳**：景别切换紧贴场景边界（97.5 s：脸出现→0.17 s 后变景别→锚卡弹入）。→ 场景边界前后 1.5 s 内不换景别；回到脸后 1 s 内不弹卡。
4. **卡片压脸**：我们的框比她紧（脸在 0.33H、不见手），手边卡落在 0.45H = 腮和嘴的高度，大字「看颜色」正好压在脸上。她的手边卡在胸口旁。→ 手边卡和大字移到下巴与字幕之间的带（0.56–0.68H），绝不进脸框。
5. **字幕**（Hao 问她是否逐字高亮）：**没有**。她的字幕是一行白色粗体略斜、细黑描边、5–12 字一句、固定在 ≈0.63H（紧贴信封式素材下沿），所有镜头位置不变、颜色不变。清楚来自：短、大、固定、不变色。我们的字幕 2–3 行、0.77H、切镜头时变金变红，所以显得乱。→ 字幕改一行（≤12 字，长句按从句切），固定 0.70H 左右，整集只用白色；金/红只留给大字。

修正前 Ep35 不动，先在 Ep34 上重渲 v3 给 Hao 比。
