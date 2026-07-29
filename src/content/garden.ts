/*
 * Digital Garden — numbered ideas, tended over years. Never finished.
 * Numbers come from Hao's private idea log; only the tended ones surface here.
 */
export type Idea = {
  no: number;
  lines: string[];
  planted: string;
  status: "seedling" | "growing" | "evergreen";
};

export const IDEAS: Idea[] = [
  {
    no: 171,
    lines: ["Specifications become more valuable than implementations."],
    planted: "2026",
    status: "growing",
  },
  {
    no: 154,
    lines: ["Managers won't disappear.", "They'll manage AI."],
    planted: "2026",
    status: "growing",
  },
  {
    no: 138,
    lines: ["Books are software.", "Readers compile them."],
    planted: "2026",
    status: "growing",
  },
];
