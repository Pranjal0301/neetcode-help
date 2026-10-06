#!/usr/bin/env python3
"""
Print a category's current content compactly, to see what still needs writing.

Usage:  python tools/dump_category.py <slug> [slug ...]
"""
import json
import sys
from pathlib import Path

CONTENT = Path(__file__).resolve().parent.parent / "content" / "dsa"


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1
    for slug in argv[1:]:
        path = CONTENT / f"{slug}.json"
        if not path.exists():
            print(f"no such category: {slug}", file=sys.stderr)
            return 1
        d = json.loads(path.read_text(encoding="utf-8"))
        concept = d.get("concept")
        print(f"\n##### {slug}")
        print(f"  concept: {'present' if concept else 'MISSING'}"
              f"  triggers: {len(d.get('recognitionTriggers') or [])}"
              f"  template: {'yes' if d.get('patternTemplate') else 'no'}")
        if concept:
            body = (concept.get("body") or "").strip()
            print(f"  concept body: {body[:150]!r}{' ...' if len(body) > 150 else ''}")
        for p in d["problems"]:
            print(f"\n  #{p['id']} {p['title']} [{p['difficulty']}] tags={p['tags']}")
            print(f"     pattern  = {p['pattern']!r}")
            print(f"     insight  = {(p['keyInsight'] or '')[:220]!r}")
            print(f"     approach = {len(p['approach'])} steps"
                  f"   complexity = {p['complexity']}"
                  f"   dryRun = {bool(p['dryRun'])}"
                  f"   diagram = {bool(p['diagram'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
