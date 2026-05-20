#!/usr/bin/env python3
"""Signature item library at 48x48.

Each function takes a canvas and optional palette/size, draws the item, returns
the canvas. Designed to be composable: the variant generator (variants.py)
calls these with different palettes and size knobs.

All items render with the "anchor" roughly centered at (24, 24) so they look
right in the contact sheet. When promoted to production they get repositioned
onto the character canvas.
"""
import math
from items_v3 import (
    new_canvas, put, paint, fill_rect, mix,
    draw_sphere, draw_glow_ring, draw_sparkles, draw_antenna,
    SPHERE_PALETTES, WHITE, BLACK, GOLD, GOLD_DARK, GOLD_LIGHT,
    SILVER, SILVER_DARK, SILVER_LIGHT,
)


# ===========================================================================
# SPHERICAL ITEMS
# ===========================================================================

def ai_orb_v2(canvas, palette_name="cyber", size="M"):
    """Glowing AI agent orb with antenna and orbiting sparkles. v2 of the
    original sig_ai_agent, but at 48x48 with proper shading."""
    pal = SPHERE_PALETTES[palette_name]
    shadow, mid, hi = pal
    radius = {"S": 7, "M": 10, "L": 13}[size]
    cx, cy = 24, 26

    # Outer glow ring
    draw_glow_ring(canvas, cx, cy, radius + 3, mid, alpha=60)
    draw_glow_ring(canvas, cx, cy, radius + 2, mid, alpha=110)
    # Sphere
    draw_sphere(canvas, cx, cy, radius, pal)
    # Antenna with bright tip
    draw_antenna(canvas, cx, cy - radius - 1, 6, mid, tip_color=hi)
    # Bright signal dot above antenna
    put(canvas, cx, cy - radius - 8, WHITE)
    # Orbiting sparkles
    spark_color = mix(hi, WHITE, 0.5)
    sparks = [
        (cx - radius - 3, cy - radius + 2),
        (cx + radius + 3, cy - radius + 4),
        (cx - radius - 2, cy + radius - 2),
        (cx + radius + 3, cy + radius - 1),
    ]
    draw_sparkles(canvas, sparks, spark_color)
    return canvas


def crystal_ball(canvas, palette_name="amethyst", size="M"):
    """Crystal ball on a small wooden stand. Translucent feel via interior
    swirl."""
    pal = SPHERE_PALETTES[palette_name]
    shadow, mid, hi = pal
    radius = {"S": 8, "M": 11, "L": 14}[size]
    cx, cy = 24, 22

    # Sphere
    draw_sphere(canvas, cx, cy, radius, pal)
    # Interior swirl: 3 short diagonal streaks of highlight
    streak = mix(hi, WHITE, 0.4)
    for i, off in enumerate([(-2, -1), (1, 0), (-1, 3)]):
        ox, oy = off
        for k in range(3):
            put(canvas, cx + ox + k, cy + oy - k, streak, alpha=200)
    # Wooden stand below
    stand_top = cy + radius
    fill_rect(canvas, cx - radius + 1, stand_top, cx + radius - 1, stand_top + 1, (95, 60, 30))
    fill_rect(canvas, cx - radius + 2, stand_top + 2, cx + radius - 2, stand_top + 3, (70, 45, 22))
    # Stand feet
    put(canvas, cx - radius + 2, stand_top + 4, (50, 32, 16))
    put(canvas, cx + radius - 2, stand_top + 4, (50, 32, 16))
    return canvas


def plasma_sphere(canvas, palette_name="plasma", size="M"):
    """Glass plasma globe with electric arcs inside."""
    pal = SPHERE_PALETTES[palette_name]
    shadow, mid, hi = pal
    radius = {"S": 8, "M": 11, "L": 14}[size]
    cx, cy = 24, 24

    # Darker, more transparent base sphere
    dark_pal = (mix(shadow, BLACK, 0.3), mix(shadow, mid, 0.4), mid)
    draw_sphere(canvas, cx, cy, radius, dark_pal)
    # Core bright dot
    fill_rect(canvas, cx - 1, cy - 1, cx + 1, cy + 1, hi)
    put(canvas, cx, cy, WHITE)
    # Electric arcs (zigzags from center out)
    arc = mix(hi, WHITE, 0.6)
    arcs = [
        [(cx, cy), (cx + 2, cy - 2), (cx + 3, cy - 4), (cx + 5, cy - 5), (cx + 7, cy - 6)],
        [(cx, cy), (cx - 2, cy + 1), (cx - 4, cy + 3), (cx - 5, cy + 5), (cx - 7, cy + 6)],
        [(cx, cy), (cx + 1, cy + 3), (cx + 2, cy + 5), (cx + 3, cy + 7)],
        [(cx, cy), (cx - 1, cy - 3), (cx - 3, cy - 4), (cx - 4, cy - 6)],
    ]
    for path in arcs:
        for (x, y) in path:
            put(canvas, x, y, arc)
    # Base ring (the glass mount)
    fill_rect(canvas, cx - radius, cy + radius + 1, cx + radius, cy + radius + 2, (60, 60, 70))
    return canvas


def brain_orb(canvas, palette_name="ruby", size="M"):
    """Braintrust logo as a 3D brain-textured orb."""
    pal = SPHERE_PALETTES[palette_name]
    shadow, mid, hi = pal
    radius = {"S": 8, "M": 11, "L": 14}[size]
    cx, cy = 24, 24

    # Sphere base
    draw_sphere(canvas, cx, cy, radius, pal)
    # Brain "folds": short curved highlight lines following the surface
    fold = mix(hi, WHITE, 0.3)
    for off in [(-radius + 3, -2), (-radius + 4, 2), (-2, -radius + 3), (2, -radius + 4),
                (radius - 4, -1), (radius - 5, 3), (-1, radius - 4), (3, radius - 5)]:
        x, y = cx + off[0], cy + off[1]
        put(canvas, x, y, fold)
        put(canvas, x + 1, y, fold)
    # Central groove (the brain's split)
    groove = mix(shadow, mid, 0.5)
    for dy in range(-radius + 2, radius - 1):
        # zigzag the groove slightly
        wobble = int(math.sin(dy * 0.6) * 1.2)
        put(canvas, cx + wobble, cy + dy, groove, alpha=200)
    return canvas


def halo_orb(canvas, palette_name="gold", size="M"):
    """Floating orb with a golden halo above it."""
    pal = SPHERE_PALETTES[palette_name]
    shadow, mid, hi = pal
    radius = {"S": 7, "M": 9, "L": 12}[size]
    cx, cy = 24, 30

    # Sphere
    draw_sphere(canvas, cx, cy, radius, pal)
    # Halo: golden ellipse above the head
    halo_y = cy - radius - 5
    halo_outer = (255, 220, 80)
    halo_inner = (255, 245, 180)
    # Outer ring
    for ang_deg in range(0, 360, 4):
        ang = math.radians(ang_deg)
        x = int(cx + math.cos(ang) * 9)
        y = int(halo_y + math.sin(ang) * 3)
        put(canvas, x, y, halo_outer)
    # Inner ring (highlight)
    for ang_deg in range(0, 360, 8):
        ang = math.radians(ang_deg)
        x = int(cx + math.cos(ang) * 8)
        y = int(halo_y + math.sin(ang) * 2.5)
        put(canvas, x, y, halo_inner)
    # Connecting glow shaft (subtle, faded)
    for dy in range(halo_y + 3, cy - radius):
        put(canvas, cx, dy, halo_outer, alpha=120)
    return canvas


def disco_ball(canvas, palette_name="holo", size="M"):
    """Mirrored disco ball with light rays."""
    radius = {"S": 8, "M": 11, "L": 14}[size]
    cx, cy = 24, 24

    # Base silver sphere with cool palette
    base_pal = ((90, 100, 130), (170, 180, 210), (240, 245, 255))
    draw_sphere(canvas, cx, cy, radius, base_pal, specular=False)
    # Facet grid (small bright + dark squares)
    facet_hi = (255, 255, 255)
    facet_low = (60, 70, 90)
    for ry in range(-radius + 2, radius - 1, 2):
        for rx in range(-radius + 2, radius - 1, 2):
            if rx * rx + ry * ry > (radius - 2) ** 2:
                continue
            # Alternating cells
            cell = facet_hi if (rx + ry) % 4 == 0 else facet_low
            put(canvas, cx + rx, cy + ry, cell, alpha=180)
    # Bright sparkles around it
    spark_color = WHITE
    sparks = [
        (cx - radius - 4, cy - radius - 1),
        (cx + radius + 4, cy - radius),
        (cx - radius - 3, cy + radius + 2),
        (cx + radius + 3, cy + radius + 1),
        (cx, cy - radius - 5),
    ]
    draw_sparkles(canvas, sparks, spark_color)
    # Hanging string
    for dy in range(0, 4):
        put(canvas, cx, cy - radius - 1 - dy, (180, 180, 180))
    return canvas


# ===========================================================================
# CREATIVE NEW (non-spherical)
# ===========================================================================

def lightning_bolt(canvas, palette_name="gold", size="M"):
    """Stylized lightning bolt with electric glow."""
    pal = SPHERE_PALETTES[palette_name]
    shadow, mid, hi = pal
    cx, cy = 24, 24
    scale = {"S": 1.0, "M": 1.3, "L": 1.6}[size]

    # Bolt path: zigzag down-right then down-left
    # Defined as polygon of (col, row) at scale=1.0 centered at (cx, cy)
    bolt_outline = [
        (-3, -10), (3, -10), (1, -3), (5, -3), (-3, 10), (-1, 2), (-5, 2), (-3, -10)
    ]
    pts = [(cx + int(x * scale), cy + int(y * scale)) for (x, y) in bolt_outline]

    # Flood fill the polygon: simple scan
    minx = min(p[0] for p in pts)
    maxx = max(p[0] for p in pts)
    miny = min(p[1] for p in pts)
    maxy = max(p[1] for p in pts)
    for y in range(miny, maxy + 1):
        # Find x ranges where inside polygon via ray crossing
        intersections = []
        for i in range(len(pts) - 1):
            x1, y1 = pts[i]
            x2, y2 = pts[i + 1]
            if (y1 <= y < y2) or (y2 <= y < y1):
                t = (y - y1) / (y2 - y1) if y2 != y1 else 0
                xi = x1 + t * (x2 - x1)
                intersections.append(xi)
        intersections.sort()
        for j in range(0, len(intersections) - 1, 2):
            x0 = int(intersections[j])
            x1 = int(intersections[j + 1])
            for x in range(x0, x1 + 1):
                put(canvas, x, y, mid)

    # Edge highlight on left side of bolt
    for (x, y) in pts:
        put(canvas, x, y, hi)
    # Inner core highlight
    for y in range(miny + 3, maxy - 2):
        put(canvas, cx, y, mix(hi, WHITE, 0.4))
    # Outer glow sparkles
    sparks = [(cx - 8, cy - 6), (cx + 8, cy + 6), (cx - 7, cy + 4), (cx + 6, cy - 8)]
    draw_sparkles(canvas, sparks, mix(hi, WHITE, 0.6))
    return canvas


def neon_dollar(canvas, palette_name="emerald", size="M"):
    """Glowing neon $ sign."""
    pal = SPHERE_PALETTES[palette_name]
    shadow, mid, hi = pal
    cx, cy = 24, 24
    sz = {"S": 0.85, "M": 1.0, "L": 1.2}[size]

    # $ as pixel pattern (10 wide, 16 tall at scale 1.0)
    pattern = [
        "....##....",
        "..######..",
        ".##....##.",
        ".##.......",
        ".##.......",
        "..######..",
        "....####..",
        ".......##.",
        ".......##.",
        ".##....##.",
        "..######..",
        "....##....",
    ]
    glyph_w = len(pattern[0])
    glyph_h = len(pattern)
    sx = cx - int(glyph_w * sz / 2)
    sy = cy - int(glyph_h * sz / 2)
    # Render glyph
    for ry, row in enumerate(pattern):
        for rx, ch in enumerate(row):
            if ch == "#":
                x = sx + int(rx * sz)
                y = sy + int(ry * sz)
                put(canvas, x, y, mid)
                # Highlight the leftmost pixel of each filled run
                if rx > 0 and row[rx - 1] == ".":
                    put(canvas, x, y, hi)
    # Outer neon glow (soft halo)
    for ry, row in enumerate(pattern):
        for rx, ch in enumerate(row):
            if ch == "#":
                x = sx + int(rx * sz)
                y = sy + int(ry * sz)
                for (dx, dy) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    px, py = x + dx, y + dy
                    if 0 <= px < 48 and 0 <= py < 48:
                        existing = canvas.getpixel((px, py))
                        if existing[3] == 0:
                            put(canvas, px, py, mid, alpha=110)
    return canvas


# === Item registry ===

ITEMS = {
    "ai_orb_v2":     ai_orb_v2,
    "crystal_ball":  crystal_ball,
    "plasma_sphere": plasma_sphere,
    "brain_orb":     brain_orb,
    "halo_orb":      halo_orb,
    "disco_ball":    disco_ball,
    "lightning":     lightning_bolt,
    "neon_dollar":   neon_dollar,
}


if __name__ == "__main__":
    # Render one of each at default palette
    import pathlib
    out = pathlib.Path("public/variants/_smoke")
    out.mkdir(parents=True, exist_ok=True)
    for name, fn in ITEMS.items():
        c = new_canvas()
        fn(c)
        c.save(out / f"{name}.png")
    print(f"wrote {len(ITEMS)} item smoke tests to {out}")
