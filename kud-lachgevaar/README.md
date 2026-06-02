# KUD: Lachgevaar 💥

Maak samen de wreedste, domste **3-panel KUD-strip**. Eén stapel losse KUD-panelen; de rechter legt
het begin, jij vult met één kaart het slotpaneel aan, de grappigste wint. Onofficieel fan-kaartspel,
in het Nederlands, **naar Joking Hazard** (Cyanide & Happiness), helemaal omgebouwd rond **KUD**
(Peter Lub).

> **Onofficieel · privégebruik · 3–10 spelers.** Mechaniek-inspiratie: *Joking Hazard* © Explosm.
> KUD-beelden © Peter Lub / KUD — privé uitprinten oké, delen/publiceren vereist toestemming.
> Zie [`docs/CREDITS.md`](docs/CREDITS.md).

---

## Zo werkt het (kort)
1. Iedereen heeft 7 panelen op de hand.
2. De **bouwer** draait paneel 1 en speelt paneel 2 → het begin van de strip staat.
3. Iedereen levert gedekt een **paneel 3** in. De bouwer leest elke strip voor en kiest de grappigste.
4. Winnaar krijgt een punt. **Rode kaarten** zijn slotpanelen; eerste bij **3 punten** wint.

Volledige regels: [`docs/SPELREGELS.md`](docs/SPELREGELS.md).

## ⭐ Belangrijkste voor jou: art & tekst verzamelen
Het spel leeft van goede panelen. De complete praktische gids — KUD-frames uit afleveringen halen
(`yt-dlp` + `ffmpeg`), vierkant bijsnijden, in KUD-stijl bijschrijven, en de auteursrecht-afspraken —
staat in **[`docs/ART-EN-TEKST-VERZAMELEN.md`](docs/ART-EN-TEKST-VERZAMELEN.md)**.

## Snel starten (print & play)
```bash
cd framework
python3 generate_cards.py        # bouwt ../print/print.html (vierkante kaarten, A4)
```
Open `print/print.html` en print op A4 (schaal 100%). Zónder eigen art krijg je nette
**placeholders** met de scene-omschrijving van elk paneel — meteen testspeelbaar, en tegelijk je
verzamel-checklist. Voeg vierkante KUD-frames toe in [`print/assets/`](print/assets/) en draai opnieuw.

Startset: **60 panelen** (42 gewoon · 13 rode slotpanelen · 5 blanco).

## Mappenstructuur
| Pad | Wat |
|-----|-----|
| [`docs/SPELREGELS.md`](docs/SPELREGELS.md) | Speelbare regels (NL) |
| [`docs/ART-EN-TEKST-VERZAMELEN.md`](docs/ART-EN-TEKST-VERZAMELEN.md) | **Hoe je passende art & tekst verzamelt** |
| [`docs/SPELONTWERP.md`](docs/SPELONTWERP.md) | Ontwerp + vertaling van *Joking Hazard* naar KUD |
| [`docs/CREDITS.md`](docs/CREDITS.md) | Credits, bronnen & auteursrecht |
| [`framework/kaart-schema.md`](framework/kaart-schema.md) | Datamodel van de panelen |
| [`framework/data/panels.csv`](framework/data/panels.csv) | De panelen (uitbreidbaar) |
| [`framework/generate_cards.py`](framework/generate_cards.py) | CSV + art → print-klaar HTML |
| [`print/assets/`](print/assets/) | Jouw vierkante KUD-frames (bestandsnaam = `art`) |

> Zusterprojecten in deze repo: [`../kud-therapie/`](../kud-therapie/),
> [`../kud-verschrikkelijk-stel/`](../kud-verschrikkelijk-stel/) en [`../kud-kudland/`](../kud-kudland/).
