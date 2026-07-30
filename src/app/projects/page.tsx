import type { Metadata } from "next";
import Link from "next/link";
import {
  SiteShell,
  Container,
  Kicker,
  PageTitle,
  Lede,
} from "@/components/site/Chrome";
import { PROJECTS } from "@/content/projects";

export const metadata: Metadata = {
  title: "Projects",
  description:
    "Software worth keeping — Hao Qian's projects, each with the full story: problem, design, implementation, lessons.",
};

export default function ProjectsPage() {
  return (
    <SiteShell current="/projects">
      <Container>
        <section className="pt-16 min-[900px]:pt-20">
          <Kicker>Projects · {PROJECTS.length} kept</Kicker>
          <PageTitle>Software worth keeping.</PageTitle>
          <Lede>
            Not a showcase — a record. Each project carries its full story:
            the problem, the context, the design, the implementation, and the
            lessons that outlasted the code.
          </Lede>
        </section>

        <section className="mt-14 border-t border-ink">
          {PROJECTS.map((p) => (
            <Link
              key={p.slug}
              href={`/projects/${p.slug}`}
              className="group grid grid-cols-[1fr_auto] items-baseline gap-x-6 border-b border-hairline px-1 py-5 transition-colors duration-[250ms] hover:bg-surface min-[900px]:grid-cols-[130px_1fr_auto]"
            >
              <span className="hidden font-mono text-[12px] text-faint min-[900px]:block">
                {p.years}
              </span>
              <span className="min-w-0">
                <span className="font-serif text-[19px] leading-[1.4] transition-colors duration-[250ms] group-hover:text-accent">
                  {p.name}
                </span>
                <span className="mt-1 block text-[13.5px] leading-[1.6] text-ink-2">
                  {p.oneLiner}
                </span>
              </span>
              <span className="text-[13px] text-faint transition-colors duration-[250ms] group-hover:text-accent">
                Read the story →
              </span>
            </Link>
          ))}
        </section>
      </Container>
    </SiteShell>
  );
}
