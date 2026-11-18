"use client";

import { useMemo, useRef, useState, useSyncExternalStore } from "react";
import {
  BalloonSky,
  balloonLife,
  makeBalloons,
  type Balloon,
} from "@/components/site/BalloonDrift";
import { buzz, playFireworks } from "@/lib/fireworks";
import { recordLine, renderGoodNews } from "@/lib/pingan-share";
import {
  BACK_AT_WORK,
  HOLD_BACK,
  HOLD_MS,
  HOLD_OUT,
  HOLD_ZH,
  HOW_BACK,
  HOW_OUT,
  JI,
  LEAN,
  LET_GO,
  MILESTONES,
  OUT_LINES,
  PAD_TAP,
  PINGAN_START,
  SAFE_LINES,
  STATUS,
  WHO,
  YI,
  type Who,
} from "@/content/pingan";
import s from "./PinganSign.module.css";

/*
 * 平安牌 — the house sign at /pingan (2026-11-18). A joke Hao and his wife made
 * up over breakfast: a works-site safety board ("本家庭已连续 N 天无人被裁")
 * over two hanging signs, one each.
 *
 *   tap a sign        it swings and says something
 *   hold it 2 seconds it really turns over — and that is good news (喜报)
 *
 * Nobody should have to read to know the sign wants holding (Hao, twice the
 * same day: 不用读任何文字就想按一下). A long press is a hidden gesture, so it
 * gets a signifier everyone already knows: a round thumbprint pad on each
 * sign — 按手印, and the phone's fingerprint sensor, both mean "put your
 * finger here and keep it there". Until this phone has turned a sign once, a
 * cartoon hand keeps showing how: it presses the pad, the ring round the pad
 * fills, it lets go. Under a real finger the sign sinks like a button, the
 * ring fills and the band fills left to right for exactly as long as the hold
 * takes; letting go early says so.
 *
 * Each phone keeps its own sign (localStorage, `pingan:v1`): no server, no
 * accounts, nothing about either of them in the repo. The news reaches the
 * other phone as a picture: the share sheet where the browser has one, and
 * otherwise the picture itself, to long-press and keep (in-app browsers such
 * as WeChat's have no share sheet and cannot download). The count is honest —
 * days since the sign went up, or since the last one of them went back to work.
 */

type Saved = {
  /** the day each sign was turned over (yyyy-mm-dd); absent = 没被裁 */
  h?: string;
  w?: string;
  /** the day the count last started again */
  since?: string;
  /** the run of quiet days that ended at the last turn */
  record?: number;
  /** this phone has turned a sign once: the showing hand can stop */
  taught?: boolean;
};

const KEY = "pingan:v1";
const PEOPLE: Who[] = ["h", "w"];
const TAP_MS = 250;
const WEEKDAYS = ["周日", "周一", "周二", "周三", "周四", "周五", "周六"];

const listeners = new Set<() => void>();
let memory = "";

function subscribe(cb: () => void) {
  listeners.add(cb);
  window.addEventListener("storage", cb);
  /* a tab left open overnight wakes up on the right day */
  document.addEventListener("visibilitychange", cb);
  return () => {
    listeners.delete(cb);
    window.removeEventListener("storage", cb);
    document.removeEventListener("visibilitychange", cb);
  };
}

function readSaved(): string {
  try {
    return window.localStorage.getItem(KEY) ?? memory;
  } catch {
    return memory;
  }
}

function writeSaved(next: Saved) {
  memory = JSON.stringify(next);
  try {
    window.localStorage.setItem(KEY, memory);
  } catch {
    /* private window: the sign still works for this visit */
  }
  listeners.forEach((l) => l());
}

const isDay = (v: unknown): v is string =>
  typeof v === "string" && /^\d{4}-\d{2}-\d{2}$/.test(v);

function parseSaved(raw: string): Saved {
  try {
    const v = JSON.parse(raw);
    if (v && typeof v === "object") {
      return {
        h: isDay(v.h) ? v.h : undefined,
        w: isDay(v.w) ? v.w : undefined,
        since: isDay(v.since) ? v.since : undefined,
        record: Number.isFinite(v.record) ? Math.max(0, Math.floor(v.record)) : undefined,
        taught: v.taught === true ? true : undefined,
      };
    }
  } catch {
    /* empty or damaged: both signs read 没被裁 */
  }
  return {};
}

const empty = () => "";

function dateKey(d: Date): string {
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${d.getFullYear()}-${m}-${day}`;
}

function dayNumber(key: string): number {
  const [y, m, d] = key.split("-").map(Number);
  return Math.floor(Date.UTC(y, m - 1, d) / 86_400_000);
}

const dotted = (key: string) => key.split("-").join(".");
const mod = (n: number, m: number) => ((n % m) + m) % m;

/** Quiet days in a row, today included. Nought while either sign is turned. */
function streakOf(saved: Saved, today: string): number {
  if (saved.h || saved.w) return 0;
  const from = saved.since && saved.since > PINGAN_START ? saved.since : PINGAN_START;
  return Math.max(0, dayNumber(today) - dayNumber(from)) + 1;
}

function calm(): boolean {
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

/* ── the two faces: one hand, thick ink, flat fills, a blush ─────────── */

const INK = "#1F1D1A";
const SKIN = "#FFD9B8";
const HAIR_W = "#4A3228";

function Mug({ who, out }: { who: Who; out: boolean }) {
  return (
    <svg viewBox="9 8 82 88" className={s.mug} aria-hidden="true">
      <g stroke={INK} strokeWidth="4" strokeLinejoin="round" strokeLinecap="round">
        {who === "w" && (
          <path
            d="M19 60 Q14 22 50 22 Q86 22 81 60 L83 88 Q74 94 68 86 L68 58 L32 58 L32 86 Q26 94 17 88 Z"
            fill={HAIR_W}
          />
        )}
        {who === "h" && (
          <>
            <circle cx="21" cy="60" r="6" fill={SKIN} />
            <circle cx="79" cy="60" r="6" fill={SKIN} />
          </>
        )}
        <circle cx="50" cy="58" r="29" fill={SKIN} />
        {who === "h" ? (
          <path
            d="M22 53 Q19 25 50 25 Q81 25 78 53 Q72 41 58 40 Q40 39 22 53 Z"
            fill={INK}
          />
        ) : (
          <path
            d="M22 55 Q21 26 50 26 Q79 26 78 55 Q66 39 48 43 Q34 45 22 55 Z"
            fill={HAIR_W}
          />
        )}
        {who === "w" && !out && (
          <>
            <path d="M63 35 l9 4" strokeWidth="9" />
            <path d="M63 35 l9 4" stroke="#FFD84D" strokeWidth="4" />
          </>
        )}
      </g>
      <ellipse cx="32" cy="68" rx="6" ry="4" fill="#FF9C8A" />
      <ellipse cx="68" cy="68" rx="6" ry="4" fill="#FF9C8A" />
      <g
        stroke={INK}
        strokeWidth="4"
        strokeLinejoin="round"
        strokeLinecap="round"
        fill="none"
      >
        {out ? (
          <>
            {/* laughing: > < and a wide-open mouth, under a graduation cap */}
            <path d="M33 54 l9 5 l-9 5" />
            <path d="M67 54 l-9 5 l9 5" />
            <path d="M39 70 Q50 88 61 70 Z" fill="#C2392F" />
            <path d="M29 28 L29 38 Q50 46 71 38 L71 28 Z" fill="#2F4B8F" />
            <path d="M50 11 L84 23 L50 35 L16 23 Z" fill="#2F4B8F" />
            <path d="M84 23 V42" strokeWidth="8" />
            <path d="M84 23 V42" stroke="#FFC93C" strokeWidth="3.5" />
            <circle cx="84" cy="46" r="4.5" fill="#FFC93C" strokeWidth="3" />
          </>
        ) : (
          <>
            <path d="M34 59 q5 -6 10 0" />
            <path d="M56 59 q5 -6 10 0" />
            <path d="M41 71 Q50 80 59 71" />
          </>
        )}
      </g>
    </svg>
  );
}

/**
 * The thumbprint pad: where the finger goes. A raised round button with a
 * print in ink and a ring that fills for as long as the hold takes.
 */
function Pad() {
  return (
    <span className={s.pad} data-pad="">
      <svg viewBox="0 0 48 48" aria-hidden="true">
        <circle cx="24" cy="24" r="20.5" fill="none" stroke="currentColor" strokeWidth="4" opacity="0.16" />
        {/* two rings on purpose: one the demonstration fills, one a real finger
            fills — so a real hold always starts from empty, never from wherever
            the demonstration happened to be */}
        {[s.padDemo, s.padGo].map((ring) => (
          <circle
            key={ring}
            className={ring}
            cx="24"
            cy="24"
            r="20.5"
            fill="none"
            stroke="currentColor"
            strokeWidth="4"
            strokeLinecap="round"
            transform="rotate(-90 24 24)"
          />
        ))}
        <g fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round">
          <path d="M12 29 v-4 a12 12 0 0 1 24 0 v3" strokeDasharray="27 4 100" />
          <path d="M16 32.5 v-7.5 a8 8 0 0 1 16 0 v6" strokeDasharray="100" />
          <path d="M20 35 v-10 a4 4 0 0 1 8 0 v8" strokeDasharray="14 3.5 100" />
          <path d="M24 25.5 v10.5" />
        </g>
      </svg>
    </span>
  );
}

/** The hand that shows how, until this phone has done it once. */
function DemoHand() {
  return (
    <svg viewBox="0 0 40 52" className={s.hand} aria-hidden="true">
      <g stroke={INK} strokeWidth="3" strokeLinejoin="round" strokeLinecap="round" fill={SKIN}>
        <rect x="3.5" y="27" width="9.5" height="15" rx="4.75" transform="rotate(-28 8 34)" />
        <rect x="9" y="22" width="26" height="26" rx="9" />
        <rect x="14" y="2.5" width="11" height="30" rx="5.5" />
      </g>
      {/* the finger grows out of the palm: no seam */}
      <rect x="15.5" y="20.3" width="8" height="14" fill={SKIN} />
      <rect x="12.4" y="23.6" width="14.2" height="10.8" fill={SKIN} />
      <path d="M30 23.5 v6" stroke={INK} strokeWidth="2.6" strokeLinecap="round" fill="none" />
    </svg>
  );
}

/* ── the sign ────────────────────────────────────────────────────────── */

export function PinganSign() {
  const today = useSyncExternalStore(subscribe, () => dateKey(new Date()), empty);
  const savedRaw = useSyncExternalStore(subscribe, readSaved, empty);
  const saved = useMemo(() => parseSaved(savedRaw), [savedRaw]);

  const [bubble, setBubble] = useState<{ who: Who; text: string; n: number } | null>(null);
  /* a finger is on this sign: it sinks and its band starts to fill */
  const [pressing, setPressing] = useState<Who | null>(null);
  const [news, setNews] = useState(false);
  const [saving, setSaving] = useState(false);
  /* the drawn 喜报, shown to long-press where there is no share sheet */
  const [picture, setPicture] = useState("");
  const [balloons, setBalloons] = useState<Balloon[]>([]);

  const root = useRef<HTMLElement>(null);
  const hangs = useRef<Record<Who, HTMLDivElement | null>>({ h: null, w: null });
  const inners = useRef<Record<Who, HTMLSpanElement | null>>({ h: null, w: null });
  const press = useRef<{
    who: Who;
    at: number;
    x: number;
    y: number;
    onPad: boolean;
    done: boolean;
  } | null>(null);
  const holdTimers = useRef<number[]>([]);
  const bubbleTimer = useRef(0);
  const lastLine = useRef<Record<Who, number>>({ h: -1, w: -1 });
  const stopShow = useRef<(() => void) | null>(null);

  const out = PEOPLE.filter((k) => saved[k]);
  const taught = !!saved.taught || out.length > 0;
  const streak = today ? streakOf(saved, today) : null;
  const digits = streak === null ? ["·"] : String(streak).split("");
  const stamp = MILESTONES.find(([n]) => n === streak)?.[1];
  const status =
    out.length === 2 ? STATUS.both : out.length === 1 ? STATUS[out[0]] : STATUS.none;

  const day = today ? dayNumber(today) : null;
  const yi = day === null ? "" : YI[mod(day, YI.length)];
  const ji = day === null ? "" : JI[mod(day, JI.length)];
  const [, mm, dd] = today ? today.split("-").map(Number) : [0, 0, 0];
  const weekday = day === null ? "" : WEEKDAYS[mod(day + 4, 7)];

  /* the good news, read off the signs as they stand */
  const newsFor = out.length === 2 ? "both" : out[0];
  const turnedOn = out.map((k) => saved[k] as string).sort();
  const goodNews = newsFor && {
    subject: newsFor === "both" ? "全家" : `${WHO[newsFor]}同志`,
    lean: LEAN[newsFor],
    record: saved.record ?? 0,
    date: dotted(turnedOn[turnedOn.length - 1]),
  };

  function releaseBalloons(n: number) {
    const batch = makeBalloons(n);
    setBalloons(batch);
    window.setTimeout(() => setBalloons([]), balloonLife(batch));
  }

  function say(who: Who, text: string, ms = 2400) {
    window.clearTimeout(bubbleTimer.current);
    setBubble({ who, text, n: Date.now() });
    bubbleTimer.current = window.setTimeout(() => setBubble(null), ms);
  }

  function swing(who: Who) {
    if (calm()) return;
    hangs.current[who]?.animate(
      [0, 7, -5, 3, -1.5, 0].map((deg) => ({ transform: `rotate(${deg}deg)` })),
      { duration: 900, easing: "ease-out" }
    );
  }

  function talk(who: Who) {
    const pool = saved[who] ? OUT_LINES : SAFE_LINES;
    let i = Math.floor(Math.random() * pool.length);
    if (i === lastLine.current[who]) i = (i + 1) % pool.length;
    lastLine.current[who] = i;
    say(who, pool[i]);
    swing(who);
  }

  function openNews() {
    stopShow.current?.();
    setNews(true);
    if (calm()) return;
    stopShow.current = playFireworks("finale", undefined, () => {
      stopShow.current = null;
    });
    releaseBalloons(12);
  }

  function closeNews() {
    stopShow.current?.();
    stopShow.current = null;
    setNews(false);
  }

  /*
   * Turning a sign over, flat. It squeezes shut edge-on, changes its face
   * while it is a line, and opens again — the width only ever runs 1 → 0 → 1.
   * No 3D, no second face waiting on the back: the first version was a
   * two-faced card on rotateY(180deg), and on Hao's phone the turned sign
   * read mirrored (左右相反). Nothing here can be seen from behind.
   */
  function flipSign(who: Who, commit: () => void) {
    const el = inners.current[who];
    if (!el || typeof el.animate !== "function" || calm()) {
      commit();
      return;
    }
    const shut = el.animate([{ transform: "scaleX(1)" }, { transform: "scaleX(0)" }], {
      duration: 190,
      easing: "ease-in",
      fill: "forwards",
    });
    shut.onfinish = () => {
      commit();
      el.animate(
        [
          { transform: "scaleX(0)" },
          { transform: "scaleX(1.07)", offset: 0.7 },
          { transform: "scaleX(1)" },
        ],
        { duration: 330, easing: "ease-out" }
      );
      shut.cancel();
    };
  }

  function turn(who: Who, at: { x: number; y: number }) {
    const cur = parseSaved(readSaved());
    const now = dateKey(new Date());
    if (cur[who]) {
      /* back at work: the count starts again once nobody is out */
      const next: Saved = { ...cur, [who]: undefined, taught: true };
      if (!next.h && !next.w) next.since = now;
      buzz([15, 40, 15]);
      flipSign(who, () => {
        writeSaved(next);
        say(who, BACK_AT_WORK, 3200);
        if (calm()) return;
        playFireworks("burst", at);
        releaseBalloons(7);
      });
      return;
    }
    const record = cur.h || cur.w ? (cur.record ?? 0) : streakOf(cur, now);
    window.clearTimeout(bubbleTimer.current);
    setBubble(null);
    buzz([20, 60, 20, 60, 40]);
    flipSign(who, () => {
      writeSaved({ ...cur, [who]: now, record, taught: true });
      /* let the turned sign be read for a moment, then break the news */
      window.setTimeout(openNews, calm() ? 0 : 800);
    });
  }

  function clearHold() {
    holdTimers.current.forEach((t) => window.clearTimeout(t));
    holdTimers.current = [];
  }

  function down(who: Who, e: React.PointerEvent<HTMLButtonElement>) {
    if (e.button > 0) return;
    try {
      e.currentTarget.setPointerCapture(e.pointerId);
    } catch {
      /* the hold still works without capture */
    }
    clearHold();
    const mine = {
      who,
      at: performance.now(),
      x: e.clientX,
      y: e.clientY,
      onPad: !!(e.target as Element).closest?.("[data-pad]"),
      done: false,
    };
    press.current = mine;
    setPressing(who);
    buzz(8);
    const lines = saved[who] ? HOLD_BACK : HOLD_OUT;
    const step = (HOLD_MS - TAP_MS) / lines.length;
    holdTimers.current = [
      ...lines.map((line, i) =>
        window.setTimeout(() => {
          if (i > 0) buzz(10);
          say(who, line, HOLD_MS);
        }, TAP_MS + i * step)
      ),
      window.setTimeout(() => {
        mine.done = true;
        setPressing(null);
        turn(who, mine);
      }, HOLD_MS),
    ];
  }

  function up(who: Who, cancelled: boolean) {
    const p = press.current;
    if (!p || p.who !== who) return;
    press.current = null;
    clearHold();
    setPressing(null);
    if (p.done) return;
    if (cancelled) {
      window.clearTimeout(bubbleTimer.current);
      setBubble(null);
      return;
    }
    if (performance.now() - p.at >= TAP_MS) say(who, LET_GO);
    else if (p.onPad && !saved[who]) say(who, PAD_TAP);
    else talk(who);
  }

  async function saveNews() {
    if (!goodNews || !root.current) return;
    setSaving(true);
    try {
      const blob = await renderGoodNews(goodNews, root.current);
      const name = `喜报-${goodNews.date}.png`;
      const file = new File([blob], name, { type: "image/png" });
      /* phones: the share sheet is the way into the album, or straight to chat */
      if (window.matchMedia("(pointer: coarse)").matches) {
        if (navigator.canShare?.({ files: [file] })) {
          try {
            await navigator.share({ files: [file] });
            return;
          } catch (err) {
            if ((err as Error).name === "AbortError") return;
          }
        }
        /* no share sheet (WeChat's browser, say): hand over the picture itself */
        setPicture(URL.createObjectURL(blob));
        return;
      }
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = name;
      a.click();
      window.setTimeout(() => URL.revokeObjectURL(url), 4000);
    } finally {
      setSaving(false);
    }
  }

  function closePicture() {
    URL.revokeObjectURL(picture);
    setPicture("");
  }

  return (
    <main ref={root} lang="zh-Hans" className={s.page}>
      <div className={s.stripe} aria-hidden="true" />

      <div className={s.col}>
        <section className={s.board} aria-label="家庭平安公告牌">
          <i className={s.screw} aria-hidden="true" />
          <i className={s.screw} aria-hidden="true" />
          <i className={s.screw} aria-hidden="true" />
          <i className={s.screw} aria-hidden="true" />
          <div className={s.tag}>家庭平安公告牌</div>
          <h1 className={s.lead}>本家庭已连续</h1>
          <div className={s.count}>
            {digits.map((d, i) => (
              <span key={i} className={`${s.tile} ${digits.length > 2 ? s.tileSmall : ""}`}>
                {d}
              </span>
            ))}
            <span className={s.unit}>天</span>
          </div>
          <div className={`${s.verdict} ${out.length ? s.verdictOut : ""}`}>无人被裁</div>
          <div className={s.since}>
            {out.length > 0 && goodNews
              ? `${goodNews.date} 喜报 · 上个纪录 ${goodNews.record} 天`
              : `自 ${dotted(saved.since && saved.since > PINGAN_START ? saved.since : PINGAN_START)} 起算`}
          </div>
          {stamp && (
            <div className={s.stamp} aria-label={stamp}>
              {[...stamp].map((ch, i) => (
                <span key={i} aria-hidden="true">
                  {ch}
                </span>
              ))}
            </div>
          )}
        </section>

        <div className={s.signs}>
          {PEOPLE.map((who) => {
            const isOut = !!saved[who];
            return (
              <div
                key={who}
                className={`${s.hang} ${taught ? "" : s.untaught}`}
                style={{ "--demo-delay": who === "h" ? "0.6s" : "3.6s" } as React.CSSProperties}
              >
                {bubble?.who === who && (
                  <div key={bubble.n} className={s.bubble} role="status">
                    {bubble.text}
                  </div>
                )}
                <div
                  ref={(el) => {
                    hangs.current[who] = el;
                  }}
                  className={s.swing}
                >
                  <svg viewBox="0 0 100 16.7" className={s.strings} aria-hidden="true">
                    <path
                      d="M22 17 L50 4 L78 17"
                      fill="none"
                      stroke={INK}
                      strokeWidth="1.8"
                      strokeLinejoin="round"
                    />
                    <circle cx="50" cy="4" r="3" fill="#D8D0BD" stroke={INK} strokeWidth="1.6" />
                  </svg>
                  <button
                    type="button"
                    className={`${s.sign} ${pressing === who ? s.pressing : ""}`}
                    style={{ "--hold": `${HOLD_MS}ms` } as React.CSSProperties}
                    aria-label={`${WHO[who]}：${isOut ? "被裁了" : "没被裁"}。轻点问一句，按住${HOLD_ZH}翻牌`}
                    onPointerDown={(e) => down(who, e)}
                    onPointerUp={() => up(who, false)}
                    onPointerCancel={() => up(who, true)}
                    onContextMenu={(e) => e.preventDefault()}
                    onClick={(e) => {
                      /* keyboard and screen readers: no pointer, so just ask */
                      if (e.detail === 0) talk(who);
                    }}
                  >
                    {/* one face at a time, never a hidden back: see flipSign */}
                    <span
                      ref={(el) => {
                        inners.current[who] = el;
                      }}
                      className={s.inner}
                    >
                      <span className={`${s.face} ${isOut ? s.back : ""}`}>
                        <span className={s.name}>{WHO[who]}</span>
                        <Mug who={who} out={isOut} />
                        <span className={`${s.band} ${isOut ? s.bandOut : ""}`}>
                          <span className={s.meter} />
                          <span className={s.words}>
                            <span className={s.state}>{isOut ? "被裁了" : "没被裁"}</span>
                            <span className={s.how}>{isOut ? HOW_BACK : HOW_OUT}</span>
                          </span>
                          <Pad />
                        </span>
                      </span>
                    </span>
                  </button>
                  {!taught && <DemoHand />}
                </div>
              </div>
            );
          })}
        </div>

        {out.length > 0 ? (
          <button type="button" className={s.status} onClick={openNews}>
            {status} · 看喜报
          </button>
        ) : (
          <div className={s.status}>{status}</div>
        )}

        <section className={s.almanac} aria-label="今日黄历">
          <div className={s.almHead}>
            <span>今日黄历</span>
            <span className={s.almDate}>{today ? `${mm}月${dd}日 · ${weekday}` : ""}</span>
          </div>
          <div className={s.row}>
            <span className={s.yi}>宜</span>
            <span>{yi}</span>
          </div>
          <div className={s.row}>
            <span className={s.ji}>忌</span>
            <span>{ji}</span>
          </div>
        </section>

        <p className={s.slogan}>高高兴兴上班去 · 平平安安没被裁</p>
      </div>

      <div className={s.stripe} aria-hidden="true" />

      {news && goodNews && (
        <div className={s.news} role="dialog" aria-modal="true" aria-label="喜报">
          <div className={s.poster}>
            <div className={s.newsTitle}>喜报</div>
            <div className={s.newsLine}>热烈祝贺</div>
            <div className={s.newsWho}>{goodNews.subject}</div>
            <div className={s.newsDid}>光荣毕业</div>
            <div className={s.newsRule} />
            {goodNews.record > 0 && (
              <div className={s.newsRecord}>{recordLine(goodNews.record)}</div>
            )}
            <div className={s.newsLean}>
              {goodNews.lean.map((line) => (
                <div key={line}>{line}</div>
              ))}
            </div>
            <div className={s.newsDate}>{goodNews.date} · 本家庭 宣</div>
          </div>
          <div className={s.newsBtns}>
            <button
              type="button"
              className={`${s.btn} ${s.btnGold}`}
              onClick={saveNews}
              disabled={saving}
            >
              {saving ? "正在画…" : "存成图片"}
            </button>
            <button type="button" className={s.btn} onClick={closeNews}>
              收下了
            </button>
          </div>
        </div>
      )}

      {picture && (
        <div className={s.picture} role="dialog" aria-modal="true" aria-label="喜报图片">
          {/* a blob drawn a moment ago: nothing for next/image to optimise */}
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src={picture} alt="喜报" className={s.pictureImg} />
          <p className={s.pictureHint}>长按图片 · 保存或发给对方</p>
          <button type="button" className={s.btn} onClick={closePicture}>
            好了
          </button>
        </div>
      )}

      <BalloonSky balloons={balloons} />
    </main>
  );
}
