import { ogCard, OG_SIZE, OG_CONTENT_TYPE } from "@/lib/og";

export const alt = "Books by Hao Qian";
export const size = OG_SIZE;
export const contentType = OG_CONTENT_TYPE;

export default function Image() {
  return ogCard({
    kicker: "Books",
    title: "The shelf so far.",
    sub: "Friends Intelligence · Fish Fun · Working Theory (in progress)",
  });
}
