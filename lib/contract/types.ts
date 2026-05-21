import type { Abi } from "viem";

export type ContractMode = "thirdweb-drop" | "custom-erc721" | "placeholder";

export interface ContractAdapter {
  mode: ContractMode;
  /** ABI shipped to wagmi `useReadContract` / `useWriteContract`. */
  abi: Abi;
  /** Whether a usable contract address is configured. */
  isReady(): boolean;
  /** Function called by the MintCard write hook. */
  mintFunctionName: "claim" | "mint";
  /** Returns the args tuple for the mint write call. */
  buildMintArgs(opts: {
    receiver: `0x${string}`;
    quantity: bigint;
    priceWei: bigint;
  }): readonly unknown[];
  /** Returns msg.value for the mint write call. */
  buildMintValue(opts: { quantity: bigint; priceWei: bigint }): bigint;
  /** Functions the UI may call via wagmi useReadContract. */
  reads: {
    totalMinted: string | null;
    maxSupply: string | null;
    activeClaimConditionId: string | null;
    getClaimConditionById: string | null;
    paused: string | null;
  };
  /** Capabilities, used by the admin/status dashboard. */
  capabilities: {
    allowlist: boolean;
    royalties: boolean;
    contractUri: boolean;
  };
}
