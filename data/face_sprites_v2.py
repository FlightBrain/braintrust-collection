"""Face sprite v2 - upgraded head, eyes, brows, mouth, nose, ears, freckles, dimples.

Drop-in replacements for the corresponding draw_* functions in character_builder.py.
Same 32x32 canvas, same head bounding box (rows 9-25, cols 10-21).

Imports the helpers and palettes from character_builder so we don't redefine them.
All functions are pure side-effect: they mutate `canvas` (PIL Image) in place.

Key upgrades vs v1:
  - Heads: distinct silhouettes (long is 2 cols narrower, round is 1 row taller,
    square has flat sides, oval has tapered jaw), 1px lower-jaw shadow line,
    cheekbone highlight + shadow on both sides.
  - Eyes: 6 shapes (was 3). Every iris has a top-right white catchlight.
  - Brows: 5 styles (was 3). Furrowed angles down toward nose, raised is asymmetric.
  - Mouth: 7 kinds (was 5). Adds frown and open_o. Teeth pixel for grins.
  - Nose: 4 styles (was 3). Adds 'button' for a small round nose.
  - NEW draw_ears_v2: replaces inline ear pixels in draw_head with a sized variant.
  - NEW draw_freckles, draw_dimples: optional cosmetic details.
"""

from character_builder import (
    paint,
    fill_rect,
    mix,
    SKIN,
    SKIN_SHADOW,
    SKIN_LIGHT,
    HAIR,
    HAIR_SHADOW,
    EYE,
    LIP,
    LIP_SHADOW,
    TEETH,
    WHITE,
    BLACK,
)


# ============ HEAD V2 ============
def draw_head_v2(canvas, skin_key, face_shape="oval"):
    """Improved head: more distinct silhouettes, lower-jaw shadow line,
    cheek gradient (highlight + shadow on both sides).
    """
    s = SKIN[skin_key]
    ss = SKIN_SHADOW[skin_key]
    sl = SKIN_LIGHT[skin_key]
    # extra-dark shadow for the jaw underline (deeper depth cue)
    jaw_dark = mix(ss, BLACK, 0.25)

    if face_shape == "oval":
        # Tapered top, full middle, narrowing jaw
        for x in range(13, 19): canvas.putpixel((x, 9), s)
        for x in range(12, 20): canvas.putpixel((x, 10), s)
        fill_rect(canvas, 11, 11, 20, 22, s)
        for x in range(11, 21): canvas.putpixel((x, 23), s)
        for x in range(12, 20): canvas.putpixel((x, 24), s)
        for x in range(13, 19): canvas.putpixel((x, 25), s)
        # Lower-jaw shadow line (depth)
        paint(canvas, [(13, 26), (14, 26), (15, 26), (16, 26), (17, 26), (18, 26)], jaw_dark)
        jaw_bottom_y = 25

    elif face_shape == "round":
        # Fuller cheeks: pushes wider at row 12-22, rounder bottom
        for x in range(12, 20): canvas.putpixel((x, 9), s)
        for x in range(11, 21): canvas.putpixel((x, 10), s)
        fill_rect(canvas, 10, 11, 21, 23, s)
        for x in range(11, 21): canvas.putpixel((x, 24), s)
        for x in range(12, 20): canvas.putpixel((x, 25), s)
        # extra full-cheek pixels (jut out at row 17-18)
        canvas.putpixel((10, 18), s)
        canvas.putpixel((21, 18), s)
        # Lower-jaw shadow line
        paint(canvas, [(13, 26), (14, 26), (15, 26), (16, 26), (17, 26), (18, 26)], jaw_dark)
        jaw_bottom_y = 25

    elif face_shape == "square":
        # Flat sides top-to-bottom, sharp corners
        for x in range(11, 21): canvas.putpixel((x, 9), s)
        fill_rect(canvas, 10, 10, 21, 24, s)
        for x in range(10, 22): canvas.putpixel((x, 25), s)
        # Lower-jaw shadow runs the full square width for blockier look
        paint(canvas, [(11, 26), (12, 26), (13, 26), (14, 26), (15, 26),
                       (16, 26), (17, 26), (18, 26), (19, 26), (20, 26)], jaw_dark)
        jaw_bottom_y = 25

    elif face_shape == "long":
        # Notably thinner (cols 12-19, 2 narrower than oval)
        for x in range(13, 19): canvas.putpixel((x, 9), s)
        for x in range(12, 20): canvas.putpixel((x, 10), s)
        fill_rect(canvas, 12, 11, 19, 25, s)
        for x in range(13, 19): canvas.putpixel((x, 26), s)
        # Slim cheek inset (col 11 and 20 stay background)
        # Lower-jaw shadow line
        paint(canvas, [(14, 27), (15, 27), (16, 27), (17, 27)], jaw_dark)
        jaw_bottom_y = 26
    else:
        # fallback to oval
        for x in range(13, 19): canvas.putpixel((x, 9), s)
        for x in range(12, 20): canvas.putpixel((x, 10), s)
        fill_rect(canvas, 11, 11, 20, 22, s)
        for x in range(11, 21): canvas.putpixel((x, 23), s)
        for x in range(12, 20): canvas.putpixel((x, 24), s)
        for x in range(13, 19): canvas.putpixel((x, 25), s)
        paint(canvas, [(13, 26), (14, 26), (15, 26), (16, 26), (17, 26), (18, 26)], jaw_dark)
        jaw_bottom_y = 25

    # Cheek gradient: 1-2 pixel highlight on left, 1-2 pixel shadow on right
    # Left cheekbone highlight (forehead-to-cheek)
    paint(canvas, [(11, 12), (11, 13), (11, 14)], sl)
    paint(canvas, [(12, 12)], sl)
    # Left cheek mid-tone (subtle below highlight)
    paint(canvas, [(12, 19), (12, 20)], ss)
    # Right cheekbone shadow stack
    paint(canvas, [(20, 13), (20, 14), (20, 15), (20, 16),
                   (20, 17), (20, 18), (20, 19), (20, 20), (20, 21)], ss)
    # Right cheek deeper shadow (under cheekbone)
    paint(canvas, [(19, 21), (19, 22)], ss)
    # Forehead subtle shadow under hairline
    paint(canvas, [(13, 11), (17, 11)], ss)

    # Neck
    fill_rect(canvas, 13, jaw_bottom_y + 1, 18, jaw_bottom_y + 3, s)
    paint(canvas, [(13, jaw_bottom_y + 2), (13, jaw_bottom_y + 3)], ss)


# ============ EARS V2 (NEW) ============
def draw_ears_v2(canvas, skin_key, size="small"):
    """Draw ears at col 9 and col 22, rows 16-19. Skin + shadow colors.

    size='small'  -> 1-pixel wide ear nubs
    size='large'  -> 2-pixel wide ears with inner shadow detail
    """
    s = SKIN[skin_key]
    ss = SKIN_SHADOW[skin_key]
    if size == "small":
        paint(canvas, [(9, 17), (9, 18)], s)
        paint(canvas, [(9, 16), (9, 19)], ss)
        paint(canvas, [(22, 17), (22, 18)], s)
        paint(canvas, [(22, 16), (22, 19)], ss)
    elif size == "large":
        # left ear: 2 cols wide (8-9), 4 rows tall
        paint(canvas, [(8, 17), (8, 18), (9, 16), (9, 17), (9, 18), (9, 19)], s)
        # inner shadow groove
        paint(canvas, [(8, 16), (8, 19), (9, 17)], ss)
        # right ear: 2 cols wide (22-23)
        paint(canvas, [(22, 16), (22, 17), (22, 18), (22, 19), (23, 17), (23, 18)], s)
        paint(canvas, [(23, 16), (23, 19), (22, 17)], ss)
    else:
        # default = small
        paint(canvas, [(9, 17), (9, 18), (22, 17), (22, 18)], s)
        paint(canvas, [(9, 16), (9, 19), (22, 16), (22, 19)], ss)


# ============ EYES V2 ============
def draw_eyes_v2(canvas, color_key, eye_shape="normal"):
    """Six eye shapes. Each iris is 2x1 with a top-right white catchlight.

    Eye row anchor = 16. Whites span cols 12-14 (left) and 17-19 (right).
    """
    e = EYE[color_key]
    pupil = mix(e, BLACK, 0.55)
    iris_hi = mix(e, WHITE, 0.25)  # lighter iris pixel for depth

    # eye whites baseline (3 wide)
    L_white = [(12, 16), (13, 16), (14, 16)]
    R_white = [(17, 16), (18, 16), (19, 16)]

    if eye_shape == "normal":
        paint(canvas, L_white, WHITE)
        paint(canvas, R_white, WHITE)
        # iris 2 wide, pupil center, lighter iris edge
        paint(canvas, [(13, 16)], pupil)
        paint(canvas, [(14, 16)], iris_hi)
        paint(canvas, [(18, 16)], pupil)
        paint(canvas, [(19, 16)], iris_hi)
        # top-right catchlight
        canvas.putpixel((14, 15), WHITE)
        canvas.putpixel((19, 15), WHITE)

    elif eye_shape == "wide":
        # 2 rows tall, "awake / surprised"
        paint(canvas, L_white, WHITE)
        paint(canvas, R_white, WHITE)
        paint(canvas, [(12, 17), (13, 17), (14, 17)], WHITE)
        paint(canvas, [(17, 17), (18, 17), (19, 17)], WHITE)
        # 2x1 iris stacked
        paint(canvas, [(13, 16), (13, 17)], pupil)
        paint(canvas, [(14, 16), (14, 17)], iris_hi)
        paint(canvas, [(18, 16), (18, 17)], pupil)
        paint(canvas, [(19, 16), (19, 17)], iris_hi)
        # catchlight on top
        canvas.putpixel((14, 15), WHITE)
        canvas.putpixel((19, 15), WHITE)

    elif eye_shape == "narrow":
        # squinty: thin slit, mostly iris, dark line above
        paint(canvas, [(12, 16), (13, 16), (14, 16)], pupil)
        paint(canvas, [(17, 16), (18, 16), (19, 16)], pupil)
        # tiny gleam
        canvas.putpixel((14, 16), iris_hi)
        canvas.putpixel((19, 16), iris_hi)
        # under-line shadow
        paint(canvas, [(12, 15), (13, 15), (14, 15)], mix(pupil, BLACK, 0.3))
        paint(canvas, [(17, 15), (18, 15), (19, 15)], mix(pupil, BLACK, 0.3))

    elif eye_shape == "feminine":
        # lashes above eye, regular iris below
        paint(canvas, L_white, WHITE)
        paint(canvas, R_white, WHITE)
        paint(canvas, [(13, 16)], pupil)
        paint(canvas, [(14, 16)], iris_hi)
        paint(canvas, [(18, 16)], pupil)
        paint(canvas, [(19, 16)], iris_hi)
        # catchlight
        canvas.putpixel((14, 15), WHITE)
        canvas.putpixel((19, 15), WHITE)
        # eyelashes above eye (sweeping outward)
        paint(canvas, [(12, 15), (14, 15)], BLACK)
        paint(canvas, [(11, 14), (15, 14)], BLACK)
        paint(canvas, [(17, 15), (19, 15)], BLACK)
        paint(canvas, [(16, 14), (20, 14)], BLACK)

    elif eye_shape == "tired":
        # under-eye bags + drooping lid
        paint(canvas, L_white, WHITE)
        paint(canvas, R_white, WHITE)
        paint(canvas, [(13, 16)], pupil)
        paint(canvas, [(14, 16)], iris_hi)
        paint(canvas, [(18, 16)], pupil)
        paint(canvas, [(19, 16)], iris_hi)
        # drooping upper lid (covers catchlight area)
        paint(canvas, [(12, 15), (13, 15)], mix(pupil, BLACK, 0.4))
        paint(canvas, [(18, 15), (19, 15)], mix(pupil, BLACK, 0.4))
        # under-eye bags (slight shadow row below)
        # uses a darker tone derived from the iris so it reads as a bag
        bag = mix(pupil, BLACK, 0.55)
        paint(canvas, [(12, 17), (13, 17), (14, 17)], bag)
        paint(canvas, [(17, 17), (18, 17), (19, 17)], bag)

    elif eye_shape == "glowing":
        # theme-accent glowing dot (cyan-ish) in pupil
        glow = (180, 240, 255)
        paint(canvas, L_white, WHITE)
        paint(canvas, R_white, WHITE)
        paint(canvas, [(13, 16)], BLACK)
        paint(canvas, [(14, 16)], glow)
        paint(canvas, [(18, 16)], BLACK)
        paint(canvas, [(19, 16)], glow)
        # extra catchlight above iris for that "lit" effect
        canvas.putpixel((14, 15), glow)
        canvas.putpixel((19, 15), glow)

    else:
        # fallback: normal
        paint(canvas, L_white, WHITE)
        paint(canvas, R_white, WHITE)
        paint(canvas, [(13, 16)], pupil)
        paint(canvas, [(14, 16)], iris_hi)
        paint(canvas, [(18, 16)], pupil)
        paint(canvas, [(19, 16)], iris_hi)
        canvas.putpixel((14, 15), WHITE)
        canvas.putpixel((19, 15), WHITE)


# ============ EYEBROWS V2 ============
def draw_eyebrows_v2(canvas, hair_color_key, style="straight"):
    """Five brow styles using hair shadow color."""
    b = HAIR_SHADOW[hair_color_key]
    if style == "straight":
        paint(canvas, [(12, 14), (13, 14), (14, 14)], b)
        paint(canvas, [(17, 14), (18, 14), (19, 14)], b)
    elif style == "thick":
        # 5 wide, 2 rows tall on outer end
        paint(canvas, [(11, 14), (12, 14), (13, 14), (14, 14), (15, 14)], b)
        paint(canvas, [(16, 14), (17, 14), (18, 14), (19, 14), (20, 14)], b)
        paint(canvas, [(12, 13), (13, 13)], b)
        paint(canvas, [(18, 13), (19, 13)], b)
    elif style == "arched":
        # peak in middle
        paint(canvas, [(12, 14), (14, 14)], b)
        paint(canvas, [(13, 13)], b)
        paint(canvas, [(17, 14), (19, 14)], b)
        paint(canvas, [(18, 13)], b)
    elif style == "furrowed":
        # angles down toward nose: inner end lower than outer end
        paint(canvas, [(12, 13), (13, 13), (14, 14), (15, 14)], b)
        paint(canvas, [(16, 14), (17, 14), (18, 13), (19, 13)], b)
        # extra furrow line between brows
        paint(canvas, [(15, 15), (16, 15)], mix(b, BLACK, 0.3))
    elif style == "raised":
        # one brow raised (left brow up one pixel), other normal
        paint(canvas, [(12, 13), (13, 13), (14, 13)], b)
        paint(canvas, [(17, 14), (18, 14), (19, 14)], b)
    else:
        # fallback straight
        paint(canvas, [(12, 14), (13, 14), (14, 14)], b)
        paint(canvas, [(17, 14), (18, 14), (19, 14)], b)


# ============ NOSE V2 ============
def draw_nose_v2(canvas, skin_key, style="standard"):
    """Four nose styles. Uses skin shadow for the nose line, skin light for bridge highlight."""
    s = SKIN[skin_key]
    ss = SKIN_SHADOW[skin_key]
    sl = SKIN_LIGHT[skin_key]
    if style == "standard":
        # vertical line + hook to right at tip + bridge highlight
        paint(canvas, [(15, 18), (15, 19), (15, 20)], ss)
        paint(canvas, [(16, 20)], ss)
        canvas.putpixel((16, 18), sl)  # bridge highlight
    elif style == "wide":
        # 3 pixels wide nostrils
        paint(canvas, [(14, 19), (15, 19), (16, 19)], ss)
        paint(canvas, [(14, 20), (16, 20)], ss)
        paint(canvas, [(15, 20)], mix(ss, BLACK, 0.3))  # darker shadow under
    elif style == "subtle":
        # just a small bump
        paint(canvas, [(15, 20)], ss)
        canvas.putpixel((15, 19), sl)
    elif style == "button":
        # small round nose tip, no bridge line
        paint(canvas, [(15, 20), (16, 20)], ss)
        paint(canvas, [(15, 19), (16, 19)], s)  # filled top
        canvas.putpixel((15, 19), sl)  # tiny highlight
    else:
        paint(canvas, [(15, 18), (15, 19), (15, 20)], ss)
        paint(canvas, [(16, 20)], ss)


# ============ MOUTH V2 ============
def draw_mouth_v2(canvas, kind, skin_key=None):
    """Seven mouth kinds with better tooth/lip distinction."""
    if kind == "smile":
        # curves up at corners (top of lip line dips at center)
        paint(canvas, [(13, 23), (18, 23)], LIP)
        paint(canvas, [(14, 24), (15, 24), (16, 24), (17, 24)], LIP)
        paint(canvas, [(14, 23), (15, 23), (16, 23), (17, 23)], LIP_SHADOW)
        canvas.putpixel((15, 24), TEETH)  # tiny teeth flash

    elif kind == "grin":
        # open mouth showing teeth
        paint(canvas, [(13, 23), (14, 23), (15, 23), (16, 23), (17, 23), (18, 23)], BLACK)
        paint(canvas, [(14, 24), (15, 24), (16, 24), (17, 24)], TEETH)
        # teeth gap line
        canvas.putpixel((15, 24), mix(TEETH, BLACK, 0.15))
        paint(canvas, [(13, 24), (18, 24)], LIP_SHADOW)
        paint(canvas, [(14, 25), (15, 25), (16, 25), (17, 25)], LIP_SHADOW)

    elif kind == "big_grin":
        # wide open, both rows of teeth
        paint(canvas, [(12, 23), (13, 23), (14, 23), (15, 23), (16, 23),
                       (17, 23), (18, 23), (19, 23)], BLACK)
        paint(canvas, [(13, 24), (14, 24), (15, 24), (16, 24), (17, 24), (18, 24)], TEETH)
        # tooth gap
        canvas.putpixel((15, 24), mix(TEETH, BLACK, 0.1))
        canvas.putpixel((16, 24), mix(TEETH, BLACK, 0.1))
        paint(canvas, [(13, 25), (14, 25), (15, 25), (16, 25), (17, 25), (18, 25)], LIP_SHADOW)

    elif kind == "smirk":
        # asymmetric: right corner up
        paint(canvas, [(14, 23), (15, 23), (16, 23), (17, 23)], LIP)
        paint(canvas, [(18, 22), (17, 22)], LIP_SHADOW)
        paint(canvas, [(15, 24), (16, 24)], LIP_SHADOW)

    elif kind == "neutral":
        # flat line with slight lip
        paint(canvas, [(14, 23), (15, 23), (16, 23), (17, 23)], LIP_SHADOW)
        paint(canvas, [(15, 24), (16, 24)], LIP)

    elif kind == "frown":
        # corners down, center dips up (inverted smile)
        paint(canvas, [(13, 24), (18, 24)], LIP)
        paint(canvas, [(14, 23), (15, 23), (16, 23), (17, 23)], LIP_SHADOW)
        paint(canvas, [(15, 22), (16, 22)], LIP_SHADOW)  # center bump down

    elif kind == "open_o":
        # small "O" shape for surprise or talking
        paint(canvas, [(15, 22), (16, 22)], LIP_SHADOW)
        paint(canvas, [(14, 23), (17, 23)], LIP)
        paint(canvas, [(15, 23), (16, 23)], BLACK)  # inside mouth
        paint(canvas, [(15, 24), (16, 24)], LIP)
        paint(canvas, [(14, 24), (17, 24)], LIP_SHADOW)
    else:
        # fallback neutral
        paint(canvas, [(14, 23), (15, 23), (16, 23), (17, 23)], LIP_SHADOW)


# ============ FRECKLES (NEW, OPTIONAL) ============
def draw_freckles(canvas, skin_key):
    """Scatter 4-6 small skin-shadow pixels on the cheeks.

    Placed across the bridge of the nose and outer cheeks. Same seed every call
    so a given face is deterministic when this is enabled.
    """
    ss = SKIN_SHADOW[skin_key]
    # symmetric scatter: 6 freckles total
    paint(canvas, [
        (12, 19),  # left outer cheek
        (13, 20),  # left cheek mid
        (14, 18),  # bridge left
        (17, 18),  # bridge right
        (18, 20),  # right cheek mid
        (19, 19),  # right outer cheek
    ], ss)


# ============ DIMPLES (NEW, OPTIONAL) ============
def draw_dimples(canvas, skin_key):
    """1 pixel on each cheek in a slightly darker skin shadow tone."""
    ss = SKIN_SHADOW[skin_key]
    dimple = mix(ss, BLACK, 0.2)
    paint(canvas, [(12, 22), (19, 22)], dimple)
