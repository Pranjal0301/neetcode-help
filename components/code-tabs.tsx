"use client";

import { useEffect, useState } from "react";
import type { HighlightedCode } from "@/lib/highlight";
import { LANGUAGES, type Language } from "@/lib/types";
import { useStore } from "@/lib/store";

/**
 * Language tabs over pre-highlighted code. The chosen language is global and
 * persisted, so moving between problems keeps showing the language you work in.
 */
export function CodeTabs({ blocks }: { blocks: HighlightedCode[] }) {
  const { state, setLang } = useStore();
  const available = blocks.map((b) => b.lang);

  // Derived, not mirrored: the stored preference is the source of truth, and
  // falls back to the first available language when this problem lacks it.
  const active: Language = available.includes(state.lang)
    ? state.lang
    : available[0];
  const current = blocks.find((b) => b.lang === active) ?? blocks[0];

  return (
    <div>
      <div className="flex items-center gap-0 border-b border-line">
        {LANGUAGES.filter((l) => available.includes(l.id)).map((l) => (
          <button
            key={l.id}
            type="button"
            onClick={() => setLang(l.id)}
            className={`-mb-px border-b-2 px-3.5 py-2 font-mono text-[12px] font-semibold transition-colors sm:px-4 ${
              active === l.id
                ? "border-accent bg-accent/[0.06] text-accent-soft"
                : "border-transparent text-ink-dim hover:text-ink"
            }`}
          >
            {l.label}
          </button>
        ))}
        <CopyButton text={current.raw} />
      </div>
      <div
        className="codeblock overflow-x-auto rounded-b-card border-t-0 px-4 py-3.5 [&_pre]:!bg-transparent [&_pre]:m-0"
        // Shiki markup generated at build time from content in this repo.
        dangerouslySetInnerHTML={{ __html: current.html }}
      />
    </div>
  );
}

function CopyButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    if (!copied) return;
    const t = setTimeout(() => setCopied(false), 1600);
    return () => clearTimeout(t);
  }, [copied]);

  return (
    <button
      type="button"
      onClick={async () => {
        try {
          await navigator.clipboard.writeText(text);
          setCopied(true);
        } catch {
          // Clipboard blocked (insecure origin or denied permission) — ignore.
        }
      }}
      className="ml-auto mr-1 shrink-0 rounded-md px-2.5 py-1 font-mono text-[11px] text-ink-dim transition-colors hover:text-ink-bright"
    >
      {copied ? "Copied" : "Copy"}
    </button>
  );
}
