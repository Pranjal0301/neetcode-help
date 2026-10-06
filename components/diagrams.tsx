import type { DiagramRef } from "@/lib/types";

/**
 * Diagrams are declared as data in the content files:
 *
 *   { "kind": "array", "props": { "values": [2,7,11], "pointers": [...] } }
 *
 * so authoring one is a JSON edit, not hand-written SVG. Each primitive below
 * is theme-aware and sized in a viewBox so it scales down to phone width.
 */

const INK = "#c8cdd8";
const DIM = "#6b7280";
const BRIGHT = "#eef0f6";
const ACCENT = "#7c5cfc";
const ACCENT_SOFT = "#a78bfa";
const CELL = "#161a30";
const CELL_LINE = "#ffffff1f";

// ---------- array ----------

type Pointer = { at: number; label: string; tone?: "accent" | "info" | "hard" };

type ArrayProps = {
  values: (string | number)[];
  /** Indices to fill with the accent colour. */
  highlight?: number[];
  /** Labelled carets under specific indices. */
  pointers?: Pointer[];
  /** Show 0-based indices above each cell. */
  showIndices?: boolean;
  /** Inclusive index range drawn as a bracket, for window problems. */
  window?: { from: number; to: number; label?: string };
};

const POINTER_TONES = { accent: ACCENT_SOFT, info: "#60a5fa", hard: "#f87171" };

function ArrayDiagram({
  values,
  highlight = [],
  pointers = [],
  showIndices = true,
  window: win,
}: ArrayProps) {
  const w = 54;
  const h = 40;
  const gap = 6;
  const padX = 10;
  const topPad = showIndices ? 20 : 6;
  const winPad = win ? 22 : 0;
  const bottomPad = pointers.length > 0 ? 34 : 8;
  const width = padX * 2 + values.length * (w + gap) - gap;
  const height = topPad + winPad + h + bottomPad;
  const x = (i: number) => padX + i * (w + gap);

  return (
    <svg
      viewBox={`0 0 ${width} ${height}`}
      width={width}
      height={height}
      className="h-auto max-w-full"
      role="img"
    >
      {showIndices &&
        values.map((_, i) => (
          <text
            key={`i${i}`}
            x={x(i) + w / 2}
            y={13}
            textAnchor="middle"
            fontSize="11"
            fontFamily="monospace"
            fill={DIM}
          >
            {i}
          </text>
        ))}

      {win && (
        <>
          <rect
            x={x(win.from) - 3}
            y={topPad + winPad - 6}
            width={x(win.to) + w - x(win.from) + 6}
            height={h + 12}
            rx="8"
            fill={`${ACCENT}1a`}
            stroke={ACCENT}
            strokeDasharray="4 3"
          />
          {win.label && (
            <text
              x={x(win.from) + (x(win.to) + w - x(win.from)) / 2}
              y={topPad + 8}
              textAnchor="middle"
              fontSize="11"
              fontFamily="monospace"
              fill={ACCENT_SOFT}
            >
              {win.label}
            </text>
          )}
        </>
      )}

      {values.map((v, i) => {
        const on = highlight.includes(i);
        return (
          <g key={i}>
            <rect
              x={x(i)}
              y={topPad + winPad}
              width={w}
              height={h}
              rx="6"
              fill={on ? `${ACCENT}33` : CELL}
              stroke={on ? ACCENT : CELL_LINE}
            />
            <text
              x={x(i) + w / 2}
              y={topPad + winPad + h / 2 + 5}
              textAnchor="middle"
              fontSize="14"
              fontFamily="monospace"
              fill={on ? BRIGHT : INK}
            >
              {v}
            </text>
          </g>
        );
      })}

      {pointers.map((p, i) => {
        const colour = POINTER_TONES[p.tone ?? "accent"];
        const cx = x(p.at) + w / 2;
        const top = topPad + winPad + h;
        // Stagger labels so two pointers on the same index stay readable.
        const dy = i % 2 === 0 ? 0 : 13;
        return (
          <g key={`p${i}`}>
            <path
              d={`M${cx} ${top + 3} l-4 7 h8 z`}
              fill={colour}
              transform={`translate(0 ${dy})`}
            />
            <text
              x={cx}
              y={top + 24 + dy}
              textAnchor="middle"
              fontSize="11"
              fontFamily="monospace"
              fontWeight="600"
              fill={colour}
            >
              {p.label}
            </text>
          </g>
        );
      })}
    </svg>
  );
}

// ---------- 2D grid / DP table ----------

type GridProps = {
  cells: (string | number | null)[][];
  rowLabels?: string[];
  colLabels?: string[];
  /** [row, col] pairs to accent. */
  highlight?: [number, number][];
  /** Arrows showing which cells a value is derived from. */
  from?: { to: [number, number]; sources: [number, number][] };
};

function GridDiagram({
  cells,
  rowLabels,
  colLabels,
  highlight = [],
  from,
}: GridProps) {
  const s = 42;
  const gap = 4;
  const labelX = rowLabels ? 34 : 8;
  const labelY = colLabels ? 22 : 8;
  const cols = Math.max(...cells.map((r) => r.length));
  const width = labelX + cols * (s + gap) - gap + 8;
  const height = labelY + cells.length * (s + gap) - gap + 8;
  const cx = (c: number) => labelX + c * (s + gap);
  const cy = (r: number) => labelY + r * (s + gap);
  const isOn = (r: number, c: number) =>
    highlight.some(([hr, hc]) => hr === r && hc === c);

  return (
    <svg
      viewBox={`0 0 ${width} ${height}`}
      width={width}
      height={height}
      className="h-auto max-w-full"
      role="img"
    >
      <defs>
        <marker
          id="dgrid-arrow"
          markerWidth="7"
          markerHeight="6"
          refX="6"
          refY="3"
          orient="auto"
        >
          <path d="M0,0 L7,3 L0,6 z" fill={ACCENT_SOFT} />
        </marker>
      </defs>

      {colLabels?.map((l, c) => (
        <text
          key={`c${c}`}
          x={cx(c) + s / 2}
          y={14}
          textAnchor="middle"
          fontSize="11"
          fontFamily="monospace"
          fill={DIM}
        >
          {l}
        </text>
      ))}
      {rowLabels?.map((l, r) => (
        <text
          key={`r${r}`}
          x={labelX - 8}
          y={cy(r) + s / 2 + 4}
          textAnchor="end"
          fontSize="11"
          fontFamily="monospace"
          fill={DIM}
        >
          {l}
        </text>
      ))}

      {cells.map((row, r) =>
        row.map((v, c) => {
          const on = isOn(r, c);
          return (
            <g key={`${r}-${c}`}>
              <rect
                x={cx(c)}
                y={cy(r)}
                width={s}
                height={s}
                rx="5"
                fill={on ? `${ACCENT}33` : CELL}
                stroke={on ? ACCENT : CELL_LINE}
              />
              {v !== null && (
                <text
                  x={cx(c) + s / 2}
                  y={cy(r) + s / 2 + 4}
                  textAnchor="middle"
                  fontSize="13"
                  fontFamily="monospace"
                  fill={on ? BRIGHT : INK}
                >
                  {v}
                </text>
              )}
            </g>
          );
        }),
      )}

      {from?.sources.map((src, i) => (
        <line
          key={`a${i}`}
          x1={cx(src[1]) + s / 2}
          y1={cy(src[0]) + s / 2}
          x2={cx(from.to[1]) + s / 2}
          y2={cy(from.to[0]) + s / 2}
          stroke={ACCENT_SOFT}
          strokeWidth="1.5"
          markerEnd="url(#dgrid-arrow)"
          opacity="0.75"
        />
      ))}
    </svg>
  );
}

// ---------- linked list ----------

type LinkedListProps = {
  nodes: (string | number)[];
  /** Labelled pointers above specific node indices. */
  pointers?: Pointer[];
  /** Draw the tail pointing back to this index, for cycle problems. */
  cycleTo?: number;
  nullTerminated?: boolean;
};

function LinkedListDiagram({
  nodes,
  pointers = [],
  cycleTo,
  nullTerminated = true,
}: LinkedListProps) {
  const w = 46;
  const h = 36;
  const gap = 34;
  const padX = 10;
  const topPad = pointers.length > 0 ? 28 : 8;
  const bottomPad = cycleTo !== undefined ? 34 : 8;
  const tail = nullTerminated ? 40 : 0;
  const width = padX * 2 + nodes.length * (w + gap) - gap + tail;
  const height = topPad + h + bottomPad;
  const x = (i: number) => padX + i * (w + gap);
  const midY = topPad + h / 2;

  return (
    <svg
      viewBox={`0 0 ${width} ${height}`}
      width={width}
      height={height}
      className="h-auto max-w-full"
      role="img"
    >
      <defs>
        <marker
          id="dll-arrow"
          markerWidth="7"
          markerHeight="6"
          refX="6"
          refY="3"
          orient="auto"
        >
          <path d="M0,0 L7,3 L0,6 z" fill={DIM} />
        </marker>
      </defs>

      {nodes.map((v, i) => (
        <g key={i}>
          <rect
            x={x(i)}
            y={topPad}
            width={w}
            height={h}
            rx="6"
            fill={CELL}
            stroke={CELL_LINE}
          />
          <text
            x={x(i) + w / 2}
            y={midY + 5}
            textAnchor="middle"
            fontSize="14"
            fontFamily="monospace"
            fill={INK}
          >
            {v}
          </text>
          {i < nodes.length - 1 && (
            <line
              x1={x(i) + w + 4}
              y1={midY}
              x2={x(i + 1) - 5}
              y2={midY}
              stroke={DIM}
              strokeWidth="1.5"
              markerEnd="url(#dll-arrow)"
            />
          )}
        </g>
      ))}

      {nullTerminated && cycleTo === undefined && (
        <>
          <line
            x1={x(nodes.length - 1) + w + 4}
            y1={midY}
            x2={x(nodes.length - 1) + w + 22}
            y2={midY}
            stroke={DIM}
            strokeWidth="1.5"
            markerEnd="url(#dll-arrow)"
          />
          <text
            x={x(nodes.length - 1) + w + 28}
            y={midY + 4}
            fontSize="11"
            fontFamily="monospace"
            fill={DIM}
          >
            null
          </text>
        </>
      )}

      {cycleTo !== undefined && (
        <path
          d={`M${x(nodes.length - 1) + w / 2} ${topPad + h + 2}
              L${x(nodes.length - 1) + w / 2} ${topPad + h + 18}
              L${x(cycleTo) + w / 2} ${topPad + h + 18}
              L${x(cycleTo) + w / 2} ${topPad + h + 3}`}
          fill="none"
          stroke={POINTER_TONES.hard}
          strokeWidth="1.5"
          markerEnd="url(#dll-arrow)"
        />
      )}

      {pointers.map((p, i) => {
        const colour = POINTER_TONES[p.tone ?? "accent"];
        const px = x(p.at) + w / 2;
        return (
          <g key={`p${i}`}>
            <text
              x={px}
              y={12}
              textAnchor="middle"
              fontSize="11"
              fontFamily="monospace"
              fontWeight="600"
              fill={colour}
            >
              {p.label}
            </text>
            <path d={`M${px} ${topPad - 3} l-4 -7 h8 z`} fill={colour} />
          </g>
        );
      })}
    </svg>
  );
}

// ---------- binary tree ----------

type TreeProps = {
  /** Level-order values; null for an absent child. */
  levels: (string | number | null)[];
  highlight?: number[];
  caption?: string;
};

function TreeDiagram({ levels, highlight = [] }: TreeProps) {
  const depth = Math.ceil(Math.log2(levels.length + 1));
  const r = 17;
  const vGap = 62;
  const width = Math.max(260, 2 ** (depth - 1) * 62);
  const height = depth * vGap + 20;

  // Standard heap layout: node i sits at depth floor(log2(i+1)).
  const pos = (i: number) => {
    const level = Math.floor(Math.log2(i + 1));
    const indexInLevel = i - (2 ** level - 1);
    const slots = 2 ** level;
    return {
      x: (width / slots) * (indexInLevel + 0.5),
      y: 24 + level * vGap,
    };
  };

  return (
    <svg
      viewBox={`0 0 ${width} ${height}`}
      width={width}
      height={height}
      className="h-auto max-w-full"
      role="img"
    >
      {levels.map((v, i) => {
        if (v === null || v === undefined) return null;
        const p = pos(i);
        return [1, 2].map((off) => {
          const child = 2 * i + off;
          if (levels[child] === null || levels[child] === undefined) return null;
          const c = pos(child);
          return (
            <line
              key={`e${i}-${child}`}
              x1={p.x}
              y1={p.y + r}
              x2={c.x}
              y2={c.y - r}
              stroke={CELL_LINE}
              strokeWidth="1.5"
            />
          );
        });
      })}

      {levels.map((v, i) => {
        if (v === null || v === undefined) return null;
        const p = pos(i);
        const on = highlight.includes(i);
        return (
          <g key={`n${i}`}>
            <circle
              cx={p.x}
              cy={p.y}
              r={r}
              fill={on ? `${ACCENT}33` : CELL}
              stroke={on ? ACCENT : CELL_LINE}
              strokeWidth="1.5"
            />
            <text
              x={p.x}
              y={p.y + 5}
              textAnchor="middle"
              fontSize="13"
              fontFamily="monospace"
              fill={on ? BRIGHT : INK}
            >
              {v}
            </text>
          </g>
        );
      })}
    </svg>
  );
}

// ---------- registry ----------

/* eslint-disable @typescript-eslint/no-explicit-any */
const REGISTRY: Record<string, (props: any) => React.ReactElement | null> = {
  array: ArrayDiagram,
  grid: GridDiagram,
  linkedList: LinkedListDiagram,
  tree: TreeDiagram,
};
/* eslint-enable @typescript-eslint/no-explicit-any */

export function Diagram({ diagram }: { diagram: DiagramRef }) {
  const Component = REGISTRY[diagram.kind];
  if (!Component) {
    // An unknown kind is a content bug, not a crash. Say so in development
    // and render nothing in production.
    if (process.env.NODE_ENV !== "production") {
      return (
        <div className="card border-hard/40 px-4 py-3 text-[13px] text-hard">
          Unknown diagram kind “{diagram.kind}”.
        </div>
      );
    }
    return null;
  }
  return (
    <figure className="card overflow-x-auto px-4 py-4">
      <Component {...(diagram.props ?? {})} />
      {diagram.caption && (
        <figcaption className="mt-3 border-t border-line pt-2.5 text-[13px] text-ink-dim">
          {diagram.caption}
        </figcaption>
      )}
    </figure>
  );
}

/**
 * Inline SVG carried over verbatim from the legacy guide. Content is authored in
 * this repo, so there is no untrusted-input path here; these get replaced by
 * declarative diagrams as each category is reworked.
 */
export function LegacySvg({ svg }: { svg: string }) {
  return (
    <figure
      className="card overflow-x-auto px-4 py-4 [&_svg]:h-auto [&_svg]:max-w-full"
      dangerouslySetInnerHTML={{ __html: svg }}
    />
  );
}
