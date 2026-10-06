import { Fragment } from "react";

/**
 * Minimal inline-markdown renderer for content strings.
 *
 * The content files only ever use `**bold**`, `*italic*` and `` `code` ``,
 * so a 20-line tokeniser beats pulling in a markdown library — and because it
 * returns React nodes rather than HTML, there is no dangerouslySetInnerHTML
 * and nothing to sanitise.
 */

const TOKEN = /(\*\*.+?\*\*|`[^`]+`|\*[^*\n]+\*)/g;

function renderInline(text: string, keyPrefix: string): React.ReactNode[] {
  const parts = text.split(TOKEN).filter((p) => p !== "");
  return parts.map((part, i) => {
    const key = `${keyPrefix}-${i}`;
    if (part.startsWith("**") && part.endsWith("**")) {
      return (
        <strong key={key} className="font-semibold text-ink-bright">
          {part.slice(2, -2)}
        </strong>
      );
    }
    if (part.startsWith("`") && part.endsWith("`")) {
      return (
        <code
          key={key}
          className="rounded bg-codebg px-1.5 py-0.5 font-mono text-[0.86em] text-accent-soft"
        >
          {part.slice(1, -1)}
        </code>
      );
    }
    if (part.startsWith("*") && part.endsWith("*") && part.length > 2) {
      return (
        <em key={key} className="italic">
          {part.slice(1, -1)}
        </em>
      );
    }
    return <Fragment key={key}>{part}</Fragment>;
  });
}

/** A single run of inline text — no block wrapper. */
export function Inline({ text }: { text: string }) {
  return <>{renderInline(text, "i")}</>;
}

/** Multi-paragraph text. Blank lines split paragraphs, single newlines break. */
export function RichText({
  text,
  className = "",
}: {
  text: string;
  className?: string;
}) {
  const paragraphs = text.split(/\n{2,}/).filter((p) => p.trim() !== "");
  return (
    <div className={className}>
      {paragraphs.map((para, pi) => (
        <p key={pi} className={pi > 0 ? "mt-3" : undefined}>
          {para.split("\n").map((line, li) => (
            <Fragment key={li}>
              {li > 0 && <br />}
              {renderInline(line, `p${pi}-${li}`)}
            </Fragment>
          ))}
        </p>
      ))}
    </div>
  );
}
