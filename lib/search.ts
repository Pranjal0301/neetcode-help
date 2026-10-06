/**
 * Client-safe search. This module must stay free of Node imports — the search
 * palette is a client component, so anything reachable from here ends up in the
 * browser bundle. Building the index lives in lib/content.ts (server only).
 */
import type { Difficulty } from "./types";

/** Slim record shipped to the client for the search palette. */
export type SearchEntry = {
  id: string;
  title: string;
  slug: string;
  category: string;
  categoryTitle: string;
  categoryIcon: string;
  difficulty: Difficulty;
  pattern: string | null;
  tags: string[];
};

/**
 * Ranked substring search. Deliberately simple: an exact problem-number match
 * wins, then title prefix, then title substring, then pattern/tag matches.
 */
export function searchEntries(
  entries: SearchEntry[],
  query: string,
  limit = 12,
): SearchEntry[] {
  const q = query.trim().toLowerCase();
  if (!q) return [];

  const scored: { entry: SearchEntry; score: number }[] = [];
  for (const entry of entries) {
    const title = entry.title.toLowerCase();
    let score = 0;
    if (entry.id === q) score = 100;
    else if (title === q) score = 90;
    else if (title.startsWith(q)) score = 70;
    else if (title.includes(q)) score = 50;
    else if (entry.id.startsWith(q)) score = 45;
    else if (entry.pattern?.toLowerCase().includes(q)) score = 30;
    else if (entry.categoryTitle.toLowerCase().includes(q)) score = 20;
    else if (entry.tags.some((t) => t.includes(q))) score = 15;
    else {
      // Last resort: every query word appears somewhere in the title.
      const words = q.split(/\s+/);
      if (words.length > 1 && words.every((w) => title.includes(w))) score = 10;
    }
    if (score > 0) scored.push({ entry, score });
  }

  return scored
    .sort((a, b) => b.score - a.score || a.entry.title.localeCompare(b.entry.title))
    .slice(0, limit)
    .map((s) => s.entry);
}
