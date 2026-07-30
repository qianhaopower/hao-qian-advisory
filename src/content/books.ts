/*
 * Books — the permanent shelf. Copy is drawn from Hao's own production
 * material: Book Publisher/FRIENDS-INTELLIGENCE-PRODUCTION/00-admin (metadata,
 * Amazon description), the Fish Fun repo (KDP-LISTING.md, book-plan.md), and
 * the Friends Intelligence Diagram Engine (fig sources).
 */

export type BookSection = { heading: string; paras: string[] };
export type BookFigure = { src: string; caption: string };
export type BookListItem = { title: string; note: string };
export type BookLink = { label: string; note?: string; href?: string };
export type BookEvent = { date: string; note: string };

export type Book = {
  slug: string;
  title: string;
  subtitle?: string;
  byline?: string;
  kicker: string;
  status: "published" | "in-progress";
  cover?: { src: string; alt: string };
  coverLabel?: string;
  oneLiner: string;
  facts: string[];
  /** prominent one-click purchase action, shown in the page header */
  buy?: { label: string; href: string };
  sections: BookSection[];
  insideHeading?: string;
  inside?: BookListItem[];
  figuresHeading?: string;
  figures?: BookFigure[];
  editions: BookLink[];
  related?: BookLink[];
  history?: BookEvent[];
};

export const BOOKS: Book[] = [
  {
    slug: "friends-intelligence",
    title: "Friends Intelligence",
    subtitle:
      "The Hidden Patterns Connecting Money, Relationships, Health, and Decisions",
    kicker: "Book · Published June 2026",
    status: "published",
    cover: {
      src: "/friendsintelligence/cover.jpg",
      alt: "Friends Intelligence cover",
    },
    oneLiner:
      "Seven everyday intelligences — F.R.I.E.N.D.S — and the hidden patterns that connect them.",
    facts: [
      "Paperback & Kindle",
      "222 pages · 6×9″",
      "ISBN 9798181687486",
      "First edition, 2026",
    ],
    buy: {
      label: "Buy on Amazon — Paperback & Kindle",
      href: "https://www.amazon.com.au/dp/B0H5R5C8B6",
    },
    sections: [
      {
        heading: "Why this book exists",
        paras: [
          "An ancient Roman dropped into the modern world might think we had solved suffering — medicine, abundance, knowledge in our pockets. So why do so many of us still feel tired, distracted, anxious, and stuck?",
          "The answer is patterns: the invisible defaults, shaped by biology and modern life, that quietly run our money, relationships, health, and decisions. We rarely see them, but they compound. A single choice is just a moment; the same choice repeated for years becomes a life.",
          "We're told that changing your life means trying harder — a new diet, a new budget, a new morning routine. Most of what runs our days isn't willpower. It's patterns, and patterns can be redesigned.",
        ],
      },
      {
        heading: "Seven intelligences, one system",
        paras: [
          "The patterns aren't random, and they're never separate. They cluster into seven everyday intelligences that together spell FRIENDS — and the real power comes from seeing how they connect. Poor sleep dulls emotional control; stress becomes a spending problem; distraction erodes relationships. Loops like these can be redesigned.",
          "Along the way you'll meet simple, memorable ideas: the Fitness Bank, the Food Modes, the Workshop and the Factory, and a “cognitive room” for the people who matter. Every chapter ends with short self-assessments and small daily practices you can start today.",
        ],
      },
    ],
    insideHeading: "The seven pillars",
    inside: [
      { title: "Financial", note: "why money is so hard for the human mind, and how to think clearly about it" },
      { title: "Relationship", note: "how to make real room in your mind for the people who matter" },
      { title: "Information", note: "how to guard your attention and actually learn" },
      { title: "Emotional", note: "how feelings quietly build the reality you live in" },
      { title: "Nutrition", note: "how to eat well in a world designed to make you overeat" },
      { title: "Dynamic", note: "how to move and train in a way that lasts a lifetime" },
      { title: "Sleep", note: "how to protect the foundation everything else rests on" },
    ],
    figuresHeading: "From the book's 27 figures",
    figures: [
      {
        src: "/books/fi/fig-0-friends-pillars.png",
        caption: "Seven Pillars of Intelligence — the wheel that opens the book.",
      },
      {
        src: "/books/fi/fig-3-2-workshop-vs-factory.png",
        caption: "Two Minds at Work — the Workshop and the Factory.",
      },
      {
        src: "/books/fi/fig-6-3-fitness-bank-account.png",
        caption: "The Fitness Bank — small deposits now, withdrawals for life.",
      },
    ],
    editions: [
      { label: "Paperback & Kindle", note: "available", href: "https://www.amazon.com.au/dp/B0H5R5C8B6" },
      { label: "Audiobook", note: "to come" },
      { label: "中文版 · Chinese edition", note: "to come" },
    ],
    related: [
      { label: "Companion app", note: "assessment, focus pillar, daily practices", href: "https://friendsintelligence.net" },
      { label: "The original draft blog", note: "the book, serialised before it was a book", href: "https://www.friendsintelligence.info" },
      { label: "Launch note on LinkedIn", note: "June 2026", href: "https://www.linkedin.com/posts/hao-qian-9ab0b04b_my-book-is-finally-published-it-feels-good-activity-7474331629511921664-FQIe" },
    ],
    history: [
      { date: "2025", note: "Drafted in public — chapters serialised on the Friends Intelligence blog." },
      { date: "Jun 2026", note: "Typeset in Vellum; all 27 figures rendered by a purpose-built diagram engine." },
      { date: "15 Jun 2026", note: "Ebook and paperback submitted to KDP; ebook live." },
      { date: "21 Jun 2026", note: "Announced. In print." },
      { date: "To come", note: "Audiobook and Chinese edition." },
    ],
  },
  {
    slug: "fish-fun",
    title: "Fish Fun",
    byline: "Written and drawn by Isabelle Qian, age 6 · with her dad",
    kicker: "Book · Published July 2026",
    status: "published",
    cover: { src: "/books/fish-fun-cover.jpg", alt: "Fish Fun cover" },
    oneLiner:
      "Goldie, Zoey, Lulu and Stella — four real fish from our living-room tank, their adventures drawn by hand by a six-year-old.",
    facts: [
      "Hardcover · 400 pages · premium colour",
      "8.25×11″",
      "ISBN 9798188767174",
      "Reading age 3–8",
    ],
    buy: {
      label: "Buy on Amazon — Hardcover",
      href: "https://www.amazon.com/dp/B0HBVBBBBX",
    },
    sections: [
      {
        heading: "It started with a real fish tank",
        paras: [
          "There is an actual tank in our living room, and Goldie, Zoey, Lulu and Stella are actual fish. Stella really did arrive one day in a plastic bag. After school, after days out, before bed, Isabelle and I would look at the tank and tell each other stories about what the fish had been up to — flying to the moon, going to university, riding a haunted hotel elevator, arguing over one slice of pizza.",
        ],
      },
      {
        heading: "Then she drew them",
        paras: [
          "Isabelle drew every one of those stories herself. Every idea, every composition, every wobbly line and speech bubble in this book began as her pencil on paper — more than a hundred drawings over one drawing-mad year of being six. None of it was generated by a machine: the adventures are hers, told in her words and drawn by her hand.",
          "My job came after: I scanned her originals, wrote her stories down exactly as she told them, and used AI strictly as a colouring and production assistant — finishing her own linework so it could survive premium-colour printing, never redrawing her ideas. The rule of the whole project, written down on day one: when technical perfection conflicts with the authenticity of a six-year-old's imagination, always choose authenticity.",
        ],
      },
      {
        heading: "From bedtime stories to a bound book",
        paras: [
          "The book is organised the way the tank actually happened: part one is life as three fish; part two begins the day Stella arrives in her bag. In between run the recurring sagas — Lulu at Work, University, the Haunted Hotel, Game Time, the Water Park. The pages were typeset into print masters, proofed with a physical copy, and published as a 400-page hardcover.",
        ],
      },
      {
        heading: "A keepsake, on purpose",
        paras: [
          "Premium-colour hardcovers of this size are expensive to print, and this one was never built to be a bestseller. It was built to exist — so that the family can order copies, and so that the tank, the stories, and the drawings of being six are bound, on paper, forever.",
        ],
      },
    ],
    figuresHeading: "From the tank to the page",
    figures: [
      {
        src: "/books/fish-fun/the-real-tank.jpg",
        caption: "Where it all started — the real tank, the real fish, food tins and all.",
      },
      {
        src: "/books/fish-fun/original-091.jpg",
        caption: "Isabelle's original pencil drawing: the day Stella arrived in a plastic bag.",
      },
      {
        src: "/books/fish-fun/page-091.jpg",
        caption: "The same drawing, colour-finished for print — her composition, her bubbles, untouched. “Who are you?” “Hi! Another fish!”",
      },
      {
        src: "/books/fish-fun/original-092.jpg",
        caption: "Her pencil original of the very last page.",
      },
      {
        src: "/books/fish-fun/page-092.jpg",
        caption: "And the printed last page — the four of them discover Fish Fun. “It's a book.” “It is about us!”",
      },
    ],
    editions: [
      { label: "Hardcover", note: "available", href: "https://www.amazon.com/dp/B0HBVBBBBX" },
    ],
    history: [
      { date: "2025–26", note: "A real tank, four real fish, and a six-year-old who draws their adventures relentlessly." },
      { date: "22 Jul 2026", note: "Image lock — every master verified at print resolution." },
      { date: "23 Jul 2026", note: "Interior built and QA'd: 400 pages, cover-to-cover." },
      { date: "24 Jul 2026", note: "Published. Isabelle Qian, author." },
    ],
  },
  {
    slug: "working-theory",
    title: "Working Theory",
    kicker: "Book · In progress",
    status: "in-progress",
    coverLabel: "manuscript open",
    oneLiner: "The book the essay series is quietly becoming.",
    facts: ["Compiled from the series", "One theory at a time"],
    sections: [
      {
        heading: "Books are software",
        paras: [
          "Idea № 138 in the garden says: books are software — readers compile them. This book is being built that way deliberately. Each theory ships first as an essay, gets tested against real readers and real weeks of work, and earns its place in the manuscript by surviving.",
          "The series comes first; the book is the release build.",
        ],
      },
    ],
    editions: [
      { label: "Read the series", note: "every theory, in full", href: "/writing" },
      { label: "Idea № 138 in the garden", note: "the method, as an idea", href: "/garden" },
    ],
  },
];

export function getBook(slug: string): Book | undefined {
  return BOOKS.find((b) => b.slug === slug);
}
