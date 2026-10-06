"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useMemo, useRef, useState } from "react";
import { searchEntries, type SearchEntry } from "@/lib/search";
import { dueIdsFrom, useStore } from "@/lib/store";
import { useNow } from "@/lib/use-now";
import { DifficultyBadge } from "./ui";

const NAV = [
  { href: "/dsa", label: "Guide" },
  { href: "/revise", label: "Revise" },
  { href: "/drills", label: "Drills" },
  { href: "/mock", label: "Mock" },
  { href: "/plan", label: "Plan" },
];

export function HeaderClient({ entries }: { entries: SearchEntry[] }) {
  const pathname = usePathname();
  const { state, hydrated } = useStore();
  const now = useNow();
  const [open, setOpen] = useState(false);

  const solvedCount = useMemo(
    () => Object.values(state.problems).filter((r) => r.solved).length,
    [state.problems],
  );
  const dueCount = useMemo(() => dueIdsFrom(state, now).length, [state, now]);

  // Cmd/Ctrl+K opens search from anywhere.
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setOpen((o) => !o);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  return (
    <>
      <header className="sticky top-0 z-40 border-b border-line bg-canvas/85 backdrop-blur-xl">
        <div className="mx-auto flex h-14 max-w-6xl items-center gap-2 px-4 sm:gap-4">
          <Link
            href="/"
            className="flex shrink-0 items-center gap-2 font-display text-[15px] font-bold text-ink-bright"
          >
            <span aria-hidden="true">&#9671;</span>
            <span className="hidden sm:inline">DSA Mastery</span>
          </Link>

          <nav className="flex min-w-0 flex-1 items-center gap-0.5 overflow-x-auto">
            {NAV.map((item) => {
              const active =
                pathname === item.href || pathname.startsWith(`${item.href}/`);
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`relative shrink-0 rounded-md px-2.5 py-1.5 text-[13px] font-semibold transition-colors ${
                    active
                      ? "bg-accent/12 text-accent-soft"
                      : "text-ink-dim hover:text-ink-bright"
                  }`}
                >
                  {item.label}
                  {item.href === "/revise" && dueCount > 0 && (
                    <span className="ml-1.5 rounded-full bg-accent px-1.5 py-px font-mono text-[10px] text-white">
                      {dueCount}
                    </span>
                  )}
                </Link>
              );
            })}
          </nav>

          <button
            type="button"
            onClick={() => setOpen(true)}
            className="flex shrink-0 items-center gap-2 rounded-md border border-line px-2.5 py-1.5 text-[12px] text-ink-dim transition-colors hover:border-line-strong hover:text-ink"
            aria-label="Search problems"
          >
            <span aria-hidden="true">&#9906;</span>
            <span className="hidden md:inline">Search</span>
            <kbd className="hidden rounded border border-line bg-raised px-1.5 font-mono text-[10px] md:inline">
              Ctrl K
            </kbd>
          </button>

          <div
            className="hidden shrink-0 font-mono text-[12px] text-ink-dim lg:block"
            title="Problems marked solved"
          >
            {hydrated ? (
              <>
                <span className="text-accent-soft">{solvedCount}</span>
                <span>/{entries.length}</span>
              </>
            ) : (
              <span className="opacity-0">0/{entries.length}</span>
            )}
          </div>
        </div>
      </header>

      {open && <SearchPalette entries={entries} onClose={() => setOpen(false)} />}
    </>
  );
}

function SearchPalette({
  entries,
  onClose,
}: {
  entries: SearchEntry[];
  onClose: () => void;
}) {
  const router = useRouter();
  const [query, setQuery] = useState("");
  const [cursor, setCursor] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);
  const results = useMemo(() => searchEntries(entries, query), [entries, query]);

  useEffect(() => inputRef.current?.focus(), []);

  // Clamp rather than reset in an effect — the list shrinks as you type.
  const active = Math.min(cursor, Math.max(0, results.length - 1));

  const go = (entry: SearchEntry) => {
    onClose();
    router.push(`/dsa/${entry.category}/${entry.slug}`);
  };

  const onKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Escape") return onClose();
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setCursor(Math.min(active + 1, results.length - 1));
    }
    if (e.key === "ArrowUp") {
      e.preventDefault();
      setCursor(Math.max(active - 1, 0));
    }
    if (e.key === "Enter" && results[active]) {
      e.preventDefault();
      go(results[active]);
    }
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-start justify-center bg-black/60 p-4 pt-[12vh] backdrop-blur-sm"
      onClick={onClose}
      role="presentation"
    >
      <div
        className="w-full max-w-xl overflow-hidden rounded-card border border-line-strong bg-raised shadow-2xl"
        onClick={(e) => e.stopPropagation()}
        role="dialog"
        aria-modal="true"
        aria-label="Search problems"
      >
        <input
          ref={inputRef}
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            setCursor(0);
          }}
          onKeyDown={onKeyDown}
          placeholder="Search by name, number, pattern or category…"
          className="w-full border-b border-line bg-transparent px-4 py-3.5 text-[15px] text-ink-bright outline-none placeholder:text-ink-dim"
        />
        <div className="max-h-[55vh] overflow-y-auto">
          {query && results.length === 0 && (
            <p className="px-4 py-6 text-center text-[13px] text-ink-dim">
              Nothing matches “{query}”.
            </p>
          )}
          {!query && (
            <p className="px-4 py-6 text-center text-[13px] text-ink-dim">
              Try “two sum”, “239”, “monotonic” or “graphs”.
            </p>
          )}
          {results.map((entry, i) => (
            <button
              key={`${entry.category}/${entry.slug}`}
              type="button"
              onClick={() => go(entry)}
              onMouseEnter={() => setCursor(i)}
              className={`flex w-full items-center gap-3 px-4 py-2.5 text-left transition-colors ${
                i === active ? "bg-accent/12" : "hover:bg-white/[0.03]"
              }`}
            >
              <span className="shrink-0 font-mono text-[11px] text-ink-dim">
                #{entry.id}
              </span>
              <span className="min-w-0 flex-1 truncate text-[14px] text-ink-bright">
                {entry.title}
              </span>
              {entry.pattern && (
                <span className="hidden shrink-0 font-mono text-[11px] text-accent-soft sm:inline">
                  {entry.pattern}
                </span>
              )}
              <DifficultyBadge difficulty={entry.difficulty} />
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
