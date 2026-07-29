# HaoQian.co

> Turning ideas into systems.

The personal digital library of Hao Qian — a permanent home for books, Working Theory essays, projects, talks and a digital garden. Built to be tended for decades, not redesigned every season.

- **Strategy:** [STRATEGY.md](STRATEGY.md)
- **Content inventory:** [CONTENT-INVENTORY.md](CONTENT-INVENTORY.md)
- **Working notes for agents/contributors:** [CLAUDE.md](CLAUDE.md)

## Stack

Next.js 16 (App Router) · Tailwind CSS 4 · deployed via AWS Amplify (push to `main`).

```bash
npm run dev     # local dev on :3000
npm run build   # production build
npm run lint
```

## Where things live

| Path | What |
|---|---|
| `src/content/` | All content as typed data files — the shelves |
| `src/components/site/Chrome.tsx` | Header, footer, page shell, primitives |
| `src/app/` | The rooms: books, writing, projects, talks, garden, about, archive |
| `public/` | Static assets incl. legacy sites and book covers |
| `/advisory` | Archived 2026 advisory practice (unlinked, still functional) |
