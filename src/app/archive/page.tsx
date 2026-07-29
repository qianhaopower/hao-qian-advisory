import type { Metadata } from "next";
import {
  SiteShell,
  Container,
  Kicker,
  PageTitle,
  Lede,
} from "@/components/site/Chrome";

export const metadata: Metadata = {
  title: "Archive",
  description:
    "The record of how things were made — drafts, past versions, and retired chapters of HaoQian.co.",
};

const HOLDINGS: { meta: string; title: string; note: string; href: string }[] = [
  {
    meta: "2025–26 · Draft blog",
    title: "F.R.I.E.N.D.S Intelligence — the original draft",
    note: "The book before it was a book: chapters serialised for feedback.",
    href: "https://www.friendsintelligence.info",
  },
  {
    meta: "2026 · Practice",
    title: "Leadership Advisory",
    note: "The 1:1 advisory practice this site once led with. Kept intact; enquiries still reach me.",
    href: "/advisory",
  },
  {
    meta: "2025–26 · Sites",
    title: "Local business sites",
    note: "Small sites built for Melbourne neighbours — café, pies, jianbing, hair.",
    href: "/sites",
  },
];

export default function ArchivePage() {
  return (
    <SiteShell>
      <Container>
        <section className="pt-16 min-[900px]:pt-20">
          <Kicker>Archive</Kicker>
          <PageTitle>How things were made.</PageTitle>
          <Lede>
            Libraries keep their records. Drafts, past versions, retired
            chapters and the occasional failed experiment live here — the
            process, preserved alongside the work.
          </Lede>
        </section>

        <section className="mt-14 border-t border-ink">
          {HOLDINGS.map((h) => (
            <a
              key={h.href}
              href={h.href}
              className="group grid grid-cols-[1fr_auto] items-baseline gap-x-6 border-b border-hairline px-1 py-5 transition-colors duration-[250ms] hover:bg-surface min-[900px]:grid-cols-[170px_1fr_auto]"
            >
              <span className="hidden font-mono text-[12px] text-faint min-[900px]:block">
                {h.meta}
              </span>
              <span className="min-w-0">
                <span className="font-serif text-[19px] leading-[1.4]">
                  {h.title}
                </span>
                <span className="mt-1 block text-[13.5px] leading-[1.6] text-ink-2">
                  {h.note}
                </span>
              </span>
              <span className="text-[13px] text-accent transition-colors duration-[250ms] group-hover:text-accent-deep">
                Open →
              </span>
            </a>
          ))}
        </section>

        <p className="mt-10 max-w-[640px] text-[14.5px] leading-[1.65] text-ink-2">
          More holdings — book production files, illustrations, slides, design
          drafts — are being catalogued.
        </p>
      </Container>
    </SiteShell>
  );
}
