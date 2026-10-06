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
  planCoverage,
  startOfDay,
  TIER_LABELS,
  TRACKS,
  type PlanDay,
  type PlanProblem,
} from "@/lib/plan";
import { Callout, DifficultyBadge, ProgressBar, SectionHeading } from "./ui";

export function PlanView({ problems }: { problems: PlanProblem[] }) {
  const { state, hydrated, setPlan, record } = useStore();
  const now = useNow();
  const [showAllDays, setShowAllDays] = useState(false);
  const [showCoverage, setShowCoverage] = useState(false);

  const chosen = state.plan?.track;
  const track = getTrack(chosen ?? "d45");
  const startedAt = state.plan?.startedAt ?? (now ? startOfDay(now) : 0);

  const { days, selected } = useMemo(
    () => buildSchedule(problems, track, startedAt),
    [problems, track, startedAt],
  );
  const coverage = useMemo(
    () => planCoverage(problems, selected),
    [problems, selected],
  );

  const solvedIn = (list: PlanProblem[]) =>
    list.filter((p) => record(p.id).solved).length;

  const dayIndex = hydrated && now ? daysSince(startedAt, now) : 0;
  const today = days[dayIndex];
  const totalSelected = selected.length;
  const totalDone = useMemo(
    () => solvedIn(selected),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [selected, state.problems],
  );

  // Pace: how many the schedule expected by now, against how many are done.
  const expectedByNow = days
    .slice(0, Math.max(0, dayIndex + 1))
    .reduce((n, d) => n + d.problems.length, 0);
  const paceDelta = totalDone - expectedByNow;

  const patternsCovered = coverage.filter((c) => c.selected > 0).length;

  return (
    <div className="space-y-8">
      <section>
        <SectionHeading hint="How long until your interview? The plan picks what fits — switching keeps everything you have already solved.">
          How much time do you have?
        </SectionHeading>
        <div className="flex flex-wrap gap-2">
          {TRACKS.map((t) => {
            const active = hydrated && chosen === t.id;
            return (
              <button
                key={t.id}
                type="button"
                onClick={() => setPlan(t.id)}
                className={`rounded-full border px-4 py-2 text-[13.5px] font-semibold transition-colors ${
                  active
                    ? "border-accent/60 bg-accent/15 text-accent-soft"
                    : "border-line text-ink-dim hover:border-line-strong hover:text-ink"
                }`}
              >
                {t.label}
              </button>
            );
          })}
        </div>
      </section>

      {!hydrated && <p className="text-[13px] text-ink-dim">Loading your plan…</p>}

      {hydrated && !chosen && (
        <Callout tone="info" title="Pick a length above">
          Every option covers all 18 patterns — the shorter ones simply take
          fewer problems from each, starting with the ones you cannot skip.
        </Callout>
      )}

      {hydrated && chosen && (
        <>
          <section className="card p-5">
            <div className="flex flex-wrap items-baseline justify-between gap-x-4 gap-y-1">
              <h2 className="font-display text-[20px] font-bold text-ink-bright">
                {track.label}
              </h2>
              <span className="font-mono text-[12px] text-accent-soft">
                {track.intensity}
              </span>
            </div>
            <p className="mt-2 text-[14px] text-ink-dim">{track.summary}</p>
            <div className="mt-4 flex flex-wrap gap-x-6 gap-y-2 border-t border-line pt-3.5 font-mono text-[12px]">
              <span className="text-ink-dim">
                <span className="text-ink-bright">{totalSelected}</span> problems
              </span>
              <span className="text-ink-dim">
                <span className="text-ink-bright">{patternsCovered}</span> of{" "}
                {coverage.length} patterns
              </span>
              {track.days > 0 && (
                <span className="text-ink-dim">
                  <span className="text-ink-bright">{days.length}</span> days
                  {track.reviewEvery > 0 && " incl. review days"}
                </span>
              )}
            </div>
          </section>

          {track.days === 0 ? (
            <Callout tone="accent" title="Unpaced">
              No dates to fall behind on. Work{" "}
              <Link href="/dsa" className="underline">
                the guide
              </Link>{" "}
              in order and let the{" "}
              <Link href="/revise" className="underline">
                review queue
              </Link>{" "}
              tell you what to come back to.
            </Callout>
          ) : (
            <>
              <section className="card p-5">
                <div className="flex flex-wrap items-end justify-between gap-4">
                  <div>
                    <div className="text-[13px] text-ink-dim">
                      Day {Math.min(dayIndex + 1, days.length)} of {days.length}
                    </div>
                    <div className="font-display text-[26px] leading-tight font-bold text-ink-bright">
                      {totalDone}
                      <span className="text-[17px] text-ink-dim">
                        /{totalSelected} done
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
                  value={totalDone}
                  max={totalSelected}
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
                    <DayRow
                      day={today}
                      solved={solvedIn(today.problems)}
                      highlight
                    />
                  )}
                </section>
              ) : (
                <Callout tone="easy" title="Schedule complete">
                  You have run past the end of this plan. Keep the review queue
                  clear and start doing timed mocks.
                </Callout>
              )}
            </>
          )}

          <section>
            <button
              type="button"
              onClick={() => setShowCoverage((v) => !v)}
              className="mb-3 flex w-full items-baseline justify-between gap-2 text-left"
            >
              <span className="font-display text-[13px] font-bold tracking-[0.12em] text-ink-dim uppercase">
                Coverage
              </span>
              <span className="text-[12px] text-ink-dim">
                {showCoverage ? "hide" : "what this plan includes"}
              </span>
            </button>
            {showCoverage && (
              <div className="card divide-y divide-line">
                {coverage.map((row) => (
                  <div
                    key={row.category}
                    className="flex items-center gap-3 px-4 py-2.5"
                  >
                    <span className="w-36 shrink-0 truncate text-[13px] text-ink">
                      {row.categoryTitle}
                    </span>
                    <ProgressBar
                      value={row.selected}
                      max={row.total}
                      className="flex-1"
                    />
                    <span className="w-12 shrink-0 text-right font-mono text-[11px] text-ink-dim">
                      {row.selected}/{row.total}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </section>

          {track.days > 0 && days.length > 0 && (
            <section>
              <SectionHeading>Schedule</SectionHeading>
              <div className="space-y-2">
                {(showAllDays
                  ? days
                  : days.slice(0, Math.min(days.length, dayIndex + 8))
                ).map((day) => (
                  <DayRow
                    key={day.dayNumber}
                    day={day}
                    solved={solvedIn(day.problems)}
                    past={day.dayNumber < dayIndex + 1}
                    highlight={day.dayNumber === dayIndex + 1}
                  />
                ))}
              </div>
              {!showAllDays && days.length > dayIndex + 8 && (
                <button
                  type="button"
                  onClick={() => setShowAllDays(true)}
                  className="mt-3 w-full rounded-card border border-line py-2.5 text-[13px] text-ink-dim transition-colors hover:border-line-strong hover:text-ink"
                >
                  Show all {days.length} days
                </button>
              )}
            </section>
          )}
        </>
      )}
    </div>
  );
}

const TIER_TONES: Record<number, string> = {
  1: "text-hard",
  2: "text-medium",
  3: "text-ink-dim",
};

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
        highlight
          ? "border-accent/50"
          : past && !complete
            ? "border-medium/30"
            : ""
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
                <span
                  className={`w-3 shrink-0 font-mono text-[11px] ${TIER_TONES[p.tier]}`}
                  title={`${TIER_LABELS[p.tier]} (tier ${p.tier})`}
                >
                  {p.tier}
                </span>
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
