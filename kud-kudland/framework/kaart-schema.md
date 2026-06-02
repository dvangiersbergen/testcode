# Datamodel — KUDLAND

Twee CSV's in `data/` sturen de hele build aan.

## `manifest.csv` — bron-afleveringen (door `fetch_art.py`)
| Kolom | Betekenis |
|-------|-----------|
| `videoId` | YouTube-video-id; bijbehorende thumbnail staat als `../print/assets/<videoId>.jpg`. |
| `title` | Afleveringstitel (RSS/oEmbed). Wordt als label op de tegel/galerij gebruikt. |

## `tiles.csv` — tegeldefinities (door `make_tiles.py`, vrij te bewerken)
| Kolom | Betekenis |
|-------|-----------|
| `id` | `videoId` van de aflevering (of `START` voor het startveld). |
| `title` | Titel/label van de tegel. |
| `n` `e` `s` `w` | Randterrein boven/rechts/onder/links: `Z`=Zee, `G`=Land, `W`=Weg, `L`=Lucht, `*`=wild. |
| `personage` | De scene-eigenaar op de tegel (bv. `Konijntje`, `Werner de walvis`). |
| `sterren` | 0–3 — hoe iconisch de scene; telt mee in de score (✦). |
| `special` | `` (geen), `konijntje` (×2), `koe` (+3 lucht), `pilon` (wild, 0 ✦), `zwoele`, `start`. |

## Handmatig finetunen
`tiles.csv` is gewoon tekst: wil je een echte topafleving meer gewicht geven, zet `sterren` op 3;
wil je een terrein-mix aanpassen, verander `n/e/s/w`. Draai daarna `python3 build.py` opnieuw —
de tegels, `print.html` en `KUDLAND.pdf` worden opnieuw gegenereerd.

## Uitbreiden met meer afleveringen
Verhoog `MAX_TILES` in `fetch_art.py`, draai `fetch_art.py` → `make_tiles.py` → `build.py`.
