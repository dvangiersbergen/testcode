# Spelontwerp & framework — KUD: De Waardeloze Therapeut

Dit document legt de ontwerpkeuzes vast: hoe het origineel werkt, hoe we het naar KUD vertalen,
waarom het mechaniek past bij de stijl, en hoe het kaart-framework technisch in elkaar zit.

---

## 1. Het origineel: *Horrible Therapist* (Exploding Kittens)

Geverifieerde mechaniek (officiële regels):

- Drie aparte decks: **Question** (70), **Answer** (135), **Treatment** (175).
- Iedere ronde is één speler de **Therapist**.
- De Therapist draait een **Question**-kaart open, trekt **3 Answer**-kaarten en kiest er 1 →
  samen vormen die de opzet van de "patiënt".
- Alle andere spelers leggen 1 **Treatment**-kaart uit een hand van **5**.
- De Therapist kiest de grappigste Treatment; die speler scoort.
- Het geheel leest als een **strip van 3 panelen**. Eerste bij **3 punten** wint.

Bron: officialgamerules.org / geekyhobbies — *Horrible Therapist*, Exploding Kittens.

## 2. Waarom dit perfect bij KUD past

KUD is **animatie**: het is letterlijk beeld. Een paneel-strip-spel is daardoor ideaal — elk
paneel kan een KUD-still zijn. De humor van KUD draait bovendien om **botsing**: nuchtere opzet
+ absurde wending. Dat is exact wat een "klacht → behandeling"-mechaniek doet: de speler levert
de absurde wending op een serieus klinkend probleem.

Dit is dezelfde familie als *Joking Hazard* (Cyanide & Happiness) en *What Do You Meme* —
beeld-gedreven panel-/reactiespellen. We kiezen bewust voor de Horrible-Therapist-structuur
omdat de **therapie-framing** (patiënt op de bank + diagnose) een sterk, samenhangend thema
geeft i.p.v. losse plaatjes.

## 3. Vertaaltabel

| Horrible Therapist | KUD: De Waardeloze Therapeut | Paneel | Drager |
|--------------------|------------------------------|--------|--------|
| Question (open gedraaid) | **Patiënt** — KUD-personage op de bank | 1 | **beeld** (still) |
| Answer (3 trekken, 1 kiezen) | **Klacht** — het absurde probleem | 2 | tekst |
| Treatment (handkaart, hand van 5) | **Behandeling** — KUD-fragment als therapie | 3 | **beeld** (still) + bijschrift |
| Therapist (rol per ronde) | **Therapeut** — bouwt opzet + jureert | — | — |
| Point | **Diploma** | — | — |
| 3 points to win | 3 Diploma's → **Hoofdtherapeut** | — | — |

Ontwerpkeuze: **paneel 1 en 3 zijn beeldkaarten** (art-focus), **paneel 2 is tekst**. Zo blijft
het spel maximaal visueel/KUD, terwijl de tekstklacht genoeg sturing geeft voor scherpe grappen.

## 4. Thema-mechanieken (meer dan een reskin)

Toegevoegd om KUD-DNA in de spelregels te brengen (zie `SPELREGELS.md` + `speciale-kaarten.csv`):

- **Zwoele Man** — bonus-Diploma; bouwt voort op een geverifieerd terugkerend personage.
- **Te laat** — naar de gelijknamige video: een "te laat" omruil-actie.
- **Djingle Djengle** — naar het interactieve liedjesproject: bijschrift zíngen.
- **pilon** — running-gag-kaart die niet genegeerd mag worden.
- **Nieuw! / Plot Twist** — wisselt de patiënt mid-ronde (verwijzing naar de "Nieuw!"-video).
- **"Ik snap het zelf ook niet helemaal"** — joker-bijschrift; een geverifieerd Peter Lub-citaat.

## 5. Het kaart-framework (technisch)

Alles is **data-gedreven en uitbreidbaar**. Je voegt kaarten toe door regels aan CSV-bestanden
toe te voegen en (optioneel) een afbeelding in `print/assets/` te zetten — daarna genereer je
een print-klaar vel.

```
kud-therapie/
├── docs/            spelregels, dit ontwerp, credits
├── content/         geverifieerde KUD-catalogus + grappigheids-framework
├── framework/
│   ├── kaart-schema.md         het datamodel (kolommen + regels)
│   ├── data/                   de kaartinhoud (CSV)
│   │   ├── patienten.csv
│   │   ├── klachten.csv
│   │   ├── behandelingen.csv
│   │   └── speciale-kaarten.csv
│   └── generate_cards.py       CSV + assets  ->  print/print.html
└── print/
    ├── assets/      jouw KUD-stills (.png/.jpg), bestandsnaam = kolom `fragment`
    └── print.html   gegenereerd, print-klaar (A4, snijbaar)
```

### Werkwijze om je eigen fragmenten toe te voegen

1. Vraag de KUD-maker om de stills/fragmenten (toestemming = privégebruik).
2. Zet elke afbeelding in `print/assets/`, bv. `konijntje.png`.
3. Zet in de juiste CSV een regel met `fragment=konijntje.png`, een `bijschrift`, en de `bron`.
4. Draai `python3 framework/generate_cards.py`.
5. Open `print/print.html` in de browser → printen op 300 g/m² → snijden → spelen.

Kaarten zonder afbeelding krijgen automatisch een **placeholder** met de gewenste fragmentnaam,
zodat het deck nu al speelbaar/testbaar is en je precies weet welke art je nog nodig hebt.

## 6. Kaartformaat & print

- Standaard kaartformaat **63 × 88 mm** (poker/MtG), met 3 mm snijmarge-indicatie.
- Layout: 9 kaarten per A4 (3×3). Aparte vellen voor kaartruggen per type.
- Kleurcodering per type (zie `kaart-schema.md`) zodat sorteren makkelijk is.

## 7. Juridisch / scope

Privé thuisspel. Geen verkoop, geen distributie. Mechaniek-inspiratie: *Horrible Therapist*
(Exploding Kittens). KUD-IP © Peter Lub, gebruikt met toestemming. Zie `CREDITS.md`.
