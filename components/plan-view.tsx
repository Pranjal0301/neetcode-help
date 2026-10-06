"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import { useStore } from "@/lib/store";
import { useNow } from "@/lib/use-now";
import {
  buildSchedule,
  daysSince,
  formatDate,
  getTrack,
  startOfDay,
  TRACKS,
  type PlanDay,
  type PlanProblem,
} from "@/lib/plan";
import { Callout, DifficultyBadge, ProgressBar, SectionHeading } from "./ui";

export function PlanView({ problems }: { problems: PlanProblem[] }) {
  const { state, hydrated, setPlan, record } = useStore();
  const now = useNow();
  const [showAll, setShowAll] = useState(false);

  const track = getTrack(state.plan?.track ?? "standard");
  // Before hydration there is no clock, so anchor to the epoch-safe fallback;
  // the schedule is not rendered until `hydrated` anyway.
  const startedAt = state.plan?.startedAt ?? (now ? startOfDay(now) : 0);

  const { days, usedFallback } = useMemo(
    () => buildSchedule(problems, track, startedAt),
    [problems, track, startedAt],
  );

  const solvedCount = (day: PlanDay) =>
    day.problems.filter((p) => record(p.id).solved).length;

  const dayIndex = hydrated && now ? daysSince(startedAt, now) : 0;
  const today = days[dayIndex];
  const totalScoped = days.reduce((n, d) => n + d.problems.length, 0);
  const totalSolvedInScope = useMemo(
    () =>
      days.reduce(
        (n, d) => n + d.problems.filter((p) => record(p.id).solved).length,
        0,
      ),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [days, state.problems],
  );

  // Pace: how many the schedule expected by now, vs how many are done.
  const expectedByNow = days
    .slice(0, Math.max(0, dayIndex + 1))
    .reduce((n, d) => n + d.problems.length, 0);
  const paceDelta = totalSolvedInScope - expectedByNow;

  return (
    <div className="space-y-8">
      <section>
        <SectionHeading hint="Switching tracks keeps your solved problems — only the dates change.">
          Pick a pace
        </SectionHeading>
        <div className="grid gap-3 sm:grid-cols-2">
          {TRACKS.map((t) => {
            const active = hydrated && state.plan?.track === t.id;
            return (
              <button
                key={t.id}
                type="button"
                onClick={() => setPlan(t.id)}
                className={`card p-4 text-left transition-colors ${
                  active
                    ? "border-accent/50 bg-accent/[0.07]"
                    : "hover:border-line-strong"
                }`}
              >
                <div className="flex items-baseline justify-between gap-2">
                  <span className="font-display text-[15px] font-semibold text-ink-bright">
                    {t.label}
                  </span>
                  <span className="font-mono text-[11px] text-ink-dim">
                    {t.days > 0 ? `${t.days} days` : "no end date"}
                  </span>
                </div>
                <p className="mt-1.5 text-[13px] leading-snug text-ink-dim">
                  {t.summary}
                </p>
              </button>
            );
          })}
        </div>
      </section>

      {!hydrated && (
        <p className="text-[13px] text-ink-dim">Loading your plan…</p>
      )}

      {hydrated && !state.plan && (
        <Callout tone="info" title="No track selected">
          Choose a pace above and the schedule appears here, dated from today.
        </Callout>
      )}

      {hydrated && state.plan && track.perDay === 0 && (
        <Callout tone="accent" title="Unpaced">
          No dates to fall behind on. Work{" "}
          <Link href="/dsa" className="underline">
            the guide
          </Link>{" "}
          in order, and let the{" "}
          <Link href="/revise" className="underline">
            review queue
          </Link>{" "}
          tell you what to come back to.
        </Callout>
      )}

      {hydrated && state.plan && days.length > 0 && (
        <>
          {usedFallback && (
            <Callout tone="medium" title="Using a fallback subset">
              The curated must-do list is still being written, so Sprint is
              currently covering every easy and medium problem ({totalScoped} of{" "}
              {problems.length}) and skipping the hard ones.
            </Callout>
          )}

          <section className="card p-5">
            <div className="flex flex-wrap items-end justify-between gap-4">
              <div>
                <div className="text-[13px] text-ink-dim">
                  Day {Math.min(dayIndex + 1, days.length)} of {days.length}
                </div>
                <div className="font-display text-[26px] leading-tight font-bold text-ink-bright">
                  {totalSolvedInScope}
                  <span className="text-[17px] text-ink-dim">
                    /{totalScoped} done
                  </span>
                </div>
              </div>
              <div className="text-right">
                <div className="text-[11px] tracking-wide text-ink-dim uppercase">
                  Pace
                </div>
                <div
                  className={`font-mono text-[15px] ${
                    paceDelta >= 0 ? "text-easy" : "text-medium"
                  }`}
                >
                  {paceDelta === 0
                    ? "on track"
                    : paceDelta > 0
                      ? `${paceDelta} ahead`
                      : `${Math.abs(paceDelta)} behind`}
                </div>
              </div>
            </div>
            <ProgressBar
              value={totalSolvedInScope}
              max={totalScoped}
              className="mt-4"
            />
          </section>

          {today ? (
            <section>
              <SectionHeading>Today</SectionHeading>
              {today.isReviewDay ? (
                <Callout tone="accent" title="Review day" icon="&#8635;">
                  No new problems. Clear your{" "}
                  <Link href="/revise" className="underline">
                    review queue
                  </Link>{" "}
                  and redo anything you rated Again.
                </Callout>
              ) : (
                <DayRow day={today} solved={solvedCount(today)} highlight />
              )}
            </section>
          ) : (
            <Callout tone="easy" title="Schedule complete">
              You have run past the end of this track. Keep the review queue
              clear and start doing timed mocks.
            </Callout>
          )}

          <section>
            <SectionHeading>Schedule</SectionHeading>
            <div className="space-y-2">
              {(showAll ? days : days.slice(0, Math.min(days.length, dayIndex + 8)))
                .map((day) => (
                  <DayRow
                    key={day.dayNumber}
                    day={day}
                    solved={solvedCount(day)}
                    past={day.dayNumber < dayIndex + 1}
                    highlight={day.dayNumber === dayIndex + 1}
                  />
                ))}
            </div>
            {!showAll && days.length > dayIndex + 8 && (
              <button
                type="button"
                onClick={() => setShowAll(true)}
                className="mt-3 w-full rounded-card border border-line py-2.5 text-[13px] text-ink-dim transition-colors hover:border-line-strong hover:text-ink"
              >
                Show all {days.length} days
              </button>
            )}
          </section>
        </>
      )}
    </div>
  );
}

function DayRow({
  day,
  solved,
  past = false,
  highlight = false,
}: {
  day: PlanDay;
  solved: number;
  past?: boolean;
  highlight?: boolean;
}) {
  const complete = day.problems.length > 0 && solved === day.problems.length;
  return (
    <div
      className={`card overflow-hidden p-0 ${
        highlight ? "border-accent/50" : past && !complete ? "border-medium/30" : ""
      }`}
    >
      <div className="flex items-center gap-3 border-b border-line px-4 py-2">
        <span className="font-mono text-[11px] text-ink-dim">
          Day {day.dayNumber}
        </span>
        <span className="text-[12px] text-ink-dim">{formatDate(day.date)}</span>
        {day.isReviewDay && (
          <span className="rounded-full bg-accent/15 px-2 py-0.5 font-mono text-[10px] text-accent-soft">
            review
          </span>
        )}
        <span className="ml-auto font-mono text-[11px]">
          {day.problems.length > 0 && (
            <span className={complete ? "text-easy" : "text-ink-dim"}>
              {solved}/{day.problems.length}
            </span>
          )}
        </span>
      </div>
      {day.problems.length > 0 && (
        <ul className="divide-y divide-line">
          {day.problems.map((p) => (
            <li key={p.id}>
              <Link
                href={`/dsa/${p.category}/${p.slug}`}
                className="flex items-center gap-2.5 px-4 py-2 transition-colors hover:bg-white/[0.03]"
              >
                <span className="w-9 shrink-0 font-mono text-[11px] text-ink-dim">
                  #{p.id}
                </span>
                <span className="min-w-0 flex-1 truncate text-[13.5px] text-ink-bright">
                  {p.title}
                </span>
                <span className="hidden shrink-0 text-[11px] text-ink-dim sm:inline">
                  {p.categoryTitle}
                </span>
                <DifficultyBadge difficulty={p.difficulty} />
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
