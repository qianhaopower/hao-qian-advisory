"use client";

import { useRef } from "react";
import { track } from "@/lib/analytics";

/*
 * A plain <video> that tells the counter how far a film was really watched.
 * GA's own video tracking only understands YouTube embeds, so the library's
 * self-hosted films report here:
 *
 *   video_start     the first play
 *   video_progress  25 / 50 / 75 — the share of the film actually PLAYED
 *                   (the browser's `played` ranges), so dragging the scrubber
 *                   to the end does not count as watching
 *   video_complete  the film reached its end
 *
 * Each fires once per page view.
 */

const MARKS = [25, 50, 75];

type Props = React.ComponentProps<"video"> & {
  ga: { slug: string; series: string; title: string };
};

function playedPercent(v: HTMLVideoElement): number {
  if (!v.duration || !Number.isFinite(v.duration)) return 0;
  let seconds = 0;
  for (let i = 0; i < v.played.length; i++) {
    seconds += v.played.end(i) - v.played.start(i);
  }
  return (seconds / v.duration) * 100;
}

export function TrackedVideo({ ga, children, ...props }: Props) {
  const sent = useRef<Set<string>>(null);

  const once = (key: string, event: string, v: HTMLVideoElement, percent?: number) => {
    sent.current ??= new Set();
    if (sent.current.has(key)) return;
    sent.current.add(key);
    track(event, {
      slug: ga.slug,
      series: ga.series,
      video_title: ga.title,
      video_provider: "haoqian.co",
      video_url: v.currentSrc,
      video_duration: Number.isFinite(v.duration) ? Math.round(v.duration) : undefined,
      video_percent: percent,
    });
  };

  return (
    <video
      {...props}
      onPlay={(e) => once("start", "video_start", e.currentTarget)}
      onTimeUpdate={(e) => {
        const v = e.currentTarget;
        const pct = playedPercent(v);
        for (const m of MARKS) {
          if (pct >= m) once(`p${m}`, "video_progress", v, m);
        }
      }}
      onEnded={(e) => once("end", "video_complete", e.currentTarget, 100)}
    >
      {children}
    </video>
  );
}
