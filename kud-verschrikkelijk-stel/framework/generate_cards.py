#!/usr/bin/env python3
"""
generate_cards.py — KUD: Verschrikkelijk Stel (Die Groene × Die Roze)

Leest de CSV-kaartdata in ./data/ en bouwt een print-klaar HTML-vel in ../print/print.html.
3-panel-stripspel naar 'Horrible Couple' (The Oatmeal × Exploding Kittens):
  VRAAG (paneel 1, beeld+tekst) -> REACTIE (paneel 2, tekst) -> COMPROMIS (paneel 3, beeld).

- Beeldkaarten verwijzen naar afbeeldingen in ../print/assets/ (kolom `fragment`).
- Ontbreekt de afbeelding? Dan komt er automatisch een PLACEHOLDER met de gewenste naam.

Gebruik:
    python3 generate_cards.py            # fronts + backs voor alle types
    python3 generate_cards.py --no-backs # alleen voorkanten

Geen externe dependencies (alleen de Python-standaardbibliotheek).
"""

from __future__ import annotations

import argparse
import csv
import html
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE / "data"
PRINT_DIR = HERE.parent / "print"
ASSETS_DIR = PRINT_DIR / "assets"
OUT_FILE = PRINT_DIR / "print.html"

# Type -> (label, kleur, beeldkaart?)
TYPES = {
    "vraag":     {"label": "VRAAG",     "color": "#d81b8c", "image": True},   # Die Roze stelt de vraag
    "reactie":   {"label": "REACTIE",   "color": "#2e7d32", "image": False},  # Die Groene reageert
    "compromis": {"label": "COMPROMIS", "color": "#00838f", "image": True},   # handkaarten
    "speciaal":  {"label": "SPECIAAL",  "color": "#6a1b9a", "image": True},
}

CSV_FILES = {
    "vraag":     "vragen.csv",
    "reactie":   "reacties.csv",
    "compromis": "compromissen.csv",
    "speciaal":  "speciale-kaarten.csv",
}

IMG_EXTS = (".png", ".jpg", ".jpeg", ".webp", ".gif")


def load_cards() -> list[dict]:
    cards: list[dict] = []
    for ctype, fname in CSV_FILES.items():
        path = DATA_DIR / fname
        if not path.exists():
            print(f"  ! overslaan (niet gevonden): {fname}", file=sys.stderr)
            continue
        with path.open(encoding="utf-8", newline="") as fh:
            rows = list(csv.DictReader(fh))
            for row in rows:
                row["type"] = (row.get("type") or ctype).strip()
                cards.append(row)
            print(f"  + {len(rows):3d} kaarten uit {fname}")
    return cards


def asset_exists(fragment: str) -> bool:
    if not fragment:
        return False
    p = ASSETS_DIR / fragment
    return p.exists() and p.suffix.lower() in IMG_EXTS


def esc(text: str) -> str:
    return html.escape((text or "").strip())


def art_block(fragment: str) -> str:
    if asset_exists(fragment):
        return f'<div class="art"><img src="assets/{esc(fragment)}" alt="{esc(fragment)}"></div>'
    want = esc(fragment) if fragment else "(geen fragment opgegeven)"
    return (
        '<div class="art placeholder">'
        '<div class="ph-icon">🖼️</div><div class="ph-text">FRAGMENT NODIG</div>'
        f'<div class="ph-name">{want}</div></div>'
    )


def render_card(card: dict) -> str:
    ctype = card.get("type", "")
    meta = TYPES.get(ctype, {"label": ctype.upper(), "color": "#444", "image": True})
    color = meta["color"]
    bijschrift = esc(card.get("bijschrift", ""))
    fragment = (card.get("fragment") or "").strip()
    cid = esc(card.get("id", ""))
    bron = esc(card.get("bron", ""))
    effect = esc(card.get("effect", ""))
    score = (card.get("score") or "").strip()

    golden = ""
    try:
        if score and int(float(score)) >= 18:
            golden = " golden"
    except ValueError:
        pass

    if ctype == "vraag":
        body = art_block(fragment) + f'<div class="caption vraagtekst">{bijschrift}</div>'
    elif ctype == "reactie":
        body = f'<div class="art textcard"><div class="bigtext">{bijschrift}</div></div>'
    elif ctype == "speciaal":
        body = (art_block(fragment) +
                f'<div class="caption"><div class="title">{bijschrift}</div>'
                f'<div class="effect">{effect}</div></div>')
    else:  # compromis
        body = art_block(fragment) + f'<div class="caption">{bijschrift}</div>'

    footer = f'<div class="footer"><span class="cid">{cid}</span>'
    if bron:
        footer += f'<span class="bron">{bron}</span>'
    footer += "</div>"

    return (f'<div class="card{golden}" style="--c:{color}">'
            f'<div class="band">{meta["label"]}</div>{body}{footer}</div>')


def render_back(ctype: str) -> str:
    meta = TYPES[ctype]
    return (f'<div class="card back" style="--c:{meta["color"]}">'
            f'<div class="back-inner"><div class="back-logo">KUD</div>'
            f'<div class="back-sub">Verschrikkelijk Stel</div>'
            f'<div class="back-type">{meta["label"]}</div></div></div>')


def chunk(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


CSS = """
* { box-sizing: border-box; }
body { margin: 0; background: #ddd; font-family: 'Helvetica Neue', Arial, sans-serif; }
.sheet { width: 210mm; min-height: 297mm; padding: 8mm; margin: 0 auto 6mm; background: #fff;
  display: grid; grid-template-columns: repeat(3, 63mm); grid-auto-rows: 88mm; gap: 4mm;
  justify-content: center; align-content: start; }
.section-title { width: 210mm; margin: 10mm auto 2mm; font-weight: 800; color: #333; }
.card { width: 63mm; height: 88mm; border: 0.4mm solid var(--c); border-radius: 3mm; overflow: hidden;
  display: flex; flex-direction: column; background: #fff; position: relative; page-break-inside: avoid; }
.card.golden { box-shadow: inset 0 0 0 1.2mm gold; }
.band { background: var(--c); color: #fff; font-weight: 800; font-size: 3mm; letter-spacing: 0.6mm;
  padding: 1.4mm 2.5mm; text-align: center; }
.art { flex: 1; display: flex; align-items: center; justify-content: center; overflow: hidden; background:#fafafa; }
.art img { width: 100%; height: 100%; object-fit: cover; }
.art.placeholder { flex-direction: column; gap: 1.5mm; color: var(--c); text-align: center; padding: 3mm;
  background: repeating-linear-gradient(45deg, #f3f3f3, #f3f3f3 3mm, #ececec 3mm, #ececec 6mm); }
.ph-icon { font-size: 9mm; } .ph-text { font-weight: 800; font-size: 3mm; letter-spacing: 0.4mm; }
.ph-name { font-size: 3mm; color: #555; word-break: break-all; }
.art.textcard { padding: 5mm; background: #fff; }
.bigtext { font-size: 5mm; font-weight: 700; color: #111; line-height: 1.25; text-align: center; }
.caption { padding: 2.5mm 3mm; font-size: 3.4mm; font-weight: 600; color: #111; text-align: center; }
.caption.vraagtekst { font-size: 3.8mm; font-weight: 700; }
.caption .title { font-weight: 800; color: var(--c); margin-bottom: 1mm; }
.caption .effect { font-size: 2.9mm; font-weight: 500; color: #333; }
.footer { display: flex; justify-content: space-between; align-items: center; padding: 1.5mm 2.5mm;
  font-size: 2.4mm; color: #888; border-top: 0.2mm solid #eee; }
.bron { font-style: italic; max-width: 38mm; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.card.back { align-items: center; justify-content: center; background: var(--c); }
.back-inner { text-align: center; color: #fff; }
.back-logo { font-size: 16mm; font-weight: 900; letter-spacing: 1mm; }
.back-sub { font-size: 3.4mm; font-weight: 600; opacity: 0.9; }
.back-type { margin-top: 3mm; font-size: 3mm; font-weight: 800; letter-spacing: 0.6mm;
  border: 0.4mm solid #fff; border-radius: 2mm; display: inline-block; padding: 1mm 2.5mm; }
@media print { body { background: #fff; } .sheet { box-shadow: none; margin: 0 auto; page-break-after: always; }
  .section-title { page-break-before: always; } }
@page { size: A4; margin: 0; }
"""


def build_html(cards, with_backs):
    parts = ["<!DOCTYPE html><html lang='nl'><head><meta charset='utf-8'>",
             "<title>KUD: Verschrikkelijk Stel — printvel</title>",
             f"<style>{CSS}</style></head><body>"]
    order = ["vraag", "reactie", "compromis", "speciaal"]
    by_type = {t: [] for t in order}
    for c in cards:
        by_type.setdefault(c["type"], []).append(c)

    for t in order:
        group = by_type.get(t, [])
        if not group:
            continue
        parts.append(f"<div class='section-title'>{TYPES[t]['label']} — {len(group)} kaarten</div>")
        for page in chunk(group, 9):
            parts.append("<div class='sheet'>")
            parts.extend(render_card(c) for c in page)
            parts.append("</div>")

    if with_backs:
        for t in order:
            n = len(by_type.get(t, []))
            if not n:
                continue
            parts.append(f"<div class='section-title'>ACHTERKANT — {TYPES[t]['label']}</div>")
            for page in chunk([t] * n, 9):
                parts.append("<div class='sheet'>")
                parts.extend(render_back(t) for _ in page)
                parts.append("</div>")

    parts.append("</body></html>")
    return "".join(parts)


def main():
    ap = argparse.ArgumentParser(description="Genereer print-klaar HTML voor KUD: Verschrikkelijk Stel.")
    ap.add_argument("--no-backs", action="store_true", help="Sla achterkanten over.")
    args = ap.parse_args()

    print("KUD: Verschrikkelijk Stel — kaartgenerator")
    print(f"Data:   {DATA_DIR}\nAssets: {ASSETS_DIR}")
    cards = load_cards()
    if not cards:
        print("Geen kaarten gevonden. Staan de CSV-bestanden in data/?", file=sys.stderr)
        return 1

    missing = sum(1 for c in cards
                  if TYPES.get(c["type"], {}).get("image")
                  and not asset_exists((c.get("fragment") or "").strip()))
    PRINT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(build_html(cards, with_backs=not args.no_backs), encoding="utf-8")

    print(f"\nKlaar: {len(cards)} kaarten -> {OUT_FILE}")
    if missing:
        print(f"Let op: {missing} beeldkaarten gebruiken nog een PLACEHOLDER "
              f"(zet de afbeelding in {ASSETS_DIR.name}/ en draai opnieuw).")
    print("Open print.html in je browser en print op A4 (schaal 100%).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
