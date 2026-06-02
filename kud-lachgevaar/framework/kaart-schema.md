# Kaart-schema (datamodel)

Eén bestand stuurt het spel aan: `data/panels.csv`. UTF-8, komma-gescheiden, eerste regel = kopregel.
Elke regel is één **paneel** (een kaart). De generator (`generate_cards.py`) maakt `../print/print.html`.

## Kolommen
| Kolom | Verplicht | Omschrijving |
|-------|-----------|--------------|
| `id` | ✅ | Unieke code, bv. `PAN-001`, `RED-003`, `BLK-002`. |
| `scene` | aanbevolen | Korte omschrijving van het KUD-beeld. Dient als **placeholder-tekst** én als jouw verzamel-checklist: wat moet er op dit paneel staan. |
| `tekst` | optioneel | Bijschrift dat op de kaart komt. **Leeg = woordloos paneel** (vaak het sterkst). |
| `rood` | optioneel | `1` = rood **slotpaneel** (alleen als laatste paneel speelbaar; krijgt ★-badge en rode rand). |
| `blanco` | optioneel | `1` = **blanco** doe-het-zelf-kaart (geen art/tekst nodig). |
| `art` | beeldkaarten | Bestandsnaam in `../print/assets/` (bv. `groene-camera.png`). Leeg = placeholder. |
| `bron` | optioneel | Welke aflevering/personage het frame is (handig bij het verzamelen). |
| `notitie` | optioneel | Ontwerpnotitie; komt niet op de kaart. |

## Waarden voor `rood`/`blanco`
`1`, `ja`, `true`, `x` of `y` tellen als "aan"; leeg of `0` als "uit".

## Conventies
- `tekst` ≤ ±60 tekens, zodat het onder een vierkant paneel past.
- **Origineel** schrijven; geen letterlijke KUD-dialoog/songteksten (auteursrecht).
- Eén regel = één kaart. Dubbel nodig? Zet de regel twee keer neer.
- Balans-richtlijn: ~70% gewoon, ~25% `rood`, ~5% `blanco`.

## Voorbeeldregels
```csv
id,scene,tekst,rood,blanco,bron,notitie
PAN-001,"Die Groene kijkt recht in de camera, neutraal",,,,"KUD personage","Goede opener"
RED-001,"Zwoele Man duikt plots op en knipoogt","'…hallo.'",1,,"Zwoele man","Sterke slotgrap"
BLK-001,"",,,1,"","DIY paneel"
```

Workflow om art toe te voegen: zie [`../docs/ART-EN-TEKST-VERZAMELEN.md`](../docs/ART-EN-TEKST-VERZAMELEN.md).
