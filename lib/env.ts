// Typed env loader. All vars are NEXT_PUBLIC_* so they ship to the browser.
// Defaults match Base mainnet (chain id 8453). Override via .env.local.

export const env = {
  chainId: Number(process.env.NEXT_PUBLIC_CHAIN_ID ?? 8453),
  chainName: process.env.NEXT_PUBLIC_CHAIN_NAME ?? "Base",
  contractAddress: (process.env.NEXT_PUBLIC_CONTRACT_ADDRESS ?? "") as `0x${string}` | "",
  totalSupply: Number(process.env.NEXT_PUBLIC_TOTAL_SUPPLY ?? 15),
  mintPriceEth: process.env.NEXT_PUBLIC_MINT_PRICE ?? "0", // in ETH, e.g. "0.005"
  marketplaceUrl: process.env.NEXT_PUBLIC_MARKETPLACE_URL ?? "",
  rpcUrl: process.env.NEXT_PUBLIC_RPC_URL ?? "https://mainnet.base.org",
  walletConnectProjectId:
    process.env.NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID ?? "",
} as const;

export const hasContract = () =>
  !!env.contractAddress && /^0x[0-9a-fA-F]{40}$/.test(env.contractAddress);
