import fs from "fs";
import path from "path";
import { Header } from "@/components/Header";
import { FooterNav } from "@/components/FooterNav";

type Person = {
  slug: string;
  name: string;
  trait?: string;
  id?: number;
};

type Rarity = {
  tier: string;
  tier_color: string;
  rank: number;
  score: number;
};

async function loadData() {
  const peoplePath = path.join(process.cwd(), "public", "auto_people.json");
  const rarityPath = path.join(process.cwd(), "public", "rarity.json");
  const people: Person[] = JSON.parse(fs.readFileSync(peoplePath, "utf-8"));
  const rarity: Record<string, Rarity> = JSON.parse(fs.readFileSync(rarityPath, "utf-8"));
  return { people, rarity };
}

export default async function GalleryPage() {
  const { people, rarity } = await loadData();

  return (
    <main>
      <Header />
      <section className="mx-auto max-w-6xl px-6 pt-16 pb-12">
        <p className="font-mono text-[10px] uppercase tracking-[0.24em] text-muted">
          The collection
        </p>
        <h1 className="mt-2 text-4xl font-black tracking-tight md:text-5xl">
          Genesis · 15 cards
        </h1>
        <p className="mt-3 max-w-2xl text-sm leading-relaxed text-muted">
          Existing artwork. Each card is a 1-of-1 with hand-picked NFT
          accessories and a unique rarity tier.
        </p>

        <div className="mt-10 grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-5">
          {people.map((p) => {
            const r = rarity[p.slug];
            const color = r?.tier_color ?? "#8B95A8";
            return (
              <div
                key={p.slug}
                className="overflow-hidden rounded-xl border border-line bg-panel"
                style={{ boxShadow: `0 0 0 1px ${color}22` }}
              >
                <div className="aspect-square">
                  <img
                    src={`/nfts/corporate/${p.slug}_nft.svg`}
                    alt={p.name}
                    className="pixelated h-full w-full object-cover"
                  />
                </div>
                <div className="border-t border-line px-3 py-3">
                  <p className="truncate text-sm font-semibold">{p.name}</p>
                  {r && (
                    <p
                      className="mt-1 font-mono text-[9px] uppercase tracking-[0.2em]"
                      style={{ color }}
                    >
                      {r.tier} · #{String(r.rank).padStart(2, "0")}/15
                    </p>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </section>
      <FooterNav />
    </main>
  );
}
