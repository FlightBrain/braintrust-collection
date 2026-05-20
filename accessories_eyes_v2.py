#!/usr/bin/env python3
"""Eye accessories v2. Overrides weak v3 entries and adds NFT-grade new ones.

All items anchored to the face template eye positions:
  Left eye:  cols 19-20, rows 21-22
  Right eye: cols 27-28, rows 21-22
  Brows:     row 19

Bold pixel work, 3-tone shading, alpha glows. No em dashes anywhere.
"""
import math
from items_v3 import (
    new_canvas, put, paint, fill_rect, mix,
    WHITE, BLACK, GOLD, GOLD_LIGHT,
)


# ============================================================================
# Local palette (kept here so this file is standalone, mirrors accessories_v3)
# ============================================================================
RED       = (220, 40, 50)
RED_HOT   = (255, 60, 70)
RED_DEEP  = (140, 10, 20)
BLUE      = (50, 130, 230)
BLUE_HOT  = (60, 180, 255)
GREEN     = (60, 200, 100)
GREEN_HOT = (40, 255, 120)
PURPLE    = (160, 80, 220)
PURPLE_HI = (210, 160, 255)
CYAN      = (0, 220, 255)
CYAN_HI   = (200, 255, 255)
PINK      = (255, 100, 180)
PINK_HI   = (255, 200, 230)
SILVER    = (200, 205, 215)
SILVER_HI = (250, 252, 255)
SILVER_LO = (130, 135, 150)


# ============================================================================
# Glow helper, used by several items below
# ============================================================================

def _soft_glow(canvas, cx, cy, radius, color, max_alpha=160, overwrite=False):
    """Soft radial alpha glow centered on (cx,cy).

    Skips pixels that already hold strong opaque content (alpha > 220)
    unless overwrite=True. Glow falls off linearly with distance.
    """
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            d = math.sqrt(dx * dx + dy * dy)
            if d > radius:
                continue
            x, y = cx + dx, cy + dy
            if not (0 <= x < 48 and 0 <= y < 48):
                continue
            falloff = 1.0 - (d / radius)
            alpha = int(max_alpha * falloff * falloff)
            if alpha <= 0:
                continue
            existing = canvas.getpixel((x, y))
            if not overwrite and existing[3] > 220:
                continue
            put(canvas, x, y, color, alpha=alpha)


# ============================================================================
# FIXES: overrides for weak v3 entries
# ============================================================================

def glowing_eyes(canvas, color="white"):
    """Solid demonic eyes with strong outer halo glow."""
    color_map = {
        "white":  (WHITE,             (220, 235, 255)),
        "red":    ((255, 50, 60),     (255, 120, 130)),
        "cyan":   (CYAN,              CYAN_HI),
        "yellow": ((255, 230, 40),    (255, 250, 200)),
    }
    core, glow = color_map[color]

    # Outer halo, big and strong. Drawn FIRST so the solid core sits on top.
    for (cx, cy) in [(19, 21), (27, 21)]:
        _soft_glow(canvas, cx, cy, radius=7, color=glow, max_alpha=230,
                   overwrite=True)
        # Secondary tighter halo for extra intensity
        _soft_glow(canvas, cx, cy, radius=4, color=core, max_alpha=200,
                   overwrite=True)

    # Solid pupil block, completely opaque, slightly bigger than v3.
    for (cx, cy) in [(19, 21), (27, 21)]:
        fill_rect(canvas, cx - 1, cy - 1, cx + 2, cy + 2, core)
        # Inner hot core, a touch brighter near center
        put(canvas, cx, cy, mix(core, WHITE, 0.5))
        put(canvas, cx + 1, cy, mix(core, WHITE, 0.5))


def three_d_glasses(canvas, color=None):
    """Retro 3D glasses. Chunky 2px frame, saturated red/blue lenses."""
    red_lens     = (255, 30, 40)
    red_lens_hi  = (255, 140, 150)
    blue_lens    = (30, 90, 255)
    blue_lens_hi = (130, 180, 255)

    # Lens fills
    fill_rect(canvas, 17, 20, 22, 23, red_lens)
    fill_rect(canvas, 25, 20, 30, 23, blue_lens)

    # Lens highlights (diagonal gleam)
    paint(canvas, [(18, 20), (18, 21), (19, 20)], red_lens_hi)
    paint(canvas, [(26, 20), (26, 21), (27, 20)], blue_lens_hi)

    # Chunky 2px white frame around each lens
    # Top + bottom
    fill_rect(canvas, 16, 18, 23, 19, WHITE)
    fill_rect(canvas, 16, 24, 23, 25, WHITE)
    fill_rect(canvas, 24, 18, 31, 19, WHITE)
    fill_rect(canvas, 24, 24, 31, 25, WHITE)
    # Left + right
    fill_rect(canvas, 15, 18, 16, 25, WHITE)
    fill_rect(canvas, 22, 18, 23, 25, WHITE)
    fill_rect(canvas, 24, 18, 25, 25, WHITE)
    fill_rect(canvas, 30, 18, 31, 25, WHITE)

    # Restore lens fills (frame just overwrote the top/bottom rows)
    fill_rect(canvas, 17, 20, 21, 23, red_lens)
    fill_rect(canvas, 26, 20, 30, 23, blue_lens)
    paint(canvas, [(18, 20), (18, 21), (19, 20)], red_lens_hi)
    paint(canvas, [(26, 20), (26, 21), (27, 20)], blue_lens_hi)

    # Bridge (chunky)
    fill_rect(canvas, 22, 20, 25, 21, WHITE)


def x_eyes(canvas, color="black"):
    """Big bold X marks with depth shadow."""
    main = (15, 15, 20) if color == "black" else RED
    shadow = mix(main, WHITE, 0.0)  # pure dark
    shadow = (max(0, main[0] - 40), max(0, main[1] - 40), max(0, main[2] - 40))

    # Each X spans 5x5 (cols span 4 for the stroke, plus a shadow row).
    # Left X: anchor center at (19.5, 21.5), so cols 17..22, rows 19..24
    for cx in [19, 27]:
        # Draw shadow first (offset +1,+1)
        for d in range(0, 5):
            put(canvas, cx - 2 + d + 1, 19 + d + 1, shadow, alpha=180)
            put(canvas, cx + 2 - d + 1, 19 + d + 1, shadow, alpha=180)
        # Main X stroke, double thickness for boldness
        for d in range(0, 5):
            # diagonal NW to SE
            put(canvas, cx - 2 + d, 19 + d, main)
            put(canvas, cx - 1 + d, 19 + d, main)
            # diagonal NE to SW
            put(canvas, cx + 2 - d, 19 + d, main)
            put(canvas, cx + 1 - d, 19 + d, main)
        # Center crossing brightened
        put(canvas, cx, 21, mix(main, WHITE, 0.4))


def money_eyes(canvas, color="green"):
    """Clean bold $ glyph, 5w x 7t, with green halo glow."""
    if color == "green":
        sign     = (40, 220, 110)
        sign_hi  = (180, 255, 200)
        sign_lo  = (20, 130, 60)
        glow_col = (60, 255, 130)
    else:
        sign     = GOLD
        sign_hi  = GOLD_LIGHT
        sign_lo  = (180, 140, 0)
        glow_col = (255, 230, 80)

    # 5w x 7t bold $ pattern. '#' = main, '@' = highlight, '%' = shadow.
    # Top stroke, middle stroke, bottom stroke with vertical bar through.
    pattern = [
        "..#..",
        ".####",
        "##...",
        ".###.",
        "...##",
        "####.",
        "..#..",
    ]

    # Two eye anchors: top-left of glyph
    # Glyph 5w fits centered on cols 19-20 if anchored at col 17,
    # and on cols 27-28 if anchored at col 25.
    for anchor_x in [17, 25]:
        anchor_y = 18
        cx = anchor_x + 2  # glyph center col
        cy = anchor_y + 3  # glyph center row
        # Halo first
        _soft_glow(canvas, cx, cy, radius=5, color=glow_col,
                   max_alpha=140, overwrite=True)
        # Then glyph
        for ry, row in enumerate(pattern):
            for rx, ch in enumerate(row):
                if ch == ".":
                    continue
                x, y = anchor_x + rx, anchor_y + ry
                if ch == "#":
                    put(canvas, x, y, sign)
                elif ch == "@":
                    put(canvas, x, y, sign_hi)
                elif ch == "%":
                    put(canvas, x, y, sign_lo)


# ============================================================================
# NEW: NFT-grade additions
# ============================================================================

def heart_eyes(canvas, color="pink"):
    """Pink/red heart-shaped eyes with sparkle dots above."""
    if color == "pink":
        base, hi, dark = PINK, PINK_HI, (200, 50, 120)
    else:
        base, hi, dark = (240, 40, 70), (255, 160, 180), (160, 10, 30)

    # 5w x 5t heart. '#' main, '@' highlight, '%' shadow, '.' skip.
    pattern = [
        "#.#.#",  # two lobes split by valley
        "#####",
        "#####",
        ".###.",
        "..#..",
    ]
    # Note: row 0 above is actually peaks. The real classic 5x5 heart is:
    pattern = [
        ".#.#.",
        "#####",
        "#####",
        ".###.",
        "..#..",
    ]
    for anchor_x in [17, 25]:
        anchor_y = 19
        # Wipe the eye-white block underneath (skin will show in the gaps,
        # which is what we want for the bilobed top valley).
        for dy in range(0, 5):
            for dx in range(0, 5):
                put(canvas, anchor_x + dx, anchor_y + dy, (0, 0, 0, 0))
        # Paint heart body
        for ry, row in enumerate(pattern):
            for rx, ch in enumerate(row):
                if ch != "#":
                    continue
                x, y = anchor_x + rx, anchor_y + ry
                put(canvas, x, y, base)
        # Highlight cluster top-left of each heart (glossy)
        put(canvas, anchor_x + 1, anchor_y + 1, hi)
        # Bottom-right shadow
        put(canvas, anchor_x + 3, anchor_y + 2, dark)
        put(canvas, anchor_x + 2, anchor_y + 3, dark)

        # Sparkle dots above the heart
        cx = anchor_x + 2
        sx_a, sy_a = cx - 3, anchor_y - 2
        sx_b, sy_b = cx + 2, anchor_y - 3
        put(canvas, sx_a, sy_a, WHITE)
        put(canvas, sx_a + 1, sy_a, mix(WHITE, base, 0.4))
        put(canvas, sx_a, sy_a + 1, mix(WHITE, base, 0.4))
        put(canvas, sx_b, sy_b, WHITE)
        put(canvas, sx_b + 1, sy_b, mix(WHITE, base, 0.4))


def hypnosis_swirl(canvas, color=None):
    """Concentric spiral pattern in each eye, alternating black/white."""
    # Clear and paint a 5x5 box per eye for the swirl, centered at eye anchor
    for cx, cy in [(19, 21), (27, 21)]:
        # Paint a clean 5x5 white background
        fill_rect(canvas, cx - 2, cy - 2, cx + 2, cy + 2, WHITE)
        # Spiral arms: walk outward in a square spiral, alternate colors
        # Manual coords for a tight 5x5 spiral
        spiral_a = [  # black ring 1 (outer)
            (cx - 2, cy - 2), (cx - 1, cy - 2), (cx, cy - 2),
            (cx + 1, cy - 2), (cx + 2, cy - 2),
            (cx + 2, cy - 1), (cx + 2, cy), (cx + 2, cy + 1), (cx + 2, cy + 2),
            (cx + 1, cy + 2), (cx, cy + 2), (cx - 1, cy + 2), (cx - 2, cy + 2),
            (cx - 2, cy + 1),
        ]
        spiral_b = [  # black arm inward
            (cx - 1, cy), (cx - 1, cy + 1), (cx, cy + 1), (cx + 1, cy + 1),
            (cx + 1, cy), (cx + 1, cy - 1), (cx, cy - 1),
        ]
        paint(canvas, spiral_a, BLACK)
        paint(canvas, spiral_b, BLACK)
        # Center pixel pure white (hypnotic dot)
        put(canvas, cx, cy, WHITE)


def third_eye(canvas, color="purple"):
    """Glowing extra eye on forehead at col 24, row 16, with divine rays."""
    color_map = {
        "purple": (PURPLE, PURPLE_HI, (90, 30, 140)),
        "cyan":   (CYAN, CYAN_HI, (0, 100, 140)),
        "gold":   (GOLD, GOLD_LIGHT, (170, 130, 0)),
    }
    base, hi, dark = color_map[color]
    cx, cy = 24, 16

    # Divine glow rays (8 directions), drawn first
    ray_dirs = [(0, -1), (1, -1), (1, 0), (1, 1),
                (0, 1), (-1, 1), (-1, 0), (-1, -1)]
    for (dx, dy) in ray_dirs:
        for step in range(2, 6):
            x, y = cx + dx * step, cy + dy * step
            if 0 <= x < 48 and 0 <= y < 48:
                alpha = max(40, 200 - step * 30)
                put(canvas, x, y, hi, alpha=alpha)

    # Outer glow blob
    _soft_glow(canvas, cx, cy, radius=4, color=base, max_alpha=160,
               overwrite=True)

    # Eye almond shape: 5w x 3t, then vertical pupil
    # White of the eye
    fill_rect(canvas, cx - 2, cy - 1, cx + 2, cy + 1, WHITE)
    put(canvas, cx - 2, cy - 1, (0, 0, 0, 0))  # corner cut
    put(canvas, cx + 2, cy - 1, (0, 0, 0, 0))
    put(canvas, cx - 2, cy + 1, (0, 0, 0, 0))
    put(canvas, cx + 2, cy + 1, (0, 0, 0, 0))
    # Iris fill (base color) covering middle
    fill_rect(canvas, cx - 1, cy - 1, cx + 1, cy + 1, base)
    # Vertical slit pupil
    put(canvas, cx, cy - 1, BLACK)
    put(canvas, cx, cy, BLACK)
    put(canvas, cx, cy + 1, BLACK)
    # Highlight gleam
    put(canvas, cx - 1, cy - 1, hi)


def kaleidoscope_eyes(canvas, color=None):
    """Per-eye 3x3 grid of bright rainbow color cells."""
    rainbow = [
        (255, 60, 80),    (255, 170, 50),   (255, 240, 80),
        (60, 230, 120),   (60, 190, 255),   (160, 100, 240),
        (255, 110, 210),  (255, 255, 255),  (255, 200, 60),
    ]
    # Use a different rotation for each eye for a mirror-like kaleidoscope feel
    for eye_idx, anchor_x in enumerate([17, 25]):
        anchor_y = 19
        rot = 4 if eye_idx else 0
        for ry in range(3):
            for rx in range(3):
                idx = (ry * 3 + rx + rot) % len(rainbow)
                col = rainbow[idx]
                x, y = anchor_x + rx, anchor_y + ry
                put(canvas, x, y, col)
        # 1px dark border around the 3x3 grid for definition
        for x in range(anchor_x - 1, anchor_x + 4):
            put(canvas, x, anchor_y - 1, BLACK)
            put(canvas, x, anchor_y + 3, BLACK)
        for y in range(anchor_y - 1, anchor_y + 4):
            put(canvas, anchor_x - 1, y, BLACK)
            put(canvas, anchor_x + 3, y, BLACK)


def anime_sparkle_eyes(canvas, color="blue"):
    """Giant sparkly anime eyes with multiple highlights and gradient."""
    grad_map = {
        "blue":   ((20, 60, 180), (60, 130, 255), (180, 220, 255)),
        "green":  ((20, 110, 50), (60, 200, 100), (180, 255, 200)),
        "purple": ((70, 30, 130), (160, 80, 220), (220, 180, 255)),
    }
    dark, mid, hi = grad_map[color]

    for anchor_x in [17, 25]:
        # 6 wide x 6 tall mega-eye, rows 18..23
        ax, ay = anchor_x, 18
        # White outline
        fill_rect(canvas, ax - 1, ay - 1, ax + 6, ay + 6, BLACK)
        fill_rect(canvas, ax, ay, ax + 5, ay + 5, WHITE)
        # Iris (round-ish, fills the lower portion)
        # Top of iris row
        fill_rect(canvas, ax + 1, ay + 1, ax + 4, ay + 1, dark)
        # Middle rows
        fill_rect(canvas, ax, ay + 2, ax + 5, ay + 4, mid)
        # Edge darken
        for y in range(ay + 2, ay + 5):
            put(canvas, ax, y, dark)
            put(canvas, ax + 5, y, dark)
        # Bottom curve
        fill_rect(canvas, ax + 1, ay + 5, ax + 4, ay + 5, dark)
        # Pupil
        fill_rect(canvas, ax + 2, ay + 3, ax + 3, ay + 4, BLACK)
        # Big highlight (top-right)
        put(canvas, ax + 4, ay + 2, WHITE)
        put(canvas, ax + 4, ay + 1, WHITE)
        put(canvas, ax + 3, ay + 2, WHITE)
        # Small highlight (bottom-left)
        put(canvas, ax + 1, ay + 4, hi)
        # Lower sparkle dot
        put(canvas, ax + 2, ay + 5, mix(hi, WHITE, 0.5))


def blindfold(canvas, color="black"):
    """Black silk band across both eyes with tie-knot bump on the right."""
    color_map = {
        "black": ((15, 15, 20),  (60, 60, 70),   (5, 5, 10)),
        "red":   ((150, 20, 30), (220, 60, 80),  (90, 10, 20)),
        "silk":  ((40, 40, 60),  (130, 130, 180),(20, 20, 35)),
    }
    base, hi, dark = color_map[color]

    # Main band across eyes, rows 20..23, full face width
    fill_rect(canvas, 13, 20, 34, 23, base)
    # Silk highlight stripe top
    fill_rect(canvas, 13, 20, 34, 20, hi)
    # Bottom shadow
    fill_rect(canvas, 13, 23, 34, 23, dark)
    # Subtle silk sheen pattern
    for x in range(15, 33, 4):
        put(canvas, x, 21, mix(base, hi, 0.5))

    # Tie knot on the right side (small bow)
    # Knot block
    fill_rect(canvas, 35, 20, 37, 23, base)
    fill_rect(canvas, 35, 20, 37, 20, hi)
    fill_rect(canvas, 35, 23, 37, 23, dark)
    # Loose tails trailing right
    paint(canvas, [(38, 21), (39, 22), (40, 23)], base)
    paint(canvas, [(38, 22), (39, 23)], dark)


def skull_eye_socket(canvas, color=None):
    """Right eye replaced with a black hollow socket. Skull mark below."""
    # Bigger hollow socket: rows 19..24, cols 25..30
    fill_rect(canvas, 25, 19, 30, 24, BLACK)
    # Dark-grey inner rim for depth
    paint(canvas, [(25, 19), (30, 19), (25, 24), (30, 24)], (40, 40, 45))
    # Cracked edges around the socket
    paint(canvas, [(24, 20), (24, 22), (31, 21), (31, 23)], BLACK)
    # Single hot glint deep inside (like a void with one tiny spark)
    put(canvas, 27, 22, (90, 90, 95))

    # Skull mark below the socket. 5x5 skull, centered on col 27, rows 26..30.
    # Cranium (white block)
    fill_rect(canvas, 25, 26, 29, 28, WHITE)
    # Eye sockets of mini skull
    fill_rect(canvas, 26, 27, 26, 27, BLACK)
    fill_rect(canvas, 28, 27, 28, 27, BLACK)
    # Nose triangle
    put(canvas, 27, 28, BLACK)
    # Jaw (two teeth tabs)
    put(canvas, 25, 29, WHITE)
    put(canvas, 27, 29, WHITE)
    put(canvas, 29, 29, WHITE)
    # Tooth gaps
    put(canvas, 26, 29, BLACK)
    put(canvas, 28, 29, BLACK)
    # Tiny drop shadow under
    fill_rect(canvas, 25, 30, 29, 30, (60, 60, 60), alpha=140)


def evil_red_glow(canvas, color=None):
    """Horizontal red slit eyes with diffuse red haze."""
    slit = (255, 30, 40)
    slit_hot = (255, 120, 130)
    haze = (255, 50, 60)

    # Wipe original eye whites with skin-ish tone is unnecessary; the slits
    # and haze will dominate. Just paint over.
    # Red haze around each eye, drawn first
    for (cx, cy) in [(19, 21), (27, 21)]:
        _soft_glow(canvas, cx, cy, radius=5, color=haze, max_alpha=170,
                   overwrite=True)

    # Slit rows: row 21 across each eye, 4 pixels wide, 1 pixel tall
    for cx in [18, 26]:
        fill_rect(canvas, cx, 21, cx + 3, 21, slit)
        # Hot center pixel
        put(canvas, cx + 1, 21, slit_hot)
        put(canvas, cx + 2, 21, slit_hot)
        # Tiny darker rim above and below for definition
        fill_rect(canvas, cx, 20, cx + 3, 20, RED_DEEP, alpha=180)
        fill_rect(canvas, cx, 22, cx + 3, 22, RED_DEEP, alpha=180)


def cyber_implant(canvas, color="cyan"):
    """Mechanical right eye with cyan crosshair and bolts."""
    color_map = {
        "cyan": (CYAN, CYAN_HI, (0, 100, 140)),
        "red":  (RED_HOT, (255, 180, 180), (130, 10, 20)),
    }
    glow, hi, dark = color_map[color]

    # Socket: dark mechanical plate around right eye (cols 24..31, rows 18..25)
    fill_rect(canvas, 24, 18, 31, 25, (30, 32, 40))
    # Plate highlight (top edge) and shadow (bottom)
    fill_rect(canvas, 24, 18, 31, 18, (90, 95, 110))
    fill_rect(canvas, 24, 25, 31, 25, (10, 12, 18))
    # Bolts at four corners
    for (bx, by) in [(24, 18), (31, 18), (24, 25), (31, 25)]:
        put(canvas, bx, by, SILVER_HI)
    # Inner socket recess
    fill_rect(canvas, 25, 19, 30, 24, (10, 12, 18))

    # Lens: round-ish glowing disc center at (27.5, 21.5)
    # Fill inner lens 4w x 4t
    fill_rect(canvas, 26, 20, 29, 23, glow)
    # Edge darken (corners)
    paint(canvas, [(26, 20), (29, 20), (26, 23), (29, 23)], dark)
    # Crosshair: vertical and horizontal black lines through center
    fill_rect(canvas, 27, 20, 28, 23, BLACK)  # vertical bar pair
    fill_rect(canvas, 26, 21, 29, 22, BLACK)  # horizontal bar pair
    # Re-paint glowing dot at exact center
    put(canvas, 27, 21, hi)
    put(canvas, 28, 22, hi)
    # Outer glow halo
    _soft_glow(canvas, 27, 21, radius=4, color=glow, max_alpha=120)

    # Small status LED on the plate
    put(canvas, 30, 19, (40, 255, 100))
    put(canvas, 25, 24, (255, 60, 60))


def tear_drop_blood(canvas, color=None):
    """Single red blood tear streaming from the right eye, 2px wide."""
    blood     = (210, 20, 35)
    blood_hi  = (255, 90, 100)
    blood_lo  = (130, 5, 15)

    # Bead at the lower lid of the right eye (2x2)
    fill_rect(canvas, 27, 23, 28, 24, blood)
    put(canvas, 27, 23, blood_hi)

    # Stream down the cheek, 2px wide, slight rightward curve.
    # Coordinates of the LEFT column of the stream:
    left_col_by_row = {
        25: 27, 26: 27,
        27: 28, 28: 28, 29: 28,
        30: 28, 31: 28,
    }
    for y, lx in left_col_by_row.items():
        put(canvas, lx, y, blood)
        put(canvas, lx + 1, y, blood)
        # Left-side highlight
        put(canvas, lx, y, blood_hi if y % 3 == 0 else blood)
        # Right-side shadow
        put(canvas, lx + 1, y, blood_lo if y % 4 == 0 else blood)

    # Big drip droplet at the bottom (3x3 teardrop)
    fill_rect(canvas, 27, 32, 29, 33, blood)
    put(canvas, 27, 32, blood_hi)
    put(canvas, 29, 33, blood_lo)
    put(canvas, 28, 34, blood)


# ============================================================================
# REGISTRY
# ============================================================================

ACCESSORIES_EYES_V2 = {
    "glowing_eyes":       (glowing_eyes,       ["white", "red", "cyan", "yellow"]),
    "three_d_glasses":    (three_d_glasses,    [None]),
    "x_eyes":             (x_eyes,             ["black", "red"]),
    "money_eyes":         (money_eyes,         ["green", "gold"]),
    "heart_eyes":         (heart_eyes,         ["pink", "red"]),
    "hypnosis_swirl":     (hypnosis_swirl,     [None]),
    "third_eye":          (third_eye,          ["purple", "cyan", "gold"]),
    "kaleidoscope_eyes":  (kaleidoscope_eyes,  [None]),
    "anime_sparkle_eyes": (anime_sparkle_eyes, ["blue", "green", "purple"]),
    "blindfold":          (blindfold,          ["black", "red", "silk"]),
    "skull_eye_socket":   (skull_eye_socket,   [None]),
    "evil_red_glow":      (evil_red_glow,      [None]),
    "cyber_implant":      (cyber_implant,      ["cyan", "red"]),
    "tear_drop_blood":    (tear_drop_blood,    [None]),
}


# ============================================================================
# Smoke test
# ============================================================================

if __name__ == "__main__":
    import pathlib
    from face_template import draw_face_template

    out = pathlib.Path("public/variants/_eyes_v2_smoke")
    out.mkdir(parents=True, exist_ok=True)

    failures = []
    for name, (fn, colors) in ACCESSORIES_EYES_V2.items():
        c = new_canvas()
        draw_face_template(c)
        try:
            if colors[0] is None:
                fn(c)
            else:
                fn(c, color=colors[0])
            c.save(out / f"{name}.png")
        except Exception as e:
            failures.append((name, repr(e)))

    print(f"wrote {len(ACCESSORIES_EYES_V2) - len(failures)} eyes_v2 smoke tests to {out}")
    if failures:
        print("FAILURES:")
        for n, err in failures:
            print(f"  {n}: {err}")
    else:
        print("all passed")
