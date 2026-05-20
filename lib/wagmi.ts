"use client";

import { getDefaultConfig } from "@rainbow-me/rainbowkit";
import { base, baseSepolia, mainnet } from "wagmi/chains";
import { http } from "viem";
import { env } from "./env";

// Pick the chain that matches NEXT_PUBLIC_CHAIN_ID. Default Base mainnet.
const chainMap: Record<number, (typeof base | typeof baseSepolia | typeof mainnet)> = {
  [base.id]: base,
  [baseSepolia.id]: baseSepolia,
  [mainnet.id]: mainnet,
};

const activeChain = chainMap[env.chainId] ?? base;

export const wagmiConfig = getDefaultConfig({
  appName: "Braintrust Collection",
  projectId: env.walletConnectProjectId || "00000000000000000000000000000000",
  chains: [activeChain],
  transports: {
    [activeChain.id]: http(env.rpcUrl),
  },
  ssr: true,
});

export { activeChain };
