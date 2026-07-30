import { getEssays } from "@/lib/essays";

export const dynamic = "force-static";

const SITE_URL = "https://haoqian.co";

function esc(s: string): string {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

export async function GET() {
  const essays = getEssays();
  const items = essays
    .map((e) => {
      const url = `${SITE_URL}/writing/${e.slug}`;
      return `    <item>
      <title>${esc(`Working Theory № ${e.no} — ${e.title}`)}</title>
      <link>${url}</link>
      <guid isPermaLink="true">${url}</guid>
      <pubDate>${new Date(`${e.date}T00:00:00Z`).toUTCString()}</pubDate>
      <description>${esc(e.excerpt)}</description>
    </item>`;
    })
    .join("\n");

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Working Theory — Hao Qian</title>
    <link>${SITE_URL}/writing</link>
    <atom:link href="${SITE_URL}/feed.xml" rel="self" type="application/rss+xml"/>
    <description>A numbered essay series on AI, engineering, systems thinking and leadership. Turning ideas into systems.</description>
    <language>en</language>
${items}
  </channel>
</rss>
`;

  return new Response(xml, {
    headers: { "Content-Type": "application/rss+xml; charset=utf-8" },
  });
}
