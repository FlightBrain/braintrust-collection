import { RarityBadge } from "./RarityBadge";
import type { Tier } from "@/lib/card-copy";

type Attr = { trait_type: string; value: string | number };

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
  // Pull the 4 most useful traits for the back display
  const visible = attributes
    .filter(
      (a) =>
        a.trait_type.startsWith("Accessory: ") ||
        a.trait_type === "Variant Rarity" ||
        a.trait_type === "Edition"
    )
    .slice(0, 5);

  return (
    <div className="flex h-full flex-col gap-3 rounded-2xl border border-line bg-panel p-5">
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
        <p className="mt-1 text-[13px] leading-relaxed text-accent">{whyText}</p>
      </div>

      {/* Traits */}
      {visible.length > 0 && (
        <div className="mt-auto">
          <p className="font-mono text-[10px] uppercase tracking-[0.18em] text-muted">
            Traits
          </p>
          <ul className="mt-2 grid grid-cols-2 gap-1.5">
            {visible.map((a, i) => (
              <li
                key={i}
                className="rounded border border-line bg-bg/40 px-2 py-1 text-[11px]"
              >
                <span className="text-muted">
                  {a.trait_type.replace(/^Accessory: /, "").replace(/_/g, " ")}
                </span>
                <span className="ml-1 font-semibold text-white">
                  {typeof a.value === "string"
                    ? a.value.replace(/_/g, " ")
                    : a.value}
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Footer */}
      <p className="mt-2 font-mono text-[9px] uppercase tracking-[0.2em] text-muted">
        Click card to flip back
      </p>
    </div>
  );
}
