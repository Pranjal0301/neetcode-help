#!/usr/bin/env python3
"""
Merge an enrichment patch into content/dsa/<category>.json.

Usage:  python tools/patch_content.py <patch.json> [more.json ...]

A patch looks like:

    {
      "category": "arrays-hashing",
      "category_fields": { "recognitionTriggers": [...], "patternTemplate": {...} },
      "problems": {
        "217": { "pattern": "Hash Set", "pitfalls": ["..."] }
      }
    }

Only the keys present in the patch are replaced; everything else — notably the
four language solutions — is left exactly as it was. Unknown field names and
unknown problem ids are hard errors, so a typo cannot silently write a field
that nothing renders.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content" / "dsa"

PROBLEM_FIELDS = {
    "id", "slug", "title", "difficulty", "category", "order", "tags", "links",
    "pattern", "patternTriggers", "keyInsight", "bruteForce", "approach",
    "code", "complexity", "dryRun", "diagram", "pitfalls", "edgeCases",
    "followUps", "related", "core",
}

CATEGORY_FIELDS = {
    "slug", "title", "icon", "order", "concept", "patternTemplate",
    "recognitionTriggers", "problems",
}

LANGS = {"python", "cpp", "java", "js"}


def fail(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def check_shape(pid, field, value):
    """Catch structural mistakes the renderer would silently swallow."""
    if field in ("patternTriggers", "approach", "pitfalls", "edgeCases", "related"):
        if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
            fail(f"{pid}.{field} must be a list of strings")
    elif field == "followUps":
        if not isinstance(value, list):
            fail(f"{pid}.followUps must be a list")
        for item in value:
            if not isinstance(item, dict) or set(item) != {"q", "a"}:
                fail(f"{pid}.followUps entries need exactly the keys q and a")
    elif field == "bruteForce" and value is not None:
        need = {"idea", "time", "space", "whyItFails"}
        if not isinstance(value, dict) or set(value) != need:
            fail(f"{pid}.bruteForce needs exactly the keys {sorted(need)}")
    elif field == "complexity" and value is not None:
        if not isinstance(value, dict) or not set(value) <= {"time", "space", "note"}:
            fail(f"{pid}.complexity allows only time, space and note")
        if "time" not in value or "space" not in value:
            fail(f"{pid}.complexity should give both time and space")
    elif field == "diagram" and value is not None:
        if not isinstance(value, dict) or "kind" not in value:
            fail(f"{pid}.diagram needs a kind")
        if not set(value) <= {"kind", "props", "caption"}:
            fail(f"{pid}.diagram allows only kind, props and caption")
    elif field == "code":
        if not isinstance(value, dict) or not set(value) <= LANGS:
            fail(f"{pid}.code keys must be a subset of {sorted(LANGS)}")
    elif field == "core":
        if not isinstance(value, bool):
            fail(f"{pid}.core must be true or false")
    elif field in ("keyInsight", "dryRun", "pattern") and value is not None:
        if not isinstance(value, str):
            fail(f"{pid}.{field} must be a string or null")


def apply_patch(path):
    patch = json.loads(path.read_text(encoding="utf-8"))
    cslug = patch.get("category")
    if not cslug:
        fail(f"{path.name}: missing \"category\"")

    target = CONTENT / f"{cslug}.json"
    if not target.exists():
        fail(f"{path.name}: no such category file: {target.name}")

    data = json.loads(target.read_text(encoding="utf-8"))
    by_id = {p["id"]: p for p in data["problems"]}

    changed_fields = 0
    touched_problems = set()

    for field, value in (patch.get("category_fields") or {}).items():
        if field not in CATEGORY_FIELDS:
            fail(f"{path.name}: unknown category field \"{field}\"")
        if field == "problems":
            fail(f"{path.name}: patch problems via \"problems\", not category_fields")
        data[field] = value
        changed_fields += 1

    for pid, fields in (patch.get("problems") or {}).items():
        if pid not in by_id:
            fail(f"{path.name}: problem {pid} is not in {cslug}")
        for field, value in fields.items():
            if field not in PROBLEM_FIELDS:
                fail(f"{path.name}: unknown problem field \"{field}\" on {pid}")
            check_shape(pid, field, value)
            by_id[pid][field] = value
            changed_fields += 1
        touched_problems.add(pid)

    target.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(
        f"{cslug}: {changed_fields} field(s) across "
        f"{len(touched_problems)} problem(s)"
        + (" + category" if patch.get("category_fields") else "")
    )


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1
    for arg in argv[1:]:
        apply_patch(Path(arg))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
