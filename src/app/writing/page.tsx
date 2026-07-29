import type { Metadata } from "next";
import {
  SiteShell,
  Container,
  Kicker,
  PageTitle,
  Lede,
  Note,
} from "@/components/site/Chrome";
import { WORKING_THEORY } from "@/content/writing";

export const metadata: Metadata = {
  title: "Writing",
  description:
    "Working Theory — Hao Qian's essay series on AI, engineering, systems and leadership.",
};

export default function WritingPage() {
  return (
    <SiteShell current="/writing">
      <Container>
        <section className="pt-16 min-[900px]:pt-20">
          <Kicker>Working Theory · № 1–52 · roughly two a week since Jan 2026</Kicker>
          <PageTitle>One theory at a time.</PageTitle>
          <Lede>
            Working Theory is a numbered essay series on AI, engineering,
            systems thinking and leadership. It is serialised on LinkedIn
            first; every essay is being brought home to live here in full.
          </Lede>
        </section>

        <section className="mt-14 border-t border-ink">
          {WORKING_THEORY.map((post) => (
            <a
              key={post.url}
              href={post.url}
              className="group grid grid-cols-[1fr_auto] items-baseline gap-x-6 border-b border-hairline px-1 py-[18px] transition-colors duration-[250ms] hover:bg-surface min-[900px]:grid-cols-[110px_1fr_auto]"
            >
              <span className="hidden font-mono text-[12px] text-faint min-[900px]:block">
                № {post.no}
              </span>
              <span className="font-serif text-[19px] leading-[1.4]">
                <span className="mr-3 font-mono text-[12px] text-faint min-[900px]:hidden">
                  № {post.no}
                </span>
                {post.title}
              </span>
              <span className="text-[13px] text-accent transition-colors duration-[250ms] group-hover:text-accent-deep">
                Read on LinkedIn →
              </span>
            </a>
          ))}
        </section>

        <div className="mt-10 max-w-[720px]">
          <Note>
            The complete series — every theory since № 1. Full text lives on
            LinkedIn for now and migrates home, one essay page at a time, in a
            coming update.
          </Note>
        </div>
      </Container>
    </SiteShell>
  );
}
