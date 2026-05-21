import fs from "node:fs";
import path from "node:path";
import { Header } from "@/components/Header";
import { FooterNav } from "@/components/FooterNav";
import { env, hasContract, explorerAddressUrl } from "@/lib/env";
import { isTestnet } from "@/lib/chains";
import { computeLaunchStatus, LAUNCH_STATUS_LABELS, LEGAL_BLOCKERS } from "@/lib/status";
import { contractMode } from "@/lib/contract/adapter";

export const metadata = {
  title: "Status · Braintrust Collection (read-only)",
  robots: { index: false, follow: false },
};

type Verdict = "PASS" | "WARN" | "BLOCKED" | "TODO";

const verdictTone: Record<Verdict, string> = {
  PASS: "border-accent/40 bg-accent/5 text-accent",
  WARN: "border-legendary/40 bg-legendary/5 text-legendary",
  BLOCKED: "border-mythic/40 bg-mythic/5 text-mythic",
  TODO: "border-line bg-bg/40 text-muted",
};

function loadMetadataSummary() {
  const dir = path.join(process.cwd(), "public", "metadata");
  if (!fs.existsSync(dir)) return { token_count: 0, collection: false };
  const files = fs.readdirSync(dir);
  return {
    token_count: files.filter((f) => /^\d+\.json$/.test(f)).length,
    collection: files.includes("collection.json"),
  };
}

function loadDocsCheck() {
  const docs = path.join(process.cwd(), "docs");
  if (!fs.existsSync(docs)) return { exists: false, count: 0 };
  return {
    exists: true,
    count: fs.readdirSync(docs).filter((f) => f.endsWith(".md")).length,
  };
}

export default function AdminStatusPage() {
  const launch = computeLaunchStatus();
  const meta = loadMetadataSummary();
  const docs = loadDocsCheck();
  const contractReady = hasContract();
  const testnet = isTestnet(env.chainId);
  const baseImg = process.env.NEXT_PUBLIC_BASE_IMAGE_URI ?? "";

  const cards: { title: string; verdict: Verdict; lines: string[] }[] = [
    {
      title: "Website",
      verdict: "PASS",
      lines: ["Next.js 14 App Router", "9 routes prerendered", "Mobile, a11y, status pill, dev preview"],
    },
    {
      title: "Wallet Connect",
      verdict: env.walletConnectProjectId ? "PASS" : "TODO",
      lines: env.walletConnectProjectId
        ? ["Reown project ID configured", "RainbowKit modal wired"]
        : ["Project ID missing", "Wallet connect will not work in production"],
    },
    {
      title: "Contract",
      verdict: contractReady ? (testnet ? "PASS" : "WARN") : "TODO",
      lines: contractReady
        ? [
            `Address configured: ${env.contractAddress.slice(0, 6)}...${env.contractAddress.slice(-4)}`,
            `Chain: ${env.chainName} (${env.chainId})`,
            `Adapter mode: ${contractMode}`,
            !testnet ? "On mainnet, double-check legal approvals." : "Testnet OK to test mints.",
          ]
        : [
            "No contract address set yet.",
            "Deploy thirdweb DropERC721 on Base Sepolia.",
            "Then paste address into NEXT_PUBLIC_CONTRACT_ADDRESS.",
          ],
    },
    {
      title: "Metadata",
      verdict: meta.token_count === env.totalSupply && meta.collection ? "PASS" : "TODO",
      lines: [
        `Token files: ${meta.token_count} / ${env.totalSupply}`,
        `Collection metadata: ${meta.collection ? "present" : "missing"}`,
        `Base image URI: ${baseImg || "(unset)"}`,
      ],
    },
    {
      title: "IPFS",
      verdict: baseImg.startsWith("ipfs://") ? "PASS" : "TODO",
      lines: baseImg.startsWith("ipfs://")
        ? ["Image base URI is ipfs://", "Pin metadata next."]
        : [
            "Not pinned yet.",
            "Local/HTTP image URLs only. Required for mainnet, optional for testnet.",
          ],
    },
    {
      title: "Allowlist",
      verdict: "TODO",
      lines: [
        "data/allowlist.example.csv: present",
        "Real coworker list: not yet collected",
        "thirdweb claim phase: not yet configured",
      ],
    },
    {
      title: "Marketplace",
      verdict: env.marketplaceUrl ? "PASS" : "TODO",
      lines: env.marketplaceUrl
        ? [`URL: ${env.marketplaceUrl}`]
        : ["Not listed yet. Set NEXT_PUBLIC_MARKETPLACE_URL after listing on OpenSea."],
    },
    {
      title: "Docs",
      verdict: docs.count >= 5 ? "PASS" : "TODO",
      lines: [`${docs.count} markdown guides under /docs`],
    },
    {
      title: "Legal",
      verdict: LEGAL_BLOCKERS.every((b) => b.cleared) ? "PASS" : "BLOCKED",
      lines: LEGAL_BLOCKERS.map((b) => `${b.cleared ? "OK" : "OPEN"}: ${b.label}`),
    },
    {
      title: "Mainnet",
      verdict:
        launch === "MAINNET_LIVE"
          ? "PASS"
          : launch.startsWith("TESTNET")
          ? "TODO"
          : "BLOCKED",
      lines: [LAUNCH_STATUS_LABELS[launch], "No mainnet contract has been deployed."],
    },
  ];

  return (
    <main>
      <Header />
      <section className="mx-auto max-w-6xl px-4 pb-12 pt-10 sm:px-6">
        <div className="mb-6 rounded-xl border border-line bg-panel p-5">
          <p className="font-mono text-[10px] uppercase tracking-[0.24em] text-muted">
            Read-only status
          </p>
          <h1 className="mt-1 text-3xl font-black tracking-tight md:text-4xl">
            {LAUNCH_STATUS_LABELS[launch]}
          </h1>
          <p className="mt-2 text-sm leading-relaxed text-muted">
            This page is information only. No admin actions, no mint controls,
            no secret values are shown. Use it to verify what is configured
            before launch.
          </p>
        </div>

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {cards.map((c) => (
            <div
              key={c.title}
              className={`rounded-xl border p-5 ${verdictTone[c.verdict]}`}
            >
              <div className="flex items-center justify-between">
                <p className="font-mono text-[10px] font-bold uppercase tracking-[0.22em]">
                  {c.title}
                </p>
                <span className="font-mono text-[10px] font-bold uppercase tracking-[0.2em]">
                  {c.verdict}
                </span>
              </div>
              <ul className="mt-3 space-y-1 text-xs leading-relaxed text-white/80">
                {c.lines.map((l, i) => (
                  <li key={i}>{l}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="mt-10 rounded-xl border border-line bg-panel p-5">
          <p className="font-mono text-[10px] uppercase tracking-[0.24em] text-muted">
            Helpful docs
          </p>
          <ul className="mt-3 grid grid-cols-1 gap-1.5 text-sm md:grid-cols-2">
            <li><a className="text-accent hover:underline" href="https://github.com/FlightBrain/braintrust-collection/blob/main/docs/thirdweb-base-sepolia-walkthrough.md" target="_blank" rel="noreferrer noopener">thirdweb Base Sepolia walkthrough</a></li>
            <li><a className="text-accent hover:underline" href="https://github.com/FlightBrain/braintrust-collection/blob/main/docs/vercel-env-walkthrough.md" target="_blank" rel="noreferrer noopener">Vercel env walkthrough</a></li>
            <li><a className="text-accent hover:underline" href="https://github.com/FlightBrain/braintrust-collection/blob/main/docs/free-coworker-allowlist.md" target="_blank" rel="noreferrer noopener">Free coworker allowlist</a></li>
            <li><a className="text-accent hover:underline" href="https://github.com/FlightBrain/braintrust-collection/blob/main/docs/ipfs-finalization.md" target="_blank" rel="noreferrer noopener">IPFS finalization</a></li>
            <li><a className="text-accent hover:underline" href="https://github.com/FlightBrain/braintrust-collection/blob/main/docs/legal-brand-consent-checklist.md" target="_blank" rel="noreferrer noopener">Legal + brand consent checklist</a></li>
            <li><a className="text-accent hover:underline" href="https://github.com/FlightBrain/braintrust-collection/blob/main/docs/qa-checklist.md" target="_blank" rel="noreferrer noopener">QA checklist</a></li>
          </ul>
        </div>

        {contractReady && (
          <p className="mt-6 text-center font-mono text-[10px] uppercase tracking-[0.22em] text-muted">
            Contract on chain:&nbsp;
            <a
              className="text-accent hover:underline"
              href={explorerAddressUrl(env.chainId, env.contractAddress)}
              target="_blank"
              rel="noreferrer noopener"
            >
              {env.contractAddress}
            </a>
          </p>
        )}
      </section>
      <FooterNav />
    </main>
  );
}
