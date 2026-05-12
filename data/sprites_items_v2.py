"""
sprites_items_v2.py

Rewritten sig_* and acc_* sprite functions for 32x32 pixel character canvas.

Each function operates on a PIL Image `canvas` (32x32, RGB). Helpers expected
in the importing module:

    paint(canvas, [(x, y), ...], color)
    fill_rect(canvas, x0, y0, x1, y1, color)
    canvas.putpixel((x, y), color)

Layout reference (mirrors character_builder.py):
    - Hair sits roughly rows 5-10, cols 9-22.
    - Face occupies rows 9-25, cols 10-21.
    - Eyes row 16. Mouth row 23. Ears at cols 9 and 22 rows 16-18.
    - Shirt fills rows 28-31 cols 5-26 (plus row 27 cols 7-24).
    - Floating space above head: rows 0-5, any col.
    - Off-shoulder open space: cols 0-4 and 27-31, rows 9-31 (varies by hair).

Each sprite uses 2-3 tones (main / shadow / highlight) for visual readability
at 32x32, per project art direction.

Functions intentionally keep the same names and signatures as the originals in
character_builder.py so they can be drop-in replaced.
"""

# Shared palette constants (do not import from character_builder to keep this
# module independently importable; values match character_builder.py).
WHITE = (255, 255, 255)
BLACK = (10, 10, 10)
GOLD = (255, 200, 60)
GOLD_DARK = (180, 130, 35)
GOLD_LIGHT = (255, 230, 140)
SILVER = (200, 200, 200)
SILVER_DARK = (130, 140, 150)
SILVER_LIGHT = (240, 245, 250)


# ---- local helpers (so this file is self-contained) -------------------------
def _paint(canvas, pixels, color):
    w, h = canvas.size
    for x, y in pixels:
        if 0 <= x < w and 0 <= y < h:
            canvas.putpixel((x, y), color)


def _fill_rect(canvas, x0, y0, x1, y1, color):
    w, h = canvas.size
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            if 0 <= x < w and 0 <= y < h:
                canvas.putpixel((x, y), color)


def _mix(a, b, t):
    return (
        int(a[0] * (1 - t) + b[0] * t),
        int(a[1] * (1 - t) + b[1] * t),
        int(a[2] * (1 - t) + b[2] * t),
    )


# ============================================================================
# SIGNATURE ITEMS
# ============================================================================

def sig_pocket_square(canvas, color):
    """Small fabric triangle peeking from suit pocket on left chest.

    Lives at rows 27-30 cols 11-13. Looks like a folded square handkerchief.
    """
    shadow = _mix(color, BLACK, 0.45)
    highlight = _mix(color, WHITE, 0.45)
    # Triangular peak of fabric (3 rows tall)
    _paint(canvas, [(11, 28), (12, 28), (13, 28)], color)
    _paint(canvas, [(12, 29), (13, 29)], color)
    _paint(canvas, [(13, 30)], color)
    # Highlight on top edge (fold catches light)
    _paint(canvas, [(11, 28), (12, 28)], highlight)
    # Shadow under fold
    _paint(canvas, [(13, 29), (13, 30)], shadow)


def sig_necklace_gold(canvas):
    """V-shaped gold chain with pendant resting on neck/collarbone.

    Chain dips from cols 12-19 along rows 26-28, pendant centered at row 29.
    """
    # Chain forming a clear V across the neck
    _paint(canvas, [(12, 26), (19, 26)], GOLD_DARK)
    _paint(canvas, [(13, 27), (18, 27)], GOLD)
    _paint(canvas, [(14, 27), (17, 27)], GOLD_LIGHT)
    _paint(canvas, [(14, 28), (17, 28)], GOLD)
    _paint(canvas, [(15, 28), (16, 28)], GOLD_DARK)
    # Pendant teardrop centered below chain
    _paint(canvas, [(15, 29), (16, 29)], GOLD)
    _paint(canvas, [(15, 30), (16, 30)], GOLD_DARK)
    _paint(canvas, [(15, 29)], GOLD_LIGHT)  # highlight


def sig_headset(canvas):
    """Over-ear headset: band across head, earpiece on left ear, mic arm to mouth."""
    band_dark = BLACK
    band = (40, 40, 50)
    accent = (90, 90, 110)
    # Headband arch across top of hair (rows 5-7)
    _paint(canvas, [(11, 7), (12, 6), (13, 5), (14, 5), (15, 5),
                    (16, 5), (17, 5), (18, 5), (19, 6), (20, 7)], band_dark)
    _paint(canvas, [(13, 6), (14, 6), (17, 6), (18, 6)], band)
    # Padded crown highlight
    _paint(canvas, [(15, 5), (16, 5)], accent)
    # Left ear cup (visible over ear at col 9)
    _fill_rect(canvas, 7, 16, 9, 19, band_dark)
    _fill_rect(canvas, 8, 17, 9, 18, band)
    _paint(canvas, [(8, 17)], accent)  # speaker highlight
    # Mic boom arm sweeping toward mouth
    _paint(canvas, [(8, 20), (8, 21), (9, 22), (10, 22), (11, 22)], band_dark)
    _paint(canvas, [(9, 22)], band)
    # Foam mic tip (red wind-cover ball)
    _paint(canvas, [(12, 22)], (220, 60, 60))
    _paint(canvas, [(12, 23)], (160, 30, 30))


def sig_watch(canvas):
    """Square smartwatch on left wrist (cols 1-4, rows 26-31, off-shirt for visibility)."""
    band = (50, 50, 65)
    band_light = (95, 95, 115)
    face = (15, 18, 28)
    glass = (90, 200, 240)
    glass_hi = (210, 240, 255)
    # Band segments (above and below face)
    _paint(canvas, [(1, 26), (2, 26), (3, 26), (4, 26)], band)
    _paint(canvas, [(2, 26), (3, 26)], band_light)
    # Watch case (silver bezel) rows 27-30
    _fill_rect(canvas, 1, 27, 4, 30, SILVER_DARK)
    _paint(canvas, [(1, 27), (4, 27), (1, 30), (4, 30)], SILVER)
    # Watch face screen (rows 28-29 cols 2-3)
    _fill_rect(canvas, 2, 28, 3, 29, face)
    _paint(canvas, [(2, 28)], glass_hi)  # screen highlight
    _paint(canvas, [(3, 29)], glass)
    # Bezel top-left highlight
    _paint(canvas, [(1, 27), (2, 27)], SILVER_LIGHT)
    # Crown/button nub on right side of case
    _paint(canvas, [(5, 28)], band_light)
    # Lower band
    _paint(canvas, [(1, 31), (2, 31), (3, 31), (4, 31)], band)
    _paint(canvas, [(2, 31), (3, 31)], band_light)


def sig_question_mark(canvas, color):
    """Clear, readable '?' floating above the head (rows 0-6, cols 14-18)."""
    highlight = _mix(color, WHITE, 0.5)
    shadow = _mix(color, BLACK, 0.35)
    # Top curve of the ?
    _paint(canvas, [(15, 1), (16, 1), (17, 1)], color)
    _paint(canvas, [(14, 2), (18, 2)], color)
    _paint(canvas, [(18, 3)], color)
    # Hook of the ?
    _paint(canvas, [(17, 4)], color)
    # Stem coming down
    _paint(canvas, [(16, 4), (16, 5)], color)
    # Dot of the ?
    _paint(canvas, [(16, 7)], color)
    # Soft highlight on the top curve
    _paint(canvas, [(15, 1), (16, 1)], highlight)
    # Shadow on hook
    _paint(canvas, [(18, 3), (17, 4)], shadow)


def sig_pint_glass(canvas):
    """Tall pint glass with white foam head and amber beer body.

    Sits to the left of the head, cols 2-6, rows 12-22. Three-tone amber.
    """
    glass_edge = (170, 195, 210)
    glass_mid = (210, 230, 240)
    glass_hi = (245, 250, 255)
    foam_main = (250, 245, 225)
    foam_hi = WHITE
    foam_sh = (215, 205, 175)
    beer_dark = (110, 55, 10)
    beer_main = (190, 115, 30)
    beer_hi = (235, 175, 80)

    # Glass walls (slightly tapered pint shape)
    _paint(canvas, [(2, 13), (2, 14), (2, 15), (2, 16), (2, 17),
                    (2, 18), (2, 19), (2, 20)], glass_edge)
    _paint(canvas, [(6, 13), (6, 14), (6, 15), (6, 16), (6, 17),
                    (6, 18), (6, 19), (6, 20)], glass_edge)
    # Foam head (rounded top, slightly bulging)
    _fill_rect(canvas, 3, 12, 5, 14, foam_main)
    _paint(canvas, [(2, 13), (6, 13)], foam_main)
    _paint(canvas, [(3, 12), (4, 12)], foam_hi)
    _paint(canvas, [(5, 14)], foam_sh)
    # Beer body (amber gradient: light top, deep bottom)
    _fill_rect(canvas, 3, 15, 5, 20, beer_main)
    _paint(canvas, [(3, 15), (4, 15), (5, 15)], beer_hi)  # top sunlit row
    _paint(canvas, [(3, 19), (4, 20), (5, 19), (5, 20)], beer_dark)  # bottom shadow
    # Single vertical highlight stripe (glass reflection)
    _paint(canvas, [(3, 16), (3, 18)], glass_hi)
    # Glass base (slightly wider)
    _paint(canvas, [(2, 21), (3, 21), (4, 21), (5, 21), (6, 21)], glass_mid)
    _paint(canvas, [(2, 22), (3, 22), (4, 22), (5, 22), (6, 22)], glass_edge)
    _paint(canvas, [(1, 22), (7, 22)], glass_edge)


def sig_crown(canvas, color):
    """5-point gold crown floating above head with center jewel."""
    shadow = _mix(color, BLACK, 0.4)
    highlight = _mix(color, WHITE, 0.45)
    jewel = (220, 50, 80)
    jewel_hi = (255, 150, 170)
    # Base band (rows 4-5, cols 11-20)
    _fill_rect(canvas, 11, 4, 20, 5, color)
    # Bottom edge shadow
    _paint(canvas, [(11, 5), (12, 5), (13, 5), (14, 5), (15, 5),
                    (16, 5), (17, 5), (18, 5), (19, 5), (20, 5)], shadow)
    # Top edge highlight
    _paint(canvas, [(12, 4), (14, 4), (16, 4), (18, 4)], highlight)
    # 5 evenly spaced spikes pointing up (rows 1-3)
    # Spike 1 (left), 2, 3 (center, tallest), 4, 5 (right)
    _paint(canvas, [(11, 3), (12, 3)], color)       # left spike
    _paint(canvas, [(14, 3), (15, 3)], color)       # left-mid spike
    _paint(canvas, [(15, 2), (16, 2)], color)       # center spike
    _paint(canvas, [(15, 1), (16, 1)], color)       # tallest tip
    _paint(canvas, [(17, 3), (18, 3)], color)       # right-mid spike
    _paint(canvas, [(19, 3), (20, 3)], color)       # right spike
    # Shadow on right side of each spike
    _paint(canvas, [(12, 3), (15, 3), (18, 3), (20, 3), (16, 2)], shadow)
    # Center jewel inset in band
    _paint(canvas, [(15, 4), (16, 4)], jewel)
    _paint(canvas, [(15, 4)], jewel_hi)


def sig_chain(canvas):
    """Thick gold rope chain across the neck with hanging medallion pendant.

    Spans cols 11-20 along rows 26-28 with a pendant at rows 29-31 center.
    """
    # Rope chain links: alternating gold/dark-gold dots for a beaded look
    chain_y_top = 26
    chain_y_bot = 27
    for x in range(11, 21):
        light = (x % 2 == 0)
        _paint(canvas, [(x, chain_y_top)], GOLD if light else GOLD_DARK)
        _paint(canvas, [(x, chain_y_bot)], GOLD_DARK if light else GOLD)
    # Dip in middle (chain hangs)
    _paint(canvas, [(14, 28), (15, 28), (16, 28), (17, 28)], GOLD)
    _paint(canvas, [(14, 28), (17, 28)], GOLD_DARK)
    # Pendant: gold medallion with darker inner border
    _fill_rect(canvas, 14, 29, 17, 31, GOLD)
    _paint(canvas, [(14, 29), (17, 29), (14, 31), (17, 31)], GOLD_DARK)
    _paint(canvas, [(15, 30), (16, 30)], GOLD_LIGHT)  # center highlight
    _paint(canvas, [(15, 29), (16, 29)], GOLD_LIGHT)  # top highlight


def sig_ai_agent(canvas, color):
    """Glowing orb floating off the right shoulder with antenna and sparkles."""
    glow_outer = _mix(color, BLACK, 0.45)
    glow_mid = color
    glow_hi = _mix(color, WHITE, 0.55)
    core = WHITE
    spark = _mix(color, WHITE, 0.7)

    # Orb body (cols 25-29, rows 22-26)
    _fill_rect(canvas, 26, 23, 28, 25, glow_mid)
    _paint(canvas, [(25, 24), (29, 24)], glow_mid)
    _paint(canvas, [(26, 22), (27, 22), (28, 22)], glow_outer)
    _paint(canvas, [(26, 26), (27, 26), (28, 26)], glow_outer)
    _paint(canvas, [(25, 23), (25, 25)], glow_outer)
    _paint(canvas, [(29, 23), (29, 25)], glow_outer)
    # Inner core
    _paint(canvas, [(27, 24)], core)
    _paint(canvas, [(26, 24), (28, 24), (27, 23), (27, 25)], glow_hi)
    # Antenna with tip
    _paint(canvas, [(27, 21), (27, 20)], glow_outer)
    _paint(canvas, [(27, 19)], glow_hi)
    _paint(canvas, [(27, 18)], core)
    # Sparkles around orb
    _paint(canvas, [(24, 22), (30, 22), (24, 27), (30, 26)], spark)
    _paint(canvas, [(25, 21), (29, 27)], glow_hi)


def sig_cross_necklace(canvas):
    """Clear silver cross pendant on a thin chain at the collar.

    Chain dips along row 27 cols 13-18, cross hangs rows 28-31 centered col 15-16.
    """
    chain = SILVER_DARK
    chain_hi = SILVER_LIGHT
    cross_main = SILVER
    cross_sh = (130, 140, 150)
    cross_hi = SILVER_LIGHT
    # Thin chain
    _paint(canvas, [(12, 26), (13, 27), (14, 27), (17, 27),
                    (18, 27), (19, 26)], chain)
    _paint(canvas, [(15, 27), (16, 27)], chain_hi)
    # Cross vertical stem (rows 28-31 col 15-16)
    _fill_rect(canvas, 15, 28, 16, 31, cross_main)
    # Cross horizontal arm (row 29 cols 13-18)
    _paint(canvas, [(13, 29), (14, 29), (17, 29), (18, 29)], cross_main)
    # Shadow + highlight
    _paint(canvas, [(16, 28), (16, 29), (16, 30), (16, 31)], cross_sh)
    _paint(canvas, [(13, 29), (15, 28)], cross_hi)
    # Tiny dark outline at bottom tip for separation
    _paint(canvas, [(15, 31)], chain)


def sig_surfboard(canvas):
    """Vertical surfboard peeking behind the right shoulder with a tail fin.

    Wider 3-pixel board (cols 25-27) with rounded nose, center stripe, and a
    distinct fin tab at the tail so the silhouette reads as a surfboard.
    """
    board_main = (245, 248, 250)
    board_sh = (175, 190, 205)
    board_hi = WHITE
    stripe = (220, 70, 60)
    stripe_sh = (160, 35, 30)
    fin = (60, 90, 140)
    fin_sh = (35, 55, 90)
    # Rounded nose tip (top)
    _paint(canvas, [(26, 6)], board_main)
    _paint(canvas, [(25, 7), (26, 7), (27, 7)], board_main)
    # Main board body (cols 25-27, rows 8-23)
    _fill_rect(canvas, 25, 8, 27, 23, board_main)
    # Rounded tail
    _paint(canvas, [(25, 24), (26, 24), (27, 24)], board_main)
    _paint(canvas, [(26, 25)], board_main)
    # Right edge shadow
    _paint(canvas, [(27, 9), (27, 11), (27, 13), (27, 15),
                    (27, 17), (27, 19), (27, 21), (27, 23)], board_sh)
    # Left edge highlight
    _paint(canvas, [(25, 9), (25, 11), (25, 13), (25, 15),
                    (25, 17), (25, 19), (25, 21)], board_hi)
    # Center red racing stripe down the spine
    _paint(canvas, [(26, 9), (26, 10), (26, 11), (26, 12), (26, 13),
                    (26, 14), (26, 15), (26, 16), (26, 17), (26, 18),
                    (26, 19), (26, 20), (26, 21), (26, 22)], stripe)
    _paint(canvas, [(26, 11), (26, 15), (26, 19)], stripe_sh)
    # Tail fin protruding from the bottom (clearly skeg-shaped)
    _paint(canvas, [(27, 25), (28, 25)], fin)
    _paint(canvas, [(28, 26), (29, 26)], fin)
    _paint(canvas, [(29, 27)], fin)
    _paint(canvas, [(28, 25), (29, 27)], fin_sh)


def sig_bt_pin(canvas, color):
    """Braintrust brand pin on left chest with brand color glow.

    Sits at cols 6-9, rows 28-30 (clearly on shirt area).
    """
    glow = _mix(color, WHITE, 0.55)
    shadow = _mix(color, BLACK, 0.5)
    # Round-ish pin body
    _paint(canvas, [(7, 28), (8, 28)], color)
    _fill_rect(canvas, 6, 29, 9, 30, color)
    _paint(canvas, [(7, 31), (8, 31)], color)
    # Letter mark (BT styled as offset dots)
    _paint(canvas, [(7, 29)], WHITE)  # B dot
    _paint(canvas, [(8, 30)], WHITE)  # T dot
    # Highlight on upper-left edge
    _paint(canvas, [(6, 29), (7, 28)], glow)
    # Shadow on lower-right
    _paint(canvas, [(9, 30), (8, 31)], shadow)


def sig_earring(canvas):
    """Single gold hoop earring dangling from left ear (col 8-9, rows 18-20)."""
    # Top attachment to ear
    _paint(canvas, [(9, 18)], GOLD_DARK)
    # Hoop: open ring shape
    _paint(canvas, [(8, 19), (10, 19)], GOLD_DARK)
    _paint(canvas, [(8, 20), (10, 20)], GOLD)
    _paint(canvas, [(9, 21)], GOLD_DARK)
    # Highlight on the upper-left of the ring
    _paint(canvas, [(8, 19)], GOLD_LIGHT)


def sig_headphones(canvas, color=BLACK):
    """Over-ear studio headphones with padded cups (kept for back-compat)."""
    shadow = _mix(color, BLACK, 0.4) if color != BLACK else (40, 40, 50)
    highlight = _mix(color, WHITE, 0.35)
    # Band arching over the head (rows 5-7)
    _paint(canvas, [(11, 8), (12, 7), (13, 6), (14, 6), (15, 6),
                    (16, 6), (17, 6), (18, 6), (19, 7), (20, 8)], color)
    _paint(canvas, [(14, 6), (15, 6), (16, 6)], highlight)
    # Left ear cup
    _fill_rect(canvas, 7, 16, 9, 19, color)
    _paint(canvas, [(8, 17), (8, 18)], shadow)
    _paint(canvas, [(7, 16)], highlight)
    # Right ear cup
    _fill_rect(canvas, 22, 16, 24, 19, color)
    _paint(canvas, [(23, 17), (23, 18)], shadow)
    _paint(canvas, [(24, 16)], highlight)


def sig_cap(canvas, color):
    """Baseball cap with brim, crown, and front logo (rows 4-10, cols 8-22)."""
    shadow = _mix(color, BLACK, 0.45)
    highlight = _mix(color, WHITE, 0.3)
    # Crown (top dome of the cap)
    _fill_rect(canvas, 10, 6, 21, 9, color)
    _paint(canvas, [(11, 5), (12, 5), (13, 5), (14, 5),
                    (15, 5), (16, 5), (17, 5), (18, 5), (19, 5), (20, 5)], color)
    # Crown highlight (front-top catches light)
    _paint(canvas, [(12, 6), (13, 6), (14, 6)], highlight)
    # Seam line down center of crown
    _paint(canvas, [(15, 6), (15, 7), (15, 8)], shadow)
    # Brim: extends out to the left over forehead (rows 10-11)
    _paint(canvas, [(7, 10), (8, 10), (9, 10), (10, 10), (11, 10),
                    (12, 10), (13, 10), (14, 10), (15, 10), (16, 10)], color)
    _paint(canvas, [(7, 11), (8, 11), (9, 11), (10, 11), (11, 11),
                    (12, 11), (13, 11), (14, 11)], shadow)
    # Brim underside line for depth
    _paint(canvas, [(8, 11), (10, 11), (12, 11)], shadow)
    # Front logo patch (rows 7-8, cols 15-17)
    _paint(canvas, [(15, 7), (16, 7), (17, 7)], WHITE)
    _paint(canvas, [(16, 8)], WHITE)
    # Back of cap (snap area)
    _paint(canvas, [(20, 9), (21, 9)], shadow)


# ============================================================================
# HEAD ACCESSORIES (drawn LAST, over face)
# ============================================================================

def acc_sunglasses(canvas):
    """Black wayfarer sunglasses: chunky frames, bridge, no skin gap behind."""
    frame = BLACK
    lens = (25, 25, 35)
    glint = (110, 130, 180)
    # Top brow line of frame (thick)
    _paint(canvas, [(11, 15), (12, 15), (13, 15), (14, 15), (15, 15),
                    (16, 15), (17, 15), (18, 15), (19, 15), (20, 15)], frame)
    # Left lens (filled dark, not see-through)
    _fill_rect(canvas, 11, 16, 14, 17, lens)
    # Right lens
    _fill_rect(canvas, 17, 16, 20, 17, lens)
    # Outer frame edges
    _paint(canvas, [(11, 16), (11, 17), (14, 16), (14, 17),
                    (17, 16), (17, 17), (20, 16), (20, 17)], frame)
    # Bottom frame line
    _paint(canvas, [(11, 17), (12, 17), (13, 17), (14, 17),
                    (17, 17), (18, 17), (19, 17), (20, 17)], frame)
    # Solid bridge (no skin showing through)
    _paint(canvas, [(15, 16), (16, 16)], frame)
    # Specular highlight glints
    _paint(canvas, [(12, 16), (18, 16)], glint)


def acc_aviators(canvas):
    """Gold teardrop aviator frames with reflective brown/gold gradient lenses."""
    frame = (200, 165, 70)
    frame_dark = (140, 105, 30)
    lens_top = (180, 140, 75)
    lens_mid = (130, 90, 45)
    lens_bot = (80, 55, 25)
    lens_hi = (240, 215, 140)
    # Top of frames (slightly curved teardrop)
    _paint(canvas, [(11, 15), (12, 15), (13, 15), (14, 15),
                    (17, 15), (18, 15), (19, 15), (20, 15)], frame)
    # Side curves
    _paint(canvas, [(11, 16), (14, 16), (17, 16), (20, 16)], frame)
    # Bottom rounded
    _paint(canvas, [(12, 17), (13, 17), (18, 17), (19, 17)], frame_dark)
    # Lens fill: reflective gradient
    _paint(canvas, [(12, 16)], lens_hi)        # bright reflection
    _paint(canvas, [(13, 16)], lens_top)
    _paint(canvas, [(12, 17)], lens_mid)
    _paint(canvas, [(13, 17)], lens_bot)
    _paint(canvas, [(18, 16)], lens_hi)
    _paint(canvas, [(19, 16)], lens_top)
    _paint(canvas, [(18, 17)], lens_mid)
    _paint(canvas, [(19, 17)], lens_bot)
    # Bridge connecting the two lenses (thin, gold)
    _paint(canvas, [(15, 15), (16, 15)], frame)
    _paint(canvas, [(15, 16), (16, 16)], frame_dark)


def acc_glasses_clear(canvas):
    """Thin clear-frame glasses: eyes still visible through lenses."""
    frame = (60, 50, 45)
    frame_hi = (130, 115, 100)
    # Top frame
    _paint(canvas, [(11, 15), (12, 15), (13, 15), (14, 15),
                    (17, 15), (18, 15), (19, 15), (20, 15)], frame)
    # Sides
    _paint(canvas, [(11, 16), (11, 17), (14, 16), (14, 17),
                    (17, 16), (17, 17), (20, 16), (20, 17)], frame)
    # Bottom (only the rims, not crossing through eye)
    _paint(canvas, [(12, 17), (13, 17), (18, 17), (19, 17)], frame)
    # Bridge: thin, just one row, leaving nose visible below
    _paint(canvas, [(15, 15), (16, 15)], frame)
    # Subtle highlight on top of each lens (catches light)
    _paint(canvas, [(12, 15), (18, 15)], frame_hi)


def acc_ar_smart_glasses(canvas, color):
    """Cyberpunk AR visor: continuous lens band with glowing edge."""
    visor_dark = (15, 15, 25)
    visor_mid = (35, 35, 55)
    glow = _mix(color, WHITE, 0.4)
    glow_hot = _mix(color, WHITE, 0.7)
    # Top edge of visor (sharp)
    _paint(canvas, [(10, 15), (11, 15), (12, 15), (13, 15), (14, 15),
                    (15, 15), (16, 15), (17, 15), (18, 15),
                    (19, 15), (20, 15), (21, 15)], visor_dark)
    # Visor lens body (one continuous band)
    _fill_rect(canvas, 11, 16, 20, 16, visor_mid)
    # Glow stripe across the bottom of the lens
    _paint(canvas, [(11, 17), (12, 17), (13, 17), (14, 17), (15, 17),
                    (16, 17), (17, 17), (18, 17), (19, 17), (20, 17)], glow)
    # Hot scan-line glints
    _paint(canvas, [(13, 17), (18, 17)], glow_hot)
    # HUD pixels in the lens
    _paint(canvas, [(12, 16), (19, 16)], glow_hot)
    # Bridge tone (slightly darker visor through middle)
    _paint(canvas, [(15, 16), (16, 16)], visor_dark)


def acc_laser_eyes(canvas, color=(255, 50, 50)):
    """Glowing laser beams shooting out of both eyes horizontally (kept compatible)."""
    inner = _mix(color, WHITE, 0.7)
    trail = _mix(color, (10, 10, 15), 0.3)
    # Beam cores at eye position (row 16)
    _paint(canvas, [(13, 16), (18, 16)], color)
    # Bright inner glow above
    _paint(canvas, [(13, 15), (18, 15)], inner)
    # Outward beam trails
    for x in range(0, 12):
        canvas.putpixel((x, 16), trail)
    for x in range(19, 32):
        canvas.putpixel((x, 16), trail)
    # Hot tips at the ends
    _paint(canvas, [(0, 16), (31, 16)], inner)


def acc_earbuds(canvas):
    """Small white wireless earbuds: pod in ear with stem hanging down."""
    pod = WHITE
    pod_sh = (200, 200, 210)
    pod_dk = (140, 140, 155)
    # Left earbud
    _paint(canvas, [(9, 17), (10, 17)], pod)
    _paint(canvas, [(9, 18)], pod_sh)
    _paint(canvas, [(10, 18)], pod_dk)  # speaker mesh hint
    # Left stem
    _paint(canvas, [(9, 19), (9, 20)], pod)
    _paint(canvas, [(9, 20)], pod_sh)
    # Right earbud
    _paint(canvas, [(21, 17), (22, 17)], pod)
    _paint(canvas, [(22, 18)], pod_sh)
    _paint(canvas, [(21, 18)], pod_dk)
    # Right stem
    _paint(canvas, [(22, 19), (22, 20)], pod)
    _paint(canvas, [(22, 20)], pod_sh)


def acc_beanie(canvas, color):
    """Knit beanie covering the top of the head with a cuffed brim and ribbed texture."""
    shadow = _mix(color, BLACK, 0.4)
    highlight = _mix(color, WHITE, 0.25)
    # Crown of beanie (rounded top)
    _paint(canvas, [(12, 4), (13, 4), (14, 4), (15, 4),
                    (16, 4), (17, 4), (18, 4), (19, 4)], color)
    _fill_rect(canvas, 10, 5, 21, 9, color)
    # Knit ribbing (vertical lines)
    for x in range(11, 21, 2):
        _paint(canvas, [(x, 5), (x, 6), (x, 7), (x, 8)], shadow)
    for x in range(12, 21, 2):
        _paint(canvas, [(x, 5), (x, 7)], highlight)
    # Cuff (folded brim) at rows 9-10, slightly thicker, darker tone
    _fill_rect(canvas, 9, 9, 22, 10, shadow)
    _paint(canvas, [(10, 10), (12, 10), (14, 10), (16, 10),
                    (18, 10), (20, 10)], color)
    # Pom-pom on top
    _paint(canvas, [(15, 3), (16, 3)], highlight)
    _paint(canvas, [(15, 2), (16, 2)], color)


def acc_red_lips(canvas):
    """Bright red lip color replacing default mouth tone."""
    red = (210, 35, 55)
    red_dark = (140, 20, 35)
    red_hi = (250, 130, 140)
    # Upper lip
    _paint(canvas, [(13, 23), (14, 23), (15, 23),
                    (16, 23), (17, 23), (18, 23)], red)
    # Cupid's bow shadow
    _paint(canvas, [(15, 22), (16, 22)], red_dark)
    # Lower lip
    _paint(canvas, [(14, 24), (15, 24), (16, 24), (17, 24)], red_dark)
    # Highlight pinpoints (gloss)
    _paint(canvas, [(14, 23), (17, 23)], red_hi)
    # Soft outer corners
    _paint(canvas, [(13, 23), (18, 23)], red_dark)


def acc_earring_stud(canvas):
    """Small gold stud earring on left ear."""
    # Single stud just below the ear midpoint
    _paint(canvas, [(9, 19)], GOLD)
    _paint(canvas, [(9, 20)], GOLD_DARK)


def acc_party_horn(canvas, color):
    """Party horn cone extending from the mouth (kept for back-compat, improved)."""
    main = color
    shadow = _mix(color, BLACK, 0.4)
    highlight = _mix(color, WHITE, 0.4)
    # Tapering cone from mouth corner outward
    _paint(canvas, [(19, 23), (20, 23)], main)
    _paint(canvas, [(20, 22), (21, 22)], main)
    _paint(canvas, [(22, 21), (23, 21)], main)
    _paint(canvas, [(24, 20), (25, 20)], main)
    _paint(canvas, [(20, 23), (22, 22)], shadow)
    _paint(canvas, [(19, 23), (21, 22), (23, 21)], highlight)
    # Sparkle puff at the tip
    _paint(canvas, [(26, 19), (27, 20)], WHITE)
    _paint(canvas, [(26, 20)], highlight)
