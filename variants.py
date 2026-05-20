#!/usr/bin/env python3
"""Variant farm: composite every accessory over the face template.

Merges v3 base accessories with v2 expansions from 4 parallel agent outputs.
v2 entries OVERRIDE same-named v3 entries (the fixes).

Output: public/variants/{category}/{accessory}/{color}.png
Manifest: public/variants/manifest.json
"""
import json
import pathlib
import shutil

from items_v3 import new_canvas
from face_template import draw_face_template

# Base v3
from accessories_v3 import ACCESSORIES as ACC_V3
# v2 expansions
from accessories_head_v2 import ACCESSORIES_HEAD_V2
from accessories_eyes_v2 import ACCESSORIES_EYES_V2
from accessories_neck_v2 import ACCESSORIES_NECK_V2
from accessories_mouthface_v2 import ACCESSORIES_MOUTHFACE_V2


# === Merge: v2 overrides v3 for matching names ===
ACCESSORIES = {}
ACCESSORIES.update(ACC_V3)
ACCESSORIES.update(ACCESSORIES_HEAD_V2)
ACCESSORIES.update(ACCESSORIES_EYES_V2)
ACCESSORIES.update(ACCESSORIES_NECK_V2)
ACCESSORIES.update(ACCESSORIES_MOUTHFACE_V2)


# === Category routing ===
CATEGORY = {
    # HEAD
    "king_crown":         "head",
    "jeweled_crown":      "head",
    "laurel_crown":       "head",
    "top_hat":            "head",
    "beanie":             "head",
    "cowboy_hat":         "head",
    "devil_horns":        "head",
    "halo":               "head",
    "wizard_hat":         "head",
    "spartan_helmet":     "head",
    "motorcycle_helmet":  "head",
    "baseball_cap":       "head",
    "durag":              "head",
    "knight_helmet":      "head",
    "crown_of_thorns":    "head",
    "viking_helmet":      "head",
    "headband":           "head",

    # EYES
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
    "heart_eyes":         "eyes",
    "hypnosis_swirl":     "eyes",
    "third_eye":          "eyes",
    "kaleidoscope_eyes":  "eyes",
    "anime_sparkle_eyes": "eyes",
    "blindfold":          "eyes",
    "skull_eye_socket":   "eyes",
    "evil_red_glow":      "eyes",
    "cyber_implant":      "eyes",
    "tear_drop_blood":    "eyes",

    # MOUTH
    "cigar":              "mouth",
    "cigarette":          "mouth",
    "vampire_fangs":      "mouth",
    "gold_grill":         "mouth",
    "pipe_sherlock":      "mouth",
    "joint":              "mouth",
    "gold_tooth_single":  "mouth",
    "lipstick":           "mouth",
    "tongue_out":         "mouth",
    "bubble_gum_bubble":  "mouth",

    # NECK
    "fat_gold_chain":     "neck",
    "diamond_chain":      "neck",
    "bowtie":             "neck",
    "necktie":            "neck",
    "pearl_necklace":     "neck",
    "brain_pendant_chain":"neck",
    "dog_tags":           "neck",
    "bandana_neck":       "neck",
    "ascot":              "neck",
    "choker_spike":       "neck",
    "crystal_pendant":    "neck",
    "gold_medallion":     "neck",

    # FACE
    "face_tattoo":        "face",
    "scar":               "face",
    "mustache_handlebar": "face",
    "blush":              "face",
    "kiss_print":         "face",
    "mustache_chevron":   "face",
    "beard_full":         "face",
    "goatee":             "face",
    "face_paint_war":     "face",
    "freckles":           "face",
    "birthmark_star":     "face",
}

CATEGORY_ORDER = ["head", "eyes", "mouth", "neck", "face"]

OUT = pathlib.Path("public/variants")


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
    skipped = []

    for name, (fn, colors) in ACCESSORIES.items():
        cat = CATEGORY.get(name)
        if cat is None:
            skipped.append(name)
            continue
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
            except Exception as e:
                print(f"  ! {name} ({color}): {e}")
                continue

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
    print(f"wrote {total} accessory variants across {len(ACCESSORIES) - len(skipped)} accessories")
    if skipped:
        print(f"skipped {len(skipped)} unmapped: {skipped}")
    print(f"manifest: {OUT / 'manifest.json'}")
    # Per-category breakdown
    for cat in CATEGORY_ORDER:
        items = manifest["categories"][cat]
        variant_count = sum(len(v) for v in items.values())
        print(f"  {cat}: {len(items)} accessories, {variant_count} variants")


if __name__ == "__main__":
    main()
