import Link from "next/link";
import { getConnections } from "@/content/connections";

/*
 * The Connected panel — Design Foundations §05. Green is reserved for exactly
 * this: links between works. Renders nothing when a work has no connections.
 */
export function Connections({ id }: { id: string }) {
  const refs = getConnections(id);
  if (refs.length === 0) return null;

  return (
    <aside className="rounded-[2px] border border-line bg-surface px-7 py-6">
      <div className="meta mb-3 !text-[11px] text-connect">Connected</div>
      <div className="flex flex-col">
        {refs.map((r, i) => (
          <Link
            key={r.id}
            href={r.href}
            className={`block py-3 text-[14px] leading-[1.45] text-ink transition-colors duration-[250ms] hover:text-connect-deep ${
              i < refs.length - 1 ? "border-b border-line" : ""
            }`}
          >
            <span className="mb-0.5 block font-mono text-[10.5px] uppercase tracking-[0.12em] text-faint">
              {r.tag}
            </span>
            {r.title}
          </Link>
        ))}
      </div>
    </aside>
  );
}
