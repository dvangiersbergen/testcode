# KUDLAND 🗺️

Een **legspel met échte KUD-afleveringen**. Iedere tegel is een KUD-aflevering met vier
randterreinen (Zee · Land · Weg · Lucht); je legt de afleveringen aan elkaar tot de kaart van
Kudland en claimt de grootste, meest iconische scenes. **2–4 spelers · ±25 min.**

Genre: tegellegspel (in de geest van Carcassonne / Kingdomino). De KUD-art doet **mechanisch** mee:
de randen bepalen waar een tegel mag liggen.

> **Onofficieel fan-prototype** — alleen voor privé/testgebruik. KUD-beelden © Peter Lub / KUD.
> Zie [`docs/CREDITS.md`](docs/CREDITS.md).

## 📦 Het belangrijkste bestand
**[`print/KUDLAND.pdf`](print/KUDLAND.pdf)** — het complete regelboek + tegel-galerij + token-vel.
Hierin zie je in één oogopslag hoe het concept eruitziet.

## Hoe het is gebouwd (reproduceerbaar)
```bash
cd framework
python3 fetch_art.py     # 1) download echte KUD-thumbnails -> print/assets/  (+ data/manifest.csv)
python3 make_tiles.py    # 2) wijs randterreinen/personage/sterren toe -> data/tiles.csv
python3 build.py         # 3) componeer tegels + print.html + KUDLAND.pdf
```
Vereist: Python + **Pillow** (`pip install Pillow`). Geen yt-dlp/ffmpeg nodig — er worden
video-**thumbnails** gebruikt (frames extraheren kon niet in deze omgeving).

## Inhoud
| Pad | Wat |
|-----|-----|
| [`print/KUDLAND.pdf`](print/KUDLAND.pdf) | **Regelboek + galerij + tokens (de hoofd-deliverable)** |
| [`print/print.html`](print/print.html) | Knipvel om de tegels op A4 te printen (60 mm) |
| [`print/tiles/`](print/tiles/) | De gecomponeerde speeltegels (PNG) |
| [`print/assets/`](print/assets/) | Opgehaalde KUD-thumbnails (bron-art) |
| [`docs/SPELREGELS.md`](docs/SPELREGELS.md) | Spelregels (tekst) |
| [`docs/SPELONTWERP.md`](docs/SPELONTWERP.md) | Ontwerp, mechaniek & hoe de art is verkregen |
| [`docs/CREDITS.md`](docs/CREDITS.md) | Credits, bronnen & auteursrecht |
| [`framework/`](framework/) | De drie scripts + `data/` (manifest, tiles) |

## Status
28 echte KUD-afleveringen + 1 startveld = **29 tegels**. Met thumbnail-resolutie art; voor een net
product horen hoge-resolutie stills met toestemming van Peter Lub gebruikt te worden.

> Zusterprojecten in deze repo: [`../kud-therapie/`](../kud-therapie/) en
> [`../kud-verschrikkelijk-stel/`](../kud-verschrikkelijk-stel/).
