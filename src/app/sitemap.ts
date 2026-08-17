import type { MetadataRoute } from "next";
import { getEssays } from "@/lib/essays";
import { BOOKS } from "@/content/books";
import { getPublishedEpisodes } from "@/lib/videos";

const SITE_URL = "https://haoqian.co";

export default function sitemap(): MetadataRoute.Sitemap {
  const staticRoutes = [
    "",
    "/books",
    "/writing",
    "/videos",
    "/projects",
    "/talks",
    "/balloons",
    "/garden",
    "/about",
    "/archive",
    "/search",
  ].map((p) => ({ url: `${SITE_URL}${p}` }));

  const bookRoutes = BOOKS.map((b) => ({
    url: `${SITE_URL}/books/${b.slug}`,
  }));

  const essayRoutes = getEssays().map((e) => ({
    url: `${SITE_URL}/writing/${e.slug}`,
    lastModified: e.date,
  }));

  const episodeRoutes = getPublishedEpisodes().map((e) => ({
    url: `${SITE_URL}/videos/${e.slug}`,
    lastModified: e.publishedAt,
  }));

  return [...staticRoutes, ...bookRoutes, ...essayRoutes, ...episodeRoutes];
}
