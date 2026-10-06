"use client";

import Link from "next/link";

/**
 * Review mode hides the worked solution so a review is a real recall attempt
 * rather than a re-read.
 *
 * It is driven by a `data-review` attribute set on <html> by a pre-paint script
 * (see app/layout.tsx) and applied in CSS, not by React state. That matters:
 * reading `?review=1` after hydration would flash the full solution on screen
 * for a moment first, which defeats the whole point. This way the problem pages
 * also stay statically generated.
 */

/** Clears review mode for the rest of this page view. */
export function RevealButton() {
  return (
    <button
      type="button"
      onClick={() => {
        document.documentElement.removeAttribute("data-review");
      }}
      className="mt-4 rounded-md border border-accent/50 bg-accent/15 px-4 py-2 text-[13.5px] font-semibold text-accent-soft transition-colors hover:bg-accent/25"
    >
      Reveal solution
    </button>
  );
}

/** The "try it first" card. Server-rendered; CSS shows it only in review mode. */
export function RevealPrompt() {
  return (
    <div className="review-only card border-accent/40 bg-accent/[0.05] px-5 py-6 text-center">
      <p className="font-display text-[16px] font-semibold text-ink-bright">
        Try it first
      </p>
      <p className="mx-auto mt-1.5 max-w-sm text-[13.5px] text-ink-dim">
        Write the solution on paper or in an editor. Reveal only once you are
        stuck or done — then rate your recall honestly.
      </p>
      <RevealButton />
    </div>
  );
}

/** Banner with a route back to the queue. Visible in review mode only. */
export function ReviewBanner() {
  return (
    <div className="review-only mb-5 flex flex-wrap items-center justify-between gap-2 rounded-card border border-accent/40 bg-accent/[0.07] px-4 py-2.5">
      <span className="text-[13px] text-accent-soft">Review session</span>
      <Link
        href="/revise"
        className="text-[12.5px] text-ink-dim underline hover:text-ink-bright"
      >
        Back to queue
      </Link>
    </div>
  );
}
