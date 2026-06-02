# KUD: Verschrikkelijk Stel — Spelregels

*Het 3-panel relatie-stripspel met Die Groene & Die Roze.*

> Onofficieel fan-kaartspel voor thuis. Spelmechaniek geïnspireerd op **Horrible Couple**
> (The Oatmeal × Exploding Kittens). Alle KUD-personages en -beelden © Peter Lub / KUD,
> gebruikt **met toestemming van de maker**, uitsluitend voor privégebruik. Zie `CREDITS.md`.

---

## Het idee

KUD's beroemdste stel — **Die Groene & Die Roze** — heeft een relatie vol absurde problemen.
Iedere ronde bouw je een **strip van 3 panelen**:

```
┌───────────┐   ┌───────────┐   ┌───────────┐
│  PANEEL 1 │   │  PANEEL 2 │   │  PANEEL 3 │
│   VRAAG   │ + │  REACTIE  │ + │ COMPROMIS │
│(het probl.)│  │ (de tegen-│   │(KUD-frag- │
│            │  │  reactie) │   │ ment: de  │
│            │  │           │   │ oplossing)│
└───────────┘   └───────────┘   └───────────┘
```

Er zijn **twee manieren** om te spelen:

- 💞 **Stelmodus (coöperatief)** — speel als koppel: raad welk Compromis van je partner kwam.
  Hoe langer je reeks goed, hoe hoger de **Liefdes-O-Meter**.
- 🎉 **Feestmodus (competitief)** — iedereen legt zijn grappigste Compromis in; een jury kiest
  de meest belachelijke. Eerste met **3 punten** wint.

---

## Wat zit erin

- **Vraag-kaarten** (paneel 1) — het relatieprobleem (beeld van het stel + tekst).
- **Reactie-kaarten** (paneel 2) — hoe de partner reageert (tekst).
- **Compromis-kaarten** (paneel 3) — een KUD-fragment als absurde oplossing (jouw handkaarten, beeld).
- **Speciale kaarten** — KUD-thema-kaarten met een eigen regeltje.

**Startset:** 25 Vraag · 40 Reactie · 60 Compromis · 10 Speciaal (uitbreidbaar via de CSV's).
**Spelers:** 2–8 · **Leeftijd:** 16+ · **Duur:** ±15–30 min.

---

## Voorbereiding (beide modi)

1. Sorteer in drie stapels: **Vraag**, **Reactie**, **Compromis**. Schud apart, leg gedekt neer.
2. Meng de **Speciale kaarten** door de Compromis-stapel (optioneel).
3. Iedere speler trekt **5 Compromis-kaarten** als hand. Niet laten zien.
4. Kies een startspeler.

---

## 💞 Stelmodus (coöperatief — voor 1 of meer koppels)

Doel: samen de langste reeks goede gokken halen → zo hoog mogelijk op de **Liefdes-O-Meter**.

Eén speler is per ronde de **Inlegger**, zijn partner is de **Rader**.

1. **Vraag.** De Inlegger draait de bovenste **Vraag**-kaart open (paneel 1).
2. **Reactie.** De Inlegger trekt **3 Reactie-kaarten**, kiest er 1 die het beste/grappigste past,
   legt die naast de Vraag (paneel 2). De andere 2 gaan weg.
3. **Compromis kiezen.** De Inlegger kiest **1 Compromis uit zijn hand** (de oplossing die híj
   zou kiezen), trekt er **2 willekeurige** Compromis-kaarten bij, schudt deze **3** gedekt door
   elkaar en geeft ze aan de Rader.
4. **Raden.** De Rader draait de 3 om, leest elke complete strip hardop voor, en raadt **welk
   Compromis écht uit de hand van de Inlegger kwam**.
5. **Score.**
   - **Goed geraden:** jullie scoren samen **1 punt** en houden die kaart zichtbaar als bewijs.
     Je reeks (streak) groeit → schuif 1 omhoog op de Liefdes-O-Meter.
   - **Fout:** de reeks valt terug naar **0**. (Geen ramp — Die Groene & Die Roze maken het ook
     altijd weer goed.)
6. **Bijtrekken** tot 5 en **rollen wisselen**: de Rader wordt Inlegger, of geef door aan het
   volgende koppel.

**Liefdes-O-Meter (richtlijn voor de hoogste reeks):**
`0–2` Knipperende relatie · `3–4` Stabiel instabiel · `5–6` Zwoel verliefd ·
`7+` **Onverwoestbaar K-u-d-koppel** 🏆

---

## 🎉 Feestmodus (competitief — 3–8 spelers)

Eén speler is per ronde de **Jury** (rouleert met de klok mee). De Jury legt zelf geen Compromis in.

1. **Vraag.** De Jury draait een **Vraag**-kaart open.
2. **Reactie.** De Jury trekt **3 Reactie-kaarten**, kiest de leukste en legt die erbij.
3. **Compromis.** Alle andere spelers leggen **gedekt 1 Compromis** uit hun hand in.
4. **Onthullen.** De Jury schudt de inzendingen, draait ze om en leest elke 3-panel-strip
   dramatisch voor.
5. **Oordeel.** De Jury kiest de meest belachelijke/grappigste strip. Die speler krijgt **1 punt**
   (houd de gewonnen Vraag-kaart als puntbewijs).
6. **Bijtrekken** tot 5, **Jury** schuift door.

**Winnen:** eerste met **3 punten** is **Hoofd-relatietherapeut van Enkhuizen**.
*(Of, in echte Horrible-Couple-stijl: het koppel dat aan het eind nog steeds met elkaar praat.)*

---

## Speciale kaarten (KUD-thema)

Zitten tussen de Compromis-kaarten; werken in beide modi. Volledige teksten in
`../framework/data/speciale-kaarten.csv`.

| Kaart | Kort effect |
|-------|-------------|
| **Zwoele Man** | Wint/wordt geraden? +1 extra op de Liefdes-O-Meter. |
| **Te laat** | Ruil na het onthullen je Compromis alsnog om. |
| **Djingle Djengle** | Zing je Compromis; lukt het, dan blijft je reeks staan bij een misser. |
| **Ik snap het zelf ook niet helemaal** | Joker-Compromis; partner mag in Stelmodus één keer hergokken. |
| **pilon** | Pure onzin-Compromis die de jury niet mag negeren. |
| **Konijntje** | Zó schattig dat er eerst hardop "awww" geroepen moet worden. |
| **De Bonk** | Stelmodus all-in: dubbele punten of reeks naar nul. |
| **Anoniem te werk** | Jury stemt blind; winnaar onthult zich daarna. |
| **25 seconden lang** | Beoordelaar heeft 25 sec; te laat = inlegger scoort. |
| **Nieuw! (Plot Twist)** | Vervang de Vraag-kaart; iedereen mag zijn Compromis wisselen. |

---

## Varianten

- **Dubbele dosis.** Leg 2 Compromis-kaarten in als combostrip (paneel 3a + 3b).
- **Koppels-toernooi.** Meerdere koppels spelen Stelmodus om de hoogste Liefdes-O-Meter.
- **Gemengd.** Speel Feestmodus, maar de Jury is telkens iemands partner — extra gênant.
- **Eigen fragmenten.** Plak je eigen KUD-stills op blanco Compromis-kaarten (zie de generator).

Veel plezier. En onthoud: een goed compromis snap je zelf ook niet helemaal.
