"use client";

import { useRef, useState } from "react";
import {
  actions,
  emptyRecord,
  STORAGE_KEY,
  useStore,
  type StoreState,
} from "@/lib/store";
import { Callout, SectionHeading } from "./ui";

type Notice = { tone: "easy" | "hard"; text: string } | null;

export function SettingsView({ totalProblems }: { totalProblems: number }) {
  const { state, hydrated } = useStore();
  const [notice, setNotice] = useState<Notice>(null);
  const [pasted, setPasted] = useState("");
  const fileRef = useRef<HTMLInputElement>(null);

  const solved = Object.values(state.problems).filter((r) => r.solved).length;
  const scheduled = Object.values(state.problems).filter(
    (r) => r.srs && r.srs.lastReviewedAt > 0,
  ).length;

  const download = () => {
    const blob = new Blob([JSON.stringify(state, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `dsa-mastery-${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const applyImport = (raw: string) => {
    try {
      const parsed = JSON.parse(raw) as StoreState;
      if (!parsed || typeof parsed !== "object" || !parsed.problems) {
        throw new Error("not a progress file");
      }
      actions.replaceAll(parsed);
      const count = Object.values(parsed.problems).filter(
        (r) => r?.solved,
      ).length;
      setNotice({
        tone: "easy",
        text: `Imported ${count} solved problem${count === 1 ? "" : "s"}.`,
      });
      setPasted("");
    } catch (err) {
      setNotice({
        tone: "hard",
        text: `Could not import that: ${err instanceof Error ? err.message : "invalid JSON"}.`,
      });
    }
  };

  /** Accept the legacy guide's own `{ "217": true }` shape too. */
  const importLegacy = (raw: string) => {
    try {
      const checked = JSON.parse(raw) as Record<string, boolean>;
      const problems = { ...state.problems };
      let count = 0;
      for (const [id, on] of Object.entries(checked)) {
        if (!on) continue;
        if (!problems[id]?.solved) {
          problems[id] = { ...emptyRecord(), solved: true, solvedAt: Date.now() };
          count += 1;
        }
      }
      actions.replaceAll({ ...state, problems });
      setNotice({
        tone: "easy",
        text: `Brought across ${count} solved problem${count === 1 ? "" : "s"} from the legacy guide.`,
      });
      setPasted("");
    } catch {
      setNotice({
        tone: "hard",
        text: "That did not look like the legacy neetcode_checked value.",
      });
    }
  };

  return (
    <div className="space-y-8">
      <section>
        <SectionHeading>Stored on this device</SectionHeading>
        <div className="card divide-y divide-line">
          <Row label="Problems solved" value={hydrated ? `${solved} / ${totalProblems}` : "—"} />
          <Row label="In review rotation" value={hydrated ? String(scheduled) : "—"} />
          <Row label="Mocks recorded" value={hydrated ? String(state.mocks.length) : "—"} />
          <Row
            label="Drill questions answered"
            value={hydrated ? String(state.drills.attempts) : "—"}
          />
          <Row label="Study track" value={hydrated ? (state.plan?.track ?? "none") : "—"} />
        </div>
        <p className="mt-2.5 text-[12.5px] text-ink-dim">
          All of it lives in your browser under{" "}
          <code className="rounded bg-codebg px-1.5 py-0.5 font-mono text-[11.5px]">
            {STORAGE_KEY}
          </code>
          . Nothing is sent anywhere. Clearing site data erases it, so export a
          copy if you care about the history.
        </p>
      </section>

      {notice && (
        <Callout tone={notice.tone} title={notice.tone === "easy" ? "Done" : "Failed"}>
          {notice.text}
        </Callout>
      )}

      <section>
        <SectionHeading hint="Use this to move progress between browsers, devices, or origins.">
          Backup
        </SectionHeading>
        <div className="flex flex-wrap gap-3">
          <button
            type="button"
            onClick={download}
            className="rounded-md border border-accent/50 bg-accent/15 px-4 py-2 text-[13.5px] font-semibold text-accent-soft transition-colors hover:bg-accent/25"
          >
            Export to file
          </button>
          <button
            type="button"
            onClick={() => fileRef.current?.click()}
            className="rounded-md border border-line px-4 py-2 text-[13.5px] font-semibold text-ink-dim transition-colors hover:border-line-strong hover:text-ink"
          >
            Import from file
          </button>
          <input
            ref={fileRef}
            type="file"
            accept="application/json,.json"
            className="hidden"
            onChange={async (e) => {
              const file = e.target.files?.[0];
              if (file) applyImport(await file.text());
              e.target.value = "";
            }}
          />
        </div>
      </section>

      <section>
        <SectionHeading hint="Open the legacy guide, run localStorage.getItem('neetcode_checked') in the console, and paste the result here.">
          Bring progress from the legacy guide
        </SectionHeading>
        <textarea
          value={pasted}
          onChange={(e) => setPasted(e.target.value)}
          rows={3}
          placeholder='{"217":true,"242":true,…}'
          className="w-full resize-y rounded-card border border-line bg-codebg px-3.5 py-2.5 font-mono text-[12.5px] text-ink outline-none transition-colors placeholder:text-ink-dim/70 focus:border-accent/50"
        />
        <div className="mt-2.5 flex flex-wrap gap-3">
          <button
            type="button"
            disabled={!pasted.trim()}
            onClick={() => importLegacy(pasted)}
            className="rounded-md border border-line px-4 py-2 text-[13.5px] font-semibold text-ink-dim transition-colors enabled:hover:border-line-strong enabled:hover:text-ink disabled:opacity-40"
          >
            Merge legacy progress
          </button>
          <button
            type="button"
            disabled={!pasted.trim()}
            onClick={() => applyImport(pasted)}
            className="rounded-md border border-line px-4 py-2 text-[13.5px] font-semibold text-ink-dim transition-colors enabled:hover:border-line-strong enabled:hover:text-ink disabled:opacity-40"
          >
            Replace with a full export
          </button>
        </div>
      </section>

      <section>
        <SectionHeading>Danger zone</SectionHeading>
        <ResetButton />
      </section>
    </div>
  );
}

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between px-4 py-2.5">
      <span className="text-[13.5px] text-ink">{label}</span>
      <span className="font-mono text-[13px] text-ink-bright">{value}</span>
    </div>
  );
}

/** Two-step, because there is no undo. */
function ResetButton() {
  const [armed, setArmed] = useState(false);

  if (!armed) {
    return (
      <button
        type="button"
        onClick={() => setArmed(true)}
        className="rounded-md border border-line px-4 py-2 text-[13.5px] font-semibold text-ink-dim transition-colors hover:border-hard/50 hover:text-hard"
      >
        Erase all progress
      </button>
    );
  }

  return (
    <div className="flex flex-wrap items-center gap-3">
      <span className="text-[13.5px] text-hard">
        This cannot be undone. Export first?
      </span>
      <button
        type="button"
        onClick={() => {
          actions.reset();
          setArmed(false);
        }}
        className="rounded-md border border-hard/50 bg-hard/15 px-4 py-2 text-[13.5px] font-semibold text-hard transition-colors hover:bg-hard/25"
      >
        Yes, erase everything
      </button>
      <button
        type="button"
        onClick={() => setArmed(false)}
        className="rounded-md border border-line px-4 py-2 text-[13.5px] text-ink-dim transition-colors hover:text-ink"
      >
        Cancel
      </button>
    </div>
  );
}
