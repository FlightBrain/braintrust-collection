#!/usr/bin/env python3
"""Personalized 48x48 face template, driven by per-SDR traits from auto_people.json.

Each SDR gets a face customized for: skin tone, hair color, hair style (incl.
long hair for women), eyes, mouth, beard. The face anchors stay the same as
face_template.py so all accessories still align.

Face anchors (unchanged):
  Head top:    row 6
  Eye row:     row 21-22 (cols 19-20, 27-28)
  Mouth row:   row 31-32 (cols 20-27)
  Chin:        row 36
  Neck:        row 37-41
  Shoulder:    row 42-47
"""
from items_v3 import new_canvas, put, paint, fill_rect, mix


# ============ Palettes ============

SKIN = {
    "light":      (252, 224, 194),
    "light_warm": (245, 210, 180),
    "warm":       (235, 195, 160),
    "tan":        (215, 170, 130),
    "medium":     (195, 150, 110),
    "deep":       (140, 100, 70),
}

SKIN_DARK = {
    "light":      (220, 188, 158),
    "light_warm": (215, 178, 145),
    "warm":       (200, 160, 125),
    "tan":        (180, 135, 95),
    "medium":     (160, 115, 80),
    "deep":       (105, 70, 45),
}

SKIN_LITE = {
    "light":      (255, 235, 210),
    "light_warm": (252, 225, 198),
    "warm":       (250, 215, 185),
    "tan":        (235, 195, 155),
    "medium":     (220, 175, 135),
    "deep":       (165, 125, 90),
}

HAIR = {
    "blonde":  (230, 195, 130),
    "lblonde": (245, 220, 165),
    "lbrown":  (150, 110, 70),
    "brown":   (95, 65, 40),
    "dbrown":  (60, 40, 25),
    "black":   (30, 25, 22),
    "auburn":  (140, 75, 45),
    "red":     (180, 80, 35),
    "gray":    (160, 160, 160),
}

HAIR_SHADOW = {
    "blonde":  (180, 145, 85),
    "lblonde": (200, 170, 120),
    "lbrown":  (110, 80, 50),
    "brown":   (60, 40, 25),
    "dbrown":  (35, 25, 15),
    "black":   (15, 12, 10),
    "auburn":  (95, 50, 25),
    "red":     (130, 50, 20),
    "gray":    (110, 110, 110),
}

HAIR_LIGHT = {
    "blonde":  (250, 220, 165),
    "lblonde": (255, 235, 195),
    "lbrown":  (185, 140, 95),
    "brown":   (135, 90, 60),
    "dbrown":  (95, 65, 40),
    "black":   (55, 48, 45),
    "auburn":  (180, 105, 65),
    "red":     (220, 110, 60),
    "gray":    (200, 200, 200),
}

EYES = {
    "brown": (75, 50, 30),
    "blue":  (60, 110, 175),
    "green": (70, 130, 80),
    "hazel": (130, 100, 60),
    "gray":  (110, 115, 120),
}

EYE_WHITE = (250, 245, 240)
LIP = (180, 110, 95)
LIP_WOMAN = (200, 100, 110)
SHIRT = (40, 45, 55)
SHIRT_DARK = (28, 32, 42)


# ============ Hair styles ============

def hair_short_parted(canvas, hc, hs, hl):
    """Short side-parted: classic men's cut, low volume."""
    fill_rect(canvas, 17, 5, 30, 5, hc)
    fill_rect(canvas, 15, 6, 32, 6, hc)
    fill_rect(canvas, 14, 7, 33, 7, hc)
    fill_rect(canvas, 14, 8, 33, 8, hc)
    # Part on left
    paint(canvas, [(20, 7), (21, 7), (22, 8)], hs)
    # Highlight on right swept-over hair
    fill_rect(canvas, 23, 6, 30, 6, hl)
    # Sideburns
    put(canvas, 14, 9, hs); put(canvas, 33, 9, hs)


def hair_messy(canvas, hc, hs, hl):
    """Messy, slightly tousled, asymmetric."""
    fill_rect(canvas, 16, 4, 29, 4, hc)
    fill_rect(canvas, 14, 5, 33, 5, hc)
    fill_rect(canvas, 14, 6, 33, 6, hc)
    fill_rect(canvas, 14, 7, 34, 7, hc)
    fill_rect(canvas, 14, 8, 33, 8, hc)
    # Messy tufts sticking up
    put(canvas, 18, 3, hc); put(canvas, 19, 3, hc)
    put(canvas, 24, 3, hc)
    put(canvas, 28, 3, hc); put(canvas, 27, 3, hc)
    # Highlights
    paint(canvas, [(20, 5), (25, 5), (29, 6)], hl)
    # Shadow at hairline
    paint(canvas, [(14, 9), (33, 9)], hs)


def hair_curly_short(canvas, hc, hs, hl):
    """Tight curls, lots of volume but short."""
    # Base
    fill_rect(canvas, 14, 5, 33, 8, hc)
    # Curly bumps along the top
    for x in [15, 18, 21, 24, 27, 30, 32]:
        put(canvas, x, 4, hc)
        put(canvas, x, 3, hc)
    # Curl highlights
    for x in [16, 19, 22, 25, 28, 31]:
        put(canvas, x, 4, hl)
    # Shadow on sides
    fill_rect(canvas, 14, 8, 14, 10, hs)
    fill_rect(canvas, 33, 8, 33, 10, hs)


def hair_curly_long(canvas, hc, hs, hl):
    """Longer curly hair, volume over ears."""
    fill_rect(canvas, 13, 4, 34, 9, hc)
    # Volume bumps top
    for x in [14, 17, 21, 25, 29, 32]:
        put(canvas, x, 3, hc)
        put(canvas, x, 2, hc)
    # Highlights
    for x in [16, 20, 24, 28, 31]:
        put(canvas, x, 3, hl)
    # Curls extending down to ear level
    fill_rect(canvas, 13, 10, 14, 13, hc)
    fill_rect(canvas, 33, 10, 34, 13, hc)
    paint(canvas, [(13, 13), (34, 13)], hs)


def hair_undercut(canvas, hc, hs, hl):
    """Short on sides, longer/styled on top."""
    # Top is thick
    fill_rect(canvas, 16, 4, 31, 6, hc)
    # Sides are shaved (just a thin line)
    fill_rect(canvas, 14, 7, 33, 7, hs)
    put(canvas, 14, 8, hs); put(canvas, 33, 8, hs)
    # Highlight swept on top
    fill_rect(canvas, 17, 4, 28, 4, hl)


def hair_slick_back(canvas, hc, hs, hl):
    """Slicked back hair, smooth on top, low volume."""
    fill_rect(canvas, 15, 5, 32, 6, hc)
    fill_rect(canvas, 14, 7, 33, 8, hc)
    # Slick lines from front to back
    fill_rect(canvas, 16, 5, 31, 5, hl)
    # Edge
    paint(canvas, [(14, 9), (33, 9)], hs)


def hair_fade(canvas, hc, hs, hl):
    """Modern fade: short faded sides, slightly longer top."""
    fill_rect(canvas, 16, 5, 31, 6, hc)
    fill_rect(canvas, 14, 7, 33, 7, hc)
    # Faded sides (lighter)
    fill_rect(canvas, 14, 8, 14, 10, hs)
    fill_rect(canvas, 33, 8, 33, 10, hs)
    # Highlight on top
    fill_rect(canvas, 18, 5, 29, 5, hl)


def hair_long_straight(canvas, hc, hs, hl):
    """Long straight hair for women: top + flowing down past shoulders."""
    # Top of head
    fill_rect(canvas, 16, 4, 31, 4, hc)
    fill_rect(canvas, 14, 5, 33, 5, hc)
    fill_rect(canvas, 14, 6, 33, 6, hc)
    fill_rect(canvas, 13, 7, 34, 7, hc)
    fill_rect(canvas, 13, 8, 34, 8, hc)
    # Hair flows down LEFT side past the face
    fill_rect(canvas, 11, 9, 13, 36, hc)
    fill_rect(canvas, 12, 37, 13, 41, hc)
    # And down RIGHT side
    fill_rect(canvas, 34, 9, 36, 36, hc)
    fill_rect(canvas, 34, 37, 35, 41, hc)
    # Strands behind ears (slight V down the neck)
    paint(canvas, [(13, 42), (34, 42)], hc)
    # Center parting line
    put(canvas, 23, 5, hl); put(canvas, 23, 6, hl)
    # Highlights flowing down (sun-kissed look)
    for y in range(10, 30, 4):
        put(canvas, 12, y, hl)
        put(canvas, 35, y, hl)
    # Edge shadow at the very tip
    paint(canvas, [(11, 36), (36, 36)], hs)
    paint(canvas, [(13, 41), (34, 41)], hs)


def hair_beach_blonde(canvas, hc, hs, hl):
    """Long beach-wavy blonde hair for women: wavy edges, sun-bleached highlights."""
    # Top crown
    fill_rect(canvas, 15, 4, 32, 4, hc)
    fill_rect(canvas, 13, 5, 34, 5, hc)
    fill_rect(canvas, 13, 6, 34, 6, hc)
    fill_rect(canvas, 12, 7, 35, 7, hc)
    fill_rect(canvas, 12, 8, 35, 8, hc)
    # Center part
    put(canvas, 24, 4, hl); put(canvas, 24, 5, hl)
    # Hair flows down both sides with WAVES (offset columns to suggest curls)
    # Left waves
    fill_rect(canvas, 10, 9, 13, 14, hc)
    fill_rect(canvas, 11, 15, 13, 19, hc)
    fill_rect(canvas, 10, 20, 13, 25, hc)
    fill_rect(canvas, 11, 26, 13, 31, hc)
    fill_rect(canvas, 10, 32, 13, 37, hc)
    fill_rect(canvas, 11, 38, 13, 42, hc)
    # Right waves (mirrored)
    fill_rect(canvas, 34, 9, 37, 14, hc)
    fill_rect(canvas, 34, 15, 36, 19, hc)
    fill_rect(canvas, 34, 20, 37, 25, hc)
    fill_rect(canvas, 34, 26, 36, 31, hc)
    fill_rect(canvas, 34, 32, 37, 37, hc)
    fill_rect(canvas, 34, 38, 36, 42, hc)
    # Sun-bleached highlights cascading down
    for y in [10, 16, 22, 28, 34]:
        put(canvas, 11, y, hl)
        put(canvas, 36, y, hl)
    # Soft shadows on inner edges
    for y in range(10, 40, 5):
        put(canvas, 13, y, hs)
        put(canvas, 34, y, hs)


def hair_pixie(canvas, hc, hs, hl):
    """Short pixie cut for women, slightly tousled."""
    fill_rect(canvas, 15, 4, 32, 4, hc)
    fill_rect(canvas, 13, 5, 34, 5, hc)
    fill_rect(canvas, 13, 6, 34, 6, hc)
    fill_rect(canvas, 13, 7, 34, 7, hc)
    fill_rect(canvas, 13, 8, 34, 8, hc)
    # Bangs
    fill_rect(canvas, 17, 9, 22, 9, hc)
    fill_rect(canvas, 18, 10, 21, 10, hs)
    # Highlights
    fill_rect(canvas, 16, 4, 29, 4, hl)
    # Sideburns
    put(canvas, 13, 9, hc); put(canvas, 34, 9, hc)


HAIR_STYLES = {
    "short_parted": hair_short_parted,
    "messy":        hair_messy,
    "curly_short":  hair_curly_short,
    "curly_long":   hair_curly_long,
    "undercut":     hair_undercut,
    "slick_back":   hair_slick_back,
    "fade":         hair_fade,
    "long_straight": hair_long_straight,
    "beach_blonde":  hair_beach_blonde,
    "pixie":         hair_pixie,
}


# ============ Face parts ============

def _draw_head_shape(canvas, skin_key, face_shape, female=False):
    """Draw the head silhouette."""
    s = SKIN[skin_key]
    sd = SKIN_DARK[skin_key]
    sl = SKIN_LITE[skin_key]
    # Default head shape (oval/square/long/round all very similar at 48x48)
    # Top
    fill_rect(canvas, 17, 6, 30, 6, s)
    fill_rect(canvas, 16, 7, 31, 7, s)
    fill_rect(canvas, 15, 8, 32, 8, s)
    fill_rect(canvas, 14, 9, 33, 33, s)
    # Chin shape varies a bit
    if face_shape == "round":
        fill_rect(canvas, 15, 34, 32, 34, s)
        fill_rect(canvas, 16, 35, 31, 35, s)
        fill_rect(canvas, 17, 36, 30, 36, s)
    elif face_shape == "long":
        fill_rect(canvas, 15, 34, 32, 34, s)
        fill_rect(canvas, 17, 35, 30, 35, s)
        fill_rect(canvas, 19, 36, 28, 36, s)
        fill_rect(canvas, 20, 37, 27, 37, s)
    else:  # oval / square
        fill_rect(canvas, 15, 34, 32, 34, s)
        fill_rect(canvas, 16, 35, 31, 35, s)
        fill_rect(canvas, 18, 36, 29, 36, s)
    # Female faces slightly softer: narrower jaw
    if female:
        # Trim 1px off each side at jawline
        canvas.putpixel((14, 33), (0, 0, 0, 0))
        canvas.putpixel((33, 33), (0, 0, 0, 0))
        canvas.putpixel((15, 34), (0, 0, 0, 0))
        canvas.putpixel((32, 34), (0, 0, 0, 0))
    # Shadow side
    for y in range(9, 34):
        put(canvas, 33, y, sd)
    if not female:
        for y in range(31, 34):
            put(canvas, 32, y, sd)
    # Light side
    for y in range(10, 30):
        put(canvas, 14, y, sl)


def _draw_eyes(canvas, eye_color, female=False):
    ec = EYES[eye_color]
    # Left eye
    fill_rect(canvas, 19, 21, 20, 22, EYE_WHITE)
    put(canvas, 19, 21, ec)
    put(canvas, 20, 22, ec)
    # Right eye
    fill_rect(canvas, 27, 21, 28, 22, EYE_WHITE)
    put(canvas, 27, 21, ec)
    put(canvas, 28, 22, ec)
    # Eyelashes for female (small black ticks on outer corners)
    if female:
        put(canvas, 18, 20, (15, 12, 18))
        put(canvas, 21, 20, (15, 12, 18))
        put(canvas, 26, 20, (15, 12, 18))
        put(canvas, 29, 20, (15, 12, 18))


def _draw_brows(canvas, brow_style, hair_color_key, female=False):
    """Brow shape based on style. Color matches hair (or darker if blonde)."""
    base_color = HAIR_SHADOW.get(hair_color_key, (50, 35, 25))
    if female and hair_color_key in ("blonde", "lblonde"):
        # Darken female brows so they read
        base_color = (110, 80, 50)
    if brow_style == "thick":
        paint(canvas, [(19, 19), (20, 19), (21, 19), (19, 18), (20, 18)], base_color)
        paint(canvas, [(26, 19), (27, 19), (28, 19), (27, 18), (28, 18)], base_color)
    elif brow_style == "arched":
        paint(canvas, [(19, 19), (20, 19), (21, 19), (21, 18)], base_color)
        paint(canvas, [(26, 18), (26, 19), (27, 19), (28, 19)], base_color)
    elif brow_style == "straight":
        paint(canvas, [(19, 19), (20, 19), (21, 19)], base_color)
        paint(canvas, [(26, 19), (27, 19), (28, 19)], base_color)
    else:
        paint(canvas, [(19, 19), (20, 19), (21, 19)], base_color)
        paint(canvas, [(26, 19), (27, 19), (28, 19)], base_color)


def _draw_nose(canvas, skin_key):
    sd = SKIN_DARK[skin_key]
    put(canvas, 24, 25, sd)
    put(canvas, 24, 26, sd)
    put(canvas, 23, 27, sd)
    put(canvas, 24, 27, sd)


def _draw_mouth(canvas, mouth_style, female=False):
    lip_color = LIP_WOMAN if female else LIP
    if mouth_style == "big_grin":
        # Wide open smile with teeth
        fill_rect(canvas, 20, 31, 27, 31, lip_color)
        fill_rect(canvas, 21, 32, 26, 32, EYE_WHITE)  # teeth
        fill_rect(canvas, 20, 33, 27, 33, lip_color)
    elif mouth_style == "grin":
        fill_rect(canvas, 21, 31, 26, 31, lip_color)
        fill_rect(canvas, 22, 32, 25, 32, lip_color)
        put(canvas, 20, 32, mix(lip_color, SKIN["light"], 0.4))
        put(canvas, 27, 32, mix(lip_color, SKIN["light"], 0.4))
    elif mouth_style == "smile":
        fill_rect(canvas, 21, 31, 26, 31, lip_color)
        put(canvas, 20, 32, lip_color)
        put(canvas, 27, 32, lip_color)
    elif mouth_style == "smirk":
        fill_rect(canvas, 21, 31, 26, 31, lip_color)
        put(canvas, 27, 30, lip_color)  # right corner up
    else:  # neutral
        fill_rect(canvas, 21, 31, 26, 31, lip_color)


def _draw_beard(canvas, beard_style, hair_color_key, skin_key):
    if beard_style is None or beard_style == "none":
        return
    color = HAIR_SHADOW.get(hair_color_key, (50, 35, 25))
    if beard_style == "stubble":
        # Light dots on jaw
        for x in range(17, 31, 2):
            put(canvas, x, 34, color, alpha=160)
        for x in range(18, 30, 2):
            put(canvas, x, 35, color, alpha=160)
    elif beard_style == "scruff":
        # Heavier coverage
        fill_rect(canvas, 17, 33, 30, 33, color)
        fill_rect(canvas, 16, 34, 31, 34, color)
        fill_rect(canvas, 17, 35, 30, 35, color)
        # Carve out mouth
        fill_rect(canvas, 21, 31, 26, 32, (0, 0, 0, 0))


def _draw_neck_shirt(canvas, skin_key):
    s = SKIN[skin_key]
    sd = SKIN_DARK[skin_key]
    # Neck
    fill_rect(canvas, 20, 37, 27, 41, sd)
    fill_rect(canvas, 21, 37, 26, 41, s)
    # Shirt
    fill_rect(canvas, 8,  42, 39, 47, SHIRT)
    fill_rect(canvas, 8,  42, 39, 42, mix(SHIRT, EYE_WHITE, 0.15))
    fill_rect(canvas, 19, 42, 28, 43, SHIRT_DARK)
    paint(canvas, [(20, 42), (27, 42)], SHIRT)


# ============ Public API ============

# Slugs known to be female SDRs
FEMALE_SLUGS = {"ava", "catherine", "shaune"}


def draw_personalized_face(canvas, traits):
    """Render a personalized face on the canvas.

    traits = dict with keys: slug, face_shape, hair_style, hair_color, skin,
             eyes, mouth, brow_style, beard
    """
    slug = traits.get("slug", "")
    is_female = slug in FEMALE_SLUGS or traits.get("female", False)

    skin_key = traits.get("skin", "light")
    hair_color_key = traits.get("hair_color", "brown")
    hair_style_key = traits.get("hair_style", "short_parted")
    eye_color = traits.get("eyes", "brown")
    brow_style = traits.get("brow_style", "straight")
    mouth_style = traits.get("mouth", "smile")
    beard_style = traits.get("beard")
    face_shape = traits.get("face_shape", "oval")

    # 1. Head silhouette
    _draw_head_shape(canvas, skin_key, face_shape, female=is_female)
    # 2. Hair (women: long hair has to render around the face, so do hair first
    #    so the face overlays the top of it correctly... but we already drew the
    #    head. For women, the hair has SIDE strands that go beside the face
    #    BEHIND the head. So we re-render head over hair: do hair first then head.)
    # Simpler: hair_long/beach_blonde drawing carefully positions side strands
    #          OUTSIDE the head silhouette (cols 11-13 and 34-36). Drawing hair
    #          AFTER the head works fine because hair only paints those outer
    #          columns plus the top of the skull.
    hair_fn = HAIR_STYLES.get(hair_style_key, hair_short_parted)
    hc = HAIR[hair_color_key]
    hs = HAIR_SHADOW[hair_color_key]
    hl = HAIR_LIGHT[hair_color_key]
    hair_fn(canvas, hc, hs, hl)
    # 3. Brows
    _draw_brows(canvas, brow_style, hair_color_key, female=is_female)
    # 4. Eyes
    _draw_eyes(canvas, eye_color, female=is_female)
    # 5. Nose
    _draw_nose(canvas, skin_key)
    # 6. Mouth
    _draw_mouth(canvas, mouth_style, female=is_female)
    # 7. Beard (men only)
    if not is_female:
        _draw_beard(canvas, beard_style, hair_color_key, skin_key)
    # 8. Neck + shirt
    _draw_neck_shirt(canvas, skin_key)

    return canvas


if __name__ == "__main__":
    import json
    import pathlib
    out = pathlib.Path("public/variants/_face_v2")
    out.mkdir(parents=True, exist_ok=True)
    people = json.load(open("public/auto_people.json"))
    for p in people:
        c = new_canvas()
        draw_personalized_face(c, p)
        c.save(out / f"{p['slug']}.png")
        print(f"  {p['name']:22} -> {p['slug']}.png")
    print(f"wrote {len(people)} personalized faces")
