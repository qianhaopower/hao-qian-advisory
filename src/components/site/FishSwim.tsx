"use client";

import { useEffect, useRef, useState } from "react";

/*
 * Goldie, Zoey, Lulu and Stella — the actual cast, in their actual colours —
 * swim across the Fish Fun page once, when the reader reaches the tank.
 */

type FishSpec = {
  name: string;
  body: string;
  belly: string;
  size: number;
  delay: number;
  dur: number;
  y: number;
  spots?: boolean;
  stripes?: boolean;
};

const CAST: FishSpec[] = [
  { name: "goldie", body: "#E3A427", belly: "#F4CD74", size: 84, delay: 0, dur: 9.5, y: 2 },
  { name: "zoey", body: "#33312B", belly: "#57534A", size: 62, delay: 1.1, dur: 11, y: 30 },
  { name: "lulu", body: "#C9A06B", belly: "#E2CBA2", size: 50, delay: 2.0, dur: 12, y: 10, spots: true },
  { name: "stella", body: "#EAE4D6", belly: "#F6F2E8", size: 54, delay: 2.9, dur: 10.5, y: 40, stripes: true },
];

function FishSvg({ f }: { f: FishSpec }) {
  const clip = `fish-clip-${f.name}`;
  return (
    <svg
      width={f.size}
      height={f.size * 0.56}
      viewBox="-10 -4 64 38"
      aria-hidden="true"
    >
      <defs>
        <clipPath id={clip}>
          <ellipse cx="28" cy="16" rx="22" ry="12.5" />
        </clipPath>
      </defs>
      <path d="M9 16 L-8 5 L-5 16 L-8 27 Z" fill={f.body} opacity="0.9" />
      <path d="M24 5 L31 -3 L34 6 Z" fill={f.body} opacity="0.85" />
      <ellipse cx="28" cy="16" rx="22" ry="12.5" fill={f.body} />
      <ellipse cx="26" cy="21" rx="16" ry="7" fill={f.belly} opacity="0.6" clipPath={`url(#${clip})`} />
      {f.spots &&
        [
          [21, 11],
          [31, 19],
          [37, 10],
          [26, 15],
        ].map(([x, y], i) => (
          <circle key={i} cx={x} cy={y} r="2.4" fill="#8A6B3F" opacity="0.65" clipPath={`url(#${clip})`} />
        ))}
      {f.stripes &&
        [15, 24, 33, 42].map((x, i) => (
          <rect key={i} x={x} y="0" width="4" height="34" fill="#4A4A45" opacity="0.6" clipPath={`url(#${clip})`} />
        ))}
      <circle cx="41" cy="12" r="3.4" fill="#FFFFFF" />
      <circle cx="42.2" cy="12" r="1.7" fill="#1F1D1A" />
      <path d="M48.5 17 q2.4 1.6 0 3.4" stroke="#1F1D1A" strokeWidth="1.1" fill="none" opacity="0.55" />
    </svg>
  );
}

export function FishSwim() {
  const sentinel = useRef<HTMLDivElement>(null);
  const played = useRef(false);
  const [swimming, setSwimming] = useState(false);

  useEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const el = sentinel.current;
    if (!el) return;
    const io = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting && !played.current) {
        played.current = true;
        setSwimming(true);
        setTimeout(() => setSwimming(false), 16000);
        io.disconnect();
      }
    });
    io.observe(el);
    return () => io.disconnect();
  }, []);

  return (
    <>
      <div ref={sentinel} aria-hidden="true" />
      {swimming && (
        <div className="pointer-events-none fixed inset-x-0 bottom-6 z-40 h-28" aria-hidden="true">
          {CAST.map((f) => (
            <div
              key={f.name}
              className="fish-swim absolute left-0"
              style={{
                bottom: f.y,
                animationDuration: `${f.dur}s`,
                animationDelay: `${f.delay}s`,
              }}
            >
              <div
                className="fish-bob"
                style={{ animationDuration: `${2.1 + f.size / 90}s` }}
              >
                <FishSvg f={f} />
              </div>
            </div>
          ))}
        </div>
      )}
    </>
  );
}
