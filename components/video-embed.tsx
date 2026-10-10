"use client";

import Image from "next/image";
import { useState } from "react";
import {
  youtubeEmbedUrl,
  youtubeThumbnail,
  youtubeWatchUrl,
} from "@/lib/youtube";
import { ExternalLink } from "./ui";

/**
 * Click-to-play YouTube embed, so a walkthrough is watchable without leaving
 * the problem.
 *
 * The iframe is mounted only once play is pressed. YouTube's player pulls in
 * close to a megabyte of script and sets cookies the moment it loads, and most
 * visits to a problem page never watch the video — so until then this is one
 * lazy thumbnail and a button. Playback runs on the nocookie host.
 */
export function VideoEmbed({ id, title }: { id: string; title: string }) {
  const [playing, setPlaying] = useState(false);
  // Degrade rather than show a broken image: a handful of links in the content
  // files point at videos that have since been pulled, and those have no
  // poster frame at any size. "none" leaves the plain card behind the button.
  const [poster, setPoster] = useState<"max" | "hq" | "none">("max");

  return (
    <div className="card overflow-hidden p-0">
      <div className="relative aspect-video w-full bg-codebg">
        {playing ? (
          <iframe
            src={youtubeEmbedUrl(id, { autoplay: true })}
            title={`${title} — NeetCode walkthrough`}
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
            allowFullScreen
            className="absolute inset-0 h-full w-full border-0"
          />
        ) : (
          <button
            type="button"
            onClick={() => setPlaying(true)}
            aria-label={`Play the NeetCode walkthrough for ${title}`}
            className="group absolute inset-0 h-full w-full cursor-pointer"
          >
            {poster !== "none" && (
              <Image
                src={youtubeThumbnail(id, poster)}
                alt=""
                fill
                sizes="(min-width: 48rem) 46rem, 100vw"
                onError={() =>
                  setPoster((p) => (p === "max" ? "hq" : "none"))
                }
                className="object-cover opacity-55 transition-opacity duration-300 group-hover:opacity-80"
              />
            )}
            <span
              aria-hidden="true"
              className="absolute inset-0 bg-gradient-to-t from-canvas/85 via-canvas/20 to-canvas/10"
            />
            <span
              aria-hidden="true"
              className="absolute inset-0 flex items-center justify-center"
            >
              <span className="flex h-16 w-16 items-center justify-center rounded-full border border-white/20 bg-accent/90 shadow-lg shadow-accent/30 transition-transform duration-200 group-hover:scale-110">
                <svg viewBox="0 0 24 24" className="ml-1 h-7 w-7 fill-white">
                  <path d="M8 5.1v13.8L19 12z" />
                </svg>
              </span>
            </span>
            <span
              aria-hidden="true"
              className="absolute bottom-3 left-4 font-display text-[11px] font-bold tracking-[0.12em] text-ink-bright/75 uppercase"
            >
              NeetCode walkthrough
            </span>
          </button>
        )}
      </div>

      <div className="flex items-center justify-between gap-3 border-t border-line px-4 py-2.5">
        <p className="min-w-0 truncate text-[12.5px] text-ink-dim">
          {playing
            ? "Streaming from YouTube"
            : "Nothing loads from YouTube until you press play"}
        </p>
        <div className="flex shrink-0 items-center gap-2">
          {playing && (
            <button
              type="button"
              onClick={() => setPlaying(false)}
              className="cursor-pointer rounded-md border border-line px-2.5 py-1 text-[12px] font-semibold text-ink-dim transition-colors hover:border-line-strong hover:text-ink-bright"
            >
              Close
            </button>
          )}
          <ExternalLink href={youtubeWatchUrl(id)}>
            YouTube &#8599;
          </ExternalLink>
        </div>
      </div>
    </div>
  );
}
