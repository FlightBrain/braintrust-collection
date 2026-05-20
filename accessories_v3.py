#!/usr/bin/env python3
"""Wearable accessories at 48x48. CryptoPunks-style: items go ON the face/head.

Categories:
  HEAD:  king_crown, jeweled_crown, laurel_crown, top_hat, beanie, cowboy_hat,
         devil_horns, halo, wizard_hat, do_rag
  EYES:  pixel_shades, aviators, three_d_glasses, vr_headset, cyber_visor,
         monocle, eyepatch, laser_eyes_red, laser_eyes_blue, laser_eyes_rainbow,
         money_eyes, x_eyes, glowing_eyes
  MOUTH: cigar, cigarette, vampire_fangs, gold_grill, pipe, joint
  NECK:  fat_gold_chain, diamond_chain, bowtie, bandana
  FACE:  face_tattoo, scar, blush, mustache_handlebar

All anchored to the face template at face_template.py. Coords assume the
default head sits at rows 6..36.
"""
import math
from items_v3 import new_canvas, put, paint, fill_rect, mix, WHITE, BLACK, GOLD, GOLD_LIGHT, GOLD_DARK

# === Common palettes ===
RED    = (220, 40, 50)
BLUE   = (50, 130, 230)
GREEN  = (60, 200, 100)
PURPLE = (160, 80, 220)
CYAN   = (0, 220, 255)
PINK   = (255, 100, 180)
SILVER = (200, 205, 215)
SILVER_HI = (250, 252, 255)
SILVER_LO = (130, 135, 150)
BROWN  = (110, 70, 35)
BROWN_HI = (150, 100, 55)
BROWN_LO = (75, 45, 20)
DIAMOND = (200, 240, 255)
DIAMOND_HI = (255, 255, 255)


# ===========================================================================
# HEAD
# ===========================================================================

def king_crown(canvas, color="gold"):
    """Classic 5-spike royal crown sitting on the hairline (rows 2-6)."""
    pal_map = {
        "gold":   (GOLD, GOLD_LIGHT, GOLD_DARK),
        "silver": (SILVER, SILVER_HI, SILVER_LO),
        "rose":   ((230, 130, 150), (255, 200, 215), (180, 80, 110)),
        "cyber":  (CYAN, (200, 255, 255), (0, 130, 160)),
    }
    base, hi, dark = pal_map[color]
    # Band: rows 5-6, cols 13-34
    fill_rect(canvas, 13, 5, 34, 6, base)
    fill_rect(canvas, 13, 6, 34, 6, dark)
    fill_rect(canvas, 13, 5, 34, 5, hi)
    # 5 spikes (V-shaped peaks)
    spike_cols = [14, 19, 24, 29, 33]
    for sx in spike_cols:
        # 4-pixel tall spike
        put(canvas, sx, 4, base)
        put(canvas, sx, 3, base)
        put(canvas, sx, 2, hi)
        # Side flanks
        if sx + 1 < 35: put(canvas, sx + 1, 4, base)
        if sx - 1 >= 13: put(canvas, sx - 1, 4, base)
    # Jewels on band (3 colors for "real")
    jewel_pos = [16, 24, 32]
    jewel_colors = [(220, 30, 60), (40, 130, 230), (60, 200, 100)]
    for px, jc in zip(jewel_pos, jewel_colors):
        put(canvas, px, 6, jc)
        put(canvas, px - 1, 6, mix(jc, BLACK, 0.3))
        put(canvas, px + 1, 6, mix(jc, BLACK, 0.3))


def jeweled_crown(canvas, color="gold"):
    """Tall ornate crown with central giant gem."""
    base, hi, dark = (GOLD, GOLD_LIGHT, GOLD_DARK) if color == "gold" else (SILVER, SILVER_HI, SILVER_LO)
    # Band
    fill_rect(canvas, 13, 5, 34, 7, base)
    fill_rect(canvas, 13, 7, 34, 7, dark)
    fill_rect(canvas, 13, 5, 34, 5, hi)
    # Central peak (big)
    fill_rect(canvas, 22, 1, 26, 5, base)
    fill_rect(canvas, 22, 1, 22, 5, hi)
    # Two side peaks
    fill_rect(canvas, 17, 3, 18, 5, base)
    fill_rect(canvas, 30, 3, 31, 5, base)
    # Central giant gem (purple)
    fill_rect(canvas, 23, 2, 25, 4, PURPLE)
    put(canvas, 23, 2, mix(PURPLE, WHITE, 0.5))
    put(canvas, 25, 4, mix(PURPLE, BLACK, 0.4))
    # Smaller jewels on band
    put(canvas, 16, 6, RED); put(canvas, 32, 6, BLUE)
    put(canvas, 20, 6, GREEN); put(canvas, 28, 6, GREEN)


def laurel_crown(canvas, color="gold"):
    """Roman laurel wreath. Leaves wrap around hairline."""
    leaf_dark  = (80, 130, 60) if color == "green" else GOLD_DARK
    leaf_mid   = (130, 200, 90) if color == "green" else GOLD
    leaf_hi    = (180, 240, 130) if color == "green" else GOLD_LIGHT
    # Left side leaves (4 pairs)
    leaves_l = [(11, 9), (13, 7), (16, 6), (19, 5)]
    leaves_r = [(28, 5), (31, 6), (34, 7), (36, 9)]
    for (x, y) in leaves_l:
        put(canvas, x, y, leaf_mid); put(canvas, x + 1, y, leaf_mid)
        put(canvas, x, y - 1, leaf_hi)
        put(canvas, x + 1, y + 1, leaf_dark)
    for (x, y) in leaves_r:
        put(canvas, x, y, leaf_mid); put(canvas, x - 1, y, leaf_mid)
        put(canvas, x, y - 1, leaf_hi)
        put(canvas, x - 1, y + 1, leaf_dark)
    # Center berries (red)
    put(canvas, 23, 4, (200, 30, 40))
    put(canvas, 24, 4, (220, 50, 60))
    put(canvas, 25, 4, (200, 30, 40))


def top_hat(canvas, color="black"):
    """Tall victorian top hat."""
    if color == "black":
        base, hi, dark = (20, 22, 28), (60, 65, 75), (5, 7, 10)
    elif color == "red":
        base, hi, dark = (180, 30, 40), (230, 80, 90), (110, 15, 20)
    else:
        base, hi, dark = (80, 90, 110), (130, 140, 160), (40, 45, 55)
    # Brim: rows 7-8
    fill_rect(canvas, 11, 7, 36, 8, base)
    fill_rect(canvas, 11, 7, 36, 7, hi)
    fill_rect(canvas, 11, 8, 36, 8, dark)
    # Hat body: rows 1-6
    fill_rect(canvas, 16, 1, 31, 6, base)
    fill_rect(canvas, 16, 1, 31, 1, hi)
    fill_rect(canvas, 16, 1, 16, 6, hi)
    fill_rect(canvas, 31, 1, 31, 6, dark)
    # Hatband (lighter or contrast)
    fill_rect(canvas, 16, 5, 31, 6, mix(base, hi, 0.3))


def beanie(canvas, color="red"):
    """Knit beanie covering top of head."""
    pal = {
        "red":    ((200, 40, 50), (240, 80, 90), (140, 20, 30)),
        "navy":   ((30, 50, 110), (60, 90, 160), (15, 25, 65)),
        "green":  ((60, 150, 70), (100, 200, 110), (30, 90, 40)),
        "yellow": ((240, 200, 60), (255, 230, 100), (180, 140, 30)),
    }
    base, hi, dark = pal[color]
    fill_rect(canvas, 14, 4, 33, 9, base)
    # Brim cuff
    fill_rect(canvas, 14, 8, 33, 9, dark)
    # Knit texture (horizontal stripes)
    for y in [5, 7]:
        for x in range(14, 34, 2):
            put(canvas, x, y, mix(base, dark, 0.3))
    # Pom pom on top
    fill_rect(canvas, 22, 1, 25, 3, hi)
    put(canvas, 23, 1, WHITE)
    put(canvas, 24, 2, mix(hi, WHITE, 0.5))


def cowboy_hat(canvas, color="brown"):
    """Wide-brim cowboy hat with pinched crown."""
    base, hi, dark = (BROWN, BROWN_HI, BROWN_LO) if color == "brown" else ((50, 50, 50), (90, 90, 90), (25, 25, 25))
    # Wide brim: rows 7-8, very wide
    fill_rect(canvas, 9, 7, 38, 8, base)
    fill_rect(canvas, 9, 7, 38, 7, hi)
    fill_rect(canvas, 9, 8, 38, 8, dark)
    # Crown: rows 2-6
    fill_rect(canvas, 17, 2, 30, 6, base)
    # Pinch (darker center valley)
    fill_rect(canvas, 23, 2, 24, 4, dark)
    # Band
    fill_rect(canvas, 17, 6, 30, 6, dark)


def devil_horns(canvas, color="red"):
    """Two pointed horns sticking up from forehead."""
    if color == "red":
        base, hi, dark = (180, 30, 40), (240, 80, 90), (110, 15, 20)
    else:
        base, hi, dark = (40, 35, 30), (90, 80, 70), (20, 15, 10)
    # Left horn (curved): cols 16-18, rows 1-7
    paint(canvas, [(17, 7), (17, 6), (17, 5), (18, 4), (18, 3), (18, 2)], base)
    paint(canvas, [(17, 6), (18, 5)], hi)
    put(canvas, 19, 1, dark)  # tip
    # Right horn (mirror)
    paint(canvas, [(30, 7), (30, 6), (30, 5), (29, 4), (29, 3), (29, 2)], base)
    paint(canvas, [(30, 6), (29, 5)], hi)
    put(canvas, 28, 1, dark)
    # Inner curve shading
    put(canvas, 18, 6, dark); put(canvas, 29, 6, dark)


def halo(canvas, color="gold"):
    """Floating golden halo above the head."""
    base = GOLD if color == "gold" else CYAN
    hi   = GOLD_LIGHT if color == "gold" else (200, 255, 255)
    # Ellipse: cy=3, rx=10, ry=2.5
    for ang_deg in range(0, 360, 4):
        ang = math.radians(ang_deg)
        x = int(24 + math.cos(ang) * 10)
        y = int(3 + math.sin(ang) * 2.5)
        put(canvas, x, y, base)
    # Inner highlight ring
    for ang_deg in range(0, 360, 8):
        ang = math.radians(ang_deg)
        x = int(24 + math.cos(ang) * 8.5)
        y = int(3 + math.sin(ang) * 1.8)
        put(canvas, x, y, hi)


def wizard_hat(canvas, color="purple"):
    """Tall pointed wizard hat with stars."""
    if color == "purple":
        base, hi, dark = (90, 50, 160), (140, 100, 220), (50, 25, 100)
    elif color == "blue":
        base, hi, dark = (40, 70, 180), (90, 130, 230), (20, 35, 100)
    else:
        base, hi, dark = (20, 22, 28), (60, 65, 75), (5, 7, 10)
    # Brim
    fill_rect(canvas, 11, 8, 36, 9, base)
    fill_rect(canvas, 11, 9, 36, 9, dark)
    # Cone (point at col 24, row 0; base cols 17-31, row 8)
    for y in range(0, 8):
        # Width at this row: lerp from 1 at top to 14 at bottom
        half = int((y / 8) * 7) + 1
        cx = 24
        # Slight bend to the right
        cx_offset = int(math.sin(y * 0.3) * 1.5)
        fill_rect(canvas, cx - half + cx_offset, y, cx + half + cx_offset, y, base)
        # Left highlight
        put(canvas, cx - half + cx_offset, y, hi)
    # Stars (white sparkles)
    for (sx, sy) in [(20, 5), (27, 3), (24, 7)]:
        put(canvas, sx, sy, WHITE)
        put(canvas, sx + 1, sy, WHITE)
        put(canvas, sx, sy + 1, WHITE)


# ===========================================================================
# EYES
# ===========================================================================

def pixel_shades(canvas, color="black"):
    """Iconic CryptoPunks pixel sunglasses, 2-pixel-tall block."""
    pal = {
        "black":  (15, 15, 20),
        "red":    (180, 30, 40),
        "blue":   (40, 80, 200),
        "green":  (40, 160, 80),
        "white":  (240, 240, 240),
    }
    color_val = pal[color]
    # Lenses: 2 wide each, with bridge
    fill_rect(canvas, 18, 20, 21, 23, color_val)
    fill_rect(canvas, 26, 20, 29, 23, color_val)
    # Bridge
    fill_rect(canvas, 22, 21, 25, 21, color_val)
    # Frame top edge (lighter highlight)
    fill_rect(canvas, 18, 20, 21, 20, mix(color_val, WHITE, 0.4))
    fill_rect(canvas, 26, 20, 29, 20, mix(color_val, WHITE, 0.4))
    # Reflective glint
    put(canvas, 19, 21, mix(color_val, WHITE, 0.7))
    put(canvas, 27, 21, mix(color_val, WHITE, 0.7))


def aviators(canvas, color="gold"):
    """Teardrop aviator sunglasses."""
    frame = GOLD if color == "gold" else SILVER
    frame_dark = GOLD_DARK if color == "gold" else SILVER_LO
    lens = (40, 60, 80) if color == "gold" else (50, 50, 70)
    # Left teardrop lens
    fill_rect(canvas, 17, 20, 22, 23, lens)
    paint(canvas, [(18, 24), (19, 24), (20, 24), (21, 24)], lens)
    # Right teardrop
    fill_rect(canvas, 25, 20, 30, 23, lens)
    paint(canvas, [(26, 24), (27, 24), (28, 24), (29, 24)], lens)
    # Gold frame outline
    for x in range(17, 23):
        put(canvas, x, 19, frame); put(canvas, x, 25, frame_dark)
    for y in range(19, 25):
        put(canvas, 16, y, frame); put(canvas, 23, y, frame)
    for x in range(25, 31):
        put(canvas, x, 19, frame); put(canvas, x, 25, frame_dark)
    for y in range(19, 25):
        put(canvas, 24, y, frame); put(canvas, 31, y, frame)
    # Bridge
    fill_rect(canvas, 23, 20, 24, 20, frame)
    # Reflective gleam (curved line on lens)
    paint(canvas, [(18, 21), (19, 20)], (200, 220, 240))
    paint(canvas, [(26, 21), (27, 20)], (200, 220, 240))


def three_d_glasses(canvas, color=None):
    """Retro 3D movie glasses, one red lens, one blue."""
    # Left lens RED
    fill_rect(canvas, 17, 20, 22, 23, (220, 40, 50))
    put(canvas, 18, 21, (255, 120, 130))  # gleam
    # Right lens BLUE
    fill_rect(canvas, 25, 20, 30, 23, (40, 100, 220))
    put(canvas, 26, 21, (120, 180, 255))
    # White frame
    for x in range(17, 23):
        put(canvas, x, 19, WHITE); put(canvas, x, 24, WHITE)
    for x in range(25, 31):
        put(canvas, x, 19, WHITE); put(canvas, x, 24, WHITE)
    for y in range(19, 25):
        put(canvas, 16, y, WHITE); put(canvas, 23, y, WHITE)
        put(canvas, 24, y, WHITE); put(canvas, 31, y, WHITE)


def vr_headset(canvas, color="black"):
    """Bulky VR headset covering eyes, with strap."""
    if color == "black":
        body, hi, dark = (25, 28, 35), (70, 75, 90), (10, 12, 18)
    else:
        body, hi, dark = (180, 180, 200), (230, 230, 245), (120, 125, 140)
    # Main face plate
    fill_rect(canvas, 14, 17, 33, 26, body)
    # Top edge highlight
    fill_rect(canvas, 14, 17, 33, 17, hi)
    # Bottom edge dark
    fill_rect(canvas, 14, 26, 33, 26, dark)
    # Two lens windows (glowing cyan)
    fill_rect(canvas, 17, 20, 21, 23, (0, 30, 50))
    fill_rect(canvas, 26, 20, 30, 23, (0, 30, 50))
    # Lens glow
    put(canvas, 19, 21, CYAN); put(canvas, 27, 21, CYAN)
    put(canvas, 19, 22, mix(CYAN, WHITE, 0.5))
    put(canvas, 27, 22, mix(CYAN, WHITE, 0.5))
    # Side strap
    fill_rect(canvas, 12, 19, 13, 22, body)
    fill_rect(canvas, 34, 19, 35, 22, body)
    # Brand logo (small accent stripe)
    fill_rect(canvas, 23, 24, 24, 25, CYAN)


def cyber_visor(canvas, color="cyan"):
    """Single horizontal bar visor across both eyes, cyberpunk."""
    color_map = {
        "cyan":   (CYAN, (200, 255, 255)),
        "red":    (RED, (255, 150, 160)),
        "green":  ((40, 255, 100), (200, 255, 220)),
        "purple": (PURPLE, (220, 180, 255)),
    }
    base, hi = color_map[color]
    # Visor bar
    fill_rect(canvas, 14, 20, 33, 23, (10, 10, 15))
    # Glowing inner line
    fill_rect(canvas, 14, 21, 33, 22, base)
    fill_rect(canvas, 14, 21, 33, 21, hi)
    # End caps darker
    put(canvas, 14, 21, mix(base, BLACK, 0.4)); put(canvas, 33, 22, mix(base, BLACK, 0.4))
    # Top frame edge
    fill_rect(canvas, 13, 20, 34, 20, (40, 40, 50))


def monocle(canvas, color="gold"):
    """Single round monocle over right eye, with chain."""
    frame = GOLD if color == "gold" else SILVER
    # Lens ring (circle around right eye)
    ring_pts = [(26, 19), (27, 19), (28, 19), (29, 19),
                (25, 20), (30, 20),
                (25, 21), (30, 21),
                (25, 22), (30, 22),
                (25, 23), (30, 23),
                (26, 24), (27, 24), (28, 24), (29, 24)]
    paint(canvas, ring_pts, frame)
    # Chain dangling from monocle to shirt
    paint(canvas, [(30, 25), (31, 26), (31, 27), (32, 28), (32, 29),
                   (31, 30), (31, 31), (30, 32), (30, 33), (29, 34)], frame)
    # Glint
    put(canvas, 27, 20, (220, 230, 250))


def eyepatch(canvas, color="black"):
    """Pirate eyepatch over left eye, with strap."""
    base = (15, 15, 18) if color == "black" else (90, 50, 30)
    hi = (40, 40, 45) if color == "black" else (130, 80, 50)
    # Patch
    fill_rect(canvas, 17, 20, 22, 24, base)
    # Curved bottom
    paint(canvas, [(17, 25), (22, 25)], base)
    put(canvas, 19, 25, base); put(canvas, 20, 25, base); put(canvas, 21, 25, base)
    # Highlight
    fill_rect(canvas, 18, 20, 19, 21, hi)
    # Strap across forehead
    for x in range(14, 35):
        put(canvas, x, 17, base)


def laser_eyes(canvas, color="red"):
    """Glowing laser beams shooting from each eye, all the way to canvas edge."""
    color_map = {
        "red":    ((255, 30, 30), (255, 150, 150)),
        "blue":   ((30, 130, 255), (150, 200, 255)),
        "green":  ((30, 255, 100), (180, 255, 200)),
        "purple": (PURPLE, (220, 180, 255)),
        "white":  (WHITE, WHITE),
    }
    base, hi = color_map[color]
    # Eye glow (white-hot core where eyeballs were)
    fill_rect(canvas, 19, 20, 20, 23, WHITE)
    fill_rect(canvas, 27, 20, 28, 23, WHITE)
    # Beams shooting outward and down (toward viewer)
    # Left eye beam: cols 18-21 going outward
    for dy in range(0, 4):
        for dx in range(-5, 6):
            x = 19 + dx + dy
            y = 22 + dy
            if 0 <= x < 48 and 0 <= y < 48:
                alpha = 220 if abs(dx) <= 1 else 140
                if dy == 0:
                    put(canvas, x, y, hi, alpha=alpha)
                else:
                    put(canvas, x, y, base, alpha=alpha)
    # Right eye beam, mirrored
    for dy in range(0, 4):
        for dx in range(-5, 6):
            x = 28 + dx - dy
            y = 22 + dy
            if 0 <= x < 48 and 0 <= y < 48:
                alpha = 220 if abs(dx) <= 1 else 140
                if dy == 0:
                    put(canvas, x, y, hi, alpha=alpha)
                else:
                    put(canvas, x, y, base, alpha=alpha)
    # Outer glow blob around eyes
    for (cx, cy) in [(19, 21), (28, 21)]:
        for r_dy in range(-2, 3):
            for r_dx in range(-3, 4):
                if r_dx*r_dx + r_dy*r_dy > 5: continue
                x, y = cx + r_dx, cy + r_dy
                existing = canvas.getpixel((x, y))
                if existing[3] < 200:
                    put(canvas, x, y, hi, alpha=120)


def laser_eyes_rainbow(canvas, color=None):
    """Same as laser_eyes but each beam cycles through rainbow colors."""
    rainbow = [(255, 40, 40), (255, 150, 40), (255, 230, 40), (40, 200, 80), (40, 130, 255), (160, 80, 220)]
    # Eye core
    fill_rect(canvas, 19, 20, 20, 23, WHITE)
    fill_rect(canvas, 27, 20, 28, 23, WHITE)
    # Beams with color stripes
    for dy in range(0, 5):
        c = rainbow[dy % len(rainbow)]
        for dx in range(-3, 4):
            x_l = 19 + dx + dy
            x_r = 28 + dx - dy
            y = 22 + dy
            for x in [x_l, x_r]:
                if 0 <= x < 48 and 0 <= y < 48:
                    put(canvas, x, y, c, alpha=200 if abs(dx) <= 1 else 130)


def money_eyes(canvas, color="green"):
    """Dollar signs where the eyes are. Cha-ching."""
    sign = (60, 200, 100) if color == "green" else GOLD
    sign_hi = (160, 255, 180) if color == "green" else GOLD_LIGHT
    # $ pixel pattern, 3 wide x 5 tall
    pattern = [
        ".#.",
        "###",
        "#..",
        "###",
        "..#",
        "###",
        ".#.",
    ]
    for (cx, cy) in [(19, 19), (27, 19)]:
        for ry, row in enumerate(pattern):
            for rx, ch in enumerate(row):
                if ch == "#":
                    x, y = cx + rx, cy + ry
                    put(canvas, x, y, sign)
                    if rx == 0:
                        put(canvas, x, y, sign_hi)


def x_eyes(canvas, color="black"):
    """X marks the spot. KO'd."""
    c = (15, 15, 20) if color == "black" else RED
    # Left X
    for d in range(0, 4):
        put(canvas, 18 + d, 20 + d, c)
        put(canvas, 21 - d, 20 + d, c)
    # Right X
    for d in range(0, 4):
        put(canvas, 26 + d, 20 + d, c)
        put(canvas, 29 - d, 20 + d, c)


def glowing_eyes(canvas, color="white"):
    """Solid glowing eyes with no pupils, demonic."""
    color_map = {
        "white":  (WHITE, (200, 230, 255)),
        "red":    ((255, 60, 70), (255, 200, 200)),
        "cyan":   (CYAN, (200, 255, 255)),
        "yellow": ((255, 230, 40), (255, 250, 180)),
    }
    base, glow = color_map[color]
    fill_rect(canvas, 19, 20, 20, 23, base)
    fill_rect(canvas, 27, 20, 28, 23, base)
    # Outer halo glow
    for (cx, cy) in [(19, 21), (27, 21)]:
        for dx in [-1, 0, 1, 2]:
            for dy in [-1, 0, 1, 2]:
                if dx == 0 and dy == 0: continue
                x, y = cx + dx, cy + dy
                if canvas.getpixel((x, y))[3] < 200:
                    put(canvas, x, y, glow, alpha=110)


# ===========================================================================
# MOUTH
# ===========================================================================

def cigar(canvas, color="brown"):
    """Lit cigar in mouth, with ember and smoke."""
    body = (95, 60, 35)
    band = GOLD
    ember = (255, 100, 30)
    # Cigar body sticking out to the right
    fill_rect(canvas, 26, 31, 35, 32, body)
    # Gold band near mouth
    fill_rect(canvas, 27, 31, 28, 32, band)
    # Ember tip
    fill_rect(canvas, 36, 31, 37, 32, ember)
    put(canvas, 37, 31, WHITE)
    # Smoke wisps
    paint(canvas, [(37, 28), (38, 26), (37, 24), (36, 22)], (180, 180, 200), alpha=180)


def cigarette(canvas, color="white"):
    """Thin lit cigarette."""
    fill_rect(canvas, 26, 32, 35, 32, WHITE)
    # Filter end
    fill_rect(canvas, 26, 32, 28, 32, (220, 200, 130))
    # Ember
    put(canvas, 36, 32, (255, 80, 30))
    # Smoke
    paint(canvas, [(36, 29), (37, 27), (36, 25)], (200, 200, 220), alpha=160)


def vampire_fangs(canvas, color=None):
    """Two pointy fangs hanging from upper lip."""
    fang = WHITE
    fang_shade = (220, 220, 200)
    # Left fang
    put(canvas, 22, 31, fang); put(canvas, 22, 32, fang); put(canvas, 22, 33, fang_shade)
    # Right fang
    put(canvas, 25, 31, fang); put(canvas, 25, 32, fang); put(canvas, 25, 33, fang_shade)
    # Red lip behind
    fill_rect(canvas, 21, 31, 26, 31, (160, 30, 40))


def gold_grill(canvas, color="gold"):
    """Gold teeth grill across the mouth."""
    g = GOLD if color == "gold" else (200, 240, 255)  # gold or diamond
    g_hi = GOLD_LIGHT if color == "gold" else WHITE
    fill_rect(canvas, 20, 31, 27, 32, g)
    # Tooth divisions
    for x in [21, 23, 25]:
        put(canvas, x, 31, mix(g, BLACK, 0.3))
        put(canvas, x, 32, mix(g, BLACK, 0.3))
    # Highlight row
    fill_rect(canvas, 20, 31, 27, 31, g_hi)


# ===========================================================================
# NECK
# ===========================================================================

def fat_gold_chain(canvas, color="gold"):
    """Thick rope chain around the neck with pendant."""
    c = GOLD if color == "gold" else SILVER
    c_hi = GOLD_LIGHT if color == "gold" else SILVER_HI
    c_dark = GOLD_DARK if color == "gold" else SILVER_LO
    # Chain links across collarbone (row 40-41)
    for x in range(11, 37, 2):
        put(canvas, x, 40, c)
        put(canvas, x + 1, 40, c_hi)
        put(canvas, x, 41, c_dark)
    # Pendant: BT logo or just a big gold square gem
    fill_rect(canvas, 22, 42, 26, 46, c)
    fill_rect(canvas, 22, 42, 22, 46, c_hi)
    fill_rect(canvas, 26, 42, 26, 46, c_dark)
    # BT symbol on pendant (simple brain shape)
    fill_rect(canvas, 23, 43, 25, 45, mix(c, BLACK, 0.4))


def diamond_chain(canvas, color="white"):
    """Iced-out diamond chain."""
    # Each "link" is a diamond
    for x in range(11, 37, 3):
        put(canvas, x, 40, DIAMOND_HI)
        put(canvas, x + 1, 40, DIAMOND)
        put(canvas, x, 41, DIAMOND)
        put(canvas, x + 1, 41, mix(DIAMOND, BLACK, 0.3))
    # Diamond pendant
    fill_rect(canvas, 22, 42, 26, 46, DIAMOND)
    fill_rect(canvas, 22, 42, 22, 46, DIAMOND_HI)
    # Sparkle
    put(canvas, 23, 43, WHITE)
    put(canvas, 25, 45, WHITE)


def bowtie(canvas, color="red"):
    """Classy bowtie on shirt collar."""
    color_map = {
        "red":    ((180, 30, 40), (230, 80, 90), (110, 15, 20)),
        "black":  ((20, 20, 25), (60, 60, 70), (5, 5, 10)),
        "purple": (PURPLE, (220, 180, 255), (60, 30, 100)),
    }
    base, hi, dark = color_map[color]
    # Left wing
    fill_rect(canvas, 20, 42, 22, 44, base)
    put(canvas, 20, 42, dark); put(canvas, 20, 44, dark)
    put(canvas, 21, 43, hi)
    # Center knot
    fill_rect(canvas, 23, 42, 24, 44, dark)
    # Right wing
    fill_rect(canvas, 25, 42, 27, 44, base)
    put(canvas, 27, 42, dark); put(canvas, 27, 44, dark)
    put(canvas, 26, 43, hi)


# ===========================================================================
# FACE
# ===========================================================================

def face_tattoo(canvas, color="black"):
    """Small teardrop tattoo under right eye."""
    c = (15, 15, 20) if color == "black" else PURPLE
    put(canvas, 28, 23, c)
    put(canvas, 27, 24, c); put(canvas, 28, 24, c)
    put(canvas, 28, 25, c)


def scar(canvas, color=None):
    """Diagonal scar across left cheek."""
    c = (180, 100, 90)
    paint(canvas, [(15, 22), (16, 23), (17, 24), (18, 25), (19, 26)], c)
    # Cross-hatch (stitches)
    paint(canvas, [(15, 23), (17, 23), (19, 25)], mix(c, BLACK, 0.4))


def mustache_handlebar(canvas, color="black"):
    """Curled handlebar mustache."""
    c = (30, 25, 20) if color == "black" else (130, 90, 50)
    # Center bar under nose
    fill_rect(canvas, 21, 29, 26, 30, c)
    # Curls on each end
    paint(canvas, [(19, 29), (20, 29), (20, 28), (19, 28)], c)
    paint(canvas, [(27, 29), (28, 29), (28, 28), (27, 28)], c)


def blush(canvas, color="pink"):
    """Pink blush on both cheeks."""
    c = (255, 150, 180)
    fill_rect(canvas, 15, 26, 17, 27, c)
    fill_rect(canvas, 31, 26, 33, 27, c)


# === REGISTRY ===

ACCESSORIES = {
    # HEAD
    "king_crown":         (king_crown,         ["gold", "silver", "rose", "cyber"]),
    "jeweled_crown":      (jeweled_crown,      ["gold", "silver"]),
    "laurel_crown":       (laurel_crown,       ["gold", "green"]),
    "top_hat":            (top_hat,            ["black", "red", "silver"]),
    "beanie":             (beanie,             ["red", "navy", "green", "yellow"]),
    "cowboy_hat":         (cowboy_hat,         ["brown", "black"]),
    "devil_horns":        (devil_horns,        ["red", "black"]),
    "halo":               (halo,               ["gold", "cyan"]),
    "wizard_hat":         (wizard_hat,         ["purple", "blue", "black"]),

    # EYES
    "pixel_shades":       (pixel_shades,       ["black", "red", "blue", "green", "white"]),
    "aviators":           (aviators,           ["gold", "silver"]),
    "three_d_glasses":    (three_d_glasses,    [None]),
    "vr_headset":         (vr_headset,         ["black", "silver"]),
    "cyber_visor":        (cyber_visor,        ["cyan", "red", "green", "purple"]),
    "monocle":            (monocle,            ["gold", "silver"]),
    "eyepatch":           (eyepatch,           ["black", "brown"]),
    "laser_eyes":         (laser_eyes,         ["red", "blue", "green", "purple", "white"]),
    "laser_eyes_rainbow": (laser_eyes_rainbow, [None]),
    "money_eyes":         (money_eyes,         ["green", "gold"]),
    "x_eyes":             (x_eyes,             ["black", "red"]),
    "glowing_eyes":       (glowing_eyes,       ["white", "red", "cyan", "yellow"]),

    # MOUTH
    "cigar":              (cigar,              ["brown"]),
    "cigarette":          (cigarette,          ["white"]),
    "vampire_fangs":      (vampire_fangs,      [None]),
    "gold_grill":         (gold_grill,         ["gold", "diamond"]),

    # NECK
    "fat_gold_chain":     (fat_gold_chain,     ["gold", "silver"]),
    "diamond_chain":      (diamond_chain,      ["white"]),
    "bowtie":             (bowtie,             ["red", "black", "purple"]),

    # FACE
    "face_tattoo":        (face_tattoo,        ["black", "purple"]),
    "scar":               (scar,               [None]),
    "mustache_handlebar": (mustache_handlebar, ["black", "brown"]),
    "blush":              (blush,              ["pink"]),
}


if __name__ == "__main__":
    # Smoke test: render each at default
    import pathlib
    from face_template import draw_face_template
    out = pathlib.Path("public/variants/_acc_smoke")
    out.mkdir(parents=True, exist_ok=True)
    for name, (fn, colors) in ACCESSORIES.items():
        c = new_canvas()
        draw_face_template(c)
        try:
            fn(c, color=colors[0])
        except TypeError:
            fn(c)
        c.save(out / f"{name}.png")
    print(f"wrote {len(ACCESSORIES)} accessory smoke tests")
