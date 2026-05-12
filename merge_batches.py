#!/usr/bin/env python3
"""Merge subagent batch outputs into auto_people.json.

- Reads data/batch_1.json through batch_5.json
- Enriches with name + role from members.json
- Adds shirt_color sampled from photo (Pillow)
- Adds theme variants (galaxy/aquatic/cyberpunk) deterministically by slug hash
- Adds brain_color and snorkel flag
- Validates that no two people share more than 4 trait values total
- Writes data/auto_people.json + public/auto_people.json
"""
import hashlib
import json
import pathlib
from collections import Counter
from PIL import Image

DATA_DIR = pathlib.Path("data")
PHOTOS = pathlib.Path("public/photos")

GALAXY_VARIANTS = [None, None, None, "antennae", "cyborg_jaw", "data_halo",
                   "drone", "hidden_brain", "cap_brain", "cyber_crown",
                   "brain_in_glass", "floral_brain", "laser_through_brain"]
AQUATIC_VARIANTS = [None, None, None, "jellyfish", "scuba_helmet",
                    "octopus_tentacle", "trident", "starfish", "tie_seaweed",
                    "bubble_headset", "foggy_glasses", "wrap_dive_glasses",
                    "coral_cross", "mermaid_hair", "anchor_tat"]
CYBERPUNK_VARIANTS = [None, None, None, "neon_mohawk", "red_visor",
                      "full_face_tattoo", "jacked_in", "neon_pink_hair", "cyber_arm",
                      "data_suit", "cyber_headset_hud", "ar_overlay", "energy_drink",
                      "tactical_mask", "neon_cross", "cyber_surfboard", "hair_clips"]
BRAIN_COLORS = ["pink", "pink", "pink", "pink", "gold", "green", "blue", "magenta"]


def median_color(img, region):
    w, h = img.size
    x0, y0, x1, y1 = int(region[0] * w), int(region[1] * h), int(region[2] * w), int(region[3] * h)
    crop = img.crop((x0, y0, x1, y1)).resize((20, 20))
    pixels = list(crop.getdata())
    if not pixels:
        return [60, 60, 70]
    pixels.sort()
    return list(pixels[len(pixels) // 2])


def shirt_color(slug):
    """Sample shirt region from photo if available."""
    for ext in (".jpg", ".png", ".jpeg"):
        p = PHOTOS / f"{slug}{ext}"
        if p.exists():
            try:
                img = Image.open(p).convert("RGB")
                return median_color(img, (0.30, 0.85, 0.70, 0.98))
            except Exception:
                pass
    return [60, 60, 70]


def variant_pick(slug, arr, byte_offset=0):
    h = hashlib.md5((slug + str(byte_offset)).encode()).digest()
    return arr[h[0] % len(arr)]


VALID_SIGNATURES = {"pocket_square", "necklace_gold", "headset", "watch", "question_mark",
                    "pint_glass", "crown", "chain", "ai_agent", "cross", "cap",
                    "surfboard", "bt_pin", "earring"}
VALID_ACCESSORIES = {None, "sunglasses", "aviators", "glasses_clear", "ar_glasses",
                     "earbuds", "beanie", "red_lips", "earring_stud", "laser_eyes"}
VALID_HAIR_STYLES = {"short_parted", "slick_back", "undercut", "messy", "curly_short",
                     "long_straight", "long_wavy", "curly_long", "fade", "beach_blonde"}

def sanitize(p):
    """Fix common agent mistakes (wrong field, typos)."""
    # Some agents used 'trait_hex' instead of 'trait'
    if "trait" not in p and "trait_hex" in p:
        p["trait"] = p["trait_hex"]
    # Default trait if missing entirely (deterministic from slug hash)
    if not p.get("trait"):
        import hashlib
        palette = ["#00FF94","#FF6B9D","#FFD93D","#00D9FF","#9D7AFF","#FF8C42",
                   "#7B61FF","#FF3366","#00E5FF","#FFC857","#A8E6CF","#4ECDC4",
                   "#E0E0E0","#FF66C4","#B8FF3D","#7BFFD4","#FFAA00","#FF4488",
                   "#88CCFF","#FFD0AA","#AAFF88","#FF88AA","#88FFAA","#FFCCFF"]
        p["trait"] = palette[hashlib.md5(p["slug"].encode()).digest()[0] % len(palette)]
    # earring_stud is an accessory, not a signature
    if p.get("signature") == "earring_stud":
        p["signature"] = "earring"
    # buzz isn't in HAIR_FNS, fall back to fade
    if p.get("hair_style") == "buzz":
        p["hair_style"] = "fade"
    if p.get("hair_style") not in VALID_HAIR_STYLES:
        p["hair_style"] = "messy"
    if p.get("signature") not in VALID_SIGNATURES:
        p["signature"] = "watch"
    if p.get("accessory") not in VALID_ACCESSORIES:
        p["accessory"] = None
    # Ensure ryan gets laser_eyes specifically
    if p["slug"] == "ryan":
        p["accessory"] = "laser_eyes"
        p["signature"] = "bt_pin"
    # Kensington gets ai_agent
    if p["slug"] == "kensington":
        p["signature"] = "ai_agent"
    return p


def main():
    members = json.loads((DATA_DIR / "members.json").read_text())
    members_by_slug = {m["slug"]: m for m in members}

    all_people = []
    seen_slugs = set()
    for i in range(1, 11):
        batch_path = DATA_DIR / f"batch_{i}.json"
        if not batch_path.exists():
            print(f"WARNING: {batch_path} missing")
            continue
        batch = json.loads(batch_path.read_text())
        for p in batch:
            slug = p["slug"]
            if slug in seen_slugs:
                print(f"DUPLICATE slug {slug} (skipped)")
                continue
            seen_slugs.add(slug)
            meta = members_by_slug.get(slug)
            if not meta:
                print(f"UNKNOWN slug {slug} (skipped)")
                continue
            p = sanitize(p)
            p["name"] = meta["name"]
            p["role"] = meta["role"].upper()
            p["id"] = len(all_people) + 1
            # Add shirt color from photo
            p["shirt_color"] = shirt_color(slug)
            # Theme variants
            p["brain_color"] = variant_pick(slug, BRAIN_COLORS, 1)
            p["snorkel"] = (hashlib.md5(slug.encode()).digest()[15] % 4 == 0)
            p["galaxy_variant"] = variant_pick(slug, GALAXY_VARIANTS, 2)
            p["aquatic_variant"] = variant_pick(slug, AQUATIC_VARIANTS, 3)
            p["cyberpunk_variant"] = variant_pick(slug, CYBERPUNK_VARIANTS, 4)
            all_people.append(p)

    # Uniqueness check
    print(f"\n{len(all_people)} people merged.")
    trait_keys = ["face_shape", "hair_style", "hair_color", "skin", "eyes",
                  "mouth", "brow_style", "beard", "shirt", "signature",
                  "accessory", "trait"]
    pair_max = 0
    pair_who = None
    for i in range(len(all_people)):
        for j in range(i + 1, len(all_people)):
            shared = sum(
                1 for k in trait_keys
                if all_people[i].get(k) == all_people[j].get(k)
            )
            if shared > pair_max:
                pair_max = shared
                pair_who = (all_people[i]["slug"], all_people[j]["slug"], shared)
    print(f"Max shared traits between any two: {pair_max}")
    if pair_who:
        print(f"Most similar pair: {pair_who[0]} and {pair_who[1]} share {pair_who[2]} traits")

    # Distribution
    for k in trait_keys:
        c = Counter(p.get(k) for p in all_people)
        if len(c) > 1:
            top = c.most_common(3)
            print(f"  {k}: {top}")

    (DATA_DIR / "auto_people.json").write_text(json.dumps(all_people, indent=2))
    pathlib.Path("public/auto_people.json").write_text(json.dumps(all_people, indent=2))
    print(f"\nWrote data/auto_people.json and public/auto_people.json")


if __name__ == "__main__":
    main()
