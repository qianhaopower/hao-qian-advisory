"use client";

import { Volume2, VolumeX } from "lucide-react";

type SoundToggleProps = {
  enabled: boolean;
  onToggle: () => void;
};

export default function SoundToggle({ enabled, onToggle }: SoundToggleProps) {
  return (
    <button
      type="button"
      onClick={onToggle}
      aria-pressed={enabled}
      aria-label={enabled ? "Turn sound off" : "Turn sound on"}
      title={enabled ? "Sound is on" : "Sound is off"}
      className="flex items-center gap-2 rounded-full border border-white/15 bg-white/5 px-3 py-1.5 text-xs font-bold text-white/80 backdrop-blur transition hover:bg-white/10 active:scale-95"
    >
      {enabled ? (
        <Volume2 className="h-4 w-4 text-emerald-400" />
      ) : (
        <VolumeX className="h-4 w-4 text-white/50" />
      )}
      <span>{enabled ? "Sound On" : "Sound Off"}</span>
    </button>
  );
}
