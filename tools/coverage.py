#!/usr/bin/env python3
"""
Report content coverage across every category.

Usage:  python tools/coverage.py [category-slug ...]

With no arguments it prints the whole-track table plus a per-category grid, so
the remaining authoring work is always visible. With a slug it lists which
fields each problem in that category is still missing.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content" / "dsa"

# field label -> predicate on a problem dict
CHECKS = {
    "pattern": lambda p: bool(p.get("pattern")),
    "triggers": lambda p: bool(p.get("patternTriggers")),
    "insight": lambda p: bool(p.get("keyInsight")),
    "brute": lambda p: bool(p.get("bruteForce")),
    "approach": lambda p: bool(p.get("approach")),
    "complexity": lambda p: bool((p.get("complexity") or {}).get("time"))
    and bool((p.get("complexity") or {}).get("space")),
    "dryRun": lambda p: bool(p.get("dryRun")),
    "diagram": lambda p: bool(p.get("diagram")),
    "pitfalls": lambda p: bool(p.get("pitfalls")),
    "edges": lambda p: bool(p.get("edgeCases")),
    "followUps": lambda p: bool(p.get("followUps")),
    "related": lambda p: bool(p.get("related")),
    "code4": lambda p: len(p.get("code") or {}) >= 4,
}

# A diagram only earns its place on some problems, so it does not count
# against completeness — it is still reported so the tally stays visible.
OPTIONAL = {"diagram"}

REQUIRED = {k: v for k, v in CHECKS.items() if k not in OPTIONAL}


def load():
    index = json.loads((CONTENT / "_index.json").read_text(encoding="utf-8"))
    return [
        json.loads((CONTENT / f"{e['slug']}.json").read_text(encoding="utf-8"))
        for e in sorted(index, key=lambda e: e["order"])
    ]


def detail(cats, slug):
    cat = next((c for c in cats if c["slug"] == slug), None)
    if not cat:
        print(f"no such category: {slug}", file=sys.stderr)
        return 1
    print(f"\n{cat['title']} ({len(cat['problems'])} problems)\n")
    for p in cat["problems"]:
        missing = [name for name, ok in REQUIRED.items() if not ok(p)]
        status = "complete" if not missing else ", ".join(missing)
        mark = "ok " if not missing else "   "
        print(f"  {mark}#{p['id']:<5} {p['title'][:34]:<34} {status}")
    print()
    return 0


def main(argv):
    cats = load()

    if len(argv) > 1:
        return max(detail(cats, slug) for slug in argv[1:])

    problems = [p for c in cats for p in c["problems"]]
    total = len(problems)

    print(f"\nContent coverage — {total} problems, {len(cats)} categories\n")
    print(f"  {'field':<12}{'have':>6}{'missing':>9}   {'progress':<22}")
    print("  " + "-" * 51)
    for name, ok in CHECKS.items():
        have = sum(1 for p in problems if ok(p))
        label = name if name in REQUIRED else f"{name}*"
        filled = round(20 * have / total) if total else 0
        bar = "#" * filled + "." * (20 - filled)
        print(f"  {label:<12}{have:>6}{total - have:>9}   {bar}")

    # Per-category completion: a problem counts as done when nothing is missing.
    print(f"\n  {'category':<20}{'done':>6}{'of':>5}   missing most")
    print("  " + "-" * 51)
    for c in cats:
        ps = c["problems"]
        done = sum(1 for p in ps if all(ok(p) for ok in REQUIRED.values()))
        gaps = {
            name: sum(1 for p in ps if not ok(p))
            for name, ok in REQUIRED.items()
        }
        worst = sorted((n for n, v in gaps.items() if v), key=lambda n: -gaps[n])[:3]
        note = ", ".join(f"{n}({gaps[n]})" for n in worst) or "nothing"
        flags = []
        if not c.get("concept"):
            flags.append("no concept")
        if not c.get("recognitionTriggers"):
            flags.append("no triggers")
        if not c.get("patternTemplate"):
            flags.append("no template")
        suffix = f"  [{'; '.join(flags)}]" if flags else ""
        print(f"  {c['slug']:<20}{done:>6}{len(ps):>5}   {note}{suffix}")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
