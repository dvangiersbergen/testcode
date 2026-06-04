# Grafisch vormgever — Joris Maes (review + concepten)

## Kritiek op de huidige graphics
- **Flavor-balk**: een dikke zwarte "tombstone" met systeemfont; vecht met de still i.p.v. eruit te groeien.
- **Poort-nops**: te klein, los, onverankerd in het kaderwerk; symbool nauwelijks zichtbaar.
- **Kader**: karakterloze rechthoek, geen relatie met de "kapotte monitor"-wereld.
- **Signaalbaan**: te egaal/placeholder; geen textuur of breedte-ritme (geen onderscheid kabel vs. storing).
- **Typografie**: generiek, geen systeem, geen KUD-toon.

## Vier concept-richtingen (renderbaar, met specs)
- **A · RUIS** — lo-fi VHS-grunge. Diepzwart, scanline-signaalbaan in fel scanline-groen/roze/blauw/geel, CRT-bezel, monospace caps, flavor-balk met scanlines, VHS-bits (PLAY / timecode). *Joris' aanrader.*
- **B · DRAGER** — Swiss editorial/grid. Warm papier, harde zwarte kaders, condensed grotesk, 3-zone-layout, enkele lijn-baan met zwarte outline, vierkante poorten. Strak/serieus.
- **C · STICKER** — riso/handgemaakt. Gebroken wit + halftone, riso-oranje kader, still als opgeplakte sticker met schaduw, brushy tape-baan (licht gedraaid), ronde sticker-poorten, badge + bijschrift.
- **D · TECHNISCH** — industrieel kabelschema. Donker marineblauw, IBM Plex Mono, zeshoekige connector-poorten, dubbele baan (lijn + stippel-protocollijn), meetlat-kader. Sereus/technisch.

## Aanbeveling
**A · RUIS.** KANALEN gaat over een signaal dat het net haalt; KUD is een signaal dat het nooit
helemaal haalt. De scanline-baan geeft elke verbinding lading. B is te foutloos voor KUD, C te
schattig, D dwingt een paletwissel die botst met de uitbundige cartoon-stills.

**Productie-aandachtspunt:** scanlines & CRT-gloed als **vector** aanleveren (niet raster); lijnen
≥0,25 mm in het finale bestand; proefdruk op 310 gsm black-core vóór de hele oplage.

**Mock:** `examples/concepten.png` (A/B/C naast elkaar) — render door de lead o.b.v. deze specs.
