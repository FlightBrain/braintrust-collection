/**
 * Generates ERC-721 metadata JSON for the wallet-bound 3-variant flow.
 *
 * Layout: 15 SDRs x 3 variants = 45 tokens.
 *   Tokens 0,1,2   -> SDR 0 (alec)   variants Common, Rare, Mythic
 *   Tokens 3,4,5   -> SDR 1 (ava)    variants Common, Rare, Mythic
 *   ...
 *   Tokens 42,43,44 -> SDR 14 (shaune) variants Common, Rare, Mythic
 *
 * Reads:
 *   public/auto_people.json
 *   public/rarity.json
 *   public/sdrs/assignments.json (assigned accessories per SDR, optional)
 *
 * Writes:
 *   public/metadata/{0..44}.json
 *   public/metadata/_index.json
 *
 * IMAGE NOTE: until we generate dedicated variant SVGs, all 3 variants of a
 * given SDR reference the same SVG (the existing /nfts/corporate/{slug}_nft.svg).
 * Metadata attributes encode the variant + rarity tier. Art is unchanged.
 * Variant SVGs will be generated as a separate task after this system is
 * approved.
 */
import fs from "node:fs";
import path from "node:path";

const ROOT = path.resolve(__dirname, "..");
const PEOPLE_PATH = path.join(ROOT, "public", "auto_people.json");
const RARITY_PATH = path.join(ROOT, "public", "rarity.json");
const ASSIGN_PATH = path.join(ROOT, "public", "sdrs", "assignments.json");
const LOADOUTS_PATH = path.join(ROOT, "public", "nfts", "variants", "_loadouts.json");
const OUT_DIR = path.join(ROOT, "public", "metadata");

const BASE_IMAGE_URI =
  process.env.NEXT_PUBLIC_BASE_IMAGE_URI ??
  "https://braintrust-collection.vercel.app";

const VARIANTS_PER_SDR = 3;

// Rarity tiers per variant index. Pre-generated, not random on chain.
const VARIANT_TIERS = ["Common", "Rare", "Mythic"] as const;
// File-name suffix for each tier (lowercased).
const VARIANT_FILE_TIER = ["common", "rare", "mythic"] as const;

type Person = { slug: string; name: string; trait?: string };
type Rarity = { tier: string; rank: number; score: number };
type Assignment = { slug: string; items: string[] };

type PerTierLoadouts = Record<string, { common: string[]; rare: string[]; mythic: string[] }>;

function load() {
  const people: Person[] = JSON.parse(fs.readFileSync(PEOPLE_PATH, "utf-8"));
  const rarity: Record<string, Rarity> = JSON.parse(fs.readFileSync(RARITY_PATH, "utf-8"));
  const assignments: { sdrs: Assignment[] } = fs.existsSync(ASSIGN_PATH)
    ? JSON.parse(fs.readFileSync(ASSIGN_PATH, "utf-8"))
    : { sdrs: [] };
  const accByslug: Record<string, string[]> = {};
  for (const a of assignments.sdrs) accByslug[a.slug] = a.items ?? [];

  // Per-tier loadouts emitted by generate_variant_artwork.py. Authoritative.
  const tierLoadouts: PerTierLoadouts = fs.existsSync(LOADOUTS_PATH)
    ? JSON.parse(fs.readFileSync(LOADOUTS_PATH, "utf-8"))
    : {};

  return { people, rarity, accByslug, tierLoadouts };
}

const TIER_KEY = ["common", "rare", "mythic"] as const;

function metadataFor(
  p: Person,
  sdrIndex: number,
  variantIndex: number,
  rarity: Record<string, Rarity>,
  accByslug: Record<string, string[]>,
  tierLoadouts: PerTierLoadouts
) {
  const tokenId = sdrIndex * VARIANTS_PER_SDR + variantIndex;
  const r = rarity[p.slug];
  // Prefer per-tier loadouts (authoritative). Fall back to the legacy
  // single-loadout assignment if the loadouts file is missing.
  const tierKey = TIER_KEY[variantIndex];
  const accs =
    tierLoadouts[p.slug]?.[tierKey] ?? (variantIndex === 1 ? (accByslug[p.slug] ?? []) : []);
  const variantTier = VARIANT_TIERS[variantIndex];

  const attributes: { trait_type: string; value: string | number }[] = [
    { trait_type: "Name", value: p.name },
    { trait_type: "SDR Index", value: sdrIndex },
    { trait_type: "Variant", value: variantIndex + 1 },
    { trait_type: "Variants Total", value: VARIANTS_PER_SDR },
    { trait_type: "Variant Rarity", value: variantTier },
    { trait_type: "Edition", value: "Genesis" },
  ];
  if (r) {
    attributes.push({ trait_type: "Original Rarity", value: r.tier });
    attributes.push({ trait_type: "Original Rank", value: r.rank });
  }
  if (p.trait) attributes.push({ trait_type: "Trait Color", value: p.trait });
  for (const acc of accs) {
    const [item, color] = acc.split("__");
    attributes.push({ trait_type: `Accessory: ${item}`, value: color });
  }

  return {
    name: `${p.name} · Variant ${variantIndex + 1} of ${VARIANTS_PER_SDR} · #${String(tokenId).padStart(3, "0")}`,
    description:
      `Braintrust Collection: Genesis. ` +
      `Variant ${variantIndex + 1} of ${VARIANTS_PER_SDR} for ${p.name} (${variantTier} rarity). ` +
      `Wallet-bound coworker mint: only ${p.name}'s wallet can claim ${p.name}'s variants.`,
    image: `${BASE_IMAGE_URI}/nfts/variants/${p.slug}_${VARIANT_FILE_TIER[variantIndex]}.svg`,
    external_url: `https://braintrust-collection.vercel.app/gallery#${p.slug}`,
    attributes,
  };
}

function main() {
  const { people, rarity, accByslug, tierLoadouts } = load();

  // Wipe + rebuild only the per-token JSONs; preserve collection.json + _index.json (regenerated).
  fs.mkdirSync(OUT_DIR, { recursive: true });
  for (const f of fs.readdirSync(OUT_DIR)) {
    if (/^\d+\.json$/.test(f)) fs.unlinkSync(path.join(OUT_DIR, f));
  }

  const index: { tokenId: number; slug: string; variant: number; file: string }[] = [];

  for (let sdrIndex = 0; sdrIndex < people.length; sdrIndex++) {
    const p = people[sdrIndex];
    for (let v = 0; v < VARIANTS_PER_SDR; v++) {
      const tokenId = sdrIndex * VARIANTS_PER_SDR + v;
      const meta = metadataFor(p, sdrIndex, v, rarity, accByslug, tierLoadouts);
      const file = `${tokenId}.json`;
      fs.writeFileSync(path.join(OUT_DIR, file), JSON.stringify(meta, null, 2));
      index.push({ tokenId, slug: p.slug, variant: v + 1, file });
    }
    console.log(
      `  SDR ${String(sdrIndex).padStart(2, "0")} ${p.name.padEnd(22)} -> tokens ${sdrIndex * 3}, ${sdrIndex * 3 + 1}, ${sdrIndex * 3 + 2}`
    );
  }

  fs.writeFileSync(path.join(OUT_DIR, "_index.json"), JSON.stringify(index, null, 2));
  console.log(`\nwrote ${index.length} token metadata files to ${OUT_DIR}`);
}

main();
