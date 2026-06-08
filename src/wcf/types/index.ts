export type TeamCategory = "worldcup" | "chaos";

export type Team = {
  id: string;
  name: string;
  code: string;
  flag: string;
  category: TeamCategory;
  primaryColor: string;
  secondaryColor: string;
  accentColor: string;
  specialMove: string;
  funnyTrait: string;
};

export type FighterState =
  | "idle"
  | "enter"
  | "taunt"
  | "dash"
  | "punch"
  | "kick"
  | "hit"
  | "fall"
  | "ko"
  | "victory";

export type BattlePhase =
  | "setup"
  | "entrance"
  | "vs"
  | "round1"
  | "round2"
  | "chaos"
  | "ko"
  | "result";

export type BattleResult = {
  winner: Team;
  loser: Team;
  victoryType: string;
  damageReport: string[];
  varDecision: string;
  oneLiner: string;
  hypeLevel: number;
};
