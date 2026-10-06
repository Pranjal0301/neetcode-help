import type { Metadata } from "next";
import { getAllProblems } from "@/lib/content";
import { SettingsView } from "@/components/settings-view";

export const metadata: Metadata = {
  title: "Settings",
  description: "Back up, import or erase your study progress.",
};

export default function SettingsPage() {
  return (
    <div className="mx-auto max-w-2xl px-4 py-8 sm:py-10">
      <header className="mb-8">
        <h1 className="font-display text-[28px] leading-tight font-bold text-ink-bright sm:text-[34px]">
          Settings
        </h1>
        <p className="mt-2 text-[14.5px] text-ink-dim">
          Your progress never leaves this browser, which also means nothing
          restores it for you. Keep an export somewhere.
        </p>
      </header>

      <SettingsView totalProblems={getAllProblems().length} />
    </div>
  );
}
