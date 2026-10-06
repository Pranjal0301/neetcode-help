import type { Metadata } from "next";
import { getCategories } from "@/lib/content";
import { MockView, type MockProblem } from "@/components/mock-view";

export const metadata: Metadata = {
  title: "Timed mock",
  description:
    "A countdown and hidden solutions, so you practise solving under real interview pressure.",
};

export default function MockPage() {
  const problems: MockProblem[] = getCategories().flatMap((c) =>
    c.problems.map((p) => ({
      id: p.id,
      title: p.title,
      slug: p.slug,
      category: c.slug,
      categoryTitle: c.title,
      difficulty: p.difficulty,
      leetcode: p.links.leetcode,
    })),
  );

  return (
    <div className="mx-auto max-w-2xl px-4 py-8 sm:py-10">
      <header className="mb-8">
        <h1 className="font-display text-[28px] leading-tight font-bold text-ink-bright sm:text-[34px]">
          Timed mock
        </h1>
        <p className="mt-2 text-[14.5px] text-ink-dim">
          Knowing a solution and producing it in 30 minutes with someone
          watching are different skills. This practises the second one.
        </p>
      </header>

      <MockView problems={problems} />
    </div>
  );
}
