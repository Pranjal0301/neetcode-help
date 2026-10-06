/**
 * Spaced repetition scheduling — an SM-2 variant tuned for DSA problems.
 *
 * The thing being recalled is not a fact but an approach: "could I reconstruct
 * the optimal solution unaided?". Intervals are therefore shorter than a
 * vocabulary deck would use, and a lapse sends the problem back to same-day
 * review rather than merely shortening the interval.
 */

export type Rating = "again" | "hard" | "good" | "easy";

export const RATINGS: { id: Rating; label: string; hint: string }[] = [
  { id: "again", label: "Again", hint: "Could not solve it — show me today" },
  { id: "hard", label: "Hard", hint: "Got there, but slowly or with hints" },
  { id: "good", label: "Good", hint: "Solved it cleanly" },
  { id: "easy", label: "Easy", hint: "Instant — space it out further" },
];

export type SrsState = {
  /** Consecutive successful reviews. Reset to 0 on a lapse. */
  reps: number;
  /** Difficulty multiplier, SM-2 style. */
  ease: number;
  /** Current interval in days. */
  intervalDays: number;
  /** Epoch ms when this problem is next due. */
  dueAt: number;
  lastReviewedAt: number;
  lastRating: Rating | null;
  /** Total times this problem has been rated "again". */
  lapses: number;
};

const MIN_EASE = 1.3;
const MAX_EASE = 2.8;
export const DAY_MS = 86_400_000;

export function initialSrs(now = Date.now()): SrsState {
  return {
    reps: 0,
    ease: 2.3,
    intervalDays: 0,
    dueAt: now,
    lastReviewedAt: 0,
    lastRating: null,
    lapses: 0,
  };
}

const clampEase = (e: number) => Math.min(MAX_EASE, Math.max(MIN_EASE, e));

/** The first two successful intervals are fixed; after that ease compounds. */
function nextInterval(state: SrsState, rating: Rating): number {
  const { reps, ease, intervalDays } = state;
  switch (rating) {
    case "again":
      return 0;
    case "hard":
      // Keep it close: nudge forward but never past a few days.
      return reps === 0 ? 1 : Math.max(1, Math.round(intervalDays * 1.2));
    case "good":
      if (reps === 0) return 1;
      if (reps === 1) return 3;
      return Math.max(1, Math.round(intervalDays * ease));
    case "easy":
      if (reps === 0) return 3;
      if (reps === 1) return 6;
      return Math.max(1, Math.round(intervalDays * ease * 1.25));
  }
}

const EASE_DELTA: Record<Rating, number> = {
  again: -0.2,
  hard: -0.15,
  good: 0,
  easy: 0.1,
};

export function review(
  state: SrsState,
  rating: Rating,
  now = Date.now(),
): SrsState {
  const intervalDays = nextInterval(state, rating);
  const lapsed = rating === "again";
  return {
    reps: lapsed ? 0 : state.reps + 1,
    ease: clampEase(state.ease + EASE_DELTA[rating]),
    intervalDays,
    // A lapse comes back in ten minutes, not tomorrow.
    dueAt: lapsed ? now + 10 * 60_000 : now + intervalDays * DAY_MS,
    lastReviewedAt: now,
    lastRating: rating,
    lapses: state.lapses + (lapsed ? 1 : 0),
  };
}

export function isDue(state: SrsState | undefined, now = Date.now()): boolean {
  if (!state || state.lastReviewedAt === 0) return false;
  return state.dueAt <= now;
}

/** Human-readable gap until the next review, for the rating buttons. */
export function formatDue(dueAt: number, now = Date.now()): string {
  const ms = dueAt - now;
  if (ms <= 0) return "now";
  const mins = Math.round(ms / 60_000);
  if (mins < 60) return `${mins}m`;
  const hours = Math.round(ms / 3_600_000);
  if (hours < 24) return `${hours}h`;
  const days = Math.round(ms / DAY_MS);
  if (days < 31) return `${days}d`;
  return `${Math.round(days / 30)}mo`;
}

/** What interval each rating would produce, to label the buttons honestly. */
export function previewIntervals(
  state: SrsState,
  now = Date.now(),
): Record<Rating, string> {
  const out = {} as Record<Rating, string>;
  for (const { id } of RATINGS) {
    out[id] = formatDue(review(state, id, now).dueAt, now);
  }
  return out;
}
