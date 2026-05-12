#!/usr/bin/env python3
"""Rarity scoring v2: percentile-based tiers, weighted trait categories.

SIGNATURE traits: weight = 200 / count_in_collection
ACCESSORY traits: weight = 60 / count
APPEARANCE traits: weight = 12 / count
Combo bonus: +50 for any iconic pair.

Tier assignment by percentile (negative skew toward common):
- Top 1%: MYTHIC
- Next 4%: LEGENDARY
- Next 10%: RARE
- Next 25%: UNCOMMON
- Bottom 60%: COMMON
"""
import json
import pathlib
from collections import Counter

SIGNATURE_KEYS = ["signature"]
ACCESSORY_KEYS = ["accessory", "brow_style", "snorkel", "brain_color"]
APPEARANCE_KEYS = ["hair_color", "eyes", "skin", "beard", "mouth", "face_shape", "shirt", "hair_style"]
SIG_W = 200
ACC_W = 60
APP_W = 12

COMBO_BONUS = 50
ICONIC_COMBOS = [
    ("signature:ai_agent",   "accessory:ar_glasses"),
    ("signature:bt_pin",     "accessory:laser_eyes"),
    ("signature:crown",      "accessory:aviators"),
    ("signature:chain",      "accessory:sunglasses"),
    ("signature:surfboard",  "snorkel:True"),
    ("brain_color:gold",     "signature:ai_agent"),
]


def count_traits(people):
    counts = {}
    for p in people:
        for k in SIGNATURE_KEYS + ACCESSORY_KEYS + APPEARANCE_KEYS:
            v = p.get(k, "none")
            v = "none" if v in (None, "") else v
            counts[f"{k}:{v}"] = counts.get(f"{k}:{v}", 0) + 1
    return counts


def score_person(p, counts):
    score = 0.0
    breakdown = []
    for k in SIGNATURE_KEYS:
        v = p.get(k, "none") or "none"
        c = counts.get(f"{k}:{v}", 1)
        w = SIG_W / c
        score += w
        breakdown.append({"trait": k.upper(), "value": str(v).upper(), "count": c, "weight": round(w, 1)})
    for k in ACCESSORY_KEYS:
        v = p.get(k, "none") or "none"
        c = counts.get(f"{k}:{v}", 1)
        w = ACC_W / c
        score += w
        breakdown.append({"trait": k.upper(), "value": str(v).upper(), "count": c, "weight": round(w, 1)})
    for k in APPEARANCE_KEYS:
        v = p.get(k, "none") or "none"
        c = counts.get(f"{k}:{v}", 1)
        w = APP_W / c
        score += w
        breakdown.append({"trait": k.upper(), "value": str(v).upper(), "count": c, "weight": round(w, 1)})

    has = set()
    for k in SIGNATURE_KEYS + ACCESSORY_KEYS + APPEARANCE_KEYS:
        v = p.get(k, "none") or "none"
        has.add(f"{k}:{v}")
    combo_count = 0
    for a, b in ICONIC_COMBOS:
        if a in has and b in has:
            score += COMBO_BONUS
            combo_count += 1
    if combo_count:
        breakdown.append({"trait": "COMBOS", "value": f"{combo_count} ICONIC", "count": 1, "weight": combo_count * COMBO_BONUS})

    return score, breakdown


def assign_tier(rank, total):
    p = rank / total
    if p < 0.01:      return "MYTHIC", "#FF3366"
    elif p < 0.05:    return "LEGENDARY", "#FFD93D"
    elif p < 0.15:    return "RARE", "#9D7AFF"
    elif p < 0.40:    return "UNCOMMON", "#00D9FF"
    else:             return "COMMON", "#8B95A8"


def main():
    people = json.loads(pathlib.Path("data/auto_people.json").read_text())
    counts = count_traits(people)
    total = len(people)
    scored = []
    for p in people:
        s, b = score_person(p, counts)
        scored.append({"slug": p["slug"], "score": round(s, 2), "breakdown": b})
    scored.sort(key=lambda x: -x["score"])
    for rank, item in enumerate(scored):
        tier, color = assign_tier(rank, total)
        item["tier"] = tier
        item["tier_color"] = color
        item["rank"] = rank + 1
    by_slug = {item["slug"]: item for item in scored}
    pathlib.Path("public/rarity.json").write_text(json.dumps(by_slug, indent=2))
    print(f"Wrote public/rarity.json with {total} entries\n")
    tiers = Counter(item["tier"] for item in scored)
    print(f"Distribution: {dict(tiers)}")
    print()
    print(f"{'RANK':<6}{'SLUG':<18}{'TIER':<14}{'SCORE':<10}")
    for item in scored[:8]:
        print(f"#{item['rank']:<5}{item['slug']:<18}{item['tier']:<14}{item['score']:<10}")
    print("...")
    for item in scored[-5:]:
        print(f"#{item['rank']:<5}{item['slug']:<18}{item['tier']:<14}{item['score']:<10}")


if __name__ == "__main__":
    main()
