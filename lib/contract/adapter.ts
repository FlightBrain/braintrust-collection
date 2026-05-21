import { thirdwebDropAdapter } from "./thirdwebDrop";
import { customErc721Adapter } from "./customErc721";
import type { ContractAdapter, ContractMode } from "./types";

const mode = (process.env.NEXT_PUBLIC_CONTRACT_MODE as ContractMode | undefined)
  ?? "thirdweb-drop";

export const contractAdapter: ContractAdapter =
  mode === "custom-erc721" ? customErc721Adapter : thirdwebDropAdapter;

export const contractMode: ContractMode = mode;

export { thirdwebDropAdapter, customErc721Adapter };
export type { ContractAdapter, ContractMode };
