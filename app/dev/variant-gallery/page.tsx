import fs from "node:fs";
import path from "node:path";
import { Header } from "@/components/Header";
import { FooterNav } from "@/components/FooterNav";

export const metadata = {
  title: "Dev Preview · Variant Gallery · Braintrust Collection",
  robots: { index: false, follow: false },
};

type Person = { slug: string; name: string };

const TIERS = ["common", "rare", "mythic"] as const;
const TIER_LABEL: Record<(typeof TIERS)[number], { label: string; color: string }> = {
  common: { label: "COMMON", color: "#8B95A8" },
  rare: { label: "RARE", color: "#9D7AFF" },
  mythic: { label: "MYTHIC", color: "#FFD93D" },
};

async function loadPeople(): Promise<Person[]> {
  const p = path.join(process.cwd(), "public", "auto_people.json");
  return JSON.parse(fs.readFileSync(p, "utf-8"));
}

export default async function VariantGalleryPage() {
  const people = await loadPeople();

  return (
    <main>
      <Header />
      <section className="mx-auto max-w-7xl px-4 pb-12 pt-10 sm:px-6">
        <div className="mb-8 rounded-xl border border-legendary/40 bg-legendary/5 p-5 text-legendary">
          <p className="font-mono text-[10px] font-bold uppercase tracking-[0.24em]">
            Dev preview, all 45 variants
          </p>
          <p className="mt-2 text-sm leading-relaxed text-white/80">
            15 SDRs x 3 tiers = 45 cards. Common is the bare personalized face,
            Rare adds curated accessories, Mythic adds a premium accessory plus a
            gold-treatment SVG frame. Each card has a unique token ID and is
            only mintable by the bound coworker wallet.
          </p>
        </div>

        <h1 className="text-3xl font-black tracking-tight md:text-4xl">
          Variant gallery
        </h1>
        <p className="mt-2 max-w-2xl text-sm leading-relaxed text-muted">
          Originals at <code className="font-mono text-[11px]">public/nfts/corporate/</code>
          remain unchanged. New artwork lives at
          <code className="font-mono text-[11px]">public/nfts/variants/</code>.
        </p>

        <div className="mt-10 space-y-10">
          {people.map((p, sdrIndex) => (
            <div key={p.slug}>
              <div className="mb-3 flex items-baseline justify-between border-b border-line pb-2">
                <h2 className="text-lg font-bold tracking-tight">
                  {p.name}
                </h2>
                <span className="font-mono text-[10px] uppercase tracking-[0.2em] text-muted">
                  slug: {p.slug} · tokens {sdrIndex * 3}, {sdrIndex * 3 + 1}, {sdrIndex * 3 + 2}
                </span>
              </div>
              <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
                {TIERS.map((tier, vIdx) => {
                  const tokenId = sdrIndex * 3 + vIdx;
                  const tierInfo = TIER_LABEL[tier];
                  return (
                    <div
                      key={tier}
                      className="overflow-hidden rounded-xl border border-line bg-panel"
                      style={{ boxShadow: `0 0 0 1px ${tierInfo.color}22` }}
                    >
                      <img
                        src={`/nfts/variants/${p.slug}_${tier}.svg`}
                        alt={`${p.name} ${tierInfo.label}`}
                        className="block w-full"
                        loading="lazy"
                      />
                      <div className="border-t border-line px-3 py-2 text-xs">
                        <div className="flex items-center justify-between">
                          <span
                            className="font-mono text-[10px] font-semibold uppercase tracking-[0.2em]"
                            style={{ color: tierInfo.color }}
                          >
                            {tierInfo.label}
                          </span>
                          <span className="font-mono text-[10px] text-muted">
                            #{String(tokenId).padStart(3, "0")}
                          </span>
                        </div>
                        <div className="mt-1 break-all font-mono text-[10px] text-muted">
                          /nfts/variants/{p.slug}_{tier}.svg
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      </section>
      <FooterNav />
    </main>
  );
}
