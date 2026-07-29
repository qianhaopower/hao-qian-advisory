import type { Metadata } from "next";
import {
  SiteShell,
  Container,
  Kicker,
  PageTitle,
  Lede,
  Note,
} from "@/components/site/Chrome";

export const metadata: Metadata = {
  title: "Talks",
  description:
    "Public thinking — talks, meetups, podcasts and recordings by Hao Qian.",
};

export default function TalksPage() {
  return (
    <SiteShell current="/talks">
      <Container>
        <section className="pt-16 min-[900px]:pt-20">
          <Kicker>Talks · collecting</Kicker>
          <PageTitle>Public thinking.</PageTitle>
          <Lede>
            Conference talks, meetups, podcasts, and internal talks made
            public — with slides and recordings, so ideas can be cited long
            after the room empties.
          </Lede>
        </section>

        <div className="mt-14 max-w-[720px]">
          <Note label="Empty · deliberately">
            This room is open but the shelves are bare — talks are collected
            here as they happen, not backfilled with filler. The first
            recordings and slides arrive with the next speaking dates.
          </Note>
        </div>
      </Container>
    </SiteShell>
  );
}
