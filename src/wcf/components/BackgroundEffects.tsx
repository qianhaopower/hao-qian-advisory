"use client";

import { motion } from "framer-motion";
import { useMemo } from "react";

// Pure deterministic pseudo-random (no Math.random during render).
function seeded(n: number): number {
  const x = Math.sin(n * 78.233) * 43758.5453;
  return x - Math.floor(x);
}

export default function BackgroundEffects() {
  const stars = useMemo(
    () =>
      Array.from({ length: 22 }, (_, i) => ({
        id: i,
        left: seeded(i + 1) * 100,
        top: seeded(i + 2) * 42,
        size: 1 + seeded(i + 3) * 1.6,
        delay: seeded(i + 4) * 4,
        duration: 2 + seeded(i + 5) * 3,
      })),
    []
  );

  return (
    <div className="pointer-events-none fixed inset-0 -z-10 overflow-hidden">
      {/* Base cinematic gradient */}
      <div className="absolute inset-0 bg-[radial-gradient(130%_120%_at_50%_-5%,#141b38_0%,#0a0f22_42%,#04060e_100%)]" />

      {/* Subtle grid */}
      <div
        className="absolute inset-0 opacity-[0.05]"
        style={{
          backgroundImage:
            "linear-gradient(to right, #ffffff 1px, transparent 1px), linear-gradient(to bottom, #ffffff 1px, transparent 1px)",
          backgroundSize: "48px 48px",
          maskImage:
            "radial-gradient(120% 80% at 50% 30%, #000 30%, transparent 75%)",
          WebkitMaskImage:
            "radial-gradient(120% 80% at 50% 30%, #000 30%, transparent 75%)",
        }}
      />

      {/* Faint star/flashbulb field near the top */}
      {stars.map((s) => (
        <motion.span
          key={s.id}
          className="absolute rounded-full bg-white"
          style={{
            left: `${s.left}%`,
            top: `${s.top}%`,
            width: s.size,
            height: s.size,
          }}
          animate={{ opacity: [0.05, 0.55, 0.05] }}
          transition={{
            duration: s.duration,
            delay: s.delay,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />
      ))}

      {/* Drifting color orbs */}
      <motion.div
        className="absolute -left-24 top-10 h-72 w-72 rounded-full bg-fuchsia-600/25 blur-3xl"
        animate={{ x: [0, 40, 0], y: [0, 30, 0] }}
        transition={{ duration: 14, repeat: Infinity, ease: "easeInOut" }}
      />
      <motion.div
        className="absolute -right-20 top-1/3 h-80 w-80 rounded-full bg-cyan-500/20 blur-3xl"
        animate={{ x: [0, -50, 0], y: [0, 40, 0] }}
        transition={{ duration: 18, repeat: Infinity, ease: "easeInOut" }}
      />
      <motion.div
        className="absolute bottom-10 left-1/3 h-72 w-72 rounded-full bg-amber-500/15 blur-3xl"
        animate={{ x: [0, 30, 0], y: [0, -30, 0] }}
        transition={{ duration: 16, repeat: Infinity, ease: "easeInOut" }}
      />

      {/* Stadium horizon glow rising from the bottom */}
      <div
        className="absolute inset-x-0 bottom-0 h-1/3"
        style={{
          background:
            "radial-gradient(120% 100% at 50% 100%, rgba(99,102,241,0.18), transparent 70%)",
        }}
      />

      {/* Edge vignette for cinematic framing */}
      <div
        className="absolute inset-0"
        style={{ boxShadow: "inset 0 0 200px 60px rgba(0,0,0,0.7)" }}
      />
    </div>
  );
}
