import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  reactCompiler: true,
  async redirects() {
    return [
      // /friendsintelligence used to be an App route. On Amplify the path still
      // resolves to that (now-deleted) route and 404s before an afterFiles
      // rewrite can catch it. Redirects are applied before route resolution, so
      // send visitors straight to the deployed static file (serves 200). Assets
      // use absolute /friendsintelligence/... paths, so they resolve fine.
      { source: "/friendsintelligence", destination: "/friendsintelligence/index.html", permanent: false },
      { source: "/friendsintelligence/", destination: "/friendsintelligence/index.html", permanent: false },
    ];
  },
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
    ];
  },
};

export default nextConfig;
