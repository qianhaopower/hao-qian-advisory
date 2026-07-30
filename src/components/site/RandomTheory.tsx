"use client";

/* Library serendipity — pull one theory off the shelf at random. */
export function RandomTheory({
  slugs,
  label = "Read one at random",
}: {
  slugs: string[];
  label?: string;
}) {
  return (
    <button
      onClick={() => {
        const slug = slugs[Math.floor(Math.random() * slugs.length)];
        window.location.href = `/writing/${slug}`;
      }}
      className="inline-flex items-baseline gap-2 rounded-[2px] border border-btnline px-4 py-2 font-mono text-[12px] uppercase tracking-[0.12em] text-ink-2 transition-colors duration-[250ms] hover:border-ink hover:text-ink"
    >
      <span aria-hidden="true" className="text-[14px] leading-none">⚂</span>
      {label}
    </button>
  );
}
