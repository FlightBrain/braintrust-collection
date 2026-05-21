"use client";

import { useEffect } from "react";
import { RarityBadge } from "./RarityBadge";
import { TraitGrid } from "./TraitGrid";
import { NftCard } from "./NftCard";
import { describeVariant, whyThisCard, rarityBlurb } from "@/lib/card-copy";
import type { Tier } from "@/lib/card-copy";

type Attr = { trait_type: string; value: string | number };

export type VariantData = {
  tokenId: number;
  slug: string;
  name: string;
  tier: Tier;
  variantNumber: number;
  imagePath: string;
  attributes: Attr[];
};

export function VariantDetailModal({
  variant,
  onClose,
}: {
  variant: VariantData | null;
  onClose: () => void;
}) {
  useEffect(() => {
    if (!variant) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    document.addEventListener("keydown", onKey);
    const prev = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("keydown", onKey);
      document.body.style.overflow = prev;
    };
  }, [variant, onClose]);

  if (!variant) return null;

  const accessoryAttrs = variant.attributes
    .filter((a) => a.trait_type.startsWith("Accessory: "))
    .map((a) => `${a.trait_type.replace(/^Accessory: /, "")}__${a.value}`);

  const description = describeVariant({
    tier: variant.tier,
    name: variant.name,
    accessoryCount: accessoryAttrs.length,
    accessoryNames: accessoryAttrs,
  });
  const why = whyThisCard({ tier: variant.tier, name: variant.name });

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-label={`${variant.name} ${variant.tier} card details`}
      className="fixed inset-0 z-50 overflow-y-auto"
    >
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-bg/85 backdrop-blur"
        onClick={onClose}
        aria-hidden="true"
      />
      {/* Panel */}
      <div className="relative mx-auto my-8 max-w-4xl px-4 sm:px-6">
        <div className="rounded-2xl border border-line bg-panel p-5 shadow-2xl sm:p-8">
          {/* Close */}
          <div className="mb-4 flex items-center justify-between">
            <p className="font-mono text-[10px] uppercase tracking-[0.22em] text-muted">
              Card detail
            </p>
            <button
              type="button"
              onClick={onClose}
              className="flex h-10 w-10 items-center justify-center rounded-md border border-line text-white hover:border-accent hover:text-accent focus:outline-none focus-visible:ring-2 focus-visible:ring-accent"
              aria-label="Close detail"
            >
              <svg
                width="18"
                height="18"
                viewBox="0 0 20 20"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                aria-hidden="true"
              >
                <line x1="4" y1="4" x2="16" y2="16" />
                <line x1="16" y1="4" x2="4" y2="16" />
              </svg>
            </button>
          </div>

          {/* Two-column layout: art on left, info on right */}
          <div className="grid gap-6 md:grid-cols-2">
            <div className="mx-auto w-full max-w-md">
              <NftCard
                name={variant.name}
                slug={variant.slug}
                tier={variant.tier}
                tokenId={variant.tokenId}
                variantNumber={variant.variantNumber}
                imagePath={variant.imagePath}
                description={description}
                whyText={why}
                attributes={variant.attributes}
              />
            </div>

            <div className="space-y-5">
              <div>
                <div className="flex flex-wrap items-center gap-2">
                  <h2 className="text-2xl font-black leading-tight">
                    {variant.name}
                  </h2>
                  <RarityBadge tier={variant.tier} size="md" />
                </div>
                <p className="mt-1 font-mono text-[11px] uppercase tracking-[0.2em] text-muted">
                  Token #{String(variant.tokenId).padStart(3, "0")} · Variant{" "}
                  {variant.variantNumber} of 3
                </p>
              </div>

              <div>
                <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-muted">
                  About this card
                </p>
                <p className="mt-1 text-sm leading-relaxed text-white/85">
                  {description}
                </p>
              </div>

              <div>
                <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-muted">
                  Why this card
                </p>
                <p className="mt-1 text-sm leading-relaxed text-accent">
                  {why}
                </p>
              </div>

              <div>
                <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-muted">
                  Rarity
                </p>
                <p className="mt-1 text-sm leading-relaxed text-white/85">
                  {rarityBlurb(variant.tier)}
                </p>
              </div>

              <div>
                <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-muted">
                  Traits
                </p>
                <div className="mt-2">
                  <TraitGrid attributes={variant.attributes} />
                </div>
              </div>

              <div className="rounded-xl border border-line bg-bg/40 p-3">
                <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-muted">
                  Mint eligibility
                </p>
                <p className="mt-1 text-xs leading-relaxed text-white/80">
                  Only {variant.name}'s wallet can mint this card. Each
                  coworker on the allowlist can claim their 3 variants once.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
