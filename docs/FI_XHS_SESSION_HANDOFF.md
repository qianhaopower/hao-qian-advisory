# FI 小红书线 — 新 session 启动简报(2026-09-05)

**先读**:`docs/XHS_FORMAT_REFERENCE.md`(全部规则,尤其末尾 PRODUCTION LAW + Episode checklist v2),
记忆 `fi-xiaohongshu-line.md`(踩坑史)。CLAUDE.md 的硬规则不变:不碰 Working Theory 线(英语素材一律不动)。

**状态**:CapCut 路线已稳定,9 集完成(天光/咖啡/调光/温度/夫妻20分钟/孵假蛋/一致性/碰一碰 + 首条测试)。Ep9 是 Hao 认可的基准("都按照这个结果做")。Ep7 起人声用 audio_master.py 母带链(法典第 0 步)。
Hao 只做:录像(开拍先 2 秒封面脸、侧领夹麦、头顶少留白)→ 看草稿 → 导出 → 发。

**每集一条命令链**(工作目录随意,素材放 ~/Movies/FI-videos/<ep>/):
1. 探测语言 → 封面脸候选(前 5 秒抽帧,挑睁眼含笑)→ face1.png
2. 测说话起点和说话终点(RMS)→ 剪辑必须重编码视频(hevc_videotoolbox,禁止 -c:v copy)→ 简单音频链(HP80+轻压缩+线性增益 −14+真峰限制,不做频谱处理;audio_master 仅 A/B 后可选) → **avsync_check.py 三项全过才能往下走**(Ep7 口型晚 0.78s 的教训)
3. transcribe.py(对剪后的源)→ 校对(错字类 + 幻觉尾巴)
4. fx.json:title(暧昧/反转钩子,首帧即封面;金线≤8字、白线≤9字)、pillar{zh,en}(右上角柱子标签,封面必带)、corner_mark、face_frame、reframe、
   cap_colors、toplines 8–12、punch 3–4(在头旁,不挡脸)、floaters/doodles(脸部禁区外)、zoom 2、
   inserts ≈1/22s(每轮只采一个稀缺类别;联系表看情绪:插入演的是这句话的感受,不是名词;
   竖裁前看 6 帧)、endcard_<柱子>_cta(带一行点赞收藏)、bgm(自动增益)
5. venv-jy/bin/python scripts/xhs-pipeline/to_capcut.py <source_ready> <名字> → 读 JSON 数段落
6. Hao 导出 → 我不等吩咐压成 上传版.mp4 → 三件套直接贴在对话里(标题3选1/正文+标签/置顶评论 含音乐署名),不能只写进文件
4b. **插图首选「模拟动画」风格**(Hao 2026-09-21 认可):俯视小世界 + 小人沿路径走 + 游戏 HUD 计分,成对做(错的走法/对的走法),每段 6–10 秒放慢;引擎在 scripts/xhs-pipeline/make_supermarket_sim.py,法典有整节规范。
7. 归档(2026-09-12 起):导出压缩后,原片/母版 .mov/上传版/发布包 移到 ~/Movies/FI-videos/archive/epNN-slug/(命名 epNN-slug-raw-IMG_xxxx.MOV / -master.mov / -upload-xhs.mp4 / -posting.md),更新 archive/README.md,然后 rsync 到 Google Drive「My Drive/FI-videos/archive/」。母版 .mov 是发其他平台用的无水印版。CapCut 里每集只留最后一版草稿,旧版进废纸篓。
8. 每集附表达反馈(语速字/分、停顿、口头禅占比、动量指数 vs 前几集、抽帧看手势表情、眼神),一集只给一个改进目标

**待办**:下一集换柱子(ep5 打印机vs买车 骨架在 content-src/video-scripts/fi-xhs-ep5-printer-car.md);
花字资源采集(Hao 在 CapCut 随手用一个花字保存,我读 ID);账号名未定(角标占位 Friends Intelligence);
7 天后看前几条数据。未提交的仓库改动:docs/、scripts/xhs-pipeline/、content-src/video-scripts/fi-xhs-*——
要不要 commit 由 Hao 说。
