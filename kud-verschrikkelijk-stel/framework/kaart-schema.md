# Kaart-schema (datamodel)

Alle kaartinhoud staat in CSV-bestanden in `data/`. De generator (`generate_cards.py`) leest deze
en maakt `print/print.html`. UTF-8, komma-gescheiden, eerste regel = kopregel.

## Kolommen

| Kolom | Verplicht | Omschrijving |
|-------|-----------|--------------|
| `id` | ✅ | Unieke code, bv. `VRA-001`, `REA-014`, `COM-032`, `SPC-003`. |
| `type` | ✅ | `vraag` \| `reactie` \| `compromis` \| `speciaal`. |
| `bijschrift` | ✅ | De tekst op de kaart. Bij `vraag` = het dilemma; bij `reactie` = de reactie-regel; bij `compromis` = de oplossing-punchline; bij `speciaal` = de titel. |
| `fragment` | beeldkaarten | Bestandsnaam in `../print/assets/` (bv. `konijntje.png`). Leeg = placeholder. Gebruikt bij `vraag`, `compromis`, `speciaal`. |
| `bron` | aanbevolen | Welke KUD-video/personage het fragment is. |
| `zekerheid` | aanbevolen | `geverifieerd` \| `onzeker` \| `origineel`. |
| `score` | optioneel | Grappigheids-rubricscore 0–25 (zie `../../kud-therapie/content/grappigheid-analyse.md`). ≥18 → gouden rand. |
| `effect` | alleen `speciaal` | De spelregel-tekst van de speciale kaart. |
| `notitie` | optioneel | Ontwerpnotitie, komt niet op de kaart. |

## Per type

- **`vraag`** (paneel 1): beeld van het stel (`fragment`) + dilemma (`bijschrift`). Wordt opengedraaid.
- **`reactie`** (paneel 2): alleen tekst (`bijschrift`). Inlegger/Jury trekt er 3, kiest 1.
- **`compromis`** (paneel 3, handkaart): KUD-fragment (`fragment`) + punchline (`bijschrift`).
- **`speciaal`**: heeft een `effect`; beeld optioneel. Houd er weinig (±10% van de compromis-stapel).

## Conventies

- `bijschrift` ≤ ±90 tekens zodat het op de kaart past.
- Geen verbatim in-video quotes tenzij geverifieerd; markeer met `zekerheid`.
- Eén regel = één kaart. Dezelfde kaart dubbel? Zet de regel twee keer neer.

## Voorbeeldregel

```csv
id,type,bijschrift,fragment,bron,zekerheid,score,effect,notitie
COM-001,compromis,"We nemen gewoon een konijntje. Konijntjes lossen alles op.",konijntje.png,"Konijntje (Aka The Junkies)",geverifieerd,22,,"Sterke universele punchline"
```
