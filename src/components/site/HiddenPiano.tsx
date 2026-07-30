"use client";

import { useEffect, useRef, useState } from "react";

/*
 * The About page is in tune. Home row = white keys, the row above = black
 * keys. Every sound is synthesised on the spot — no audio files, in the
 * same spirit as World Cup Fighter's procedural audio.
 */

const NOTES: { key: string; freq: number; label: string; black?: boolean }[] = [
  { key: "a", freq: 261.63, label: "C" },
  { key: "w", freq: 277.18, label: "C♯", black: true },
  { key: "s", freq: 293.66, label: "D" },
  { key: "e", freq: 311.13, label: "D♯", black: true },
  { key: "d", freq: 329.63, label: "E" },
  { key: "f", freq: 349.23, label: "F" },
  { key: "t", freq: 369.99, label: "F♯", black: true },
  { key: "g", freq: 392.0, label: "G" },
  { key: "y", freq: 415.3, label: "G♯", black: true },
  { key: "h", freq: 440.0, label: "A" },
  { key: "u", freq: 466.16, label: "A♯", black: true },
  { key: "j", freq: 493.88, label: "B" },
  { key: "k", freq: 523.25, label: "C′" },
  { key: "o", freq: 554.37, label: "C♯′", black: true },
  { key: "l", freq: 587.33, label: "D′" },
];

export function HiddenPiano() {
  const ctxRef = useRef<AudioContext | null>(null);
  const hideTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const [visible, setVisible] = useState(false);
  const [active, setActive] = useState<string | null>(null);

  useEffect(() => {
    const play = (freq: number) => {
      if (!ctxRef.current) {
        const AC =
          window.AudioContext ||
          (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
        ctxRef.current = new AC();
      }
      const ctx = ctxRef.current;
      if (ctx.state === "suspended") void ctx.resume();
      const now = ctx.currentTime;

      const gain = ctx.createGain();
      gain.gain.setValueAtTime(0.0001, now);
      gain.gain.exponentialRampToValueAtTime(0.4, now + 0.008);
      gain.gain.exponentialRampToValueAtTime(0.0001, now + 1.5);

      const filter = ctx.createBiquadFilter();
      filter.type = "lowpass";
      filter.frequency.value = 3200;

      const o1 = ctx.createOscillator();
      o1.type = "sine";
      o1.frequency.value = freq;

      const o2 = ctx.createOscillator();
      o2.type = "triangle";
      o2.frequency.value = freq * 2;
      const g2 = ctx.createGain();
      g2.gain.value = 0.18;

      o1.connect(filter);
      o2.connect(g2);
      g2.connect(filter);
      filter.connect(gain);
      gain.connect(ctx.destination);
      o1.start(now);
      o2.start(now);
      o1.stop(now + 1.6);
      o2.stop(now + 1.6);
    };

    const onKey = (e: KeyboardEvent) => {
      if (e.metaKey || e.ctrlKey || e.altKey || e.repeat) return;
      const target = e.target as HTMLElement;
      if (target.tagName === "INPUT" || target.tagName === "TEXTAREA") return;
      const note = NOTES.find((n) => n.key === e.key.toLowerCase());
      if (!note) return;
      play(note.freq);
      setVisible(true);
      setActive(note.key);
      setTimeout(() => setActive((k) => (k === note.key ? null : k)), 180);
      if (hideTimer.current) clearTimeout(hideTimer.current);
      hideTimer.current = setTimeout(() => setVisible(false), 5000);
    };

    window.addEventListener("keydown", onKey);
    return () => {
      window.removeEventListener("keydown", onKey);
      if (hideTimer.current) clearTimeout(hideTimer.current);
      void ctxRef.current?.close();
    };
  }, []);

  if (!visible) return null;

  return (
    <div className="pointer-events-none fixed bottom-7 left-1/2 z-50 -translate-x-1/2">
      <div className="flex items-end gap-1 rounded-[2px] border border-line bg-paper px-3 py-2.5 shadow-[0_4px_18px_rgba(31,29,26,0.10)]">
        {NOTES.map((n) => (
          <div
            key={n.key}
            className={`flex flex-col items-center justify-end rounded-[2px] border font-mono text-[9px] uppercase transition-colors duration-100 ${
              n.black
                ? "h-8 w-5 -mx-0.5 z-10 border-ink bg-ink text-paper"
                : "h-11 w-6 border-btnline bg-paper text-faint"
            } ${active === n.key ? "!bg-accent !text-paper !border-accent" : ""}`}
          >
            <span className="mb-1">{n.key}</span>
          </div>
        ))}
        <span className="ml-3 self-center font-mono text-[10px] uppercase tracking-[0.12em] text-faint">
          ♪ in tune
        </span>
      </div>
    </div>
  );
}
