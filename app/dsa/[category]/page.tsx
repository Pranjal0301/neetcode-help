import Link from "next/link";
import { notFound } from "next/navigation";
import type { Metadata } from "next";
import { getCategories, getCategory } from "@/lib/content";
import { highlightAll } from "@/lib/highlight";
import { LANGUAGES } from "@/lib/types";
import { CodeTabs } from "@/components/code-tabs";
import { LegacySvg } from "@/components/diagrams";
import { ProblemList } from "@/components/problem-list";
import { Inline, RichText } from "@/components/rich-text";
import { Callout, SectionHeading } from "@/components/ui";

type Params = { category: string };

export function generateStaticParams(): Params[] {
  return getCategories().map((c) => ({ category: c.slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<Params>;
}): Promise<Metadata> {
  const { category } = await params;
  const c = getCategory(category);
  if (!c) return {};
  return {
    title: c.title,
    description: `${c.problems.length} NeetCode problems on ${c.title}, with the pattern explained first.`,
  };
}

export default async function CategoryPage({
  params,
}: {
  params: Promise<Params>;
}) {
  const { category: slug } = await params;
  const category = getCategory(slug);
  if (!category) notFound();

  const templateBlocks = category.patternTemplate
    ? await highlightAll(
        category.patternTemplate,
        LANGUAGES.map((l) => l.id),
      )
    : [];

  const counts = category.problems.reduce<Record<string, number>>((acc, p) => {
    acc[p.difficulty] = (acc[p.difficulty] ?? 0) + 1;
    return acc;
  }, {});

  return (
    <div className="mx-auto max-w-3xl px-4 py-8 sm:py-10">
      <nav className="mb-5 text-[12px] text-ink-dim">
        <Link href="/dsa" className="hover:text-ink-bright">
          Guide
        </Link>
      </nav>

      <header className="mb-8">
        <div className="flex items-center gap-3">
          <span className="text-3xl" aria-hidden="true">
            {category.icon}
          </span>
          <h1 className="font-display text-[28px] leading-tight font-bold text-ink-bright sm:text-[34px]">
            {category.title}
          </h1>
        </div>
        <p className="mt-2.5 font-mono text-[12px] text-ink-dim">
          {category.problems.length} problems
          {counts.easy ? ` · ${counts.easy} easy` : ""}
          {counts.medium ? ` · ${counts.medium} medium` : ""}
          {counts.hard ? ` · ${counts.hard} hard` : ""}
        </p>
      </header>

      <div className="space-y-8">
        {category.recognitionTriggers.length > 0 && (
          <Callout tone="info" title="How to recognise these problems" icon="&#9906;">
            <ul className="space-y-1.5">
              {category.recognitionTriggers.map((t, i) => (
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

        {category.concept && (
          <section>
            <SectionHeading>{category.concept.heading}</SectionHeading>
            <div className="card space-y-4 px-4 py-4">
              {category.concept.body && (
                <RichText text={category.concept.body} className="text-[14.5px]" />
              )}
              {category.concept.bullets.length > 0 && (
                <ul className="space-y-1.5 text-[14px]">
                  {category.concept.bullets.map((b, i) => (
                    <li key={i} className="flex gap-2">
                      <span
                        className="mt-px shrink-0 text-accent-soft"
                        aria-hidden="true"
                      >
                        &rsaquo;
                      </span>
                      <span>
                        <Inline text={b} />
                      </span>
                    </li>
                  ))}
                </ul>
              )}
            </div>
            {category.concept.legacySvg && (
              <div className="mt-3">
                <LegacySvg svg={category.concept.legacySvg} />
              </div>
            )}
          </section>
        )}

        {templateBlocks.length > 0 && (
          <section>
            <SectionHeading hint="Learn this skeleton once; most problems here are variations on it.">
              Pattern template
            </SectionHeading>
            <div className="card overflow-hidden p-0">
              <CodeTabs blocks={templateBlocks} />
            </div>
          </section>
        )}

        <section>
          <SectionHeading>Problems</SectionHeading>
          <ProblemList
            items={category.problems.map((p) => ({
              id: p.id,
              slug: p.slug,
              title: p.title,
              difficulty: p.difficulty,
              category: category.slug,
              pattern: p.pattern,
              tier: p.tier,
            }))}
          />
        </section>
      </div>
    </div>
  );
}
