import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  reactCompiler: true,
  async rewrites() {
    return [
      { source: "/calla-cups", destination: "/calla-cups/index.html" },
      { source: "/calla-cups/", destination: "/calla-cups/index.html" },
    ];
  },
};

export default nextConfig;
