import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* Disable Turbopack - not supported on Android/ARM */
  turbo: false,
};

export default nextConfig;
