#!/usr/bin/env python3
"""Head accessories v2: improved fixes for weak items and new NFT-grade pieces.

Improves over accessories_v3.py for: beanie, halo, laurel_crown, devil_horns.
Adds: spartan_helmet, motorcycle_helmet, baseball_cap, durag, knight_helmet,
crown_of_thorns, viking_helmet, headband.

All items render onto the neutral face template (face_template.py). Head spans
rows 6..36, cols 14..33. Eyes are at rows 21..22 (cols 19..20 and 27..28).
Items must not clip into eye rows.

Style: 3-tone shading per item (shadow, mid, highlight). No em dashes.
"""
import math
from items_v3 import (
    new_canvas, put, paint, fill_rect, mix,
    WHITE, BLACK, GOLD, GOLD_LIGHT, GOLD_DARK,
)

# === Common palettes ===
RED        = (220, 40, 50)
RED_DARK   = (140, 20, 30)
RED_HI     = (245, 90, 100)
NAVY       = (30, 50, 110)
NAVY_DARK  = (15, 25, 65)
NAVY_HI    = (70, 100, 170)
GREEN      = (60, 150, 70)
GREEN_DARK = (30, 90, 40)
GREEN_HI   = (110, 210, 120)
YELLOW     = (240, 200, 60)
YELLOW_DARK= (180, 140, 30)
YELLOW_HI  = (255, 235, 110)
SILVER     = (200, 205, 215)
SILVER_HI  = (250, 252, 255)
SILVER_LO  = (130, 135, 150)
STEEL      = (160, 168, 185)
STEEL_HI   = (220, 226, 240)
STEEL_LO   = (95, 100, 115)
BRONZE     = (170, 110, 50)
BRONZE_HI  = (220, 160, 80)
BRONZE_LO  = (105, 65, 25)
SILK_BLUE  = (60, 90, 180)
SILK_BLUE_HI = (130, 160, 230)
SILK_BLUE_LO = (30, 50, 110)
THORN      = (55, 40, 25)
THORN_HI   = (95, 75, 50)
THORN_LO   = (25, 18, 12)
BLOOD      = (170, 25, 35)


# ===========================================================================
# FIXES: beanie, halo, laurel_crown, devil_horns
# ===========================================================================

def beanie(canvas, color="red"):
    """Knit beanie covering the top of the head, cuff brim, pom-pom on top.

    Cap body rows 3..9, cols 14..33. Cuff brim rows 8..9. Knit ribs across.
    """
    pal = {
        "red":    (RED,    RED_HI,    RED_DARK),
        "navy":   (NAVY,   NAVY_HI,   NAVY_DARK),
        "green":  (GREEN,  GREEN_HI,  GREEN_DARK),
        "yellow": (YELLOW, YELLOW_HI, YELLOW_DARK),
    }
    base, hi, dark = pal[color]

    # Dome shape: narrower at top, full at bottom.
    # Row by row width, anchored so it sits on the head.
    rows = {
        3:  (19, 28),
        4:  (17, 30),
        5:  (15, 32),
        6:  (14, 33),
        7:  (14, 33),
        8:  (14, 33),
        9:  (14, 33),
    }
    for y, (x0, x1) in rows.items():
        fill_rect(canvas, x0, y, x1, y, base)

    # Top-left highlight curve on dome.
    for (x, y) in [(20, 3), (18, 4), (16, 5), (15, 6), (14, 7), (14, 8)]:
        put(canvas, x, y, hi)
    # Right-side shadow curve.
    for (x, y) in [(28, 3), (30, 4), (32, 5), (33, 6), (33, 7)]:
        put(canvas, x, y, dark)

    # Knit rib texture: vertical dotted columns across mid rows.
    for y in (4, 6):
        x0, x1 = rows[y]
        for x in range(x0 + 1, x1, 3):
            put(canvas, x, y, mix(base, dark, 0.45))
    # Secondary purl row.
    for x in range(15, 33, 3):
        put(canvas, x, 7, mix(base, hi, 0.35))

    # Cuff brim (folded, slightly darker, two rows tall).
    fill_rect(canvas, 14, 8, 33, 9, dark)
    # Cuff ribbing (vertical lines).
    for x in range(15, 34, 2):
        put(canvas, x, 8, mix(dark, BLACK, 0.3))
        put(canvas, x, 9, mix(dark, BLACK, 0.5))
    # Cuff top highlight edge.
    for x in range(14, 34):
        put(canvas, x, 8, mix(dark, hi, 0.25)) if x % 2 == 0 else None

    # Pom-pom on top, fluffy cluster.
    pom_pixels = [
        (23, 0), (24, 0),
        (22, 1), (23, 1), (24, 1), (25, 1),
        (22, 2), (23, 2), (24, 2), (25, 2),
        (23, 3), (24, 3),
    ]
    for (x, y) in pom_pixels:
        put(canvas, x, y, hi)
    # Pom highlights and shadow.
    put(canvas, 22, 1, WHITE)
    put(canvas, 23, 0, WHITE)
    put(canvas, 25, 2, mix(hi, dark, 0.4))
    put(canvas, 24, 3, mix(hi, dark, 0.5))


def halo(canvas, color="gold"):
    """Floating ring above the head, thicker and gradient-shaded."""
    if color == "gold":
        base, hi, dark = GOLD, GOLD_LIGHT, GOLD_DARK
    else:
        base, hi, dark = (0, 220, 255), (200, 255, 255), (0, 110, 150)

    cx, cy = 24, 3
    rx_out, ry_out = 11, 3.0
    rx_in,  ry_in  = 8,  1.6

    # Fill the elliptical ring with mid tone.
    for y in range(0, 7):
        for x in range(10, 39):
            dx = (x - cx) / rx_out
            dy = (y - cy) / ry_out
            outer = dx * dx + dy * dy
            dxi = (x - cx) / rx_in
            dyi = (y - cy) / ry_in
            inner = dxi * dxi + dyi * dyi
            if outer <= 1.0 and inner >= 1.0:
                # Position-based shading: top brighter, bottom darker.
                if y <= cy - 1:
                    put(canvas, x, y, hi)
                elif y >= cy + 1:
                    put(canvas, x, y, dark)
                else:
                    put(canvas, x, y, base)

    # Inner specular dashes for that polished gold gleam.
    for ang_deg in (200, 215, 230):
        ang = math.radians(ang_deg)
        x = int(cx + math.cos(ang) * 9.5)
        y = int(cy + math.sin(ang) * 2.2)
        put(canvas, x, y, WHITE)
    # Soft outer glow dots.
    for ang_deg in range(0, 360, 24):
        ang = math.radians(ang_deg)
        x = int(cx + math.cos(ang) * (rx_out + 0.6))
        y = int(cy + math.sin(ang) * (ry_out + 0.3))
        put(canvas, x, y, hi, alpha=110)


def laurel_crown(canvas, color="gold"):
    """Roman wreath. Six leaves per side, each a 3-pixel mini leaf with stem.

    Red berries cluster across the brow center.
    """
    if color == "green":
        leaf_dark = (55, 110, 45)
        leaf_mid  = (95, 175, 75)
        leaf_hi   = (160, 230, 120)
        stem      = (70, 95, 50)
    else:
        leaf_dark = GOLD_DARK
        leaf_mid  = GOLD
        leaf_hi   = GOLD_LIGHT
        stem      = (140, 100, 30)

    # Each leaf: (tip_x, tip_y, direction) where direction is "left" or "right".
    # Leaves on the left half angle up-left, leaves on the right half angle up-right.
    left_leaves = [
        (12,  9, "left"),
        (12,  7, "left"),
        (14,  5, "left"),
        (17,  4, "left"),
        (20,  3, "left"),
        (22,  3, "left"),
    ]
    right_leaves = [
        (35,  9, "right"),
        (35,  7, "right"),
        (33,  5, "right"),
        (30,  4, "right"),
        (27,  3, "right"),
        (25,  3, "right"),
    ]

    def draw_leaf(tip_x, tip_y, direction):
        # A 3-pixel leaf body plus a stem pixel.
        if direction == "left":
            # Leaf points up-left.
            body = [
                (tip_x,     tip_y),
                (tip_x + 1, tip_y),
                (tip_x + 1, tip_y + 1),
                (tip_x + 2, tip_y + 1),
            ]
            tip = (tip_x, tip_y)
            shade = (tip_x + 2, tip_y + 1)
            stem_px = (tip_x + 3, tip_y + 2)
        else:
            body = [
                (tip_x,     tip_y),
                (tip_x - 1, tip_y),
                (tip_x - 1, tip_y + 1),
                (tip_x - 2, tip_y + 1),
            ]
            tip = (tip_x, tip_y)
            shade = (tip_x - 2, tip_y + 1)
            stem_px = (tip_x - 3, tip_y + 2)
        for (x, y) in body:
            put(canvas, x, y, leaf_mid)
        put(canvas, tip[0], tip[1], leaf_hi)
        put(canvas, shade[0], shade[1], leaf_dark)
        put(canvas, stem_px[0], stem_px[1], stem)

    for (x, y, d) in left_leaves:
        draw_leaf(x, y, d)
    for (x, y, d) in right_leaves:
        draw_leaf(x, y, d)

    # Berry cluster at center brow (3 berries with shading).
    berries = [(22, 4), (24, 4), (26, 4)]
    for (bx, by) in berries:
        put(canvas, bx, by, BLOOD)
        put(canvas, bx, by - 1, mix(BLOOD, WHITE, 0.4))
        put(canvas, bx + 1, by, mix(BLOOD, BLACK, 0.4))


def devil_horns(canvas, color="red"):
    """Two prominent horns curving out then up to a sharp point.

    Rows 1..7, each horn 4..5 pixels wide at base, tapering to a single tip.
    """
    if color == "red":
        base, hi, dark = (190, 30, 40), (240, 95, 105), (115, 12, 22)
    else:
        base, hi, dark = (45, 38, 32), (95, 85, 75), (22, 18, 14)

    # ----- Left horn -----
    # Base flares out from forehead, curves up and inward (no, outward then up).
    # Use coords to build a thick crescent.
    left = [
        # Base (widest at the head).
        (15, 7), (16, 7), (17, 7), (18, 7),
        (14, 6), (15, 6), (16, 6), (17, 6),
        (13, 5), (14, 5), (15, 5), (16, 5),
        # Curve up-left.
        (13, 4), (14, 4), (15, 4),
        (14, 3), (15, 3),
        (15, 2),
        # Tip.
        (16, 1),
    ]
    for (x, y) in left:
        put(canvas, x, y, base)
    # Highlights on inner-front of left horn.
    for (x, y) in [(15, 6), (14, 5), (14, 4), (15, 3), (15, 2)]:
        put(canvas, x, y, hi)
    # Shadow on outer back edge.
    for (x, y) in [(13, 5), (13, 4), (17, 7), (18, 7)]:
        put(canvas, x, y, dark)
    # Sharp tip pixel.
    put(canvas, 16, 1, hi)
    put(canvas, 16, 0, dark)

    # ----- Right horn (mirror) -----
    right = [
        (29, 7), (30, 7), (31, 7), (32, 7),
        (30, 6), (31, 6), (32, 6), (33, 6),
        (31, 5), (32, 5), (33, 5), (34, 5),
        (32, 4), (33, 4), (34, 4),
        (32, 3), (33, 3),
        (32, 2),
        (31, 1),
    ]
    for (x, y) in right:
        put(canvas, x, y, base)
    for (x, y) in [(32, 6), (33, 5), (33, 4), (32, 3), (32, 2)]:
        put(canvas, x, y, hi)
    for (x, y) in [(34, 5), (34, 4), (30, 7), (29, 7)]:
        put(canvas, x, y, dark)
    put(canvas, 31, 1, hi)
    put(canvas, 31, 0, dark)


# ===========================================================================
# NEW: helmets, caps, durag, headband
# ===========================================================================

def spartan_helmet(canvas, color="bronze"):
    """Bronze hoplite helmet with a red mohawk crest and nose guard."""
    base, hi, dark = BRONZE, BRONZE_HI, BRONZE_LO
    crest_base, crest_hi, crest_dark = RED, RED_HI, RED_DARK

    # Helmet dome (covers top and sides of head).
    fill_rect(canvas, 14, 7, 33, 18, base)
    fill_rect(canvas, 15, 6, 32, 6, base)
    fill_rect(canvas, 16, 5, 31, 5, base)
    fill_rect(canvas, 17, 4, 30, 4, base)

    # Top highlight on left dome.
    for (x, y) in [(17, 4), (16, 5), (15, 6), (14, 7), (14, 8), (14, 9)]:
        put(canvas, x, y, hi)
    fill_rect(canvas, 17, 7, 22, 7, mix(base, hi, 0.4))
    # Bottom rim shadow.
    fill_rect(canvas, 14, 18, 33, 18, dark)
    fill_rect(canvas, 33, 9, 33, 17, dark)

    # Eye openings: carve out around eyes.
    # Spartan-style: keep nose guard down the center, big almond eye slits.
    # Clear the eye area (rows 19..23) by NOT painting brow band there.
    # The helmet brow rim goes from row 16..18 above the eyes.
    fill_rect(canvas, 14, 16, 33, 17, mix(base, dark, 0.5))
    fill_rect(canvas, 14, 18, 33, 18, dark)

    # Nose guard (vertical bronze strip down center).
    fill_rect(canvas, 23, 18, 24, 28, base)
    put(canvas, 23, 18, hi)
    put(canvas, 24, 28, dark)
    fill_rect(canvas, 24, 19, 24, 27, dark)

    # Cheek guards down sides (curve down past brow).
    fill_rect(canvas, 14, 19, 15, 25, base)
    fill_rect(canvas, 32, 19, 33, 25, base)
    put(canvas, 14, 25, dark); put(canvas, 33, 25, dark)
    put(canvas, 14, 19, hi);   put(canvas, 33, 19, mix(base, hi, 0.4))

    # Mohawk crest: red strip front-to-back along the top.
    # Front of crest sits on row 0..4, runs back down the dome.
    crest_cols = list(range(19, 30))  # crest base columns
    # Tall crest pixels above the dome.
    for x in crest_cols:
        put(canvas, x, 3, crest_base)
        put(canvas, x, 2, crest_base)
        put(canvas, x, 1, crest_base)
    for x in (20, 23, 26, 28):
        put(canvas, x, 0, crest_base)
    # Crest highlights along front edge.
    for x in crest_cols:
        put(canvas, x, 1, crest_hi)
    put(canvas, 19, 2, crest_dark)
    put(canvas, 29, 2, crest_dark)
    # Crest base attaches to helmet (mounting strip).
    fill_rect(canvas, 19, 4, 29, 4, crest_dark)

    # Decorative rivet line across brow.
    for x in (16, 20, 24, 28, 31):
        put(canvas, x, 17, hi)


def motorcycle_helmet(canvas, color="black"):
    """Full-face helmet with dark visor across the eyes, glossy curve."""
    pal = {
        "black": ((25, 28, 35),  (75, 80, 95),  (8, 10, 14)),
        "red":   (RED,           RED_HI,        RED_DARK),
        "white": ((235, 235, 240),(255, 255, 255),(160, 160, 170)),
    }
    base, hi, dark = pal[color]

    # Helmet shell (covers head, top to chin).
    fill_rect(canvas, 14, 9, 33, 35, base)
    fill_rect(canvas, 15, 8, 32, 8, base)
    fill_rect(canvas, 16, 7, 31, 7, base)
    fill_rect(canvas, 17, 6, 30, 6, base)
    fill_rect(canvas, 18, 5, 29, 5, base)
    # Chin contour.
    fill_rect(canvas, 16, 36, 31, 36, base)
    fill_rect(canvas, 18, 37, 29, 37, dark)

    # Glossy curve highlight across the top.
    for (x, y) in [(20, 5), (18, 6), (17, 7), (16, 8), (15, 9), (14, 10), (14, 11), (14, 12)]:
        put(canvas, x, y, hi)
    fill_rect(canvas, 19, 6, 25, 6, mix(base, hi, 0.35))
    # Side and bottom shadow.
    for y in range(10, 35):
        put(canvas, 33, y, dark)
    fill_rect(canvas, 14, 35, 33, 35, dark)

    # Visor recess (dark band across eyes, rows 19..24).
    fill_rect(canvas, 14, 19, 33, 25, (10, 12, 18))
    # Visor glass (smoked dark blue).
    fill_rect(canvas, 15, 20, 32, 24, (18, 22, 38))
    # Visor reflective gradient.
    for x in range(15, 33):
        put(canvas, x, 20, (40, 50, 75))
    # Diagonal shine streak on visor.
    for (x, y) in [(18, 23), (19, 22), (20, 21), (21, 20)]:
        put(canvas, x, y, (130, 160, 200))
    for (x, y) in [(25, 23), (26, 22), (27, 21)]:
        put(canvas, x, y, (90, 110, 150))
    # Visor frame trim.
    fill_rect(canvas, 14, 19, 33, 19, dark)
    fill_rect(canvas, 14, 25, 33, 25, dark)

    # Mouth vent (horizontal slats below visor).
    fill_rect(canvas, 19, 31, 28, 33, dark)
    for x in range(20, 28, 2):
        put(canvas, x, 32, mix(dark, BLACK, 0.5))


def baseball_cap(canvas, color="red"):
    """Forward-facing ball cap with curved brim."""
    pal = {
        "red":   (RED,    RED_HI,    RED_DARK),
        "navy":  (NAVY,   NAVY_HI,   NAVY_DARK),
        "white": ((235, 235, 240), (255, 255, 255), (160, 160, 170)),
    }
    base, hi, dark = pal[color]

    # Crown (cap body): rows 4..10, dome shape.
    crown_rows = {
        4:  (20, 27),
        5:  (18, 29),
        6:  (16, 31),
        7:  (15, 32),
        8:  (14, 33),
        9:  (14, 33),
        10: (14, 33),
    }
    for y, (x0, x1) in crown_rows.items():
        fill_rect(canvas, x0, y, x1, y, base)

    # Crown panels (stitched seam line down the front center).
    for y in range(4, 10):
        put(canvas, 24, y, mix(base, dark, 0.35))

    # Highlight on left-front of crown.
    for (x, y) in [(21, 4), (19, 5), (17, 6), (16, 7), (15, 8), (14, 9), (14, 10)]:
        put(canvas, x, y, hi)
    # Right-back shadow.
    for (x, y) in [(27, 4), (29, 5), (31, 6), (32, 7), (33, 8), (33, 9), (33, 10)]:
        put(canvas, x, y, dark)

    # Front panel button on top.
    put(canvas, 24, 3, base)
    put(canvas, 24, 3, hi)

    # Brim: curved shadow extending forward (rows 11..13, wider).
    fill_rect(canvas, 14, 11, 34, 11, base)
    fill_rect(canvas, 13, 12, 35, 12, dark)
    # Brim tip (slight curve down at edges).
    put(canvas, 12, 13, dark)
    put(canvas, 36, 13, dark)
    fill_rect(canvas, 14, 13, 34, 13, mix(dark, BLACK, 0.4))
    # Brim under-shadow on face.
    for x in range(15, 34):
        existing = canvas.getpixel((x, 14))
        if existing[3] > 0:
            r, g, b, a = existing
            put(canvas, x, 14, (max(r - 40, 0), max(g - 40, 0), max(b - 40, 0)), a)

    # Logo patch (small contrasting square front center).
    logo = WHITE if color != "white" else NAVY
    fill_rect(canvas, 23, 7, 25, 9, logo)
    put(canvas, 24, 8, mix(logo, BLACK, 0.4))


def durag(canvas, color="black"):
    """Silk durag covering the top of head with two streamer tails down the side."""
    pal = {
        "black": ((25, 25, 30),  (75, 78, 90),  (8, 8, 12)),
        "red":   (RED,           RED_HI,        RED_DARK),
        "blue":  (SILK_BLUE,     SILK_BLUE_HI,  SILK_BLUE_LO),
    }
    base, hi, dark = pal[color]

    # Cap section covers top and back of head: rows 3..14.
    rows = {
        3:  (20, 27),
        4:  (18, 29),
        5:  (16, 31),
        6:  (15, 32),
        7:  (14, 33),
        8:  (14, 33),
        9:  (14, 33),
        10: (14, 33),
        11: (14, 33),
        12: (14, 33),
        13: (14, 33),
        14: (14, 33),
    }
    for y, (x0, x1) in rows.items():
        fill_rect(canvas, x0, y, x1, y, base)

    # Silk sheen: long diagonal highlights down the left front.
    for (x, y) in [(21, 4), (20, 5), (19, 6), (18, 7), (17, 8), (17, 9),
                   (18, 10), (19, 11), (20, 12), (21, 13)]:
        put(canvas, x, y, hi)
    # Secondary sheen streak.
    for (x, y) in [(25, 4), (24, 5), (23, 6), (22, 7), (22, 8)]:
        put(canvas, x, y, mix(base, hi, 0.5))
    # Right-side shadow fold.
    for y in range(6, 15):
        put(canvas, 33, y, dark)
    for (x, y) in [(31, 5), (32, 6), (32, 7), (33, 8)]:
        put(canvas, x, y, dark)

    # Tie knot at the back-left (cluster of folded fabric).
    fill_rect(canvas, 14, 15, 16, 17, base)
    put(canvas, 14, 15, hi)
    put(canvas, 16, 17, dark)
    put(canvas, 15, 16, mix(base, hi, 0.5))

    # Two streamer tails hanging down on the left side.
    # Tail 1 (upper, longer).
    tail1 = [
        (13, 17), (12, 18), (12, 19), (11, 20), (11, 21),
        (10, 22), (10, 23), (10, 24), (11, 25), (11, 26),
        (12, 27), (12, 28),
    ]
    for (x, y) in tail1:
        put(canvas, x, y, base)
    # Tail 1 silk highlight.
    for (x, y) in [(12, 18), (11, 20), (10, 23), (11, 26)]:
        put(canvas, x, y, hi)
    # Tail 1 shadow side.
    for (x, y) in [(13, 17), (12, 19), (11, 21), (10, 24), (12, 27)]:
        put(canvas, x, y, dark)

    # Tail 2 (lower, shorter, slightly behind).
    tail2 = [
        (14, 18), (13, 19), (13, 20), (14, 21), (14, 22),
        (13, 23), (13, 24), (14, 25),
    ]
    for (x, y) in tail2:
        put(canvas, x, y, mix(base, dark, 0.3))
    for (x, y) in [(13, 19), (14, 21), (13, 23)]:
        put(canvas, x, y, mix(base, hi, 0.3))


def knight_helmet(canvas, color="steel"):
    """Steel medieval helm with horizontal eye slit and gleaming rivets."""
    base, hi, dark = STEEL, STEEL_HI, STEEL_LO

    # Helmet shell (covers full head down to chin).
    fill_rect(canvas, 14, 8, 33, 36, base)
    fill_rect(canvas, 15, 7, 32, 7, base)
    fill_rect(canvas, 16, 6, 31, 6, base)
    fill_rect(canvas, 17, 5, 30, 5, base)
    fill_rect(canvas, 18, 4, 29, 4, base)
    fill_rect(canvas, 20, 3, 27, 3, base)

    # Top dome highlight curve.
    for (x, y) in [(20, 3), (18, 4), (17, 5), (16, 6), (15, 7), (14, 8),
                   (14, 9), (14, 10), (14, 11), (14, 12)]:
        put(canvas, x, y, hi)
    fill_rect(canvas, 20, 4, 25, 4, mix(base, hi, 0.4))
    # Right edge shadow.
    for y in range(8, 36):
        put(canvas, 33, y, dark)
    for (x, y) in [(29, 4), (30, 5), (31, 6), (32, 7)]:
        put(canvas, x, y, dark)

    # Vertical crest ridge down center top.
    for y in range(3, 18):
        put(canvas, 24, y, hi)
    put(canvas, 24, 3, WHITE)

    # Eye slit: horizontal dark band across rows 21..22, cols 16..31.
    fill_rect(canvas, 16, 20, 31, 23, dark)
    fill_rect(canvas, 17, 21, 30, 22, BLACK)
    # Slit upper and lower lip (raised metal).
    for x in range(16, 32):
        put(canvas, x, 20, hi)
        put(canvas, x, 23, mix(base, dark, 0.6))

    # Breathing holes (small dark dots low on the face).
    for x in (20, 22, 26, 28):
        put(canvas, x, 30, BLACK)
        put(canvas, x, 30, mix(base, BLACK, 0.7))
    for x in (21, 25, 27):
        put(canvas, x, 32, mix(base, BLACK, 0.7))

    # Rivets along the brow and jawline.
    rivets = [(16, 18), (20, 18), (24, 18), (28, 18), (31, 18),
              (16, 26), (31, 26),
              (17, 34), (24, 34), (30, 34)]
    for (x, y) in rivets:
        put(canvas, x, y, hi)
        put(canvas, x, y + 1, dark) if y + 1 < 48 else None

    # Chin guard line.
    fill_rect(canvas, 14, 35, 33, 35, dark)
    fill_rect(canvas, 15, 36, 32, 36, mix(base, dark, 0.4))


def crown_of_thorns(canvas, color=None):
    """Woven dark thorny ring around the head with barbs and tiny blood drops."""
    base, hi, dark = THORN, THORN_HI, THORN_LO

    # Woven band around the forehead, rows 11..14.
    band_pts = []
    for x in range(14, 34):
        band_pts.append((x, 12))
        band_pts.append((x, 13))
    for (x, y) in band_pts:
        put(canvas, x, y, base)

    # Woven weave (alternating shaded segments).
    for x in range(14, 34):
        if (x // 2) % 2 == 0:
            put(canvas, x, 12, mix(base, hi, 0.4))
            put(canvas, x, 13, dark)
        else:
            put(canvas, x, 12, dark)
            put(canvas, x, 13, mix(base, hi, 0.3))

    # Vertical interlace strands.
    for x in (15, 18, 21, 24, 27, 30, 33):
        put(canvas, x, 11, base)
        put(canvas, x, 14, base)
    for x in (16, 19, 22, 25, 28, 31):
        put(canvas, x, 11, dark)
        put(canvas, x, 14, dark)

    # Sharp barbs sticking outward and upward.
    barbs_up = [
        (14, 10), (17, 9), (20, 10), (23, 8), (26, 9), (29, 10), (32, 8),
    ]
    for (x, y) in barbs_up:
        put(canvas, x, y, base)
        put(canvas, x, y - 1, hi)
        # Side roots.
        put(canvas, x - 1, y, dark) if x - 1 >= 0 else None
        put(canvas, x + 1, y, dark) if x + 1 < 48 else None

    # Side-pointing barbs.
    put(canvas, 13, 12, base); put(canvas, 12, 12, hi)
    put(canvas, 13, 13, dark)
    put(canvas, 34, 12, base); put(canvas, 35, 12, hi)
    put(canvas, 34, 13, dark)

    # Downward barb under brow.
    put(canvas, 18, 15, base); put(canvas, 18, 16, hi)
    put(canvas, 30, 15, base); put(canvas, 30, 16, hi)

    # Tiny blood drops.
    drops = [(17, 17), (29, 17), (23, 15)]
    for (x, y) in drops:
        put(canvas, x, y, BLOOD)
        put(canvas, x, y + 1, mix(BLOOD, BLACK, 0.5))


def viking_helmet(canvas, color="silver"):
    """Iron helmet with two curved horns coming out the sides."""
    pal = {
        "silver": (SILVER, SILVER_HI, SILVER_LO),
        "bronze": (BRONZE, BRONZE_HI, BRONZE_LO),
    }
    base, hi, dark = pal[color]

    # Helmet dome rows 3..12.
    dome = {
        3:  (22, 25),
        4:  (20, 27),
        5:  (18, 29),
        6:  (17, 30),
        7:  (16, 31),
        8:  (15, 32),
        9:  (14, 33),
        10: (14, 33),
        11: (14, 33),
        12: (14, 33),
    }
    for y, (x0, x1) in dome.items():
        fill_rect(canvas, x0, y, x1, y, base)

    # Top dome highlight (left-front).
    for (x, y) in [(22, 3), (20, 4), (18, 5), (17, 6), (16, 7), (15, 8), (14, 9), (14, 10)]:
        put(canvas, x, y, hi)
    # Shadow side.
    for (x, y) in [(25, 3), (27, 4), (29, 5), (30, 6), (31, 7), (32, 8), (33, 9), (33, 10), (33, 11)]:
        put(canvas, x, y, dark)

    # Central crest ridge (vertical stripe).
    for y in range(3, 13):
        put(canvas, 23, y, hi) if y % 2 == 0 else put(canvas, 24, y, dark)

    # Brow rim band.
    fill_rect(canvas, 14, 12, 33, 13, mix(base, dark, 0.45))
    fill_rect(canvas, 14, 13, 33, 13, dark)

    # Nose guard (short).
    fill_rect(canvas, 23, 14, 24, 19, base)
    put(canvas, 23, 14, hi); put(canvas, 24, 19, dark)

    # Rivets across brow.
    for x in (16, 20, 24, 28, 32):
        put(canvas, x, 12, hi)

    # ----- Left horn (curved out and up) -----
    bone_base = (240, 230, 200)
    bone_hi   = (255, 250, 230)
    bone_dark = (170, 150, 110)
    left_horn = [
        (12, 9), (11, 9), (10, 9),
        (10, 8), (9, 8), (9, 7),
        (9, 6),  (10, 6), (10, 5),
        (11, 4), (11, 3),
    ]
    for (x, y) in left_horn:
        put(canvas, x, y, bone_base)
    for (x, y) in [(9, 8), (9, 7), (10, 6), (10, 5), (11, 4)]:
        put(canvas, x, y, bone_hi)
    for (x, y) in [(12, 9), (10, 9), (9, 6), (11, 3)]:
        put(canvas, x, y, bone_dark)
    # Tip.
    put(canvas, 11, 2, bone_hi)
    put(canvas, 12, 3, bone_dark)
    # Mount band where horn meets helmet.
    put(canvas, 13, 9, dark); put(canvas, 13, 10, dark)

    # ----- Right horn (mirror) -----
    right_horn = [
        (35, 9), (36, 9), (37, 9),
        (37, 8), (38, 8), (38, 7),
        (38, 6), (37, 6), (37, 5),
        (36, 4), (36, 3),
    ]
    for (x, y) in right_horn:
        put(canvas, x, y, bone_base)
    for (x, y) in [(38, 8), (38, 7), (37, 6), (37, 5), (36, 4)]:
        put(canvas, x, y, bone_hi)
    for (x, y) in [(35, 9), (37, 9), (38, 6), (36, 3)]:
        put(canvas, x, y, bone_dark)
    put(canvas, 36, 2, bone_hi)
    put(canvas, 35, 3, bone_dark)
    put(canvas, 34, 9, dark); put(canvas, 34, 10, dark)


def headband(canvas, color="red"):
    """Athletic headband across the forehead just above the brow."""
    pal = {
        "red":   (RED,    RED_HI,    RED_DARK),
        "white": ((235, 235, 240), (255, 255, 255), (160, 160, 170)),
        "black": ((25, 25, 30),    (75, 78, 90),    (8, 8, 12)),
    }
    base, hi, dark = pal[color]

    # Band wraps around forehead rows 15..17.
    # Sits below the typical hairline and above the brow (row 19).
    fill_rect(canvas, 14, 15, 33, 17, base)

    # Top highlight strip.
    fill_rect(canvas, 14, 15, 33, 15, hi)
    # Bottom shadow strip.
    fill_rect(canvas, 14, 17, 33, 17, dark)

    # Side wrap pixels (curves around the head edges).
    put(canvas, 13, 16, base); put(canvas, 34, 16, base)
    put(canvas, 13, 15, hi);   put(canvas, 34, 15, mix(base, hi, 0.4))
    put(canvas, 13, 17, dark); put(canvas, 34, 17, dark)

    # Fabric texture: subtle ribbed lines.
    for x in range(15, 33, 3):
        put(canvas, x, 16, mix(base, hi, 0.3))

    # Small contrasting logo center.
    if color == "white":
        logo, logo_shade = RED, RED_DARK
    elif color == "red":
        logo, logo_shade = WHITE, (200, 200, 210)
    else:
        logo, logo_shade = (240, 200, 60), (180, 140, 30)
    fill_rect(canvas, 23, 16, 25, 16, logo)
    put(canvas, 24, 16, logo_shade)


# === REGISTRY ===

ACCESSORIES_HEAD_V2 = {
    "beanie":            (beanie,            ["red", "navy", "green", "yellow"]),
    "halo":              (halo,              ["gold", "cyan"]),
    "laurel_crown":      (laurel_crown,      ["gold", "green"]),
    "devil_horns":       (devil_horns,       ["red", "black"]),
    "spartan_helmet":    (spartan_helmet,    ["bronze"]),
    "motorcycle_helmet": (motorcycle_helmet, ["black", "red", "white"]),
    "baseball_cap":      (baseball_cap,      ["red", "navy", "white"]),
    "durag":             (durag,             ["black", "red", "blue"]),
    "knight_helmet":     (knight_helmet,     ["steel"]),
    "crown_of_thorns":   (crown_of_thorns,   [None]),
    "viking_helmet":     (viking_helmet,     ["silver", "bronze"]),
    "headband":          (headband,          ["red", "white", "black"]),
}


if __name__ == "__main__":
    import pathlib
    from face_template import draw_face_template

    out = pathlib.Path("public/variants/_head_v2_smoke")
    out.mkdir(parents=True, exist_ok=True)
    for name, (fn, colors) in ACCESSORIES_HEAD_V2.items():
        c = new_canvas()
        draw_face_template(c)
        first = colors[0]
        try:
            if first is None:
                fn(c)
            else:
                fn(c, color=first)
        except TypeError:
            fn(c)
        c.save(out / f"{name}.png")
    print(f"wrote {len(ACCESSORIES_HEAD_V2)} head v2 accessory smoke tests to {out}")
