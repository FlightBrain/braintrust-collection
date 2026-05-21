import type { ContractAdapter } from "./types";

/**
 * Placeholder adapter for a custom ERC-721 contract.
 *
 * Set NEXT_PUBLIC_CONTRACT_MODE=custom-erc721 to use it. The site assumes the
 * contract exposes `mint(uint256 quantity)` as a payable function. If your
 * contract uses a different name or signature, edit this file before launch.
 *
 * Required functions for the UI to render properly:
 *   - mint(uint256) payable
 *   - totalSupply() view returns (uint256)
 *   - maxSupply() view returns (uint256)
 *   - mintPrice() view returns (uint256)         [optional, falls back to env]
 *   - paused() view returns (bool)               [optional]
 *
 * Optional but recommended:
 *   - maxPerWallet() view returns (uint256)
 *   - contractURI() view returns (string)         [marketplace metadata]
 *   - royaltyInfo(uint256, uint256) (ERC-2981)    [creator earnings]
 */
const customErc721Abi = [
  {
    type: "function",
    name: "mint",
    stateMutability: "payable",
    inputs: [{ name: "quantity", type: "uint256" }],
    outputs: [],
  },
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
] as const;

export const customErc721Adapter: ContractAdapter = {
  mode: "custom-erc721",
  abi: customErc721Abi as unknown as ContractAdapter["abi"],
  isReady() {
    return true;
  },
  mintFunctionName: "mint",
  buildMintArgs({ quantity }) {
    return [quantity];
  },
  buildMintValue({ quantity, priceWei }) {
    return priceWei * quantity;
  },
  reads: {
    totalMinted: "totalSupply",
    maxSupply: "maxSupply",
    activeClaimConditionId: null,
    getClaimConditionById: null,
    paused: "paused",
  },
  capabilities: {
    allowlist: false,
    royalties: false,
    contractUri: false,
  },
};
