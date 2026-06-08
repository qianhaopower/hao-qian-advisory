import type { Metadata } from "next";
import "./worldcupfighter.css";

export const metadata: Metadata = {
  title: "World Cup Fight Simulator",
  description:
    "Scientifically inaccurate. Emotionally correct. Pick two teams, hit FIGHT, and watch a silly cartoon showdown decide it all.",
};

export default function WorldCupFighterLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <div className="wcf-root flex min-h-screen flex-col">{children}</div>
  );
}
