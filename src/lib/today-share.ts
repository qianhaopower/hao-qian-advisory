import { PILLARS, type DeckCard } from "@/lib/today-deck";

/*
 * The card as a 1080 × 1440 picture (3:4 — what 小红书 and a phone album
 * like), drawn client-side on a canvas. Same idea as the constellation
 * poster: the page's own fonts, no server, no upload.
 *
 * The drawing is the card's live <svg>: its shapes are rasterised as an image,
 * and its lettering is lifted out and set again with the page fonts (an SVG
 * drawn as an image cannot see web fonts).
 */

const W = 1080;
const H = 1440;
const M = 64;
const INK = "#1F1D1A";
const ART_W = W - M * 2;
const ART_H = Math.round((ART_W * 236) / 368);
const ART_Y = 156;

function fontVar(name: string, fallback: string): string {
  const v = getComputedStyle(document.body).getPropertyValue(name).trim();
  return v ? `${v}, ${fallback}` : fallback;
}

function roundRect(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  w: number,
  h: number,
  r: number
) {
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.arcTo(x + w, y, x + w, y + h, r);
  ctx.arcTo(x + w, y + h, x, y + h, r);
  ctx.arcTo(x, y + h, x, y, r);
  ctx.arcTo(x, y, x + w, y, r);
  ctx.closePath();
}

const NO_LINE_START = "，。、；：！？）」』”’%";

/** Greedy wrap for Chinese: break anywhere, but never start a line with punctuation. */
function wrap(ctx: CanvasRenderingContext2D, text: string, maxW: number): string[] {
  const lines: string[] = [];
  let line = "";
  for (const ch of text) {
    if (ctx.measureText(line + ch).width > maxW && line && !NO_LINE_START.includes(ch)) {
      lines.push(line);
      line = ch;
    } else {
      line += ch;
    }
  }
  if (line) lines.push(line);
  return lines;
}

type Lettering = {
  text: string;
  x: number;
  y: number;
  size: number;
  weight: string;
  family: string;
  fill: string;
  align: CanvasTextAlign;
};

function liftLettering(art: SVGSVGElement): Lettering[] {
  return [...art.querySelectorAll("text")].map((el) => {
    const cs = getComputedStyle(el);
    const anchor = el.getAttribute("text-anchor");
    return {
      text: el.textContent ?? "",
      x: Number(el.getAttribute("x") ?? 0),
      y: Number(el.getAttribute("y") ?? 0),
      size: Number(el.getAttribute("font-size") ?? 16),
      weight: cs.fontWeight,
      family: cs.fontFamily,
      fill: el.getAttribute("fill") ?? INK,
      align: anchor === "middle" ? "center" : anchor === "end" ? "right" : "left",
    };
  });
}

function rasterise(art: SVGSVGElement, w: number, h: number): Promise<HTMLImageElement> {
  const clone = art.cloneNode(true) as SVGSVGElement;
  clone.querySelectorAll("text").forEach((t) => t.remove());
  clone.setAttribute("xmlns", "http://www.w3.org/2000/svg");
  clone.setAttribute("width", String(w));
  clone.setAttribute("height", String(h));
  clone.removeAttribute("style");
  const xml = new XMLSerializer().serializeToString(clone);
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = () => reject(new Error("card art did not rasterise"));
    img.src = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(xml)}`;
  });
}

export async function renderShareImage(
  card: DeckCard,
  art: SVGSVGElement,
  handle: string
): Promise<Blob> {
  const p = PILLARS[card.pillar];
  const zh = fontVar("--font-noto-serif-sc", '"Songti SC", serif');
  const num = fontVar("--font-newsreader", "Georgia, serif");
  const mono = fontVar("--font-plex-mono", "monospace");
  const sans = fontVar("--font-instrument", '"PingFang SC", sans-serif');
  const lettering = liftLettering(art);

  /* make sure every glyph this card needs has actually arrived */
  const all = [card.do, card.why, card.when ?? "", p.zh, handle, "今天只做一件事第集"]
    .concat(lettering.map((l) => l.text))
    .join("");
  try {
    await Promise.all([
      document.fonts.load(`900 80px ${zh}`, all),
      document.fonts.load(`600 60px ${num}`, "0123456789"),
      document.fonts.load(`500 26px ${mono}`, "HAOQIAN.CO/TODAY"),
      document.fonts.ready,
    ]);
  } catch {
    /* fall through with whatever fonts are there */
  }

  const canvas = document.createElement("canvas");
  canvas.width = W;
  canvas.height = H;
  const ctx = canvas.getContext("2d");
  if (!ctx) throw new Error("no canvas");

  ctx.fillStyle = p.tint;
  ctx.fillRect(0, 0, W, H);
  ctx.textBaseline = "alphabetic";

  /* masthead */
  ctx.fillStyle = INK;
  ctx.textAlign = "left";
  ctx.font = `900 38px ${zh}`;
  ctx.fillText("今天只做一件事", M, 108);
  const tag = `${p.zh} № ${card.noLabel}`;
  ctx.font = `900 30px ${zh}`;
  const tagW = ctx.measureText(tag).width + 48;
  roundRect(ctx, W - M - tagW, 66, tagW, 56, 28);
  ctx.lineWidth = 4;
  ctx.strokeStyle = INK;
  ctx.stroke();
  ctx.textAlign = "center";
  ctx.fillText(tag, W - M - tagW / 2, 105);

  /* the drawing */
  roundRect(ctx, M, ART_Y, ART_W, ART_H, 30);
  ctx.fillStyle = p.wash;
  ctx.fill();
  ctx.save();
  roundRect(ctx, M, ART_Y, ART_W, ART_H, 30);
  ctx.clip();
  const img = await rasterise(art, ART_W, ART_H);
  ctx.drawImage(img, M, ART_Y, ART_W, ART_H);
  const k = ART_W / 368;
  for (const l of lettering) {
    ctx.font = `${l.weight} ${l.size * k}px ${l.family}`;
    ctx.fillStyle = l.fill;
    ctx.textAlign = l.align;
    ctx.fillText(l.text, M + l.x * k, ART_Y + l.y * k);
  }
  ctx.restore();
  roundRect(ctx, M, ART_Y, ART_W, ART_H, 30);
  ctx.lineWidth = 5;
  ctx.strokeStyle = INK;
  ctx.stroke();

  /* the moment to do it */
  if (card.when) {
    ctx.font = `900 34px ${zh}`;
    const w = ctx.measureText(card.when).width + 56;
    const x = M + ART_W - w - 24;
    const y = ART_Y + ART_H - 64 - 24;
    roundRect(ctx, x, y, w, 64, 32);
    ctx.fillStyle = "#F2B632";
    ctx.fill();
    ctx.lineWidth = 4;
    ctx.stroke();
    ctx.fillStyle = INK;
    ctx.textAlign = "center";
    ctx.fillText(card.when, x + w / 2, y + 45);
  }

  /* the one thing */
  ctx.fillStyle = INK;
  ctx.textAlign = "left";
  ctx.font = `900 88px ${zh}`;
  let y = ART_Y + ART_H + 128;
  for (const line of card.do.split("\n")) {
    ctx.fillText(line, M, y);
    y += 112;
  }

  /* why */
  ctx.font = `400 38px ${sans}`;
  y -= 112 - 78;
  for (const line of wrap(ctx, card.why, ART_W).slice(0, 3)) {
    ctx.fillText(line, M, y);
    y += 58;
  }

  /* colophon */
  ctx.fillRect(M, H - 112, ART_W, 3);
  ctx.font = `900 30px ${zh}`;
  ctx.fillText(`${handle} · 第 ${card.no} 集`, M, H - 58);
  ctx.textAlign = "right";
  ctx.font = `500 26px ${mono}`;
  try {
    (ctx as CanvasRenderingContext2D & { letterSpacing: string }).letterSpacing = "3px";
  } catch {
    /* older browsers: no tracking */
  }
  ctx.fillText("HAOQIAN.CO/TODAY", W - M, H - 58);

  return new Promise((resolve, reject) => {
    canvas.toBlob(
      (blob) => (blob ? resolve(blob) : reject(new Error("no image"))),
      "image/png"
    );
  });
}
