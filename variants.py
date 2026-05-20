#!/usr/bin/env python3
"""Variant farm: sweep every item across palettes + sizes.

Output: public/variants/{item}/{palette}_{size}.png

Also writes public/variants/manifest.json so picker.html can render the grid
without hardcoding paths.
"""
import json
import pathlib
import shutil

from items_v3 import new_canvas, SPHERE_PALETTES
from items_v3_lib import ITEMS

OUT = pathlib.Path("public/variants")

# Per-item palette choices. Some items only make sense in certain colors.
ITEM_PALETTES = {
    "ai_orb_v2":     ["cyber", "emerald", "amethyst", "plasma", "molten", "holo"],
    "crystal_ball":  ["amethyst", "sapphire", "ruby", "emerald", "void", "holo"],
    "plasma_sphere": ["plasma", "cyber", "amethyst", "molten", "void", "holo"],
    "brain_orb":     ["ruby", "amethyst", "plasma", "emerald", "gold", "molten"],
    "halo_orb":      ["gold", "holo", "emerald", "sapphire", "amethyst", "ruby"],
    "disco_ball":    ["holo", "amethyst", "gold", "cyber", "ruby", "emerald"],
    "lightning":     ["gold", "cyber", "plasma", "ruby", "emerald", "holo"],
    "neon_dollar":   ["emerald", "gold", "cyber", "plasma", "ruby", "molten"],
}

SIZES = ["M", "L"]  # Skip S, too small for a contact sheet pick


def clean_output():
    for sub in OUT.iterdir() if OUT.exists() else []:
        if sub.is_dir() and not sub.name.startswith("_"):
            shutil.rmtree(sub)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    clean_output()

    manifest = {"items": {}}
    total = 0

    for item_name, fn in ITEMS.items():
        item_dir = OUT / item_name
        item_dir.mkdir(parents=True, exist_ok=True)
        variants = []

        for palette in ITEM_PALETTES.get(item_name, list(SPHERE_PALETTES)[:6]):
            for size in SIZES:
                vid = f"{palette}_{size}"
                canvas = new_canvas()
                try:
                    fn(canvas, palette_name=palette, size=size)
                except TypeError:
                    # Item doesn't take palette/size kwargs, render default
                    canvas = new_canvas()
                    fn(canvas)
                rel = f"variants/{item_name}/{vid}.png"
                canvas.save(OUT / item_name / f"{vid}.png")
                variants.append({
                    "id": f"{item_name}__{vid}",
                    "path": rel,
                    "palette": palette,
                    "size": size,
                })
                total += 1

        manifest["items"][item_name] = variants

    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"wrote {total} variants across {len(ITEMS)} items")
    print(f"manifest: {OUT / 'manifest.json'}")


if __name__ == "__main__":
    main()
