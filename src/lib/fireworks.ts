/*
 * Fireworks for the /today deck — the reward for ticking a card off.
 *
 * Same idea as the Friends Intelligence app's celebrate.ts (a small burst
 * every day, a louder one at a milestone: "celebration exists, addiction does
 * not"), drawn here by hand on one throwaway canvas: no library, no files.
 *
 *   burst  — a few shells from where the visitor tapped. Works on paper or
 *            on the dark theme: saturated colours, no backdrop.
 *   finale — the eight-day show: dozens of shells and a last volley, meant to
 *            be played over the night-sky overlay the deck puts up.
 *
 * The caller decides whether to play at all (prefers-reduced-motion).
 */

type Spark = {
  x: number;
  y: number;
  vx: number;
  vy: number;
  life: number;
  max: number;
  color: string;
  r: number;
};

type Rocket = {
  at: number;
  x: number;
  y: number;
  targetY: number;
  vy: number;
  color: string;
  count: number;
  power: number;
  ring: boolean;
};

const COLORS = [
  "#F2B632",
  "#E4572E",
  "#4A90D9",
  "#2F8F5B",
  "#F06292",
  "#9B6FD0",
  "#FF8A5B",
];
const GLINT = "#FFE9A8";

const rand = (a: number, b: number) => a + Math.random() * (b - a);
const pick = <T,>(xs: T[]) => xs[Math.floor(Math.random() * xs.length)];

export function playFireworks(
  kind: "burst" | "finale",
  origin?: { x: number; y: number },
  onEnd?: () => void
): () => void {
  const W = window.innerWidth;
  const H = window.innerHeight;
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  const canvas = document.createElement("canvas");
  canvas.width = Math.round(W * dpr);
  canvas.height = Math.round(H * dpr);
  canvas.setAttribute("aria-hidden", "true");
  Object.assign(canvas.style, {
    position: "fixed",
    inset: "0",
    width: "100vw",
    height: "100vh",
    pointerEvents: "none",
    zIndex: "70",
  });
  document.body.appendChild(canvas);
  const ctx = canvas.getContext("2d");
  if (!ctx) {
    canvas.remove();
    onEnd?.();
    return () => {};
  }
  ctx.scale(dpr, dpr);
  ctx.lineCap = "round";

  const finale = kind === "finale";
  const sparks: Spark[] = [];
  const rockets: Rocket[] = [];
  /* size the show to the screen: a phone gets tighter shells than a desktop */
  const reach = Math.min(1, Math.max(0.6, Math.min(W, H) / 800));

  function explode(
    x: number,
    y: number,
    color: string,
    count: number,
    power: number,
    ring: boolean
  ) {
    const second = pick(COLORS);
    for (let i = 0; i < count; i++) {
      const a = (i / count) * Math.PI * 2 + rand(-0.06, 0.06);
      const v = power * reach * (ring ? rand(0.92, 1) : rand(0.25, 1));
      const max = rand(900, 1500);
      sparks.push({
        x,
        y,
        vx: Math.cos(a) * v,
        vy: Math.sin(a) * v,
        life: max,
        max,
        color: i % 5 === 0 ? GLINT : i % 2 === 0 ? color : second,
        r: rand(1.6, 3),
      });
    }
  }

  function rocket(at: number, x: number, targetY: number, big: boolean) {
    const flight = 620;
    rockets.push({
      at,
      x,
      y: H + 12,
      targetY,
      vy: (targetY - (H + 12)) / flight,
      color: pick(COLORS),
      count: big ? 150 : 96,
      power: big ? 0.62 : 0.5,
      ring: Math.random() < 0.3,
    });
  }

  if (finale) {
    for (let i = 0; i < 26; i++) {
      rocket(rand(0, 6200), rand(W * 0.1, W * 0.9), rand(H * 0.14, H * 0.5), i % 3 === 0);
    }
    /* the last volley, all at once */
    for (let i = 0; i < 7; i++) {
      rocket(6900 + i * 40, W * (0.11 + i * 0.13), rand(H * 0.16, H * 0.34), true);
    }
  } else {
    const ox = origin?.x ?? W / 2;
    const oy = origin?.y ?? H * 0.6;
    explode(ox, oy, pick(COLORS), 80, 0.46, false);
    const cx = Math.min(W * 0.8, Math.max(W * 0.2, ox));
    rocket(140, cx - W * 0.18, rand(H * 0.18, H * 0.34), false);
    rocket(420, cx + W * 0.2, rand(H * 0.16, H * 0.3), true);
    rocket(760, cx, rand(H * 0.12, H * 0.24), true);
  }

  let raf = 0;
  let last = 0;
  let start = 0;
  let stopped = false;

  function stop(tell: boolean) {
    if (stopped) return;
    stopped = true;
    cancelAnimationFrame(raf);
    canvas.remove();
    if (tell) onEnd?.();
  }

  function frame(now: number) {
    if (stopped || !ctx) return;
    if (!start) {
      start = now;
      last = now;
    }
    const dt = Math.min(40, now - last);
    last = now;
    const t = now - start;

    ctx.clearRect(0, 0, W, H);
    ctx.globalCompositeOperation = finale ? "lighter" : "source-over";

    for (let i = rockets.length - 1; i >= 0; i--) {
      const r = rockets[i];
      if (t < r.at) continue;
      r.y += r.vy * dt;
      if (r.y <= r.targetY) {
        explode(r.x, r.targetY, r.color, r.count, r.power, r.ring);
        rockets.splice(i, 1);
        continue;
      }
      ctx.globalAlpha = 0.9;
      ctx.strokeStyle = finale ? GLINT : r.color;
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.moveTo(r.x, r.y + 22);
      ctx.lineTo(r.x, r.y);
      ctx.stroke();
    }

    const drag = Math.pow(0.985, dt / 16);
    for (let i = sparks.length - 1; i >= 0; i--) {
      const s = sparks[i];
      s.life -= dt;
      if (s.life <= 0) {
        sparks.splice(i, 1);
        continue;
      }
      s.vx *= drag;
      s.vy = s.vy * drag + 0.00042 * dt;
      s.x += s.vx * dt;
      s.y += s.vy * dt;
      ctx.globalAlpha = Math.min(1, (s.life / s.max) * 1.6);
      ctx.strokeStyle = s.color;
      ctx.lineWidth = s.r * 1.5;
      ctx.beginPath();
      ctx.moveTo(s.x - s.vx * 30, s.y - s.vy * 30);
      ctx.lineTo(s.x, s.y);
      ctx.stroke();
    }
    ctx.globalAlpha = 1;

    if (rockets.length === 0 && sparks.length === 0) {
      stop(true);
      return;
    }
    raf = requestAnimationFrame(frame);
  }

  raf = requestAnimationFrame(frame);
  return () => stop(false);
}

/** The small physical nudge the app gives too — where the phone allows it. */
export function buzz(pattern: number | number[]) {
  try {
    navigator.vibrate?.(pattern);
  } catch {
    /* some browsers throw when called too often */
  }
}
