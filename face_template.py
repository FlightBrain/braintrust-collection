#!/usr/bin/env python3
"""Neutral 48x48 face/head template used as the canvas accessories sit on.

This is NOT a final character. It's a generic mannequin so KB can see how
each accessory looks on a face, like a CryptoPunks profile preview.

Face anchors (for accessory positioning):
  - Head top:    row 6
  - Hair line:   row 9
  - Brow line:   row 18
  - Eye row:     row 21..22
  - Left eye:    cols 19..20
  - Right eye:   cols 27..28
  - Nose tip:    col 24, row 26
  - Mouth row:   row 31..32
  - Mouth cols:  20..27
  - Chin:        row 36
  - Neck top:    row 38
  - Shoulder:    row 44
"""
from items_v3 import new_canvas, put, paint, fill_rect, mix
import pathlib


SKIN      = (245, 205, 175)
SKIN_DARK = (210, 165, 130)
SKIN_LITE = (255, 225, 200)
HAIR      = (75, 50, 35)
HAIR_DARK = (50, 35, 25)
EYE       = (50, 40, 35)
EYE_WHITE = (250, 245, 240)
LIP       = (180, 110, 95)
SHIRT     = (40, 45, 55)
SHIRT_DARK = (28, 32, 42)
BG        = (15, 19, 32)


def draw_face_template(canvas):
    """Draw the neutral head onto a 48x48 canvas. Returns canvas."""
    # === Head: rounded rectangle, rows 6..36 ===
    # Top rounding
    fill_rect(canvas, 17, 6,  30, 6,  SKIN)
    fill_rect(canvas, 16, 7,  31, 7,  SKIN)
    fill_rect(canvas, 15, 8,  32, 8,  SKIN)
    # Main face block
    fill_rect(canvas, 14, 9,  33, 33, SKIN)
    # Bottom rounding (chin)
    fill_rect(canvas, 15, 34, 32, 34, SKIN)
    fill_rect(canvas, 16, 35, 31, 35, SKIN)
    fill_rect(canvas, 18, 36, 29, 36, SKIN)

    # Subtle shadow on right side of face
    for y in range(9, 34):
        put(canvas, 33, y, SKIN_DARK)
        put(canvas, 32, y, SKIN_DARK) if y > 30 else None
    # Light on left side
    for y in range(10, 30):
        put(canvas, 14, y, SKIN_LITE)

    # === Hair: simple cap on top ===
    fill_rect(canvas, 17, 5, 30, 5, HAIR)
    fill_rect(canvas, 15, 6, 32, 6, HAIR)
    fill_rect(canvas, 14, 7, 33, 7, HAIR)
    fill_rect(canvas, 14, 8, 33, 8, HAIR)
    # Hairline edge fades to dark
    paint(canvas, [(14, 9), (33, 9)], HAIR_DARK)
    # Side burns
    put(canvas, 14, 10, HAIR_DARK)
    put(canvas, 33, 10, HAIR_DARK)

    # === Eyes ===
    # Left eye: cols 19-20, rows 21-22
    fill_rect(canvas, 19, 21, 20, 22, EYE_WHITE)
    put(canvas, 19, 21, EYE)
    put(canvas, 20, 22, EYE)
    # Right eye: cols 27-28
    fill_rect(canvas, 27, 21, 28, 22, EYE_WHITE)
    put(canvas, 27, 21, EYE)
    put(canvas, 28, 22, EYE)
    # Brows (thin line above each eye)
    paint(canvas, [(19, 19), (20, 19), (21, 19)], HAIR_DARK)
    paint(canvas, [(26, 19), (27, 19), (28, 19)], HAIR_DARK)

    # === Nose ===
    put(canvas, 24, 25, SKIN_DARK)
    put(canvas, 24, 26, SKIN_DARK)
    put(canvas, 23, 27, SKIN_DARK)
    put(canvas, 24, 27, SKIN_DARK)

    # === Mouth: neutral straight line ===
    fill_rect(canvas, 21, 31, 26, 31, LIP)
    put(canvas, 20, 31, mix(LIP, SKIN, 0.5))
    put(canvas, 27, 31, mix(LIP, SKIN, 0.5))

    # === Neck ===
    fill_rect(canvas, 20, 37, 27, 41, SKIN_DARK)
    fill_rect(canvas, 21, 37, 26, 41, SKIN)

    # === Shoulders / shirt ===
    fill_rect(canvas, 8,  42, 39, 47, SHIRT)
    # Shirt highlight line
    fill_rect(canvas, 8,  42, 39, 42, mix(SHIRT, EYE_WHITE, 0.15))
    # Collar
    fill_rect(canvas, 19, 42, 28, 43, SHIRT_DARK)
    paint(canvas, [(20, 42), (27, 42)], SHIRT)

    return canvas


if __name__ == "__main__":
    out = pathlib.Path("public/variants/_face")
    out.mkdir(parents=True, exist_ok=True)
    c = new_canvas()
    draw_face_template(c)
    c.save(out / "face.png")
    print(f"face template -> {out / 'face.png'}")
