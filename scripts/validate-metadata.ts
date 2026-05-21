/**
 * Validates every per-token metadata JSON in public/metadata/.
 *
 * Checks per file:
 *   - Required fields: name, description, image, attributes
 *   - attributes is an array of { trait_type, value } objects
 *   - image is non-empty
 *   - if image is a relative URL or starts with the local dev host, warn that
 *     it must be replaced with ipfs:// before launch
 *   - if image starts with ipfs:// or https://ipfs/, confirm CIDv1 format
 *   - confirm the referenced artwork file exists (when image is local)
 *
 * Checks across files:
 *   - Token IDs are sequential 1..N
 *   - File count matches NEXT_PUBLIC_TOTAL_SUPPLY (warn only)
 *
 * Exits non-zero on any hard error so CI/scripts can catch issues.
 */
import fs from "node:fs";
import path from "node:path";

const ROOT = path.resolve(__dirname, "..");
const META_DIR = path.join(ROOT, "public", "metadata");
const NFTS_DIR = path.join(ROOT, "public", "nfts", "corporate");

const expectedSupply = Number(process.env.NEXT_PUBLIC_TOTAL_SUPPLY ?? 15);

type Result = { file: string; errors: string[]; warnings: string[] };

function isCidV1Base32(cid: string): boolean {
  // base32 CIDv1 is lowercase, alphabet a-z + 2-7, prefix "b"
  return /^b[a-z2-7]{58,}$/.test(cid);
}

function validateOne(file: string): Result {
  const filePath = path.join(META_DIR, file);
  const errors: string[] = [];
  const warnings: string[] = [];
  let data: Record<string, unknown>;
  try {
    data = JSON.parse(fs.readFileSync(filePath, "utf-8"));
  } catch (e) {
    return { file, errors: [`JSON parse failed: ${(e as Error).message}`], warnings: [] };
  }

  for (const key of ["name", "description", "image", "attributes"] as const) {
    if (data[key] === undefined || data[key] === null || data[key] === "") {
      errors.push(`missing required field "${key}"`);
    }
  }

  if (!Array.isArray(data.attributes)) {
    errors.push(`"attributes" must be an array`);
  } else {
    for (let i = 0; i < data.attributes.length; i++) {
      const a = data.attributes[i] as Record<string, unknown>;
      if (typeof a !== "object" || a === null) {
        errors.push(`attributes[${i}] not an object`);
        continue;
      }
      if (typeof a.trait_type !== "string") errors.push(`attributes[${i}].trait_type missing or not string`);
      if (!("value" in a)) errors.push(`attributes[${i}].value missing`);
    }
  }

  const image = data.image as string | undefined;
  if (typeof image === "string") {
    if (image.startsWith("ipfs://")) {
      // ipfs://<cid>[/<path>]
      const cid = image.slice("ipfs://".length).split("/")[0];
      if (!isCidV1Base32(cid)) {
        warnings.push(`image CID "${cid}" is not CIDv1 base32. CIDv1 is recommended for marketplace compatibility.`);
      }
    } else if (image.startsWith("http://") || image.startsWith("https://")) {
      if (!image.includes("ipfs")) {
        warnings.push(`image is an HTTP URL, not ipfs://. Replace with ipfs:// before mainnet launch.`);
      }
    } else if (image.startsWith("/")) {
      warnings.push(`image is a local path. Replace with ipfs:// before mainnet launch.`);
    }

    // Verify local file exists when applicable
    if (image.includes("/nfts/corporate/")) {
      const filename = image.split("/nfts/corporate/")[1].split("?")[0];
      const local = path.join(NFTS_DIR, filename);
      if (!fs.existsSync(local)) {
        errors.push(`referenced artwork file does not exist: ${local}`);
      }
    }
  }

  return { file, errors, warnings };
}

function main() {
  if (!fs.existsSync(META_DIR)) {
    console.error(`ERROR: ${META_DIR} does not exist. Run \`npm run metadata\` first.`);
    process.exit(1);
  }

  const files = fs
    .readdirSync(META_DIR)
    .filter((f) => /^\d+\.json$/.test(f))
    .sort((a, b) => parseInt(a) - parseInt(b));

  if (files.length === 0) {
    console.error(`ERROR: no per-token metadata found in ${META_DIR}. Run \`npm run metadata\` first.`);
    process.exit(1);
  }

  let totalErrors = 0;
  let totalWarnings = 0;
  for (const f of files) {
    const r = validateOne(f);
    if (r.errors.length || r.warnings.length) {
      console.log(`\n${f}`);
      for (const e of r.errors) {
        console.log(`  ERROR: ${e}`);
        totalErrors++;
      }
      for (const w of r.warnings) {
        console.log(`  WARN:  ${w}`);
        totalWarnings++;
      }
    }
  }

  // Sequential token IDs (accept either 0-based or 1-based start)
  const ids = files.map((f) => parseInt(f)).sort((a, b) => a - b);
  const start = ids[0];
  if (start !== 0 && start !== 1) {
    console.log(`\nERROR: token IDs must start at 0 or 1. First id: ${start}.`);
    totalErrors++;
  } else {
    for (let i = 0; i < ids.length; i++) {
      if (ids[i] !== start + i) {
        console.log(`\nERROR: token ID sequence broken at index ${i}. Expected ${start + i}, got ${ids[i]}.`);
        totalErrors++;
        break;
      }
    }
  }

  if (ids.length !== expectedSupply) {
    console.log(
      `\nWARN: metadata count (${ids.length}) does not match NEXT_PUBLIC_TOTAL_SUPPLY (${expectedSupply}).`
    );
    totalWarnings++;
  }

  console.log(
    `\nValidated ${files.length} token metadata files. ${totalErrors} errors, ${totalWarnings} warnings.`
  );

  // Collection-level metadata (optional but recommended)
  const collectionPath = path.join(META_DIR, "collection.json");
  if (!fs.existsSync(collectionPath)) {
    console.log(`\nWARN: collection.json missing. Run \`npm run collection-metadata\` to generate it.`);
  } else {
    const c = JSON.parse(fs.readFileSync(collectionPath, "utf-8"));
    const required = ["name", "description", "image", "external_link", "seller_fee_basis_points", "fee_recipient"];
    const missing = required.filter((k) => !c[k] && c[k] !== 0);
    if (missing.length) {
      console.log(`\nCollection metadata is missing: ${missing.join(", ")}`);
      totalWarnings += missing.length;
    } else {
      console.log(`Collection metadata OK.`);
    }
  }

  process.exit(totalErrors > 0 ? 1 : 0);
}

main();
