# DSA Mastery Platform — Build Plan

Goal: a study platform that gets Pranjal interview-ready for 15–20 LPA SDE roles,
following the NeetCode 150, with rich explanations, real diagrams, and active-recall tooling.

> This file records the original stack decisions and the phase outline.
> For current status and the detailed breakdown of remaining work, see
> [ROADMAP.md](ROADMAP.md). Phases 0, 1, 2 and 4 are complete; 3, 5 and 6 are not.

## Stack decision

| Concern | Choice | Why |
|---|---|---|
| Framework | Next.js 16 (App Router) + TypeScript | Per-problem routes = fast loads + deep links. The 4 study tools are stateful apps; React makes them tractable. |
| Styling | Tailwind CSS v4 + shadcn/ui | Keeps the existing dark indigo aesthetic, but componentised. |
| Content | Typed data files (`content/dsa/*.json`) | Enriching 150 problems x 8 fields becomes a data edit, not HTML surgery. |
| Diagrams | Hand-authored inline SVG React components | Reusable primitives (array, pointers, tree, graph, DP grid, heap) instead of one-off SVG. |
| Persistence | localStorage first, schema-versioned | Zero backend. Progress, SRS state, mock history survive reloads. |
| Hosting | Vercel + PWA offline cache | Revise on phone during commute; works offline once cached. |

The legacy `index.html` stays untouched and working until the new app reaches parity.

## Content schema (per problem)

Fields marked NEW did not exist in the legacy file.

- `id`, `slug`, `title`, `difficulty`, `category`, `order`, `tags`, `links`
- `pattern` — the named technique
- `patternTriggers` (NEW) — the phrases in a problem statement that should make you reach for this pattern
- `keyInsight`
- `bruteForce` (NEW) — naive idea, its complexity, and why it fails
- `approach` — numbered steps
- `code` — python / cpp / java / js
- `complexity` — time, space, note
- `dryRun` — concrete trace
- `diagram` (NEW) — component key + props
- `pitfalls` (NEW) — what people get wrong
- `edgeCases` (NEW) — the inputs an interviewer probes
- `followUps` (NEW) — "what if the array were sorted / streaming / huge?" with answers
- `related` (NEW) — sibling problem slugs
- `core` (NEW) — is this in the must-do subset?

Explanations are written language-neutral; traces use plain pseudocode so all four
language tabs stay first-class.

## Phases

### Phase 0 — Extract & verify
Parse the 958KB `index.html` into `content/dsa/<category>.json`. Emit a coverage report
proving nothing was lost. This de-risks every later phase.

### Phase 1 — New app at parity
Next.js scaffold, category + problem routes, code tabs, search, progress. Same look, real architecture.

### Phase 2 — Content depth, all 150
Fill every gap: pattern tags (62 to 150), approach steps (10 to 150), complexity (69 to 150),
dry runs (16 to 150), plus the five NEW fields on all 150. Delivered category by category,
each one complete before moving on.

### Phase 3 — Diagram system
~60+ diagrams from reusable SVG primitives, theme-aware, legible on mobile.

### Phase 4 — Study tooling
1. **Revision / spaced repetition** — rate recall after each problem, get a due-today queue (SM-2 style).
2. **Pattern drills** — shown a problem statement, pick the pattern. Trains the skill interviews test.
3. **Timed mock mode** — pick N problems, countdown, solutions hidden until time is up.
4. **Study plans** — four selectable tracks (4–6 week sprint / 2–3 month standard / 4–6 month thorough / unpaced), each with day-by-day targets and pace tracking.

### Phase 5 — AI/ML track
Same content model, second track: fundamentals (linear algebra, probability, gradients),
classical ML, deep learning, transformers/LLMs — each with from-scratch NumPy implementations
plus PyTorch idiom, and the same drill/SRS tooling.

### Phase 6 — Ship
Vercel deploy, PWA offline, Lighthouse pass, optional standalone offline HTML export.
