# DSA Mastery

A pattern-first study platform for the NeetCode 150, built for interview prep.

Every problem gets the brute force before the trick, a numbered approach, all four
languages, complexity, a worked trace, the mistakes people actually make, and the
follow-ups an interviewer asks. On top of the content sit four study tools:
spaced repetition, pattern-recognition drills, timed mocks, and dated study plans.

**All 150 problems are written in full** — pattern, triggers, key insight, brute
force, approach, complexity, dry run, pitfalls, edge cases, follow-ups and related
problems. Every dry-run trace was produced by running the algorithm rather than
written by hand, which is how three real content errors were caught.

Still open: the diagram pass (38 of ~120 done), an AI/ML track, and deployment.
See [docs/ROADMAP.md](docs/ROADMAP.md).

## Run it

```bash
npm install
npm run dev          # http://localhost:3000
```

```bash
npm run build        # static export of every page
npm run lint
```

## How it is put together

| Path | What lives there |
|---|---|
| `content/dsa/*.json` | All problem content, one file per NeetCode category. **This is the source of truth.** |
| `app/` | Next.js App Router pages. Every route is statically generated. |
| `components/` | UI. `diagrams.tsx` holds the declarative SVG primitives. |
| `lib/` | Content loading, search, SRS scheduling, study plans, the localStorage store. |
| `tools/extract_content.py` | One-time migration that parsed the legacy HTML into `content/`. Re-runnable, read-only on `legacy/`. |
| `legacy/` | The original single-file guide. Still opens in a browser with no build step. |
| `docs/PLAN.md` | Stack decisions and the phase plan. |

Content is data, not markup, so adding a field across all 150 problems is a JSON
edit rather than surgery on a 958KB HTML file. Code is syntax-highlighted at build
time with Shiki, so the browser downloads no highlighter.

### Your progress

Everything personal — solved marks, review schedule, notes, mock history — is
kept in `localStorage` under `dsa-mastery:v1`. There is no account and no server.
Progress from the legacy guide is migrated automatically when both are served
from the same origin.

Because `localStorage` is per-origin, opening the legacy file through Live Server
(port 5501) and the new app (port 3000) means they do not share state. Use the
export/import on `/settings` to move it across.

## Adding a problem's content

Open the category file, find the problem by `id`, and fill in the fields. Anything
left empty or `null` simply does not render — no placeholders leak to the page.

```jsonc
{
  "id": "217",
  "pattern": "Hash Set",
  "patternTriggers": ["asked whether anything repeats", "membership in O(1)"],
  "keyInsight": "A set answers 'have I seen this?' in O(1)…",
  "bruteForce": { "idea": "…", "time": "O(N^2)", "space": "O(1)", "whyItFails": "…" },
  "approach": ["Create an empty hash set", "…"],
  "complexity": { "time": "O(N)", "space": "O(N)", "note": "…" },
  "dryRun": "Input: [1, 2, 3, 1]\n…",
  "diagram": { "kind": "array", "props": { "values": [1, 2, 3, 1], "highlight": [0, 3] } },
  "pitfalls": ["…"],
  "edgeCases": ["empty array", "single element"],
  "followUps": [{ "q": "What if it will not fit in memory?", "a": "…" }],
  "related": ["two-sum"],
  "core": true
}
```

The home page shows live coverage across every field, so the remaining gaps are
always visible.
