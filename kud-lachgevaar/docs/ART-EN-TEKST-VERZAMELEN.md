# Art & tekst verzamelen voor KUD: Lachgevaar

Dit is het belangrijkste werk: het spel valt of staat met goede **strip-panelen**. Hieronder een
praktische werkwijze om passende KUD-beelden en -teksten te verzamelen en in het spel te krijgen.

> ⚖️ **Eerst dit:** alle KUD-beelden en personages zijn © **Peter Lub / KUD**. Frames uit
> afleveringen en kanaal-thumbnails zijn auteursrechtelijk beschermd. Voor **privé thuisgebruik**
> (zelf uitprinten, met vrienden spelen) is dit doorgaans prima. Wil je het **delen, drukken,
> publiceren of verkopen**, dan heb je **toestemming van Peter Lub** nodig. Vraag het gewoon —
> makers vinden fan-projecten vaak leuk, mits netjes gevraagd en gecrediteerd.

---

## Deel 1 — Art (de panelen)

### 1.1 Wat is een goed paneel?
Joking Hazard-humor komt uit de **combinatie** van drie panelen, niet uit één plaatje. Mik daarom op:

- **Opener-/setup-panelen:** één personage, neutrale of verwachtingsvolle blik, recht in beeld,
  weinig achtergrondruis. (bv. Die Groene kijkt in de camera.)
- **Reactie-panelen:** duidelijke emotie — geschokt, leeg, boos, te blij.
- **Slot-/punchline-panelen (de "rode" kaarten):** absurde of plotselinge beelden die alles
  kantelen (Werner de walvis valt uit de lucht, een konijntje, een explosie, Zwoele Man).
- **Visueel = sterker dan tekst.** Veel van de beste panelen hebben **geen** bijschrift.

Vuistregel bij het kijken: *"Zou dit beeld grappig zijn als willekeurig 1e, 2e óf 3e paneel?"*
Hoe meer posities het aankan, hoe waardevoller de kaart.

### 1.2 Bronnen van beeld
1. **De afleveringen zelf** (beste kwaliteit en variatie) — KUD YouTube-kanaal van Peter Lub.
2. **Kanaal-thumbnails** (snelst, maar 1 beeld per aflevering en lage resolutie).
3. **Eigen screenshots** tijdens het kijken (pauzeer op een grappig frame).

### 1.3 Frames uit afleveringen halen — gereedschap
Je hebt twee tools nodig: **yt-dlp** (video binnenhalen) en **ffmpeg** (frames eruit knippen).

```bash
# installeren (eenmalig)
pip install -U yt-dlp           # of: brew install yt-dlp
#   ffmpeg: brew install ffmpeg   |   sudo apt install ffmpeg   |   choco install ffmpeg

# 1) aflevering downloaden (kies een redelijke kwaliteit)
yt-dlp -f "bv*[height<=1080]+ba/b" -o "aflevering.%(ext)s" "<YOUTUBE-URL>"

# 2a) één frame op een exact tijdstip (mm:ss) — voor een specifieke grap
ffmpeg -ss 00:01:23 -i aflevering.mp4 -frames:v 1 -q:v 2 paneel.png

# 2b) automatisch frames op scène-wisselingen (vangt veel bruikbare 'shots')
mkdir -p frames
ffmpeg -i aflevering.mp4 -vf "select='gt(scene,0.4)'" -vsync vfr frames/scene_%04d.png

# 2c) gewoon elke 2 seconden een frame (grof maar compleet)
ffmpeg -i aflevering.mp4 -vf fps=1/2 frames/grid_%04d.png
```

Geen zin in commandline? Alternatieven: **VLC** (Video ▸ Momentopname maken), **pauzeren +
schermafbeelding**, of **OBS** met een hotkey-screenshot.

### 1.4 Bijsnijden naar vierkant
De kaarten zijn **vierkant** (panelen leggen zo netjes naast elkaar tot een strip). Snijd je beeld
centraal vierkant bij:

```bash
# ImageMagick: centrale vierkante crop, daarna schalen naar 1000x1000
magick paneel.png -gravity center -extent "%[fx:min(w,h)]x%[fx:min(w,h)]" -resize 1000x1000 assets-klaar/paneel.png
```

Richtlijn: **~1000×1000 px** is ruim voldoende voor scherp printen op ~60 mm.

### 1.5 In het spel krijgen
1. Zet het vierkante bestand in [`../print/assets/`](../print/assets/), bv. `groene-camera.png`.
2. Vul in `framework/data/panels.csv` de kolom **`art`** met exact die bestandsnaam.
3. Draai `python3 framework/generate_cards.py`. Klaar — `print/print.html` toont nu jouw beeld
   i.p.v. de placeholder. Panelen zonder bestand blijven een nette placeholder (handig om te zien
   wat je nog mist).

---

## Deel 2 — Tekst (bijschriften)

### 2.1 Vaak: géén tekst
Laat panelen zo veel mogelijk **woordloos**. De grap ontstaat uit de volgorde. Tekst voegt alleen
iets toe als het de juxtapositie scherper maakt.

### 2.2 Als je wél tekst gebruikt — toon & stijl
- **Kort en droog.** Eén korte zin of een los woord. ("Boeiend.", "Konijntje.", "…oké dan.")
- **Understatement.** Hoe absurder het beeld, hoe nuchterder de tekst.
- **Open einde in setup-panelen.** ("Ik moet je iets vertellen.") zodat elk slotpaneel erop past.
- **KUD-nuchter, niet uitleggerig.** Niet de grap navertellen.

> 🚫 **Belangrijk:** schrijf **eigen** bijschriften in KUD-stijl. Neem **geen** letterlijke dialoog,
> songteksten of langere fragmenten uit de afleveringen over — dat is auteursrechtelijk materiaal.
> Laat je inspireren door de toon, niet door de woorden.

### 2.3 Tekst in het spel krijgen
Vul de kolom **`tekst`** in `panels.csv`. Die verschijnt als bijschrift onder het beeld. Leeg laten =
woordloos paneel.

---

## Deel 3 — Een efficiënte werkwijze (scène-bank)

Bouw terwijl je kijkt een lijst op. `panels.csv` is precies die lijst:

| stap | wat |
|------|-----|
| 1 | Kijk een aflevering met `panels.csv` open ernaast. |
| 2 | Zie je een bruikbaar shot? Noteer een regel: `id`, korte `scene`-omschrijving, evt. `tekst`, en `rood=1` als het een knaller-slot is. Zet de `bron` (afleveringtitel) erbij. |
| 3 | Pak het frame (1.3), snijd vierkant (1.4), zet in `assets/`, vul `art` in. |
| 4 | Regenereer en testspeel. |

**Balans-richtlijn voor een leuk deck (~60–120 kaarten):**
- ~70% gewone panelen (setups + reacties),
- ~25% rode slotpanelen (`rood=1`),
- ~5% blanco (`blanco=1`) om zelf in te vullen.

Streef naar **variatie in personages** (Die Groene, Die Roze, Zwoele Man, Konijntje, Werner,
Wiebe, Cleeuwn, pilon, …) en in **shot-types** (close-up, totaal, reactie, absurd).

Zie [`../framework/kaart-schema.md`](../framework/kaart-schema.md) voor alle kolommen.
