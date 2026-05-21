import { env, hasContract } from "./env";
import { isTestnet } from "./chains";

/**
 * High-level launch status. Drives UI copy + admin dashboard.
 */
export type LaunchStatus =
  | "LOCAL_DEV"
  | "TESTNET_READY_NO_CONTRACT"
  | "TESTNET_CONTRACT_CONFIGURED"
  | "MAINNET_BLOCKED_LEGAL"
  | "MAINNET_READY_TECHNICAL_ONLY"
  | "MAINNET_LIVE";

export const LAUNCH_STATUS_LABELS: Record<LaunchStatus, string> = {
  LOCAL_DEV: "Local development",
  TESTNET_READY_NO_CONTRACT: "Testnet preview, contract pending",
  TESTNET_CONTRACT_CONFIGURED: "Testnet live",
  MAINNET_BLOCKED_LEGAL: "Mainnet blocked by legal approvals",
  MAINNET_READY_TECHNICAL_ONLY: "Mainnet technically ready, awaiting launch",
  MAINNET_LIVE: "Mainnet live",
};

// Legal blockers we know about. These must be resolved before any mainnet
// announcement. Update this list only when an item is explicitly cleared.
export const LEGAL_BLOCKERS = [
  {
    id: "employee-likeness-consent",
    label: "Employee likeness consent",
    description:
      "Written consent from each of the 15 depicted Braintrust employees.",
    cleared: false,
  },
  {
    id: "braintrust-brand-approval",
    label: "Braintrust brand approval",
    description:
      "Sign-off on use of the Braintrust name, logo, and sales-floor framing.",
    cleared: false,
  },
] as const;

export function legalBlockersOutstanding(): number {
  return LEGAL_BLOCKERS.filter((b) => !b.cleared).length;
}

export function computeLaunchStatus(): LaunchStatus {
  const testnet = isTestnet(env.chainId);
  const contractReady = hasContract();
  const legalOpen = legalBlockersOutstanding() > 0;

  if (testnet && !contractReady) return "TESTNET_READY_NO_CONTRACT";
  if (testnet && contractReady) return "TESTNET_CONTRACT_CONFIGURED";

  // Mainnet path
  if (!contractReady && legalOpen) return "MAINNET_BLOCKED_LEGAL";
  if (!contractReady) return "MAINNET_BLOCKED_LEGAL";
  if (legalOpen) return "MAINNET_BLOCKED_LEGAL";
  return "MAINNET_LIVE";
}

/**
 * Compact safe-to-show status for the admin/status page + /api/status.
 * Never includes secrets.
 */
export function publicStatusSummary() {
  const status = computeLaunchStatus();
  return {
    status,
    label: LAUNCH_STATUS_LABELS[status],
    chain: {
      id: env.chainId,
      name: env.chainName,
      testnet: isTestnet(env.chainId),
    },
    contractConfigured: hasContract(),
    // Mask address: only show prefix + length parity check
    contractAddressPreview: env.contractAddress
      ? `${env.contractAddress.slice(0, 6)}...${env.contractAddress.slice(-4)}`
      : null,
    walletConnectConfigured: !!env.walletConnectProjectId,
    marketplaceConfigured: !!env.marketplaceUrl,
    feeRecipientConfigured: !!process.env.NEXT_PUBLIC_FEE_RECIPIENT,
    baseImageUriIsIpfs:
      (process.env.NEXT_PUBLIC_BASE_IMAGE_URI ?? "").startsWith("ipfs://"),
    totalSupply: env.totalSupply,
    mintPriceEth: env.mintPriceEth,
    legalBlockersOpen: legalBlockersOutstanding(),
  };
}
