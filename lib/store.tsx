"use client";

/**
 * All study state lives in localStorage — no backend, no account.
 * Keyed by LeetCode problem id, which is stable across any content reshuffle.
 *
 * localStorage is an external store, so it is read through useSyncExternalStore
 * rather than copied into component state inside an effect. That keeps render
 * pure, makes the server snapshot explicit, and gives cross-tab sync for free.
 */

import { useSyncExternalStore } from "react";
import type { Language } from "./types";
import type { TrackId } from "./plan";
import { initialSrs, isDue, review, type Rating, type SrsState } from "./srs";

export type { TrackId };

export const STORAGE_KEY = "dsa-mastery:v1";
const LEGACY_CHECKED_KEY = "neetcode_checked";
const LEGACY_LANG_KEY = "neetcode_lang";

export type MockResult = {
  at: number;
  /** Problem ids included in the attempt. */
  problems: string[];
  solved: string[];
  /** Seconds allotted and seconds actually used. */
  allottedSec: number;
  usedSec: number;
};

/** An in-flight mock, persisted so a refresh mid-attempt resumes it. */
export type ActiveMock = {
  ids: string[];
  startedAt: number;
  endsAt: number;
  solved: string[];
};

export type ProblemRecord = {
  solved: boolean;
  solvedAt: number | null;
  srs: SrsState | null;
  notes: string;
  /** Flagged for a second look regardless of SRS schedule. */
  starred: boolean;
};

export type StoreState = {
  version: 1;
  lang: Language;
  problems: Record<string, ProblemRecord>;
  plan: { track: TrackId; startedAt: number } | null;
  mocks: MockResult[];
  activeMock: ActiveMock | null;
  drills: { attempts: number; correct: number };
};

export function emptyRecord(): ProblemRecord {
  return { solved: false, solvedAt: null, srs: null, notes: "", starred: false };
}

function emptyState(): StoreState {
  return {
    version: 1,
    lang: "python",
    problems: {},
    plan: null,
    mocks: [],
    activeMock: null,
    drills: { attempts: 0, correct: 0 },
  };
}

/** Pull forward progress from the legacy single-file guide, if it is on this origin. */
function migrateLegacy(base: StoreState): StoreState {
  try {
    const rawChecked = localStorage.getItem(LEGACY_CHECKED_KEY);
    const rawLang = localStorage.getItem(LEGACY_LANG_KEY);
    if (!rawChecked && !rawLang) return base;

    const next: StoreState = { ...base, problems: { ...base.problems } };
    if (rawChecked) {
      const checked = JSON.parse(rawChecked) as Record<string, boolean>;
      for (const [id, on] of Object.entries(checked)) {
        if (!on || next.problems[id]?.solved) continue;
        next.problems[id] = {
          ...emptyRecord(),
          solved: true,
          solvedAt: Date.now(),
        };
      }
    }
    if (rawLang && ["python", "cpp", "java", "js"].includes(rawLang)) {
      next.lang = rawLang as Language;
    }
    return next;
  } catch {
    return base;
  }
}

function load(): StoreState {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return migrateLegacy(emptyState());
    const parsed = JSON.parse(raw) as StoreState;
    if (parsed.version !== 1) return migrateLegacy(emptyState());
    // Tolerate state written by an older build that lacked newer fields.
    return { ...emptyState(), ...parsed };
  } catch {
    return emptyState();
  }
}

// ---------------------------------------------------------------- the store

/** Stable reference for SSR and the hydration render. */
const SERVER_STATE = emptyState();

let current: StoreState | null = null;
const listeners = new Set<() => void>();

function snapshot(): StoreState {
  current ??= load();
  return current;
}

function serverSnapshot(): StoreState {
  return SERVER_STATE;
}

function emit() {
  for (const l of listeners) l();
}

/** Another tab wrote to localStorage — adopt it. */
function onStorage(e: StorageEvent) {
  if (e.key !== STORAGE_KEY || !e.newValue) return;
  try {
    current = { ...emptyState(), ...(JSON.parse(e.newValue) as StoreState) };
    emit();
  } catch {
    /* ignore a malformed write from another tab */
  }
}

function subscribe(cb: () => void): () => void {
  if (listeners.size === 0) window.addEventListener("storage", onStorage);
  listeners.add(cb);
  return () => {
    listeners.delete(cb);
    if (listeners.size === 0) window.removeEventListener("storage", onStorage);
  };
}

function update(fn: (s: StoreState) => StoreState) {
  current = fn(snapshot());
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(current));
  } catch {
    // Quota exceeded or storage blocked (private window) — the app still works
    // for this session, it just will not remember.
  }
  emit();
}

function mutateProblem(id: string, fn: (r: ProblemRecord) => ProblemRecord) {
  update((s) => ({
    ...s,
    problems: { ...s.problems, [id]: fn(s.problems[id] ?? emptyRecord()) },
  }));
}

/**
 * Actions are module-level and referentially stable, so they need no context
 * and never invalidate a memo.
 */
export const actions = {
  toggleSolved(id: string) {
    mutateProblem(id, (r) => ({
      ...r,
      solved: !r.solved,
      solvedAt: r.solved ? null : Date.now(),
      // First solve enters the review schedule.
      srs: r.solved ? r.srs : (r.srs ?? initialSrs()),
    }));
  },
  /** Idempotent, unlike toggleSolved — used when a mock reports its results. */
  markSolved(id: string) {
    mutateProblem(id, (r) =>
      r.solved
        ? r
        : { ...r, solved: true, solvedAt: Date.now(), srs: r.srs ?? initialSrs() },
    );
  },
  toggleStarred(id: string) {
    mutateProblem(id, (r) => ({ ...r, starred: !r.starred }));
  },
  rate(id: string, rating: Rating) {
    mutateProblem(id, (r) => ({
      ...r,
      solved: rating === "again" ? r.solved : true,
      solvedAt: r.solvedAt ?? Date.now(),
      srs: review(r.srs ?? initialSrs(), rating),
    }));
  },
  setNotes(id: string, notes: string) {
    mutateProblem(id, (r) => ({ ...r, notes }));
  },
  setLang(lang: Language) {
    update((s) => ({ ...s, lang }));
  },
  setPlan(track: TrackId) {
    update((s) => ({
      ...s,
      plan: {
        track,
        // Keep the original start date when re-selecting the same track.
        startedAt: s.plan?.track === track ? s.plan.startedAt : Date.now(),
      },
    }));
  },
  setActiveMock(active: ActiveMock | null) {
    update((s) => ({ ...s, activeMock: active }));
  },
  addMock(result: MockResult) {
    update((s) => ({ ...s, mocks: [result, ...s.mocks].slice(0, 50) }));
  },
  recordDrill(correct: boolean) {
    update((s) => ({
      ...s,
      drills: {
        attempts: s.drills.attempts + 1,
        correct: s.drills.correct + (correct ? 1 : 0),
      },
    }));
  },
  replaceAll(next: StoreState) {
    update(() => ({ ...emptyState(), ...next }));
  },
  reset() {
    update(() => emptyState());
  },
};

// ---------------------------------------------------------------- hooks

const noopSubscribe = () => () => {};

/**
 * False during SSR and the hydration render, true afterwards. Lets components
 * render a neutral placeholder instead of claiming "0 solved" before the real
 * state is readable.
 */
export function useIsHydrated(): boolean {
  return useSyncExternalStore(
    noopSubscribe,
    () => true,
    () => false,
  );
}

export function useStoreState(): StoreState {
  return useSyncExternalStore(subscribe, snapshot, serverSnapshot);
}

export type UseStore = {
  state: StoreState;
  hydrated: boolean;
  record: (id: string) => ProblemRecord;
} & typeof actions;

export function useStore(): UseStore {
  const state = useStoreState();
  const hydrated = useIsHydrated();
  return {
    state,
    hydrated,
    record: (id: string) => state.problems[id] ?? emptyRecord(),
    ...actions,
  };
}

/** Problem ids whose review is due at `now`. */
export function dueIdsFrom(state: StoreState, now: number): string[] {
  if (!now) return [];
  return Object.entries(state.problems)
    .filter(([, r]) => isDue(r.srs ?? undefined, now))
    .sort((a, b) => (a[1].srs?.dueAt ?? 0) - (b[1].srs?.dueAt ?? 0))
    .map(([id]) => id);
}
