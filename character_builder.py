#!/usr/bin/env python3
"""Procedural pixel art character builder v2.
32x32 base, hand-coded sprite parts, signature items per person.
Supports themes: corporate (default), aquatic, galaxy.
"""
from PIL import Image
import pathlib
import sys

SIZE = 32
SCALE = 18   # 32 * 18 = 576 final

# ============ PALETTES ============
SKIN = {
    "light":      (252, 224, 194),
    "light_warm": (245, 205, 170),
    "medium":     (220, 170, 135),
    "tan":        (200, 150, 110),
    "warm":       (230, 185, 145),
}
SKIN_SHADOW = {
    "light":      (220, 188, 158),
    "light_warm": (210, 170, 135),
    "medium":     (185, 138, 100),
    "tan":        (165, 118, 80),
    "warm":       (195, 148, 110),
}
SKIN_LIGHT = {
    "light":      (255, 235, 210),
    "light_warm": (252, 218, 188),
    "medium":     (232, 188, 155),
    "tan":        (215, 170, 130),
    "warm":       (242, 200, 165),
}
HAIR = {
    "blonde":  (235, 200, 130), "lblonde": (245, 215, 155),
    "lbrown":  (155, 110, 65),  "brown":   (110, 75, 45),
    "dbrown":  (75, 50, 30),    "black":   (40, 30, 25),
    "auburn":  (155, 85, 50),
}
HAIR_SHADOW = {
    "blonde":  (180, 145, 85),  "lblonde": (200, 165, 110),
    "lbrown":  (110, 75, 40),   "brown":   (75, 50, 30),
    "dbrown":  (50, 35, 20),    "black":   (25, 20, 15),
    "auburn":  (115, 60, 35),
}
HAIR_LIGHT = {
    "blonde":  (255, 225, 165), "lblonde": (255, 240, 195),
    "lbrown":  (190, 140, 90),  "brown":   (140, 95, 60),
    "dbrown":  (100, 70, 45),   "black":   (60, 50, 45),
    "auburn":  (190, 105, 65),
}
EYE = {
    "brown": (90, 60, 30), "blue":  (90, 145, 195),
    "green": (95, 140, 95), "hazel": (140, 105, 60),
}
LIP = (200, 130, 115)
LIP_SHADOW = (165, 100, 90)
TEETH = (255, 252, 245)
WHITE = (255, 255, 255)
BLACK = (10, 10, 10)
GOLD = (255, 200, 60)
GOLD_DARK = (180, 130, 35)
SILVER = (200, 200, 200)
GLOW = (180, 240, 255)


def paint(canvas, pixels, color):
    for x, y in pixels:
        if 0 <= x < SIZE and 0 <= y < SIZE:
            canvas.putpixel((x, y), color)


def fill_rect(canvas, x0, y0, x1, y1, color):
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            if 0 <= x < SIZE and 0 <= y < SIZE:
                canvas.putpixel((x, y), color)


def hex_to_rgb(h):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def mix(a, b, t):
    return (int(a[0] * (1-t) + b[0] * t), int(a[1] * (1-t) + b[1] * t), int(a[2] * (1-t) + b[2] * t))


# ============ BACKGROUND ============
def draw_background(canvas, trait_hex, theme="corporate"):
    trait = hex_to_rgb(trait_hex)
    # Dark muted base derived from trait
    base = mix(trait, (8, 12, 20), 0.78)
    fill_rect(canvas, 0, 0, SIZE-1, SIZE-1, base)

    if theme == "corporate":
        # Subtle dot grid (every 4 pixels)
        dot = mix(base, trait, 0.18)
        for x in range(2, SIZE, 4):
            for y in range(2, SIZE, 4):
                canvas.putpixel((x, y), dot)
        # Corner brackets in trait color
        for i in range(3):
            canvas.putpixel((0, i), trait); canvas.putpixel((i, 0), trait)
            canvas.putpixel((SIZE-1-i, 0), trait); canvas.putpixel((SIZE-1, i), trait)
            canvas.putpixel((0, SIZE-1-i), trait); canvas.putpixel((i, SIZE-1), trait)
            canvas.putpixel((SIZE-1-i, SIZE-1), trait); canvas.putpixel((SIZE-1, SIZE-1-i), trait)


# ============ HEAD ============
def draw_head(canvas, skin_key, face_shape="oval"):
    s = SKIN[skin_key]
    ss = SKIN_SHADOW[skin_key]
    sl = SKIN_LIGHT[skin_key]

    # Face cols 10-21 (12 wide), rows 9-25 (17 rows)
    if face_shape == "oval":
        # Top of head curve
        for x in range(12, 20): canvas.putpixel((x, 9), s)
        for x in range(11, 21): canvas.putpixel((x, 10), s)
        # Face body (full width)
        fill_rect(canvas, 10, 11, 21, 22, s)
        # Jaw narrow
        for x in range(11, 21): canvas.putpixel((x, 23), s)
        for x in range(12, 20): canvas.putpixel((x, 24), s)
        for x in range(13, 19): canvas.putpixel((x, 25), s)
    elif face_shape == "round":
        for x in range(12, 20): canvas.putpixel((x, 9), s)
        for x in range(11, 21): canvas.putpixel((x, 10), s)
        fill_rect(canvas, 10, 11, 21, 23, s)
        for x in range(11, 21): canvas.putpixel((x, 24), s)
        for x in range(12, 20): canvas.putpixel((x, 25), s)
    elif face_shape == "square":
        for x in range(11, 21): canvas.putpixel((x, 9), s)
        fill_rect(canvas, 10, 10, 21, 24, s)
        for x in range(11, 21): canvas.putpixel((x, 25), s)
    elif face_shape == "long":
        for x in range(13, 19): canvas.putpixel((x, 9), s)
        for x in range(12, 20): canvas.putpixel((x, 10), s)
        fill_rect(canvas, 11, 11, 20, 25, s)
        for x in range(12, 20): canvas.putpixel((x, 26), s)

    # Right side jaw shadow for depth
    paint(canvas, [(20, 13), (20, 14), (20, 15), (20, 16), (20, 17), (20, 18), (20, 19), (20, 20), (20, 21)], ss)
    # Left side soft highlight
    paint(canvas, [(11, 13), (11, 14), (11, 15)], sl)
    # Cheek shadow (softens under cheekbone)
    paint(canvas, [(12, 21), (19, 21)], ss)

    # Ears
    paint(canvas, [(9, 16), (9, 17), (9, 18)], ss)
    paint(canvas, [(22, 16), (22, 17), (22, 18)], ss)
    paint(canvas, [(10, 17)], s)
    paint(canvas, [(21, 17)], s)

    # Neck
    fill_rect(canvas, 13, 26, 18, 28, s)
    paint(canvas, [(13, 27), (13, 28)], ss)  # neck shadow


# ============ EYES ============
def draw_eyes(canvas, color_key, eye_shape="normal"):
    e = EYE[color_key]
    if eye_shape == "normal":
        # Whites
        paint(canvas, [(12, 16), (13, 16), (14, 16)], WHITE)
        paint(canvas, [(17, 16), (18, 16), (19, 16)], WHITE)
        # Iris
        paint(canvas, [(13, 16)], e)
        paint(canvas, [(18, 16)], e)
        # Pupil + highlight
        paint(canvas, [(13, 16)], mix(e, BLACK, 0.5))
        canvas.putpixel((14, 15), WHITE)  # eye highlight
        canvas.putpixel((19, 15), WHITE)
    elif eye_shape == "wide":
        paint(canvas, [(12, 16), (13, 16), (14, 16)], WHITE)
        paint(canvas, [(17, 16), (18, 16), (19, 16)], WHITE)
        paint(canvas, [(12, 17), (13, 17), (14, 17)], WHITE)
        paint(canvas, [(17, 17), (18, 17), (19, 17)], WHITE)
        paint(canvas, [(13, 16), (13, 17)], e)
        paint(canvas, [(18, 16), (18, 17)], e)
    elif eye_shape == "narrow":
        paint(canvas, [(12, 16), (13, 16), (14, 16)], mix(e, BLACK, 0.7))
        paint(canvas, [(17, 16), (18, 16), (19, 16)], mix(e, BLACK, 0.7))


def draw_eyebrows(canvas, hair_color_key, style="straight"):
    b = HAIR_SHADOW[hair_color_key]
    if style == "straight":
        paint(canvas, [(12, 14), (13, 14), (14, 14)], b)
        paint(canvas, [(17, 14), (18, 14), (19, 14)], b)
    elif style == "thick":
        paint(canvas, [(11, 14), (12, 14), (13, 14), (14, 14), (15, 14)], b)
        paint(canvas, [(16, 14), (17, 14), (18, 14), (19, 14), (20, 14)], b)
    elif style == "arched":
        paint(canvas, [(12, 14), (13, 13), (14, 14)], b)
        paint(canvas, [(17, 14), (18, 13), (19, 14)], b)


# ============ NOSE ============
def draw_nose(canvas, skin_key, style="standard"):
    ss = SKIN_SHADOW[skin_key]
    if style == "standard":
        paint(canvas, [(15, 18), (15, 19), (15, 20)], ss)
        paint(canvas, [(16, 20)], ss)
    elif style == "wide":
        paint(canvas, [(14, 19), (15, 19), (16, 19)], ss)
        paint(canvas, [(14, 20), (16, 20)], ss)
    elif style == "subtle":
        paint(canvas, [(15, 20)], ss)


# ============ MOUTH ============
def draw_mouth(canvas, kind, skin_key=None):
    if kind == "smile":
        paint(canvas, [(13, 23), (14, 23), (15, 23), (16, 23), (17, 23), (18, 23)], LIP)
        paint(canvas, [(14, 24), (15, 24), (16, 24), (17, 24)], LIP_SHADOW)
    elif kind == "grin":
        paint(canvas, [(13, 23), (14, 23), (15, 23), (16, 23), (17, 23), (18, 23)], BLACK)
        paint(canvas, [(14, 24), (15, 24), (16, 24), (17, 24)], TEETH)
        paint(canvas, [(13, 24), (18, 24)], LIP_SHADOW)
    elif kind == "big_grin":
        paint(canvas, [(12, 23), (13, 23), (14, 23), (15, 23), (16, 23), (17, 23), (18, 23), (19, 23)], BLACK)
        paint(canvas, [(13, 24), (14, 24), (15, 24), (16, 24), (17, 24), (18, 24)], TEETH)
        paint(canvas, [(15, 25), (16, 25)], LIP_SHADOW)
    elif kind == "smirk":
        paint(canvas, [(14, 23), (15, 23), (16, 23), (17, 23)], LIP)
        paint(canvas, [(18, 22), (17, 22)], LIP_SHADOW)
    elif kind == "neutral":
        paint(canvas, [(14, 23), (15, 23), (16, 23), (17, 23)], LIP_SHADOW)


# ============ BEARD ============
def draw_beard(canvas, kind, hair_color_key):
    if kind == "none": return
    h = HAIR[hair_color_key]
    hs = HAIR_SHADOW[hair_color_key]
    if kind == "stubble":
        # Scattered shadow dots
        for x, y in [(12, 22), (14, 22), (16, 22), (18, 22), (13, 25), (15, 25), (17, 25), (11, 23), (19, 23)]:
            canvas.putpixel((x, y), mix(canvas.getpixel((x, y)), hs, 0.5))
    elif kind == "scruff":
        paint(canvas, [(11, 22), (12, 22), (18, 22), (19, 22)], hs)
        paint(canvas, [(11, 23), (12, 23), (18, 23), (19, 23)], hs)
        paint(canvas, [(12, 24), (13, 24), (17, 24), (18, 24)], hs)
        paint(canvas, [(13, 25), (14, 25), (16, 25), (17, 25)], hs)
    elif kind == "full":
        for x in range(11, 20):
            canvas.putpixel((x, 22), h)
            canvas.putpixel((x, 23), h)
            canvas.putpixel((x, 24), h)
        for x in range(12, 19):
            canvas.putpixel((x, 25), h)
        # Mouth slot
        paint(canvas, [(14, 23), (15, 23), (16, 23), (17, 23)], hs)
    elif kind == "mustache":
        paint(canvas, [(13, 22), (14, 22), (15, 22), (16, 22), (17, 22), (18, 22)], h)


# ============ HAIR ============
def hair_short_parted(canvas, color_key):
    h = HAIR[color_key]; hs = HAIR_SHADOW[color_key]; hl = HAIR_LIGHT[color_key]
    # Top dome
    for x in range(11, 21): canvas.putpixel((x, 7), h)
    for x in range(10, 22): canvas.putpixel((x, 8), h)
    for x in range(10, 22): canvas.putpixel((x, 9), h)
    # Forehead front sweep
    for x in range(11, 21): canvas.putpixel((x, 10), h)
    # Part line (right side)
    paint(canvas, [(16, 7), (16, 8), (16, 9), (17, 9), (17, 10)], hs)
    # Highlight
    paint(canvas, [(12, 7), (13, 7), (12, 8)], hl)
    # Side covering ears partially
    paint(canvas, [(10, 10), (10, 11), (10, 12), (21, 10), (21, 11), (21, 12)], h)
    paint(canvas, [(9, 11), (22, 11)], h)


def hair_slick_back(canvas, color_key):
    h = HAIR[color_key]; hs = HAIR_SHADOW[color_key]; hl = HAIR_LIGHT[color_key]
    for x in range(11, 21): canvas.putpixel((x, 7), h)
    for x in range(10, 22): canvas.putpixel((x, 8), h)
    for x in range(10, 22): canvas.putpixel((x, 9), h)
    # Slick lines back
    paint(canvas, [(12, 7), (14, 7), (16, 7), (18, 7), (20, 7)], hl)
    paint(canvas, [(13, 8), (15, 8), (17, 8), (19, 8)], hs)
    # Forehead exposed (no front sweep)
    paint(canvas, [(10, 10), (21, 10), (10, 11), (21, 11), (10, 12), (21, 12)], h)


def hair_undercut(canvas, color_key):
    h = HAIR[color_key]; hs = HAIR_SHADOW[color_key]; hl = HAIR_LIGHT[color_key]
    # Tall top
    for x in range(11, 20): canvas.putpixel((x, 5), h)
    for x in range(10, 21): canvas.putpixel((x, 6), h)
    for x in range(10, 21): canvas.putpixel((x, 7), h)
    for x in range(10, 21): canvas.putpixel((x, 8), h)
    # Buzz sides (shadow)
    paint(canvas, [(10, 9), (10, 10), (10, 11), (10, 12), (21, 9), (21, 10), (21, 11), (21, 12)], hs)
    # Top highlight
    paint(canvas, [(13, 5), (14, 5), (15, 5)], hl)
    paint(canvas, [(13, 6), (15, 6), (17, 6)], hl)
    # Front
    paint(canvas, [(13, 9), (14, 9), (15, 9)], h)


def hair_messy(canvas, color_key):
    h = HAIR[color_key]; hs = HAIR_SHADOW[color_key]; hl = HAIR_LIGHT[color_key]
    # Spikes/tufts
    paint(canvas, [(11, 5), (14, 5), (17, 5), (20, 5)], h)
    paint(canvas, [(10, 6), (11, 6), (12, 6), (14, 6), (15, 6), (17, 6), (18, 6), (20, 6), (21, 6)], h)
    for x in range(10, 22): canvas.putpixel((x, 7), h)
    for x in range(10, 22): canvas.putpixel((x, 8), h)
    for x in range(10, 22): canvas.putpixel((x, 9), h)
    paint(canvas, [(11, 6), (15, 6), (18, 6)], hl)
    paint(canvas, [(12, 8), (16, 8), (19, 8)], hs)
    paint(canvas, [(10, 10), (10, 11), (21, 10), (21, 11)], h)


def hair_curly_short(canvas, color_key):
    h = HAIR[color_key]; hs = HAIR_SHADOW[color_key]
    # Curl bumps
    paint(canvas, [(11, 5), (13, 5), (15, 5), (17, 5), (19, 5)], h)
    paint(canvas, [(10, 6), (11, 6), (12, 6), (13, 6), (14, 6), (15, 6), (16, 6), (17, 6), (18, 6), (19, 6), (20, 6), (21, 6)], h)
    paint(canvas, [(11, 6), (14, 6), (17, 6), (20, 6)], hs)
    for x in range(10, 22): canvas.putpixel((x, 7), h)
    for x in range(10, 22): canvas.putpixel((x, 8), h)
    paint(canvas, [(11, 7), (14, 7), (17, 7), (20, 7)], hs)
    for x in range(10, 22): canvas.putpixel((x, 9), h)
    paint(canvas, [(13, 9), (16, 9), (19, 9)], hs)
    paint(canvas, [(10, 10), (10, 11), (21, 10), (21, 11)], h)


def hair_long_straight(canvas, color_key):
    h = HAIR[color_key]; hs = HAIR_SHADOW[color_key]; hl = HAIR_LIGHT[color_key]
    # Crown
    for x in range(11, 21): canvas.putpixel((x, 6), h)
    for x in range(10, 22): canvas.putpixel((x, 7), h)
    for x in range(9, 23): canvas.putpixel((x, 8), h)
    for x in range(9, 23): canvas.putpixel((x, 9), h)
    # Part center
    paint(canvas, [(15, 6), (15, 7), (15, 8)], hs)
    # Highlights
    paint(canvas, [(12, 7), (18, 7)], hl)
    # Long sides past shoulders
    for y in range(10, 26):
        canvas.putpixel((9, y), h)
        canvas.putpixel((22, y), h)
    for y in range(11, 26):
        canvas.putpixel((8, y), hs)
        canvas.putpixel((23, y), hs)
    # Hair past shoulders flows
    paint(canvas, [(8, 26), (9, 26), (22, 26), (23, 26)], h)
    paint(canvas, [(7, 24), (7, 25), (24, 24), (24, 25)], hs)


def hair_long_wavy(canvas, color_key):
    h = HAIR[color_key]; hs = HAIR_SHADOW[color_key]; hl = HAIR_LIGHT[color_key]
    # Crown with slight waves
    for x in range(11, 21): canvas.putpixel((x, 6), h)
    for x in range(10, 22): canvas.putpixel((x, 7), h)
    for x in range(9, 23): canvas.putpixel((x, 8), h)
    for x in range(9, 23): canvas.putpixel((x, 9), h)
    paint(canvas, [(15, 6), (15, 7)], hs)
    paint(canvas, [(12, 7), (13, 7), (18, 7), (19, 7)], hl)
    # Wavy long sides
    waves_l = [(9, 10), (9, 11), (8, 12), (9, 13), (9, 14), (8, 15), (9, 16), (9, 17), (8, 18), (9, 19), (9, 20), (8, 21), (9, 22), (9, 23), (8, 24), (9, 25), (9, 26)]
    waves_r = [(22, 10), (22, 11), (23, 12), (22, 13), (22, 14), (23, 15), (22, 16), (22, 17), (23, 18), (22, 19), (22, 20), (23, 21), (22, 22), (22, 23), (23, 24), (22, 25), (22, 26)]
    paint(canvas, waves_l, h)
    paint(canvas, waves_r, h)
    paint(canvas, [(7, 13), (7, 18), (7, 23), (24, 13), (24, 18), (24, 23)], hs)
    paint(canvas, [(7, 26), (24, 26)], h)


def hair_curly_long(canvas, color_key):
    h = HAIR[color_key]; hs = HAIR_SHADOW[color_key]; hl = HAIR_LIGHT[color_key]
    # Tall curly volume
    paint(canvas, [(10, 4), (12, 4), (14, 4), (16, 4), (18, 4), (20, 4)], h)
    for x in range(9, 23): canvas.putpixel((x, 5), h)
    for x in range(8, 24): canvas.putpixel((x, 6), h)
    paint(canvas, [(9, 5), (12, 5), (15, 5), (18, 5), (21, 5)], hs)
    for x in range(8, 24): canvas.putpixel((x, 7), h)
    for x in range(8, 24): canvas.putpixel((x, 8), h)
    for x in range(9, 23): canvas.putpixel((x, 9), h)
    paint(canvas, [(11, 6), (15, 6), (19, 6)], hl)
    paint(canvas, [(10, 7), (14, 7), (18, 7), (22, 7)], hs)
    # Sides
    for y in range(10, 22):
        canvas.putpixel((9, y), h)
        canvas.putpixel((22, y), h)
    paint(canvas, [(8, 12), (8, 16), (8, 20), (23, 12), (23, 16), (23, 20)], h)


def hair_fade(canvas, color_key):
    h = HAIR[color_key]; hs = HAIR_SHADOW[color_key]; hl = HAIR_LIGHT[color_key]
    # Top high and tight
    for x in range(11, 20): canvas.putpixel((x, 6), h)
    for x in range(10, 21): canvas.putpixel((x, 7), h)
    for x in range(10, 21): canvas.putpixel((x, 8), h)
    for x in range(11, 20): canvas.putpixel((x, 9), h)
    paint(canvas, [(12, 6), (15, 6), (18, 6)], hl)
    # Fade out at sides (lighter shadow)
    paint(canvas, [(10, 9), (21, 9), (10, 10), (21, 10)], hs)
    paint(canvas, [(10, 11), (21, 11)], mix(hs, SKIN["light"], 0.3))


def hair_long_blonde_beach(canvas, color_key):
    """Beachy waves with sun highlights, for the surfer types."""
    h = HAIR[color_key]; hs = HAIR_SHADOW[color_key]; hl = HAIR_LIGHT[color_key]
    for x in range(11, 21): canvas.putpixel((x, 6), h)
    for x in range(10, 22): canvas.putpixel((x, 7), h)
    for x in range(9, 23): canvas.putpixel((x, 8), h)
    for x in range(9, 23): canvas.putpixel((x, 9), h)
    paint(canvas, [(15, 7)], hs)
    paint(canvas, [(12, 7), (14, 7), (18, 7), (20, 7)], hl)
    # Flowing long sides (sunlit streaks)
    for y in range(10, 25):
        canvas.putpixel((9, y), h)
        canvas.putpixel((22, y), h)
    for y in range(11, 25):
        canvas.putpixel((8, y), h)
        canvas.putpixel((23, y), h)
    # Highlight streaks (vertical, not alternating)
    paint(canvas, [(9, 12), (9, 13), (9, 17), (9, 18), (9, 22), (9, 23)], hl)
    paint(canvas, [(22, 12), (22, 13), (22, 17), (22, 18), (22, 22), (22, 23)], hl)
    paint(canvas, [(8, 24), (23, 24)], hs)


HAIR_FNS = {
    "short_parted": hair_short_parted,
    "slick_back":   hair_slick_back,
    "undercut":     hair_undercut,
    "messy":        hair_messy,
    "curly_short":  hair_curly_short,
    "long_straight":hair_long_straight,
    "long_wavy":    hair_long_wavy,
    "curly_long":   hair_curly_long,
    "fade":         hair_fade,
    "beach_blonde": hair_long_blonde_beach,
}


# ============ CLOTHES ============
def draw_shirt(canvas, kind, color_main, accent=None):
    """Shirt occupies rows 28-31, cols 5-26."""
    fill_rect(canvas, 5, 28, 26, 31, color_main)
    fill_rect(canvas, 7, 27, 24, 27, color_main)

    if kind == "suit_tie":
        # White shirt v
        paint(canvas, [(14, 27), (15, 27), (16, 27), (17, 27)], WHITE)
        paint(canvas, [(15, 28), (16, 28)], WHITE)
        # Tie
        tie_color = accent or (60, 90, 160)
        paint(canvas, [(15, 28), (16, 28)], tie_color)
        paint(canvas, [(15, 29), (16, 29), (15, 30), (16, 30), (15, 31), (16, 31)], tie_color)
        # Tie pattern (dots)
        paint(canvas, [(15, 29), (16, 30)], mix(tie_color, WHITE, 0.4))
    elif kind == "blazer_open":
        paint(canvas, [(13, 27), (14, 27), (15, 27), (16, 27), (17, 27), (18, 27)], WHITE)
        paint(canvas, [(14, 28), (15, 28), (16, 28), (17, 28)], WHITE)
        paint(canvas, [(15, 29), (16, 29)], WHITE)
        # Lapels
        paint(canvas, [(13, 28), (18, 28)], mix(color_main, BLACK, 0.3))
    elif kind == "polo":
        # Collar
        paint(canvas, [(13, 27), (14, 27), (17, 27), (18, 27)], color_main)
        paint(canvas, [(15, 27), (16, 27)], mix(color_main, WHITE, 0.2))
        # Placket
        paint(canvas, [(15, 28), (16, 28)], mix(color_main, BLACK, 0.3))
        paint(canvas, [(15, 29), (15, 30)], mix(color_main, BLACK, 0.3))
        # Buttons
        paint(canvas, [(15, 29)], WHITE)
        paint(canvas, [(15, 30)], WHITE)
    elif kind == "sweater":
        # Crew neck
        paint(canvas, [(14, 27), (15, 27), (16, 27), (17, 27)], mix(color_main, BLACK, 0.4))
        # Knit pattern (subtle texture)
        for x in range(5, 27, 2):
            canvas.putpixel((x, 29), mix(color_main, WHITE, 0.1))
        for x in range(6, 27, 2):
            canvas.putpixel((x, 30), mix(color_main, BLACK, 0.15))
    elif kind == "button_up":
        # Collar wings
        paint(canvas, [(12, 27), (13, 27), (19, 27), (20, 27)], color_main)
        paint(canvas, [(14, 27), (15, 27), (16, 27), (17, 27)], mix(color_main, WHITE, 0.15))
        # Button line center
        paint(canvas, [(15, 28), (15, 29), (15, 30), (15, 31)], mix(color_main, BLACK, 0.2))
        paint(canvas, [(15, 29), (15, 31)], mix(color_main, WHITE, 0.3))  # buttons
    elif kind == "zip_up":
        # Zipper
        paint(canvas, [(15, 27), (16, 27)], mix(color_main, BLACK, 0.5))
        paint(canvas, [(15, 28), (16, 28), (15, 29), (16, 29), (15, 30), (16, 30), (15, 31), (16, 31)], mix(color_main, BLACK, 0.5))
        paint(canvas, [(15, 28), (15, 29), (15, 30), (15, 31)], SILVER)
    elif kind == "hoodie":
        # Hood drape
        paint(canvas, [(11, 27), (12, 27), (19, 27), (20, 27)], color_main)
        paint(canvas, [(13, 27), (14, 27), (17, 27), (18, 27)], mix(color_main, BLACK, 0.3))
        # Drawstrings
        paint(canvas, [(14, 29), (17, 29)], WHITE)
        paint(canvas, [(14, 30), (17, 30)], WHITE)
    elif kind == "tshirt":
        paint(canvas, [(14, 27), (15, 27), (16, 27), (17, 27)], mix(color_main, BLACK, 0.3))


# ============ SIGNATURE ITEMS ============
def sig_pocket_square(canvas, color):
    paint(canvas, [(9, 30), (10, 30)], color)
    paint(canvas, [(9, 31)], color)


def sig_necklace_gold(canvas):
    paint(canvas, [(13, 27), (14, 28), (16, 28), (17, 27)], GOLD_DARK)
    paint(canvas, [(15, 28), (15, 29)], GOLD)


def sig_headset(canvas):
    # Headset band over head
    paint(canvas, [(11, 8), (11, 9), (12, 7), (19, 7), (20, 8), (20, 9)], BLACK)
    # Earpiece
    paint(canvas, [(9, 17), (9, 18), (9, 19)], BLACK)
    paint(canvas, [(10, 18)], BLACK)
    # Mic arm
    paint(canvas, [(10, 19), (10, 20), (10, 21), (11, 21)], BLACK)
    paint(canvas, [(12, 21)], (255, 100, 100))  # mic tip red


def sig_watch(canvas):
    # Subtle band on right shoulder edge
    paint(canvas, [(25, 30), (26, 30), (25, 31), (26, 31)], SILVER)
    paint(canvas, [(25, 30)], (50, 50, 60))


def sig_question_mark(canvas, color):
    # Floating ? above head
    paint(canvas, [(15, 2), (16, 2), (17, 2)], color)
    paint(canvas, [(17, 3)], color)
    paint(canvas, [(16, 4)], color)
    paint(canvas, [(16, 6)], color)


def sig_pint_glass(canvas):
    # Pint glass to left of head
    paint(canvas, [(3, 15), (4, 15), (3, 21), (4, 21)], SILVER)
    paint(canvas, [(3, 16), (3, 17), (3, 18), (3, 19), (3, 20)], (60, 30, 15))  # beer dark
    paint(canvas, [(4, 16), (4, 17), (4, 18), (4, 19), (4, 20)], (90, 50, 25))
    paint(canvas, [(3, 15), (4, 15)], (255, 250, 230))  # foam


def sig_crown(canvas, color):
    # Small crown above hair
    paint(canvas, [(14, 3), (16, 3), (18, 3)], color)
    paint(canvas, [(14, 4), (15, 4), (16, 4), (17, 4), (18, 4)], color)
    paint(canvas, [(15, 3)], mix(color, BLACK, 0.3))


def sig_chain(canvas):
    # Gold chain on neck
    paint(canvas, [(13, 27), (14, 28), (15, 28), (16, 28), (17, 28), (18, 27)], GOLD)
    paint(canvas, [(14, 28), (17, 28)], GOLD_DARK)
    # Pendant (medallion)
    paint(canvas, [(15, 29), (16, 29)], GOLD)
    paint(canvas, [(15, 29)], GOLD_DARK)


def sig_ai_agent(canvas, color):
    # Glowing orb on shoulder (the AI companion)
    paint(canvas, [(25, 26), (25, 27), (26, 25), (26, 26), (26, 27), (26, 28), (27, 26), (27, 27)], color)
    paint(canvas, [(26, 26)], WHITE)  # highlight
    # Ring/halo glow
    paint(canvas, [(25, 25), (27, 25), (25, 28), (27, 28)], mix(color, WHITE, 0.4))
    # Sparkle
    canvas.putpixel((29, 24), WHITE)
    canvas.putpixel((24, 24), color)


def sig_cross_necklace(canvas):
    # Small silver cross
    paint(canvas, [(15, 28)], SILVER)
    paint(canvas, [(14, 29), (15, 29), (16, 29)], SILVER)
    paint(canvas, [(15, 30)], SILVER)


def sig_surfboard(canvas):
    # Surfboard behind right shoulder peeking
    fill_rect(canvas, 26, 18, 27, 28, (240, 240, 240))
    paint(canvas, [(26, 18), (27, 28)], (200, 200, 200))
    paint(canvas, [(26, 22)], (255, 80, 80))  # stripe


def sig_bt_pin(canvas, color):
    # Big BT pin (existing but scaled up)
    paint(canvas, [(7, 29), (8, 29), (9, 29), (7, 30), (9, 30), (7, 31), (8, 31), (9, 31)], color)
    paint(canvas, [(8, 30)], BLACK)  # inner B-T mark spot


def sig_earring(canvas):
    # Small gold earring
    canvas.putpixel((9, 19), GOLD)


def sig_headphones(canvas, color=BLACK):
    # Over-ear headphones
    paint(canvas, [(11, 8), (12, 8), (19, 8), (20, 8)], color)
    paint(canvas, [(11, 9), (20, 9)], color)
    # Earcups
    paint(canvas, [(8, 16), (8, 17), (8, 18), (9, 16), (9, 17), (9, 18)], color)
    paint(canvas, [(23, 16), (23, 17), (23, 18), (22, 16), (22, 17), (22, 18)], color)


def sig_cap(canvas, color):
    # Snapback brim
    for x in range(5, 18): canvas.putpixel((x, 10), color)
    for x in range(5, 19): canvas.putpixel((x, 9), color)
    # Crown
    for x in range(10, 22): canvas.putpixel((x, 6), color)
    for x in range(10, 22): canvas.putpixel((x, 7), color)
    for x in range(10, 22): canvas.putpixel((x, 8), color)
    # Front logo dot
    paint(canvas, [(15, 7), (16, 7)], WHITE)


# ============ HEAD ACCESSORIES (drawn LAST, over face) ============
def acc_sunglasses(canvas):
    # Black wayfarers
    paint(canvas, [(11, 15), (12, 15), (13, 15), (14, 15), (15, 15), (16, 15), (17, 15), (18, 15), (19, 15), (20, 15)], BLACK)
    fill_rect(canvas, 11, 16, 14, 17, BLACK)
    fill_rect(canvas, 17, 16, 20, 17, BLACK)
    paint(canvas, [(15, 16), (16, 16)], BLACK)
    # Highlight glint
    paint(canvas, [(12, 16), (18, 16)], (60, 60, 80))


def acc_aviators(canvas):
    # Teardrop frame
    paint(canvas, [(11, 15), (12, 15), (13, 15), (14, 15), (15, 15), (17, 15), (18, 15), (19, 15), (20, 15)], (60, 60, 70))
    paint(canvas, [(11, 16), (14, 16), (17, 16), (20, 16)], (60, 60, 70))
    # Lens tint (gold/brown gradient)
    fill_rect(canvas, 12, 16, 13, 17, (100, 75, 40))
    fill_rect(canvas, 18, 16, 19, 17, (100, 75, 40))
    paint(canvas, [(12, 16), (18, 16)], (180, 140, 80))  # highlight
    paint(canvas, [(12, 17), (13, 17), (18, 17), (19, 17)], (80, 60, 35))
    # Bridge
    paint(canvas, [(15, 16), (16, 16)], (60, 60, 70))


def acc_glasses_clear(canvas):
    # Thin clear/black frames
    paint(canvas, [(11, 15), (14, 15), (17, 15), (20, 15)], BLACK)
    paint(canvas, [(11, 16), (14, 16), (17, 16), (20, 16)], BLACK)
    paint(canvas, [(11, 17), (12, 17), (13, 17), (14, 17), (17, 17), (18, 17), (19, 17), (20, 17)], BLACK)
    paint(canvas, [(15, 16), (16, 16)], BLACK)  # bridge


def acc_ar_smart_glasses(canvas, color):
    # Cyber/AR glasses (thin frame with cyan glow)
    paint(canvas, [(11, 15), (12, 15), (13, 15), (14, 15), (15, 15), (16, 15), (17, 15), (18, 15), (19, 15), (20, 15)], (40, 40, 50))
    fill_rect(canvas, 12, 16, 13, 16, mix(color, WHITE, 0.3))
    fill_rect(canvas, 18, 16, 19, 16, mix(color, WHITE, 0.3))
    paint(canvas, [(13, 16), (19, 16)], WHITE)  # AR highlight
    paint(canvas, [(15, 16), (16, 16)], (40, 40, 50))


def acc_laser_eyes(canvas, color=(255, 50, 50)):
    # Beams shooting out of eyes horizontally
    paint(canvas, [(13, 16), (18, 16)], color)
    # Glow trail outward
    for x in range(0, 12):
        canvas.putpixel((x, 16), mix(color, hex_to_rgb("#050709"), 0.3))
    for x in range(19, SIZE):
        canvas.putpixel((x, 16), mix(color, hex_to_rgb("#050709"), 0.3))
    # Inner glow
    paint(canvas, [(13, 15), (18, 15)], mix(color, WHITE, 0.6))


def acc_earbuds(canvas):
    # Small white pods in ears
    paint(canvas, [(9, 17)], WHITE)
    paint(canvas, [(22, 17)], WHITE)
    # Stem hint
    paint(canvas, [(9, 18)], (220, 220, 220))
    paint(canvas, [(22, 18)], (220, 220, 220))


def acc_beanie(canvas, color):
    # Knit beanie covering top of head
    for x in range(10, 22):
        for y in range(5, 9):
            canvas.putpixel((x, y), color)
    paint(canvas, [(11, 5), (13, 5), (15, 5), (17, 5), (19, 5)], mix(color, BLACK, 0.3))
    # Cuff line
    for x in range(9, 23): canvas.putpixel((x, 9), mix(color, BLACK, 0.4))
    for x in range(9, 23): canvas.putpixel((x, 10), color)


def acc_red_lips(canvas):
    # Replace existing lip with red
    paint(canvas, [(13, 23), (14, 23), (15, 23), (16, 23), (17, 23), (18, 23)], (200, 40, 60))
    paint(canvas, [(14, 24), (15, 24), (16, 24), (17, 24)], (150, 30, 45))


def acc_earring_stud(canvas):
    # Gold stud earring on left ear, larger than the signature dot
    paint(canvas, [(9, 18), (9, 19)], GOLD)
    canvas.putpixel((9, 19), GOLD_DARK)


def acc_party_horn(canvas, color):
    # Cone shape coming out of mouth right side
    paint(canvas, [(19, 22), (20, 22), (21, 21)], color)
    paint(canvas, [(22, 20), (23, 20)], color)
    paint(canvas, [(24, 19)], mix(color, WHITE, 0.5))


# ============ THEME OVERLAYS ============
def theme_aquatic(canvas, trait_hex, person=None):
    """Submerge: wave gradient BG, bubbles, seaweed, fish, gills, wet hair, snorkel for some."""
    trait = hex_to_rgb(trait_hex)
    deep = (8, 20, 45)
    mid = (15, 50, 90)
    shallow = (35, 100, 145)
    bubble_color = (200, 230, 245)
    bubble_dim = (140, 180, 210)
    seaweed = (40, 110, 70)
    seaweed_dark = (25, 80, 50)
    fish_color = (220, 180, 120)
    fish_accent = (200, 120, 80)

    # Wave gradient BG (light at top to dark at bottom)
    for y in range(SIZE):
        if y < 8:
            row_color = mix(shallow, mid, y / 8)
        elif y < 20:
            row_color = mix(mid, deep, (y - 8) / 12)
        else:
            row_color = deep
        for x in range(SIZE):
            # Only paint over the original dark navy bg pixels (not character)
            current = canvas.getpixel((x, y))
            if current == mix(trait, (8, 12, 20), 0.78) or sum(current) < 100:
                canvas.putpixel((x, y), row_color)

    # Refresh corner brackets and dot grid in trait color over new bg
    for i in range(3):
        canvas.putpixel((0, i), trait); canvas.putpixel((i, 0), trait)
        canvas.putpixel((SIZE-1-i, 0), trait); canvas.putpixel((SIZE-1, i), trait)
        canvas.putpixel((0, SIZE-1-i), trait); canvas.putpixel((i, SIZE-1), trait)
        canvas.putpixel((SIZE-1-i, SIZE-1), trait); canvas.putpixel((SIZE-1, SIZE-1-i), trait)

    # Seaweed strands (left + right edges)
    for y in range(18, SIZE):
        canvas.putpixel((0, y), seaweed_dark)
        canvas.putpixel((SIZE-1, y), seaweed_dark)
    # Wavy seaweed at bottom (varied)
    for x, y in [(1, 22), (1, 24), (1, 26), (1, 28), (2, 23), (2, 25), (2, 27)]:
        canvas.putpixel((x, y), seaweed)
    for x, y in [(SIZE-2, 23), (SIZE-2, 25), (SIZE-2, 27), (SIZE-3, 22), (SIZE-3, 24), (SIZE-3, 26)]:
        canvas.putpixel((x, y), seaweed)

    # Background fish (silhouette swimming)
    # Fish 1 top-right
    paint(canvas, [(26, 5), (27, 5), (28, 5), (29, 5)], fish_color)
    paint(canvas, [(28, 4), (28, 6)], fish_color)
    paint(canvas, [(30, 4), (30, 6)], fish_color)
    canvas.putpixel((27, 5), BLACK)  # eye
    # Fish 2 left-middle, smaller
    paint(canvas, [(2, 13), (3, 13), (4, 13)], fish_accent)
    paint(canvas, [(1, 12), (1, 14)], fish_accent)
    canvas.putpixel((3, 13), BLACK)

    # God rays (light shafts from above, diagonal)
    ray_color = (170, 220, 250)
    ray_pale = (130, 180, 220)
    for x, y in [(5, 0), (5, 1), (6, 2), (6, 3), (7, 4)]:
        if 0 <= x < SIZE and 0 <= y < SIZE and sum(canvas.getpixel((x, y))) < 200:
            canvas.putpixel((x, y), ray_color)
    for x, y in [(11, 0), (11, 1), (12, 2), (12, 3)]:
        if 0 <= x < SIZE and 0 <= y < SIZE and sum(canvas.getpixel((x, y))) < 200:
            canvas.putpixel((x, y), ray_pale)
    for x, y in [(25, 0), (25, 1), (24, 2), (24, 3), (23, 4)]:
        if 0 <= x < SIZE and 0 <= y < SIZE and sum(canvas.getpixel((x, y))) < 200:
            canvas.putpixel((x, y), ray_color)

    # Bubble streams
    for (x, y) in [(3, 5), (5, 9), (28, 11), (4, 18), (27, 19), (5, 22), (29, 23), (2, 28), (30, 28), (4, 14), (29, 6)]:
        if 0 <= x < SIZE and 0 <= y < SIZE:
            canvas.putpixel((x, y), bubble_color)
        if 0 <= x+1 < SIZE and 0 <= y+1 < SIZE:
            canvas.putpixel((x+1, y+1), bubble_dim)

    # Sunken anchor silhouette in bottom-right corner
    anchor = (90, 95, 105)
    anchor_dark = (60, 65, 75)
    paint(canvas, [(28, 24), (29, 23), (30, 23)], anchor)
    paint(canvas, [(29, 24), (29, 25), (29, 26), (29, 27)], anchor)
    paint(canvas, [(27, 27), (28, 27), (30, 27), (31, 27)], anchor)
    paint(canvas, [(27, 28), (31, 28)], anchor_dark)

    # Mouth bubbles (cluster rising from mouth)
    paint(canvas, [(19, 22), (20, 21), (21, 20), (22, 19), (23, 18)], bubble_color)
    paint(canvas, [(20, 22), (21, 21), (22, 20)], bubble_dim)

    # Gills on neck (two slits)
    paint(canvas, [(13, 26), (13, 27)], (180, 50, 70))
    paint(canvas, [(18, 26), (18, 27)], (180, 50, 70))

    # Extra fish in middle-bottom (third fish, smaller)
    paint(canvas, [(25, 21), (26, 21)], (180, 100, 60))
    paint(canvas, [(27, 20), (27, 22)], (180, 100, 60))
    canvas.putpixel((26, 21), BLACK)

    # === Per-person rare aquatic variants ===
    aq_variant = (person or {}).get("aquatic_variant")
    if aq_variant == "jellyfish":
        # Jellyfish dome with tentacles in upper right (replaces AI orb area)
        jelly = (200, 150, 255)
        paint(canvas, [(25, 21), (26, 21), (27, 21), (28, 21)], jelly)
        paint(canvas, [(24, 22), (29, 22)], jelly)
        # Tentacles
        paint(canvas, [(25, 23), (25, 24), (25, 25)], jelly)
        paint(canvas, [(27, 23), (27, 24), (27, 25), (27, 26)], jelly)
        paint(canvas, [(29, 23), (29, 24), (29, 25)], jelly)
        # Glow center
        paint(canvas, [(26, 21), (27, 21)], (255, 200, 255))
    if aq_variant == "scuba_helmet":
        # Full scuba helmet replacing snorkel for Duncan
        helm = (130, 135, 150)
        helm_dark = (80, 85, 100)
        glass = (160, 220, 240)
        # Dome
        for x in range(9, 23):
            for y in range(11, 19):
                canvas.putpixel((x, y), helm)
        # Glass face plate (large oval)
        fill_rect(canvas, 11, 13, 21, 18, glass)
        # Outline
        paint(canvas, [(10, 13), (22, 13), (10, 14), (22, 14), (10, 15), (22, 15), (10, 16), (22, 16), (10, 17), (22, 17), (10, 18), (22, 18)], helm_dark)
        # Top tank attachment
        paint(canvas, [(15, 9), (16, 9), (15, 10), (16, 10)], helm_dark)
        paint(canvas, [(14, 11), (17, 11)], helm_dark)
    if aq_variant == "octopus_tentacle":
        # Octopus tentacle wrapping around shoulder
        oct_color = (180, 60, 130)
        oct_dark = (130, 30, 90)
        # Body bump in upper right
        paint(canvas, [(26, 8), (27, 8), (28, 8)], oct_color)
        paint(canvas, [(26, 9), (27, 9), (28, 9), (29, 9)], oct_color)
        # Suckers on tentacle wrapping shoulder
        paint(canvas, [(27, 10), (28, 11), (29, 12), (28, 13), (27, 14), (26, 15)], oct_color)
        paint(canvas, [(28, 11), (28, 13), (26, 15)], oct_dark)
        paint(canvas, [(26, 27), (27, 27), (28, 27)], oct_color)
        paint(canvas, [(27, 28), (28, 28)], oct_dark)  # sucker bottom
    if aq_variant == "trident":
        # Trident behind right shoulder
        paint(canvas, [(28, 4), (28, 5)], (220, 215, 200))  # prongs
        paint(canvas, [(27, 4), (29, 4)], (220, 215, 200))
        paint(canvas, [(28, 6), (28, 7), (28, 8), (28, 9), (28, 10), (28, 11)], (140, 95, 50))  # shaft
    if aq_variant == "starfish":
        # Starfish on shoulder
        paint(canvas, [(4, 26), (5, 25), (6, 26)], (255, 165, 80))
        paint(canvas, [(5, 26), (5, 27)], (255, 200, 100))
        paint(canvas, [(4, 27), (6, 27)], (255, 165, 80))
    if aq_variant == "laser_eyes_underwater":
        # Orange laser visible underwater for Ryan
        paint(canvas, [(13, 16), (18, 16)], (255, 120, 50))
        for x in range(0, 12):
            canvas.putpixel((x, 16), mix((255, 120, 50), hex_to_rgb("#050709"), 0.3))
        for x in range(19, SIZE):
            canvas.putpixel((x, 16), mix((255, 120, 50), hex_to_rgb("#050709"), 0.3))
    if aq_variant == "tie_seaweed":
        # Tie becomes flowing green seaweed
        paint(canvas, [(15, 28), (16, 28), (15, 29), (16, 29)], (40, 140, 70))
        paint(canvas, [(15, 30), (16, 30), (15, 31), (17, 31)], (60, 170, 90))
        paint(canvas, [(14, 30), (17, 30)], (40, 140, 70))
    if aq_variant == "bubble_headset":
        # Extra bubbles surrounding the headset
        paint(canvas, [(7, 19), (8, 21), (6, 18)], (220, 240, 250))
        paint(canvas, [(11, 21), (12, 22)], (220, 240, 250))
    if aq_variant == "foggy_glasses":
        # Water droplets on the glass lenses
        paint(canvas, [(12, 16), (13, 17), (18, 17), (19, 16)], (180, 220, 240))
    if aq_variant == "wrap_dive_glasses":
        # Override sunglasses to wraparound dive shades (wider)
        for x in range(9, 22):
            canvas.putpixel((x, 15), BLACK)
            canvas.putpixel((x, 16), (30, 80, 130))
            canvas.putpixel((x, 17), BLACK)
        paint(canvas, [(11, 16), (14, 16), (17, 16), (20, 16)], (100, 180, 220))
    if aq_variant == "coral_cross":
        # Cross signature turns coral pink
        paint(canvas, [(15, 28)], (255, 120, 130))
        paint(canvas, [(14, 29), (15, 29), (16, 29)], (255, 120, 130))
        paint(canvas, [(15, 30)], (255, 120, 130))
    if aq_variant == "diving_cap":
        # Cap becomes diving cap with side strap
        paint(canvas, [(7, 11), (24, 11)], (40, 80, 120))
        paint(canvas, [(9, 12), (22, 12)], (40, 80, 120))
    if aq_variant == "mermaid_hair":
        # Hair flows with seafoam highlights
        paint(canvas, [(8, 14), (8, 17), (8, 20), (23, 14), (23, 17), (23, 20)], (140, 220, 230))
    if aq_variant == "anchor_tat":
        # Anchor tattoo on neck
        paint(canvas, [(15, 27)], (200, 200, 220))
        paint(canvas, [(14, 28), (16, 28)], (200, 200, 220))


def add_snorkel(canvas, person):
    """Snorkel + dive mask for select chars (called as accessory in aquatic).
    Mouthpiece now actually attaches to the mouth at rows 23-24."""
    # Dive mask (covers eyes)
    mask_color = (15, 60, 100)
    glass_color = (100, 200, 230)
    # Strap
    for x in range(9, 23): canvas.putpixel((x, 14), mask_color)
    # Mask body
    fill_rect(canvas, 10, 15, 21, 17, mask_color)
    # Lenses
    fill_rect(canvas, 11, 15, 14, 16, glass_color)
    fill_rect(canvas, 17, 15, 20, 16, glass_color)
    paint(canvas, [(12, 15), (18, 15)], WHITE)  # lens highlight
    # Snorkel tube up the right side
    for y in range(2, 12): canvas.putpixel((23, y), mask_color)
    paint(canvas, [(23, 1), (24, 1), (24, 2), (24, 3)], (200, 200, 50))  # snorkel tip
    # Snorkel curves down toward face (going from row 12 to mouth)
    paint(canvas, [(23, 13), (23, 14), (22, 15)], mask_color)
    paint(canvas, [(21, 18), (21, 19), (21, 20), (21, 21), (21, 22)], mask_color)  # tube down
    # Mouthpiece (actually covers/attaches to mouth at rows 23-24)
    paint(canvas, [(19, 22), (20, 22), (21, 22)], mask_color)
    paint(canvas, [(19, 23), (20, 23), (21, 23)], mask_color)  # mouthpiece around mouth
    paint(canvas, [(20, 23), (21, 23)], (200, 200, 50))  # bite plate yellow


def theme_cyberpunk(canvas, trait_hex, person=None):
    """Neon street: magenta/cyan grid bg, code rain, hoodie up, cyber visor, neon scar tattoos."""
    trait = hex_to_rgb(trait_hex)
    NEON_MAGENTA = (255, 60, 200)
    NEON_CYAN = (60, 230, 255)
    NEON_GREEN = (60, 255, 140)
    DARK_BG = (8, 8, 18)

    # Original bg color (what draw_background set)
    orig_bg = mix(trait, (8, 12, 20), 0.78)

    # Repaint background ONLY (preserve character pixels)
    def is_bg(c):
        # Match original bg or dot-grid variant
        return abs(c[0] - orig_bg[0]) < 30 and abs(c[1] - orig_bg[1]) < 30 and abs(c[2] - orig_bg[2]) < 30

    for x in range(SIZE):
        for y in range(SIZE):
            if is_bg(canvas.getpixel((x, y))):
                canvas.putpixel((x, y), DARK_BG)

    # Neon grid lines over the new dark bg only
    grid_dim = mix(NEON_MAGENTA, DARK_BG, 0.7)
    for x in range(0, SIZE, 4):
        for y in range(SIZE):
            if canvas.getpixel((x, y)) == DARK_BG:
                canvas.putpixel((x, y), grid_dim)
    for y in range(0, SIZE, 4):
        for x in range(SIZE):
            if canvas.getpixel((x, y)) == DARK_BG:
                canvas.putpixel((x, y), grid_dim)
    # Horizon line - brighter cyan + magenta accent rows
    for x in range(0, SIZE, 4):
        if canvas.getpixel((x, 4)) == grid_dim or canvas.getpixel((x, 4)) == DARK_BG:
            canvas.putpixel((x, 4), mix(NEON_CYAN, DARK_BG, 0.5))

    # Corner brackets in cyan
    for i in range(3):
        canvas.putpixel((0, i), NEON_CYAN); canvas.putpixel((i, 0), NEON_CYAN)
        canvas.putpixel((SIZE-1-i, 0), NEON_MAGENTA); canvas.putpixel((SIZE-1, i), NEON_MAGENTA)
        canvas.putpixel((0, SIZE-1-i), NEON_MAGENTA); canvas.putpixel((i, SIZE-1), NEON_MAGENTA)
        canvas.putpixel((SIZE-1-i, SIZE-1), NEON_CYAN); canvas.putpixel((SIZE-1, SIZE-1-i), NEON_CYAN)

    # Hoodie up over head (dark with neon trim)
    hoodie_color = (20, 22, 35)
    slug_hash = sum(ord(c) for c in person["slug"]) if person else 0
    hoodie_trim = NEON_CYAN if slug_hash % 2 == 0 else NEON_MAGENTA
    # Hood draping over top of head
    for x in range(8, 24):
        canvas.putpixel((x, 8), hoodie_color)
        canvas.putpixel((x, 9), hoodie_color)
    paint(canvas, [(8, 10), (9, 10), (22, 10), (23, 10)], hoodie_color)
    # Side draping
    paint(canvas, [(8, 11), (8, 12), (8, 13), (23, 11), (23, 12), (23, 13)], hoodie_color)
    # Hood interior shadow
    paint(canvas, [(10, 10), (11, 10), (20, 10), (21, 10)], mix(hoodie_color, BLACK, 0.5))
    # Neon trim line along hood edge
    paint(canvas, [(7, 9), (24, 9)], hoodie_trim)
    paint(canvas, [(7, 13), (24, 13)], hoodie_trim)

    # Cyber visor (replaces eyes - horizontal neon strip)
    visor_glow = NEON_CYAN if slug_hash % 3 != 0 else NEON_MAGENTA
    paint(canvas, [(10, 15), (11, 15), (12, 15), (13, 15), (14, 15), (15, 15), (16, 15), (17, 15), (18, 15), (19, 15), (20, 15), (21, 15)], BLACK)
    paint(canvas, [(10, 16), (11, 16), (12, 16), (13, 16), (14, 16), (15, 16), (16, 16), (17, 16), (18, 16), (19, 16), (20, 16), (21, 16)], visor_glow)
    paint(canvas, [(11, 16), (15, 16), (19, 16)], WHITE)  # glints
    paint(canvas, [(10, 17), (11, 17), (12, 17), (13, 17), (14, 17), (15, 17), (16, 17), (17, 17), (18, 17), (19, 17), (20, 17), (21, 17)], BLACK)

    # Neon scar tattoo on cheek
    paint(canvas, [(12, 21), (11, 22), (12, 22)], NEON_MAGENTA)
    paint(canvas, [(11, 23)], mix(NEON_MAGENTA, WHITE, 0.4))

    # Code rain (vertical 0/1 streams) in margins
    rain = NEON_GREEN
    for col_x, bits in [(1, [0, 1, 1, 0, 1, 0, 1, 1]), (3, [1, 0, 1, 1, 0, 0, 1]),
                        (28, [1, 1, 0, 1, 0, 1]), (30, [0, 1, 0, 0, 1, 1, 0])]:
        for i, b in enumerate(bits):
            y = (3 + i)
            if 0 <= col_x < SIZE and 0 <= y < SIZE:
                curr = canvas.getpixel((col_x, y))
                if sum(curr) < 100:
                    fade = 1 - (i / len(bits)) * 0.7
                    c = (int(rain[0] * fade), int(rain[1] * fade), int(rain[2] * fade))
                    canvas.putpixel((col_x, y), c if b else mix(c, DARK_BG, 0.7))

    # Floating data fragments near bottom
    for (x, y) in [(2, 26), (3, 26), (29, 27), (30, 27)]:
        if 0 <= x < SIZE and 0 <= y < SIZE:
            curr = canvas.getpixel((x, y))
            if sum(curr) < 100:
                canvas.putpixel((x, y), NEON_CYAN)

    # Neon halo behind head
    halo = mix(NEON_MAGENTA, DARK_BG, 0.6)
    for x, y in [(7, 11), (24, 11), (7, 14), (24, 14)]:
        canvas.putpixel((x, y), halo)

    # === Per-person rare cyberpunk variants ===
    cy_variant = (person or {}).get("cyberpunk_variant")
    if cy_variant == "neon_mohawk":
        # Bright neon mohawk visible above hoodie
        paint(canvas, [(14, 2), (15, 2), (16, 2), (17, 2)], NEON_MAGENTA)
        paint(canvas, [(14, 3), (15, 3), (16, 3), (17, 3)], NEON_CYAN)
        paint(canvas, [(15, 4), (16, 4)], NEON_MAGENTA)
        # Skip hoodie cap for this person (override)
        for x in range(8, 24):
            canvas.putpixel((x, 8), DARK_BG)
            canvas.putpixel((x, 9), DARK_BG)
    if cy_variant == "red_visor":
        # Override visor color with red laser strip
        paint(canvas, [(10, 16), (11, 16), (12, 16), (13, 16), (14, 16), (15, 16), (16, 16), (17, 16), (18, 16), (19, 16), (20, 16), (21, 16)], (255, 60, 80))
        paint(canvas, [(11, 16), (15, 16), (19, 16)], (255, 200, 200))
    if cy_variant == "full_face_tattoo":
        # Tribal cyber tattoos across cheeks + forehead
        tattoo = NEON_CYAN
        paint(canvas, [(11, 13), (12, 12), (13, 13)], tattoo)
        paint(canvas, [(18, 13), (19, 12), (20, 13)], tattoo)
        paint(canvas, [(13, 20), (14, 21), (15, 20)], NEON_MAGENTA)
        paint(canvas, [(17, 20), (18, 21), (19, 20)], NEON_MAGENTA)
    if cy_variant == "jacked_in":
        # Cables sprouting from skull through hoodie (for the AI-native Kensington)
        paint(canvas, [(11, 8), (12, 7), (13, 6)], NEON_CYAN)
        paint(canvas, [(20, 8), (19, 7), (18, 6)], NEON_MAGENTA)
        paint(canvas, [(16, 8), (16, 7), (17, 6)], NEON_GREEN)
        paint(canvas, [(13, 6), (17, 6), (16, 6)], (255, 200, 60))  # gold connectors
    if cy_variant == "neon_pink_hair":
        # Override hair area with neon pink
        for x in range(11, 21):
            canvas.putpixel((x, 6), NEON_MAGENTA)
            canvas.putpixel((x, 7), NEON_MAGENTA)
        paint(canvas, [(12, 6), (15, 6), (18, 6)], (255, 200, 230))
    if cy_variant == "cyber_arm":
        # Robotic forearm visible bottom-right
        paint(canvas, [(22, 28), (23, 28), (24, 28), (25, 28)], (140, 145, 160))
        paint(canvas, [(22, 29), (23, 29), (24, 29), (25, 29)], (90, 95, 110))
        paint(canvas, [(22, 30), (23, 30), (24, 30), (25, 30)], (140, 145, 160))
        paint(canvas, [(26, 28), (26, 29), (26, 30)], NEON_CYAN)
        paint(canvas, [(23, 28), (25, 30)], NEON_MAGENTA)  # accent stripe
    if cy_variant == "data_suit":
        # Glowing data lines running through suit
        paint(canvas, [(7, 28), (8, 29), (9, 30)], NEON_CYAN)
        paint(canvas, [(22, 28), (23, 29), (24, 30)], NEON_MAGENTA)
        paint(canvas, [(13, 29), (14, 29), (15, 29)], NEON_GREEN)
    if cy_variant == "cyber_headset_hud":
        # HUD readout floating to the right of head
        paint(canvas, [(24, 14), (25, 14), (26, 14)], NEON_CYAN)
        paint(canvas, [(24, 15), (26, 15)], NEON_CYAN)
        paint(canvas, [(24, 16), (25, 16), (26, 16)], NEON_MAGENTA)
        paint(canvas, [(28, 14), (29, 14)], NEON_GREEN)  # status indicator
    if cy_variant == "ar_overlay":
        # AR projection floating above + to the right
        paint(canvas, [(26, 10), (27, 10), (28, 10)], NEON_CYAN)
        paint(canvas, [(26, 11), (28, 11)], NEON_CYAN)
        paint(canvas, [(26, 12), (27, 12), (28, 12)], mix(NEON_CYAN, WHITE, 0.4))
        paint(canvas, [(29, 11)], NEON_GREEN)
    if cy_variant == "energy_drink":
        # Replace pint glass with energy drink can
        paint(canvas, [(3, 15), (4, 15)], (255, 60, 100))  # can top
        paint(canvas, [(3, 16), (3, 17), (3, 18), (3, 19), (3, 20)], NEON_CYAN)  # can body
        paint(canvas, [(4, 16), (4, 17), (4, 18), (4, 19), (4, 20)], (255, 60, 100))
        paint(canvas, [(3, 17), (4, 19)], NEON_GREEN)  # label dots
        paint(canvas, [(3, 21), (4, 21)], (60, 60, 70))  # bottom
    if cy_variant == "tactical_mask":
        # Mask covering lower face
        paint(canvas, [(11, 21), (12, 21), (13, 21), (14, 21), (15, 21), (16, 21), (17, 21), (18, 21), (19, 21), (20, 21)], (30, 30, 40))
        for y in range(22, 26):
            for x in range(11, 21):
                canvas.putpixel((x, y), (30, 30, 40))
        # Vent grilles
        paint(canvas, [(13, 24), (15, 24), (17, 24), (19, 24)], NEON_CYAN)
    if cy_variant == "neon_cross":
        # Cross glows in trait color
        paint(canvas, [(15, 28)], NEON_CYAN)
        paint(canvas, [(14, 29), (15, 29), (16, 29)], NEON_CYAN)
        paint(canvas, [(15, 30)], NEON_CYAN)
    if cy_variant == "cyber_surfboard":
        # Surfboard with neon stripes
        paint(canvas, [(26, 18), (27, 18), (26, 19), (27, 19), (26, 20), (27, 20), (26, 21), (27, 21), (26, 22), (27, 22), (26, 23), (27, 23), (26, 24), (27, 24), (26, 25), (27, 25), (26, 26), (27, 26), (26, 27), (27, 27)], NEON_MAGENTA)
        paint(canvas, [(26, 19), (26, 22), (26, 25)], NEON_CYAN)
        paint(canvas, [(27, 21), (27, 24)], NEON_GREEN)
    if cy_variant == "hair_clips":
        # Neon hair clips
        paint(canvas, [(11, 9), (20, 9)], NEON_MAGENTA)
        paint(canvas, [(10, 10), (21, 10)], NEON_CYAN)


BRAIN_PALETTES = {
    "pink":    {"main": (255, 140, 180), "med": (235, 110, 155), "shadow": (180, 70, 110), "light": (255, 200, 220), "deep": (140, 50, 90)},
    "gold":    {"main": (255, 200, 60),  "med": (220, 165, 30),  "shadow": (170, 125, 20), "light": (255, 235, 140), "deep": (130, 95, 15)},
    "green":   {"main": (140, 240, 140), "med": (90, 200, 90),   "shadow": (50, 145, 60),  "light": (200, 255, 200), "deep": (30, 100, 40)},
    "blue":    {"main": (140, 200, 255), "med": (90, 165, 225),  "shadow": (50, 115, 180), "light": (200, 230, 255), "deep": (25, 70, 130)},
    "magenta": {"main": (255, 100, 220), "med": (220, 70, 190),  "shadow": (170, 40, 150), "light": (255, 170, 240), "deep": (110, 25, 95)},
}

def theme_galaxy(canvas, trait_hex, person=None):
    """Full brain exposure. Entire skull-cap replaced with brain folds + cables + cyborg accents."""
    trait = hex_to_rgb(trait_hex)
    brain_color_key = (person or {}).get("brain_color", "pink")
    pal = BRAIN_PALETTES.get(brain_color_key, BRAIN_PALETTES["pink"])
    brain_pink = pal["main"]
    brain_med = pal["med"]
    brain_shadow = pal["shadow"]
    brain_light = pal["light"]
    brain_deep = pal["deep"]
    bone = (240, 230, 215)
    circuit_glow = mix(trait, WHITE, 0.4)

    # === Full brain dome covering rows 3-12 ===
    # Brain shape spans full head width (cols 9-22 normally, but expand slightly)
    # Row 3: narrow top
    paint(canvas, [(13, 3), (14, 3), (15, 3), (16, 3), (17, 3), (18, 3)], brain_pink)
    # Row 4: wider
    paint(canvas, [(11, 4), (12, 4), (13, 4), (14, 4), (15, 4), (16, 4), (17, 4), (18, 4), (19, 4), (20, 4)], brain_pink)
    # Rows 5-11: full dome
    for y in range(5, 12):
        for x in range(9, 23):
            canvas.putpixel((x, y), brain_pink)
    # Row 12: starting to narrow into forehead area (overlaps with eyebrows)
    paint(canvas, [(10, 12), (11, 12), (12, 12), (19, 12), (20, 12), (21, 12)], brain_pink)

    # === Brain folds (darker pink lines following curves) ===
    # Fold 1: top arc
    paint(canvas, [(12, 5), (14, 4), (16, 4), (18, 5), (19, 5)], brain_shadow)
    paint(canvas, [(13, 6), (15, 6), (17, 6), (19, 6)], brain_shadow)
    # Fold 2: middle wave
    paint(canvas, [(10, 7), (12, 7), (14, 7), (16, 7), (18, 7), (20, 7), (21, 7)], brain_shadow)
    paint(canvas, [(11, 8), (13, 8), (15, 8), (17, 8), (19, 8)], brain_med)
    # Fold 3: lower wave
    paint(canvas, [(10, 9), (12, 9), (14, 9), (16, 9), (18, 9), (20, 9)], brain_shadow)
    paint(canvas, [(11, 10), (13, 10), (15, 10), (17, 10), (19, 10), (21, 10)], brain_med)
    # Hemisphere divide (vertical line down the middle)
    paint(canvas, [(15, 3), (15, 4), (15, 5), (15, 7), (15, 9), (15, 11)], brain_deep)
    paint(canvas, [(15, 6), (15, 8), (15, 10)], brain_shadow)

    # === Highlights (light pink dots for shine) ===
    paint(canvas, [(11, 5), (13, 5), (17, 5), (19, 5), (11, 6), (13, 7), (17, 8), (19, 9), (11, 9), (13, 10), (17, 10)], brain_light)

    # === Skull rim line (subtle dark line where brain meets face) ===
    paint(canvas, [(9, 12), (10, 11), (21, 11), (22, 12)], brain_deep)
    paint(canvas, [(9, 13), (22, 13)], mix(SKIN_SHADOW["light"], brain_deep, 0.4))

    # === Skull edge (bone-white line where brain meets face) ===
    paint(canvas, [(9, 11), (10, 11), (11, 11)], bone)
    paint(canvas, [(20, 11), (21, 11), (22, 11)], bone)
    paint(canvas, [(8, 12), (9, 12), (22, 12), (23, 12)], mix(bone, brain_deep, 0.3))

    # === Neural circuit traces glowing across brain (trait-color lines) ===
    paint(canvas, [(11, 6), (12, 6), (13, 7), (14, 7)], circuit_glow)
    paint(canvas, [(17, 7), (18, 7), (19, 6), (20, 6)], circuit_glow)
    paint(canvas, [(10, 9), (11, 10)], circuit_glow)
    paint(canvas, [(20, 10), (21, 9)], circuit_glow)
    # Circuit junction nodes
    paint(canvas, [(12, 6), (19, 6), (11, 10), (20, 10), (15, 8)], trait)

    # === Cybernetic cables sprouting from brain (8 cables) ===
    cable_dark = (60, 60, 75)
    cable_gold = (255, 200, 60)
    # Top exits
    paint(canvas, [(12, 2), (11, 1), (10, 0)], trait)
    paint(canvas, [(13, 3)], cable_gold)
    paint(canvas, [(14, 2), (14, 1), (13, 0)], mix(trait, WHITE, 0.5))
    paint(canvas, [(15, 3)], cable_gold)
    paint(canvas, [(16, 2), (16, 1), (17, 0)], mix(trait, WHITE, 0.4))
    paint(canvas, [(16, 3)], cable_gold)
    paint(canvas, [(18, 2), (18, 1), (19, 0)], cable_dark)
    paint(canvas, [(17, 3)], cable_gold)
    paint(canvas, [(20, 2), (21, 1), (22, 0)], trait)
    paint(canvas, [(19, 3)], cable_gold)
    # Side exits (ear-jacks)
    paint(canvas, [(8, 6), (7, 6), (6, 7), (5, 7), (4, 8), (3, 8)], cable_dark)
    paint(canvas, [(2, 8)], trait)
    paint(canvas, [(8, 9), (7, 10), (6, 11)], mix(trait, WHITE, 0.3))
    paint(canvas, [(5, 12)], cable_gold)
    paint(canvas, [(23, 6), (24, 6), (25, 7), (26, 7), (27, 8), (28, 8)], cable_dark)
    paint(canvas, [(29, 8)], trait)
    paint(canvas, [(23, 9), (24, 10), (25, 11)], mix(trait, WHITE, 0.3))
    paint(canvas, [(26, 12)], cable_gold)

    # === Robotic neck plate with status LEDs ===
    plate = (50, 55, 70)
    plate_edge = (90, 95, 110)
    fill_rect(canvas, 12, 27, 19, 28, plate)
    paint(canvas, [(12, 27), (19, 27)], plate_edge)
    # Status LEDs (3 little glowing dots)
    paint(canvas, [(14, 27)], trait)
    paint(canvas, [(15, 27)], (255, 80, 80))   # red LED
    paint(canvas, [(17, 27)], cable_gold)      # gold LED
    paint(canvas, [(18, 27)], mix(trait, WHITE, 0.6))

    # === Glowing aura around head (faint ring) ===
    aura = mix(trait, hex_to_rgb("#050709"), 0.6)
    for (x, y) in [(8, 4), (9, 3), (10, 2), (13, 1), (16, 0), (19, 1), (22, 2), (23, 3), (24, 4)]:
        if 0 <= x < SIZE and 0 <= y < SIZE:
            curr = canvas.getpixel((x, y))
            # Only paint if dark bg
            if sum(curr) < 80:
                canvas.putpixel((x, y), aura)

    # === Neural network background nodes ===
    node_color = mix(trait, WHITE, 0.5)
    line_color = mix(trait, hex_to_rgb("#050709"), 0.5)
    for (x, y) in [(1, 14), (2, 20), (5, 25), (3, 30), (30, 14), (29, 20), (27, 26), (28, 30), (1, 5), (30, 5)]:
        if 0 <= x < SIZE and 0 <= y < SIZE:
            curr = canvas.getpixel((x, y))
            if sum(curr) < 80:
                canvas.putpixel((x, y), node_color)
    # Faint connecting trails
    for (x, y) in [(2, 17), (3, 22), (4, 27), (29, 17), (28, 23), (27, 28)]:
        if 0 <= x < SIZE and 0 <= y < SIZE:
            curr = canvas.getpixel((x, y))
            if sum(curr) < 80:
                canvas.putpixel((x, y), line_color)

    # === Matrix code rain (vertical 0/1 streams) ===
    rain_bright = mix(trait, WHITE, 0.6)
    rain_dim = mix(trait, hex_to_rgb("#050709"), 0.3)
    rain_columns = [(0, [0, 1, 1, 0, 1, 0]), (1, [1, 0, 0, 1, 1]), (4, [1, 1, 0, 1]),
                    (27, [0, 1, 1, 0, 1]), (30, [1, 0, 1, 0, 1, 1]), (31, [0, 1, 0])]
    for col_x, bits in rain_columns:
        start_y = 14 + col_x % 4
        for i, b in enumerate(bits):
            y = start_y + i
            x = col_x
            if 0 <= x < SIZE and 0 <= y < SIZE:
                curr = canvas.getpixel((x, y))
                if sum(curr) < 100:
                    # First pixel is brightest, fades down
                    c = rain_bright if i == 0 else (rain_dim if i > 2 else mix(rain_bright, rain_dim, i / 3))
                    canvas.putpixel((x, y), c if b else mix(c, hex_to_rgb("#050709"), 0.6))

    # === Holographic UI panels around character ===
    panel_color = mix(trait, WHITE, 0.5)
    panel_dim = mix(trait, hex_to_rgb("#050709"), 0.4)
    # Left readout: status bar with brackets
    paint(canvas, [(0, 18), (1, 18)], panel_color)  # [ corner
    paint(canvas, [(0, 19), (0, 20)], panel_color)  # | bar
    paint(canvas, [(1, 20)], panel_dim)
    paint(canvas, [(0, 21)], panel_color)
    paint(canvas, [(1, 21)], panel_color)  # ] corner
    # Health-bar style indicator (3 dots)
    paint(canvas, [(2, 19)], trait)
    paint(canvas, [(3, 19)], trait)
    paint(canvas, [(4, 19)], panel_dim)
    # Right readout: opposite corner UI
    paint(canvas, [(30, 21), (31, 21)], panel_color)
    paint(canvas, [(31, 22), (31, 23)], panel_color)
    paint(canvas, [(30, 24)], panel_dim)
    paint(canvas, [(30, 25), (31, 25)], panel_color)
    paint(canvas, [(29, 22), (28, 22), (27, 22)], panel_color)  # data line

    # === Energy crackles around brain (jagged lightning) ===
    crackle = mix(trait, WHITE, 0.7)
    # Top-left crackle
    paint(canvas, [(8, 0), (7, 1), (8, 2), (9, 1)], crackle)
    # Top-right crackle
    paint(canvas, [(23, 0), (24, 1), (23, 2), (22, 1)], crackle)
    # Left side crackle
    paint(canvas, [(0, 11), (1, 10), (2, 11)], crackle)
    # Right side crackle
    paint(canvas, [(31, 11), (30, 10), (29, 11)], crackle)

    # === Floating data fragments ===
    fragments = [
        ((1, 4), [1, 0]), ((30, 4), [0, 1]),
        ((1, 8), [1, 1]), ((29, 9), [1, 0]),
        ((1, 30), [0, 1]), ((29, 30), [1, 0]),
    ]
    glyph_color = mix(trait, WHITE, 0.45)
    for (x, y), bits in fragments:
        for i, b in enumerate(bits):
            if 0 <= x + i < SIZE and 0 <= y < SIZE:
                curr = canvas.getpixel((x + i, y))
                if sum(curr) < 100:
                    canvas.putpixel((x + i, y), glyph_color if b else mix(glyph_color, hex_to_rgb("#050709"), 0.5))

    # === Multi-color cyber eye glow (override the simple cyan) ===
    # Outer halo around eyes in trait color
    paint(canvas, [(11, 16), (15, 16), (16, 16), (20, 16)], mix(trait, WHITE, 0.5))
    paint(canvas, [(11, 17), (20, 17)], mix(trait, hex_to_rgb("#050709"), 0.3))
    # Eye glow trails (light streaks)
    paint(canvas, [(13, 15), (18, 15)], WHITE)

    # === Per-person rare variants ===
    galaxy_variant = (person or {}).get("galaxy_variant")
    if galaxy_variant == "antennae":
        # Two antennae sticking up
        paint(canvas, [(11, 0), (11, 1), (11, 2)], (200, 200, 220))
        paint(canvas, [(20, 0), (20, 1), (20, 2)], (200, 200, 220))
        paint(canvas, [(11, 0), (20, 0)], trait)  # glowing tips
    if galaxy_variant == "cyborg_jaw":
        # Right side of jaw replaced with metal plate
        plate = (90, 95, 110)
        plate_edge = (140, 145, 160)
        for y in range(20, 26):
            canvas.putpixel((19, y), plate)
            canvas.putpixel((20, y), plate_edge)
        paint(canvas, [(19, 22), (19, 24)], (255, 60, 60))  # rivet LEDs
    if galaxy_variant == "laser_through_brain":
        # Red lasers shooting from eyes THROUGH the brain (visible burn marks)
        paint(canvas, [(13, 8), (13, 9), (13, 10)], (255, 50, 50))
        paint(canvas, [(18, 8), (18, 9), (18, 10)], (255, 50, 50))
        # Burn glow
        paint(canvas, [(13, 6), (13, 7), (18, 6), (18, 7)], (255, 150, 100))
    if galaxy_variant == "data_halo":
        # Floating data ring around head (8 glowing dots)
        for x, y in [(7, 8), (10, 4), (16, 2), (22, 4), (25, 8), (25, 18), (7, 18)]:
            if 0 <= x < SIZE and 0 <= y < SIZE:
                curr = canvas.getpixel((x, y))
                if sum(curr) < 120:
                    canvas.putpixel((x, y), (255, 215, 60))
    if galaxy_variant == "drone":
        # Replace AI agent orb with mini drone (4 rotor + body)
        paint(canvas, [(25, 26), (26, 26), (27, 26)], (200, 200, 220))
        paint(canvas, [(24, 25), (28, 25)], trait)
        paint(canvas, [(25, 27), (27, 27)], (60, 60, 70))
        paint(canvas, [(26, 28)], (255, 60, 60))  # red light
    if galaxy_variant == "hidden_brain":
        # Black hood covering brain entirely, only purple glow leaking through
        for x in range(8, 24):
            for y in range(3, 12):
                if 0 <= x < SIZE and 0 <= y < SIZE:
                    canvas.putpixel((x, y), (12, 8, 20))
        # Faint glow leaking through
        paint(canvas, [(13, 9), (15, 9), (18, 9), (12, 11), (20, 11)], (157, 122, 255))
        paint(canvas, [(16, 6), (15, 8)], (200, 170, 255))
        # Question mark above
        paint(canvas, [(15, 2), (16, 2), (17, 2), (17, 3), (16, 4), (16, 6)], trait)
    if galaxy_variant == "cap_brain":
        # Cap sits ON TOP of brain (rebel keeps his cap on)
        cap_c = (15, 15, 15)
        for x in range(5, 18): canvas.putpixel((x, 4), cap_c)  # brim
        for x in range(5, 19): canvas.putpixel((x, 3), cap_c)
        for x in range(10, 22): canvas.putpixel((x, 1), cap_c)  # crown
        for x in range(10, 22): canvas.putpixel((x, 2), cap_c)
        # Logo
        paint(canvas, [(15, 2), (16, 2)], WHITE)
    if galaxy_variant == "cyber_crown":
        # Metallic glowing crown sitting on top of brain
        paint(canvas, [(11, 3), (13, 3), (15, 3), (17, 3), (19, 3)], (255, 215, 60))
        paint(canvas, [(11, 4), (12, 4), (13, 4), (14, 4), (15, 4), (16, 4), (17, 4), (18, 4), (19, 4)], (255, 215, 60))
        paint(canvas, [(13, 4), (17, 4)], (255, 250, 200))  # jewels
        paint(canvas, [(15, 4)], (255, 60, 60))  # ruby
    if galaxy_variant == "brain_in_glass":
        # Brain visible inside a glass vessel on shoulder
        paint(canvas, [(2, 14), (3, 14), (4, 14), (5, 14)], (180, 220, 240))  # glass top
        paint(canvas, [(2, 15), (2, 16), (2, 17), (5, 15), (5, 16), (5, 17)], (180, 220, 240))
        paint(canvas, [(3, 15), (4, 15)], brain_pink)
        paint(canvas, [(3, 16), (4, 16)], brain_med)
        paint(canvas, [(3, 17), (4, 17)], brain_shadow)
        paint(canvas, [(2, 18), (3, 18), (4, 18), (5, 18)], (180, 220, 240))
    if galaxy_variant == "floral_brain":
        # Flower bloom patterns on brain
        paint(canvas, [(12, 7), (13, 6), (14, 7), (13, 8)], (255, 200, 100))
        paint(canvas, [(13, 7)], (255, 240, 60))  # center
        paint(canvas, [(17, 9), (18, 8), (19, 9), (18, 10)], (200, 100, 200))
        paint(canvas, [(18, 9)], (255, 220, 250))


# ============ COMPOSE ============
def build(person, theme="corporate"):
    canvas = Image.new("RGB", (SIZE, SIZE))
    draw_background(canvas, person["trait"], theme)

    draw_shirt(canvas, person["shirt"], person["shirt_color"], person.get("shirt_accent"))

    draw_head(canvas, person["skin"], person.get("face_shape", "oval"))

    style = person["hair_style"]
    if style in HAIR_FNS:
        HAIR_FNS[style](canvas, person["hair_color"])

    draw_eyebrows(canvas, person["hair_color"], person.get("brow_style", "straight"))
    draw_eyes(canvas, person["eyes"], person.get("eye_shape", "normal"))
    draw_nose(canvas, person["skin"], person.get("nose", "standard"))
    draw_mouth(canvas, person["mouth"], person["skin"])
    draw_beard(canvas, person.get("beard", "none"), person["hair_color"])

    # Signature item dispatch
    sig = person.get("signature")
    trait_color = hex_to_rgb(person["trait"])
    if sig == "pocket_square":   sig_pocket_square(canvas, trait_color)
    elif sig == "necklace_gold": sig_necklace_gold(canvas)
    elif sig == "headset":       sig_headset(canvas)
    elif sig == "watch":         sig_watch(canvas)
    elif sig == "question_mark": sig_question_mark(canvas, trait_color)
    elif sig == "pint_glass":    sig_pint_glass(canvas)
    elif sig == "crown":         sig_crown(canvas, GOLD)
    elif sig == "chain":         sig_chain(canvas)
    elif sig == "ai_agent":      sig_ai_agent(canvas, trait_color)
    elif sig == "cross":         sig_cross_necklace(canvas)
    elif sig == "surfboard":     sig_surfboard(canvas)
    elif sig == "bt_pin":        sig_bt_pin(canvas, trait_color)
    elif sig == "earring":       sig_earring(canvas)
    elif sig == "headphones":    sig_headphones(canvas)
    elif sig == "cap":           sig_cap(canvas, person.get("cap_color", (15, 15, 15)))

    # Accessory layer (drawn on top of face)
    acc = person.get("accessory")
    trait_color = hex_to_rgb(person["trait"])
    if acc == "sunglasses":      acc_sunglasses(canvas)
    elif acc == "aviators":      acc_aviators(canvas)
    elif acc == "glasses_clear": acc_glasses_clear(canvas)
    elif acc == "ar_glasses":    acc_ar_smart_glasses(canvas, trait_color)
    elif acc == "laser_eyes":    acc_laser_eyes(canvas, person.get("laser_color", (255, 50, 50)))
    elif acc == "earbuds":       acc_earbuds(canvas)
    elif acc == "beanie":        acc_beanie(canvas, person.get("beanie_color", (40, 40, 50)))
    elif acc == "red_lips":      acc_red_lips(canvas)
    elif acc == "earring_stud":  acc_earring_stud(canvas)

    if theme == "aquatic":
        theme_aquatic(canvas, person["trait"], person)
        if person.get("snorkel"):
            add_snorkel(canvas, person)

    if theme == "cyberpunk":
        theme_cyberpunk(canvas, person["trait"], person)

    if theme == "galaxy":
        theme_galaxy(canvas, person["trait"], person)
        # Cybernetic glowing eyes (override face eyes with intense glow)
        paint(canvas, [(12, 16), (13, 16), (14, 16)], GLOW)
        paint(canvas, [(17, 16), (18, 16), (19, 16)], GLOW)
        paint(canvas, [(13, 16), (18, 16)], WHITE)  # eye core
        if acc in ("sunglasses", "aviators", "glasses_clear", "ar_glasses"):
            paint(canvas, [(11, 15), (12, 15), (13, 15), (14, 15), (15, 15), (16, 15), (17, 15), (18, 15), (19, 15), (20, 15)], hex_to_rgb(person["trait"]))

    return canvas


# ============ PEOPLE ============
PEOPLE = [
    # Alec: corporate young gun, slick-back, suit + pocket square + bow tie energy
    {"slug": "alec", "trait": "#00FF94", "skin": "light", "hair_color": "dbrown", "hair_style": "slick_back",
     "eyes": "brown", "mouth": "big_grin", "shirt": "suit_tie", "shirt_color": (30, 30, 35), "shirt_accent": (60, 100, 170),
     "face_shape": "oval", "signature": "pocket_square", "brow_style": "thick",
     "aquatic_variant": "tie_seaweed",
     "cyberpunk_variant": "data_suit"},

    # Ava: LONG thin face, beach blonde, hazel eyes, white sweater, big_grin, arched brow, red lips
    {"slug": "ava", "trait": "#FF6B9D", "skin": "light_warm", "hair_color": "blonde", "hair_style": "beach_blonde",
     "eyes": "hazel", "mouth": "big_grin", "shirt": "sweater", "shirt_color": (240, 230, 215),
     "face_shape": "long", "signature": "necklace_gold", "brow_style": "arched", "accessory": "red_lips", "snorkel": True,
     "brain_color": "magenta", "galaxy_variant": "antennae",
     "aquatic_variant": "octopus_tentacle",
     "cyberpunk_variant": "neon_pink_hair"},

    # Catherine: headset + arched brow + lipstick (the caller)
    {"slug": "catherine", "trait": "#FFD93D", "skin": "light_warm", "hair_color": "dbrown", "hair_style": "long_straight",
     "eyes": "brown", "mouth": "smile", "shirt": "sweater", "shirt_color": (40, 35, 40),
     "face_shape": "oval", "signature": "headset", "brow_style": "arched", "accessory": "red_lips",
     "aquatic_variant": "bubble_headset",
     "cyberpunk_variant": "cyber_headset_hud"},

    # Chris: clear glasses + short parted hair (academic vibe)
    {"slug": "chris", "trait": "#00D9FF", "skin": "light", "hair_color": "brown", "hair_style": "short_parted",
     "eyes": "blue", "mouth": "big_grin", "shirt": "polo", "shirt_color": (35, 45, 60),
     "face_shape": "oval", "signature": "watch", "accessory": "glasses_clear",
     "brain_color": "blue",
     "aquatic_variant": "foggy_glasses",
     "cyberpunk_variant": "ar_overlay"},

    # Duncan: BEANIE + sunglasses (full mystery)
    {"slug": "duncan", "trait": "#9D7AFF", "skin": "light", "hair_color": "brown", "hair_style": "short_parted",
     "eyes": "brown", "mouth": "neutral", "shirt": "hoodie", "shirt_color": (60, 50, 80),
     "face_shape": "oval", "signature": "question_mark", "accessory": "sunglasses", "beanie_color": (60, 50, 80),
     "aquatic_variant": "scuba_helmet",
     "galaxy_variant": "hidden_brain"},

    # Evan: pint glass + scruff + dimple grin
    {"slug": "evan", "trait": "#FF8C42", "skin": "light", "hair_color": "lbrown", "hair_style": "messy",
     "eyes": "blue", "mouth": "big_grin", "shirt": "button_up", "shirt_color": (30, 35, 55), "beard": "scruff",
     "face_shape": "oval", "signature": "pint_glass",
     "aquatic_variant": "trident",
     "galaxy_variant": "brain_in_glass",
     "cyberpunk_variant": "energy_drink"},

    # Garrett: AVIATORS + AE crown + beard (senior AE energy)
    {"slug": "garrett", "trait": "#7B61FF", "skin": "light", "hair_color": "brown", "hair_style": "messy",
     "eyes": "brown", "mouth": "smirk", "shirt": "polo", "shirt_color": (25, 25, 30), "beard": "stubble",
     "face_shape": "square", "signature": "crown", "accessory": "aviators",
     "brain_color": "green", "galaxy_variant": "cyborg_jaw",
     "cyberpunk_variant": "neon_mohawk"},

    # Joe: SUNGLASSES + chain + stubble + dark suit (operator)
    {"slug": "joe", "trait": "#FF3366", "skin": "light_warm", "hair_color": "dbrown", "hair_style": "short_parted",
     "eyes": "brown", "mouth": "smirk", "beard": "stubble", "shirt": "suit_tie", "shirt_color": (70, 75, 85),
     "shirt_accent": (140, 145, 160), "face_shape": "oval", "signature": "chain", "accessory": "sunglasses",
     "galaxy_variant": "data_halo",
     "cyberpunk_variant": "cyber_arm",
     "aquatic_variant": "wrap_dive_glasses"},

    # Kensington: AR GLASSES + AI agent orb + undercut (always plugged in)
    {"slug": "kensington", "trait": "#00E5FF", "skin": "light", "hair_color": "lblonde", "hair_style": "undercut",
     "eyes": "blue", "mouth": "big_grin", "shirt": "zip_up", "shirt_color": (90, 65, 45),
     "face_shape": "oval", "signature": "ai_agent", "accessory": "ar_glasses",
     "brain_color": "gold", "galaxy_variant": "drone",
     "aquatic_variant": "jellyfish",
     "cyberpunk_variant": "jacked_in"},

    # Keslar: curly + green eyes + cross + blazer (collegiate athlete)
    {"slug": "keslar", "trait": "#FFC857", "skin": "light_warm", "hair_color": "dbrown", "hair_style": "curly_short",
     "eyes": "green", "mouth": "smile", "beard": "stubble", "shirt": "blazer_open", "shirt_color": (25, 35, 70),
     "face_shape": "square", "signature": "cross",
     "aquatic_variant": "coral_cross",
     "cyberpunk_variant": "neon_cross"},

    # Nick: VINTAGE CAP + scruff + AE
    {"slug": "nick", "trait": "#A8E6CF", "skin": "light_warm", "hair_color": "brown", "hair_style": "short_parted",
     "eyes": "brown", "mouth": "grin", "beard": "scruff", "shirt": "polo", "shirt_color": (180, 180, 180),
     "face_shape": "oval", "signature": "cap", "cap_color": (90, 50, 40),  # vintage brown cap
     "galaxy_variant": "cyber_crown",
     "cyberpunk_variant": "tactical_mask"},

    # Owen: BEANIE + surfboard + curly blonde (surfer)
    {"slug": "owen", "trait": "#4ECDC4", "skin": "light", "hair_color": "blonde", "hair_style": "curly_short",
     "eyes": "blue", "mouth": "big_grin", "shirt": "tshirt", "shirt_color": (240, 240, 240),
     "face_shape": "oval", "signature": "surfboard", "snorkel": True,
     "cyberpunk_variant": "cyber_surfboard"},

    # Ryan: LASER EYES + big BT pin + sweater (the boss / channel manager)
    {"slug": "ryan", "trait": "#E0E0E0", "skin": "light", "hair_color": "blonde", "hair_style": "short_parted",
     "eyes": "blue", "mouth": "big_grin", "shirt": "sweater", "shirt_color": (20, 20, 22),
     "face_shape": "oval", "signature": "bt_pin", "accessory": "laser_eyes", "laser_color": (255, 100, 50),
     "galaxy_variant": "laser_through_brain",
     "aquatic_variant": "laser_eyes_underwater",
     "cyberpunk_variant": "red_visor"},

    # Sacha: black snapback + chain + smirk
    {"slug": "sacha", "trait": "#FF66C4", "skin": "warm", "hair_color": "black", "hair_style": "messy",
     "eyes": "brown", "mouth": "smirk", "shirt": "tshirt", "shirt_color": (25, 25, 25),
     "face_shape": "oval", "signature": "cap", "cap_color": (15, 15, 15), "snorkel": True,
     "aquatic_variant": "starfish",
     "cyberpunk_variant": "full_face_tattoo",
     "galaxy_variant": "cap_brain"},

    # Shaune: ROUND tanner face, long_wavy ash-blonde, blue eyes, denim-blue button-up, softer smile, thick brow, gold earring stud (girl, denim vest vibe)
    {"slug": "shaune", "trait": "#B8FF3D", "skin": "tan", "hair_color": "lblonde", "hair_style": "long_wavy",
     "eyes": "blue", "mouth": "smile", "shirt": "button_up", "shirt_color": (175, 200, 220),
     "face_shape": "round", "signature": "necklace_gold", "brow_style": "thick", "accessory": "earring_stud", "snorkel": True,
     "aquatic_variant": "mermaid_hair",
     "galaxy_variant": "floral_brain",
     "cyberpunk_variant": "hair_clips"},
]


def load_people_from_json():
    """Load auto_people.json, normalize shirt_color list → tuple."""
    import json
    raw = json.loads(pathlib.Path("data/auto_people.json").read_text())
    normalized = []
    for p in raw:
        sc = p.get("shirt_color")
        if isinstance(sc, list):
            p["shirt_color"] = tuple(sc)
        normalized.append(p)
    return normalized


def main():
    theme = sys.argv[1] if len(sys.argv) > 1 else "corporate"
    out_dir = pathlib.Path(f"public/pixels/{theme}")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Use auto-generated people if data/auto_people.json exists, else fall back to hardcoded PEOPLE
    if pathlib.Path("data/auto_people.json").exists():
        people = load_people_from_json()
    else:
        people = PEOPLE

    for p in people:
        img = build(p, theme=theme)
        final = img.resize((SIZE * SCALE, SIZE * SCALE), Image.NEAREST)
        out_path = out_dir / f"{p['slug']}.png"
        final.save(out_path, "PNG", optimize=True)
        print(f"OK {out_path}")
    print(f"\nBuilt {len(people)} characters for theme: {theme}")


if __name__ == "__main__":
    main()
