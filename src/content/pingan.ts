/*
 * 平安牌 — the words on the house sign at /pingan (2026-11-18).
 *
 * An unlisted page for two readers: not in the nav, the home index, the
 * sitemap or the search, and marked noindex. Nobody is named here and nothing
 * about who is or is not at work is ever written down in this file — each
 * phone keeps its own sign in localStorage.
 *
 * Edit freely: every list below is just lines. The two almanac lists should
 * keep lengths with no common factor (31 and 29), so a pairing takes years to
 * come round again.
 */

/** The day the sign went up. The count starts here, this day included. */
export const PINGAN_START = "2026-11-18";

export type Who = "h" | "w";

/**
 * How long a sign must be held before it turns over — and how the page says
 * so. Two seconds (Hao, 2026-11-18: three was too long and nobody could tell
 * the sign wanted holding). Change the pair together.
 */
export const HOLD_MS = 2000;
export const HOLD_ZH = "两秒";

export const WHO: Record<Who, string> = { h: "老公", w: "老婆" };

/** A tap on a sign that still reads 没被裁. */
export const SAFE_LINES = [
  "还没呢，别咒我",
  "工牌还刷得开",
  "今天 HR 没找我",
  "邮箱还登得上",
  "今日 HR 未翻本宫牌子",
  "苟住了，勿念",
  "活着，谢谢关心",
  "老板今天对我笑了……慌",
  "日历里没有神秘会议",
  "又混过一天",
  "别戳了，在上班",
  "工资还会到账的吧？",
  "稳得很（大概）",
  "再戳要加班了",
];

/** A tap on a sign that has been turned over. */
export const OUT_LINES = [
  "毕业了，勿扰",
  "向社会输送人才",
  "今天睡到自然醒",
  "终于不用开会了",
  "简历已更新",
  "气球摊筹备中",
  "现在是全职家属",
  `按住${HOLD_ZH}：再就业`,
];

/** What the sign says while it is being held, one line after another. */
export const HOLD_OUT = ["真的假的？", "别闹", "……好吧"];
export const HOLD_BACK = ["找到下家了？", "真的？", "恭喜！"];

export const LET_GO = `没按满${HOLD_ZH}，不算数`;

/** Printed small on each sign, under its verdict — for anyone who does read. */
export const HOW_OUT = `按住${HOLD_ZH}翻牌`;
export const HOW_BACK = `按住${HOLD_ZH}再就业`;

/** A quick tap on the thumbprint pad itself: so close. */
export const PAD_TAP = "按住，别松手";
export const BACK_AT_WORK = "再就业成功！";

/** The line under the two signs. */
export const STATUS = {
  none: "双职工家庭 · 今天也平安",
  h: "老公毕业了 · 老婆，以后靠你了",
  w: "老婆毕业了 · 老公，以后靠你了",
  both: "全家毕业 · Plan B 已启动",
};

/** Who the good news leans on. Plan B is the family's real one. */
export const LEAN: Record<Who | "both", string[]> = {
  h: ["老婆，以后靠你了"],
  w: ["老公，以后靠你了"],
  both: ["Plan B 启动：", "一本书、一架钢琴、街上的气球"],
};

/** Days worth a stamp — four characters, set two over two like a seal. */
export const MILESTONES: [number, string][] = [
  [7, "苟满一周"],
  [30, "平安满月"],
  [50, "半百之喜"],
  [100, "百日大吉"],
  [200, "二百不倒"],
  [365, "整整一年"],
];

/** 今日宜 — 31 of them. */
export const YI = [
  "准时下班",
  "带薪喝水",
  "带薪上厕所",
  "更新简历（以防万一）",
  "给对方买杯奶茶",
  "午饭多加一个蛋",
  "认真摸鱼",
  "把年假排上",
  "夸同事一句",
  "早睡",
  "看一眼存款，然后深呼吸",
  "自己带咖啡",
  "在家多吃一口饭",
  "给工牌拍张照留念",
  "开会时认真点头",
  "把活干完再走",
  "回家练琴",
  "扎一个气球",
  "写两页书",
  "抱一下对方",
  "陪娃画条鱼",
  "饭后百步走",
  "周五穿好看点",
  "对老板微笑",
  "吃顿好的",
  "回家路上买束花",
  "多吃公司零食",
  "收拾工位（别误会）",
  "早点回家",
  "喝杯热的",
  "互相报个平安",
];

/** 今日忌 — 29 of them. */
export const JI = [
  "点开 HR 的会议邀请",
  "周五下午看邮箱",
  "回复全员邮件",
  "问「我们组还招人吗」",
  "提涨薪",
  "在工位叹气",
  "接受「快速同步 15 分钟」",
  "刷前同事的动态",
  "心算赔偿金",
  "迟到",
  "和老板对视超过三秒",
  "在群里只发一个「？」",
  "下单大件",
  "把私人物品留在工位",
  "问「公司最近怎么样」",
  "请长假",
  "说「这个做不了」",
  "看财报",
  "午睡睡过头",
  "熬夜",
  "空腹喝咖啡",
  "抢着背锅",
  "在茶水间聊八卦",
  "开会迟到还开摄像头",
  "立 flag",
  "周一请假",
  "说「反正也裁不到我」",
  "跟 HR 开玩笑",
  "忘了给对方报平安",
];
