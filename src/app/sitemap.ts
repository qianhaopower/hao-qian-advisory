import type { MetadataRoute } from "next";
import { getEssays } from "@/lib/essays";
import { BOOKS } from "@/content/books";

const SITE_URL = "https://haoqian.co";

export default function sitemap(): MetadataRoute.Sitemap {
  const staticRoutes = [
    "",
    "/books",
    "/writing",
    "/projects",
    "/talks",
    "/garden",
    "/about",
    "/archive",
  ].map((p) => ({ url: `${SITE_URL}${p}` }));

  const bookRoutes = BOOKS.map((b) => ({
    url: `${SITE_URL}/books/${b.slug}`,
  }));

  const essayRoutes = getEssays().map((e) => ({
    url: `${SITE_URL}/writing/${e.slug}`,
    lastModified: e.date,
  }));

  return [...staticRoutes, ...bookRoutes, ...essayRoutes];
}
