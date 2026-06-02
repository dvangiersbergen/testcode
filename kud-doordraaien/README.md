# KUD: DOORDRAAIEN — concept + playtest

2-speler competitief kaartspel op basis van **Tapeworm**, met KUD-afleveringen als art.
Eindeloos uitdijende "filmstrip": dump je kaarten door scènes aan te leggen, scoor kijkcijfers
door verhaallijnen af te sluiten. Volledige regels: [`DESIGN.md`](DESIGN.md).

## Wat hier ligt
| Pad | Wat |
|-----|-----|
| [`DESIGN.md`](DESIGN.md) | De speelregels (concept v0.3) |
| [`cards/KUD-Doordraaien-concept.pdf`](cards/KUD-Doordraaien-concept.pdf) | **De concept­kaarten** (high-end, met anatomie-uitleg) |
| [`cards/overzicht.png`](cards/overzicht.png) | Contactvel van alle 16 kaarten |
| [`cards/png/`](cards/png/) | Losse kaart-PNG's |
| [`cards/render_cards.py`](cards/render_cards.py) | Kaartgenerator (Pillow; gebruikt de KUD-thumbnails uit `../kud-kudland/`) |
| [`sim/simulate.py`](sim/simulate.py) | Speelbare regelengine + 360-potjes-playtest |
| [`sim/results.md`](sim/results.md) | Geaggregeerde resultaten & balanssignalen |
| [`sim/sample_game.md`](sim/sample_game.md) | Eén becommentarieerd potje |
| [`playtest/BETA-FEEDBACK.md`](playtest/BETA-FEEDBACK.md) | **Synthese van 4 fan-beta-testers** + v0.4-voorstellen |

## Reproduceren
```bash
python3 cards/render_cards.py     # kaarten + PDF
python3 sim/simulate.py           # 360 potjes -> results.md + sample_game.md
```
Vereist Pillow (`pip install Pillow`). KUD-beelden © Peter Lub / KUD — privé concept-/prototype-gebruik.
