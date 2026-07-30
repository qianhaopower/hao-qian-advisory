import Link from "next/link";
import {
  SiteShell,
  Container,
  Kicker,
  PageTitle,
  Lede,
} from "@/components/site/Chrome";
import { ShelfSuggestions } from "@/components/site/ShelfSuggestions";
import { getEssays } from "@/lib/essays";

export default function NotFound() {
  const pool = getEssays().map((e) => ({
    no: e.no,
    title: e.title,
    slug: e.slug,
  }));

  return (
    <SiteShell>
      <Container>
        <section className="pt-16 min-[900px]:pt-20">
          <Kicker>404 · shelf not found</Kicker>
          <PageTitle>This shelf is empty.</PageTitle>
          <Lede>
            Whatever was meant to be here has been moved, renamed, or never
            existed. Libraries hate to send anyone away empty-handed — so here
            are three theories, pulled at random.
          </Lede>
        </section>

        <section className="mt-12 max-w-[640px]">
          <ShelfSuggestions pool={pool} />
          <div className="mt-8 flex flex-wrap gap-x-8 gap-y-3 text-[14px]">
            <Link
              href="/"
              className="text-accent transition-colors duration-[250ms] hover:text-accent-deep"
            >
              Back to the front desk →
            </Link>
            <Link
              href="/search"
              className="text-accent transition-colors duration-[250ms] hover:text-accent-deep"
            >
              Search the library →
            </Link>
          </div>
        </section>
      </Container>
    </SiteShell>
  );
}
