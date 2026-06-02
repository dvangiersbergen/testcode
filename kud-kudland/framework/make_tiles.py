#!/usr/bin/env python3
"""
make_tiles.py — bouwt data/tiles.csv uit data/manifest.csv.

Per aflevering-thumbnail wordt deterministisch een KUDLAND-tegel gedefinieerd:
  - 4 randterreinen N,E,S,W uit {Z=Zee, G=Land, W=Weg, L=Lucht, *=wild}
  - 1 personage (de 'fan-magneet' / scene-eigenaar)
  - sterren 0..3 (hoe iconisch de scene is)
  - special: '', konijntje, koe, pilon, zwoele

Deterministisch (md5 van videoId) => zelfde input geeft altijd dezelfde tegels.
Daarna garanderen we dat elk special-type minstens 1x voorkomt.
"""
from __future__ import annotations
import csv, hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "data" / "manifest.csv"
TILES = HERE / "data" / "tiles.csv"

TERRAINS = ["Z", "G", "W", "L"]            # zee, land, weg, lucht
PERSONAGES = [
    "Die Groene", "Die Roze", "Zwoele Man", "Konijntje", "Werner de walvis",
    "Albatros", "Vliegende Koe", "Cleeuwn", "Wiebe", "De Ridder", "Papegaai", "Pilon",
]
# titel-trefwoord -> personage (thematische overrides)
KEYWORDS = {
    "zwaard": "De Ridder", "zelda": "De Ridder", "ridder": "De Ridder",
    "eet me niet": "Werner de walvis", "walvis": "Werner de walvis",
    "comazuipen": "Wiebe", "drama": "Cleeuwn", "krols": "Die Roze",
    "te laat": "Die Groene", "nieuw": "Die Groene", "politieschets": "Papegaai",
}
SPECIAL_BY_CHAR = {"Konijntje": "konijntje", "Vliegende Koe": "koe",
                   "Pilon": "pilon", "Zwoele Man": "zwoele"}


def hbytes(s: str) -> bytes:
    return hashlib.md5(s.encode()).digest()


def tile_for(vid: str, title: str) -> dict:
    h = hbytes(vid)
    edges = [TERRAINS[h[i] % len(TERRAINS)] for i in range(4)]
    # personage: trefwoord wint, anders hash
    char = None
    low = title.lower()
    for kw, c in KEYWORDS.items():
        if kw in low:
            char = c; break
    if char is None:
        char = PERSONAGES[h[4] % len(PERSONAGES)]
    stars = h[5] % 4                          # 0..3
    special = SPECIAL_BY_CHAR.get(char, "")
    if special == "pilon":
        edges = ["*", "*", "*", "*"]          # pilon = wildcard randen
        stars = 0
    return {"id": vid, "title": title,
            "n": edges[0], "e": edges[1], "s": edges[2], "w": edges[3],
            "personage": char, "sterren": stars, "special": special}


def main() -> int:
    rows = list(csv.DictReader(MANIFEST.open(encoding="utf-8")))
    tiles = [tile_for(r["videoId"], r["title"]) for r in rows]

    # garandeer minstens 1 van elk special-type
    have = {t["special"] for t in tiles}
    need = [(c, s) for c, s in SPECIAL_BY_CHAR.items() if s not in have]
    for i, (char, sp) in enumerate(need):
        t = tiles[-(i + 1)]
        t["personage"], t["special"] = char, sp
        if sp == "pilon":
            t.update(n="*", e="*", s="*", w="*", sterren=0)

    # startbron: 1 'startveld' met alle vier terreinen (1 per rand) voor flexibele opbouw
    start = {"id": "START", "title": "Het Plein van Kudland",
             "n": "G", "e": "Z", "s": "W", "w": "L",
             "personage": "Die Groene", "sterren": 1, "special": "start"}
    tiles.insert(0, start)

    cols = ["id", "title", "n", "e", "s", "w", "personage", "sterren", "special"]
    with TILES.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(tiles)

    print(f"tiles.csv: {len(tiles)} tegels (incl. startveld)")
    from collections import Counter
    print("  terreinen:", Counter(e for t in tiles for e in (t['n'],t['e'],t['s'],t['w'])))
    print("  specials :", Counter(t['special'] for t in tiles if t['special']))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
