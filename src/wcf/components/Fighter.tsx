"use client";

import { motion, Transition } from "framer-motion";
import { FighterState, Team } from "@wcf/types";

type FighterProps = {
  team: Team;
  side: "left" | "right";
  state: FighterState;
};

type Expression = "happy" | "fierce" | "hurt" | "ko";

// Design coordinate space — the whole mascot is laid out inside this box and
// then mirrored (for the right fighter) and scaled responsively.
const RIG_W = 120;
const RIG_H = 176;

function expressionFor(state: FighterState): Expression {
  switch (state) {
    case "hit":
    case "fall":
      return "hurt";
    case "ko":
      return "ko";
    case "taunt":
    case "dash":
    case "punch":
    case "kick":
      return "fierce";
    default:
      return "happy";
  }
}

/* --------------------------- whole-body animation -------------------------- */
// `dir` is +1 for the left fighter (faces/attacks right) and -1 for the right.
function getBodyAnimation(state: FighterState, dir: number) {
  switch (state) {
    case "enter":
      return { x: 0, y: 0, rotate: 0, scaleX: 1, scaleY: 1, opacity: 1 };
    case "idle":
      return { x: 0, y: [0, -5, 0], rotate: 0, scaleX: 1, scaleY: 1, opacity: 1 };
    case "taunt":
      return { x: 0, y: [0, -3, 0], rotate: [0, -3, 3, 0], scaleX: 1.02, scaleY: 1.02, opacity: 1 };
    case "dash":
      return { x: dir * 58, y: [0, -6, 0], rotate: -dir * 10, scaleX: 1.04, scaleY: 1.04, opacity: 1 };
    case "punch":
      return { x: dir * 32, y: 0, rotate: -dir * 6, scaleX: 1.05, scaleY: 1.05, opacity: 1 };
    case "kick":
      return { x: dir * 24, y: -6, rotate: -dir * 4, scaleX: 1.04, scaleY: 1.04, opacity: 1 };
    case "hit":
      return { x: -dir * 32, y: 0, rotate: dir * 12, scaleX: 1.08, scaleY: 0.9, opacity: 1 };
    case "fall":
      return { x: -dir * 18, y: 34, rotate: -dir * 78, scaleX: 1, scaleY: 1, opacity: 0.95 };
    case "ko":
      return { x: -dir * 20, y: 38, rotate: -dir * 84, scaleX: 1, scaleY: 1, opacity: 0.92 };
    case "victory":
      return { x: 0, y: [0, -22, 0], rotate: 0, scaleX: 1.05, scaleY: 1.05, opacity: 1 };
    default:
      return { x: 0, y: 0, rotate: 0, scaleX: 1, scaleY: 1, opacity: 1 };
  }
}

function getBodyTransition(state: FighterState): Transition {
  switch (state) {
    case "idle":
      return { duration: 1.7, repeat: Infinity, ease: "easeInOut" };
    case "victory":
      return { duration: 0.65, repeat: Infinity, ease: "easeInOut" };
    case "taunt":
      return { duration: 0.6, repeat: Infinity, ease: "easeInOut" };
    case "dash":
      return { duration: 0.3, ease: "easeOut" };
    case "punch":
      return { type: "spring", stiffness: 520, damping: 14 };
    case "kick":
      return { type: "spring", stiffness: 460, damping: 14 };
    case "hit":
      return { type: "spring", stiffness: 600, damping: 12 };
    case "enter":
      return { type: "spring", stiffness: 130, damping: 11 };
    case "fall":
    case "ko":
      return { type: "spring", stiffness: 90, damping: 12 };
    default:
      return { duration: 0.4, ease: "easeOut" };
  }
}

/* ------------------------------ limb animation ----------------------------- */
// All limb poses are authored as if the mascot faces right; the mirror layer
// flips them for the right-hand fighter.
function leadArm(state: FighterState) {
  switch (state) {
    case "idle":
      return { rotate: [12, 16, 12] };
    case "taunt":
      return { rotate: [12, -16, 12] };
    case "dash":
      return { rotate: 44 };
    case "punch":
      return { rotate: -86, scaleY: 1.2 };
    case "kick":
      return { rotate: -16 };
    case "hit":
      return { rotate: 66 };
    case "fall":
      return { rotate: 36 };
    case "ko":
      return { rotate: 44 };
    case "victory":
      return { rotate: [-150, -162, -150] };
    default:
      return { rotate: 12 };
  }
}

function rearArm(state: FighterState) {
  switch (state) {
    case "idle":
      return { rotate: [-10, -14, -10] };
    case "taunt":
      return { rotate: [-10, 16, -10] };
    case "dash":
      return { rotate: -46 };
    case "punch":
      return { rotate: 34 };
    case "kick":
      return { rotate: 16 };
    case "hit":
      return { rotate: -58 };
    case "fall":
      return { rotate: -30 };
    case "ko":
      return { rotate: -36 };
    case "victory":
      return { rotate: [150, 162, 150] };
    default:
      return { rotate: -10 };
  }
}

function leadLeg(state: FighterState) {
  switch (state) {
    case "kick":
      return { rotate: -62 };
    case "dash":
      return { rotate: -14 };
    case "fall":
      return { rotate: -22 };
    case "ko":
      return { rotate: -26 };
    case "victory":
      return { rotate: [4, -4, 4] };
    default:
      return { rotate: 5 };
  }
}

function rearLeg(state: FighterState) {
  switch (state) {
    case "dash":
      return { rotate: 22 };
    case "kick":
      return { rotate: 10 };
    case "fall":
      return { rotate: 24 };
    case "ko":
      return { rotate: 28 };
    default:
      return { rotate: -5 };
  }
}

const limbTransition = (state: FighterState): Transition => {
  if (state === "idle") return { duration: 1.7, repeat: Infinity, ease: "easeInOut" };
  if (state === "taunt") return { duration: 0.6, repeat: Infinity, ease: "easeInOut" };
  if (state === "victory") return { duration: 0.65, repeat: Infinity, ease: "easeInOut" };
  if (state === "punch" || state === "kick" || state === "hit")
    return { type: "spring", stiffness: 600, damping: 13 };
  return { duration: 0.25, ease: "easeOut" };
};

/* ---------------------------------- face ----------------------------------- */
function Face({ expr, accent }: { expr: Expression; accent: string }) {
  // Eyes sit slightly toward the opponent (right, in design space).
  const browRot = expr === "fierce" ? 18 : expr === "hurt" ? -16 : 6;

  return (
    <div className="absolute inset-0">
      {/* Eyebrows */}
      {expr !== "ko" && (
        <>
          <span
            className="absolute h-[3px] w-3 rounded-full"
            style={{ left: 12, top: 13, background: accent, transform: `rotate(${browRot}deg)` }}
          />
          <span
            className="absolute h-[3px] w-3 rounded-full"
            style={{ left: 27, top: 13, background: accent, transform: `rotate(${-browRot}deg)` }}
          />
        </>
      )}

      {/* Eyes */}
      {expr === "ko" ? (
        <>
          <CrossEye left={13} top={18} />
          <CrossEye left={28} top={18} />
        </>
      ) : expr === "hurt" ? (
        <>
          <span
            className="absolute h-2 w-[10px] rounded-t-full border-t-[3px]"
            style={{ left: 12, top: 22, borderColor: "#1f2430" }}
          />
          <span
            className="absolute h-2 w-[10px] rounded-t-full border-t-[3px]"
            style={{ left: 27, top: 22, borderColor: "#1f2430" }}
          />
        </>
      ) : (
        <>
          <Eye left={13} top={19} narrow={expr === "fierce"} />
          <Eye left={28} top={19} narrow={expr === "fierce"} />
        </>
      )}

      {/* Cheeks */}
      {(expr === "happy" || expr === "ko") && (
        <>
          <span className="absolute h-[5px] w-2 rounded-full bg-rose-400/50" style={{ left: 8, top: 30 }} />
          <span className="absolute h-[5px] w-2 rounded-full bg-rose-400/50" style={{ left: 34, top: 30 }} />
        </>
      )}

      {/* Mouth */}
      {expr === "happy" && (
        <span
          className="absolute rounded-b-full border-b-[3px]"
          style={{ left: 19, top: 31, width: 12, height: 7, borderColor: "#3a1f1f" }}
        />
      )}
      {expr === "fierce" && (
        <span className="absolute rounded-sm" style={{ left: 20, top: 33, width: 10, height: 4, background: "#3a1f1f" }} />
      )}
      {(expr === "hurt" || expr === "ko") && (
        <span
          className="absolute rounded-full"
          style={{ left: 20, top: 31, width: 10, height: 9, background: "#5b2330" }}
        />
      )}
    </div>
  );
}

function Eye({ left, top, narrow }: { left: number; top: number; narrow?: boolean }) {
  return (
    <span
      className="absolute rounded-full bg-white"
      style={{
        left,
        top,
        width: 10,
        height: narrow ? 7 : 11,
        boxShadow: "inset 0 0 0 1px rgba(0,0,0,0.12)",
      }}
    >
      <span className="absolute rounded-full bg-[#15151f]" style={{ left: 3, top: narrow ? 1 : 3, width: 5, height: 5 }}>
        <span className="absolute left-[1px] top-[1px] h-[2px] w-[2px] rounded-full bg-white" />
      </span>
    </span>
  );
}

function CrossEye({ left, top }: { left: number; top: number }) {
  return (
    <span className="absolute" style={{ left, top, width: 9, height: 9 }}>
      <span className="absolute left-1/2 top-1/2 h-[3px] w-[11px] -translate-x-1/2 -translate-y-1/2 rotate-45 rounded-full bg-[#15151f]" />
      <span className="absolute left-1/2 top-1/2 h-[3px] w-[11px] -translate-x-1/2 -translate-y-1/2 -rotate-45 rounded-full bg-[#15151f]" />
    </span>
  );
}

/* ---------------------------------- arm ------------------------------------ */
function Arm({
  state,
  team,
  lead,
}: {
  state: FighterState;
  team: Team;
  lead: boolean;
}) {
  const shoulderLeft = lead ? 80 : 30; // design-space x of the shoulder
  return (
    <motion.div
      className="absolute"
      style={{ left: shoulderLeft, top: 78, width: 12, height: 30, transformOrigin: "top center" }}
      animate={lead ? leadArm(state) : rearArm(state)}
      transition={limbTransition(state)}
    >
      {/* upper arm (sleeve colour) */}
      <div className="absolute left-0 top-0 h-5 w-3 rounded-full" style={{ background: team.secondaryColor }} />
      {/* forearm */}
      <div
        className="absolute left-0 top-3 h-5 w-3 rounded-full"
        style={{ background: team.primaryColor, filter: "brightness(1.05)" }}
      />
      {/* glove / fist */}
      <div
        className="absolute -left-[3px] top-[26px] h-[18px] w-[18px] rounded-full border-2"
        style={{ background: "#f8fafc", borderColor: team.accentColor, boxShadow: "inset -2px -2px 0 rgba(0,0,0,0.12)" }}
      >
        <span className="absolute right-[3px] top-1/2 h-2 w-[3px] -translate-y-1/2 rounded-full bg-black/15" />
      </div>
    </motion.div>
  );
}

/* ---------------------------------- leg ------------------------------------ */
function Leg({
  state,
  team,
  lead,
}: {
  state: FighterState;
  team: Team;
  lead: boolean;
}) {
  const hipLeft = lead ? 64 : 44;
  return (
    <motion.div
      className="absolute"
      style={{ left: hipLeft, top: 128, width: 12, height: 30, transformOrigin: "top center", zIndex: lead ? 6 : 1 }}
      animate={lead ? leadLeg(state) : rearLeg(state)}
      transition={limbTransition(state)}
    >
      {/* sock / leg */}
      <div className="absolute left-0 top-0 h-6 w-3 rounded-md" style={{ background: team.accentColor }} />
      {/* shoe */}
      <div className="absolute -left-1 top-[22px] h-[10px] w-[20px] rounded-[40%]" style={{ background: "#1b2030" }}>
        <span className="absolute bottom-0 left-0 h-[3px] w-full rounded-b-[40%]" style={{ background: team.primaryColor }} />
      </div>
    </motion.div>
  );
}

/* -------------------------------- effects ---------------------------------- */
function SpeedLines() {
  return (
    <div className="pointer-events-none absolute" style={{ right: RIG_W - 18, top: 56 }} aria-hidden>
      <div className="flex flex-col items-end gap-1.5">
        {[0, 1, 2, 3].map((i) => (
          <motion.span
            key={i}
            className="block h-1 rounded-full"
            style={{ width: 14 + i * 8, background: "linear-gradient(90deg, transparent, rgba(255,255,255,0.85))" }}
            initial={{ opacity: 0, x: 16 }}
            animate={{ opacity: [0, 0.9, 0], x: -10 }}
            transition={{ duration: 0.4, delay: i * 0.05, repeat: Infinity, repeatDelay: 0.06 }}
          />
        ))}
      </div>
    </div>
  );
}

function MotionTrail({ team }: { team: Team }) {
  return (
    <div className="pointer-events-none absolute inset-0" aria-hidden>
      {[1, 2].map((i) => (
        <motion.div
          key={i}
          className="absolute rounded-2xl"
          style={{ left: 34, top: 24, width: 52, height: 88, background: team.primaryColor, filter: "blur(2px)" }}
          initial={{ opacity: 0 }}
          animate={{ opacity: [0, 0.22 / i, 0], x: -14 * i }}
          transition={{ duration: 0.5, repeat: Infinity, ease: "easeOut" }}
        />
      ))}
    </div>
  );
}

function GloveBurst() {
  return (
    <motion.div
      className="pointer-events-none absolute"
      style={{ left: RIG_W - 14, top: 70 }}
      initial={{ scale: 0.3, opacity: 0 }}
      animate={{ scale: [0.3, 1.2, 0.9], opacity: [0, 1, 0] }}
      transition={{ duration: 0.45, repeat: Infinity, repeatDelay: 0.05 }}
      aria-hidden
    >
      <div
        className="h-8 w-8"
        style={{
          background: "radial-gradient(circle, #fff 0%, #fde047 45%, transparent 65%)",
          clipPath:
            "polygon(50% 0, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%)",
        }}
      />
    </motion.div>
  );
}

function FootBurst() {
  return (
    <motion.div
      className="pointer-events-none absolute"
      style={{ left: RIG_W - 8, top: 120 }}
      initial={{ scale: 0.3, opacity: 0 }}
      animate={{ scale: [0.3, 1.1, 0.8], opacity: [0, 1, 0] }}
      transition={{ duration: 0.45, repeat: Infinity, repeatDelay: 0.05 }}
      aria-hidden
    >
      <div
        className="h-7 w-7"
        style={{
          background: "radial-gradient(circle, #fff 0%, #f97316 45%, transparent 65%)",
          clipPath:
            "polygon(50% 0, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%)",
        }}
      />
    </motion.div>
  );
}

function SweatDrop() {
  return (
    <motion.div
      className="pointer-events-none absolute"
      style={{ left: 84, top: 26 }}
      initial={{ y: 0, opacity: 0 }}
      animate={{ y: [0, 14, 22], opacity: [0, 1, 0] }}
      transition={{ duration: 0.9, repeat: Infinity, repeatDelay: 0.2 }}
      aria-hidden
    >
      <div className="h-3 w-2 rounded-b-full rounded-t-full bg-sky-300" style={{ borderRadius: "50% 50% 50% 50% / 70% 70% 40% 40%" }} />
    </motion.div>
  );
}

function DizzyStars() {
  return (
    <div className="pointer-events-none absolute" style={{ left: 40, top: 6, width: 40, height: 24 }} aria-hidden>
      <motion.div
        className="absolute inset-0"
        animate={{ rotate: 360 }}
        transition={{ duration: 1.5, repeat: Infinity, ease: "linear" }}
      >
        <span className="absolute left-0 top-2 text-sm">⭐</span>
        <span className="absolute right-0 top-2 text-sm">💫</span>
        <span className="absolute left-1/2 top-0 -translate-x-1/2 text-xs">✨</span>
      </motion.div>
    </div>
  );
}

/* -------------------------------- Fighter ---------------------------------- */
export default function Fighter({ team, side, state }: FighterProps) {
  const dir = side === "left" ? 1 : -1;
  const facing = dir; // +1 faces right, -1 faces left
  const startX = side === "left" ? -170 : 170;
  const expr = expressionFor(state);

  const isDash = state === "dash";
  const isVictory = state === "victory";

  return (
    <div className="relative flex flex-col items-center">
      {/* Team-coloured spotlight pool so the mascot reads against the arena */}
      <div
        className="pointer-events-none absolute bottom-0 left-1/2 h-16 w-36 -translate-x-1/2 rounded-[50%] blur-xl sm:h-24 sm:w-56"
        style={{ background: `radial-gradient(ellipse at center, ${team.primaryColor}99, transparent 70%)` }}
        aria-hidden
      />

      {/* Responsive scale — smaller on phones, larger on desktop. Nested so it
          composes with the per-state motion transforms. */}
      <div className="relative origin-bottom scale-[0.76] sm:scale-[1.32]">
        <motion.div
          className="relative"
          style={{ width: RIG_W, height: RIG_H, transformOrigin: "bottom center" }}
          initial={{ x: startX, opacity: 0 }}
          animate={getBodyAnimation(state, dir)}
          transition={getBodyTransition(state)}
        >
          {/* Victory glow (positioned via left/top so framer can own the transform) */}
          {isVictory && (
            <motion.div
              className="absolute -z-10 h-40 w-40 rounded-full"
              style={{ left: -20, top: 8, background: `radial-gradient(circle, ${team.primaryColor}88, transparent 65%)` }}
              animate={{ opacity: [0.5, 1, 0.5], scale: [0.9, 1.1, 0.9] }}
              transition={{ duration: 0.8, repeat: Infinity }}
            />
          )}

          {/* Mirror layer — author once facing right, flip for the right fighter */}
          <div className="absolute inset-0" style={{ transform: `scaleX(${facing})`, transformOrigin: "center" }}>
            {isDash && <MotionTrail team={team} />}
            {(isDash || state === "punch" || state === "kick") && <SpeedLines />}

            {/* Floating flag — static wrapper centres it, motion bobs it,
                inner span counter-flips so it reads correctly when mirrored. */}
            <div className="absolute left-1/2 top-[-2px] z-40 -translate-x-1/2" aria-hidden>
              <motion.div
                animate={{ y: [0, -4, 0], rotate: [-4, 4, -4] }}
                transition={{ duration: 2.4, repeat: Infinity, ease: "easeInOut" }}
              >
                <span
                  className="block text-2xl drop-shadow-lg sm:text-[28px]"
                  style={{ transform: `scaleX(${facing})` }}
                >
                  {team.flag}
                </span>
              </motion.div>
            </div>

            {/* Rear arm (behind torso) */}
            <Arm state={state} team={team} lead={false} />

            {/* Legs */}
            <Leg state={state} team={team} lead={false} />
            <Leg state={state} team={team} lead />

            {/* Shorts */}
            <div
              className="absolute z-[8] rounded-b-xl rounded-t-md"
              style={{ left: 36, top: 118, width: 48, height: 18, background: team.secondaryColor, boxShadow: "inset 0 -3px 0 rgba(0,0,0,0.12)" }}
            />

            {/* Torso / jersey */}
            <div
              className="absolute z-10 overflow-hidden rounded-[14px] border-2"
              style={{ left: 33, top: 70, width: 54, height: 52, background: team.primaryColor, borderColor: team.accentColor }}
            >
              {/* shading */}
              <div className="absolute inset-0" style={{ background: "linear-gradient(160deg, rgba(255,255,255,0.25), transparent 45%, rgba(0,0,0,0.18))" }} />
              {/* side panels (secondary colour) */}
              <div className="absolute left-0 top-0 h-full w-2.5" style={{ background: team.secondaryColor, opacity: 0.9 }} />
              <div className="absolute right-0 top-0 h-full w-2.5" style={{ background: team.secondaryColor, opacity: 0.9 }} />
              {/* collar */}
              <div className="absolute left-1/2 top-0 h-2 w-6 -translate-x-1/2 rounded-b-md" style={{ background: team.accentColor }} />
              {/* chest badge (counter-flip the code text) */}
              <div
                className="absolute left-1/2 top-[18px] flex h-5 items-center justify-center rounded-md px-1"
                style={{ background: team.accentColor, transform: `translateX(-50%) scaleX(${facing})`, transformOrigin: "center" }}
              >
                <span className="text-[9px] font-black tracking-tight" style={{ color: team.primaryColor }}>
                  {team.code}
                </span>
              </div>
            </div>

            {/* Head */}
            <div
              className="absolute z-20 overflow-hidden rounded-[46%] border-2"
              style={{ left: 34, top: 24, width: 52, height: 50, background: team.secondaryColor, borderColor: team.accentColor }}
            >
              {/* sheen + shade for a 3D look on any colour */}
              <div className="absolute inset-0" style={{ background: "radial-gradient(circle at 32% 28%, rgba(255,255,255,0.55), transparent 45%)" }} />
              <div className="absolute inset-0" style={{ background: "linear-gradient(180deg, transparent 55%, rgba(0,0,0,0.16))" }} />
              <Face expr={expr} accent={team.accentColor} />
            </div>

            {/* Front (lead) arm — drawn above the torso */}
            <div className="absolute inset-0 z-30">
              <Arm state={state} team={team} lead />
            </div>

            {/* Cartoon effect overlays */}
            {state === "punch" && <GloveBurst />}
            {state === "kick" && <FootBurst />}
            {(state === "hit" || state === "fall") && <SweatDrop />}
            {(state === "ko" || state === "fall") && <DizzyStars />}

            {/* Body contact shadow */}
            <div
              className="absolute left-1/2 top-[150px] -z-10 h-3 w-16 -translate-x-1/2 rounded-[50%] bg-black/30 blur-[2px]"
              aria-hidden
            />
          </div>
        </motion.div>
      </div>

      {/* Grounded floor shadow (stays put while the body jumps/falls) */}
      <motion.div
        className="mt-0 h-2.5 w-16 rounded-[50%] bg-black/60 blur-[3px] sm:w-24"
        animate={
          state === "victory"
            ? { scaleX: [1, 0.62, 1], opacity: [0.45, 0.25, 0.45] }
            : state === "idle"
              ? { scaleX: [1, 0.95, 1], opacity: [0.45, 0.36, 0.45] }
              : state === "dash" || state === "kick"
                ? { scaleX: 0.82, opacity: 0.32 }
                : state === "ko" || state === "fall"
                  ? { scaleX: 1.2, opacity: 0.28 }
                  : { scaleX: 1, opacity: 0.45 }
        }
        transition={
          state === "victory"
            ? { duration: 0.65, repeat: Infinity }
            : state === "idle"
              ? { duration: 1.7, repeat: Infinity }
              : { duration: 0.3 }
        }
        aria-hidden
      />
    </div>
  );
}
