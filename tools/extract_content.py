#!/usr/bin/env python3
"""
Phase 0: extract structured content out of the legacy single-file index.html
into content/dsa/<category>.json.

Read-only on index.html. Prints a coverage report so we can prove nothing was lost.
"""
import re, json, html, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "index.html"
OUT = ROOT / "content" / "dsa"

APOSTROPHES = "‘’'"

# ---------- text helpers ----------

def unescape(s):
    return html.unescape(s)

def to_markdown(frag):
    """Convert a small inline HTML fragment to markdown-ish plain text."""
    s = frag
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
    s = re.sub(r"</p>\s*<p>", "\n\n", s, flags=re.I)
    s = re.sub(r"<strong>(.*?)</strong>", r"**\1**", s, flags=re.S | re.I)
    s = re.sub(r"<b>(.*?)</b>", r"**\1**", s, flags=re.S | re.I)
    s = re.sub(r"<em>(.*?)</em>", r"*\1*", s, flags=re.S | re.I)
    s = re.sub(r"<i>(.*?)</i>", r"*\1*", s, flags=re.S | re.I)
    s = re.sub(r"<code>(.*?)</code>", r"`\1`", s, flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", "", s)
    s = unescape(s)
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()

def plain(frag):
    s = re.sub(r"<[^>]+>", "", frag)
    return re.sub(r"\s+", " ", unescape(s)).strip()

def code_text(frag):
    """Strip syntax-highlight spans from a <pre> body, keep whitespace exactly."""
    s = re.sub(r"</?span[^>]*>", "", frag)
    return unescape(s).rstrip()

def slugify(title):
    s = unescape(title).lower()
    s = "".join(ch for ch in s if ch not in APOSTROPHES)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")

# ---------- block splitting ----------

def split_blocks(text, marker_re):
    """Split text into (header_match, chunk) pairs on a repeated opening marker."""
    starts = list(re.finditer(marker_re, text))
    out = []
    for i, m in enumerate(starts):
        end = starts[i + 1].start() if i + 1 < len(starts) else len(text)
        out.append((m, text[m.start():end]))
    return out

# ---------- field extractors ----------

def grab(pattern, chunk, group=1, flags=re.S):
    m = re.search(pattern, chunk, flags)
    return m.group(group) if m else None

def extract_code(body):
    code = {}
    for m in re.finditer(
        r'<div class="lang-panel[^"]*"\s+data-lang="(\w+)">\s*<pre>(.*?)</pre>', body, re.S
    ):
        code[m.group(1)] = code_text(m.group(2))
    if not code:
        # legacy problem with no language tabs: first <pre> is the python solution
        first = grab(r"<pre>(.*?)</pre>", body)
        if first:
            code["python"] = code_text(first)
    return code

def extract_approach_steps(body):
    ol = grab(r'<ol class="approach-steps">(.*?)</ol>', body)
    if not ol:
        return []
    return [to_markdown(li) for li in re.findall(r"<li>(.*?)</li>", ol, re.S)]

def extract_complexity(body):
    """Pull Time/Space out of the complexity box.

    Matches the <strong> labels directly rather than trying to balance the
    box's closing </div>s, which the legacy markup nests inconsistently.
    """
    start = body.find('<div class="complexity-box"')
    if start == -1:
        return None
    region = body[start:]
    for terminator in ('<div class="dry-run"', '<div class="lang-tabs"', '<div class="problem"'):
        cut = region.find(terminator)
        if cut != -1:
            region = region[:cut]
    out = {}
    for m in re.finditer(
        r"<strong>\s*(Time|Space)\s*:?\s*</strong>\s*([^<]*)", region, re.I
    ):
        label, value = m.group(1).lower(), unescape(m.group(2)).strip()
        value = value.lstrip(":").strip()
        # legacy values sometimes carry an inline note: "O(1) - at most 26 chars"
        note = None
        split = re.match(r"^(O\([^)]*\)[^\s-]*)\s*[-–—]\s*(.+)$", value)
        if split:
            value, note = split.group(1).strip(), split.group(2).strip()
        out[label] = value
        if note:
            out.setdefault("note", note)
    return out or None

def extract_dry_run(body):
    dr = grab(r'<div class="dry-run">.*?<pre>(.*?)</pre>', body)
    return code_text(dr) if dr else None

def extract_links(header):
    links = {}
    for m in re.finditer(r'<a href="([^"]+)"[^>]*class="problem-link (\w+)-link"', header):
        url, kind = m.group(1), m.group(2)
        links["leetcode" if kind == "lc" else "neetcodeVideo"] = url
    if not links:
        for m in re.finditer(r'<a href="(https://[^"]+)"', header):
            u = m.group(1)
            if "leetcode.com" in u:
                links["leetcode"] = u
            elif "youtube.com" in u or "youtu.be" in u:
                links["neetcodeVideo"] = u
    return links

# ---------- main ----------

def main():
    raw = SRC.read_text(encoding="utf-8")
    container = raw[raw.index('<div class="container" id="content">'):]

    categories = []
    all_problems = 0
    cov = {k: 0 for k in
           ("pattern", "keyInsight", "approach", "complexityTime", "complexitySpace",
            "dryRun", "code4", "links")}
    difficulties = {}

    cat_blocks = split_blocks(container, r'<div class="category(?: open)?" data-category="[^"]+">')

    for cm, cchunk in cat_blocks:
        cslug = grab(r'data-category="([^"]+)"', cm.group(0))
        ctitle = plain(grab(r'<span class="category-title">(.*?)</span>', cchunk) or cslug)
        cicon = unescape(grab(r'<span class="category-icon">(.*?)</span>', cchunk) or "")

        # category-level teaching content
        concept_html = grab(
            r'<div class="concept-box">(.*?)(?=<!-- Problem|<div class="problem")', cchunk)
        concept = {}
        if concept_html:
            concept["heading"] = plain(grab(r"<h3>(.*?)</h3>", concept_html) or "Core Concepts")
            paras = re.findall(r"<p>(.*?)</p>", concept_html, re.S)
            concept["body"] = "\n\n".join(to_markdown(p) for p in paras)
            ul = grab(r"<ul>(.*?)</ul>", concept_html)
            concept["bullets"] = (
                [to_markdown(li) for li in re.findall(r"<li>(.*?)</li>", ul, re.S)] if ul else []
            )
            svg = grab(r"(<svg\b.*?</svg>)", concept_html)
            concept["legacySvg"] = svg.strip() if svg else None

        problems = []
        pblocks = split_blocks(cchunk, r'<div class="problem" data-difficulty=')
        for order, (_pm, pchunk) in enumerate(pblocks, start=1):
            header = grab(
                r'(<div class="problem-header".*?)(?=<div class="problem-body")', pchunk
            ) or pchunk[:4000]
            body = (pchunk[pchunk.find('<div class="problem-body"'):]
                    if '<div class="problem-body"' in pchunk else pchunk)

            pid = grab(r'data-id="(\d+)"', pchunk)
            title = plain(grab(r'<span class="problem-name">(.*?)</span>', pchunk) or "")
            if not pid or not title:
                print(f"  !! skipped malformed problem in {cslug} at order {order}",
                      file=sys.stderr)
                continue

            difficulty = grab(r'data-difficulty="(\w+)"', pchunk[:300]) or "medium"
            tags_raw = grab(r'data-tags="([^"]*)"', pchunk) or ""
            pattern = plain(grab(r'<span class="approach-tag">(.*?)</span>', body) or "") or None
            ki = grab(r'<div class="key-insight">(.*?)</div>', body)
            key_insight = None
            if ki:
                key_insight = re.sub(r"^\*\*Key Insight:\*\*\s*", "", to_markdown(ki)).strip()

            code = extract_code(body)
            steps = extract_approach_steps(body)
            comp = extract_complexity(body)
            dry = extract_dry_run(body)
            links = extract_links(header)

            problems.append({
                "id": pid,
                "slug": slugify(title),
                "title": title,
                "difficulty": difficulty,
                "category": cslug,
                "order": order,
                "tags": [t for t in tags_raw.split() if t],
                "links": links,
                "pattern": pattern,
                "patternTriggers": [],
                "keyInsight": key_insight,
                "bruteForce": None,
                "approach": steps,
                "code": code,
                "complexity": comp,
                "dryRun": dry,
                "diagram": None,
                "pitfalls": [],
                "edgeCases": [],
                "followUps": [],
                "related": [],
                "core": False,
            })

            all_problems += 1
            difficulties[difficulty] = difficulties.get(difficulty, 0) + 1
            if pattern: cov["pattern"] += 1
            if key_insight: cov["keyInsight"] += 1
            if steps: cov["approach"] += 1
            if comp and comp.get("time"): cov["complexityTime"] += 1
            if comp and comp.get("space"): cov["complexitySpace"] += 1
            if dry: cov["dryRun"] += 1
            if len(code) >= 4: cov["code4"] += 1
            if links.get("leetcode"): cov["links"] += 1

        categories.append({
            "slug": cslug,
            "title": ctitle,
            "icon": cicon,
            "order": len(categories) + 1,
            "concept": concept or None,
            "patternTemplate": None,
            "recognitionTriggers": [],
            "problems": problems,
        })

    OUT.mkdir(parents=True, exist_ok=True)
    for cat in categories:
        (OUT / f"{cat['slug']}.json").write_text(
            json.dumps(cat, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    index = [{"slug": c["slug"], "title": c["title"], "icon": c["icon"],
              "order": c["order"], "count": len(c["problems"])} for c in categories]
    (OUT / "_index.json").write_text(
        json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # ---- coverage report ----
    print(f"\nExtracted {len(categories)} categories, {all_problems} problems "
          f"-> {OUT.relative_to(ROOT)}\n")
    print(f"{'field':<22}{'have':>6}{'missing':>9}")
    print("-" * 37)
    for k, v in cov.items():
        print(f"{k:<22}{v:>6}{all_problems - v:>9}")
    print(f"\ndifficulty mix: {difficulties}\n")
    for c in categories:
        flag = "  (no concept box)" if not c["concept"] else ""
        print(f"  {c['slug']:<20} {len(c['problems']):>3} problems{flag}")

    dupes = {}
    for c in categories:
        for p in c["problems"]:
            dupes.setdefault(p["slug"], []).append(p["id"])
    collide = {k: v for k, v in dupes.items() if len(v) > 1}
    if collide:
        print(f"\n!! duplicate slugs: {collide}")

    return 0 if all_problems == 150 else 1

if __name__ == "__main__":
    sys.exit(main())
