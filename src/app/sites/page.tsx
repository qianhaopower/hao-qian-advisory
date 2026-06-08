import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Sites",
  description: "A small collection of sites built by Hao Qian.",
};

const SITES = [
  {
    href: "/calla-cups",
    name: "Calla & Cups",
    description: "Independent café in Canterbury, Melbourne.",
    thumb: "/calla-cups/images/interior.jpg",
  },
  {
    href: "/rolfspies",
    name: "Rolf's Pies",
    description: "Pie shop in Box Hill South.",
    thumb: "/rolfspies/photos/pies-rack.jpeg",
  },
  {
    href: "/tianjinwei",
    name: "Tianjin Pancake House",
    description: "Tianjin-style jianbing in Melbourne.",
    thumb: "/tianjinwei/images/hero-tianjin.png",
  },
  {
    href: "/premiumhairstyle",
    name: "Premium Hairstyles",
    description: "Hair salon at Burwood One Shopping Centre, Burwood East.",
    thumb: "/premiumhairstyle/images/storefront.avif",
  },
  {
    href: "/worldcupfighter",
    name: "World Cup Fighter",
    description: "A silly cartoon fight simulator — pick two teams, hit FIGHT.",
    thumb: "/sites/wcf-thumb.svg",
  },
];

export default function SitesPage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <div className="mx-auto max-w-3xl px-5 py-12 md:py-16">
        <header className="mb-10">
          <div className="text-sm font-medium tracking-wide text-slate-600">
            Hao Qian — Sites
          </div>
          <h1 className="mt-4 text-3xl font-semibold leading-tight md:text-4xl">
            A small collection of sites.
          </h1>
          <p className="mt-4 text-lg leading-relaxed text-slate-700">
            Static landing pages built for local businesses. Tap a card to open the site.
          </p>
        </header>

        <section className="grid grid-cols-1 gap-5 md:grid-cols-2">
          {SITES.map((s) => (
            <a
              key={s.href}
              href={s.href}
              className="group overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm transition hover:-translate-y-0.5 hover:border-slate-300 hover:shadow-md"
            >
              <div className="relative aspect-[16/10] overflow-hidden bg-slate-100">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img
                  src={s.thumb}
                  alt={`${s.name} preview`}
                  className="h-full w-full object-cover transition duration-300 group-hover:scale-[1.03]"
                  loading="lazy"
                />
              </div>
              <div className="p-5">
                <div className="flex items-baseline justify-between gap-3">
                  <h2 className="text-lg font-semibold leading-tight">{s.name}</h2>
                  <span className="text-sm text-slate-400 transition group-hover:text-slate-700">→</span>
                </div>
                <p className="mt-2 text-sm leading-relaxed text-slate-600">{s.description}</p>
                <div className="mt-3 font-mono text-xs text-slate-400">hao.qian{s.href}</div>
              </div>
            </a>
          ))}
        </section>

        <footer className="mt-12 border-t border-slate-200 pt-6 text-sm text-slate-500">
          © {new Date().getFullYear()} Hao Qian
        </footer>
      </div>
    </main>
  );
}
