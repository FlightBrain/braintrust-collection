import Link from "next/link";

const FEATURED_SLUGS = ["ryan", "kensington", "duncan", "catherine", "ava"];

export function Hero() {
  return (
    <section className="relative overflow-hidden border-b border-line">
      <div className="absolute inset-0 -z-10 bg-[radial-gradient(ellipse_at_top,rgba(0,255,148,0.10),transparent_60%)]" />
      <div className="mx-auto max-w-6xl px-6 pt-20 pb-12 text-center">
        <p className="mb-6 inline-flex items-center gap-2 rounded-full border border-line px-3 py-1 font-mono text-[10px] uppercase tracking-[0.24em] text-muted">
          <span className="block h-1.5 w-1.5 animate-pulse rounded-full bg-accent shadow-[0_0_10px] shadow-accent" />
          Volume I · Genesis · Base
        </p>
        <h1 className="bg-gradient-to-b from-white to-[#8B95A8] bg-clip-text text-[clamp(40px,7vw,84px)] font-black leading-[0.95] tracking-tight text-transparent">
          The Sales Floor <br />
          <span className="bg-gradient-to-br from-accent to-[#00E5FF] bg-clip-text text-transparent">
            on-chain.
          </span>
        </h1>
        <p className="mx-auto mt-6 max-w-xl text-base leading-relaxed text-muted">
          15 hand-pixeled collectible cards. The original Braintrust sales
          floor, kitted out with NFT accessories chosen from a 157-variant
          catalog.
        </p>

        {/* Floating art preview */}
        <div
          className="mx-auto mt-12 grid max-w-3xl grid-cols-2 gap-3 sm:grid-cols-3 md:grid-cols-5"
          aria-label="Featured cards"
        >
          {FEATURED_SLUGS.map((slug, i) => (
            <div
              key={slug}
              className="aspect-square overflow-hidden rounded-xl border border-line bg-panel"
              style={{
                transform: `translateY(${i % 2 === 0 ? "0" : "12px"})`,
              }}
            >
              <img
                src={`/nfts/corporate/${slug}_nft.svg`}
                alt={`Braintrust Collection card ${slug}`}
                className="pixelated h-full w-full"
                loading="lazy"
              />
            </div>
          ))}
        </div>

        <div className="mt-10 flex justify-center gap-3">
          <Link
            href="#mint"
            className="rounded-md bg-accent px-5 py-2.5 font-mono text-[11px] font-bold uppercase tracking-[0.18em] text-bg transition hover:scale-105"
          >
            Mint a card
          </Link>
          <Link
            href="/gallery"
            className="rounded-md border border-line px-5 py-2.5 font-mono text-[11px] font-bold uppercase tracking-[0.18em] text-white transition hover:border-accent hover:text-accent"
          >
            View gallery
          </Link>
        </div>
      </div>
    </section>
  );
}
