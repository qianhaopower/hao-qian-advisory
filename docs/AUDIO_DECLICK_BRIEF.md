# 去咔声交接简报（2026-08-29）

给接手音频清理的 session：Hao 说的"爆破音/咔咔声"已经定性，别从头分析，按这份简报做。

## 这个声音是什么（已由 Hao 亲耳确认）

- **1–3 毫秒的宽频短脉冲**，主要出现在字与字的缝隙里，无周期性。
- Hao 听过"只含被去除咔声"的 diff 轨（`~/Downloads/click-check/D-只有被去掉的咔声.m4a`），确认 100% 就是他听到的声音。改动前先听这个文件校准耳朵。
- **已排除**：挂钟/周期噪声、无线断点/数字故障、衣服持续摩擦、DJI 硬件问题。
- 根因二选一未定（口腔音 vs 衣料轻碰麦壳），等 Hao 的 4×20s 对照实验；但**不影响后期去除**。
- 注意：旧手机麦的素材里同样有这声音，只是被底噪埋着。新 DJI 麦（Mic Mini 2）更干净 + pipeline 的 `loudnorm` 提升 ~18 dB 把它暴露了。**这是设备变好才听见的问题。**

## 已验证的事实（别重复试错）

1. `ffmpeg adeclick` **方向对但强度不够**：能抓住这类脉冲的特征（diff 轨就是它去掉的部分），但 114 个检出只去掉 ~17 个；`adeclick=w=20:o=75:t=1` 两遍串联也只到 97。单靠默认 adeclick 交不了差。
2. WPE 去混响、普通降噪（afftdn）对这个声音无效——它不是稳态噪声。
3. 行业标准答案是 **iZotope RX 的 De-click / Mouth De-click**（RX Elements 打折约 US$30）。若 Hao 已购，走 RX 批处理；未购则在 ffmpeg/sox/python 范围内做更强的脉冲检测+插值修复（思路：高通 4 kHz 包络检出 >中位数+20 dB 的 <5 ms 脉冲 → 对原始波形做 AR 插值/短窗频谱修复），效果必须用下面的验收法证明。

## 验收方法（量化 + 人耳）

- **量化**：16 kHz 单声道提取 → 4 kHz 高通 → 2 ms 帧 RMS 包络 → 计数超过中位数 +20 dB、间隔 >30 ms 的脉冲。处理前后对比计数（参考值：IMG_2595.MOV 全片 794 个 / 3.28 每秒）。目标：降 80% 以上且语音无可闻损伤。
- **人耳**：每次输出两个文件给 Hao——修复版 + **diff 轨（原始减修复、放大 8 倍）**。diff 轨里应该只有咔声、没有语音成分；若 diff 里能听到语音，说明伤到了正文，回退。
- 测试素材：`~/Downloads/IMG_2595.MOV`（4 分钟坐姿，最明显；Hao 指认 67–68 s 处特别清楚）。其余新素材：`Rubber Ball/Debug Decision/Impact Org Memory_2026-08-29*.MP4`。

## 落地位置

验收通过后把去咔声挂进 `scripts/video-pipeline/encode.py` 的音频链，顺序：**去咔声 → loudnorm**（loudnorm 现在在 fc2 的 `[0:a]loudnorm=I=-14:TP=-1.5:LRA=11[af]`）。先去咔再提响度，否则咔声被一起放大。

背景数据（混响基线、DJI vs Galloway 对比）在 memory `video-audio-clicks-and-baseline.md`。
