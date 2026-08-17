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
   * Final video. Either a file URL (.mp4/.webm — local /videos/... path or
   * CDN) rendered as a native player, or a YouTube/Vimeo embed URL rendered
   * as an iframe. Omit while the episode is in production.
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
    videoUrl: "/videos/speaker-theory/final.mp4",
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
];
