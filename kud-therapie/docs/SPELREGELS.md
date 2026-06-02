# KUD: De Waardeloze Therapeut — Spelregels

*Het absurdistische therapie-stripspel met KUD-fragmenten.*

> Een onofficieel fan-kaartspel voor thuis. Spelmechaniek geïnspireerd op
> *Horrible Therapist* (Exploding Kittens). Alle KUD-personages en -beelden zijn
> © Peter Lub / KUD en worden gebruikt **met toestemming van de maker**, uitsluitend
> voor privégebruik. Zie `../docs/CREDITS.md`.

---

## Het idee

Iedere ronde ontstaat er een **KUD-strip van 3 panelen**:

```
┌───────────┐   ┌───────────┐   ┌───────────┐
│  PANEEL 1 │   │  PANEEL 2 │   │  PANEEL 3 │
│  PATIËNT  │ + │  KLACHT   │ + │BEHANDELING│
│ (KUD-fig) │   │ (probleem)│   │(KUD-frag) │
└───────────┘   └───────────┘   └───────────┘
   wie ligt        wat is        jouw waardeloze
  er op de bank?  het probleem?     therapie
```

De **Therapeut** van die ronde bouwt paneel 1 + 2 (de patiënt en zijn klacht).
Alle andere spelers leggen in het geheim paneel 3 bij: hun grappigste/meest
gestoorde **Behandeling**. De Therapeut kiest welke strip de beste is. Die speler
verdient een **Diploma**.

**Doel:** als eerste **3 Diploma's** halen en je uitroepen tot **Hoofdtherapeut van Enkhuizen**.

---

## Wat zit erin

- **Patiënt-kaarten** (paneel 1) — een KUD-personage op de bank (beeldkaart).
- **Klacht-kaarten** (paneel 2) — een absurd probleem (tekst).
- **Behandeling-kaarten** (paneel 3) — een KUD-fragment als therapie (beeldkaart, jouw handkaarten).
- **Speciale kaarten** — KUD-thema-kaarten met een eigen regeltje (zie onderaan).

> Aantallen zijn vrij: de meegeleverde startset is uitbreidbaar via de CSV-bestanden in
> `../framework/data/`. Aanrader om te beginnen: ±20 Patiënt, ±40 Klacht, ±60 Behandeling.

**Spelers:** 3–8 · **Leeftijd:** 16+ (volwassen humor) · **Duur:** 20–40 min.

---

## Voorbereiding

1. Sorteer de kaarten in drie stapels: **Patiënt**, **Klacht**, **Behandeling**.
   Schud elke stapel apart en leg ze gedekt in het midden.
2. Meng de **Speciale kaarten** door de Behandeling-stapel (optioneel — zie variant).
3. Iedere speler trekt **5 Behandeling-kaarten** als handkaarten. Niet laten zien.
4. Kies wie als eerste **Therapeut** is. (Tip: wie het laatst bij een echte therapeut zat.)

---

## Een ronde, stap voor stap

De ronde-Therapeut speelt zelf **geen** Behandeling; hij bouwt de strip en jureert.

1. **Paneel 1 — Patiënt.** De Therapeut draait de bovenste **Patiënt**-kaart open en
   legt die zichtbaar neer. *Dit is wie er vandaag op de bank ligt.*
2. **Paneel 2 — Klacht.** De Therapeut trekt **3 Klacht-kaarten**, kiest in het geheim de
   leukste, en legt die naast de Patiënt. De andere 2 gaan op de aflegstapel.
   *Nu staat de opzet vast: deze patiënt, dit probleem.*
3. **Paneel 3 — Behandeling.** Alle andere spelers kiezen **1 Behandeling-kaart** uit hun hand
   die de grappigste/wreedste/meest KUD-waardige "therapie" vormt, en leggen die **gedekt** in.
4. **Onthullen.** De Therapeut schudt de ingelegde kaarten, draait ze één voor één om en leest
   elke complete 3-panel-strip hardop en dramatisch voor (in dokterstem).
5. **Oordeel.** De Therapeut kiest de strip die hem het hardst liet lachen. De maker daarvan
   wint de ronde en pakt de **Klacht-kaart** als **Diploma** (puntbewijs).
6. **Bijtrekken.** Iedereen vult zijn hand weer aan tot 5 Behandeling-kaarten.
7. **Doorgeven.** De rol van Therapeut gaat één plek met de klok mee. Nieuwe ronde.

---

## Winnen

De eerste speler met **3 Diploma's** wint en is **Hoofdtherapeut**.

- **Korter potje:** speel tot 2 Diploma's.
- **Langer potje:** speel tot 5 Diploma's.
- **Festival-variant:** speel een vast aantal rondes (bv. 2× het aantal spelers); meeste
  Diploma's wint.

---

## Speciale kaarten (KUD-thema)

Deze kaarten zitten tussen de Behandeling-kaarten en geven extra KUD-chaos. Volledige lijst en
exacte teksten in `../framework/data/speciale-kaarten.csv`.

| Kaart | Effect (korte versie) |
|-------|-----------------------|
| **Zwoele Man** | Speel als Behandeling. Wint deze strip? Dan krijg je er een **2e Diploma** bij — extra zwoel. |
| **Te laat** | Speel ná het onthullen: ruil je ingelegde Behandeling alsnog om voor een nieuwe handkaart. |
| **Djingle Djengle** | Je moet je bijschrift **zingen**. Lacht de Therapeut? Dan ligt jouw strip bovenaan de stapel. |
| **"Ik snap het zelf ook niet helemaal"** | Plak deze bij je Behandeling: maak elke therapie nóg absurder (geldt als joker-bijschrift). |
| **pilon** | Leg een pilon als behandeling. Pure onzin. De Therapeut mág hem niet negeren. |
| **Nieuw! / Plot Twist** | Vervang midden in de ronde de Patiënt door de volgende Patiënt-kaart. |

> Special-kaarten zijn optioneel. Laat ze weg voor een strakker, sneller basisspel.

---

## Varianten

- **Anoniem te werk** *(ode aan Peter Lub).* De Therapeut weet niet wie welke kaart inlegde
  (standaard al zo door te schudden) — speel bewust met pokerface, geen reacties tijdens het lezen.
- **Dubbele dosis.** Spelers leggen 2 Behandeling-kaarten in als één combostrip (paneel 3a + 3b).
- **Rebound.** De winnaar van de ronde wordt de volgende Therapeut (i.p.v. met de klok mee).
- **Eigen fragmenten.** Print blanco kaarten en plak je eigen favoriete KUD-still erop. Zie
  `../docs/SPELONTWERP.md` en de generator in `../framework/`.

Veel plezier. En onthoud: *je hoeft het zelf ook niet helemaal te snappen.*
