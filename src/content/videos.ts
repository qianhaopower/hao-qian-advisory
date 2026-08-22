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
];
