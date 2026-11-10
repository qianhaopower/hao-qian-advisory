import { PILLARS, cardText, type DeckCard, type Lang } from "@/lib/today-deck";

/*
 * The card as a picture, drawn client-side on a canvas. Same idea as the
 * constellation poster: the page's own fonts, no server, no upload.
 *
 *   中文     1080 × 1440 (3:4 — what 小红书 and a phone album like)
 *   English  1080 × 1350 (4:5 — the tallest picture LinkedIn shows uncropped)
 *
 * The drawing is the card's live <svg>: its shapes are rasterised as an image,
 * and its lettering is lifted out and set again with the page fonts (an SVG
 * drawn as an image cannot see web fonts).
 */

const W = 1080;
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
function wrapZh(ctx: CanvasRenderingContext2D, text: string, maxW: number): string[] {
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

/** Greedy wrap for English: break at spaces. */
function wrapEn(ctx: CanvasRenderingContext2D, text: string, maxW: number): string[] {
  const lines: string[] = [];
  let line = "";
  for (const word of text.split(" ")) {
    const next = line ? `${line} ${word}` : word;
    if (ctx.measureText(next).width > maxW && line) {
      lines.push(line);
      line = word;
    } else {
      line = next;
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

function track(ctx: CanvasRenderingContext2D, px: number) {
  try {
    (ctx as CanvasRenderingContext2D & { letterSpacing: string }).letterSpacing = `${px}px`;
  } catch {
    /* older browsers: no tracking */
  }
}

export async function renderShareImage(
  card: DeckCard,
  art: SVGSVGElement,
  handle: string,
  lang: Lang = "zh"
): Promise<Blob> {
  const en = lang === "en";
  const H = en ? 1350 : 1440;
  const p = PILLARS[card.pillar];
  const t = cardText(card, lang);
  const zh = fontVar("--font-noto-serif-sc", '"Songti SC", serif');
  const serif = fontVar("--font-newsreader", "Georgia, serif");
  const mono = fontVar("--font-plex-mono", "monospace");
  const sans = fontVar("--font-instrument", '"PingFang SC", sans-serif');
  const lettering = liftLettering(art);

  /* make sure every glyph this card needs has actually arrived */
  const all = [t.do, t.why, t.when ?? "", p.zh, handle, "今天只做一件事第集"]
    .concat(lettering.map((l) => l.text))
    .join("");
  try {
    await Promise.all([
      document.fonts.load(`900 80px ${zh}`, all),
      document.fonts.load(`600 60px ${serif}`, all),
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
  if (en) {
    ctx.font = `500 30px ${mono}`;
    track(ctx, 5);
    ctx.fillText("ONE THING TODAY", M, 105);
    track(ctx, 0);
  } else {
    ctx.font = `900 38px ${zh}`;
    ctx.fillText("今天只做一件事", M, 108);
  }
  const tag = en ? `${p.en} № ${card.noLabel}` : `${p.zh} № ${card.noLabel}`;
  ctx.font = en ? `600 30px ${serif}` : `900 30px ${zh}`;
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
  if (t.when) {
    ctx.font = en ? `600 34px ${serif}` : `900 34px ${zh}`;
    const w = ctx.measureText(t.when).width + 56;
    const x = M + ART_W - w - 24;
    const y = ART_Y + ART_H - 64 - 24;
    roundRect(ctx, x, y, w, 64, 32);
    ctx.fillStyle = "#F2B632";
    ctx.fill();
    ctx.lineWidth = 4;
    ctx.stroke();
    ctx.fillStyle = INK;
    ctx.textAlign = "center";
    ctx.fillText(t.when, x + w / 2, y + 45);
  }

  /* the one thing, then why */
  ctx.fillStyle = INK;
  ctx.textAlign = "left";
  let y = ART_Y + ART_H;
  if (en) {
    /* shrink until the action sets in three lines or fewer */
    let size = 80;
    let lines: string[] = [];
    for (; size >= 56; size -= 4) {
      ctx.font = `600 ${size}px ${serif}`;
      lines = wrapEn(ctx, t.do, ART_W);
      if (lines.length <= (size > 68 ? 2 : 3)) break;
    }
    y += size + 34;
    for (const line of lines) {
      ctx.fillText(line, M, y);
      y += Math.round(size * 1.14);
    }
    ctx.font = `400 34px ${sans}`;
    y += 50 - Math.round(size * 1.14) + 34;
    const room = Math.max(1, Math.floor((H - 132 - y) / 50) + 1);
    for (const line of wrapEn(ctx, t.why, ART_W).slice(0, room)) {
      ctx.fillText(line, M, y);
      y += 50;
    }
  } else {
    ctx.font = `900 88px ${zh}`;
    y += 128;
    for (const line of t.do.split("\n")) {
      ctx.fillText(line, M, y);
      y += 112;
    }
    ctx.font = `400 38px ${sans}`;
    y -= 112 - 78;
    for (const line of wrapZh(ctx, t.why, ART_W).slice(0, 3)) {
      ctx.fillText(line, M, y);
      y += 58;
    }
  }

  /* colophon */
  ctx.fillRect(M, H - 112, ART_W, 3);
  if (en) {
    ctx.font = `600 30px ${serif}`;
    ctx.fillText(`Friends Intelligence · Ep. ${card.no}`, M, H - 58);
  } else {
    ctx.font = `900 30px ${zh}`;
    ctx.fillText(`${handle} · 第 ${card.no} 集`, M, H - 58);
  }
  ctx.textAlign = "right";
  ctx.font = `500 26px ${mono}`;
  track(ctx, 3);
  ctx.fillText(`HAOQIAN.CO/TODAY${en ? "/EN" : ""}`, W - M, H - 58);

  return new Promise((resolve, reject) => {
    canvas.toBlob(
      (blob) => (blob ? resolve(blob) : reject(new Error("no image"))),
      "image/png"
    );
  });
}
