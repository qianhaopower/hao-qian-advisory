import { BattleResult } from "@wcf/types";

export function resultToText(result: BattleResult): string {
  return `
World Cup Fight Simulator

${result.winner.name} ${result.winner.flag} vs ${result.loser.name} ${result.loser.flag}

Winner: ${result.winner.name} ${result.winner.flag}
Victory Type: ${result.victoryType}
Hype Level: ${result.hypeLevel}%

Damage Report:
${result.damageReport.map((item) => `- ${item}`).join("\n")}

VAR Decision:
${result.varDecision}

${result.oneLiner}

Scientifically inaccurate. Emotionally correct.
For entertainment only. Not a prediction.
  `.trim();
}

export async function copyText(text: string): Promise<boolean> {
  try {
    if (navigator?.clipboard?.writeText) {
      await navigator.clipboard.writeText(text);
      return true;
    }
  } catch {
    // fall through to legacy fallback
  }

  // Fallback for browsers / contexts without the async clipboard API.
  try {
    const textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.style.position = "fixed";
    textarea.style.opacity = "0";
    document.body.appendChild(textarea);
    textarea.select();
    const ok = document.execCommand("copy");
    document.body.removeChild(textarea);
    return ok;
  } catch {
    return false;
  }
}
