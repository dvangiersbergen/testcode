# Panelen (art) — plaats hier je vierkante KUD-frames

Zet hier de KUD-beelden die je verzamelt (zie [`../../docs/ART-EN-TEKST-VERZAMELEN.md`](../../docs/ART-EN-TEKST-VERZAMELEN.md)).

## Regels
- Bestandsnaam = exact de waarde in de kolom `art` van `panels.csv`, bv. `groene-camera.png`.
- Formaten: `.png`, `.jpg`, `.jpeg`, `.webp`, `.gif`.
- **Vierkant** bijsnijden (de kaarten zijn vierkant). Richtlijn ~1000×1000 px.
- Ontbreekt een bestand? De generator zet automatisch een **placeholder** met de scene-omschrijving,
  zodat je kunt testspelen en ziet wat je nog mist.

## Snel vierkant maken (ImageMagick)
```bash
magick frame.png -gravity center -extent "%[fx:min(w,h)]x%[fx:min(w,h)]" -resize 1000x1000 groene-camera.png
```

## Toestemming
KUD-beelden © Peter Lub / KUD. Privé thuisgebruik doorgaans oké; delen/publiceren/drukken vereist
toestemming. Zie `../../docs/CREDITS.md`.
