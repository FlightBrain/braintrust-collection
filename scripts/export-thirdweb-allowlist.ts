/**
 * Convert an internal allowlist (CSV/JSON) into a thirdweb-friendly CSV.
 *
 * Output columns:
 *   address,maxClaimable,price,currencyAddress
 *
 * NOTE: thirdweb's import format has evolved over time. Verify the column
 * names match your version in the dashboard before uploading. If they don't,
 * edit OUT_HEADERS below.
 *
 * Usage:
 *   npm run export-thirdweb-allowlist
 *   npm run export-thirdweb-allowlist -- data/allowlist.csv data/allowlist.thirdweb.csv
 */
import fs from "node:fs";
import path from "node:path";

const inputPath = path.resolve(process.argv[2] ?? "data/allowlist.example.csv");
const outputPath = path.resolve(process.argv[3] ?? "data/allowlist.thirdweb.csv");

const NATIVE_TOKEN = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE";
const OUT_HEADERS = ["address", "maxClaimable", "price", "currencyAddress"];

if (!fs.existsSync(inputPath)) {
  console.error(`ERROR: input not found: ${inputPath}`);
  process.exit(1);
}

type Row = {
  wallet_address: string;
  max_claimable: number;
  price: number;
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
      wallet_address: obj.wallet_address,
      max_claimable: Number(obj.max_claimable),
      price: Number(obj.price),
    };
  });
}

function loadJson(filePath: string): Row[] {
  return JSON.parse(fs.readFileSync(filePath, "utf-8"));
}

const rows = inputPath.endsWith(".json") ? loadJson(inputPath) : loadCsv(inputPath);

const out: string[] = [OUT_HEADERS.join(",")];
for (const r of rows) {
  out.push(
    [r.wallet_address, r.max_claimable, r.price, NATIVE_TOKEN].join(",")
  );
}

fs.mkdirSync(path.dirname(outputPath), { recursive: true });
fs.writeFileSync(outputPath, out.join("\n") + "\n");

console.log(`Wrote ${rows.length} rows to ${outputPath}`);
console.log("");
console.log("TODO before upload: verify thirdweb's current CSV schema matches");
console.log("  columns: address, maxClaimable, price, currencyAddress");
