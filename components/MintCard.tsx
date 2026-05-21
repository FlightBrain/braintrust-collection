"use client";

import { useEffect, useState } from "react";
import {
  useAccount,
  useChainId,
  useReadContract,
  useSwitchChain,
  useWriteContract,
  useWaitForTransactionReceipt,
} from "wagmi";
import { parseEther, formatEther } from "viem";
import { ConnectButton } from "@rainbow-me/rainbowkit";
import { env, hasContract, explorerTxUrl, explorerNameFor } from "@/lib/env";
import {
  collectionAbi,
  makeEmptyAllowlistProof,
  NATIVE_TOKEN_ADDRESS,
} from "@/lib/contract";
import { activeChain } from "@/lib/wagmi";
import { slugForIndex1Based, SDR_NAMES } from "@/lib/sdr-list";
import { RarityBadge } from "./RarityBadge";
import type { Tier } from "@/lib/card-copy";

const TIERS: { tier: Tier; key: "common" | "rare" | "mythic" }[] = [
  { tier: "Common", key: "common" },
  { tier: "Rare", key: "rare" },
  { tier: "Mythic", key: "mythic" },
];

type ClaimCondition = {
  startTimestamp: bigint;
  maxClaimableSupply: bigint;
  supplyClaimed: bigint;
  quantityLimitPerWallet: bigint;
  merkleRoot: `0x${string}`;
  pricePerToken: bigint;
  currency: `0x${string}`;
  metadata: string;
};

function shortError(err: unknown): string {
  const e = err as { shortMessage?: string; message?: string };
  const msg = e?.shortMessage ?? e?.message ?? String(err);
  if (msg.includes("User rejected") || msg.includes("User denied"))
    return "You rejected the transaction.";
  if (msg.includes("insufficient funds"))
    return "Insufficient funds in your wallet for gas + mint price.";
  if (msg.includes("NotAllowlisted"))
    return "Your wallet is not on the allowlist for this drop.";
  if (msg.includes("DropClaimExceedLimit"))
    return "You have already claimed all 3 variants of your card.";
  if (msg.includes("DropClaimExceedMaxSupply"))
    return "Sold out.";
  if (msg.includes("DropNoActiveCondition"))
    return "Sale has not started yet.";
  if (msg.includes("DropPaused"))
    return "Sale is paused.";
  if (msg.includes("execution reverted"))
    return "Transaction reverted. You may have exceeded your claim limit or your wallet may not be on the allowlist.";
  return msg.slice(0, 140);
}

export function MintCard() {
  const { address, isConnected } = useAccount();
  const chainId = useChainId();
  const { switchChain, isPending: isSwitching } = useSwitchChain();

  const enabled = hasContract();
  const contractCfg = enabled
    ? { address: env.contractAddress as `0x${string}`, abi: collectionAbi }
    : null;

  // thirdweb DropERC721: nextTokenIdToMint() is the total minted count.
  const mintedRead = useReadContract({
    ...(contractCfg ?? {}),
    functionName: "nextTokenIdToMint",
    query: { enabled: !!contractCfg },
  });
  const maxSupplyRead = useReadContract({
    ...(contractCfg ?? {}),
    functionName: "maxTotalSupply",
    query: { enabled: !!contractCfg },
  });
  // Active claim condition gives us the live price + per-wallet limit.
  const activeIdRead = useReadContract({
    ...(contractCfg ?? {}),
    functionName: "getActiveClaimConditionId",
    query: { enabled: !!contractCfg },
  });
  const conditionRead = useReadContract({
    ...(contractCfg ?? {}),
    functionName: "getClaimConditionById",
    args:
      activeIdRead.data !== undefined ? [activeIdRead.data as bigint] : undefined,
    query: { enabled: !!contractCfg && activeIdRead.data !== undefined },
  });

  // Wallet-bound 3-variant drop: read per-wallet state. Best-effort: if the
  // contract is not the local mock (e.g. real thirdweb DropERC721), these
  // reads will fail silently and the UI falls back to the generic claim flow.
  const slugIndexRead = useReadContract({
    ...(contractCfg ?? {}),
    functionName: "slugIndexFor",
    args: address ? [address] : undefined,
    query: { enabled: !!contractCfg && !!address },
  });
  const remainingRead = useReadContract({
    ...(contractCfg ?? {}),
    functionName: "remainingForWallet",
    args: address ? [address] : undefined,
    query: { enabled: !!contractCfg && !!address },
  });
  const slugIndex1Based = slugIndexRead.data as bigint | undefined;
  const remainingForWallet = remainingRead.data as bigint | undefined;
  const isAllowlisted = slugIndex1Based !== undefined && slugIndex1Based > 0n;
  const fullyClaimed =
    remainingForWallet !== undefined && remainingForWallet === 0n;
  // Map on-chain slug index to a human-readable name + slug for art paths.
  const ownerSlug = slugIndex1Based
    ? slugForIndex1Based(Number(slugIndex1Based))
    : null;
  const ownerName = ownerSlug ? SDR_NAMES[ownerSlug] : null;
  // How many of the 3 variants the wallet has already claimed (0..3).
  const claimedCount =
    remainingForWallet !== undefined ? 3 - Number(remainingForWallet) : 0;

  const condition = conditionRead.data as ClaimCondition | undefined;

  const totalMinted = Number(mintedRead.data ?? 0n);
  const maxSupply = Number(maxSupplyRead.data ?? BigInt(env.totalSupply));
  const priceWei =
    condition?.pricePerToken ??
    (env.mintPriceEth ? parseEther(env.mintPriceEth) : 0n);
  const maxPerWallet = condition?.quantityLimitPerWallet ?? 0n;

  // Sale state derivation
  const now = Math.floor(Date.now() / 1000);
  const saleStarted =
    !condition || Number(condition.startTimestamp) <= now;
  const soldOut =
    enabled &&
    mintedRead.data !== undefined &&
    maxSupplyRead.data !== undefined &&
    (mintedRead.data as bigint) >= (maxSupplyRead.data as bigint);
  const wrongNetwork = isConnected && chainId !== activeChain.id;

  const [quantity, setQuantity] = useState(1);
  // The contract reports the per-wallet cap (3). The actual remaining for
  // this wallet is `remainingForWallet`. Clamp quantity selector to that.
  const remainingForUser =
    remainingForWallet !== undefined
      ? Number(remainingForWallet)
      : maxPerWallet > 0n
      ? Number(maxPerWallet)
      : 1;
  const maxPerTx = Math.max(1, remainingForUser);

  const {
    writeContract,
    data: txHash,
    isPending: isWriting,
    error: writeError,
    reset,
  } = useWriteContract();
  const receipt = useWaitForTransactionReceipt({ hash: txHash });

  // Refetch minted-count + condition + per-wallet state after a confirmed claim.
  useEffect(() => {
    if (receipt.isSuccess) {
      mintedRead.refetch();
      conditionRead.refetch();
      remainingRead.refetch();
    }
  }, [receipt.isSuccess]); // eslint-disable-line react-hooks/exhaustive-deps

  const totalCostWei = priceWei * BigInt(quantity);

  const onClaim = async () => {
    if (!enabled || !address) return;
    reset();
    const proof = makeEmptyAllowlistProof();
    writeContract({
      address: env.contractAddress as `0x${string}`,
      abi: collectionAbi,
      functionName: "claim",
      args: [
        address,
        BigInt(quantity),
        NATIVE_TOKEN_ADDRESS,
        priceWei,
        proof,
        "0x", // empty data
      ],
      value: totalCostWei,
    });
  };

  // === Render ===

  return (
    <section id="mint" className="mx-auto mt-16 max-w-2xl px-6">
      <div className="rounded-2xl border border-line bg-panel p-6 shadow-2xl sm:p-8">
        <p className="font-mono text-[10px] uppercase tracking-[0.24em] text-accent">
          Mint
        </p>
        <h2 className="mt-1 text-2xl font-bold tracking-tight">
          {ownerName ? `${ownerName}'s cards` : "Genesis Drop"}{" "}
          <span className="text-muted">· {env.chainName}</span>
        </h2>
        {ownerName && (
          <p className="mt-1 text-sm text-muted">
            You can mint up to 3 {ownerName.split(" ")[0]} cards. Each variant is unique.
          </p>
        )}

        <div className="mt-6 grid grid-cols-2 gap-4 sm:grid-cols-3">
          <Stat
            label="Price"
            value={
              priceWei === 0n
                ? "Free"
                : `${formatEther(priceWei)} ETH`
            }
          />
          <Stat
            label="Minted"
            value={
              enabled ? `${totalMinted} / ${maxSupply}` : `0 / ${env.totalSupply}`
            }
          />
          <Stat
            label={isConnected ? "Your variants" : "Max per wallet"}
            value={
              isConnected && remainingForWallet !== undefined
                ? `${3 - Number(remainingForWallet)} of 3 claimed`
                : maxPerWallet > 0n
                ? `${maxPerWallet} per wallet`
                : "n/a"
            }
          />
        </div>

        {/* Variant thumb strip for the connected coworker */}
        {ownerName && ownerSlug && (
          <div className="mt-6 rounded-xl border border-line bg-bg/30 p-4">
            <p className="mb-3 font-mono text-[10px] uppercase tracking-[0.18em] text-muted">
              Your three variants
            </p>
            <div className="grid grid-cols-3 gap-3">
              {TIERS.map((t, i) => {
                const claimed = i < claimedCount;
                return (
                  <div
                    key={t.key}
                    className={`overflow-hidden rounded-lg border bg-panel transition ${claimed ? "border-line opacity-50" : "border-line"}`}
                  >
                    <img
                      src={`/nfts/variants/${ownerSlug}_${t.key}.svg`}
                      alt={`${ownerName} ${t.tier} variant`}
                      className="block w-full"
                      loading="lazy"
                    />
                    <div className="flex items-center justify-between gap-1 px-2 py-1.5">
                      <RarityBadge tier={t.tier} size="sm" withDot={false} />
                      <span className="font-mono text-[9px] uppercase tracking-[0.18em] text-muted">
                        {claimed ? "Claimed" : "Available"}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        <div className="mt-8">
          {!enabled ? (
            <StateBlock
              tone="warn"
              title="Contract not yet deployed"
              body={`The mint contract address has not been configured for ${env.chainName}. The site will go live once NEXT_PUBLIC_CONTRACT_ADDRESS is set in production. See the README for thirdweb deployment steps.`}
            />
          ) : !isConnected ? (
            <div className="flex flex-col items-center gap-3 rounded-xl border border-line bg-bg/40 p-6 text-center">
              <p className="text-sm text-muted">Connect your wallet to mint.</p>
              <ConnectButton />
            </div>
          ) : wrongNetwork ? (
            <StateBlock
              tone="warn"
              title="Wrong network"
              body={`You are connected to chain ${chainId}. Switch to ${activeChain.name} to mint.`}
              action={
                <button
                  className="rounded-md bg-accent px-4 py-2 font-mono text-[11px] font-bold uppercase tracking-[0.18em] text-bg transition hover:scale-105 disabled:opacity-50"
                  onClick={() => switchChain({ chainId: activeChain.id })}
                  disabled={isSwitching}
                  aria-label={`Switch network to ${activeChain.name}`}
                >
                  {isSwitching ? "Switching..." : `Switch to ${activeChain.name}`}
                </button>
              }
            />
          ) : isConnected && !isAllowlisted && slugIndexRead.isFetched ? (
            <StateBlock
              tone="warn"
              title="This wallet is not on the coworker allowlist"
              body="Cards are only mintable from the wallet of the depicted coworker. If you think this is your card, reach out and we'll check the mapping."
            />
          ) : isConnected && fullyClaimed ? (
            <StateBlock
              tone="dim"
              title={`All 3 of ${ownerName ? ownerName.split(" ")[0] + "'s" : "your"} variants claimed`}
              body="You've minted Common, Rare, and Mythic. Check your wallet's NFT tab to see them, or open the gallery to compare with other coworkers."
            />
          ) : soldOut ? (
            <StateBlock
              tone="dim"
              title="Sold out"
              body="Every card in this drop has been minted. Check the marketplace for resales."
              action={
                env.marketplaceUrl ? (
                  <a
                    className="rounded-md border border-accent px-4 py-2 font-mono text-[11px] font-bold uppercase tracking-[0.18em] text-accent hover:bg-accent hover:text-bg"
                    href={env.marketplaceUrl}
                    target="_blank"
                    rel="noreferrer noopener"
                  >
                    View on marketplace
                  </a>
                ) : null
              }
            />
          ) : !saleStarted ? (
            <StateBlock
              tone="dim"
              title="Sale not started"
              body={`The public sale starts at ${new Date(
                Number(condition?.startTimestamp ?? 0n) * 1000
              ).toLocaleString()}. Come back then.`}
            />
          ) : receipt.isLoading ? (
            <StateBlock
              tone="info"
              title="Transaction pending"
              body="Waiting for your transaction to confirm. This usually takes a few seconds."
            />
          ) : receipt.isSuccess && txHash ? (
            (() => {
              const txUrl = explorerTxUrl(activeChain.id, txHash);
              const explorerName = explorerNameFor(activeChain.id);
              return (
                <StateBlock
                  tone="success"
                  title={txUrl ? "Minted!" : "Local test mint complete"}
                  body={
                    txUrl
                      ? `Your card is on its way to your wallet. Check the NFTs tab to see it.`
                      : `Your card has been minted to your wallet on the local chain. Tx hash: ${txHash.slice(0, 10)}...${txHash.slice(-8)}`
                  }
                  action={
                    txUrl && explorerName ? (
                      <a
                        className="rounded-md border border-accent px-4 py-2 font-mono text-[11px] font-bold uppercase tracking-[0.18em] text-accent hover:bg-accent hover:text-bg focus:outline-none focus-visible:ring-2 focus-visible:ring-accent"
                        href={txUrl}
                        target="_blank"
                        rel="noreferrer noopener"
                      >
                        View on {explorerName}
                      </a>
                    ) : null
                  }
                />
              );
            })()
          ) : writeError ? (
            <StateBlock
              tone="error"
              title="Transaction failed"
              body={shortError(writeError)}
              action={
                <button
                  className="rounded-md border border-line px-4 py-2 font-mono text-[11px] font-bold uppercase tracking-[0.18em] text-white hover:border-accent hover:text-accent"
                  onClick={() => reset()}
                  aria-label="Try minting again"
                >
                  Try again
                </button>
              }
            />
          ) : (
            <div className="rounded-xl border border-line bg-bg/40 p-6">
              {maxPerTx > 1 && (
                <div className="mb-4 flex items-center justify-between">
                  <label className="font-mono text-[11px] uppercase tracking-[0.18em] text-muted" htmlFor="qty">
                    Quantity
                  </label>
                  <div className="flex items-center gap-2">
                    <button
                      type="button"
                      className="h-11 w-11 rounded border border-line text-lg hover:border-accent focus:outline-none focus-visible:ring-2 focus-visible:ring-accent disabled:opacity-40"
                      onClick={() => setQuantity((q) => Math.max(1, q - 1))}
                      disabled={quantity <= 1}
                      aria-label="Decrease quantity"
                    >
                      −
                    </button>
                    <span id="qty" className="w-10 text-center font-mono text-base" aria-live="polite">
                      {quantity}
                    </span>
                    <button
                      type="button"
                      className="h-11 w-11 rounded border border-line text-lg hover:border-accent focus:outline-none focus-visible:ring-2 focus-visible:ring-accent disabled:opacity-40"
                      onClick={() =>
                        setQuantity((q) => Math.min(maxPerTx, q + 1))
                      }
                      disabled={quantity >= maxPerTx}
                      aria-label="Increase quantity"
                    >
                      +
                    </button>
                  </div>
                </div>
              )}
              <button
                onClick={onClaim}
                disabled={isWriting || receipt.isLoading}
                className="min-h-[48px] w-full rounded-md bg-accent px-5 py-3 font-mono text-[12px] font-bold uppercase tracking-[0.18em] text-bg transition hover:scale-[1.02] disabled:opacity-50 focus:outline-none focus-visible:ring-2 focus-visible:ring-accent focus-visible:ring-offset-2 focus-visible:ring-offset-bg motion-reduce:transition-none motion-reduce:hover:transform-none"
                aria-label={`Mint ${quantity} card${quantity > 1 ? "s" : ""}`}
              >
                {isWriting
                  ? "Confirm in your wallet..."
                  : priceWei === 0n
                  ? `Claim ${quantity > 1 ? `${quantity} cards` : "next card"}`
                  : `Claim ${quantity > 1 ? `${quantity} cards` : "card"} for ${formatEther(totalCostWei)} ETH`}
              </button>
              {priceWei > 0n && quantity > 1 && (
                <p className="mt-3 text-center font-mono text-[11px] text-muted">
                  Total: {formatEther(totalCostWei)} ETH
                </p>
              )}
            </div>
          )}
        </div>
      </div>
    </section>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg border border-line bg-bg/40 px-4 py-3">
      <div className="font-mono text-[9px] uppercase tracking-[0.2em] text-muted">{label}</div>
      <div className="mt-1 text-sm font-semibold text-white">{value}</div>
    </div>
  );
}

function StateBlock({
  title,
  body,
  tone,
  action,
}: {
  title: string;
  body: string;
  tone: "info" | "warn" | "error" | "success" | "dim";
  action?: React.ReactNode;
}) {
  const toneClasses: Record<typeof tone, string> = {
    info: "border-uncommon/40 bg-uncommon/5 text-uncommon",
    warn: "border-legendary/40 bg-legendary/5 text-legendary",
    error: "border-mythic/40 bg-mythic/5 text-mythic",
    success: "border-accent/40 bg-accent/5 text-accent",
    dim: "border-line bg-bg/40 text-muted",
  };
  return (
    <div
      role={tone === "error" ? "alert" : "status"}
      className={`flex flex-col items-center gap-3 rounded-xl border p-6 text-center ${toneClasses[tone]}`}
    >
      <p className="font-mono text-[11px] font-bold uppercase tracking-[0.2em]">{title}</p>
      <p className="text-sm leading-relaxed text-white/80">{body}</p>
      {action}
    </div>
  );
}
