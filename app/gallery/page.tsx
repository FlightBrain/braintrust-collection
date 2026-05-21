"use client";

import { useEffect, useState } from "react";
import { Header } from "@/components/Header";
import { FooterNav } from "@/components/FooterNav";
import { RarityBadge } from "@/components/RarityBadge";
import { NftCard } from "@/components/NftCard";
import { VariantDetailModal, type VariantData } from "@/components/VariantDetailModal";
import { describeVariant, whyThisCard, type Tier } from "@/lib/card-copy";

type Person = { slug: string; name: string };
type Attr = { trait_type: string; value: string | number };
type TokenMeta = { name: string; description: string; image: string; attributes: Attr[] };

const TIERS: { tier: Tier; key: "common" | "rare" | "mythic" }[] = [
  { tier: "Common", key: "common" },
  { tier: "Rare", key: "rare" },
  { tier: "Mythic", key: "mythic" },
];

export default function GalleryPage() {
  const [people, setPeople] = useState<Person[]>([]);
  const [metadata, setMetadata] = useState<Record<number, TokenMeta>>({});
  const [selected, setSelected] = useState<VariantData | null>(null);

  useEffect(() => {
    (async () => {
      const peopleRes = await fetch("/auto_people.json");
      const peopleJson: Person[] = await peopleRes.json();
      setPeople(peopleJson);
      // Fetch all 45 metadata files in parallel
      const promises = peopleJson.flatMap((_, sdrIdx) =>
        [0, 1, 2].map(async (v) => {
          const tokenId = sdrIdx * 3 + v;
          const r = await fetch(`/metadata/${tokenId}.json`);
          if (!r.ok) return null;
          const d: TokenMeta = await r.json();
          return [tokenId, d] as const;
        })
      );
      const results = await Promise.all(promises);
      const map: Record<number, TokenMeta> = {};
      for (const r of results) if (r) map[r[0]] = r[1];
      setMetadata(map);
    })();
  }, []);

  const openVariant = (sdrIdx: number, variantIdx: number, person: Person) => {
    const tokenId = sdrIdx * 3 + variantIdx;
    const m = metadata[tokenId];
    if (!m) return;
    setSelected({
      tokenId,
      slug: person.slug,
      name: person.name,
      tier: TIERS[variantIdx].tier,
      variantNumber: variantIdx + 1,
      imagePath: `/nfts/variants/${person.slug}_${TIERS[variantIdx].key}.svg`,
      attributes: m.attributes,
    });
  };

  return (
    <main>
      <Header />
      <section className="mx-auto max-w-6xl px-4 pb-12 pt-12 sm:px-6">
        <p className="font-mono text-[10px] uppercase tracking-[0.24em] text-muted">
          The collection
        </p>
        <h1 className="mt-2 text-4xl font-black tracking-tight md:text-5xl">
          45 cards. 15 coworkers. 3 variants each.
        </h1>
        <p className="mt-3 max-w-2xl text-sm leading-relaxed text-muted">
          A wallet-bound mint: each coworker can claim their own three cards,
          one Common, one Rare, one Mythic. Click any card to flip it and
          read about that variant.
        </p>

        {/* Rarity legend */}
        <div className="mt-6 flex flex-wrap gap-2">
          <RarityBadge tier="Common" size="md" />
          <RarityBadge tier="Rare" size="md" />
          <RarityBadge tier="Mythic" size="md" />
        </div>

        {/* Grid grouped by person */}
        <div className="mt-10 space-y-12">
          {people.map((p, sdrIdx) => (
            <div key={p.slug}>
              <div className="mb-4 flex items-baseline justify-between border-b border-line pb-2">
                <h2 className="text-lg font-bold tracking-tight">{p.name}</h2>
                <span className="font-mono text-[10px] uppercase tracking-[0.2em] text-muted">
                  tokens {sdrIdx * 3}–{sdrIdx * 3 + 2}
                </span>
              </div>
              <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
                {TIERS.map((t, vIdx) => {
                  const tokenId = sdrIdx * 3 + vIdx;
                  const meta = metadata[tokenId];
                  if (!meta) {
                    return (
                      <div
                        key={t.key}
                        className="aspect-square rounded-2xl border border-line bg-panel"
                        aria-label="Loading"
                      />
                    );
                  }
                  return (
                    <NftCard
                      key={t.key}
                      name={p.name}
                      slug={p.slug}
                      tier={t.tier}
                      tokenId={tokenId}
                      variantNumber={vIdx + 1}
                      imagePath={`/nfts/variants/${p.slug}_${t.key}.svg`}
                      description={describeVariant({
                        tier: t.tier,
                        name: p.name,
                        accessoryCount: meta.attributes.filter((a) =>
                          a.trait_type.startsWith("Accessory: ")
                        ).length,
                        accessoryNames: meta.attributes
                          .filter((a) => a.trait_type.startsWith("Accessory: "))
                          .map(
                            (a) =>
                              `${a.trait_type.replace(/^Accessory: /, "")}__${a.value}`
                          ),
                      })}
                      whyText={whyThisCard({ tier: t.tier, name: p.name })}
                      attributes={meta.attributes}
                      flippable={false}
                      onClick={() => openVariant(sdrIdx, vIdx, p)}
                    />
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      </section>

      <VariantDetailModal variant={selected} onClose={() => setSelected(null)} />

      <FooterNav />
    </main>
  );
}
