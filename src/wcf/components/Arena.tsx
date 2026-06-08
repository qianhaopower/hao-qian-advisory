"use client";

import { AnimatePresence, motion, Transition } from "framer-motion";
import { useMemo } from "react";
import { BattlePhase, BattleResult, FighterState, Team } from "@wcf/types";
import Fighter from "./Fighter";

// Deterministic pseudo-random in [0,1) — pure (no Math.random), so it can run
// during render and produces identical output on server and client.
function seeded(n: number): number {
  const x = Math.sin(n * 12.9898) * 43758.5453;
  return x - Math.floor(x);
}

// Comic starburst outline shared by the impact bursts.
const STAR_CLIP =
  "polygon(50% 0, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%)";

type ArenaProps = {
  teamA: Team;
  teamB: Team;
  leftState: FighterState;
  rightState: FighterState;
  phase: BattlePhase;
  result?: BattleResult | null;
};

const phaseLabels: Record<BattlePhase, string> = {
  setup: "READY",
  entrance: "ENTRANCE",
  vs: "VS",
  round1: "ROUND 1",
  round2: "ROUND 2",
  chaos: "CHAOS",
  ko: "K.O.",
  result: "RESULT",
};

const ROUND_CAPTIONS: Partial<Record<BattlePhase, { title: string; sub?: string }>> = {
  round1: { title: "ROUND 1", sub: "Confidence Attack" },
  round2: { title: "ROUND 2", sub: "Tactical Confusion" },
  chaos: { title: "CHAOS MODE", sub: "Reality Destabilising" },
  ko: { title: "FINAL HIT", sub: "" },
};

// Comic words per phase, positioned near the receiving fighter.
const COMIC_BURSTS: Partial<
  Record<BattlePhase, { word: string; left: number; color: string; delay: number }[]>
> = {
  round1: [{ word: "POW!", left: 70, color: "#fde047", delay: 0 }],
  round2: [{ word: "BONK!", left: 30, color: "#fde047", delay: 0 }],
  chaos: [
    { word: "VAR?!", left: 50, color: "#ffffff", delay: 0.3 },
    { word: "OOF!", left: 36, color: "#fde047", delay: 1.0 },
    { word: "POW!", left: 66, color: "#fde047", delay: 1.6 },
  ],
};

const sponsorTags = [
  "VIBES ONLY",
  "NO BETTING",
  "HYPE LEVEL LOADING",
  "100% UNOFFICIAL",
  "EMOTIONALLY CORRECT",
  "CARTOON PHYSICS APPROVED",
];

// Fake, vibes-based health that swings with the fight phase.
function healthFor(
  phase: BattlePhase,
  isLeft: boolean,
  leftWon: boolean | null
): number {
  switch (phase) {
    case "setup":
    case "entrance":
    case "vs":
      return 100;
    case "round1":
      return isLeft ? 95 : 66;
    case "round2":
      return isLeft ? 62 : 50;
    case "chaos":
      return isLeft ? 44 : 40;
    case "ko":
    case "result":
      if (leftWon === null) return 30;
      return leftWon === isLeft ? 58 : 7;
    default:
      return 100;
  }
}

// Camera move applied to the whole arena per phase.
function cameraAnim(phase: BattlePhase) {
  switch (phase) {
    case "round1":
    case "round2":
      return { x: [0, -7, 7, -4, 0], y: [0, 3, -3, 0], scale: [1, 1.02, 1] };
    case "chaos":
      return { x: [0, -9, 9, -6, 6, 0], y: [0, 5, -5, 3, 0], scale: 1.045 };
    case "ko":
      return { x: 0, y: 0, scale: [1, 1.07] }; // slow push-in = slow-mo feel
    case "vs":
      return { x: 0, y: 0, scale: [1.015, 1] };
    default:
      return { x: 0, y: 0, scale: 1 };
  }
}

function cameraTrans(phase: BattlePhase): Transition {
  switch (phase) {
    case "chaos":
      return { duration: 0.4, repeat: Infinity };
    case "round1":
    case "round2":
      return { duration: 0.45 };
    case "ko":
      return { duration: 1.4, ease: "easeOut" };
    default:
      return { duration: 0.4, ease: "easeOut" };
  }
}

/* -------------------------------- Stadium ---------------------------------- */

function Spotlights({ teamA, teamB }: { teamA: Team; teamB: Team }) {
  return (
    <div className="pointer-events-none absolute inset-0 z-0 overflow-hidden">
      <motion.div
        className="absolute -top-10 left-0 h-[150%] w-3/5"
        style={{
          background: `linear-gradient(155deg, ${teamA.primaryColor}33 0%, rgba(255,255,255,0.14) 6%, transparent 52%)`,
          clipPath: "polygon(0 0, 40% 0, 72% 100%, 14% 100%)",
          filter: "blur(8px)",
        }}
        animate={{ opacity: [0.45, 0.8, 0.45] }}
        transition={{ duration: 4.5, repeat: Infinity, ease: "easeInOut" }}
      />
      <motion.div
        className="absolute -top-10 right-0 h-[150%] w-3/5"
        style={{
          background: `linear-gradient(-155deg, ${teamB.primaryColor}33 0%, rgba(255,255,255,0.14) 6%, transparent 52%)`,
          clipPath: "polygon(60% 0, 100% 0, 86% 100%, 28% 100%)",
          filter: "blur(8px)",
        }}
        animate={{ opacity: [0.8, 0.45, 0.8] }}
        transition={{ duration: 4.5, repeat: Infinity, ease: "easeInOut" }}
      />
    </div>
  );
}

function Crowd() {
  const flashes = useMemo(
    () =>
      Array.from({ length: 7 }, (_, i) => ({
        id: i,
        left: 8 + seeded(i + 11) * 84,
        top: 6 + seeded(i + 21) * 16,
        delay: seeded(i + 31) * 3,
      })),
    []
  );

  return (
    <div className="pointer-events-none absolute inset-x-0 top-0 z-0 h-2/5">
      <div
        className="absolute inset-0 opacity-50"
        style={{
          backgroundImage:
            "radial-gradient(circle, rgba(255,255,255,0.16) 1.3px, transparent 1.7px)",
          backgroundSize: "15px 11px",
          maskImage: "radial-gradient(135% 78% at 50% 125%, #000 32%, transparent 72%)",
          WebkitMaskImage: "radial-gradient(135% 78% at 50% 125%, #000 32%, transparent 72%)",
        }}
      />
      {flashes.map((f) => (
        <motion.span
          key={f.id}
          className="absolute h-1 w-1 rounded-full bg-white"
          style={{ left: `${f.left}%`, top: `${f.top}%` }}
          animate={{ opacity: [0, 1, 0], scale: [0.5, 1.6, 0.5] }}
          transition={{
            duration: 0.5,
            delay: f.delay,
            repeat: Infinity,
            repeatDelay: 2.2 + seeded(f.id + 41) * 2.5,
          }}
        />
      ))}
    </div>
  );
}

function PerspectiveFloor({ teamA, teamB }: { teamA: Team; teamB: Team }) {
  return (
    <div className="pointer-events-none absolute inset-x-0 bottom-0 z-0 h-[58%] overflow-hidden [perspective:540px]">
      <motion.div
        className="absolute inset-x-[-30%] bottom-0 top-0 origin-bottom"
        style={{
          transform: "rotateX(73deg)",
          backgroundImage:
            "linear-gradient(rgba(255,255,255,0.13) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.13) 1px, transparent 1px)",
          backgroundSize: "46px 46px",
          maskImage: "linear-gradient(to top, rgba(0,0,0,0.95) 4%, transparent 82%)",
          WebkitMaskImage: "linear-gradient(to top, rgba(0,0,0,0.95) 4%, transparent 82%)",
        }}
        animate={{ backgroundPositionY: ["0px", "46px"] }}
        transition={{ duration: 5, repeat: Infinity, ease: "linear" }}
      />
      <div
        className="absolute bottom-1 left-1/2 h-28 w-[88%] -translate-x-1/2 rounded-[50%]"
        style={{
          background: `radial-gradient(ellipse at center, ${teamA.primaryColor}3a, ${teamB.primaryColor}26 55%, transparent 74%)`,
          boxShadow: "0 -12px 60px rgba(255,255,255,0.06)",
        }}
      />
      <div className="absolute bottom-4 left-1/2 h-20 w-[74%] -translate-x-1/2 rounded-[50%] border border-white/20" />
      <div className="absolute bottom-7 left-1/2 h-14 w-[56%] -translate-x-1/2 rounded-[50%] border border-white/10" />
    </div>
  );
}

function Dust() {
  const motes = useMemo(
    () =>
      Array.from({ length: 16 }, (_, i) => ({
        id: i,
        left: seeded(i + 51) * 100,
        bottom: seeded(i + 61) * 70,
        size: 2 + seeded(i + 71) * 3,
        duration: 6 + seeded(i + 81) * 8,
        delay: seeded(i + 91) * 6,
        drift: (seeded(i + 101) - 0.5) * 40,
      })),
    []
  );

  return (
    <div className="pointer-events-none absolute inset-0 z-[7] overflow-hidden">
      {motes.map((m) => (
        <motion.span
          key={m.id}
          className="absolute rounded-full bg-white/40"
          style={{ left: `${m.left}%`, bottom: `${m.bottom}%`, width: m.size, height: m.size }}
          animate={{ y: [0, -60, 0], x: [0, m.drift, 0], opacity: [0, 0.6, 0] }}
          transition={{ duration: m.duration, delay: m.delay, repeat: Infinity, ease: "easeInOut" }}
        />
      ))}
    </div>
  );
}

/* ----------------------------------- HUD ----------------------------------- */

function HealthBar({
  color,
  value,
  align,
}: {
  color: string;
  value: number;
  align: "left" | "right";
}) {
  const low = value <= 20;
  return (
    <div className="h-2 w-full overflow-hidden rounded-full bg-white/10 ring-1 ring-inset ring-white/10">
      <motion.div
        className={`h-full rounded-full ${align === "right" ? "ml-auto" : ""}`}
        style={{
          background: low
            ? "linear-gradient(90deg, #ef4444, #fca5a5)"
            : `linear-gradient(90deg, ${color}, rgba(255,255,255,0.85))`,
          transformOrigin: align,
        }}
        animate={{ width: `${value}%`, opacity: low ? [1, 0.5, 1] : 1 }}
        transition={{
          width: { duration: 0.6, ease: "easeOut" },
          opacity: { duration: 0.6, repeat: low ? Infinity : 0 },
        }}
      />
    </div>
  );
}

function TeamHud({ team, health, side }: { team: Team; health: number; side: "left" | "right" }) {
  const align = side === "left" ? "left" : "right";
  return (
    <div
      className={`flex min-w-0 flex-1 items-center gap-2 ${
        side === "right" ? "flex-row-reverse" : ""
      }`}
    >
      <span className="text-lg drop-shadow sm:text-2xl" aria-hidden>
        {team.flag}
      </span>
      <div className="min-w-0 flex-1">
        <div
          className={`mb-1 flex items-center gap-1.5 ${
            side === "right" ? "flex-row-reverse" : ""
          }`}
        >
          <span
            className="truncate text-xs font-black tracking-wider text-white sm:text-sm"
            style={{ textShadow: `0 0 10px ${team.primaryColor}` }}
          >
            {team.code}
          </span>
          <span
            className="h-2 w-2 shrink-0 rounded-full"
            style={{ backgroundColor: team.primaryColor, boxShadow: `0 0 8px ${team.primaryColor}` }}
          />
        </div>
        <HealthBar color={team.primaryColor} value={health} align={align} />
      </div>
    </div>
  );
}

/* --------------------------------- VS badge -------------------------------- */

function VsBadge({ phase }: { phase: BattlePhase }) {
  const isChaos = phase === "chaos";
  const isVs = phase === "vs";
  return (
    <motion.div
      className="pointer-events-none absolute left-1/2 top-[44%] z-20 -translate-x-1/2 -translate-y-1/2 select-none"
      animate={
        isVs
          ? { scale: [2.4, 0.9, 1], rotate: [12, -5, 0] }
          : isChaos
            ? { rotate: [0, -5, 5, -3, 3, 0], scale: [1, 1.12, 1] }
            : { scale: [1, 1.06, 1] }
      }
      transition={
        isVs
          ? { duration: 0.7, times: [0, 0.6, 1], ease: "easeOut" }
          : isChaos
            ? { duration: 0.45, repeat: Infinity }
            : { duration: 2.2, repeat: Infinity, ease: "easeInOut" }
      }
    >
      {/* Shockwave ring on the VS zoom-in */}
      <AnimatePresence>
        {isVs && (
          <motion.div
            className="absolute left-1/2 top-1/2 h-20 w-20 -translate-x-1/2 -translate-y-1/2 rounded-full border-2 border-white/80"
            initial={{ scale: 0.2, opacity: 0.8 }}
            animate={{ scale: 4.5, opacity: 0 }}
            transition={{ duration: 0.7, ease: "easeOut" }}
          />
        )}
      </AnimatePresence>

      <motion.div
        className="absolute left-1/2 top-1/2 h-24 w-24 -translate-x-1/2 -translate-y-1/2 rounded-full sm:h-36 sm:w-36"
        style={{
          background:
            "radial-gradient(circle, rgba(244,63,94,0.45), rgba(168,85,247,0.25) 45%, transparent 70%)",
          filter: "blur(6px)",
        }}
        animate={{ opacity: [0.6, 1, 0.6] }}
        transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
      />
      <div className="relative flex h-16 w-16 items-center justify-center rounded-full border border-white/25 bg-white/5 shadow-[0_8px_40px_rgba(0,0,0,0.5)] backdrop-blur-md sm:h-28 sm:w-28">
        <div
          className="absolute inset-0 rounded-full"
          style={{ background: "linear-gradient(160deg, rgba(255,255,255,0.35) 0%, transparent 40%)" }}
        />
        <span
          className="bg-gradient-to-b from-white via-zinc-200 to-zinc-500 bg-clip-text text-3xl font-black italic tracking-tighter text-transparent sm:text-6xl"
          style={{
            WebkitTextStroke: "1px rgba(255,255,255,0.25)",
            filter: "drop-shadow(0 2px 6px rgba(0,0,0,0.6))",
          }}
        >
          VS
        </span>
      </div>
    </motion.div>
  );
}

/* ------------------------------ Cinematic bits ----------------------------- */

function NameCard({ team, side, delay }: { team: Team; side: "left" | "right"; delay: number }) {
  const from = side === "left" ? -180 : 180;
  return (
    <motion.div
      className="absolute inset-x-0 top-[28%] z-30 flex flex-col items-center text-center"
      initial={{ opacity: 0, x: from, scale: 1.15 }}
      animate={{ opacity: [0, 1, 1, 0], x: [from, 0, 0, -from * 0.25], scale: 1 }}
      transition={{ duration: 1.0, delay, times: [0, 0.25, 0.72, 1], ease: "easeOut" }}
    >
      <span className="text-4xl drop-shadow sm:text-6xl" aria-hidden>
        {team.flag}
      </span>
      <span
        className="mt-1 text-3xl font-black uppercase italic leading-none tracking-tight text-white sm:text-5xl"
        style={{ textShadow: `0 0 32px ${team.primaryColor}` }}
      >
        {team.name}
      </span>
      <span
        className="text-xs font-black uppercase tracking-[0.5em] sm:text-base"
        style={{ color: team.primaryColor }}
      >
        Enters
      </span>
    </motion.div>
  );
}

function FlagParticles({ team, side }: { team: Team; side: "left" | "right" }) {
  const base = side === "left" ? 200 : 320;
  const parts = useMemo(
    () =>
      Array.from({ length: 7 }, (_, i) => ({
        id: i,
        x: (side === "left" ? 6 : 70) + seeded(i + base) * 24,
        delay: seeded(i + base + 1) * 0.7,
        dx: (seeded(i + base + 2) - 0.5) * 70,
        dur: 1.3 + seeded(i + base + 3) * 1.0,
      })),
    [side, base]
  );
  return (
    <>
      {parts.map((p) => (
        <motion.span
          key={p.id}
          className="absolute text-base sm:text-2xl"
          style={{ left: `${p.x}%`, bottom: "14%" }}
          initial={{ y: 0, x: 0, opacity: 0, scale: 0.5 }}
          animate={{ y: -170, x: p.dx, opacity: [0, 1, 1, 0], scale: 1, rotate: p.dx }}
          transition={{ duration: p.dur, delay: p.delay, ease: "easeOut" }}
          aria-hidden
        >
          {team.flag}
        </motion.span>
      ))}
    </>
  );
}

function SpotlightFlash({ side, delay }: { side: "left" | "right"; delay: number }) {
  return (
    <motion.div
      className="absolute top-0 h-full w-1/2"
      style={{
        ...(side === "left" ? { left: 0 } : { right: 0 }),
        background: `linear-gradient(${
          side === "left" ? "160deg" : "200deg"
        }, rgba(255,255,255,0.5), transparent 45%)`,
        filter: "blur(10px)",
      }}
      initial={{ opacity: 0 }}
      animate={{ opacity: [0, 0.8, 0, 0.5, 0] }}
      transition={{ duration: 0.9, delay }}
    />
  );
}

function EntranceAnnounce({ teamA, teamB }: { teamA: Team; teamB: Team }) {
  return (
    <motion.div
      className="pointer-events-none absolute inset-0 z-30 overflow-hidden"
      initial={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      <SpotlightFlash side="left" delay={0} />
      <SpotlightFlash side="right" delay={0.85} />
      <FlagParticles team={teamA} side="left" />
      <FlagParticles team={teamB} side="right" />
      <NameCard team={teamA} side="left" delay={0.1} />
      <NameCard team={teamB} side="right" delay={0.95} />
    </motion.div>
  );
}

function RoundCaption({ phase }: { phase: BattlePhase }) {
  const cap = ROUND_CAPTIONS[phase];
  return (
    <AnimatePresence mode="wait">
      {cap && (
        <motion.div
          key={phase}
          className="pointer-events-none absolute inset-x-0 top-[13%] z-30 flex flex-col items-center px-4 text-center"
          initial={{ opacity: 0, scale: 1.3, y: -6 }}
          animate={{ opacity: [0, 1, 1, 0], scale: [1.3, 1, 1, 0.96], y: 0 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 1.4, times: [0, 0.18, 0.7, 1] }}
        >
          <span
            className="text-2xl font-black uppercase italic tracking-wider text-white sm:text-4xl"
            style={{ textShadow: "0 0 26px rgba(244,63,94,0.6)" }}
          >
            {cap.title}
          </span>
          {cap.sub && (
            // pl offsets the trailing letter-spacing so the text stays optically centered.
            <span className="max-w-full pl-[0.2em] text-[11px] font-black uppercase tracking-[0.2em] text-amber-300 sm:pl-[0.35em] sm:text-sm sm:tracking-[0.35em]">
              {cap.sub}
            </span>
          )}
        </motion.div>
      )}
    </AnimatePresence>
  );
}

function ComicBurst({ phase }: { phase: BattlePhase }) {
  const list = COMIC_BURSTS[phase];
  return (
    <AnimatePresence>
      {list && (
        <div key={phase} className="pointer-events-none absolute inset-0 z-30">
          {list.map((b, i) => (
            <motion.div
              key={i}
              className="absolute -translate-x-1/2 -translate-y-1/2"
              style={{ left: `${b.left}%`, top: "46%" }}
              initial={{ scale: 0.2, opacity: 0, rotate: -12 }}
              animate={{ scale: [0.2, 1.2, 1, 0.9], opacity: [0, 1, 1, 0], rotate: 0 }}
              transition={{ duration: 0.9, delay: b.delay, times: [0, 0.35, 0.7, 1] }}
            >
              <div
                className="absolute left-1/2 top-1/2 h-24 w-24 -translate-x-1/2 -translate-y-1/2 sm:h-32 sm:w-32"
                style={{
                  background: `radial-gradient(circle, ${b.color} 0%, #f97316 40%, transparent 62%)`,
                  clipPath: STAR_CLIP,
                }}
              />
              <span
                className="relative text-2xl font-black italic tracking-tight text-white sm:text-4xl"
                style={{ textShadow: "0 2px 0 #b91c1c, 0 0 14px rgba(0,0,0,0.5)" }}
              >
                {b.word}
              </span>
            </motion.div>
          ))}
        </div>
      )}
    </AnimatePresence>
  );
}

function SparkBurst({ color }: { color: string }) {
  const rays = useMemo(() => Array.from({ length: 14 }, (_, i) => i), []);
  return (
    <div className="pointer-events-none absolute left-1/2 top-1/2 z-20 -translate-x-1/2 -translate-y-1/2">
      {rays.map((i) => (
        <motion.span
          key={i}
          className="absolute left-0 top-0 h-1 w-16 origin-left rounded-full sm:w-24"
          style={{ background: `linear-gradient(90deg, ${color}, transparent)`, rotate: `${(360 / rays.length) * i}deg` }}
          initial={{ scaleX: 0, opacity: 0 }}
          animate={{ scaleX: [0, 1, 0.85], opacity: [0, 1, 0] }}
          transition={{ duration: 0.8, ease: "easeOut" }}
        />
      ))}
    </div>
  );
}

function Confetti({ colors }: { colors: string[] }) {
  const pieces = useMemo(
    () =>
      Array.from({ length: 44 }, (_, i) => ({
        id: i,
        left: seeded(i + 1) * 100,
        delay: seeded(i + 2) * 0.6,
        duration: 1.6 + seeded(i + 3) * 1.6,
        color: colors[i % colors.length],
        size: 6 + seeded(i + 4) * 8,
        rotate: seeded(i + 5) * 360,
      })),
    [colors]
  );

  return (
    <div className="pointer-events-none absolute inset-0 z-40 overflow-hidden">
      {pieces.map((p) => (
        <motion.span
          key={p.id}
          className="absolute top-[-10%] block rounded-sm"
          style={{ left: `${p.left}%`, width: p.size, height: p.size * 0.6, backgroundColor: p.color }}
          initial={{ y: "-10%", opacity: 0, rotate: 0 }}
          animate={{ y: "120%", opacity: [0, 1, 1, 0], rotate: p.rotate }}
          transition={{ duration: p.duration, delay: p.delay, ease: "easeIn" }}
        />
      ))}
    </div>
  );
}

function WinnerReveal({ winner }: { winner: Team }) {
  return (
    <div className="pointer-events-none absolute inset-x-0 top-[14%] z-40 flex flex-col items-center text-center">
      <motion.span
        className="text-[10px] font-black uppercase tracking-[0.5em] text-white/70 sm:text-xs"
        initial={{ opacity: 0, y: -8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
      >
        Winner Revealed
      </motion.span>
      <motion.span
        className="text-4xl font-black uppercase italic tracking-tight text-amber-300 sm:text-6xl"
        style={{ textShadow: "0 0 34px rgba(251,191,36,0.75)" }}
        initial={{ scale: 2.6, opacity: 0, rotate: -8 }}
        animate={{ scale: 1, opacity: 1, rotate: 0 }}
        transition={{ type: "spring", stiffness: 240, damping: 13, delay: 0.15 }}
      >
        WINNER
      </motion.span>
      <motion.div
        className="mt-1 flex items-center gap-2"
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.55 }}
      >
        <span className="text-3xl sm:text-5xl" aria-hidden>
          {winner.flag}
        </span>
        <span
          className="text-2xl font-black uppercase tracking-tight text-white sm:text-4xl"
          style={{ textShadow: `0 0 24px ${winner.primaryColor}` }}
        >
          {winner.name}
        </span>
      </motion.div>
    </div>
  );
}

function HypeMeter({ level }: { level: number }) {
  return (
    <motion.div
      className="pointer-events-none absolute bottom-8 left-1/2 z-40 w-56 max-w-[72%] -translate-x-1/2 rounded-xl border border-white/15 bg-black/65 px-3 py-2 backdrop-blur sm:bottom-10"
      initial={{ y: 26, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ delay: 0.5, type: "spring", stiffness: 200, damping: 18 }}
    >
      <div className="mb-1 flex items-center justify-between text-[9px] font-black uppercase tracking-[0.2em] text-white/70 sm:text-[10px]">
        <span>🔥 Hype Level</span>
        <span>{level}%</span>
      </div>
      <div className="h-2 w-full overflow-hidden rounded-full bg-white/10">
        <motion.div
          className="h-full rounded-full"
          style={{ background: "linear-gradient(90deg,#f59e0b,#f97316,#ef4444)" }}
          initial={{ width: 0 }}
          animate={{ width: `${level}%` }}
          transition={{ delay: 0.7, duration: 0.9, ease: "easeOut" }}
        />
      </div>
    </motion.div>
  );
}

function GlitchOverlay() {
  const bands = [0, 1, 2, 3];
  return (
    <div className="pointer-events-none absolute inset-0 z-50 overflow-hidden">
      {bands.map((i) => (
        <motion.div
          key={i}
          className="absolute inset-x-0"
          style={{
            top: `${14 + i * 22}%`,
            height: "10%",
            background: i % 2 ? "rgba(34,211,238,0.22)" : "rgba(244,63,94,0.22)",
            mixBlendMode: "screen",
          }}
          animate={{
            x: [0, i % 2 ? 14 : -14, 0, i % 2 ? -9 : 9, 0],
            opacity: [0.15, 0.6, 0.1, 0.5, 0.15],
          }}
          transition={{ duration: 0.3, repeat: Infinity, repeatType: "mirror", delay: i * 0.08 }}
        />
      ))}
      <motion.div
        className="absolute left-1/2 top-[9%] -translate-x-1/2 whitespace-nowrap"
        animate={{ x: [-2, 2, -1, 1, -2], opacity: [1, 0.7, 1, 0.85, 1] }}
        transition={{ duration: 0.25, repeat: Infinity }}
      >
        <span
          className="text-xs font-black uppercase tracking-[0.3em] text-cyan-300 sm:text-sm"
          style={{ textShadow: "2px 0 #ef4444, -2px 0 #22d3ee" }}
        >
          ⚠ Timeline Unstable
        </span>
      </motion.div>
    </div>
  );
}

/* ---------------------------------- Arena ---------------------------------- */

export default function Arena({ teamA, teamB, leftState, rightState, phase, result }: ArenaProps) {
  const isKO = phase === "ko";
  const isResult = phase === "result";
  const winner = result?.winner ?? null;

  // Infer the winning side from fighter poses before the result object exists.
  const leftWon =
    winner != null
      ? winner.id === teamA.id
      : leftState === "victory"
        ? true
        : rightState === "victory"
          ? false
          : null;

  const leftHealth = healthFor(phase, true, leftWon);
  const rightHealth = healthFor(phase, false, leftWon);

  const chaosInvolved = teamA.category === "chaos" || teamB.category === "chaos";
  const isChinaWin = winner?.id === "china";

  return (
    <motion.div
      className="relative mx-auto w-full max-w-4xl overflow-hidden rounded-[2rem] border border-white/10 bg-black/50 shadow-2xl backdrop-blur"
      style={{ transformOrigin: "center 58%" }}
      animate={cameraAnim(phase)}
      transition={cameraTrans(phase)}
    >
      {/* ---- Background stadium cluster (z-0) ---- */}
      <div
        className="absolute inset-0 z-0"
        style={{
          background: "radial-gradient(120% 90% at 50% 8%, #161d39 0%, #0b1022 48%, #05070f 100%)",
        }}
      />
      <Spotlights teamA={teamA} teamB={teamB} />
      <Crowd />
      <div
        className="absolute left-0 top-0 z-0 h-full w-1/2 opacity-40 blur-2xl"
        style={{ background: `radial-gradient(circle at 14% 42%, ${teamA.primaryColor}aa, transparent 60%)` }}
      />
      <div
        className="absolute right-0 top-0 z-0 h-full w-1/2 opacity-40 blur-2xl"
        style={{ background: `radial-gradient(circle at 86% 42%, ${teamB.primaryColor}aa, transparent 60%)` }}
      />
      <PerspectiveFloor teamA={teamA} teamB={teamB} />
      <div
        className="absolute left-1/2 top-[42%] z-0 h-[64%] w-[48%] -translate-x-1/2 -translate-y-1/2"
        style={{ background: "radial-gradient(ellipse at center, rgba(2,4,10,0.72) 0%, transparent 70%)" }}
      />
      <div className="absolute inset-0 z-0" style={{ boxShadow: "inset 0 0 130px 28px rgba(0,0,0,0.65)" }} />

      {/* ---- Top HUD (z-30) ---- */}
      <div className="absolute inset-x-0 top-0 z-30 flex items-start gap-2 px-3 pt-3 sm:gap-4 sm:px-5 sm:pt-4">
        <TeamHud team={teamA} health={leftHealth} side="left" />
        <div className="flex shrink-0 flex-col items-center pt-0.5">
          <AnimatePresence mode="wait">
            <motion.span
              key={phase}
              initial={{ y: -12, opacity: 0, scale: 0.8 }}
              animate={{ y: 0, opacity: 1, scale: 1 }}
              exit={{ y: 8, opacity: 0 }}
              className="rounded-full border border-white/15 bg-white/10 px-3 py-1 text-[10px] font-black uppercase tracking-[0.25em] text-white shadow-lg backdrop-blur sm:text-xs"
            >
              {phaseLabels[phase]}
            </motion.span>
          </AnimatePresence>
        </div>
        <TeamHud team={teamB} health={rightHealth} side="right" />
      </div>

      {/* ---- Sponsor boards marquee (z-[6], behind fighters) ---- */}
      <div className="absolute inset-x-0 bottom-0 z-[6] overflow-hidden border-t border-white/10 bg-black/40 backdrop-blur-sm">
        <motion.div
          className="flex w-max whitespace-nowrap py-1 text-[9px] font-bold uppercase tracking-[0.25em] text-white/35 sm:text-[10px]"
          animate={{ x: ["0%", "-50%"] }}
          transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
        >
          {[...sponsorTags, ...sponsorTags].map((tag, i) => (
            <span key={i} className="px-4">
              {tag} <span className="text-rose-400/40">•</span>
            </span>
          ))}
        </motion.div>
      </div>

      {/* ---- Fight stage (z-10) ---- */}
      <div className="relative z-10 mx-auto flex min-h-[380px] w-full max-w-2xl items-end justify-between px-5 pb-12 pt-20 sm:min-h-[460px] sm:px-4 sm:pb-16 sm:pt-24">
        <Fighter team={teamA} side="left" state={leftState} />
        <Fighter team={teamB} side="right" state={rightState} />
      </div>

      {/* ---- Center VS (hidden during entrance & result) ---- */}
      {phase !== "entrance" && !isResult && <VsBadge phase={phase} />}

      {/* ---- Cinematic overlays ---- */}
      <AnimatePresence>
        {phase === "entrance" && <EntranceAnnounce key="entrance" teamA={teamA} teamB={teamB} />}
      </AnimatePresence>
      <RoundCaption phase={phase} />
      <ComicBurst phase={phase} />

      {/* ---- KO bright flash (z-40) ---- */}
      <AnimatePresence>
        {isKO && (
          <motion.div
            className="absolute inset-0 z-40 bg-white"
            initial={{ opacity: 0 }}
            animate={{ opacity: [0, 0.85, 0, 0.5, 0] }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.8 }}
          />
        )}
      </AnimatePresence>

      {/* ---- Winner reveal moment (z-20 / z-40 / z-50) ---- */}
      {isResult && winner && (
        <>
          <SparkBurst color={winner.primaryColor} />
          <Confetti colors={[winner.primaryColor, winner.secondaryColor, winner.accentColor, "#ffffff"]} />
          <WinnerReveal winner={winner} />
          {chaosInvolved && result && <HypeMeter level={result.hypeLevel} />}
          {isChinaWin && <GlitchOverlay />}
        </>
      )}

      <Dust />
    </motion.div>
  );
}
