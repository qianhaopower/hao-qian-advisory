"use client";

import { useEffect, useState } from "react";
import { LAUNCH_DATE } from "@/app/friendsintelligence/launchDate";

type TimeLeft = {
  days: number;
  hours: number;
  minutes: number;
  seconds: number;
};

function getTimeLeft(target: Date): TimeLeft | null {
  const diff = target.getTime() - Date.now();
  if (diff <= 0) return null;

  const totalSeconds = Math.floor(diff / 1000);
  return {
    days: Math.floor(totalSeconds / 86400),
    hours: Math.floor((totalSeconds % 86400) / 3600),
    minutes: Math.floor((totalSeconds % 3600) / 60),
    seconds: totalSeconds % 60,
  };
}

function pad(value: number) {
  return value.toString().padStart(2, "0");
}

export function FriendsCountdown() {
  // `mounted` guards against hydration mismatch — the clock is only
  // meaningful on the client, so we render placeholders until mount.
  const [mounted, setMounted] = useState(false);
  const [timeLeft, setTimeLeft] = useState<TimeLeft | null>(null);

  useEffect(() => {
    setMounted(true);
    setTimeLeft(getTimeLeft(LAUNCH_DATE));

    const id = setInterval(() => {
      setTimeLeft(getTimeLeft(LAUNCH_DATE));
    }, 1000);

    return () => clearInterval(id);
  }, []);

  // Launch reached.
  if (mounted && timeLeft === null) {
    return (
      <div className="flex flex-col items-center">
        <span className="text-[11px] font-medium uppercase tracking-[0.5em] text-[#e3b455] [text-shadow:0_0_14px_rgba(227,180,85,0.4)]">
          Launched
        </span>
        <p className="mt-4 text-3xl font-semibold tracking-wide text-[#f4efe3] md:text-4xl">
          Now Available
        </p>
      </div>
    );
  }

  const cells = [
    { label: "Days", value: timeLeft?.days ?? 0 },
    { label: "Hours", value: timeLeft?.hours ?? 0 },
    { label: "Minutes", value: timeLeft?.minutes ?? 0 },
    { label: "Seconds", value: timeLeft?.seconds ?? 0 },
  ];

  return (
    <div className="flex flex-col items-center">
      <span className="text-[11px] font-medium uppercase tracking-[0.5em] text-[#e3b455] [text-shadow:0_0_14px_rgba(227,180,85,0.4)]">
        Counting Down
      </span>

      {/* Quiet gold hairline to set the countdown apart */}
      <span className="mt-3 h-px w-10 bg-gradient-to-r from-transparent via-[#d6a441]/60 to-transparent" />

      <div className="mt-5 grid grid-cols-4 gap-2 sm:gap-2.5">
        {cells.map((cell) => (
          <div
            key={cell.label}
            className="flex min-w-[62px] flex-col items-center rounded-xl border border-[#d6a441]/15 bg-white/[0.05] px-3 py-2.5 shadow-[0_0_36px_-16px_rgba(227,180,85,0.5)] backdrop-blur-sm sm:min-w-[82px] sm:px-5 sm:py-3.5">
            <span className="font-mono text-3xl font-semibold tabular-nums text-[#f4efe3] [text-shadow:0_0_18px_rgba(227,180,85,0.22)] sm:text-[2.75rem] sm:leading-none">
              {mounted ? pad(cell.value) : "--"}
            </span>
            <span className="mt-2 text-[10px] uppercase tracking-[0.2em] text-[#b0a994] sm:text-[11px]">
              {cell.label}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
