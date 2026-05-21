/**
 * Central chain config used across the app. Keep this list small and
 * intentional. Adding a chain here also requires adding it to lib/wagmi.ts.
 */

export const CHAINS = {
  baseMainnet: {
    id: 8453,
    name: "Base",
    shortName: "Base",
    testnet: false,
    rpc: "https://mainnet.base.org",
    explorer: "https://basescan.org",
    nativeCurrency: { name: "Ether", symbol: "ETH", decimals: 18 },
  },
  baseSepolia: {
    id: 84532,
    name: "Base Sepolia",
    shortName: "Sepolia",
    testnet: true,
    rpc: "https://sepolia.base.org",
    explorer: "https://sepolia.basescan.org",
    nativeCurrency: { name: "Ether", symbol: "ETH", decimals: 18 },
  },
  ethereum: {
    id: 1,
    name: "Ethereum",
    shortName: "Ethereum",
    testnet: false,
    rpc: "https://ethereum-rpc.publicnode.com",
    explorer: "https://etherscan.io",
    nativeCurrency: { name: "Ether", symbol: "ETH", decimals: 18 },
  },
  ethereumSepolia: {
    id: 11155111,
    name: "Sepolia",
    shortName: "Sepolia",
    testnet: true,
    rpc: "https://ethereum-sepolia-rpc.publicnode.com",
    explorer: "https://sepolia.etherscan.io",
    nativeCurrency: { name: "Ether", symbol: "ETH", decimals: 18 },
  },
} as const;

export type ChainConfig = (typeof CHAINS)[keyof typeof CHAINS];

export function chainById(id: number): ChainConfig | undefined {
  return Object.values(CHAINS).find((c) => c.id === id);
}

export function isTestnet(id: number): boolean {
  return chainById(id)?.testnet ?? false;
}

export function explorerTxUrl(chainId: number, txHash: string): string {
  const c = chainById(chainId);
  return `${c?.explorer ?? CHAINS.baseMainnet.explorer}/tx/${txHash}`;
}

export function explorerAddressUrl(chainId: number, address: string): string {
  const c = chainById(chainId);
  return `${c?.explorer ?? CHAINS.baseMainnet.explorer}/address/${address}`;
}
