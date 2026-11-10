"use client";

import { useMemo, useRef, useState, useSyncExternalStore } from "react";
import {
  PILLARS,
  PILLAR_ORDER,
  cardForDay,
  dateKey,
  dateLabel,
  dayNumber,
  type DeckCard,
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

/*
 * 今天只做一件事 — the stage and the deck.
 *
 * One card a day, the same card for everyone (lib/today-deck.cardForDay).
 * What the visitor did lives only in their own browser (localStorage): no
 * accounts, no server, and no counts of anybody else. The card on the stage
 * is whatever ?card= names, so every card has a link of its own.
 */

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

/* ── small pieces ─────────────────────────────────────────────────────── */

const INK = "#1F1D1A";

function BigButton({
  children,
  onClick,
  primary = false,
  disabled = false,
}: {
  children: React.ReactNode;
  onClick: () => void;
  primary?: boolean;
  disabled?: boolean;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      className={`zh-display inline-flex h-[56px] items-center justify-center gap-2.5 rounded-full border-2 px-7 text-[18px] tracking-[0.04em] transition-colors duration-[250ms] disabled:opacity-60 ${
        primary
          ? "bg-[#1F1D1A] text-[#FBFAF7] hover:bg-[#3A362F]"
          : "bg-transparent text-[#1F1D1A] hover:bg-surface"
      }`}
      style={{ borderColor: INK }}
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

/* ── the room ─────────────────────────────────────────────────────────── */

export function TodayDeck({ cards, handle }: { cards: DeckCard[]; handle: string }) {
  const today = useSyncExternalStore(subscribe, () => dateKey(new Date()), empty);
  const savedRaw = useSyncExternalStore(subscribe, readSaved, empty);
  const urlCard = useSyncExternalStore(subscribe, readUrlCard, empty);
  const saved = useMemo(() => parseSaved(savedRaw), [savedRaw]);

  const [animated, setAnimated] = useState(false);
  const [filter, setFilter] = useState<PillarId | "all">("all");
  const [balloons, setBalloons] = useState<Balloon[]>([]);
  const [saving, setSaving] = useState(false);
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

  const pillars = PILLAR_ORDER.filter((p) => cards.some((c) => c.pillar === p));
  const visible = filter === "all" ? cards : cards.filter((c) => c.pillar === filter);

  function turnOver() {
    setAnimated(true);
    writeSaved({ ...saved, seen: today });
  }

  function show(slug: string) {
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

  function markDone() {
    if (!shown || doneNow) return;
    writeSaved({ ...saved, done: [...saved.done, [shown.episode, today]] });
    if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      const batch = makeBalloons(7);
      setBalloons(batch);
      setTimeout(() => setBalloons([]), balloonLife(batch));
    }
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
      const blob = await renderShareImage(shown, art, handle);
      const name = `one-thing-ep${shown.noLabel}.png`;
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

  return (
    <div lang="zh-Hans">
      {/* ── the stage ── */}
      <section
        ref={stage}
        className="grid scroll-mt-6 grid-cols-1 items-center gap-x-16 gap-y-10 pt-10 min-[900px]:grid-cols-[1fr_400px] min-[900px]:pt-14"
      >
        <div className="order-2 min-[900px]:order-1">
          {!shown && (
            <>
              <h2 className="zh-display text-[30px] leading-[1.25] min-[900px]:text-[38px]">
                今天这一张，
                <br />
                还没翻开。
              </h2>
              <p className="mt-4 max-w-[440px] text-[16px] leading-[1.7] text-ink-2">
                不用改变人生。翻一张，做一件，就够了。
              </p>
              <div className="mt-8">
                <BigButton primary onClick={turnOver} disabled={!today}>
                  翻开今天这一张
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
            </>
          )}

          {shown && !doneNow && (
            <>
              <div className="meta !text-[11px]" lang="en">
                {isToday ? "Today’s card" : "Another card"} · Ep. {shown.no} ·{" "}
                {PILLARS[shown.pillar].en}
              </div>
              <h2 className="zh-display mt-4 whitespace-pre-line text-[30px] leading-[1.25] min-[900px]:text-[38px]">
                {shown.do}
              </h2>
              <p
                lang="en"
                className="mt-3 max-w-[440px] font-serif text-[17px] italic leading-[1.5] text-faint"
              >
                {shown.en}
              </p>
              <div className="mt-8 flex flex-wrap items-center gap-3">
                <BigButton primary onClick={markDone}>
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
                  做了
                </BigButton>
                <BigButton onClick={another}>换一张</BigButton>
              </div>
              {!isToday && (
                <div className="mt-5">
                  <QuietButton onClick={backToToday}>回到今天这一张</QuietButton>
                </div>
              )}
            </>
          )}

          {shown && doneNow && (
            <>
              <h2 className="zh-display text-[52px] leading-[1.1] min-[900px]:text-[64px]">
                做了。
              </h2>
              <p className="mt-3 max-w-[440px] text-[16px] leading-[1.7] text-ink-2">
                {shown.do.replace(/\n/g, "")}
                <br />
                这是你做的第 {saved.done.length} 件。
              </p>

              {isToday && tomorrowCard && (
                <div className="mt-6 flex max-w-[360px] items-center gap-4 rounded-[2px] bg-surface px-4 py-3">
                  <div
                    aria-hidden="true"
                    className="zh-display flex h-[58px] w-[42px] flex-none rotate-[-5deg] items-center justify-center rounded-[6px] border-2 text-[17px]"
                    style={{
                      background: PILLARS[tomorrowCard.pillar].tint,
                      borderColor: INK,
                    }}
                  >
                    明
                  </div>
                  <div>
                    <div className="text-[13px] text-ink-2">
                      明天这一张 · {PILLARS[tomorrowCard.pillar].zh}
                    </div>
                    <div className="zh-display mt-0.5 text-[16px]">明早才能翻开</div>
                  </div>
                </div>
              )}

              <div className="mt-7 flex flex-wrap items-center gap-3">
                <BigButton primary onClick={saveImage} disabled={saving}>
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
                  {saving ? "正在画…" : "存成图片"}
                </BigButton>
                <BigButton onClick={another}>再看一张</BigButton>
              </div>
              <div className="mt-5 flex flex-wrap gap-x-6 gap-y-2">
                {!isToday && (
                  <QuietButton onClick={backToToday}>回到今天这一张</QuietButton>
                )}
                <QuietButton onClick={undo}>点错了，撤销</QuietButton>
              </div>
            </>
          )}
        </div>

        <div className="order-1 mx-auto w-full max-w-[400px] min-[900px]:order-2">
          <div className="meta mb-3 flex justify-between !text-[11px]">
            <span lang="en">haoqian.co / today</span>
            <span className="!normal-case !tracking-[0.08em]">
              {today ? dateLabel(today) : " "}
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
                  <ActionCard card={shown} stamped={doneNow} />
                ) : (
                  <div className="aspect-[5/7] w-full" />
                )}
              </div>
              <div className="card-flip-back">
                {shown ? (
                  <CardBack label={today ? dateLabel(today) : undefined} />
                ) : (
                  <button
                    type="button"
                    onClick={turnOver}
                    disabled={!today}
                    aria-label="翻开今天这一张"
                    className="block w-full cursor-pointer text-left"
                  >
                    <CardBack label={today ? dateLabel(today) : undefined} />
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
          <h2 className="zh-display text-[26px] leading-[1.2] min-[900px]:text-[30px]">
            整副牌
          </h2>
          <div className="meta !text-[11px]" lang="en">
            The whole deck · {cards.length} card{cards.length === 1 ? "" : "s"} ·
            one per episode
          </div>
        </div>

        <div className="mt-6 flex flex-wrap gap-2.5">
          <button
            type="button"
            onClick={() => setFilter("all")}
            aria-pressed={filter === "all"}
            className={`zh-display h-[44px] rounded-full border-2 px-5 text-[15px] transition-colors duration-[250ms] ${
              filter === "all" ? "bg-[#1F1D1A] text-[#FBFAF7]" : "text-[#1F1D1A]"
            }`}
            style={{ borderColor: INK }}
          >
            全部 {cards.length}
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
                className="zh-display h-[44px] rounded-full border-2 px-5 text-[15px] text-[#1F1D1A]"
                style={{
                  borderColor: INK,
                  background: PILLARS[id].tint,
                  outline: on ? `2px solid ${INK}` : "none",
                  outlineOffset: 2,
                }}
              >
                {PILLARS[id].zh} {n}
              </button>
            );
          })}
        </div>

        <ul className="mt-8 grid grid-cols-2 gap-4 min-[700px]:grid-cols-3 min-[700px]:gap-5 min-[1000px]:grid-cols-4">
          {visible.map((c) => (
            <li key={c.episode} className="flex">
              <a
                href={`/today?card=${c.episode}`}
                onClick={(e) => {
                  if (e.metaKey || e.ctrlKey || e.shiftKey) return;
                  e.preventDefault();
                  show(c.episode);
                }}
                className="flex w-full transition-transform duration-[250ms] hover:-translate-y-1"
              >
                <ActionCard
                  card={c}
                  variant="mini"
                  stamped={everDone.has(c.episode)}
                />
              </a>
            </li>
          ))}
        </ul>
      </section>

      <BalloonSky balloons={balloons} />
    </div>
  );
}
