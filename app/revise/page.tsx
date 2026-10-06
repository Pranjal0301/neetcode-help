import type { Metadata } from "next";
import { getCategories } from "@/lib/content";
import { ReviseView, type ReviseItem } from "@/components/revise-view";

export const metadata: Metadata = {
  title: "Revise",
  description:
    "Spaced repetition over the problems you have solved, so the approaches are still there on interview day.",
};

export default function RevisePage() {
  const items: ReviseItem[] = getCategories().flatMap((c) =>
    c.problems.map((p) => ({
      id: p.id,
      title: p.title,
      slug: p.slug,
      category: c.slug,
      categoryTitle: c.title,
      difficulty: p.difficulty,
      pattern: p.pattern,
    })),
  );

  return (
    <div className="mx-auto max-w-3xl px-4 py-8 sm:py-10">
      <header className="mb-8">
        <h1 className="font-display text-[28px] leading-tight font-bold text-ink-bright sm:text-[34px]">
          Revise
        </h1>
        <p className="mt-2 max-w-xl text-[14.5px] text-ink-dim">
          Solving a problem once is not learning it. Each problem comes back
          just before you would have forgotten the approach — and comes back
          sooner if you rate it honestly.
        </p>
      </header>

      <ReviseView items={items} />
    </div>
  );
}
