import Link from "next/link";
import { env, explorerAddressUrl } from "@/lib/env";

export function FooterNav() {
  return (
    <footer className="mt-24 border-t border-line">
      <div className="mx-auto max-w-6xl px-6 py-10">
        <div className="grid gap-8 md:grid-cols-4">
          <div>
            <p className="font-mono text-[10px] uppercase tracking-[0.24em] text-muted">
              The Drop
            </p>
            <p className="mt-2 text-sm leading-relaxed text-white/80">
              Braintrust Collection: Genesis. 15 hand-pixeled cards.
            </p>
          </div>
          <div>
            <p className="font-mono text-[10px] uppercase tracking-[0.24em] text-muted">
              Project
            </p>
            <ul className="mt-2 space-y-1 text-sm">
              <li><Link className="hover:text-accent" href="/">Mint</Link></li>
              <li><Link className="hover:text-accent" href="/gallery">Gallery</Link></li>
              <li><Link className="hover:text-accent" href="/faq">FAQ</Link></li>
            </ul>
          </div>
          <div>
            <p className="font-mono text-[10px] uppercase tracking-[0.24em] text-muted">
              Legal
            </p>
            <ul className="mt-2 space-y-1 text-sm">
              <li><Link className="hover:text-accent" href="/terms">Terms</Link></li>
              <li><Link className="hover:text-accent" href="/privacy">Privacy</Link></li>
              <li><Link className="hover:text-accent" href="/license">License</Link></li>
            </ul>
          </div>
          <div>
            <p className="font-mono text-[10px] uppercase tracking-[0.24em] text-muted">
              On-chain
            </p>
            <ul className="mt-2 space-y-1 text-sm">
              <li><span className="text-muted">Chain:</span> {env.chainName}</li>
              {env.contractAddress ? (() => {
                const href = explorerAddressUrl(env.chainId, env.contractAddress);
                const short = `${env.contractAddress.slice(0, 6)}...${env.contractAddress.slice(-4)}`;
                return (
                  <li className="break-all">
                    <span className="text-muted">Contract:</span>{" "}
                    {href ? (
                      <a
                        className="text-accent hover:underline"
                        href={href}
                        target="_blank"
                        rel="noreferrer noopener"
                      >
                        {short}
                      </a>
                    ) : (
                      <span className="text-accent">{short}</span>
                    )}
                  </li>
                );
              })() : (
                <li className="text-muted">Contract: not yet deployed</li>
              )}
              {env.marketplaceUrl && (
                <li>
                  <a
                    className="text-accent hover:underline"
                    href={env.marketplaceUrl}
                    target="_blank"
                    rel="noreferrer noopener"
                  >
                    OpenSea
                  </a>
                </li>
              )}
            </ul>
          </div>
        </div>
        <p className="mt-10 font-mono text-[10px] uppercase tracking-[0.2em] text-muted">
          NFTs are collectibles, not investment products.
        </p>
      </div>
    </footer>
  );
}
