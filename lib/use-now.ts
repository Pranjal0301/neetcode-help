"use client";

import { useSyncExternalStore } from "react";

/**
 * The current time, as an external store rather than a render-time
 * `Date.now()` call.
 *
 * Reading the clock during render is impure: the server and client would
 * disagree, so anything derived from it (such as whether a review is due)
 * could render differently on each and break hydration.
 *
 * Values are quantised so `getSnapshot` stays stable between calls within a
 * render pass, and are 0 during SSR and the hydration render — treat 0 as
 * "not known yet" and render something time-independent.
 */

type Clock = {
  subscribe: (onChange: () => void) => () => void;
  getSnapshot: () => number;
};

function makeClock(quantumMs: number): Clock {
  return {
    subscribe(onChange) {
      const timer = setInterval(onChange, quantumMs);
      return () => clearInterval(timer);
    },
    getSnapshot() {
      return Math.floor(Date.now() / quantumMs) * quantumMs;
    },
  };
}

const serverSnapshot = () => 0;

/** Half-minute resolution — enough for "is this review due?". */
const COARSE = makeClock(30_000);

/** One-second resolution, for countdown timers. */
const FINE = makeClock(1_000);

export function useNow(): number {
  return useSyncExternalStore(
    COARSE.subscribe,
    COARSE.getSnapshot,
    serverSnapshot,
  );
}

export function useSecond(): number {
  return useSyncExternalStore(FINE.subscribe, FINE.getSnapshot, serverSnapshot);
}
