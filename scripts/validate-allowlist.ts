/**
 * Validate an allowlist CSV or JSON file.
 *
 * Required columns/keys:
 *   name           (optional)
 *   slug           REQUIRED. One of the 15 SDR slugs from public/auto_people.json.
 *   wallet_address REQUIRED. 0x + 40 hex chars.
 *   max_claimable  REQUIRED. Must be 1..3 (3 for the free coworker drop).
 *   price          REQUIRED. Must be 0 for the coworker drop.
 *   notes_optional (optional)
 *
 * Usage:
 *   npm run validate-allowlist
 *   npm run validate-allowlist -- data/allowlist.csv
 */
import fs from "node:fs";
import path from "node:path";

const input = process.argv[2] ?? "data/allowlist.example.csv";
const abs = path.resolve(input);

if (!fs.existsSync(abs)) {
  console.error(`ERROR: file not found: ${abs}`);
  process.exit(1);
}

const peoplePath = path.join(process.cwd(), "public", "auto_people.json");
const KNOWN_SLUGS: Set<string> = new Set(
  (JSON.parse(fs.readFileSync(peoplePath, "utf-8")) as { slug: string }[]).map(
    (p) => p.slug
  )
);

type Row = {
  name?: string;
  slug: string;
  wallet_address: string;
  max_claimable: number;
  price: number;
  notes_optional?: string;
};

function loadCsv(filePath: string): Row[] {
  const txt = fs.readFileSync(filePath, "utf-8").trim();
  const [headerLine, ...lines] = txt.split(/\r?\n/);
  const headers = headerLine.split(",").map((h) => h.trim());
  return lines.map((line) => {
    const cols = line.split(",").map((c) => c.trim());
    const obj: Record<string, string> = {};
    for (let i = 0; i < headers.length; i++) obj[headers[i]] = cols[i] ?? "";
    return {
      name: obj.name || obj.name_optional || undefined,
      slug: obj.slug,
      wallet_address: obj.wallet_address,
      max_claimable: Number(obj.max_claimable),
      price: Number(obj.price),
      notes_optional: obj.notes_optional || undefined,
    };
  });
}

function loadJson(filePath: string): Row[] {
  return JSON.parse(fs.readFileSync(filePath, "utf-8"));
}

const rows = abs.endsWith(".json") ? loadJson(abs) : loadCsv(abs);

let errors = 0;
let warns = 0;
const seenWallets = new Set<string>();

for (let i = 0; i < rows.length; i++) {
  const r = rows[i];
  const line = i + 2; // header is line 1

  if (!r.wallet_address) {
    console.log(`ERROR line ${line}: wallet_address missing`);
    errors++;
    continue;
  }
  if (!/^0x[0-9a-fA-F]{40}$/.test(r.wallet_address)) {
    console.log(`ERROR line ${line}: invalid wallet "${r.wallet_address}"`);
    errors++;
    continue;
  }
  const addrLower = r.wallet_address.toLowerCase();
  if (seenWallets.has(addrLower)) {
    console.log(`ERROR line ${line}: duplicate wallet ${addrLower}`);
    errors++;
  }
  seenWallets.add(addrLower);

  if (!r.slug) {
    console.log(`ERROR line ${line}: slug missing (must be one of the 15 SDR slugs)`);
    errors++;
  } else if (!KNOWN_SLUGS.has(r.slug)) {
    console.log(
      `ERROR line ${line}: slug "${r.slug}" not in public/auto_people.json. Known: ${[...KNOWN_SLUGS].join(", ")}`
    );
    errors++;
  }

  if (!Number.isFinite(r.max_claimable) || r.max_claimable < 1 || r.max_claimable > 3) {
    console.log(
      `ERROR line ${line}: max_claimable must be 1, 2, or 3 (got ${r.max_claimable})`
    );
    errors++;
  }
  if (!Number.isFinite(r.price) || r.price < 0) {
    console.log(`ERROR line ${line}: price must be a non-negative number`);
    errors++;
  }
  if (r.price > 0) {
    console.log(
      `WARN  line ${line}: price > 0 (got ${r.price}). Coworker drop is supposed to be free.`
    );
    warns++;
  }
}

// Group by slug to confirm no slug is over-allocated
const perSlug: Record<string, number> = {};
for (const r of rows) {
  const add = Number.isFinite(r.max_claimable) ? r.max_claimable : 0;
  perSlug[r.slug] = (perSlug[r.slug] ?? 0) + add;
}
for (const [slug, total] of Object.entries(perSlug)) {
  if (total > 3) {
    console.log(
      `WARN  slug "${slug}" is allocated to multiple wallets totaling ${total} variants (only 3 exist on chain).`
    );
    warns++;
  }
}

console.log(
  `\nValidated ${rows.length} rows. ${errors} errors, ${warns} warnings, ${seenWallets.size} unique wallets.`
);

if (errors > 0) process.exit(1);
process.exit(0);
