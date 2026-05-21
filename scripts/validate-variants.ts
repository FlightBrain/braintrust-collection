/**
 * Validate the variant artwork system end-to-end.
 *
 * Checks:
 *   - public/nfts/variants/ exists
 *   - each of 15 SDRs has 3 SVG files (common, rare, mythic) = 45 total
 *   - public/nfts/corporate/ is unchanged in count + still has the slug originals
 *   - each public/metadata/{0..44}.json points to an image that exists locally
 *   - no two tokens share the same image URL
 *   - no metadata image points to public/nfts/corporate/ anymore (we want variants)
 *
 * Usage:
 *   npm run validate-variants
 */
import fs from "node:fs";
import path from "node:path";

const ROOT = path.resolve(__dirname, "..");
const PEOPLE_PATH = path.join(ROOT, "public", "auto_people.json");
const META_DIR = path.join(ROOT, "public", "metadata");
const VARIANTS_DIR = path.join(ROOT, "public", "nfts", "variants");
const CORPORATE_DIR = path.join(ROOT, "public", "nfts", "corporate");

const TIERS = ["common", "rare", "mythic"] as const;

let errors = 0;
let warns = 0;

function err(msg: string) {
  console.log(`ERROR ${msg}`);
  errors++;
}
function warn(msg: string) {
  console.log(`WARN  ${msg}`);
  warns++;
}

if (!fs.existsSync(VARIANTS_DIR)) {
  err(`variants directory missing: ${VARIANTS_DIR}`);
  console.log(`Run: python3 generate_variant_artwork.py`);
  process.exit(1);
}

const people: { slug: string; name: string }[] = JSON.parse(
  fs.readFileSync(PEOPLE_PATH, "utf-8")
);

// 1. Every SDR has 3 variant SVGs
for (const p of people) {
  for (const tier of TIERS) {
    const expected = path.join(VARIANTS_DIR, `${p.slug}_${tier}.svg`);
    if (!fs.existsSync(expected)) {
      err(`missing variant SVG: ${expected}`);
    }
  }
}

// 2. Originals preserved
if (!fs.existsSync(CORPORATE_DIR)) {
  err(`originals directory missing: ${CORPORATE_DIR}`);
} else {
  for (const p of people) {
    const original = path.join(CORPORATE_DIR, `${p.slug}_nft.svg`);
    if (!fs.existsSync(original)) {
      err(`original SVG missing for ${p.slug}: ${original}`);
    }
  }
}

// 3. Every metadata file points to an existing variant SVG
const tokenFiles = fs
  .readdirSync(META_DIR)
  .filter((f) => /^\d+\.json$/.test(f))
  .sort((a, b) => parseInt(a) - parseInt(b));

if (tokenFiles.length !== 45) {
  warn(`expected 45 token metadata files, got ${tokenFiles.length}`);
}

const imageUrls = new Set<string>();
for (const f of tokenFiles) {
  const tokenId = parseInt(f);
  const d = JSON.parse(fs.readFileSync(path.join(META_DIR, f), "utf-8"));
  const img = d.image as string | undefined;

  if (!img) {
    err(`${f}: missing image field`);
    continue;
  }
  if (img.includes("/nfts/corporate/")) {
    err(
      `${f}: image still points at /nfts/corporate/. Should be /nfts/variants/ now.`
    );
  }
  if (imageUrls.has(img)) {
    err(`${f}: duplicate image URL ${img}`);
  }
  imageUrls.add(img);

  // Verify referenced local file exists
  const match = img.match(/\/nfts\/variants\/([^/?#]+\.svg)/);
  if (!match) {
    warn(`${f}: image URL is not a /nfts/variants/*.svg path: ${img}`);
    continue;
  }
  const local = path.join(VARIANTS_DIR, match[1]);
  if (!fs.existsSync(local)) {
    err(`${f}: referenced variant SVG does not exist: ${local}`);
  }

  // Token ID -> expected slug + tier
  const sdrIndex = Math.floor(tokenId / 3);
  const variantIdx = tokenId % 3;
  const expectedFile = `${people[sdrIndex].slug}_${TIERS[variantIdx]}.svg`;
  if (match[1] !== expectedFile) {
    err(
      `${f}: token ${tokenId} should reference ${expectedFile} but references ${match[1]}`
    );
  }
}

// 4. Sequential token ids 0..44
for (let i = 0; i < tokenFiles.length; i++) {
  if (parseInt(tokenFiles[i]) !== i) {
    err(`token id sequence broken at ${i} (got ${tokenFiles[i]})`);
    break;
  }
}

console.log(
  `\nVariant validation: ${errors} errors, ${warns} warnings, ${imageUrls.size} unique image URLs.`
);
process.exit(errors > 0 ? 1 : 0);
