"use client";

import { useCallback, useEffect, useState } from "react";
import { createPortal } from "react-dom";
import type { BalloonArchiveItem } from "@/content/balloon-archive";

/*
 * The works grid with a lightbox — click a balloon to see it big.
 * No library: a fixed overlay in the library's own light palette,
 * ← → to browse, Esc / backdrop / ✕ to close.
 */

function archiveDate(iso: string): string {
  const d = new Date(`${iso}T00:00:00`);
  if (Number.isNaN(d.getTime())) return iso;
  return d
    .toLocaleDateString("en-AU", { month: "short", year: "numeric" })
    .toUpperCase();
}

export function BalloonGallery({
  items,
  crop = true,
}: {
  items: BalloonArchiveItem[];
  /** true → square tiles (product shots); false → natural aspect (street photos) */
  crop?: boolean;
}) {
  const [open, setOpen] = useState<number | null>(null);

  const step = useCallback(
    (dir: number) => {
      setOpen((cur) =>
        cur === null ? cur : (cur + dir + items.length) % items.length
      );
    },
    [items.length]
  );

  useEffect(() => {
    if (open === null) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") setOpen(null);
      if (e.key === "ArrowLeft") step(-1);
      if (e.key === "ArrowRight") step(1);
    };
    window.addEventListener("keydown", onKey);
    const prevOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      window.removeEventListener("keydown", onKey);
      document.body.style.overflow = prevOverflow;
    };
  }, [open, step]);

  const current = open === null ? null : items[open];

  return (
    <>
      <div
        className={
          crop
            ? "mt-6 grid grid-cols-2 gap-4 min-[700px]:grid-cols-3 min-[1000px]:grid-cols-4"
            : "mt-6 grid grid-cols-1 gap-6 min-[700px]:grid-cols-2"
        }
      >
        {items.map((item, i) => (
          <figure key={item.src}>
            <button
              type="button"
              onClick={() => setOpen(i)}
              aria-label={`View balloon work ${i + 1} of ${items.length} full size`}
              className="block w-full cursor-zoom-in overflow-hidden rounded-[2px] border border-line transition-colors duration-[250ms] hover:border-ink-3"
            >
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src={item.src}
                alt={item.caption || "Balloon work by Little Wow Balloons"}
                loading="lazy"
                className={
                  crop
                    ? "block aspect-square w-full object-cover"
                    : "block w-full"
                }
              />
            </button>
            <figcaption className="mt-2">
              {item.date && (
                <span className="meta !text-[10.5px]">
                  {archiveDate(item.date)}
                </span>
              )}
              {item.caption && (
                <span className="mt-1 block text-[13px] leading-[1.55] text-ink-2">
                  {item.caption}
                </span>
              )}
            </figcaption>
          </figure>
        ))}
      </div>

      {current &&
        createPortal(
          <div
            role="dialog"
            aria-modal="true"
            aria-label="Balloon work, full size"
            className="fixed inset-0 z-50 flex flex-col items-center justify-center bg-paper/95 px-6 py-10"
            onClick={() => setOpen(null)}
          >
          <div
            className="fade-up flex max-h-full max-w-full flex-col items-center"
            onClick={(e) => e.stopPropagation()}
          >
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={current.src}
              alt={current.caption || "Balloon work by Little Wow Balloons"}
              className="max-h-[78vh] max-w-full rounded-[2px] border border-line object-contain"
            />
            <div className="mt-4 flex items-baseline gap-6">
              <button
                type="button"
                onClick={() => step(-1)}
                aria-label="Previous work"
                className="meta !text-[12px] cursor-pointer text-ink-2 transition-colors duration-[250ms] hover:text-accent"
              >
                ←
              </button>
              <span className="meta !text-[11px]">
                {(open ?? 0) + 1} / {items.length}
                {current.date ? ` · ${archiveDate(current.date)}` : ""}
              </span>
              <button
                type="button"
                onClick={() => step(1)}
                aria-label="Next work"
                className="meta !text-[12px] cursor-pointer text-ink-2 transition-colors duration-[250ms] hover:text-accent"
              >
                →
              </button>
            </div>
            {current.caption && (
              <p className="mt-2 max-w-[520px] text-center text-[13.5px] leading-[1.6] text-ink-2">
                {current.caption}
              </p>
            )}
          </div>
            <button
              type="button"
              onClick={() => setOpen(null)}
              aria-label="Close"
              className="meta !text-[12px] absolute right-6 top-6 cursor-pointer text-ink-2 transition-colors duration-[250ms] hover:text-accent"
            >
              ✕ close
            </button>
          </div>,
          document.body
        )}
    </>
  );
}
