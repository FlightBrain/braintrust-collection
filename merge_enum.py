#!/usr/bin/env python3
"""Merge enum_a-e.json into members.json, skip duplicates."""
import json
import pathlib

DATA = pathlib.Path("data")
EXISTING = json.loads((DATA / "members.json").read_text())
seen = {m["slug"] for m in EXISTING}
print(f"Existing members: {len(EXISTING)}")

added = 0
for letter in "abcde":
    enum_path = DATA / f"enum_{letter}.json"
    if not enum_path.exists():
        print(f"WARN: {enum_path} missing")
        continue
    raw = json.loads(enum_path.read_text())
    # Some agents wrapped the list, some didn't
    if isinstance(raw, dict):
        batch = raw.get("people") or raw.get("results") or raw.get("users") or []
    else:
        batch = raw
    for entry in batch:
        if not isinstance(entry, dict):
            continue
        slug = entry.get("slug")
        if not slug:
            continue
        if slug in seen:
            print(f"  skip (dup): {slug}")
            continue
        photo = (entry.get("photo") or entry.get("photo_url")
                 or entry.get("profile_pic") or "")
        if not photo or "secure.gravatar.com" in photo:
            print(f"  skip (no photo): {slug}")
            continue
        name = entry.get("name") or entry.get("real_name") or slug
        EXISTING.append({
            "slug": slug,
            "name": name,
            "role": entry.get("role") or entry.get("title") or "",
            "photo": photo,
        })
        seen.add(slug)
        added += 1

(DATA / "members.json").write_text(json.dumps(EXISTING, indent=2))
print(f"\nAdded {added} new members. Total: {len(EXISTING)}")
