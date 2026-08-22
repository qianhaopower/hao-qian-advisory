/*
 * Video episodes — the library's on-camera work.
 *
 * Same philosophy as the rest of the library: the website is the canonical
 * home; platforms (LinkedIn first) are distribution. Adding an episode =
 * adding one entry to EPISODES below. No CMS, ever.
 *
 * Series are configurable so a second line (e.g. a Friends Intelligence
 * series for Xiaohongshu/Instagram) can be added later without touching
 * page code — but only the Working Theory line exists today.
 *
 * Draft episodes: status "draft" keeps an episode OUT of the index page,
 * home, search, sitemap and structured data, and its page is noindex —
 * but the page still builds, so Hao can preview it at its future URL
 * before flipping status to "published".
 */

export type VideoSeriesId = "working-theory";

export type VideoSeries = {
  id: VideoSeriesId;
  /** Display name — matches the naming used across the library. */
  name: string;
  /** Short qualifier distinguishing the video line from the essay line. */
  form: string;
  description: string;
  /** Where episodes are distributed after publishing here first. */
  platform: string;
};

export const VIDEO_SERIES: Record<VideoSeriesId, VideoSeries> = {
  "working-theory": {
    id: "working-theory",
    name: "Working Theory",
    form: "On camera",
    description:
      "The theory series, spoken — one idea per episode, face to camera, published here first and distributed on LinkedIn.",
    platform: "LinkedIn",
  },
};

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
  /** LinkedIn publishing package (manual publishing, Phase 1). */
  linkedinCaption?: string;
  linkedinTags?: string[];
  /** Filled in AFTER publishing natively on LinkedIn. */
  linkedinPublishedUrl?: string;
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
  },
];
