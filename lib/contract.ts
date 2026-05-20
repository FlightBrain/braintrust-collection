// thirdweb DropERC721 ABI shim, with the bits the mint UI uses.
//
// The canonical thirdweb DropERC721 `claim` function signature is:
//
//   function claim(
//     address receiver,
//     uint256 quantity,
//     address currency,
//     uint256 pricePerToken,
//     AllowlistProof calldata allowlistProof,
//     bytes memory data
//   ) external payable
//
// Where AllowlistProof is:
//
//   struct AllowlistProof {
//     bytes32[] proof;
//     uint256 quantityLimitPerWallet;
//     uint256 pricePerToken;
//     address currency;
//   }
//
// For a PUBLIC (open) claim phase with no allowlist, the proof is empty and
// the quantityLimitPerWallet / pricePerToken / currency fields are zeroed.
// The contract validates the actual claim against the active claim phase
// configured in the thirdweb dashboard.

export const NATIVE_TOKEN_ADDRESS =
  "0xEEeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE" as const;

// Empty allowlist proof, used for public claim phases.
export function makeEmptyAllowlistProof() {
  return {
    proof: [] as `0x${string}`[],
    quantityLimitPerWallet: 0n,
    pricePerToken: 0n,
    currency: NATIVE_TOKEN_ADDRESS as `0x${string}`,
  } as const;
}

export const collectionAbi = [
  // === Reads ===
  {
    type: "function",
    name: "totalSupply",
    stateMutability: "view",
    inputs: [],
    outputs: [{ type: "uint256" }],
  },
  // thirdweb DropERC721: max total claimable across all phases. Some contracts
  // expose this as nextTokenIdToMint() instead; we read both at the hook layer
  // and fall back to env.totalSupply if neither is present.
  {
    type: "function",
    name: "nextTokenIdToMint",
    stateMutability: "view",
    inputs: [],
    outputs: [{ type: "uint256" }],
  },
  {
    type: "function",
    name: "maxTotalSupply",
    stateMutability: "view",
    inputs: [],
    outputs: [{ type: "uint256" }],
  },
  // Active claim condition (price + max-per-wallet + supply for the current phase)
  {
    type: "function",
    name: "claimCondition",
    stateMutability: "view",
    inputs: [],
    outputs: [
      { name: "currentStartId", type: "uint256" },
      { name: "count", type: "uint256" },
    ],
  },
  {
    type: "function",
    name: "getActiveClaimConditionId",
    stateMutability: "view",
    inputs: [],
    outputs: [{ type: "uint256" }],
  },
  {
    type: "function",
    name: "getClaimConditionById",
    stateMutability: "view",
    inputs: [{ name: "conditionId", type: "uint256" }],
    outputs: [
      {
        components: [
          { name: "startTimestamp", type: "uint256" },
          { name: "maxClaimableSupply", type: "uint256" },
          { name: "supplyClaimed", type: "uint256" },
          { name: "quantityLimitPerWallet", type: "uint256" },
          { name: "merkleRoot", type: "bytes32" },
          { name: "pricePerToken", type: "uint256" },
          { name: "currency", type: "address" },
          { name: "metadata", type: "string" },
        ],
        name: "condition",
        type: "tuple",
      },
    ],
  },
  {
    type: "function",
    name: "paused",
    stateMutability: "view",
    inputs: [],
    outputs: [{ type: "bool" }],
  },
  // === Writes ===
  {
    type: "function",
    name: "claim",
    stateMutability: "payable",
    inputs: [
      { name: "receiver", type: "address" },
      { name: "quantity", type: "uint256" },
      { name: "currency", type: "address" },
      { name: "pricePerToken", type: "uint256" },
      {
        components: [
          { name: "proof", type: "bytes32[]" },
          { name: "quantityLimitPerWallet", type: "uint256" },
          { name: "pricePerToken", type: "uint256" },
          { name: "currency", type: "address" },
        ],
        name: "allowlistProof",
        type: "tuple",
      },
      { name: "data", type: "bytes" },
    ],
    outputs: [],
  },
] as const;
