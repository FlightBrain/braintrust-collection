# Braintrust Collection · QA Audit

Audit date: 2026-05-11. Live site: https://braintrust-collection.vercel.app

---

## 1. Missing photos / broken images

**Status:** 1 of 77 members has no photo file.

| Slug | Issue |
|------|-------|
| `duncan` (Duncan Lewis, SDR) | `photo` field in `members.json` is an empty string. No `public/photos/duncan.*` exists. Pixel art `pixels/corporate/duncan.png` exists but was generated without a source photo. `https://braintrust-collection.vercel.app/photos/duncan.jpg` returns HTTP 404. |

**No gravatar URLs detected** in `members.json` (0 entries contain `secure.gravatar.com`).

**Orphan files in `public/photos/` and `public/pixels/corporate/` (not in members.json):**

| File | Slug | Issue |
|------|------|-------|
| `photos/austin.png`, `pixels/corporate/austin.png` | `austin` | Member list has `austin-c` (Austin Collins) and `austin-moehle` (Austin Moehle) only. The bare `austin` slug is dead weight. |
| `photos/matt.jpg`, `pixels/corporate/matt.png` | `matt` | Member list has `matt-perpick`. The bare `matt` slug has no corresponding entry. |

Both `austin` and `matt` also produce NFT SVGs in all 3 themes (`nfts/{theme}/austin_nft.svg`, `matt_nft.svg`) but neither renders in the grid because the grid is driven by `auto_people.json` (77 entries) which does not contain them.

**Action:** Either delete the 4 stray files (`photos/austin.*`, `photos/matt.*`, `pixels/corporate/austin.png`, `pixels/corporate/matt.png`, plus 6 NFT SVGs across 3 themes) or add `austin` and `matt` as proper member entries. Add a real photo for Duncan Lewis or remove him from the roster.

---

## 2. Duplicate items audit

**Headline:** Full 12-trait combinations are unique across all 77 members (0 exact dupes). But individual trait values are heavily reused.

**Top 10 worst single-trait duplicates** (most concerning for "no two should look the same"):

| Rank | Field | Value | Count | Slugs (truncated) |
|------|-------|-------|-------|-------------------|
| 1 | accessory | `null` (no accessory at all) | 42 | manu, eden, matt-perpick, ornella, morgane, clarissa, shelly, carleton, lexi, tony... |
| 2 | beard | `none` | 37 | manu, eden, ornella, morgane, clarissa, sarah-zeng, saralyn... |
| 3 | brain_color | `pink` | 38 | eden, matt-perpick, clarissa, sarah-zeng, saralyn, renee, max... |
| 4 | brow_style | `straight` | 28 | eden, matt-perpick, bryan, clarissa, sarah-zeng, max, mo... |
| 5 | face_shape | `oval` | 27 | ankur, eden, ornella, clarissa, shelly, renee, carleton... |
| 6 | eyes | `brown` | 27 | ankur, manu, eden, ornella, clarissa, sarah-zeng, saralyn... |
| 7 | brow_style | `thick` | 26 | ankur, ornella, carleton, tara, austin-moehle, olmo, mike-deeks... |
| 8 | hair_color | `dbrown` | 24 | manu, eden, saralyn, renee, carleton, tara, austin-moehle, olmo... |
| 9 | mouth | `smile` | 23 | ankur, matt-perpick, clarissa, carleton, john-huang, dan, mike-deeks... |
| 10 | brow_style | `arched` | 23 | manu, morgane, saralyn, shelly, renee, lexi, tony, stephen... |

**Signature dupes** (the main visible "trait" on each card):
- `earring` (10): clarissa, sarah-zeng, shelly, lexi, tara, evan-keith, casey, katherine-m, ava, catherine
- `bt_pin` (8): manu, saralyn, tony, david-elner, jack-bullard, mohan, jaiden, ryan
- `crown` (7): ankur, doug, alex-jb, walton, dave-smith, garrett, nick
- `ai_agent` (7): eden, john-huang, olmo, andrew, ameya, mengying, kensington
- `watch` (7): matt-perpick, kevin-green, remi, pb, jay, chris, keslar
- `necklace_gold` (7): ornella, renee, drew, stelliana, liv, evan, shaune
- `cap` (5), `pint_glass` (5), `surfboard` (5), `question_mark` (5)
- `chain` (4), `headset` (4)
- `pocket_square` (3)

**Accessory dupes:**
- `glasses_clear` (9): ankur, bryan, mo, john-huang, phil-h, pedro, nathan, sam-foxhall, martin
- `earring_stud` (7), `red_lips` (5), `sunglasses` (4), `earbuds` (4), `beanie` (2), `aviators` (2)

**Hair style dupes:**
- `short_parted` (16), `messy` (11), `fade` (10), `long_straight` (9), `curly_short` (7), `slick_back` (7), `long_wavy` (6), `undercut` (5), `curly_long` (3), `beach_blonde` (3)

The combo of "no accessory" (42 people) + same hair_style + same eye color leaves many faces looking like near-clones. See section 5 for proposed new items.

---

## 3. Faces that don't match the photo (spot-check)

Photos read and compared 1:1 against `pixels/corporate/{slug}.png` for 15 samples.

| # | Slug | Accuracy (1-5) | What is off |
|---|------|----------------|-------------|
| 1 | ankur | 2 | Photo: medium skin, clear thin-rim glasses, slight beard shadow. Pixel: a thick black bandit-style mask in place of glasses, way too dark. Glasses sprite reads as a domino mask. |
| 2 | manu | 1 | Source photo is a CHILDHOOD photo of a toddler in a "Tennis Anyone?" shirt. Pixel art shows an adult male with stubble and a button. The pixel is completely fictional vs the source. |
| 3 | eden | 3 | Photo: clean-shaven, friendly grin, no facial hair. Pixel: harsh angry brow, frowning mouth, looks 20 years older. Hair color OK. |
| 4 | bryan | 3 | Photo: green jacket, white tee under, salt-and-pepper hair, light beard, no hat, no glasses. Pixel: backwards cap (wrong), thick black bandit-mask glasses (wrong, not in photo), full beard. Bryan does not wear a cap. Glasses sprite is too aggressive. |
| 5 | ornella | 2 | Photo: long black hair, light skin, gold necklace yes. Pixel: face is too gaunt/sallow with grey shading, eyebrows extremely heavy unibrow, mouth missing/flat. Looks unhappy. |
| 6 | kensington | 2 | Photo: short blonde-brown undercut, clean-shaven, brown zip-up over navy shirt. Pixel: hair is shorter and darker brown, the "ai_agent" signature does not appear visible, mouth is just a thick black bar (no smile), looks angry. |
| 7 | ryan | 3 | Photo: blonde hair, clean-shaven, black sweater with `#` brain pin. Pixel: laser eyes signature is dominant which obscures resemblance, mouth bar very harsh. Laser eyes are correct as a 1-of-1 trait but they overwhelm the face. |
| 8 | ava | 3 | Photo: long beachy blonde hair, warm tan, smiling. Pixel: hair is straight and platinum (too cool a blonde), expression frowning/severe, eyebrows too thick. The hair sprite is in the right ballpark but coloration is wrong (should be honey/golden, not yellow). |
| 9 | catherine | 2 | Photo: long dark brown hair, warm light skin, soft smile, lip gloss. Pixel: hair too short and droopy, harsh red lipstick painted on, eyebrows too thick and dark, looks angry. The lipstick is way too saturated red vs the natural nude tone. |
| 10 | sacha | 2 | Photo: black baseball cap, dark brown beard, dark hair. Pixel: cap is right, but skin tone reads warm/orange and the beard is dotted-stubble not a full beard. Eyebrow unibrow too thick. |
| 11 | jay | 3 | Photo: short auburn-brown hair, light beard, blue button-up. Pixel: hair color OK, blue shirt OK, full beard reasonable, but eyebrows too heavy. Decent likeness. |
| 12 | walton | 2 | Photo is a family photo with wife and 2 kids; Walton has a beard, ball cap, plaid shirt. Pixel: gold crown sig OK, beard OK, but no cap (photo shows cap clearly) and color of hair is brown/dbrown vs his actual hair which is darker. Decent stab. |
| 13 | luca | 3 | Photo: backwards black ball cap, clean-shaven young face, black tee. Pixel: cap is right, but pixel shows scruff/stubble beard he doesn't have in photo. Otherwise OK. |
| 14 | morgane | 2 | Photo: warm blonde with brunette streaks, smiling wide. Pixel: dirty mustard-yellow hair (not pleasant blonde), missing the gold necklace signature she'd be a fit for, frowning mouth. Looks unhappy and dated. |
| 15 | tara | 2 | Photo: dark brown long hair, light brown skin, big white smile, gold studs. Pixel: gold earring yes, but mouth is a tiny scowl, eyebrows unibrow-thick, hair sprite is "long_straight" with a side-part that doesn't match her bangs. |

**Cross-cutting issues from the spot-check:**

1. **Eyebrow sprite is too aggressive on everyone.** The "thick" and "straight" variants render as nearly unibrows. Soften by 1-2 pixels.
2. **Mouth sprite frowns by default.** Even people whose `mouth` is `smile` or `big_grin` end up with a flat black bar mouth. The smile sprite is not communicating happiness.
3. **Glasses_clear sprite reads as a black bandit-mask**, not glasses. Should be 2 pixel-thin rims with a bridge, not a solid filled rectangle.
4. **Skin tones cluster too cool / sallow.** `light_warm` and `light` pixels both render with a grey undertone that makes everyone look ill. Push the hue toward warm cream / peach.
5. **Source photos for `manu`, `walton`, `ornella` are not headshots.** Manu uses a toddler photo, Walton uses a family photo, Ornella uses a photo where she's mostly turned to her dog. These should be re-collected.
6. **Some people are missing visible signatures** in their pixel (e.g. Kensington's `ai_agent` sig is on the canvas but barely visible).

---

## 4. Site bugs

Live site checks against https://braintrust-collection.vercel.app (verified via WebFetch and source review of `public/index.html`).

| Area | Status | Notes |
|------|--------|-------|
| Grid render | OK | 77 entries returned from `/auto_people.json`. Grid loop iterates all of them. |
| Search "ankur" | OK (likely) | Search input matches against `name`, `trait_name`, and `tags`. "ankur" matches name. |
| Search "joe" | OK | Matches name. |
| Search "ai_agent" | **Bug** | Input string is lowercased (`q = e.target.value.toLowerCase().trim()`) but tags are stored uppercase (`AI_AGENT`). The check `(p.tags \|\| []).join(' ').toLowerCase().includes(q)` lowercases tags before comparing, so `ai_agent` will match. **Actually OK after re-read.** |
| Filter bar | **Bug** | Filter list is hardcoded as `['ALL', 'AE', 'SUNGLASSES', 'LASER_EYES', 'AI_AGENT', 'BEACH', 'SNORKEL', 'CHAIN', 'CROWN', 'MYSTERY']`. `BEACH` and `MYSTERY` match 0 people. `SNORKEL` matches 22 people but the visual snorkel only appears in the aquatic theme which has been removed. Clicking BEACH or MYSTERY empties the grid silently. |
| Filter `SNORKEL` | **Bug** | `deriveTags` pushes `SNORKEL` whenever `p.snorkel === true` (22 people), but the corporate / galaxy / cyberpunk pixel art does not render the snorkel asset, so the filter selects people who do not visually have a snorkel. |
| Leaderboard | **Bug (cosmetic)** | Modal subtitle hardcodes "ALL 15 OPERATORS RANKED" but there are 77 people in `rarity.json`. Compare modal also subtitle says "77 OPERATORS × 3 VOLUMES" which is correct. Modal does iterate all 77 in `sorted`. |
| Pack opening modal | OK | Wire-up confirmed for `pack-open-btn`, `pack-btn-floating`, `pack-again-btn`. `openPack()` at line 1781 exists. |
| Stats dashboard | OK | `renderStats` populates `#rarity-bars`, `#trait-bars`, `#mint-counter` (animates 0 to 231). |
| Mint counter target | OK | Counter animates to 231 (= 77 × 3 editions). Matches footer text. |
| Theme switcher | OK | 3 themes: corporate, galaxy, cyberpunk. The fourth (aquatic) was removed from the UI but lingering data exists: `auto_people.json` still has `aquatic_variant` field on every person, and there are 35 stray SVGs in `public/nfts/aquatic/`. |
| Aquatic art incomplete | **Bug** | `public/nfts/aquatic/` has 35 SVGs (vs 79 for the other 3 themes). If the aquatic theme is gone, delete the folder. If it's coming back, generate the missing 44. |
| Rank format on card back | **Bug** | Line 808: `RANK ${r.rank}/15`. Should be `/77`. |
| Rank format in modal | **Bug** | Line 1044: `#${r.rank}/15`. Should be `/77`. |
| Token format | OK | `${p.id}/077` is correct. |
| Volume header | **Bug (cosmetic)** | `vol-mythics` shows hardcoded `01`. Per `rarity.json`, count of MYTHIC tier members may differ. Worth recounting and binding to data. |
| Mint reveal overlay | **Bug** | Lines 702-705 hardcode "15 Operators unrevealed" and "60 unique mints" but the collection is now 77 operators × 3 editions = 231 mints. |
| Hero sub on default theme | **Bug** | Line 558: "15 portraits, 3 editions, 45 mints" hardcoded. Each theme button's `data-sub` also says "15 portraits, 3 editions, 45 mints" (corporate) and "60 unique mints" (mint reveal). All should say 77 and 231. |
| Footer | OK | "3 VOLUMES · 231 MINTS" is correct. |
| Filter `LASER_EYES` | OK | 1 match (Ryan). Confetti hook works on flip. |
| `BEACH` filter | **Bug** | 0 matches. Either remove the pill or add `beach` signatures to people. |
| `MYSTERY` filter | **Bug** | 0 matches. Remove or add a `mystery` signature. |
| `compare-grid` template | **Bug** | Uses 3-column grid for corporate/galaxy/cyberpunk (lines 1013, 1018-1019). No 4th column needed since aquatic is gone. Looks correct given current 3-theme state. |
| Theme keyboard nav | OK | Arrow keys cycle theme buttons. |
| Direct link routing `?nft=ankur&theme=corporate` | OK | Whitelist updated to `['corporate','galaxy','cyberpunk']`. |
| Image 404s | Found | `photos/duncan.jpg` returns 404. Used only as a source; not referenced by the grid. The grid renders SVGs, not raw photos, so users do not see this directly. |
| Music button, sound button, achievements toast, ticker | OK | All wired. Ticker uses fake trades for vibes. |
| Mint stats overlay | **Bug** | Line 705 hardcodes "77 OPERATORS · 3 EDITIONS · 231 MINTS · 1 MYTHIC". Count check needed: how many MYTHICs? Verify against `rarity.json`. |

---

## 5. Items that should be unique but aren't (proposed new sprites)

The "42 people have null accessory" + "7 people share crown" pattern means the floor is full of near-twins. Below are proposed new sprites to differentiate.

### New signature ideas (15 proposed)

| Sprite | Description | Fits whom (suggested) |
|--------|-------------|-----------------------|
| `mechanical_keyboard` | Tiny keyboard floating bottom-right | engineers (john-huang, hurshal, david-elner) |
| `fountain_pen` | Black/gold pen across chest | counsel/exec (tony, michael-basil) |
| `airpods_max` | Over-ear headphones (different sprite from `headset`) | dan, ameya, mengying |
| `vape_pen` | Discreet pen vape | sacha, joe, shaune |
| `kombucha` | Glass bottle | morgane, liv, ornella |
| `pocket_protector` | Pen array on chest | retro nerd vibe for hossein, doug |
| `lab_coat` | White coat shoulders | sam-foxhall, mengying |
| `cigar` | Lit cigar | dave-smith, bryan |
| `coffee_mug` | Steaming mug | catherine, alec, owen |
| `microphone` | Stand mic (podcast vibe) | walton, jay (storytellers) |
| `chess_piece` | Knight or king floating | luca (photo shows chess), kensington |
| `dog` | Small dog peeking | tara, ornella, eden (dog parents) |
| `surfboard_short` | Short board variant (different from current) | one of the 5 surfboards |
| `bike_helmet` | Cycling helmet | austin-c |
| `dumbbell` | Single weight | mike-deeks, max |

### New accessory ideas (15 proposed)

| Sprite | Description |
|--------|-------------|
| `glasses_round` | Round wireframe (clearly different from `glasses_clear`) |
| `glasses_thick_black` | Heavy buddy-holly style |
| `monocle` | Single lens (joke tier) |
| `sweatband` | Athletic headband |
| `bandana` | Tied around forehead |
| `nose_ring` | Septum or nostril |
| `eyebrow_piercing` | Single barbell |
| `lip_piercing` | Small stud below lip |
| `freckles` | Pixel freckle dots |
| `mole` | Marilyn-style beauty mark |
| `tattoo_neck` | Small ink on neck |
| `scar_eye` | Vertical scar through eyebrow |
| `eyepatch` | Pirate variant |
| `face_paint` | Sports team stripe |
| `band_aid` | Small bandage on cheek |

### Watch / wristband variants (current `watch` is shared by 7 people)

| Sprite |
|--------|
| `watch_apple_black`, `watch_apple_silver`, `watch_apple_gold` |
| `watch_classic_brown_leather`, `watch_classic_silver_metal` |
| `wristband_rubber_color` (single color band, swappable) |
| `friendship_bracelet` |

### Hair color variants (current 7 colors is too few for 77 people)

Add: `auburn_dark`, `red_natural`, `silver_grey`, `salt_pepper`, `platinum`, `dyed_pink`, `dyed_blue`.

---

## 6. Specific people (verdict per person)

| # | Slug | Verdict | What's wrong | Fix |
|---|------|---------|--------------|-----|
| 1 | **ankur** | Off | Bandit-mask glasses, eyebrows too thick, mouth flat. Skin tone is OK. | Switch `accessory` to a thinner round-rim sprite. Lift mouth into a real smile (his photo is clearly smiling). |
| 2 | **manu** | Wrong source | Source photo is a baby photo. Pixel art is generic adult. The mismatch is total. | Re-pull Manu's adult Slack avatar. Re-render pixel. |
| 3 | **eden** | Off | Pixel looks angry; photo shows wide friendly smile, clean-shaven, brown wavy hair. | Use `mouth: big_grin`, soften brow, lighten hair to `brown` not `dbrown`. Remove ai_agent overlay or shrink it. |
| 4 | **bryan** | Off | Pixel has backwards cap and bandit-mask glasses neither of which appear in photo. Photo: short side-part salt-pepper, no glasses, no hat, light beard. | Remove cap. Remove glasses. Keep beard. Use `hair_color: salt_pepper` (proposed new color). |
| 5 | **ornella** | Off | Pixel face is grey/gaunt, unibrow, no mouth visible. Photo has warm tan skin, long black hair, soft expression. | Switch skin to `tan` not `medium`. Soften brow. Render a small mouth (smile or smirk). |
| 6 | **kensington** | Off | Hair too dark, expression too severe, ai_agent sig nearly invisible. | Hair_color to `lblonde` not `lbrown`. Switch mouth to `big_grin`. Make ai_agent more prominent. |
| 7 | **ryan** | Acceptable | Laser eyes are a strong signature and worth keeping. Hair should be `blonde` not `lbrown` (his hair reads blonde in photo). | Change hair_color to `blonde`. |
| 8 | **ava** | Off | Hair color is platinum yellow; should be warm honey blonde. Expression too severe. | Add a new `hair_color: honey` or shift `blonde` warmer. Change mouth to `big_grin`. |
| 9 | **catherine** | Off | Red lipstick way too painted-on; her photo shows natural lip color. Eyebrows too thick. | Replace `red_lips` accessory with something subtler (or remove). Soften brow. Use `mouth: smirk`. |
| 10 | **sacha** | Mostly OK | Cap is good. Stubble dots are good. But skin reads too orange, and unibrow is too heavy. | Switch skin from `warm` to a balanced tan. Trim brow. |

---

## Cross-cutting recommendations (priority order)

1. **Fix the rank string `/15` to `/77`** in two locations (lines 808 and 1044 of `index.html`). Most visible bug.
2. **Update mint reveal overlay copy** (lines 700-705) to say 77 operators, 3 editions, 231 mints. Currently says 15.
3. **Update hero `data-sub` for corporate theme** to say "77 portraits, 3 editions, 231 mints" (line 565). Repeat for galaxy/cyberpunk sub copy as needed.
4. **Remove or fix `BEACH` and `MYSTERY` filter pills** (line 848). They match 0 people.
5. **Remove `SNORKEL` filter** since aquatic theme is gone and snorkel does not render on the active themes.
6. **Soften the global eyebrow sprite** (thick and straight variants both render as near-unibrows).
7. **Redesign the `glasses_clear` sprite** to read as glasses, not a bandit mask.
8. **Make the `smile` and `big_grin` mouth sprites actually look happy.** Right now all 5 mouth variants read as flat or frowning.
9. **Get a real photo for Duncan Lewis** OR remove him from the collection.
10. **Re-collect headshots for Manu (baby photo), Walton (family photo), Ornella (dog photo).** Their pixel art has nothing to anchor to.
11. **Delete orphan `austin` and `matt` files** OR add them as legit members (currently 4 photos + 4 pixels + 6 NFTs are stranded).
12. **Delete `public/nfts/aquatic/` and the `aquatic_variant` field** from `auto_people.json` if the theme is permanently retired. Currently 35 partial SVGs sitting there.
13. **Add 10+ new signature sprites** (see section 5) to break up the 42-person "no signature" plus 10-person "earring" cluster.
14. **Add hair color variants** (silver, salt_pepper, platinum, auburn_dark) so 24 people don't share `dbrown`.
15. **Bind `vol-mythics` count to actual data** (line 611, currently hardcoded `01`).

---

## File references

- `data/members.json` (77 entries)
- `data/auto_people.json` (77 entries)
- `public/rarity.json` (77 entries)
- `public/photos/` (78 files, 1 stray `austin.png`, 1 stray `matt.jpg`)
- `public/pixels/corporate/` (79 files, includes strays `austin.png` + `matt.png`)
- `public/nfts/corporate/` (79 SVGs, 2 strays)
- `public/nfts/galaxy/` (79 SVGs, 2 strays)
- `public/nfts/cyberpunk/` (79 SVGs, 2 strays)
- `public/nfts/aquatic/` (35 SVGs, theme retired but folder lingering)
- `public/index.html` (1847 lines, primary site source)
