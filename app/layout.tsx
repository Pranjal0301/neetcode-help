import type { Metadata, Viewport } from "next";
import Link from "next/link";
import { Inter, JetBrains_Mono, Outfit } from "next/font/google";
import "./globals.css";
import { SiteHeader } from "@/components/site-header";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

const jetbrains = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-jetbrains",
  display: "swap",
});

const outfit = Outfit({
  subsets: ["latin"],
  variable: "--font-outfit",
  display: "swap",
});

export const metadata: Metadata = {
  title: {
    default: "DSA Mastery — NeetCode 150 Study Platform",
    template: "%s · DSA Mastery",
  },
  description:
    "Pattern-first preparation through the NeetCode 150: worked explanations, diagrams, dry runs, spaced repetition and timed mocks.",
  icons: { icon: "/favicon.svg" },
};

export const viewport: Viewport = {
  themeColor: "#0c0e1a",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        {/*
          Runs before first paint so review mode never flashes the solution.
          Kept inline and tiny for that reason — a React effect would be too late.
        */}
        <script
          dangerouslySetInnerHTML={{
            __html: `try{if(new URLSearchParams(location.search).get('review')==='1')document.documentElement.setAttribute('data-review','1')}catch(e){}`,
          }}
        />
      </head>
      <body
        className={`${inter.variable} ${jetbrains.variable} ${outfit.variable} min-h-dvh`}
      >
        <SiteHeader />
        <main>{children}</main>
        <footer className="mt-16 border-t border-line">
          <div className="mx-auto flex max-w-3xl flex-wrap items-center gap-x-5 gap-y-2 px-4 py-6 text-[12.5px] text-ink-dim">
            <span>Progress is stored in this browser only.</span>
            <Link href="/settings" className="hover:text-ink-bright">
              Settings &amp; backup
            </Link>
            <a
              href="https://neetcode.io/practice"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-ink-bright"
            >
              NeetCode
            </a>
          </div>
        </footer>
      </body>
    </html>
  );
}
