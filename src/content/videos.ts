/*
 * Video episodes — the library's on-camera work.
 *
 * Same philosophy as the rest of the library: the website is the canonical
 * home; platforms are distribution. Adding an episode = adding one entry to
 * EPISODES below. No CMS, ever.
 *
 * Two series live here, each with its own language and its own channel:
 *   working-theory        English · distributed on LinkedIn
 *   friends-intelligence  中文     · distributed on 小红书 (Xiaohongshu)
 * Page code reads VIDEO_SERIES; adding a third line = one more entry here.
 *
 * Draft episodes: status "draft" keeps an episode OUT of the index page,
 * home, search, sitemap and structured data, and its page is noindex —
 * but the page still builds, so Hao can preview it at its future URL
 * before flipping status to "published".
 */
import { SITE } from "@/content/site";

export type VideoSeriesId = "working-theory" | "friends-intelligence";

export type VideoSeries = {
  id: VideoSeriesId;
  /** Display name — matches the naming used across the library. */
  name: string;
  /** Short qualifier distinguishing the video line from the essay/book line. */
  form: string;
  /** BCP 47 language of the episodes, e.g. "en", "zh-Hans". */
  language: string;
  /** How the language reads on the page, e.g. "English", "中文". */
  languageLabel: string;
  /** English description — used in metadata and the library chrome. */
  description: string;
  /** Description in the series' own language, shown beside the English one. */
  nativeDescription?: string;
  /** Where episodes are distributed after publishing here first. */
  platform: string;
  /** The channel itself — omitted until the URL is known; never a guess. */
  platformUrl?: string;
  /** The account name on that channel, when it differs from Hao's own. */
  platformHandle?: string;
  /** Where the ideas come from — the essays, the book. */
  origin?: { label: string; href: string };
};

export const VIDEO_SERIES: Record<VideoSeriesId, VideoSeries> = {
  "working-theory": {
    id: "working-theory",
    name: "Working Theory",
    form: "On camera",
    language: "en",
    languageLabel: "English",
    description:
      "The theory series, spoken — one idea per episode, face to camera, published here first and distributed on LinkedIn.",
    platform: "LinkedIn",
    platformUrl: SITE.linkedin,
    origin: { label: "From the essays", href: "/writing" },
  },
  "friends-intelligence": {
    id: "friends-intelligence",
    name: "Friends Intelligence",
    form: "On camera",
    language: "zh-Hans",
    languageLabel: "中文",
    description:
      "The book's seven intelligences, spoken in Chinese — one everyday practice per episode, face to camera, published here first and distributed on 小红书 (Xiaohongshu).",
    nativeDescription:
      "用七种智慧拆解生活：财富 · 关系 · 学习 · 情绪 · 营养 · 运动 · 睡眠。每集一个小窍门，先在这里发表，再发到小红书。",
    platform: "小红书",
    platformUrl: SITE.xiaohongshu || undefined,
    platformHandle: SITE.xiaohongshuHandle,
    origin: { label: "From the book", href: "/books/friends-intelligence" },
  },
};

/** Display order on /videos and the home index. */
export const VIDEO_SERIES_ORDER: VideoSeriesId[] = [
  "working-theory",
  "friends-intelligence",
];

export type SupportingVisual = {
  /** public path, e.g. /videos/wtv-1/figure-1.jpg */
  src: string;
  alt: string;
  caption?: string;
};

export type SevenDaySignals = {
  /** date the snapshot was taken, ISO yyyy-mm-dd */
  recordedAt: string;
  /** reach: views or impressions on the distribution platform */
  reach?: number;
  /** meaningful response: comments + saves + shares */
  responses?: number;
  /** identity/conversion signal: relevant follows, useful DMs, invitations */
  inbound?: string;
  note?: string;
};

export type VideoEpisode = {
  slug: string;
  series: VideoSeriesId;
  /** Episode number within the series (video numbering, not essay №). */
  sequence: number;
  title: string;
  /** English gloss of a non-English title — for readers of the library, and share cards. */
  titleEn?: string;
  status: "draft" | "published";
  /** ISO yyyy-mm-dd. Required once published. */
  publishedAt?: string;
  /** BCP 47, e.g. "en" */
  language: string;
  /** Whole seconds. Omit until the final cut exists. */
  durationSeconds?: number;
  /** The opening claim — one sentence the viewer can repeat. */
  hook: string;
  /** 2–3 sentence summary for listings and metadata. */
  summary: string;
  /**
   * Final video. Either a file URL (.mp4/.webm) rendered as a native player,
   * or a YouTube/Vimeo embed URL rendered as an iframe. Video files live on
   * the media shelf (GitHub release "media" — scripts/publish-video.sh),
   * never in the repo. Omit while the episode is in production.
   */
  videoUrl?: string;
  /** "9:16" (default for this series) or "16:9" */
  aspect?: "9:16" | "16:9";
  /** Poster/thumbnail, public path or URL. */
  poster?: string;
  /** WebVTT captions file (public path). Used only with file URLs. */
  captions?: string;
  /** The full script/transcript, one string per paragraph. Part of the permanent record. */
  transcript?: string[];
  /** The idea to keep — short list the viewer should remember. */
  keyPoints?: string[];
  /** Diagrams, charts, evidence shown in the episode. */
  supportingVisuals?: SupportingVisual[];
  /** Where the episode sits in its source — a book pillar, an essay series. */
  topic?: string;
  /** LinkedIn publishing package (manual publishing, Phase 1). */
  linkedinCaption?: string;
  linkedinTags?: string[];
  /** Filled in AFTER publishing natively on LinkedIn. */
  linkedinPublishedUrl?: string;
  /** Publishing package for a non-LinkedIn channel (小红书 note text + tags). */
  platformCaption?: string;
  platformTags?: string[];
  /** Filled in AFTER the note goes live on that channel. */
  platformPublishedUrl?: string;
  /** Seven-day snapshot, recorded manually. */
  signals?: SevenDaySignals;
};

export const EPISODES: VideoEpisode[] = [
  {
    slug: "speaker-theory",
    series: "working-theory",
    sequence: 1,
    title: "Speaker Theory",
    status: "published",
    publishedAt: "2026-08-16",
    language: "en",
    durationSeconds: 108,
    hook: "The same sentence, said by a different person — or heard on a different day — is a different sentence.",
    summary:
      "Why leadership communication is like adjusting a speaker's volume: the same words land as a whisper from a peer and a siren from a manager, your title moves your default volume, and the listener's moment moves their sensitivity. Told through one real story — a single curious question at a project review, asked during performance season.",
    videoUrl:
      "https://github.com/qianhaopower/hao-qian-advisory/releases/download/media/speaker-theory.mp4",
    aspect: "9:16",
    poster: "/videos/speaker-theory/poster.jpg",
    captions: "/videos/speaker-theory/captions.vtt",
    transcript: [
      "The same sentence, said by a different person — or heard on a different day — is a different sentence.",
      "What lands as a whisper from a peer can land as a siren from a manager.",
      "We are taught that communication is about choosing the right words. I spent years polishing the words. Turns out, the words are only half of it.",
      "I once told the team: “We need to tighten our project timeline.” One engineer heard: small adjustments. Another heard: we're in trouble — drop everything. Same words. Same meeting.",
      "And here's the part I learned the hard way. At a final perf review — with genuinely good results — I asked one question, out of pure curiosity: “Why is this number different from what we expected?”",
      "Over the next few days, team members found me, one by one, quietly asking what my real concern was. Whether I thought the project had failed. I didn't. I was just curious.",
      "But it was the performance review season. Everyone's sensitivity was turned all the way up. And my title meant my question left my mouth at volume 3 — and arrived at volume 10.",
      "That's the thing about titles: when your title changes, your default volume changes with it. A comment that used to be one opinion becomes the direction. You don't get to opt out of this.",
      "So here is my working theory: leadership communication is like adjusting a speaker's volume. The message isn't just the words — it's the words, times who you are, times where they are.",
    ],
    keyPoints: [
      "The message isn't just the words — it's the words, times who you are, times where they are.",
      "Most word problems are volume problems.",
    ],
    linkedinCaption:
      "Most word problems are volume problems.\n\nEp. 1 of Working Theory, on camera: why the same sentence lands as a whisper from a peer and a siren from a manager — and what changed when my title did.\n\nFull episode, transcript included, lives here first: https://haoqian.co/videos/speaker-theory",
    linkedinTags: ["WorkingTheory", "Leadership"],
    linkedinPublishedUrl:
      "https://www.linkedin.com/feed/update/urn:li:activity:7494997549993431040/",
  },
  {
    slug: "ai-throughput-shift",
    series: "working-theory",
    sequence: 2,
    title: "AI Throughput Shift",
    status: "published",
    publishedAt: "2026-08-18",
    language: "en",
    durationSeconds: 87,
    hook: "AI didn't make engineers faster. It changed the job.",
    summary:
      "The same size project: four engineers and four months in 2021, two engineers and one month last year — call it 8 to 16 times faster, with nobody working longer hours. What changed is what engineers actually do all day: less writing code, more reviewing, aligning and setting guardrails — the judgment work. Which leaves one management question: team structure, planning and growth paths were all designed for the old job — do they still match the job engineers are actually doing now?",
    videoUrl:
      "https://github.com/qianhaopower/hao-qian-advisory/releases/download/media/ai-throughput-shift.mp4",
    aspect: "9:16",
    poster: "/videos/ai-throughput-shift/poster.jpg",
    captions: "/videos/ai-throughput-shift/captions.vtt",
    transcript: [
      "Four engineers. Four months. That's what a project took us in 2021. Last year, my team shipped a project about the same size: two engineers, one month. Call it 8 to 16 times faster.",
      "Nobody worked longer hours. Nobody typed faster. What changed is what engineers actually do all day.",
      "In my team, engineers spend less of their day writing code, and more of it reviewing code, aligning requirements, and setting guardrails — the judgment work.",
      "One more thing changed. In 2021, if we needed a new framework, delivery slowed down while people went off and learned it. Nobody does that anymore. You learn it while you build. Same week. Same task.",
      "So here is my working theory: AI didn't make engineers faster. It changed the job.",
      "That's what I keep coming back to as a manager: my team's structure, my planning, the way engineers grow here — all of it was designed for the old job.",
      "So the question isn't “how much faster can we go.” It is: does the way I run this team still match the job my engineers are actually doing now?",
    ],
    keyPoints: [
      "AI didn't make engineers faster — it changed what engineers do all day: the judgment work of reviewing, aligning and setting guardrails.",
      "Team structure, planning and growth paths were designed for the old job — check they still match the job engineers are actually doing.",
    ],
    linkedinCaption:
      "Four engineers, four months — that was 2021. Two engineers, one month — last year. Same size project.\n\nEp. 2 of Working Theory, on camera: AI changed what engineers actually do all day — and most teams are still structured for the old job.\n\nFull episode + transcript: https://haoqian.co/videos/ai-throughput-shift\n\n#WorkingTheory #EngineeringLeadership",
    linkedinTags: ["WorkingTheory", "EngineeringLeadership"],
    linkedinPublishedUrl:
      "https://www.linkedin.com/feed/update/urn:li:activity:7495452142133080066/",
  },
  {
    slug: "retrain-the-model",
    series: "working-theory",
    sequence: 3,
    title: "Retrain the Model",
    status: "published",
    publishedAt: "2026-08-20",
    language: "en",
    durationSeconds: 106,
    hook: "You don't argue with a stale model. You retrain it.",
    summary:
      "LinkedIn locked Hao out for posting three times in ten minutes — its spam filter is a model trained on the old world's data, where no human writes that fast. But that morning the three posts were real: ideas argued out loud with AI as a sparring partner, work that used to take hours done in minutes. Orgs run on models like that filter too — approval chains, review cycles, meeting cadence, planning timelines, all trained on how fast a human used to work. You don't argue with a stale model; you retrain it.",
    videoUrl:
      "https://github.com/qianhaopower/hao-qian-advisory/releases/download/media/retrain-the-model.mp4",
    aspect: "9:16",
    poster: "/videos/retrain-the-model/poster.jpg",
    captions: "/videos/retrain-the-model/captions.vtt",
    transcript: [
      "LinkedIn locked me out for a bit a few months ago. My crime: posting three times in about ten minutes. The system looked at that and decided: “No human writes that fast. Must be a bot.”",
      "Here is what actually happened that morning. I had three ideas in my head. I talked them through with AI, by voice — thinking out loud, arguing back, rewriting as I went. The ideas were mine. The writing was mine. AI was a sparring partner.",
      "By the time I sat down, all three were ready to post. Work that used to take hours took minutes.",
      "The way I see it, LinkedIn's spam filter is a model — and every model is trained on the old world's data. In the old world, three real posts — three real posts in ten minutes — means a bot. So the model looked at me and said: “Broken.” But the model is what's broken down.",
      "And the models like this are everywhere. Your org runs on them, too. Approval chains, review cycles, meeting cadence, planning timelines — all trained on how fast a human used to work.",
      "So here is my working theory: the rules were trained on old data. AI just changed the data. You don't argue with a stale model — you retrain it.",
      "So which of your models is still running on old data?",
    ],
    keyPoints: [
      "Every rule in your org is a model trained on the old world's data — approval chains, review cycles, planning timelines all encode how fast a human used to work.",
      "AI changed the data. You don't argue with a stale model — you retrain it.",
    ],
    linkedinCaption:
      "LinkedIn locked me out for a bit a few months ago. My crime: posting three times in ten minutes.\n\nIts spam filter is a model trained on the old world's data. Your org runs on models like it too — approval chains, review cycles, planning timelines.\n\nEp. 3 of Working Theory, on camera: you don't argue with a stale model. You retrain it.\n\nFull episode + transcript: https://haoqian.co/videos/retrain-the-model\n\n#WorkingTheory #AI",
    linkedinTags: ["WorkingTheory", "AI"],
    linkedinPublishedUrl:
      "https://www.linkedin.com/feed/update/urn:li:activity:7496085419265142784/",
  },
  {
    slug: "iq-to-eq",
    series: "working-theory",
    sequence: 4,
    title: "IQ-to-EQ Career Weighting",
    status: "published",
    publishedAt: "2026-08-21",
    language: "en",
    durationSeconds: 87,
    hook: "Your career runs on two lines — IQ and EQ. Both rise. One rises faster.",
    summary:
      "Early on, IQ does the heavy lifting: problems land well-defined and the job is to solve them well. Then scope grows, problems arrive fuzzy, and the day fills with hard conflicts, trade-offs and conversations — EQ becomes proportionally more important, and keeps going. One hard meeting where everyone walks out aligned can save a team weeks; a few sentences in the room can turn it. The bigger your scope, the more the EQ line carries your career — which line have you been training?",
    videoUrl:
      "https://github.com/qianhaopower/hao-qian-advisory/releases/download/media/iq-to-eq.mp4",
    aspect: "9:16",
    poster: "/videos/iq-to-eq/poster.jpg",
    captions: "/videos/iq-to-eq/captions.vtt",
    transcript: [
      "Your career runs on two lines. The IQ line. And the EQ line. Both keep rising. But one rises faster.",
      "At the very start, IQ does the heavy lifting. As a junior, you get a lot of care from the seniors around you. Problems land on your desk well-defined. The job is to solve them well.",
      "Then the job changes. Scope gets bigger. Problems arrive fuzzy. You're working with people from very different backgrounds. Hard conflicts. Hard trade-offs. Hard conversations — daily.",
      "So IQ still matters. EQ just becomes, proportionally, more important. And it keeps going.",
      "The moment I realised this: one hard meeting, where everyone walks out actually aligned, can save my team weeks of work. Because alignment moves multiple teams in one direction. And inside that room, a few sentences can turn the whole meeting. That's all EQ playing.",
      "So here is my working theory: the weight keeps shifting. The bigger your scope, the more the EQ line carries your career.",
      "Worth checking your own two lines — which one have you been training?",
    ],
    keyPoints: [
      "Both lines keep rising; the EQ line rises faster as scope grows.",
      "One hard meeting that ends aligned can save a team weeks — that's EQ at work.",
    ],
    linkedinCaption:
      "One hard meeting, done well, can save a team weeks of work.\n\nEp. 4 of Working Theory, on camera: your career runs on two lines — IQ and EQ. Both rise. One rises faster.\n\nFull episode + transcript: https://haoqian.co/videos/iq-to-eq\n\n#WorkingTheory #CareerGrowth",
    linkedinTags: ["WorkingTheory", "CareerGrowth"],
    linkedinPublishedUrl:
      "https://www.linkedin.com/feed/update/urn:li:activity:7496420869465079808/",
  },
  {
    slug: "goldilocks-load",
    series: "working-theory",
    sequence: 5,
    title: "The Goldilocks Load",
    status: "published",
    publishedAt: "2026-08-22",
    language: "en",
    durationSeconds: 110,
    hook: "People grow at the Goldilocks load — a little more than they can carry today, light enough to recover from.",
    summary:
      "A good trainer adds five kilos to the bar — maybe ten, never twenty. Careers work the same way: the job is to keep finding the extra weight that's just right, whether that's a harder problem, a riskier deployment, one more team to align, or a project that runs months instead of weeks. One real example from Hao's team: an engineer who could coordinate inside the team and next door, given exactly one extra team beyond the org — on purpose, as a stretch — aligned them beautifully, and his range and Hao's trust grew together. Finding that weight, one person at a time, is most of the manager's job.",
    videoUrl:
      "https://github.com/qianhaopower/hao-qian-advisory/releases/download/media/goldilocks-load.mp4",
    aspect: "9:16",
    poster: "/videos/goldilocks-load/poster.jpg",
    captions: "/videos/goldilocks-load/captions.vtt",
    transcript: [
      "How do you grow a person on your team? Same way a good trainer grows you. They add five kilos to the bar. Maybe ten. Never twenty. Enough that you feel it. Light enough that you recover.",
      "Careers work the same way. The job is to keep finding the Goldilocks load — the extra weight that's just right. In a career, the extra weight comes in a few shapes: a harder technical problem, a riskier deployment, one more team to align, or a project that runs months instead of weeks.",
      "Get the load right, and the person steps out of their comfort zone, learns something new — and still feels neither stressed nor defeated.",
      "Here's one from my team. One engineer could already coordinate inside our team, and with the team next door. The next level: aligning teams beyond our org. So I set it up on purpose, as a stretch. One extra team beyond our org. Just one. He aligned them beautifully. And from that point on, his range grew — and so did my trust. Next time something like this comes up, it's his.",
      "So here is my working theory: people grow at the Goldilocks load. A little more than what they can carry today. Light enough to recover from. And finding that weight — again and again, one person at a time — that's most of the manager's job.",
    ],
    keyPoints: [
      "Add five kilos, never twenty: the extra weight that's just right.",
      "Finding that weight for each person, again and again, is most of the manager's job.",
    ],
    linkedinCaption:
      "A good trainer adds five kilos, never twenty. Growing people works the same way.\n\nEp. 5 of Working Theory, on camera: the Goldilocks load — a little more than someone can carry today, light enough to recover from. One real example from my team.\n\nFull episode + transcript: https://haoqian.co/videos/goldilocks-load\n\n#WorkingTheory #EngineeringManagement",
    linkedinTags: ["WorkingTheory", "EngineeringManagement"],
    linkedinPublishedUrl:
      "https://www.linkedin.com/posts/hao-qian-9ab0b04b_workingtheory-engineeringmanagement-ugcPost-7496899874139832323-bBRf/",
  },
  {
    slug: "attention-is-not-cheap",
    series: "working-theory",
    sequence: 6,
    title: "Attention Is Not Cheap",
    status: "published",
    publishedAt: "2026-08-22",
    language: "en",
    durationSeconds: 95,
    hook: "Information is cheap. Attention is not.",
    summary:
      "Text, video, documents — the carriers of information cost almost nothing to make now, and work is drowning in them. But the passage from seeing something to understanding it is as narrow as it has always been. Hao wrote a ten-page proposal with every edge case and every risk; his manager's feedback was “you lost me” — she cared, she just physically couldn't. The hard skill in the AI era runs both ways: presenting information at the right level of attention, and spending your own attention on the right information.",
    videoUrl:
      "https://github.com/qianhaopower/hao-qian-advisory/releases/download/media/attention-is-not-cheap.mp4",
    aspect: "9:16",
    poster: "/videos/attention-is-not-cheap/poster.jpg",
    captions: "/videos/attention-is-not-cheap/captions.vtt",
    transcript: [
      "Information is cheap. Attention is not.",
      "Text, video, documents — the carriers of information cost almost nothing to make now. We live in a world drowning in information. Certainly at work. But the passage from seeing something to understanding it — that passage is still narrow. As narrow as it's always been.",
      "Here is how I learned that. I recently wrote a proposal. Ten pages. Every edge case. Every risk — with a mitigation plan for each. I didn't write a proposal. I wrote a mini book.",
      "My manager's feedback: “Too much detail. It is diluting your point. You lost me.” And she was right. She cared. She just physically couldn't. I drowned her in detail. I asked for attention that nobody can afford. The proposal didn't pass.",
      "So here is my working theory: the hard skill in the AI era runs both ways — presenting information at the right level of attention, and spending our own attention on the right information. Information will keep getting cheaper. Attention stays scarce.",
      "So, honest question: what's the longest document you ever sent that nobody actually read?",
    ],
    keyPoints: [
      "The passage from seeing to understanding is as narrow as it has always been.",
      "The hard skill runs both ways: present at the right level of attention, and spend your own attention on the right information.",
    ],
    linkedinCaption:
      "Information is cheap. Attention is not.\n\nEp. 6 of Working Theory, on camera: I wrote a ten-page proposal with every edge case and every risk. My manager's feedback: \"You lost me.\" She was right.\n\nFull episode + transcript: https://haoqian.co/videos/attention-is-not-cheap\n\n#WorkingTheory #Leadership",
    linkedinTags: ["WorkingTheory", "Leadership"],
    linkedinPublishedUrl:
      "https://www.linkedin.com/feed/update/urn:li:activity:7497600638604750848/",
  },
  {
    slug: "html-is-the-new-english",
    series: "working-theory",
    sequence: 7,
    title: "HTML Is The New English",
    status: "published",
    publishedAt: "2026-08-22",
    language: "en",
    durationSeconds: 86,
    hook: "HTML is the new English.",
    summary:
      "A few years ago even a simple web page took real skill; that barrier is gone. Anyone can describe what they want to an agent and get back an animated page with diagrams, formatting, video and sound. At work, people are building pages instead of sending long docs — pulling the data together, connecting the dots in diagrams, animating it. The downside is real (version control, commenting on a sentence); the upside is that you see it in a way a static page never showed you. Present your information in ways you couldn't imagine before — expand your vocabulary to code.",
    videoUrl:
      "https://github.com/qianhaopower/hao-qian-advisory/releases/download/media/html-is-the-new-english.mp4",
    aspect: "9:16",
    poster: "/videos/html-is-the-new-english/poster.jpg",
    captions: "/videos/html-is-the-new-english/captions.vtt",
    transcript: [
      "HTML is the new English.",
      "A few years ago, producing code — even a simple web page — took real skill. That barrier is gone. Today anyone can open a laptop, describe to an agent what they want, and get a page with diagrams, rich formatting, colour, video, sound — a beautiful animated page they can present.",
      "English is still better at some things. But the ways we can communicate asynchronously just expanded — exponentially. Because now, anyone can make HTML.",
      "Here is what I see at work. We write a lot of internal doc pages. Long ones. Now, more and more, instead of sending a doc, people build a page. They pull data all together. They connect the dots in diagrams. They animate it. And they send you that.",
      "The downside is real. You lose version control. You lose commenting on sentences. The upside: you see it. In a way a static page could never show you.",
      "So here is my working theory: present your information in ways you could not imagine before. Expand your vocabulary to code.",
    ],
    keyPoints: [
      "The barrier to making code is gone — anyone can make HTML now.",
      "Expand your vocabulary to code: present information in ways a static page never could.",
    ],
    linkedinCaption:
      "HTML is the new English.\n\nEp. 7 of Working Theory, on camera: the barrier to making code is gone — so people are sending animated pages instead of long documents, and communication just got a new vocabulary.\n\nFull episode + transcript: https://haoqian.co/videos/html-is-the-new-english\n\n#WorkingTheory #AI",
    linkedinTags: ["WorkingTheory", "AI"],
    linkedinPublishedUrl:
      "https://www.linkedin.com/feed/update/urn:li:activity:7498694264994820096/",
  },
  {
    slug: "good-work-doesnt-speak",
    series: "working-theory",
    sequence: 8,
    title: "Good Work Doesn't Speak",
    status: "published",
    publishedAt: "2026-08-29",
    language: "en",
    durationSeconds: 97,
    hook: "Many new managers believe good work speaks for itself. It doesn't.",
    summary:
      "You solved a serious cross-department problem — and everyone else saw one small task. In a large company people see only a compressed version of reality: each leader holds one fragment, nobody sees the whole system. So fixing the problem is only step one; the real job is converting the value you created into organizational memory — in the right forum, explain what broke, why it mattered, what changed, and why it won't happen again. That's not exaggerating the impact; it's making the full picture visible. The trust it earns becomes the capital for the next, bigger problem.",
    videoUrl:
      "https://github.com/qianhaopower/hao-qian-advisory/releases/download/media/good-work-doesnt-speak.mp4",
    aspect: "9:16",
    poster: "/videos/good-work-doesnt-speak/poster.jpg",
    captions: "/videos/good-work-doesnt-speak/captions.vtt",
    transcript: [
      "Have you ever done something that is really difficult — and watched everyone treat it like it was easy? You solved a serious cross-department problem. But everyone else saw one small task.",
      "Many new managers believe good work speaks for itself. It doesn't. And this isn't about bragging.",
      "In large companies, people see only a compressed version of reality from a few sources. You understand the dependencies, the escalations, and the root causes. But each leader sees only one fragment. Nobody sees the whole system.",
      "Fixing the problem is only the first step. You also need to convert the value you created into organizational memory. In the right forum, explain what broke, why it mattered, what changed, and why it won't happen again.",
      "You are not exaggerating the impact. You are making the full picture visible.",
      "When the organization understands and remembers your impact, you earn trust. The trust becomes the capital to solve the next, bigger problem. You grow. And your team grows with you.",
    ],
    keyPoints: [
      "Each leader sees one fragment of what you did; nobody sees the whole system — good work cannot speak for itself.",
      "Convert the value into organizational memory: what broke, why it mattered, what changed, why it won't happen again.",
    ],
    linkedinCaption:
      "Many new managers believe good work speaks for itself. It doesn't.\n\nEp. 8 of Working Theory, on camera: in a large company every leader sees one fragment of what you did. Fixing the problem is step one — converting it into organizational memory is the real job.\n\nFull episode + transcript: https://haoqian.co/videos/good-work-doesnt-speak\n\n#WorkingTheory #EngineeringLeadership",
    linkedinTags: ["WorkingTheory", "EngineeringLeadership"],
  },
  {
    slug: "self-assessment",
    series: "working-theory",
    sequence: 11,
    title: "Self-Assessment",
    status: "published",
    publishedAt: "2026-08-31",
    language: "en",
    durationSeconds: 135,
    hook: "By the time you write your self-assessment, it's too late to tell a new story.",
    summary:
      "The first unscripted episode — spoken freely, no teleprompter. The common self-assessment mistake is telling a new story and hoping your manager digs in; but a manager recalls a whole cycle of perceived reality before your document ever lands. Anything completely new is a risk: unseen work, invisible impact, or worse. The fix runs through the whole cycle — use every one-on-one to present your impact, the data you changed, the needle you moved, so the self-assessment becomes a summary of a reality you already share.",
    videoUrl:
      "https://github.com/qianhaopower/hao-qian-advisory/releases/download/media/self-assessment.mp4",
    aspect: "9:16",
    poster: "/videos/self-assessment/poster.jpg",
    captions: "/videos/self-assessment/captions.vtt",
    transcript: [
      "Today, I'm going to talk about self-assessments. Everybody knows self-assessments is really important in terms of performance management. Basically, it's a piece of document that you officially present to your manager: what you have done in this performance cycle.",
      "However, a common mistake a lot of people make is: create a new story in their self-assessment, in the hope of your manager is going to actually dig into the new story during the performance management cycle. It's not the best way.",
      "Because essentially, your manager is really trying to recall their perceived reality during the whole cycle, even before your self-assessment landed in his or her desk. Essentially, you are trying to present information to match with the reality that is already in your manager's mind.",
      "If you present something that is completely new — that is a risk. It's either: you've done something, but it's never in your manager's eye, or the impact is not in your manager's view — which is a problem. Or you are fabricating something — which is even worse.",
      "So the best way to make sure your impact is really in your manager's mind is: during all of the one-on-ones across the whole performance management cycle — being six months, or being a whole year — using all the one-on-ones to present your impact, to present the data you changed, to present the needle you moved.",
      "Only when you are doing those things, your manager will have a shared reality with you of what you have actually changed. And then your self-assessment will become a summary view of what's already in your manager's head. And that is the best way to making sure your self-assessment landed in the right way.",
      "Hope this helps.",
    ],
    keyPoints: [
      "A self-assessment that tells a new story is a risk — your manager already holds a cycle's worth of perceived reality.",
      "Use every one-on-one to build shared reality; the self-assessment should only be its summary.",
    ],
    linkedinCaption:
      "By the time you write your self-assessment, it's too late to tell a new story.\n\nWorking Theory, on camera — unscripted this time: your manager recalls a whole cycle of perceived reality. Build the shared reality in your one-on-ones, and let the self-assessment be the summary.\n\nFull episode + transcript: https://haoqian.co/videos/self-assessment\n\n#WorkingTheory #PerformanceReview",
    linkedinTags: ["WorkingTheory", "PerformanceReview"],
  },
  /* ------------------------------------------------------------------ */
  /* Friends Intelligence · 中文 · 小红书                                 */
  /* Captions and transcripts are Hao's spoken words (voice-first, no    */
  /* teleprompter), proofread from the CapCut caption track; punctuation */
  /* and paragraphs added for reading. Video = the CapCut export on the  */
  /* media shelf; poster = the designed frame-1 cover baked into it.     */
  /* ------------------------------------------------------------------ */
  {
    slug: "fi-sleep-daylight",
    series: "friends-intelligence",
    sequence: 1,
    title: "晚上睡不着，先改早上这一件事",
    titleEn: "Morning daylight: the sleep fix that starts at sunrise",
    status: "published",
    publishedAt: "2026-08-30",
    language: "zh-Hans",
    durationSeconds: 244,
    topic: "睡眠智慧 · Sleep Intelligence",
    hook: "起床第一时间让眼睛见到天光，大脑才开始计时。",
    summary:
      "睡不好的人，问题往往出在睁眼后的头两小时：大脑靠自然光判断“一天开始了”，看到天光才开始倒数十六小时的清醒时间。七点醒、九点才见光，大脑就要到凌晨一点才困。把昼夜节律的账算清楚，再给一个作弊技巧：模仿天光的灯。",
    videoUrl:
      "https://github.com/qianhaopower/hao-qian-advisory/releases/download/media/fi-sleep-daylight.mp4",
    aspect: "9:16",
    poster: "/videos/fi-sleep-daylight/poster.jpg",
    captions: "/videos/fi-sleep-daylight/captions.vtt",
    transcript: [
      "今天我们跟大家分享一个睡好觉的小窍门。最近有很多朋友跟我说呀，睡眠是越来越不好——不管是工作压力大呀，还是学习太紧张啊，还是带孩子太累呀，总之就是睡得不太好，对吧？有时候晚上还醒，醒完了以后呢也睡不着，第二天比较累。我跟很多朋友都说了，这个小窍门真的很有用。",
      "这个小窍门是什么呢？你早上起来以后，眼睛尽早地接触天光。什么叫天光？就是说自然界的光，对吧。最好的办法就是说走出去，散个步走一会儿；不过你要是不想走呢，在自己的后院子里——如果要是有的话——做一些运动也好，或者是做一些什么事情也好。",
      "为什么说眼睛接触天光是一个小窍门呢？这个就是因为呀，我们的人脑它是几百万年进化的产物，它是通过自然界的信号来判断自己的昼夜节律的。我们几百万年来进化，从以前还没有进化到人的这个过程中开始，一直到现在，生物体就是有了松果体，大脑有了这套机制以后的话，都是从眼睛开始接触自然界的光线作为一天开始的信号——昼夜节律开始变成“昼”。那么人一天差不多，在“昼”的过程中达到一定的时间，比如说12到16小时，或者16到18小时——可能每个生物的情况不太一样——就要开始睡觉了。那么你这个“昼”的起点是什么，就决定了你晚上什么时候困。",
      "所以说你眼睛接触天光以后的话，就相当于是告诉你大脑：从现在开始计时，对吧。如果我们接触天光比较晚——假如说你7点醒了，然后被窝里边划手机干一些别的，你9点出去上班的时候，或者说是出门的时候眼睛看到了天光——那个就相当于是说你脑子从9点开始才计时。那假如说你一天需要睡8小时，你清醒的时间差不多是16小时，9加16等于25，那你就晚上到25点——就是你第二天的凌晨1点——你的大脑才开始变困。那你自然晚上12点还睡不着觉，对不对？",
      "那有人会问我说：我要接触天光，我根本就没有这个条件，对吧？我没有时间早上出去运动，或者是我做不到，那怎么办呢？有一个 shortcut，就是有一个作弊的技巧，就是买一种模仿自然光线的这种灯。你可以网上搜一下——我不是打广告，就是说你随便找一下有这种灯。这种灯它是什么呢？它的光线是极化的，就是全极化，就是 polarize。因为我们现在这些普通的灯的话，它是属于各种偏振光，它的光的极化的话只是一部分，它没有所有成分的光。那天光为什么好呢？是因为它所有成分的光是全的，这样的话你大脑才能真正接受到一天开始的信号。那么设计这些灯的人呢，他就会知道说，我们要尽量模仿太阳的这个情况，对吧。我有一些同事，他就是买的这种模仿天光的灯，然后呢早上刷牙的时候，打开灯对着这个灯刷牙，可能几分钟，但他的睡眠就会有改善。",
      "所以说我就把这个分享在这里。有些朋友也可以去看我的书，里面会讲得更多一些。所以说希望可以帮到大家。",
    ],
    keyPoints: [
      "眼睛见到天光的那一刻，大脑才开始给这一天计时。",
      "9 + 16 = 25：见光越晚，困意来得越晚。",
    ],
    platformCaption:
      "起床第一时间让眼睛见到天光，大脑才开始计时。\n道理和做法都在视频里，包括一个作弊技巧。\n\n#睡眠 #失眠 #睡眠质量 #昼夜节律 #健康生活 #自我提升",
    platformTags: ["睡眠", "失眠", "睡眠质量", "昼夜节律", "健康生活", "自我提升"],
  },
  {
    slug: "fi-coffee",
    series: "friends-intelligence",
    sequence: 2,
    title: "下午一杯咖啡，晚上凭什么睡不着",
    titleEn: "Caffeine, adenosine, and the eight-hour rule",
    status: "published",
    publishedAt: "2026-08-31",
    language: "zh-Hans",
    durationSeconds: 165,
    topic: "睡眠智慧 · Sleep Intelligence",
    hook: "咖啡因和困意分子腺苷长得像双胞胎，占了大脑的座位，你就“以为”自己不困。",
    summary:
      "咖啡为什么提神：咖啡因分子和腺苷长得几乎一样，抢先和大脑的受体结合，腺苷排不上号，大脑就以为自己不困。代谢一轮要八小时——想十一点睡着，下午三点就是最后一杯。",
    videoUrl:
      "https://github.com/qianhaopower/hao-qian-advisory/releases/download/media/fi-coffee.mp4",
    aspect: "9:16",
    poster: "/videos/fi-coffee/poster.jpg",
    captions: "/videos/fi-coffee/captions.vtt",
    transcript: [
      "今天我们来接着讲一讲怎么睡个好觉。我们今天来讲一讲咖啡，或者说是含咖啡因的饮料——比如说茶呀，甚至一些巧克力和这些零食里面有咖啡因。那咖啡因到底是怎么影响我们的睡眠的？",
      "就是咖啡因的话，它这个分子——咖啡因的 molecule——它是和一个叫腺苷的一种 molecule 是很像的。这个腺苷如果你要理解的话，就是如果你要记得的话，就是三磷酸腺苷 ATP，也就是我们高中生物课中学的那种腺苷。咖啡因的分子和腺苷的分子它长得很像。",
      "我们人的头脑中有一套机制，就是说人脑不停地在监测腺苷的浓度，来决定你到底有多困：腺苷的浓度越高，你就会越困。那我们在清醒的状态下，人脑是一直在生产腺苷的，那它的浓度就会自然越来越高。那攒到一定程度——一般是到了晚上——这个值达到了顶峰以后的话，我们就会非常的困。",
      "但是我们刚才说过，咖啡因这个分子和腺苷的分子结构非常相似，所以说咖啡因的分子在人脑中达到一个浓度以后，它就顶替了腺苷，和人脑的受体结合在一起了。你就可以理解这是人脑的受体，咖啡因分子来了以后就结合，那么腺苷就没有机会再和这些受体结合，那就会造成大脑以为自己不困。这就是为什么咖啡会提神。",
      "那么具体说我们怎么样用这个知识来让自己睡个好觉呢？就是说记住咖啡的代谢时间大约是8个小时——正常人脑、普通成年人。所以就是说，如果你要是晚上打算11点睡觉，那么11减8就是3，那就是说下午3点以后，你不要再喝含有咖啡因的饮料或者是食物之类的。这样的话就会比较安全地把你体内的咖啡因代谢掉。这些咖啡因没了以后的话，这些受体会打开，那么腺苷就会有机会结合这个受体，那会让你知道：原来我困了。",
      "好吧，这就是今天的关于怎么睡觉的一个方法。",
    ],
    keyPoints: [
      "咖啡因不是给你充电，是挡住了“我困了”这个信号。",
      "11 − 8 = 3：想几点睡，往前推八小时就是最后一杯。",
    ],
    platformCaption:
      "咖啡因和困意分子腺苷长得像双胞胎，占了大脑的座位，你就“以为”自己不困。\n代谢要8小时：11点睡觉，下午3点就是最后一杯。\n\n#睡眠 #咖啡 #咖啡因 #失眠 #健康生活 #科普",
    platformTags: ["睡眠", "咖啡", "咖啡因", "失眠", "健康生活", "科普"],
  },
  {
    slug: "fi-dim-lights",
    series: "friends-intelligence",
    sequence: 3,
    title: "晚上总睡不好，睡前一小时先关大灯",
    titleEn: "Dim the lights: melatonin, blue light, and the hour before bed",
    status: "published",
    publishedAt: "2026-09-02",
    language: "zh-Hans",
    durationSeconds: 228,
    topic: "睡眠智慧 · Sleep Intelligence",
    hook: "睡前一到两小时把灯调暗，松果体才开始分泌褪黑素。",
    summary:
      "天光讲的是一天的起点，这一集讲终点：睡前一两个小时逐渐调暗房间，松果体才会分泌褪黑素——脑白金模拟的正是这个过程。眼睛对蓝光最敏感，所以暖灯优先、屏幕少看；真能做到睡前不碰手机，改善是立竿见影的。",
    videoUrl:
      "https://github.com/qianhaopower/hao-qian-advisory/releases/download/media/fi-dim-lights.mp4",
    aspect: "9:16",
    poster: "/videos/fi-dim-lights/poster.jpg",
    captions: "/videos/fi-dim-lights/captions.vtt",
    transcript: [
      "我们再来分享一个怎样睡好觉的小窍门。我们上一次说到，早上起来以后的话，眼睛尽早地接触天光——就是这个自然光——是可以让我们睡觉更好，是因为我们的昼夜节律会进入一个比较好的节奏。那么今天的小窍门就是，在晚上睡觉之前的一两个小时，怎样做可以更加加强我们睡眠的节奏。",
      "这个小窍门其实很简单，就是在睡前的一到两个小时，逐渐把你房间的光减暗。并不是说让你一点一点减暗，就是说你十点半、十一点睡觉，那么从九点半开始，你就可以把大灯关上，开几个小灯，甚至是说把大灯调暗一些，对吧，就整体在一个比较暗的环境之下。",
      "为什么要这样做呢？是因为我们的大脑，尤其是松果体 Pineal Gland，它在工作的过程中呢，它是根据这个光线来调节它分泌激素——就是这个褪黑素 Melatonin——的含量的。它在光很强的时候的话，它的分泌是不旺盛的；在光线弱的时候的话，它就相当于是告诉大脑说：我们天黑了，要睡觉，分泌褪黑素，对吧。以前我们记得有一段时间，脑白金好像很火，它其实就是在模拟人脑这个过程——脑白金里边很重要的一个成分，就是褪黑素。所以说我们光线调暗以后呢，实际上就是给我们的松果体创造了一个条件，让它有充分的环境来分泌褪黑素，我们可以去好好地睡觉。",
      "还有一个点呢，就是说人脑——它是这个眼睛，或者说是眼睛背后一直到人脑这一套系统——它对蓝光是非常敏感的。背后的原理就是说，因为蓝光含的能量最高，对吧；如果我们高中物理还记得的话，就是说同样强度的光，红光其实比蓝光含的能量要少。所以就是说我们的眼睛对蓝光很敏感，所以就是说，你不要让你睡前的环境中有特别强的这种蓝色光源。那其实你看你的电脑的话，你也可以注意到，有时候它会说这种 Night Shift，就是夜间工作模式，对吧，实际上它就是把蓝光的成分降低，就是有助于让你更好地进入一种睡眠的状态。所以说如果晚上你要有灯的话，千万是这种暖色的灯，或者说最起码是白色的灯，不要是那种很亮的、像酒吧那种蓝色的灯，这个是对你睡眠是有好处的。",
      "当然还有最重要的：什么蓝光最多呢？屏幕的蓝光很多，对吧。就算你是用 Night Shift 的手机，电脑，这些蓝光都很多。所以说如果可能的话，睡前一到两个小时不玩手机——可能很难，少玩手机，对吧。如果你要是真能做到不玩手机，你会发现你的睡眠会有立竿见影的效果，立竿见影的改善，对吧。",
      "那今天我们就再分享一个睡前光线对人脑的作用、来改善睡眠的一个小窍门。",
    ],
    keyPoints: [
      "褪黑素不是买来吃的，是关灯关出来的。",
      "蓝光能量最高、眼睛最敏感：暖灯优先，屏幕能少看就少看。",
    ],
    platformCaption:
      "睡前一到两小时把灯调暗，松果体才开始分泌褪黑素。\n蓝光最提神：暖灯优先，屏幕能少看就少看。\n\n#睡眠 #失眠 #褪黑素 #蓝光 #睡眠质量 #健康生活",
    platformTags: ["睡眠", "失眠", "褪黑素", "蓝光", "睡眠质量", "健康生活"],
  },
  {
    slug: "fi-temperature",
    series: "friends-intelligence",
    sequence: 4,
    title: "晚上翻来覆去睡不着，先把卧室调低两度",
    titleEn: "Half a degree cooler: room temperature and the hot-shower paradox",
    status: "published",
    publishedAt: "2026-09-03",
    language: "zh-Hans",
    durationSeconds: 207,
    topic: "睡眠智慧 · Sleep Intelligence",
    hook: "睡眠时体温要比白天低 0.5°C，降不下去就翻来覆去。",
    summary:
      "身体入睡时平均体温要比白天低半度，降温和睡好觉互为因果；屋里一热，身体想降却降不下去，就辗转反侧。两招：卧室比平时低两度；睡前洗个热水澡——毛细血管扩张散热，先热后凉，反而更快进入低温状态。",
    videoUrl:
      "https://github.com/qianhaopower/hao-qian-advisory/releases/download/media/fi-temperature.mp4",
    aspect: "9:16",
    poster: "/videos/fi-temperature/poster.jpg",
    captions: "/videos/fi-temperature/captions.vtt",
    transcript: [
      "我们接着来分享睡眠智慧。今天我们来说一说温度。这个睡好觉的一个小窍门，就是房间的温度要稍微低一点——不是说让你非常冻得难受那种温度低，而是说在你平时适应的房间的温度下，略微稍微低一点点。比如说你平时待在22度的房间比较舒服，那你睡觉的时候的话，可以适当地把房间调成20度，甚至19度都是可以的。",
      "为什么呢？是因为我们整个人体在睡眠的时候，身体的平均温度要比你白天的平均温度差不多低0.5摄氏度。也就是说，体温低0.5摄氏度和睡一个好觉，它实际上是一个互为因果的关系：就是说你身体只有能进入这种比白天低0.5摄氏度的状态，你才会睡得比较好；你睡得好的时候，你身体会进入一个很稳定、代谢比较低的一个修复的过程，那么它的温度也会降低。所以说它是一个互为因果的过程。这个也就解释了为什么我们有的时候屋里有一些热，就会所谓辗转反侧睡不着觉——就是因为我们的身体会非常努力地想进入这种比平时低0.5摄氏度的状态，但是它进入不了那种状态，所以就不好睡着。",
      "那具体怎么做，就是让自己达到这种微微凉爽的状态呢？除了可以把我们房间的温度通过空调啊，或者说一些其他的制冷设施，稍微调低一点以外的话，还有一个很简单的办法，就是说睡前洗一个热水澡。这个听着好像有点奇怪：说为什么洗一个热水澡，反而身体会降温呢？这就是因为我们洗澡的时候水比较热，会让我们整个身体的毛细血管呢——尤其是这个末梢的毛细血管，手啊脚啊这些——扩张。扩张以后的毛细血管它是一个散热的过程，就像这个暖气的散热片一样。那散热的过程的话，你洗完澡它还会继续持续，所以说就会在你洗完澡的时候很快地带走一些热量，让你的身体更快地、更容易地进入这种比平时低0.5摄氏度的状态。所以这就是为什么人们说洗个热水澡容易睡一个好觉——就是通过降温的过程。当然洗热水澡还有其他作用，比如说放松肌肉啊，比如说加速一些乳酸的分解啊，那我们就不在这个温度这块讲了。",
      "所以呢，今天就把关于体温和睡觉、房间温度和睡觉的这个关系分享给大家。",
    ],
    keyPoints: [
      "入睡的秘密：身体要先降 0.5 度。",
      "热水澡助眠，靠的是洗完以后的散热，不是热本身。",
    ],
    platformCaption:
      "睡眠时体温要比白天低0.5°C，降不下去就翻来覆去。\n两招：卧室调低两度；睡前洗个热水澡——血管扩张散热，先热后凉。\n\n#睡眠 #失眠 #睡眠质量 #热水澡 #健康生活 #科普",
    platformTags: ["睡眠", "失眠", "睡眠质量", "热水澡", "健康生活", "科普"],
  },
  {
    slug: "fi-couple-20min",
    series: "friends-intelligence",
    sequence: 6,
    title: "夫妻之间这件事，每天都应该做",
    titleEn: "Twenty undistracted minutes a day",
    status: "published",
    publishedAt: "2026-09-05",
    language: "zh-Hans",
    durationSeconds: 193,
    topic: "关系智慧 · Relationship Intelligence",
    hook: "每天 20 分钟，不看手机、不聊家务，只把注意力给对方。",
    summary:
      "夫妻每天在一起的时间很多，但吃饭、躺着刷手机、靠在沙发上看电视，并不会自动变成真正的交流。手机、工作、孩子、账单给脑子套上一层枷锁，要有意识地每天空出二十分钟打破它。脑科学的底子是一句话：越了解，越喜欢——To know is to love。",
    videoUrl:
      "https://github.com/qianhaopower/hao-qian-advisory/releases/download/media/fi-couple-20min.mp4",
    aspect: "9:16",
    poster: "/videos/fi-couple-20min/poster.jpg",
    captions: "/videos/fi-couple-20min/captions.vtt",
    transcript: [
      "夫妻之间这件事，每天都应该做。只要你坚持做这件事，那么你们的夫妻关系会非常的好。这件事是什么呢？很简单，就是每天有20分钟不受打扰的交流的时间。",
      "夫妻之间每天都会花很多时间在一起：一起吃饭啊，躺着聊会天啊，靠在沙发上看会电视啊。但是这个时间并不是自然而然地就会转化成真正有效的交流时间。我们可以回想一下，我们上次真的和自己的爱人——太太、先生、男朋友、女朋友——在一起，不受打扰地、真正地把自己的注意力给对方的时间。所以说20分钟听着感觉不是很长，实际上是一个需要你真正值得认真去做才能做到的事情。",
      "为什么我们这20分钟这么难做到呢？是因为我们的生活有太多的打扰了，distractions：手机无限多好玩的事情，工作上的烦恼，安排孩子的事情，买菜做饭、安排假期，水电煤气账单，下周老板的期待。这些事情无时不刻地都会给我们脑子套上一层枷锁。我们真正要让夫妻之间的关系维持在一个很好的状态，就是你要有意识地去每天空出一些时间来打破这些枷锁，真正地去和你的太太、先生、男朋友、女朋友交流：问一问你最近在想什么事情，有什么事情是你比较开心的，有什么事情是你比较在意的；你也说一说你自己的事情。",
      "其实这个是有生理学、或者说是生物学上的脑科学的背景，就是我们的人脑越了解一个东西或者是一个人，我们就会越喜欢他。所以说有一句话叫做 To know is to love，就是说我知道得越多，我会越喜欢——知道和喜欢和爱，它是相关的事情，这个是有脑科学基础的。",
      "所以说每天我们给我们的伴侣安排20分钟不受打扰的时间，是真真正正地在为你们的爱情提高温度。",
    ],
    keyPoints: [
      "在一起的时间不等于交流的时间。",
      "越了解，越喜欢：知道、喜欢和爱是相关的。",
    ],
    platformCaption:
      "坚持做，夫妻关系会非常好。\n不是你想的那件事。\n是每天20分钟——不看手机、不聊家务，只把注意力给对方。\n脑科学有句话：越了解，越喜欢。\n\n#夫妻关系 #婚姻 #情感 #两性关系 #沟通 #恋爱",
    platformTags: ["夫妻关系", "婚姻", "情感", "两性关系", "沟通", "恋爱"],
  },
];
