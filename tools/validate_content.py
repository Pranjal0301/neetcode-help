#!/usr/bin/env python3
"""
Validate the content files beyond what the renderer would notice.

Usage:  python tools/validate_content.py

Checks that every `related` slug resolves to a real problem, that no problem
points at itself, that diagram kinds are ones the renderer knows, that every
category has its teaching fields, and that ids and slugs are unique. Exits
non-zero if anything is wrong, so it can gate a commit.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content" / "dsa"
DIAGRAMS = ROOT / "components" / "diagrams.tsx"


def known_diagram_kinds():
    """Read the registry out of diagrams.tsx rather than duplicating the list."""
    text = DIAGRAMS.read_text(encoding="utf-8")
    start = text.find("const REGISTRY")
    if start == -1:
        return None
    end = text.find("};", start)
    body = text[start:end]
    kinds = set()
    for line in body.splitlines():
        line = line.strip()
        if ":" in line and not line.startswith("//") and not line.startswith("const"):
            kinds.add(line.split(":")[0].strip())
    return kinds


def main():
    index = json.loads((CONTENT / "_index.json").read_text(encoding="utf-8"))
    cats = [
        json.loads((CONTENT / f"{e['slug']}.json").read_text(encoding="utf-8"))
        for e in sorted(index, key=lambda e: e["order"])
    ]

    problems = [p for c in cats for p in c["problems"]]
    slugs = {p["slug"] for p in problems}
    errors = []
    warnings = []

    # --- ids and slugs must be unique ---
    for field in ("id", "slug"):
        seen = {}
        for p in problems:
            seen.setdefault(p[field], []).append(p["title"])
        for value, titles in seen.items():
            if len(titles) > 1:
                errors.append(f"duplicate {field} {value!r}: {titles}")

    # --- related slugs must resolve, and not self-reference ---
    for p in problems:
        for rel in p["related"]:
            if rel == p["slug"]:
                errors.append(f"#{p['id']} {p['title']}: related points at itself")
            elif rel not in slugs:
                errors.append(
                    f"#{p['id']} {p['title']}: related slug {rel!r} does not exist"
                )

    # --- diagram kinds must be renderable ---
    kinds = known_diagram_kinds()
    if kinds:
        for p in problems:
            d = p.get("diagram")
            if d and d.get("kind") not in kinds:
                errors.append(
                    f"#{p['id']} {p['title']}: unknown diagram kind "
                    f"{d.get('kind')!r} (known: {sorted(kinds)})"
                )
    else:
        warnings.append("could not read the diagram registry; skipped kind checks")

    # --- every problem needs a study tier ---
    for p in problems:
        if p.get("tier") not in (1, 2, 3):
            errors.append(
                f"#{p['id']} {p['title']}: tier is {p.get('tier')!r}, expected 1, 2 or 3"
            )
        if "core" in p:
            errors.append(f"#{p['id']} {p['title']}: retired `core` field still present")

    # --- complexity should give both bounds ---
    for p in problems:
        cx = p.get("complexity") or {}
        if not cx.get("time") or not cx.get("space"):
            errors.append(f"#{p['id']} {p['title']}: complexity missing time or space")

    # --- category teaching fields ---
    for c in cats:
        if not c.get("concept") or not (c["concept"].get("body") or "").strip():
            errors.append(f"category {c['slug']}: concept body is empty")
        if not c.get("recognitionTriggers"):
            errors.append(f"category {c['slug']}: no recognitionTriggers")
        tmpl = c.get("patternTemplate") or {}
        missing = {"python", "cpp", "java", "js"} - set(tmpl)
        if missing:
            errors.append(
                f"category {c['slug']}: patternTemplate missing {sorted(missing)}"
            )

    # --- report ---
    print(f"checked {len(problems)} problems across {len(cats)} categories")
    for w in warnings:
        print(f"  warning: {w}")
    if errors:
        print(f"\n{len(errors)} problem(s) found:\n")
        for e in errors:
            print(f"  {e}")
        return 1
    print("  all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
