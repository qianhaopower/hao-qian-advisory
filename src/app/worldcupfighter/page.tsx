"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { BattlePhase, BattleResult, FighterState, Team } from "@wcf/types";
import { teams, getTeamById } from "@wcf/lib/teams";
import { generateBattleResult } from "@wcf/lib/battle";
import { audioManager } from "@wcf/lib/proceduralAudio";
import { trackEvent } from "@wcf/lib/track";
import BackgroundEffects from "@wcf/components/BackgroundEffects";
import ControlPanel from "@wcf/components/ControlPanel";
import Arena from "@wcf/components/Arena";
import ResultCard from "@wcf/components/ResultCard";

const DEFAULT_A = getTeamById("brazil") ?? teams[0];
const DEFAULT_B = getTeamById("china") ?? teams[1];

function randomTeam(exclude?: string): Team {
  const pool = exclude ? teams.filter((t) => t.id !== exclude) : teams;
  return pool[Math.floor(Math.random() * pool.length)];
}

export default function Home() {
  const [teamA, setTeamA] = useState<Team>(DEFAULT_A);
  const [teamB, setTeamB] = useState<Team>(DEFAULT_B);
  const [phase, setPhase] = useState<BattlePhase>("setup");
  const [leftState, setLeftState] = useState<FighterState>("idle");
  const [rightState, setRightState] = useState<FighterState>("idle");
  const [result, setResult] = useState<BattleResult | null>(null);
  const [isFighting, setIsFighting] = useState(false);
  const [soundEnabled, setSoundEnabled] = useState(false);

  const timers = useRef<ReturnType<typeof setTimeout>[]>([]);

  const clearTimers = useCallback(() => {
    timers.current.forEach(clearTimeout);
    timers.current = [];
  }, []);

  useEffect(() => clearTimers, [clearTimers]);

  // Anonymous page view, once per load.
  useEffect(() => {
    trackEvent("page_view");
  }, []);

  // Restore the saved sound preference. This only flips the flag — it never
  // creates an AudioContext (that requires a user gesture), so the page stays
  // silent on load even for returning visitors with sound on.
  useEffect(() => {
    try {
      if (localStorage.getItem("soundEnabled") === "true") {
        // Hydration-safe restore: localStorage can't be read during SSR/first
        // render, so syncing from it must happen here, after mount.
        // eslint-disable-next-line react-hooks/set-state-in-effect
        setSoundEnabled(true);
        audioManager.setEnabled(true);
      }
    } catch {
      // localStorage unavailable — stay off.
    }
    return () => audioManager.stopMusic();
  }, []);

  // Pre-select the matchup from a shared ?a=&b= link (both must be valid and
  // distinct). Runs once on mount; malformed params are ignored.
  useEffect(() => {
    try {
      const params = new URLSearchParams(window.location.search);
      const ta = getTeamById(params.get("a") ?? "");
      const tb = getTeamById(params.get("b") ?? "");
      if (ta && tb && ta.id !== tb.id) {
        // Hydration-safe: query params can't be read during SSR, so syncing
        // the matchup must happen here, after mount.
        // eslint-disable-next-line react-hooks/set-state-in-effect
        setTeamA(ta);
        setTeamB(tb);
      }
    } catch {
      // ignore malformed params
    }
  }, []);

  const handleToggleSound = useCallback(() => {
    const next = !soundEnabled;
    setSoundEnabled(next);
    if (next) {
      // Unlock audio inside this user gesture, then confirm with a click.
      audioManager.init();
      audioManager.setEnabled(true);
      audioManager.playClick();
      trackEvent("sound_enabled");
    } else {
      audioManager.setEnabled(false);
      audioManager.stopMusic();
    }
    try {
      localStorage.setItem("soundEnabled", String(next));
    } catch {
      // ignore persistence failures
    }
  }, [soundEnabled]);

  const schedule = useCallback((fn: () => void, ms: number) => {
    timers.current.push(setTimeout(fn, ms));
  }, []);

  // Prevent identical fighters: auto-switch the opposite side.
  const handleTeamAChange = useCallback(
    (team: Team) => {
      setTeamA(team);
      if (team.id === teamB.id) setTeamB(randomTeam(team.id));
    },
    [teamB.id]
  );

  const handleTeamBChange = useCallback(
    (team: Team) => {
      setTeamB(team);
      if (team.id === teamA.id) setTeamA(randomTeam(team.id));
    },
    [teamA.id]
  );

  const handleRandomMatchup = useCallback(() => {
    audioManager.playClick();
    const a = randomTeam();
    setTeamA(a);
    setTeamB(randomTeam(a.id));
  }, []);

  const startFight = useCallback(() => {
    clearTimers();
    setIsFighting(true);
    setResult(null);

    const battleResult = generateBattleResult(teamA, teamB);
    const leftWon = battleResult.winner.id === teamA.id;

    trackEvent("fight_started", { teamA: teamA.id, teamB: teamB.id });

    // Fight click is a valid gesture — unlock + start audio (no-ops if muted).
    audioManager.playFightStart();
    audioManager.startMusic();

    // 0ms — dramatic entrance: both teams slide in, names announced
    setPhase("entrance");
    setLeftState("enter");
    setRightState("enter");

    // 2000ms — VS zoom-in moment, fighters size each other up
    schedule(() => {
      setPhase("vs");
      setLeftState("taunt");
      setRightState("taunt");
    }, 2000);

    // 3000ms — round 1: A punches, B reels
    schedule(() => {
      setPhase("round1");
      setLeftState("punch");
      setRightState("hit");
      audioManager.playPunch();
      audioManager.playHit();
    }, 3000);

    // 4200ms — round 2: B kicks, A reels
    schedule(() => {
      setPhase("round2");
      setLeftState("hit");
      setRightState("kick");
      audioManager.playKick();
      audioManager.playHit();
    }, 4200);

    // 5400ms — chaos: both dash, camera zooms and shakes
    schedule(() => {
      setPhase("chaos");
      setLeftState("dash");
      setRightState("dash");
      audioManager.playChaos();
    }, 5400);

    // 7200ms — final hit / KO: winner celebrates, loser falls (slow-mo beat)
    schedule(() => {
      setPhase("ko");
      setLeftState(leftWon ? "victory" : "fall");
      setRightState(leftWon ? "fall" : "victory");
      audioManager.playKO();
    }, 7200);

    // 8600ms — winner revealed: stop the music, play the jingle
    schedule(() => {
      setLeftState(leftWon ? "victory" : "ko");
      setRightState(leftWon ? "ko" : "victory");
      setResult(battleResult);
      setPhase("result");
      setIsFighting(false);
      audioManager.stopMusic();
      audioManager.playWinner();
      trackEvent("fight_completed", {
        teamA: teamA.id,
        teamB: teamB.id,
        winner: battleResult.winner.id,
      });
    }, 8600);
  }, [teamA, teamB, schedule, clearTimers]);

  const handleFightAgain = useCallback(() => {
    audioManager.stopMusic();
    audioManager.playClick();
    clearTimers();
    setResult(null);
    setPhase("setup");
    setLeftState("idle");
    setRightState("idle");
    setIsFighting(false);
  }, [clearTimers]);

  return (
    <main className="relative flex min-h-screen w-full flex-col items-center overflow-x-hidden px-4 py-8 sm:py-12">
      <BackgroundEffects />

      {/* Hero */}
      <header className="mb-8 text-center">
        <motion.h1
          initial={{ y: -16, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className="bg-gradient-to-b from-white via-white to-white/40 bg-clip-text px-4 text-[clamp(1.9rem,8vw,3.75rem)] font-black uppercase italic leading-tight tracking-tight text-transparent drop-shadow-sm"
        >
          World Cup
          <br />
          Fight Simulator
        </motion.h1>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="mt-3 text-sm font-semibold text-white/60 sm:text-base"
        >
          Scientifically inaccurate. Emotionally correct.
        </motion.p>
      </header>

      <div className="flex w-full flex-col items-center gap-6">
        <ControlPanel
          teamA={teamA}
          teamB={teamB}
          onTeamAChange={handleTeamAChange}
          onTeamBChange={handleTeamBChange}
          onFight={startFight}
          onRandomMatchup={handleRandomMatchup}
          disabled={isFighting}
          soundEnabled={soundEnabled}
          onToggleSound={handleToggleSound}
        />

        <Arena
          teamA={teamA}
          teamB={teamB}
          leftState={leftState}
          rightState={rightState}
          phase={phase}
          result={result}
        />

        <AnimatePresence>
          {result && phase === "result" && (
            <motion.div
              key="result"
              initial={{ y: 24, opacity: 0, scale: 0.96 }}
              animate={{ y: 0, opacity: 1, scale: 1 }}
              exit={{ y: 12, opacity: 0 }}
              transition={{ type: "spring", stiffness: 140, damping: 16 }}
              className="w-full"
            >
              <ResultCard result={result} onFightAgain={handleFightAgain} />
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Footer disclaimer */}
      <footer className="mt-12 max-w-md text-center text-xs leading-relaxed text-white/40">
        A silly fan-made toy. Not affiliated with FIFA, teams, leagues, or
        players. Not a betting or prediction tool.
      </footer>
    </main>
  );
}
