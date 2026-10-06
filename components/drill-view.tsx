"use client";

import Link from "next/link";
import { useCallback, useMemo, useState } from "react";
import { useStore } from "@/lib/store";
import { Callout, DifficultyBadge, ProgressBar, SectionHeading } from "./ui";
import type { Difficulty } from "@/lib/types";

export type DrillProblem = {
  id: string;
  title: string;
  slug: string;
  category: string;
  categoryTitle: string;
  difficulty: Difficulty;
  pattern: string | null;
  leetcode?: string;
};

export type DrillCategory = { slug: string; title: string; icon: string };

const QUESTION_COUNT = 10;
const OPTION_COUNT = 4;

type Question = {
  problem: DrillProblem;
  options: DrillCategory[];
};

function shuffle<T>(items: T[]): T[] {
  const a = items.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function buildQuestions(
  problems: DrillProblem[],
  categories: DrillCategory[],
): Question[] {
  return shuffle(problems)
    .slice(0, QUESTION_COUNT)
    .map((problem) => {
      const distractors = shuffle(
        categories.filter((c) => c.slug !== problem.category),
      ).slice(0, OPTION_COUNT - 1);
      const correct = categories.find((c) => c.slug === problem.category)!;
      return { problem, options: shuffle([correct, ...distractors]) };
    });
}

export function DrillView({
  problems,
  categories,
}: {
  problems: DrillProblem[];
  categories: DrillCategory[];
}) {
  const { state, hydrated, recordDrill } = useStore();
  const [questions, setQuestions] = useState<Question[] | null>(null);
  const [index, setIndex] = useState(0);
  const [picked, setPicked] = useState<string | null>(null);
  const [score, setScore] = useState(0);

  // Questions are randomised, so they are only ever built on the client —
  // generating them during render would mismatch the prerendered HTML.
  const start = useCallback(() => {
    setQuestions(buildQuestions(problems, categories));
    setIndex(0);
    setPicked(null);
    setScore(0);
  }, [problems, categories]);

  const lifetime = useMemo(() => {
    const { attempts, correct } = state.drills;
    return attempts > 0 ? Math.round((correct / attempts) * 100) : null;
  }, [state.drills]);

  if (!questions) {
    return (
      <div className="space-y-6">
        <Callout tone="info" title="What this trains" icon="&#9906;">
          Interviews rarely ask a problem you have seen. They ask one you have
          not, and the whole game is mapping it to a pattern you know in the
          first two minutes. This drills exactly that step — and nothing else.
        </Callout>

        {hydrated && lifetime !== null && (
          <div className="card flex items-center justify-between px-4 py-3.5">
            <span className="text-[13.5px] text-ink-dim">
              Lifetime accuracy over {state.drills.attempts} questions
            </span>
            <span className="font-display text-[20px] font-bold text-accent-soft">
              {lifetime}%
            </span>
          </div>
        )}

        <button
          type="button"
          onClick={start}
          className="w-full rounded-card border border-accent/50 bg-accent/15 py-3 font-semibold text-accent-soft transition-colors hover:bg-accent/25"
        >
          Start {QUESTION_COUNT} questions
        </button>
      </div>
    );
  }

  const finished = index >= questions.length;

  if (finished) {
    const pct = Math.round((score / questions.length) * 100);
    return (
      <div className="space-y-6">
        <div className="card px-5 py-6 text-center">
          <div className="font-display text-[40px] leading-none font-bold text-ink-bright">
            {score}
            <span className="text-[22px] text-ink-dim">/{questions.length}</span>
          </div>
          <p className="mt-2 text-[14px] text-ink-dim">
            {pct >= 90
              ? "Pattern recognition is sharp. Move to timed mocks."
              : pct >= 60
                ? "Decent. The misses below are the categories to reread."
                : "Worth rereading the category pages — the pattern blurbs are the fix."}
          </p>
        </div>

        <section>
          <SectionHeading>Review</SectionHeading>
          <ul className="card divide-y divide-line">
            {questions.map((q) => (
              <li key={q.problem.id}>
                <Link
                  href={`/dsa/${q.problem.category}/${q.problem.slug}`}
                  className="flex items-center gap-2.5 px-4 py-2.5 transition-colors hover:bg-white/[0.03]"
                >
                  <span className="min-w-0 flex-1 truncate text-[14px] text-ink-bright">
                    {q.problem.title}
                  </span>
                  <span className="shrink-0 font-mono text-[11px] text-accent-soft">
                    {q.problem.categoryTitle}
                  </span>
                </Link>
              </li>
            ))}
          </ul>
        </section>

        <button
          type="button"
          onClick={start}
          className="w-full rounded-card border border-accent/50 bg-accent/15 py-3 font-semibold text-accent-soft transition-colors hover:bg-accent/25"
        >
          Go again
        </button>
      </div>
    );
  }

  const q = questions[index];
  const answered = picked !== null;

  const choose = (slug: string) => {
    if (answered) return;
    const correct = slug === q.problem.category;
    setPicked(slug);
    if (correct) setScore((s) => s + 1);
    recordDrill(correct);
  };

  return (
    <div className="space-y-5">
      <div>
        <div className="mb-2 flex items-baseline justify-between font-mono text-[11px] text-ink-dim">
          <span>
            Question {index + 1} of {questions.length}
          </span>
          <span>{score} correct</span>
        </div>
        <ProgressBar value={index} max={questions.length} />
      </div>

      <div className="card px-5 py-5">
        <div className="mb-2 flex items-center gap-2.5">
          <span className="font-mono text-[11px] text-ink-dim">
            #{q.problem.id}
          </span>
          <DifficultyBadge difficulty={q.problem.difficulty} />
        </div>
        <h2 className="font-display text-[21px] leading-tight font-bold text-ink-bright">
          {q.problem.title}
        </h2>
        <p className="mt-2.5 text-[13px] text-ink-dim">
          Which pattern would you reach for?
          {q.problem.leetcode && (
            <>
              {" "}
              <a
                href={q.problem.leetcode}
                target="_blank"
                rel="noopener noreferrer"
                className="underline hover:text-ink"
              >
                Read the statement
              </a>{" "}
              if you do not recognise it.
            </>
          )}
        </p>
      </div>

      <div className="grid gap-2 sm:grid-cols-2">
        {q.options.map((opt) => {
          const isCorrect = opt.slug === q.problem.category;
          const isPicked = opt.slug === picked;
          let tone = "border-line hover:border-line-strong";
          if (answered && isCorrect) tone = "border-easy/60 bg-easy/10";
          else if (answered && isPicked) tone = "border-hard/60 bg-hard/10";
          else if (answered) tone = "border-line opacity-50";
          return (
            <button
              key={opt.slug}
              type="button"
              onClick={() => choose(opt.slug)}
              disabled={answered}
              className={`card flex items-center gap-2.5 p-3.5 text-left transition-colors ${tone}`}
            >
              <span className="text-lg" aria-hidden="true">
                {opt.icon}
              </span>
              <span className="min-w-0 flex-1 text-[14px] text-ink-bright">
                {opt.title}
              </span>
              {answered && isCorrect && (
                <span className="shrink-0 text-easy" aria-hidden="true">
                  &#10003;
                </span>
              )}
            </button>
          );
        })}
      </div>

      {answered && (
        <>
          <Callout
            tone={picked === q.problem.category ? "easy" : "hard"}
            title={picked === q.problem.category ? "Correct" : "Not quite"}
          >
            <strong className="text-ink-bright">{q.problem.title}</strong> is a{" "}
            <strong className="text-ink-bright">
              {q.problem.categoryTitle}
            </strong>{" "}
            problem
            {q.problem.pattern && (
              <>
                , specifically{" "}
                <strong className="text-ink-bright">{q.problem.pattern}</strong>
              </>
            )}
            .{" "}
            <Link
              href={`/dsa/${q.problem.category}/${q.problem.slug}`}
              className="underline hover:text-ink-bright"
            >
              See why
            </Link>
            .
          </Callout>
          <button
            type="button"
            onClick={() => {
              setPicked(null);
              setIndex((i) => i + 1);
            }}
            className="w-full rounded-card border border-accent/50 bg-accent/15 py-3 font-semibold text-accent-soft transition-colors hover:bg-accent/25"
          >
            {index + 1 === questions.length ? "See results" : "Next question"}
          </button>
        </>
      )}
    </div>
  );
}
