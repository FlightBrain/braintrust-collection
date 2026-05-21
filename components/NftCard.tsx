"use client";

import { useState } from "react";
import { RarityBadge } from "./RarityBadge";
import { CardBack } from "./CardBack";
import type { Tier } from "@/lib/card-copy";

type Attr = { trait_type: string; value: string | number };

export function NftCard({
  name,
  slug,
  tier,
  tokenId,
  variantNumber,
  imagePath,
  description,
  whyText,
  attributes,
  flippable = true,
  onClick,
}: {
  name: string;
  slug: string;
  tier: Tier;
  tokenId: number;
  variantNumber: number;
  imagePath: string;
  description: string;
  whyText: string;
  attributes: Attr[];
  flippable?: boolean;
  onClick?: () => void;
}) {
  const [flipped, setFlipped] = useState(false);
  const toggle = () => {
    if (onClick) onClick();
    else if (flippable) setFlipped((f) => !f);
  };

  return (
    <div className="card-flip-wrapper aspect-square w-full">
      <button
        type="button"
        onClick={toggle}
        aria-label={
          onClick
            ? `Open details for ${name} ${tier} card`
            : `${flipped ? "Hide" : "Show"} details for ${name} ${tier} card`
        }
        aria-pressed={flippable && !onClick ? flipped : undefined}
        className="card-flip-button group block h-full w-full focus:outline-none focus-visible:ring-2 focus-visible:ring-accent focus-visible:ring-offset-2 focus-visible:ring-offset-bg rounded-2xl"
      >
        <div className={`card-flip ${flipped ? "flipped" : ""}`}>
          {/* FRONT: artwork is the hero */}
          <div className="card-face card-front overflow-hidden rounded-2xl border border-line bg-panel transition-shadow group-hover:shadow-[0_0_40px_rgba(0,255,148,0.12)]">
            <img
              src={imagePath}
              alt={`${name}, ${tier} variant, token ${tokenId}`}
              className="block h-full w-full object-cover"
              loading="lazy"
            />
            {/* Subtle overlay strip with name + rarity + token id */}
            <div className="pointer-events-none absolute inset-x-0 bottom-0 flex items-center justify-between gap-2 bg-gradient-to-t from-bg/95 via-bg/60 to-transparent px-3 py-2">
              <div className="min-w-0">
                <p className="truncate text-left text-[12px] font-bold text-white">
                  {name}
                </p>
                <p className="font-mono text-[9px] uppercase tracking-[0.2em] text-muted">
                  #{String(tokenId).padStart(3, "0")}
                </p>
              </div>
              <RarityBadge tier={tier} size="sm" />
            </div>
          </div>
          {/* BACK: collector info */}
          <div className="card-face card-back">
            <CardBack
              name={name}
              tier={tier}
              tokenId={tokenId}
              variantNumber={variantNumber}
              description={description}
              whyText={whyText}
              attributes={attributes}
            />
          </div>
        </div>
      </button>
    </div>
  );
}
