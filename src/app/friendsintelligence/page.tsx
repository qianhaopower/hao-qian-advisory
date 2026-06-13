import type { Metadata } from "next";
import { FriendsBookCover } from "@/components/FriendsBookCover";
import { FriendsCountdown } from "@/components/FriendsCountdown";
import { FriendsSignupForm } from "@/components/FriendsSignupForm";

export const metadata: Metadata = {
  title: "Friends Intelligence",
  description:
    "Friends Intelligence — a new book by Hao Qian. A Life Operating System for Better Decisions and Energy. Coming soon.",
};

export default function FriendsIntelligencePage() {
  return (
    <main className="min-h-screen bg-[#0d1626] bg-[radial-gradient(circle_at_50%_20%,#1b2c4b_0%,#0d1626_60%)] text-[#f4efe3]">
      <div className="mx-auto flex min-h-screen max-w-xl flex-col items-center px-6 py-10 text-center md:py-16">
        {/* Book cover — the hero of the page (click to enlarge) */}
        <FriendsBookCover />

        {/* Title — sits below the cover in the hierarchy */}
        <h1 className="mt-6 text-2xl font-semibold uppercase leading-tight tracking-[0.16em] text-[#f4efe3] sm:text-3xl md:mt-7 md:text-4xl">
          Friends Intelligence
        </h1>

        {/* Subtitle */}
        <p className="mt-2.5 max-w-md text-[15px] leading-relaxed text-[#c9c3b4] sm:text-base md:mt-3">
          A Life Operating System for Better Decisions and Energy
        </p>

        {/* Countdown — the second visual focus */}
        <div className="mt-7 md:mt-9">
          <FriendsCountdown />
        </div>

        {/* Email signup */}
        <div className="mt-7 w-full max-w-md md:mt-9">
          <FriendsSignupForm />
        </div>

        {/* Author */}
        <div className="mt-8 md:mt-10">
          <p className="text-sm uppercase tracking-[0.3em] text-[#cfc8b8]">
            By Hao Qian
          </p>
          <p className="mt-2 text-[11px] tracking-[0.12em] text-[#8b8576]">
            Author of Friends Intelligence
          </p>
        </div>

        {/* Footer link back to the homepage */}
        <footer className="mt-10 border-t border-white/10 pt-5 md:mt-12">
          <a
            href="/"
            className="text-xs tracking-wide text-[#8b8576] transition hover:text-[#d6a441]"
          >
            ← Back to haoqian.co
          </a>
        </footer>
      </div>
    </main>
  );
}
