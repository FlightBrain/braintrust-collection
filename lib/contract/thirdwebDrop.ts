import { collectionAbi, makeEmptyAllowlistProof, NATIVE_TOKEN_ADDRESS } from "../contract";
import type { ContractAdapter } from "./types";

export const thirdwebDropAdapter: ContractAdapter = {
  mode: "thirdweb-drop",
  abi: collectionAbi as unknown as ContractAdapter["abi"],
  isReady() {
    // Address validation lives in lib/env.ts hasContract(); the page-level
    // code gates rendering before calling the adapter.
    return true;
  },
  mintFunctionName: "claim",
  buildMintArgs({ receiver, quantity, priceWei }) {
    const proof = makeEmptyAllowlistProof();
    return [
      receiver,
      quantity,
      NATIVE_TOKEN_ADDRESS,
      priceWei,
      proof,
      "0x" as `0x${string}`,
    ];
  },
  buildMintValue({ quantity, priceWei }) {
    return priceWei * quantity;
  },
  reads: {
    totalMinted: "nextTokenIdToMint",
    maxSupply: "maxTotalSupply",
    activeClaimConditionId: "getActiveClaimConditionId",
    getClaimConditionById: "getClaimConditionById",
    paused: "paused",
  },
  capabilities: {
    allowlist: true,
    royalties: true,
    contractUri: true,
  },
};
