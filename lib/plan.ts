/**
 * Study plans. Client-safe — no Node imports.
 *
 * A plan is defined by how many days you have. From that follows a **problem
 * budget** — how many problems can realistically be done well in that time —
 * and the budget is filled from the priority tiers, round-robin across
 * categories so that even a one-week plan touches all 18 patterns rather than
 * exhausting arrays-and-hashing and never reaching graphs.
 */
import type { Difficulty } from "./types";

export type TrackId =
  | "d7"
  | "d10"
  | "d15"
  | "d20"
  | "d30"
  | "d45"
  | "d60"
  | "d90"
  | "unpaced";

export type Track = {
  id: TrackId;
  label: string;
  /** Calendar length. 0 means unpaced. */
  days: number;
  /**
   * How many problems to cover. 0 means every problem.
   * Sized so the daily load stays achievable — a 7-day plan is a cram at
   * roughly 8 a day, a 90-day plan is under 2.
   */
  problemBudget: number;
  /** Every Nth day is review-only. 0 disables rest days. */
  reviewEvery: number;
  summary: string;
  /** Shown under the duration chips to set expectations honestly. */
  intensity: string;
};

/**
 * Budgets are anchored to the tier boundaries: 54 is exactly tier 1, and 111
 * is exactly tiers 1 and 2. The short plans land on those boundaries on
 * purpose, so "7 days" means "every essential pattern and nothing else".
 */
export const TRACKS: Track[] = [
  {
    id: "d7",
    label: "7 days",
    days: 7,
    problemBudget: 54,
    reviewEvery: 0,
    intensity: "~8 a day",
    summary:
      "Interview this week. Tier 1 only — every pattern represented, nothing optional. Brutal but survivable.",
  },
  {
    id: "d10",
    label: "10 days",
    days: 10,
    problemBudget: 70,
    reviewEvery: 0,
    intensity: "~7 a day",
    summary:
      "All the essentials plus the most valuable reinforcement problems. The shortest plan that does not feel like triage.",
  },
  {
    id: "d15",
    label: "15 days",
    days: 15,
    problemBudget: 90,
    reviewEvery: 0,
    intensity: "~6 a day",
    summary:
      "Essentials plus most of tier 2. Enough room to actually trace the dry runs rather than skim them.",
  },
  {
    id: "d20",
    label: "20 days",
    days: 20,
    problemBudget: 111,
    reviewEvery: 7,
    intensity: "~6 a day",
    summary:
      "Tiers 1 and 2 in full, with a weekly review day. The sweet spot if you have three weeks.",
  },
  {
    id: "d30",
    label: "30 days",
    days: 30,
    problemBudget: 130,
    reviewEvery: 7,
    intensity: "~5 a day",
    summary:
      "Nearly everything, at a pace that leaves time to redo what you got wrong.",
  },
  {
    id: "d45",
    label: "45 days",
    days: 45,
    problemBudget: 0,
    reviewEvery: 7,
    intensity: "~4 a day",
    summary: "All 150, with a weekly review day. Comfortable and complete.",
  },
  {
    id: "d60",
    label: "60 days",
    days: 60,
    problemBudget: 0,
    reviewEvery: 7,
    intensity: "~3 a day",
    summary:
      "All 150 at the classic NeetCode pace. Room for the follow-up questions too.",
  },
  {
    id: "d90",
    label: "90 days",
    days: 90,
    problemBudget: 0,
    reviewEvery: 6,
    intensity: "~2 a day",
    summary:
      "All 150, done properly — trace it, write it from memory, answer the follow-ups.",
  },
  {
    id: "unpaced",
    label: "Unpaced",
    days: 0,
    problemBudget: 0,
    reviewEvery: 0,
    intensity: "no deadline",
    summary:
      "No calendar. Work the guide in order and let the review queue set the rhythm.",
  },
];

/** Plans stored before the day-count rewrite, mapped to their closest match. */
const LEGACY_TRACKS: Record<string, TrackId> = {
  sprint: "d20",
  standard: "d60",
  thorough: "d90",
};

export function getTrack(id: string): Track {
  const mapped = LEGACY_TRACKS[id] ?? id;
  return TRACKS.find((t) => t.id === mapped) ?? TRACKS[5];
}

export type PlanProblem = {
  id: string;
  title: string;
  category: string;
  categoryTitle: string;
  slug: string;
  difficulty: Difficulty;
  /** 1 = essential, 2 = important, 3 = depth. */
  tier: number;
};

export type PlanDay = {
  /** 1-based day number within the track. */
  dayNumber: number;
  date: Date;
  /** Empty on a review-only day. */
  problems: PlanProblem[];
  isReviewDay: boolean;
};

const DAY_MS = 86_400_000;

/** Midnight local time, so "today" means the user's today. */
export function startOfDay(ms: number): number {
  const d = new Date(ms);
  d.setHours(0, 0, 0, 0);
  return d.getTime();
}

export function daysSince(startedAt: number, now = Date.now()): number {
  return Math.floor((startOfDay(now) - startOfDay(startedAt)) / DAY_MS);
}

/**
 * Pick which problems a budget covers.
 *
 * Fills tier 1 first, then 2, then 3 — and within each tier takes one problem
 * from each category in turn before coming back for seconds. That round-robin
 * is what stops a small budget from being swallowed by the largest category:
 * a budget of 30 spans every pattern instead of being 15 tree problems.
 *
 * The result is returned in guide order, so the schedule still reads
 * category by category.
 */
export function selectProblems(
  all: PlanProblem[],
  budget: number,
): PlanProblem[] {
  if (budget <= 0 || budget >= all.length) return all;

  // Group by category, preserving the order the categories appear in.
  const byCategory = new Map<string, PlanProblem[]>();
  for (const p of all) {
    const list = byCategory.get(p.category);
    if (list) list.push(p);
    else byCategory.set(p.category, [p]);
  }

  const chosen = new Set<string>();
  const queues = [...byCategory.values()];

  for (const tier of [1, 2, 3]) {
    // Each category's remaining problems at this tier, in guide order.
    const pools = queues.map((list) =>
      list.filter((p) => p.tier === tier && !chosen.has(p.id)),
    );
    let cursor = 0;
    let progress = true;
    while (chosen.size < budget && progress) {
      progress = false;
      for (let i = 0; i < pools.length && chosen.size < budget; i++) {
        const pool = pools[(i + cursor) % pools.length];
        const next = pool.shift();
        if (next) {
          chosen.add(next.id);
          progress = true;
        }
      }
      cursor += 1;
    }
    if (chosen.size >= budget) break;
  }

  return all.filter((p) => chosen.has(p.id));
}

/** How many problems the selection takes from each category. */
export type CoverageRow = {
  category: string;
  categoryTitle: string;
  selected: number;
  total: number;
};

export function planCoverage(
  all: PlanProblem[],
  selected: PlanProblem[],
): CoverageRow[] {
  const order: string[] = [];
  const totals = new Map<string, { title: string; total: number }>();
  for (const p of all) {
    const existing = totals.get(p.category);
    if (existing) existing.total += 1;
    else {
      totals.set(p.category, { title: p.categoryTitle, total: 1 });
      order.push(p.category);
    }
  }
  const picked = new Map<string, number>();
  for (const p of selected) {
    picked.set(p.category, (picked.get(p.category) ?? 0) + 1);
  }
  return order.map((category) => ({
    category,
    categoryTitle: totals.get(category)!.title,
    selected: picked.get(category) ?? 0,
    total: totals.get(category)!.total,
  }));
}

/** Lay the selected problems out across dated days. */
export function buildSchedule(
  all: PlanProblem[],
  track: Track,
  startedAt: number,
): { days: PlanDay[]; selected: PlanProblem[] } {
  const selected = selectProblems(all, track.problemBudget);
  if (track.days === 0) return { days: [], selected };

  // How many of the track's days actually carry new problems.
  const reviewDays =
    track.reviewEvery > 0 ? Math.floor(track.days / track.reviewEvery) : 0;
  const studyDays = Math.max(1, track.days - reviewDays);

  const days: PlanDay[] = [];
  const start = startOfDay(startedAt);
  let studyIndex = 0;

  // Spread the problems evenly over exactly the track's length rather than
  // taking ceil(n / days) each day — that would compress a 20-day plan into
  // 18 and overstate the daily load. Slicing on proportional boundaries
  // distributes the remainder, so days differ by at most one problem.
  for (let dayNumber = 1; dayNumber <= track.days; dayNumber++) {
    const isReviewDay =
      track.reviewEvery > 0 && dayNumber % track.reviewEvery === 0;
    let problems: PlanProblem[] = [];
    if (!isReviewDay) {
      const from = Math.floor((studyIndex * selected.length) / studyDays);
      const to = Math.floor(((studyIndex + 1) * selected.length) / studyDays);
      problems = selected.slice(from, to);
      studyIndex += 1;
    }
    days.push({
      dayNumber,
      date: new Date(start + (dayNumber - 1) * DAY_MS),
      problems,
      // A day that ends up with nothing to do is a review day in practice.
      isReviewDay: isReviewDay || problems.length === 0,
    });
  }

  return { days, selected };
}

export function formatDate(d: Date): string {
  return d.toLocaleDateString(undefined, {
    weekday: "short",
    day: "numeric",
    month: "short",
  });
}

export const TIER_LABELS: Record<number, string> = {
  1: "Essential",
  2: "Important",
  3: "Depth",
};
