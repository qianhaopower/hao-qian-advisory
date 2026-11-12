import type { ReactNode } from "react";
import type { Lang, PillarId } from "@/lib/today-deck";

/*
 * The drawings on the /today cards — one small cartoon per episode, in one
 * hand: thick ink outline, flat bright fills, faces with a blush.
 *
 * Rules for a scene:
 *  - Canvas is 368 × 236; the ground line sits at y = 214.
 *  - Keep the top-left corner (x < 110, y < 44) clear: the card prints its
 *    number there. If the card has a `when` sticker, keep the bottom-right
 *    (x > 250, y > 194) clear too.
 *  - Literal hex colours only, and no CSS classes: the share image redraws
 *    the drawing outside the page, where the site's tokens do not exist.
 *  - <text> only through Label (words, in both languages) or Num (figures),
 *    never inside a transformed group: the share image lifts the lettering
 *    out and sets it again in canvas.
 *  - Draw what the episode is about. No decoration for its own sake.
 */

const INK = "#1F1D1A";
const PAPER = "#FFFDF8";
const GOLD = "#F2B632";
const SUN = "#F9D65C";
const RED = "#E4572E";
const CORAL = "#FF8A5B";
const BLUE = "#4A90D9";
const SKY = "#BFE3FF";
const LEAF = "#2F8F5B";
const GREEN = "#4CAF72";
const MINT = "#9BD4A4";
const BLUSH = "#FF9E8A";
const WOOD = "#E8C9A0";
const COCOA = "#7A4B2A";
const GREY = "#C9C4B8";
const SLATE = "#57534A";
const CREAM = "#FFE2A8";
const PERI = "#CFDDFB";
const ROSE = "#FFD2C8";
const SAGE = "#CDEBD3";
const STORM = "#C9D3E6";

const ZH_FONT =
  'var(--font-noto-serif-sc), "Songti SC", "Noto Serif CJK SC", serif';
const NUM_FONT = "var(--font-newsreader), Georgia, serif";

type EyeKind = "dot" | "happy" | "sleepy" | "wide" | "grumpy";
type MouthKind = "smile" | "grin" | "frown" | "o" | "flat";

function Eyes({
  x,
  y,
  gap = 28,
  k = "dot",
  look = 0,
  lookY = 0,
}: {
  x: number;
  y: number;
  gap?: number;
  k?: EyeKind;
  look?: number;
  lookY?: number;
}) {
  const l = x - gap / 2;
  const r = x + gap / 2;
  if (k === "happy")
    return <path d={`M${l - 7} ${y + 3}q7-10 14 0M${r - 7} ${y + 3}q7-10 14 0`} />;
  if (k === "sleepy")
    return <path d={`M${l - 7} ${y}q7 8 14 0M${r - 7} ${y}q7 8 14 0`} />;
  if (k === "wide")
    return (
      <>
        <circle cx={l} cy={y} r={9} fill={PAPER} strokeWidth={2.5} />
        <circle cx={r} cy={y} r={9} fill={PAPER} strokeWidth={2.5} />
        <circle cx={l + look} cy={y + lookY} r={4} fill={INK} stroke="none" />
        <circle cx={r + look} cy={y + lookY} r={4} fill={INK} stroke="none" />
      </>
    );
  return (
    <>
      <circle cx={l} cy={y} r={4.5} fill={INK} stroke="none" />
      <circle cx={r} cy={y} r={4.5} fill={INK} stroke="none" />
      {k === "grumpy" && (
        <path d={`M${l - 8} ${y - 12}l13 5M${r + 8} ${y - 12}l-13 5`} />
      )}
    </>
  );
}

function Mouth({
  x,
  y,
  k = "smile",
  w = 24,
}: {
  x: number;
  y: number;
  k?: MouthKind;
  w?: number;
}) {
  const h = w / 2;
  if (k === "grin")
    return <path d={`M${x - h} ${y}q${h} ${h + 4} ${w} 0z`} fill={PAPER} />;
  if (k === "frown") return <path d={`M${x - h} ${y + 6}q${h} ${-h} ${w} 0`} />;
  if (k === "o") return <circle cx={x} cy={y + 3} r={5} fill={INK} stroke="none" />;
  if (k === "flat") return <path d={`M${x - h} ${y + 3}h${w}`} />;
  return <path d={`M${x - h} ${y}q${h} ${h} ${w} 0`} />;
}

function Face({
  x,
  y,
  eyes = "dot",
  mouth = "smile",
  gap = 28,
  look = 0,
  lookY = 0,
  blush = true,
  bw,
  br = 7,
  mw = 24,
}: {
  x: number;
  y: number;
  eyes?: EyeKind;
  mouth?: MouthKind;
  gap?: number;
  look?: number;
  lookY?: number;
  blush?: boolean;
  /** half the distance between the two blush marks */
  bw?: number;
  br?: number;
  mw?: number;
}) {
  const b = bw ?? gap / 2 + 17;
  return (
    <>
      {blush && (
        <>
          <circle cx={x - b} cy={y + 14} r={br} fill={BLUSH} stroke="none" />
          <circle cx={x + b} cy={y + 14} r={br} fill={BLUSH} stroke="none" />
        </>
      )}
      <Eyes x={x} y={y} gap={gap} k={eyes} look={look} lookY={lookY} />
      <Mouth x={x} y={y + 14} k={mouth} w={mw} />
    </>
  );
}

/** The deck's little person: a round body, two legs, one face. */
function Buddy({
  x,
  y,
  r = 44,
  fill = PAPER,
  eyes = "happy",
  mouth = "smile",
  look = 0,
  lookY = 0,
  legs = true,
  fy,
}: {
  x: number;
  y: number;
  r?: number;
  fill?: string;
  eyes?: EyeKind;
  mouth?: MouthKind;
  look?: number;
  lookY?: number;
  legs?: boolean;
  /** face offset from the centre */
  fy?: number;
}) {
  const foot = Math.min(212, y + r + 14);
  const gap = eyes === "wide" ? Math.max(24, r * 0.62) : r * 0.6;
  return (
    <>
      {legs && (
        <path
          d={`M${x - r * 0.35} ${y + r - 6}V${foot}M${x + r * 0.35} ${y + r - 6}V${foot}`}
          strokeWidth={5}
        />
      )}
      <circle cx={x} cy={y} r={r} fill={fill} />
      <Face
        x={x}
        y={y + (fy ?? -r * 0.14)}
        eyes={eyes}
        mouth={mouth}
        gap={gap}
        look={look}
        lookY={lookY}
        bw={r * 0.66}
        br={r * 0.15}
        mw={r * 0.5}
      />
    </>
  );
}

function Spark({ x, y, r = 9 }: { x: number; y: number; r?: number }) {
  const a = r / 3;
  const b = (r * 2) / 3;
  return (
    <path
      d={`M${x} ${y - r}l${a} ${b} ${b} ${a} ${-b} ${a} ${-a} ${b} ${-a} ${-b} ${-b} ${-a} ${b} ${-a}z`}
      fill={SUN}
      strokeWidth={2}
    />
  );
}

function Ground() {
  return <path d="M16 214h336" strokeWidth={2} />;
}

function Tick({ x, y, r = 15 }: { x: number; y: number; r?: number }) {
  return (
    <>
      <circle cx={x} cy={y} r={r} fill={LEAF} strokeWidth={2.5} />
      <path d={`M${x - 7} ${y}l5 6 9-11`} stroke={PAPER} strokeWidth={3.5} />
    </>
  );
}

function Cross({ x, y, r = 15 }: { x: number; y: number; r?: number }) {
  return (
    <>
      <circle cx={x} cy={y} r={r} fill={PAPER} strokeWidth={2.5} />
      <path
        d={`M${x - 6} ${y - 6}l12 12M${x + 6} ${y - 6}l-12 12`}
        stroke="#C0392B"
        strokeWidth={3.5}
      />
    </>
  );
}

function Heart({ x, y, s = 1 }: { x: number; y: number; s?: number }) {
  return (
    <path
      transform={`translate(${x} ${y}) scale(${s})`}
      d="M0 22c-26-16-30-36-16-44 8-5 16 2 16 8 0-6 8-13 16-8 14 8 10 28-16 44z"
      fill={RED}
      strokeWidth={3 / s}
    />
  );
}

function Zs({ x, y }: { x: number; y: number }) {
  return (
    <>
      <path d={`M${x} ${y}h12l-12 14h12`} strokeWidth={2.5} />
      <path d={`M${x + 18} ${y - 30}h16l-16 18h16`} />
    </>
  );
}

function Disc({
  x,
  y,
  r,
  fill = GOLD,
}: {
  x: number;
  y: number;
  r: number;
  fill?: string;
}) {
  return <circle cx={x} cy={y} r={r} fill={fill} />;
}

/** Speech bubble with a tail pointing at (tx, ty), which sits below the box. */
function Bubble({
  x,
  y,
  w,
  h,
  tx,
  ty,
}: {
  x: number;
  y: number;
  w: number;
  h: number;
  tx: number;
  ty: number;
}) {
  const bx = Math.max(x + 14, Math.min(tx, x + w - 38));
  return (
    <>
      <path d={`M${bx} ${y + h - 2}L${tx} ${ty}L${bx + 24} ${y + h - 2}z`} fill={PAPER} />
      <rect x={x} y={y} width={w} height={h} rx={16} fill={PAPER} />
      <path d={`M${bx + 3} ${y + h}h18`} stroke={PAPER} strokeWidth={4} strokeLinecap="butt" />
    </>
  );
}

function Zh({
  x,
  y,
  s = 16,
  a = "middle",
  fill = INK,
  children,
}: {
  x: number;
  y: number;
  s?: number;
  a?: "start" | "middle" | "end";
  fill?: string;
  children: string;
}) {
  return (
    <text
      x={x}
      y={y}
      fontSize={s}
      textAnchor={a}
      fill={fill}
      stroke="none"
      style={{ fontFamily: ZH_FONT, fontWeight: 900 }}
    >
      {children}
    </text>
  );
}

function Num({
  x,
  y,
  s = 24,
  a = "middle",
  fill = INK,
  children,
}: {
  x: number;
  y: number;
  s?: number;
  a?: "start" | "middle" | "end";
  fill?: string;
  children: string;
}) {
  return (
    <text
      x={x}
      y={y}
      fontSize={s}
      textAnchor={a}
      fill={fill}
      stroke="none"
      style={{ fontFamily: NUM_FONT, fontWeight: 600 }}
    >
      {children}
    </text>
  );
}

/** Lettering inside a drawing, in the language of the card being shown. */
function Label({
  lang,
  x,
  y,
  s = 16,
  a = "middle",
  fill = INK,
  zh,
  en,
  es,
  ey,
}: {
  lang: Lang;
  x: number;
  y: number;
  s?: number;
  a?: "start" | "middle" | "end";
  fill?: string;
  zh: string;
  en: string;
  /** size of the English lettering (Latin runs wider than Chinese) */
  es?: number;
  /** baseline of the English lettering, when it must sit differently */
  ey?: number;
}) {
  return lang === "en" ? (
    <Num x={x} y={ey ?? y} s={es ?? s} a={a} fill={fill}>
      {en}
    </Num>
  ) : (
    <Zh x={x} y={y} s={s} a={a} fill={fill}>
      {zh}
    </Zh>
  );
}

function Apple({ dx = 0 }: { dx?: number }) {
  return (
    <g transform={`translate(${dx} 0)`}>
      <path
        d="M118 92c-30-14-60 6-60 46 0 36 24 64 44 64 8 0 10-4 16-4s8 4 16 4c20 0 44-28 44-64 0-40-30-60-60-46z"
        fill={RED}
      />
      <path d="M118 92c0-14 4-22 12-28" strokeWidth={4} />
      <path d="M130 70c10-10 24-10 30-4-8 10-22 12-30 4z" fill={MINT} />
      <Face x={118} y={138} eyes="happy" mouth="grin" gap={30} blush={false} mw={28} />
    </g>
  );
}

/* ── The scenes, by episode slug ───────────────────────────────────────── */

const SCENES: Record<string, (lang: Lang) => ReactNode> = {
  /* 睡眠 */
  "fi-sleep-daylight": () => (
    <>
      <Ground />
      <path
        d="M272 26v12M272 130v12M214 84h12M318 84h12M231 43l9 9M304 116l9 9M313 43l-9 9M240 116l-9 9"
        stroke={GOLD}
        strokeWidth={4}
      />
      <circle cx={272} cy={84} r={36} fill={SUN} />
      <Face x={272} y={78} eyes="happy" mouth="smile" gap={24} bw={24} />
      <path d="M76 132c-16-18-16-38-6-54M148 132c16-18 16-38 6-54" strokeWidth={5} />
      <circle cx={70} cy={74} r={9} fill={PAPER} />
      <circle cx={154} cy={74} r={9} fill={PAPER} />
      <Buddy x={112} y={152} r={46} eyes="happy" mouth="grin" />
      <Spark x={196} y={156} r={8} />
      <Spark x={338} y={152} r={7} />
    </>
  ),

  "fi-coffee": () => (
    <>
      <path d="M306 30a34 34 0 1 0 34 44a27 27 0 0 1-34-44z" fill={SUN} />
      <Spark x={262} y={46} r={8} />
      <Spark x={344} y={120} r={6} />
      <circle cx={92} cy={108} r={46} fill={PAPER} />
      <path d="M92 68v6M92 142v6M52 108h6" strokeWidth={2.5} />
      <circle cx={126} cy={108} r={11} fill={GOLD} strokeWidth={2} />
      <path d="M92 108V78" />
      <path d="M92 108h20" strokeWidth={5} />
      <circle cx={92} cy={108} r={4} fill={INK} stroke="none" />
      <path d="M70 152l-8 18M114 152l8 18" />
      <ellipse cx={230} cy={205} rx={76} ry={8} fill={PAPER} />
      <path d="M284 132c30 0 30 46 0 46" strokeWidth={9} />
      <path d="M284 132c30 0 30 46 0 46" stroke={PAPER} />
      <path d="M176 112h108v72a20 20 0 0 1-20 20h-68a20 20 0 0 1-20-20z" fill={PAPER} />
      <ellipse cx={230} cy={112} rx={54} ry={10} fill={COCOA} />
      <Face x={230} y={150} eyes="sleepy" mouth="o" gap={36} bw={34} />
      <path d="M214 96c-8-10 8-14 0-26M238 92c-8-10 8-14 0-26" strokeWidth={2.5} />
      <Zs x={154} y={74} />
      <Ground />
    </>
  ),

  "fi-dim-lights": () => (
    <>
      <Ground />
      <path d="M140 0v44" />
      <path d="M112 44h56l16 44H96z" fill={GREY} />
      <path d="M118 88a22 22 0 0 0 44 0z" fill={PAPER} />
      <Eyes x={140} y={66} k="sleepy" gap={26} />
      <Zs x={192} y={58} />
      <rect x={44} y={120} width={28} height={44} rx={5} fill={PAPER} />
      <path d="M58 146v10" strokeWidth={6} />
      <path d="M236 170h96M250 170v44M318 170v44" />
      <path d="M270 170v-26" />
      <path d="M252 144h36l-8-34h-20z" fill={SUN} />
      <path
        d="M240 118l-12-6M300 118l12-6M270 98v-12M246 104l-8-10M294 104l8-10"
        stroke={GOLD}
      />
    </>
  ),

  "fi-temperature": () => (
    <>
      <Ground />
      <rect x={110} y={40} width={36} height={136} rx={18} fill={PAPER} />
      <path d="M128 150V98" stroke={BLUE} strokeWidth={10} />
      <circle cx={128} cy={178} r={30} fill={SKY} />
      <path d="M146 64h10M146 88h10M146 112h10M146 136h10" strokeWidth={2.5} />
      <Face x={128} y={172} eyes="happy" mouth="smile" gap={22} bw={20} br={5} mw={16} />
      <Num x={240} y={134} s={84}>
        −2°
      </Num>
      <path d="M338 76v56M324 116l14 16 14-16" stroke={BLUE} strokeWidth={5} />
      <path d="M204 40v24M192 46l24 12M216 46l-24 12" stroke={BLUE} strokeWidth={2.5} />
      <path d="M190 168v24M178 174l24 12M202 174l-24 12" stroke={BLUE} strokeWidth={2.5} />
    </>
  ),

  "fi-sleep-appetite": () => (
    <>
      <Ground />
      <path d="M300 34a30 30 0 1 0 30 38a24 24 0 0 1-30-38z" fill={SUN} />
      <Spark x={250} y={50} r={6} />
      <Spark x={206} y={78} r={5} />
      <path d="M40 104v108M262 170v42" strokeWidth={6} />
      <rect x={40} y={160} width={224} height={34} rx={8} fill={PAPER} />
      <ellipse cx={84} cy={156} rx={32} ry={12} fill={PAPER} />
      <circle cx={94} cy={134} r={24} fill={CREAM} />
      <Eyes x={96} y={134} k="sleepy" gap={20} />
      <Mouth x={96} y={144} k="smile" w={10} />
      <rect x={114} y={140} width={150} height={54} rx={14} fill={SKY} />
      <Zs x={130} y={112} />
      <circle cx={318} cy={150} r={26} fill="#F6A8C0" />
      <circle cx={318} cy={152} r={8} fill={PAPER} />
      <Eyes x={318} y={136} k="dot" gap={16} />
      <path d="M298 148l4 4M336 144l-4 4M304 164l3-3" stroke={PAPER} strokeWidth={2.5} />
    </>
  ),

  /* 关系 */
  "fi-couple-20min": (lang) => (
    <>
      <Ground />
      <rect x={40} y={96} width={200} height={84} rx={20} fill="#E7B7D6" />
      <Buddy x={104} y={128} r={34} fill={CREAM} eyes="wide" look={3} legs={false} />
      <Buddy x={176} y={128} r={34} fill={PERI} eyes="wide" look={-3} legs={false} />
      <rect x={28} y={152} width={224} height={42} rx={14} fill="#F3D4E8" />
      <path d="M52 194v18M228 194v18" strokeWidth={5} />
      <Heart x={140} y={62} s={0.6} />
      <path d="M306 58V46M294 46h24" strokeWidth={4} />
      <circle cx={306} cy={96} r={38} fill={PAPER} />
      <Num x={306} y={104} s={34}>
        20
      </Num>
      <Label lang={lang} x={306} y={122} s={12} zh="分钟" en="min" es={12} />
    </>
  ),

  "fi-fake-egg": () => (
    <>
      <Ground />
      <circle cx={140} cy={174} r={38} fill="#D9E64A" />
      <path
        d="M110 152c18 10 24 34 14 54M170 152c-18 10-24 34-14 54"
        stroke={PAPER}
      />
      <path d="M88 108l-16-14 4 26z" fill={PAPER} />
      <ellipse cx={140} cy={118} rx={56} ry={38} fill={PAPER} />
      <path d="M106 114c14 16 40 18 56 4" />
      <circle cx={186} cy={84} r={24} fill={PAPER} />
      <path d="M206 78l24 8-24 8z" fill={CORAL} />
      <circle cx={192} cy={78} r={4} fill={INK} stroke="none" />
      <circle cx={178} cy={92} r={5} fill={BLUSH} stroke="none" />
      <ellipse cx={296} cy={180} rx={22} ry={30} fill="#FFF3D1" />
      <Eyes x={296} y={174} k="dot" gap={16} />
      <Mouth x={296} y={182} k="frown" w={12} />
      <path d="M322 150c-3 6-4 10 0 12 4-2 3-6 0-12z" fill={SKY} strokeWidth={2} />
      <Num x={296} y={132} s={30}>
        ?
      </Num>
    </>
  ),

  "fi-consistency": () => (
    <>
      <Ground />
      <rect x={150} y={40} width={84} height={174} rx={4} fill={WOOD} />
      <rect x={164} y={56} width={56} height={56} rx={3} strokeWidth={2} />
      <circle cx={220} cy={134} r={5} fill={GOLD} strokeWidth={2} />
      <rect x={52} y={204} width={84} height={10} rx={3} fill={CORAL} strokeWidth={2} />
      <path
        d="M52 128a22 22 0 0 1 14-40a28 28 0 0 1 52-4a22 22 0 0 1 6 44z"
        fill={STORM}
      />
      <Eyes x={88} y={104} k="grumpy" gap={24} />
      <Mouth x={88} y={110} k="frown" w={14} />
      <path d="M64 142l-4 12M88 142l-4 12M112 142l-4 12" stroke={BLUE} />
      <path d="M296 92V80M254 110l-9-8M338 110l9-8" stroke={GOLD} strokeWidth={4} />
      <Buddy x={296} y={148} r={40} fill={SUN} eyes="happy" mouth="grin" />
    </>
  ),

  "fi-touch": () => (
    <>
      <Ground />
      <path d="M152 160c12 10 22 12 32 8M216 160c-12 10-22 12-32 8" strokeWidth={5} />
      <Buddy x={112} y={146} r={44} fill={ROSE} />
      <Buddy x={256} y={146} r={44} fill={SAGE} />
      <circle cx={184} cy={168} r={10} fill={PAPER} />
      <Heart x={184} y={112} s={0.7} />
      <Heart x={158} y={72} s={0.4} />
      <Heart x={214} y={60} s={0.5} />
      <Spark x={60} y={72} />
      <Spark x={320} y={72} r={7} />
    </>
  ),

  "fi-contra": (lang) => (
    <>
      <Ground />
      <Buddy x={70} y={156} r={30} fill={CREAM} eyes="wide" look={3} mouth="flat" />
      <Buddy x={138} y={156} r={30} fill={PERI} eyes="wide" look={3} mouth="flat" />
      <path d="M43 141q27-12 54 0M111 141q27-12 54 0" stroke={RED} strokeWidth={5} />
      <path
        d="M180 148h56M180 164h56"
        stroke={GOLD}
        strokeWidth={4}
        strokeDasharray="2 10"
      />
      <path
        d="M290 78l12 20 22-8-4 24 22 10-18 14 10 22-24-2-8 22-14-18-20 12 0-24-22-8 16-16-12-20 24 2z"
        fill="#B08BC0"
      />
      <Eyes x={290} y={126} k="grumpy" gap={24} />
      <Mouth x={290} y={136} k="frown" w={16} />
      <Label lang={lang} x={290} y={62} s={18} zh="问题" en="the problem" es={14} />
    </>
  ),

  "fi-eye-contact": () => (
    <>
      <path d="M86 202v12M122 202v12M246 202v12M282 202v12" strokeWidth={5} />
      <circle cx={104} cy={150} r={56} fill={CREAM} />
      <circle cx={264} cy={150} r={56} fill={PERI} />
      <circle cx={76} cy={164} r={8} fill={BLUSH} stroke="none" />
      <circle cx={292} cy={164} r={8} fill={BLUSH} stroke="none" />
      <Eyes x={111} y={138} k="wide" gap={34} look={5} />
      <Eyes x={257} y={138} k="wide" gap={34} look={-5} />
      <path d="M100 166q12 12 24 0M244 166q12 12 24 0" />
      <path d="M150 138h70" stroke={RED} strokeWidth={3.5} strokeDasharray="1 10" />
      <Heart x={184} y={70} s={1} />
      <path d="M74 98c6-10 16-16 28-16M294 98c-6-10-16-16-28-16" strokeWidth={2.5} />
      <Spark x={44} y={72} />
      <Spark x={328} y={64} />
      <Ground />
    </>
  ),

  /* 营养 */
  "fi-supermarket": () => (
    <>
      <Ground />
      <rect x={34} y={62} width={70} height={100} rx={4} fill={SUN} />
      <path d="M44 84l5 6 9-11" stroke={LEAF} strokeWidth={3.5} />
      <path d="M45 138l10 10M55 138l-10 10" stroke="#C0392B" strokeWidth={3.5} />
      <path d="M68 86h26M68 116h26M68 144h26" strokeWidth={2.5} />
      <Num x={51} y={124} s={22}>
        ?
      </Num>
      <circle cx={178} cy={82} r={15} fill={RED} />
      <path d="M222 94V68l10-10 10 10v26z" fill={SKY} />
      <path d="M262 94c-6-14 2-28 14-30 6 12 0 24-14 30z" fill={MINT} />
      <path d="M132 92h150l-16 70H148z" fill={PAPER} />
      <path d="M132 92l-10-22H98" strokeWidth={5} />
      <path d="M148 162l-6 22h130" />
      <circle cx={160} cy={198} r={10} fill={PAPER} />
      <circle cx={256} cy={198} r={10} fill={PAPER} />
      <Face x={207} y={118} eyes="happy" mouth="smile" gap={30} />
      <Spark x={326} y={62} />
    </>
  ),

  "fi-six-countries": () => (
    <>
      <Ground />
      <path d="M40 64v130h160" />
      <g fill={GREY} stroke="none">
        <circle cx={60} cy={150} r={5} />
        <circle cx={74} cy={106} r={5} />
        <circle cx={92} cy={176} r={5} />
        <circle cx={98} cy={86} r={5} />
        <circle cx={118} cy={170} r={5} />
        <circle cx={124} cy={96} r={5} />
        <circle cx={142} cy={150} r={5} />
        <circle cx={150} cy={78} r={5} />
        <circle cx={166} cy={132} r={5} />
        <circle cx={172} cy={176} r={5} />
        <circle cx={186} cy={112} r={5} />
      </g>
      <path d="M52 183L192 73" strokeDasharray="6 7" strokeWidth={2.5} />
      <g fill={GOLD} strokeWidth={2}>
        <circle cx={58} cy={178} r={6.5} />
        <circle cx={84} cy={158} r={6.5} />
        <circle cx={108} cy={139} r={6.5} />
        <circle cx={134} cy={119} r={6.5} />
        <circle cx={160} cy={98} r={6.5} />
        <circle cx={186} cy={78} r={6.5} />
      </g>
      <path
        d="M286 96c-10-22-4-36 4-44M286 96c0-24 10-34 20-38M286 96c8-18 22-24 34-22"
        stroke={LEAF}
        strokeWidth={4}
      />
      <path
        d="M262 96c20-8 44-2 48 10 4 14-20 70-34 92-14-22-30-80-14-102z"
        fill={CORAL}
      />
      <Face x={286} y={120} eyes="happy" mouth="smile" gap={18} bw={17} br={4} mw={14} />
    </>
  ),

  "fi-sugar-names": (lang) => (
    <>
      <Ground />
      <rect x={50} y={56} width={120} height={150} rx={10} fill={PAPER} />
      <Label lang={lang} x={110} y={84} s={15} zh="配料表" en="INGREDIENTS" es={11} />
      <path
        d="M66 100h88M66 116h70M66 132h56M66 148h40M66 164h46M66 180h60"
        stroke={GREY}
        strokeWidth={2.5}
      />
      <path d="M216 178l28 28" strokeWidth={9} />
      <circle cx={186} cy={146} r={44} fill="#FFF3D1" />
      <rect x={166} y={126} width={40} height={40} rx={6} fill={PAPER} />
      <circle cx={177} cy={142} r={7} strokeWidth={2.5} />
      <circle cx={195} cy={142} r={7} strokeWidth={2.5} />
      <path d="M184 142h4" strokeWidth={2.5} />
      <path d="M176 156q5-6 10 0q5-6 10 0" />
      <Num x={300} y={124} s={80}>
        23
      </Num>
      <Label lang={lang} x={300} y={152} s={18} zh="个化名" en="aliases" es={18} />
    </>
  ),

  "fi-glycation": () => (
    <>
      <Ground />
      <path
        d="M112 120V70c-12-4-12-28 10-28h46c22 0 22 24 10 28v50z"
        fill="#E9B872"
      />
      <Face x={145} y={72} eyes="wide" mouth="o" gap={24} blush={false} />
      <path d="M94 82c-6-8 6-12 0-22M198 82c-6-8 6-12 0-22" stroke={RED} strokeWidth={2.5} />
      <path d="M92 200v12M198 200v12" strokeWidth={5} />
      <rect x={70} y={112} width={150} height={90} rx={18} fill={CORAL} />
      <path d="M100 113h90" strokeWidth={5} />
      <path d="M220 140h16v26" strokeWidth={5} />
      <circle cx={96} cy={178} r={6} fill={PAPER} strokeWidth={2.5} />
      <rect x={264} y={56} width={28} height={28} rx={5} fill={PAPER} />
      <rect x={302} y={96} width={28} height={28} rx={5} fill={PAPER} />
      <rect x={258} y={134} width={28} height={28} rx={5} fill={PAPER} />
      <Spark x={322} y={56} r={7} />
      <Spark x={316} y={158} r={6} />
    </>
  ),

  "fi-brain-brake": () => (
    <>
      <Ground />
      <rect x={50} y={48} width={160} height={166} rx={6} fill={WOOD} />
      <rect x={134} y={58} width={68} height={148} fill={SLATE} strokeWidth={2.5} />
      <path d="M134 136h68" stroke={WOOD} strokeWidth={5} />
      <path d="M148 96l6-6 6 6 6-6 6 6 6-6 6 6v38h-36z" fill={SUN} strokeWidth={2.5} />
      <Eyes x={166} y={112} k="sleepy" gap={14} />
      <path d="M130 48v166" />
      <circle cx={118} cy={132} r={4} fill={INK} stroke="none" />
      <path d="M210 48l36 14v152h-36z" fill={WOOD} />
      <path d="M278 88V64l16-4v24" />
      <circle cx={273} cy={90} r={5} fill={INK} stroke="none" />
      <circle cx={289} cy={86} r={5} fill={INK} stroke="none" />
      <Buddy x={306} y={152} r={36} eyes="happy" mouth="o" />
    </>
  ),

  "fi-insulin-rollercoaster": () => (
    <>
      <Ground />
      <ellipse cx={104} cy={194} rx={70} ry={12} fill={PAPER} />
      <path d="M96 192v-42h16v42z" fill={MINT} />
      <circle cx={80} cy={130} r={24} fill={GREEN} />
      <circle cx={128} cy={130} r={24} fill={GREEN} />
      <circle cx={104} cy={110} r={28} fill={GREEN} />
      <circle cx={104} cy={128} r={22} fill={GREEN} stroke="none" />
      <Face x={104} y={122} eyes="happy" mouth="smile" gap={22} blush={false} mw={18} />
      <Disc x={44} y={84} r={18} />
      <Num x={44} y={93} s={26}>
        1
      </Num>
      <path d="M170 104c12-16 30-16 42 0" strokeDasharray="3 8" />
      <path d="M202 92l10 12-15 3" />
      <path d="M228 158c0-36 96-36 96 0z" fill={PAPER} />
      <path d="M216 156h120c0 34-22 50-60 50s-60-16-60-50z" fill={SKY} />
      <Face x={276} y={172} eyes="sleepy" mouth="smile" gap={24} mw={18} />
      <Disc x={336} y={92} r={18} />
      <Num x={336} y={101} s={26}>
        2
      </Num>
    </>
  ),

  "fi-fatty-acid": () => (
    <>
      <Ground />
      <path d="M78 140c-16-6-20-22-34-20M178 140c16-6 20-22 34-20" strokeWidth={5} />
      <path d="M112 196v16M146 196v16" strokeWidth={5} />
      <path
        d="M128 84c36 0 56 24 56 58s-20 58-56 58-56-24-56-58 20-58 56-58z"
        fill="#C89B6A"
      />
      <path
        d="M128 84v18M128 184v16M88 112c8-8 16 4 24-4M144 108c8-6 16 6 24-2M90 180c10 6 16-6 26 0M142 182c8-6 18 4 26-2"
        strokeWidth={2.5}
      />
      <Face x={128} y={136} eyes="happy" mouth="grin" gap={28} />
      <path d="M252 122l-22-16v32z" fill={SKY} />
      <path d="M252 122c16-22 56-22 72 0-16 22-56 22-72 0z" fill={SKY} />
      <circle cx={304} cy={118} r={3.5} fill={INK} stroke="none" />
      <path d="M286 108c-6 8-6 20 0 28" strokeWidth={2} />
      <Disc x={300} y={58} r={24} />
      <Num x={300} y={66} s={22}>
        Ω3
      </Num>
      <circle cx={340} cy={96} r={4} strokeWidth={2} />
      <circle cx={346} cy={146} r={3} strokeWidth={2} />
    </>
  ),

  "fi-also-sugar": (lang) => (
    <>
      <Ground />
      <Apple />
      <Tick x={180} y={84} />
      <path d="M284 86V58l14-8" strokeWidth={5} />
      <rect x={240} y={86} width={64} height={126} rx={6} fill={CORAL} />
      <path d="M240 106h64" />
      <Eyes x={272} y={128} k="wide" gap={24} look={-3} />
      <path d="M266 144h12" />
      <rect x={240} y={158} width={64} height={28} fill={PAPER} />
      <Label lang={lang} x={272} y={178} s={15} zh="0蔗糖" en="0 sugar" es={13} />
      <rect x={316} y={130} width={20} height={20} rx={4} fill={PAPER} strokeWidth={2.5} />
      <rect x={326} y={98} width={20} height={20} rx={4} fill={PAPER} strokeWidth={2.5} />
    </>
  ),

  "fi-trans-fat": () => (
    <>
      <Ground />
      <path
        d="M110 212c-8-12 4-16 0-26 10 6 14 16 8 26zM150 212c-8-12 4-16 0-26 10 6 14 16 8 26zM190 212c-8-12 4-16 0-26 10 6 14 16 8 26z"
        fill={CORAL}
        strokeWidth={2}
      />
      <path d="M238 158l86-20" strokeWidth={11} />
      <path d="M70 150h170l-12 36H82z" fill={SLATE} />
      <ellipse cx={155} cy={150} rx={85} ry={14} fill={SUN} />
      <path d="M128 140c-6-8 6-12 0-20M178 140c-6-8 6-12 0-20" strokeWidth={2.5} />
      <path
        d="M112 118a20 20 0 0 1 8-38a30 30 0 0 1 58-6a22 22 0 0 1 12 44z"
        fill={GREY}
      />
      <Eyes x={150} y={88} k="wide" gap={24} />
      <Mouth x={150} y={100} k="o" />
      <Cross x={208} y={64} />
      <Spark x={300} y={72} />
    </>
  ),

  "fi-free-radical": () => (
    <>
      <ellipse cx={184} cy={190} rx={150} ry={20} fill={PAPER} />
      <path d="M92 120l-10-10M92 120l10-10M92 120v-14" stroke={LEAF} strokeWidth={4} />
      <circle cx={92} cy={152} r={32} fill={RED} />
      <Face x={92} y={148} eyes="happy" mouth="smile" gap={22} blush={false} mw={18} />
      <path d="M158 186v-36h16v36z" fill={MINT} />
      <circle cx={148} cy={132} r={20} fill={GREEN} />
      <circle cx={184} cy={132} r={20} fill={GREEN} />
      <circle cx={166} cy={114} r={24} fill={GREEN} />
      <circle cx={166} cy={130} r={18} fill={GREEN} stroke="none" />
      <Face x={166} y={124} eyes="dot" mouth="smile" gap={18} blush={false} mw={14} />
      <circle cx={226} cy={168} r={17} fill="#6C7BD9" />
      <circle cx={250} cy={152} r={17} fill="#6C7BD9" />
      <Eyes x={250} y={150} k="dot" gap={12} />
      <path d="M302 118c0-10 4-14 10-16" stroke={LEAF} strokeWidth={4} />
      <path d="M276 174c-8-30 4-56 26-56s34 26 26 56c-4 14-48 14-52 0z" fill={SUN} />
      <Face x={302} y={146} eyes="happy" mouth="smile" gap={20} bw={19} br={5} mw={16} />
      <Spark x={130} y={68} />
      <Spark x={226} y={86} r={7} />
      <Spark x={334} y={72} r={8} />
    </>
  ),

  "fi-glycogen": () => (
    <>
      <Ground />
      <path d="M72 108h28M60 134h32M74 160h24" strokeWidth={2.5} />
      <path d="M162 186l-14 24h-12M196 186l12 24h12" strokeWidth={5} />
      <path d="M136 132c-14 6-20 18-18 30M224 132c14-6 22-16 22-30" strokeWidth={5} />
      <rect x={166} y={52} width={28} height={14} rx={3} fill={GREY} />
      <rect x={136} y={64} width={88} height={124} rx={14} fill={PAPER} />
      <rect x={148} y={152} width={64} height={24} rx={6} fill={GREEN} strokeWidth={2} />
      <rect x={148} y={122} width={64} height={24} rx={6} fill={MINT} strokeWidth={2} />
      <Face x={180} y={88} eyes="happy" mouth="smile" gap={26} mw={18} />
      <path d="M302 60l-20 34h16l-8 30 26-40h-16z" fill={GOLD} />
      <path d="M38 192h56c0 14-12 22-28 22s-28-8-28-22z" fill={SKY} />
      <path d="M58 188l30-24M68 190l28-20" strokeWidth={2.5} />
    </>
  ),

  "fi-belly-fat": (lang) => (
    <>
      <Ground />
      <path d="M128 200v12M168 200v12" strokeWidth={5} />
      <circle cx={148} cy={154} r={54} fill="#FFC9A0" />
      <circle cx={148} cy={76} r={30} fill={PAPER} />
      <Eyes x={148} y={74} k="wide" gap={24} lookY={4} />
      <Mouth x={148} y={88} k="o" />
      <path d="M124 136l12 5M172 136l-12 5" />
      <path d="M128 154q20 20 40 0z" fill={RED} />
      <circle cx={148} cy={186} r={3} fill={INK} stroke="none" />
      <Bubble x={226} y={84} w={116} h={60} tx={206} ty={160} />
      <Label lang={lang} x={284} y={123} s={24} zh="我饿！" en="Feed me!" es={20} />
      <circle cx={56} cy={188} r={20} fill="#C89B6A" />
      <g fill={COCOA} stroke="none">
        <circle cx={50} cy={182} r={3} />
        <circle cx={62} cy={192} r={3} />
        <circle cx={60} cy={178} r={2.5} />
        <circle cx={48} cy={196} r={2.5} />
      </g>
    </>
  ),

  "fi-carbs-five-words": (lang) => (
    <>
      <Ground />
      <path
        d="M48 170c-4-30 30-56 70-52 36 4 60 26 54 50-6 26-44 40-78 36-28-4-44-14-46-34z"
        fill="#C7708F"
      />
      <path d="M62 148l-6-4M152 134l8-6M98 124l-2-8" strokeWidth={2} />
      <Face x={110} y={156} eyes="happy" mouth="smile" gap={28} />
      <g transform="translate(0 20)">
        <path d="M236 190c-14-40-8-92 16-100 24 8 30 60 16 100z" fill={SUN} />
        <path d="M238 162h30M240 176h26" strokeWidth={1.5} />
        <path
          d="M228 192c-16-22-18-52-8-70 8 26 14 46 22 70zM276 192c16-22 18-52 8-70-8 26-14 46-22 70z"
          fill={MINT}
        />
        <Face x={252} y={126} eyes="dot" mouth="smile" gap={14} blush={false} mw={12} />
      </g>
      <Disc x={318} y={76} r={26} />
      <Label lang={lang} x={318} y={85} s={26} zh="慢" en="slow" es={18} ey={82} />
    </>
  ),

  "fi-gut-serotonin": () => (
    <>
      <path
        d="M52 110l-10-4M52 140l-10 4M116 110l10-4M116 140l10 4M152 100l-10-4M216 100l10-4M152 130l-10 4M216 130l10 4M252 110l-10-4M316 110l10-4M316 140l10 4M252 140l-10 4"
        strokeWidth={2.5}
      />
      <rect x={52} y={84} width={64} height={96} rx={32} fill={MINT} />
      <Face x={84} y={118} eyes="happy" mouth="grin" gap={22} bw={22} br={5} mw={18} />
      <rect x={152} y={68} width={64} height={112} rx={32} fill={SKY} />
      <Face x={184} y={106} eyes="happy" mouth="grin" gap={22} bw={22} br={5} mw={18} />
      <rect x={252} y={84} width={64} height={96} rx={32} fill="#FFC94A" />
      <Face x={284} y={118} eyes="happy" mouth="grin" gap={22} bw={22} br={5} mw={18} />
      <path d="M30 186h308" />
      <path d="M58 186v28M310 186v28" strokeWidth={5} />
      <g fill={PAPER} strokeWidth={2.5}>
        <path d="M68 170h32c0 10-7 16-16 16s-16-6-16-16z" />
        <path d="M168 170h32c0 10-7 16-16 16s-16-6-16-16z" />
        <path d="M268 170h32c0 10-7 16-16 16s-16-6-16-16z" />
      </g>
      <g fill={COCOA} stroke="none">
        <circle cx={78} cy={166} r={3.5} />
        <circle cx={88} cy={164} r={3.5} />
        <circle cx={178} cy={166} r={3.5} />
        <circle cx={190} cy={164} r={3.5} />
        <circle cx={278} cy={166} r={3.5} />
        <circle cx={290} cy={164} r={3.5} />
      </g>
      <Heart x={134} y={56} s={0.4} />
      <Spark x={234} y={50} r={7} />
      <Spark x={338} y={64} r={6} />
    </>
  ),

  "fi-fries-story": (lang) => (
    <>
      <Ground />
      <Apple dx={-10} />
      <Tick x={170} y={84} />
      <path
        d="M226 128V84h12v44zM244 128V70h12v58zM262 128V80h12v48zM280 128V92h12v36z"
        fill={SUN}
        strokeWidth={2.5}
      />
      <path d="M214 124h90l-10 88h-70z" fill={RED} />
      <Eyes x={259} y={158} k="dot" gap={22} />
      <path d="M251 172q8 8 16 0" />
      <path d="M322 150c-4 8-5 13 0 15 5-2 4-7 0-15z" fill={GOLD} strokeWidth={2} />
      <path d="M336 176c-4 8-5 13 0 15 5-2 4-7 0-15z" fill={GOLD} strokeWidth={2} />
      <Bubble x={258} y={28} w={94} h={46} tx={296} ty={92} />
      <Num x={292} y={60} s={24}>
        15g
      </Num>
      <Label lang={lang} x={330} y={59} s={17} zh="油" en="oil" es={17} />
    </>
  ),

  "fi-obesity-disease": (lang) => (
    <>
      <Ground />
      <Buddy x={136} y={134} r={62} fill={CREAM} eyes="happy" mouth="smile" fy={-30} />
      <path d="M76 152q60 22 120 0v16q-60 22-120 0z" fill={SUN} />
      <path d="M96 162v8M116 167v8M136 169v8M156 167v8M176 162v8" strokeWidth={2} />
      <path d="M196 152l22-8v16l-22 8z" fill={PAPER} />
      <Label lang={lang} x={252} y={96} s={19} a="start" zh="男" en="M" es={19} />
      <Num x={280} y={98} s={38} a="start">
        90
      </Num>
      <Label lang={lang} x={252} y={142} s={19} a="start" zh="女" en="F" es={19} />
      <Num x={280} y={144} s={38} a="start">
        85
      </Num>
      <Label lang={lang} x={296} y={172} s={13} zh="厘米以下" en="cm or under" es={12} />
    </>
  ),

  "fi-water-nutrient": () => (
    <>
      <Ground />
      <path
        d="M300 34v8M300 98v8M264 70h8M328 70h8M275 45l6 6M319 89l6 6M325 45l-6 6M281 89l-6 6"
        stroke={GOLD}
        strokeWidth={4}
      />
      <circle cx={300} cy={70} r={22} fill={SUN} />
      <path d="M210 96c28 0 28 62 0 62" strokeWidth={6} />
      <rect x={150} y={40} width={44} height={18} rx={5} fill={BLUE} />
      <path
        d="M134 74c0-10 8-16 18-16h40c10 0 18 6 18 16v112c0 12-8 20-20 20h-36c-12 0-20-8-20-20z"
        fill={PAPER}
      />
      <path
        d="M136 104q18-8 36 0t36 0v82c0 10-8 18-18 18h-36c-10 0-18-8-18-18z"
        fill={SKY}
        stroke="none"
      />
      <path d="M136 104q18-8 36 0t36 0" stroke={BLUE} strokeWidth={2.5} />
      <path d="M196 86h10M196 124h10M196 162h10" strokeWidth={2} />
      <Face x={170} y={140} eyes="happy" mouth="smile" gap={24} mw={18} />
      <path d="M46 160h42l-6 52H52z" fill={SKY} />
      <Spark x={96} y={104} r={7} />
    </>
  ),

  "fi-dietary-fibre": () => (
    <>
      <Ground />
      <path
        d="M94 86c-22-8-30-26-26-38 16 2 28 16 26 38zM94 86c20-10 34-6 40 6-12 10-30 8-40-6zM94 86c-2-20 6-34 18-38 8 14 0 30-18 38z"
        fill={GREEN}
      />
      <rect x={76} y={84} width={36} height={128} rx={12} fill={MINT} />
      <path d="M86 150v52M102 150v52" strokeWidth={1.5} />
      <Eyes x={94} y={112} k="dot" gap={14} />
      <Mouth x={94} y={122} k="o" />
      <path d="M130 124c20-20 40-22 58-10" strokeDasharray="3 8" />
      <path d="M178 104l12 10-14 6" />
      <path d="M176 152c10-28 100-28 110 0z" fill="#E9D3A8" />
      <g fill={COCOA} stroke="none">
        <circle cx={206} cy={142} r={2.5} />
        <circle cx={230} cy={136} r={2.5} />
        <circle cx={254} cy={142} r={2.5} />
      </g>
      <path d="M166 150h130c0 36-24 58-65 58s-65-22-65-58z" fill={PAPER} />
      <Face x={231} y={170} eyes="happy" mouth="smile" gap={26} mw={18} />
      <path
        d="M318 86c14-2 22 10 18 24-4 12-18 18-26 10 8-6 8-14 2-20-4-6 0-12 6-14z"
        fill="#C0563B"
      />
      <Spark x={292} y={62} r={7} />
    </>
  ),

  "fi-appetite-dial": (lang) => (
    <>
      <Ground />
      <path d="M98 194h64l10 20H88z" fill={GREY} />
      <circle cx={130} cy={134} r={62} fill={PAPER} />
      <circle cx={130} cy={134} r={44} fill="#FFF3D1" strokeWidth={2.5} />
      <path d="M130 76v10M102 95l-5-8M158 95l5-8M85 118l-9-4M175 118l9-4" strokeWidth={2.5} />
      <path d="M130 134L96 122" stroke={RED} strokeWidth={5} />
      <circle cx={130} cy={134} r={5} fill={INK} stroke="none" />
      <Face x={130} y={150} eyes="happy" mouth="smile" gap={24} bw={22} br={5} mw={16} />
      <Num x={56} y={98} s={30}>
        −
      </Num>
      <Num x={204} y={98} s={30}>
        +
      </Num>
      <path d="M258 146c-14-4-18-18-12-30M318 146c14-4 18-18 12-30" strokeWidth={5} />
      <circle cx={246} cy={112} r={8} fill={PAPER} />
      <circle cx={330} cy={112} r={8} fill={PAPER} />
      <path d="M278 176v16M298 176v16" strokeWidth={5} />
      <ellipse cx={288} cy={140} rx={32} ry={40} fill={PAPER} />
      <Face x={288} y={134} eyes="happy" mouth="grin" gap={20} bw={21} br={5} mw={18} />
      <Label lang={lang} x={288} y={84} s={15} zh="蛋白质" en="protein" es={15} />
    </>
  ),

  "fi-snack-portions": (lang) => (
    <>
      <Ground />
      <path
        d="M50 66l12-10 12 10 12-10 12 10 12-10 12 10 12-10 12 10v138a8 8 0 0 1-8 8H58a8 8 0 0 1-8-8z"
        fill={CORAL}
      />
      <path d="M50 162h96v30H50z" fill={PAPER} strokeWidth={2.5} />
      <Label lang={lang} x={98} y={183} s={16} zh="大包装" en="BIG PACK" es={12} ey={182} />
      <Eyes x={98} y={120} k="grumpy" gap={28} />
      <Mouth x={98} y={132} k="frown" w={24} />
      <Cross x={152} y={58} />
      <path
        d="M232 138l8-8 8 8 8-8 8 8 8-8 8 8 8-8 8 8v68a6 6 0 0 1-6 6h-52a6 6 0 0 1-6-6z"
        fill="#FFC94A"
      />
      <Face x={264} y={164} eyes="happy" mouth="smile" gap={26} bw={21} br={5} mw={22} />
      <Bubble x={204} y={50} w={132} h={50} tx={262} ty={122} />
      <Label lang={lang} x={246} y={84} s={18} zh="第一口" en="1st bite" es={14} />
      <Num x={304} y={85} s={26} fill="#B4530A">
        80%
      </Num>
      <Tick x={320} y={150} />
      <Spark x={190} y={160} />
    </>
  ),

  /* 运动 */
  "fi-bdnf": (lang) => (
    <>
      <Ground />
      <path d="M140 176l-18 32h-12M176 176l16 32h14" strokeWidth={5} />
      <path d="M156 72V44" stroke={LEAF} strokeWidth={4} />
      <path
        d="M156 50c-16-4-22-16-20-24 12 0 22 8 20 24zM156 46c14-6 24-2 28 8-10 6-22 4-28-8z"
        fill={MINT}
      />
      <path
        d="M100 150c-24-6-28-40-6-52 0-28 34-40 54-24 22-18 60-4 58 26 22 10 18 46-8 50-10 22-40 26-56 12-16 8-36 4-42-12z"
        fill="#FFB7C5"
      />
      <path
        d="M152 72c-8 14 8 22-2 38M120 84c10 0 14 10 6 16M102 112c12-6 22 0 22 10M186 80c-10 2-12 12-4 16M202 108c-12-6-22 2-20 12"
        strokeWidth={2.5}
      />
      <Face x={152} y={138} eyes="happy" mouth="grin" gap={30} />
      <Disc x={300} y={84} r={32} />
      <Num x={300} y={91} s={19}>
        BDNF
      </Num>
      <Label lang={lang} x={300} y={140} s={14} zh="大脑的肥料" en="brain fertiliser" es={12} />
      <Spark x={254} y={44} r={7} />
    </>
  ),

  "fi-muscle-fibres": (lang) => (
    <>
      <Ground />
      <path d="M168 190l-18 12h-16M200 190l18 12h16" strokeWidth={5} />
      <path d="M146 122c-30-2-40-28-30-52M222 122c30-2 40-28 30-52" strokeWidth={5} />
      <circle cx={114} cy={64} r={11} fill={PAPER} />
      <circle cx={254} cy={64} r={11} fill={PAPER} />
      <path d="M170 60h28v14h-28z" fill={PAPER} />
      <path d="M166 42h36a4 4 0 0 1 4 4v14h-44V46a4 4 0 0 1 4-4z" fill={BLUE} />
      <path
        d="M170 74c-16 6-24 14-24 30v68a20 20 0 0 0 20 20h36a20 20 0 0 0 20-20v-68c0-16-8-24-24-30z"
        fill={PAPER}
      />
      <path d="M148 112h72v60a18 18 0 0 1-18 18h-36a18 18 0 0 1-18-18z" fill={SKY} stroke="none" />
      <path d="M148 110q18-10 36 0t36 0" stroke={BLUE} strokeWidth={2.5} />
      <path d="M162 124l12 3M206 124l-12 3" />
      <Face x={184} y={136} eyes="dot" mouth="grin" gap={28} bw={26} br={6} mw={26} />
      <path d="M238 92c-5 8-6 14 0 16 6-2 5-8 0-16z" fill={SKY} strokeWidth={2} />
      <path d="M92 44l8 8M86 60H74M100 36V26M276 44l-8 8M282 60h12M268 36V26" strokeWidth={2.5} />
      <Disc x={56} y={150} r={32} />
      <Num x={56} y={150} s={26}>
        ×10
      </Num>
      <Label lang={lang} x={56} y={168} s={14} zh="深蹲" en="squats" es={12} />
      <Disc x={312} y={150} r={32} />
      <Num x={312} y={150} s={26}>
        ×10
      </Num>
      <Label lang={lang} x={312} y={168} s={14} zh="弯举" en="curls" es={12} />
    </>
  ),

  "fi-bone-density": () => (
    <>
      <Ground />
      <path d="M152 122c-20-10-28-28-26-50M208 122c20-10 28-28 26-50" strokeWidth={5} />
      <path d="M100 70h160" strokeWidth={6} />
      <rect x={84} y={46} width={18} height={48} rx={5} fill={SLATE} />
      <rect x={258} y={46} width={18} height={48} rx={5} fill={SLATE} />
      <path
        d="M160 96c-14-14-34 4-18 18 4 4 8 4 10 8v56c-2 4-6 4-10 8-16 14 4 32 18 18 6-6 14-6 20-6s14 0 20 6c14 14 34-4 18-18-4-4-8-4-10-8v-56c2-4 6-4 10-8 16-14-4-32-18-18-6 6-14 6-20 6s-14 0-20-6z"
        fill={PAPER}
      />
      <Face x={180} y={136} eyes="happy" mouth="grin" gap={22} bw={20} br={5} mw={18} />
      <path d="M290 132c-16 8-30 10-46 8" strokeDasharray="3 8" />
      <Disc x={312} y={120} r={22} />
      <Num x={312} y={127} s={20}>
        Ca
      </Num>
      <Disc x={332} y={166} r={13} />
      <Spark x={318} y={66} r={7} />
    </>
  ),

  "fi-fitness-word": (lang) => (
    <>
      <path d="M150 48L226 103 197 193H103L74 103z" fill={PAPER} />
      <path
        d="M150 88l38 28-14.500 44.500h-47L112 116zM150 128V48M150 128l76-25M150 128l47 65M150 128l-47 65M150 128l-76-25"
        strokeWidth={1.5}
      />
      <path d="M150 56L211 108 164 147 117 173 85 107z" fill={GOLD} fillOpacity={0.85} />
      <circle cx={164} cy={147} r={7} fill={RED} strokeWidth={2.5} />
      <Label lang={lang} x={166} y={50} s={14} a="start" zh="力量" en="strength" es={12} />
      <Label lang={lang} x={234} y={96} s={14} a="start" zh="耐力" en="endurance" es={12} />
      <Label lang={lang} x={206} y={212} s={14} zh="柔韧" en="flexibility" es={12} />
      <Label lang={lang} x={94} y={212} s={14} zh="灵活" en="mobility" es={12} />
      <Label lang={lang} x={66} y={96} s={14} a="end" zh="爆发" en="power" es={12} />
      <path d="M272 152c-28 10-56 10-90 0" strokeDasharray="3 8" />
      <path d="M194 146l-13 5 9 10" />
      <Buddy x={308} y={152} r={32} fill={SAGE} eyes="wide" look={-3} mouth="o" />
    </>
  ),

  "fi-soreness": () => (
    <>
      <Ground />
      <path d="M178 132c16-10 22-26 18-44" strokeWidth={5} />
      <path d="M176 80h44" strokeWidth={5} />
      <rect x={164} y={66} width={14} height={28} rx={4} fill={BLUE} />
      <rect x={218} y={66} width={14} height={28} rx={4} fill={BLUE} />
      <path d="M96 140c-16-4-24-16-22-30" strokeWidth={5} />
      <circle cx={74} cy={106} r={8} fill={PAPER} />
      <Buddy x={136} y={152} r={46} fill={SAGE} eyes="happy" mouth="grin" />
      <path d="M274 52v12M322 52v12" strokeWidth={4} />
      <rect x={252} y={58} width={92} height={90} rx={8} fill={PAPER} />
      <path d="M252 82h92V66a8 8 0 0 0-8-8h-76a8 8 0 0 0-8 8z" fill={RED} />
      <path
        d="M266 104l5 6 9-11M292 104l5 6 9-11M318 104l5 6 9-11M266 128l5 6 9-11"
        stroke={LEAF}
        strokeWidth={3.5}
      />
      <circle cx={299} cy={128} r={8} strokeWidth={2.5} strokeDasharray="2 5" />
    </>
  ),

  /* 情绪 */
  "fi-cognitive-defusion": (lang) => (
    <>
      <Ground />
      <path d="M136 152c10-4 16-10 20-18" strokeWidth={5} />
      <path d="M160 126c20-38 70 44 102 26" strokeWidth={2} />
      <circle cx={158} cy={130} r={8} fill={PAPER} />
      <Buddy x={96} y={158} r={44} eyes="happy" mouth="smile" />
      <path d="M254 142l8 12 8-12z" fill={STORM} />
      <ellipse cx={262} cy={84} rx={62} ry={60} fill={STORM} />
      <path d="M220 62c6-12 16-20 28-22" stroke={PAPER} strokeWidth={4} />
      <Label lang={lang} x={264} y={86} s={24} zh="完蛋了" en="I’m doomed" es={18} />
      <path d="M240 104l-4 10M264 104l-4 10M288 104l-4 10" stroke={BLUE} strokeWidth={2.5} />
      <rect x={176} y={160} width={70} height={26} rx={4} fill={SUN} />
      <Label lang={lang} x={211} y={178} s={14} zh="一个想法" en="a thought" es={12} ey={177} />
    </>
  ),

  "fi-dare-to-be-happy": (lang) => (
    <>
      <Ground />
      <path d="M98 204v10M142 204v10" strokeWidth={5} />
      <path d="M66 150c-18 4-26 16-24 30" strokeWidth={5} />
      <path d="M172 128c18-8 24-24 20-42" strokeWidth={5} />
      <circle cx={190} cy={80} r={11} fill={PAPER} />
      <circle cx={120} cy={148} r={58} fill={PAPER} />
      <circle cx={86} cy={160} r={9} fill={BLUSH} stroke="none" />
      <circle cx={154} cy={160} r={9} fill={BLUSH} stroke="none" />
      <path d="M94 140q9-12 18 0M128 140q9-12 18 0" strokeWidth={3.5} />
      <path d="M100 160q20 22 40 0z" fill={RED} />
      <path
        d="M120 186l4 9 10 1-8 7 3 10-9-6-9 6 3-10-8-7 10-1z"
        fill={GOLD}
        strokeWidth={2.5}
      />
      <Bubble x={212} y={36} w={138} h={84} tx={206} ty={140} />
      <Label lang={lang} x={281} y={72} s={24} zh="我做得" en="I did" es={22} />
      <Label lang={lang} x={281} y={102} s={24} zh="很好！" en="that well!" es={22} />
      <Spark x={52} y={62} r={11} />
      <Spark x={300} y={168} />
      <Spark x={250} y={184} r={6} />
    </>
  ),

  "fi-stress-switch-vision": (lang) => (
    <>
      <Ground />
      <path d="M92 214l76-116h32l76 116z" fill={CREAM} />
      <path d="M184 120v12M184 150v16M184 184v16" strokeWidth={4} />
      <circle cx={58} cy={118} r={22} fill={LEAF} />
      <path d="M58 140v34" strokeWidth={5} />
      <circle cx={310} cy={118} r={22} fill={LEAF} />
      <path d="M310 140v34" strokeWidth={5} />
      <Buddy x={184} y={168} r={34} eyes="wide" />
      <path d="M126 62h-34M100 52l-10 10 10 10" strokeWidth={4} />
      <path d="M242 62h34M268 52l10 10-10 10" strokeWidth={4} />
      <Label lang={lang} x={184} y={70} s={22} zh="往前走" en="walk on" es={18} />
    </>
  ),

  "fi-stress-switch-eyes": (lang) => (
    <>
      <Ground />
      <rect x={30} y={120} width={40} height={94} rx={3} fill={WOOD} />
      <circle cx={62} cy={168} r={3} fill={INK} stroke="none" />
      <rect x={296} y={110} width={46} height={46} rx={3} fill={SKY} />
      <path d="M319 110v46M296 133h46" strokeWidth={2} />
      <path d="M184 22v16" strokeWidth={3} />
      <path d="M158 60l26-20 26 20z" fill={SUN} />
      <circle cx={184} cy={150} r={56} fill={PAPER} />
      <circle cx={152} cy={162} r={9} fill={BLUSH} stroke="none" />
      <circle cx={216} cy={162} r={9} fill={BLUSH} stroke="none" />
      <path d="M150 132q12-10 24 0M194 132q12-10 24 0" strokeWidth={3} />
      <path d="M154 152q10 8 20 0M194 152q10 8 20 0" strokeWidth={3.5} />
      <path d="M170 178q14 10 28 0" strokeWidth={3.5} />
      <Label lang={lang} x={92} y={82} s={20} zh="松开眉头" en="soften the brow" es={14} />
    </>
  ),
};

/* A card whose own drawing has not been made yet borrows its pillar's. */
const FALLBACK: Record<PillarId, (lang: Lang) => ReactNode> = {
  sleep: () => (
    <>
      <Ground />
      <path d="M214 54a52 52 0 1 0 52 66a42 42 0 0 1-52-66z" fill={SUN} />
      <Zs x={118} y={110} />
      <Spark x={292} y={70} />
      <Spark x={96} y={160} r={7} />
    </>
  ),
  nutrition: () => (
    <>
      <Ground />
      <path d="M136 132c0-40 96-40 96 0z" fill={PAPER} />
      <path d="M120 130h128c0 40-24 60-64 60s-64-20-64-60z" fill={SUN} />
      <Face x={184} y={150} eyes="happy" mouth="smile" gap={26} />
      <path d="M150 190h68l8 24h-84z" fill={SUN} />
      <Spark x={86} y={90} />
      <Spark x={290} y={84} r={7} />
    </>
  ),
  exercise: () => (
    <>
      <Ground />
      <path d="M110 130h148" strokeWidth={8} />
      <rect x={84} y={92} width={30} height={76} rx={8} fill={BLUE} />
      <rect x={254} y={92} width={30} height={76} rx={8} fill={BLUE} />
      <Spark x={184} y={76} />
      <Spark x={184} y={184} r={7} />
    </>
  ),
  emotion: () => (
    <>
      <Ground />
      <Buddy x={184} y={150} r={50} eyes="happy" mouth="grin" />
      <Heart x={270} y={84} s={0.8} />
      <Spark x={96} y={86} />
    </>
  ),
  relationship: () => (
    <>
      <Ground />
      <Buddy x={128} y={150} r={46} fill={CREAM} eyes="wide" look={4} />
      <Buddy x={240} y={150} r={46} fill={PERI} eyes="wide" look={-4} />
      <Heart x={184} y={72} s={0.8} />
    </>
  ),
};

export function hasOwnArt(slug: string): boolean {
  return slug in SCENES;
}

export function CardArt({
  slug,
  pillar,
  label,
  lang = "zh",
}: {
  slug: string;
  pillar: PillarId;
  /** Short description for screen readers. */
  label: string;
  /** Language of the lettering inside the drawing. */
  lang?: Lang;
}) {
  const scene = SCENES[slug] ?? FALLBACK[pillar];
  return (
    <svg
      data-card-art={slug}
      viewBox="0 0 368 236"
      role="img"
      aria-label={label}
      fill="none"
      stroke={INK}
      strokeWidth={3}
      strokeLinecap="round"
      strokeLinejoin="round"
      style={{ display: "block", width: "100%", height: "auto" }}
    >
      {scene(lang)}
    </svg>
  );
}
