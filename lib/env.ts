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
  // WalletConnect/Reown project ID. Public-safe (identifies the dApp, not the
  // user). Default below is the project for this collection; override via env.
  walletConnectProjectId:
    process.env.NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID ||
    "1244257340c4eca87602fb431b8ec3a9",
} as const;

export const hasContract = () =>
  !!env.contractAddress && /^0x[0-9a-fA-F]{40}$/.test(env.contractAddress);

// Block explorer base URL for the active chain. Used for success-tx links.
export function explorerUrlFor(chainId: number): string {
  switch (chainId) {
    case 8453:   return "https://basescan.org";       // Base mainnet
    case 84532:  return "https://sepolia.basescan.org"; // Base Sepolia
    case 1:      return "https://etherscan.io";
    case 11155111: return "https://sepolia.etherscan.io";
    default:     return "https://basescan.org";
  }
}

export function explorerTxUrl(chainId: number, txHash: string): string {
  return `${explorerUrlFor(chainId)}/tx/${txHash}`;
}

export function explorerAddressUrl(chainId: number, address: string): string {
  return `${explorerUrlFor(chainId)}/address/${address}`;
}
