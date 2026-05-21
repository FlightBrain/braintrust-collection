/**
 * Environment health check. Warns about missing or suspicious env values.
 * Never fails the build unless STRICT=1 is set (used by prelaunch:strict).
 *
 * Usage:
 *   npm run check-env
 *   STRICT=1 npm run check-env   (exits 1 on any warning)
 */
import "dotenv/config";

const strict = process.env.STRICT === "1";

type Issue = { level: "INFO" | "WARN" | "ERROR"; key: string; msg: string };
const issues: Issue[] = [];

function warn(key: string, msg: string) { issues.push({ level: "WARN", key, msg }); }
function err(key: string, msg: string) { issues.push({ level: "ERROR", key, msg }); }
function info(key: string, msg: string) { issues.push({ level: "INFO", key, msg }); }

const env = (k: string) => process.env[k] ?? "";

const chainId = Number(env("NEXT_PUBLIC_CHAIN_ID") || "0");
const ALLOWED_CHAINS = [1, 8453, 84532, 11155111];

// Chain ID
if (!env("NEXT_PUBLIC_CHAIN_ID")) {
  warn("NEXT_PUBLIC_CHAIN_ID", "missing. Defaults to Base mainnet (8453).");
} else if (!ALLOWED_CHAINS.includes(chainId)) {
  warn(
    "NEXT_PUBLIC_CHAIN_ID",
    `unexpected value "${chainId}". Allowed: ${ALLOWED_CHAINS.join(", ")}.`
  );
}

// Chain name
if (!env("NEXT_PUBLIC_CHAIN_NAME")) {
  warn("NEXT_PUBLIC_CHAIN_NAME", "missing. Display label will fall back.");
}

// RPC URL
if (!env("NEXT_PUBLIC_RPC_URL")) {
  warn("NEXT_PUBLIC_RPC_URL", "missing. Public default will be used.");
}

// WalletConnect
if (!env("NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID")) {
  warn(
    "NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID",
    "missing. WalletConnect/Reown wallets will not work. Default fallback in lib/env.ts may apply."
  );
}

// Contract address
const addr = env("NEXT_PUBLIC_CONTRACT_ADDRESS");
if (!addr) {
  info(
    "NEXT_PUBLIC_CONTRACT_ADDRESS",
    "missing. UI will show 'contract not yet deployed'. Set after deploy."
  );
} else if (!/^0x[0-9a-fA-F]{40}$/.test(addr)) {
  err(
    "NEXT_PUBLIC_CONTRACT_ADDRESS",
    `invalid format: "${addr}". Must be 0x + 40 hex chars.`
  );
}

// Total supply
const totalSupply = Number(env("NEXT_PUBLIC_TOTAL_SUPPLY") || "0");
if (!totalSupply || totalSupply <= 0) {
  warn(
    "NEXT_PUBLIC_TOTAL_SUPPLY",
    "missing or zero. Display fallback set to 15."
  );
}

// Mint price
const price = env("NEXT_PUBLIC_MINT_PRICE");
if (price === "" || isNaN(Number(price))) {
  warn(
    "NEXT_PUBLIC_MINT_PRICE",
    "missing or not a number. Free claims (0) will still work."
  );
}

// Marketplace
if (!env("NEXT_PUBLIC_MARKETPLACE_URL")) {
  info(
    "NEXT_PUBLIC_MARKETPLACE_URL",
    "blank. Sold-out state will not link out. Set after listing."
  );
}

// Base image URI
const baseImg = env("NEXT_PUBLIC_BASE_IMAGE_URI");
if (!baseImg) {
  info("NEXT_PUBLIC_BASE_IMAGE_URI", "blank. Metadata will use site default.");
} else if (chainId === 8453 && !baseImg.startsWith("ipfs://")) {
  warn(
    "NEXT_PUBLIC_BASE_IMAGE_URI",
    "mainnet is configured but image URI is not ipfs://. Pin to IPFS before launch."
  );
}

// Fee recipient
if (!env("NEXT_PUBLIC_FEE_RECIPIENT")) {
  warn(
    "NEXT_PUBLIC_FEE_RECIPIENT",
    "blank. Required for ERC-2981 royalty configuration before mainnet."
  );
}

// Report
const errs = issues.filter((i) => i.level === "ERROR");
const warns = issues.filter((i) => i.level === "WARN");
const infos = issues.filter((i) => i.level === "INFO");

console.log("=== Environment health check ===");
console.log(`  Chain: ${chainId || "(unset)"} ${env("NEXT_PUBLIC_CHAIN_NAME")}`);
console.log(`  Contract: ${addr ? addr.slice(0, 10) + "..." : "(unset)"}`);
console.log("");
for (const i of [...errs, ...warns, ...infos]) {
  console.log(`  ${i.level.padEnd(5)} ${i.key}: ${i.msg}`);
}
console.log("");
console.log(
  `  ${errs.length} errors, ${warns.length} warnings, ${infos.length} info.`
);

if (errs.length > 0) process.exit(1);
if (strict && warns.length > 0) {
  console.log("\nSTRICT mode: failing on warnings.");
  process.exit(1);
}
process.exit(0);
