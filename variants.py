#!/usr/bin/env python3
"""Variant farm: composite every accessory over the face template.

Output: public/variants/{category}/{accessory}__{color}.png
Manifest: public/variants/manifest.json
"""
import json
import pathlib
import shutil

from items_v3 import new_canvas
from face_template import draw_face_template
from accessories_v3 import ACCESSORIES

OUT = pathlib.Path("public/variants")

# Category routing for sectioning in the picker
CATEGORY = {
    "king_crown":         "head",
    "jeweled_crown":      "head",
    "laurel_crown":       "head",
    "top_hat":            "head",
    "beanie":             "head",
    "cowboy_hat":         "head",
    "devil_horns":        "head",
    "halo":               "head",
    "wizard_hat":         "head",

    "pixel_shades":       "eyes",
    "aviators":           "eyes",
    "three_d_glasses":    "eyes",
    "vr_headset":         "eyes",
    "cyber_visor":        "eyes",
    "monocle":            "eyes",
    "eyepatch":           "eyes",
    "laser_eyes":         "eyes",
    "laser_eyes_rainbow": "eyes",
    "money_eyes":         "eyes",
    "x_eyes":             "eyes",
    "glowing_eyes":       "eyes",

    "cigar":              "mouth",
    "cigarette":          "mouth",
    "vampire_fangs":      "mouth",
    "gold_grill":         "mouth",

    "fat_gold_chain":     "neck",
    "diamond_chain":      "neck",
    "bowtie":             "neck",

    "face_tattoo":        "face",
    "scar":               "face",
    "mustache_handlebar": "face",
    "blush":              "face",
}

CATEGORY_ORDER = ["head", "eyes", "mouth", "neck", "face"]


def clean_output():
    if not OUT.exists():
        return
    for sub in OUT.iterdir():
        if sub.is_dir() and not sub.name.startswith("_"):
            shutil.rmtree(sub)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    clean_output()

    manifest = {"categories": {cat: {} for cat in CATEGORY_ORDER}}
    total = 0

    for name, (fn, colors) in ACCESSORIES.items():
        cat = CATEGORY.get(name, "face")
        item_dir = OUT / cat / name
        item_dir.mkdir(parents=True, exist_ok=True)
        variants = []

        for color in colors:
            canvas = new_canvas()
            draw_face_template(canvas)
            try:
                if color is None:
                    fn(canvas)
                else:
                    fn(canvas, color=color)
            except TypeError:
                fn(canvas)

            color_label = color or "default"
            fname = f"{color_label}.png"
            canvas.save(item_dir / fname)
            variants.append({
                "id": f"{name}__{color_label}",
                "path": f"variants/{cat}/{name}/{fname}",
                "color": color_label,
            })
            total += 1

        manifest["categories"][cat][name] = variants

    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"wrote {total} accessory variants across {len(ACCESSORIES)} accessories")
    print(f"manifest: {OUT / 'manifest.json'}")


if __name__ == "__main__":
    main()
