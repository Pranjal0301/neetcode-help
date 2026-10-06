import type { Metadata } from "next";
import { getCategories } from "@/lib/content";
import {
  DrillView,
  type DrillCategory,
  type DrillProblem,
} from "@/components/drill-view";

export const metadata: Metadata = {
  title: "Pattern drills",
  description:
    "Read a problem, name the pattern. Trains the mapping step interviews actually test.",
};

export default function DrillsPage() {
  const categories = getCategories();

  const drillCategories: DrillCategory[] = categories.map((c) => ({
    slug: c.slug,
    title: c.title,
    icon: c.icon,
  }));

  const problems: DrillProblem[] = categories.flatMap((c) =>
    c.problems.map((p) => ({
      id: p.id,
      title: p.title,
      slug: p.slug,
      category: c.slug,
      categoryTitle: c.title,
      difficulty: p.difficulty,
      pattern: p.pattern,
      leetcode: p.links.leetcode,
    })),
  );

  return (
    <div className="mx-auto max-w-2xl px-4 py-8 sm:py-10">
      <header className="mb-8">
        <h1 className="font-display text-[28px] leading-tight font-bold text-ink-bright sm:text-[34px]">
          Pattern drills
        </h1>
        <p className="mt-2 text-[14.5px] text-ink-dim">
          No coding. Just the first two minutes of an interview, over and over.
        </p>
      </header>

      <DrillView problems={problems} categories={drillCategories} />
    </div>
  );
}
