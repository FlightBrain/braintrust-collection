import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        bg: "#050709",
        panel: "#0F1320",
        line: "rgba(255,255,255,0.08)",
        muted: "#8B95A8",
        accent: "#00FF94",
        mythic: "#FF3366",
        legendary: "#FFD93D",
        rare: "#9D7AFF",
        uncommon: "#00D9FF",
        common: "#8B95A8",
      },
      fontFamily: {
        mono: ["'JetBrains Mono'", "ui-monospace", "monospace"],
        sans: ["Inter", "ui-sans-serif", "system-ui"],
      },
    },
  },
  plugins: [],
};

export default config;
