/**
 * Server-side content loading. Reads content/dsa/*.json from disk once per
 * process and caches it, so static generation parses each file a single time.
 */
import fs from "node:fs";
import path from "node:path";
import type { SearchEntry } from "./search";
import type { Category, CategoryIndexEntry, Problem } from "./types";

const CONTENT_DIR = path.join(process.cwd(), "content", "dsa");

let cache: Category[] | null = null;

function readJson<T>(file: string): T {
  return JSON.parse(fs.readFileSync(path.join(CONTENT_DIR, file), "utf-8")) as T;
}

export function getCategories(): Category[] {
  if (cache) return cache;
  const index = readJson<CategoryIndexEntry[]>("_index.json");
  cache = index
    .slice()
    .sort((a, b) => a.order - b.order)
    .map((entry) => readJson<Category>(`${entry.slug}.json`));
  return cache;
}

export function getCategory(slug: string): Category | undefined {
  return getCategories().find((c) => c.slug === slug);
}

export function getAllProblems(): Problem[] {
  return getCategories().flatMap((c) => c.problems);
}

export function getProblem(
  categorySlug: string,
  problemSlug: string,
): Problem | undefined {
  return getCategory(categorySlug)?.problems.find((p) => p.slug === problemSlug);
}

/** Flat ordered list, used for prev/next navigation across the whole track. */
export function getProblemSequence(): { category: string; slug: string }[] {
  return getCategories().flatMap((c) =>
    c.problems.map((p) => ({ category: c.slug, slug: p.slug })),
  );
}

export function getNeighbours(categorySlug: string, problemSlug: string) {
  const seq = getProblemSequence();
  const i = seq.findIndex(
    (p) => p.category === categorySlug && p.slug === problemSlug,
  );
  return {
    prev: i > 0 ? seq[i - 1] : null,
    next: i >= 0 && i < seq.length - 1 ? seq[i + 1] : null,
  };
}

/** Resolve a related-problem slug to something linkable. */
export function resolveSlug(slug: string): Problem | undefined {
  return getAllProblems().find((p) => p.slug === slug);
}

/** Build the client search index. Server only — reads from disk. */
export function getSearchIndex(): SearchEntry[] {
  return getCategories().flatMap((c) =>
    c.problems.map((p) => ({
      id: p.id,
      title: p.title,
      slug: p.slug,
      category: c.slug,
      categoryTitle: c.title,
      categoryIcon: c.icon,
      difficulty: p.difficulty,
      pattern: p.pattern,
      tags: p.tags,
    })),
  );
}

export type CoverageRow = {
  field: string;
  have: number;
  total: number;
};

/** Drives the content-completeness panel, so gaps stay visible while we fill them. */
export function getCoverage(): CoverageRow[] {
  const all = getAllProblems();
  const total = all.length;
  const count = (pred: (p: Problem) => boolean) => all.filter(pred).length;
  return [
    { field: "Pattern", have: count((p) => !!p.pattern), total },
    { field: "Pattern triggers", have: count((p) => p.patternTriggers.length > 0), total },
    { field: "Key insight", have: count((p) => !!p.keyInsight), total },
    { field: "Brute force", have: count((p) => !!p.bruteForce), total },
    { field: "Approach steps", have: count((p) => p.approach.length > 0), total },
    { field: "Complexity", have: count((p) => !!p.complexity?.time && !!p.complexity?.space), total },
    { field: "Dry run", have: count((p) => !!p.dryRun), total },
    { field: "Diagram", have: count((p) => !!p.diagram), total },
    { field: "Pitfalls", have: count((p) => p.pitfalls.length > 0), total },
    { field: "Edge cases", have: count((p) => p.edgeCases.length > 0), total },
    { field: "Follow-ups", have: count((p) => p.followUps.length > 0), total },
    { field: "All 4 languages", have: count((p) => Object.keys(p.code).length >= 4), total },
  ];
}
