#!/usr/bin/env python3
"""Generate 45 NFT variant SVGs (15 SDRs x 3 tiers).

Tiers:
  - Common: personalized face only, no accessories. Plain card frame.
  - Rare:   personalized face + KB's curated assignment. Silver gradient frame, RARE badge.
  - Mythic: Rare loadout + 1 premium add (gold_medallion / halo_gold / face_tattoo_star).
            Gold gradient frame with sparkles, MYTHIC badge, warm backdrop.

Output: public/nfts/variants/{slug}_{common,rare,mythic}.svg

DOES NOT TOUCH public/nfts/corporate/*.svg. Those originals remain unchanged.
"""
import base64
import io
import json
import pathlib

from items_v3 import new_canvas
from face_template_v2 import draw_personalized_face
from accessories_v3 import ACCESSORIES as ACC_V3
from accessories_head_v2 import ACCESSORIES_HEAD_V2
from accessories_eyes_v2 import ACCESSORIES_EYES_V2
from accessories_neck_v2 import ACCESSORIES_NECK_V2
from accessories_mouthface_v2 import ACCESSORIES_MOUTHFACE_V2
from assign import ASSIGNMENTS, category_of, LAYER_ORDER

# Merge every accessory registry into one map
ACCESSORIES = {}
ACCESSORIES.update(ACC_V3)
ACCESSORIES.update(ACCESSORIES_HEAD_V2)
ACCESSORIES.update(ACCESSORIES_EYES_V2)
ACCESSORIES.update(ACCESSORIES_NECK_V2)
ACCESSORIES.update(ACCESSORIES_MOUTHFACE_V2)

PEOPLE_PATH = pathlib.Path("public/auto_people.json")
OUT_DIR = pathlib.Path("public/nfts/variants")

TRAIT_NAMES = {
    "#00FF94":"EMERALD", "#FF6B9D":"ROSE", "#FFD93D":"GOLD", "#00D9FF":"CYAN",
    "#9D7AFF":"AMETHYST", "#FF8C42":"AMBER", "#7B61FF":"VIOLET", "#FF3366":"CRIMSON",
    "#00E5FF":"ELECTRIC", "#FFC857":"SOLAR", "#A8E6CF":"MINT", "#4ECDC4":"TEAL",
    "#E0E0E0":"PLATINUM", "#FF66C4":"MAGENTA", "#B8FF3D":"LIME", "#7BFFD4":"AQUA",
    "#FFAA00":"SUN", "#FF4488":"BLUSH", "#88CCFF":"SKY", "#FFD0AA":"SAND",
}


def trait_name(trait_hex):
    return TRAIT_NAMES.get(trait_hex.upper(), "CHROMA")


def darken(hex_color, factor=0.18):
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"#{int(r*factor):02X}{int(g*factor):02X}{int(b*factor):02X}"


def make_grid_lines():
    lines = []
    for x in range(0, 1024, 64):
        lines.append(f'<line x1="{x}" y1="0" x2="{x}" y2="1024" stroke="#0F1320" stroke-width="1"/>')
    for y in range(0, 1024, 64):
        lines.append(f'<line x1="0" y1="{y}" x2="1024" y2="{y}" stroke="#0F1320" stroke-width="1"/>')
    return "\n    ".join(lines)


def render_png(traits, accessories_list):
    """Render a 48x48 PNG: personalized face + listed accessories. Returns PNG bytes."""
    canvas = new_canvas()
    draw_personalized_face(canvas, traits)
    sorted_items = sorted(
        accessories_list,
        key=lambda i: LAYER_ORDER[category_of(i.split("__")[0])],
    )
    for item_id in sorted_items:
        if "__" not in item_id:
            continue
        acc_name, color = item_id.split("__", 1)
        if acc_name not in ACCESSORIES:
            continue
        fn, _ = ACCESSORIES[acc_name]
        color_val = None if color == "default" else color
        try:
            if color_val is None:
                fn(canvas)
            else:
                fn(canvas, color=color_val)
        except TypeError:
            fn(canvas)
    buf = io.BytesIO()
    canvas.save(buf, format="PNG")
    return buf.getvalue()


def mythic_addons_for(rare_items):
    """Deprecated: see MYTHIC_LOADOUTS below for hand-curated per-SDR sets."""
    return []


# BANNED accessories: never use these in any loadout. KB feedback says the
# multi-color rainbow eye designs read as cheap. Keep them out of every tier.
BANNED_ACCESSORIES = {"laser_eyes_rainbow", "kaleidoscope_eyes"}


# Hand-curated Mythic loadout per SDR. The Mythic tier is NOT a uniform addon
# on top of Rare; each SDR gets a unique premium kit that reflects their
# personality. One item per slot (head/eyes/mouth/neck/face) to avoid visual
# overlap inside the same pixel zone.
MYTHIC_LOADOUTS = {
    "alec":       ["top_hat__silver",       "monocle__gold",           "fat_gold_chain__gold",     "mustache_handlebar__black"],
    "ava":        ["halo__gold",            "heart_eyes__red",         "pearl_necklace__white",    "face_tattoo__heart"],
    "catherine":  ["laurel_crown__gold",    "heart_eyes__pink",        "diamond_chain__white",     "kiss_print__red"],
    "chris":      ["motorcycle_helmet__red", "fat_gold_chain__gold",   "scar__default"],
    "duncan":     ["wizard_hat__purple",    "glowing_eyes__cyan",      "ascot__navy",              "goatee__black"],
    "evan":       ["durag__black",          "money_eyes__gold",        "gold_grill__diamond",      "diamond_chain__white"],
    "garrett":    ["king_crown__gold",      "cigar__brown",            "diamond_chain__white",     "beard_full__black"],
    "joe":        ["spartan_helmet__bronze", "glowing_eyes__red",      "fat_gold_chain__gold",     "face_tattoo__dollar"],
    "kensington": ["jeweled_crown__gold",   "cyber_visor__cyan",       "gold_medallion__gold"],
    "keslar":     ["viking_helmet__bronze", "glowing_eyes__yellow",    "ascot__red",               "beard_full__red"],
    "nick":       ["top_hat__black",        "monocle__gold",           "necktie__striped",         "mustache_handlebar__brown"],
    "owen":       ["cowboy_hat__brown",     "cigar__brown",            "bandana_neck__red",        "scar__default"],
    "ryan":       ["headband__red",         "cyber_implant__cyan",     "brain_pendant_chain__gold", "third_eye__cyan"],
    "sacha":      ["baseball_cap__red",    "cyber_visor__red",        "gold_medallion__gold",     "kiss_print__hot_pink"],
    "shaune":     ["knight_helmet__steel",  "pipe_sherlock__default",  "diamond_chain__white",     "birthmark_star__default"],
}

# Sanity check: refuse to generate if any loadout contains a banned accessory.
for _slug, _items in MYTHIC_LOADOUTS.items():
    for _item in _items:
        _name = _item.split("__")[0]
        if _name in BANNED_ACCESSORIES:
            raise ValueError(
                f"BANNED accessory '{_name}' used in {_slug} mythic loadout. "
                f"Remove it before regenerating."
            )


# ===== SVG templates per tier =====

def svg_common(png_b64, trait_hex, rank, name_upper):
    backdrop = darken(trait_hex, 0.18)
    trait_lbl = trait_name(trait_hex)
    grid = make_grid_lines()
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024">
  <defs><style>image {{ image-rendering: pixelated; image-rendering: crisp-edges; }}</style></defs>
  <rect width="1024" height="1024" fill="#050709"/>
  <g opacity="0.4">
    {grid}
  </g>
  <rect x="0" y="0" width="1024" height="80" fill="#0A0E17"/>
  <line x1="0" y1="80" x2="1024" y2="80" stroke="{trait_hex}" stroke-width="2"/>
  <text x="40" y="50" font-family="'JetBrains Mono', monospace" font-size="18" font-weight="700" fill="#FFFFFF" letter-spacing="6">BRAINTRUST</text>
  <text x="984" y="50" font-family="'JetBrains Mono', monospace" font-size="18" font-weight="700" fill="{trait_hex}" text-anchor="end" letter-spacing="3">#{rank} / 045</text>
  <g>
    <rect x="852" y="100" width="140" height="32" rx="4" fill="rgba(139,149,168,0.15)" stroke="#8B95A8" stroke-width="1"/>
    <text x="922" y="121" font-family="'JetBrains Mono', monospace" font-size="13" font-weight="700" fill="#8B95A8" text-anchor="middle" letter-spacing="3">COMMON</text>
  </g>
  <rect x="112" y="148" width="800" height="600" fill="{backdrop}"/>
  <image href="data:image/png;base64,{png_b64}" x="212" y="148" width="600" height="600" preserveAspectRatio="xMidYMid meet"/>
  <rect x="112" y="148" width="800" height="600" fill="none" stroke="{trait_hex}" stroke-width="3"/>
  <g stroke="{trait_hex}" stroke-width="3" fill="none">
    <polyline points="112,168 112,148 132,148"/>
    <polyline points="892,148 912,148 912,168"/>
    <polyline points="912,728 912,748 892,748"/>
    <polyline points="132,748 112,748 112,728"/>
  </g>
  <text x="512" y="820" font-family="Inter, system-ui, sans-serif" font-size="56" font-weight="800" fill="#FFFFFF" text-anchor="middle" letter-spacing="-2">{name_upper}</text>
  <line x1="380" y1="868" x2="644" y2="868" stroke="{trait_hex}" stroke-width="1" opacity="0.4"/>
  <g font-family="'JetBrains Mono', monospace" font-size="13" letter-spacing="2">
    <text x="160" y="918" fill="#8B95A8">TRAIT</text>
    <text x="280" y="918" fill="{trait_hex}" font-weight="700">{trait_lbl}</text>
    <text x="540" y="918" fill="#8B95A8">TIER</text>
    <text x="680" y="918" fill="{trait_hex}" font-weight="700">COMMON</text>
    <text x="160" y="948" fill="#8B95A8">CHAIN</text>
    <text x="280" y="948" fill="{trait_hex}" font-weight="700">BT-1</text>
    <text x="540" y="948" fill="#8B95A8">MINT</text>
    <text x="680" y="948" fill="{trait_hex}" font-weight="700">MMXXVI</text>
  </g>
  <line x1="0" y1="980" x2="1024" y2="980" stroke="{trait_hex}" stroke-width="2"/>
  <text x="40" y="1010" font-family="'JetBrains Mono', monospace" font-size="11" fill="#FFFFFF" opacity="0.5" letter-spacing="2">braintrust.dev</text>
  <text x="984" y="1010" font-family="'JetBrains Mono', monospace" font-size="11" fill="{trait_hex}" text-anchor="end" letter-spacing="3">1 OF 1</text>
</svg>
'''


def svg_rare(png_b64, trait_hex, rank, name_upper):
    backdrop = darken(trait_hex, 0.20)
    trait_lbl = trait_name(trait_hex)
    grid = make_grid_lines()
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024">
  <defs>
    <style>image {{ image-rendering: pixelated; image-rendering: crisp-edges; }}</style>
    <linearGradient id="rareGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#9D7AFF"/>
      <stop offset="50%" stop-color="#E0E0E0"/>
      <stop offset="100%" stop-color="#9D7AFF"/>
    </linearGradient>
  </defs>
  <rect width="1024" height="1024" fill="#050709"/>
  <g opacity="0.4">
    {grid}
  </g>
  <rect x="0" y="0" width="1024" height="80" fill="#0A0E17"/>
  <line x1="0" y1="80" x2="1024" y2="80" stroke="url(#rareGrad)" stroke-width="3"/>
  <text x="40" y="50" font-family="'JetBrains Mono', monospace" font-size="18" font-weight="700" fill="#FFFFFF" letter-spacing="6">BRAINTRUST</text>
  <text x="984" y="50" font-family="'JetBrains Mono', monospace" font-size="18" font-weight="700" fill="url(#rareGrad)" text-anchor="end" letter-spacing="3">#{rank} / 045</text>
  <g>
    <rect x="852" y="100" width="140" height="32" rx="4" fill="rgba(157,122,255,0.18)" stroke="url(#rareGrad)" stroke-width="2"/>
    <text x="922" y="121" font-family="'JetBrains Mono', monospace" font-size="13" font-weight="700" fill="#9D7AFF" text-anchor="middle" letter-spacing="3">RARE</text>
  </g>
  <rect x="112" y="148" width="800" height="600" fill="{backdrop}"/>
  <image href="data:image/png;base64,{png_b64}" x="212" y="148" width="600" height="600" preserveAspectRatio="xMidYMid meet"/>
  <rect x="112" y="148" width="800" height="600" fill="none" stroke="url(#rareGrad)" stroke-width="5"/>
  <g stroke="url(#rareGrad)" stroke-width="5" fill="none">
    <polyline points="112,168 112,148 132,148"/>
    <polyline points="892,148 912,148 912,168"/>
    <polyline points="912,728 912,748 892,748"/>
    <polyline points="132,748 112,748 112,728"/>
  </g>
  <text x="512" y="820" font-family="Inter, system-ui, sans-serif" font-size="56" font-weight="800" fill="#FFFFFF" text-anchor="middle" letter-spacing="-2">{name_upper}</text>
  <line x1="380" y1="868" x2="644" y2="868" stroke="url(#rareGrad)" stroke-width="2" opacity="0.6"/>
  <g font-family="'JetBrains Mono', monospace" font-size="13" letter-spacing="2">
    <text x="160" y="918" fill="#8B95A8">TRAIT</text>
    <text x="280" y="918" fill="{trait_hex}" font-weight="700">{trait_lbl}</text>
    <text x="540" y="918" fill="#8B95A8">TIER</text>
    <text x="680" y="918" fill="#9D7AFF" font-weight="700">RARE</text>
    <text x="160" y="948" fill="#8B95A8">CHAIN</text>
    <text x="280" y="948" fill="{trait_hex}" font-weight="700">BT-1</text>
    <text x="540" y="948" fill="#8B95A8">MINT</text>
    <text x="680" y="948" fill="{trait_hex}" font-weight="700">MMXXVI</text>
  </g>
  <line x1="0" y1="980" x2="1024" y2="980" stroke="url(#rareGrad)" stroke-width="3"/>
  <text x="40" y="1010" font-family="'JetBrains Mono', monospace" font-size="11" fill="#FFFFFF" opacity="0.5" letter-spacing="2">braintrust.dev</text>
  <text x="984" y="1010" font-family="'JetBrains Mono', monospace" font-size="11" fill="#9D7AFF" text-anchor="end" letter-spacing="3">1 OF 1</text>
</svg>
'''


def svg_mythic(png_b64, trait_hex, rank, name_upper):
    backdrop = "#1F1500"
    trait_lbl = trait_name(trait_hex)
    grid = make_grid_lines()
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024">
  <defs>
    <style>image {{ image-rendering: pixelated; image-rendering: crisp-edges; }}</style>
    <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFD93D"/>
      <stop offset="50%" stop-color="#FFF4B0"/>
      <stop offset="100%" stop-color="#FFAA00"/>
    </linearGradient>
    <radialGradient id="goldGlow" cx="50%" cy="50%" r="60%">
      <stop offset="0%" stop-color="rgba(255,217,61,0.28)"/>
      <stop offset="100%" stop-color="rgba(255,217,61,0)"/>
    </radialGradient>
  </defs>
  <rect width="1024" height="1024" fill="#050709"/>
  <rect width="1024" height="1024" fill="url(#goldGlow)"/>
  <g opacity="0.4">
    {grid}
  </g>
  <rect x="0" y="0" width="1024" height="80" fill="#0A0E17"/>
  <line x1="0" y1="80" x2="1024" y2="80" stroke="url(#goldGrad)" stroke-width="4"/>
  <text x="40" y="50" font-family="'JetBrains Mono', monospace" font-size="18" font-weight="700" fill="#FFFFFF" letter-spacing="6">BRAINTRUST</text>
  <text x="984" y="50" font-family="'JetBrains Mono', monospace" font-size="18" font-weight="700" fill="url(#goldGrad)" text-anchor="end" letter-spacing="3">#{rank} / 045</text>
  <g>
    <rect x="822" y="98" width="170" height="36" rx="6" fill="rgba(255,217,61,0.22)" stroke="url(#goldGrad)" stroke-width="3"/>
    <text x="907" y="121" font-family="'JetBrains Mono', monospace" font-size="14" font-weight="700" fill="#FFD93D" text-anchor="middle" letter-spacing="4">MYTHIC</text>
  </g>
  <g fill="#FFF4B0">
    <circle cx="160" cy="200" r="3"/>
    <circle cx="864" cy="220" r="2"/>
    <circle cx="200" cy="700" r="2"/>
    <circle cx="860" cy="700" r="3"/>
    <circle cx="120" cy="400" r="2"/>
    <circle cx="900" cy="500" r="2"/>
    <circle cx="100" cy="600" r="2"/>
    <circle cx="940" cy="350" r="3"/>
  </g>
  <rect x="112" y="148" width="800" height="600" fill="{backdrop}"/>
  <image href="data:image/png;base64,{png_b64}" x="212" y="148" width="600" height="600" preserveAspectRatio="xMidYMid meet"/>
  <rect x="112" y="148" width="800" height="600" fill="none" stroke="url(#goldGrad)" stroke-width="7"/>
  <g stroke="url(#goldGrad)" stroke-width="7" fill="none">
    <polyline points="112,168 112,148 132,148"/>
    <polyline points="892,148 912,148 912,168"/>
    <polyline points="912,728 912,748 892,748"/>
    <polyline points="132,748 112,748 112,728"/>
  </g>
  <text x="512" y="820" font-family="Inter, system-ui, sans-serif" font-size="56" font-weight="800" fill="#FFFFFF" text-anchor="middle" letter-spacing="-2">{name_upper}</text>
  <line x1="380" y1="868" x2="644" y2="868" stroke="url(#goldGrad)" stroke-width="3"/>
  <g font-family="'JetBrains Mono', monospace" font-size="13" letter-spacing="2">
    <text x="160" y="918" fill="#8B95A8">TRAIT</text>
    <text x="280" y="918" fill="{trait_hex}" font-weight="700">{trait_lbl}</text>
    <text x="540" y="918" fill="#8B95A8">TIER</text>
    <text x="680" y="918" fill="#FFD93D" font-weight="700">MYTHIC</text>
    <text x="160" y="948" fill="#8B95A8">CHAIN</text>
    <text x="280" y="948" fill="{trait_hex}" font-weight="700">BT-1</text>
    <text x="540" y="948" fill="#8B95A8">MINT</text>
    <text x="680" y="948" fill="{trait_hex}" font-weight="700">MMXXVI</text>
  </g>
  <line x1="0" y1="980" x2="1024" y2="980" stroke="url(#goldGrad)" stroke-width="4"/>
  <text x="40" y="1010" font-family="'JetBrains Mono', monospace" font-size="11" fill="#FFFFFF" opacity="0.5" letter-spacing="2">braintrust.dev</text>
  <text x="984" y="1010" font-family="'JetBrains Mono', monospace" font-size="11" fill="#FFD93D" text-anchor="end" letter-spacing="3">1 OF 1</text>
</svg>
'''


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    # Refuse to clobber any file outside our variants/ dir.
    print(f"Originals at public/nfts/corporate/ will NOT be touched.")
    print(f"Output target: {OUT_DIR}")
    print()

    people = json.load(open(PEOPLE_PATH))
    written = []

    for sdr_index, traits in enumerate(people):
        slug = traits["slug"]
        rare_loadout = ASSIGNMENTS[slug]["items"] if slug in ASSIGNMENTS else []
        # Mythic uses a hand-curated unique loadout per SDR (NOT a uniform
        # addon on top of Rare).
        mythic_loadout = MYTHIC_LOADOUTS.get(slug, list(rare_loadout))

        common_png = render_png(traits, [])
        rare_png = render_png(traits, rare_loadout)
        mythic_png = render_png(traits, mythic_loadout)

        trait_hex = traits.get("trait", "#7B61FF")
        name_upper = traits["name"].upper()

        renderers = [
            ("common", common_png, svg_common),
            ("rare", rare_png, svg_rare),
            ("mythic", mythic_png, svg_mythic),
        ]
        for variant_idx, (variant, png_bytes, svg_fn) in enumerate(renderers):
            token_id = sdr_index * 3 + variant_idx
            png_b64 = base64.b64encode(png_bytes).decode()
            svg = svg_fn(png_b64, trait_hex, str(token_id).zfill(3), name_upper)
            out_file = OUT_DIR / f"{slug}_{variant}.svg"
            out_file.write_text(svg)
            written.append({"token_id": token_id, "slug": slug, "variant": variant, "path": str(out_file)})

        print(
            f"  SDR {sdr_index:2}  {traits['name']:22}  tokens {sdr_index*3:>2},{sdr_index*3+1:>2},{sdr_index*3+2:>2}  -> common/rare/mythic"
        )

    # Write a manifest
    manifest_path = OUT_DIR / "_manifest.json"
    manifest_path.write_text(json.dumps({"variants": written}, indent=2))

    # Also write a per-slug per-tier loadout file so the metadata generator
    # (TS) can attach the CORRECT accessory list per variant.
    loadouts: dict = {}
    for traits in people:
        slug = traits["slug"]
        rare_loadout = ASSIGNMENTS[slug]["items"] if slug in ASSIGNMENTS else []
        mythic_loadout = MYTHIC_LOADOUTS.get(slug, list(rare_loadout))
        loadouts[slug] = {
            "common": [],
            "rare": rare_loadout,
            "mythic": mythic_loadout,
        }
    loadouts_path = OUT_DIR / "_loadouts.json"
    loadouts_path.write_text(json.dumps(loadouts, indent=2))

    print(f"\nwrote {len(written)} variant SVGs to {OUT_DIR}")
    print(f"manifest:  {manifest_path}")
    print(f"loadouts:  {loadouts_path}")
    print(f"originals at public/nfts/corporate/ are unchanged.")


if __name__ == "__main__":
    main()
