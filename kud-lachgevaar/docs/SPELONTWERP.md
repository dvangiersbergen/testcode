# Spelontwerp — KUD: Lachgevaar

## Het origineel: Joking Hazard (Cyanide & Happiness / Explosm)
Geverifieerde kern:
- Eén homogene stapel **strip-panelen**; elke kaart kan paneel 1, 2 of 3 zijn.
- Iedere ronde maakt een **bouwer/rechter** het begin van een 3-panel-strip; de overige spelers
  vullen het laatste paneel aan met één handkaart. De bouwer kiest de grappigste.
- **Rode kaarten** mogen alleen als slotpaneel; valt er een rode bovenop als opener, dan leveren
  spelers twee kaarten in en is de ronde **2 punten** waard.
- **Blanco kaarten** om zelf te maken. Hand van **7**. Eerste bij **3 punten** wint.

Bronnen: jokinghazardgame.com · officialgamerules.org · ultraboardgames.com (Joking Hazard).

## Waarom dit goed bij KUD past
KUD is **visuele animatie**: korte, absurde sketches met een vast clubje personages. Joking Hazard
draait volledig op **beeld-juxtapositie** — precies waar KUD-frames sterk in zijn. Eén stapel
losse KUD-panelen die je in willekeurige vololgorde tot een strip kunt leggen, levert vanzelf de
typische KUD-wending op. Dit is bovendien mechanisch **anders** dan de andere twee KUD-spellen in
deze repo (die splitsen kaarten in vraag/reactie/etc.); hier is alles één uitwisselbare paneel-pot.

## Vertaaltabel
| Joking Hazard | KUD: Lachgevaar |
|---------------|-----------------|
| Comic panel cards | **Panelen** (KUD-frames, kolom `art`, evt. `tekst`) |
| Red (final-only) cards | **Rode slotpanelen** (`rood=1`, ★-badge) |
| Blank cards | **Blanco panelen** (`blanco=1`) |
| Judge builds panel 1+2 | **Bouwer** draait paneel 1, speelt paneel 2 |
| Players submit final panel | Spelers leveren paneel 3 in |
| Red opener → 2 cards, 2 points | Idem: paneel 1+2 inleveren, 2 punten |
| First to 3 points | Eerste bij **3 punten** |

## Ontwerpkeuzes
- **Vierkante kaarten** (62 mm): authentiek paneelformaat én ze leggen netjes naast elkaar tot een
  strip.
- **Beeld primair, tekst optioneel.** De generator toont een paneel met of zonder bijschrift; veel
  van de beste kaarten zijn woordloos.
- **Placeholders met scene-omschrijving:** zonder eigen art is het spel meteen testbaar, en je ziet
  exact welk KUD-fragment elke kaart nodig heeft → directe verzamel-checklist.
- **Data-gedreven:** één CSV (`panels.csv`) + een pure-stdlib generator. Uitbreiden = regels
  toevoegen en een afbeelding in `assets/` zetten.

## Het framework
```
kud-lachgevaar/
├── docs/           spelregels · art-en-tekst-verzamelen · dit ontwerp · credits
├── framework/
│   ├── kaart-schema.md
│   ├── data/panels.csv        de panelen (uitbreidbaar)
│   └── generate_cards.py      CSV + assets -> print/print.html
└── print/
    ├── assets/     jouw vierkante KUD-frames (bestandsnaam = kolom `art`)
    └── print.html  gegenereerd, print-klaar (A4, 62×62 mm, 3×4)
```

## Scope
Privé fan-prototype, niet voor verkoop/distributie. Mechaniek-inspiratie: *Joking Hazard*
(Explosm). KUD-IP © Peter Lub. Zie `CREDITS.md` en `ART-EN-TEKST-VERZAMELEN.md` (auteursrecht).
