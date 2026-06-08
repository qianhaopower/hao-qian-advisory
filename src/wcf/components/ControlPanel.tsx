"use client";

import { Shuffle, Swords } from "lucide-react";
import { Team } from "@wcf/types";
import TeamSelect from "./TeamSelect";
import SoundToggle from "./SoundToggle";

type ControlPanelProps = {
  teamA: Team;
  teamB: Team;
  onTeamAChange: (team: Team) => void;
  onTeamBChange: (team: Team) => void;
  onFight: () => void;
  onRandomMatchup: () => void;
  disabled: boolean;
  soundEnabled: boolean;
  onToggleSound: () => void;
};

export default function ControlPanel({
  teamA,
  teamB,
  onTeamAChange,
  onTeamBChange,
  onFight,
  onRandomMatchup,
  disabled,
  soundEnabled,
  onToggleSound,
}: ControlPanelProps) {
  return (
    <div className="mx-auto w-full max-w-3xl rounded-3xl border border-white/10 bg-white/5 p-5 shadow-xl backdrop-blur sm:p-6">
      <div className="mb-4 flex items-center justify-between gap-3">
        <span className="text-xs font-bold uppercase tracking-[0.25em] text-white/40">
          Choose your fighters
        </span>
        <SoundToggle enabled={soundEnabled} onToggle={onToggleSound} />
      </div>

      <div className="grid grid-cols-1 items-end gap-4 sm:grid-cols-[1fr_auto_1fr]">
        <TeamSelect
          label="Fighter A"
          value={teamA}
          onChange={onTeamAChange}
          accentColor={teamA.primaryColor}
          disabled={disabled}
        />

        <div className="hidden pb-3 text-center text-2xl font-black italic text-white/40 sm:block">
          vs
        </div>

        <TeamSelect
          label="Fighter B"
          value={teamB}
          onChange={onTeamBChange}
          accentColor={teamB.primaryColor}
          disabled={disabled}
        />
      </div>

      <div className="mt-5 flex flex-col gap-3 sm:flex-row">
        <button
          type="button"
          onClick={onRandomMatchup}
          disabled={disabled}
          className="flex items-center justify-center gap-2 rounded-2xl border border-white/15 bg-white/5 px-5 py-3 font-bold text-white/80 transition hover:bg-white/10 active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-50 sm:w-auto"
        >
          <Shuffle className="h-5 w-5" />
          Random Chaos
        </button>

        <button
          type="button"
          onClick={onFight}
          disabled={disabled}
          className="group relative flex flex-1 items-center justify-center gap-2 overflow-hidden rounded-2xl bg-gradient-to-r from-fuchsia-600 via-rose-500 to-amber-500 px-6 py-3.5 text-lg font-black uppercase tracking-wider text-white shadow-[0_0_30px_rgba(244,63,94,0.5)] transition active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-60"
        >
          <span className="absolute inset-0 -translate-x-full bg-white/20 transition-transform duration-700 group-hover:translate-x-full" />
          <Swords className="h-6 w-6" />
          {disabled ? "Fighting..." : "Fight!"}
        </button>
      </div>
    </div>
  );
}
