/**
 * Human-written copy for the card detail experience.
 *
 * Card descriptions are derived from metadata. They describe the CARD
 * (variant, accessories, frame treatment) and never make biographical
 * claims about the depicted person.
 */

export type Tier = "Common" | "Rare" | "Mythic";

const TIER_FRAME_NOTE: Record<Tier, string> = {
  Common: "Standard trait-color frame.",
  Rare: "Silver-gradient frame with a RARE badge.",
  Mythic: "Gold-gradient frame with corner sparkles, radial glow, and a MYTHIC badge.",
};

/**
 * Generate the long-form description shown on the card back and detail modal.
 * Style matches the brief: short, specific, collector-focused.
 */
export function describeVariant(opts: {
  tier: Tier;
  name: string;
  accessoryCount: number;
  accessoryNames?: string[];
}): string {
  const { tier, name, accessoryCount, accessoryNames = [] } = opts;
  const accessoryClause = accessoryNames.length
    ? accessoryNames.slice(0, 4).map(humanizeAccessory).join(", ")
    : "no accessories";

  if (tier === "Common") {
    return [
      `${name}'s Common card. The base personalized portrait, ${accessoryClause}.`,
      "This is the entry variant in the three-card set: the cleanest look, the lowest rarity. " +
        TIER_FRAME_NOTE.Common,
    ].join(" ");
  }
  if (tier === "Rare") {
    return [
      `${name}'s Rare variant. Adds ${accessoryCount} curated accessor${accessoryCount === 1 ? "y" : "ies"}: ${accessoryClause}.`,
      "Same character identity as the Common card, dressed for the floor. " +
        TIER_FRAME_NOTE.Rare,
    ].join(" ");
  }
  return [
    `${name}'s Mythic card. The premium variant in the three-card set, featuring ${accessoryClause}.`,
    "The strongest visual treatment of the three. " + TIER_FRAME_NOTE.Mythic,
  ].join(" ");
}

/**
 * Why this card is special (one-line collector hook).
 */
export function whyThisCard(opts: { tier: Tier; name: string }): string {
  const { tier, name } = opts;
  if (tier === "Common") return `The cleanest read of ${name}'s card. One of three.`;
  if (tier === "Rare") return `${name}'s daily-driver look. One of three.`;
  return `${name}'s most ornate variant. The pull every coworker wants.`;
}

/**
 * Turn "fat_gold_chain__gold" into "fat gold chain (gold)" for display.
 */
export function humanizeAccessory(raw: string): string {
  const [item, color = ""] = raw.split("__");
  const itemPretty = item.replace(/_/g, " ");
  if (!color || color === "default") return itemPretty;
  return `${itemPretty} (${color.replace(/_/g, " ")})`;
}

/**
 * Mint-status copy used by MintCard and CardBack.
 */
export function mintStatusCopy(opts: {
  isConnected: boolean;
  isAllowlisted: boolean;
  ownerName: string | null;
  remaining: number | null;
  totalForWallet: number;
}): { headline: string; body: string } {
  const { isConnected, isAllowlisted, ownerName, remaining, totalForWallet } = opts;
  if (!isConnected) {
    return {
      headline: "Connect your wallet to mint",
      body: "Each coworker is bound to their own card. Connect to see if any are available for your address.",
    };
  }
  if (!isAllowlisted) {
    return {
      headline: "This wallet is not on the coworker allowlist",
      body: "Cards are only mintable from the wallet of the depicted coworker. If you think this is your card, reach out and we will check the mapping.",
    };
  }
  if (remaining === 0) {
    return {
      headline: `All ${totalForWallet} of your variants are claimed`,
      body: `${ownerName ?? "You"} have already minted every variant. Check your wallet's NFT tab to see them.`,
    };
  }
  const remainingText = remaining === null ? totalForWallet : remaining;
  return {
    headline: `You're connected as ${ownerName ?? "yourself"}`,
    body: `You can mint up to ${remainingText} more ${ownerName ?? ""} card${remainingText === 1 ? "" : "s"}. Each variant is unique.`,
  };
}

/**
 * Compact rarity blurb shown next to the badge on detail pages.
 */
export function rarityBlurb(tier: Tier): string {
  if (tier === "Common") {
    return "Common: 15 cards in the collection (1 per coworker, variant 1 of 3).";
  }
  if (tier === "Rare") {
    return "Rare: 15 cards (1 per coworker, variant 2 of 3).";
  }
  return "Mythic: 15 cards (1 per coworker, variant 3 of 3). The premium variant.";
}
