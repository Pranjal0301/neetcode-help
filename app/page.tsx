import { getCategories, getCoverage } from "@/lib/content";
import { CategoryGrid } from "@/components/category-grid";
import { Dashboard } from "@/components/dashboard";
import { NavCard, ProgressBar, SectionHeading } from "@/components/ui";

const TOOLS = [
  {
    href: "/revise",
    icon: "\u{1F504}",
    title: "Revise",
    description:
      "Spaced repetition over everything you have solved, so approaches stay recallable.",
  },
  {
    href: "/drills",
    icon: "\u{1F3AF}",
    title: "Pattern drills",
    description:
      "Read a problem statement, name the pattern. The one skill interviews actually test.",
  },
  {
    href: "/mock",
    icon: "\u{23F1}",
    title: "Timed mock",
    description:
      "A countdown and hidden solutions, so you practise under interview pressure.",
  },
  {
    href: "/plan",
    icon: "\u{1F5D3}",
    title: "Study plan",
    description:
      "Pick a pace — sprint to thorough — and get day-by-day targets with pace tracking.",
  },
];

export default function HomePage() {
  const categories = getCategories();
  const total = categories.reduce((n, c) => n + c.problems.length, 0);
  const coverage = getCoverage();
  const sequence = categories.flatMap((c) =>
    c.problems.map((p) => ({
      id: p.id,
      title: p.title,
      category: c.slug,
      slug: p.slug,
    })),
  );

  return (
    <div className="mx-auto max-w-3xl px-4 py-10 sm:py-14">
      <header className="mb-9">
        <h1 className="font-display text-[34px] leading-[1.1] font-extrabold text-ink-bright sm:text-[44px]">
          Get interview ready,
          <br />
          <span className="bg-gradient-to-r from-accent-soft to-cyan bg-clip-text text-transparent">
            one pattern at a time.
          </span>
        </h1>
        <p className="mt-4 max-w-xl text-[15px] text-ink-dim">
          The NeetCode 150, taught pattern-first — brute force before the trick,
          a worked trace for every problem, and active recall so it is still
          there on interview day.
        </p>
      </header>

      <Dashboard totalProblems={total} sequence={sequence} />

      <section className="mt-10">
        <SectionHeading>Study tools</SectionHeading>
        <div className="grid gap-3 sm:grid-cols-2">
          {TOOLS.map((t) => (
            <NavCard key={t.href} {...t} />
          ))}
        </div>
      </section>

      <section className="mt-10">
        <SectionHeading>Patterns</SectionHeading>
        <CategoryGrid
          categories={categories.map((c) => ({
            slug: c.slug,
            title: c.title,
            icon: c.icon,
            count: c.problems.length,
            ids: c.problems.map((p) => p.id),
          }))}
        />
      </section>

      <section className="mt-10">
        <SectionHeading hint="Content being written out across all 150 problems. This panel is the honest status.">
          Content coverage
        </SectionHeading>
        <div className="card divide-y divide-line">
          {coverage.map((row) => (
            <div key={row.field} className="flex items-center gap-3 px-4 py-2.5">
              <span className="w-36 shrink-0 text-[13px] text-ink">
                {row.field}
              </span>
              <ProgressBar value={row.have} max={row.total} className="flex-1" />
              <span className="w-16 shrink-0 text-right font-mono text-[11px] text-ink-dim">
                {row.have}/{row.total}
              </span>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
