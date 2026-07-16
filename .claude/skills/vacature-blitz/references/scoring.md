# Radar-score specificatie (0–100)

De reactiveringsscore rangschikt kandidaten uit de eigen database op de kans
dat proactieve benadering NU tot een plaatsing leidt. De score is bewust
**uitlegbaar**: elke component wordt met puntentelling aan de intercedent
getoond, zodat die kan afwijken op basis van eigen kennis.

## Componenten

### 1. Timing — dagen sinds laatste contact (0–30)

| Dagen sinds laatste contact | Punten | Redenering                                  |
|-----------------------------|--------|----------------------------------------------|
| < 21                        | 5      | Net gesproken; situatie zelden veranderd     |
| 21–60                       | 18     | Warm, maar mogelijk nog in zelfde situatie   |
| 61–270                      | 30     | **Sweet spot**: situatie kan veranderd zijn, bureau nog bekend |
| 271–420                     | 20     | Koeler; heractivatie kost meer               |
| > 420                       | 10     | Koud, maar niet kansloos                     |

### 2. Historie — eerdere plaatsingen via het bureau (0–25)

`min(25, plaatsingen × 6)`. Eerdere succesvolle plaatsingen voorspellen
plaatsbaarheid én vertrouwen in het bureau.

### 3. Vraag — skills-match met NU openstaande vacature(s) (0–30)

`12 + (overlappende skills × 9)`, gemaximeerd op 30; 0 als geen enkele open
vacature past. Kern van het model: **bellen met een concrete baan converteert,
bellen "om bij te praten" niet.** De best passende vacature wordt de belreden.

### 4. Beschikbaarheid (0–15)

| Beschikbaarheid       | Punten |
|-----------------------|--------|
| direct                | 15     |
| overige (datum, deeltijd, weekend) | 10 |
| in overleg            | 8      |

## Interpretatie

| Score  | Actie                                                     |
|--------|-----------------------------------------------------------|
| ≥ 70   | Vandaag bellen, top van de bellijst                        |
| 45–69  | Deze week bellen of WhatsApp-eerst                         |
| < 45   | Alleen benaderen bij schaarse skills of talentpool-onderhoud |

## Matching-lagen per vacature

- **Directe match**: skills-overlap ≥ 2 (of alle gevraagde skills als de
  vacature er minder dan 2 heeft).
- **Opleidbare match** (alleen bij `opleidbaar: true`): overlap ≥ 1 én
  kandidaat is leerbereid; of overlap 0 maar leerbereid én direct beschikbaar
  (de "brede vijver" — laag gerangschikt maar zichtbaar).

## Wat NOOIT meeweegt

Leeftijd, afkomst, geslacht, religie, gezondheid, nationaliteit of daarvan
afgeleide proxies (bijv. naam, woonwijk als etnisch signaal). Reisafstand mag
alleen als praktische factor (woonplaats ↔ werklocatie), nooit als proxy.
