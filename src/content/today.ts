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
 *  - `en` is the same card in English (the /today/en edition, for readers who
 *    come from LinkedIn): its own `do`, `why` and optional `when`, translated
 *    from the Chinese — never a different piece of advice. Keep `do` under
 *    ~70 characters and `why` under ~140.
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
    en: {
      do: "First thing after waking, go and see daylight.",
      why: "Your brain starts the day’s clock the moment your eyes meet daylight. The later the light, the later you feel sleepy.",
      when: "On waking",
    },
  },
  {
    episode: "fi-coffee",
    pillar: "sleep",
    do: "下午三点以后，\n不喝咖啡。",
    why: "想十一点睡，往前推八个小时，就是今天的最后一杯：11 − 8 = 3。",
    en: {
      do: "No coffee after 3 pm.",
      why: "To sleep at 11, count back eight hours — that is your last cup. 11 − 8 = 3.",
    },
  },
  {
    episode: "fi-dim-lights",
    pillar: "sleep",
    do: "睡前一小时，\n先关大灯。",
    why: "褪黑素不是买来吃的，是关灯关出来的。暖灯优先，屏幕能少看就少看。",
    en: {
      do: "An hour before bed, switch off the big light.",
      why: "Melatonin isn’t something you buy. You make it by dimming the lights — warm lamps first, fewer screens.",
    },
  },
  {
    episode: "fi-temperature",
    pillar: "sleep",
    do: "睡前，把卧室\n调低两度。",
    why: "入睡的秘密：身体要先降 0.5 度。屋里一热，想降降不下去，就翻来覆去。",
    en: {
      do: "Before bed, turn the bedroom down two degrees.",
      why: "To fall asleep, your body has to cool by half a degree. In a warm room it can’t, so you toss and turn.",
    },
  },
  {
    episode: "fi-sleep-appetite",
    pillar: "sleep",
    do: "想吃得健康，\n今晚先早睡。",
    why: "没睡好，身体以为有危机，刹车又没电，手就伸向甜的、油的。",
    when: "今晚",
    en: {
      do: "Want to eat well? Sleep early tonight.",
      why: "After a bad night your body thinks there is a crisis and the brakes run flat — so the hand reaches for sweet and oily.",
      when: "Tonight",
    },
  },

  /* ── 关系 ───────────────────────────────────────────── */
  {
    episode: "fi-couple-20min",
    pillar: "relationship",
    do: "今天留 20 分钟，\n只给对方。",
    why: "不看手机，不聊家务。在一起的时间，不等于交流的时间。",
    when: "今晚",
    en: {
      do: "Give your partner 20 minutes today.",
      why: "No phone, no talk about chores. Time spent together is not the same as time spent talking.",
      when: "Tonight",
    },
  },
  {
    episode: "fi-fake-egg",
    pillar: "relationship",
    do: "在一起的时候，\n把手机放下。",
    why: "鸭子会放下真蛋去孵网球。手机就是你的网球：刷得越多，身边的人越显得无聊。",
    en: {
      do: "When you are together, put the phone down.",
      why: "A duck will leave its real egg to sit on a tennis ball. The phone is your tennis ball: the more you scroll, the duller real people look.",
    },
  },
  {
    episode: "fi-consistency",
    pillar: "relationship",
    do: "进家门前，\n把坏天气\n留在门外。",
    why: "情绪可预测，是亲密关系里的安全感。外面越不确定，身边这个人的稳定越珍贵。",
    en: {
      do: "Before you walk in, leave the bad weather outside.",
      why: "A predictable mood is what safety feels like in a relationship. The less certain the world, the more that steadiness is worth.",
    },
  },
  {
    episode: "fi-touch",
    pillar: "relationship",
    do: "今天，\n多碰一碰对方。",
    why: "牵牵手，搭搭肩。皮肤接触时，身体会分泌催产素，从生理上给关系升温。",
    en: {
      do: "Touch them a little more today.",
      why: "Hold a hand, rest a hand on a shoulder. Skin contact releases oxytocin — it warms a relationship physically.",
    },
  },
  {
    episode: "fi-contra",
    pillar: "relationship",
    do: "把「你为什么不」\n换成「我们怎么」",
    why: "把问题放在你们外面，不要放在你们之间。像魂斗罗：两个人一起面对外面。",
    when: "快吵起来时",
    en: {
      do: "Swap “why don’t you…” for “how do we…”.",
      why: "Put the problem outside the two of you, not between you. Two players on one side, facing out.",
      when: "Before a fight",
    },
  },
  {
    episode: "fi-eye-contact",
    pillar: "relationship",
    do: "说话的时候，\n看着他的眼睛。",
    why: "相互注视之后，好感和亲近感都会上升。",
    en: {
      do: "When you talk, look into their eyes.",
      why: "After a shared gaze, liking and closeness both go up.",
    },
  },

  /* ── 营养 ───────────────────────────────────────────── */
  {
    episode: "fi-supermarket",
    pillar: "nutrition",
    do: "进超市前，\n先分三类：\n必买、可买、不买。",
    why: "鸡蛋牛奶故意放在最远的角落，就是要你把整个超市逛一遍。",
    en: {
      do: "Before the supermarket, sort the list in three: must, maybe, never.",
      why: "Eggs, milk and bread sit in the farthest corner on purpose — so you walk past everything else.",
    },
  },
  {
    episode: "fi-six-countries",
    pillar: "nutrition",
    do: "这一顿，\n选新鲜的，\n不选加工的。",
    why: "一张只画了六个国家的图，让脂肪背了五十年的锅。新鲜的，永远比加工的强。",
    en: {
      do: "For this meal, pick fresh over processed.",
      why: "A chart that showed only six countries had fat take the blame for fifty years. Fresh always beats processed.",
    },
  },
  {
    episode: "fi-sugar-names",
    pillar: "nutrition",
    do: "翻到包装背面，\n数数糖的化名。",
    why: "只躲 Sugar 这个词，远远不够：糖有 23 个化名。",
    when: "拿起包装时",
    en: {
      do: "Flip the pack over and count sugar’s aliases.",
      why: "Avoiding the word “sugar” is nowhere near enough: it goes by 23 other names.",
      when: "Pack in hand",
    },
  },
  {
    episode: "fi-glycation",
    pillar: "nutrition",
    do: "今天，\n少吃一样甜的。",
    why: "吃很多糖，就像把身体放进面包机里烤。这不是比喻，是同一个化学反应：糖化。",
    en: {
      do: "Skip one sweet thing today.",
      why: "Eating a lot of sugar is like putting your body in a toaster. Not a metaphor — it is the same reaction: glycation.",
    },
  },
  {
    episode: "fi-brain-brake",
    pillar: "nutrition",
    do: "把零食放到\n看不见的地方。",
    why: "大脑的刹车每天能踩的次数有限。看不见的零食，不需要踩刹车。",
    en: {
      do: "Put the snacks where you can’t see them.",
      why: "Your brain’s brake only works so many times a day. A snack you can’t see needs no braking.",
    },
  },
  {
    episode: "fi-insulin-rollercoaster",
    pillar: "nutrition",
    do: "这一顿，\n先吃菜，再吃饭。",
    why: "先蔬菜纤维，再米饭面条。血糖平稳，人也更从容。",
    en: {
      do: "This meal: vegetables first, then the rice.",
      why: "Fibre first, then rice or noodles. Steadier blood sugar, and a steadier you.",
    },
  },
  {
    episode: "fi-fatty-acid",
    pillar: "nutrition",
    do: "今天，\n吃一把核桃。",
    why: "细胞里的比例，就是盘子里的比例。Omega-3 多一点，细胞膜更柔韧。",
    en: {
      do: "Eat a handful of walnuts today.",
      why: "The mix in your cells is the mix on your plate. More omega-3, and the cell membrane stays supple.",
    },
  },
  {
    episode: "fi-also-sugar",
    pillar: "nutrition",
    do: "想吃甜的，\n吃一个完整的水果。",
    why: "完整的水果没有配料表。「0 蔗糖」「不加糖」，不等于没有糖。",
    en: {
      do: "Craving something sweet? Eat a whole fruit.",
      why: "A whole fruit has no ingredient list. “No added sugar” does not mean no sugar.",
    },
  },
  {
    episode: "fi-trans-fat",
    pillar: "nutrition",
    do: "炒菜，\n别等油冒烟。",
    why: "油冒烟的过程，就是把脂肪变成反式脂肪的过程。",
    when: "做饭的时候",
    en: {
      do: "When you cook, don’t let the oil smoke.",
      why: "Smoking oil is fat turning into trans fat.",
      when: "While cooking",
    },
  },
  {
    episode: "fi-free-radical",
    pillar: "nutrition",
    do: "今天的盘子，\n多一种颜色。",
    why: "自由基是身体运转时冒的火花。最好的抗氧化，来自五颜六色的新鲜蔬果。",
    en: {
      do: "Add one more colour to today’s plate.",
      why: "Free radicals are the sparks a running body throws off. The best antioxidants come from fresh produce in many colours.",
    },
  },
  {
    episode: "fi-glycogen",
    pillar: "nutrition",
    do: "饭后别坐下，\n先动一动。",
    why: "让肌肉里的小电池先放电、再充电，糖变成脂肪的那一步就少发生。",
    when: "吃完饭以后",
    en: {
      do: "After eating, don’t sit down. Move a little.",
      why: "Let the small batteries in your muscles drain, then recharge — and less of the sugar ends up as fat.",
      when: "After a meal",
    },
  },
  {
    episode: "fi-belly-fat",
    pillar: "nutrition",
    do: "想吃零食时，\n先看一眼小肚子。",
    why: "是它在说话，我没那么饿。",
    when: "手伸向零食时",
    en: {
      do: "Before a snack, glance at your belly.",
      why: "That is the belly talking. I’m not that hungry.",
      when: "Reaching for one",
    },
  },
  {
    episode: "fi-carbs-five-words",
    pillar: "nutrition",
    do: "今天的主食，\n换成慢碳。",
    why: "吸收越慢的碳水越好：蒸土豆、红薯、燕麦、玉米、藜麦。",
    en: {
      do: "Swap today’s staple for a slow carb.",
      why: "The slower a carb is absorbed, the better: steamed potato, sweet potato, oats, corn, quinoa.",
    },
  },
  {
    episode: "fi-gut-serotonin",
    pillar: "nutrition",
    do: "今天，喂饱\n肚子里的细菌。",
    why: "它们吃纤维：豆类、瓜果、蔬菜、全谷物。吃饱了，顺便给你造血清素。",
    en: {
      do: "Feed the bacteria in your gut today.",
      why: "They eat fibre: beans, fruit, vegetables, whole grains. Well fed, they make serotonin for you on the side.",
    },
  },
  {
    episode: "fi-fries-story",
    pillar: "nutrition",
    do: "想补纤维，\n吃苹果，别点薯条。",
    why: "100 克土豆的纤维和苹果差不多，可一份薯条还带着 15 克油。",
    en: {
      do: "Want fibre? Eat the apple, not the fries.",
      why: "100 g of potato has about as much fibre as an apple — but a serve of fries brings 15 g of oil with it.",
    },
  },
  {
    episode: "fi-obesity-disease",
    pillar: "nutrition",
    do: "找一根软尺，\n量一下腰围。",
    why: "最直观的自查：男 90 厘米、女 85 厘米以下，基本可以（中国标准）。",
    en: {
      do: "Find a tape measure and check your waist.",
      why: "The plainest self-check: under 90 cm for men and 85 cm for women is broadly fine (China’s standard).",
    },
  },
  {
    episode: "fi-water-nutrient",
    pillar: "nutrition",
    do: "早上灌满大杯子，\n今天喝完。",
    why: "够不够，看小便颜色：无色或淡黄、没有气味，就是够了。",
    when: "早上",
    en: {
      do: "Fill one big bottle in the morning. Finish it today.",
      why: "Enough or not? Look at the colour: clear or pale yellow, with no smell, means enough.",
      when: "Morning",
    },
  },
  {
    episode: "fi-dietary-fibre",
    pillar: "nutrition",
    do: "补纤维，\n别只盯着芹菜。",
    why: "芹菜的丝只是其中一种。可溶性纤维在燕麦、豆类和水果的果胶里。",
    en: {
      do: "For fibre, look past the celery.",
      why: "Celery’s strings are only one kind. Soluble fibre lives in oats, beans and the pectin in fruit.",
    },
  },
  {
    episode: "fi-appetite-dial",
    pillar: "nutrition",
    do: "这一顿，\n多加一份蛋白质。",
    why: "食欲不是定值，是个可以拧的旋钮。蛋白质多一点，同样的热量更饱。",
    en: {
      do: "Add a serving of protein to this meal.",
      why: "Appetite is not fixed — it is a dial you can turn. A bit more protein, and the same calories keep you fuller.",
    },
  },
  {
    episode: "fi-snack-portions",
    pillar: "nutrition",
    do: "零食，\n只买小包装。",
    why: "第一口，就拿走了大部分的爽。一块饼干 25 卡，却有 80% 的满足。",
    en: {
      do: "Buy snacks in the small pack only.",
      why: "The first bite carries most of the pleasure. One biscuit is 25 calories and 80% of the satisfaction.",
    },
  },

  /* ── 运动 ───────────────────────────────────────────── */
  {
    episode: "fi-bdnf",
    pillar: "exercise",
    do: "要动脑之前，\n先动动腿。",
    why: "肌肉一动，大脑开始造 BDNF，那是大脑的肥料。运动完再学，学得更好。",
    when: "学习、开会前",
    en: {
      do: "Before you need your brain, move your legs.",
      why: "When muscles move, the brain starts making BDNF — fertiliser for the brain. Learn after exercise and it sticks better.",
      when: "Before study",
    },
  },
  {
    episode: "fi-muscle-fibres",
    pillar: "exercise",
    do: "深蹲十个，\n水瓶弯举十个。",
    why: "天天走一万步，练的是慢肌。站起来用的是快肌，要加一点力量。",
    when: "在家就行",
    en: {
      do: "Ten squats. Ten curls with a water bottle.",
      why: "Ten thousand steps a day train the slow fibres. Standing up uses the fast ones — add a little strength.",
      when: "At home",
    },
  },
  {
    episode: "fi-bone-density",
    pillar: "exercise",
    do: "今天，\n举一点重的东西。",
    why: "骨头是存钙的银行。举重量，就是告诉骨头：要承压，快存款。",
    en: {
      do: "Lift something heavy today.",
      why: "Bone is a bank that stores calcium. Lifting a load tells it: bear weight, make a deposit.",
    },
  },
  {
    episode: "fi-fitness-word",
    pillar: "exercise",
    do: "今天，练一下\n你最短的那个角。",
    why: "身体是五边形战士：力量、耐力、柔韧、灵活度、爆发力。不是一个角长就强。",
    en: {
      do: "Train your shortest corner today.",
      why: "The body is a pentagon: strength, endurance, flexibility, mobility, power. One long corner does not make you fit.",
    },
  },
  {
    episode: "fi-soreness",
    pillar: "exercise",
    do: "别练到瘫。\n练到下次还想去。",
    why: "大脑会记住痛。变强靠的是超量恢复，不需要酸痛做前提。",
    en: {
      do: "Don’t train to collapse. Train so you’ll come back.",
      why: "The brain remembers pain. You get stronger through recovery — soreness is not required.",
    },
  },

  /* ── 情绪 ───────────────────────────────────────────── */
  {
    episode: "fi-cognitive-defusion",
    pillar: "emotion",
    do: "在念头前面加一句：\n「我有一个想法」",
    why: "「我完蛋了」和「我有一个想法：我完蛋了」，是两回事。",
    when: "觉得完蛋了时",
    en: {
      do: "Put “I’m having the thought that…” in front of it.",
      why: "“I’m doomed” and “I’m having the thought that I’m doomed” are two different things.",
      when: "When you panic",
    },
  },
  {
    episode: "fi-dare-to-be-happy",
    pillar: "emotion",
    do: "对自己说一句：\n我做得很好。",
    why: "总说「运气好」「没什么」，大脑的天平会慢慢倒向威胁。",
    when: "被夸的时候",
    en: {
      do: "Tell yourself: I did that well.",
      why: "Keep saying “just luck” and “it was nothing”, and the brain’s scale slowly tips toward threat.",
      when: "When praised",
    },
  },
];
