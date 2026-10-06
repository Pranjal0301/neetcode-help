"use client";

import Link from "next/link";
import { useMemo } from "react";
import { dueIdsFrom, useStore } from "@/lib/store";
import { isDue } from "@/lib/srs";
import { useNow } from "@/lib/use-now";
import { ProgressBar } from "./ui";

export type DashboardProps = {
  totalProblems: number;
  /** Every problem id, in guide order, for "continue where you left off". */
  sequence: { id: string; title: string; category: string; slug: string }[];
};

export function Dashboard({ totalProblems, sequence }: DashboardProps) {
  const { state, hydrated } = useStore();
  const now = useNow();

  const stats = useMemo(() => {
    const solved = sequence.filter((p) => state.problems[p.id]?.solved);
    const starred = sequence.filter((p) => state.problems[p.id]?.starred);
    const due = sequence.filter((p) =>
      isDue(state.problems[p.id]?.srs ?? undefined, now),
    );
    const next = sequence.find((p) => !state.problems[p.id]?.solved);
    return { solved, starred, due, next };
  }, [sequence, state.problems, now]);

  const dueCount = useMemo(() => dueIdsFrom(state, now).length, [state, now]);
  const accuracy =
    state.drills.attempts > 0
      ? Math.round((state.drills.correct / state.drills.attempts) * 100)
      : null;

  return (
    <div className="space-y-4">
      <div className="card p-5">
        <div className="flex items-end justify-between gap-4">
          <div>
            <div className="font-display text-[34px] leading-none font-bold text-ink-bright">
              {hydrated ? stats.solved.length : "—"}
              <span className="text-[20px] text-ink-dim">/{totalProblems}</span>
            </div>
            <div className="mt-1 text-[13px] text-ink-dim">problems solved</div>
          </div>
          <div className="text-right font-mono text-[12px] text-ink-dim">
            {hydrated && stats.starred.length > 0 && (
              <div>{stats.starred.length} starred</div>
            )}
            {accuracy !== null && <div>{accuracy}% drill accuracy</div>}
          </div>
        </div>
        <ProgressBar
          value={hydrated ? stats.solved.length : 0}
          max={totalProblems}
          className="mt-4"
        />
      </div>

      <div className="grid gap-3 sm:grid-cols-2">
        <Link
          href="/revise"
          className={`card flex flex-col justify-between gap-3 p-5 transition-colors hover:border-accent/40 ${
            dueCount > 0 ? "border-accent/40 bg-accent/[0.06]" : ""
          }`}
        >
          <div>
            <div className="font-display text-[15px] font-semibold text-ink-bright">
              Review queue
            </div>
            <p className="mt-1 text-[13px] text-ink-dim">
              {!hydrated
                ? "Checking what is due…"
                : dueCount > 0
                  ? `${dueCount} problem${dueCount === 1 ? "" : "s"} due — right before you would forget them.`
                  : "Nothing due. Solve something and rate your recall to start the schedule."}
            </p>
          </div>
          {dueCount > 0 && (
            <span className="font-display text-[28px] leading-none font-bold text-accent-soft">
              {dueCount}
            </span>
          )}
        </Link>

        <Link
          href={
            hydrated && stats.next
              ? `/dsa/${stats.next.category}/${stats.next.slug}`
              : "/dsa"
          }
          className="card flex flex-col justify-between gap-3 p-5 transition-colors hover:border-accent/40"
        >
          <div>
            <div className="font-display text-[15px] font-semibold text-ink-bright">
              {hydrated && stats.solved.length > 0 ? "Continue" : "Start here"}
            </div>
            <p className="mt-1 text-[13px] text-ink-dim">
              {hydrated && stats.next
                ? stats.next.title
                : "Work the guide in order — the patterns build on each other."}
            </p>
          </div>
        </Link>
      </div>
    </div>
  );
}
