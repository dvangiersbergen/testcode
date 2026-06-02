#!/usr/bin/env python3
"""
fetch_art.py — haalt echte KUD-afbeeldingen (video-thumbnails) op van het officiele
KUD YouTube-kanaal van Peter Lub en zet ze in ../print/assets/.

Waarom thumbnails: dit is de hoogst-toegankelijke echte KUD-art per aflevering.
Frames uit de video's halen kan niet (geen yt-dlp/ffmpeg in deze omgeving).

Output:
  ../print/assets/<videoId>.jpg   (de thumbnails)
  data/manifest.csv               (videoId,title)

Alleen voor PRIVE prototype-gebruik. Alle beelden (c) Peter Lub / KUD.
"""
from __future__ import annotations
import csv, re, sys, time
from pathlib import Path
import requests

HERE = Path(__file__).resolve().parent
ASSETS = HERE.parent / "print" / "assets"
MANIFEST = HERE / "data" / "manifest.csv"

CHANNEL_ID = "UC39KF9j7hucS2xncTO8d5CQ"          # "Kud" — Peter Lub
RSS = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
VIDEOS_PAGE = f"https://www.youtube.com/channel/{CHANNEL_ID}/videos"
HEADERS = {"User-Agent": "Mozilla/5.0", "Accept-Language": "nl-NL,nl;q=0.9"}
MAX_TILES = 28
THUMB = "https://i.ytimg.com/vi/{vid}/hqdefault.jpg"


def get(url: str) -> str:
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    return r.text


def rss_titles() -> dict[str, str]:
    """videoId -> title uit de RSS-feed (betrouwbaar, ~15 nieuwste)."""
    xml = get(RSS)
    out = {}
    for m in re.finditer(r"<entry>(.*?)</entry>", xml, re.S):
        block = m.group(1)
        vid = re.search(r"<yt:videoId>([\w-]{11})</yt:videoId>", block)
        title = re.search(r"<title>(.*?)</title>", block, re.S)
        if vid and title:
            out[vid.group(1)] = re.sub(r"\s+", " ", title.group(1)).strip()
    return out


def page_ids() -> list[str]:
    """Extra videoId's van de /videos-pagina (volgorde behouden, ontdubbeld)."""
    try:
        html = get(VIDEOS_PAGE)
    except Exception as e:
        print(f"  (videos-pagina niet beschikbaar: {e})")
        return []
    seen, ids = set(), []
    for m in re.finditer(r'"videoId":"([\w-]{11})"', html):
        v = m.group(1)
        if v not in seen:
            seen.add(v); ids.append(v)
    return ids


def main() -> int:
    ASSETS.mkdir(parents=True, exist_ok=True)
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)

    print(f"Kanaal: Kud ({CHANNEL_ID})")
    titles = rss_titles()
    print(f"  RSS-titels: {len(titles)}")
    order = list(titles.keys())
    for v in page_ids():                      # vul aan tot MAX_TILES
        if v not in titles:
            titles.setdefault(v, "KUD-aflevering")
            order.append(v)
        if len(order) >= MAX_TILES:
            break
    order = order[:MAX_TILES]
    print(f"  Te downloaden tegels: {len(order)}")

    rows, ok = [], 0
    for i, vid in enumerate(order, 1):
        dest = ASSETS / f"{vid}.jpg"
        if not dest.exists():
            try:
                r = requests.get(THUMB.format(vid=vid), headers=HEADERS, timeout=20)
                if r.status_code == 200 and len(r.content) > 2000:
                    dest.write_bytes(r.content)
                    ok += 1
                else:
                    print(f"  ! {vid}: http {r.status_code}, {len(r.content)} bytes — overslaan")
                    continue
            except Exception as e:
                print(f"  ! {vid}: {e}")
                continue
            time.sleep(0.2)
        else:
            ok += 1
        rows.append({"videoId": vid, "title": titles[vid]})
        print(f"  [{i:2d}/{len(order)}] {vid}  {titles[vid][:48]}")

    with MANIFEST.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["videoId", "title"])
        w.writeheader(); w.writerows(rows)

    print(f"\nKlaar: {ok} thumbnails -> {ASSETS}")
    print(f"Manifest: {MANIFEST}")
    return 0 if rows else 1


if __name__ == "__main__":
    raise SystemExit(main())
