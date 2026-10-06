# Roadmap

Detailed plan for the remaining work. `docs/PLAN.md` holds the original stack
decisions and phase overview; this file is the actionable breakdown of what is
left, with acceptance criteria for each piece.

## Status

| Phase | What | State |
|---|---|---|
| 0 | Extract 150 problems from the legacy HTML into structured content | **done** |
| 1 | Next.js 16 app, 178 statically generated routes, Shiki highlighting | **done** |
| 4 | Revise (SRS), Drills, Mock, Plan, Settings | **done** |
| 2 | Full content for all 150 problems, 12 fields each | **done** |
| 3 | Diagram system — 38 of 150 have one | **38 / ~120 target** |
| 5 | AI/ML track | not started |
| 6 | Vercel deploy + PWA offline | not started |
| — | Known gaps (below) | open |

Content volume today: ~1.26 MB of JSON across 18 category files.

---

## Phase 3 — Diagrams

### Why this is worth doing

The written content carries the explanations, but several categories are
fundamentally spatial. A monotonic stack, a sliding-window deque, an interval
overlap or a graph traversal is understood far faster from a picture than from
a paragraph, and these are exactly the problems that are hardest to hold in
your head under interview pressure.

### Current coverage

```
category             probs  diagrams  missing   primitive needed
arrays-hashing           9         6        3   array (have)
two-pointers             5         5        0   —
sliding-window           6         5        1   deque (new)
stack                    7         3        4   stack (new)
binary-search            7         2        5   array (have)
linked-list             11         4        7   linkedList (have)
trees                   15         4       11   tree (have)
tries                    3         0        3   trie (new)
heap                     7         0        7   heap (new)
backtracking             9         1        8   recursionTree (new)
graphs                  13         2       11   graph (new)
advanced-graphs          6         0        6   graph (new, weighted)
1d-dp                   12         2       10   array / grid (have)
2d-dp                   11         3        8   grid (have)
greedy                   8         0        8   array / timeline (new)
intervals                6         0        6   timeline (new)
math                     8         1        7   grid (have)
bit-manipulation         7         0        7   bits (new)
                       150        38      112
```

Existing primitives: `array` (19 uses), `grid` (12), `linkedList` (3), `tree` (4).

### New primitives to build

Each is a React component in `components/diagrams.tsx`, declared as data in the
content files (`{ "kind": "...", "props": {...}, "caption": "..." }`) so
authoring a diagram stays a JSON edit. All must be theme-aware and legible at
400px wide.

| Kind | Props | Serves |
|---|---|---|
| `stack` | `items`, `top` label, `highlight`, `annotations` | Valid Parentheses, Min Stack, Daily Temperatures, Largest Rectangle, Car Fleet |
| `heap` | `values` (array form), `showIndices`, `highlight`, `swapArrows` | all 7 heap problems; shows the array/tree duality that heaps rest on |
| `graph` | `nodes` (id + position), `edges` (directed?, weight?), `highlight`, `labels` | Clone Graph, Course Schedule, Word Ladder, all 6 advanced-graphs |
| `bits` | `value`, `width` (8/16/32), `highlight`, `labels`, `secondRow` for XOR/AND pairs | all 7 bit-manipulation problems |
| `timeline` | `intervals` (start, end, label), `queries`, `highlight` | all 6 intervals, plus Partition Labels and Gas Station |
| `recursionTree` | `nodes` (label, depth, pruned?) | Subsets, Permutations, N-Queens, Generate Parentheses, Combination Sum |
| `deque` | `items`, `frontLabel`, `backLabel`, `evicted` | Sliding Window Maximum, and the monotonic-deque follow-ups |
| `trie` | `words`, `highlightPath`, `markWordEnds` | all 3 trie problems |
| `stateMachine` | `states`, `transitions` (from, to, label) | Stock with Cooldown, Course Schedule's three DFS states |

### What deliberately will not get a diagram

Pure design and simulation problems gain nothing from one: LRU Cache (the
structure is already described by its two parts), Design Twitter, Time Based
Key-Value Store, Encode and Decode Strings, Plus One, Pow(x,n), Reverse
Integer, Happy Number. Target is therefore **~120 of 150**, not all of them.
`tools/coverage.py` already treats `diagram` as optional for this reason.

### Build order

1. `bits`, `timeline`, `stack` — three self-contained primitives covering 21
   problems across the three categories with zero diagram coverage today.
2. `graph` — the largest single win, 17 problems across graphs and
   advanced-graphs.
3. `heap`, `deque`, `trie` — 17 more.
4. `recursionTree`, `stateMachine` — the two conceptually hardest to draw well.
5. Fill the remaining gaps in categories that already have their primitive
   (trees 11, linked-list 7, 1d-dp 10, 2d-dp 8, binary-search 5, math 7).

### Acceptance

- `python tools/validate_content.py` passes (it already checks diagram kinds
  against the registry read out of `diagrams.tsx`).
- Every diagram renders inside a 400px viewport with no horizontal page scroll.
- Every caption states what the picture *shows*, not what the problem is —
  the existing captions are the quality bar.
- Diagram values are cross-checked against the verified traces, as the Unique
  Paths, LCS and Edit Distance tables already were.

---

## Phase 5 — AI/ML track

### Why it needs its own content model

The DSA model assumes a problem with a LeetCode link, four language solutions
and one optimal approach. An ML topic has none of those: it has a derivation,
a from-scratch implementation, a framework idiom, and a set of conceptual
misconceptions. Forcing it into the `Problem` type would mean half the fields
are null and the important ones do not exist.

So: a parallel model under `content/ai/`, sharing the app shell, the SRS, and
the study-plan machinery, but with its own schema and renderer.

### Proposed schema

```jsonc
{
  "slug": "logistic-regression",
  "title": "Logistic Regression",
  "module": "classical-ml",
  "order": 3,
  "difficulty": "core",            // core | intermediate | advanced
  "tags": ["classification", "gradient-descent", "convex"],

  "intuition": "...",              // plain language, why it exists
  "theory": "...",                 // the maths, stated precisely
  "derivation": [                  // step by step, not asserted
    "Start from the likelihood ...",
    "Take the log ...",
    "Differentiate to get (sigmoid(z) - y) x ..."
  ],
  "fromScratch": "...",            // NumPy, no framework
  "framework": "...",              // sklearn / PyTorch idiom
  "complexity": { "train": "...", "inference": "...", "space": "..." },
  "hyperparameters": [ { "name": "C", "effect": "..." } ],
  "assumptions": ["..."],          // when it is the wrong tool
  "pitfalls": ["..."],
  "misconceptions": [              // the conceptual version of pitfalls
    { "claim": "Logistic regression is a classifier", "correction": "..." }
  ],
  "interviewQuestions": [ { "q": "...", "a": "..." } ],
  "related": ["linear-regression", "svm"],
  "diagram": { "kind": "...", "props": {} }
}
```

### Track structure — 5 modules, ~68 topics

**1. Maths foundations (12)** — matrix calculus, eigendecomposition, SVD,
probability and Bayes, common distributions, expectation and variance, MLE vs
MAP, convexity, gradients and the chain rule, numerical stability, information
theory basics (entropy, KL divergence), sampling.

**2. Classical ML (16)** — linear regression, regularisation (L1/L2 and why
L1 is sparse), logistic regression, decision trees with entropy and gini,
random forests, gradient boosting (and why XGBoost dominates tabular),
SVM and the kernel trick, k-means, hierarchical clustering, PCA, kNN,
Naive Bayes, bias-variance, cross-validation, metrics (precision, recall, F1,
ROC-AUC, PR-AUC and when each misleads), class imbalance.

**3. Deep learning (18)** — the perceptron, backpropagation derived by hand,
activation functions and dead ReLUs, weight initialisation, vanishing and
exploding gradients, batch norm and layer norm, dropout, optimisers (SGD,
momentum, RMSprop, Adam, AdamW), learning-rate schedules, loss functions,
convolution arithmetic, pooling, classic CNN architectures, RNNs, LSTM and
GRU gates, sequence-to-sequence, attention, autoencoders.

**4. Transformers & LLMs (12)** — self-attention from first principles,
scaled dot-product and why the scaling, multi-head attention, positional
encodings, the full transformer block, BPE tokenisation, pretraining
objectives, fine-tuning vs prompting, LoRA and PEFT, RAG, decoding strategies
(greedy, beam, top-k, nucleus), evaluating generative models.

**5. ML system design (10)** — recommendation systems, search ranking, fraud
detection, feature stores, training/serving skew, online vs offline
evaluation, A/B testing, data drift and monitoring, model serving and latency
budgets, the cost of retraining.

### What is reused unchanged

- **SRS** — rating recall on a concept works exactly as it does on a problem;
  the store is keyed by id and does not care what the id refers to.
- **Study plans** — the four tracks extend to a combined DSA + ML schedule.
- **Settings** — export/import covers both tracks for free.

### What needs changing in the app

1. **`CodeTabs` must accept arbitrary tab labels.** It is currently hard-coded
   to the four `Language` values. The ML track needs "From scratch (NumPy)"
   and "PyTorch" / "sklearn" as its two tabs. This is a small generalisation:
   take `{label, code, lang}` triples instead of a `Language` map.
2. **A second renderer** at `app/ai/[module]/[slug]/page.tsx` for the new
   section order (intuition → theory → derivation → code → pitfalls →
   misconceptions → interview questions).
3. **Drills variant** — "given this scenario, which algorithm?" and "which
   metric is appropriate here?", both of which train the same recognition
   skill the DSA drills do.
4. **Navigation** — a track switcher, since the two tracks are peers rather
   than one nested in the other.

### Honest sizing

This is comparable in size to Phase 2. 68 topics with derivations and
from-scratch implementations is a large authoring effort, and it should be
built module by module with each module complete before the next starts —
the same discipline that worked for the 18 DSA categories. Module 2
(Classical ML) is the highest-yield starting point for interviews.

### Acceptance

- Every topic has intuition, theory, at least one derivation step, both code
  variants, pitfalls and interview questions.
- Every from-scratch implementation is **executed** and its output checked
  against the framework version — the equivalent of the verified dry runs,
  and non-negotiable for the same reason.
- A parallel `tools/validate_content.py` check for the AI schema.

---

## Phase 6 — Ship

### Vercel deploy

- Connect the GitHub repo; the build is already `next build` with no special
  configuration and every route is static.
- Preview deploys per branch come free and are useful for reviewing content
  changes before merging.
- No environment variables and no backend, so nothing to configure.

### PWA / offline

The point is studying on a commute without signal. Next 16 ships guidance at
`node_modules/next/dist/docs/01-app/02-guides/offline-support.md` — read it
before writing the service worker rather than assuming the older `next-pwa`
approach still applies.

- `app/manifest.ts` with name, icons, `theme_color: #0c0e1a`, `display: standalone`.
- A service worker precaching the app shell and the category index, then
  caching problem pages on first visit.
- The content is static, so a cache-first strategy with a version bump on
  deploy is sufficient — no revalidation logic needed.
- `localStorage` already survives offline, so progress and the review queue
  keep working with no network.

### Performance budget

- Lighthouse ≥ 95 on performance and accessibility for the home page and a
  problem page.
- First-load JS under 120 KB gzipped. Shiki runs at build time so it
  contributes nothing; the main client cost is the search index, which is
  currently shipped on every page and could be lazy-loaded with the palette.

### Optional

A standalone single-file HTML export, so the whole guide remains openable with
no server — the property the legacy file had. Would be a `tools/export_html.py`
that renders the content to one self-contained file.

### Acceptance

- Installable as a PWA on Android and iOS.
- A problem page opens with the network disabled after one prior visit.
- Lighthouse thresholds met.

---

## Known gaps

### 1. ~~The `core` flag is too permissive~~ — **resolved**

The boolean was replaced with a priority **tier** (1 essential / 2 important /
3 depth), curated across all 150 problems by `tools/assign_tiers.py`, which
also records the inclusion rule. Distribution is 54 / 57 / 39.

Study plans are now driven by **length**: 7, 10, 15, 20, 30, 45, 60 and 90
days, plus unpaced. Each has a problem budget filled tier-by-tier, round-robin
across categories, so every length covers all 18 patterns — a 7-day plan takes
54 problems spanning every category rather than 54 tree problems.

Verified invariants (`.tmp/check-plans.ts`, worth promoting to a real test):
all 18 patterns covered at every length; tiers filled strictly in order;
budgets exact; every selected problem scheduled exactly once; selection is
monotone, so a longer plan is a superset of a shorter one; and each plan spans
exactly its stated number of days with daily loads differing by at most one.

### 2. No tests

`lib/srs.ts`, `lib/plan.ts` and `lib/search.ts` are pure functions with real
logic in them — the SM-2 interval arithmetic, the schedule builder, the search
ranking — and none of it is covered. A small Vitest suite over those three
modules would be cheap and would catch regressions in exactly the code where a
silent change would be hardest to notice.

### 3. Search does not index the new content

`lib/search.ts` ranks on title, id, pattern, category and tags. Now that every
problem has `patternTriggers` and a `keyInsight`, searching for a concept
("monotonic", "bottleneck", "canonical") would be far more useful if those
fields were indexed too. The cost is a larger client payload, which argues for
lazy-loading the index along with the palette.

### 4. Accessibility pass not done

Keyboard focus is handled and the controls have `aria-pressed` and labels, but
there has been no screen-reader pass, no contrast audit against WCAG AA, and
the SVG diagrams have `role="img"` without `aria-label` descriptions.

### 5. `legacy/build.py` is dead weight

Documented in `legacy/README.md` as not runnable (hardcoded Linux paths, and
it mutates `index.html` in place so a second run would double-inject). Kept for
provenance. Worth deleting once nobody wants the history.

---

## Suggested order

1. ~~Re-curate the `core` flag~~ — done; see gap 1.
2. **Phase 3 diagrams**, in the build order above. Highest learning value per
   hour of the remaining work.
3. **Phase 6 ship** — deploy and PWA. Small, and it changes how the thing gets
   used day to day (phone, offline, commute).
4. **Tests** on the three pure modules.
5. **Phase 5 AI/ML track**, module by module, starting with Classical ML.
