import { RarityBadge } from "./RarityBadge";
import type { Tier } from "@/lib/card-copy";

type Attr = { trait_type: string; value: string | number };

const TIER_ACCENT: Record<Tier, { tint: string; border: string; glow: string }> = {
  Common: {
    tint: "rgba(139,149,168,0.05)",
    border: "rgba(139,149,168,0.25)",
    glow: "rgba(139,149,168,0)",
  },
  Rare: {
    tint: "rgba(157,122,255,0.07)",
    border: "rgba(157,122,255,0.40)",
    glow: "rgba(157,122,255,0.18)",
  },
  Mythic: {
    tint: "rgba(255,217,61,0.07)",
    border: "rgba(255,217,61,0.55)",
    glow: "rgba(255,217,61,0.22)",
  },
};

export function CardBack({
  name,
  tier,
  tokenId,
  variantNumber,
  description,
  whyText,
  attributes,
}: {
  name: string;
  tier: Tier;
  tokenId: number;
  variantNumber: number;
  description: string;
  whyText: string;
  attributes: Attr[];
}) {
  const a = TIER_ACCENT[tier];

  // Pull the 4 most useful traits for the back display
  const visible = attributes
    .filter(
      (att) =>
        att.trait_type.startsWith("Accessory: ") ||
        att.trait_type === "Variant Rarity" ||
        att.trait_type === "Edition"
    )
    .slice(0, 5);

  return (
    <div
      className="flex h-full flex-col gap-3 rounded-2xl border p-5"
      style={{
        background: `linear-gradient(180deg, ${a.tint} 0%, transparent 60%), #0F1320`,
        borderColor: a.border,
        boxShadow: `inset 0 0 60px ${a.glow}`,
      }}
    >
      {/* Header */}
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="font-mono text-[10px] uppercase tracking-[0.22em] text-muted">
            Card #{String(tokenId).padStart(3, "0")} · Variant {variantNumber} of 3
          </p>
          <h3 className="mt-1 text-xl font-bold leading-tight">{name}</h3>
        </div>
        <RarityBadge tier={tier} size="md" />
      </div>

      {/* Accent divider */}
      <div className="h-px w-full" style={{ background: a.border }} />

      {/* Description */}
      <div>
        <p className="font-mono text-[10px] uppercase tracking-[0.18em] text-muted">
          About this card
        </p>
        <p className="mt-1 text-[13px] leading-relaxed text-white/85">
          {description}
        </p>
      </div>

      {/* Why this card */}
      <div>
        <p className="font-mono text-[10px] uppercase tracking-[0.18em] text-muted">
          Why this card
        </p>
        <p
          className="mt-1 text-[13px] leading-relaxed"
          style={{ color: tier === "Mythic" ? "#FFD93D" : tier === "Rare" ? "#9D7AFF" : "#00FF94" }}
        >
          {whyText}
        </p>
      </div>

      {/* Traits */}
      {visible.length > 0 && (
        <div className="mt-auto">
          <p className="font-mono text-[10px] uppercase tracking-[0.18em] text-muted">
            Traits
          </p>
          <ul className="mt-2 grid grid-cols-2 gap-1.5">
            {visible.map((att, i) => (
              <li
                key={i}
                className="rounded border px-2 py-1 text-[11px]"
                style={{ borderColor: a.border, background: a.tint }}
              >
                <span className="text-muted">
                  {att.trait_type.replace(/^Accessory: /, "").replace(/_/g, " ")}
                </span>
                <span className="ml-1 font-semibold text-white">
                  {typeof att.value === "string"
                    ? att.value.replace(/_/g, " ")
                    : att.value}
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
