import { thirdwebDropAdapter } from "./thirdwebDrop";
import { customErc721Adapter } from "./customErc721";
import type { ContractAdapter, ContractMode } from "./types";

// "local-mock-drop" is an alias for thirdweb-drop because LocalMockDrop.sol
// implements the same ABI surface (claim + read functions). Using a separate
// mode name lets the admin/status page label the contract clearly.
const rawMode = (process.env.NEXT_PUBLIC_CONTRACT_MODE as string | undefined)
  ?? "thirdweb-drop";

const mode: ContractMode =
  rawMode === "custom-erc721"
    ? "custom-erc721"
    : rawMode === "placeholder"
    ? "placeholder"
    : "thirdweb-drop"; // covers thirdweb-drop AND local-mock-drop

export const contractAdapter: ContractAdapter =
  mode === "custom-erc721" ? customErc721Adapter : thirdwebDropAdapter;

export const contractMode: ContractMode = mode;
export const contractModeLabel: string = rawMode; // preserves "local-mock-drop" for display

export { thirdwebDropAdapter, customErc721Adapter };
export type { ContractAdapter, ContractMode };
