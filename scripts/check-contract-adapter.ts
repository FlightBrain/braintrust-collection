/**
 * Smoke-tests the contract adapter without touching a real contract.
 * Confirms the configured adapter produces sensible args and config.
 */
import "dotenv/config";
import { contractAdapter, contractMode, thirdwebDropAdapter, customErc721Adapter } from "../lib/contract/adapter";

console.log("=== Contract adapter check ===");
console.log(`  Mode (NEXT_PUBLIC_CONTRACT_MODE): ${contractMode}`);
console.log(`  Active adapter: ${contractAdapter.mode}`);
console.log(`  Mint function: ${contractAdapter.mintFunctionName}`);
console.log(`  Capabilities:`);
for (const [k, v] of Object.entries(contractAdapter.capabilities)) {
  console.log(`    - ${k}: ${v}`);
}
console.log(`  Reads:`);
for (const [k, v] of Object.entries(contractAdapter.reads)) {
  console.log(`    - ${k}: ${v ?? "(not supported)"}`);
}

const receiver = "0x1234567890123456789012345678901234567890" as const;
console.log("\n  Sample mint call:");

const args1 = thirdwebDropAdapter.buildMintArgs({
  receiver,
  quantity: 1n,
  priceWei: 0n,
});
console.log(`  thirdweb-drop:  args[0..2]=[${args1[0]}, ${args1[1]}, ${args1[2]}]`);

const args2 = customErc721Adapter.buildMintArgs({
  receiver,
  quantity: 1n,
  priceWei: 0n,
});
console.log(`  custom-erc721:  args=[${args2[0]}]`);

const value = contractAdapter.buildMintValue({ quantity: 2n, priceWei: parseEth("0.001") });
console.log(`\n  Sample value for 2 @ 0.001 ETH: ${value} wei`);

function parseEth(s: string): bigint {
  // tiny parser: only handles up to 18 decimals
  const [whole, frac = ""] = s.split(".");
  const f = (frac + "0".repeat(18)).slice(0, 18);
  return BigInt(whole) * 10n ** 18n + BigInt(f);
}

console.log("\nAdapter check passed.");
process.exit(0);
