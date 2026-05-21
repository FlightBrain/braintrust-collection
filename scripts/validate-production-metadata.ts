/**
 * Strict pre-mainnet validator for metadata. Fails the build if anything
 * looks unsafe to ship.
 *
 * Run with:
 *   METADATA_MODE=ipfs npm run validate-production-metadata
 */
import fs from "node:fs";
import path from "node:path";

const ROOT = path.resolve(__dirname, "..");
const META_DIR = path.join(ROOT, "public", "metadata");
const MODE = process.env.METADATA_MODE ?? "ipfs";

if (!fs.existsSync(META_DIR)) {
  console.error("ERROR: public/metadata missing. Run `npm run generate-metadata` first.");
  process.exit(1);
}

let errors = 0;

const tokenFiles = fs
  .readdirSync(META_DIR)
  .filter((f) => /^\d+\.json$/.test(f))
  .sort((a, b) => parseInt(a) - parseInt(b));

if (tokenFiles.length === 0) {
  console.error("ERROR: no token metadata.");
  process.exit(1);
}

const names = new Set<string>();
const tokenIds = new Set<number>();

for (const f of tokenFiles) {
  const id = parseInt(f);
  if (tokenIds.has(id)) {
    console.log(`ERROR ${f}: duplicate token id ${id}`);
    errors++;
  }
  tokenIds.add(id);

  try {
    const d = JSON.parse(fs.readFileSync(path.join(META_DIR, f), "utf-8"));
    for (const k of ["name", "description", "image", "attributes"]) {
      if (d[k] === undefined || d[k] === null || d[k] === "") {
        console.log(`ERROR ${f}: missing ${k}`);
        errors++;
      }
    }
    if (typeof d.name === "string") {
      if (names.has(d.name)) {
        console.log(`ERROR ${f}: duplicate name "${d.name}"`);
        errors++;
      }
      names.add(d.name);
    }
    if (Array.isArray(d.attributes)) {
      for (let i = 0; i < d.attributes.length; i++) {
        const a = d.attributes[i];
        if (typeof a.trait_type !== "string") {
          console.log(`ERROR ${f}: attributes[${i}].trait_type not a string`);
          errors++;
        }
        if (a.value === undefined || a.value === null) {
          console.log(`ERROR ${f}: attributes[${i}].value null/undefined`);
          errors++;
        }
      }
    } else {
      console.log(`ERROR ${f}: attributes not an array`);
      errors++;
    }

    if (MODE === "ipfs") {
      if (typeof d.image === "string") {
        if (!d.image.startsWith("ipfs://")) {
          console.log(`ERROR ${f}: image is not ipfs://`);
          errors++;
        }
      }
    }
    if (typeof d.image === "string") {
      if (d.image.includes("localhost") || d.image.includes(".vercel.app/")) {
        console.log(`ERROR ${f}: image points to localhost/preview URL: ${d.image}`);
        errors++;
      }
    }
  } catch (e) {
    console.log(`ERROR ${f}: JSON parse failed: ${(e as Error).message}`);
    errors++;
  }
}

// Sequential ids
const sortedIds = [...tokenIds].sort((a, b) => a - b);
for (let i = 0; i < sortedIds.length; i++) {
  if (sortedIds[i] !== i + 1) {
    console.log(`ERROR: token id sequence broken at ${i + 1} (got ${sortedIds[i]})`);
    errors++;
    break;
  }
}

// Collection metadata
const cPath = path.join(META_DIR, "collection.json");
if (!fs.existsSync(cPath)) {
  console.log(`ERROR collection.json missing.`);
  errors++;
} else {
  const c = JSON.parse(fs.readFileSync(cPath, "utf-8"));
  const reqs = ["name", "description", "image", "external_link", "seller_fee_basis_points", "fee_recipient"] as const;
  for (const k of reqs) {
    if (c[k] === undefined || c[k] === null || c[k] === "" || (k === "seller_fee_basis_points" && typeof c[k] !== "number")) {
      console.log(`ERROR collection.json: missing ${k}`);
      errors++;
    }
  }
  if (MODE === "ipfs" && typeof c.image === "string" && !c.image.startsWith("ipfs://")) {
    console.log(`ERROR collection.json: image is not ipfs://`);
    errors++;
  }
  if (typeof c.image === "string" && (c.image.includes("localhost") || c.image.includes(".vercel.app/"))) {
    console.log(`ERROR collection.json: image points to localhost/preview URL`);
    errors++;
  }
}

console.log(`\nStrict validation: ${errors} errors.`);
if (errors > 0) process.exit(1);
console.log("OK to upload.");
process.exit(0);
