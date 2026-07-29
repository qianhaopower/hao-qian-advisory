import type { Metadata } from "next";
import { SiteShell, Container, Kicker, PageTitle } from "@/components/site/Chrome";
import { SITE } from "@/content/site";

export const metadata: Metadata = {
  title: "About",
  description:
    "Who Hao Qian is, why he builds, and what this library is for.",
};

const TIMELINE: { year: string; text: string; now?: boolean }[] = [
  {
    year: "2026",
    text: "The library opens. Friends Intelligence and Fish Fun published.",
    now: true,
  },
  {
    year: "2017",
    text: "Became a people manager — the start of a decade of engineering leadership.",
  },
];

export default function AboutPage() {
  return (
    <SiteShell current="/about">
      <Container>
        <section className="pt-16 min-[900px]:pt-20">
          <Kicker>About</Kicker>
          <PageTitle>Who I am, and why I build.</PageTitle>
        </section>

        <section className="prose-read mt-12">
          <h2 className="mb-4 font-serif text-[26px] font-medium leading-[1.3] min-[900px]:text-[28px]">
            Who am I?
          </h2>
          <p>
            I grew up in China and live in Melbourne, Australia, with my family.
            By day I lead software engineering teams — I have been a people
            manager since 2017, across startups and large enterprises, with
            close to a hundred people managed along the way. Outside work I
            write books, build software, play the piano, solve Rubik&rsquo;s
            cubes, and twist balloon animals — sometimes on local streets and
            at festivals.
          </p>

          <h2 className="mb-4 mt-12 font-serif text-[26px] font-medium leading-[1.3] min-[900px]:text-[28px]">
            Why do I build?
          </h2>
          <p>
            Because most of what runs our lives — and our teams, and our
            software — is patterns. Patterns can be seen, named, and
            redesigned. Every book, essay, project and idea here is the same
            move repeated: take something that works as instinct, and turn it
            into a system someone else can use.
          </p>
          <p>
            <em>{SITE.principle}</em> That is the rule this site exists to
            keep. LinkedIn, GitHub, Amazon and YouTube are places my work
            visits; this library is where it lives.
          </p>

          <h2 className="mb-4 mt-12 font-serif text-[26px] font-medium leading-[1.3] min-[900px]:text-[28px]">
            What am I trying to achieve?
          </h2>
          <p>
            In ten years, this site should hold a complete record of my
            thinking. In twenty, a complete collection of my work. In thirty,
            my children should be able to walk these shelves and see how their
            father grew, thought, and made things — one idea at a time.
          </p>
        </section>

        {/* Timeline — §05 */}
        <section className="mt-16 max-w-[640px]">
          <div className="meta mb-8">Milestones</div>
          <div className="flex flex-col gap-7 border-l border-btnline pl-8">
            {TIMELINE.map((t) => (
              <div key={t.year} className="relative">
                <div
                  className={`absolute -left-[36.5px] top-1.5 h-2 w-2 rounded-full ${
                    t.now ? "bg-ink" : "border border-faint bg-paper"
                  }`}
                />
                <div className="font-mono text-[11.5px] text-faint">{t.year}</div>
                <div
                  className={`mt-1 font-serif text-[18px] ${
                    t.now ? "text-ink" : "text-ink-2"
                  }`}
                >
                  {t.text}
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Elsewhere */}
        <section className="mt-16 max-w-[640px]">
          <div className="meta mb-5">Elsewhere</div>
          <ul className="flex flex-col gap-2 text-[14.5px] leading-[1.65] text-ink-2">
            <li>
              <a className="text-accent transition-colors duration-[250ms] hover:text-accent-deep" href={SITE.linkedin}>
                LinkedIn
              </a>{" "}
              — where Working Theory is serialised first.
            </li>
            <li>
              <a className="text-accent transition-colors duration-[250ms] hover:text-accent-deep" href="https://www.amazon.com.au/dp/B0H5R5C8B6">
                Friends Intelligence on Amazon
              </a>{" "}
              and its companion app,{" "}
              <a className="text-accent transition-colors duration-[250ms] hover:text-accent-deep" href="https://friendsintelligence.net">
                friendsintelligence.net
              </a>
              .
            </li>
            <li>
              <a className="text-accent transition-colors duration-[250ms] hover:text-accent-deep" href="https://www.amazon.com/dp/B0HBVBBBBX">
                Fish Fun on Amazon
              </a>{" "}
              — made with my daughter.
            </li>
          </ul>
        </section>

        <p className="mt-20 font-serif text-[23px] italic leading-[1.5]">
          I&rsquo;m building a body of work.
        </p>
      </Container>
    </SiteShell>
  );
}
