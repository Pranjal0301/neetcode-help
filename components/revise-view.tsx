"use client";

import Link from "next/link";
import type { StoreState } from "@/lib/store";
import { useStore } from "@/lib/store";
import { DAY_MS, formatDue, isDue } from "@/lib/srs";
import { useNow } from "@/lib/use-now";
import { Callout, DifficultyBadge, SectionHeading } from "./ui";
import type { Difficulty } from "@/lib/types";

export type ReviseItem = {
  id: string;
  title: string;
  slug: string;
  category: string;
  categoryTitle: string;
  difficulty: Difficulty;
  pattern: string | null;
};

/**
 * Split the catalogue into review buckets. Pure, so the React Compiler can
 * memoise the call site without a hand-written useMemo.
 */
function groupForReview(
  items: ReviseItem[],
  records: StoreState["problems"],
  now: number,
) {
  const due: { item: ReviseItem; dueAt: number }[] = [];
  const soon: { item: ReviseItem; dueAt: number }[] = [];
  const starred: ReviseItem[] = [];
  const unscheduled: ReviseItem[] = [];

  for (const item of items) {
    const r = records[item.id];
    if (!r) continue;
    if (r.starred) starred.push(item);
    const srs = r.srs;
    if (!srs || srs.lastReviewedAt === 0) {
      if (r.solved) unscheduled.push(item);
      continue;
    }
    if (isDue(srs, now)) due.push({ item, dueAt: srs.dueAt });
    else if (srs.dueAt - now < 7 * DAY_MS) soon.push({ item, dueAt: srs.dueAt });
  }

  // Longest-overdue first, then soonest-upcoming.
  due.sort((a, b) => a.dueAt - b.dueAt);
  soon.sort((a, b) => a.dueAt - b.dueAt);

  return { due: due.map((d) => d.item), soon, starred, unscheduled };
}

export function ReviseView({ items }: { items: ReviseItem[] }) {
  const { state, hydrated } = useStore();
  const now = useNow();
  const groups = groupForReview(items, state.problems, now);

  if (!hydrated) {
    return <p className="text-[13px] text-ink-dim">Loading your queue…</p>;
  }

  const scheduled = items.filter((i) => {
    const srs = state.problems[i.id]?.srs;
    return srs && srs.lastReviewedAt > 0;
  }).length;

  return (
    <div className="space-y-8">
      <div className="grid grid-cols-3 gap-3">
        <Stat label="Due now" value={groups.due.length} tone="accent" />
        <Stat label="Next 7 days" value={groups.soon.length} />
        <Stat label="In schedule" value={scheduled} />
      </div>

      {groups.due.length > 0 ? (
        <section>
          <SectionHeading hint="Attempt each one before revealing the solution — that is what makes the review count.">
            Due now
          </SectionHeading>
          <Link
            href={`/dsa/${groups.due[0].category}/${groups.due[0].slug}?review=1`}
            className="card mb-3 block border-accent/50 bg-accent/[0.07] px-4 py-3.5 transition-colors hover:border-accent"
          >
            <div className="text-[12px] text-accent-soft">
              Start review session
            </div>
            <div className="font-display text-[16px] font-semibold text-ink-bright">
              {groups.due[0].title}
            </div>
            <div className="mt-0.5 text-[12px] text-ink-dim">
              {groups.due.length} due · solutions stay hidden until you reveal
              them
            </div>
          </Link>
          <QueueList items={groups.due} review />
        </section>
      ) : (
        <Callout tone="easy" title="Queue clear" icon="&#10003;">
          {scheduled === 0 ? (
            <>
              Nothing is scheduled yet. Solve a problem, rate your recall at the
              bottom of its page, and it enters the rotation.
            </>
          ) : (
            <>
              Nothing due right now. {groups.soon.length > 0 && "Next up below."}
            </>
          )}
        </Callout>
      )}

      {groups.soon.length > 0 && (
        <section>
          <SectionHeading>Coming up</SectionHeading>
          <ul className="card divide-y divide-line">
            {groups.soon.map(({ item, dueAt }) => (
              <li key={item.id}>
                <Link
                  href={`/dsa/${item.category}/${item.slug}`}
                  className="flex items-center gap-2.5 px-4 py-2.5 transition-colors hover:bg-white/[0.03]"
                >
                  <span className="w-9 shrink-0 font-mono text-[11px] text-ink-dim">
                    #{item.id}
                  </span>
                  <span className="min-w-0 flex-1 truncate text-[14px] text-ink">
                    {item.title}
                  </span>
                  <span className="shrink-0 font-mono text-[11px] text-ink-dim">
                    in {formatDue(dueAt, now)}
                  </span>
                </Link>
              </li>
            ))}
          </ul>
        </section>
      )}

      {groups.unscheduled.length > 0 && (
        <section>
          <SectionHeading hint="Marked solved but never rated, so they are not in the rotation yet.">
            Not scheduled
          </SectionHeading>
          <QueueList items={groups.unscheduled} review />
        </section>
      )}

      {groups.starred.length > 0 && (
        <section>
          <SectionHeading>Starred</SectionHeading>
          <QueueList items={groups.starred} />
        </section>
      )}
    </div>
  );
}

function Stat({
  label,
  value,
  tone,
}: {
  label: string;
  value: number;
  tone?: "accent";
}) {
  return (
    <div
      className={`card px-4 py-3.5 ${
        tone === "accent" && value > 0 ? "border-accent/40 bg-accent/[0.06]" : ""
      }`}
    >
      <div
        className={`font-display text-[24px] leading-none font-bold ${
          tone === "accent" && value > 0 ? "text-accent-soft" : "text-ink-bright"
        }`}
      >
        {value}
      </div>
      <div className="mt-1 text-[11.5px] text-ink-dim">{label}</div>
    </div>
  );
}

function QueueList({
  items,
  review = false,
}: {
  items: ReviseItem[];
  review?: boolean;
}) {
  return (
    <ul className="card divide-y divide-line">
      {items.map((item) => (
        <li key={item.id}>
          <Link
            href={`/dsa/${item.category}/${item.slug}${review ? "?review=1" : ""}`}
            className="flex items-center gap-2.5 px-4 py-2.5 transition-colors hover:bg-white/[0.03]"
          >
            <span className="w-9 shrink-0 font-mono text-[11px] text-ink-dim">
              #{item.id}
            </span>
            <span className="min-w-0 flex-1 truncate text-[14px] text-ink-bright">
              {item.title}
            </span>
            <span className="hidden shrink-0 text-[11px] text-ink-dim md:inline">
              {item.categoryTitle}
            </span>
            <DifficultyBadge difficulty={item.difficulty} />
          </Link>
        </li>
      ))}
    </ul>
  );
}
