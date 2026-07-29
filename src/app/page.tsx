import Link from "next/link";
import { SiteShell, Container } from "@/components/site/Chrome";
import { HOME_INDEX, SITE } from "@/content/site";

export default function HomePage() {
  return (
    <SiteShell>
      <Container>
        {/* Masthead */}
        <section className="pt-16 min-[900px]:pt-24">
          <div className="meta">Hao Qian · Melbourne · A library, not a website</div>
          <h1 className="mt-7 max-w-[900px] font-serif text-[44px] font-normal leading-[1.08] tracking-[-0.015em] min-[900px]:text-[76px] min-[900px]:leading-[1.05]">
            {SITE.tagline}
          </h1>
          <p className="mt-7 max-w-[640px] font-serif text-[20px] leading-[1.55] text-ink-2 min-[900px]:text-[24px] min-[900px]:leading-[1.5]">
            {SITE.intro}
          </p>
        </section>

        {/* Index of the library */}
        <nav className="mt-16 border-t border-ink min-[900px]:mt-24">
          {HOME_INDEX.map((entry) => (
            <Link
              key={entry.href}
              href={entry.href}
              className="group grid grid-cols-[1fr_auto] items-baseline gap-x-6 gap-y-1 border-b border-hairline py-5 transition-colors duration-[250ms] hover:bg-surface min-[900px]:grid-cols-[220px_1fr_auto] min-[900px]:py-6"
            >
              <span className="meta order-2 col-span-2 min-[900px]:order-none min-[900px]:col-span-1">
                {entry.meta}
              </span>
              <span className="font-serif text-[26px] leading-[1.25] min-[900px]:text-[28px]">
                {entry.label}
                <span className="ml-4 hidden text-[15px] text-ink-2 min-[900px]:inline">
                  {entry.blurb}
                </span>
              </span>
              <span className="text-[15px] text-faint transition-colors duration-[250ms] group-hover:text-accent">
                →
              </span>
            </Link>
          ))}
        </nav>
      </Container>
    </SiteShell>
  );
}
