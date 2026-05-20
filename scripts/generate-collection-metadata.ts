/**
 * Generates collection-level metadata used by `contractURI()` on the deployed
 * contract. Conforms to the OpenSea metadata standard:
 *   https://docs.opensea.io/docs/contract-level-metadata
 *
 * Output: public/metadata/collection.json
 *
 * Required on-chain support: the deployed contract MUST implement
 *   function contractURI() public view returns (string memory)
 * pointing at this JSON (post-IPFS pin). If using thirdweb NFT Drop,
 * contractURI is supported out of the box and you set the metadata via the
 * thirdweb dashboard. For custom ERC-721s, add contractURI() before launch.
 *
 * Does NOT touch artwork.
 */
import fs from "node:fs";
import path from "node:path";

const ROOT = path.resolve(__dirname, "..");
const OUT_PATH = path.join(ROOT, "public", "metadata", "collection.json");

const BASE_IMAGE_URI =
  process.env.NEXT_PUBLIC_BASE_IMAGE_URI ??
  "https://braintrust-collection.vercel.app";
const COLLECTION_NAME =
  process.env.COLLECTION_NAME ?? "Braintrust Collection: Genesis";
const COLLECTION_DESCRIPTION =
  process.env.COLLECTION_DESCRIPTION ??
  "Braintrust Collection: Genesis. 15 hand-pixeled collectible cards. " +
    "The original Braintrust sales floor, kitted out with NFT accessories " +
    "chosen from a 157-variant catalog. Each card is a 1-of-1 with a unique " +
    "rarity tier.";
const EXTERNAL_LINK = process.env.COLLECTION_EXTERNAL_LINK ?? "https://braintrust-collection.vercel.app";
const FEE_RECIPIENT = process.env.NEXT_PUBLIC_FEE_RECIPIENT ?? "";
const SELLER_FEE_BPS = Number(process.env.NEXT_PUBLIC_SELLER_FEE_BPS ?? 500); // 5%

const collection = {
  name: COLLECTION_NAME,
  description: COLLECTION_DESCRIPTION,
  // Banner/logo for the collection on OpenSea, etc. For production this MUST
  // be an ipfs:// URL once art is pinned. The default points at the first
  // SVG until the deployer updates it.
  image: `${BASE_IMAGE_URI}/nfts/corporate/ryan_nft.svg`,
  external_link: EXTERNAL_LINK,
  // Secondary-sale royalty in basis points (100 = 1%, 500 = 5%, 1000 = 10%).
  // Marketplaces honor this where the contract supports ERC-2981.
  seller_fee_basis_points: SELLER_FEE_BPS,
  // Address that receives the secondary-sale royalty.
  // Must be set before launch.
  fee_recipient: FEE_RECIPIENT,
};

fs.mkdirSync(path.dirname(OUT_PATH), { recursive: true });
fs.writeFileSync(OUT_PATH, JSON.stringify(collection, null, 2));
console.log(`wrote ${OUT_PATH}`);
if (!FEE_RECIPIENT) {
  console.log(
    "  WARN: fee_recipient is empty. Set NEXT_PUBLIC_FEE_RECIPIENT before launch."
  );
}
if (BASE_IMAGE_URI.startsWith("http")) {
  console.log(
    "  WARN: image is an HTTP URL, not ipfs://. Re-run after IPFS pin for production."
  );
}
