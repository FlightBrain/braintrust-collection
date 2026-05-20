/**
 * Generates ERC-721 metadata JSON for each token in the collection.
 *
 * Reads existing per-SDR data:
 *   public/auto_people.json  (name, trait, accessories, etc.)
 *   public/rarity.json       (tier, rank, score)
 *   public/sdrs/assignments.json (each SDR's chosen accessories)
 *
 * Writes:
 *   public/metadata/{tokenId}.json    (one per token)
 *   public/metadata/_index.json       (collection-level index)
 *
 * Image URL: by default points at the local /nfts/corporate/{slug}_nft.svg.
 * For production, edit BASE_IMAGE_URI to an IPFS gateway URI (e.g.
 *   ipfs://<cid>/{slug}_nft.svg or https://<gateway>/ipfs/<cid>/{slug}_nft.svg).
 *
 * Does NOT touch any artwork. Only writes metadata JSON.
 */
import fs from "node:fs";
import path from "node:path";

const ROOT = path.resolve(__dirname, "..");
const PEOPLE_PATH = path.join(ROOT, "public", "auto_people.json");
const RARITY_PATH = path.join(ROOT, "public", "rarity.json");
const ASSIGN_PATH = path.join(ROOT, "public", "sdrs", "assignments.json");
const OUT_DIR = path.join(ROOT, "public", "metadata");

// Edit this for production. Use an IPFS URI once art is pinned.
const BASE_IMAGE_URI =
  process.env.NEXT_PUBLIC_BASE_IMAGE_URI ??
  "https://braintrust-collection.vercel.app";

type Person = { slug: string; name: string; trait?: string };
type Rarity = { tier: string; rank: number; score: number };
type Assignment = { slug: string; items: string[] };

function load() {
  const people: Person[] = JSON.parse(fs.readFileSync(PEOPLE_PATH, "utf-8"));
  const rarity: Record<string, Rarity> = JSON.parse(fs.readFileSync(RARITY_PATH, "utf-8"));
  const assignments: { sdrs: Assignment[] } = fs.existsSync(ASSIGN_PATH)
    ? JSON.parse(fs.readFileSync(ASSIGN_PATH, "utf-8"))
    : { sdrs: [] };
  const accByslug: Record<string, string[]> = {};
  for (const a of assignments.sdrs) accByslug[a.slug] = a.items ?? [];
  return { people, rarity, accByslug };
}

function metadataFor(p: Person, idx: number, rarity: Record<string, Rarity>, accByslug: Record<string, string[]>) {
  const tokenId = idx + 1;
  const r = rarity[p.slug];
  const accs = accByslug[p.slug] ?? [];

  const attributes: { trait_type: string; value: string | number }[] = [];
  if (r) {
    attributes.push({ trait_type: "Rarity", value: r.tier });
    attributes.push({ trait_type: "Rank", value: r.rank });
    attributes.push({ trait_type: "Score", value: r.score });
  }
  if (p.trait) attributes.push({ trait_type: "Trait Color", value: p.trait });
  attributes.push({ trait_type: "Edition", value: "Genesis" });
  for (const acc of accs) {
    const [item, color] = acc.split("__");
    attributes.push({ trait_type: `Accessory: ${item}`, value: color });
  }

  return {
    name: `${p.name} · Genesis #${String(tokenId).padStart(3, "0")}`,
    description:
      "Braintrust Collection: Genesis. 15 hand-pixeled collectible cards. " +
      "1 of 1, with hand-picked NFT accessories.",
    image: `${BASE_IMAGE_URI}/nfts/corporate/${p.slug}_nft.svg`,
    external_url: `https://braintrust-collection.vercel.app/gallery#${p.slug}`,
    attributes,
  };
}

function main() {
  const { people, rarity, accByslug } = load();
  fs.mkdirSync(OUT_DIR, { recursive: true });

  const index: { tokenId: number; slug: string; file: string }[] = [];

  for (let i = 0; i < people.length; i++) {
    const p = people[i];
    const meta = metadataFor(p, i, rarity, accByslug);
    const file = `${i + 1}.json`;
    fs.writeFileSync(path.join(OUT_DIR, file), JSON.stringify(meta, null, 2));
    index.push({ tokenId: i + 1, slug: p.slug, file });
    console.log(`  #${String(i + 1).padStart(3, "0")} ${p.name.padEnd(22)} -> metadata/${file}`);
  }

  fs.writeFileSync(path.join(OUT_DIR, "_index.json"), JSON.stringify(index, null, 2));
  console.log(`\nwrote ${people.length} token metadata files to ${OUT_DIR}`);
}

main();
