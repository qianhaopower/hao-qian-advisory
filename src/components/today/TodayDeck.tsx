"use client";

import { useMemo, useRef, useState, useSyncExternalStore } from "react";
import { createPortal } from "react-dom";
import {
  PILLARS,
  PILLAR_ORDER,
  cardForDay,
  cardText,
  dateKey,
  dateLabel,
  dayNumber,
  deckPath,
  type DeckCard,
  type Lang,
  type PillarId,
} from "@/lib/today-deck";
import { ActionCard, CardBack } from "@/components/today/ActionCard";
import {
  BalloonSky,
  balloonLife,
  makeBalloons,
  type Balloon,
} from "@/components/site/BalloonDrift";
import { renderShareImage } from "@/lib/today-share";
import { buzz, playFireworks } from "@/lib/fireworks";

/*
 * 今天只做一件事 / One thing today — the stage and the deck.
 *
 * One card a day, the same card for everyone (lib/today-deck.cardForDay).
 * What the visitor did lives only in their own browser (localStorage): no
 * accounts, no server, and no counts of anybody else. The card on the stage
 * is whatever ?card= names, so every card has a link of its own.
 *
 * The reward (2026-11-11, Hao: "点了以后要给大家一个巨大的惊喜"): every tick
 * sets off fireworks from the button, and every eighth DAY with something
 * done turns the page to night for the big show. Days are counted, not
 * streaks — a missed day costs nothing.
 */

const SHOW_EVERY = 8;

/* ── what this visitor has turned over and done (their browser only) ──── */

const KEY = "today:v1";
type Saved = { seen?: string; done: [slug: string, day: string][] };

const listeners = new Set<() => void>();
let memory = "";

function subscribe(cb: () => void) {
  listeners.add(cb);
  window.addEventListener("storage", cb);
  window.addEventListener("popstate", cb);
  return () => {
    listeners.delete(cb);
    window.removeEventListener("storage", cb);
    window.removeEventListener("popstate", cb);
  };
}

function readSaved(): string {
  try {
    return window.localStorage.getItem(KEY) ?? "";
  } catch {
    return memory;
  }
}

function writeSaved(next: Saved) {
  memory = JSON.stringify(next);
  try {
    window.localStorage.setItem(KEY, memory);
  } catch {
    /* private window: the deck still works for this visit */
  }
  listeners.forEach((l) => l());
}

function parseSaved(raw: string): Saved {
  try {
    const v = JSON.parse(raw);
    if (v && Array.isArray(v.done)) return v as Saved;
  } catch {
    /* empty or damaged: start clean */
  }
  return { done: [] };
}

function readUrlCard(): string {
  return new URLSearchParams(window.location.search).get("card") ?? "";
}

function writeUrlCard(slug: string) {
  const url = new URL(window.location.href);
  if (slug) url.searchParams.set("card", slug);
  else url.searchParams.delete("card");
  window.history.replaceState(null, "", url);
  listeners.forEach((l) => l());
}

const empty = () => "";

function calm(): boolean {
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

/* ── the words, in both editions ──────────────────────────────────────── */

const WORDS = {
  zh: {
    waitingTitle: "今天这一张，\n还没翻开。",
    waitingBody: "不用改变人生。翻一张，做一件，就够了。",
    turn: "翻开今天这一张",
    did: "我做到了",
    another: "换一张",
    hint: "做完了，再回来点一下。每点一次，放一次烟花。",
    backToday: "回到今天这一张",
    doneTitle: "做到了！",
    count: (n: number) => `这是你做到的第 ${n} 件。`,
    tomorrow: "明天这一张",
    tomorrowWait: "明早才能翻开",
    tomorrowMark: "明",
    save: "存成图片",
    saving: "正在画…",
    again: "再看一张",
    undo: "点错了，撤销",
    toGo: (n: number) => `做满 ${SHOW_EVERY} 天，放一场大烟花 · 还差 ${n} 天`,
    full: `做满 ${SHOW_EVERY} 天了`,
    peek: "偷看一眼",
    deck: "整副牌",
    all: "全部",
    showTitle: (d: number) => `第 ${d} 天！`,
    showLine: `做满 ${SHOW_EVERY} 天了。这一场烟花，是给你的。`,
    showPeek: "这是做满 8 天的那一场。",
    showClose: "点一下回去",
    flipLabel: "翻开今天这一张",
  },
  en: {
    waitingTitle: "Today’s card is\nstill face down.",
    waitingBody: "No need to change your life. Turn one over, do one thing. That is enough.",
    turn: "Turn over today’s card",
    did: "I did it",
    another: "Another card",
    hint: "Come back and tap when it is done. Every tap sets off fireworks.",
    backToday: "Back to today’s card",
    doneTitle: "Done!",
    count: (n: number) =>
      n === 1 ? "That is the first thing you have done." : `That makes ${n} things done.`,
    tomorrow: "Tomorrow’s card",
    tomorrowWait: "It turns over in the morning",
    tomorrowMark: "明",
    save: "Save as picture",
    saving: "Drawing…",
    again: "See another",
    undo: "Tapped by mistake — undo",
    toGo: (n: number) =>
      `${SHOW_EVERY} days done sets off the big fireworks · ${n} to go`,
    full: `${SHOW_EVERY} days done`,
    peek: "peek",
    deck: "The whole deck",
    all: "All",
    showTitle: (d: number) => `Day ${d}!`,
    showLine: "Eight days done. These fireworks are yours.",
    showPeek: "This is the show for day eight.",
    showClose: "tap to go back",
    flipLabel: "Turn over today’s card",
  },
} as const;

/* ── small pieces ─────────────────────────────────────────────────────── */

const INK = "#1F1D1A";

function BigButton({
  children,
  onClick,
  primary = false,
  disabled = false,
  lang,
}: {
  children: React.ReactNode;
  onClick: (e: React.MouseEvent<HTMLButtonElement>) => void;
  primary?: boolean;
  disabled?: boolean;
  lang: Lang;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      className={`inline-flex h-[56px] items-center justify-center gap-2.5 rounded-full border-2 border-ink px-7 transition-colors duration-[250ms] disabled:opacity-60 ${
        lang === "en"
          ? "font-serif text-[19px] font-semibold"
          : "zh-display text-[18px] tracking-[0.04em]"
      } ${
        primary
          ? "bg-ink text-paper hover:bg-ink-2"
          : "bg-transparent text-ink hover:bg-surface"
      }`}
    >
      {children}
    </button>
  );
}

function QuietButton({
  children,
  onClick,
}: {
  children: React.ReactNode;
  onClick: () => void;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className="text-[14px] text-ink-2 underline decoration-btnline underline-offset-4 transition-colors duration-[250ms] hover:text-accent hover:decoration-accent"
    >
      {children}
    </button>
  );
}

/** Eight lamps: one lights for every day with something done. */
function Lamps({
  lit,
  label,
  peek,
  onPeek,
}: {
  lit: number;
  label: string;
  peek: string;
  onPeek: () => void;
}) {
  return (
    <div className="mt-8 flex max-w-[440px] flex-wrap items-center gap-x-4 gap-y-2 border-t border-line pt-4">
      <div className="flex gap-1.5" aria-hidden="true">
        {Array.from({ length: SHOW_EVERY }, (_, i) => (
          <span
            key={i}
            className="h-[13px] w-[13px] rounded-full border-[1.5px] border-ink"
            style={{ background: i < lit ? "#F2B632" : "transparent" }}
          />
        ))}
      </div>
      <span className="text-[13px] leading-[1.5] text-ink-2">{label}</span>
      <QuietButton onClick={onPeek}>{peek}</QuietButton>
    </div>
  );
}

/* ── the room ─────────────────────────────────────────────────────────── */

export function TodayDeck({
  cards,
  handle,
  lang = "zh",
}: {
  cards: DeckCard[];
  /** The 小红书 account name printed on the Chinese share picture. */
  handle: string;
  lang?: Lang;
}) {
  const w = WORDS[lang];
  const en = lang === "en";
  const display = en ? "font-serif font-semibold tracking-[-0.01em]" : "zh-display";

  const today = useSyncExternalStore(subscribe, () => dateKey(new Date()), empty);
  const savedRaw = useSyncExternalStore(subscribe, readSaved, empty);
  const urlCard = useSyncExternalStore(subscribe, readUrlCard, empty);
  const saved = useMemo(() => parseSaved(savedRaw), [savedRaw]);

  const [animated, setAnimated] = useState(false);
  const [filter, setFilter] = useState<PillarId | "all">("all");
  const [balloons, setBalloons] = useState<Balloon[]>([]);
  const [saving, setSaving] = useState(false);
  /* the eight-day show: which day it is for, and whether it is only a peek */
  const [show, setShow] = useState<{ day: number; peek: boolean } | null>(null);
  const stopShow = useRef<(() => void) | null>(null);
  const stage = useRef<HTMLDivElement>(null);

  const bySlug = useMemo(() => new Map(cards.map((c) => [c.episode, c])), [cards]);
  const todayCard = today ? cardForDay(cards, dayNumber(today)) : null;
  const tomorrowCard = today ? cardForDay(cards, dayNumber(today) + 1) : null;

  const picked = urlCard ? bySlug.get(urlCard) : undefined;
  const shown = picked ?? (today && saved.seen === today ? todayCard : null);
  const isToday = !!shown && !!todayCard && shown.episode === todayCard.episode;
  const doneNow =
    !!shown && saved.done.some(([s, d]) => s === shown.episode && d === today);
  const everDone = useMemo(() => new Set(saved.done.map(([s]) => s)), [saved]);
  const daysDone = useMemo(() => new Set(saved.done.map(([, d]) => d)), [saved]);

  /* lamps lit in the current round of eight */
  const round = daysDone.size % SHOW_EVERY;
  const lit =
    round === 0 && daysDone.size > 0 && daysDone.has(today) ? SHOW_EVERY : round;
  const lampLabel = lit === SHOW_EVERY ? w.full : w.toGo(SHOW_EVERY - lit);

  const pillars = PILLAR_ORDER.filter((p) => cards.some((c) => c.pillar === p));
  const visible = filter === "all" ? cards : cards.filter((c) => c.pillar === filter);
  const text = shown ? cardText(shown, lang) : null;
  const other = shown ? cardText(shown, en ? "zh" : "en") : null;

  function releaseBalloons(n: number) {
    const batch = makeBalloons(n);
    setBalloons(batch);
    setTimeout(() => setBalloons([]), balloonLife(batch));
  }

  function bigShow(day: number, peek: boolean) {
    stopShow.current?.();
    setShow({ day, peek });
    buzz([15, 40, 15]);
    if (calm()) return;
    stopShow.current = playFireworks("finale", undefined, () => {
      stopShow.current = null;
      setShow(null);
    });
    releaseBalloons(12);
  }

  function closeShow() {
    stopShow.current?.();
    stopShow.current = null;
    setShow(null);
  }

  function turnOver() {
    setAnimated(true);
    writeSaved({ ...saved, seen: today });
  }

  function open(slug: string) {
    setAnimated(true);
    writeUrlCard(slug);
    stage.current?.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function another() {
    const others = cards.filter((c) => c.episode !== shown?.episode);
    if (others.length === 0) return;
    writeUrlCard(others[Math.floor(Math.random() * others.length)].episode);
  }

  function backToToday() {
    writeUrlCard("");
  }

  function markDone(e: React.MouseEvent<HTMLButtonElement>) {
    if (!shown || doneNow) return;
    const firstToday = !daysDone.has(today);
    const days = daysDone.size + (firstToday ? 1 : 0);
    writeSaved({ ...saved, done: [...saved.done, [shown.episode, today]] });
    if (firstToday && days % SHOW_EVERY === 0) {
      bigShow(days, false);
      return;
    }
    buzz(15);
    if (calm()) return;
    playFireworks("burst", { x: e.clientX, y: e.clientY });
    releaseBalloons(7);
  }

  function undo() {
    if (!shown) return;
    writeSaved({
      ...saved,
      done: saved.done.filter(([s, d]) => !(s === shown.episode && d === today)),
    });
  }

  async function saveImage() {
    if (!shown) return;
    const art = stage.current?.querySelector<SVGSVGElement>("svg[data-card-art]");
    if (!art) return;
    setSaving(true);
    try {
      const blob = await renderShareImage(shown, art, handle, lang);
      const name = `one-thing-ep${shown.noLabel}${en ? "-en" : ""}.png`;
      const file = new File([blob], name, { type: "image/png" });
      /* phones: the share sheet is the way into the photo album */
      const touch = window.matchMedia("(pointer: coarse)").matches;
      if (touch && navigator.canShare?.({ files: [file] })) {
        try {
          await navigator.share({ files: [file] });
          return;
        } catch (err) {
          if ((err as Error).name === "AbortError") return;
        }
      }
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = name;
      a.click();
      setTimeout(() => URL.revokeObjectURL(url), 4000);
    } finally {
      setSaving(false);
    }
  }

  const lamps = (
    <Lamps lit={lit} label={lampLabel} peek={w.peek} onPeek={() => bigShow(SHOW_EVERY, true)} />
  );
  const otherEdition = `${deckPath(en ? "zh" : "en")}${urlCard ? `?card=${urlCard}` : ""}`;

  return (
    <div lang={en ? "en" : "zh-Hans"}>
      {/* ── the stage ── */}
      <section
        ref={stage}
        className="grid scroll-mt-6 grid-cols-1 items-center gap-x-16 gap-y-10 pt-10 min-[900px]:grid-cols-[1fr_400px] min-[900px]:pt-14"
      >
        <div className="order-2 min-[900px]:order-1">
          {!shown && (
            <>
              <h2
                className={`${display} whitespace-pre-line text-[30px] leading-[1.25] min-[900px]:text-[38px]`}
              >
                {w.waitingTitle}
              </h2>
              <p className="mt-4 max-w-[440px] text-[16px] leading-[1.7] text-ink-2">
                {w.waitingBody}
              </p>
              <div className="mt-8">
                <BigButton primary onClick={turnOver} disabled={!today} lang={lang}>
                  {w.turn}
                  <svg
                    aria-hidden="true"
                    width="18"
                    height="18"
                    viewBox="0 0 18 18"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="1.8"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  >
                    <path d="M3 9h12M10 4l5 5-5 5" />
                  </svg>
                </BigButton>
              </div>
              {lamps}
            </>
          )}

          {shown && text && other && !doneNow && (
            <>
              <div className="meta !text-[11px]" lang="en">
                {isToday ? "Today’s card" : "Another card"} · Ep. {shown.no} ·{" "}
                {PILLARS[shown.pillar].en}
              </div>
              <h2
                className={`${display} mt-4 text-[30px] leading-[1.25] min-[900px]:text-[38px] ${
                  en ? "max-w-[460px] text-balance" : "whitespace-pre-line"
                }`}
              >
                {text.do}
              </h2>
              <p
                lang={en ? "zh-Hans" : "en"}
                className="mt-3 max-w-[440px] font-serif text-[17px] italic leading-[1.5] text-faint"
              >
                {other.do.replace(/\n/g, "")}
              </p>
              <div className="mt-8 flex flex-wrap items-center gap-3">
                <BigButton primary onClick={markDone} lang={lang}>
                  <svg
                    aria-hidden="true"
                    width="18"
                    height="18"
                    viewBox="0 0 18 18"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  >
                    <path d="M3.5 9.5l3.5 3.5 7.5-8" />
                  </svg>
                  {w.did}
                </BigButton>
                <BigButton onClick={another} lang={lang}>
                  {w.another}
                </BigButton>
              </div>
              <p className="mt-4 max-w-[440px] text-[14px] leading-[1.6] text-ink-2">
                {w.hint}
              </p>
              {!isToday && (
                <div className="mt-4">
                  <QuietButton onClick={backToToday}>{w.backToday}</QuietButton>
                </div>
              )}
              {lamps}
            </>
          )}

          {shown && text && doneNow && (
            <>
              <h2 className={`${display} text-[52px] leading-[1.1] min-[900px]:text-[64px]`}>
                {w.doneTitle}
              </h2>
              <p className="mt-3 max-w-[440px] text-[16px] leading-[1.7] text-ink-2">
                {text.do.replace(/\n/g, "")}
                <br />
                {w.count(saved.done.length)}
              </p>

              {isToday && tomorrowCard && (
                <div className="mt-6 flex max-w-[360px] items-center gap-4 rounded-[2px] bg-surface px-4 py-3">
                  <div
                    aria-hidden="true"
                    lang="zh-Hans"
                    className="zh-display flex h-[58px] w-[42px] flex-none rotate-[-5deg] items-center justify-center rounded-[6px] border-2 text-[17px]"
                    style={{
                      background: PILLARS[tomorrowCard.pillar].tint,
                      borderColor: INK,
                      color: INK,
                    }}
                  >
                    {w.tomorrowMark}
                  </div>
                  <div>
                    <div className="text-[13px] text-ink-2">
                      {w.tomorrow} ·{" "}
                      {en ? PILLARS[tomorrowCard.pillar].en : PILLARS[tomorrowCard.pillar].zh}
                    </div>
                    <div className={`${display} mt-0.5 text-[16px]`}>{w.tomorrowWait}</div>
                  </div>
                </div>
              )}

              <div className="mt-7 flex flex-wrap items-center gap-3">
                <BigButton primary onClick={saveImage} disabled={saving} lang={lang}>
                  <svg
                    aria-hidden="true"
                    width="18"
                    height="18"
                    viewBox="0 0 18 18"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="1.8"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  >
                    <path d="M9 2.500v9M5 8l4 4 4-4M3 15.500h12" />
                  </svg>
                  {saving ? w.saving : w.save}
                </BigButton>
                <BigButton onClick={another} lang={lang}>
                  {w.again}
                </BigButton>
              </div>
              <div className="mt-5 flex flex-wrap gap-x-6 gap-y-2">
                {!isToday && <QuietButton onClick={backToToday}>{w.backToday}</QuietButton>}
                <QuietButton onClick={undo}>{w.undo}</QuietButton>
              </div>
              {lamps}
            </>
          )}
        </div>

        <div className="order-1 mx-auto w-full max-w-[400px] min-[900px]:order-2">
          <div className="meta mb-3 flex justify-between !text-[11px]">
            <span className="flex gap-2 !normal-case !tracking-[0.08em]">
              {en ? (
                <a
                  href={otherEdition}
                  lang="zh-Hans"
                  className="transition-colors duration-[250ms] hover:text-accent"
                >
                  中文
                </a>
              ) : (
                <span className="text-ink">中文</span>
              )}
              <span aria-hidden="true">/</span>
              {en ? (
                <span className="text-ink">English</span>
              ) : (
                <a
                  href={otherEdition}
                  lang="en"
                  className="transition-colors duration-[250ms] hover:text-accent"
                >
                  English
                </a>
              )}
            </span>
            <span className="!normal-case !tracking-[0.08em]">
              {today ? dateLabel(today, lang) : " "}
            </span>
          </div>
          <div className="card-flip">
            <div
              className={`card-flip-inner ${animated ? "is-animated" : ""} ${
                shown ? "" : "is-back"
              }`}
            >
              <div className="card-flip-face">
                {shown ? (
                  <ActionCard card={shown} stamped={doneNow} lang={lang} />
                ) : (
                  <div className="aspect-[5/7] w-full" />
                )}
              </div>
              <div className="card-flip-back">
                {shown ? (
                  <CardBack label={today ? dateLabel(today, lang) : undefined} lang={lang} />
                ) : (
                  <button
                    type="button"
                    onClick={turnOver}
                    disabled={!today}
                    aria-label={w.flipLabel}
                    className="block w-full cursor-pointer text-left"
                  >
                    <CardBack label={today ? dateLabel(today, lang) : undefined} lang={lang} />
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── the whole deck ── */}
      <section className="mt-20 min-[900px]:mt-24">
        <div className="flex flex-wrap items-baseline justify-between gap-x-8 gap-y-3 border-t border-ink pt-6">
          <h2 className={`${display} text-[26px] leading-[1.2] min-[900px]:text-[30px]`}>
            {w.deck}
          </h2>
          <div className="meta !text-[11px]" lang="en">
            {en ? "" : "The whole deck · "}
            {cards.length} card{cards.length === 1 ? "" : "s"} · one per episode
          </div>
        </div>

        <div className="mt-6 flex flex-wrap gap-2.5">
          <button
            type="button"
            onClick={() => setFilter("all")}
            aria-pressed={filter === "all"}
            className={`h-[44px] rounded-full border-2 border-ink px-5 text-[15px] transition-colors duration-[250ms] ${
              en ? "font-serif font-semibold" : "zh-display"
            } ${filter === "all" ? "bg-ink text-paper" : "text-ink"}`}
          >
            {w.all} {cards.length}
          </button>
          {pillars.map((id) => {
            const n = cards.filter((c) => c.pillar === id).length;
            const on = filter === id;
            return (
              <button
                key={id}
                type="button"
                onClick={() => setFilter(on ? "all" : id)}
                aria-pressed={on}
                className={`h-[44px] rounded-full border-2 px-5 text-[15px] ${
                  en ? "font-serif font-semibold" : "zh-display"
                }`}
                style={{
                  borderColor: INK,
                  color: INK,
                  background: PILLARS[id].tint,
                  outline: on ? "2px solid var(--ink)" : "none",
                  outlineOffset: 2,
                }}
              >
                {en ? PILLARS[id].en : PILLARS[id].zh} {n}
              </button>
            );
          })}
        </div>

        <ul className="mt-8 grid grid-cols-2 gap-4 min-[700px]:grid-cols-3 min-[700px]:gap-5 min-[1000px]:grid-cols-4">
          {visible.map((c) => (
            <li key={c.episode} className="flex">
              <a
                href={`${deckPath(lang)}?card=${c.episode}`}
                onClick={(e) => {
                  if (e.metaKey || e.ctrlKey || e.shiftKey) return;
                  e.preventDefault();
                  open(c.episode);
                }}
                className="flex w-full transition-transform duration-[250ms] hover:-translate-y-1"
              >
                <ActionCard
                  card={c}
                  variant="mini"
                  stamped={everDone.has(c.episode)}
                  lang={lang}
                />
              </a>
            </li>
          ))}
        </ul>
      </section>

      <BalloonSky balloons={balloons} />

      {/* the eight-day show: the page turns to night for it */}
      {show &&
        createPortal(
          <button
            type="button"
            onClick={closeShow}
            lang={en ? "en" : "zh-Hans"}
            className="today-night fixed inset-0 z-[60] flex cursor-pointer flex-col items-center justify-center px-6 text-center"
          >
            <span
              className={`${display} text-[64px] leading-[1.1] min-[700px]:text-[120px]`}
              style={{ color: "#F9D65C" }}
            >
              {w.showTitle(show.day)}
            </span>
            <span
              className="mt-5 max-w-[520px] text-[18px] leading-[1.6] min-[700px]:text-[22px]"
              style={{ color: "#FBFAF7" }}
            >
              {show.peek ? w.showPeek : w.showLine}
            </span>
            <span
              className="mt-10 font-mono text-[11px] uppercase tracking-[0.14em]"
              style={{ color: "#B9B4A9" }}
            >
              {w.showClose}
            </span>
          </button>,
          document.body
        )}
    </div>
  );
}
