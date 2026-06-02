# Kaart-schema (datamodel)

Alle kaartinhoud staat in CSV-bestanden in `data/`. De generator (`generate_cards.py`) leest deze
en maakt `print/print.html`. UTF-8, komma-gescheiden, eerste regel = kopregel.

## Gemeenschappelijke kolommen

| Kolom | Verplicht | Omschrijving |
|-------|-----------|--------------|
| `id` | ✅ | Unieke code, bv. `PAT-001`, `KLA-014`, `BEH-032`, `SPC-003`. |
| `type` | ✅ | `patient` \| `klacht` \| `behandeling` \| `speciaal`. |
| `bijschrift` | ✅ | De tekst op de kaart (Dutch). Kort houden. |
| `fragment` | beeldkaarten | Bestandsnaam in `../print/assets/` (bv. `konijntje.png`). Leeg = placeholder. |
| `bron` | aanbevolen | Welke KUD-video/personage het fragment is (voor jezelf + credits). |
| `zekerheid` | aanbevolen | `geverifieerd` \| `onzeker` \| `origineel`. Stuurt geen layout, puur administratie. |
| `score` | optioneel | Grappigheids-rubricscore 0–25 (zie `content/grappigheid-analyse.md`). ≥18 = "Gouden Diploma"-rand. |
| `effect` | alleen `speciaal` | De spelregel-tekst van de speciale kaart. |
| `notitie` | optioneel | Vrije ontwerpnotitie, komt niet op de kaart. |

## Per type

### `patient` (paneel 1, beeldkaart)
KUD-personage op de bank. `fragment` = personage-still. `bijschrift` = naam/korte intro.

### `klacht` (paneel 2, tekstkaart)
Het absurde probleem. Alleen `bijschrift` telt; `fragment` meestal leeg. Schrijf als
patiënt-uitspraak of korte situatie. Dit is ook het "Diploma"-puntbewijs.

### `behandeling` (paneel 3, beeldkaart — handkaarten)
KUD-fragment als therapie. `fragment` = still, `bijschrift` = de punchline-regel. Mik op
**combineerbare** beelden (zie grappigheids-rubric).

### `speciaal` (zit tussen de behandelingen)
Heeft een `effect`. Beeld optioneel. Houd er weinig (±10% van de behandelstapel).

## Regels & conventies

- Houd `bijschrift` ≤ ±90 tekens zodat het op de kaart past.
- Gebruik geen echte verbatim in-video quotes tenzij geverifieerd; markeer met `zekerheid`.
- Eén regel = één kaart. Voeg gerust honderden regels toe; de generator pagineert vanzelf.
- Wil je een kaart dubbel in het deck? Voeg de regel twee keer toe (of beheer aantallen later).

## Voorbeeldregel

```csv
id,type,bijschrift,fragment,bron,zekerheid,score,effect,notitie
BEH-007,behandeling,"Gewoon een konijntje. Probleem opgelost.",konijntje.png,"Konijntje (Aka The Junkies)",geverifieerd,22,,"Sterke universele punchline"
```
