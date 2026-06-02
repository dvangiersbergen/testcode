#!/usr/bin/env python3
"""
generate_cards.py — KUD: Lachgevaar (naar Joking Hazard)

Eén homogene stapel STRIP-PANELEN. Leest data/panels.csv en bouwt een print-klaar
vierkant kaartvel in ../print/print.html. Vierkante kaarten leggen netjes naast elkaar
tot een 3-panel-strip.

- Beeldkaarten verwijzen naar afbeeldingen in ../print/assets/ (kolom `art`).
- Ontbreekt de afbeelding? Dan komt er een PLACEHOLDER met de scene-beschrijving,
  zodat je nu al kunt testspelen en precies weet welk KUD-fragment je nog nodig hebt.

Gebruik:
    python3 generate_cards.py              # voorkanten + achterkanten
    python3 generate_cards.py --no-backs

Alleen de Python-standaardbibliotheek.
"""
from __future__ import annotations
import argparse, csv, html, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "data" / "panels.csv"
PRINT_DIR = HERE.parent / "print"
ASSETS = PRINT_DIR / "assets"
OUT = PRINT_DIR / "print.html"
IMG_EXTS = (".png", ".jpg", ".jpeg", ".webp", ".gif")

GREEN = "#2f7d32"
RED = "#d32f2f"


def load_panels() -> list[dict]:
    if not DATA.exists():
        print(f"Niet gevonden: {DATA}", file=sys.stderr)
        return []
    with DATA.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    print(f"  + {len(rows)} panelen uit {DATA.name}")
    return rows


def truthy(v: str) -> bool:
    return str(v or "").strip().lower() in {"1", "ja", "true", "x", "y"}


def asset_exists(name: str) -> bool:
    if not name:
        return False
    p = ASSETS / name
    return p.exists() and p.suffix.lower() in IMG_EXTS


def esc(t: str) -> str:
    return html.escape((t or "").strip())


def art_block(card: dict) -> str:
    art = (card.get("art") or "").strip()
    if asset_exists(art):
        return f'<div class="art"><img src="assets/{esc(art)}" alt=""></div>'
    scene = esc(card.get("scene", "")) or "(beschrijf de scene)"
    return ('<div class="art placeholder">'
            '<div class="ph-icon">🎬</div><div class="ph-text">KUD-FRAGMENT</div>'
            f'<div class="ph-scene">{scene}</div>'
            f'<div class="ph-file">{esc(art) or "bestandsnaam in art-kolom"}</div></div>')


def render_card(card: dict) -> str:
    rood = truthy(card.get("rood"))
    blanco = truthy(card.get("blanco"))
    cid = esc(card.get("id", ""))
    tekst = esc(card.get("tekst", ""))

    cls = "card"
    if rood:
        cls += " rood"
    if blanco:
        cls += " blanco"

    if blanco:
        body = ('<div class="art blank"><div class="bl-icon">✎</div>'
                '<div class="bl-text">TEKEN / PLAK<br>JE EIGEN<br>KUD-PANEEL</div></div>')
    else:
        body = art_block(card)
        if tekst:
            body += f'<div class="caption">{tekst}</div>'

    badge = '<div class="badge">★ SLOTPANEEL</div>' if rood else ""
    footer = f'<div class="footer"><span>{cid}</span>{"<span>blanco</span>" if blanco else ""}</div>'
    return f'<div class="{cls}">{badge}{body}{footer}</div>'


def render_back(rood=False) -> str:
    cls = "card back rood" if rood else "card back"
    return (f'<div class="{cls}"><div class="back-inner">'
            f'<div class="back-logo">KUD</div><div class="back-sub">Lachgevaar</div></div></div>')


def chunk(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


CSS = f"""
* {{ box-sizing: border-box; }}
body {{ margin:0; background:#ddd; font-family:'Helvetica Neue',Arial,sans-serif; }}
.sheet {{ width:210mm; min-height:297mm; padding:9mm; margin:0 auto 6mm; background:#fff;
  display:grid; grid-template-columns:repeat(3,62mm); grid-auto-rows:62mm; gap:3mm;
  justify-content:center; align-content:start; }}
.section-title {{ width:210mm; margin:9mm auto 2mm; font-weight:800; color:#333; }}
.card {{ position:relative; width:62mm; height:62mm; border:0.9mm solid #111; border-radius:1.5mm;
  overflow:hidden; display:flex; flex-direction:column; background:#fff; page-break-inside:avoid; }}
.card.rood {{ border-color:{RED}; border-width:1.6mm; }}
.art {{ flex:1; display:flex; align-items:center; justify-content:center; overflow:hidden; background:#fafafa; }}
.art img {{ width:100%; height:100%; object-fit:cover; }}
.art.placeholder {{ flex-direction:column; gap:1mm; color:#444; text-align:center; padding:3mm;
  background:repeating-linear-gradient(45deg,#f3f3f3,#f3f3f3 3mm,#ececec 3mm,#ececec 6mm); }}
.ph-icon {{ font-size:8mm; }} .ph-text {{ font-weight:800; font-size:2.8mm; letter-spacing:0.4mm; color:{GREEN}; }}
.ph-scene {{ font-size:3mm; font-weight:600; color:#222; line-height:1.2; }}
.ph-file {{ font-size:2.3mm; color:#777; word-break:break-all; }}
.art.blank {{ flex-direction:column; gap:2mm; color:#999;
  background:repeating-linear-gradient(45deg,#fff,#fff 4mm,#f6f6f6 4mm,#f6f6f6 8mm);
  border:0.4mm dashed #bbb; margin:2mm; border-radius:1mm; }}
.bl-icon {{ font-size:10mm; }} .bl-text {{ font-weight:800; font-size:3mm; text-align:center; letter-spacing:0.3mm; }}
.caption {{ padding:1.8mm 2.5mm; font-size:3.1mm; font-weight:600; color:#111; text-align:center;
  border-top:0.3mm solid #eee; background:#fff; }}
.badge {{ position:absolute; top:0; right:0; background:{RED}; color:#fff; font-weight:800;
  font-size:2.3mm; padding:0.8mm 1.8mm; border-bottom-left-radius:1.5mm; letter-spacing:0.3mm; z-index:2; }}
.footer {{ display:flex; justify-content:space-between; padding:1mm 2mm; font-size:2.3mm; color:#999; }}
.card.back {{ align-items:center; justify-content:center; background:{GREEN}; }}
.card.back.rood {{ background:{RED}; }}
.back-inner {{ text-align:center; color:#fff; }}
.back-logo {{ font-size:15mm; font-weight:900; letter-spacing:1mm; }}
.back-sub {{ font-size:3.4mm; font-weight:600; opacity:.9; }}
@media print {{ body {{ background:#fff; }} .sheet {{ margin:0 auto; page-break-after:always; }}
  .section-title {{ page-break-before:always; }} }}
@page {{ size:A4; margin:0; }}
"""


def build(cards, with_backs):
    parts = ["<!DOCTYPE html><html lang='nl'><head><meta charset='utf-8'>",
             "<title>KUD: Lachgevaar — printvel</title>", f"<style>{CSS}</style></head><body>"]
    normal = [c for c in cards if not truthy(c.get("rood"))]
    rood = [c for c in cards if truthy(c.get("rood"))]

    parts.append(f"<div class='section-title'>PANELEN — {len(normal)} kaarten</div>")
    for page in chunk(normal, 12):
        parts.append("<div class='sheet'>")
        parts.extend(render_card(c) for c in page)
        parts.append("</div>")

    if rood:
        parts.append(f"<div class='section-title'>RODE SLOTPANELEN — {len(rood)} kaarten</div>")
        for page in chunk(rood, 12):
            parts.append("<div class='sheet'>")
            parts.extend(render_card(c) for c in page)
            parts.append("</div>")

    if with_backs:
        parts.append(f"<div class='section-title'>ACHTERKANT</div>")
        for page in chunk([0] * len(normal), 12):
            parts.append("<div class='sheet'>")
            parts.extend(render_back(False) for _ in page)
            parts.append("</div>")
        if rood:
            parts.append(f"<div class='section-title'>ACHTERKANT — ROOD</div>")
            for page in chunk([0] * len(rood), 12):
                parts.append("<div class='sheet'>")
                parts.extend(render_back(True) for _ in page)
                parts.append("</div>")

    parts.append("</body></html>")
    return "".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-backs", action="store_true")
    args = ap.parse_args()

    print("KUD: Lachgevaar — kaartgenerator")
    cards = load_panels()
    if not cards:
        return 1
    missing = sum(1 for c in cards
                  if not truthy(c.get("blanco")) and not asset_exists((c.get("art") or "").strip()))
    PRINT_DIR.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(cards, not args.no_backs), encoding="utf-8")
    print(f"\nKlaar: {len(cards)} panelen -> {OUT}")
    if missing:
        print(f"Let op: {missing} panelen gebruiken nog een PLACEHOLDER "
              f"(zet de afbeelding in {ASSETS.name}/ en draai opnieuw).")
    print("Open print.html en print op A4 (schaal 100%).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
