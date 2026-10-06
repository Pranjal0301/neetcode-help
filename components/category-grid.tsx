"use client";

import Link from "next/link";
import { useStore } from "@/lib/store";
import { ProgressBar } from "./ui";

export type CategoryCard = {
  slug: string;
  title: string;
  icon: string;
  count: number;
  /** Problem ids in this category, to compute solved counts client-side. */
  ids: string[];
};

export function CategoryGrid({ categories }: { categories: CategoryCard[] }) {
  const { record, hydrated } = useStore();

  return (
    <div className="grid gap-3 sm:grid-cols-2">
      {categories.map((c) => {
        const solved = hydrated
          ? c.ids.filter((id) => record(id).solved).length
          : 0;
        const done = solved === c.count && c.count > 0;
        return (
          <Link
            key={c.slug}
            href={`/dsa/${c.slug}`}
            className="card group flex flex-col gap-3 p-4 transition-colors hover:border-accent/40"
          >
            <div className="flex items-center gap-2.5">
              <span className="text-xl" aria-hidden="true">
                {c.icon}
              </span>
              <span className="min-w-0 flex-1 truncate font-display text-[15px] font-semibold text-ink-bright">
                {c.title}
              </span>
              {done && (
                <span className="shrink-0 text-[13px] text-easy" title="All solved">
                  &#10003;
                </span>
              )}
            </div>
            <div>
              <div className="mb-1.5 flex items-baseline justify-between font-mono text-[11px]">
                <span className="text-ink-dim">
                  {hydrated ? `${solved}/${c.count}` : `${c.count} problems`}
                </span>
                {hydrated && solved > 0 && (
                  <span className="text-accent-soft">
                    {Math.round((solved / c.count) * 100)}%
                  </span>
                )}
              </div>
              <ProgressBar value={solved} max={c.count} />
            </div>
          </Link>
        );
      })}
    </div>
  );
}
