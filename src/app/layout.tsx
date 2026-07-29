import type { Metadata } from "next";
import { Newsreader, Instrument_Sans, IBM_Plex_Mono } from "next/font/google";
import "./globals.css";

const newsreader = Newsreader({
  variable: "--font-newsreader",
  subsets: ["latin"],
  style: ["normal", "italic"],
  weight: ["300", "400", "500", "600"],
});

const instrumentSans = Instrument_Sans({
  variable: "--font-instrument",
  subsets: ["latin"],
  weight: ["400", "500", "600"],
});

const plexMono = IBM_Plex_Mono({
  variable: "--font-plex-mono",
  subsets: ["latin"],
  weight: ["400", "500"],
});

export const metadata: Metadata = {
  metadataBase: new URL("https://haoqian.co"),
  title: {
    default: "Hao Qian — Turning ideas into systems",
    template: "%s · Hao Qian",
  },
  description:
    "The library of Hao Qian: books, Working Theory essays, projects, talks and a digital garden. A permanent home for a life's work.",
  openGraph: {
    title: "Hao Qian — Turning ideas into systems",
    description:
      "A library, not a website. Books, essays, projects, talks and ideas — collected permanently.",
    url: "https://haoqian.co",
    siteName: "HaoQian.co",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${newsreader.variable} ${instrumentSans.variable} ${plexMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
