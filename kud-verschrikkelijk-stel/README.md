# KUD: Verschrikkelijk Stel 💚💗

Een **3-panel relatie-stripspel** met **Die Groene & Die Roze** — KUD's beroemdste (en meest
verschrikkelijke) koppel. Onofficieel fan-kaartspel voor thuis, in het Nederlands. Geïnspireerd op
**Horrible Couple** (The Oatmeal × Exploding Kittens), volledig omgebouwd rond **KUD** (Peter Lub).

> **Onofficieel · privégebruik · art met toestemming.** Mechaniek-inspiratie: *Horrible Couple*
> © The Oatmeal × Exploding Kittens. Alle KUD-beelden © Peter Lub / KUD, te gebruiken **met
> toestemming van de maker**. Zie [`docs/CREDITS.md`](docs/CREDITS.md).

---

## Het spel in één plaatje

Iedere ronde bouw je een **strip van 3 panelen**:

> **VRAAG** (het relatieprobleem van Groen & Roze) **+ REACTIE** (de tegenreactie)
> **+ COMPROMIS** (jouw KUD-fragment als absurde oplossing)

Twee manieren om te spelen:
- 💞 **Stelmodus (coöperatief):** raad welk Compromis van je partner kwam → klim op de **Liefdes-O-Meter**.
- 🎉 **Feestmodus (competitief):** jury kiest het grappigste Compromis → eerste bij **3 punten** wint.

**Puur kaarten spelen — geen tekenen of schrijven.** Volledige regels: [`docs/SPELREGELS.md`](docs/SPELREGELS.md)

---

## Snel starten (print & play)

```bash
cd framework
python3 generate_cards.py        # bouwt ../print/print.html
```

Open `print/print.html` en print op A4 (schaal 100%). Zónder eigen art krijg je nette
**placeholders** met de naam van het benodigde fragment — je kunt dus meteen testspelen. Voeg
echte KUD-stills toe in [`print/assets/`](print/assets/) en draai opnieuw.

De startset bevat **135 kaarten**: 25 Vraag · 40 Reactie · 60 Compromis · 10 Speciaal.

---

## Mappenstructuur

| Pad | Wat |
|-----|-----|
| [`docs/SPELREGELS.md`](docs/SPELREGELS.md) | Speelbare regels (NL) — beide modi |
| [`docs/SPELONTWERP.md`](docs/SPELONTWERP.md) | Ontwerp + vertaling van *Horrible Couple* naar KUD |
| [`docs/CREDITS.md`](docs/CREDITS.md) | Credits, bronnen & toestemming |
| [`framework/kaart-schema.md`](framework/kaart-schema.md) | Datamodel van de kaarten |
| [`framework/data/*.csv`](framework/data/) | De kaartinhoud (uitbreidbaar) |
| [`framework/generate_cards.py`](framework/generate_cards.py) | CSV + art → print-klaar HTML |
| [`print/assets/`](print/assets/) | Jouw KUD-stills (bestandsnaam = `fragment`) |
| `print/print.html` | Gegenereerd printvel |

> **Zusterproject:** [`../kud-therapie/`](../kud-therapie/) — *KUD: De Waardeloze Therapeut*
> (naar *Horrible Therapist*). Daar staat ook de geverifieerde KUD-fragmentencatalogus + de
> grappigheids-rubric die je hier kunt hergebruiken.

---

## Eerlijkheid over de inhoud
- ✅ Geverifieerde KUD-feiten/citaten zijn gemarkeerd (`zekerheid=geverifieerd`), met bron in de
  catalogus van het zusterproject.
- ✏️ De meeste kaartteksten zijn **origineel in KUD-stijl** geschreven — géén verzonnen quotes.
  Vervang ze gerust door echte fragmentregels.
