#!/usr/bin/env python3
"""Hair sprites v2 for the Braintrust pixel art NFT collection.

Each hair function paints onto a 32x32 PIL canvas. Three-tone shading
(main / shadow / highlight) is used consistently so every silhouette
reads at a glance. The head sits at rows 9-25, cols 10-21; the hair
body lives at rows 3-12 (with long styles extending to row 25).

All 15 functions share the signature `hair_xxx(canvas, color_key)`.
The HAIR_FNS_V2 dict at the bottom maps style name to function.

Helpers from character_builder.py are imported at runtime.
"""

from character_builder import HAIR, HAIR_SHADOW, HAIR_LIGHT, SKIN, paint, mix


# ---------------------------------------------------------------------------
# 1. SHORT PARTED
# Clean side-part with a visible part line, forehead fringe sweeping left,
# trimmed sides covering the upper ear.
# ---------------------------------------------------------------------------
def hair_short_parted(canvas, color_key):
    h  = HAIR[color_key]
    hs = HAIR_SHADOW[color_key]
    hl = HAIR_LIGHT[color_key]

    # Crown dome
    for x in range(11, 21): canvas.putpixel((x, 7), h)
    for x in range(10, 22): canvas.putpixel((x, 8), h)
    for x in range(10, 22): canvas.putpixel((x, 9), h)

    # Front sweep across forehead with a clear directional flow (left -> right)
    paint(canvas, [(11, 10), (12, 10), (13, 10), (14, 10), (15, 10), (16, 10), (17, 10), (18, 10), (19, 10)], h)
    # Fringe tail dipping over the right brow
    paint(canvas, [(19, 11), (20, 11)], h)

    # The signature: part line on the right side (col 17, rows 7-10)
    paint(canvas, [(17, 7), (17, 8), (17, 9), (17, 10)], hs)
    # Shadow under the front bangs
    paint(canvas, [(11, 11), (12, 11), (13, 11)], hs)

    # Highlights up top (where light hits the crown)
    paint(canvas, [(12, 7), (13, 7), (14, 7), (12, 8), (13, 8)], hl)
    paint(canvas, [(18, 8), (19, 8)], hl)

    # Sides covering temples
    paint(canvas, [(10, 10), (10, 11), (10, 12), (21, 10), (21, 11), (21, 12)], h)
    paint(canvas, [(9, 11), (22, 11)], hs)


# ---------------------------------------------------------------------------
# 2. SLICK BACK
# Sleek, swept-back hair. Horizontal highlight stripes evoke gel sheen.
# Forehead fully exposed (hair hugs the scalp tight, no front bangs).
# ---------------------------------------------------------------------------
def hair_slick_back(canvas, color_key):
    h  = HAIR[color_key]
    hs = HAIR_SHADOW[color_key]
    hl = HAIR_LIGHT[color_key]

    # Crown - slightly tighter than short_parted, sloping back
    for x in range(12, 20): canvas.putpixel((x, 6), h)
    for x in range(11, 21): canvas.putpixel((x, 7), h)
    for x in range(10, 22): canvas.putpixel((x, 8), h)
    for x in range(10, 22): canvas.putpixel((x, 9), h)

    # Forehead exposed: no row 10 fill across the middle (skin shows through),
    # only temple corners
    paint(canvas, [(10, 10), (11, 10), (20, 10), (21, 10)], h)
    paint(canvas, [(10, 11), (21, 11)], h)
    paint(canvas, [(10, 12), (21, 12)], hs)

    # Signature gel-sheen highlight stripes running back along the top
    paint(canvas, [(13, 6), (14, 6), (15, 6), (16, 6)], hl)
    paint(canvas, [(12, 7), (14, 7), (16, 7), (18, 7), (20, 7)], hl)

    # Shadow grooves between the strands (parallel slick lines)
    paint(canvas, [(13, 8), (15, 8), (17, 8), (19, 8)], hs)
    paint(canvas, [(11, 9), (12, 9), (20, 9), (21, 9)], hs)


# ---------------------------------------------------------------------------
# 3. UNDERCUT
# Tall, voluminous top with a sharp horizontal break at the shaved sides.
# The signature is the dark band at the side fade.
# ---------------------------------------------------------------------------
def hair_undercut(canvas, color_key):
    h  = HAIR[color_key]
    hs = HAIR_SHADOW[color_key]
    hl = HAIR_LIGHT[color_key]

    # Tall top mass (rows 4-8)
    for x in range(12, 19): canvas.putpixel((x, 4), h)
    for x in range(11, 20): canvas.putpixel((x, 5), h)
    for x in range(11, 21): canvas.putpixel((x, 6), h)
    for x in range(11, 21): canvas.putpixel((x, 7), h)
    for x in range(11, 21): canvas.putpixel((x, 8), h)

    # Front quiff dropping forward over the brow
    paint(canvas, [(12, 9), (13, 9), (14, 9), (15, 9), (16, 9), (17, 9)], h)
    paint(canvas, [(13, 10), (14, 10), (15, 10)], h)

    # Signature: dark shaved band at sides (rows 9-12, cols 10 & 21)
    paint(canvas, [(10, 8), (10, 9), (10, 10), (10, 11), (10, 12),
                   (21, 8), (21, 9), (21, 10), (21, 11), (21, 12)], hs)

    # Highlight on top of the crown / quiff
    paint(canvas, [(13, 4), (14, 4), (15, 4)], hl)
    paint(canvas, [(13, 5), (16, 5)], hl)
    paint(canvas, [(14, 6), (17, 6)], hl)

    # Shadow at the underside where top meets the shaved sides
    paint(canvas, [(11, 8), (20, 8)], hs)


# ---------------------------------------------------------------------------
# 4. MESSY
# Spiky, irregular tufts of varying heights. Signature: jagged top silhouette.
# ---------------------------------------------------------------------------
def hair_messy(canvas, color_key):
    h  = HAIR[color_key]
    hs = HAIR_SHADOW[color_key]
    hl = HAIR_LIGHT[color_key]

    # Tall irregular spikes (each tuft a different height)
    paint(canvas, [(11, 5), (15, 5), (19, 5)], h)            # tall tufts
    paint(canvas, [(12, 6), (13, 6), (14, 6), (16, 6), (17, 6), (18, 6), (20, 6)], h)  # medium
    paint(canvas, [(10, 7), (11, 7), (12, 7), (13, 7), (14, 7), (15, 7), (16, 7),
                   (17, 7), (18, 7), (19, 7), (20, 7), (21, 7)], h)

    # Body of hair
    for x in range(10, 22): canvas.putpixel((x, 8), h)
    for x in range(10, 22): canvas.putpixel((x, 9), h)

    # Wisps hanging onto the forehead (asymmetric, not a clean line)
    paint(canvas, [(11, 10), (12, 10), (15, 10), (16, 10), (19, 10), (20, 10)], h)

    # Highlights on the tips of select spikes
    paint(canvas, [(11, 5), (15, 5)], hl)
    paint(canvas, [(13, 6), (17, 6)], hl)

    # Shadow valleys between tufts and underneath
    paint(canvas, [(12, 7), (14, 7), (18, 7), (20, 7)], hs)
    paint(canvas, [(13, 9), (17, 9), (19, 9)], hs)

    # Sideburns
    paint(canvas, [(10, 10), (10, 11), (21, 10), (21, 11)], h)


# ---------------------------------------------------------------------------
# 5. CURLY SHORT
# Rounded curl bumps on top, three-tone curl shading.
# Signature: a tight pattern of curls, with shadow underneath each curl.
# ---------------------------------------------------------------------------
def hair_curly_short(canvas, color_key):
    h  = HAIR[color_key]
    hs = HAIR_SHADOW[color_key]
    hl = HAIR_LIGHT[color_key]

    # Top row of curl crowns (bumps)
    paint(canvas, [(11, 5), (13, 5), (15, 5), (17, 5), (19, 5)], h)
    # Curl row 2 (between row 1 bumps - bumps offset)
    paint(canvas, [(10, 6), (11, 6), (12, 6), (13, 6), (14, 6), (15, 6),
                   (16, 6), (17, 6), (18, 6), (19, 6), (20, 6), (21, 6)], h)

    # Curl shadows directly under each top bump
    paint(canvas, [(11, 7), (13, 7), (15, 7), (17, 7), (19, 7)], hs)

    # Body of curls
    for x in range(10, 22): canvas.putpixel((x, 7), h) if x not in [11, 13, 15, 17, 19] else None
    for x in range(10, 22): canvas.putpixel((x, 8), h)
    for x in range(10, 22): canvas.putpixel((x, 9), h)

    # Second row of curl shadows (offset for texture)
    paint(canvas, [(12, 9), (14, 9), (16, 9), (18, 9), (20, 9)], hs)

    # Forehead curl line
    paint(canvas, [(11, 10), (13, 10), (15, 10), (17, 10), (19, 10)], h)

    # Highlights on a few curl tops (light direction: upper left)
    paint(canvas, [(11, 5), (13, 5)], hl)
    paint(canvas, [(12, 6), (14, 6)], hl)

    # Sideburns curl
    paint(canvas, [(10, 10), (10, 11), (21, 10), (21, 11)], h)


# ---------------------------------------------------------------------------
# 6. LONG STRAIGHT
# Long flat hair falling past the shoulders. Center part. Vertical sheen.
# ---------------------------------------------------------------------------
def hair_long_straight(canvas, color_key):
    h  = HAIR[color_key]
    hs = HAIR_SHADOW[color_key]
    hl = HAIR_LIGHT[color_key]

    # Crown
    for x in range(11, 21): canvas.putpixel((x, 6), h)
    for x in range(10, 22): canvas.putpixel((x, 7), h)
    for x in range(9, 23):  canvas.putpixel((x, 8), h)
    for x in range(9, 23):  canvas.putpixel((x, 9), h)

    # Front fringe curtain framing the forehead
    paint(canvas, [(10, 10), (11, 10), (20, 10), (21, 10)], h)

    # Signature: center part line (a single shadow column down the middle)
    paint(canvas, [(15, 6), (15, 7), (15, 8)], hs)

    # Vertical sheen highlights (parallel to the hair flow)
    paint(canvas, [(12, 7), (12, 8)], hl)
    paint(canvas, [(18, 7), (18, 8)], hl)

    # Long sides past shoulders (straight curtain falling to row 25)
    for y in range(10, 26):
        canvas.putpixel((9, y), h)
        canvas.putpixel((22, y), h)
    for y in range(11, 26):
        canvas.putpixel((8, y), hs)
        canvas.putpixel((23, y), hs)

    # Vertical highlight streaks down the long hair
    paint(canvas, [(9, 13), (9, 14), (9, 19), (9, 20)], hl)
    paint(canvas, [(22, 13), (22, 14), (22, 19), (22, 20)], hl)

    # Tips at the bottom (a touch wider for weight)
    paint(canvas, [(8, 25), (23, 25)], h)
    paint(canvas, [(7, 24), (7, 25), (24, 24), (24, 25)], hs)


# ---------------------------------------------------------------------------
# 7. LONG WAVY
# Long hair with clear S-curves down the sides. Slight volume up top.
# ---------------------------------------------------------------------------
def hair_long_wavy(canvas, color_key):
    h  = HAIR[color_key]
    hs = HAIR_SHADOW[color_key]
    hl = HAIR_LIGHT[color_key]

    # Crown - slightly fuller than long_straight
    paint(canvas, [(12, 5), (14, 5), (16, 5), (18, 5), (20, 5)], h)
    for x in range(11, 21): canvas.putpixel((x, 6), h)
    for x in range(10, 22): canvas.putpixel((x, 7), h)
    for x in range(9, 23):  canvas.putpixel((x, 8), h)
    for x in range(9, 23):  canvas.putpixel((x, 9), h)

    # Front fringe with slight wave
    paint(canvas, [(10, 10), (11, 10), (12, 10), (19, 10), (20, 10), (21, 10)], h)

    # Center part with side flick
    paint(canvas, [(15, 6), (15, 7)], hs)
    paint(canvas, [(13, 7), (14, 7), (17, 7), (18, 7)], hl)

    # Signature: clear S-wave silhouette on each side
    waves_l = [
        (9, 11), (9, 12),
        (8, 13), (8, 14),
        (9, 15), (9, 16),
        (8, 17), (8, 18),
        (9, 19), (9, 20),
        (8, 21), (8, 22),
        (9, 23), (9, 24), (9, 25),
    ]
    waves_r = [
        (22, 11), (22, 12),
        (23, 13), (23, 14),
        (22, 15), (22, 16),
        (23, 17), (23, 18),
        (22, 19), (22, 20),
        (23, 21), (23, 22),
        (22, 23), (22, 24), (22, 25),
    ]
    paint(canvas, waves_l, h)
    paint(canvas, waves_r, h)

    # Shadow on inside of each wave bulge
    paint(canvas, [(9, 13), (9, 14), (9, 17), (9, 18), (9, 21), (9, 22)], hs)
    paint(canvas, [(22, 13), (22, 14), (22, 17), (22, 18), (22, 21), (22, 22)], hs)

    # Highlight on the outer crest of waves
    paint(canvas, [(8, 13), (8, 17), (8, 21)], hl)
    paint(canvas, [(23, 13), (23, 17), (23, 21)], hl)


# ---------------------------------------------------------------------------
# 8. CURLY LONG
# Big halo of curls extending down past the shoulders. Tall volume.
# Signature: scalloped (bumpy) edges everywhere, not a straight curtain.
# ---------------------------------------------------------------------------
def hair_curly_long(canvas, color_key):
    h  = HAIR[color_key]
    hs = HAIR_SHADOW[color_key]
    hl = HAIR_LIGHT[color_key]

    # Tall curly volume top - scalloped silhouette
    paint(canvas, [(11, 3), (14, 3), (17, 3), (20, 3)], h)
    paint(canvas, [(10, 4), (11, 4), (12, 4), (13, 4), (14, 4), (15, 4),
                   (16, 4), (17, 4), (18, 4), (19, 4), (20, 4), (21, 4)], h)
    for x in range(9, 23): canvas.putpixel((x, 5), h)
    for x in range(8, 24): canvas.putpixel((x, 6), h)
    for x in range(8, 24): canvas.putpixel((x, 7), h)
    for x in range(8, 24): canvas.putpixel((x, 8), h)
    for x in range(9, 23): canvas.putpixel((x, 9), h)

    # Curl shadows scattered through the volume
    paint(canvas, [(10, 5), (13, 5), (16, 5), (19, 5), (22, 5)], hs)
    paint(canvas, [(9, 7), (12, 7), (15, 7), (18, 7), (21, 7)], hs)
    paint(canvas, [(10, 8), (14, 8), (17, 8), (20, 8)], hs)

    # Curl highlights on top
    paint(canvas, [(11, 3), (14, 3)], hl)
    paint(canvas, [(11, 4), (15, 4), (18, 4)], hl)
    paint(canvas, [(10, 6), (14, 6), (18, 6)], hl)

    # Forehead curl edge
    paint(canvas, [(10, 10), (12, 10), (14, 10), (17, 10), (19, 10), (21, 10)], h)

    # Long curly sides with bumpy silhouette (rows 11-22)
    # Left side
    left_curls = [
        (8, 11), (9, 11),
        (7, 12), (8, 12), (9, 12),
        (8, 13), (9, 13),
        (7, 14), (8, 14), (9, 14),
        (8, 15), (9, 15),
        (7, 16), (8, 16), (9, 16),
        (8, 17), (9, 17),
        (7, 18), (8, 18), (9, 18),
        (8, 19), (9, 19),
        (8, 20), (9, 20),
        (9, 21), (9, 22),
    ]
    right_curls = [
        (22, 11), (23, 11),
        (22, 12), (23, 12), (24, 12),
        (22, 13), (23, 13),
        (22, 14), (23, 14), (24, 14),
        (22, 15), (23, 15),
        (22, 16), (23, 16), (24, 16),
        (22, 17), (23, 17),
        (22, 18), (23, 18), (24, 18),
        (22, 19), (23, 19),
        (22, 20), (23, 20),
        (22, 21), (22, 22),
    ]
    paint(canvas, left_curls, h)
    paint(canvas, right_curls, h)

    # Curl-edge shadows
    paint(canvas, [(7, 12), (7, 16), (24, 12), (24, 16)], hs)


# ---------------------------------------------------------------------------
# 9. FADE
# Sharp horizontal fade at the temples. Crisp side silhouette.
# Signature: visible 3-step gradient at the sideburn area.
# ---------------------------------------------------------------------------
def hair_fade(canvas, color_key):
    h  = HAIR[color_key]
    hs = HAIR_SHADOW[color_key]
    hl = HAIR_LIGHT[color_key]

    # Flat top (compact, tight crown)
    for x in range(11, 20): canvas.putpixel((x, 6), h)
    for x in range(11, 21): canvas.putpixel((x, 7), h)
    for x in range(11, 21): canvas.putpixel((x, 8), h)
    for x in range(11, 21): canvas.putpixel((x, 9), h)

    # Front hairline (a clean line, sharp edge)
    paint(canvas, [(12, 10), (13, 10), (14, 10), (15, 10), (16, 10), (17, 10), (18, 10)], h)

    # Highlights on top
    paint(canvas, [(12, 6), (14, 6), (16, 6), (18, 6)], hl)
    paint(canvas, [(13, 7), (15, 7), (17, 7)], hl)

    # Signature: 3-step fade gradient at the sides
    # Top of fade (main hair color)
    paint(canvas, [(10, 7), (10, 8), (21, 7), (21, 8)], h)
    # Mid fade (shadow)
    paint(canvas, [(10, 9), (10, 10), (21, 9), (21, 10)], hs)
    # Bottom of fade (faded to a near-skin shadow)
    skin_blend = mix(hs, SKIN["light"], 0.4)
    paint(canvas, [(10, 11), (10, 12), (21, 11), (21, 12)], skin_blend)

    # Subtle line break between top and side (defines the fade edge)
    paint(canvas, [(11, 9), (20, 9)], hs)


# ---------------------------------------------------------------------------
# 10. BEACH BLONDE
# Sun-bleached, wind-swept asymmetric flow. Streaks of brighter highlight.
# Hair flicks to the right (asymmetric, not symmetric like long_straight).
# ---------------------------------------------------------------------------
def hair_long_blonde_beach(canvas, color_key):
    h  = HAIR[color_key]
    hs = HAIR_SHADOW[color_key]
    hl = HAIR_LIGHT[color_key]

    # Wind-swept crown - higher on the left, falling to the right
    paint(canvas, [(11, 5), (12, 5), (13, 5)], h)
    for x in range(10, 22): canvas.putpixel((x, 6), h)
    for x in range(10, 22): canvas.putpixel((x, 7), h)
    for x in range(9, 23):  canvas.putpixel((x, 8), h)
    for x in range(9, 23):  canvas.putpixel((x, 9), h)

    # Asymmetric front sweep - more hair on the left side of forehead
    paint(canvas, [(10, 10), (11, 10), (12, 10), (13, 10), (14, 10), (19, 10), (20, 10), (21, 10)], h)
    paint(canvas, [(11, 11), (12, 11)], h)   # left side hangs lower

    # Signature: sun-bleached streaks (light) flowing diagonally
    paint(canvas, [(11, 5), (12, 5)], hl)
    paint(canvas, [(11, 6), (12, 6), (13, 6)], hl)
    paint(canvas, [(12, 7), (13, 7), (14, 7)], hl)
    paint(canvas, [(17, 6), (18, 6), (19, 6)], hl)

    # Shadow on the swept side (creates wind direction)
    paint(canvas, [(15, 6), (16, 7), (17, 8)], hs)

    # Long flowing sides, asymmetric (left falls longer)
    # Left: rows 11-25 (longer)
    for y in range(11, 26):
        canvas.putpixel((9, y), h)
    for y in range(12, 26):
        canvas.putpixel((8, y), h)
    # Right: rows 11-24 (shorter, more swept back)
    for y in range(11, 25):
        canvas.putpixel((22, y), h)
    for y in range(13, 25):
        canvas.putpixel((23, y), h)

    # Sun streaks running down the long hair
    paint(canvas, [(8, 13), (8, 14), (8, 18), (8, 19), (8, 23), (8, 24)], hl)
    paint(canvas, [(9, 16), (9, 21)], hl)
    paint(canvas, [(22, 14), (22, 18), (22, 22), (23, 16), (23, 20)], hl)

    # Shadow at hair underside / inner edge for depth
    paint(canvas, [(10, 12), (10, 17), (10, 22), (21, 12), (21, 17), (21, 22)], hs)

    # Wind-flicked tips at the bottom (asymmetric flare)
    paint(canvas, [(7, 24), (7, 25), (8, 25)], h)
    paint(canvas, [(23, 24), (24, 23)], h)


# ===========================================================================
# NEW STYLES
# ===========================================================================

# ---------------------------------------------------------------------------
# 11. PONYTAIL
# Hair pulled back tight, a clear ponytail flicked to one side.
# Signature: visible ponytail blob behind the head (cols 22-25, rows 10-18).
# ---------------------------------------------------------------------------
def hair_ponytail(canvas, color_key):
    h  = HAIR[color_key]
    hs = HAIR_SHADOW[color_key]
    hl = HAIR_LIGHT[color_key]

    # Crown pulled back tight, slight peak at hairline
    for x in range(11, 21): canvas.putpixel((x, 7), h)
    for x in range(10, 22): canvas.putpixel((x, 8), h)
    for x in range(10, 22): canvas.putpixel((x, 9), h)

    # Smooth tight pulled-back lines on top (horizontal sheen, no front bangs)
    paint(canvas, [(11, 7), (13, 7), (15, 7), (17, 7), (19, 7)], hl)
    paint(canvas, [(12, 8), (14, 8), (16, 8), (18, 8), (20, 8)], hl)
    paint(canvas, [(13, 9), (15, 9), (17, 9), (19, 9)], hs)

    # Tight forehead band (no fringe, just clean edge)
    paint(canvas, [(10, 10), (11, 10), (20, 10), (21, 10)], h)
    paint(canvas, [(10, 11), (21, 11)], hs)

    # Signature: the ponytail itself, flicked to the right behind the head
    # Base of ponytail at the back of head (above ear)
    paint(canvas, [(22, 11), (22, 12), (22, 13)], h)
    # Tail extending out and down-right
    paint(canvas, [(23, 12), (23, 13), (23, 14), (24, 13), (24, 14), (24, 15),
                   (25, 14), (25, 15), (25, 16), (24, 16), (24, 17), (23, 17), (23, 18)], h)
    # Tail tip
    paint(canvas, [(23, 19), (22, 19)], h)

    # Ponytail shadow (right side / underside)
    paint(canvas, [(25, 14), (25, 15), (25, 16), (24, 17), (23, 18), (22, 19)], hs)
    # Ponytail highlight (top / outer curl)
    paint(canvas, [(23, 12), (24, 13), (23, 14)], hl)

    # Hair tie band (a small darker pixel cluster at the base)
    paint(canvas, [(22, 12)], hs)


# ---------------------------------------------------------------------------
# 12. TOP KNOT
# Small bun on top, sides short / shaved. Modern utilitarian style.
# Signature: round knot above the crown, clean shaved sides.
# ---------------------------------------------------------------------------
def hair_top_knot(canvas, color_key):
    h  = HAIR[color_key]
    hs = HAIR_SHADOW[color_key]
    hl = HAIR_LIGHT[color_key]

    # Signature: the knot itself (a small round bun on top, rows 3-5)
    paint(canvas, [(14, 3), (15, 3), (16, 3), (17, 3)], h)
    paint(canvas, [(13, 4), (14, 4), (15, 4), (16, 4), (17, 4), (18, 4)], h)
    paint(canvas, [(13, 5), (14, 5), (15, 5), (16, 5), (17, 5), (18, 5)], h)
    paint(canvas, [(14, 6), (15, 6), (16, 6), (17, 6)], h)

    # Knot highlight (light from upper left)
    paint(canvas, [(14, 3), (15, 3)], hl)
    paint(canvas, [(13, 4), (14, 4)], hl)
    # Knot shadow underneath
    paint(canvas, [(15, 6), (16, 6), (17, 6)], hs)
    paint(canvas, [(17, 5), (18, 5)], hs)

    # Top of head: hair pulled tight back into the knot (rows 7-8 thin layer)
    for x in range(11, 21): canvas.putpixel((x, 7), h)
    for x in range(11, 21): canvas.putpixel((x, 8), h)

    # Sheen lines pulling toward the knot
    paint(canvas, [(12, 7), (13, 7), (18, 7), (19, 7)], hl)
    paint(canvas, [(11, 8), (13, 8), (17, 8), (19, 8)], hs)

    # Shaved sides (dark band wrapping around temple)
    paint(canvas, [(10, 7), (10, 8), (10, 9), (10, 10), (10, 11), (10, 12),
                   (21, 7), (21, 8), (21, 9), (21, 10), (21, 11), (21, 12)], hs)
    # Hairline (clean, exposed forehead)
    paint(canvas, [(11, 9), (12, 9), (19, 9), (20, 9)], h)


# ---------------------------------------------------------------------------
# 13. MOHAWK
# Tall raised center strip running front-to-back. Shaved sides.
# Signature: vertical strip of hair from row 3 down, with bare temples.
# ---------------------------------------------------------------------------
def hair_mohawk(canvas, color_key):
    h  = HAIR[color_key]
    hs = HAIR_SHADOW[color_key]
    hl = HAIR_LIGHT[color_key]

    # The strip: tall center column of hair (cols 14-17, rows 3-9)
    # Tallest in the middle, tapered front and back
    paint(canvas, [(15, 3), (16, 3)], h)                               # peak
    paint(canvas, [(14, 4), (15, 4), (16, 4), (17, 4)], h)
    paint(canvas, [(14, 5), (15, 5), (16, 5), (17, 5)], h)
    paint(canvas, [(14, 6), (15, 6), (16, 6), (17, 6)], h)
    paint(canvas, [(13, 7), (14, 7), (15, 7), (16, 7), (17, 7), (18, 7)], h)  # base widens
    paint(canvas, [(13, 8), (14, 8), (15, 8), (16, 8), (17, 8), (18, 8)], h)
    paint(canvas, [(13, 9), (14, 9), (15, 9), (16, 9), (17, 9), (18, 9)], h)

    # Spiky front fringe pointing down the forehead
    paint(canvas, [(14, 10), (15, 10), (16, 10), (17, 10)], h)
    paint(canvas, [(15, 11), (16, 11)], h)

    # Highlights on the front facing edge of the strip
    paint(canvas, [(15, 3), (15, 4), (15, 5), (14, 6), (14, 7)], hl)

    # Shadows on the back of the strip (depth)
    paint(canvas, [(16, 4), (17, 4), (17, 5), (17, 6), (18, 7), (18, 8), (18, 9)], hs)

    # Shaved sides (very dark band at temples - skin shows above this)
    paint(canvas, [(11, 8), (12, 8), (19, 8), (20, 8)], hs)
    paint(canvas, [(11, 9), (12, 9), (19, 9), (20, 9)], hs)
    # A subtle stubble dotting on the shaved part
    paint(canvas, [(11, 10), (13, 10), (19, 10), (20, 10)], hs)


# ---------------------------------------------------------------------------
# 14. LOCS
# Vertical lock strands hanging down. Each strand is a distinct column.
# Signature: visible vertical separation between locks.
# ---------------------------------------------------------------------------
def hair_locs(canvas, color_key):
    h  = HAIR[color_key]
    hs = HAIR_SHADOW[color_key]
    hl = HAIR_LIGHT[color_key]

    # Crown (slightly tall, bunched locks at the top)
    paint(canvas, [(11, 5), (13, 5), (15, 5), (17, 5), (19, 5)], h)
    for x in range(10, 22): canvas.putpixel((x, 6), h)
    for x in range(10, 22): canvas.putpixel((x, 7), h)
    for x in range(10, 22): canvas.putpixel((x, 8), h)
    for x in range(10, 22): canvas.putpixel((x, 9), h)

    # Front hairline (textured, not smooth)
    paint(canvas, [(11, 10), (13, 10), (15, 10), (17, 10), (19, 10), (21, 10)], h)

    # Top highlights on the crown lock tips
    paint(canvas, [(11, 5), (15, 5)], hl)
    paint(canvas, [(12, 6), (16, 6)], hl)

    # Shadow gutters between top locks
    paint(canvas, [(12, 5), (14, 5), (16, 5), (18, 5), (20, 5)], hs)
    paint(canvas, [(12, 7), (14, 7), (16, 7), (18, 7), (20, 7)], hs)

    # Signature: vertical hanging locks, rows 10-22, in distinct columns
    # Each lock is its own column, with shadow gutters between
    lock_cols = [9, 11, 13, 15, 17, 19, 21]      # 7 hanging locks
    gutter_cols = [10, 12, 14, 16, 18, 20]       # shadow between locks

    for lc in lock_cols:
        for y in range(11, 24):
            if lc == 15:  # middle lock hidden behind face - only show ends
                if y < 11 or y > 22:
                    canvas.putpixel((lc, y), h)
                continue
            if lc in (11, 13, 17, 19) and 11 <= y <= 22:
                # interior locks blocked by face; skip
                continue
            canvas.putpixel((lc, y), h)

    # Outside locks (cols 9, 21) extend the full length
    for y in range(10, 25):
        canvas.putpixel((9, y), h)
        canvas.putpixel((21, y), h)
    # Outer outer locks (further out)
    for y in range(12, 24):
        canvas.putpixel((8, y), h)
        canvas.putpixel((22, y), h)

    # Shadow gutters between outer locks
    paint(canvas, [(8, 13), (8, 17), (8, 21)], hs)
    paint(canvas, [(22, 13), (22, 17), (22, 21)], hs)

    # Highlight stripes on a few locks
    paint(canvas, [(9, 14), (9, 19), (21, 14), (21, 19)], hl)

    # Lock tips (rounded ends at the bottom)
    paint(canvas, [(8, 24), (9, 25), (21, 25), (22, 24)], h)
    paint(canvas, [(8, 25), (22, 25)], hs)


# ---------------------------------------------------------------------------
# 15. BUN (low)
# Hair pulled back smooth, gathered into a low bun behind the head.
# Signature: round low bun visible to the side, neat smooth scalp.
# ---------------------------------------------------------------------------
def hair_bun(canvas, color_key):
    h  = HAIR[color_key]
    hs = HAIR_SHADOW[color_key]
    hl = HAIR_LIGHT[color_key]

    # Smooth crown pulled back tight
    for x in range(11, 21): canvas.putpixel((x, 6), h)
    for x in range(10, 22): canvas.putpixel((x, 7), h)
    for x in range(10, 22): canvas.putpixel((x, 8), h)
    for x in range(10, 22): canvas.putpixel((x, 9), h)

    # Center part (subtle, only at the very front)
    paint(canvas, [(15, 6), (15, 7)], hs)

    # Horizontal sheen pulling back toward the bun
    paint(canvas, [(12, 7), (14, 7), (18, 7), (20, 7)], hl)
    paint(canvas, [(11, 8), (13, 8), (17, 8), (19, 8), (21, 8)], hl)

    # Clean hairline at forehead (no fringe)
    paint(canvas, [(10, 10), (11, 10), (20, 10), (21, 10)], h)

    # Shadow at the hair / face transition
    paint(canvas, [(10, 11), (21, 11)], hs)

    # Hair flowing back along the sides of the head toward the bun
    paint(canvas, [(9, 11), (9, 12), (9, 13)], h)
    paint(canvas, [(22, 11), (22, 12), (22, 13)], h)

    # Signature: low bun behind the head (rows 13-19, cols 22-25, on the right
    # so it's visible against the head silhouette)
    # Bun body (round, ~3-wide blob)
    paint(canvas, [(23, 14), (24, 14), (25, 14)], h)
    paint(canvas, [(22, 15), (23, 15), (24, 15), (25, 15), (26, 15)], h)
    paint(canvas, [(22, 16), (23, 16), (24, 16), (25, 16), (26, 16)], h)
    paint(canvas, [(22, 17), (23, 17), (24, 17), (25, 17), (26, 17)], h)
    paint(canvas, [(23, 18), (24, 18), (25, 18)], h)

    # Bun highlight (light from upper left of the bun)
    paint(canvas, [(23, 14), (24, 14)], hl)
    paint(canvas, [(22, 15), (23, 15)], hl)

    # Bun shadow (right and bottom)
    paint(canvas, [(26, 16), (26, 17), (25, 18)], hs)

    # Wrap of hair around the bun (the tied band)
    paint(canvas, [(22, 16), (22, 17)], hs)

    # Small wisp escaping at the nape
    paint(canvas, [(21, 14), (21, 15)], h)


# ===========================================================================
# DICTIONARY
# ===========================================================================
HAIR_FNS_V2 = {
    "short_parted":  hair_short_parted,
    "slick_back":    hair_slick_back,
    "undercut":      hair_undercut,
    "messy":         hair_messy,
    "curly_short":   hair_curly_short,
    "long_straight": hair_long_straight,
    "long_wavy":     hair_long_wavy,
    "curly_long":    hair_curly_long,
    "fade":          hair_fade,
    "beach_blonde":  hair_long_blonde_beach,
    # New styles
    "ponytail":      hair_ponytail,
    "top_knot":      hair_top_knot,
    "mohawk":        hair_mohawk,
    "locs":          hair_locs,
    "bun":           hair_bun,
}
