#!/usr/bin/env python3
"""Auto-assign accessories from KB's picks to the 15 SDRs.

For each SDR: render the face template + their assigned accessories at 48x48,
save to public/sdrs/{slug}.png. Also writes public/sdrs/assignments.json so the
reveal page can list who got what.
"""
import json
import pathlib

from items_v3 import new_canvas
from face_template import draw_face_template

# Pull every accessory function from the merged registry.
from accessories_v3 import ACCESSORIES as ACC_V3
from accessories_head_v2 import ACCESSORIES_HEAD_V2
from accessories_eyes_v2 import ACCESSORIES_EYES_V2
from accessories_neck_v2 import ACCESSORIES_NECK_V2
from accessories_mouthface_v2 import ACCESSORIES_MOUTHFACE_V2

ACCESSORIES = {}
ACCESSORIES.update(ACC_V3)
ACCESSORIES.update(ACCESSORIES_HEAD_V2)
ACCESSORIES.update(ACCESSORIES_EYES_V2)
ACCESSORIES.update(ACCESSORIES_NECK_V2)
ACCESSORIES.update(ACCESSORIES_MOUTHFACE_V2)


# KB's 64 winners (locked in 2026-05-20).
# Saved separately for the record.
PICKS = [
    # HEAD
    "king_crown__gold", "jeweled_crown__gold", "laurel_crown__green",
    "top_hat__black", "top_hat__silver", "top_hat__red",
    "beanie__navy",
    "cowboy_hat__black", "cowboy_hat__brown",
    "devil_horns__red", "devil_horns__black",
    "halo__cyan", "halo__gold",
    "wizard_hat__blue", "wizard_hat__purple",
    "spartan_helmet__bronze",
    "motorcycle_helmet__red",
    "baseball_cap__red",
    "durag__black",
    "knight_helmet__steel",
    "crown_of_thorns__default",
    "viking_helmet__bronze",
    "headband__red", "headband__white",
    # EYES
    "pixel_shades__black", "pixel_shades__green", "pixel_shades__blue",
    "aviators__gold",
    "three_d_glasses__default",
    "vr_headset__silver",
    "cyber_visor__red", "cyber_visor__purple",
    "monocle__gold",
    "money_eyes__green",
    "x_eyes__red",
    "glowing_eyes__red",
    "heart_eyes__red", "heart_eyes__pink",
    "third_eye__purple", "third_eye__gold",
    "tear_drop_blood__default",
    # MOUTH
    "cigar__brown",
    "cigarette__white",
    "gold_grill__diamond",
    "pipe_sherlock__default",
    "bubble_gum_bubble__default",
    # NECK
    "fat_gold_chain__gold",
    "necktie__navy",
    "pearl_necklace__white",
    "brain_pendant_chain__gold",
    "gold_medallion__gold",
    # FACE
    "scar__default",
    "face_tattoo__heart", "face_tattoo__dollar",
    "blush__red",
    "kiss_print__red",
    "mustache_chevron__black", "mustache_chevron__brown",
    "beard_full__black", "beard_full__red", "beard_full__white",
    "goatee__brown", "goatee__black",
    "birthmark_star__default",
]


# === Per-SDR assignment ===
# Each SDR gets 2-4 accessories that fit their vibe / role.
# Layering order matters: face/eyes -> head -> mouth/neck.
ASSIGNMENTS = {
    "kensington": {
        "name": "Kensington Belza",
        "role": "Strategic SDR",
        "items": ["jeweled_crown__gold", "third_eye__purple", "gold_medallion__gold"],
    },
    "garrett": {
        "name": "Garrett Buchanan",
        "role": "Account Executive",
        "items": ["king_crown__gold", "cigar__brown", "beard_full__black"],
    },
    "nick": {
        "name": "Nick Gaspardone",
        "role": "Account Executive",
        "items": ["top_hat__black", "aviators__gold", "necktie__navy"],
    },
    "ryan": {
        "name": "Ryan Gwyn",
        "role": "Channel Manager",
        "items": ["brain_pendant_chain__gold", "glowing_eyes__red", "pixel_shades__black"],
    },
    "owen": {
        "name": "Owen Bloomer",
        "role": "SDR",
        "items": ["cowboy_hat__brown", "cigarette__white", "mustache_chevron__brown"],
    },
    "sacha": {
        "name": "Sacha Thompson",
        "role": "SDR",
        "items": ["baseball_cap__red", "headband__white", "bubble_gum_bubble__default"],
    },
    "duncan": {
        "name": "Duncan Lewis",
        "role": "SDR",
        "items": ["wizard_hat__purple", "crown_of_thorns__default", "goatee__black"],
    },
    "catherine": {
        "name": "Catherine Vincent",
        "role": "SDR",
        "items": ["heart_eyes__pink", "kiss_print__red", "pearl_necklace__white"],
    },
    "ava": {
        "name": "Ava Baker",
        "role": "SDR",
        "items": ["halo__gold", "heart_eyes__red", "face_tattoo__heart"],
    },
    "alec": {
        "name": "Alec Sloan",
        "role": "SDR",
        "items": ["top_hat__silver", "monocle__gold", "fat_gold_chain__gold"],
    },
    "chris": {
        "name": "Chris Koenig",
        "role": "SDR",
        "items": ["motorcycle_helmet__red", "cyber_visor__red", "scar__default"],
    },
    "joe": {
        "name": "Joe Meade",
        "role": "SDR",
        "items": ["spartan_helmet__bronze", "mustache_chevron__black", "face_tattoo__dollar"],
    },
    "keslar": {
        "name": "Keslar Simpson",
        "role": "SDR",
        "items": ["viking_helmet__bronze", "beard_full__red"],
    },
    "evan": {
        "name": "Evan O'Reilly",
        "role": "SDR",
        "items": ["durag__black", "gold_grill__diamond", "money_eyes__green"],
    },
    "shaune": {
        "name": "Shaune Lundstrom",
        "role": "SDR",
        "items": ["knight_helmet__steel", "pipe_sherlock__default", "birthmark_star__default"],
    },
}


# Render order: face tattoos/scars first (under everything), then eyes, then
# mouth/neck, then head (so hats sit on top).
LAYER_ORDER = {
    "face":  0,
    "neck":  1,
    "mouth": 2,
    "eyes":  3,
    "head":  4,
}

# Map accessory name -> category (used for layer ordering).
def category_of(name):
    head_names = {"king_crown","jeweled_crown","laurel_crown","top_hat","beanie","cowboy_hat","devil_horns","halo","wizard_hat","spartan_helmet","motorcycle_helmet","baseball_cap","durag","knight_helmet","crown_of_thorns","viking_helmet","headband"}
    eye_names  = {"pixel_shades","aviators","three_d_glasses","vr_headset","cyber_visor","monocle","eyepatch","laser_eyes","laser_eyes_rainbow","money_eyes","x_eyes","glowing_eyes","heart_eyes","hypnosis_swirl","third_eye","kaleidoscope_eyes","anime_sparkle_eyes","blindfold","skull_eye_socket","evil_red_glow","cyber_implant","tear_drop_blood"}
    mouth_names = {"cigar","cigarette","vampire_fangs","gold_grill","pipe_sherlock","joint","gold_tooth_single","lipstick","tongue_out","bubble_gum_bubble"}
    neck_names  = {"fat_gold_chain","diamond_chain","bowtie","necktie","pearl_necklace","brain_pendant_chain","dog_tags","bandana_neck","ascot","choker_spike","crystal_pendant","gold_medallion"}
    if name in head_names: return "head"
    if name in eye_names:  return "eyes"
    if name in mouth_names: return "mouth"
    if name in neck_names: return "neck"
    return "face"


def render_sdr(items):
    """Render the face template with all listed accessories layered correctly."""
    canvas = new_canvas()
    draw_face_template(canvas)
    # Sort by layer order so e.g. crown ends up on top
    sorted_items = sorted(items, key=lambda i: LAYER_ORDER[category_of(i.split("__")[0])])
    for item_id in sorted_items:
        acc_name, color = item_id.split("__", 1)
        if acc_name not in ACCESSORIES:
            print(f"  ! missing accessory: {acc_name}")
            continue
        fn, _ = ACCESSORIES[acc_name]
        color_val = None if color == "default" else color
        try:
            if color_val is None:
                fn(canvas)
            else:
                fn(canvas, color=color_val)
        except TypeError:
            fn(canvas)
    return canvas


def main():
    out = pathlib.Path("public/sdrs")
    out.mkdir(parents=True, exist_ok=True)

    # Save picks JSON for the record
    (out.parent / "picks_v18.json").write_text(json.dumps({"picks": PICKS}, indent=2))

    # Render each SDR
    written = []
    for slug, data in ASSIGNMENTS.items():
        c = render_sdr(data["items"])
        path = out / f"{slug}.png"
        c.save(path)
        written.append({
            "slug": slug,
            "name": data["name"],
            "role": data["role"],
            "items": data["items"],
            "path": f"sdrs/{slug}.png",
        })
        print(f"  rendered {data['name']:22} -> {path}")

    (out / "assignments.json").write_text(json.dumps({"sdrs": written}, indent=2))
    print(f"\nwrote {len(written)} SDR portraits + assignments.json")


if __name__ == "__main__":
    main()
