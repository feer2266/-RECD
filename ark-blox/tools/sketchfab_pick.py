"""Find realistic, downloadable Sketchfab models for every `todo` row in model_manifest.csv.

Usage: python3 ark-blox/tools/sketchfab_pick.py [--only PREFIX] [--top N]

Search needs no account. For each asset the "|"-separated SketchfabQuery terms are
tried in order until one gives usable candidates. A candidate must be downloadable,
CC0 or CC-BY (safe for a Roblox game with credit), and not tagged low poly /
stylized / voxel / AI-generated / ripped from ARK. Candidates are scored on realism
tags, triangle budget and popularity; the best N go to model_candidates.csv.

Pick one per asset by setting Chosen=1 in that file, then run sketchfab_download.py.
"""
import argparse
import csv
import json
import math
import os
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "model_manifest.csv")
OUT = os.path.join(ROOT, "model_candidates.csv")
API = "https://api.sketchfab.com/v3/search"

LICENSES = {"CC0 Public Domain": "CC0", "CC Attribution": "CC-BY"}
BAD_TAGS = {"lowpoly", "low-poly", "low_poly", "lowpolyart", "stylized", "cartoon", "toon", "voxel", "pixel",
            "blockbench", "minecraft", "roblox", "chibi", "cute", "ai", "meshy", "createdwithai", "tripo",
            "ai-generated", "ark", "arksurvivalevolved", "ark-survival-evolved", "arksurvival", "fanart"}
BAD_WORDS = ("low poly", "lowpoly", "low-poly", "stylized", "cartoon", "voxel", "minecraft", "roblox", "ark survival")
GOOD_TAGS = {"realistic", "pbr", "photogrammetry", "scan", "3dscan", "photoscan", "substancepainter",
             "game-ready", "gameready", "gameasset", "game-asset", "survival", "prop", "props"}
# Roblox MeshPart limit is 20k triangles; up to MAX_FACES is fine to decimate in Blender.
TRI_BUDGET = 20000
MAX_FACES = 150000
MIN_FACES = 300

FIELDS = ["AssetPath", "DisplayName", "Rank", "Chosen", "Score", "Query", "Uid", "Name", "Author", "License",
          "Faces", "NeedsDecimate", "Likes", "Url", "Thumb"]


def search(q):
    params = {"type": "models", "q": q, "downloadable": "true", "count": 24, "max_face_count": MAX_FACES}
    url = API + "?" + urllib.parse.urlencode(params)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "ark-blox"}),
                                        timeout=30) as r:
                return json.load(r)["results"]
        except Exception as e:  # rate limit or network hiccup
            wait = 2 ** (attempt + 1)
            print(f"  retry {q!r} in {wait}s ({e})")
            time.sleep(wait)
    return []


def score(r, query):
    lic = LICENSES.get((r.get("license") or {}).get("label"))
    if not lic or r.get("isAgeRestricted"):
        return None
    tags = {t["slug"].lower() for t in r.get("tags", [])}
    text = (r["name"] + " " + (r.get("description") or "")[:300]).lower()
    if tags & BAD_TAGS or any(w in text for w in BAD_WORDS):
        return None
    faces = r.get("faceCount") or 0
    if faces < MIN_FACES:
        return None
    words = [w for w in query.lower().split() if len(w) > 2 and w not in ("realistic", "photogrammetry")]
    name = r["name"].lower()
    s = sum(2 for w in words if w in name)
    s += 3 * len(tags & GOOD_TAGS) + (2 if "realistic" in text or "pbr" in text else 0)
    s += 2 if faces <= TRI_BUDGET else (1 if faces <= 60000 else 0)
    s += math.log10(1 + r.get("likeCount", 0)) * 2 + (3 if r.get("staffpickedAt") else 0)
    return round(s, 2), lic, faces


def pick(row, top):
    out = []
    for q in row["SketchfabQuery"].split("|"):
        for r in search(q):
            sc = score(r, q)
            if sc is None or any(o["Uid"] == r["uid"] for o in out):
                continue
            s, lic, faces = sc
            thumbs = sorted(r["thumbnails"]["images"], key=lambda i: abs(i["width"] - 256))
            out.append({"AssetPath": row["AssetPath"], "DisplayName": row["DisplayName"], "Score": s, "Query": q,
                        "Uid": r["uid"], "Name": r["name"], "Author": r["user"]["username"], "License": lic,
                        "Faces": faces, "NeedsDecimate": int(faces > TRI_BUDGET), "Likes": r.get("likeCount", 0),
                        "Url": r["viewerUrl"], "Thumb": thumbs[0]["url"] if thumbs else ""})
        time.sleep(0.4)
        if len(out) >= top:
            break
    out.sort(key=lambda o: -o["Score"])
    out = out[:top]
    for i, o in enumerate(out):
        o["Rank"] = i + 1
        o["Chosen"] = 1 if i == 0 else 0
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="", help="AssetPath prefix, e.g. SADDLES/")
    ap.add_argument("--top", type=int, default=3)
    a = ap.parse_args()

    rows = [r for r in csv.DictReader(open(MANIFEST)) if r["Status"] == "todo" and r["AssetPath"].startswith(a.only)]
    # Keep existing results (and manual Chosen edits) for assets not being re-searched.
    kept = []
    if os.path.exists(OUT):
        redo = {r["AssetPath"] for r in rows}
        kept = [r for r in csv.DictReader(open(OUT)) if r["AssetPath"] not in redo]
    found, missing = [], []
    for i, row in enumerate(rows, 1):
        c = pick(row, a.top)
        print(f"[{i}/{len(rows)}] {row['AssetPath']}: {len(c)} ({c[0]['Name'] if c else '-'})")
        if c:
            found += c
        else:
            missing.append(row["AssetPath"])
            found.append({"AssetPath": row["AssetPath"], "DisplayName": row["DisplayName"], "Rank": 0, "Chosen": 0,
                          "Query": row["SketchfabQuery"], "Name": "NO CANDIDATE"})
    allrows = sorted(kept + found, key=lambda r: (r["AssetPath"], int(r["Rank"])))
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(allrows)
    print(f"wrote {OUT}: {len(rows) - len(missing)} assets with candidates, {len(missing)} without")
    for m in missing:
        print("  missing", m)


if __name__ == "__main__":
    main()
