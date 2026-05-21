"use client";

/**
 * Mock-only renderer for every MintCard state. Used by /dev/mint-states.
 *
 * This component reuses the same visual primitives as MintCard but never calls
 * any contract write, never connects a wallet, never reads env.contractAddress
 * for live data. It is safe to render anywhere.
 */

export type MockState =
  | "disconnected"
  | "connected"
  | "wrong-network"
  | "missing-contract"
  | "allowlist-only"
  | "not-allowlisted"
  | "paused"
  | "live-free"
  | "live-paid"
  | "sold-out"
  | "pending-tx"
  | "success"
  | "rejected"
  | "insufficient-funds"
  | "sale-not-started"
  | "metadata-pending"
  | "marketplace-pending";

const TITLE: Record<MockState, string> = {
  disconnected: "Disconnected",
  connected: "Connected (ready to mint)",
  "wrong-network": "Wrong network",
  "missing-contract": "Contract not yet deployed",
  "allowlist-only": "Allowlisted wallets only",
  "not-allowlisted": "Wallet not on allowlist",
  paused: "Sale paused",
  "live-free": "Live (free claim)",
  "live-paid": "Live (paid claim)",
  "sold-out": "Sold out",
  "pending-tx": "Transaction pending",
  success: "Minted!",
  rejected: "Transaction rejected",
  "insufficient-funds": "Insufficient funds",
  "sale-not-started": "Sale not started",
  "metadata-pending": "Metadata pending",
  "marketplace-pending": "Marketplace pending",
};

const TONE: Record<MockState, "info" | "warn" | "error" | "success" | "dim" | "neutral"> = {
  disconnected: "neutral",
  connected: "neutral",
  "wrong-network": "warn",
  "missing-contract": "warn",
  "allowlist-only": "warn",
  "not-allowlisted": "error",
  paused: "dim",
  "live-free": "neutral",
  "live-paid": "neutral",
  "sold-out": "dim",
  "pending-tx": "info",
  success: "success",
  rejected: "error",
  "insufficient-funds": "error",
  "sale-not-started": "dim",
  "metadata-pending": "info",
  "marketplace-pending": "dim",
};

const BODY: Record<MockState, string> = {
  disconnected: "Connect your wallet to continue.",
  connected: "Free for coworkers. 1 per wallet.",
  "wrong-network": "You are connected to a network we do not support yet. Switch to Base Sepolia to continue.",
  "missing-contract": "The mint contract has not been configured. Once it is deployed, this state goes away automatically.",
  "allowlist-only": "This drop is allowlisted. Only invited wallets can mint right now.",
  "not-allowlisted": "Your wallet is not on the allowlist for this drop. If you think this is a mistake, reach out to the team.",
  paused: "Minting is temporarily paused. Check back soon.",
  "live-free": "Free for coworkers. 1 per wallet.",
  "live-paid": "Open mint. Approve the transaction in your wallet to claim.",
  "sold-out": "Every card in this drop has been minted. Check the marketplace for resales.",
  "pending-tx": "Waiting for your transaction to confirm. This usually takes a few seconds.",
  success: "Your card is on its way to your wallet. Open the explorer to confirm.",
  rejected: "You rejected the transaction. No charge.",
  "insufficient-funds": "Your wallet does not have enough ETH to cover gas. Top up and try again.",
  "sale-not-started": "The public sale has not started yet.",
  "metadata-pending": "We are still pinning metadata to IPFS. The art is ready, the metadata is on its way.",
  "marketplace-pending": "The marketplace listing will be available shortly after the first mint.",
};

const PRICE: Record<MockState, string> = {
  disconnected: "Free",
  connected: "Free",
  "wrong-network": "Free",
  "missing-contract": "Free",
  "allowlist-only": "Free",
  "not-allowlisted": "Free",
  paused: "Free",
  "live-free": "Free",
  "live-paid": "0.005 ETH",
  "sold-out": "Free",
  "pending-tx": "Free",
  success: "Free",
  rejected: "Free",
  "insufficient-funds": "0.005 ETH",
  "sale-not-started": "Free",
  "metadata-pending": "Free",
  "marketplace-pending": "Free",
};

const MINTED: Record<MockState, string> = {
  "sold-out": "15 / 15",
  "missing-contract": "0 / 15",
  default: "7 / 15",
} as never;

function getMinted(s: MockState): string {
  if (s === "sold-out") return "15 / 15";
  if (s === "missing-contract") return "0 / 15";
  if (s === "live-free" || s === "live-paid") return "3 / 15";
  return "7 / 15";
}

const toneClasses: Record<"info" | "warn" | "error" | "success" | "dim" | "neutral", string> = {
  info: "border-uncommon/40 bg-uncommon/5 text-uncommon",
  warn: "border-legendary/40 bg-legendary/5 text-legendary",
  error: "border-mythic/40 bg-mythic/5 text-mythic",
  success: "border-accent/40 bg-accent/5 text-accent",
  dim: "border-line bg-bg/40 text-muted",
  neutral: "border-line bg-bg/40 text-white",
};

export function MintCardMock({ state }: { state: MockState }) {
  const tone = TONE[state];
  const showLiveCTA = state === "live-free" || state === "live-paid";

  return (
    <div className="rounded-2xl border border-line bg-panel p-6 shadow-xl">
      <p className="font-mono text-[10px] uppercase tracking-[0.24em] text-accent">
        Mint
      </p>
      <h2 className="mt-1 text-lg font-bold tracking-tight">Genesis Drop</h2>

      <div className="mt-5 grid grid-cols-3 gap-3">
        <Stat label="Price" value={PRICE[state]} />
        <Stat label="Minted" value={getMinted(state)} />
        <Stat label="Per wallet" value="1" />
      </div>

      <div className="mt-6">
        {showLiveCTA ? (
          <div className="rounded-xl border border-line bg-bg/40 p-4">
            <p className="mb-3 text-center text-sm text-muted">{BODY[state]}</p>
            <button
              type="button"
              disabled
              aria-disabled="true"
              className="min-h-[48px] w-full rounded-md bg-accent px-5 py-3 font-mono text-[12px] font-bold uppercase tracking-[0.18em] text-bg opacity-90"
            >
              {state === "live-free" ? "Mint free" : "Mint for 0.005 ETH"}
            </button>
            <p className="mt-3 text-center font-mono text-[10px] uppercase tracking-[0.18em] text-muted">
              Dev preview, no transaction will be sent
            </p>
          </div>
        ) : (
          <div
            className={`flex flex-col items-center gap-3 rounded-xl border p-5 text-center ${toneClasses[tone]}`}
            role="status"
          >
            <p className="font-mono text-[11px] font-bold uppercase tracking-[0.2em]">
              {TITLE[state]}
            </p>
            <p className="text-sm leading-relaxed text-white/80">{BODY[state]}</p>
          </div>
        )}
      </div>
    </div>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg border border-line bg-bg/40 px-3 py-2">
      <div className="font-mono text-[9px] uppercase tracking-[0.2em] text-muted">
        {label}
      </div>
      <div className="mt-1 text-sm font-semibold text-white">{value}</div>
    </div>
  );
}

export const ALL_STATES: MockState[] = [
  "disconnected",
  "connected",
  "wrong-network",
  "missing-contract",
  "allowlist-only",
  "not-allowlisted",
  "paused",
  "live-free",
  "live-paid",
  "sold-out",
  "pending-tx",
  "success",
  "rejected",
  "insufficient-funds",
  "sale-not-started",
  "metadata-pending",
  "marketplace-pending",
];
