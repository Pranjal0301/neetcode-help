# Legacy single-file version

`index.html` is the original hand-written 958KB study guide. It still works —
open it directly in a browser, no build step, no server.

It is kept here as the source of truth that `tools/extract_content.py` parsed
into `content/dsa/*.json`, and as a fallback until the new app reaches parity.

`build.py` was a one-time migration script that added the multi-language code
tabs. It is retained for provenance only and **must not be run**: its paths are
hardcoded to `/home/pranjal/Downloads/dsa-plan/`, and it mutates `index.html`
in place, so a second run would double-inject its CSS and JS.
