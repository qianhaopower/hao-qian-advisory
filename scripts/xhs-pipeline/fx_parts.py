#!/usr/bin/env python3
"""
fx_parts.py — the 小Lin-style parts library for the FI (小红书) line.

One function per visual "skill", all pure PIL, all returning a finished
1080×1920 RGB frame (or an RGBA layer for the primitives), so compose_v2.py
and to_capcut.py can call them per frame, and a demo script can render
stills.  Catalogue (docs/XHS_GRAPHICS_V2_PLAN.md §7):

  primitives   ground_dots / ground_paper / ground_diagonal / grade_face /
               face_frame / pip_circle / pip_rect / label_block / bubble /
               card / flip_counter / halftone_text / caption / shadow
  effects      fx_bubble_cluster   气泡簇      — terms floating round the head
               fx_matrix_card      锚卡矩阵    — rows × cols, ? → values
               fx_twin_cards       手边卡      — 1–3 icon cards at chest level
               fx_calc_scene       算账        — object + flip counters + arrows + big PIP
               fx_split_phone      人+手机     — speaker rect + phone mock-up with a REAL screenshot
               fx_desk_collage     纸面拼贴    — polaroids on grid paper + small PIP
               fx_poster_chapter   海报章节    — halftone big word + centre PIP

Rules baked in (from the Ep34 v2 feedback, 2026-10-31):
  * speaker frame at zoom 1.0 for anything that sits BESIDE him (bubbles,
    held cards); the wall is keyed darker so cuts to ink cards don't flash;
  * nothing is ever drawn inside the face box; held things live in the
    chest band (0.52–0.74 H); the caption is one white line at 0.80 H;
  * real artefacts only (screenshots, product photos, your own photos) —
    the library frames evidence, it never invents it.
"""
from __future__ import annotations
import math, os
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageChops

W, H = 1080, 1920
FONTS = os.path.expanduser("~/Video Studio/work/fonts")
F_HEAVY = os.path.join(FONTS, "SourceHanSansSC-Heavy.otf")
F_BRUSH = os.path.join(FONTS, "LXGWWenKai-Medium.ttf")
F_MONO = os.path.expanduser("~/Documents/hao-qian-advisory/src/assets/og/plex-mono-500.ttf")

TOK = {
    "ink": (18, 18, 22), "ink2": (30, 30, 36), "rim": (255, 255, 255),
    "white": (242, 238, 230), "muted": (186, 180, 168), "paper": (236, 232, 222),
    "gold": (222, 184, 70), "red": (214, 72, 64), "orange": (222, 92, 52),
}
TINTS = {  # low-saturation panel colours, one per row / bubble, never a fill for text
    "teal": (34, 74, 78), "violet": (72, 50, 106), "navy": (38, 52, 96),
    "wine": (96, 36, 60), "olive": (70, 78, 40), "slate": (54, 58, 70), "rust": (110, 58, 40),
}
TINT_ORDER = ["teal", "violet", "navy", "wine", "olive", "slate", "rust"]

# face geometry of the FI set-up at zoom 1.0 (raw 2160×3840 → 1080×1920):
FACE_CX, FACE_CY, FACE_R = 0.50, 0.355, 0.13      # centre + radius (fraction of W / H)
FACE_BOX = (0.33, 0.19, 0.67, 0.49)               # keep-out box (x0, y0, x1, y1)
CHEST_BAND = (0.53, 0.74)
CAPTION_Y = 0.80


# ───────────────────────── primitives ─────────────────────────
@lru_cache(maxsize=None)
def font(path: str, size: int):
    return ImageFont.truetype(path, size)


def cjk(size): return font(F_HEAVY, size)
def latin(size): return font(F_MONO, size)
def brush(size): return font(F_BRUSH, size)


def text_w(txt, f, spacing=0.0):
    d = ImageDraw.Draw(Image.new("L", (1, 1)))
    if not spacing:
        return d.textlength(txt, font=f)
    return sum(d.textlength(c, font=f) for c in txt) + spacing * f.size * (len(txt) - 1)


def draw_text(layer, xy, txt, f, fill, spacing=0.0, anchor="la", stroke=0, stroke_fill=(0, 0, 0, 220)):
    """Letter-spaced text. anchor 'la' | 'ma' (centre x) | 'ra'."""
    d = ImageDraw.Draw(layer)
    w = text_w(txt, f, spacing)
    x, y = xy
    if anchor[0] == "m": x -= w / 2
    elif anchor[0] == "r": x -= w
    for c in txt:
        d.text((x, y), c, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
        x += d.textlength(c, font=f) + spacing * f.size
    return w


def smallcaps(layer, xy, txt, size, fill, anchor="ma", tracking=0.16):
    return draw_text(layer, xy, txt.upper(), latin(size), fill, spacing=tracking, anchor=anchor)


def shadow(layer: Image.Image, radius=18, offset=(0, 14), alpha=150) -> Image.Image:
    """Return layer composited over its own soft shadow (same size + padding)."""
    pad = radius * 3 + max(abs(offset[0]), abs(offset[1]))
    out = Image.new("RGBA", (layer.width + 2 * pad, layer.height + 2 * pad), (0, 0, 0, 0))
    sh = Image.new("RGBA", out.size, (0, 0, 0, 0))
    a = layer.split()[3].point(lambda v: v * alpha // 255)
    sh.paste((0, 0, 0, 255), (pad + offset[0], pad + offset[1]), a)
    sh = sh.filter(ImageFilter.GaussianBlur(radius))
    out.alpha_composite(sh)
    out.alpha_composite(layer, (pad, pad))
    return out


def rounded(size, radius, fill, stroke=None, stroke_w=2) -> Image.Image:
    im = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], radius, fill=fill,
                        outline=stroke, width=stroke_w if stroke else 0)
    return im


def vgradient(size, top, bottom, alpha=255) -> Image.Image:
    g = Image.new("RGBA", (1, size[1]))
    px = g.load()
    for y in range(size[1]):
        t = y / max(1, size[1] - 1)
        px[0, y] = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)) + (alpha,)
    return g.resize(size)


def tint_panel(size, tint, radius=22, rim=True) -> Image.Image:
    """Her row/card panel: dark → tint gradient, hairline rim, soft inner glow at the left."""
    dark = tuple(max(0, c - 22) for c in tint)
    light = tuple(min(255, int(c * 1.25)) for c in tint)
    body = vgradient(size, light, dark)
    mask = rounded(size, radius, (255, 255, 255, 255))
    out = Image.new("RGBA", size, (0, 0, 0, 0))
    out.paste(body, (0, 0), mask)
    if rim:
        d = ImageDraw.Draw(out)
        d.rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], radius, outline=(255, 255, 255, 46), width=2)
    return out


def ground_dots(size=(W, H), base=TOK["ink"], pitch=26, dot_alpha=26, vignette=0.45) -> Image.Image:
    """Near-black ground with a faint dot grid and a vignette (her default stage)."""
    g = Image.new("RGB", size, base)
    d = ImageDraw.Draw(g)
    c = tuple(min(255, v + dot_alpha) for v in base)
    for y in range(pitch // 2, size[1], pitch):
        for x in range(pitch // 2, size[0], pitch):
            d.point((x, y), fill=c)
    return _vignette(g, vignette)


def _vignette(img: Image.Image, strength: float) -> Image.Image:
    if strength <= 0: return img
    w, h = img.size
    m = Image.new("L", (w // 8, h // 8), 0)
    d = ImageDraw.Draw(m)
    d.ellipse([-w // 32, -h // 32, m.width + w // 32, m.height + h // 32], fill=255)
    m = m.filter(ImageFilter.GaussianBlur(m.width // 5)).resize((w, h))
    dark = Image.new("RGB", (w, h), (0, 0, 0))
    inv = m.point(lambda v: int((255 - v) * strength))
    return Image.composite(dark, img, inv)


def ground_paper(size=(W, H), grid=44) -> Image.Image:
    g = Image.new("RGB", size, TOK["paper"])
    d = ImageDraw.Draw(g)
    for x in range(0, size[0], grid): d.line([(x, 0), (x, size[1])], fill=(214, 210, 200), width=1)
    for y in range(0, size[1], grid): d.line([(0, y), (size[0], y)], fill=(214, 210, 200), width=1)
    return _vignette(g, 0.18)


def ground_diagonal(size=(W, H), tint=(150, 38, 70), base=TOK["ink"]) -> Image.Image:
    g = Image.new("RGB", size, base)
    d = ImageDraw.Draw(g)
    w, h = size
    d.polygon([(0, 0), (w, 0), (w, int(h * 0.12)), (0, int(h * 0.30))], fill=tint)
    d.polygon([(0, h), (w, h), (w, int(h * 0.78)), (0, int(h * 0.92))], fill=tint)
    return _vignette(g, 0.25)


@lru_cache(maxsize=8)
def _falloff(size, cx, cy, rx, ry, strength):
    """Light fall-off centred on the face: 0 at the face, `strength` at the frame edge (cached)."""
    w, h = size
    m = Image.new("L", (w // 8, h // 8), 0)
    ImageDraw.Draw(m).ellipse([(cx - rx) // 8, (cy - ry) // 8, (cx + rx) // 8, (cy + ry) // 8], fill=255)
    m = m.filter(ImageFilter.GaussianBlur(w // 40)).resize((w, h), Image.BILINEAR)
    return m.point(lambda v: int((255 - v) * strength))


_CURVE = [v if v < 165 else int(165 + (v - 165) * 0.72) for v in range(256)] * 3


def grade_face(img: Image.Image, wall=0.62, vignette=0.22, face=None) -> Image.Image:
    """v4 (2026-10-31, after Hao: v3 看着灰暗). Measured against 小Lin's face shots: her frames sit at
    mean luma ≈100–110 but contrast (std) ≈70–76 and skin saturation ≈65; our v3 had the same mean
    luma yet contrast 63 / skin sat 44 → grey.  Hao's accepted Ep34 look: luma 120, sat 47, skin sat 88.
    So: mild highlight roll-off (>165 ×0.72, wall 190→183 before fall-off), a GENTLE fall-off only at
    the far edges, then saturation ×1.5, contrast ×1.10, brightness ×1.03.  No per-pixel key."""
    w, h = img.size
    out = img.point(_CURVE)
    cx, cy = int(w * FACE_CX), int(h * FACE_CY)
    fall = _falloff((w, h), cx, cy, int(w * 0.62), int(h * 0.40), 0.34)
    out = Image.composite(Image.new("RGB", (w, h), (0, 0, 0)), out, fall)
    out = ImageEnhance.Color(out).enhance(1.5)
    out = ImageEnhance.Contrast(out).enhance(1.10)
    return ImageEnhance.Brightness(out).enhance(1.03)


def face_frame(src: Image.Image, zoom=1.0, face_y=FACE_CY, grade=True) -> Image.Image:
    """1080×1920 speaker frame from the 2160×3840 source. zoom 1.0 = waist-up (whole frame)."""
    sw, sh = src.size
    cw, ch = int(sw / zoom), int(sh / zoom)
    fx, fy = sw * FACE_CX, sh * FACE_CY
    x0 = min(max(0, int(fx - cw / 2)), sw - cw)
    y0 = min(max(0, int(fy - ch * face_y)), sh - ch)
    fr = src.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.LANCZOS)
    return grade_face(fr) if grade else fr


def _face_square(src: Image.Image, scale=0.42) -> Image.Image:
    sw, sh = src.size
    r = int(sw * scale / 2)
    cx, cy = int(sw * FACE_CX), int(sh * FACE_CY) + int(r * 0.08)
    return src.crop((cx - r, cy - r, cx + r, cy + r))


def pip_circle(src: Image.Image, d=300, ring=TOK["gold"], ring_w=4) -> Image.Image:
    """Small round speaker, top-right; appears INSTANTLY on the cut (no shrink animation)."""
    sq = grade_face(_face_square(src).resize((d, d), Image.LANCZOS), wall=0.72, vignette=0)
    out = Image.new("RGBA", (d + 2 * ring_w, d + 2 * ring_w), (0, 0, 0, 0))
    m = Image.new("L", (d * 4, d * 4), 0); ImageDraw.Draw(m).ellipse([0, 0, d * 4 - 1, d * 4 - 1], fill=255)
    m = m.resize((d, d), Image.LANCZOS)
    out.paste(sq, (ring_w, ring_w), m)
    ImageDraw.Draw(out).ellipse([1, 1, out.width - 2, out.height - 2], outline=ring + (255,), width=ring_w)
    return shadow(out, 14, (0, 10), 120)


def pip_rect(src: Image.Image, size=(440, 640), radius=30) -> Image.Image:
    """Large portrait speaker window for 50/50 compositions (her phone / calc scenes)."""
    sw, sh = src.size
    ar = size[0] / size[1]
    ch = int(sh * 0.62); cw = int(ch * ar)
    cx, cy = int(sw * FACE_CX), int(sh * FACE_CY) + int(ch * 0.18)
    x0 = min(max(0, cx - cw // 2), sw - cw); y0 = min(max(0, cy - ch // 2), sh - ch)
    im = grade_face(src.crop((x0, y0, x0 + cw, y0 + ch)).resize(size, Image.LANCZOS), wall=0.72, vignette=0.1)
    out = Image.new("RGBA", size, (0, 0, 0, 0))
    out.paste(im, (0, 0), rounded(size, radius, (255, 255, 255, 255)))
    ImageDraw.Draw(out).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], radius, outline=(255, 255, 255, 60), width=2)
    return shadow(out, 20, (0, 16), 140)


def label_block(zh, en, zh_size=56, en_size=20, fill=TOK["white"], en_fill=None, width=None) -> Image.Image:
    """CJK word with its small-caps English underneath — the unit every card/bubble uses."""
    en_fill = en_fill or TOK["muted"]
    fz = cjk(zh_size); fe = latin(en_size)
    wz = text_w(zh, fz, 0.06); we = text_w(en.upper(), fe, 0.16) if en else 0
    w = int(width or max(wz, we) + 8)
    h = int(zh_size * 1.15 + (en_size * 1.5 if en else 0))
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw_text(im, (w / 2, 0), zh, fz, fill + (255,), spacing=0.06, anchor="ma")
    if en:
        smallcaps(im, (w / 2, zh_size * 1.18), en, en_size, en_fill + (255,))
    return im


def ornament(w=120, color=(255, 255, 255, 120)) -> Image.Image:
    """Her little filigree divider: hairline with a diamond in the middle."""
    im = Image.new("RGBA", (w, 14), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.line([(0, 7), (w // 2 - 10, 7)], fill=color, width=1); d.line([(w // 2 + 10, 7), (w, 7)], fill=color, width=1)
    d.polygon([(w // 2, 1), (w // 2 + 6, 7), (w // 2, 13), (w // 2 - 6, 7)], outline=color)
    return im


def bubble(d, zh, en, tint) -> Image.Image:
    """Round term bubble: radial tint, light rim, ornament top + bottom, label."""
    s = d * 2
    base = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    dark = tuple(max(0, c - 26) for c in tint); light = tuple(min(255, int(c * 1.35)) for c in tint)
    g = Image.new("RGBA", (s, s), (0, 0, 0, 0)); px = g.load()
    for y in range(s):
        for x in range(s):
            r = math.hypot(x - s / 2, y - s / 2) / (s / 2)
            if r <= 1:
                t = r * r
                px[x, y] = tuple(int(light[i] + (dark[i] - light[i]) * t) for i in range(3)) + (244,)
    g = g.resize((d, d), Image.LANCZOS)
    ImageDraw.Draw(g).ellipse([1, 1, d - 2, d - 2], outline=(255, 255, 255, 70), width=2)
    zs = int(d * 0.19) if len(zh) <= 3 else int(d * 0.15)
    lb = label_block(zh, en, zs, max(14, int(d * 0.06)))
    g.alpha_composite(lb, ((d - lb.width) // 2, (d - lb.height) // 2 - int(d * 0.02)))
    o = ornament(int(d * 0.42))
    g.alpha_composite(o, ((d - o.width) // 2, int(d * 0.17)))
    g.alpha_composite(o, ((d - o.width) // 2, int(d * 0.80)))
    return shadow(g, 16, (0, 12), 150)


def corner_brackets(layer, inset=14, length=26, color=(255, 255, 255, 110), w=2):
    d = ImageDraw.Draw(layer); x1, y1 = layer.width - 1 - inset, layer.height - 1 - inset; x0 = y0 = inset
    for (x, y, dx, dy) in [(x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)]:
        d.line([(x, y), (x + dx * length, y)], fill=color, width=w); d.line([(x, y), (x, y + dy * length)], fill=color, width=w)


def card(size, zh, en, tint, icon=None, radius=22) -> Image.Image:
    """Held / category card: tint panel, corner brackets, label on top, optional line icon below."""
    p = tint_panel(size, tint, radius)
    corner_brackets(p)
    lb = label_block(zh, en, int(size[0] * 0.19), max(14, int(size[0] * 0.065)))
    p.alpha_composite(lb, ((size[0] - lb.width) // 2, int(size[1] * 0.12)))
    if icon is not None:
        ic = icon(int(size[0] * 0.46))
        p.alpha_composite(ic, ((size[0] - ic.width) // 2, int(size[1] * 0.52)))
    return shadow(p, 18, (0, 14), 150)


# — simple white line icons (strokes only, never filled art) —
def icon_drop(s):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im); w = max(3, s // 22)
    pts = [(s * 0.5, s * 0.06)] + [(s * 0.5 + s * 0.32 * math.sin(a), s * 0.62 - s * 0.30 * math.cos(a)) for a in [i * math.pi / 18 - math.pi * 0.72 for i in range(27)]]
    d.line(pts + [pts[0]], fill=(255, 255, 255, 230), width=w, joint="curve")
    d.arc([s * 0.30, s * 0.46, s * 0.56, s * 0.76], 120, 200, fill=(255, 255, 255, 160), width=w)
    return im


def icon_cart(s):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im); w = max(3, s // 22); c = (255, 255, 255, 230)
    d.line([(s * 0.08, s * 0.22), (s * 0.24, s * 0.22), (s * 0.36, s * 0.66), (s * 0.84, s * 0.66), (s * 0.92, s * 0.36), (s * 0.30, s * 0.36)], fill=c, width=w, joint="curve")
    d.ellipse([s * 0.38, s * 0.74, s * 0.50, s * 0.86], outline=c, width=w); d.ellipse([s * 0.72, s * 0.74, s * 0.84, s * 0.86], outline=c, width=w)
    return im


def icon_flask(s):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im); w = max(3, s // 22); c = (255, 255, 255, 230)
    d.line([(s * 0.40, s * 0.10), (s * 0.60, s * 0.10)], fill=c, width=w)
    d.line([(s * 0.44, s * 0.10), (s * 0.44, s * 0.42), (s * 0.18, s * 0.84), (s * 0.82, s * 0.84), (s * 0.56, s * 0.42), (s * 0.56, s * 0.10)], fill=c, width=w, joint="curve")
    d.line([(s * 0.30, s * 0.66), (s * 0.70, s * 0.66)], fill=(255, 255, 255, 150), width=w)
    return im


def icon_sum(s):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im); w = max(3, s // 22); c = (255, 255, 255, 230)
    d.line([(s * 0.78, s * 0.14), (s * 0.22, s * 0.14), (s * 0.56, s * 0.50), (s * 0.22, s * 0.86), (s * 0.78, s * 0.86)], fill=c, width=w, joint="curve")
    return im


def flip_counter(txt, cell=(58, 80), fill=TOK["white"], unit=None) -> Image.Image:
    """Split-flap digits: each character in its own dark cell with a hairline across the middle."""
    gap = 6
    chars = list(txt)
    w = len(chars) * (cell[0] + gap) - gap + (text_w(unit, latin(26), 0.1) + 18 if unit else 0)
    im = Image.new("RGBA", (int(w), cell[1]), (0, 0, 0, 0))
    x = 0
    for c in chars:
        cl = rounded(cell, 8, (36, 36, 42, 255), stroke=(255, 255, 255, 40), stroke_w=1)
        d = ImageDraw.Draw(cl)
        f = cjk(int(cell[1] * 0.62)) if not c.isascii() else font(F_MONO, int(cell[1] * 0.64))
        tw = d.textlength(c, font=f)
        d.text(((cell[0] - tw) / 2, cell[1] * 0.12), c, font=f, fill=fill + (255,))
        d.line([(0, cell[1] // 2), (cell[0], cell[1] // 2)], fill=(0, 0, 0, 170), width=2)
        im.alpha_composite(cl, (x, 0)); x += cell[0] + gap
    if unit:
        smallcaps(im, (x + 12, cell[1] * 0.3), unit, 26, TOK["muted"] + (255,), anchor="la", tracking=0.1)
    return shadow(im, 10, (0, 8), 120)


def arrow(layer, p0, p1, color=(235, 232, 226, 230), w=5, head=22):
    d = ImageDraw.Draw(layer)
    d.line([p0, p1], fill=color, width=w)
    a = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    for s in (-1, 1):
        d.line([p1, (p1[0] - head * math.cos(a + s * 0.5), p1[1] - head * math.sin(a + s * 0.5))], fill=color, width=w)


def halftone_text(zh, size, color=TOK["orange"], pitch=9) -> Image.Image:
    """Pop-art chapter word: glyph filled with a dot screen + a slightly offset second pass."""
    f = brush(size)
    w = int(text_w(zh, f, 0.08) + size * 0.3); h = int(size * 1.3)
    mask = Image.new("L", (w, h), 0)
    draw_text(mask, (w / 2, size * 0.05), zh, f, 255, spacing=0.08, anchor="ma")
    # dot screen: brighter at the centre of each stroke
    screen = Image.new("L", (w, h), 0); d = ImageDraw.Draw(screen)
    for y in range(0, h, pitch):
        for x in range(0, w, pitch):
            r = pitch * 0.42
            d.ellipse([x - r, y - r, x + r, y + r], fill=255)
    dots = ImageChops.multiply(mask, screen)
    solid = Image.new("RGBA", (w, h), color + (255,))
    light = Image.new("RGBA", (w, h), tuple(min(255, c + 40) for c in color) + (255,))
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.paste(light, (0, 0), mask.point(lambda v: int(v * 0.55)))
    out.paste(solid, (0, 0), dots)
    out2 = Image.new("RGBA", (w + 6, h + 6), (0, 0, 0, 0))
    out2.paste(solid, (5, 5), mask.point(lambda v: int(v * 0.35)))     # misregistered second pass
    out2.alpha_composite(out, (0, 0))
    return out2


def caption(frame: Image.Image, txt, y=CAPTION_Y, size=60, fill=TOK["white"], italic=True):
    """One short white line, dark outline, fixed height, never recoloured."""
    layer = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    f = cjk(size)
    draw_text(layer, (W / 2, 0), txt, f, fill + (255,), spacing=0.02, anchor="ma", stroke=max(3, size // 14))
    if italic:
        layer = layer.transform(layer.size, Image.AFFINE, (1, 0.14, -0.14 * size, 0, 1, 0), Image.BICUBIC)
    frame.alpha_composite(layer, (0, int(H * y)))


def paste(frame, layer, cx, cy):
    """Paste an RGBA layer centred at (cx, cy) in fractions of W/H or pixels."""
    if isinstance(cx, float) and cx <= 1: cx = int(cx * W)
    if isinstance(cy, float) and cy <= 1: cy = int(cy * H)
    frame.alpha_composite(layer, (int(cx - layer.width / 2), int(cy - layer.height / 2)))


def fit(img: Image.Image, box, radius=0, shadow_r=0) -> Image.Image:
    """Scale an image to fit inside box (w,h), optional rounded corners + shadow."""
    im = img.convert("RGBA").copy(); im.thumbnail(box, Image.LANCZOS)
    if radius:
        m = rounded(im.size, radius, (255, 255, 255, 255)); im.putalpha(m.split()[3])
    return shadow(im, shadow_r, (0, shadow_r // 2), 150) if shadow_r else im


# ───────────────────────── effects ─────────────────────────
def _frame(src, zoom=1.0, face_y=FACE_CY):
    return face_frame(src, zoom, face_y).convert("RGBA")


def fx_bubble_cluster(src, items, cap=None):
    """items: [(zh, en), ...] up to 7. Laid out round the head on her slots; face box stays clear."""
    fr = _frame(src, 1.0)
    slots = [(0.21, 0.23, 250), (0.80, 0.19, 230), (0.16, 0.46, 220), (0.84, 0.42, 240),
             (0.25, 0.70, 300), (0.76, 0.68, 280), (0.50, 0.14, 180)]
    for i, (zh, en) in enumerate(items[:7]):
        x, y, d = slots[i]
        paste(fr, bubble(d, zh, en, TINTS[TINT_ORDER[i % len(TINT_ORDER)]]), x, y)
    if cap: caption(fr, cap)
    return fr.convert("RGB")


def fx_matrix_card(src, title, cols, rows, values, cap=None):
    """rows: [(zh, en, tint)], cols: [(zh, en)], values: {(r, c): 'text' | None}  None → '?' disc."""
    fr = ground_dots().convert("RGBA")
    cw, ch = 980, 1180
    cardim = rounded((cw, ch), 34, (24, 24, 30, 255), stroke=(255, 255, 255, 50), stroke_w=2)
    corner_brackets(cardim, 16, 34)
    d = ImageDraw.Draw(cardim)
    # header row
    lx = 300; colx = [lx + 60 + i * ((cw - lx - 80) // len(cols)) + ((cw - lx - 80) // len(cols)) // 2 for i in range(len(cols))]
    for i, (zh, en) in enumerate(cols):
        lb = label_block(zh, en, 46, 16)
        cardim.alpha_composite(lb, (int(colx[i] - lb.width / 2), 44))
    d.line([(40, 150), (cw - 40, 150)], fill=(255, 255, 255, 70), width=2)
    rh = (ch - 190) // len(rows) - 18
    for r, (zh, en, tint) in enumerate(rows):
        y = 176 + r * (rh + 18)
        panel = tint_panel((cw - 60, rh), TINTS[tint], 18)
        # label pane on the left, slightly lighter
        pane = tint_panel((lx - 60, rh), tuple(min(255, int(c * 1.18)) for c in TINTS[tint]), 18)
        panel.alpha_composite(pane, (0, 0))
        lb = label_block(zh, en, 40 if len(zh) <= 4 else 32, 15, width=lx - 80)
        panel.alpha_composite(lb, (int((lx - 60 - lb.width) / 2), int((rh - lb.height) / 2)))
        for c in range(len(cols)):
            v = values.get((r, c))
            cx = colx[c] - 30
            if v is None:
                disc = Image.new("RGBA", (96, 96), (0, 0, 0, 0)); ImageDraw.Draw(disc).ellipse([0, 0, 95, 95], fill=(255, 255, 255, 28))
                draw_text(disc, (48, 14), "?", cjk(54), (236, 232, 226, 200), anchor="ma")
                panel.alpha_composite(disc, (int(cx - 48), rh // 2 - 48))
            else:
                fc = flip_counter(v, (46, 64))
                panel.alpha_composite(fc, (int(cx - fc.width / 2), rh // 2 - fc.height // 2))
        cardim.alpha_composite(panel, (30, y))
    cardim = shadow(cardim, 26, (0, 20), 170)
    paste(fr, cardim, 0.5, 0.52)
    tl = label_block(title[0], title[1], 44, 18)
    paste(fr, tl, 0.42, 0.115)
    paste(fr, pip_circle(src, 220), 0.86, 0.115)
    if cap: caption(fr, cap, 0.86)
    return fr.convert("RGB")


def fx_twin_cards(src, cards, cap=None):
    """cards: [(zh, en, tint, icon)] 1–3; sit in the chest band, never on the face."""
    fr = _frame(src, 1.0)
    n = len(cards); cw, ch = (300, 400) if n == 2 else ((360, 460) if n == 1 else (250, 340))
    gap = 60; total = n * cw + (n - 1) * gap; x0 = (W - total) // 2
    cy = int(H * (CHEST_BAND[0] + CHEST_BAND[1]) / 2) + 40
    for i, (zh, en, tint, icon) in enumerate(cards):
        paste(fr, card((cw, ch), zh, en, TINTS[tint], icon), x0 + i * (cw + gap) + cw // 2, cy)
    if cap: caption(fr, cap, 0.83)
    return fr.convert("RGB")


def _counter_row(lab, val, unit, gold=False, big=False):
    th = 96 if big else 70; tw = 150 if big else 118
    tag = rounded((tw, th), 12, (36, 36, 42, 255), stroke=(TOK["gold"] + (170,)) if gold else (255, 255, 255, 40), stroke_w=2 if gold else 1)
    draw_text(tag, (tw / 2, 14 if big else 10), lab, cjk(54 if big else 38), (TOK["gold"] if gold else TOK["white"]) + (255,), anchor="ma")
    cell = (84, 116) if big else ((64, 88) if gold else (56, 76))
    fc = flip_counter(val, cell, fill=TOK["gold"] if gold else TOK["white"], unit=unit)
    row = Image.new("RGBA", (tw + 16 + fc.width, max(fc.height, th)), (0, 0, 0, 0))
    row.alpha_composite(tag, (0, (row.height - th) // 2)); row.alpha_composite(fc, (tw + 16, (row.height - fc.height) // 2))
    return row


def fx_calc_scene(src, cats, counters, total, obj=None, cap=None):
    """cats: [(zh,en,tint,icon)] three small cards on top; counters: [(label, value, unit)] down the
    left; total: (label, value, unit) in gold with an arrow from the counters; big speaker window right."""
    fr = ground_dots().convert("RGBA")
    n = len(cats); cw, ch = 220, 290; gap = 40; x0 = (W - (n * cw + (n - 1) * gap)) // 2
    for i, (zh, en, tint, icon) in enumerate(cats):
        paste(fr, card((cw, ch), zh, en, TINTS[tint], icon, 18), x0 + i * (cw + gap) + cw // 2, 0.21)
    x_left = 70; y = int(H * 0.42)
    for (lab, val, unit) in counters:
        row = _counter_row(lab, val, unit); fr.alpha_composite(row, (x_left, y)); y += row.height + 26
    y += 30
    arrow(fr, (x_left + 60, y - 36), (x_left + 60, y + 4))
    tot = _counter_row(total[0], total[1], total[2], gold=True); fr.alpha_composite(tot, (x_left, y + 10))
    if obj is not None:
        paste(fr, fit(obj, (380, 380)), 0.26, 0.86)
    paste(fr, pip_rect(src, (430, 620)), 0.75, 0.70)
    if cap: caption(fr, cap, 0.90)
    return fr.convert("RGB")


def _phone(screen: Image.Image, size=(470, 960)) -> Image.Image:
    body = rounded(size, 64, (12, 12, 14, 255), stroke=(120, 120, 128, 255), stroke_w=3)
    bez = 14
    scr = screen.convert("RGB").copy()
    sw, sh = size[0] - 2 * bez, size[1] - 2 * bez
    # contain-fit on a white screen (a real screenshot normally fills it exactly)
    canvas = Image.new("RGB", (sw, sh), (250, 250, 250))
    scr.thumbnail((sw - 24, sh - 120), Image.LANCZOS)
    canvas.paste(scr, ((sw - scr.width) // 2, 72))
    body.paste(canvas, (bez, bez), rounded((sw, sh), 52, (255, 255, 255, 255)))
    d = ImageDraw.Draw(body); d.rounded_rectangle([size[0] // 2 - 60, bez + 12, size[0] // 2 + 60, bez + 44], 16, fill=(12, 12, 14, 255))
    return shadow(body, 26, (0, 22), 170)


def fx_split_phone(src, screen, cap=None, tint=None):
    """Speaker (rounded portrait) left, phone with a REAL screenshot right."""
    fr = (ground_diagonal(tint=tint) if tint else ground_dots()).convert("RGBA")
    paste(fr, pip_rect(src, (440, 900), 40), 0.27, 0.50)
    paste(fr, _phone(screen), 0.73, 0.50)
    if cap: caption(fr, cap, 0.84)
    return fr.convert("RGB")


def fx_desk_collage(src, photos, cap=None):
    """2–4 real photos as tilted polaroids on grid paper; small round speaker at the top."""
    fr = ground_paper().convert("RGBA")
    slots = [(0.27, 0.40, -4), (0.74, 0.36, 3), (0.26, 0.74, 2), (0.73, 0.76, -3)][:len(photos)]
    for im, (x, y, ang) in zip(photos, slots):
        pic = im.convert("RGB").copy(); pic.thumbnail((430, 430), Image.LANCZOS)
        pol = Image.new("RGBA", (pic.width + 36, pic.height + 36), (250, 248, 244, 255))
        pol.paste(pic, (18, 18))
        pol = shadow(pol.rotate(ang, expand=True, resample=Image.BICUBIC), 18, (0, 14), 120)
        paste(fr, pol, x, y)
    paste(fr, pip_circle(src, 260, ring=(255, 255, 255)), 0.5, 0.11)
    if cap: caption(fr, cap, 0.90)
    return fr.convert("RGB")


def fx_poster_chapter(src, zh, en, cap=None, color=TOK["orange"]):
    """Pop-art chapter: halftone big word on warm paper, English above, speaker in a centre window."""
    fr = Image.new("RGB", (W, H), (240, 232, 218)).convert("RGBA")
    fr = _vignette(fr.convert("RGB"), 0.15).convert("RGBA")
    smallcaps(fr, (W / 2, int(H * 0.11)), en, 30, color + (255,), tracking=0.22)
    big = halftone_text(zh, 420 if len(zh) <= 2 else 300, color)
    paste(fr, big, 0.5, 0.31)
    # burst behind the window
    d = ImageDraw.Draw(fr); cx, cy = W // 2, int(H * 0.60)
    for k in range(14):
        a = k * math.pi * 2 / 14; r0, r1 = 260, 420 if k % 2 else 340
        d.polygon([(cx + r0 * math.cos(a - 0.06), cy + r0 * math.sin(a - 0.06)), (cx + r1 * math.cos(a), cy + r1 * math.sin(a)),
                   (cx + r0 * math.cos(a + 0.06), cy + r0 * math.sin(a + 0.06))], fill=color + (210,))
    paste(fr, pip_rect(src, (380, 520), 26), 0.5, 0.60)
    if cap: caption(fr, cap, 0.86, fill=(30, 28, 26), italic=True)
    return fr.convert("RGB")


# ───────── added from Hao's second batch of screenshots (2026-10-31) ─────────
def _find_coeffs(pa, pb):
    import numpy as np
    M = []
    for p1, p2 in zip(pa, pb):
        M.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0] * p1[0], -p2[0] * p1[1]])
        M.append([0, 0, 0, p1[0], p1[1], 1, -p2[1] * p1[0], -p2[1] * p1[1]])
    A = np.array(M, dtype=float); B = np.array(pb, dtype=float).reshape(8)
    return tuple(np.linalg.solve(A, B))


def skew_card(im: Image.Image, k=0.10, side="left") -> Image.Image:
    """Mild perspective: the far edge shrinks by k (her outer cards in a trio)."""
    w, h = im.size; dy = int(h * k / 2)
    if side == "left":   # right edge nearer the viewer → left edge shorter
        quad = [(0, dy), (w, 0), (w, h), (0, h - dy)]
    else:
        quad = [(0, 0), (w, dy), (w, h - dy), (0, h)]
    coeffs = _find_coeffs(quad, [(0, 0), (w, 0), (w, h), (0, h)])
    return im.transform((w, h), Image.PERSPECTIVE, coeffs, Image.BICUBIC)


def chip(txt, w=170, h=46, fill=(255, 250, 214), ink=(40, 36, 30)) -> Image.Image:
    """Her pale label pill with the little › disc."""
    im = rounded((w, h), h // 2, fill + (255,))
    draw_text(im, (w / 2 - 14, 6), txt, cjk(28), ink + (255,), anchor="ma")
    d = ImageDraw.Draw(im); d.ellipse([w - h + 8, 8, w - 8, h - 8], fill=ink + (255,))
    d.text((w - h // 2 - 6, 8), "›", font=latin(26), fill=fill + (255,))
    return im


def light_card(size, top, zh, tint=(246, 240, 212)) -> Image.Image:
    """Pale card over footage: a top line (logo text / flag word), then the label pill."""
    c = rounded(size, 18, tint + (255,), stroke=(255, 255, 255, 200), stroke_w=2)
    draw_text(c, (size[0] / 2, size[1] * 0.16), top, cjk(42) if not top.isascii() else font(F_MONO, 36),
              (48, 44, 40, 255), anchor="ma")
    ch = chip(zh, int(size[0] * 0.78))
    c.alpha_composite(ch, ((size[0] - ch.width) // 2, int(size[1] * 0.62)))
    return shadow(c, 14, (0, 10), 130)


def fx_card_row(src, footage: Image.Image, cards, shown=None, cap=None):
    """Letterboxed footage + small PIP; cards appear ONE BY ONE along the bottom of the footage
    (in video: `shown` grows on each matched word). cards: [(top, zh)]."""
    fr = ground_dots().convert("RGBA")
    box_w = 1000; f = footage.convert("RGB").copy(); f = f.resize((box_w, int(box_w * f.height / f.width)), Image.LANCZOS)
    fy = int(H * 0.40 - f.height / 2)
    fr.paste(f, ((W - box_w) // 2, fy))
    paste(fr, pip_circle(src, 220, ring=(255, 255, 255)), 0.84, (fy + 90) / H)
    n = len(cards); cw, ch = 200, 240; gap = 24; x0 = (W - (n * cw + (n - 1) * gap)) // 2
    for i, (top, zh) in enumerate(cards[: (shown if shown is not None else n)]):
        paste(fr, light_card((cw, ch), top, zh), x0 + i * (cw + gap) + cw // 2, fy + f.height - 150)
    if cap: caption(fr, cap, 0.73)
    return fr.convert("RGB")


def fx_side_tag(src, zh, en, tint="violet", img: Image.Image | None = None, side="left", cap=None):
    """Tall card parked at the frame edge at hand height; slides in while he keeps talking."""
    fr = _frame(src, 1.0)
    cw, ch = 300, 640
    p = tint_panel((cw, ch), TINTS[tint], 26)
    lb = label_block(zh, en, 52 if len(zh) <= 3 else 40, 16, width=cw - 30)
    p.alpha_composite(lb, ((cw - lb.width) // 2, 60))
    if img is not None:
        pic = fit(img, (cw - 60, ch - 260)); p.alpha_composite(pic, ((cw - pic.width) // 2, ch - pic.height - 30))
    p = shadow(p, 20, (0, 14), 150)
    paste(fr, p, 0.16 if side == "left" else 0.84, 0.64)
    if cap: caption(fr, cap, 0.80)
    return fr.convert("RGB")


def fx_logo_trio(src, labels, shown=3, cap=None):
    """Two black name cards at hand level, then a third, larger, in the middle (her HYROX / LOWROX / LiNROX)."""
    fr = _frame(src, 1.0)
    cy = int(H * 0.66)
    def plate(txt, w, h, size):
        c = Image.new("RGBA", (w, h), (10, 10, 12, 255))
        draw_text(c, (w / 2, (h - size) / 2 - 4), txt.upper(), latin(size), (240, 236, 228, 255), spacing=0.32, anchor="ma")
        return c
    L = skew_card(plate(labels[0], 290, 210, 34), 0.12, "left"); R = skew_card(plate(labels[1], 290, 210, 34), 0.12, "right")
    if shown >= 1: paste(fr, shadow(L, 14, (0, 10), 140), 0.165, cy)
    if shown >= 2: paste(fr, shadow(R, 14, (0, 10), 140), 0.835, cy)
    if shown >= 3 and len(labels) > 2:
        paste(fr, shadow(plate(labels[2], 380, 250, 50), 18, (0, 14), 170), 0.50, cy - 10)
    if cap: caption(fr, cap, 0.80)
    return fr.convert("RGB")


def fx_photo_fan(src, photos, cap=None):
    """Three real photos fanned across the lower third of the face shot; caption sits ABOVE them."""
    fr = _frame(src, 1.0)
    slots = [(0.30, 0.76, -7), (0.72, 0.74, 5), (0.50, 0.88, -2)]
    for im, (x, y, ang) in zip(photos, slots):
        pic = im.convert("RGB").copy(); pic.thumbnail((500, 380), Image.LANCZOS)
        pol = Image.new("RGBA", (pic.width + 24, pic.height + 24), (250, 248, 244, 255)); pol.paste(pic, (12, 12))
        paste(fr, shadow(pol.rotate(ang, expand=True, resample=Image.BICUBIC), 18, (0, 14), 150), x, y)
    if cap: caption(fr, cap, 0.57)
    return fr.convert("RGB")
