import type { Tier } from "@/lib/card-copy";

const STYLES: Record<Tier, { color: string; bg: string; border: string }> = {
  Common: {
    color: "#8B95A8",
    bg: "rgba(139,149,168,0.10)",
    border: "rgba(139,149,168,0.40)",
  },
  Rare: {
    color: "#9D7AFF",
    bg: "rgba(157,122,255,0.12)",
    border: "rgba(157,122,255,0.40)",
  },
  Mythic: {
    color: "#FFD93D",
    bg: "rgba(255,217,61,0.12)",
    border: "rgba(255,217,61,0.50)",
  },
};

export function RarityBadge({
  tier,
  size = "md",
  withDot = true,
}: {
  tier: Tier;
  size?: "sm" | "md" | "lg";
  withDot?: boolean;
}) {
  const s = STYLES[tier];
  const sizeClasses =
    size === "sm"
      ? "px-2 py-0.5 text-[9px]"
      : size === "lg"
      ? "px-3.5 py-1.5 text-[12px]"
      : "px-2.5 py-1 text-[10px]";
  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full border font-mono font-bold uppercase tracking-[0.22em] ${sizeClasses}`}
      style={{ color: s.color, background: s.bg, borderColor: s.border }}
      aria-label={`${tier} rarity`}
    >
      {withDot && (
        <span
          className="block h-1.5 w-1.5 rounded-full"
          style={{ background: s.color }}
          aria-hidden="true"
        />
      )}
      {tier}
    </span>
  );
}
