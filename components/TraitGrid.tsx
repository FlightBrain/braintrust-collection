/**
 * Filtered, collector-friendly trait pills.
 *
 * Hides internal/admin trait_types and reorders what's shown so the most
 * useful traits come first.
 */
type Attr = { trait_type: string; value: string | number };

const HIDE = new Set([
  "SDR Index",
  "Original Rank",
  "Trait Color",
  "Variants Total",
]);

const PRIORITY = [
  "Name",
  "Variant",
  "Variant Rarity",
  "Original Rarity",
  "Edition",
];

function sortAttrs(attrs: Attr[]): Attr[] {
  return [...attrs]
    .filter((a) => !HIDE.has(a.trait_type))
    .sort((a, b) => {
      const ai = PRIORITY.indexOf(a.trait_type);
      const bi = PRIORITY.indexOf(b.trait_type);
      if (ai !== -1 && bi !== -1) return ai - bi;
      if (ai !== -1) return -1;
      if (bi !== -1) return 1;
      // Accessory: x sort by trait_type alphabetically for stability
      return a.trait_type.localeCompare(b.trait_type);
    });
}

export function TraitGrid({ attributes }: { attributes: Attr[] }) {
  const visible = sortAttrs(attributes);
  return (
    <div className="grid grid-cols-2 gap-2 sm:grid-cols-3">
      {visible.map((a, i) => (
        <div
          key={i}
          className="rounded-lg border border-line bg-bg/40 px-3 py-2"
        >
          <div className="font-mono text-[9px] uppercase tracking-[0.18em] text-muted">
            {a.trait_type.replace(/^Accessory: /, "").replace(/_/g, " ")}
          </div>
          <div className="mt-1 text-sm font-semibold text-white">
            {typeof a.value === "string"
              ? a.value.replace(/_/g, " ")
              : a.value}
          </div>
        </div>
      ))}
    </div>
  );
}
