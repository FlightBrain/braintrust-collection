import { Header } from "@/components/Header";
import { FooterNav } from "@/components/FooterNav";
import { env } from "@/lib/env";

const faqs: { q: string; a: string }[] = [
  {
    q: `What chain is the collection on?`,
    a: `Braintrust Collection: Genesis is minted on ${env.chainName} (chain ID ${env.chainId}). You will need a wallet that supports ${env.chainName} and a small amount of ETH on ${env.chainName} to cover gas + mint price.`,
  },
  {
    q: "How do I mint?",
    a: "1. Click Connect Wallet at the top of the page. 2. Pick your wallet (MetaMask, Coinbase Wallet, WalletConnect, etc.). 3. Confirm you are on the correct network. 4. Click Mint and approve the transaction in your wallet. Your card will appear in your wallet once the transaction confirms.",
  },
  {
    q: "What wallet do I need?",
    a: "Any EVM-compatible wallet works: MetaMask, Coinbase Wallet, Rainbow, Trust, or anything that connects via WalletConnect. You will need a small amount of ETH on the mint chain for the mint price plus gas fees.",
  },
  {
    q: "What do I receive when I mint?",
    a: "An ERC-721 token in your wallet. The token references a JSON metadata file (name, description, image, attributes) which in turn references the artwork. Both metadata and artwork are pinned to decentralized storage so they remain available even if this website goes offline.",
  },
  {
    q: "Are commercial rights included?",
    a: "By default: no. Buying the NFT does not transfer the copyright in the underlying artwork. You receive ownership of the token and a personal-use license to display it. See the License page for the full terms.",
  },
  {
    q: "Where is the art stored?",
    a: "Originals are hosted in this repository and pinned to IPFS (and optionally Arweave) before launch. Once pinned, the contract's baseURI points at the IPFS hash, so the art survives independent of this website.",
  },
  {
    q: "What if my transaction fails?",
    a: "Common causes: not enough ETH for gas + price, sale is paused, you hit the per-wallet limit, or the contract is sold out. The mint card on the home page surfaces a specific error message for each case. If a transaction reverts, you only pay gas (the mint price is refunded).",
  },
  {
    q: "Is this an investment?",
    a: "No. NFTs in this collection are collectibles and art. There is no expectation of financial return, no roadmap of future utility, and no promise that the value will go up. Buy if you like the art.",
  },
  {
    q: "What if you ask for my seed phrase?",
    a: "We never will. Nobody legitimate ever needs your seed phrase or private keys. If anyone, including a fake support agent, a DM, or a website pretending to be us, asks for your seed phrase, close the window and ignore them.",
  },
];

export default function FaqPage() {
  return (
    <main>
      <Header />
      <section className="mx-auto max-w-3xl px-6 pt-16 pb-20">
        <p className="font-mono text-[10px] uppercase tracking-[0.24em] text-muted">
          Help
        </p>
        <h1 className="mt-2 text-4xl font-black tracking-tight md:text-5xl">FAQ</h1>

        <div className="mt-10 space-y-6">
          {faqs.map((f, i) => (
            <div key={i} className="rounded-xl border border-line bg-panel p-6">
              <h2 className="text-base font-bold tracking-tight">{f.q}</h2>
              <p className="mt-2 text-sm leading-relaxed text-muted">{f.a}</p>
            </div>
          ))}
        </div>
      </section>
      <FooterNav />
    </main>
  );
}
