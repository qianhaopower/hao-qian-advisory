import type { NextConfig } from "next";
import { createHash } from "node:crypto";
import { readdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";

/*
 * A fingerprint of the house sign's own source (/pingan). The page carries it
 * and compares it with the one that is live, so a phone holding an old copy
 * can reload itself — see src/lib/pingan-fresh.ts. Hashed from the files, not
 * from a clock or a commit: the same in every build worker, and it changes
 * only when the sign does.
 */
function fingerprint(paths: string[]): string {
  const hash = createHash("sha1");
  const add = (rel: string) => {
    const abs = join(process.cwd(), rel);
    if (statSync(abs).isDirectory()) {
      for (const name of readdirSync(abs).sort()) add(`${rel}/${name}`);
    } else {
      hash.update(rel).update(readFileSync(abs));
    }
  };
  paths.forEach(add);
  return hash.digest("hex").slice(0, 8);
}

const PINGAN_VERSION = fingerprint([
  "src/app/pingan",
  "src/components/pingan",
  "src/content/pingan.ts",
  "src/lib/pingan-share.ts",
  "src/lib/pingan-fresh.ts",
  "src/lib/fireworks.ts",
  "src/components/site/BalloonDrift.tsx",
]);

const nextConfig: NextConfig = {
  /* config options here */
  reactCompiler: true,
  env: { NEXT_PUBLIC_PINGAN_VERSION: PINGAN_VERSION },
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
