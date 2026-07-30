import { ogCard, OG_SIZE, OG_CONTENT_TYPE } from "@/lib/og";
import { getBook } from "@/content/books";

export const alt = "A book by Hao Qian";
export const size = OG_SIZE;
export const contentType = OG_CONTENT_TYPE;

export default async function Image({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const book = getBook(slug);
  if (!book) return ogCard({ kicker: "Books", title: "The shelf" });
  return ogCard({
    kicker: book.kicker,
    title: book.title,
    sub: book.subtitle ?? book.oneLiner,
  });
}
