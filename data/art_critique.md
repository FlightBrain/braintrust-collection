# Pixel Art Critique, Braintrust NFT Collection

Reviewer: pixel art quality pass on `character_builder.py` and 20+ sample PNGs from `public/pixels/corporate/`.

Sample reviewed: alec, ava, catherine, kensington, garrett, joe, ryan, duncan, shaune, evan, chris, keslar, nick, owen, sacha, walton, dave-smith, ankur, lexi, morgane, jack-bullard, jay, bryan, nathan, manu, tony, sarah-zeng, clarissa, martin, saralyn, casey, austin, eden, mengying, ornella, pb, jack-gardner, ameya, austin-c, luca, john-huang, jaiden, austin-moehle, drew, dan, renee, phil-h.

Photo pairs compared: kensington, catherine, joe, walton, bryan, ava, nathan, garrett, jay, sacha.

---

## TL;DR

The art is currently in a weird "almost-Minecraft" zone, not a polished NFT zone. The biggest problems:

1. Every character has the **same face shape, same eye position, same mouth row, same nose**. Silhouettes are identical. You cannot tell anyone apart from 30 feet.
2. The **eyes are broken**: the "normal" pupil math collapses iris/pupil into a single 1px dark dot, and the highlight is placed in the eyebrow gap row so it floats above the eye instead of being inside the iris. Wide eyes always look up-and-left.
3. **Mouths are giant black bars or weirdly low**. The "big_grin" is a hard black rectangle that reads as a mail slot, not a smile. About half the collection has this.
4. The **face is too long for the `long` variant** (female characters get a chin sag that reads as weeping / distress).
5. **Skin has almost no shading**, just one column of shadow on the right ear/jaw, so faces look like flat cardboard cut-outs.
6. **Hair is a flat color cap**. There are 10 hair functions but visually most read identical because every one is "fill the same dome, drop in 2-3 highlight pixels."
7. **No body / shoulders**. Everyone is a floating head plus a 4-row shirt block with no shoulder structure. The neck floats unconnected to a torso.
8. **Accessory layer collisions**. Garrett's aviators are not visible. Joe's sunglasses partially render. Owen's beanie is missing. Several characters look like the data does not match what is drawn.

---

## 1. Top 5 visual problems and concrete fixes

### Problem 1: Eyes are mathematically broken

**What's wrong:** In `draw_eyes` for `eye_shape="normal"`:
- Whites are painted at `(12,16),(13,16),(14,16)` and `(17,16),(18,16),(19,16)`, 3px wide each.
- Iris is painted at `(13,16)` and `(18,16)`, the center pixel of each white block. Fine so far.
- Pupil is painted on the SAME pixel as iris with `mix(e, BLACK, 0.5)`, so the iris is fully overwritten and there's no visible iris ring, just a single dark dot.
- "Highlight" pixels go at `(14,15)` and `(19,15)`, which is row 15, the row BETWEEN the eyebrows (row 14) and the eye whites (row 16). The highlights end up floating in the forehead gap as random white specks (see Alec, Jay, Joe, where there's a stray white pixel above each eye).

**Why it looks bad:** Every character ends up with two solid dark dots for eyes plus stray pixels above them. There's no sense of gaze direction, no color, no life. The four EYE colors in the palette (`brown/blue/green/hazel`) are functionally invisible because they get immediately overwritten by the pupil.

**Concrete fix:** Make eyes 2 rows tall, fix the pupil/highlight stacking:
```python
def draw_eyes(canvas, color_key, eye_shape="normal", skin_key="light"):
    e = EYE[color_key]
    ss = SKIN_SHADOW[skin_key]
    if eye_shape == "normal":
        # Whites rows 16-17, 2px wide each
        fill_rect(canvas, 12, 16, 13, 17, WHITE)
        fill_rect(canvas, 18, 16, 19, 17, WHITE)
        # Iris fills lower pixel of each white (looking forward, slightly down)
        paint(canvas, [(12, 17), (18, 17)], e)
        # Pupil at outer-lower pixel of each iris
        paint(canvas, [(13, 17), (19, 17)], mix(e, BLACK, 0.7))
        # Highlight: 1px white at TOP-INNER of each iris (catches light)
        paint(canvas, [(12, 16), (18, 16)], WHITE)
        # Soft eyelid shadow row above (between brow row 14 and eye row 16)
        paint(canvas, [(12, 15), (13, 15), (18, 15), (19, 15)], ss)
```
Row 15 becomes a real eyelid shadow, not a floating sparkle. Iris color is now visible. Pupil is distinct from iris.

### Problem 2: Mouth is a black mail-slot

**What's wrong:** The `big_grin` mouth paints `(12,23)...(19,23)` solid `BLACK` for 8 pixels straight, then teeth fill below. There's no curvature, no lip color above, no corners that go up. It reads as a horizontal black bar across the lower face. Look at Alec, Catherine (with red lips it's a red bar), Kensington, Saralyn, Eden, Austin: all the same hard rectangle.

`smile` is slightly better (LIP color, then LIP_SHADOW row below) but it's the same flat 6px rectangle, no upturn at corners.

`grin` is the most natural-looking but only a few characters use it.

**Why it looks bad:** A smile in pixel art needs an upturn at the corners. Without it, every "happy" face looks like a frown or a deadpan slot. Worse, the lip color (200,130,115) is too saturated and warm, it reads as messy lipstick on men.

**Concrete fix:** All smile mouths should curve at the corners and be 2 rows shorter (6px wide max, not 8). Replace `draw_mouth`:
```python
# smile (closed, upturned corners)
paint(canvas, [(13, 24), (18, 24)], LIP_SHADOW)  # corners drop down a row
paint(canvas, [(14, 23), (15, 23), (16, 23), (17, 23)], LIP)  # upper lip
paint(canvas, [(14, 24), (17, 24)], LIP)  # lower lip middle

# grin (teeth showing, upturned corners)
paint(canvas, [(13, 24), (18, 24)], BLACK)  # corner pixels drop
paint(canvas, [(14, 23), (15, 23), (16, 23), (17, 23)], BLACK)  # thin upper line
paint(canvas, [(14, 24), (15, 24), (16, 24), (17, 24)], TEETH)
paint(canvas, [(13, 25), (18, 25)], LIP_SHADOW)  # bottom lip subtle

# big_grin: cap at 6px wide, not 8px
paint(canvas, [(12, 24), (19, 24)], BLACK)  # corners that turn UP
paint(canvas, [(13, 23), (14, 23), (15, 23), (16, 23), (17, 23), (18, 23)], BLACK)
paint(canvas, [(13, 24), (14, 24), (15, 24), (16, 24), (17, 24), (18, 24)], TEETH)
# remove the (15, 25), (16, 25) lower-lip pixels that look like drool
# add smile lines / dimples instead
paint(canvas, [(12, 22), (19, 22)], mix(LIP_SHADOW, SKIN[skin_key], 0.5))
```

### Problem 3: Long-face proportion catastrophe for women

**What's wrong:** `face_shape="long"` in `draw_head` paints rows 9-26 (18 rows tall, 2 taller than oval). But the eye row stays at 16 and the mouth row stays at 23. So a `long` face has:
- 7 rows of forehead above the eye
- 7 rows of mid-face from eye to mouth
- 4 rows of chin below the mouth

That chin-to-neck distance is what makes Ava, Catherine, Saralyn, Renee, Ornella look like a frowning Modigliani painting. Combined with the dark long_straight hair flanking each side, the face looks gaunt and stretched.

**Why it looks bad:** Real face proportions have eyes roughly at the vertical midline. Here, the eyes are 7 rows from top of head and 9 rows from chin. The chin is way too long. It pushes the mouth visually high, and the empty skin below the mouth reads as a sad sag.

**Concrete fix:** When face_shape is `long`, push features DOWN to match. Add a `y_offset` parameter in `build()`:
```python
y_off = 1 if person.get("face_shape") == "long" else 0
draw_eyes(canvas, person["eyes"], ..., y_off=y_off)
draw_eyebrows(canvas, ..., y_off=y_off)
draw_nose(canvas, ..., y_off=y_off)
draw_mouth(canvas, ..., y_off=y_off)
```
Then each draw function adds `y_off` to every Y coordinate. Eyes drop to row 17, brow to row 15, mouth to row 24.

Alternative simpler fix: shorten the `long` face to 16 rows tall, with the extra row added to the FOREHEAD, not the chin:
```python
elif face_shape == "long":
    for x in range(13, 19): canvas.putpixel((x, 8), s)
    for x in range(12, 20): canvas.putpixel((x, 9), s)
    fill_rect(canvas, 11, 10, 20, 24, s)
    for x in range(12, 20): canvas.putpixel((x, 25), s)
```

### Problem 4: Skin is flat cardboard

**What's wrong:** `draw_head` puts ONE column of shadow on the right side (col 20, rows 13-21) and a tiny 3-pixel highlight on the left (col 11, rows 13-15). That's it for face shading on roughly 190 face pixels. The face reads as a flat construction-paper cutout.

There's no:
- Nose shadow integrated with the face
- Cheek warmth/blush
- Forehead highlight (where light hits a real face)
- Under-eye soft shadow
- Lower jaw shadow (where chin meets neck)
- Side-of-face shading on the LEFT (currently only the right side gets shadow)

**Why it looks bad:** Compare to any CryptoPunk or pixel portrait. Skin always has at least 2 tones and ideally 3 (light, mid, shadow). The current art has 1 tone for 95% of the face.

**Concrete fix:** Add three more passes to `draw_head` after the base skin fill:
```python
# Forehead highlight (top of face catches light, runs along brow line)
paint(canvas, [(13, 11), (14, 11), (15, 11), (16, 11), (17, 11), (18, 11)], sl)
paint(canvas, [(13, 12), (18, 12)], sl)
# Left jaw shadow (mirror of right) - softer, just 1 col
paint(canvas, [(11, 19), (11, 20), (11, 21)], mix(s, ss, 0.5))
# Under-eye shadow (subtle dark crescent, row below the eye)
paint(canvas, [(12, 18), (19, 18)], mix(s, ss, 0.3))
# Chin shadow (row below mouth)
paint(canvas, [(14, 25), (15, 25), (16, 25), (17, 25)], mix(s, ss, 0.3))
# Cheek warmth (2 pixels each side, lower face)
paint(canvas, [(12, 20), (19, 20)], mix(s, (240, 150, 130), 0.3))
# Nose-side highlight (left side of nose catches light)
paint(canvas, [(14, 19), (14, 20)], sl)
```

### Problem 5: Hair is interchangeable

**What's wrong:** Looking at alec (slick_back), kensington (undercut), eden (undercut), pb (messy), john-huang (messy), keslar (curly_short), manu (messy), nick (short_parted), dave-smith (messy), drew (messy), evan (messy), joe (short_parted), tony (short_parted): these all read as the same brown-fade dome with 2-3 slightly darker pixels on top. The `undercut` is the ONLY style that's visually distinct.

Issues:
- All hair occupies the same rows (5-12).
- Highlights are 2-3 pixels in approximately the same positions.
- `messy`, `short_parted`, and `fade` are visually 90% identical at 32x32 because they all fill the same dome.
- No volume on top of head, every hairstyle gives a uniform flat-top look (Kensington's undercut looks like a solid block of brown, not "messy spiky hair on top with shaved sides").

**Why it looks bad:** In a 79-character collection, ~50 characters look like they got the same haircut. That destroys the "unique character" feel an NFT collection needs.

**Concrete fix (silhouette differentiation):**
- `slick_back`: hair should be 1 row TALLER than the rest (row 5-9 dome) with visible diagonal "slicked" highlight streaks going back. Currently it's identical to short_parted.
- `short_parted`: add a visible part. Pixels on row 9 at col 16-17 should be SKIN color, not hair, to suggest the part line cutting through.
- `messy`: needs jagged TOP edge. Currently the top of `messy` is `(11,5), (14,5), (17,5), (20,5)` then a full row at 6. Spike it: add pixels at row 4 at `(12, 4), (16, 4), (19, 4)` for alternating heights.
- `fade`: needs visible buzz contrast. The sides (col 10, 21, rows 9-12) should be SKIN color with a darker shadow stipple, not hair color.
- `curly_short`: add bumpy top edge. Paint `(11,4),(14,4),(17,4),(20,4)` in addition to row 5 for visible curl-bumps above the dome.
- Reduce row span to 6-11 (6 rows) for short cuts so face has more breathing room above the brow.

Also add **3-tone shading** to every hair function:
```python
# In every hair fn after the main fill:
# Shadow row at back of head
for x in range(10, 22): canvas.putpixel((x, 9), hs)
# Highlight cluster on the top-left (light source from upper-left)
paint(canvas, [(11, 6), (12, 6), (12, 7), (13, 7)], hl)
```

---

## 2. Pixel art principles checklist

Scoring 1-5 (1 = bad, 5 = great):

| Principle | Score | Notes |
|---|---|---|
| Strong silhouettes | **2/5** | All faces are roughly oval, same 12-wide head, same hair-dome shape. The only differentiators are hairstyle (10 options that read as 4 distinct silhouettes) and accessories (cap, beanie, sunglasses, snorkel). Without accessories or color, you can't tell who is who. |
| Limited intentional palette | **3/5** | The palette is reasonable (5 skin tones, 7 hair tones, 4 eye colors) but colors are too desaturated and similar in value. `light` skin (252,224,194) vs `light_warm` (245,205,170) is a 7-step difference per channel, invisible at 32x32. The trait background colors are saturated (#00FF94 etc) but they get muted to 78% black mix so the BG is barely distinguishable across characters. |
| No anti-aliasing | **5/5** | This is done right. `Image.NEAREST` scaling preserves crisp pixels. No subpixel artifacts. |
| Pixel placement intention | **2/5** | Many pixels are wasted. The eye highlight in the eyebrow gap (Problem 1) is a bug. The mouth bar (Problem 2) is unintentional flatness. The cheek shadow at `(12,21),(19,21)` is just 2 random pixels that read as zits. The right-ear shadow (col 20, rows 13-21) is so consistent across faces it becomes a "Braintrust character mark" rather than a depth cue. |
| Feature proportions | **2/5** | Eyes are too small (effectively 1px iris). Eyebrows are too thick (3px wide, 1px tall, they read as bars). Nose is acceptable (3px vertical). Mouth is too wide (6-8px) for the 12-wide face. Forehead is too tall (4-5 rows from hairline to brow). |
| Distinct hair shapes | **2/5** | Undercut, curly_long, long_straight, long_wavy, beach_blonde have distinct outlines. Short_parted, slick_back, messy, curly_short, fade are visually 90% identical at this resolution. |
| Skin shading and depth | **1/5** | One column of shadow plus 3 highlight pixels. Faces are flat cards. No nose-side shading, no jaw shadow, no forehead highlight, no cheek tone. |
| Clothing detail | **3/5** | Suit_tie, hoodie, button_up are fine. Polo and sweater are nearly indistinguishable (a 4-pixel collar variation). Tshirt has only a 4-pixel collar accent and reads as "shirtless with a barcode." Zip_up is a black strip down the middle, looks like the character is holding a TV remote. |
| Color harmony | **3/5** | The dark muted backgrounds work together as a collection. Trait colors (the corner brackets) pop nicely. But the gold/silver signature items (chain, watch, necklace_gold) clash with the muted skin tones, they look pasted on from a different palette. |

**Overall: 2.5/5.** Competent technical pixel art but lacking the intentional design choices that make a collection memorable.

---

## 3. Reference research, what to emulate

### CryptoPunks (24x24)
**Style:** Chunky, low-fidelity, every face uses the SAME base head and varies attributes (hair, accessory, skin). The genius is the attribute combinatorics: 10000 punks from ~7 base heads and dozens of accessories. Silhouettes are weak (almost all punks are identical front-facing busts) but the attributes are SO varied and recognizable (cigarette, 3D glasses, beanie, mohawk) that you ID a punk by accessory, not face.

**Lesson:** We're already on this template (same base head, vary the attributes). What we lack is **attribute distinctness**. Our hat vs no-hat is clear, our hair shapes are not. Increase the visual distance between attributes.

### BAYC (Bored Apes)
**Illustrated, not pixel.** Skip. Not a pixel art reference.

### Pudgy Penguins
**Style:** Rounded, friendly, soft-shaded illustrations. Penguins all use ONE body but vary clothing/accessories heavily. Limited palette per piece, lots of soft highlights, charming proportions (big eye, small body). Not pixel.

**Lesson:** The CHARM comes from oversized expressive features (big eyes, big smile). Our characters' eyes are too small and our mouths are bars. Take the "big eye, soft smile" energy and translate it into pixel logic.

### Doodles
**Style:** Illustrated, smooth vector look. Big heads, pastel palette. Body language varies (poses, hand positions). Not pixel.

**Lesson:** Doodles' edge is **body language**. Different head tilts, different hands. We could add 1-2 pose variants (head turned slightly, head tilted, hand raised to chin) to break the "everyone faces forward identically" problem.

### Goblintown
**Style:** Hand-illustrated, ugly-on-purpose, lo-fi cartoon. Vibe-driven, not technically refined. Not pixel.

**Lesson:** Personality beats polish. If our characters had MORE expression (a smirk, a wink, a tongue-out, a side-eye), they'd feel like Goblintown characters even if executed less precisely.

### Recommendation: emulate **CryptoPunks**

CryptoPunks is the only true pixel reference. We should:
1. **Match the 24x24 chunky energy.** At 32x32 we should NOT try to do 32x32 detailed work. We should do 24x24 art on a 32x32 canvas, giving everything more visual breathing room. The face should be wider (12 wide goes to 14), eyes bigger (1px iris goes to 2px iris with 2px white per side), mouth narrower (6-8px goes to 4-6px).
2. **Use accessory differentiation as the primary ID mechanism.** Already started, but go further. Each character should have 2-3 distinct attributes that uniquely ID them (not just 1).
3. **Drop the "every character is unique" pretense and embrace the modular pattern.** Celebrate the shared base head and make the attributes the personality.

---

## 4. Specific characters that look bad

### Ava (`ava.png`)
**What's wrong:**
- Long face shape plus long_straight hair makes her face look stretched 18 rows tall with eyes pushed too high. The 4-row chin below the mouth reads as a frown.
- The "big_grin" mouth is a hard black rectangle across her face. She looks like she's wearing electrical tape, not smiling. The photo shows a wide warm smile. The pixel shows a mail slot.
- Beach blonde hair is barely distinguishable from her skin tone (light_warm). The face blends into the hair on the sides.
- The hazel "irises" are 1px tan dots, invisible from any distance.

### Catherine (`catherine.png`)
**What's wrong:**
- "Wide" eye shape paints 12 white pixels per eye but irises at the LEFT pixels of each white block, so both eyes look glued to the upper-left. She looks dazed.
- Headset signature is barely visible at this resolution (a few black pixels next to her face), fails the "signature item identifies the character" test.
- Red lips on the wide flat mouth becomes a "red rectangle" pasted on her chin. In her photo she has soft warm lipstick. In pixel art it looks like a Halloween costume wound.
- Long face shape is wrong for her. Her real face is heart/oval shaped. Should be `oval`, not `long`.

### Garrett (`garrett.png`)
**What's wrong:**
- The "aviators" accessory specified in code is NOT VISIBLE in the output. It's completely overwritten or never paints. Garrett looks like he's wearing nothing on his eyes but the data says aviators. **This is a layer order bug or pixel-collision bug.** Check `build()` order: hair, eyebrows, eyes, nose, mouth, beard, signature, accessory. The aviator paints over rows 15-17, but I see his eyebrows on row 14 then "wide" eyes painted on top with no visible aviator frame.
- Crown floats above his head in gold but the empty space between hair (row 5) and crown (row 3-4) creates a "halo effect", the crown looks unattached.
- The smirk mouth painted at `(18, 22), (17, 22)` ABOVE the regular smirk line creates a weird upward-twisted look that reads as a scowl, not a smirk.
- His photo: clean, warm, big smile, fresh-faced. Pixel: brooding, scowling, crowned king. Wrong vibe entirely.

### Joe (`joe.png`)
**What's wrong:**
- Sunglasses are specified but I see eyes, not sunglasses. Same accessory-layer bug as Garrett, but partially: I see dark pixels on row 15 but the actual lenses are missing. Looks like Joe has a unibrow, not shades.
- "Stubble" beard is a scattered dot pattern that, combined with the LIP_SHADOW on mouth row 23, makes him look diseased rather than 5 o'clock shadowed.
- Chain signature paints `(13,27),(14,28),(15,28),(16,28),(17,28),(18,27)` in GOLD but only a tiny blue dot shows in his shirt area, the chain is mostly hidden under shirt color.

### Saralyn (`saralyn.png`)
**What's wrong:**
- Wide eyes again pushed to upper-left, giving "shocked dazed" expression.
- Long face shape with long_straight hair, another stretched Modigliani.
- Red lips painted as a thick horizontal rectangle on row 23-24 look like a wound, not a smile. The lips need an UPTURN at the corners to read as a smile.
- Trait color (pink) in the corner brackets fights with the red lips, two reds competing.

### Nick (`nick.png`)
**What's wrong:**
- Vintage cap specified (`cap_color: (90, 50, 40)` brown) but I see a brown brick on the right side that doesn't read as a cap. The cap function paints rows 6-10, but the rows 6-8 form a "crown" shape that just looks like a chunk of his hair is missing.
- Crown signature ALSO appears above (this is wrong, Nick was supposed to have `cap` as signature, but a yellow crown floats above). **This is a data/render mismatch**, the auto_traits.py probably overrode the original PEOPLE definition.
- Scruff beard plus grin mouth produces a "messy mouth dot pattern" that reads as crumbs on his chin.

### Sacha (`sacha.png`)
**What's wrong:**
- Snapback cap paints over rows 6-10. It works visually but the cap brim (rows 9-10) covers the eyebrows and forehead, then eyes paint on top. So eyebrows are HIDDEN, and the cap visually merges into the eye row. Looks like Sacha has a heavy unibrow and a small hat balanced on top.
- Stubble beard pattern (scattered dots) at row 22-25 has dots inside the mouth area, they overlap and create a messy chin look.

### Owen (`owen.png`)
**What's wrong:**
- Beanie specified but NOT rendered (the beanie_color is unset, so it falls to default and doesn't paint). Owen is supposed to be the surfer with the beanie plus surfboard plus curly blonde combo. We get only the curly hair and the surfboard.
- Curly_short hair at this resolution looks like a "bumpy bowl cut", not a curly look.
- Surfboard at col 26-27 is rendered as a flat white-grey stripe with one red pixel, reads more as a thermometer or candy bar than a surfboard.

### Austin (`austin.png`)
**What's wrong:**
- Crown signature on top plus curly_short hair: the crown sits IN the curly bumps, looking like someone glued cardboard to his hair.
- His pixel skin tone is `tan` (200, 150, 110), which is fine, but combined with thick "straight" brows (HAIR_SHADOW for brown = 75,50,30), the brows look painted on, like clown makeup.
- The "big_grin" black bar mouth is especially bad here because his skin is darker, the black mouth has very little contrast with the dark beard area and reads as a literal hole in his face.

---

## 5. Implementation recommendations

In priority order, these code changes should ship to upgrade quality:

### 1. Fix the eyes (`character_builder.py`, `draw_eyes`)
Replace the entire function. Change pupil to NOT overwrite the iris, place the white highlight INSIDE the iris pixel (top-left of iris), and remove the floating row-15 highlight bug. Make eyes 2 rows tall by default. Add eyelid shadow. Pass `skin_key` so the eyelid shadow color is correct. See Problem 1 fix above for exact code.

### 2. Fix the mouths (`character_builder.py`, `draw_mouth`)
All smile variants should have CORNER PIXELS that turn up (placed 1 row higher than the mouth body). Remove the 8-pixel-wide `big_grin`, cap at 6 pixels. Replace solid BLACK lip-line with `mix(BLACK, LIP_SHADOW, 0.5)` for less harshness. Move LIP color above the teeth line for `grin`, not below. See Problem 2 fix for code.

### 3. Add 3-tone face shading (`character_builder.py`, `draw_head`)
After the base skin fill, add: forehead highlight row 11-12, left jaw shadow col 11 rows 19-21 (mirror right side), under-eye shadow row 18 col 12 and 19, chin shadow row 25, cheek warmth pixels at col 12, 19 row 20, nose-side highlight col 14 rows 19-20. This single change will lift the perceived quality two grades. See Problem 4 fix.

### 4. Fix face proportions for `long` face (`character_builder.py`, `draw_head` + `build()`)
Either pass `y_offset=1` to all feature draws when `face_shape=="long"`, OR shorten the long face to 16 rows tall. Currently the chin sag on Ava/Catherine/Saralyn/Renee is the worst single issue in the collection. See Problem 3 fix.

### 5. Make hair shapes distinct (`character_builder.py`, hair_* functions)
- `messy`: add 2 jagged spikes at row 4 above current row 5 spikes: `paint(canvas, [(13, 4), (17, 4)], h)`
- `slick_back`: shift entire hair UP one row (rows 5-8 instead of 6-9), add slick highlight streaks `(11, 6), (13, 6), (15, 6), (17, 6), (19, 6)` in HAIR_LIGHT
- `short_parted`: add visible part GAP, paint `(16, 7), (16, 8)` in SKIN_LIGHT (use the head's skin tone)
- `fade`: side pixels (col 10, 21, rows 9-12) should be SKIN color stippled with hair shadow, not hair color, to create the buzz-fade effect
- `curly_short`: add a row of 4 bumps at row 4: `(11,4),(14,4),(17,4),(20,4)` to push curls above the head dome

### 6. Fix accessory layer collisions (`character_builder.py`, `build()`)
Aviators, sunglasses, glasses_clear all paint over the eye row but several characters render with both eyes AND glasses smashed together (Garrett, Joe). When an `accessory` is set on the eye row, the eye draw should be SKIPPED entirely (not painted then covered) so we get clean glass on a clean face:
```python
EYE_COVERING_ACCS = {"sunglasses", "aviators", "ar_glasses"}
# glasses_clear has transparent lenses, draw eyes BEHIND
if person.get("accessory") not in EYE_COVERING_ACCS:
    draw_eyes(canvas, person["eyes"], person.get("eye_shape", "normal"))
```
For `glasses_clear`, the lens (rows 16-17 inside the frame) should be SKIN_LIGHT or WHITE with the eye drawn INSIDE the frame, currently it paints solid black for the bottom row, blocking the eye.

### 7. Shrink eyebrows (`character_builder.py`, `draw_eyebrows`)
The `straight` style is 3 pixels wide and 1 row tall, which is fine. The `thick` style is 5 pixels wide and looks like Sesame Street's Bert. Cap `thick` at 4 pixels. The HAIR_SHADOW color for black hair is `(25, 20, 15)`, too close to pure black. Replace with `mix(HAIR_SHADOW[k], skin_color, 0.2)` so brows have skin tone bleeding in (a classic pixel-art softening trick).

### 8. Add shoulder shading (`character_builder.py`, `draw_shirt`)
The shirt currently fills rows 28-31, but the shoulders look like a flat brick. Add slope and shading:
```python
# After fill_rect:
# Shoulder slope: corners drop one row
paint(canvas, [(5, 28), (6, 28), (25, 28), (26, 28)], mix(color_main, BLACK, 0.4))
# Vertical highlight column down the left chest
paint(canvas, [(9, 29), (9, 30), (9, 31)], mix(color_main, WHITE, 0.15))
# Right shadow column
paint(canvas, [(22, 29), (22, 30), (22, 31)], mix(color_main, BLACK, 0.3))
```

### 9. Widen skin-tone spread (`character_builder.py`, SKIN palette)
Current 5 skin tones are too close in value. Widen the range:
- `light`: keep
- `light_warm`: shift toward `(248, 210, 175)` (more saturated warm)
- `medium`: shift toward `(208, 158, 120)` (warmer)
- `tan`: shift to `(180, 130, 95)` (darker)
- `warm`: shift to `(225, 175, 130)`

Also ADD a `deep` skin tone: `(150, 100, 65)` with shadow `(110, 70, 45)` and light `(170, 120, 85)`. The collection currently has zero darker-skin characters represented in any meaningful range.

### 10. Eye-shape diversity in `auto_traits.py`
The auto-trait generator defaults nearly everyone to `eye_shape="normal"`. After fixing the eye function (rec 1), randomize across `normal`, `wide`, `narrow` at 60/25/15% weights so the collection has actual variety. The narrow variant especially helps distinguish older / "operator" characters from young / "wide-eyed" ones.

### Bonus 11. Background style variants
All 79 BGs use the same dot-grid plus corner-bracket pattern with only the trait color varying. Add 3-4 background style variants (solid, gradient, diagonal stripe, halftone, dot-grid) randomly assigned. Currently if you scroll through the collection, every BG reads as "the same dotted wallpaper" and the characters lose pop.

### Bonus 12. Convert the stray eye highlight bug to a feature
After fixing `draw_eyes`, optionally KEEP a single white pixel at `(13, 15)` for left eye and `(18, 15)` for right eye (moved one column INWARD from current placement) to add a sparkle WITHOUT making it look like a forehead pimple. This becomes a deliberate "stare highlight" rather than a bug.

---

## Closing note

The technical foundation is solid. Sprite functions are modular, theme overlays compose cleanly, the build pipeline works. The problems are all at the **art direction** layer: eye math is wrong, mouths are too geometric, faces are too flat, hair shapes don't differentiate, and the long-face female proportions are unflattering.

Fix items 1, 2, 3, and 4 first (eyes, mouths, skin shading, long-face proportions). Those four changes alone will take the collection from "competent procedural pixel art" to "looks like an intentional Bored-Apes-tier collection." The other six items are polish.

Estimated implementation time: 4-6 hours for items 1-4, another 4-6 hours for items 5-10. Worth it.
