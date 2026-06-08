"use client";

import { useState } from "react";
import { Check, Copy, Download, Link2, RotateCcw, Share2 } from "lucide-react";
import { BattleResult } from "@wcf/types";
import { copyText, resultToText } from "@wcf/lib/copy";
import { hypeTier } from "@wcf/lib/battle";
import { downloadElementAsImage } from "@wcf/lib/screenshot";
import { trackEvent } from "@wcf/lib/track";
import {
  canNativeShare,
  getShareText,
  getShareUrl,
  getSocialUrl,
  nativeShare,
  openShareWindow,
  ShareTarget,
} from "@wcf/lib/share";

const SOCIALS: { target: ShareTarget; label: string; bg: string }[] = [
  { target: "x", label: "X", bg: "#000000" },
  { target: "whatsapp", label: "WhatsApp", bg: "#25D366" },
  { target: "facebook", label: "Facebook", bg: "#1877F2" },
  { target: "reddit", label: "Reddit", bg: "#FF4500" },
  { target: "telegram", label: "Telegram", bg: "#229ED9" },
];

type ResultCardProps = {
  result: BattleResult;
  onFightAgain: () => void;
};

const CARD_ID = "result-card";

export default function ResultCard({ result, onFightAgain }: ResultCardProps) {
  const [copied, setCopied] = useState(false);
  const [downloading, setDownloading] = useState(false);
  const [shareOpen, setShareOpen] = useState(false);
  const [linkCopied, setLinkCopied] = useState(false);

  const { winner, loser } = result;

  const shareText = getShareText(result);
  const shareUrl = getShareUrl(winner.id, loser.id);

  async function handleCopy() {
    const ok = await copyText(resultToText(result));
    if (ok) {
      setCopied(true);
      setTimeout(() => setCopied(false), 1800);
    }
  }

  async function handleDownload() {
    setDownloading(true);
    try {
      await downloadElementAsImage(
        CARD_ID,
        `wcfs-${winner.code}-vs-${loser.code}.png`
      );
      trackEvent("result_downloaded");
    } finally {
      setDownloading(false);
    }
  }

  // Main share action: drop a shareable link on the clipboard and reveal the
  // one-click social buttons.
  async function handleShare() {
    const ok = await copyText(`${shareText} ${shareUrl}`);
    if (ok) {
      setLinkCopied(true);
      setTimeout(() => setLinkCopied(false), 2000);
    }
    setShareOpen((open) => !open);
  }

  async function handleCopyLink() {
    const ok = await copyText(shareUrl);
    if (ok) {
      setLinkCopied(true);
      setTimeout(() => setLinkCopied(false), 2000);
    }
  }

  return (
    <div className="mx-auto flex w-full max-w-md flex-col gap-4">
      {/* Captured card — colors are inline (hex/rgba) so html2canvas can render them */}
      <div
        id={CARD_ID}
        style={{
          background: `linear-gradient(160deg, #0b1020 0%, #12182f 60%, ${winner.primaryColor}22 100%)`,
          border: `1px solid ${winner.primaryColor}66`,
          borderRadius: 24,
          padding: 24,
          color: "#ffffff",
          boxShadow: `0 0 40px ${winner.primaryColor}40`,
          fontFamily:
            "ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, sans-serif",
        }}
      >
        {/* Header */}
        <div
          style={{
            textAlign: "center",
            fontSize: 11,
            letterSpacing: "0.28em",
            fontWeight: 800,
            color: "rgba(255,255,255,0.55)",
            textTransform: "uppercase",
          }}
        >
          World Cup Fight Simulator
        </div>

        <div
          style={{
            textAlign: "center",
            marginTop: 6,
            fontSize: 14,
            fontWeight: 700,
            color: "rgba(255,255,255,0.85)",
          }}
        >
          {winner.flag} {winner.code} <span style={{ opacity: 0.5 }}>vs</span>{" "}
          {loser.code} {loser.flag}
        </div>

        {/* Winner */}
        <div style={{ textAlign: "center", marginTop: 18 }}>
          <div
            style={{
              fontSize: 11,
              letterSpacing: "0.2em",
              fontWeight: 800,
              color: "rgba(255,255,255,0.5)",
              textTransform: "uppercase",
            }}
          >
            Winner
          </div>
          <div style={{ fontSize: 44, lineHeight: 1.1, marginTop: 4 }}>
            {winner.flag}
          </div>
          <div
            style={{
              fontSize: 28,
              fontWeight: 900,
              marginTop: 2,
              color: "#ffffff",
            }}
          >
            {winner.name}
          </div>
        </div>

        {/* Victory type + reality risk */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1fr 1fr",
            gap: 10,
            marginTop: 18,
          }}
        >
          <Stat label="Victory Type" value={result.victoryType} />
          <Stat
            label="Hype Level"
            value={`${hypeTier(result.hypeLevel)} · ${result.hypeLevel}%`}
          />
        </div>

        {/* Hype level bar */}
        <div
          style={{
            marginTop: 10,
            height: 8,
            width: "100%",
            borderRadius: 999,
            background: "rgba(255,255,255,0.1)",
            overflow: "hidden",
          }}
        >
          <div
            style={{
              height: "100%",
              width: `${result.hypeLevel}%`,
              borderRadius: 999,
              background: "linear-gradient(90deg, #f59e0b, #f97316, #ef4444)",
            }}
          />
        </div>

        {/* Damage report */}
        <div style={{ marginTop: 18 }}>
          <SectionLabel>Damage Report</SectionLabel>
          <ul style={{ marginTop: 8, display: "grid", gap: 6 }}>
            {result.damageReport.map((item, i) => (
              <li
                key={i}
                style={{
                  display: "flex",
                  alignItems: "baseline",
                  gap: 8,
                  fontSize: 14,
                  color: "rgba(255,255,255,0.9)",
                }}
              >
                <span style={{ flexShrink: 0, fontSize: 12, lineHeight: 1.4 }}>
                  💥
                </span>
                <span>{renderDamageLine(item)}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* VAR decision */}
        <div style={{ marginTop: 18 }}>
          <SectionLabel>VAR Decision</SectionLabel>
          <div
            style={{
              marginTop: 6,
              fontSize: 14,
              fontStyle: "italic",
              color: "rgba(255,255,255,0.8)",
            }}
          >
            {result.varDecision}
          </div>
        </div>

        {/* One-liner */}
        <div
          style={{
            marginTop: 18,
            padding: 14,
            borderRadius: 14,
            background: "rgba(255,255,255,0.06)",
            border: "1px solid rgba(255,255,255,0.08)",
            fontSize: 15,
            fontWeight: 700,
            textAlign: "center",
            color: "#ffffff",
          }}
        >
          “{result.oneLiner}”
        </div>

        {/* Footer */}
        <div
          style={{
            marginTop: 16,
            textAlign: "center",
            fontSize: 10,
            color: "rgba(255,255,255,0.4)",
          }}
        >
          Scientifically inaccurate. Emotionally correct.
          <br />
          For entertainment only. Not a prediction.
        </div>
      </div>

      {/* Action buttons (outside capture) */}
      <div className="grid grid-cols-2 gap-3">
        <button
          type="button"
          onClick={handleCopy}
          className="flex items-center justify-center gap-2 rounded-2xl border border-white/15 bg-white/5 px-4 py-3 font-bold text-white transition hover:bg-white/10 active:scale-[0.98]"
        >
          {copied ? (
            <Check className="h-5 w-5 text-emerald-400" />
          ) : (
            <Copy className="h-5 w-5" />
          )}
          {copied ? "Copied!" : "Copy Result"}
        </button>

        <button
          type="button"
          onClick={handleDownload}
          disabled={downloading}
          className="flex items-center justify-center gap-2 rounded-2xl border border-white/15 bg-white/5 px-4 py-3 font-bold text-white transition hover:bg-white/10 active:scale-[0.98] disabled:opacity-60"
        >
          <Download className="h-5 w-5" />
          {downloading ? "Saving..." : "Download"}
        </button>
      </div>

      {/* Share */}
      <div>
        <button
          type="button"
          onClick={handleShare}
          aria-expanded={shareOpen}
          className="flex w-full items-center justify-center gap-2 rounded-2xl border border-white/15 bg-white/5 px-4 py-3 font-bold text-white transition hover:bg-white/10 active:scale-[0.98]"
        >
          {linkCopied ? (
            <Check className="h-5 w-5 text-emerald-400" />
          ) : (
            <Share2 className="h-5 w-5" />
          )}
          {linkCopied ? "Link copied — share it!" : "Share Result"}
        </button>

        {shareOpen && (
          <div className="mt-3 rounded-2xl border border-white/10 bg-black/40 p-3 backdrop-blur">
            <div className="grid grid-cols-3 gap-2 sm:grid-cols-5">
              {SOCIALS.map((s) => (
                <button
                  key={s.target}
                  type="button"
                  onClick={() =>
                    openShareWindow(getSocialUrl(s.target, shareText, shareUrl))
                  }
                  className="rounded-xl px-2 py-2 text-[11px] font-bold text-white transition hover:brightness-110 active:scale-95"
                  style={{ background: s.bg }}
                >
                  {s.label}
                </button>
              ))}
            </div>

            <div className="mt-2 flex gap-2">
              <button
                type="button"
                onClick={handleCopyLink}
                className="flex flex-1 items-center justify-center gap-1.5 rounded-xl border border-white/15 bg-white/5 px-3 py-2 text-xs font-bold text-white/80 transition hover:bg-white/10 active:scale-95"
              >
                <Link2 className="h-4 w-4" />
                Copy link
              </button>
              {canNativeShare() && (
                <button
                  type="button"
                  onClick={() => nativeShare(shareText, shareUrl)}
                  className="flex flex-1 items-center justify-center gap-1.5 rounded-xl border border-white/15 bg-white/5 px-3 py-2 text-xs font-bold text-white/80 transition hover:bg-white/10 active:scale-95"
                >
                  <Share2 className="h-4 w-4" />
                  More…
                </button>
              )}
            </div>
          </div>
        )}
      </div>

      <button
        type="button"
        onClick={onFightAgain}
        className="flex items-center justify-center gap-2 rounded-2xl bg-gradient-to-r from-fuchsia-600 via-rose-500 to-amber-500 px-6 py-3.5 text-lg font-black uppercase tracking-wider text-white shadow-[0_0_24px_rgba(244,63,94,0.45)] transition active:scale-[0.98]"
      >
        <RotateCcw className="h-5 w-5" />
        Fight Again
      </button>
    </div>
  );
}

// Bold the number-ish tokens (12, 73%, 4×, 0.3s) so each line reads like a
// stat sheet rather than a plain sentence.
function renderDamageLine(text: string): React.ReactNode {
  return text.split(/(\d[\d.,]*(?:%|×|x|s)?)/g).map((part, i) =>
    /^\d/.test(part) ? (
      <strong key={i} style={{ fontWeight: 800, color: "#ffffff" }}>
        {part}
      </strong>
    ) : (
      part
    )
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div
      style={{
        borderRadius: 14,
        background: "rgba(255,255,255,0.06)",
        border: "1px solid rgba(255,255,255,0.08)",
        padding: "10px 12px",
      }}
    >
      <div
        style={{
          fontSize: 10,
          letterSpacing: "0.18em",
          fontWeight: 800,
          color: "rgba(255,255,255,0.45)",
          textTransform: "uppercase",
        }}
      >
        {label}
      </div>
      <div style={{ fontSize: 15, fontWeight: 800, marginTop: 3 }}>{value}</div>
    </div>
  );
}

function SectionLabel({ children }: { children: React.ReactNode }) {
  return (
    <div
      style={{
        fontSize: 10,
        letterSpacing: "0.2em",
        fontWeight: 800,
        color: "rgba(255,255,255,0.45)",
        textTransform: "uppercase",
      }}
    >
      {children}
    </div>
  );
}
