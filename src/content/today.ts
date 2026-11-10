/*
 * The /today deck — 今天只做一件事.
 *
 * Every Friends Intelligence episode leaves one small action; each is printed
 * here as a card. Same philosophy as the rest of the library: adding a card =
 * adding one entry below. No CMS, ever.
 *
 * Rules (keep the deck honest):
 *  - One card per episode, and only for an episode that really ends in
 *    something to DO. An episode with no single action gets no card
 *    (Ep. 12, the whole-book special, is "do all of it" — no card).
 *  - `do` and `why` come from the episode's own key points and summary in
 *    src/content/videos.ts. Never invent advice the film does not give.
 *  - `do` is written as short lines split with "\n" — at most 9 full-width
 *    characters a line, at most 3 lines — so it sets cleanly on the big card
 *    and the small one.
 *  - `why` stays under ~60 characters (three lines on the card).
 *  - `when` is optional: the moment to do it, 7 characters or fewer.
 *  - The drawing is looked up by episode slug in
 *    src/components/today/CardArt.tsx; a card without its own drawing falls
 *    back to its pillar's, so the deck can grow before the art does.
 */
import type { TodayCard } from "@/lib/today-deck";

export const TODAY_CARDS: TodayCard[] = [
  /* ── 睡眠 ───────────────────────────────────────────── */
  {
    episode: "fi-sleep-daylight",
    pillar: "sleep",
    do: "起床第一件事，\n去见天光。",
    why: "眼睛见到天光的那一刻，大脑才开始给这一天计时。见光越晚，困意来得越晚。",
    when: "起床以后",
    en: "First thing after waking, get daylight in your eyes.",
  },
  {
    episode: "fi-coffee",
    pillar: "sleep",
    do: "下午三点以后，\n不喝咖啡。",
    why: "想十一点睡，往前推八个小时，就是今天的最后一杯：11 − 8 = 3。",
    en: "No coffee after 3 pm.",
  },
  {
    episode: "fi-dim-lights",
    pillar: "sleep",
    do: "睡前一小时，\n先关大灯。",
    why: "褪黑素不是买来吃的，是关灯关出来的。暖灯优先，屏幕能少看就少看。",
    en: "An hour before bed, switch off the big light.",
  },
  {
    episode: "fi-temperature",
    pillar: "sleep",
    do: "睡前，把卧室\n调低两度。",
    why: "入睡的秘密：身体要先降 0.5 度。屋里一热，想降降不下去，就翻来覆去。",
    en: "Before bed, turn the bedroom down two degrees.",
  },
  {
    episode: "fi-sleep-appetite",
    pillar: "sleep",
    do: "想吃得健康，\n今晚先早睡。",
    why: "没睡好，身体以为有危机，刹车又没电，手就伸向甜的、油的。",
    when: "今晚",
    en: "Want to eat well tomorrow? Sleep early tonight.",
  },

  /* ── 关系 ───────────────────────────────────────────── */
  {
    episode: "fi-couple-20min",
    pillar: "relationship",
    do: "今天留 20 分钟，\n只给对方。",
    why: "不看手机，不聊家务。在一起的时间，不等于交流的时间。",
    when: "今晚",
    en: "Give your partner 20 minutes today — no phone, no chores.",
  },
  {
    episode: "fi-fake-egg",
    pillar: "relationship",
    do: "在一起的时候，\n把手机放下。",
    why: "鸭子会放下真蛋去孵网球。手机就是你的网球：刷得越多，身边的人越显得无聊。",
    en: "When you are together, put the phone down.",
  },
  {
    episode: "fi-consistency",
    pillar: "relationship",
    do: "进家门前，\n把坏天气\n留在门外。",
    why: "情绪可预测，是亲密关系里的安全感。外面越不确定，身边这个人的稳定越珍贵。",
    en: "Before you walk in the door, leave the bad weather outside.",
  },
  {
    episode: "fi-touch",
    pillar: "relationship",
    do: "今天，\n多碰一碰对方。",
    why: "牵牵手，搭搭肩。皮肤接触时，身体会分泌催产素，从生理上给关系升温。",
    en: "Touch them a little more today — a hand, a shoulder.",
  },
  {
    episode: "fi-contra",
    pillar: "relationship",
    do: "把「你为什么不」\n换成「我们怎么」",
    why: "把问题放在你们外面，不要放在你们之间。像魂斗罗：两个人一起面对外面。",
    when: "快吵起来时",
    en: "Swap “why don’t you…” for “how do we…”.",
  },
  {
    episode: "fi-eye-contact",
    pillar: "relationship",
    do: "说话的时候，\n看着他的眼睛。",
    why: "相互注视之后，好感和亲近感都会上升。",
    en: "When you talk, look into their eyes.",
  },

  /* ── 营养 ───────────────────────────────────────────── */
  {
    episode: "fi-supermarket",
    pillar: "nutrition",
    do: "进超市前，\n先分三类：\n必买、可买、不买。",
    why: "鸡蛋牛奶故意放在最远的角落，就是要你把整个超市逛一遍。",
    en: "Before the supermarket, sort your list in three: must, maybe, never.",
  },
  {
    episode: "fi-six-countries",
    pillar: "nutrition",
    do: "这一顿，\n选新鲜的，\n不选加工的。",
    why: "一张只画了六个国家的图，让脂肪背了五十年的锅。新鲜的，永远比加工的强。",
    en: "For this meal, pick fresh over processed.",
  },
  {
    episode: "fi-sugar-names",
    pillar: "nutrition",
    do: "翻到包装背面，\n数数糖的化名。",
    why: "只躲 Sugar 这个词，远远不够：糖有 23 个化名。",
    when: "拿起包装时",
    en: "Flip the pack over and count sugar’s aliases.",
  },
  {
    episode: "fi-glycation",
    pillar: "nutrition",
    do: "今天，\n少吃一样甜的。",
    why: "吃很多糖，就像把身体放进面包机里烤。这不是比喻，是同一个化学反应：糖化。",
    en: "Skip one sweet thing today.",
  },
  {
    episode: "fi-brain-brake",
    pillar: "nutrition",
    do: "把零食放到\n看不见的地方。",
    why: "大脑的刹车每天能踩的次数有限。看不见的零食，不需要踩刹车。",
    en: "Put the snacks where you cannot see them.",
  },
  {
    episode: "fi-insulin-rollercoaster",
    pillar: "nutrition",
    do: "这一顿，\n先吃菜，再吃饭。",
    why: "先蔬菜纤维，再米饭面条。血糖平稳，人也更从容。",
    en: "Vegetables first, then the rice.",
  },
  {
    episode: "fi-fatty-acid",
    pillar: "nutrition",
    do: "今天，\n吃一把核桃。",
    why: "细胞里的比例，就是盘子里的比例。Omega-3 多一点，细胞膜更柔韧。",
    en: "Eat a handful of walnuts today.",
  },
  {
    episode: "fi-also-sugar",
    pillar: "nutrition",
    do: "想吃甜的，\n吃一个完整的水果。",
    why: "完整的水果没有配料表。「0 蔗糖」「不加糖」，不等于没有糖。",
    en: "Craving something sweet? Eat a whole fruit.",
  },
  {
    episode: "fi-trans-fat",
    pillar: "nutrition",
    do: "炒菜，\n别等油冒烟。",
    why: "油冒烟的过程，就是把脂肪变成反式脂肪的过程。",
    when: "做饭的时候",
    en: "When you cook, don’t let the oil smoke.",
  },
  {
    episode: "fi-free-radical",
    pillar: "nutrition",
    do: "今天的盘子，\n多一种颜色。",
    why: "自由基是身体运转时冒的火花。最好的抗氧化，来自五颜六色的新鲜蔬果。",
    en: "Add one more colour to today’s plate.",
  },
  {
    episode: "fi-glycogen",
    pillar: "nutrition",
    do: "饭后别坐下，\n先动一动。",
    why: "让肌肉里的小电池先放电、再充电，糖变成脂肪的那一步就少发生。",
    when: "吃完饭以后",
    en: "After eating, don’t sit down — move a little.",
  },
  {
    episode: "fi-belly-fat",
    pillar: "nutrition",
    do: "想吃零食时，\n先看一眼小肚子。",
    why: "是它在说话，我没那么饿。",
    when: "手伸向零食时",
    en: "Before the snack, glance at your belly.",
  },
  {
    episode: "fi-carbs-five-words",
    pillar: "nutrition",
    do: "今天的主食，\n换成慢碳。",
    why: "吸收越慢的碳水越好：蒸土豆、红薯、燕麦、玉米、藜麦。",
    en: "Swap today’s staple for a slow carb.",
  },
  {
    episode: "fi-gut-serotonin",
    pillar: "nutrition",
    do: "今天，喂饱\n肚子里的细菌。",
    why: "它们吃纤维：豆类、瓜果、蔬菜、全谷物。吃饱了，顺便给你造血清素。",
    en: "Feed the bacteria in your gut today.",
  },
  {
    episode: "fi-fries-story",
    pillar: "nutrition",
    do: "想补纤维，\n吃苹果，别点薯条。",
    why: "100 克土豆的纤维和苹果差不多，可一份薯条还带着 15 克油。",
    en: "Want fibre? Eat the apple, not the fries.",
  },
  {
    episode: "fi-obesity-disease",
    pillar: "nutrition",
    do: "找一根软尺，\n量一下腰围。",
    why: "最直观的自查：男 90 厘米、女 85 厘米以下，基本可以（中国标准）。",
    en: "Find a tape measure and check your waist.",
  },
  {
    episode: "fi-water-nutrient",
    pillar: "nutrition",
    do: "早上灌满大杯子，\n今天喝完。",
    why: "够不够，看小便颜色：无色或淡黄、没有气味，就是够了。",
    when: "早上",
    en: "Fill one big bottle in the morning and finish it today.",
  },
  {
    episode: "fi-dietary-fibre",
    pillar: "nutrition",
    do: "补纤维，\n别只盯着芹菜。",
    why: "芹菜的丝只是其中一种。可溶性纤维在燕麦、豆类和水果的果胶里。",
    en: "For fibre, look past the celery.",
  },
  {
    episode: "fi-appetite-dial",
    pillar: "nutrition",
    do: "这一顿，\n多加一份蛋白质。",
    why: "食欲不是定值，是个可以拧的旋钮。蛋白质多一点，同样的热量更饱。",
    en: "Add a serving of protein to this meal.",
  },
  {
    episode: "fi-snack-portions",
    pillar: "nutrition",
    do: "零食，\n只买小包装。",
    why: "第一口，就拿走了大部分的爽。一块饼干 25 卡，却有 80% 的满足。",
    en: "Buy snacks in the small pack only.",
  },

  /* ── 运动 ───────────────────────────────────────────── */
  {
    episode: "fi-bdnf",
    pillar: "exercise",
    do: "要动脑之前，\n先动动腿。",
    why: "肌肉一动，大脑开始造 BDNF，那是大脑的肥料。运动完再学，学得更好。",
    when: "学习、开会前",
    en: "Before you need your brain, move your legs.",
  },
  {
    episode: "fi-muscle-fibres",
    pillar: "exercise",
    do: "深蹲十个，\n水瓶弯举十个。",
    why: "天天走一万步，练的是慢肌。站起来用的是快肌，要加一点力量。",
    when: "在家就行",
    en: "Ten squats, ten curls with a water bottle.",
  },
  {
    episode: "fi-bone-density",
    pillar: "exercise",
    do: "今天，\n举一点重的东西。",
    why: "骨头是存钙的银行。举重量，就是告诉骨头：要承压，快存款。",
    en: "Lift something heavy today.",
  },
  {
    episode: "fi-fitness-word",
    pillar: "exercise",
    do: "今天，练一下\n你最短的那个角。",
    why: "身体是五边形战士：力量、耐力、柔韧、灵活度、爆发力。不是一个角长就强。",
    en: "Train your shortest corner today.",
  },
  {
    episode: "fi-soreness",
    pillar: "exercise",
    do: "别练到瘫。\n练到下次还想去。",
    why: "大脑会记住痛。变强靠的是超量恢复，不需要酸痛做前提。",
    en: "Don’t train to collapse. Train so you will come back.",
  },

  /* ── 情绪 ───────────────────────────────────────────── */
  {
    episode: "fi-cognitive-defusion",
    pillar: "emotion",
    do: "在念头前面加一句：\n「我有一个想法」",
    why: "「我完蛋了」和「我有一个想法：我完蛋了」，是两回事。",
    when: "觉得完蛋了时",
    en: "Put “I’m having the thought that…” in front of it.",
  },
  {
    episode: "fi-dare-to-be-happy",
    pillar: "emotion",
    do: "对自己说一句：\n我做得很好。",
    why: "总说「运气好」「没什么」，大脑的天平会慢慢倒向威胁。",
    when: "被夸的时候",
    en: "Tell yourself: I did that well.",
  },
];
