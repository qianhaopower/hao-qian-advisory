/*
 * 喜报 as a picture — the house sign's way of telling the other phone.
 *
 * /pingan keeps each sign in its own phone's localStorage and there is no
 * server behind it, so the news travels the old way: a 1080 × 1440 picture,
 * drawn here on a canvas with the page's own cartoon face, to send by chat.
 * No names, no site address — the page is unlisted and the picture keeps it so.
 */

export type GoodNews = {
  /** 老公同志 / Iris同志 / 老公、Iris / 全家 / 全员 */
  subject: string;
  /** who the family leans on now, one string per line */
  lean: string[];
  /** the run of quiet days that just ended; 0 leaves the line out */
  record: number;
  /** 2026.11.18 */
  date: string;
};

const W = 1080;
const H = 1440;
const RED = "#D9281E";
const GOLD = "#FFD84D";
const CREAM = "#FFF8E7";

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

function track(ctx: CanvasRenderingContext2D, px: number) {
  try {
    (ctx as CanvasRenderingContext2D & { letterSpacing: string }).letterSpacing = `${px}px`;
  } catch {
    /* older browsers: no tracking */
  }
}

/** Set a line centred, shrinking it until it fits the poster. */
function fit(
  ctx: CanvasRenderingContext2D,
  text: string,
  y: number,
  size: number,
  family: string,
  maxW = W - 220
) {
  let px = size;
  ctx.font = `400 ${px}px ${family}`;
  while (px > 24 && ctx.measureText(text).width > maxW) {
    px -= 4;
    ctx.font = `400 ${px}px ${family}`;
  }
  ctx.fillText(text, W / 2, y);
}

export function recordLine(record: number): string {
  return `连续平安 ${record} 天 · 纪录就此定格`;
}

/**
 * `fontFrom` is any element inside the page: the cartoon face is a CSS
 * variable set on the page's wrapper, not on <body>.
 */
export async function renderGoodNews(news: GoodNews, fontFrom: Element): Promise<Blob> {
  const face = getComputedStyle(fontFrom).getPropertyValue("--font-zcool").trim();
  const family = face
    ? `${face}, "PingFang SC", sans-serif`
    : '"PingFang SC", "Microsoft YaHei", sans-serif';
  const footer = `${news.date} · 本大家庭 宣`;

  /* the face arrives in unicode-range slices: ask for every glyph we set */
  const all = ["喜报热烈祝贺光荣毕业", news.subject, ...news.lean, recordLine(news.record), footer].join("");
  try {
    await Promise.all([document.fonts.load(`400 120px ${family}`, all), document.fonts.ready]);
  } catch {
    /* fall through with whatever fonts are there */
  }

  const canvas = document.createElement("canvas");
  canvas.width = W;
  canvas.height = H;
  const ctx = canvas.getContext("2d");
  if (!ctx) throw new Error("no canvas");

  ctx.fillStyle = RED;
  ctx.fillRect(0, 0, W, H);

  /* the double gold frame */
  ctx.strokeStyle = GOLD;
  ctx.lineWidth = 12;
  roundRect(ctx, 46, 46, W - 92, H - 92, 48);
  ctx.stroke();
  ctx.lineWidth = 4;
  roundRect(ctx, 68, 68, W - 136, H - 136, 32);
  ctx.stroke();

  ctx.textAlign = "center";
  ctx.textBaseline = "alphabetic";

  ctx.fillStyle = GOLD;
  track(ctx, 30);
  fit(ctx, "喜报", 470, 380, family);

  ctx.fillStyle = CREAM;
  track(ctx, 26);
  fit(ctx, "热烈祝贺", 610, 78, family);

  track(ctx, 0);
  ctx.fillStyle = GOLD;
  fit(ctx, news.subject, 800, 170, family);
  ctx.fillStyle = CREAM;
  fit(ctx, "光荣毕业", 985, 170, family);

  ctx.fillStyle = GOLD;
  ctx.fillRect(W / 2 - 90, 1036, 180, 7);

  let y = 1108;
  if (news.record > 0) {
    ctx.fillStyle = CREAM;
    fit(ctx, recordLine(news.record), y, 50, family);
    y += 78;
  } else {
    y += 20;
  }
  ctx.fillStyle = GOLD;
  for (const line of news.lean) {
    fit(ctx, line, y, 60, family);
    y += 74;
  }

  ctx.fillStyle = CREAM;
  ctx.globalAlpha = 0.85;
  track(ctx, 4);
  fit(ctx, footer, H - 94, 34, family);
  ctx.globalAlpha = 1;

  return new Promise((resolve, reject) => {
    canvas.toBlob(
      (blob) => (blob ? resolve(blob) : reject(new Error("no image"))),
      "image/png"
    );
  });
}
