/**
 * Validate an allowlist CSV or JSON file. Default path:
 *   data/allowlist.example.csv (so it can run in CI without real data)
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

type Row = {
  name_optional?: string;
  email_optional?: string;
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
      name_optional: obj.name_optional || undefined,
      email_optional: obj.email_optional || undefined,
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
const seen = new Set<string>();

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
  if (seen.has(addrLower)) {
    console.log(`ERROR line ${line}: duplicate wallet ${addrLower}`);
    errors++;
  }
  seen.add(addrLower);

  if (!Number.isFinite(r.max_claimable) || r.max_claimable <= 0) {
    console.log(`ERROR line ${line}: max_claimable must be a positive number`);
    errors++;
  }
  if (!Number.isFinite(r.price) || r.price < 0) {
    console.log(`ERROR line ${line}: price must be a non-negative number`);
    errors++;
  }
  if (r.price > 0) {
    console.log(
      `WARN  line ${line}: price > 0 (got ${r.price}). The coworker drop is supposed to be free.`
    );
    warns++;
  }

  if (r.email_optional) {
    console.log(
      `WARN  line ${line}: email present. Consider removing emails before uploading anywhere public.`
    );
    warns++;
  }
}

console.log(
  `\nValidated ${rows.length} rows. ${errors} errors, ${warns} warnings, ${seen.size} unique wallets.`
);

if (errors > 0) process.exit(1);
process.exit(0);
