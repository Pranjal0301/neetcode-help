"use client";

import Link from "next/link";
import { useStore } from "@/lib/store";
import { isDue } from "@/lib/srs";
import { useNow } from "@/lib/use-now";
import { DifficultyBadge } from "./ui";
import type { Difficulty } from "@/lib/types";

export type ProblemListItem = {
  id: string;
  slug: string;
  title: string;
  difficulty: Difficulty;
  category: string;
  pattern: string | null;
  core: boolean;
};

/** Problem rows with live solved / starred / due state from localStorage. */
export function ProblemList({ items }: { items: ProblemListItem[] }) {
  const { record, toggleSolved, hydrated } = useStore();
  const now = useNow();

  return (
    <ul className="card divide-y divide-line">
      {items.map((p) => {
        const r = record(p.id);
        const due = hydrated && isDue(r.srs ?? undefined, now);
        return (
          <li key={`${p.category}/${p.slug}`} className="flex items-center">
            <button
              type="button"
              onClick={() => toggleSolved(p.id)}
              aria-label={r.solved ? `Mark ${p.title} unsolved` : `Mark ${p.title} solved`}
              aria-pressed={hydrated && r.solved}
              className={`my-2 ml-3 flex h-6 w-6 shrink-0 items-center justify-center rounded-md border text-[12px] transition-colors ${
                hydrated && r.solved
                  ? "border-easy/50 bg-easy/15 text-easy"
                  : "border-line text-transparent hover:border-line-strong hover:text-ink-dim"
              }`}
            >
              &#10003;
            </button>
            <Link
              href={`/dsa/${p.category}/${p.slug}`}
              className="flex min-w-0 flex-1 items-center gap-2.5 px-3 py-2.5 transition-colors hover:bg-white/[0.03]"
            >
              <span className="w-9 shrink-0 font-mono text-[11px] text-ink-dim">
                #{p.id}
              </span>
              <span
                className={`min-w-0 flex-1 truncate text-[14px] ${
                  hydrated && r.solved ? "text-ink-dim" : "text-ink-bright"
                }`}
              >
                {p.title}
              </span>
              {hydrated && r.starred && (
                <span className="shrink-0 text-[12px] text-medium" title="Starred">
                  &#9733;
                </span>
              )}
              {due && (
                <span
                  className="shrink-0 rounded-full bg-accent/15 px-2 py-0.5 font-mono text-[10px] text-accent-soft"
                  title="Due for review"
                >
                  due
                </span>
              )}
              {p.pattern && (
                <span className="hidden shrink-0 font-mono text-[11px] text-ink-dim lg:inline">
                  {p.pattern}
                </span>
              )}
              <DifficultyBadge difficulty={p.difficulty} />
            </Link>
          </li>
        );
      })}
    </ul>
  );
}
