"use client";

import { useStore } from "@/lib/store";
import { formatDue, initialSrs, previewIntervals, RATINGS } from "@/lib/srs";
import { useNow } from "@/lib/use-now";

/** Solved / starred toggles, shown in the problem header. */
export function SolvedToggle({ id }: { id: string }) {
  const { record, toggleSolved, toggleStarred, hydrated } = useStore();
  const r = record(id);

  return (
    <div className="flex items-center gap-2">
      <button
        type="button"
        onClick={() => toggleSolved(id)}
        aria-pressed={hydrated && r.solved}
        className={`flex h-7 w-7 items-center justify-center rounded-md border text-[13px] transition-colors ${
          hydrated && r.solved
            ? "border-easy/50 bg-easy/15 text-easy"
            : "border-line text-ink-dim hover:border-line-strong hover:text-ink"
        }`}
        title={r.solved ? "Marked solved" : "Mark solved"}
      >
        &#10003;
      </button>
      <button
        type="button"
        onClick={() => toggleStarred(id)}
        aria-pressed={hydrated && r.starred}
        className={`flex h-7 w-7 items-center justify-center rounded-md border text-[13px] transition-colors ${
          hydrated && r.starred
            ? "border-medium/50 bg-medium/15 text-medium"
            : "border-line text-ink-dim hover:border-line-strong hover:text-ink"
        }`}
        title={r.starred ? "Starred for review" : "Star for review"}
      >
        &#9733;
      </button>
    </div>
  );
}

/**
 * Recall rating. Answering this is what schedules the problem for review —
 * the point is to rate honestly *before* re-reading the solution.
 */
export function RecallRating({
  id,
  onRated,
}: {
  id: string;
  onRated?: () => void;
}) {
  const { record, rate } = useStore();
  const now = useNow();
  const r = record(id);

  // `now` is 0 until hydration, so the interval previews stay blank rather
  // than rendering a time the server could not have agreed on.
  const srs = r.srs ?? initialSrs(now);
  const previews = now ? previewIntervals(srs, now) : null;
  const scheduled = now && r.srs && r.srs.lastReviewedAt > 0 ? r.srs : null;

  return (
    <div>
      <div className="mb-2 flex flex-wrap items-baseline justify-between gap-2">
        <span className="text-[13px] text-ink-dim">
          Could you reconstruct this unaided?
        </span>
        {scheduled && (
          <span className="font-mono text-[11px] text-ink-dim">
            next review in {formatDue(scheduled.dueAt, now)} · {scheduled.reps}{" "}
            reps
            {scheduled.lapses > 0 && ` · ${scheduled.lapses} lapses`}
          </span>
        )}
      </div>
      <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">
        {RATINGS.map((rating) => (
          <button
            key={rating.id}
            type="button"
            onClick={() => {
              rate(id, rating.id);
              onRated?.();
            }}
            title={rating.hint}
            className="group flex flex-col items-center gap-0.5 rounded-md border border-line bg-raised px-2 py-2 transition-colors hover:border-accent/50 hover:bg-accent/[0.06]"
          >
            <span className="text-[13px] font-semibold text-ink group-hover:text-ink-bright">
              {rating.label}
            </span>
            <span className="font-mono text-[10px] text-ink-dim">
              {previews ? previews[rating.id] : " "}
            </span>
          </button>
        ))}
      </div>
    </div>
  );
}

/** Freeform scratch notes, saved as you type. */
export function ProblemNotes({ id }: { id: string }) {
  const { record, setNotes, hydrated } = useStore();
  const r = record(id);

  return (
    <textarea
      value={hydrated ? r.notes : ""}
      onChange={(e) => setNotes(id, e.target.value)}
      placeholder="Your own notes — the trick you keep forgetting, a cleaner variable name, a link…"
      rows={3}
      className="w-full resize-y rounded-card border border-line bg-codebg px-3.5 py-2.5 font-mono text-[13px] text-ink outline-none transition-colors placeholder:text-ink-dim/70 focus:border-accent/50"
    />
  );
}
