import { PILLARS, cardText, type DeckCard, type Lang } from "@/lib/today-deck";
import { CardArt } from "@/components/today/CardArt";

/*
 * One card of the /today deck, as a printed object: pillar-coloured border,
 * inner frame, the drawing, the action, the reason, a tear-off line to the
 * episode. Every measure is in cqw (the card's own width), so the same card
 * sets correctly at any size — the stage, the deck grid, an episode page.
 *
 * Colour fills a surface here and nowhere else on the site: a card is an
 * illustration (like a book cover), not interface. It is printed on its own
 * paper, so it looks the same in the light and the dark theme.
 *
 * Two editions: 中文 (the original) and English (lang="en") — same card, same
 * drawing, the lettering changes.
 */

const INK = "#1F1D1A";

function Stamp({ small = false, lang }: { small?: boolean; lang: Lang }) {
  const en = lang === "en";
  return (
    <div
      className={`pointer-events-none absolute rotate-[-12deg] rounded-full bg-[#FFFDF8] leading-none ${
        en ? "font-serif font-semibold tracking-[0.08em]" : "zh-display"
      } ${
        small
          ? "right-[5cqw] top-[5cqw] border-[1cqw] px-[4cqw] py-[2.2cqw] text-[7cqw]"
          : "right-[4cqw] top-[4cqw] border-[0.8cqw] px-[3.2cqw] py-[1.8cqw] text-[5.6cqw]"
      }`}
      style={{ borderColor: "#96610F", color: "#96610F" }}
    >
      {en ? "DONE" : "做到了"}
    </div>
  );
}

export function ActionCard({
  card,
  variant = "full",
  stamped = false,
  linkEpisode = true,
  lang = "zh",
}: {
  card: DeckCard;
  /** "full" = the whole card; "mini" = drawing + action only, for the deck grid. */
  variant?: "full" | "mini";
  /** Show the done stamp. */
  stamped?: boolean;
  /** Full variant: make the tear-off footer a link to the episode. */
  linkEpisode?: boolean;
  /** Which edition of the card to print. */
  lang?: Lang;
}) {
  const p = PILLARS[card.pillar];
  const t = cardText(card, lang);
  const en = lang === "en";
  const mini = variant === "mini";
  const label = en
    ? `${p.en} · Episode ${card.no} · ${t.do}`
    : `${p.zh} · 第 ${card.no} 集 · ${t.do.replace(/\n/g, "")}`;

  const footer = (
    <>
      <span className="flex items-center gap-[2.5cqw]">
        <svg
          aria-hidden="true"
          viewBox="0 0 28 28"
          className="h-[7cqw] w-[7cqw] flex-none"
        >
          <circle cx="14" cy="14" r="14" fill={INK} />
          <path d="M11.5 9v10l7.5-5z" fill={p.tint} />
        </svg>
        {en ? (
          <span>
            Watch Ep. {card.no}
            <span className="font-normal text-[#57534A]"> · in Chinese</span>
          </span>
        ) : (
          <>看第 {card.no} 集</>
        )}
      </span>
      {card.duration && (
        <span className="font-mono text-[2.75cqw] font-normal tracking-[0.14em]">
          {card.duration}
        </span>
      )}
    </>
  );
  const footerClass =
    "flex h-[13cqw] flex-none items-center justify-between border-t-2 border-dashed px-[4cqw] text-[3.5cqw] font-semibold";

  const doClass = en
    ? `font-serif font-semibold tracking-[-0.01em] text-balance ${
        mini ? "text-[7cqw] leading-[1.2]" : "text-[6.5cqw] leading-[1.18]"
      }`
    : `zh-display whitespace-pre-line ${
        mini ? "text-[8cqw] leading-[1.32]" : "text-[7.25cqw] leading-[1.3]"
      }`;

  return (
    <div className="@container flex w-full">
      <article
        lang={en ? "en" : "zh-Hans"}
        className={`flex w-full overflow-hidden border-2 ${
          mini ? "rounded-[7cqw] p-[4cqw]" : "aspect-[5/7] rounded-[6cqw] p-[3.5cqw]"
        }`}
        style={{ background: p.tint, borderColor: INK, color: INK }}
      >
        <div
          className={`relative flex min-w-0 flex-1 flex-col overflow-hidden border-2 bg-[#FFFDF8] ${
            mini ? "rounded-[4cqw]" : "rounded-[3.5cqw]"
          }`}
          style={{ borderColor: INK }}
        >
          <div
            className="relative flex-none border-b-2"
            style={{ background: p.wash, borderColor: INK }}
          >
            <CardArt slug={card.episode} pillar={card.pillar} label={label} lang={lang} />
            <div
              className={`absolute flex items-baseline ${
                mini
                  ? "left-[4cqw] top-[3cqw] gap-[2cqw]"
                  : "left-[3cqw] top-[2.5cqw] gap-[1.5cqw]"
              }`}
            >
              <span
                lang="en"
                className={`font-serif font-semibold leading-none ${
                  mini ? "text-[9cqw]" : "text-[7.5cqw]"
                }`}
              >
                {card.noLabel}
              </span>
              {/* the English pillar name runs too long to share the corner
                  with the drawing — it sits above the action instead */}
              {!en && (
                <span className={`zh-display ${mini ? "text-[4.5cqw]" : "text-[3.5cqw]"}`}>
                  {p.zh}
                </span>
              )}
            </div>
            {!mini && t.when && (
              <div
                className={`absolute bottom-[2.5cqw] right-[2.5cqw] rotate-[4deg] rounded-full border-2 bg-[#F2B632] px-[3cqw] py-[1.2cqw] leading-[1.25] ${
                  en ? "font-serif text-[3.3cqw] font-semibold" : "zh-display text-[3.25cqw]"
                }`}
                style={{ borderColor: INK }}
              >
                {t.when}
              </div>
            )}
          </div>

          {mini ? (
            <div className="px-[5.5cqw] pb-[6.5cqw] pt-[5.5cqw]">
              <h3 className={doClass}>{t.do}</h3>
            </div>
          ) : (
            <>
              <div className="flex min-h-0 flex-1 flex-col px-[5cqw] pt-[4.5cqw]">
                {en && (
                  <div className="mb-[1.6cqw] font-mono text-[2.6cqw] uppercase tracking-[0.14em] text-[#57534A]">
                    {p.en}
                  </div>
                )}
                <h3 className={doClass}>{t.do}</h3>
                <p
                  className={`mt-[2.5cqw] text-[#57534A] ${
                    en ? "text-[3.6cqw] leading-[1.5]" : "text-[3.75cqw] leading-[1.6]"
                  }`}
                >
                  {t.why}
                </p>
              </div>
              {linkEpisode ? (
                <a
                  href={card.href}
                  className={`${footerClass} transition-colors duration-[250ms] hover:bg-[#F4F2ED]`}
                  style={{ borderColor: INK }}
                >
                  {footer}
                </a>
              ) : (
                <div className={footerClass} style={{ borderColor: INK }}>
                  {footer}
                </div>
              )}
            </>
          )}

          {stamped && <Stamp small={mini} lang={lang} />}
        </div>
      </article>
    </div>
  );
}

/** The back of every card — what the deck shows before the day's card is turned. */
export function CardBack({ label, lang = "zh" }: { label?: string; lang?: Lang }) {
  const en = lang === "en";
  return (
    <div className="@container w-full">
      <div
        aria-hidden="true"
        className="flex aspect-[5/7] w-full overflow-hidden rounded-[6cqw] border-2 p-[3.5cqw]"
        style={{ background: "#FBF3DC", borderColor: INK, color: INK }}
      >
        <div
          className="flex min-w-0 flex-1 flex-col items-center justify-between rounded-[3.5cqw] border-2 py-[8cqw]"
          style={{ borderColor: INK }}
        >
          <span className="font-mono text-[3cqw] tracking-[0.22em]">
            ONE THING TODAY
          </span>
          <svg
            viewBox="0 0 150 150"
            className="w-[56cqw]"
            fill="none"
            stroke={INK}
            strokeWidth={1.2}
          >
            <circle cx="75" cy="75" r="70" />
            <circle cx="75" cy="75" r="58" strokeDasharray="2 6" />
            <path
              d="M75 5v140M5 75h140M25.5 25.5l99 99M124.500 25.500l-99 99"
              strokeWidth={0.6}
            />
            <circle cx="75" cy="75" r="40" fill="#FBF3DC" />
            <text
              x="75"
              y="97"
              textAnchor="middle"
              fontSize="62"
              fill={INK}
              stroke="none"
              className="zh-display"
            >
              今
            </text>
          </svg>
          {en ? (
            <span className="font-mono text-[3cqw] uppercase tracking-[0.22em]">
              {label ?? "one a day"}
            </span>
          ) : (
            <span lang="zh-Hans" className="zh-display text-[4cqw] tracking-[0.12em]">
              {label ?? "每天一张"}
            </span>
          )}
        </div>
      </div>
    </div>
  );
}
