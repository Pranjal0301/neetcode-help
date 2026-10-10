import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    // Poster frames for the NeetCode walkthrough embeds; see lib/youtube.ts.
    remotePatterns: [new URL("https://i.ytimg.com/vi/**")],
  },
};

export default nextConfig;
