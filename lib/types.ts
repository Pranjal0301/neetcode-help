/** Content model for the DSA track. Mirrors content/dsa/<category>.json. */

export type Difficulty = "easy" | "medium" | "hard";

export type Language = "python" | "cpp" | "java" | "js";

export const LANGUAGES: { id: Language; label: string }[] = [
  { id: "python", label: "Python" },
  { id: "cpp", label: "C++" },
  { id: "java", label: "Java" },
  { id: "js", label: "JavaScript" },
];

export type Complexity = {
  time?: string;
  space?: string;
  /** Why those bounds hold — the part an interviewer actually asks about. */
  note?: string;
};

export type BruteForce = {
  /** The naive idea, in one or two sentences. */
  idea: string;
  time: string;
  space: string;
  /** What specifically makes it too slow, and at what input size it breaks. */
  whyItFails: string;
};

export type FollowUp = {
  q: string;
  a: string;
};

/** A diagram is a named React component plus its props, resolved at render. */
export type DiagramRef = {
  kind: string;
  props?: Record<string, unknown>;
  caption?: string;
};

export type Problem = {
  /** LeetCode problem number. */
  id: string;
  slug: string;
  title: string;
  difficulty: Difficulty;
  category: string;
  /** Position within its category, 1-based. */
  order: number;
  tags: string[];
  links: { leetcode?: string; neetcodeVideo?: string };

  /** The named technique, e.g. "Monotonic Stack". */
  pattern: string | null;
  /** Phrases in a problem statement that should make you reach for this pattern. */
  patternTriggers: string[];
  keyInsight: string | null;
  bruteForce: BruteForce | null;
  /** Numbered walkthrough of the optimal approach. */
  approach: string[];
  code: Partial<Record<Language, string>>;
  complexity: Complexity | null;
  /** A concrete trace against real input. */
  dryRun: string | null;
  diagram: DiagramRef | null;
  pitfalls: string[];
  edgeCases: string[];
  followUps: FollowUp[];
  /** Slugs of sibling problems worth solving next. */
  related: string[];
  /** Part of the must-do subset for a time-boxed sprint. */
  core: boolean;
};

export type CategoryConcept = {
  heading: string;
  body: string;
  bullets: string[];
  /** Inline SVG carried over from the legacy file, pending a redraw. */
  legacySvg: string | null;
};

export type Category = {
  slug: string;
  title: string;
  icon: string;
  order: number;
  concept: CategoryConcept | null;
  /** The reusable code skeleton for this pattern family. */
  patternTemplate: Partial<Record<Language, string>> | null;
  /** How to recognise that a problem belongs to this category. */
  recognitionTriggers: string[];
  problems: Problem[];
};

export type CategoryIndexEntry = {
  slug: string;
  title: string;
  icon: string;
  order: number;
  count: number;
};

export const DIFFICULTY_ORDER: Record<Difficulty, number> = {
  easy: 0,
  medium: 1,
  hard: 2,
};
