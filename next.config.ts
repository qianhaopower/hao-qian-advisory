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
      { source: "/premiumhairstyle", destination: "/premiumhairstyle/index.html" },
      { source: "/premiumhairstyle/", destination: "/premiumhairstyle/index.html" },
      // Static landing page. Next lands the request on /friendsintelligence/index.html,
      // so the relative <img src="cover.jpg"> resolves to /friendsintelligence/cover.jpg.
      { source: "/friendsintelligence", destination: "/friendsintelligence/index.html" },
      { source: "/friendsintelligence/", destination: "/friendsintelligence/index.html" },
    ];
  },
};

export default nextConfig;
