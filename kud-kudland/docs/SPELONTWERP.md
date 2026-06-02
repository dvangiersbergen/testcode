# Spelontwerp — KUDLAND

Waarom dit spel, hoe de mechaniek werkt, en hoe de KUD-art mechanisch meedoet.

## Designdoel
Een 2+ kaart/tegelspel waarin de **KUD-afbeeldingen de kern** zijn, niet versiering. In KUDLAND
zijn de afleveringen letterlijk de **bouwstenen van het speelveld** — je legt de wereld van KUD op
tafel. De art doet er dus dubbel toe: visueel (herkenning, plezier) én ruimtelijk (de randen
bepalen waar een tegel mag liggen).

## Mechaniek-kern (genre: leg-/tegelspel)
Geïnspireerd op **Carcassonne** (rand-matching + gebieden claimen met pionnen) en **Kingdomino**
(score = grootte × waarde). De originele draai:

- **Randterreinen** (Zee/Land/Weg/Lucht) maken het leggen een ruimtelijke puzzel; **draaien** mag.
- **Gebieden claimen** met fan-pionnen geeft interactie en timing (wanneer claim je, wanneer sluit
  je een gebied af om te scoren?).
- **Sterren (✦)** koppelen de score aan hoe *iconisch* een aflevering is.
- **Special-afleveringen** (Pilon = wild, Konijntje ×2, Vliegende Koe +3, Zwoele Man) geven
  KUD-flavor én tactische uitschieters.

Diepte: medium, hoge herspeelbaarheid (elk potje een andere kaart). Werkt vanaf 2 spelers.

## Hoe de art is verkregen (belangrijk)
De omgeving heeft **geen** `yt-dlp`/`ffmpeg`, dus losse *videoframes* extraheren kon niet. Wél
beschikbaar: het officiële **KUD YouTube-kanaal** van Peter Lub (`UC39KF9j7hucS2xncTO8d5CQ`).
Daarvan zijn per aflevering de **officiële thumbnails** opgehaald — echte KUD-art, precies één
beeld per aflevering, wat naadloos op één-tegel-per-aflevering past.

Pijplijn (volledig reproduceerbaar):
1. `framework/fetch_art.py` → haalt videolijst (RSS + kanaalpagina) en downloadt de thumbnails
   naar `print/assets/<videoId>.jpg`; titels via RSS + oEmbed in `data/manifest.csv`.
2. `framework/make_tiles.py` → wijst per aflevering deterministisch randterreinen, een personage,
   sterren en eventuele special toe → `data/tiles.csv`.
3. `framework/build.py` → componeert elke tegel (art + terreinranden + overlays) naar
   `print/tiles/<id>.png`, en bouwt `print/print.html` (knipvel) + `print/KUDLAND.pdf`
   (regelboek + tegel-galerij + token-vel). Alleen Pillow.

Vervang of breid uit door extra thumbnails op te halen en de scripts opnieuw te draaien.

## Ontwerpkeuzes & balans
- **Terreinverdeling** is met opzet redelijk gelijk (zee/land/weg elk ~28 randen, lucht iets
  minder) zodat leggen meestal kan, maar niet triviaal is.
- **Wildcard (Pilon)** voorkomt vastlopers en is thematisch puur KUD.
- **Sterren 0–3** via hash → spreiding; iconische afleveringen kun je handmatig ophogen in
  `tiles.csv` als je echte KUD-kennis wilt verwerken.
- **Deterministisch** (md5 van videoId): dezelfde afleveringen geven altijd dezelfde tegels, dus
  het prototype is stabiel en herbouwbaar.

## Wat dit is — en niet
Dit is een **speelbaar prototype** om het concept te zien en te testen. Het is geen eindproduct:
de art is thumbnail-resolutie en het materiaal is auteursrechtelijk beschermd (zie `CREDITS.md`).
Voor een net product zou je met toestemming van Peter Lub hoge-resolutie KUD-stills gebruiken.
