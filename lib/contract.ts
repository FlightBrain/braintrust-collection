// ERC-721 + common drop-style ABI. Generic enough to work with thirdweb
// NFT Drop, OpenZeppelin ERC721, and most ERC721A clones. Functions that a
// given contract doesn't expose just won't be read (we guard with try/catch
// at the hook layer).
//
// IMPORTANT: This file is a thin ABI shim. The actual contract address is
// loaded from NEXT_PUBLIC_CONTRACT_ADDRESS at runtime via lib/env.ts.

export const collectionAbi = [
  // Reads
  {
    type: "function",
    name: "totalSupply",
    stateMutability: "view",
    inputs: [],
    outputs: [{ type: "uint256" }],
  },
  {
    type: "function",
    name: "maxSupply",
    stateMutability: "view",
    inputs: [],
    outputs: [{ type: "uint256" }],
  },
  {
    type: "function",
    name: "price",
    stateMutability: "view",
    inputs: [],
    outputs: [{ type: "uint256" }],
  },
  {
    type: "function",
    name: "mintPrice",
    stateMutability: "view",
    inputs: [],
    outputs: [{ type: "uint256" }],
  },
  {
    type: "function",
    name: "paused",
    stateMutability: "view",
    inputs: [],
    outputs: [{ type: "bool" }],
  },
  {
    type: "function",
    name: "maxPerWallet",
    stateMutability: "view",
    inputs: [],
    outputs: [{ type: "uint256" }],
  },
  // Writes
  {
    type: "function",
    name: "mint",
    stateMutability: "payable",
    inputs: [{ type: "uint256", name: "quantity" }],
    outputs: [],
  },
  {
    type: "function",
    name: "claim",
    stateMutability: "payable",
    inputs: [{ type: "uint256", name: "quantity" }],
    outputs: [],
  },
] as const;

export type MintFnName = "mint" | "claim";
