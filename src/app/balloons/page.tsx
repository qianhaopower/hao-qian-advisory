import type { Metadata } from "next";
import Link from "next/link";
import {
  SiteShell,
  Container,
  Kicker,
  PageTitle,
  Lede,
} from "@/components/site/Chrome";
import { BalloonDrift } from "@/components/site/BalloonDrift";
import { BalloonGallery } from "@/components/site/BalloonGallery";
import {
  BALLOON_ARCHIVE_ITEMS,
  BALLOON_ARCHIVE_PROFILE,
  BALLOON_STREET_ITEMS,
} from "@/content/balloon-archive";

export const metadata: Metadata = {
  title: "Balloons",
  description:
    "Balloon art by Hao Qian — Little Wow Balloons. Twisted at markets, parties and festivals across Melbourne, archived here for good.",
};

export default function BalloonsPage() {
  const p = BALLOON_ARCHIVE_PROFILE;

  return (
    <SiteShell current="/balloons">
      <Container>
        <section className="pt-16 min-[900px]:pt-20">
          <Kicker>Balloons · Little Wow Balloons</Kicker>
          <PageTitle>Turning air into WOW moments.</PageTitle>
          <Lede>
            Not everything I make is software. Little Wow Balloons is my
            balloon studio — live twisting at kids&apos; parties, markets,
            festivals and on the street across Melbourne. The same hands that
            manage engineering teams make swords and flowers out of latex, and
            those works belong in the library too.
          </Lede>
        </section>

        {BALLOON_STREET_ITEMS.length > 0 && (
          <section className="mt-12">
            <h2 className="meta !text-[11px]">
              On the street · markets, festivals, commissions
            </h2>
            <BalloonGallery items={BALLOON_STREET_ITEMS} crop={false} />
          </section>
        )}

        <div className="mt-14 flex max-w-[640px] items-start gap-4 border-t border-line pt-12">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={p.logo}
            alt="Little Wow Balloons logo"
            className="h-12 w-12 shrink-0 rounded-full border border-line"
          />
          <p className="text-[14.5px] leading-[1.6] text-ink-2">
            <a
              href={p.url}
              className="text-accent transition-colors duration-[250ms] hover:text-accent-deep"
            >
              @{p.handle} ↗
            </a>{" "}
            on Instagram was the studio&apos;s shopfront. As that account turns
            toward books and leadership, the balloon work moves here — where
            nothing expires.
          </p>
        </div>

        {BALLOON_ARCHIVE_ITEMS.length > 0 && (
          <section className="mt-12">
            <h2 className="meta !text-[11px]">
              The works · {BALLOON_ARCHIVE_ITEMS.length} archived from
              Instagram
            </h2>
            <BalloonGallery items={BALLOON_ARCHIVE_ITEMS} />
          </section>
        )}

        <div className="mt-14 flex max-w-[640px] flex-wrap items-baseline gap-x-8 gap-y-3 rounded-[2px] bg-surface px-6 py-4">
          <span className="meta !text-[11px] text-connect">The studio</span>
          <a
            href="https://littlewowballoons.com"
            className="text-[13.5px] text-accent transition-colors duration-[250ms] hover:text-accent-deep"
          >
            littlewowballoons.com ↗
          </a>
          <Link
            href="/projects/little-wow-balloons"
            className="text-[13.5px] text-accent transition-colors duration-[250ms] hover:text-accent-deep"
          >
            How the booking site was built →
          </Link>
        </div>

        <BalloonDrift />
      </Container>
    </SiteShell>
  );
}
