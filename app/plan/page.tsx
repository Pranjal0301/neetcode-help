import type { Metadata } from "next";
import { getCategories } from "@/lib/content";
import { PlanView } from "@/components/plan-view";
import type { PlanProblem } from "@/lib/plan";

export const metadata: Metadata = {
  title: "Study plan",
  description:
    "Pick a pace from sprint to thorough and get day-by-day targets with pace tracking.",
};

export default function PlanPage() {
  const problems: PlanProblem[] = getCategories().flatMap((c) =>
    c.problems.map((p) => ({
      id: p.id,
      title: p.title,
      category: c.slug,
      categoryTitle: c.title,
      slug: p.slug,
      difficulty: p.difficulty,
      tier: p.tier,
    })),
  );

  return (
    <div className="mx-auto max-w-3xl px-4 py-8 sm:py-10">
      <header className="mb-8">
        <h1 className="font-display text-[28px] leading-tight font-bold text-ink-bright sm:text-[34px]">
          Study plan
        </h1>
        <p className="mt-2 max-w-xl text-[14.5px] text-ink-dim">
          Tell it how many days you have. It picks how many problems fit and
          which ones matter most, keeping every pattern covered — so the only
          question each morning is “what is today’s list?”.
        </p>
      </header>

      <PlanView problems={problems} />
    </div>
  );
}
