#!/usr/bin/env python3
"""Build NFT trading card SVGs around pixel art characters.
Usage: python3 generate_nfts.py [corporate|aquatic|galaxy]
"""
import base64
import pathlib
import sys

def _hex_to_bg(trait_hex):
    """Derive a dark muted backdrop from the trait color."""
    h = trait_hex.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"#{int(r*0.18):02X}{int(g*0.18):02X}{int(b*0.18):02X}"

def _trait_name(trait_hex):
    """Friendly name for trait color (closest of a curated set)."""
    NAMES = [
        ("#00FF94","EMERALD"), ("#FF6B9D","ROSE"), ("#FFD93D","GOLD"), ("#00D9FF","CYAN"),
        ("#9D7AFF","AMETHYST"), ("#FF8C42","AMBER"), ("#7B61FF","VIOLET"), ("#FF3366","CRIMSON"),
        ("#00E5FF","ELECTRIC"), ("#FFC857","SOLAR"), ("#A8E6CF","MINT"), ("#4ECDC4","TEAL"),
        ("#E0E0E0","PLATINUM"), ("#FF66C4","MAGENTA"), ("#B8FF3D","LIME"), ("#7BFFD4","AQUA"),
        ("#FFAA00","SUN"), ("#FF4488","BLUSH"), ("#88CCFF","SKY"), ("#FFD0AA","SAND"),
        ("#AAFF88","SAGE"), ("#FF88AA","PEACH"), ("#88FFAA","JADE"), ("#FFCCFF","PETAL"),
    ]
    for k, v in NAMES:
        if k.upper() == trait_hex.upper():
            return v
    return "CHROMA"

def _load_people():
    raw = json.loads(pathlib.Path("data/auto_people.json").read_text())
    out = []
    for p in raw:
        p["trait_name"] = _trait_name(p["trait"])
        p["bg"] = _hex_to_bg(p["trait"])
        out.append(p)
    return out

import json
PEOPLE = _load_people()
TOTAL = len(PEOPLE)

THEME_META = {
    "corporate": {"label": "GENESIS",   "name": "BT-1"},
    "aquatic":   {"label": "TIDAL",     "name": "BT-2"},
    "galaxy":    {"label": "GALAXY",    "name": "BT-3"},
    "cyberpunk": {"label": "CYBERPUNK", "name": "BT-4"},
}


def encode_pixel(slug, theme):
    path = pathlib.Path(f"public/pixels/{theme}/{slug}.png")
    with open(path, "rb") as f:
        return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"


def build_animations(theme, trait_hex):
    """Return SVG animation overlay (positioned within 112-912 x 120-720 avatar panel)."""
    if theme == "aquatic":
        # Rising bubbles animated from bottom to top
        bubbles = ""
        for i, (cx, dur, delay, r) in enumerate([
            (180, 5, 0, 8), (340, 6, 1.2, 6), (500, 5.5, 0.6, 10),
            (660, 7, 2.5, 7), (820, 4.8, 1.8, 9), (260, 6.5, 3.2, 5),
            (580, 5.2, 4.0, 8), (740, 6.8, 0.3, 6),
        ]):
            bubbles += f'''
  <circle cx="{cx}" cy="720" r="{r}" fill="rgba(200,230,245,0.6)" stroke="rgba(255,255,255,0.4)" stroke-width="1">
    <animate attributeName="cy" from="720" to="120" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0;0.7;0.7;0" keyTimes="0;0.1;0.85;1" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>
  </circle>'''
        return bubbles
    elif theme == "galaxy":
        # Pulsing halo around brain + animated lightning crackles
        return f'''
  <circle cx="512" cy="280" r="170" fill="none" stroke="{trait_hex}" stroke-width="2" opacity="0.4">
    <animate attributeName="r" values="170;200;170" dur="2.4s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.4;0.15;0.4" dur="2.4s" repeatCount="indefinite"/>
  </circle>
  <circle cx="512" cy="280" r="140" fill="none" stroke="{trait_hex}" stroke-width="1.5" opacity="0.3">
    <animate attributeName="r" values="140;170;140" dur="2.4s" begin="0.4s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.3;0.05;0.3" dur="2.4s" begin="0.4s" repeatCount="indefinite"/>
  </circle>
  <g opacity="0.8">
    <line x1="160" y1="200" x2="200" y2="180" stroke="{trait_hex}" stroke-width="2">
      <animate attributeName="opacity" values="0;1;0" dur="0.4s" begin="1s" repeatCount="indefinite"/>
    </line>
    <line x1="820" y1="220" x2="860" y2="200" stroke="{trait_hex}" stroke-width="2">
      <animate attributeName="opacity" values="0;1;0" dur="0.4s" begin="2.2s" repeatCount="indefinite"/>
    </line>
  </g>'''
    elif theme == "cyberpunk":
        # Scrolling code rain on the sides
        cols = ""
        for i, (cx, dur, delay) in enumerate([(150, 3, 0), (200, 4, 1), (820, 3.5, 0.5), (870, 4.2, 1.8)]):
            cols += f'''
  <g font-family="JetBrains Mono, monospace" font-size="14" fill="#FF66C4" opacity="0.6">
    <text x="{cx}" y="180">01010</text>
    <text x="{cx}" y="220">11001</text>
    <text x="{cx}" y="260">10110</text>
    <text x="{cx}" y="300">00101</text>
    <animateTransform attributeName="transform" type="translate" from="0,-200" to="0,600" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>
  </g>'''
        return cols
    return ""


def build_svg(p, theme):
    pixel_data = encode_pixel(p["slug"], theme)
    token = f"{p['id']:03d} / {TOTAL:03d}"
    chain_label = THEME_META[theme]["name"]
    edition = THEME_META[theme]["label"]
    animations = build_animations(theme, p["trait"])
    # Override panel bg for cyberpunk to dark
    panel_bg = "#0A0814" if theme == "cyberpunk" else p["bg"]

    grid_rows = []
    for x in range(0, 1024, 64):
        grid_rows.append(f'<line x1="{x}" y1="0" x2="{x}" y2="1024" stroke="#0F1320" stroke-width="1"/>')
    for y in range(0, 1024, 64):
        grid_rows.append(f'<line x1="0" y1="{y}" x2="1024" y2="{y}" stroke="#0F1320" stroke-width="1"/>')
    grid = "\n    ".join(grid_rows)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024">
  <defs>
    <style>image {{ image-rendering: pixelated; image-rendering: crisp-edges; }}</style>
  </defs>

  <rect width="1024" height="1024" fill="#050709"/>
  <g opacity="0.4">{grid}</g>

  <!-- Top bar -->
  <rect x="0" y="0" width="1024" height="80" fill="#0A0E17"/>
  <line x1="0" y1="80" x2="1024" y2="80" stroke="{p['trait']}" stroke-width="2"/>
  <text x="40" y="50" font-family="'JetBrains Mono', monospace" font-size="18" font-weight="700" fill="#FFFFFF" letter-spacing="6">BRAINTRUST</text>
  <text x="984" y="50" font-family="'JetBrains Mono', monospace" font-size="18" font-weight="700" fill="{p['trait']}" text-anchor="end" letter-spacing="3">#{token}</text>

  <!-- Avatar panel -->
  <rect x="112" y="120" width="800" height="600" fill="{panel_bg}"/>
  <clipPath id="panel-clip-{p['id']}"><rect x="112" y="120" width="800" height="600"/></clipPath>
  <image href="{pixel_data}" x="212" y="120" width="600" height="600" preserveAspectRatio="xMidYMid meet"/>
  <g clip-path="url(#panel-clip-{p['id']})">{animations}</g>
  <rect x="112" y="120" width="800" height="600" fill="none" stroke="{p['trait']}" stroke-width="3"/>

  <g stroke="{p['trait']}" stroke-width="3" fill="none">
    <polyline points="112,140 112,120 132,120"/>
    <polyline points="892,120 912,120 912,140"/>
    <polyline points="912,700 912,720 892,720"/>
    <polyline points="132,720 112,720 112,700"/>
  </g>

  <!-- Name -->
  <text x="512" y="790" font-family="Inter, system-ui, sans-serif" font-size="56" font-weight="800" fill="#FFFFFF" text-anchor="middle" letter-spacing="-2">{p['name'].upper()}</text>
  <text x="512" y="828" font-family="'JetBrains Mono', monospace" font-size="14" fill="{p['trait']}" text-anchor="middle" letter-spacing="6">{p['role']}</text>

  <line x1="380" y1="858" x2="644" y2="858" stroke="{p['trait']}" stroke-width="1" opacity="0.4"/>

  <g font-family="'JetBrains Mono', monospace" font-size="13" letter-spacing="2">
    <text x="160" y="908" fill="#8B95A8">TRAIT</text>
    <text x="280" y="908" fill="{p['trait']}" font-weight="700">{p['trait_name']}</text>
    <text x="540" y="908" fill="#8B95A8">EDITION</text>
    <text x="680" y="908" fill="{p['trait']}" font-weight="700">{edition}</text>
    <text x="160" y="948" fill="#8B95A8">CHAIN</text>
    <text x="280" y="948" fill="{p['trait']}" font-weight="700">{chain_label}</text>
    <text x="540" y="948" fill="#8B95A8">MINT</text>
    <text x="680" y="948" fill="{p['trait']}" font-weight="700">MMXXVI</text>
  </g>

  <line x1="0" y1="980" x2="1024" y2="980" stroke="{p['trait']}" stroke-width="2"/>
  <text x="40" y="1010" font-family="'JetBrains Mono', monospace" font-size="11" fill="#FFFFFF" opacity="0.5" letter-spacing="2">braintrust.dev</text>
  <text x="984" y="1010" font-family="'JetBrains Mono', monospace" font-size="11" fill="{p['trait']}" text-anchor="end" letter-spacing="3">1 OF 1</text>
</svg>
'''


def main():
    theme = sys.argv[1] if len(sys.argv) > 1 else "corporate"
    out_dir = pathlib.Path(f"public/nfts/{theme}")
    out_dir.mkdir(parents=True, exist_ok=True)

    for p in PEOPLE:
        svg = build_svg(p, theme)
        (out_dir / f"{p['slug']}_nft.svg").write_text(svg)
        print(f"OK {out_dir}/{p['slug']}_nft.svg")
    print(f"\nGenerated {len(PEOPLE)} NFTs for theme: {theme}")


if __name__ == "__main__":
    main()
