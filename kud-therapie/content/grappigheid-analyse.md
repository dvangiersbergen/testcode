# Grappigheids-framework — welke KUD-fragmenten worden kaarten?

> Doel: een herhaalbare manier om te kiezen wélke KUD-fragmenten de beste **Behandeling**- en
> **Patiënt**-kaarten opleveren. Niet elk fragment is even speelbaar.

## Status van het onderzoek

De geautomatiseerde "scrape alle video's + analyseer Reddit/YouTube-comments"-stap kon in deze
omgeving niet volledig draaien (rate limits + KUD is video-content waarvan comments lastig
betrouwbaar te oogsten zijn). In plaats van verzonnen view-counts geven we hier een **rubric**
plus een **invul-sjabloon** waarmee jij (of een latere run) fragmenten objectief scoort. Harde
populariteitssignalen die wél bevestigd zijn staan in `kud-fragmenten-catalogus.md` (prijzen,
`Konijntje` als internethit, abonnee-/view-aantallen).

## De grappigheids-rubric (score 1–5 per as)

Scoor elk kandidaat-fragment op vijf assen. Tel op (max 25). ≥18 = topkaart.

| As | Vraag | 1 | 5 |
|----|-------|---|---|
| **Herkenbaarheid** | Kennen KUD-fans dit meteen? | obscuur | iconisch (bv. Konijntje) |
| **Losstaande leesbaarheid** | Werkt het fragment zónder de hele video? | nee | direct duidelijk |
| **Absurde lading** | Hoe raar/onverwacht is het beeld? | gewoon | volkomen K-U-D |
| **Combineerbaarheid** | Past het op veel verschillende klachten? | alleen 1 situatie | universele punchline |
| **Plaatje-kracht (art)** | Is de still op zichzelf grappig/sterk? | flets | screenshot-waardig |

> **Combineerbaarheid** is het belangrijkst voor een goede Behandeling-kaart: de grap ontstaat
> uit de botsing tussen klacht (panel 2) en jouw fragment (panel 3). Universele, "lege" maar
> sterke beelden winnen vaker.

## Voorlopige prioriteitenlijst (op basis van bevestigde signalen)

Gebruik dit als startpunt; herijk zodra je echte view-/like-data van de maker krijgt.

| Prioriteit | Fragment/bron | Waarom | Zekerheid |
|-----------|---------------|--------|-----------|
| ⭐⭐⭐ | **Konijntje** (ft. Aka The Junkies) | bevestigde internethit, breed bekend | hoog |
| ⭐⭐⭐ | **Zwoele Man** | terugkerend, sterk personage, eigen short | hoog |
| ⭐⭐⭐ | **pilon** | absurde in-joke, universeel inzetbaar | midden |
| ⭐⭐ | UPC-winnaars 2011/2012/2013 (titels achterhalen) | publieksprijs = bewezen grappig | midden |
| ⭐⭐ | Djingle Djengle-toppers (`Trampoline`, `De Vliegende Koe`, `Supermegaberenbonken`) | sterke, beeldende titels | midden |
| ⭐⭐ | **Wiebe (drank)** | bekend personage-moment | midden |
| ⭐ | overige Djingle Djengle + losse nummers | vullen de deck aan | laag |

## Invul-sjabloon (vul aan met echte data)

Kopieer per fragment. Zet de eindscore in `behandelingen.csv` kolom `score` zodat de generator
de sterkste kaarten als "Gouden Diploma"-variant kan markeren.

```
Fragment:            <titel / video + tijdstip>
Bron-URL:            <youtube-link>
Views / likes:       <indien bekend>
Herkenbaarheid:      _/5
Losstaande leesb.:   _/5
Absurde lading:      _/5
Combineerbaarheid:   _/5
Plaatje-kracht:      _/5
TOTAAL:              __/25
Beste klacht-match:  <waar botst dit het hardst mee?>
```

## Hoe je dit later automatiseert

Wanneer rate limits het toelaten, kun je per video ophalen: titel, view-count, like-ratio en de
top-comments. Tel hoe vaak een regel letterlijk in comments wordt geciteerd (sterk
grappigheidssignaal) en voer de rubric-score in. Houd je aan: **geen verzonnen cijfers** — leeg
laten als onbekend.
