/**
 * Procedural audio for the World Cup Fight Simulator.
 *
 * Everything is synthesised at runtime with the Web Audio API — there are no
 * audio files, no external libraries. A tiny singleton manager owns a single
 * AudioContext that is created lazily on the first user interaction (browsers
 * block audio that starts without a gesture). Sound is opt-in: nothing is
 * created or played until `setEnabled(true)` and a sound is requested.
 */

type ToneOpts = {
  frequency: number;
  duration: number;
  type?: OscillatorType;
  volume?: number;
  startTime?: number;
};

type SweepOpts = {
  from: number;
  to: number;
  duration: number;
  type?: OscillatorType;
  volume?: number;
  startTime?: number;
};

type NoiseOpts = {
  duration: number;
  volume?: number;
  filterType?: BiquadFilterType;
  filterFrequency?: number;
  startTime?: number;
};

let ctx: AudioContext | null = null;
let masterGain: GainNode | null = null;
let noiseBuffer: AudioBuffer | null = null;
let enabled = false;
let musicInterval: ReturnType<typeof setInterval> | null = null;
let musicStep = 0;

/** Lazily create / resume the AudioContext. Safe to call repeatedly. Must be
 * invoked from a user gesture the first time so the context can start. */
function init(): void {
  if (typeof window === "undefined") return;
  if (!ctx) {
    const AC: typeof AudioContext | undefined =
      window.AudioContext ||
      (window as unknown as { webkitAudioContext?: typeof AudioContext })
        .webkitAudioContext;
    if (!AC) return;
    try {
      ctx = new AC();
      masterGain = ctx.createGain();
      masterGain.gain.value = 0.35;
      masterGain.connect(ctx.destination);
    } catch {
      ctx = null;
      masterGain = null;
      return;
    }
  }
  if (ctx.state === "suspended") {
    ctx.resume().catch(() => {});
  }
}

/** Returns true only when sound is enabled and a usable context exists. */
function ready(): boolean {
  if (!enabled) return false;
  init();
  return ctx !== null && masterGain !== null;
}

function getNoiseBuffer(): AudioBuffer | null {
  if (!ctx) return null;
  if (!noiseBuffer) {
    const length = Math.floor(ctx.sampleRate * 0.4);
    noiseBuffer = ctx.createBuffer(1, length, ctx.sampleRate);
    const data = noiseBuffer.getChannelData(0);
    for (let i = 0; i < length; i++) data[i] = Math.random() * 2 - 1;
  }
  return noiseBuffer;
}

function playTone({
  frequency,
  duration,
  type = "sine",
  volume = 0.1,
  startTime = 0,
}: ToneOpts): void {
  if (!ctx || !masterGain) return;
  const t = ctx.currentTime + startTime;
  const osc = ctx.createOscillator();
  const gain = ctx.createGain();
  osc.type = type;
  osc.frequency.setValueAtTime(frequency, t);
  gain.gain.setValueAtTime(0.0001, t);
  gain.gain.exponentialRampToValueAtTime(volume, t + 0.008);
  gain.gain.exponentialRampToValueAtTime(0.0001, t + duration);
  osc.connect(gain).connect(masterGain);
  osc.start(t);
  osc.stop(t + duration + 0.03);
}

function playSweep({
  from,
  to,
  duration,
  type = "sine",
  volume = 0.12,
  startTime = 0,
}: SweepOpts): void {
  if (!ctx || !masterGain) return;
  const t = ctx.currentTime + startTime;
  const osc = ctx.createOscillator();
  const gain = ctx.createGain();
  osc.type = type;
  osc.frequency.setValueAtTime(from, t);
  osc.frequency.exponentialRampToValueAtTime(Math.max(1, to), t + duration);
  gain.gain.setValueAtTime(0.0001, t);
  gain.gain.exponentialRampToValueAtTime(volume, t + 0.008);
  gain.gain.exponentialRampToValueAtTime(0.0001, t + duration);
  osc.connect(gain).connect(masterGain);
  osc.start(t);
  osc.stop(t + duration + 0.03);
}

function playNoise({
  duration,
  volume = 0.12,
  filterType = "highpass",
  filterFrequency = 1000,
  startTime = 0,
}: NoiseOpts): void {
  if (!ctx || !masterGain) return;
  const buffer = getNoiseBuffer();
  if (!buffer) return;
  const t = ctx.currentTime + startTime;
  const src = ctx.createBufferSource();
  src.buffer = buffer;
  const filter = ctx.createBiquadFilter();
  filter.type = filterType;
  filter.frequency.setValueAtTime(filterFrequency, t);
  const gain = ctx.createGain();
  gain.gain.setValueAtTime(0.0001, t);
  gain.gain.exponentialRampToValueAtTime(volume, t + 0.006);
  gain.gain.exponentialRampToValueAtTime(0.0001, t + duration);
  src.connect(filter).connect(gain).connect(masterGain);
  src.start(t);
  src.stop(t + duration + 0.03);
}

/* --------------------------------- sounds ---------------------------------- */

function playClick(): void {
  if (!ready()) return;
  playTone({ frequency: 600, duration: 0.05, type: "sine", volume: 0.08 });
}

function playFightStart(): void {
  if (!ready()) return;
  playTone({ frequency: 300, duration: 0.09, type: "square", volume: 0.12, startTime: 0 });
  playTone({ frequency: 500, duration: 0.09, type: "square", volume: 0.12, startTime: 0.08 });
  playTone({ frequency: 700, duration: 0.12, type: "square", volume: 0.13, startTime: 0.16 });
}

function playPunch(): void {
  if (!ready()) return;
  playSweep({ from: 180, to: 80, duration: 0.08, type: "square", volume: 0.2 });
}

function playKick(): void {
  if (!ready()) return;
  playNoise({ duration: 0.12, volume: 0.16, filterType: "highpass", filterFrequency: 1200 });
  playSweep({ from: 240, to: 150, duration: 0.1, type: "triangle", volume: 0.08 });
}

function playHit(): void {
  if (!ready()) return;
  playSweep({ from: 120, to: 50, duration: 0.18, type: "triangle", volume: 0.18 });
  playNoise({ duration: 0.1, volume: 0.12, filterType: "lowpass", filterFrequency: 800 });
}

function playChaos(): void {
  if (!ready()) return;
  for (let i = 0; i < 3; i++) {
    const freq = 300 + Math.random() * 600; // 300–900Hz
    playTone({
      frequency: freq,
      duration: 0.1,
      type: "sawtooth",
      volume: 0.1,
      startTime: i * 0.12,
    });
  }
}

function playKO(): void {
  if (!ready()) return;
  playSweep({ from: 500, to: 80, duration: 0.5, type: "sawtooth", volume: 0.14 });
}

function playWinner(): void {
  if (!ready()) return;
  // C5, E5, G5, C6 arpeggio
  const notes = [523.25, 659.25, 783.99, 1046.5];
  notes.forEach((n, i) => {
    playTone({ frequency: n, duration: 0.18, type: "triangle", volume: 0.12, startTime: i * 0.16 });
  });
}

/* ----------------------------- background music ---------------------------- */

// Low, simple 8-bit fight loop. Bass on the beat, lead on the off-beat.
const MUSIC_BASS: (number | null)[] = [65.41, null, 65.41, null, 98.0, null, 110.0, null]; // C2 C2 G2 A2
const MUSIC_LEAD: number[] = [261.63, 329.63, 392.0, 329.63, 261.63, 329.63, 392.0, 329.63]; // C4 E4 G4 E4
const MUSIC_STEP_MS = 220; // ~136 BPM eighth notes

function musicTick(): void {
  if (!enabled || !ctx || !masterGain) {
    stopMusic();
    return;
  }
  const i = musicStep % 8;
  const bass = MUSIC_BASS[i];
  if (bass) playTone({ frequency: bass, duration: 0.22, type: "triangle", volume: 0.09 });
  playTone({ frequency: MUSIC_LEAD[i], duration: 0.16, type: "square", volume: 0.05 });
  if (i % 2 === 1) {
    playNoise({ duration: 0.03, volume: 0.02, filterType: "highpass", filterFrequency: 6000 });
  }
  musicStep++;
}

function startMusic(): void {
  if (!enabled) return;
  init();
  if (!ctx || !masterGain) return;
  // Never stack loops — clear any existing one first.
  if (musicInterval !== null) {
    clearInterval(musicInterval);
    musicInterval = null;
  }
  musicStep = 0;
  musicTick(); // play the first beat immediately
  musicInterval = setInterval(musicTick, MUSIC_STEP_MS);
}

function stopMusic(): void {
  if (musicInterval !== null) {
    clearInterval(musicInterval);
    musicInterval = null;
  }
  musicStep = 0;
}

/* ----------------------------------- API ----------------------------------- */

function setEnabled(value: boolean): void {
  enabled = value;
  if (!value) stopMusic();
}

function getEnabled(): boolean {
  return enabled;
}

export const audioManager = {
  init,
  setEnabled,
  getEnabled,
  startMusic,
  stopMusic,
  playClick,
  playFightStart,
  playPunch,
  playKick,
  playHit,
  playChaos,
  playKO,
  playWinner,
};
