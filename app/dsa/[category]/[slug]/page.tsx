import Link from "next/link";
import { notFound } from "next/navigation";
import type { Metadata } from "next";
import {
  getCategories,
  getCategory,
  getNeighbours,
  getProblem,
  resolveSlug,
} from "@/lib/content";
import { highlightAll } from "@/lib/highlight";
import { LANGUAGES } from "@/lib/types";
import { CodeTabs } from "@/components/code-tabs";
import { Diagram } from "@/components/diagrams";
import {
  ProblemNotes,
  RecallRating,
  SolvedToggle,
} from "@/components/problem-controls";
import { RevealPrompt, ReviewBanner } from "@/components/reveal-gate";
import { Inline, RichText } from "@/components/rich-text";
import {
  Callout,
  DifficultyBadge,
  ExternalLink,
  PatternChip,
  SectionHeading,
} from "@/components/ui";

type Params = { category: string; slug: string };

export function generateStaticParams(): Params[] {
  return getCategories().flatMap((c) =>
    c.problems.map((p) => ({ category: c.slug, slug: p.slug })),
  );
}

export async function generateMetadata({
  params,
}: {
  params: Promise<Params>;
}): Promise<Metadata> {
  const { category, slug } = await params;
  const problem = getProblem(category, slug);
  if (!problem) return {};
  return {
    title: `${problem.title} (#${problem.id})`,
    description:
      problem.keyInsight ??
      `${problem.pattern ?? "Approach"} solution to ${problem.title}, with complexity analysis and a worked trace.`,
  };
}

export default async function ProblemPage({
  params,
}: {
  params: Promise<Params>;
}) {
  const { category: categorySlug, slug } = await params;
  const category = getCategory(categorySlug);
  const problem = getProblem(categorySlug, slug);
  if (!category || !problem) notFound();

  const blocks = await highlightAll(
    problem.code,
    LANGUAGES.map((l) => l.id),
  );
  const { prev, next } = getNeighbours(categorySlug, slug);
  const related = problem.related
    .map((s) => resolveSlug(s))
    .filter((p): p is NonNullable<typeof p> => !!p);

  return (
    <article className="mx-auto max-w-3xl px-4 py-8 sm:py-10">
      <nav className="mb-5 flex items-center gap-1.5 text-[12px] text-ink-dim">
        <Link href="/dsa" className="hover:text-ink-bright">
          Guide
        </Link>
        <span aria-hidden="true">/</span>
        <Link href={`/dsa/${category.slug}`} className="hover:text-ink-bright">
          {category.title}
        </Link>
      </nav>

      <ReviewBanner />

      <header className="mb-7">
        <div className="flex items-start gap-3">
          <div className="min-w-0 flex-1">
            <div className="mb-1.5 flex items-center gap-2.5">
              <span className="font-mono text-[13px] text-ink-dim">
                #{problem.id}
              </span>
              <DifficultyBadge difficulty={problem.difficulty} />
            </div>
            <h1 className="font-display text-[26px] leading-tight font-bold text-ink-bright sm:text-[31px]">
              {problem.title}
            </h1>
          </div>
          <SolvedToggle id={problem.id} />
        </div>

        <div className="mt-4 flex flex-wrap items-center gap-2">
          {/* The pattern name is the answer in review mode, so it hides too. */}
          {problem.pattern && (
            <span className="review-gated">
              <PatternChip pattern={problem.pattern} />
            </span>
          )}
          {problem.links.leetcode && (
            <ExternalLink href={problem.links.leetcode}>LeetCode</ExternalLink>
          )}
          {problem.links.neetcodeVideo && (
            <ExternalLink href={problem.links.neetcodeVideo}>
              NeetCode video
            </ExternalLink>
          )}
        </div>
      </header>

      <div className="space-y-7">
        <RevealPrompt />

        {/* Everything explanatory hides in review mode; see components/reveal-gate.tsx. */}
        <div className="review-gated space-y-7">
          {problem.patternTriggers.length > 0 && (
          <Callout tone="info" title="Reach for this pattern when" icon="&#9906;">
            <ul className="space-y-1.5">
              {problem.patternTriggers.map((t, i) => (
                <li key={i} className="flex gap-2">
                  <span className="mt-px shrink-0 text-info" aria-hidden="true">
                    &rsaquo;
                  </span>
                  <span>
                    <Inline text={t} />
                  </span>
                </li>
              ))}
            </ul>
          </Callout>
        )}

        {problem.keyInsight && (
          <Callout tone="accent" title="Key insight" icon="&#9679;">
            <RichText text={problem.keyInsight} />
          </Callout>
        )}

        {problem.bruteForce && (
          <section>
            <SectionHeading hint="Start here in an interview, then earn the optimisation out loud.">
              Brute force first
            </SectionHeading>
            <div className="card divide-y divide-line">
              <div className="px-4 py-3.5">
                <RichText text={problem.bruteForce.idea} />
                <div className="mt-2.5 flex flex-wrap gap-x-5 gap-y-1 font-mono text-[12px]">
                  <span className="text-ink-dim">
                    Time <span className="text-hard">{problem.bruteForce.time}</span>
                  </span>
                  <span className="text-ink-dim">
                    Space{" "}
                    <span className="text-hard">{problem.bruteForce.space}</span>
                  </span>
                </div>
              </div>
              <div className="bg-hard/[0.04] px-4 py-3">
                <div className="mb-1 text-[11px] font-bold tracking-wide text-hard uppercase">
                  Why it fails
                </div>
                <RichText
                  text={problem.bruteForce.whyItFails}
                  className="text-[14px]"
                />
              </div>
            </div>
          </section>
        )}

        {problem.approach.length > 0 && (
          <section>
            <SectionHeading>Approach</SectionHeading>
            <ol className="card divide-y divide-line">
              {problem.approach.map((step, i) => (
                <li key={i} className="flex gap-3 px-4 py-3">
                  <span className="mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-accent/15 font-mono text-[11px] font-bold text-accent-soft">
                    {i + 1}
                  </span>
                  <span className="text-[14.5px]">
                    <Inline text={step} />
                  </span>
                </li>
              ))}
            </ol>
          </section>
        )}

        {problem.diagram && (
          <section>
            <SectionHeading>How it works</SectionHeading>
            <Diagram diagram={problem.diagram} />
          </section>
        )}

        {blocks.length > 0 && (
          <section>
            <SectionHeading>Solution</SectionHeading>
            <div className="card overflow-hidden p-0">
              <CodeTabs blocks={blocks} />
            </div>
          </section>
        )}

        {problem.complexity && (
          <section>
            <SectionHeading>Complexity</SectionHeading>
            <div className="card flex flex-wrap items-center gap-x-8 gap-y-2 px-4 py-3.5">
              {problem.complexity.time && (
                <div>
                  <div className="text-[11px] font-bold tracking-wide text-ink-dim uppercase">
                    Time
                  </div>
                  <div className="font-mono text-[15px] text-easy">
                    {problem.complexity.time}
                  </div>
                </div>
              )}
              {problem.complexity.space && (
                <div>
                  <div className="text-[11px] font-bold tracking-wide text-ink-dim uppercase">
                    Space
                  </div>
                  <div className="font-mono text-[15px] text-info">
                    {problem.complexity.space}
                  </div>
                </div>
              )}
              {problem.complexity.note && (
                <p className="w-full border-t border-line pt-2.5 text-[13.5px] text-ink-dim">
                  <Inline text={problem.complexity.note} />
                </p>
              )}
            </div>
          </section>
        )}

        {problem.dryRun && (
          <section>
            <SectionHeading hint="Trace it by hand once — this is what makes the pattern stick.">
              Dry run
            </SectionHeading>
            <pre className="codeblock rounded-card px-4 py-3.5 whitespace-pre text-ink">
              {problem.dryRun}
            </pre>
          </section>
        )}

        {problem.pitfalls.length > 0 && (
          <Callout tone="hard" title="Common mistakes" icon="&#9888;">
            <ul className="space-y-1.5">
              {problem.pitfalls.map((p, i) => (
                <li key={i} className="flex gap-2">
                  <span className="mt-px shrink-0 text-hard" aria-hidden="true">
                    &rsaquo;
                  </span>
                  <span>
                    <Inline text={p} />
                  </span>
                </li>
              ))}
            </ul>
          </Callout>
        )}

        {problem.edgeCases.length > 0 && (
          <section>
            <SectionHeading hint="Say these out loud before you start coding.">
              Edge cases
            </SectionHeading>
            <ul className="card divide-y divide-line">
              {problem.edgeCases.map((e, i) => (
                <li
                  key={i}
                  className="px-4 py-2.5 font-mono text-[13px] text-ink"
                >
                  <Inline text={e} />
                </li>
              ))}
            </ul>
          </section>
        )}

        {problem.followUps.length > 0 && (
          <section>
            <SectionHeading hint="Try to answer before expanding.">
              Interview follow-ups
            </SectionHeading>
            <div className="card divide-y divide-line">
              {problem.followUps.map((f, i) => (
                <details key={i} className="group">
                  <summary className="flex cursor-pointer list-none items-start gap-2.5 px-4 py-3 text-[14.5px] text-ink-bright hover:bg-white/[0.02]">
                    <span
                      className="mt-1 shrink-0 text-accent-soft transition-transform group-open:rotate-90"
                      aria-hidden="true"
                    >
                      &rsaquo;
                    </span>
                    <span>
                      <Inline text={f.q} />
                    </span>
                  </summary>
                  <div className="px-4 pb-3.5 pl-11">
                    <RichText text={f.a} className="text-[14px] text-ink" />
                  </div>
                </details>
              ))}
            </div>
          </section>
        )}

        </div>

        <section className="card px-4 py-4">
          <SectionHeading>Rate your recall</SectionHeading>
          <RecallRating id={problem.id} />
        </section>

        <section>
          <SectionHeading>Your notes</SectionHeading>
          <ProblemNotes id={problem.id} />
        </section>

        {related.length > 0 && (
          <section>
            <SectionHeading>Solve next</SectionHeading>
            <ul className="card divide-y divide-line">
              {related.map((r) => (
                <li key={r.slug}>
                  <Link
                    href={`/dsa/${r.category}/${r.slug}`}
                    className="flex items-center gap-3 px-4 py-2.5 transition-colors hover:bg-white/[0.03]"
                  >
                    <span className="font-mono text-[11px] text-ink-dim">
                      #{r.id}
                    </span>
                    <span className="min-w-0 flex-1 truncate text-[14px] text-ink-bright">
                      {r.title}
                    </span>
                    <DifficultyBadge difficulty={r.difficulty} />
                  </Link>
                </li>
              ))}
            </ul>
          </section>
        )}
      </div>

      <nav className="mt-10 flex items-stretch gap-3 border-t border-line pt-5">
        {prev ? (
          <Link
            href={`/dsa/${prev.category}/${prev.slug}`}
            className="card flex-1 px-4 py-3 text-left transition-colors hover:border-accent/40"
          >
            <div className="text-[11px] text-ink-dim">Previous</div>
            <div className="truncate text-[13.5px] text-ink-bright">
              {resolveSlug(prev.slug)?.title}
            </div>
          </Link>
        ) : (
          <div className="flex-1" />
        )}
        {next ? (
          <Link
            href={`/dsa/${next.category}/${next.slug}`}
            className="card flex-1 px-4 py-3 text-right transition-colors hover:border-accent/40"
          >
            <div className="text-[11px] text-ink-dim">Next</div>
            <div className="truncate text-[13.5px] text-ink-bright">
              {resolveSlug(next.slug)?.title}
            </div>
          </Link>
        ) : (
          <div className="flex-1" />
        )}
      </nav>
    </article>
  );
}
