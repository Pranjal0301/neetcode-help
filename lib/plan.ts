/**
 * Study tracks. Client-safe — no Node imports.
 *
 * A track turns the guide's problem order into dated daily targets, so "am I on
 * pace?" has an answer. Rest days are deliberate: the review queue needs slack
 * to catch up, and a plan with no slack is a plan you abandon in week two.
 */
import type { Difficulty } from "./types";
import type { TrackId } from "./store";

export type Track = {
  id: TrackId;
  label: string;
  /** Total calendar length. 0 means unpaced. */
  days: number;
  summary: string;
  /** New problems per study day. */
  perDay: number;
  /** Every Nth day is review-only. 0 disables rest days. */
  reviewEvery: number;
  /** Which problems the track covers. */
  scope: "all" | "core";
};

export const TRACKS: Track[] = [
  {
    id: "sprint",
    label: "Sprint",
    days: 42,
    perDay: 3,
    reviewEvery: 7,
    scope: "core",
    summary:
      "4–6 weeks. The highest-yield subset only, three a day, one review day a week. For interviews already on the calendar.",
  },
  {
    id: "standard",
    label: "Standard",
    days: 75,
    perDay: 2,
    reviewEvery: 7,
    scope: "all",
    summary:
      "2–3 months at the classic NeetCode pace. All 150, two a day, with a weekly review day.",
  },
  {
    id: "thorough",
    label: "Thorough",
    days: 150,
    perDay: 1,
    reviewEvery: 6,
    scope: "all",
    summary:
      "4–6 months. One problem a day, done properly — trace it, write it from memory, answer the follow-ups.",
  },
  {
    id: "unpaced",
    label: "Unpaced",
    days: 0,
    perDay: 0,
    reviewEvery: 0,
    scope: "all",
    summary:
      "No calendar. Work the guide in order and let the review queue set the rhythm.",
  },
];

export function getTrack(id: TrackId): Track {
  return TRACKS.find((t) => t.id === id) ?? TRACKS[1];
}

export type PlanProblem = {
  id: string;
  title: string;
  category: string;
  categoryTitle: string;
  slug: string;
  difficulty: Difficulty;
  core: boolean;
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
 * Pick the problems a track covers.
 *
 * `core` scope prefers problems curated as must-do. Until that curation is
 * complete it falls back to easy+medium, which is a defensible sprint rule
 * rather than a silent empty list.
 */
export function scopedProblems(
  all: PlanProblem[],
  scope: Track["scope"],
): { problems: PlanProblem[]; usedFallback: boolean } {
  if (scope === "all") return { problems: all, usedFallback: false };
  const curated = all.filter((p) => p.core);
  if (curated.length > 0) return { problems: curated, usedFallback: false };
  return {
    problems: all.filter((p) => p.difficulty !== "hard"),
    usedFallback: true,
  };
}

/** Lay the scoped problems out across dated days. */
export function buildSchedule(
  all: PlanProblem[],
  track: Track,
  startedAt: number,
): { days: PlanDay[]; usedFallback: boolean } {
  const { problems, usedFallback } = scopedProblems(all, track.scope);
  if (track.perDay === 0) return { days: [], usedFallback };

  const days: PlanDay[] = [];
  const start = startOfDay(startedAt);
  let cursor = 0;
  let dayNumber = 1;

  // Stop when the problems run out, with a guard against a pathological track.
  while (cursor < problems.length && dayNumber <= 1000) {
    const isReviewDay =
      track.reviewEvery > 0 && dayNumber % track.reviewEvery === 0;
    const slice = isReviewDay
      ? []
      : problems.slice(cursor, cursor + track.perDay);
    cursor += slice.length;
    days.push({
      dayNumber,
      date: new Date(start + (dayNumber - 1) * DAY_MS),
      problems: slice,
      isReviewDay,
    });
    dayNumber += 1;
  }

  return { days, usedFallback };
}

export function formatDate(d: Date): string {
  return d.toLocaleDateString(undefined, {
    weekday: "short",
    day: "numeric",
    month: "short",
  });
}
