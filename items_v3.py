#!/usr/bin/env python3
"""48x48 signature item sprites, v3.

Bigger canvas, 3-tone shading, proper specular highlights.
Every item renders standalone on a transparent 48x48 background, so we can
iterate on items independently of the character.

Pixel coords: (col, row), origin top-left. Canvas size 48x48.
"""
from PIL import Image
import pathlib
import math

SIZE = 48

# === Palettes ===
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
GOLD_DARK = (180, 140, 0)
GOLD_LIGHT = (255, 240, 150)
SILVER = (200, 205, 215)
SILVER_DARK = (130, 135, 145)
SILVER_LIGHT = (245, 248, 255)

# Named "god-tier" sphere palettes. Each is (shadow, mid, highlight).
SPHERE_PALETTES = {
    "emerald":   ((0, 80, 50),    (0, 220, 130),  (180, 255, 220)),
    "amethyst":  ((40, 20, 90),   (140, 90, 230), (235, 215, 255)),
    "ruby":      ((90, 10, 30),   (230, 40, 90),  (255, 200, 215)),
    "sapphire":  ((10, 30, 90),   (50, 130, 230), (200, 225, 255)),
    "gold":      ((130, 90, 0),   (255, 200, 60), (255, 245, 200)),
    "plasma":    ((90, 0, 90),    (240, 50, 200), (255, 220, 250)),
    "cyber":     ((0, 80, 90),    (0, 230, 255),  (200, 255, 255)),
    "void":      ((10, 10, 25),   (50, 45, 80),   (160, 140, 220)),
    "molten":    ((110, 30, 0),   (255, 100, 30), (255, 230, 150)),
    "holo":      ((90, 60, 130),  (200, 180, 255),(255, 240, 255)),
}


# === Canvas helpers ===

def new_canvas():
    """48x48 RGBA, fully transparent."""
    return Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))


def put(canvas, x, y, color, alpha=255):
    """Paint a single pixel with optional alpha."""
    if 0 <= x < SIZE and 0 <= y < SIZE:
        r, g, b = color[:3]
        canvas.putpixel((x, y), (r, g, b, alpha))


def paint(canvas, pixels, color, alpha=255):
    """Paint a list of (x,y) coords."""
    for x, y in pixels:
        put(canvas, x, y, color, alpha)


def fill_rect(canvas, x0, y0, x1, y1, color, alpha=255):
    """Inclusive rectangle fill."""
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            put(canvas, x, y, color, alpha)


def mix(a, b, t):
    """Blend two RGB colors, t in [0,1]."""
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


# === Sphere primitive (the workhorse) ===

def draw_sphere(canvas, cx, cy, radius, palette, specular=True, rim=True):
    """Hand-shaded circle.

    palette = (shadow, mid, highlight)
    specular = white dot top-left of center
    rim = subtle rim-light pixels on the bottom-right edge
    """
    shadow, mid, hi = palette

    # Filled disc.
    for y in range(cy - radius, cy + radius + 1):
        for x in range(cx - radius, cx + radius + 1):
            dx, dy = x - cx, y - cy
            d2 = dx * dx + dy * dy
            if d2 > radius * radius:
                continue
            # Light direction: top-left brighter, bottom-right darker.
            # Project (dx,dy) onto normalized (-1,-1) light vector.
            r = math.sqrt(d2) / radius if radius else 0
            light = (-dx - dy) / (radius * 1.5) if radius else 0
            shade = (light + 1) / 2  # 0..1
            # Edge darkening on outer ring.
            if r > 0.92:
                color = shadow
            elif shade > 0.78:
                color = hi
            elif shade > 0.55:
                color = mix(mid, hi, (shade - 0.55) / 0.23)
            elif shade > 0.30:
                color = mid
            else:
                color = mix(shadow, mid, shade / 0.30)
            put(canvas, x, y, color)

    # Specular highlight: small bright cluster top-left.
    if specular and radius >= 4:
        sx = cx - max(1, radius // 2)
        sy = cy - max(1, radius // 2)
        put(canvas, sx, sy, WHITE)
        if radius >= 6:
            put(canvas, sx + 1, sy, mix(hi, WHITE, 0.5))
            put(canvas, sx, sy + 1, mix(hi, WHITE, 0.5))

    # Rim light: a few bright pixels on the bottom-right edge.
    if rim and radius >= 5:
        for ang_deg in (30, 45, 60):
            ang = math.radians(ang_deg)
            rx = int(cx + math.cos(ang) * (radius - 0.5))
            ry = int(cy + math.sin(ang) * (radius - 0.5))
            put(canvas, rx, ry, mix(mid, hi, 0.4))


# === Auras, glows, sparkles ===

def draw_glow_ring(canvas, cx, cy, radius, color, alpha=80):
    """Soft outer glow, one pixel ring at given radius."""
    for ang_deg in range(0, 360, 6):
        ang = math.radians(ang_deg)
        x = int(cx + math.cos(ang) * radius)
        y = int(cy + math.sin(ang) * radius)
        put(canvas, x, y, color, alpha)


def draw_sparkles(canvas, points, color, alpha=255):
    """4-pixel cross sparkles at given anchor points."""
    for (x, y) in points:
        put(canvas, x, y, color, alpha)
        put(canvas, x + 1, y, mix(color, WHITE, 0.5), alpha)
        put(canvas, x - 1, y, mix(color, WHITE, 0.5), alpha)
        put(canvas, x, y + 1, mix(color, WHITE, 0.5), alpha)
        put(canvas, x, y - 1, mix(color, WHITE, 0.5), alpha)


def draw_antenna(canvas, x0, y0, length, color, tip_color=WHITE):
    """Vertical antenna upward from (x0,y0)."""
    for i in range(length):
        put(canvas, x0, y0 - i, color)
    put(canvas, x0, y0 - length, tip_color)


# === Save helper ===

def save(canvas, path):
    pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
    canvas.save(path)
    return path


if __name__ == "__main__":
    # Quick smoke test: draw a single sphere of each palette.
    out = pathlib.Path("public/variants/_palette_test")
    out.mkdir(parents=True, exist_ok=True)
    for name, pal in SPHERE_PALETTES.items():
        c = new_canvas()
        draw_sphere(c, 24, 24, 12, pal)
        save(c, out / f"{name}.png")
    print(f"wrote {len(SPHERE_PALETTES)} palette samples to {out}")
