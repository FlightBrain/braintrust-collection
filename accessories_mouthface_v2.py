#!/usr/bin/env python3
"""Mouth + face accessories, v2.

Overrides the weak FACE entries in accessories_v3.py (scar, face_tattoo,
mustache_handlebar, blush) and adds new mouth/face items at NFT grade.

All items sit on the face_template canvas (48x48). Mouth anchor row 31..32,
nose tip col 24 row 26, cheeks rows 24..27, jaw rows 33..36.

Style rules followed:
  * 3-tone shading per item (shadow / mid / highlight).
  * Chunky reads, no 1-pixel flat blobs.
  * No em dashes anywhere in this file.
"""
import math
from items_v3 import new_canvas, put, paint, fill_rect, mix, WHITE, BLACK, GOLD, GOLD_LIGHT, GOLD_DARK


# === Common palettes ===
RED        = (220, 40, 50)
RED_HI     = (255, 110, 120)
RED_LO     = (140, 15, 25)
PINK       = (255, 130, 175)
PINK_HI    = (255, 195, 220)
PINK_LO    = (200, 75, 130)
HOT_PINK   = (255, 50, 140)
HOT_PINK_HI = (255, 150, 200)
HOT_PINK_LO = (170, 20, 90)
PURPLE     = (160, 80, 220)
PURPLE_HI  = (220, 180, 255)
PURPLE_LO  = (90, 40, 140)
BROWN      = (110, 70, 35)
BROWN_HI   = (155, 105, 60)
BROWN_LO   = (70, 40, 15)
SKIN_DARK  = (210, 165, 130)
SMOKE      = (200, 200, 215)


# ===========================================================================
# FIXES: override weak existing items
# ===========================================================================

def scar(canvas, color=None):
    """Big dramatic diagonal scar.

    Runs from above the right eye (col 28 row 17) down to the right cheek
    (col 32 row 28). Thick main line, darker shadow outline, cross stitches
    every 2 rows.
    """
    base   = (210, 130, 120)
    hi     = (240, 175, 165)
    shadow = (140, 70, 65)
    # Main diagonal path, sampled every row from 17 to 28.
    # dx/dy = 4/11, so add roughly 1 col every 3 rows.
    path = []
    for i, y in enumerate(range(17, 29)):
        x = 28 + round(i * (4 / 11))
        path.append((x, y))
    # Thick line: paint base on path, plus one pixel to the left and right.
    for (x, y) in path:
        put(canvas, x, y, base)
        put(canvas, x + 1, y, base)
        put(canvas, x - 1, y, hi)
        put(canvas, x + 2, y, shadow)
    # Cross stitches every 2 rows, perpendicular to the diagonal.
    for idx, (x, y) in enumerate(path):
        if idx % 2 == 0:
            # Short horizontal stitch crossing the scar.
            put(canvas, x - 2, y, shadow)
            put(canvas, x + 3, y, shadow)
            # A small vertical tick above and below for the stitched look.
            put(canvas, x, y - 1, shadow)
            put(canvas, x + 1, y + 1, shadow)


def face_tattoo(canvas, color="heart"):
    """Readable symbol tattoo under right eye (cols 28..30, rows 23..25)."""
    ink     = (25, 20, 30)
    ink_hi  = (70, 55, 90)
    accent  = RED if color == "heart" else (40, 160, 80) if color == "dollar" else GOLD if color == "star" else (60, 60, 70)

    if color == "heart":
        # 3 wide, 3 tall pixel heart.
        pattern = [
            "#.#",
            "###",
            ".#.",
        ]
        anchor_x, anchor_y = 28, 23
        for ry, row in enumerate(pattern):
            for rx, ch in enumerate(row):
                if ch == "#":
                    put(canvas, anchor_x + rx, anchor_y + ry, RED)
        # Tiny highlight + dark outline below.
        put(canvas, 28, 23, RED_HI)
        put(canvas, 29, 25, RED_LO)

    elif color == "dollar":
        pattern = [
            ".#.",
            "###",
            "##.",
            "###",
            ".##",
            "###",
            ".#.",
        ]
        anchor_x, anchor_y = 28, 22
        for ry, row in enumerate(pattern):
            for rx, ch in enumerate(row):
                if ch == "#":
                    put(canvas, anchor_x + rx, anchor_y + ry, accent)
        put(canvas, 28, 22, mix(accent, WHITE, 0.5))

    elif color == "star":
        # 5-point star pixel pattern, 3x3 core plus arms.
        put(canvas, 29, 22, accent)
        put(canvas, 28, 23, accent); put(canvas, 29, 23, accent); put(canvas, 30, 23, accent)
        put(canvas, 28, 24, accent); put(canvas, 30, 24, accent)
        # Center bright dot.
        put(canvas, 29, 23, mix(accent, WHITE, 0.5))

    elif color == "cross":
        # Latin cross.
        # Vertical bar
        for y in range(22, 26):
            put(canvas, 29, y, ink)
        # Horizontal bar
        for x in range(28, 31):
            put(canvas, x, 23, ink)
        # Highlight pixel
        put(canvas, 29, 22, ink_hi)


def mustache_handlebar(canvas, color="black"):
    """Proper handlebar: 2px thick, curled-up ends.

    Spans rows 28..30, cols 18..30. Center bar 2px under nose, ends curl up.
    """
    if color == "black":
        base, hi, dark = (35, 28, 22), (75, 60, 50), (15, 10, 5)
    else:
        base, hi, dark = (BROWN, BROWN_HI, BROWN_LO)

    # Center bar (2px thick under the nose).
    fill_rect(canvas, 21, 29, 26, 30, base)
    fill_rect(canvas, 21, 29, 26, 29, hi)
    fill_rect(canvas, 21, 30, 26, 30, dark)

    # Left wing thickening outward.
    fill_rect(canvas, 19, 29, 20, 30, base)
    put(canvas, 19, 29, hi)
    # Left curl up: cols 18..19, rows 28..29.
    put(canvas, 18, 29, base)
    put(canvas, 18, 28, base)
    put(canvas, 19, 28, hi)

    # Right wing thickening outward.
    fill_rect(canvas, 27, 29, 28, 30, base)
    put(canvas, 28, 29, hi)
    # Right curl up.
    put(canvas, 29, 29, base)
    put(canvas, 29, 28, base)
    put(canvas, 28, 28, hi)

    # Shadow on lip just under the bar for depth.
    put(canvas, 22, 30, dark); put(canvas, 25, 30, dark)


def blush(canvas, color="pink"):
    """Soft circular fade pink blush on both cheeks."""
    if color == "red":
        c = (255, 110, 110)
    else:
        c = (255, 150, 180)
    # Each cheek: 3x3 footprint with falloff via alpha.
    centers = [(16, 26), (32, 26)]
    for (cx, cy) in centers:
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                d2 = dx * dx + dy * dy
                if d2 > 5:
                    continue
                x, y = cx + dx, cy + dy
                # Inner = stronger alpha, outer = soft.
                if d2 == 0:
                    a = 200
                elif d2 <= 2:
                    a = 150
                elif d2 <= 4:
                    a = 95
                else:
                    a = 55
                put(canvas, x, y, c, alpha=a)


# ===========================================================================
# NEW: mouth + face items
# ===========================================================================

def pipe_sherlock(canvas, color=None):
    """Curved tobacco pipe out the right side of mouth with smoke wisp."""
    body    = (90, 55, 30)
    body_hi = (135, 85, 50)
    body_lo = (55, 30, 12)
    stem_hi = (160, 110, 70)
    ember   = (255, 110, 30)

    # Stem: from mouth corner (col 26 row 31) running right and slightly down.
    # Rows 31..32, cols 26..32.
    fill_rect(canvas, 26, 31, 32, 32, body)
    fill_rect(canvas, 26, 31, 32, 31, stem_hi)
    fill_rect(canvas, 26, 32, 32, 32, body_lo)

    # Curve downward: cols 33..34 drops to row 33..34.
    put(canvas, 33, 32, body); put(canvas, 33, 33, body)
    put(canvas, 34, 33, body); put(canvas, 34, 34, body)
    put(canvas, 33, 33, body_hi)

    # Bowl: rows 32..35, cols 34..36 (chunky cup).
    fill_rect(canvas, 34, 33, 36, 35, body)
    fill_rect(canvas, 34, 33, 34, 35, body_hi)
    fill_rect(canvas, 36, 33, 36, 35, body_lo)
    fill_rect(canvas, 34, 35, 36, 35, body_lo)
    # Bowl rim (top of cup).
    fill_rect(canvas, 34, 32, 36, 32, body_hi)

    # Glowing ember inside the bowl.
    put(canvas, 35, 33, ember)
    put(canvas, 35, 33, mix(ember, WHITE, 0.3))
    put(canvas, 34, 33, mix(ember, body_lo, 0.5))
    put(canvas, 36, 33, mix(ember, body_lo, 0.5))

    # Smoke wisp curling up from the bowl.
    paint(canvas, [(35, 30), (36, 28), (35, 26), (34, 24), (35, 22)], SMOKE, alpha=180)
    paint(canvas, [(36, 29), (35, 27), (34, 25)], SMOKE, alpha=110)


def joint(canvas, color=None):
    """Thin rolled joint out the mouth with a small puff."""
    paper     = (240, 235, 215)
    paper_hi  = WHITE
    paper_lo  = (180, 175, 155)
    ember     = (255, 90, 30)
    ember_hi  = (255, 220, 120)

    # Joint body cols 26..34 row 32 (thin).
    fill_rect(canvas, 26, 32, 34, 32, paper)
    # Lightly twisted tip on the lit end (col 34 row 32 stays plain).
    # Top highlight: a 1px row above for thickness.
    paint(canvas, [(27, 31), (29, 31), (31, 31), (33, 31)], paper_hi, alpha=200)
    # Shadow row below.
    paint(canvas, [(27, 33), (29, 33), (31, 33), (33, 33)], paper_lo, alpha=200)

    # Filter end near mouth (a slightly tan cap).
    fill_rect(canvas, 26, 32, 27, 32, (210, 190, 140))

    # Ember at tip.
    put(canvas, 35, 32, ember)
    put(canvas, 35, 32, ember_hi)
    put(canvas, 34, 32, mix(paper, ember, 0.6))

    # Small puff of smoke up and to the right.
    paint(canvas, [(36, 30), (37, 28), (36, 26)], SMOKE, alpha=170)
    paint(canvas, [(37, 29), (35, 27)], SMOKE, alpha=100)


def gold_tooth_single(canvas, color=None):
    """Single gleaming gold tooth in an otherwise normal smile."""
    # Normal teeth row: paint the rest as off-white for smile context.
    teeth = (245, 240, 225)
    teeth_lo = (180, 175, 160)
    fill_rect(canvas, 20, 31, 27, 32, teeth)
    fill_rect(canvas, 20, 32, 27, 32, teeth_lo)
    # Tooth gaps.
    for x in [22, 25]:
        put(canvas, x, 31, teeth_lo)
        put(canvas, x, 32, mix(teeth_lo, BLACK, 0.3))
    # The gold tooth: cols 23..24, rows 31..32.
    fill_rect(canvas, 23, 31, 24, 32, GOLD)
    put(canvas, 23, 31, GOLD_LIGHT)
    put(canvas, 24, 32, GOLD_DARK)
    # Tiny sparkle on the gold.
    put(canvas, 23, 31, WHITE)


def lipstick(canvas, color="red"):
    """Full bright lips, more prominent than default mouth."""
    palettes = {
        "red":    ((230, 40, 55),  (255, 110, 120), (140, 15, 30)),
        "pink":   ((255, 110, 170), PINK_HI,        PINK_LO),
        "black":  ((30, 25, 35),   (80, 70, 90),    (5, 5, 10)),
        "purple": (PURPLE,         PURPLE_HI,       PURPLE_LO),
    }
    base, hi, dark = palettes[color]

    # Upper lip: cupid's bow.
    # Row 30: thinner upper bow.
    paint(canvas, [(21, 30), (22, 30), (25, 30), (26, 30)], base)
    put(canvas, 23, 30, dark); put(canvas, 24, 30, dark)
    # Row 31: full top lip band.
    fill_rect(canvas, 20, 31, 27, 31, base)
    # Row 32: bottom lip, plumper.
    fill_rect(canvas, 20, 32, 27, 32, base)
    # Row 33: bottom curve, narrower.
    fill_rect(canvas, 21, 33, 26, 33, base)
    paint(canvas, [(22, 33), (25, 33)], dark)

    # Highlight gloss on the bottom lip.
    paint(canvas, [(22, 32), (25, 32)], hi)
    # Corner shadow.
    put(canvas, 20, 31, dark); put(canvas, 27, 31, dark)
    put(canvas, 20, 32, dark); put(canvas, 27, 32, dark)


def kiss_print(canvas, color="red"):
    """Kiss mark on right cheek (cols 30..33, rows 25..27)."""
    if color == "hot_pink":
        c = HOT_PINK
        hi = HOT_PINK_HI
        dark = HOT_PINK_LO
    else:
        c = (230, 40, 60)
        hi = (255, 120, 140)
        dark = (140, 15, 25)

    # Upper lip of the kiss: two small bumps.
    paint(canvas, [(30, 25), (31, 25), (32, 25), (33, 25)], c)
    put(canvas, 31, 24, c); put(canvas, 32, 24, c)
    # Cleft in the middle.
    put(canvas, 31, 25, dark); put(canvas, 32, 25, dark)
    # Bottom lip.
    fill_rect(canvas, 30, 26, 33, 26, c)
    paint(canvas, [(31, 27), (32, 27)], c)
    # Highlight.
    put(canvas, 30, 26, hi)
    put(canvas, 33, 26, dark)
    # Small "smudge" detail.
    put(canvas, 34, 26, c, alpha=150)


def tongue_out(canvas, color=None):
    """Small pink tongue sticking out at the bottom of the mouth."""
    tongue    = (255, 130, 150)
    tongue_hi = (255, 190, 200)
    tongue_lo = (200, 70, 100)
    # Tongue base at rows 32..33, cols 23..25.
    fill_rect(canvas, 23, 32, 25, 33, tongue)
    # Bottom rounded.
    put(canvas, 24, 34, tongue)
    # Highlight along the top.
    fill_rect(canvas, 23, 32, 25, 32, tongue_hi)
    # Shadow on the right edge.
    put(canvas, 25, 33, tongue_lo)
    put(canvas, 24, 34, tongue_lo)
    # Center crease line.
    put(canvas, 24, 33, tongue_lo)


def mustache_chevron(canvas, color="black"):
    """Thick chevron (Tom Selleck) mustache, full coverage under nose."""
    if color == "black":
        base, hi, dark = (30, 22, 18), (70, 55, 45), (10, 7, 5)
    else:
        base, hi, dark = (BROWN, BROWN_HI, BROWN_LO)

    # Main body: rows 28..30, cols 18..30.
    fill_rect(canvas, 18, 28, 30, 30, base)
    # Outer corners angle down (chevron points).
    paint(canvas, [(17, 29), (17, 30), (31, 29), (31, 30)], base)
    paint(canvas, [(16, 30), (32, 30)], base)
    # Inner gap under the nose tip (slight notch at col 24 row 28).
    put(canvas, 24, 28, dark)
    # Highlights across the top edge for hair direction.
    for x in range(18, 31, 2):
        put(canvas, x, 28, hi)
    # Bottom shadow row.
    fill_rect(canvas, 18, 30, 30, 30, dark)
    # Strand texture.
    for x in range(19, 31, 3):
        put(canvas, x, 29, mix(base, dark, 0.5))


def beard_full(canvas, color="black"):
    """Full lumberjack beard covering chin and lower cheeks (rows 30..38)."""
    palettes = {
        "black": ((25, 22, 20),  (60, 55, 50),   (10, 8, 6)),
        "brown": ((BROWN_LO),    BROWN,          (45, 25, 10)),
        "red":   ((150, 70, 30), (200, 110, 60), (90, 35, 10)),
        "white": ((220, 220, 225), WHITE,        (170, 170, 180)),
    }
    base, hi, dark = palettes[color]

    # Wide jaw coverage. Rows 30..36 on the face proper.
    # Top edge feathers from sideburns inward.
    fill_rect(canvas, 14, 30, 33, 30, base)
    fill_rect(canvas, 14, 31, 19, 36, base)
    fill_rect(canvas, 28, 31, 33, 36, base)
    # Lower beard (chin tuft) rows 33..38.
    fill_rect(canvas, 17, 33, 30, 36, base)
    fill_rect(canvas, 18, 37, 29, 38, base)
    # Bottom feathered ends.
    paint(canvas, [(19, 38), (20, 38), (27, 38), (28, 38)], dark)

    # Carve out the mouth opening (rows 31..32, cols 20..27).
    fill_rect(canvas, 20, 31, 27, 31, (180, 110, 95))
    paint(canvas, [(20, 32), (27, 32)], base)

    # Hair texture: scatter shadow + hi pixels.
    for (x, y) in [(15, 32), (17, 34), (19, 35), (22, 35), (25, 35),
                   (29, 34), (31, 32), (16, 31), (32, 31)]:
        put(canvas, x, y, dark)
    for (x, y) in [(16, 33), (20, 34), (24, 36), (27, 34), (30, 33)]:
        put(canvas, x, y, hi)


def goatee(canvas, color="black"):
    """Small chin patch beard, just under the mouth (rows 32..36, cols 22..26)."""
    if color == "black":
        base, hi, dark = (28, 22, 18), (65, 55, 48), (10, 7, 5)
    else:
        base, hi, dark = (BROWN, BROWN_HI, BROWN_LO)

    # Mustache strip under the lip (thin).
    fill_rect(canvas, 22, 32, 25, 32, base)
    # Soul patch directly under mouth.
    fill_rect(canvas, 23, 33, 24, 33, base)
    # Chin patch.
    fill_rect(canvas, 21, 34, 26, 35, base)
    fill_rect(canvas, 22, 36, 25, 36, base)
    # Highlight along the top.
    put(canvas, 23, 32, hi); put(canvas, 24, 32, hi)
    # Bottom edge darker.
    paint(canvas, [(22, 36), (25, 36)], dark)
    paint(canvas, [(21, 35), (26, 35)], dark)


def bubble_gum_bubble(canvas, color=None):
    """Big pink bubble being blown out of the mouth."""
    bubble    = (255, 160, 200)
    bubble_hi = (255, 220, 235)
    bubble_lo = (200, 90, 140)

    # Tiny gum connector at the lips (cols 26..27 row 32).
    put(canvas, 26, 32, bubble_lo)
    put(canvas, 27, 32, bubble)

    # Round bubble centered at (30, 32), radius about 4.
    cx, cy, r = 30, 32, 4
    for y in range(cy - r, cy + r + 1):
        for x in range(cx - r, cx + r + 1):
            d2 = (x - cx) ** 2 + (y - cy) ** 2
            if d2 > r * r:
                continue
            # Edge.
            if d2 > (r - 1) ** 2:
                put(canvas, x, y, bubble_lo)
            else:
                put(canvas, x, y, bubble)
    # Specular highlight top-left.
    put(canvas, cx - 2, cy - 2, bubble_hi)
    put(canvas, cx - 1, cy - 2, WHITE)
    put(canvas, cx - 2, cy - 1, bubble_hi)
    # Inner glow.
    put(canvas, cx - 1, cy - 1, bubble_hi)


def face_paint_war(canvas, color=None):
    """Three black diagonal stripes across each cheek."""
    paint_c = (20, 18, 22)
    paint_hi = (60, 55, 65)
    # Left cheek: 3 diagonal stripes, top-left to bottom-right.
    # Each stripe 2px wide, 4px long.
    for stripe_i, anchor in enumerate([(15, 24), (15, 26), (15, 28)]):
        ax, ay = anchor
        for k in range(4):
            put(canvas, ax + k, ay + k // 2, paint_c)
            put(canvas, ax + k, ay + k // 2 + 1, paint_c)
        # Highlight on top edge.
        put(canvas, ax, ay, paint_hi)

    # Right cheek: 3 diagonal stripes, mirrored (top-right to bottom-left).
    for stripe_i, anchor in enumerate([(33, 24), (33, 26), (33, 28)]):
        ax, ay = anchor
        for k in range(4):
            put(canvas, ax - k, ay + k // 2, paint_c)
            put(canvas, ax - k, ay + k // 2 + 1, paint_c)
        put(canvas, ax, ay, paint_hi)


def freckles(canvas, color=None):
    """Scattered brown freckle dots across nose bridge and cheeks."""
    dot    = (130, 80, 50)
    dot_hi = (170, 115, 75)
    # Bridge of nose.
    spots = [
        (22, 24), (24, 24), (26, 24),
        (23, 25), (25, 25),
        # Left cheek.
        (16, 25), (17, 27), (15, 27), (18, 26), (17, 24),
        # Right cheek.
        (30, 25), (31, 27), (32, 26), (29, 24), (33, 25),
        # Light scatter higher up.
        (20, 23), (28, 23),
    ]
    for (x, y) in spots:
        put(canvas, x, y, dot)
    # A few lighter sub-spots for variety.
    for (x, y) in [(23, 26), (30, 27), (16, 24), (31, 24)]:
        put(canvas, x, y, dot_hi)


def birthmark_star(canvas, color=None):
    """Small dark star-shaped birthmark on left cheek."""
    base = (90, 55, 75)
    hi   = (140, 95, 115)
    dark = (55, 30, 45)
    cx, cy = 16, 27
    # Center.
    put(canvas, cx, cy, base)
    # 4 arms.
    put(canvas, cx, cy - 1, base)
    put(canvas, cx, cy + 1, base)
    put(canvas, cx - 1, cy, base)
    put(canvas, cx + 1, cy, base)
    # Highlight on center.
    put(canvas, cx, cy, hi)
    # Diagonal tips slightly darker (gives 5-point feel).
    put(canvas, cx - 1, cy - 1, dark)
    put(canvas, cx + 1, cy + 1, dark)


# === REGISTRY ===

ACCESSORIES_MOUTHFACE_V2 = {
    "scar":               (scar,               [None]),
    "face_tattoo":        (face_tattoo,        ["heart", "dollar", "star", "cross"]),
    "mustache_handlebar": (mustache_handlebar, ["black", "brown"]),
    "blush":              (blush,              ["pink", "red"]),
    "pipe_sherlock":      (pipe_sherlock,      [None]),
    "joint":              (joint,              [None]),
    "gold_tooth_single":  (gold_tooth_single,  [None]),
    "lipstick":           (lipstick,           ["red", "pink", "black", "purple"]),
    "kiss_print":         (kiss_print,         ["red", "hot_pink"]),
    "tongue_out":         (tongue_out,         [None]),
    "mustache_chevron":   (mustache_chevron,   ["black", "brown"]),
    "beard_full":         (beard_full,         ["black", "brown", "red", "white"]),
    "goatee":             (goatee,             ["black", "brown"]),
    "bubble_gum_bubble":  (bubble_gum_bubble,  [None]),
    "face_paint_war":     (face_paint_war,     [None]),
    "freckles":           (freckles,           [None]),
    "birthmark_star":     (birthmark_star,     [None]),
}


if __name__ == "__main__":
    import pathlib
    from face_template import draw_face_template

    out = pathlib.Path("public/variants/_mouthface_v2_smoke")
    out.mkdir(parents=True, exist_ok=True)
    ok, fail = 0, 0
    for name, (fn, colors) in ACCESSORIES_MOUTHFACE_V2.items():
        try:
            c = new_canvas()
            draw_face_template(c)
            first = colors[0]
            if first is None:
                fn(c)
            else:
                fn(c, color=first)
            c.save(out / f"{name}.png")
            ok += 1
        except Exception as e:
            fail += 1
            print(f"FAIL {name}: {e}")
    print(f"wrote {ok} smoke tests to {out} (failures: {fail})")
