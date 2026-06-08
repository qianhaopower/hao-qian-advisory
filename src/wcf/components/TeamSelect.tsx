"use client";

import { Team } from "@wcf/types";
import { worldCupTeams, chaosTeams, getTeamById } from "@wcf/lib/teams";

type TeamSelectProps = {
  label: string;
  value: Team;
  onChange: (team: Team) => void;
  accentColor: string;
  disabled?: boolean;
};

export default function TeamSelect({
  label,
  value,
  onChange,
  accentColor,
  disabled,
}: TeamSelectProps) {
  return (
    <label className="flex w-full flex-col gap-2">
      <span className="text-xs font-bold uppercase tracking-widest text-white/60">
        {label}
      </span>
      <div
        className="relative rounded-2xl border border-white/15 bg-white/5 p-[2px] shadow-lg transition-colors focus-within:border-white/40"
        style={{ boxShadow: `0 0 24px ${accentColor}33` }}
      >
        <select
          aria-label={label}
          disabled={disabled}
          value={value.id}
          onChange={(e) => {
            const team = getTeamById(e.target.value);
            if (team) onChange(team);
          }}
          className="w-full cursor-pointer appearance-none rounded-2xl bg-transparent px-4 py-3 text-base font-semibold text-white outline-none disabled:cursor-not-allowed disabled:opacity-60 sm:text-lg"
        >
          <optgroup label="World Cup Teams" className="bg-[#0b1020] text-white">
            {worldCupTeams.map((team) => (
              <option key={team.id} value={team.id} className="bg-[#0b1020]">
                {team.flag} {team.name}
              </option>
            ))}
          </optgroup>
          <optgroup label="Chaos Teams" className="bg-[#0b1020] text-white">
            {chaosTeams.map((team) => (
              <option key={team.id} value={team.id} className="bg-[#0b1020]">
                {team.flag} {team.name}
              </option>
            ))}
          </optgroup>
        </select>

        {/* chevron */}
        <span className="pointer-events-none absolute right-4 top-1/2 -translate-y-1/2 text-white/50">
          ▼
        </span>
      </div>
    </label>
  );
}
