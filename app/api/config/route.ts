import { NextResponse } from "next/server";
import { env, hasContract } from "@/lib/env";
import { isTestnet } from "@/lib/chains";
import { contractMode } from "@/lib/contract/adapter";

export const dynamic = "force-static";

/**
 * Public config endpoint. NO secrets exposed.
 */
export async function GET() {
  return NextResponse.json({
    chainId: env.chainId,
    chainName: env.chainName,
    testnet: isTestnet(env.chainId),
    contractMode,
    contractConfigured: hasContract(),
    totalSupply: env.totalSupply,
    mintPriceEth: env.mintPriceEth,
    marketplaceUrl: env.marketplaceUrl || null,
  });
}
