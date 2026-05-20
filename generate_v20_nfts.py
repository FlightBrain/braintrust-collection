#!/usr/bin/env python3
"""Wrap each v20 SDR portrait in an NFT-card SVG.

Mirrors the existing nfts/corporate/*.svg layout but:
  - Drops the role/title text (per KB).
  - Embeds the new public/sdrs/{slug}.png portrait (with assigned accessories).
  - Uses the SDR's trait color as the accent.

Output: public/nfts/corporate/{slug}_nft.svg (overwrites for the 15 SDRs).
"""
import base64
import json
import pathlib


SVG_TEMPLATE = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024">
  <defs>
    <style>image {{ image-rendering: pixelated; image-rendering: crisp-edges; }}</style>
  </defs>

  <rect width="1024" height="1024" fill="#050709"/>
  <g opacity="0.4">
    {grid_lines}
  </g>

  <!-- Top bar -->
  <rect x="0" y="0" width="1024" height="80" fill="#0A0E17"/>
  <line x1="0" y1="80" x2="1024" y2="80" stroke="{trait_color}" stroke-width="2"/>
  <text x="40" y="50" font-family="'JetBrains Mono', monospace" font-size="18" font-weight="700" fill="#FFFFFF" letter-spacing="6">BRAINTRUST</text>
  <text x="984" y="50" font-family="'JetBrains Mono', monospace" font-size="18" font-weight="700" fill="{trait_color}" text-anchor="end" letter-spacing="3">#{rank} / 015</text>

  <!-- Avatar panel -->
  <rect x="112" y="120" width="800" height="600" fill="{backdrop_color}"/>
  <image href="data:image/png;base64,{png_b64}" x="212" y="120" width="600" height="600" preserveAspectRatio="xMidYMid meet"/>
  <rect x="112" y="120" width="800" height="600" fill="none" stroke="{trait_color}" stroke-width="3"/>

  <g stroke="{trait_color}" stroke-width="3" fill="none">
    <polyline points="112,140 112,120 132,120"/>
    <polyline points="892,120 912,120 912,140"/>
    <polyline points="912,700 912,720 892,720"/>
    <polyline points="132,720 112,720 112,700"/>
  </g>

  <!-- Name (role removed per KB) -->
  <text x="512" y="800" font-family="Inter, system-ui, sans-serif" font-size="56" font-weight="800" fill="#FFFFFF" text-anchor="middle" letter-spacing="-2">{name_upper}</text>

  <line x1="380" y1="850" x2="644" y2="850" stroke="{trait_color}" stroke-width="1" opacity="0.4"/>

  <g font-family="'JetBrains Mono', monospace" font-size="13" letter-spacing="2">
    <text x="160" y="900" fill="#8B95A8">TRAIT</text>
    <text x="280" y="900" fill="{trait_color}" font-weight="700">{trait_name}</text>
    <text x="540" y="900" fill="#8B95A8">EDITION</text>
    <text x="680" y="900" fill="{trait_color}" font-weight="700">GENESIS</text>
    <text x="160" y="940" fill="#8B95A8">CHAIN</text>
    <text x="280" y="940" fill="{trait_color}" font-weight="700">BT-1</text>
    <text x="540" y="940" fill="#8B95A8">MINT</text>
    <text x="680" y="940" fill="{trait_color}" font-weight="700">MMXXVI</text>
  </g>

  <line x1="0" y1="980" x2="1024" y2="980" stroke="{trait_color}" stroke-width="2"/>
  <text x="40" y="1010" font-family="'JetBrains Mono', monospace" font-size="11" fill="#FFFFFF" opacity="0.5" letter-spacing="2">braintrust.dev</text>
  <text x="984" y="1010" font-family="'JetBrains Mono', monospace" font-size="11" fill="{trait_color}" text-anchor="end" letter-spacing="3">1 OF 1</text>
</svg>
'''


def make_grid_lines():
    lines = []
    for x in range(0, 1024, 64):
        lines.append(f'<line x1="{x}" y1="0" x2="{x}" y2="1024" stroke="#0F1320" stroke-width="1"/>')
    for y in range(0, 1024, 64):
        lines.append(f'<line x1="0" y1="{y}" x2="1024" y2="{y}" stroke="#0F1320" stroke-width="1"/>')
    return "\n    ".join(lines)


def trait_name_for(trait_hex):
    NAMES = {
        "#00FF94": "EMERALD", "#FF6B9D": "ROSE", "#FFD93D": "GOLD", "#00D9FF": "CYAN",
        "#9D7AFF": "AMETHYST", "#FF8C42": "AMBER", "#7B61FF": "VIOLET", "#FF3366": "CRIMSON",
        "#00E5FF": "ELECTRIC", "#FFC857": "SOLAR", "#A8E6CF": "MINT", "#4ECDC4": "TEAL",
        "#E0E0E0": "PLATINUM", "#FF66C4": "MAGENTA", "#B8FF3D": "LIME", "#7BFFD4": "AQUA",
        "#FFAA00": "SUN", "#FF4488": "BLUSH", "#88CCFF": "SKY", "#FFD0AA": "SAND",
    }
    return NAMES.get(trait_hex.upper(), "CHROMA")


def darken(hex_color, factor=0.18):
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"#{int(r*factor):02X}{int(g*factor):02X}{int(b*factor):02X}"


def main():
    people = json.load(open("public/auto_people.json"))
    grid = make_grid_lines()

    out_dir = pathlib.Path("public/nfts/corporate")
    out_dir.mkdir(parents=True, exist_ok=True)

    for i, p in enumerate(people, start=1):
        slug = p["slug"]
        png_path = pathlib.Path(f"public/sdrs/{slug}.png")
        if not png_path.exists():
            print(f"  ! missing {png_path}")
            continue
        png_b64 = base64.b64encode(png_path.read_bytes()).decode()

        trait_hex = p.get("trait", "#7B61FF")
        backdrop = darken(trait_hex, 0.18)
        trait_name = trait_name_for(trait_hex)

        svg = SVG_TEMPLATE.format(
            grid_lines=grid,
            trait_color=trait_hex,
            backdrop_color=backdrop,
            png_b64=png_b64,
            rank=str(i).zfill(3),
            name_upper=p["name"].upper(),
            trait_name=trait_name,
        )
        out_file = out_dir / f"{slug}_nft.svg"
        out_file.write_text(svg)
        print(f"  {p['name']:22} -> {out_file}")

    print(f"\nwrote {len(people)} v20 NFT SVGs to {out_dir}")


if __name__ == "__main__":
    main()
