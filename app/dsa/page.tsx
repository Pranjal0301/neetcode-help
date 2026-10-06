import type { Metadata } from "next";
import { getCategories } from "@/lib/content";
import { CategoryGrid } from "@/components/category-grid";

export const metadata: Metadata = {
  title: "Guide",
  description:
    "All 18 NeetCode 150 categories, pattern first — pick a category and work the list.",
};

export default function GuidePage() {
  const categories = getCategories();
  const total = categories.reduce((n, c) => n + c.problems.length, 0);

  return (
    <div className="mx-auto max-w-3xl px-4 py-8 sm:py-10">
      <header className="mb-8">
        <h1 className="font-display text-[28px] leading-tight font-bold text-ink-bright sm:text-[34px]">
          The Guide
        </h1>
        <p className="mt-2 max-w-xl text-[14.5px] text-ink-dim">
          {total} problems across {categories.length} patterns. Each category
          explains its pattern first, then works the problems that drill it — the
          order matters, so go top to bottom unless you are revising.
        </p>
      </header>

      <CategoryGrid
        categories={categories.map((c) => ({
          slug: c.slug,
          title: c.title,
          icon: c.icon,
          count: c.problems.length,
          ids: c.problems.map((p) => p.id),
        }))}
      />
    </div>
  );
}
