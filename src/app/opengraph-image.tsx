import { ogCard, OG_SIZE, OG_CONTENT_TYPE } from "@/lib/og";

export const alt = "Hao Qian — Turning ideas into systems";
export const size = OG_SIZE;
export const contentType = OG_CONTENT_TYPE;

export default function Image() {
  return ogCard({
    kicker: "Hao Qian · Melbourne",
    title: "Turning ideas into systems.",
    sub: "Books · Writing · Projects · Talks · Digital Garden",
  });
}
