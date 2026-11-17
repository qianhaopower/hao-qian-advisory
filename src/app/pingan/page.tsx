import type { Metadata, Viewport } from "next";
import { ZCOOL_KuaiLe } from "next/font/google";
import { PinganSign } from "@/components/pingan/PinganSign";

/* The sign's cartoon letter (站酷快乐体). Loaded by this page only, and not
 * preloaded: the browser fetches just the slices the sign actually sets. */
const zcool = ZCOOL_KuaiLe({
  variable: "--font-zcool",
  weight: "400",
  preload: false,
  display: "swap",
});

export const metadata: Metadata = {
  title: { absolute: "平安牌" },
  description: "高高兴兴上班去，平平安安没被裁。",
  robots: { index: false, follow: false },
  openGraph: {
    title: "平安牌",
    description: "高高兴兴上班去，平平安安没被裁。",
  },
};

export const viewport: Viewport = { themeColor: "#FFD84D" };

/*
 * /pingan — 平安牌, the house sign (2026-11-18). Unlisted on purpose: no nav,
 * no home index, no sitemap, no search entry, noindex. It has no site shell —
 * the whole screen is the sign. Words in src/content/pingan.ts.
 */
export default function PinganPage() {
  return (
    <div className={zcool.variable}>
      <PinganSign />
    </div>
  );
}
