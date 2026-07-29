import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { SiteShell, Container, Kicker } from "@/components/site/Chrome";
import { getEssay, getEssays, formatDate } from "@/lib/essays";

export function generateStaticParams() {
  return getEssays().map((e) => ({ slug: e.slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const essay = getEssay(slug);
  if (!essay) return {};
  return {
    title: `Working Theory № ${essay.no} — ${essay.title}`,
    description: essay.excerpt,
    openGraph: {
      title: `Working Theory № ${essay.no} — ${essay.title}`,
      description: essay.excerpt,
      type: "article",
      publishedTime: essay.date,
      authors: ["Hao Qian"],
      images: essay.images.length > 0 ? [essay.images[0]] : undefined,
    },
  };
}

export default async function EssayPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const essays = getEssays();
  const index = essays.findIndex((e) => e.slug === slug);
  if (index === -1) notFound();
  const essay = essays[index];
  const newer = index > 0 ? essays[index - 1] : undefined;
  const older = index < essays.length - 1 ? essays[index + 1] : undefined;

  return (
    <SiteShell current="/writing">
      <Container>
        <article className="mx-auto max-w-[640px]">
          <header className="pt-16 min-[900px]:pt-20">
            <Kicker>
              <Link
                href="/writing"
                className="transition-colors duration-[250ms] hover:text-accent"
              >
                Working Theory
              </Link>{" "}
              · № {essay.no}
              {essay.series ? ` · ${essay.series}` : ""}
            </Kicker>
            <h1 className="mt-6 font-serif text-[32px] font-normal leading-[1.18] tracking-[-0.01em] min-[900px]:text-[44px] min-[900px]:leading-[1.15]">
              {essay.title}
            </h1>
            <div className="meta mt-6 !normal-case !tracking-[0.08em]">
              {formatDate(essay.date)} · {essay.minutes} min read
              {essay.topics.length > 0 ? ` · ${essay.topics.join(" · ")}` : ""}
            </div>
          </header>

          <div className="prose-read mt-12">
            {essay.blocks.map((block, i) => (
              <p key={i}>
                {block.map((line, j) => (
                  <span key={j}>
                    {j > 0 && <br />}
                    {line}
                  </span>
                ))}
              </p>
            ))}
          </div>

          {essay.images.length > 0 && (
            <div className="mt-12 flex flex-col gap-6">
              {essay.images.map((src, i) => (
                <figure
                  key={src}
                  className="overflow-hidden rounded-[2px] border border-line"
                >
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img
                    src={src}
                    alt={`${essay.title} — figure ${i + 1}`}
                    className="block w-full"
                    loading="lazy"
                  />
                </figure>
              ))}
            </div>
          )}

          <footer className="mt-14 border-t border-line pt-6">
            <a
              href={essay.url}
              className="text-[13.5px] text-accent transition-colors duration-[250ms] hover:text-accent-deep"
            >
              Originally published on LinkedIn, {formatDate(essay.date)} →
            </a>
          </footer>
        </article>

        {/* neighbours */}
        <nav className="mx-auto mt-14 grid max-w-[640px] grid-cols-1 gap-4 min-[700px]:grid-cols-2">
          {older ? (
            <Link
              href={`/writing/${older.slug}`}
              className="group rounded-[2px] border border-line p-5 transition-colors duration-[250ms] hover:border-faint"
            >
              <div className="meta !text-[11px]">← Earlier · № {older.no}</div>
              <div className="mt-2 font-serif text-[17px] leading-[1.4] group-hover:text-accent">
                {older.title}
              </div>
            </Link>
          ) : (
            <div />
          )}
          {newer ? (
            <Link
              href={`/writing/${newer.slug}`}
              className="group rounded-[2px] border border-line p-5 text-right transition-colors duration-[250ms] hover:border-faint"
            >
              <div className="meta !text-[11px]">Later · № {newer.no} →</div>
              <div className="mt-2 font-serif text-[17px] leading-[1.4] group-hover:text-accent">
                {newer.title}
              </div>
            </Link>
          ) : (
            <div />
          )}
        </nav>
      </Container>
    </SiteShell>
  );
}
