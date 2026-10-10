/**
 * The NeetCode links in content/dsa/*.json are plain YouTube watch URLs. The
 * embed player needs the bare 11-character video id, so parsing lives here
 * rather than at the call site — and tolerates the other link shapes a future
 * content edit might paste in.
 */

const ID = /^[\w-]{11}$/;

const WATCH_HOSTS = new Set([
  "youtube.com",
  "m.youtube.com",
  "music.youtube.com",
  "youtube-nocookie.com",
]);

/** Returns the video id, or null if the URL is missing or not a YouTube one. */
export function youtubeId(url: string | null | undefined): string | null {
  if (!url) return null;
  let u: URL;
  try {
    u = new URL(url);
  } catch {
    // Allow a bare id in the content file.
    return ID.test(url) ? url : null;
  }
  const host = u.hostname.replace(/^www\./, "");
  if (host === "youtu.be") {
    const id = u.pathname.slice(1);
    return ID.test(id) ? id : null;
  }
  if (!WATCH_HOSTS.has(host)) return null;
  const v = u.searchParams.get("v");
  if (v && ID.test(v)) return v;
  const path = /^\/(?:embed|shorts|live|v)\/([\w-]{11})/.exec(u.pathname);
  return path ? path[1] : null;
}

/**
 * youtube-nocookie.com is the same player without the ad-targeting cookies,
 * which is all this app needs from it.
 */
export function youtubeEmbedUrl(
  id: string,
  { autoplay = false, start = 0 } = {},
): string {
  const params = new URLSearchParams({ rel: "0", playsinline: "1" });
  if (autoplay) params.set("autoplay", "1");
  if (start > 0) params.set("start", String(Math.floor(start)));
  return `https://www.youtube-nocookie.com/embed/${id}?${params.toString()}`;
}

/**
 * `max` is 1280x720 but absent on some uploads; `hq` is always there, at 4:3
 * with letterbox bars that object-cover crops straight back off.
 */
export function youtubeThumbnail(id: string, size: "max" | "hq"): string {
  const file = size === "max" ? "maxresdefault" : "hqdefault";
  return `https://i.ytimg.com/vi/${id}/${file}.jpg`;
}

export function youtubeWatchUrl(id: string): string {
  return `https://www.youtube.com/watch?v=${id}`;
}
