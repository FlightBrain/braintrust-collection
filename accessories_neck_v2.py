#!/usr/bin/env python3
"""Neck/collar accessories v2. NFT-grade pixel art at 48x48.

All accessories sit BELOW the chin (row 37+) and never touch the face.
Neck zone: rows 37-41 (skin). Collarbone: rows 40-41. Shirt/collar: rows 42-47.
Centered around col 24.

3-tone shading per item (shadow, mid, highlight). No em dashes.
"""
import math
from items_v3 import (
    new_canvas, put, paint, fill_rect, mix,
    WHITE, BLACK, GOLD, GOLD_LIGHT, GOLD_DARK,
)

# === Common palettes ===
RED         = (200, 35, 45)
RED_HI      = (240, 90, 100)
RED_DARK    = (130, 15, 25)
NAVY        = (30, 50, 110)
NAVY_HI     = (70, 100, 175)
NAVY_DARK   = (15, 25, 65)
SILVER      = (200, 205, 215)
SILVER_HI   = (250, 252, 255)
SILVER_LO   = (130, 135, 150)
PINK        = (255, 145, 175)
PINK_HI     = (255, 200, 220)
PINK_LO     = (190, 90, 130)
PURPLE      = (160, 80, 220)
PURPLE_HI   = (220, 180, 255)
PURPLE_LO   = (90, 30, 140)
EMERALD     = (40, 180, 100)
EMERALD_HI  = (160, 240, 190)
EMERALD_LO  = (15, 90, 50)
SAPPHIRE    = (50, 130, 230)
SAPPHIRE_HI = (180, 220, 255)
SAPPHIRE_LO = (15, 60, 140)
RUBY        = (220, 40, 80)
RUBY_HI     = (255, 170, 190)
RUBY_LO     = (120, 15, 40)
PEARL       = (245, 240, 230)
PEARL_HI    = (255, 255, 250)
PEARL_LO    = (180, 175, 165)
BANDANA_RED   = (190, 35, 45)
BANDANA_RED_HI= (230, 90, 100)
BANDANA_RED_LO= (120, 15, 25)
BANDANA_BLUE   = (40, 80, 175)
BANDANA_BLUE_HI= (90, 140, 220)
BANDANA_BLUE_LO= (20, 40, 100)


# ===========================================================================
# FIXES (override existing weak versions)
# ===========================================================================

def bowtie(canvas, color="red"):
    """BIG bowtie. Each wing 7px wide. Centered at collar rows 41-45.

    Colors: red, black, purple, striped (red+white stripes).
    """
    color_map = {
        "red":     ((180, 30, 40),   (230, 80, 90),   (110, 15, 20)),
        "black":   ((22, 22, 28),    (65, 65, 75),    (5, 5, 10)),
        "purple":  (PURPLE,          PURPLE_HI,       PURPLE_LO),
        "striped": ((180, 30, 40),   (250, 250, 250), (110, 15, 20)),
    }
    base, hi, dark = color_map[color]

    # Left wing: cols 14-22, rows 41-45 (triangle pointed inward).
    # Wider on the outside, taper to knot.
    left_shape = {
        41: (16, 22),
        42: (15, 22),
        43: (14, 22),
        44: (15, 22),
        45: (16, 22),
    }
    for y, (x0, x1) in left_shape.items():
        fill_rect(canvas, x0, y, x1, y, base)

    # Right wing: cols 26-34, mirror.
    right_shape = {
        41: (26, 32),
        42: (26, 33),
        43: (26, 34),
        44: (26, 33),
        45: (26, 32),
    }
    for y, (x0, x1) in right_shape.items():
        fill_rect(canvas, x0, y, x1, y, base)

    # Stripe pattern overlay (if striped)
    if color == "striped":
        white = (250, 250, 250)
        # Diagonal stripes on each wing
        for y in range(41, 46):
            for x in range(14, 23):
                if (x + y) % 3 == 0:
                    # only stamp on existing wing pixels
                    px = canvas.getpixel((x, y))
                    if px[3] > 0:
                        put(canvas, x, y, white)
            for x in range(26, 35):
                if (x + y) % 3 == 0:
                    px = canvas.getpixel((x, y))
                    if px[3] > 0:
                        put(canvas, x, y, white)

    # Highlights: top-left of each wing
    fill_rect(canvas, 15, 42, 17, 42, hi)
    fill_rect(canvas, 26, 42, 28, 42, hi)

    # Shadows: bottom of each wing
    fill_rect(canvas, 15, 45, 17, 45, dark)
    fill_rect(canvas, 31, 45, 33, 45, dark)

    # Outer dark edge to give definition
    paint(canvas, [(14, 43), (15, 44), (15, 42)], dark)
    paint(canvas, [(34, 43), (33, 44), (33, 42)], dark)

    # Center knot: cols 23-25, rows 41-45 (taller, dark with mid highlight)
    fill_rect(canvas, 23, 41, 25, 45, dark)
    fill_rect(canvas, 23, 42, 23, 44, base)
    put(canvas, 24, 42, hi)
    # Knot horizontal pinch lines
    put(canvas, 23, 43, base)
    put(canvas, 25, 43, base)


def fat_gold_chain(canvas, color="gold"):
    """Thick chain links + 6x6 BT-brain pendant. Maximum drip."""
    if color == "gold":
        c, c_hi, c_dark = GOLD, GOLD_LIGHT, GOLD_DARK
    else:
        c, c_hi, c_dark = SILVER, SILVER_HI, SILVER_LO

    # Chain: 2 rows thick (rows 40-41), chunky links every 3 cols.
    # Each link is 2x2 with highlight + shadow.
    for x in range(10, 38, 3):
        # 2x2 link block
        fill_rect(canvas, x, 40, x + 1, 41, c)
        put(canvas, x, 40, c_hi)         # top-left highlight
        put(canvas, x + 1, 41, c_dark)   # bottom-right shadow
        # Connector pixel between links
        if x + 2 < 38:
            put(canvas, x + 2, 40, c_dark)
            put(canvas, x + 2, 41, c)

    # Pendant: 6x6 square, rows 42-47, cols 21-26
    fill_rect(canvas, 21, 42, 26, 47, c)
    # Bezel edges
    fill_rect(canvas, 21, 42, 26, 42, c_hi)   # top highlight
    fill_rect(canvas, 21, 42, 21, 47, c_hi)   # left highlight
    fill_rect(canvas, 26, 42, 26, 47, c_dark) # right shadow
    fill_rect(canvas, 21, 47, 26, 47, c_dark) # bottom shadow

    # Bail (loop connecting pendant to chain)
    put(canvas, 23, 41, c_dark)
    put(canvas, 24, 41, c_dark)

    # BT brain logo etched into pendant (inner 4x4 area, rows 43-46, cols 22-25)
    etch = mix(c, BLACK, 0.55)
    etch_hi = mix(c, BLACK, 0.30)
    # Brain shape: two lobes with center fold
    # row 43: top of brain (two bumps)
    put(canvas, 22, 43, etch)
    put(canvas, 25, 43, etch)
    # row 44: lobes wider
    fill_rect(canvas, 22, 44, 25, 44, etch)
    put(canvas, 23, 44, etch_hi)  # center fold lighter
    # row 45: brain bottom
    fill_rect(canvas, 22, 45, 25, 45, etch)
    put(canvas, 24, 45, etch_hi)
    # row 46: stem
    put(canvas, 23, 46, etch)
    put(canvas, 24, 46, etch)


# ===========================================================================
# NEW ACCESSORIES
# ===========================================================================

def necktie(canvas, color="red"):
    """Classic suit tie. Knot at throat (cols 22-26 rows 38-40), body hangs to row 47.

    Colors: red, navy, striped (navy with diagonal red).
    """
    color_map = {
        "red":     (RED, RED_HI, RED_DARK),
        "navy":    (NAVY, NAVY_HI, NAVY_DARK),
        "striped": (NAVY, NAVY_HI, NAVY_DARK),
    }
    base, hi, dark = color_map[color]

    # Knot: cols 22-26, rows 38-40 (trapezoid-ish)
    fill_rect(canvas, 23, 38, 25, 38, base)
    fill_rect(canvas, 22, 39, 26, 39, base)
    fill_rect(canvas, 22, 40, 26, 40, base)
    # Knot dimple (vertical highlight line in center)
    put(canvas, 24, 38, hi)
    put(canvas, 24, 39, hi)
    # Knot shadow on right
    put(canvas, 26, 39, dark)
    put(canvas, 26, 40, dark)

    # Tie body: cols 22-26 row 41 (top, slightly narrower)
    fill_rect(canvas, 22, 41, 26, 41, base)
    # Widen down to a point. Standard tie tapers wider then to V tip.
    fill_rect(canvas, 21, 42, 27, 44, base)
    fill_rect(canvas, 21, 45, 27, 45, base)
    fill_rect(canvas, 22, 46, 26, 46, base)
    fill_rect(canvas, 23, 47, 25, 47, base)

    # Left highlight stripe (vertical)
    for y in range(42, 47):
        put(canvas, 22, y, hi)
    # Right shadow stripe
    for y in range(42, 47):
        put(canvas, 26, y, dark)

    # Striped pattern overlay
    if color == "striped":
        stripe = RED
        # Diagonal stripes across body
        for y in range(41, 48):
            for x in range(21, 28):
                if (x - y) % 4 == 0:
                    px = canvas.getpixel((x, y))
                    if px[3] > 0:
                        put(canvas, x, y, stripe)


def pearl_necklace(canvas, color="white"):
    """Curved row of pearls across collarbone with central drop pearl."""
    pal = {
        "white": (PEARL, PEARL_HI, PEARL_LO),
        "black": ((50, 50, 60), (110, 110, 125), (15, 15, 22)),
        "pink":  (PINK, PINK_HI, PINK_LO),
    }
    base, hi, dark = pal[color]

    # Curve of pearls across rows 39-41. Slight arc shape.
    # Each "pearl" is a 2x2 block with a highlight pixel.
    pearl_positions = [
        (11, 39), (14, 40), (17, 40), (20, 41),
        (23, 41), (26, 41), (29, 40), (32, 40), (35, 39),
    ]
    for (x, y) in pearl_positions:
        fill_rect(canvas, x, y, x + 1, y + 1, base)
        put(canvas, x, y, hi)              # top-left specular
        put(canvas, x + 1, y + 1, dark)    # bottom-right shadow

    # Connecting string (thin dark line between pearls)
    string_pts = [(13, 40), (16, 41), (19, 41), (22, 42), (25, 42), (28, 41), (31, 41), (34, 40)]
    for (x, y) in string_pts:
        px = canvas.getpixel((x, y))
        if px[3] < 200:
            put(canvas, x, y, dark)

    # Central drop pearl: bigger 3x3 below center
    fill_rect(canvas, 23, 43, 25, 45, base)
    put(canvas, 23, 43, hi)
    put(canvas, 25, 45, dark)
    put(canvas, 24, 44, hi)  # specular gleam
    # String to drop
    put(canvas, 24, 42, dark)


def brain_pendant_chain(canvas, color="gold"):
    """Thin chain with pink brain pendant (BT homage), folds visible."""
    if color == "gold":
        c, c_hi, c_dark = GOLD, GOLD_LIGHT, GOLD_DARK
    else:
        c, c_hi, c_dark = SILVER, SILVER_HI, SILVER_LO

    # Thin chain: single-pixel dotted across rows 40-41
    for x in range(11, 37, 2):
        put(canvas, x, 40, c)
        put(canvas, x + 1, 41, c_dark)

    # Connector to pendant
    put(canvas, 24, 41, c)

    # Brain pendant: cols 22-26 rows 42-45, pink with darker folds
    brain_base = PINK
    brain_hi   = PINK_HI
    brain_dark = PINK_LO

    # Brain outline (two lobes shape)
    # row 42: top bumps
    paint(canvas, [(22, 42), (23, 42), (25, 42), (26, 42)], brain_base)
    put(canvas, 24, 42, brain_dark)  # center cleft
    # row 43: full top
    fill_rect(canvas, 21, 43, 27, 43, brain_base)
    put(canvas, 22, 43, brain_hi)
    put(canvas, 26, 43, brain_hi)
    # row 44: middle (widest)
    fill_rect(canvas, 21, 44, 27, 44, brain_base)
    # fold lines (darker squiggles)
    put(canvas, 23, 44, brain_dark)
    put(canvas, 25, 44, brain_dark)
    # row 45: bottom (taper)
    fill_rect(canvas, 22, 45, 26, 45, brain_base)
    put(canvas, 24, 45, brain_dark)
    # stem / brainstem
    put(canvas, 23, 46, brain_base)
    put(canvas, 24, 46, brain_dark)
    put(canvas, 25, 46, brain_base)

    # Gold/silver bezel around top of pendant
    put(canvas, 21, 42, c_dark)
    put(canvas, 27, 42, c_dark)


def dog_tags(canvas, color="silver"):
    """Military dog tags. Ball chain + one large central tag."""
    if color == "silver":
        c, c_hi, c_dark = SILVER, SILVER_HI, SILVER_LO
    else:
        c, c_hi, c_dark = GOLD, GOLD_LIGHT, GOLD_DARK

    # Ball chain: dotted across rows 39-40
    chain_pts = [(11, 39), (13, 39), (15, 40), (17, 40), (19, 40),
                 (21, 40), (23, 40), (25, 40), (27, 40), (29, 40),
                 (31, 40), (33, 39), (35, 39)]
    for (x, y) in chain_pts:
        put(canvas, x, y, c)

    # Connector loops to tag (two short verticals)
    put(canvas, 22, 41, c_dark)
    put(canvas, 26, 41, c_dark)

    # Large central tag: cols 20-28, rows 41-47, rounded corners
    fill_rect(canvas, 21, 41, 27, 47, c)
    # Round the corners (clear corner pixels and refill rounded)
    put(canvas, 21, 41, (0, 0, 0, 0))
    put(canvas, 27, 41, (0, 0, 0, 0))
    put(canvas, 21, 47, (0, 0, 0, 0))
    put(canvas, 27, 47, (0, 0, 0, 0))

    # Top highlight
    fill_rect(canvas, 22, 41, 26, 41, c_hi)
    # Left highlight column
    fill_rect(canvas, 21, 42, 21, 46, c_hi)
    # Right shadow
    fill_rect(canvas, 27, 42, 27, 46, c_dark)
    # Bottom shadow
    fill_rect(canvas, 22, 47, 26, 47, c_dark)

    # Hole at top center (for chain)
    put(canvas, 24, 41, c_dark)

    # Etched text lines (3 horizontal lines of "stamped" text)
    etch = mix(c, BLACK, 0.55)
    fill_rect(canvas, 22, 43, 26, 43, etch)
    fill_rect(canvas, 22, 45, 25, 45, etch)
    # tiny dot detail
    put(canvas, 23, 44, etch)
    put(canvas, 25, 44, etch)


def bandana_neck(canvas, color="red"):
    """Paisley bandana wrapped around neck. Knot visible on right side."""
    pal = {
        "red":   (BANDANA_RED, BANDANA_RED_HI, BANDANA_RED_LO),
        "blue":  (BANDANA_BLUE, BANDANA_BLUE_HI, BANDANA_BLUE_LO),
        "black": ((30, 30, 38), (75, 75, 90), (10, 10, 15)),
    }
    base, hi, dark = pal[color]

    # Wrap: cols 18-30, rows 39-42 (around neck)
    fill_rect(canvas, 18, 39, 30, 42, base)
    # Top edge highlight
    fill_rect(canvas, 18, 39, 30, 39, hi)
    # Bottom edge shadow
    fill_rect(canvas, 18, 42, 30, 42, dark)
    # Left edge shadow
    fill_rect(canvas, 18, 39, 18, 42, dark)

    # Knot on right side: cols 31-34, rows 40-42 (bunched fabric)
    fill_rect(canvas, 31, 40, 34, 42, base)
    put(canvas, 31, 40, hi)
    put(canvas, 34, 42, dark)
    # Tail flaps
    paint(canvas, [(34, 41), (35, 42), (33, 43)], base)
    put(canvas, 35, 42, dark)

    # Paisley pattern: white dots scattered on the wrap
    paisley_color = (250, 250, 245) if color != "black" else (200, 200, 210)
    paisley_pts = [(20, 40), (23, 41), (26, 40), (29, 41), (21, 42), (25, 39), (28, 42)]
    for (x, y) in paisley_pts:
        px = canvas.getpixel((x, y))
        if px[3] > 0:
            put(canvas, x, y, paisley_color)

    # Knot center dimple
    put(canvas, 32, 41, dark)


def ascot(canvas, color="red"):
    """Silk ascot, V-shape at throat, tucked into shirt."""
    pal = {
        "red":  (RED, RED_HI, RED_DARK),
        "gold": (GOLD, GOLD_LIGHT, GOLD_DARK),
        "navy": (NAVY, NAVY_HI, NAVY_DARK),
    }
    base, hi, dark = pal[color]

    # V at the throat: rows 38-41, cols 20-28
    # Outer V edges
    v_shape = {
        38: [(21, 22), (26, 27)],   # two thin top pieces (collar wings)
        39: [(20, 23), (25, 28)],
        40: [(21, 27)],             # wider middle
        41: [(22, 26)],             # bottom point
    }
    for y, segments in v_shape.items():
        for (x0, x1) in segments:
            fill_rect(canvas, x0, y, x1, y, base)

    # Silk highlight (left side of each fold)
    paint(canvas, [(21, 39), (22, 40), (23, 41)], hi)
    paint(canvas, [(25, 39), (24, 40)], hi)
    # Right-side shadow
    paint(canvas, [(23, 39), (27, 40), (26, 41)], dark)
    paint(canvas, [(28, 39)], dark)

    # Body of ascot tucked at top of shirt: rows 42-43 cols 21-27 (wider bib)
    fill_rect(canvas, 21, 42, 27, 43, base)
    # Top highlight (silk sheen)
    fill_rect(canvas, 21, 42, 27, 42, hi)
    # Right shadow column
    put(canvas, 27, 43, dark)
    # Decorative pin (small gold dot center)
    pin = GOLD if color != "gold" else SILVER
    put(canvas, 24, 42, pin)


def choker_spike(canvas, color=None):
    """Punk leather choker, pure black band with silver spikes every 3px."""
    band = (15, 15, 20)
    band_hi = (45, 45, 55)
    spike = SILVER
    spike_hi = SILVER_HI
    spike_dark = SILVER_LO

    # Band: cols 18-30, rows 39-40 (tight around neck)
    fill_rect(canvas, 18, 39, 30, 40, band)
    # Subtle leather highlight on top
    fill_rect(canvas, 18, 39, 30, 39, band_hi)

    # Spikes sticking outward (up from band): every 3 px
    # Each spike is 1px wide, 2px tall pyramid
    for x in range(19, 31, 3):
        # spike points up
        put(canvas, x, 38, spike)
        put(canvas, x, 37, spike_hi)
        # base shadow on band
        put(canvas, x, 39, spike_dark)

    # Side spikes pointing outward (left and right edges)
    put(canvas, 17, 39, spike)
    put(canvas, 16, 39, spike_hi)
    put(canvas, 31, 40, spike)
    put(canvas, 32, 40, spike_hi)

    # Buckle in center (small silver square)
    fill_rect(canvas, 23, 39, 25, 40, spike_dark)
    put(canvas, 24, 39, spike_hi)


def crystal_pendant(canvas, color="purple"):
    """Single large faceted crystal hanging on a thin chain."""
    pal = {
        "purple": (PURPLE_LO, PURPLE, PURPLE_HI),
        "blue":   (SAPPHIRE_LO, SAPPHIRE, SAPPHIRE_HI),
        "green":  (EMERALD_LO, EMERALD, EMERALD_HI),
        "ruby":   (RUBY_LO, RUBY, RUBY_HI),
    }
    shadow, mid, hi = pal[color]

    # Thin chain (single-pixel dotted) across rows 39-40
    for x in range(11, 37, 2):
        put(canvas, x, 39, SILVER_LO)
        put(canvas, x + 1, 40, SILVER)

    # Connector to crystal
    put(canvas, 24, 41, SILVER_LO)

    # Faceted diamond/crystal shape:
    # Top point (small), widens to middle, tapers to bottom point.
    # Rows 42-47, cols 21-27
    crystal_shape = {
        42: (24, 24),         # top point (1 px)
        43: (23, 25),         # 3 px wide
        44: (22, 26),         # 5 px wide
        45: (21, 27),         # 7 px wide (widest)
        46: (22, 26),         # taper
        47: (24, 24),         # bottom point
    }
    for y, (x0, x1) in crystal_shape.items():
        fill_rect(canvas, x0, y, x1, y, mid)

    # Add facet shading: left side highlight, right side shadow
    # Left facet (highlight)
    paint(canvas, [(23, 43), (22, 44), (21, 45), (22, 46)], hi)
    # Right facet (shadow)
    paint(canvas, [(25, 43), (26, 44), (27, 45), (26, 46)], shadow)
    # Center line (mid)
    put(canvas, 24, 43, mix(mid, hi, 0.5))
    put(canvas, 24, 44, mid)
    put(canvas, 24, 45, mix(mid, shadow, 0.3))
    put(canvas, 24, 46, mid)

    # Specular pinpoint
    put(canvas, 23, 44, WHITE)


def gold_medallion(canvas, color="gold"):
    """Huge disk pendant with etched star, on chunky chain. Maximum drip."""
    if color == "gold":
        c, c_hi, c_dark = GOLD, GOLD_LIGHT, GOLD_DARK
    else:
        c, c_hi, c_dark = SILVER, SILVER_HI, SILVER_LO

    # Chunky chain: 2 rows thick (rows 39-40), bigger links
    for x in range(10, 38, 3):
        fill_rect(canvas, x, 39, x + 1, 40, c)
        put(canvas, x, 39, c_hi)
        put(canvas, x + 1, 40, c_dark)

    # Bail (loop connecting medallion to chain)
    put(canvas, 23, 41, c)
    put(canvas, 24, 41, c_dark)
    put(canvas, 25, 41, c)

    # Medallion disk: roughly circular, cols 19-29 rows 42-47
    # Drawn manually since it sits on the edge of canvas.
    disk_shape = {
        42: (22, 26),
        43: (20, 28),
        44: (19, 29),
        45: (19, 29),
        46: (20, 28),
        47: (22, 26),
    }
    for y, (x0, x1) in disk_shape.items():
        fill_rect(canvas, x0, y, x1, y, c)

    # Outer bezel (darker edge)
    paint(canvas, [(22, 42), (26, 42),
                   (20, 43), (28, 43),
                   (19, 44), (29, 44),
                   (19, 45), (29, 45),
                   (20, 46), (28, 46),
                   (22, 47), (26, 47)], c_dark)

    # Top-left highlight arc
    paint(canvas, [(23, 42), (24, 42),
                   (21, 43), (22, 43),
                   (20, 44), (21, 44)], c_hi)

    # Etched star (5-point) in center, dark
    etch = mix(c, BLACK, 0.55)
    # Star pattern (5-point, 5x5)
    # row 43: top point
    put(canvas, 24, 43, etch)
    # row 44: upper wings
    put(canvas, 22, 44, etch)
    put(canvas, 23, 44, etch)
    put(canvas, 24, 44, etch)
    put(canvas, 25, 44, etch)
    put(canvas, 26, 44, etch)
    # row 45: middle body
    put(canvas, 23, 45, etch)
    put(canvas, 24, 45, etch)
    put(canvas, 25, 45, etch)
    # row 46: lower legs
    put(canvas, 22, 46, etch)
    put(canvas, 26, 46, etch)


# === REGISTRY ===

ACCESSORIES_NECK_V2 = {
    "bowtie":              (bowtie,              ["red", "black", "purple", "striped"]),
    "fat_gold_chain":      (fat_gold_chain,      ["gold", "silver"]),
    "necktie":             (necktie,             ["red", "navy", "striped"]),
    "pearl_necklace":      (pearl_necklace,      ["white", "black", "pink"]),
    "brain_pendant_chain": (brain_pendant_chain, ["gold", "silver"]),
    "dog_tags":            (dog_tags,            ["silver", "gold"]),
    "bandana_neck":        (bandana_neck,        ["red", "blue", "black"]),
    "ascot":               (ascot,               ["red", "gold", "navy"]),
    "choker_spike":        (choker_spike,        [None]),
    "crystal_pendant":     (crystal_pendant,     ["purple", "blue", "green", "ruby"]),
    "gold_medallion":      (gold_medallion,      ["gold", "silver"]),
}


if __name__ == "__main__":
    import pathlib
    from face_template import draw_face_template

    out = pathlib.Path("public/variants/_neck_v2_smoke")
    out.mkdir(parents=True, exist_ok=True)

    count = 0
    for name, (fn, colors) in ACCESSORIES_NECK_V2.items():
        for col in colors:
            c = new_canvas()
            draw_face_template(c)
            try:
                if col is None:
                    fn(c)
                else:
                    fn(c, color=col)
            except TypeError:
                fn(c)
            suffix = f"_{col}" if col else ""
            c.save(out / f"{name}{suffix}.png")
            count += 1

    print(f"wrote {count} neck v2 accessory smoke tests to {out}")
