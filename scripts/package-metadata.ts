/**
 * Bundle metadata for IPFS upload.
 *
 * Copies public/metadata/{1..15}.json + collection.json into
 *   dist/metadata-package/tokens/
 *   dist/metadata-package/collection.json
 * along with a _manifest.json and README-UPLOAD.md.
 *
 * METADATA_MODE controls validation:
 *   local   (default): image URLs can be HTTP
 *   ipfs              : image URLs must be ipfs://
 *   arweave           : image URLs must be ar:// or https://arweave.net/
 */
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";

const ROOT = path.resolve(__dirname, "..");
const META_DIR = path.join(ROOT, "public", "metadata");
const OUT_DIR = path.join(ROOT, "dist", "metadata-package");
const TOKENS_DIR = path.join(OUT_DIR, "tokens");
const MODE = (process.env.METADATA_MODE ?? "local") as "local" | "ipfs" | "arweave";

if (!fs.existsSync(META_DIR)) {
  console.error("ERROR: public/metadata does not exist. Run `npm run generate-metadata` first.");
  process.exit(1);
}

// Clean output
fs.rmSync(OUT_DIR, { recursive: true, force: true });
fs.mkdirSync(TOKENS_DIR, { recursive: true });

const tokenFiles = fs
  .readdirSync(META_DIR)
  .filter((f) => /^\d+\.json$/.test(f))
  .sort((a, b) => parseInt(a) - parseInt(b));

const warnings: string[] = [];
const checksums: Record<string, string> = {};

for (const file of tokenFiles) {
  const src = path.join(META_DIR, file);
  const dest = path.join(TOKENS_DIR, file);
  const txt = fs.readFileSync(src, "utf-8");
  fs.writeFileSync(dest, txt);
  checksums[file] = crypto.createHash("sha256").update(txt).digest("hex");

  // Validate image URL for the selected mode
  try {
    const data = JSON.parse(txt);
    const img = (data.image ?? "") as string;
    if (MODE === "ipfs" && !img.startsWith("ipfs://")) {
      warnings.push(`${file}: image is not ipfs:// (got ${img.slice(0, 60)})`);
    } else if (MODE === "arweave" && !(img.startsWith("ar://") || img.includes("arweave.net"))) {
      warnings.push(`${file}: image is not Arweave (got ${img.slice(0, 60)})`);
    } else if (MODE === "local" && img.startsWith("ipfs://")) {
      warnings.push(`${file}: image is ipfs:// in local mode (cosmetic only).`);
    }
  } catch {
    warnings.push(`${file}: failed to parse JSON`);
  }
}

// Copy collection.json
const collectionSrc = path.join(META_DIR, "collection.json");
if (fs.existsSync(collectionSrc)) {
  const dest = path.join(OUT_DIR, "collection.json");
  const txt = fs.readFileSync(collectionSrc, "utf-8");
  fs.writeFileSync(dest, txt);
  checksums["collection.json"] = crypto.createHash("sha256").update(txt).digest("hex");
} else {
  warnings.push("collection.json missing. Run `npm run collection-metadata`.");
}

const baseImageUri = process.env.NEXT_PUBLIC_BASE_IMAGE_URI ?? "";

const manifest = {
  collection_name: "Braintrust Collection: Genesis",
  generated_at: new Date().toISOString(),
  metadata_mode: MODE,
  base_image_uri: baseImageUri,
  token_count: tokenFiles.length,
  files: tokenFiles,
  collection_metadata_included: fs.existsSync(path.join(OUT_DIR, "collection.json")),
  warnings,
  sha256: checksums,
};

fs.writeFileSync(
  path.join(OUT_DIR, "_manifest.json"),
  JSON.stringify(manifest, null, 2)
);

const uploadDoc = `# IPFS upload instructions

This folder contains everything you need to pin to IPFS or Arweave.

## Folder layout

- \`tokens/{1..15}.json\`: per-token metadata
- \`collection.json\`: collection-level metadata (OpenSea-style)
- \`_manifest.json\`: generation timestamp, mode, checksums, warnings

## Upload order (do not swap)

1. **Pin the art folder first** (public/nfts/corporate). Copy the CID.
2. Re-run with the new art URI:
   \`\`\`
   NEXT_PUBLIC_BASE_IMAGE_URI=ipfs://<art-cid>/ METADATA_MODE=ipfs npm run generate-metadata && npm run collection-metadata && npm run package-metadata
   \`\`\`
3. Pin THIS folder's \`tokens/\` (or the whole folder). Copy the CID.
4. Set the contract \`baseURI\` to \`ipfs://<metadata-cid>/tokens/\`.
5. Set the contract \`contractURI\` to \`ipfs://<metadata-cid>/collection.json\`.
6. Test \`tokenURI(0)\` on the contract.
7. Refresh metadata on the marketplace.

## Mode used for this build

- \`METADATA_MODE=${MODE}\`
- \`NEXT_PUBLIC_BASE_IMAGE_URI=${baseImageUri || "(empty)"}\`
${warnings.length ? `\n## Warnings\n\n` + warnings.map((w) => `- ${w}`).join("\n") + "\n" : ""}
`;

fs.writeFileSync(path.join(OUT_DIR, "README-UPLOAD.md"), uploadDoc);

console.log(`Packaged ${tokenFiles.length} tokens to ${OUT_DIR}`);
console.log(`Mode: ${MODE}`);
if (warnings.length) {
  console.log(`\nWarnings:`);
  for (const w of warnings) console.log(`  - ${w}`);
}
