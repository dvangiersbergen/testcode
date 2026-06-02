# KUD: De Waardeloze Therapeut 🛋️

Een **absurdistisch therapie-stripspel** met **KUD**-fragmenten — een onofficieel fan-kaartspel
voor thuis, in het Nederlands. Geïnspireerd op *Horrible Therapist* (Exploding Kittens), maar
volledig omgebouwd rond de stijl en personages van **KUD** (Peter Lub, Enkhuizen).

> **Onofficieel · privégebruik · art met toestemming.** Spelmechaniek-inspiratie: *Horrible
> Therapist* © Exploding Kittens. Alle KUD-beelden © Peter Lub / KUD, te gebruiken **met
> toestemming van de maker**. Zie [`docs/CREDITS.md`](docs/CREDITS.md).

---

## Het spel in één plaatje

Iedere ronde bouw je een **KUD-strip van 3 panelen**:

> **PATIËNT** (welk KUD-figuur ligt op de bank) **+ KLACHT** (welk absurd probleem)
> **+ BEHANDELING** (jouw KUD-fragment als waardeloze therapie)

De **Therapeut** van de ronde bouwt paneel 1+2 en kiest welke ingelegde Behandeling het
grappigst is. Eerste met **3 Diploma's** wint en is **Hoofdtherapeut**.

Volledige regels: [`docs/SPELREGELS.md`](docs/SPELREGELS.md)

---

## Snel starten (print & play)

```bash
cd framework
python3 generate_cards.py        # bouwt ../print/print.html
```

Open daarna `print/print.html` in je browser en print op A4 (schaal 100%). Zónder eigen art
krijg je nette **placeholders** met de naam van het benodigde fragment — je kunt dus meteen
testspelen. Voeg echte KUD-stills toe in [`print/assets/`](print/assets/) en draai opnieuw.

De startset bevat **128 kaarten**: 18 Patiënt · 40 Klacht · 60 Behandeling · 10 Speciaal.

---

## Mappenstructuur

| Pad | Wat |
|-----|-----|
| [`docs/SPELREGELS.md`](docs/SPELREGELS.md) | Speelbare regels (NL) |
| [`docs/SPELONTWERP.md`](docs/SPELONTWERP.md) | Ontwerp + vertaling van *Horrible Therapist* naar KUD |
| [`docs/CREDITS.md`](docs/CREDITS.md) | Credits, bronnen & licentie/toestemming |
| [`content/kud-fragmenten-catalogus.md`](content/kud-fragmenten-catalogus.md) | Geverifieerde KUD-personages, video's, citaten (met bronnen) |
| [`content/grappigheid-analyse.md`](content/grappigheid-analyse.md) | Grappigheids-rubric: welke fragmenten worden kaarten |
| [`framework/kaart-schema.md`](framework/kaart-schema.md) | Datamodel van de kaarten |
| [`framework/data/*.csv`](framework/data/) | De kaartinhoud (uitbreidbaar) |
| [`framework/generate_cards.py`](framework/generate_cards.py) | CSV + art → print-klaar HTML |
| [`print/assets/`](print/assets/) | Jouw KUD-stills (bestandsnaam = `fragment`) |
| `print/print.html` | Gegenereerd printvel |

---

## Zelf kaarten toevoegen

1. Voeg een regel toe aan het juiste CSV-bestand in `framework/data/` (zie
   [`framework/kaart-schema.md`](framework/kaart-schema.md)).
2. (Optioneel) Zet de bijbehorende afbeelding in `print/assets/` met exact de bestandsnaam uit
   de kolom `fragment`.
3. Draai `python3 framework/generate_cards.py` en print opnieuw.

---

## Eerlijkheid over de inhoud

- ✅ **Geverifieerde** KUD-feiten (personages, video-/liedtitels, prijzen, échte Peter Lub-citaten)
  staan met bron in [`content/kud-fragmenten-catalogus.md`](content/kud-fragmenten-catalogus.md).
- ✏️ De meeste **kaartteksten zijn origineel in KUD-stijl geschreven** — géén verzonnen verbatim
  quotes. Vervang ze gerust door echte fragmentregels (kolom `zekerheid` houdt dit bij).
- De geautomatiseerde scrape van álle video's + Reddit/YouTube-comments kon hier niet volledig
  draaien (rate limits); daarom levert dit project een **rubric + invul-sjabloon** om fragmenten
  objectief te scoren, in plaats van verzonnen cijfers.
