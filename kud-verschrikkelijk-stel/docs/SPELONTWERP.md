# Spelontwerp & framework — KUD: Verschrikkelijk Stel

Hoe het origineel werkt, hoe we het naar KUD vertalen, en hoe het kaart-framework in elkaar zit.

---

## 1. Het origineel: *Horrible Couple* (The Oatmeal × Exploding Kittens)

Geverifieerde mechaniek:

- Drie decks: **Question** (57), **Response** (166), **Compromise** (215). Hand = **5 Compromise**.
- Elke ronde wordt een **strip van 3 panelen** gebouwd: Question → Response → Compromise.
- **Couple mode (coöperatief):** Vraag open → 3 Responses trekken, 1 kiezen → kies 1 Compromise
  uit je hand + 2 willekeurige, schud, partner **raadt welke van jou was**. Goed = punt + reeks
  (Love-O-Meter); fout = reeks naar 0.
- **Party mode (competitief):** Vraag + Response → iedereen legt grappigste Compromise in → jury
  kiest de meest belachelijke. **Eerste bij 3 punten** (of "het koppel dat nog steeds praat") wint.

Bronnen: explodingkittens.com (product) · officialgamerules.org — *Horrible Couple*.

## 2. Waarom dit perfect bij KUD past

KUD's bekendste personages, **Die Groene & Die Roze**, vormen een vast **duo** — letterlijk
"het stel". Een relatie-stripspel rond hen is dus geen geforceerde reskin maar een natuurlijke
match. De humor van KUD (nuchtere opzet → absurde wending) sluit naadloos aan op de
Vraag→Reactie→Compromis-structuur: de Compromis-kaart levert de absurde wending.

Bovendien is KUD **animatie** = beeld; een paneel-stripspel laat elk paneel een KUD-still zijn.
De coöperatieve "raad je partner"-modus voegt iets toe dat *De Waardeloze Therapeut* (ons andere
KUD-spel) niet heeft: het gaat niet alleen om grappig zijn, maar om elkáár kennen.

## 3. Vertaaltabel

| Horrible Couple | KUD: Verschrikkelijk Stel | Paneel | Drager |
|-----------------|---------------------------|--------|--------|
| Question | **Vraag** — het relatieprobleem van Groen & Roze | 1 | **beeld** (still van het stel) + tekst |
| Response (3 trekken, 1 kiezen) | **Reactie** — de tegenreactie | 2 | tekst |
| Compromise (hand van 5) | **Compromis** — KUD-fragment als oplossing | 3 | **beeld** (still) + bijschrift |
| Couple mode + Love-O-Meter | **Stelmodus** + **Liefdes-O-Meter** | — | — |
| Party mode | **Feestmodus** | — | — |
| First to 3 points | Eerste bij **3 punten** | — | — |

Ontwerpkeuze: **paneel 1 en 3 zijn beeldkaarten** (art-focus), **paneel 2 is tekst**. De
Compromis-handkaarten zijn beeld → het "raad welke van je partner was" is daardoor lekker visueel.

Conform jouw wens: **puur kaarten spelen** — geen tekenen, geen schrijven.

## 4. Thema-mechanieken (meer dan een reskin)

Zie `SPELREGELS.md` + `speciale-kaarten.csv`. Highlights: **Zwoele Man** (bonus op de
Liefdes-O-Meter), **De Bonk / Supermegaberenbonken** (all-in op je reeks — uniek voor de
coöp-modus), **Djingle Djengle** (zingen redt je reeks), **25 seconden lang** (tijdsdruk),
**Konijntje**, **pilon**, en het geverifieerde Peter Lub-citaat *"Ik snap het zelf ook niet
helemaal"* als joker.

## 5. Het kaart-framework (technisch)

Identiek opgezet aan ons andere KUD-spel: **data-gedreven en uitbreidbaar**.

```
kud-verschrikkelijk-stel/
├── docs/            spelregels, dit ontwerp, credits
├── framework/
│   ├── kaart-schema.md       het datamodel (kolommen + regels)
│   ├── data/                 vragen.csv · reacties.csv · compromissen.csv · speciale-kaarten.csv
│   └── generate_cards.py     CSV + assets -> print/print.html  (alleen Python-stdlib)
└── print/
    ├── assets/      jouw KUD-stills (.png/.jpg); bestandsnaam = kolom `fragment`
    └── print.html   gegenereerd, print-klaar (A4, 63×88 mm, 3×3)
```

**Eigen fragmenten toevoegen:** afbeelding in `print/assets/` zetten → regel met `fragment=...`
in de juiste CSV → `python3 framework/generate_cards.py` → `print/print.html` printen. Kaarten
zonder afbeelding krijgen automatisch een **placeholder** met de gewenste naam, zodat je nu al
kunt testspelen en precies weet welke art je nog nodig hebt.

> De geverifieerde KUD-content (personages, video-/liedtitels, échte citaten, met bronnen) staat
> in het zusterproject: `../kud-therapie/content/kud-fragmenten-catalogus.md`.

## 6. Juridisch / scope

Privé thuisspel, geen verkoop/distributie. Mechaniek-inspiratie: *Horrible Couple* (The Oatmeal ×
Exploding Kittens). KUD-IP © Peter Lub, gebruikt met toestemming. Zie `CREDITS.md`.
