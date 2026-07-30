import Link from "next/link";
import { NAV, SITE } from "@/content/site";
import { Wordmark } from "@/components/site/Wordmark";

/* 1140px container, 48px margins (24px under 900px) — Design Foundations §04 */
export function Container({
  children,
  className = "",
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <div className={`mx-auto w-full max-w-[1140px] px-6 min-[900px]:px-12 ${className}`}>
      {children}
    </div>
  );
}

export function SiteHeader({ current }: { current?: string }) {
  return (
    <header className="border-b border-line">
      <Container className="flex items-baseline justify-between py-5">
        <Wordmark />
        <nav className="flex flex-wrap items-baseline gap-x-5 gap-y-1 text-[14px] min-[900px]:gap-x-8">
          {NAV.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={`transition-colors duration-[250ms] hover:text-accent ${
                current === item.href ? "text-ink" : "text-ink-2"
              }`}
            >
              {item.label}
            </Link>
          ))}
        </nav>
      </Container>
    </header>
  );
}

export function SiteFooter() {
  return (
    <footer className="mt-30 bg-surface">
      <Container className="flex flex-wrap items-baseline justify-between gap-x-6 gap-y-3 py-10">
        <div className="font-serif text-[17px] italic text-ink-2">
          {SITE.principle}
        </div>
        <div className="flex gap-7 text-[13px]">
          <Link
            href="/archive"
            className="text-ink-2 transition-colors duration-[250ms] hover:text-accent"
          >
            Archive
          </Link>
          <a
            href="/feed.xml"
            className="text-ink-2 transition-colors duration-[250ms] hover:text-accent"
          >
            RSS
          </a>
          <a
            href={SITE.github}
            className="text-ink-2 transition-colors duration-[250ms] hover:text-accent"
          >
            GitHub
          </a>
          <a
            href={SITE.linkedin}
            className="text-ink-2 transition-colors duration-[250ms] hover:text-accent"
          >
            LinkedIn
          </a>
        </div>
      </Container>
    </footer>
  );
}

export function SiteShell({
  current,
  children,
}: {
  current?: string;
  children: React.ReactNode;
}) {
  return (
    <div className="flex min-h-screen flex-col bg-paper text-ink">
      <SiteHeader current={current} />
      <main className="fade-up flex-1">{children}</main>
      <SiteFooter />
    </div>
  );
}

/* Section kicker — mono uppercase label above a Title (§ Meta voice) */
export function Kicker({ children }: { children: React.ReactNode }) {
  return <div className="meta">{children}</div>;
}

/* Page title — Newsreader Title 44/1.15/400 */
export function PageTitle({ children }: { children: React.ReactNode }) {
  return (
    <h1 className="mt-6 font-serif text-[34px] font-normal leading-[1.15] tracking-[-0.01em] text-ink min-[900px]:text-[44px]">
      {children}
    </h1>
  );
}

/* Serif lede under a page title */
export function Lede({ children }: { children: React.ReactNode }) {
  return (
    <p className="mt-6 max-w-[640px] font-serif text-[21px] leading-[1.55] text-ink-2 min-[900px]:text-[24px] min-[900px]:leading-[1.5]">
      {children}
    </p>
  );
}

/* Quiet callout — warm surface, mono label, no icons (§05 Reading components) */
export function Note({
  label = "Note",
  children,
}: {
  label?: string;
  children: React.ReactNode;
}) {
  return (
    <div className="flex items-baseline gap-4 rounded-[2px] bg-surface px-6 py-5">
      <span className="meta flex-none !text-[11px] text-accent">{label}</span>
      <span className="text-[14.5px] leading-[1.65] text-ink-2">{children}</span>
    </div>
  );
}
