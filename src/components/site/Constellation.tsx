"use client";

import { useEffect, useRef, useState } from "react";
import type { StarData } from "@/lib/constellation";

/*
 * The library as a constellation — ink on paper, not stars on night.
 * Every dot is a real work; solid lines are the genuine connections;
 * the faint shimmer between drifting theories is ambience, kept almost
 * invisible so the real edges stay honest.
 */

type LaidNode = {
  hx: number; // home position, normalized 0..1
  hy: number;
  r: number;
  ax: number; // drift amplitude px
  ay: number;
  sx: number; // drift speed
  sy: number;
  px: number; // phase
  py: number;
};

function mulberry32(seed: number) {
  let a = seed;
  return () => {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function layout(data: StarData): LaidNode[] {
  const rnd = mulberry32(20260730);
  const out: LaidNode[] = [];

  for (const n of data.nodes) {
    let hx = 0.5;
    let hy = 0.5;
    let r = 3;
    if (n.kind === "book") {
      // the permanent works, near the centre
      hx = 0.40 + rnd() * 0.24;
      hy = 0.34 + rnd() * 0.22;
      r = 7.5;
    } else if (n.kind === "project") {
      // a loose lower arc
      const a = Math.PI * (0.15 + rnd() * 0.7);
      hx = 0.5 + Math.cos(a) * (0.30 + rnd() * 0.14);
      hy = 0.62 + Math.sin(a) * (0.16 + rnd() * 0.14);
      r = 4.5;
    } else if (n.kind === "idea") {
      // green, upper field
      hx = 0.6 + rnd() * 0.3;
      hy = 0.10 + rnd() * 0.2;
      r = 5;
    } else if (n.cluster !== undefined) {
      // a series — its chain should read as one small constellation
      const centers: [number, number][] = [
        [0.16, 0.24],
        [0.85, 0.55],
        [0.24, 0.78],
        [0.68, 0.13],
      ];
      const [cx, cy] = centers[n.cluster % centers.length];
      hx = cx + (rnd() - 0.5) * 0.14;
      hy = cy + (rnd() - 0.5) * 0.16;
      r = 2.3;
    } else {
      // theories — the wide sky
      const a = rnd() * Math.PI * 2;
      const rad = 0.26 + rnd() * 0.3;
      hx = 0.5 + Math.cos(a) * rad * 1.05;
      hy = 0.47 + Math.sin(a) * rad * 0.82;
      r = 2.3;
    }
    out.push({
      hx,
      hy,
      r,
      ax: 4 + rnd() * 9,
      ay: 4 + rnd() * 9,
      sx: 0.00012 + rnd() * 0.00022,
      sy: 0.00012 + rnd() * 0.00022,
      px: rnd() * Math.PI * 2,
      py: rnd() * Math.PI * 2,
    });
  }

  // relax: keep everything on the sheet and gently apart
  for (let iter = 0; iter < 90; iter++) {
    for (let i = 0; i < out.length; i++) {
      const a = out[i];
      a.hx = Math.min(0.97, Math.max(0.03, a.hx));
      a.hy = Math.min(0.94, Math.max(0.05, a.hy));
      for (let j = i + 1; j < out.length; j++) {
        const b = out[j];
        const dx = b.hx - a.hx;
        const dy = b.hy - a.hy;
        const d = Math.hypot(dx, dy) || 0.0001;
        const min = 0.045;
        if (d < min) {
          const push = ((min - d) / d) * 0.5;
          a.hx -= dx * push;
          a.hy -= dy * push;
          b.hx += dx * push;
          b.hy += dy * push;
        }
      }
    }
  }
  return out;
}

export function Constellation({ data }: { data: StarData }) {
  const wrapRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [hover, setHover] = useState<{ i: number; x: number; y: number } | null>(null);
  const hoverRef = useRef<number>(-1);

  useEffect(() => {
    const wrap = wrapRef.current;
    const canvas = canvasRef.current;
    if (!wrap || !canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // exact palette from the live stylesheet
    const probe = getComputedStyle(document.documentElement);
    const col = {
      ink: probe.getPropertyValue("--ink").trim() || "#1F1D1A",
      faint: probe.getPropertyValue("--ink-faint").trim() || "#8A857A",
      accent: probe.getPropertyValue("--accent").trim() || "#4a6a90",
      connect: probe.getPropertyValue("--connect").trim() || "#3f7a5e",
    };

    const laid = layout(data);
    const touching = data.edges;
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    let w = 0;
    let h = 0;
    let dpr = 1;
    let raf = 0;
    let running = true;
    let last = performance.now();
    let t = 12000; // start mid-drift so the first frame isn't aligned

    const pos = (i: number, time: number): [number, number] => {
      const n = laid[i];
      const x = n.hx * w + Math.sin(time * n.sx + n.px) * n.ax;
      const y = n.hy * h + Math.sin(time * n.sy + n.py) * n.ay;
      return [x, y];
    };

    const resize = () => {
      dpr = Math.min(2, window.devicePixelRatio || 1);
      w = wrap.clientWidth;
      h = wrap.clientHeight;
      canvas.width = w * dpr;
      canvas.height = h * dpr;
      canvas.style.width = `${w}px`;
      canvas.style.height = `${h}px`;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    };

    const draw = (now: number) => {
      if (!reduced && running) t += Math.min(50, now - last);
      last = now;
      ctx.clearRect(0, 0, w, h);

      const hovered = hoverRef.current;
      const pts: [number, number][] = laid.map((_, i) => pos(i, t));

      // ambience: near-invisible shimmer between drifting theories
      ctx.lineWidth = 1;
      for (let i = 0; i < data.nodes.length; i++) {
        if (data.nodes[i].kind !== "essay") continue;
        for (let j = i + 1; j < data.nodes.length; j++) {
          if (data.nodes[j].kind !== "essay") continue;
          const dx = pts[i][0] - pts[j][0];
          const dy = pts[i][1] - pts[j][1];
          const d = Math.hypot(dx, dy);
          if (d < 64) {
            ctx.strokeStyle = col.faint;
            ctx.globalAlpha = (1 - d / 64) * 0.10;
            ctx.beginPath();
            ctx.moveTo(pts[i][0], pts[i][1]);
            ctx.lineTo(pts[j][0], pts[j][1]);
            ctx.stroke();
          }
        }
      }

      // the real edges
      for (const [a, b] of touching) {
        const active = hovered === a || hovered === b;
        ctx.strokeStyle = active ? col.connect : col.ink;
        ctx.globalAlpha = active ? 0.65 : 0.15;
        ctx.lineWidth = active ? 1.4 : 1;
        ctx.beginPath();
        ctx.moveTo(pts[a][0], pts[a][1]);
        ctx.lineTo(pts[b][0], pts[b][1]);
        ctx.stroke();
      }

      // nodes
      for (let i = 0; i < data.nodes.length; i++) {
        const n = data.nodes[i];
        const [x, y] = pts[i];
        const isHover = i === hovered;
        const neighbour =
          hovered >= 0 &&
          touching.some(([a, b]) => (a === hovered && b === i) || (b === hovered && a === i));

        let fill = col.ink;
        let alpha = 1;
        if (n.kind === "essay") {
          fill = col.faint;
          alpha = 0.75;
        } else if (n.kind === "project") {
          alpha = 0.8;
        } else if (n.kind === "idea") {
          fill = col.connect;
          alpha = 0.95;
        }
        if (isHover) {
          fill = col.accent;
          alpha = 1;
        }

        ctx.globalAlpha = alpha;
        ctx.fillStyle = fill;
        ctx.beginPath();
        ctx.arc(x, y, laid[i].r + (isHover ? 2.5 : 0), 0, Math.PI * 2);
        ctx.fill();

        if (isHover || neighbour) {
          ctx.globalAlpha = 0.5;
          ctx.strokeStyle = isHover ? col.accent : col.connect;
          ctx.lineWidth = 1.2;
          ctx.beginPath();
          ctx.arc(x, y, laid[i].r + 5, 0, Math.PI * 2);
          ctx.stroke();
        }
      }
      ctx.globalAlpha = 1;

      raf = requestAnimationFrame(draw);
    };

    const hit = (mx: number, my: number): number => {
      let best = -1;
      let bestD = 1e9;
      for (let i = 0; i < laid.length; i++) {
        const [x, y] = pos(i, t);
        const d = Math.hypot(mx - x, my - y);
        if (d < Math.max(14, laid[i].r + 8) && d < bestD) {
          best = i;
          bestD = d;
        }
      }
      return best;
    };

    const onMove = (e: PointerEvent) => {
      const rect = canvas.getBoundingClientRect();
      const i = hit(e.clientX - rect.left, e.clientY - rect.top);
      hoverRef.current = i;
      canvas.style.cursor = i >= 0 ? "pointer" : "default";
      if (i >= 0) {
        const [x, y] = pos(i, t);
        setHover({ i, x, y });
      } else {
        setHover(null);
      }
    };
    const onLeave = () => {
      hoverRef.current = -1;
      setHover(null);
    };
    const onClick = (e: PointerEvent) => {
      const rect = canvas.getBoundingClientRect();
      const i = hit(e.clientX - rect.left, e.clientY - rect.top);
      if (i >= 0) window.location.href = data.nodes[i].href;
    };

    const io = new IntersectionObserver(([entry]) => {
      running = entry.isIntersecting;
    });
    io.observe(wrap);
    const ro = new ResizeObserver(resize);
    ro.observe(wrap);

    resize();
    raf = requestAnimationFrame(draw);
    canvas.addEventListener("pointermove", onMove);
    canvas.addEventListener("pointerleave", onLeave);
    canvas.addEventListener("pointerup", onClick);

    return () => {
      cancelAnimationFrame(raf);
      io.disconnect();
      ro.disconnect();
      canvas.removeEventListener("pointermove", onMove);
      canvas.removeEventListener("pointerleave", onLeave);
      canvas.removeEventListener("pointerup", onClick);
    };
  }, [data]);

  const hoverNode = hover ? data.nodes[hover.i] : null;

  return (
    <div className="flex flex-col gap-3">
      <div ref={wrapRef} className="relative h-[340px] w-full min-[900px]:h-[440px]">
        <canvas ref={canvasRef} aria-hidden="true" />
        {hover && hoverNode && (
          <div
            className="pointer-events-none absolute z-10 max-w-[260px] -translate-x-1/2 rounded-[2px] border border-line bg-paper px-3.5 py-2.5 shadow-[0_2px_12px_rgba(31,29,26,0.08)]"
            style={{
              left: Math.min(Math.max(hover.x, 130), (wrapRef.current?.clientWidth ?? 300) - 130),
              top: Math.max(hover.y - 74, 6),
            }}
          >
            <div className="font-mono text-[10px] uppercase tracking-[0.12em] text-faint">
              {hoverNode.tag}
            </div>
            <div className="mt-1 font-serif text-[14.5px] leading-[1.35] text-ink">
              {hoverNode.label}
            </div>
          </div>
        )}
        <span className="sr-only">
          A drifting map of the library — every dot is a work, every line a real
          connection. Use the index below to browse.
        </span>
      </div>
      <div className="flex flex-wrap items-baseline gap-x-5 gap-y-1 font-mono text-[10.5px] uppercase tracking-[0.12em] text-faint">
        <span className="flex items-center gap-1.5">
          <span className="inline-block h-[7px] w-[7px] rounded-full bg-ink" /> {data.counts.books} books
        </span>
        <span className="flex items-center gap-1.5">
          <span className="inline-block h-[5px] w-[5px] rounded-full bg-ink opacity-80" /> {data.counts.projects} projects
        </span>
        <span className="flex items-center gap-1.5">
          <span className="inline-block h-[4px] w-[4px] rounded-full bg-faint" /> {data.counts.essays} theories
        </span>
        <span className="flex items-center gap-1.5">
          <span className="inline-block h-[5px] w-[5px] rounded-full bg-connect" /> {data.counts.ideas} ideas
        </span>
        <span className="ml-auto normal-case tracking-[0.08em]">every line is real</span>
      </div>
    </div>
  );
}
