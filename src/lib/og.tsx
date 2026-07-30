import { ImageResponse } from "next/og";
import fs from "node:fs";
import path from "node:path";

/*
 * Shared Open Graph card — the design system at 1200×630.
 * Paper ground, mono kicker, Newsreader title, quiet footer rule.
 */

export const OG_SIZE = { width: 1200, height: 630 };
export const OG_CONTENT_TYPE = "image/png";

const fontDir = path.join(process.cwd(), "src", "assets", "og");
const newsreader = fs.readFileSync(path.join(fontDir, "newsreader-500.ttf"));
const plexMono = fs.readFileSync(path.join(fontDir, "plex-mono-500.ttf"));

export function ogCard({
  kicker,
  title,
  sub,
}: {
  kicker: string;
  title: string;
  sub?: string;
}) {
  const titleSize = title.length > 64 ? 54 : title.length > 36 ? 64 : 78;

  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          background: "#FBFAF7",
          padding: "72px 80px 64px",
        }}
      >
        <div
          style={{
            display: "flex",
            fontFamily: "IBM Plex Mono",
            fontSize: 22,
            letterSpacing: "0.14em",
            textTransform: "uppercase",
            color: "#8A857A",
          }}
        >
          {kicker}
        </div>

        <div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: 28,
          }}
        >
          <div
            style={{
              display: "flex",
              fontFamily: "Newsreader",
              fontSize: titleSize,
              lineHeight: 1.12,
              letterSpacing: "-0.015em",
              color: "#1F1D1A",
              maxWidth: 1000,
            }}
          >
            {title}
          </div>
          {sub && (
            <div
              style={{
                display: "flex",
                fontFamily: "IBM Plex Mono",
                fontSize: 21,
                color: "#57534A",
                maxWidth: 980,
              }}
            >
              {sub}
            </div>
          )}
        </div>

        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            borderTop: "2px solid #1F1D1A",
            paddingTop: 26,
          }}
        >
          <div
            style={{
              display: "flex",
              fontFamily: "Newsreader",
              fontSize: 28,
              color: "#1F1D1A",
            }}
          >
            Hao Qian
          </div>
          <div
            style={{
              display: "flex",
              fontFamily: "IBM Plex Mono",
              fontSize: 20,
              letterSpacing: "0.08em",
              color: "#8A857A",
            }}
          >
            haoqian.co
          </div>
        </div>
      </div>
    ),
    {
      ...OG_SIZE,
      fonts: [
        { name: "Newsreader", data: newsreader, weight: 500, style: "normal" },
        { name: "IBM Plex Mono", data: plexMono, weight: 500, style: "normal" },
      ],
    }
  );
}
