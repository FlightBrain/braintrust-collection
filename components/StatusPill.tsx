import { env, hasContract } from "@/lib/env";

/**
 * Polished status pill shown in the header. Surfaces:
 *   - chain mode (Testnet preview / Mainnet / unknown)
 *   - contract readiness (Contract pending / Configured)
 *
 * Reads from env. Never crashes. No client-side state needed.
 */
export function StatusPill() {
  const isTestnet = env.chainId === 84532 || env.chainId === 11155111;
  const isMainnet = env.chainId === 8453 || env.chainId === 1;
  const contractReady = hasContract();

  let label: string;
  let tone: "testnet" | "mainnet" | "pending" | "muted";

  if (!contractReady) {
    label = isTestnet ? "Testnet preview" : "Mainnet not live";
    tone = "pending";
  } else if (isTestnet) {
    label = "Testnet live";
    tone = "testnet";
  } else if (isMainnet) {
    label = "Live";
    tone = "mainnet";
  } else {
    label = env.chainName;
    tone = "muted";
  }

  const toneClasses: Record<typeof tone, string> = {
    testnet: "border-uncommon/40 bg-uncommon/10 text-uncommon",
    mainnet: "border-accent/40 bg-accent/10 text-accent",
    pending: "border-legendary/40 bg-legendary/10 text-legendary",
    muted: "border-line bg-bg/40 text-muted",
  };

  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 font-mono text-[9px] font-semibold uppercase tracking-[0.18em] ${toneClasses[tone]}`}
      role="status"
      aria-label={`${label} status`}
    >
      <span
        className="block h-1.5 w-1.5 rounded-full bg-current"
        aria-hidden="true"
      />
      {label}
    </span>
  );
}
