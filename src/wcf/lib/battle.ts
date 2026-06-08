import { BattleResult, Team } from "@wcf/types";

const victoryTypes = [
  "Emotional Damage",
  "Pure Vibes",
  "Last-Minute Chaos",
  "VAR Confusion",
  "Tactical Nonsense",
  "Main Character Energy",
  "Lucky Bounce",
  "Unnecessary Drama",
  "Collective Hallucination",
  "Timeline Corruption",
];

const varDecisions = [
  "VAR unavailable due to excessive drama.",
  "VAR checked it and decided not to get involved.",
  "VAR says the vibes were technically legal.",
  "VAR review delayed because everyone was laughing.",
  "Decision confirmed. Nobody understands why.",
  "VAR has left the stadium.",
];

const normalOneLiners = [
  "{winner} wins by doing absolutely enough.",
  "{loser} requests a rematch and emotional support.",
  "{winner} has successfully weaponised national pride.",
  "{loser} has entered the reflection phase.",
  "{winner} wins. The internet will now be unbearable.",
];

const chinaWinLines = [
  "Scientists have begun investigating a possible disturbance in reality.",
  "The entire internet has requested a recount.",
  "This result has been sent to the Ministry of Impossible Dreams.",
  "Every uncle in the group chat says he always believed.",
  "Reality has failed a basic integrity check.",
];

function pick<T>(items: T[]): T {
  return items[Math.floor(Math.random() * items.length)];
}

function randInt(min: number, max: number): number {
  return min + Math.floor(Math.random() * (max - min + 1));
}

function cap(text: string): string {
  return text.charAt(0).toUpperCase() + text.slice(1);
}

// Assembles a fresh, matchup-aware "damage report" every call. Lines are built
// from live numbers (scaled off the hype level) plus each team's trait/move,
// then ordered to escalate into an absurd punchline.
function buildDamageReport(
  winner: Team,
  loser: Team,
  hype: number
): string[] {
  const chaos = winner.category === "chaos" || loser.category === "chaos";
  const integrity = Math.max(1, 100 - hype);

  // Header fuses the on-card meters into one opening punch.
  const header = `Total damage: ${hype}% emotional · ${winner.name} now 100% insufferable`;

  // Guaranteed matchup-specific lines so the report names THESE two teams.
  const loserLine = `${cap(loser.funnyTrait)} ${pick([
    "down",
    "leaked",
    "evaporated by",
    "off by",
  ])} ${randInt(40, 95)}% since kickoff`;

  const winnerLine = `${winner.specialMove} deployed ${randInt(2, 6)}× · ${pick([
    "0 explanations given",
    "still no replay angle",
    "refs just clapped",
    "physics declined to comment",
  ])}`;

  // A random stat-sheet filler with live numbers.
  const filler = pick([
    `${loser.name}'s defense ${pick([
      "filed for emotional leave",
      "left the match on read",
      "requested a recount",
      "quietly logged off",
    ])}`,
    `crowd noise peaked at ${randInt(2, 9)} collective gasps`,
    `tactical plan survived a record ${randInt(1, 4)} ${pick([
      "minutes",
      "corner kicks",
      "deep breaths",
    ])}`,
    `group chat hit ${randInt(40, 999)} unread · all in caps`,
    `possession: ${randInt(31, 71)}% — generously rounded up`,
    `${loser.specialMove} recalled for safety reasons`,
  ]);

  // Punchline: signature team > chaos > normal, the most absurd of the bunch.
  let punchline: string;
  if (winner.id === "china") {
    punchline = `Reality integrity holding at ${integrity}% · Ministry of Impossible Dreams notified`;
  } else if (winner.id === "var-united") {
    punchline = "VAR reviewed itself, found nothing, awarded a goal anyway";
  } else if (winner.id === "ai-fc") {
    punchline = `Match resolved in 0.${randInt(1, 9)}s · humans still confused`;
  } else if (chaos) {
    punchline = pick([
      "reality.exe stopped responding",
      `${randInt(2, 3)} laws of physics quietly resigned`,
      "timeline rolled back to a save point",
      "the simulation logged a warning and moved on",
    ]);
  } else {
    punchline = pick([
      `${winner.name} pride overload · neighbors formally notified`,
      `reality integrity holding at ${integrity}%`,
      `${loser.name} entered the reflection phase ${randInt(2, 9)} minutes early`,
    ]);
  }

  return [header, loserLine, winnerLine, filler, punchline];
}

function fillTemplate(text: string, winner: Team, loser: Team): string {
  return text
    .replaceAll("{winner}", winner.name)
    .replaceAll("{loser}", loser.name)
    .replaceAll("{winnerTrait}", winner.funnyTrait)
    .replaceAll("{loserTrait}", loser.funnyTrait)
    .replaceAll("{winnerMove}", winner.specialMove)
    .replaceAll("{loserMove}", loser.specialMove);
}

// "Hype Level": how electric this match felt. Every win starts genuinely
// exciting (base 45), and the more improbable the winner the more the crowd
// loses it — chaos teams and signature longshots push it toward the roof.
function calculateHype(winner: Team, loser: Team): number {
  let hype = 45;

  if (winner.category === "chaos" || loser.category === "chaos") {
    hype += 35;
  }

  if (winner.id === "china") {
    hype += 40;
  }

  if (winner.id === "var-united") {
    hype += 25;
  }

  if (winner.id === "ai-fc") {
    hype += 20;
  }

  return Math.min(99, hype + Math.floor(Math.random() * 10));
}

// One-word read on the meter so the number lands at a glance.
export function hypeTier(level: number): string {
  if (level >= 90) return "Off the Charts";
  if (level >= 80) return "Unreal";
  if (level >= 65) return "Electric";
  if (level >= 50) return "Buzzing";
  return "Warm";
}

export function generateBattleResult(teamA: Team, teamB: Team): BattleResult {
  const winner = Math.random() > 0.5 ? teamA : teamB;
  const loser = winner.id === teamA.id ? teamB : teamA;

  const hypeLevel = calculateHype(winner, loser);

  const oneLiner =
    winner.id === "china"
      ? pick(chinaWinLines)
      : fillTemplate(pick(normalOneLiners), winner, loser);

  return {
    winner,
    loser,
    victoryType:
      winner.category === "chaos"
        ? pick(["Timeline Corruption", "Collective Hallucination", "Pure Vibes"])
        : pick(victoryTypes),
    damageReport: buildDamageReport(winner, loser, hypeLevel),
    varDecision: pick(varDecisions),
    oneLiner,
    hypeLevel,
  };
}
