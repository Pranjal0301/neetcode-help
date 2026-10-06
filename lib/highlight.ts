/**
 * Build-time syntax highlighting.
 *
 * Runs during static generation only, so highlighted code costs the browser
 * nothing — no highlighter, no grammars, no client-side work. One highlighter
 * instance is shared across the whole build.
 */
import { createHighlighter, type Highlighter } from "shiki";
import type { Language } from "./types";

/** Our language ids mapped onto Shiki grammar names. */
const GRAMMAR: Record<Language, string> = {
  python: "python",
  cpp: "cpp",
  java: "java",
  js: "javascript",
};

const THEME = "github-dark-default";

let highlighterPromise: Promise<Highlighter> | null = null;

function getHighlighter(): Promise<Highlighter> {
  highlighterPromise ??= createHighlighter({
    themes: [THEME],
    langs: Object.values(GRAMMAR),
  });
  return highlighterPromise;
}

export type HighlightedCode = {
  lang: Language;
  /** Shiki's <pre><code> markup. Generated at build time from our own content. */
  html: string;
  /** The raw source, for the copy button. */
  raw: string;
};

export async function highlight(
  code: string,
  lang: Language,
): Promise<HighlightedCode> {
  const hl = await getHighlighter();
  const html = hl.codeToHtml(code, {
    lang: GRAMMAR[lang],
    theme: THEME,
    // Let our own CSS own the surface; Shiki only colours the tokens.
    structure: "classic",
  });
  return { lang, html, raw: code };
}

export async function highlightAll(
  code: Partial<Record<Language, string>>,
  order: Language[],
): Promise<HighlightedCode[]> {
  const present = order.filter((l) => typeof code[l] === "string" && code[l]!.trim() !== "");
  return Promise.all(present.map((l) => highlight(code[l]!, l)));
}
