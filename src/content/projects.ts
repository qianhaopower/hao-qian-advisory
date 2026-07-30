/*
 * Projects — software worth keeping, with the thinking behind it.
 * Every write-up follows the same template (STRATEGY.md): Problem · Context ·
 * Design · Implementation · Lessons · Current status · Future. Facts come from
 * the projects' own repos and live sites; drafted for Hao's review, in his voice.
 */

export type ProjectSection = {
  heading:
    | "Problem"
    | "Context"
    | "Design"
    | "Implementation"
    | "Lessons learned"
    | "Future ideas";
  paras: string[];
};

export type Project = {
  slug: string;
  name: string;
  years: string;
  oneLiner: string;
  status: string;
  links?: { label: string; href: string }[];
  facts?: string[];
  sections: ProjectSection[];
};

export const PROJECTS: Project[] = [
  {
    slug: "friends-intelligence-app",
    name: "Friends Intelligence App",
    years: "2026 · ongoing",
    oneLiner:
      "The book as a product — assessment, focus pillar, daily practices. Auth, payments, database, the lot.",
    status: "Live at friendsintelligence.net · free tier + Plus (A$19, lifetime)",
    links: [
      { label: "Open the app", href: "https://friendsintelligence.net" },
      { label: "The book it comes from", href: "/books/friends-intelligence" },
    ],
    facts: [
      "Next.js (App Router) · AWS Amplify · DynamoDB",
      "35-question assessment · 7 pillars · daily practices",
    ],
    sections: [
      {
        heading: "Problem",
        paras: [
          "A book can explain your patterns, but it can't check on you. Readers finish Friends Intelligence, nod, and go back to their week. The ideas needed a form that could ask questions, remember answers, and keep a gentle rhythm going after the last page.",
        ],
      },
      {
        heading: "Context",
        paras: [
          "Built solo, alongside the book itself — the same seven-pillar framework expressed twice: once as chapters, once as software. Idea № 138 in the garden says books are software and readers compile them; this is the compiled edition.",
        ],
      },
      {
        heading: "Design",
        paras: [
          "The core decision is restraint: a 35-question assessment (five per pillar, about eight minutes) produces one focus pillar, not seven dashboards. Depth over breadth — you work on the pillar that will move first, with one small daily practice at a time.",
          "Drift detection without nagging: the app notices when you fade and makes it easy to return, but it never guilt-trips. And pricing is a statement — a lifetime Plus at A$19 instead of a subscription. A wellbeing tool that charges rent forever felt wrong for a book about sustainable defaults.",
        ],
      },
      {
        heading: "Implementation",
        paras: [
          "Next.js App Router on AWS Amplify, with DynamoDB behind it (separate tables for core state and return visits). Auth and payments are real — this is a full product, not a landing page with a form.",
          "The repo runs with team-grade discipline despite one person: no direct pushes to main, feature branches merge to staging first, and a CI branch-policy check enforces it. Future me is the second engineer on this team.",
        ],
      },
      {
        heading: "Lessons learned",
        paras: [
          "Shipping the book and the app as one system beats shipping either alone — each sends people to the other, and the framework got sharper every time it had to survive being turned into questions and scores.",
          "Solo products still deserve staging environments. The branch policy has caught more late-night mistakes than any code review would have.",
        ],
      },
      {
        heading: "Future ideas",
        paras: [
          "Deeper practice content per pillar, and closing the loop with the book's coming editions — the audiobook listener and the app user should meet the same system.",
        ],
      },
    ],
  },
  {
    slug: "content-studio",
    name: "Content Studio · AI Business Mate",
    years: "2026 · ongoing",
    oneLiner:
      "Daily social content in a business's own voice — a producer/consumer system with a Google Sheet as the contract.",
    status: "Live at aibizmate.co · serving Melbourne professional-services clients",
    links: [
      { label: "The studio", href: "https://aibizmate.co" },
      { label: "Interactive demo", href: "https://aibizmate.co/demo.html" },
    ],
    facts: [
      "Static marketing site + Next.js client portal (Amplify)",
      "Local Node content engine · googleapis · SVG→PNG rendering",
    ],
    sections: [
      {
        heading: "Problem",
        paras: [
          "Accountants, brokers and advisers know they should post — and stop, because it's 9pm and the page is blank again. The work isn't unimportant; it's unreasonable. Content Studio makes the daily decision disappear: open the portal, three researched topics are waiting, drafted for every platform in your own voice.",
        ],
      },
      {
        heading: "Context",
        paras: [
          "AI Business Mate is my small Melbourne studio for exactly this kind of client — professionals whose voice matters and whose time is billable. Content Studio is its flagship service: daily posts, branded images, and on the Plus tier monthly newsletters and campaigns.",
        ],
      },
      {
        heading: "Design",
        paras: [
          "The architecture is two programs that share nothing but a Google Sheet. A local content engine — the producer — decides what gets published: it generates the copy, renders branded images, uploads them to Drive, and rewrites a ContentPacks tab. The client portal — the consumer — is a read-only display layer that honestly renders whatever the Sheet contains.",
          "That Sheet is the entire API contract. The engine runs from a laptop and never touches the deployed site; the portal picks changes up on the next page load. No queue, no database, no coupling.",
        ],
      },
      {
        heading: "Implementation",
        paras: [
          "The portal is a Next.js App Router app on Amplify (server-side auth, marketing pages as plain static HTML). The engine is a separate local Node project: content generation, SVG-to-PNG brand image rendering, and googleapis to write the Sheet and Drive.",
        ],
      },
      {
        heading: "Lessons learned",
        paras: [
          "A spreadsheet the client can open beats an admin panel you have to build. The humble Sheet-as-contract gave me producer/consumer separation, an audit trail, and a client-readable source of truth for free.",
          "Voice profiles matter more than volume. The setup call that maps how a client actually talks to their customers is the product; the automation just keeps the promise daily.",
        ],
      },
    ],
  },
  {
    slug: "fish-fun-production-line",
    name: "Fish Fun Production Line",
    years: "2026",
    oneLiner:
      "The pipeline that turned a six-year-old's drawings into a 400-page hardcover — with art treated like code.",
    status: "Book published 24 July 2026 · gift edition planned",
    links: [
      { label: "The book it produced", href: "/books/fish-fun" },
      { label: "Fish Fun on Amazon", href: "https://www.amazon.com/dp/B0HBVBBBBX" },
    ],
    facts: [
      "166 locked page images · SHA-256 manifests · Python tooling",
      "KDP 8.25×11″ premium-colour hardcover · 300–600 DPI pipeline",
    ],
    sections: [
      {
        heading: "Problem",
        paras: [
          "There is a real tank in our living room with four real fish, and a daughter who spent a year drawing their imagined adventures — by hand, in pencil, more than a hundred of them. The pile deserved better than a drawer, but a printed book demands consistency a six-year-old's output cheerfully ignores: print-safe resolution, bleed and gutter margins, one coherent visual world across a hundred pages.",
        ],
      },
      {
        heading: "Context",
        paras: [
          "The guiding principle was written down on day one: when technical perfection conflicts with the authenticity of a six-year-old's imagination, always choose authenticity. Isabelle is the author — every adventure, composition and speech bubble is hers, told in her words and drawn by her hand. AI worked strictly as the colouring and production assistant, finishing her own linework for print, never inventing a page. Every creative question — what's happening, who is who — came from her description, never from a model's guess.",
        ],
      },
      {
        heading: "Design",
        paras: [
          "A folder pipeline any engineer would recognise: originals → stories → illustrations → print pages → book. Each drawing got a stable intake ID assigned once and never renamed, linking the scan to her verbatim story, the dialogue map, the prompts, the enhanced artwork and the final print page.",
          "Consistency came from two binding documents — a character bible for the four fish and a style guide for everything else — and from audits run per page: emotion audit, guest-fish check, no invented characters or props.",
        ],
      },
      {
        heading: "Implementation",
        paras: [
          "Python tools for everything: enhancement of faint pencil scans, per-page compose scripts with kid-lettering for speech bubbles, a build script that assembles the whole book as facing spreads, and QA scripts that re-hash every locked image. A voice-note inbox let stories be captured from a phone the moment she told them.",
          "When the page review finished, all 166 page images were frozen — read-only copies plus a SHA-256 manifest, exactly like a release lock. The final interior went to KDP as a 400-page premium-colour hardcover after a physical proof; screen-only approval was never allowed.",
        ],
      },
      {
        heading: "Lessons learned",
        paras: [
          "Treat art like code and the whole project calms down: single source of truth for the current version of every page, checksums against silent regressions, an audit script for drift. The one production incident — compose scripts on eleven pages quietly writing to files the book never used — is exactly the class of bug the manifest was built to catch.",
          "The success metric was written before the tooling: not sales — a keepsake Isabelle will still love reading in twenty years. Every technical decision got easier once that was the test.",
        ],
      },
      {
        heading: "Future ideas",
        paras: [
          "A classmate gift edition — the production recipe survived the first print run and is documented, so the second book is mostly a decision, not a project.",
        ],
      },
    ],
  },
  {
    slug: "world-cup-fighter",
    name: "World Cup Fighter",
    years: "2026",
    oneLiner:
      "A silly cartoon fight simulator — 55 teams, procedural sound, shareable battle cards.",
    status: "Live at /worldcupfighter",
    links: [{ label: "Pick two teams and hit FIGHT", href: "/worldcupfighter" }],
    facts: [
      "React + TypeScript · framer-motion · Web Audio API · html2canvas",
    ],
    sections: [
      {
        heading: "Problem",
        paras: [
          "None whatsoever. The World Cup was on, and the world needed a way to settle matches by cartoon combat.",
        ],
      },
      {
        heading: "Context",
        paras: [
          "A palate-cleanser project — the kind you build to stay in love with building. It shares the site's infrastructure but none of its seriousness.",
        ],
      },
      {
        heading: "Design",
        paras: [
          "Two fighters, one arena, one button. Fifty-five teams with flags and colours, a battle engine that scripts each round, and a result card designed to be screenshotted and argued about in group chats.",
        ],
      },
      {
        heading: "Implementation",
        paras: [
          "React and TypeScript inside this site's Next.js app. Animations by framer-motion; every sound is generated procedurally with the Web Audio API — no audio files shipped at all. Share cards are rendered with html2canvas so a battle result travels as an image.",
        ],
      },
      {
        heading: "Lessons learned",
        paras: [
          "Procedural audio is criminally underused: zero assets, instant load, and punches can vary every time. And a share card is the whole growth strategy for a toy — build the screenshot first.",
        ],
      },
    ],
  },
  {
    slug: "little-wow-balloons",
    name: "Little Wow Balloons",
    years: "2025 · ongoing",
    oneLiner:
      "My balloon studio — live twisting for parties and festivals, delivered bundles across Melbourne.",
    status: "Live at littlewowballoons.com · taking bookings",
    links: [{ label: "The studio", href: "https://littlewowballoons.com" }],
    facts: ["Vite + React single-page site · AWS Amplify"],
    sections: [
      {
        heading: "Problem",
        paras: [
          "I twist balloons — at kids' parties, corporate events, festivals, schools, on the street. What began as performing needed the boring machinery of a real service: what's offered, what it costs, how to book, and answers to the questions every parent asks.",
        ],
      },
      {
        heading: "Context",
        paras: [
          "This is the personal side of the library made visible: the same hands that manage engineering teams also make swords and flowers out of latex. The business is real — live entertainment by the hour, plus pre-made delivery bundles for parties I can't attend in person.",
        ],
      },
      {
        heading: "Design",
        paras: [
          "One page, everything a booking parent needs: five event categories, transparent pricing, delivery bundles at three sizes, a gallery of actual balloon work, a three-step booking flow, and an FAQ that answers safety, coverage and insurance before anyone has to ask.",
        ],
      },
      {
        heading: "Implementation",
        paras: [
          "A deliberately small Vite + React single-page app — the second iteration of the site — deployed on Amplify. No backend; enquiries flow straight to email with a 24-hour response promise.",
        ],
      },
      {
        heading: "Lessons learned",
        paras: [
          "Service businesses win on answered questions, not aesthetics. The FAQ and transparent pricing convert better than any hero image — people book when nothing is left vague.",
        ],
      },
    ],
  },
  {
    slug: "charis-mortgage",
    name: "Charis Mortgage",
    years: "2026",
    oneLiner:
      "Client site for a Melbourne broker — calculators, three languages, and a suburb-ranking report engine with no database at all.",
    status: "Live at charismortgage.com.au",
    links: [{ label: "The site", href: "https://charismortgage.com.au" }],
    facts: [
      "Next.js · no database, no CRM, no paid runtime APIs",
      "EN · 中文 · 粤语 · Web3Forms as the only external call",
    ],
    sections: [
      {
        heading: "Problem",
        paras: [
          "Charis Fok is an independent broker who specialises in helping migrants navigate Australian lending. Her clients research hard before they trust anyone — the site had to demonstrate expertise (calculators, real guidance, reviews) in three languages, without the budget or upkeep of a SaaS stack.",
        ],
      },
      {
        heading: "Design",
        paras: [
          "The centrepiece is the Property Opportunity Report: a questionnaire that auto-ranks a suburb shortlist for the visitor, shows a free preview, and unlocks the full printable report by email. It turns an anonymous visit into a conversation with something genuinely useful changing hands.",
          "Everything else builds trust the plain way — borrowing-capacity and repayment calculators, five-star reviews surfaced prominently, and full content in English, Mandarin and Cantonese.",
        ],
      },
      {
        heading: "Implementation",
        paras: [
          "Next.js with a contrarian constraint: no database, no accounts, no CRM, no paid runtime APIs. The entire suburb dataset ships baked into the site; the only external call in production is the browser posting to Web3Forms when someone unlocks a report or sends the contact form.",
        ],
      },
      {
        heading: "Lessons learned",
        paras: [
          "For a single-client site, every moving part you don't add is future support work you don't owe. Static data plus one forms endpoint gives the client a site that effectively cannot break — and a 'report engine' doesn't need a server to feel like a product.",
        ],
      },
    ],
  },
  {
    slug: "local-business-sites",
    name: "Local Business Sites",
    years: "2025–26",
    oneLiner:
      "A café, a pie shop, a jianbing house, a hair salon — small fast sites for real neighbours.",
    status: "Live under /sites",
    links: [{ label: "The collection", href: "/sites" }],
    facts: ["Plain static HTML/CSS · real photography · zero build tooling"],
    sections: [
      {
        heading: "Problem",
        paras: [
          "Melbourne is full of excellent small businesses whose entire web presence is a Google Maps pin. Calla & Cups, Rolf's Pies, Tianjin Pancake House, Premium Hairstyles — each needed a page that shows what they make, where they are, and when they're open. Nothing more, and nothing slower.",
        ],
      },
      {
        heading: "Design",
        paras: [
          "One page per business, led by real photographs of the actual food, the actual room, the actual work. No templates dressed up as design, no cookie banners, no popups — the page equivalent of a good shopfront.",
        ],
      },
      {
        heading: "Implementation",
        paras: [
          "Deliberately plain static HTML and CSS served from this site's public folder. No build step, no framework, no dependencies to rot. A page that is finished stays finished.",
        ],
      },
      {
        heading: "Lessons learned",
        paras: [
          "Constraints are a service to the client: a site with zero moving parts is one they never have to think about again. These pages taught me the pattern that later scaled up — ship the smallest thing that is genuinely complete.",
        ],
      },
    ],
  },
  {
    slug: "haoqian-co",
    name: "HaoQian.co",
    years: "2026 · ongoing",
    oneLiner: "This library itself — a body of work given a permanent home.",
    status: "You are reading it",
    links: [
      { label: "The strategy, in public", href: "https://github.com/qianhaopower/hao-qian-advisory" },
    ],
    facts: [
      "Next.js 16 · Tailwind 4 · AWS Amplify",
      "Content as typed data files · no CMS · design by owner, build by agent",
    ],
    sections: [
      {
        heading: "Problem",
        paras: [
          "My work was scattered — essays on LinkedIn, books on Amazon, apps on their own domains, drawings in folders, ideas in chat logs. Platforms are rented rooms; they reorganise, decay, or disappear. A life's work needs a building it owns.",
        ],
      },
      {
        heading: "Context",
        paras: [
          "The strategy is written down and lives in this repo: this is not a portfolio, a blog, or a resume — it is a library built to be tended for decades. Success is measured in ten, twenty, thirty years: a complete record of the thinking, the work preserved, and children who can walk the shelves.",
        ],
      },
      {
        heading: "Design",
        paras: [
          "I designed the foundations myself in Claude Design — 'a library, not a website': Newsreader for reading, warm paper neutrals, one blue for links and one green reserved for connections between works, a 640-pixel reading measure, motion at a single 250ms curve.",
          "Everything has a home and every home has a shape: books carry their editions and history, essays carry their provenance, the garden carries numbered ideas that are never finished.",
        ],
      },
      {
        heading: "Implementation",
        paras: [
          "Next.js 16 with Tailwind 4 on AWS Amplify. All content is typed data files and plain text in the repo — no CMS, no database. The full text of every Working Theory essay was recovered from LinkedIn and lives in version control; adding a new one is a two-file change.",
          "The repo is agent-operable by design: strategy, content inventory and working conventions are documented in-repo, so any future session — human or AI — can pick up the library and keep building without re-learning it.",
        ],
      },
      {
        heading: "Lessons learned",
        paras: [
          "Own the source of truth and let platforms be distribution. Every essay brought home, every book page built from real production files, made the site more valuable than the sum of the links it replaced.",
          "The owner should make the taste decisions and the agent should make them real. The design system took one afternoon once it was mine; implementing it took an agent one more.",
        ],
      },
      {
        heading: "Future ideas",
        paras: [
          "The connections panel — the green links that let a reader walk from an idea to the essay it seeded to the book it became. Search, once the shelves are fuller. A dark pass, already specced.",
        ],
      },
    ],
  },
];

export function getProject(slug: string): Project | undefined {
  return PROJECTS.find((p) => p.slug === slug);
}
