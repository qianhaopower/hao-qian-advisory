import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  reactCompiler: true,
  async rewrites() {
    return [
      { source: "/calla-cups", destination: "/calla-cups/index.html" },
      { source: "/calla-cups/", destination: "/calla-cups/index.html" },
      { source: "/rolfspies", destination: "/rolfspies/index.html" },
      { source: "/rolfspies/", destination: "/rolfspies/index.html" },
      { source: "/tianjinwei", destination: "/tianjinwei/index.html" },
      { source: "/tianjinwei/", destination: "/tianjinwei/index.html" },
    ];
  },
};

export default nextConfig;
