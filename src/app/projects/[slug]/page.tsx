import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { SiteShell, Container, Kicker } from "@/components/site/Chrome";
import { Connections } from "@/components/site/Connections";
import { PROJECTS, getProject } from "@/content/projects";

export function generateStaticParams() {
  return PROJECTS.map((p) => ({ slug: p.slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const project = getProject(slug);
  if (!project) return {};
  return {
    title: project.name,
    description: project.oneLiner,
    openGraph: {
      title: `${project.name} — Hao Qian`,
      description: project.oneLiner,
      type: "article",
    },
  };
}

export default async function ProjectPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const project = getProject(slug);
  if (!project) notFound();

  return (
    <SiteShell current="/projects">
      <Container>
        <header className="pt-16 min-[900px]:pt-20">
          <Kicker>
            <Link
              href="/projects"
              className="transition-colors duration-[250ms] hover:text-accent"
            >
              Projects
            </Link>{" "}
            · {project.years}
          </Kicker>
          <h1 className="mt-6 font-serif text-[34px] font-normal leading-[1.15] tracking-[-0.01em] min-[900px]:text-[44px]">
            {project.name}
          </h1>
          <p className="mt-4 max-w-[640px] font-serif text-[19px] italic leading-[1.5] text-ink-2">
            {project.oneLiner}
          </p>
          {project.facts && (
            <div className="meta mt-6 !normal-case !tracking-[0.08em]">
              {project.facts.join(" · ")}
            </div>
          )}
        </header>

        {/* Status + links */}
        <div className="mt-10 flex max-w-[640px] flex-wrap items-baseline gap-x-8 gap-y-3 rounded-[2px] bg-surface px-6 py-4">
          <span className="meta !text-[11px] text-connect">Current status</span>
          <span className="text-[14.5px] text-ink-2">{project.status}</span>
          {project.links?.map((l) =>
            l.href.startsWith("/") ? (
              <Link
                key={l.href}
                href={l.href}
                className="text-[13.5px] text-accent transition-colors duration-[250ms] hover:text-accent-deep"
              >
                {l.label} →
              </Link>
            ) : (
              <a
                key={l.href}
                href={l.href}
                className="text-[13.5px] text-accent transition-colors duration-[250ms] hover:text-accent-deep"
              >
                {l.label} ↗
              </a>
            )
          )}
        </div>

        {/* The template + connections rail */}
        <div className="mt-12 grid grid-cols-1 items-start gap-10 min-[1000px]:grid-cols-[640px_minmax(240px,1fr)]">
          <div className="max-w-[640px]">
            {project.sections.map((s) => (
              <section key={s.heading} className="mb-11">
                <h2 className="mb-4 font-serif text-[24px] font-medium leading-[1.3] min-[900px]:text-[26px]">
                  {s.heading}
                </h2>
                <div className="prose-read">
                  {s.paras.map((p) => (
                    <p key={p.slice(0, 40)}>{p}</p>
                  ))}
                </div>
              </section>
            ))}
          </div>

          <div className="min-[1000px]:sticky min-[1000px]:top-10">
            <Connections id={`project:${project.slug}`} />
          </div>
        </div>
      </Container>
    </SiteShell>
  );
}
