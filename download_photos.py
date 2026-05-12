#!/usr/bin/env python3
"""Download all member photos to public/photos/<slug>.<ext>"""
import json
import pathlib
import urllib.request
import urllib.parse

members = json.loads(pathlib.Path("data/members.json").read_text())
out_dir = pathlib.Path("public/photos")
out_dir.mkdir(parents=True, exist_ok=True)

ok, skipped = 0, 0
for m in members:
    if not m.get("photo"):
        skipped += 1
        print(f"SKIP (no photo) {m['slug']}")
        continue
    url = m["photo"]
    ext = pathlib.Path(urllib.parse.urlparse(url).path).suffix or ".png"
    out = out_dir / f"{m['slug']}{ext}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            out.write_bytes(r.read())
        ok += 1
        print(f"OK {out}")
    except Exception as e:
        skipped += 1
        print(f"FAIL {m['slug']}: {e}")

print(f"\nDownloaded {ok}, skipped {skipped} of {len(members)}")
