import { EnquiryForm } from "@/components/EnquiryForm";

export default function HomePage() {
  return (
    <main className="min-h-screen bg-white text-slate-900">
      <div className="mx-auto max-w-3xl px-5 py-12 md:py-16">
        {/* Header */}
        <header className="mb-10">
          <div className="text-sm font-medium tracking-wide text-slate-600">
            Hao Qian — Leadership Advisory
          </div>

          <h1 className="mt-4 text-3xl font-semibold leading-tight md:text-4xl">
            Helping technical professionals become effective managers — without burnout.
          </h1>

          <p className="mt-4 text-lg leading-relaxed text-slate-700">
            1:1 advisory for first-time and early-stage tech managers navigating priorities,
            delegation, and managing up.
          </p>

          <a
            href="#enquiry"
            className="mt-6 inline-flex items-center justify-center rounded-xl bg-slate-900 px-5 py-3 text-sm font-semibold text-white shadow-sm hover:bg-slate-800"
          >
            Send an enquiry
          </a>
        </header>

        {/* Who this is for */}
        <section className="mb-10">
          <h2 className="text-xl font-semibold">Who this is for</h2>
          <p className="mt-3 text-slate-700 leading-relaxed">
            This work is designed for technical professionals who are stepping into greater
            responsibility and finding that the nature of work has fundamentally changed.
          </p>
          <ul className="mt-4 list-disc space-y-2 pl-5 text-slate-700">
            <li>You’ve recently moved from senior IC to manager</li>
            <li>You feel busy and reactive, but unsure what truly deserves your attention</li>
            <li>You’re struggling to balance hands-on work with leadership responsibilities</li>
            <li>You’re navigating stakeholder expectations and managing up for the first time</li>
            <li>You want to lead well without losing your technical identity or burning out</li>
          </ul>
          <p className="mt-4 text-slate-700 leading-relaxed">
            You don’t need motivation or generic leadership advice. You need clarity, leverage,
            and a way of thinking that scales.
          </p>
        </section>

        {/* What I help with */}
        <section className="mb-10">
          <h2 className="text-xl font-semibold">What I help with</h2>
          <p className="mt-3 text-slate-700 leading-relaxed">
            The focus of this work is not theory, but practical decision-making in real situations.
          </p>
          <ul className="mt-4 list-disc space-y-2 pl-5 text-slate-700">
            <li>Prioritisation and time allocation</li>
            <li>Delegation decisions and leverage</li>
            <li>Managing up and stakeholder alignment</li>
            <li>Translating business strategy into day-to-day execution</li>
            <li>Navigating ambiguity, pressure, and cognitive load</li>
            <li>Building a sustainable personal operating system for management</li>
          </ul>
          <p className="mt-4 text-slate-700 leading-relaxed">
            The goal is not to give you answers — it’s to help you develop clearer thinking and
            better judgement as a manager.
          </p>
        </section>

        {/* How it works */}
        <section className="mb-10">
          <h2 className="text-xl font-semibold">How the advisory works</h2>
          <p className="mt-3 text-slate-700 leading-relaxed">
            This is a 1:1 thinking partnership, grounded in your actual work and context.
          </p>
          <div className="mt-4 rounded-2xl border border-slate-200 bg-slate-50 p-5">
            <div className="font-semibold">Typical engagement</div>
            <ul className="mt-3 list-disc space-y-2 pl-5 text-slate-700">
              <li>90-day advisory</li>
              <li>Weekly or bi-weekly 60-minute sessions</li>
              <li>Discussions centred on live challenges, decisions, and trade-offs</li>
              <li>Light async support for critical thinking moments between sessions</li>
            </ul>
          </div>
          <p className="mt-4 text-slate-700 leading-relaxed">
            I work with a small number of clients at a time to ensure depth and quality.
          </p>
        </section>

        {/* About */}
        <section className="mb-10">
          <h2 className="text-xl font-semibold">About me</h2>
          <p className="mt-3 text-slate-700 leading-relaxed">
            I’ve been a people manager in the technology industry since 2017, working across
            startups and large enterprises, including one of Australia’s largest IT organisations.
          </p>
          <p className="mt-3 text-slate-700 leading-relaxed">
            Over that time, I’ve managed close to 100 people in total, with teams of up to 18,
            and have supported multiple senior ICs through their transition into management.
          </p>
           <p className="mt-3 text-slate-700 leading-relaxed">
            Along the way, I’ve seen the full spectrum — people stepping into leadership with confidence, others struggling quietly under the weight of new expectations, and many navigating the tension between technical excellence and people responsibility.
          </p>
          <p className="mt-3 text-slate-700 leading-relaxed">
            My approach is shaped by lived experience — understanding both the technical domain and
            the realities of people leadership at scale.
          </p>
        </section>

        {/* Pricing */}
        <section className="mb-10">
          <h2 className="text-xl font-semibold">Engagement &amp; pricing</h2>
          <p className="mt-3 text-slate-700 leading-relaxed">
            I work in 90-day advisory engagements.
          </p>
          <div className="mt-4 rounded-2xl border border-slate-200 p-5">
            <div className="font-semibold">Indicative pricing</div>
            <ul className="mt-3 list-disc space-y-2 pl-5 text-slate-700">
              <li>
                Individuals: <span className="font-semibold">AUD $3,600 – $5,400</span>
              </li>
              <li>Company-sponsored engagements may vary depending on scope</li>
            </ul>
            <p className="mt-4 text-slate-700 leading-relaxed">
              Pricing is discussed transparently after an initial conversation to ensure fit on both sides.
            </p>
          </div>
        </section>

        {/* Enquiry */}
        <section id="enquiry" className="mb-12">
          <h2 className="text-xl font-semibold">Enquiries</h2>
          <p className="mt-3 text-slate-700 leading-relaxed">
            If this resonates, you’re welcome to reach out for a short, no-pressure conversation.
            This is simply an opportunity to explore whether the work would be useful for you.
          </p>

          <div className="mt-6">
            <EnquiryForm />
          </div>

          <p className="mt-6 text-sm text-slate-600">
            Australia-based
          </p>
        </section>

        <footer className="border-t border-slate-200 pt-6 text-sm text-slate-500">
          © {new Date().getFullYear()} Hao Qian — Leadership Advisory
        </footer>
      </div>
    </main>
  );
}
