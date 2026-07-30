"use client";

import { useRef, useState } from "react";
import Link from "next/link";
import { SITE } from "@/content/site";

/*
 * The wordmark — with a secret. Five quick clicks and the balloon studio
 * pays the library a visit. (Little Wow Balloons is a real business of the
 * librarian's; the library keeps its jokes truthful too.)
 */

type Balloon = {
  id: number;
  left: number; // vw %
  size: number; // px
  color: string;
  duration: number; // s
  delay: number; // s
  sway: number; // px
};

const COLORS = ["#C96A5A", "#D9A441", "#7BA37E", "#6E88B0", "#B08BC0", "#D98A9E"];

export function Wordmark() {
  const clicks = useRef<number[]>([]);
  const nextId = useRef(0);
  const [balloons, setBalloons] = useState<Balloon[]>([]);
  const [toast, setToast] = useState(false);

  const release = () => {
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    setToast(true);
    setTimeout(() => setToast(false), 2600);
    if (reduced) return;
    const batch: Balloon[] = Array.from({ length: 14 }, () => ({
      id: nextId.current++,
      left: 4 + Math.random() * 92,
      size: 26 + Math.random() * 22,
      color: COLORS[Math.floor(Math.random() * COLORS.length)],
      duration: 4.5 + Math.random() * 2.5,
      delay: Math.random() * 0.9,
      sway: 14 + Math.random() * 22,
    }));
    setBalloons((b) => [...b, ...batch]);
    const maxLife = Math.max(...batch.map((b) => (b.duration + b.delay) * 1000)) + 200;
    setTimeout(() => {
      setBalloons((b) => b.filter((x) => !batch.some((y) => y.id === x.id)));
    }, maxLife);
  };

  const onClick = (e: React.MouseEvent) => {
    const now = Date.now();
    clicks.current = [...clicks.current.filter((t) => now - t < 2200), now];
    if (clicks.current.length >= 5) {
      e.preventDefault();
      clicks.current = [];
      release();
    }
  };

  return (
    <>
      <Link
        href="/"
        onClick={onClick}
        className="font-serif text-[19px] font-medium tracking-[0.01em] text-ink transition-colors duration-[250ms] hover:text-accent"
      >
        {SITE.name}
      </Link>

      {balloons.length > 0 && (
        <div className="pointer-events-none fixed inset-0 z-50 overflow-hidden" aria-hidden="true">
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
                  animationDuration: `${1.6 + Math.random()}s`,
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
        </div>
      )}

      {toast && (
        <div className="pointer-events-none fixed bottom-8 left-1/2 z-50 -translate-x-1/2 rounded-[2px] border border-line bg-paper px-5 py-3 font-mono text-[11px] uppercase tracking-[0.14em] text-ink-2 shadow-[0_4px_18px_rgba(31,29,26,0.10)]">
        Little Wow — the librarian also twists balloons 🎈
        </div>
      )}
    </>
  );
}
