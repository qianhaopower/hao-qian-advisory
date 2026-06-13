"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";

// Optimized WebP variants (the 2.26 MB PNG is kept only as a fallback).
const COVER_THUMB = "/friendsintelligence/cover-768.webp";
const COVER_FULL = "/friendsintelligence/cover-1280.webp";
const COVER_FALLBACK = "/friendsintelligence/cover.png";

export function FriendsBookCover() {
  const [mounted, setMounted] = useState(false);
  const [open, setOpen] = useState(false);
  const [entered, setEntered] = useState(false);

  const triggerRef = useRef<HTMLButtonElement>(null);
  const closeBtnRef = useRef<HTMLButtonElement>(null);
  const closeTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => setMounted(true), []);

  const openModal = useCallback(() => {
    if (closeTimer.current) clearTimeout(closeTimer.current);
    setOpen(true);
  }, []);

  const closeModal = useCallback(() => {
    setEntered(false);
    // Let the exit transition finish before unmounting, then restore focus.
    closeTimer.current = setTimeout(() => {
      setOpen(false);
      triggerRef.current?.focus();
    }, 220);
  }, []);

  useEffect(() => {
    if (!open) return;

    // Lock page scroll while the modal is open.
    const prevOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";

    // Trigger the enter animation on the next frame, and move focus in.
    const enterRaf = requestAnimationFrame(() => {
      setEntered(true);
      closeBtnRef.current?.focus();
    });

    const onKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        e.preventDefault();
        closeModal();
      } else if (e.key === "Tab") {
        // Only the close button is interactive — keep focus contained.
        e.preventDefault();
        closeBtnRef.current?.focus();
      }
    };
    document.addEventListener("keydown", onKeyDown);

    return () => {
      document.body.style.overflow = prevOverflow;
      document.removeEventListener("keydown", onKeyDown);
      cancelAnimationFrame(enterRaf);
    };
  }, [open, closeModal]);

  useEffect(() => {
    return () => {
      if (closeTimer.current) clearTimeout(closeTimer.current);
    };
  }, []);

  return (
    <>
      <button
        ref={triggerRef}
        type="button"
        onClick={openModal}
        aria-haspopup="dialog"
        aria-label="Enlarge the Friends Intelligence book cover"
        className="group relative block cursor-pointer rounded-lg outline-none focus-visible:ring-2 focus-visible:ring-[#d6a441]/70 focus-visible:ring-offset-2 focus-visible:ring-offset-[#0d1626]"
      >
        <picture>
          <source srcSet={COVER_THUMB} type="image/webp" />
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={COVER_FALLBACK}
            alt="Friends Intelligence — book cover"
            width={336}
            height={538}
            fetchPriority="high"
            decoding="async"
            className="w-56 rounded-lg shadow-[0_36px_80px_-28px_rgba(0,0,0,0.85)] ring-1 ring-white/10 transition duration-300 ease-out group-hover:scale-[1.02] group-hover:shadow-[0_46px_94px_-26px_rgba(0,0,0,0.92)] sm:w-72 md:w-[21rem]"
          />
        </picture>

        {/* Subtle affordance that the cover can be enlarged (esp. on touch) */}
        <span
          aria-hidden="true"
          className="pointer-events-none absolute bottom-3 right-3 flex h-8 w-8 items-center justify-center rounded-md border border-white/15 bg-black/30 text-[#f4efe3]/80 backdrop-blur-sm transition duration-300 group-hover:bg-black/45 group-hover:text-[#f4efe3]"
        >
          <svg
            width="14"
            height="14"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            aria-hidden="true"
          >
            <path d="M8 3H5a2 2 0 0 0-2 2v3" />
            <path d="M21 8V5a2 2 0 0 0-2-2h-3" />
            <path d="M3 16v3a2 2 0 0 0 2 2h3" />
            <path d="M16 21h3a2 2 0 0 0 2-2v-3" />
          </svg>
        </span>
      </button>

      {mounted && open
        ? createPortal(
            <div
              role="dialog"
              aria-modal="true"
              aria-label="Friends Intelligence book cover"
              className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6"
            >
              {/* Backdrop — click outside to close */}
              <div
                aria-hidden="true"
                onClick={closeModal}
                className={`absolute inset-0 bg-[#0a121f]/85 backdrop-blur-sm transition-opacity duration-300 ease-out ${
                  entered ? "opacity-100" : "opacity-0"
                }`}
              />

              {/* Close button */}
              <button
                ref={closeBtnRef}
                type="button"
                onClick={closeModal}
                aria-label="Close"
                className={`absolute right-4 top-4 z-10 flex h-11 w-11 items-center justify-center rounded-full border border-white/15 bg-white/10 text-[#f4efe3] backdrop-blur-sm transition duration-300 ease-out hover:bg-white/20 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#d6a441]/70 sm:right-6 sm:top-6 ${
                  entered ? "opacity-100" : "opacity-0"
                }`}
              >
                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="1.8"
                  strokeLinecap="round"
                  aria-hidden="true"
                >
                  <path d="M6 6l12 12M18 6L6 18" />
                </svg>
              </button>

              {/* Enlarged cover */}
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src={COVER_FULL}
                alt="Friends Intelligence — book cover, enlarged"
                className={`relative max-h-[82vh] w-auto max-w-[90vw] rounded-lg shadow-[0_50px_120px_-30px_rgba(0,0,0,0.9)] ring-1 ring-white/10 transition-all duration-300 ease-out ${
                  entered ? "scale-100 opacity-100" : "scale-[0.96] opacity-0"
                }`}
              />
            </div>,
            document.body,
          )
        : null}
    </>
  );
}
