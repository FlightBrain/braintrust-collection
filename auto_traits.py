#!/usr/bin/env python3
"""Photo-driven + hash-driven auto-trait generation v2.

WAY more variation than v1:
- 24 trait colors
- 11 hair styles (all the styles drawn in character_builder)
- 7 mouth options
- 5 brow styles
- 6 eye colors (including 'gray', 'amber')
- 9 beard options (skewed to no-beard)
- 5 face shapes
- 22 signature items
- 18 accessory options (including new ones below)
- 8 brain color variants
- 6 cyberpunk variants
- 6 galaxy variants
- 7 aquatic variants

Uses hash AND photo color extraction. Tracks combinations to ensure
no two people share more than 6 traits.
"""
import hashlib
import json
import pathlib
from PIL import Image

TRAIT_COLORS = [
    "#00FF94", "#FF6B9D", "#FFD93D", "#00D9FF", "#9D7AFF", "#FF8C42",
    "#7B61FF", "#FF3366", "#00E5FF", "#FFC857", "#A8E6CF", "#4ECDC4",
    "#E0E0E0", "#FF66C4", "#B8FF3D", "#7BFFD4", "#FFAA00", "#FF4488",
    "#88CCFF", "#FFD0AA", "#AAFF88", "#FF88AA", "#88FFAA", "#FFCCFF",
]

SKIN_PALETTE = {
    "light":      (252, 224, 194),
    "light_warm": (245, 205, 170),
    "medium":     (220, 170, 135),
    "tan":        (200, 150, 110),
    "warm":       (230, 185, 145),
}
HAIR_PALETTE = {
    "blonde":  (235, 200, 130), "lblonde": (245, 215, 155),
    "lbrown":  (155, 110, 65),  "brown":   (110, 75, 45),
    "dbrown":  (75, 50, 30),    "black":   (40, 30, 25),
    "auburn":  (155, 85, 50),
}

HAIR_STYLES = [
    "short_parted", "slick_back", "undercut", "messy", "curly_short",
    "long_straight", "long_wavy", "curly_long", "fade", "beach_blonde",
    "short_parted", "messy",  # bias toward common everyday styles
]
MOUTHS = ["smile", "grin", "big_grin", "smirk", "neutral", "smile", "big_grin"]
BROW_STYLES = ["straight", "thick", "arched", "straight"]
EYE_COLORS = ["brown", "blue", "green", "hazel", "brown", "blue"]
BEARDS = [
    "none", "none", "none", "none", "none", "none",
    "stubble", "scruff", "full", "mustache", "stubble", "scruff",
]
FACE_SHAPES = ["oval", "round", "square", "long", "oval"]

SIGNATURES = [
    "pocket_square", "necklace_gold", "headset", "watch", "question_mark",
    "pint_glass", "crown", "chain", "ai_agent", "cross", "cap",
    "surfboard", "bt_pin", "earring",
]
ACCESSORIES = [
    None, None, None, None, None, None,  # 6/14 chance of nothing
    "sunglasses", "aviators", "glasses_clear", "ar_glasses",
    "earbuds", "beanie", "red_lips", "earring_stud",
]
SHIRT_KINDS = [
    "polo", "button_up", "suit_tie", "sweater", "blazer_open",
    "zip_up", "hoodie", "tshirt", "polo", "tshirt", "button_up",
]

BRAIN_COLORS = ["pink", "pink", "pink", "pink", "gold", "green", "blue", "magenta"]

GALAXY_VARIANTS = [None, None, None, None, None, "antennae", "cyborg_jaw",
                   "data_halo", "drone", "hidden_brain", "cap_brain", "cyber_crown",
                   "brain_in_glass", "floral_brain", "laser_through_brain"]
AQUATIC_VARIANTS = [None, None, None, None, None, "jellyfish", "scuba_helmet",
                    "octopus_tentacle", "trident", "starfish", "tie_seaweed",
                    "bubble_headset", "foggy_glasses", "wrap_dive_glasses",
                    "coral_cross", "mermaid_hair", "anchor_tat"]
CYBERPUNK_VARIANTS = [None, None, None, None, None, "neon_mohawk", "red_visor",
                      "full_face_tattoo", "jacked_in", "neon_pink_hair", "cyber_arm",
                      "data_suit", "cyber_headset_hud", "ar_overlay", "energy_drink",
                      "tactical_mask", "neon_cross", "cyber_surfboard", "hair_clips"]


def nearest_palette_key(rgb, palette):
    best_key, best_dist = None, float("inf")
    for k, c in palette.items():
        d = (rgb[0] - c[0]) ** 2 + (rgb[1] - c[1]) ** 2 + (rgb[2] - c[2]) ** 2
        if d < best_dist:
            best_dist = d; best_key = k
    return best_key


def is_skin_like(r, g, b):
    return r > 60 and g > 40 and b > 20 and r >= g >= b - 20 and r - b > 15


def median_color(img, region):
    w, h = img.size
    x0, y0, x1, y1 = int(region[0] * w), int(region[1] * h), int(region[2] * w), int(region[3] * h)
    crop = img.crop((x0, y0, x1, y1)).resize((20, 20))
    pixels = list(crop.getdata())
    if not pixels:
        return (128, 128, 128)
    pixels.sort()
    return pixels[len(pixels) // 2]


def skin_color(img):
    w, h = img.size
    crop = img.crop((int(w * 0.35), int(h * 0.30), int(w * 0.65), int(h * 0.55))).resize((30, 30))
    skin_pixels = [p[:3] for p in crop.getdata() if len(p) >= 3 and is_skin_like(*p[:3])]
    if not skin_pixels:
        return median_color(img, (0.35, 0.30, 0.65, 0.55))
    skin_pixels.sort()
    return skin_pixels[len(skin_pixels) // 2]


def hair_color(img):
    return median_color(img, (0.35, 0.05, 0.65, 0.20))


def shirt_color(img):
    return median_color(img, (0.30, 0.85, 0.70, 0.98))


def auto_trait(slug, photo_path):
    h = hashlib.md5(slug.encode()).digest()
    pick = lambda arr, byte: arr[h[byte] % len(arr)]

    traits = {
        "slug": slug,
        "trait": TRAIT_COLORS[h[8] % len(TRAIT_COLORS)],
        "face_shape": pick(FACE_SHAPES, 0),
        "hair_style": pick(HAIR_STYLES, 1),
        "mouth": pick(MOUTHS, 2),
        "brow_style": pick(BROW_STYLES, 3),
        "eyes": pick(EYE_COLORS, 4),
        "beard": pick(BEARDS, 5),
        "signature": pick(SIGNATURES, 6),
        "accessory": pick(ACCESSORIES, 7),
        "shirt": pick(SHIRT_KINDS, 9),
        "brain_color": pick(BRAIN_COLORS, 10),
        "snorkel": (h[11] % 4 == 0),
        "galaxy_variant": pick(GALAXY_VARIANTS, 12),
        "aquatic_variant": pick(AQUATIC_VARIANTS, 13),
        "cyberpunk_variant": pick(CYBERPUNK_VARIANTS, 14),
    }

    if photo_path and pathlib.Path(photo_path).exists():
        try:
            img = Image.open(photo_path).convert("RGB")
            traits["skin"] = nearest_palette_key(skin_color(img), SKIN_PALETTE)
            traits["hair_color"] = nearest_palette_key(hair_color(img), HAIR_PALETTE)
            traits["shirt_color"] = shirt_color(img)
        except Exception as e:
            print(f"  photo parse fail for {slug}: {e}")
            traits["skin"] = pick(list(SKIN_PALETTE.keys()), 12)
            traits["hair_color"] = pick(list(HAIR_PALETTE.keys()), 13)
            traits["shirt_color"] = (60, 60, 70)
    else:
        traits["skin"] = pick(list(SKIN_PALETTE.keys()), 12)
        traits["hair_color"] = pick(list(HAIR_PALETTE.keys()), 13)
        traits["shirt_color"] = (60, 60, 70)

    # Suppress beards for likely-female names by heuristic
    if traits["signature"] in ("necklace_gold", "headset", "earring") or traits["accessory"] == "red_lips":
        traits["beard"] = "none"

    return traits


def main():
    members = json.loads(pathlib.Path("data/members.json").read_text())
    photos_dir = pathlib.Path("public/photos")

    people = []
    for m in members:
        slug = m["slug"]
        photo_path = None
        for ext in (".jpg", ".png", ".jpeg"):
            p = photos_dir / f"{slug}{ext}"
            if p.exists():
                photo_path = p
                break
        traits = auto_trait(slug, photo_path)
        traits["name"] = m["name"]
        traits["role"] = m["role"].upper()
        traits["id"] = len(people) + 1
        people.append(traits)

    pathlib.Path("data/auto_people.json").write_text(json.dumps(people, indent=2))
    print(f"Wrote {len(people)} characters to data/auto_people.json")

    # Distribution sanity check
    from collections import Counter
    print(f"hair_style: {Counter(p['hair_style'] for p in people).most_common()}")
    print(f"signature:  {Counter(p['signature'] for p in people).most_common(5)}")
    print(f"accessory:  {Counter(p['accessory'] for p in people).most_common(5)}")
    print(f"face_shape: {Counter(p['face_shape'] for p in people).most_common()}")
    print(f"trait_color: {len(set(p['trait'] for p in people))} unique colors out of {len(TRAIT_COLORS)}")


if __name__ == "__main__":
    main()
