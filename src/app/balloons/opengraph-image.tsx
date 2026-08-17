import { ogCard, OG_SIZE, OG_CONTENT_TYPE } from "@/lib/og";

export const alt = "Balloons — Little Wow Balloons";
export const size = OG_SIZE;
export const contentType = OG_CONTENT_TYPE;

export default function Image() {
  return ogCard({
    kicker: "Balloons",
    title: "Turning air into WOW moments",
    sub: "Balloon art from the Little Wow Balloons studio — archived for good",
  });
}
