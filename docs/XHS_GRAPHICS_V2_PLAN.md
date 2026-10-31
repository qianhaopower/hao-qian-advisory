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

## 7. 零件库 `scripts/xhs-pipeline/fx_parts.py` + v3 合成器（2026-10-31）

Hao 截了小Lin 免税 / HYROX 两集的 16 张图："为什么我们做不出这些效果？每个做成一个功能。" 拆完是 11 种零件，
全部进了 `fx_parts.py`（纯 PIL，一个函数一个零件），`compose_v3.py` 按 `fx_v3.json` 的时间线调用它们。

| 零件 | 她的用法 | 我们的函数 / json 键 | 放哪 |
|---|---|---|---|
| 气泡簇 bubble cluster | 名词一个个围着头冒出来 | `bubble()` / `"bubbles"` + steps | 脸两侧，7 个固定槽位，绝不进脸框 |
| 锚卡矩阵 matrix | 行×列、? 逐格翻成值，整集召回 | `matrix_layer()` / `"matrix".recalls` | 全屏 + 小头像 |
| 手边卡 twin cards | 1–3 张带线条图标的深色卡 | `card()` + `icon_*` / `"twin"` | 胸口带 0.52–0.74H |
| 算账 calc | 顶部类目卡 + 翻牌数字 + 大窗人像 | `_counter_row()`, `flip_counter()` / `"calc"` | 全屏 |
| 人+手机 split phone | 圆角人像 + 手机壳里真截图 | `fx_split_phone()`（本集没有真截图，未用） | 全屏 |
| 纸面拼贴 desk collage | 真照片做拍立得贴在格纸上 | `fx_desk_collage()`（本集无真照片，未用） | 全屏 |
| 海报章节 poster | 网点大字 + 英文小标 + 居中人像窗 | `halftone_text()`, `fx_poster_chapter()` | 章节 |
| 卡片行 card row | 素材下沿一张张弹出的浅色卡 | `light_card()`, `chip()` / `"cardrow"` + steps | 盖在任何画面上 0.60H |
| 侧卡 side tag | 画面边缘滑入的竖卡 | `"sidetag"` | 胸口带，左/右 |
| 名牌三卡 logo trio | 两张斜黑牌，再中间一张大的 | `plate()`, `skew_card()` / `"trio"` | 胸口带 |
| 照片扇 photo fan | 三张真照片叠在下三分之一 | `fx_photo_fan()`（需真照片） | 脸镜头下部 |

共用基元：`ground_dots`（点阵墨底）/ `ground_paper` / `ground_diagonal`、`tint_panel`（她的行色板：teal violet navy wine olive slate rust，低饱和，只做底不做字）、
`label_block`（中文 + 英文小字，所有卡的最小单位）、`corner_brackets`、`ornament`、`shadow`、`pip_circle` / `pip_rect`、`caption`（一行白字、细黑边、略斜）。

**人脸处理 `grade_face`**：三次试错后定稿——不逐像素抠墙（抠出灰斑和光晕，Hao 当场看见了），改成两件与内容无关的事：
高光滚降曲线（>150 压 0.62）+ 以脸为中心的光衰减。墙从 190 降到脸旁 ≈135 / 边缘 ≈100，脸保持 ≈150，帧均值 ≈103。零抠像，不会闪。

**v3 合成器的规则**（compose_v3.py 自带 lint，渲染前会打印违规）：脸段 ≥5 s；图形成组（组内只换图形，小头像不断）；
场景边界 ±1.5 s 内不换景别，有东西在身旁时锁 1.0；字幕一行、白色、0.80H，多行字幕按行拆开按字数分时；
胸口带 0.52–0.74H 是所有"旁边的东西"的家。

**v3 流程（不走 CapCut）**：原片 → `cut_by_edl.py` → `build_captions.py` → 写 `fx_v3.json`（章节 / 矩阵 / 气泡 / 卡片行 … 挂在哪句话上）
→ `compose_v3.py --stills` 看关键帧 → `compose_v3.py` 全片（4 进程，约一刻钟）→ 封面 / 正文 / 归档照旧。想手动拖时间线的那集再出 CapCut 草稿。

Ep34 v3 = `~/Movies/FI-videos/water-v3/`（fx_v3.json 另存为 `scripts/xhs-pipeline/fx_v3_example.json`）。

## 8. 备真图 `scripts/xhs-pipeline/real_assets.py`（2026-10-31，Hao：「以后不用素材库里的东西，都去真图」）

她的"质感"一半来自真东西：真网页、真文件、真产品照。所以 v3 流程在写 fx json 之前多一步 **备真图**：

```
real_assets.py shot  URL out.png [--h 7000] [--mobile]   # 无头 Chrome 截网页（桌面 1280 宽 / 手机 430 宽）
real_assets.py pdf   FILE|URL prefix --page N            # PDF 某页转 PNG（pdftoppm）
real_assets.py image URL out.jpg --license "…"           # 有授权的照片（Wikimedia Commons: Special:FilePath/<File>）
real_assets.py html  card.html out.png                   # 我们自己写的 HTML 数据卡（真数字 + 来源行；不仿别人的页面）
real_assets.py crop  in out x0 y0 x1 y1                  # 从长截图里切出相关段落
```

每集一个文件夹 `~/Movies/FI-videos/assets/real/<ep>/`，`manifest.json` 记来源 URL、标题、抓取日期、授权。
合成器里对应的零件：`screens`（真页面放桌面、1.4 s 后硬推进 focus 区、红框）、`phone`（手机壳里放手机版截图、可慢滚）、
`collage` / `fan`（真照片拍立得）、`sidetag.file`（侧卡带图）。

已知边界：PubMed 对无头浏览器做人机校验（截到的是 Checking your browser），换 nature.com / PMC / 出版社页；
eatforhealth.gov.au 对 urllib 超时，用 curl 下 PDF 再本地转；Chrome 的 `#:~:text=` 文本片段在无头模式下不滚动，
所以用长截图 + crop 定位段落。

Ep35 纤维 = 第一集全真图：Better Health Channel（桌面段落 + 手机版）、EJCN 2021 β-葡聚糖荟萃分析（nature.com）、
USDA FoodData Central 芹菜/苹果/燕麦、NHMRC 纤维 NRV 第 47 页（存档备用）、Commons 的苹果（CC0）/ 芹菜（NCI 公版）/ 谷物（USDA 公版）。
下一步让 Hao 自己拍苹果、芹菜、燕麦的照片替换 Commons 图——自己的真照片 > 别人的真照片。


**§8 补充（2026-10-31 晚，Ep38 零食回看）：** 「不用素材库」指的是证据（真页面、真照片）。情绪素材照旧可以从素材库找（Hao：满头大汗喝冰可乐那种，让人有感觉），用 `footage` 键。章节卡至少 3 s（1.2–2.7 s 他读不完）；手机截图的 `y` 要让关键句在屏幕里，不是滚到链接区。

## 9. Ep35 真图版第一次回看（2026-10-31）→ 三条新规则

Hao 看完 Ep35 真图版：① 说话的画面灰暗；② 手机、网页这类带字的图停留太短，"还没看到就切走了"；③ 小圆圈发灰、白环和图没对齐、推得太近看不见头发。

**① 脸的调色，按数字对齐她（和 Hao 认可过的 Ep34 已发布版）：**

| 每帧测量 | 小Lin 脸镜头 | Ep34 已发布（认可） | v3（被批灰暗） | v4（现行） |
|---|---|---|---|---|
| 全帧亮度 | 97–112 | 120 | 105 | 133 |
| 对比度（亮度 std） | 69–76 | 71 | 63 | 81 |
| 全帧饱和度 | 26–40 | 47 | 30 | 49 |
| 脸区亮度 / 饱和 | 106–167 / 53–69 | 139 / 88 | 153 / 44 | 168 / 67 |

教训：亮度均值一样也会"灰"——缺的是对比和肤色饱和。`grade_face` v4 = 高光滚降（>165 ×0.72）+ 只压远边缘的光衰减 0.34 + 饱和 ×1.5 + 对比 ×1.10 + 亮度 ×1.03。
测法在 `scratchpad jump/grade_compare`（全帧 + 脸区 0.38–0.62W × 0.26–0.44H）。每换一次调色先跑这张表再给 Hao 看。

**② 最短停留 = 种类底线 + 阅读时间（`compose_v3.min_hold`）：** 真网页/论文页 6 s（先整页 1.4 s 再推近），手机 6 s，
矩阵第一次出现 5 s、召回 3.5 s，算账 2.2 s × 计数器 + 1.5，拼贴每张 1.6 s，素材 2.5 s；
身旁的东西从最后一次弹出算起：名牌 2.0 s、气泡 1.6 s、图标卡 2.2 s、照片扇 1.8 s、侧卡 3 s + 0.09 s/字（带图 +2 s）、卡片行每张 2 s。
合成器自动把不够的延长到下一场景之前，延不够的打 lint。原则：字越多、越新，停得越久；人眼读一张新卡至少好几秒。

**③ 小圆圈：** 直径 280，取景 0.60 倍画幅宽（整头 + 发际，有头顶留白），和大画面同一套调色（不再单独压暗），白环 5 px 与图同心（之前的错位是阴影 padding 没有按中心贴）。

**① 修正（同日晚）：v4 仍被 Hao 判为"暗、发灰"——"原始视频甚至不用改都挺好看"。** 全版本逐项测量后的结论：他认可的 Ep34 发布版比 v4 更暗（亮度 120 vs 132）却不显灰，差别在**暖色和肤色饱和**（R−B 16、脸饱 88），而 v3/v4 偏冷偏灰（R−B 10）。
所以 `grade_face` **v5 = 不压墙、不加曲线、不加暗角**，只保留 Ep34 以来认可的 natural 家族并加一点暖：R×1.02 / B×0.98 → 饱和 ×1.45 → 对比 ×1.04 → 亮度 ×1.04。
结果：亮度 155、对比 85、饱和 47、脸亮 173 / 脸饱 79、墙 211、R−B 23。墙保持手机原片的亮度。
"脸和墨色卡亮度拉近以减少闪"的想法到此为止：Hao 的眼睛优先，闪的问题靠分组（少回脸）解决，不靠压暗他的脸。
对比表：`~/Downloads/FI-调色对比表.png`、`FI-调色v5对比.png`。

## 10. 景别切换频率 + 按这套剪一集的步骤（2026-10-31 定稿，给下一条小红书视频用）

**景别规则（Hao：一会儿一大一小太频繁）。** 量了她三部：同场景内的硬切（≈远近景切换）每分钟 3.2 / 5.9 / 7.0 次，间隔中位数 5–16 s；
我们 Ep35 之前是每分钟 8.1 次（按脸上时间 12.3 次），间隔中位数 5 s。现在 `compose_v3`：两次切换至少隔 **8 s**（`zoom_min_gap`），
从图形世界回到脸后 **3 s 内不切**（`zoom_settle`）且每次回来都落在**远景 1.0**，场景边界 ±1.5 s 不切，身旁有东西时锁远景；
超过每分钟 5 次打 lint（`zoom_max_per_min`）。渲染时打印 `zoom: N framing steps = x/min`，目标 3–5/min。
一大一小是抓注意力用的，不是节拍器。

**按这套剪一集（新视频来了照抄）：**

1. 原片进 `~/Movies/FI-videos/<slug>/`：`cut_by_edl.py` 去废话 → `post_cut.py`（人声链 HP80 + 压缩 + −14 LUFS）→ `source_ready.mp4`；`build_captions.py` → `captions.json`（照旧，含 CAPTION GATE）。
2. **备真图**：读脚本列出要证明的句子 → `real_assets.py shot/pdf/image/html` 进 `~/Movies/FI-videos/assets/real/<ep>/`（真网页、真论文、真数据页、有授权或自己拍的照片；PubMed 挡无头浏览器用出版社页）；能让 Hao 自己拍的实物先让他拍。
3. 写 `fx_v3.json`（抄 `scripts/xhs-pipeline/fx_v3_example_ep35.json`）：title / pillar / endcard / bgm；chapters；matrix（整集一张，3–5 次召回）；
   图形成组：screens（真页面 ≥6 s）、phone、collage、footage；脸上：trio / twin / bubbles / sidetag / fan / punch / cardrow，全在胸口带。
   字幕一行白色，不配色。
4. `compose_v3.py fx_v3.json --stills t1,t2,…` 看关键帧（脸色对照表、卡片不进脸框、停留够读）；看 `hold:` / `lint:` / `zoom:` 三类输出。
5. `compose_v3.py fx_v3.json` 全片（4 进程约一刻钟）→ 同时间点对比图 → 放 `~/Downloads` 给 Hao。
6. 封面 / 正文 / 发布 / 归档照 `docs/XHS_FORMAT_REFERENCE.md` 的法。脸的调色 = `fx_parts.grade_face` v5，不许再压暗。
