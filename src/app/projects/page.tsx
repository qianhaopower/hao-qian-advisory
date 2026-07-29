import type { Metadata } from "next";
import {
  SiteShell,
  Container,
  Kicker,
  PageTitle,
  Lede,
  Note,
} from "@/components/site/Chrome";
import { PROJECTS } from "@/content/projects";

export const metadata: Metadata = {
  title: "Projects",
  description:
    "Software worth keeping — Hao Qian's projects, from a book-companion app to a balloon studio.",
};

export default function ProjectsPage() {
  return (
    <SiteShell current="/projects">
      <Container>
        <section className="pt-16 min-[900px]:pt-20">
          <Kicker>Projects · {PROJECTS.length} kept</Kicker>
          <PageTitle>Software worth keeping.</PageTitle>
          <Lede>
            Not a showcase — a record. Each project will carry its full story
            here: the problem, the context, the design, the implementation,
            and the lessons that outlasted the code.
          </Lede>
        </section>

        <section className="mt-14 border-t border-ink">
          {PROJECTS.map((p) => {
            const inner = (
              <>
                <span className="hidden font-mono text-[12px] text-faint min-[900px]:block">
                  {p.years}
                </span>
                <span className="min-w-0">
                  <span className="font-serif text-[19px] leading-[1.4]">
                    {p.name}
                  </span>
                  <span className="mt-1 block text-[13.5px] leading-[1.6] text-ink-2">
                    {p.oneLiner}
                  </span>
                </span>
                <span className="text-[13px] text-accent transition-colors duration-[250ms] group-hover:text-accent-deep">
                  {p.href ? "Visit →" : "Story to come"}
                </span>
              </>
            );
            const cls =
              "group grid grid-cols-[1fr_auto] items-baseline gap-x-6 border-b border-hairline px-1 py-5 transition-colors duration-[250ms] hover:bg-surface min-[900px]:grid-cols-[130px_1fr_auto]";
            return p.href ? (
              <a key={p.slug} href={p.href} className={cls}>
                {inner}
              </a>
            ) : (
              <div key={p.slug} className={cls}>
                {inner}
              </div>
            );
          })}
        </section>

        <div className="mt-10 max-w-[720px]">
          <Note>
            The unified write-ups — Problem · Context · Design · Implementation
            · Lessons · Status · Future — are being written project by project.
          </Note>
        </div>
      </Container>
    </SiteShell>
  );
}
