"use client";

import { useEffect, useState } from "react";
import { useAccount, useChainId, useReadContract, useSwitchChain, useWriteContract, useWaitForTransactionReceipt } from "wagmi";
import { parseEther, formatEther } from "viem";
import { ConnectButton } from "@rainbow-me/rainbowkit";
import { env, hasContract } from "@/lib/env";
import { collectionAbi } from "@/lib/contract";
import { activeChain } from "@/lib/wagmi";

type ReadState = {
  totalMinted?: bigint;
  maxSupply?: bigint;
  priceWei?: bigint;
  paused?: boolean;
  maxPerWallet?: bigint;
};

function shortError(err: unknown): string {
  const msg = (err as { shortMessage?: string; message?: string })?.shortMessage
    ?? (err as { message?: string })?.message ?? String(err);
  if (msg.includes("User rejected") || msg.includes("User denied")) return "You rejected the transaction.";
  if (msg.includes("insufficient funds")) return "Insufficient funds in your wallet.";
  if (msg.includes("execution reverted")) return "Transaction reverted. The contract may be paused, sold out, or over your limit.";
  return msg.slice(0, 140);
}

export function MintCard() {
  const { address, isConnected } = useAccount();
  const chainId = useChainId();
  const { switchChain, isPending: isSwitching } = useSwitchChain();

  // Skip contract reads entirely if no contract address configured.
  const enabled = hasContract();
  const contractCfg = enabled
    ? { address: env.contractAddress as `0x${string}`, abi: collectionAbi }
    : null;

  const totalSupplyRead = useReadContract({
    ...(contractCfg ?? {}),
    functionName: "totalSupply",
    query: { enabled: !!contractCfg },
  });
  const maxSupplyRead = useReadContract({
    ...(contractCfg ?? {}),
    functionName: "maxSupply",
    query: { enabled: !!contractCfg },
  });
  const priceRead = useReadContract({
    ...(contractCfg ?? {}),
    functionName: "mintPrice",
    query: { enabled: !!contractCfg },
  });
  const pausedRead = useReadContract({
    ...(contractCfg ?? {}),
    functionName: "paused",
    query: { enabled: !!contractCfg },
  });
  const maxPerWalletRead = useReadContract({
    ...(contractCfg ?? {}),
    functionName: "maxPerWallet",
    query: { enabled: !!contractCfg },
  });

  // Fallbacks: env-supplied values when contract reads fail or are unavailable.
  const reads: ReadState = {
    totalMinted: totalSupplyRead.data as bigint | undefined,
    maxSupply: (maxSupplyRead.data as bigint | undefined) ?? BigInt(env.totalSupply),
    priceWei:
      (priceRead.data as bigint | undefined) ??
      (env.mintPriceEth ? parseEther(env.mintPriceEth) : undefined),
    paused: pausedRead.data as boolean | undefined,
    maxPerWallet: maxPerWalletRead.data as bigint | undefined,
  };

  const totalMinted = Number(reads.totalMinted ?? 0n);
  const maxSupply = Number(reads.maxSupply ?? env.totalSupply);
  const soldOut = enabled && reads.totalMinted !== undefined && reads.maxSupply !== undefined && reads.totalMinted >= reads.maxSupply;
  const paused = reads.paused === true;
  const wrongNetwork = isConnected && chainId !== activeChain.id;

  const [quantity, setQuantity] = useState(1);
  const maxPerTx = Math.max(1, Number(reads.maxPerWallet ?? 1));

  const { writeContract, data: txHash, isPending: isWriting, error: writeError, reset } = useWriteContract();
  const receipt = useWaitForTransactionReceipt({ hash: txHash });

  // Refetch reads on confirmed mint
  useEffect(() => {
    if (receipt.isSuccess) {
      totalSupplyRead.refetch();
    }
  }, [receipt.isSuccess]); // eslint-disable-line react-hooks/exhaustive-deps

  const totalCostWei =
    reads.priceWei !== undefined ? reads.priceWei * BigInt(quantity) : undefined;

  const onMint = async () => {
    if (!enabled || !reads.priceWei) return;
    reset();
    writeContract({
      address: env.contractAddress as `0x${string}`,
      abi: collectionAbi,
      // We try `mint(uint256)` first. Many drop contracts use `claim(uint256)`
      // instead; you can edit this to `claim` once you know your contract.
      functionName: "mint",
      args: [BigInt(quantity)],
      value: totalCostWei,
    });
  };

  // === Render ===

  return (
    <section id="mint" className="mx-auto mt-16 max-w-2xl px-6">
      <div className="rounded-2xl border border-line bg-panel p-8 shadow-2xl">
        <p className="font-mono text-[10px] uppercase tracking-[0.24em] text-accent">
          Mint
        </p>
        <h2 className="mt-1 text-2xl font-bold tracking-tight">
          Genesis Drop · {env.chainName}
        </h2>

        {/* Stats grid */}
        <div className="mt-6 grid grid-cols-2 gap-4 sm:grid-cols-3">
          <Stat
            label="Price"
            value={
              reads.priceWei !== undefined
                ? `${formatEther(reads.priceWei)} ETH`
                : env.mintPriceEth
                ? `${env.mintPriceEth} ETH`
                : "TBD"
            }
          />
          <Stat
            label="Minted"
            value={
              enabled ? `${totalMinted} / ${maxSupply}` : `0 / ${env.totalSupply}`
            }
          />
          <Stat
            label="Max per wallet"
            value={
              reads.maxPerWallet !== undefined ? String(reads.maxPerWallet) : "n/a"
            }
          />
        </div>

        {/* State machine */}
        <div className="mt-8">
          {!enabled ? (
            <StateBlock
              tone="warn"
              title="Contract not yet deployed"
              body="The mint contract address has not been configured. The site will go live once NEXT_PUBLIC_CONTRACT_ADDRESS is set in production. See the README for deployment steps."
            />
          ) : !isConnected ? (
            <div className="flex flex-col items-center gap-3 rounded-xl border border-line bg-bg/40 p-6 text-center">
              <p className="text-sm text-muted">Connect your wallet to mint.</p>
              <ConnectButton />
            </div>
          ) : wrongNetwork ? (
            <StateBlock
              tone="warn"
              title={`Wrong network`}
              body={`You are connected to chain ${chainId}. Switch to ${activeChain.name} to mint.`}
              action={
                <button
                  className="rounded-md bg-accent px-4 py-2 font-mono text-[11px] font-bold uppercase tracking-[0.18em] text-bg transition hover:scale-105 disabled:opacity-50"
                  onClick={() => switchChain({ chainId: activeChain.id })}
                  disabled={isSwitching}
                >
                  {isSwitching ? "Switching..." : `Switch to ${activeChain.name}`}
                </button>
              }
            />
          ) : soldOut ? (
            <StateBlock
              tone="dim"
              title="Sold out"
              body="Every card in this drop has been minted. Check the marketplace for resales."
              action={
                env.marketplaceUrl && (
                  <a
                    className="rounded-md border border-accent px-4 py-2 font-mono text-[11px] font-bold uppercase tracking-[0.18em] text-accent hover:bg-accent hover:text-bg"
                    href={env.marketplaceUrl}
                    target="_blank"
                    rel="noreferrer noopener"
                  >
                    View on marketplace
                  </a>
                )
              }
            />
          ) : paused ? (
            <StateBlock
              tone="dim"
              title="Sale paused"
              body="Minting is temporarily paused. Check back soon."
            />
          ) : receipt.isLoading ? (
            <StateBlock
              tone="info"
              title="Transaction pending"
              body="Waiting for your transaction to confirm on the network. This usually takes a few seconds."
            />
          ) : receipt.isSuccess && txHash ? (
            <StateBlock
              tone="success"
              title="Minted!"
              body="Your card is on its way to your wallet."
              action={
                <a
                  className="rounded-md border border-accent px-4 py-2 font-mono text-[11px] font-bold uppercase tracking-[0.18em] text-accent hover:bg-accent hover:text-bg"
                  href={`https://basescan.org/tx/${txHash}`}
                  target="_blank"
                  rel="noreferrer noopener"
                >
                  View on Basescan
                </a>
              }
            />
          ) : writeError ? (
            <StateBlock
              tone="error"
              title="Transaction failed"
              body={shortError(writeError)}
              action={
                <button
                  className="rounded-md border border-line px-4 py-2 font-mono text-[11px] font-bold uppercase tracking-[0.18em] text-white hover:border-accent hover:text-accent"
                  onClick={() => reset()}
                >
                  Try again
                </button>
              }
            />
          ) : (
            <div className="rounded-xl border border-line bg-bg/40 p-6">
              {maxPerTx > 1 && (
                <div className="mb-4 flex items-center justify-between">
                  <label className="font-mono text-[11px] uppercase tracking-[0.18em] text-muted">
                    Quantity
                  </label>
                  <div className="flex items-center gap-2">
                    <button
                      type="button"
                      className="h-8 w-8 rounded border border-line text-lg hover:border-accent"
                      onClick={() => setQuantity((q) => Math.max(1, q - 1))}
                    >
                      −
                    </button>
                    <span className="w-8 text-center font-mono">{quantity}</span>
                    <button
                      type="button"
                      className="h-8 w-8 rounded border border-line text-lg hover:border-accent"
                      onClick={() => setQuantity((q) => Math.min(maxPerTx, q + 1))}
                    >
                      +
                    </button>
                  </div>
                </div>
              )}
              <button
                onClick={onMint}
                disabled={isWriting || receipt.isLoading}
                className="w-full rounded-md bg-accent px-5 py-3 font-mono text-[12px] font-bold uppercase tracking-[0.18em] text-bg transition hover:scale-[1.02] disabled:opacity-50"
              >
                {isWriting ? "Confirm in wallet..." : `Mint ${quantity > 1 ? quantity + " " : ""}now`}
              </button>
              {totalCostWei !== undefined && quantity > 1 && (
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
    info:    "border-uncommon/40 bg-uncommon/5 text-uncommon",
    warn:    "border-legendary/40 bg-legendary/5 text-legendary",
    error:   "border-mythic/40 bg-mythic/5 text-mythic",
    success: "border-accent/40 bg-accent/5 text-accent",
    dim:     "border-line bg-bg/40 text-muted",
  };
  return (
    <div className={`flex flex-col items-center gap-3 rounded-xl border p-6 text-center ${toneClasses[tone]}`}>
      <p className="font-mono text-[11px] font-bold uppercase tracking-[0.2em]">{title}</p>
      <p className="text-sm leading-relaxed text-white/80">{body}</p>
      {action}
    </div>
  );
}
