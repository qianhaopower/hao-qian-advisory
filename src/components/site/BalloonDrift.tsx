"use client";

import { useEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";

/*
 * The balloon room's quiet easter egg — same spirit as the Fish Fun cast:
 * reach the end of the shelf and a small bunch of balloons drifts up the
 * page, once. Reuses the wordmark egg's rise/sway keyframes and palette;
 * skipped entirely under prefers-reduced-motion.
 */

export type Balloon = {
  id: number;
  left: number; // vw %
  size: number; // px
  color: string;
  duration: number; // s
  delay: number; // s
  sway: number; // px
  swayDur: number; // s
};

const COLORS = ["#C96A5A", "#D9A441", "#7BA37E", "#6E88B0", "#B08BC0", "#D98A9E"];

/** A fresh bunch of balloons — shared by this room and the /today deck. */
export function makeBalloons(n = 6): Balloon[] {
  return Array.from({ length: n }, (_, i) => ({
    id: i,
    left: 8 + Math.random() * 84,
    size: 24 + Math.random() * 18,
    color: COLORS[i % COLORS.length],
    duration: 5.5 + Math.random() * 2.5,
    delay: i * 0.45 + Math.random() * 0.3,
    sway: 12 + Math.random() * 18,
    swayDur: 1.6 + Math.random(),
  }));
}

/** How long a bunch stays on screen, in ms. */
export function balloonLife(batch: Balloon[]): number {
  return Math.max(...batch.map((b) => (b.duration + b.delay) * 1000)) + 200;
}

/** The balloons themselves, drifting up over the whole page. */
export function BalloonSky({ balloons }: { balloons: Balloon[] }) {
  if (balloons.length === 0) return null;
  return createPortal(
    <div
      className="pointer-events-none fixed inset-0 z-40 overflow-hidden"
      aria-hidden="true"
    >
      {balloons.map((b) => (
        <div
          key={b.id}
          className="balloon-rise absolute bottom-[-90px]"
          style={{
            left: `${b.left}vw`,
            animationDuration: `${b.duration}s`,
            animationDelay: `${b.delay}s`,
          }}
        >
          <div
            className="balloon-sway flex flex-col items-center"
            style={{
              animationDuration: `${b.swayDur}s`,
              ["--sway" as string]: `${b.sway}px`,
            }}
          >
            <div
              style={{
                width: b.size,
                height: b.size * 1.18,
                background: b.color,
                borderRadius: "50% 50% 48% 48% / 55% 55% 45% 45%",
                opacity: 0.9,
              }}
            />
            <div className="h-[26px] w-px bg-faint opacity-60" />
          </div>
        </div>
      ))}
    </div>,
    document.body
  );
}

export function BalloonDrift() {
  const sentinel = useRef<HTMLDivElement>(null);
  const played = useRef(false);
  const [balloons, setBalloons] = useState<Balloon[]>([]);

  useEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const el = sentinel.current;
    if (!el) return;
    const io = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting && !played.current) {
        played.current = true;
        const batch = makeBalloons(6);
        setBalloons(batch);
        setTimeout(() => setBalloons([]), balloonLife(batch));
        io.disconnect();
      }
    });
    io.observe(el);
    return () => io.disconnect();
  }, []);

  return (
    <>
      <div ref={sentinel} aria-hidden="true" />
      <BalloonSky balloons={balloons} />
    </>
  );
}
