# FI 小红书线 — 新 session 启动简报(2026-09-05)

**先读**:`docs/XHS_FORMAT_REFERENCE.md`(全部规则,尤其末尾 PRODUCTION LAW + Episode checklist v2),
记忆 `fi-xiaohongshu-line.md`(踩坑史)。CLAUDE.md 的硬规则不变:不碰 Working Theory 线(英语素材一律不动)。

**状态**:CapCut 路线已稳定,6 集完成(天光/咖啡/调光/温度/夫妻20分钟 + 首条测试)。
Hao 只做:录像(开拍先 2 秒封面脸、侧领夹麦、头顶少留白)→ 看草稿 → 导出 → 发。

**每集一条命令链**(工作目录随意,素材放 ~/Movies/FI-videos/<ep>/):
1. 探测语言 → 封面脸候选(前 5 秒抽帧,挑睁眼含笑)→ face1.png
2. 测说话起点 → source_ready = 剪到起点−0.8s + adeclick(温和链)+ loudnorm −14
3. transcribe.py(对剪后的源)→ 校对(错字类 + 幻觉尾巴)
4. fx.json:title(暧昧/反转钩子,首帧即封面)、corner_mark、face_frame、reframe、
   cap_colors、toplines 8–12、punch 3–4、floaters/doodles、zoom 2、inserts ≈1/22s(先采新素材、
   情绪筛片、烘竖屏)、endcard(按柱子)、bgm(自动增益)
5. venv-jy/bin/python scripts/xhs-pipeline/to_capcut.py <source_ready> <名字> → 读 JSON 数段落
6. Hao 导出 → 我不等吩咐压成 上传版.mp4 → 发布包(标题3选1/正文/标签/置顶评论 含音乐署名)

**待办**:下一集换柱子(ep5 打印机vs买车 骨架在 content-src/video-scripts/fi-xhs-ep5-printer-car.md);
花字资源采集(Hao 在 CapCut 随手用一个花字保存,我读 ID);账号名未定(角标占位 Friends Intelligence);
7 天后看前几条数据。未提交的仓库改动:docs/、scripts/xhs-pipeline/、content-src/video-scripts/fi-xhs-*——
要不要 commit 由 Hao 说。
