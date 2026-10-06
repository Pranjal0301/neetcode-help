"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import { useStore, type ActiveMock, type MockResult } from "@/lib/store";
import { useSecond } from "@/lib/use-now";
import { Callout, DifficultyBadge, ProgressBar, SectionHeading } from "./ui";
import type { Difficulty } from "@/lib/types";

export type MockProblem = {
  id: string;
  title: string;
  slug: string;
  category: string;
  categoryTitle: string;
  difficulty: Difficulty;
  leetcode?: string;
};

const COUNTS = [2, 3, 4];
const MINUTES_PER = [20, 30, 45];
const MIXES = [
  { id: "mixed", label: "Mixed", test: () => true },
  {
    id: "interview",
    label: "Medium + hard",
    test: (d: Difficulty) => d !== "easy",
  },
  { id: "hard", label: "Hard only", test: (d: Difficulty) => d === "hard" },
] as const;

function shuffle<T>(items: T[]): T[] {
  const a = items.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function formatClock(ms: number): string {
  const total = Math.max(0, Math.round(ms / 1000));
  const m = Math.floor(total / 60);
  const s = total % 60;
  return `${m}:${String(s).padStart(2, "0")}`;
}

export function MockView({ problems }: { problems: MockProblem[] }) {
  const { state, hydrated, addMock, markSolved, setActiveMock } = useStore();
  const now = useSecond();
  const [finished, setFinished] = useState<MockResult | null>(null);

  const [count, setCount] = useState(2);
  const [minutesPer, setMinutesPer] = useState(30);
  const [mix, setMix] = useState<(typeof MIXES)[number]["id"]>("interview");

  // The active mock lives in the persisted store, so a refresh resumes it.
  const active = state.activeMock;

  const byId = useMemo(
    () => new Map(problems.map((p) => [p.id, p])),
    [problems],
  );

  const start = () => {
    const mixTest = MIXES.find((m) => m.id === mix)!.test;
    const pool = problems.filter((p) => mixTest(p.difficulty));
    const chosen = shuffle(pool).slice(0, Math.min(count, pool.length));
    if (chosen.length === 0) return;
    const startedAt = Date.now();
    setActiveMock({
      ids: chosen.map((p) => p.id),
      startedAt,
      endsAt: startedAt + chosen.length * minutesPer * 60_000,
      solved: [],
    });
    setFinished(null);
  };

  const finish = (a: ActiveMock) => {
    const result: MockResult = {
      at: a.startedAt,
      problems: a.ids,
      solved: a.solved,
      allottedSec: Math.round((a.endsAt - a.startedAt) / 1000),
      usedSec: Math.round((Date.now() - a.startedAt) / 1000),
    };
    addMock(result);
    // Carry the attempt into overall progress. markSolved is idempotent.
    for (const id of a.solved) markSolved(id);
    setActiveMock(null);
    setFinished(result);
  };

  const toggleOne = (a: ActiveMock, id: string) =>
    setActiveMock({
      ...a,
      solved: a.solved.includes(id)
        ? a.solved.filter((s) => s !== id)
        : [...a.solved, id],
    });

  // ----- setup -----
  if (!active && !finished) {
    return (
      <div className="space-y-6">
        <Callout tone="info" title="How to use this" icon="&#9201;">
          Open each problem on LeetCode and solve it in their editor, against
          the clock, with no help. Solutions here stay hidden until the timer
          stops — that constraint is the whole exercise.
        </Callout>

        <section>
          <SectionHeading>Problems</SectionHeading>
          <Choices
            options={COUNTS.map((c) => ({ value: c, label: String(c) }))}
            value={count}
            onChange={setCount}
          />
        </section>

        <section>
          <SectionHeading>Minutes each</SectionHeading>
          <Choices
            options={MINUTES_PER.map((m) => ({ value: m, label: `${m} min` }))}
            value={minutesPer}
            onChange={setMinutesPer}
          />
        </section>

        <section>
          <SectionHeading>Difficulty</SectionHeading>
          <Choices
            options={MIXES.map((m) => ({ value: m.id, label: m.label }))}
            value={mix}
            onChange={setMix}
          />
        </section>

        <button
          type="button"
          onClick={start}
          className="w-full rounded-card border border-accent/50 bg-accent/15 py-3 font-semibold text-accent-soft transition-colors hover:bg-accent/25"
        >
          Start {count} × {minutesPer} min
        </button>

        {hydrated && state.mocks.length > 0 && (
          <section>
            <SectionHeading>History</SectionHeading>
            <ul className="card divide-y divide-line">
              {state.mocks.slice(0, 8).map((m) => (
                <li
                  key={m.at}
                  className="flex items-center gap-3 px-4 py-2.5 text-[13px]"
                >
                  <span className="text-ink-dim">
                    {new Date(m.at).toLocaleDateString(undefined, {
                      day: "numeric",
                      month: "short",
                    })}
                  </span>
                  <span className="flex-1 text-ink">
                    {m.solved.length}/{m.problems.length} solved
                  </span>
                  <span className="font-mono text-[11px] text-ink-dim">
                    {Math.round(m.usedSec / 60)}m of{" "}
                    {Math.round(m.allottedSec / 60)}m
                  </span>
                </li>
              ))}
            </ul>
          </section>
        )}
      </div>
    );
  }

  // ----- results -----
  if (finished) {
    return (
      <div className="space-y-6">
        <div className="card px-5 py-6 text-center">
          <div className="font-display text-[40px] leading-none font-bold text-ink-bright">
            {finished.solved.length}
            <span className="text-[22px] text-ink-dim">
              /{finished.problems.length}
            </span>
          </div>
          <p className="mt-2 text-[14px] text-ink-dim">
            {Math.round(finished.usedSec / 60)} minutes used of{" "}
            {Math.round(finished.allottedSec / 60)} allotted.
          </p>
        </div>

        <section>
          <SectionHeading>Now read the solutions</SectionHeading>
          <ul className="card divide-y divide-line">
            {finished.problems.map((id) => {
              const p = byId.get(id);
              if (!p) return null;
              const solved = finished.solved.includes(id);
              return (
                <li key={id}>
                  <Link
                    href={`/dsa/${p.category}/${p.slug}`}
                    className="flex items-center gap-2.5 px-4 py-2.5 transition-colors hover:bg-white/[0.03]"
                  >
                    <span
                      className={`shrink-0 text-[13px] ${solved ? "text-easy" : "text-hard"}`}
                      aria-hidden="true"
                    >
                      {solved ? "✓" : "✗"}
                    </span>
                    <span className="min-w-0 flex-1 truncate text-[14px] text-ink-bright">
                      {p.title}
                    </span>
                    <DifficultyBadge difficulty={p.difficulty} />
                  </Link>
                </li>
              );
            })}
          </ul>
        </section>

        <button
          type="button"
          onClick={() => setFinished(null)}
          className="w-full rounded-card border border-line py-3 text-[14px] text-ink-dim transition-colors hover:border-line-strong hover:text-ink"
        >
          New mock
        </button>
      </div>
    );
  }

  // ----- running -----
  const remaining = active!.endsAt - (now || active!.startedAt);
  const elapsed = active!.endsAt - active!.startedAt - remaining;
  const expired = remaining <= 0;
  const chosen = active!.ids
    .map((id) => byId.get(id))
    .filter((p): p is MockProblem => !!p);

  return (
    <div className="space-y-5">
      <div
        className={`card px-5 py-4 text-center ${
          expired
            ? "border-hard/50"
            : remaining < 300_000
              ? "border-medium/50"
              : ""
        }`}
      >
        <div
          className={`font-mono text-[44px] leading-none font-bold tabular-nums ${
            expired
              ? "text-hard"
              : remaining < 300_000
                ? "text-medium"
                : "text-ink-bright"
          }`}
        >
          {formatClock(remaining)}
        </div>
        <p className="mt-1.5 text-[12px] text-ink-dim">
          {expired ? "Time is up — stop coding and finish." : "remaining"}
        </p>
        <ProgressBar
          value={Math.max(0, elapsed)}
          max={active!.endsAt - active!.startedAt}
          className="mt-3"
        />
      </div>

      <ul className="card divide-y divide-line">
        {chosen.map((p) => {
          const done = active!.solved.includes(p.id);
          return (
            <li key={p.id} className="flex items-center gap-3 px-4 py-3">
              <button
                type="button"
                onClick={() => toggleOne(active!, p.id)}
                aria-pressed={done}
                aria-label={done ? `Unmark ${p.title}` : `Mark ${p.title} solved`}
                className={`flex h-6 w-6 shrink-0 items-center justify-center rounded-md border text-[12px] transition-colors ${
                  done
                    ? "border-easy/50 bg-easy/15 text-easy"
                    : "border-line text-transparent hover:border-line-strong hover:text-ink-dim"
                }`}
              >
                &#10003;
              </button>
              <div className="min-w-0 flex-1">
                <div className="truncate text-[14.5px] text-ink-bright">
                  {p.title}
                </div>
                <div className="text-[11.5px] text-ink-dim">
                  {p.categoryTitle}
                </div>
              </div>
              <DifficultyBadge difficulty={p.difficulty} />
              {p.leetcode && (
                <a
                  href={p.leetcode}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="shrink-0 rounded-md border border-line px-2.5 py-1 text-[12px] font-semibold text-ink-dim transition-colors hover:border-accent/50 hover:text-ink-bright"
                >
                  Solve
                </a>
              )}
            </li>
          );
        })}
      </ul>

      <p className="text-center text-[12.5px] text-ink-dim">
        Mark each one as you finish it. Solutions unlock when you end the mock.
      </p>

      <div className="flex gap-3">
        <button
          type="button"
          onClick={() => finish(active!)}
          className="flex-1 rounded-card border border-accent/50 bg-accent/15 py-3 font-semibold text-accent-soft transition-colors hover:bg-accent/25"
        >
          End mock &amp; see solutions
        </button>
        <button
          type="button"
          onClick={() => setActiveMock(null)}
          className="rounded-card border border-line px-4 text-[13px] text-ink-dim transition-colors hover:border-hard/50 hover:text-hard"
          title="Abandon without recording a result"
        >
          Discard
        </button>
      </div>

      {active!.solved.length > 0 && (
        <p className="text-center text-[12px] text-ink-dim">
          Ending will mark {active!.solved.length} problem
          {active!.solved.length === 1 ? "" : "s"} solved in your overall
          progress. Rate your recall on each one afterwards to put it into the
          review rotation.
        </p>
      )}
    </div>
  );
}

function Choices<T extends string | number>({
  options,
  value,
  onChange,
}: {
  options: { value: T; label: string }[];
  value: T;
  onChange: (v: T) => void;
}) {
  return (
    <div className="flex flex-wrap gap-2">
      {options.map((o) => (
        <button
          key={String(o.value)}
          type="button"
          onClick={() => onChange(o.value)}
          className={`rounded-md border px-3.5 py-2 text-[13.5px] font-semibold transition-colors ${
            o.value === value
              ? "border-accent/50 bg-accent/15 text-accent-soft"
              : "border-line text-ink-dim hover:border-line-strong hover:text-ink"
          }`}
        >
          {o.label}
        </button>
      ))}
    </div>
  );
}
