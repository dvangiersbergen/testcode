# KUD: Doordraaien — beta-testrapport

_Synthese van 4 fan-beta-testers × 360 gesimuleerde 1-tegen-1 potjes (Kijkcijfers-modus)._
Bronnen: `../sim/results.md`, `../sim/sample_game.md`, de conceptkaarten in `../cards/`.

## De testers
| Tester | Leeftijd | Profiel | Speelstijl | Cijfer |
|---|---|---|---|---|
| **Sven** | 14 | KUD-jeugdfan, houdt van snelle chaos (Uno/Exploding Kittens) | chaos-dumpen, agressie | **7/10** |
| **Marit** | 17 | KUD-fan + bordspel-strateeg (Carcassonne/eurogames) | lange lijnen uitmelken | **5/10** |
| **Joost** | 22 | KUD-nostalgie, casual party-speler | op gevoel/thema | **6,5/10** |
| **Eline** | 16 | KUD-fan + competitieve TCG-speler (min-maxer) | tempo + denial | **5,5/10** |

**Gemiddeld: 6,0/10** — "sterk thema, mechanics nog niet in balans."

---

## Wat unaniem werkt ✅
1. **De KUD-art draagt het spel.** Alle vier reageren euforisch. Sven: _"die kaarten zien er STRAK uit… ik herkende meteen Te Laat en Fallout."_ Joost: _"zodra ik die kaarten zag was ik terug op de bank als dertienjarige… voelt als screenshots, niet als goedkope fanart."_ De aflevering-stills + kleurcodering = directe nostalgie-hit en de belangrijkste verkoopkracht.
2. **De ketting-mechaniek (beurt A) is verslavend.** Sven & Marit noemen het apart het beste onderdeel: doorbouwen zolang je poorten hebt geeft echte combo-/aha-momenten. Eline waardeert de tempo-keuze "nu stoppen of alles dumpen".
3. **Thema kleeft aan de mechaniek.** "Je zit écht een aflevering te monteren" (Joost). EINDE-kaarten als aftiteling voelen goed (Marit). REPRISE-lusbonus is "elegant, lage frequentie/hoge payoff" (Eline).
4. **Denial werkt thematisch.** CLIFFHANGER + bord-choke is volgens Eline "de beste interactie die het spel heeft".

---

## De kernkritiek 🔴 (sterk consensus-signaal)

### #1 — De finale-bonus is een tweede, dominant winstsysteem
**Het grootste probleem, onafhankelijk benoemd door Marit én Eline en bevestigd in de data.**
- **52% van alle potjes** wordt beslist door "hand leeg → +5", niet door kijkcijfers.
- Gevolg: **chaos-dumpen verslaat strategisch scoren.** Marit (wiens hele plan punten maken is) scoort het *laagst* (14,0 gem.) en wint het minst (23%); Sven dumpt sneller en wint het meest (26%).
- Het voorbeeldpotje is exemplarisch: **0–0 op kijkcijfers het hele potje**, daarna leegt Sven zijn hand en wint 5–0. Marit: _"je speelt het best scorende spel en verliest alsnog… strategie wordt niet beloond, snelheid wel."_

### #2 — Te swingy voor een competitief duel
- **31% blowouts** (margin ≥12), potjes van **3 tot 88 beurten**. Eline: _"een 3-beurt-potje is geen spel, dat is een opening-hand-loterij."_
- Oorzaak deels **KNIP**: +1 open poort explodeert het bord (sample: 2× KNIP vroeg → 8 open draden in ronde 8).

### #3 — Verstikking/trekstraf voelt als beurt-skip
- **8,4 trekstraf-beurten per speler per potje.** Sven: _"ACHT KOMMA VIER DRIE, dat is te veel."_ Joost: _"beurt-skip na beurt-skip, ik zat gewoon toe te kijken."_ Eline ziet een **RNG-snowball**: eenmaal op de verkeerde kleur droog = negatieve spiraal buiten je schuld.

### #4 — Te veel regels voor casual (toegankelijkheid)
- Joost (en deels Marit/Eline): **6 kaarttypes is te veel.** Vertakking vs. Samenkomst (+1/−1 poort) worden door elkaar gehaald; de kleurwissel-regel bij Splice is onduidelijk; actiekaarten lijken visueel te veel op splices.

---

## Usability / kaartdesign-nits (concreet)
- **Type-label te klein** bovenaan (Sven, Eline, Marit) — moet groot/dik.
- **Regeltekst onderaan onleesbaar** in spel (Sven) — vergroten.
- **Actiekaarten ander frame/achtergrond** geven, los van splices (Eline).
- **Pilon-wild duidelijker** markeren (Eline).
- **Vertakking/Samenkomst-iconen** groter en ondubbelzinnig (Marit, Joost).
- **Leader-tegel** voelt kaal (Sven).

---

## Voorgestelde wijzigingen → v0.4 (geprioriteerd)

| Prio | Wijziging | Lost op | Bron |
|---|---|---|---|
| **P0** | **Finale-bonus koppelen aan score:** vervang vaste +5 door **+lengte van je langste gesloten lijn** (min 2, max 6), óf +1 per kaart in de hand van de tegenstander. | #1 dominantie snelheid; maakt scoren competitief | Marit + Eline (beide!) |
| **P0** | **EINDE extra belonen bij lange lijnen:** +2 per scène boven lengte 4. | #1 uitmelken loont eindelijk | Marit |
| **P1** | **KNIP hard cappen:** max 2 open poorten per kleur op het bord; KNIP op een verzadigde kleur is ongeldig. | #2 swinginess/bord-explosie | Eline |
| **P1** | **Trekstraf 2 → 1 + weggooi-escape:** trek 1 en gooi 1 weg (netto neutraal) i.p.v. 2 trekken; of "tweede keer op rij vast = trek 1 en speel direct als het past". | #3 dooie beurten/snowball | Sven + Eline |
| **P2** | **Vertakking + Samenkomst samenvoegen** tot één kaart met keuzesymbool (splits OF voeg samen). | #4 regellast | Joost |
| **P2** | **Kaartlayout:** type-label + actie-frame + regeltekst groter/duidelijker. | usability | allen |

---

## Per-tester scorecard (kort)
- **Sven (7):** "vette kaarten, verslavende combo's, maar verstikking zuigt het tempo eruit — fix dat en het is een 9."
- **Joost (6,5):** "art en thema een dikke 9; regelcomplexiteit en trek-beurten trekken het omlaag voor casuals."
- **Eline (5,5):** "denial + tempo-kern is er, maar 31% blowouts en 52% finale-beslissingen bewijzen dat chaos/geluk nu meer loont dan skill."
- **Marit (5):** "twee spellen in één — de finale-bonus maakt de kijkcijfer-strategie irrelevant, en het verkeerde spel wint te vaak."

## Conclusie
Het **fundament is sterk**: het thema en de art zijn een schot in de roos en de ketting-/denial-kern is leuk. Het **scoringsmodel is de bottleneck** — de losstaande finale-bonus laat snelheid de strategie overrulen (P0). Los #1 op en dempt #2/#3, en het spel verschuift van "swingy dump-race" naar het bedoelde **duel om de open draden**. Aanrader: v0.4 bouwen met de P0+P1-wijzigingen en opnieuw 360 potjes draaien om te checken of Marit's gemiddelde stijgt en de blowout-rate daalt.
