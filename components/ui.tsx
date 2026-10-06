import Link from "next/link";
import type { Difficulty } from "@/lib/types";

const DIFFICULTY_STYLES: Record<Difficulty, string> = {
  easy: "border-easy/30 bg-easy/10 text-easy",
  medium: "border-medium/30 bg-medium/10 text-medium",
  hard: "border-hard/30 bg-hard/10 text-hard",
};

export function DifficultyBadge({
  difficulty,
  className = "",
}: {
  difficulty: Difficulty;
  className?: string;
}) {
  return (
    <span
      className={`inline-flex shrink-0 items-center rounded-full border px-2 py-0.5 text-[11px] font-semibold capitalize ${DIFFICULTY_STYLES[difficulty]} ${className}`}
    >
      {difficulty}
    </span>
  );
}

/** The named technique, e.g. "Monotonic Stack". */
export function PatternChip({ pattern }: { pattern: string }) {
  return (
    <span className="inline-flex items-center gap-1.5 rounded-full border border-accent/30 bg-accent/10 px-2.5 py-0.5 font-mono text-[11px] font-semibold text-accent-soft">
      {pattern}
    </span>
  );
}

export function SectionHeading({
  children,
  id,
  hint,
}: {
  children: React.ReactNode;
  id?: string;
  hint?: string;
}) {
  return (
    <div className="mb-3">
      <h2
        id={id}
        className="font-display text-[13px] font-bold tracking-[0.12em] text-ink-dim uppercase"
      >
        {children}
      </h2>
      {hint && <p className="mt-1 text-[13px] text-ink-dim">{hint}</p>}
    </div>
  );
}

/** Coloured callout used for insights, pitfalls and warnings. */
export function Callout({
  tone = "accent",
  title,
  icon,
  children,
}: {
  tone?: "accent" | "easy" | "medium" | "hard" | "info";
  title?: string;
  icon?: string;
  children: React.ReactNode;
}) {
  const tones = {
    accent: "border-accent/30 bg-accent/[0.07]",
    easy: "border-easy/30 bg-easy/[0.07]",
    medium: "border-medium/30 bg-medium/[0.07]",
    hard: "border-hard/30 bg-hard/[0.07]",
    info: "border-info/30 bg-info/[0.07]",
  } as const;
  const titleTones = {
    accent: "text-accent-soft",
    easy: "text-easy",
    medium: "text-medium",
    hard: "text-hard",
    info: "text-info",
  } as const;

  return (
    <div className={`rounded-card border px-4 py-3.5 ${tones[tone]}`}>
      {title && (
        <div
          className={`mb-1.5 flex items-center gap-2 text-[12px] font-bold tracking-wide uppercase ${titleTones[tone]}`}
        >
          {icon && <span aria-hidden="true">{icon}</span>}
          {title}
        </div>
      )}
      <div className="text-[14.5px] leading-relaxed">{children}</div>
    </div>
  );
}

export function Card({
  children,
  className = "",
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return <div className={`card p-5 ${className}`}>{children}</div>;
}

/** Thin progress bar. `value` and `max` are counts, not percentages. */
export function ProgressBar({
  value,
  max,
  className = "",
}: {
  value: number;
  max: number;
  className?: string;
}) {
  const pct = max > 0 ? Math.min(100, (value / max) * 100) : 0;
  return (
    <div
      className={`h-1.5 overflow-hidden rounded-full bg-line ${className}`}
      role="progressbar"
      aria-valuenow={value}
      aria-valuemin={0}
      aria-valuemax={max}
    >
      <div
        className="h-full rounded-full bg-gradient-to-r from-accent to-accent-soft transition-[width] duration-500"
        style={{ width: `${pct}%` }}
      />
    </div>
  );
}

export function ExternalLink({
  href,
  children,
  className = "",
}: {
  href: string;
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      className={`inline-flex items-center gap-1.5 rounded-md border border-line px-2.5 py-1 text-[12px] font-semibold text-ink-dim transition-colors hover:border-line-strong hover:text-ink-bright ${className}`}
    >
      {children}
    </a>
  );
}

export function NavCard({
  href,
  icon,
  title,
  description,
}: {
  href: string;
  icon: string;
  title: string;
  description: string;
}) {
  return (
    <Link
      href={href}
      className="card group flex flex-col gap-1.5 p-5 transition-colors hover:border-accent/40"
    >
      <span className="text-2xl" aria-hidden="true">
        {icon}
      </span>
      <span className="font-display text-base font-semibold text-ink-bright">
        {title}
      </span>
      <span className="text-[13px] leading-snug text-ink-dim">{description}</span>
    </Link>
  );
}
