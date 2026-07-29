/*
 * Working Theory — the essay series on LinkedIn, being brought home.
 * Complete series recovered 2026-07-29 from Hao's activity export:
 * #1-#52 with full text archived in content-src/working-theory-text/.
 * Numbers 24 and 27 were skipped in the original series (confirmed by Hao);
 * 48 and 49 were each used twice — the later one is suffixed 'b' (canonical).
 */
export type WorkingTheoryPost = {
  no: string;
  title: string;
  date: string; // YYYY-MM-DD
  url: string;
};

export const WORKING_THEORY: WorkingTheoryPost[] = [
  {
    no: "52",
    title: "When You Stop Seeing The Gate",
    date: "2026-07-25",
    url: "https://www.linkedin.com/posts/hao-qian-9ab0b04b_ai-systemsthinking-leadership-activity-7486643758856294400-LsCL",
  },
  {
    no: "51",
    title: "Four-Dimensional Optimization Problem",
    date: "2026-07-18",
    url: "https://www.linkedin.com/posts/hao-qian-9ab0b04b_ai-systemsthinking-optimization-activity-7484188091037937664-n-WC",
  },
  {
    no: "50",
    title: "Testing The Test",
    date: "2026-07-17",
    url: "https://www.linkedin.com/posts/hao-qian-9ab0b04b_ai-engineering-softwaretesting-activity-7483845997295529984-amEG",
  },
  {
    no: "49b",
    title: "AI Is Fast. Reality Isn’t",
    date: "2026-07-14",
    url: "https://www.linkedin.com/posts/hao-qian-9ab0b04b_ai-leadership-systemsthinking-activity-7482938560291971072-9ObY",
  },
  {
    no: "49",
    title: "From Screenshot to Software",
    date: "2026-07-03",
    url: "https://www.linkedin.com/posts/hao-qian-9ab0b04b_working-theory-49-from-screenshot-to-software-activity-7478811933433831424-8kZp",
  },
  {
    no: "48b",
    title: "From Software Engineering to Knowledge Engineering",
    date: "2026-07-03",
    url: "https://www.linkedin.com/posts/hao-qian-9ab0b04b_working-theory-48-from-software-engineering-activity-7478809349595766784-iG6A",
  },
  {
    no: "48",
    title: "A Third Option",
    date: "2026-06-30",
    url: "https://www.linkedin.com/feed/update/urn:li:activity:7477695187197276160/",
  },
  {
    no: "47",
    title: "The Most Expensive Zero",
    date: "2026-06-24",
    url: "https://www.linkedin.com/feed/update/urn:li:activity:7475518666386661377/",
  },
  {
    no: "46",
    title: "HTML Is The New English",
    date: "2026-06-24",
    url: "https://www.linkedin.com/feed/update/urn:li:activity:7475516591556808704/",
  },
  {
    no: "45",
    title: "Build The Tool First?",
    date: "2026-06-15",
    url: "https://www.linkedin.com/feed/update/urn:li:activity:7472421057153392640/",
  },
  {
    no: "44",
    title: "AI Playbook (Part 4: Set Hard Boundaries)",
    date: "2026-05-30",
    url: "https://www.linkedin.com/feed/update/urn:li:activity:7466618314484748288/",
  },
  {
    no: "43",
    title: "AI Playbook (Part 3: Replay & Learn)",
    date: "2026-05-30",
    url: "https://www.linkedin.com/feed/update/urn:li:activity:7466617043635658752/",
  },
  {
    no: "42",
    title: "AI Playbook (Part 2: Search Before Thinking)",
    date: "2026-05-30",
    url: "https://www.linkedin.com/feed/update/urn:li:activity:7466615699361370112/",
  },
  {
    no: "41",
    title: "AI Playbook (Part 1: Cross-Check Agents)",
    date: "2026-05-30",
    url: "https://www.linkedin.com/feed/update/urn:li:activity:7466614234165104641/",
  },
  {
    no: "40",
    title: "Reinventing Wheels Gets Easier",
    date: "2026-05-26",
    url: "https://www.linkedin.com/feed/update/urn:li:activity:7465004896732475392/",
  },
  {
    no: "39",
    title: "Silicon Brain (Part 4: Leadership Leverage)",
    date: "2026-05-26",
    url: "https://www.linkedin.com/feed/update/urn:li:activity:7465001850090627072/",
  },
  {
    no: "38",
    title: "Silicon Brain (Part 3: Information Is Cheap, Attention Is Not)",
    date: "2026-05-26",
    url: "https://www.linkedin.com/feed/update/urn:li:activity:7464999098719424513/",
  },
  {
    no: "37",
    title: "Silicon Brain (Part 2: Upgrading Your Silicon Brain)",
    date: "2026-05-22",
    url: "https://www.linkedin.com/feed/update/urn:li:activity:7463553392515112962/",
  },
  {
    no: "36",
    title: "Silicon Brain (Part 1: The Right Size of Problem)",
    date: "2026-05-22",
    url: "https://www.linkedin.com/feed/update/urn:li:activity:7463552366546522112/",
  },
  {
    no: "35",
    title: "When The World Speeds Up, Old Limits Break",
    date: "2026-05-22",
    url: "https://www.linkedin.com/feed/update/urn:li:activity:7463410579526000640/",
  },
  {
    no: "34",
    title: "The Octopus Manager (Part 3: Judgment Over Execution)",
    date: "2026-05-21",
    url: "https://www.linkedin.com/feed/update/urn:li:activity:7463043619277414402/",
  },
  {
    no: "33",
    title: "The Octopus Manager (Part 2: External Working Memory)",
    date: "2026-05-21",
    url: "https://www.linkedin.com/feed/update/urn:li:activity:7463040429719191552/",
  },
  {
    no: "32",
    title: "The Octopus Manager — Part 1: Seeing the System",
    date: "2026-05-15",
    url: "https://www.linkedin.com/feed/update/urn:li:activity:7461005092067069952/",
  },
  {
    no: "31",
    title: "Meta Learning",
    date: "2026-05-12",
    url: "https://www.linkedin.com/feed/update/urn:li:activity:7459827756860821504/",
  },
  {
    no: "30",
    title: "Learning Chunk Size",
    date: "2026-05-12",
    url: "https://www.linkedin.com/feed/update/urn:li:activity:7459826351680806913/",
  },
  {
    no: "29",
    title: "Learning Depth",
    date: "2026-05-12",
    url: "https://www.linkedin.com/feed/update/urn:li:activity:7459825247211671552/",
  },
  {
    no: "28",
    title: "Dissolving Interfaces",
    date: "2026-05-11",
    url: "https://www.linkedin.com/feed/update/urn:li:activity:7459556470985211905/",
  },
  {
    no: "26",
    title: "Open Systems Win",
    date: "2026-05-06",
    url: "https://www.linkedin.com/feed/update/urn:li:activity:7457763050570391552/",
  },
  {
    no: "25",
    title: "The Human Signal Premium",
    date: "2026-05-06",
    url: "https://www.linkedin.com/feed/update/urn:li:activity:7457760701118570497/",
  },
  {
    no: "23",
    title: "The Action–Outlook Matrix",
    date: "2026-05-02",
    url: "https://www.linkedin.com/feed/update/urn:li:activity:7456182251903631361/",
  },
  {
    no: "22",
    title: "The Trust Dividend",
    date: "2026-04-30",
    url: "https://www.linkedin.com/posts/hao-qian-9ab0b04b_workingtheory-trust-leadership-activity-7455557378516901888-FzPX",
  },
  {
    no: "21",
    title: "The Relationship Bank",
    date: "2026-04-30",
    url: "https://www.linkedin.com/feed/update/urn:li:activity:7455554860860473344/",
  },
  {
    no: "20",
    title: "The Fitness Bank",
    date: "2026-04-30",
    url: "https://www.linkedin.com/feed/update/urn:li:activity:7455553164746870785/",
  },
  {
    no: "19",
    title: "The Thinking Multiplier",
    date: "2026-04-28",
    url: "https://www.linkedin.com/posts/hao-qian-9ab0b04b_workingtheory-ai-thinking-activity-7454768936807485442-nMhk",
  },
  {
    no: "18",
    title: "The Attention Budget",
    date: "2026-04-28",
    url: "https://www.linkedin.com/feed/update/urn:li:activity:7454766275508981760/",
  },
  {
    no: "17",
    title: "The Domain Size Theory",
    date: "2026-04-28",
    url: "https://www.linkedin.com/feed/update/urn:li:activity:7454764757233893376/",
  },
  {
    no: "16",
    title: "The Recovery Budget",
    date: "2026-04-27",
    url: "https://www.linkedin.com/feed/update/urn:li:activity:7454500968701825024/",
  },
  {
    no: "15",
    title: "The First Anchor Wins",
    date: "2026-04-25",
    url: "https://www.linkedin.com/feed/update/urn:li:activity:7453927899482681345/",
  },
  {
    no: "14",
    title: "The Last Thing Gets the Weight",
    date: "2026-04-25",
    url: "https://www.linkedin.com/feed/update/urn:li:activity:7453738217247293440/",
  },
  {
    no: "13",
    title: "The Urgency Illusion",
    date: "2026-04-24",
    url: "https://www.linkedin.com/feed/update/urn:li:activity:7453400731371409409/",
  },
  {
    no: "12",
    title: "The Reserved Room Theory",
    date: "2026-04-22",
    url: "https://www.linkedin.com/posts/hao-qian-9ab0b04b_workingtheory-leadership-relationships-activity-7452667383669788674-bqB5",
  },
  {
    no: "11",
    title: "The Idea Incubator Theory",
    date: "2026-04-20",
    url: "https://www.linkedin.com/feed/update/urn:li:activity:7451950119828230144/",
  },
  {
    no: "10",
    title: "Meaning Over Origin",
    date: "2026-04-19",
    url: "https://www.linkedin.com/posts/hao-qian-9ab0b04b_workingtheory-ai-meaningoverorigin-activity-7451459048316624896-GtPD",
  },
  {
    no: "9",
    title: "The Room Tension Theory",
    date: "2026-04-17",
    url: "https://www.linkedin.com/feed/update/urn:li:activity:7450845967907487744/",
  },
  {
    no: "8",
    title: "Desk Theory — Rotation",
    date: "2026-04-16",
    url: "https://www.linkedin.com/feed/update/urn:li:activity:7450500387779817472/",
  },
  {
    no: "7",
    title: "Juggling Ball Theory",
    date: "2026-04-05",
    url: "https://www.linkedin.com/posts/hao-qian-9ab0b04b_working-theory-7-juggling-ball-theory-activity-7446442245068869632-44qb",
  },
  {
    no: "6",
    title: "Decision Timing Theory",
    date: "2026-03-25",
    url: "https://www.linkedin.com/feed/update/urn:li:activity:7442518898048110592/",
  },
  {
    no: "5",
    title: "Desk Theory",
    date: "2026-03-21",
    url: "https://www.linkedin.com/feed/update/urn:li:activity:7440951570051248128/",
  },
  {
    no: "4",
    title: "Human-First",
    date: "2026-03-15",
    url: "https://www.linkedin.com/feed/update/urn:li:activity:7438889172527960064/",
  },
  {
    no: "3",
    title: "The 80% Happiness Rule",
    date: "2026-02-07",
    url: "https://www.linkedin.com/posts/hao-qian-9ab0b04b_workingtheory-leadership-activity-7425692246915592192-0khQ",
  },
  {
    no: "2",
    title: "Leadership communication is like adjusting a speaker's volume",
    date: "2026-02-06",
    url: "https://www.linkedin.com/posts/hao-qian-9ab0b04b_workingtheory-leadership-activity-7425405881347084288-vDXg",
  },
  {
    no: "1",
    title: "One change in how software teams work",
    date: "2026-01-31",
    url: "https://www.linkedin.com/feed/update/urn:li:activity:7423490691609067521/",
  },
];
