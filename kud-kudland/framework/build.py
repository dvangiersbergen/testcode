#!/usr/bin/env python3
"""
build.py — bouwt de KUDLAND-tegels en het regelboek-PDF.

Input : data/tiles.csv  +  ../print/assets/<videoId>.jpg  (echte KUD-thumbnails)
Output:
  ../print/tiles/<id>.png      gecomponeerde speeltegels (art + randterreinen + overlays)
  ../print/print.html          knipvel om de tegels te printen
  ../print/KUDLAND.pdf         regelboek (mechanics) + tegel-galerij + token-vel

Alleen Pillow (stdlib + Pillow). Alle KUD-beelden (c) Peter Lub / KUD — prive prototype.
"""
from __future__ import annotations
import csv, html, textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
TILES_CSV = HERE / "data" / "tiles.csv"
ASSETS = HERE.parent / "print" / "assets"
TILES_OUT = HERE.parent / "print" / "tiles"
PRINT_HTML = HERE.parent / "print" / "print.html"
PDF_OUT = HERE.parent / "print" / "KUDLAND.pdf"

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

TERR = {
    "Z": ("ZEE",   (43, 127, 212)),
    "G": ("LAND",  (79, 158, 63)),
    "W": ("WEG",   (130, 130, 130)),
    "L": ("LUCHT", (168, 111, 201)),
    "*": ("WILD",  (212, 160, 23)),
}
SPECIAL_BADGE = {
    "konijntje": ("KONIJNTJE x2", (214, 51, 132)),
    "koe":       ("KOE +3 LUCHT", (168, 111, 201)),
    "pilon":     ("PILON = WILD", (212, 160, 23)),
    "zwoele":    ("ZWOELE MAN",   (180, 60, 90)),
    "start":     ("STARTVELD",    (40, 40, 40)),
}

_fc: dict = {}
def font(sz: int, bold=False):
    key = (sz, bold)
    if key not in _fc:
        _fc[key] = ImageFont.truetype(FONTB if bold else FONT, sz)
    return _fc[key]

def tsize(d, txt, f):
    l, t, r, b = d.textbbox((0, 0), txt, font=f)
    return r - l, b - t


# ----------------------------------------------------------------------------- tegels
def square_crop(im: Image.Image, size: int) -> Image.Image:
    w, h = im.size
    s = min(w, h)
    im = im.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s))
    return im.resize((size, size), Image.LANCZOS)

def compose_tile(t: dict, S=720, m=96) -> Image.Image:
    img = Image.new("RGB", (S, S), "white")
    d = ImageDraw.Draw(img)
    edges = {"n": t["n"], "e": t["e"], "s": t["s"], "w": t["w"]}
    polys = {
        "n": [(0, 0), (S, 0), (S - m, m), (m, m)],
        "e": [(S, 0), (S, S), (S - m, S - m), (S - m, m)],
        "s": [(0, S), (S, S), (S - m, S - m), (m, S - m)],
        "w": [(0, 0), (0, S), (m, S - m), (m, m)],
    }
    mids = {"n": (S // 2, m // 2), "e": (S - m // 2, S // 2),
            "s": (S // 2, S - m // 2), "w": (m // 2, S // 2)}
    for side, code in edges.items():
        label, col = TERR.get(code, TERR["G"])
        d.polygon(polys[side], fill=col)
        if code == "*":  # wildcard arcering
            for off in range(-S, S, 22):
                d.line([(off, 0), (off + S, S)], fill=(255, 235, 170), width=3)
            d.polygon(polys[side], outline=(120, 90, 0))
        f = font(26, bold=True)
        tw, th = tsize(d, label, f)
        cx, cy = mids[side]
        d.text((cx - tw / 2, cy - th / 2), label, font=f, fill="white",
               stroke_width=3, stroke_fill=(0, 0, 0))
    # binnenvierkant = art
    inner = S - 2 * m
    if t["id"] == "START":
        d.rectangle([m, m, S - m, S - m], fill=(245, 230, 190))
        f = font(34, bold=True)
        for i, line in enumerate(["HET PLEIN", "VAN", "KUDLAND"]):
            tw, th = tsize(d, line, f)
            d.text(((S - tw) / 2, m + inner / 2 - 60 + i * 42), line, font=f, fill=(60, 40, 0))
    else:
        ap = ASSETS / f"{t['id']}.jpg"
        if ap.exists():
            art = square_crop(Image.open(ap).convert("RGB"), inner)
            img.paste(art, (m, m))
        else:
            d.rectangle([m, m, S - m, S - m], fill=(60, 60, 60))
    d.rectangle([m, m, S - m, S - m], outline=(255, 255, 255), width=4)
    d.rectangle([2, 2, S - 3, S - 3], outline=(20, 20, 20), width=4)

    # overlays op de art -------------------------------------------------------
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    # personage-strip onder
    pf = font(30, bold=True)
    pname = t["personage"]
    tw, th = tsize(od, pname, pf)
    od.rectangle([m, S - m - 50, S - m, S - m], fill=(0, 0, 0, 170))
    od.text(((S - tw) / 2, S - m - 46), pname, font=pf, fill=(255, 255, 255, 255))
    # sterren rechtsboven
    stars = int(t["sterren"])
    if stars:
        sf = font(34, bold=True)
        txt = "✦" * stars
        tw, th = tsize(od, txt, sf)
        od.rectangle([S - m - tw - 22, m + 8, S - m - 8, m + 8 + th + 14], fill=(0, 0, 0, 150))
        od.text((S - m - tw - 14, m + 12), txt, font=sf, fill=(255, 214, 0, 255))
    # special-badge linksboven
    sp = t["special"]
    if sp and sp in SPECIAL_BADGE and sp != "start":
        label, col = SPECIAL_BADGE[sp]
        bf = font(22, bold=True)
        tw, th = tsize(od, label, bf)
        od.rectangle([m + 8, m + 8, m + 8 + tw + 18, m + 8 + th + 12], fill=col + (235,))
        od.text((m + 17, m + 12), label, font=bf, fill=(255, 255, 255, 255))
    img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
    return img

def build_tiles(tiles):
    TILES_OUT.mkdir(parents=True, exist_ok=True)
    paths = []
    for t in tiles:
        im = compose_tile(t)
        p = TILES_OUT / f"{t['id']}.png"
        im.save(p)
        paths.append((t, p))
    print(f"  tegels gecomponeerd: {len(paths)} -> {TILES_OUT}")
    return paths


# ----------------------------------------------------------------------------- print.html
def build_html(tiles):
    cells = []
    for t in tiles:
        cells.append(
            f'<div class="tile"><img src="tiles/{html.escape(t["id"])}.png" '
            f'alt="{html.escape(t["title"])}"><div class="cap">{html.escape(t["title"])}</div></div>')
    css = """
*{box-sizing:border-box}body{margin:0;background:#ccc;font-family:Arial}
.sheet{width:210mm;min-height:297mm;padding:10mm;margin:0 auto 6mm;background:#fff;
 display:grid;grid-template-columns:repeat(3,60mm);gap:4mm;justify-content:center}
.tile{width:60mm}.tile img{width:60mm;height:60mm;display:block;border:0.3mm solid #000}
.cap{font-size:2.6mm;text-align:center;padding-top:1mm;color:#333}
@media print{body{background:#fff}.sheet{page-break-after:always;margin:0 auto}}
@page{size:A4;margin:0}"""
    pages = [tiles[i:i + 9] for i in range(0, len(tiles), 9)]
    body = ""
    for pg in pages:
        body += "<div class='sheet'>" + "".join(
            f'<div class="tile"><img src="tiles/{html.escape(t["id"])}.png"><div class="cap">{html.escape(t["title"])}</div></div>'
            for t in pg) + "</div>"
    PRINT_HTML.write_text(
        f"<!DOCTYPE html><html lang='nl'><head><meta charset='utf-8'>"
        f"<title>KUDLAND — knipvel</title><style>{css}</style></head><body>{body}</body></html>",
        encoding="utf-8")
    print(f"  print.html -> {PRINT_HTML}")


# ----------------------------------------------------------------------------- PDF
PW, PH, MAR = 1240, 1754, 96          # A4 @ 150dpi
GREEN = (47, 125, 50); INK = (25, 25, 25); GREY = (110, 110, 110)

class Doc:
    def __init__(self):
        self.pages = []; self._new();
    def _new(self):
        self.img = Image.new("RGB", (PW, PH), "white")
        self.d = ImageDraw.Draw(self.img); self.y = MAR; self.pages.append(self.img)
    def space(self, h): self.y += h
    def _room(self, h):
        if self.y + h > PH - MAR: self._new()
    def rule(self, color=GREEN, h=4):
        self._room(20); self.d.rectangle([MAR, self.y, PW - MAR, self.y + h], fill=color); self.y += h + 16
    def para(self, text, size=30, bold=False, color=INK, indent=0, gap=10, bullet=None):
        f = font(size, bold); maxw = PW - 2 * MAR - indent
        words = text.split(); line = ""; lines = []
        for w in words:
            t = (line + " " + w).strip()
            if self.d.textlength(t, font=f) <= (maxw - (34 if bullet else 0)):
                line = t
            else:
                lines.append(line); line = w
        lines.append(line)
        lh = size + 12
        for i, ln in enumerate(lines):
            self._room(lh)
            x = MAR + indent
            if bullet and i == 0:
                self.d.ellipse([x, self.y + size * 0.35, x + 12, self.y + size * 0.35 + 12], fill=GREEN)
                x += 34
            elif bullet:
                x += 34
            self.d.text((x, self.y), ln, font=f, fill=color); self.y += lh
        self.y += gap
    def h1(self, t):
        self._room(120)
        self.d.text((MAR, self.y), t, font=font(58, True), fill=GREEN); self.y += 74; self.rule()
    def h2(self, t):
        self._room(80); self.space(6)
        self.d.text((MAR, self.y), t, font=font(38, True), fill=INK); self.y += 52
    def save(self, path):
        self.pages[0].save(path, save_all=True, append_images=self.pages[1:], resolution=150.0)


def cover(doc, n_tiles):
    d, img = doc.d, doc.img
    d.rectangle([0, 0, PW, 420], fill=GREEN)
    d.text((MAR, 150), "KUDLAND", font=font(150, True), fill="white")
    d.text((MAR, 320), "Bouw het land van KUD — tegel voor tegel", font=font(34), fill=(230, 245, 230))
    d.text((MAR, 470), "Een legspel met echte KUD-afleveringen", font=font(40, True), fill=INK)
    for i, ln in enumerate([
        "2-4 spelers   |   ca. 25 min   |   12+",
        f"{n_tiles} aflevering-tegels  +  fan-pionnen",
        "",
        "Onofficieel fan-prototype. Mechaniek geinspireerd op leg-/tegelspellen",
        "(Carcassonne / Kingdomino). Alle KUD-beelden (c) Peter Lub / KUD,",
        "gebruikt voor PRIVE prototype-gebruik. Niet voor verkoop of verspreiding.",
    ]):
        d.text((MAR, 560 + i * 46), ln, font=font(28, ln.endswith("12+")), fill=INK if i < 2 else GREY)
    doc.y = 900
    doc.h2("In het kort")
    doc.para("Iedere tegel is een echte KUD-aflevering met vier randterreinen "
             "(Zee, Land, Weg, Lucht). Je legt afleveringen aan elkaar zodat de "
             "terreinen op de raakranden gelijk zijn, en claimt zo de grootste en "
             "meest iconische scenes van Kudland. Wie de meeste KUD-sterren scoort, wint.", size=30)
    doc._new()


def rules(doc):
    doc.h1("Spelregels")
    doc.h2("Doel")
    doc.para("Bouw samen een kaart van Kudland uit aflevering-tegels en beheers de "
             "grootste, meest iconische terrein-gebieden. Aan het eind heeft de speler "
             "met de meeste KUD-sterren (✦) gewonnen en wordt Burgemeester van Kudland.")
    doc.h2("Onderdelen")
    for b in [
        "Aflevering-tegels: in het midden de art van een echte KUD-aflevering.",
        "Vier randterreinen per tegel: ZEE (blauw), LAND (groen), WEG (grijs), LUCHT (paars).",
        "Een personage per tegel (de scene-eigenaar) en 0-3 sterren ✦ (hoe iconisch).",
        "Het Plein van Kudland: het startveld met alle vier de terreinen.",
        "Fan-pionnen in 4 kleuren (8 per speler) — jouw publiek dat een gebied claimt.",
    ]:
        doc.para(b, bullet=True, gap=4)
    doc.h2("Opzet")
    for b in [
        "Leg het startveld (Het Plein van Kudland) in het midden van de tafel.",
        "Schud de overige tegels tot een gedekte stapel. Leg 3 tegels open als markt.",
        "Iedere speler kiest een kleur en pakt de bijbehorende fan-pionnen.",
        "Jongste speler begint; daarna met de klok mee.",
    ]:
        doc.para(b, bullet=True, gap=4)
    doc.h2("Beurt (3 stappen)")
    doc.para("1. KIEZEN — Neem een van de 3 open markt-tegels.", bold=True, gap=4)
    doc.para("2. LEGGEN — Leg de tegel aan tegen minstens een al liggende tegel. Je mag "
             "vrij draaien, maar ELKE rand die een buurtegel raakt moet hetzelfde terrein "
             "tonen (zee-bij-zee, weg-bij-weg, enz.). Kun je nergens legaal leggen? Dan leg "
             "je de tegel onderop de stapel en kies je een andere.", indent=0, gap=4)
    doc.para("3. CLAIMEN (optioneel) — Zet een fan-pion op een terreingebied van de "
             "zojuist gelegde tegel, mits in dat gebied nog geen fan staat. Een 'gebied' is "
             "een aaneengesloten reeks tegels die via gelijke terreinranden verbonden zijn.",
             gap=4)
    doc.para("Vul daarna de markt weer aan tot 3 tegels. De beurt gaat door.", gap=12)
    doc.h2("Een gebied scoren")
    doc.para("Een terreingebied is AF zodra het volledig is ingesloten (geen open "
             "terreinrand meer vrij). De speler met de meeste fan-pionnen in dat gebied "
             "scoort: 1 punt per tegel + alle ✦ op die tegels. Daarna gaan de "
             "fan-pionnen terug naar hun eigenaars. Gelijkspel: alle betrokken spelers scoren.")
    doc.h2("Speciale afleveringen")
    for b in [
        "PILON = WILD: deze tegel heeft jokerranden die op elk terrein passen, maar levert 0 sterren.",
        "KONIJNTJE x2: het gebied waarin deze tegel ligt, scoort dubbele sterren.",
        "VLIEGENDE KOE +3: maak je een LUCHT-gebied af met deze tegel, dan +3 sterren extra.",
        "ZWOELE MAN: 1x per spel mag je een fan plaatsen in een gebied dat al geclaimd is.",
    ]:
        doc.para(b, bullet=True, gap=4)
    doc.h2("Einde & winnen")
    doc.para("Het spel eindigt zodra de stapel op is en niemand meer kan leggen. Score nu "
             "alle nog niet-afgemaakte gebieden op de normale manier. Meeste ✦ wint. "
             "Gelijk? De speler met de meeste verschillende personages in zijn gescoorde "
             "gebieden wint — anders blijft het een gedeelde titel.")
    doc.h2("Varianten")
    for b in [
        "DUO (2 sp.): speel met 6 fans elk; markt van 2 tegels voor scherpere keuzes.",
        "MISSIES: deel elke speler in het geheim 1 personage; +5 ✦ als jij het grootste "
        "gebied met dat personage beheerst aan het eind.",
        "SNELSPEL: gebruik 16 tegels i.p.v. alles.",
    ]:
        doc.para(b, bullet=True, gap=4)
    doc._new()


def gallery(doc, paths):
    doc.h1("Tegel-galerij")
    doc.para("Alle aflevering-tegels in dit prototype, gebouwd uit de officiele "
             "thumbnails van het KUD-kanaal van Peter Lub. De vier randkleuren zijn de "
             "terreinen; onderaan staat het personage, rechtsboven de sterren.", color=GREY, size=26)
    cell, cols = 330, 3
    gx = (PW - 2 * MAR - cols * cell) // (cols - 1)
    capf = font(20, True); subf = font(18)
    col = row = 0; top = doc.y
    for i, (t, p) in enumerate(paths):
        if row == 3:
            doc._new(); doc.space(10); top = doc.y; row = 0
        x = MAR + col * (cell + gx); y = top + row * (cell + 78)
        thumb = Image.open(p).resize((cell, cell), Image.LANCZOS)
        doc.img.paste(thumb, (int(x), int(y)))
        cap = t["title"] if len(t["title"]) <= 30 else t["title"][:29] + "…"
        doc.d.text((x, y + cell + 6), cap, font=capf, fill=INK)
        extra = f"{t['personage']}  ✦x{t['sterren']}"
        doc.d.text((x, y + cell + 32), extra, font=subf, fill=GREY)
        col += 1
        if col == cols: col = 0; row += 1
    doc._new()


def tokens(doc):
    doc.h1("Fan-pionnen & spelershulp")
    doc.para("Knip de fan-pionnen uit (8 per kleur) en vouw ze dubbel, of gebruik losse "
             "pionnen/munten in vier kleuren.", color=GREY, size=26)
    colors = [("Groen", (47, 125, 50)), ("Roze", (214, 51, 132)),
              ("Blauw", (43, 127, 212)), ("Geel", (212, 160, 23))]
    x0, y0, r = MAR, doc.y + 20, 34
    for ci, (name, col) in enumerate(colors):
        cy = y0 + ci * 110
        doc.d.text((x0, cy + r - 16), name, font=font(28, True), fill=col)
        for k in range(8):
            cx = x0 + 240 + k * 95
            doc.d.ellipse([cx, cy, cx + 2 * r, cy + 2 * r], fill=col, outline=(0, 0, 0), width=3)
    doc.y = y0 + 4 * 110 + 30
    doc.rule()
    doc.h2("Beurt in het kort")
    for b in ["KIEZEN: pak 1 van de 3 markttegels.",
              "LEGGEN: rand-terreinen moeten matchen (draaien mag).",
              "CLAIMEN: 1 fan op een nog vrij gebied (optioneel).",
              "Vul de markt aan tot 3."]:
        doc.para(b, bullet=True, gap=4)
    doc.h2("Scoren")
    doc.para("Afgesloten gebied: 1 punt/tegel + alle ✦. Meeste fans wint het gebied; "
             "fans keren terug. Konijntje x2, Vliegende Koe +3 lucht, Pilon = wild, "
             "Zwoele Man 1x in bezet gebied.")


def build_pdf(paths):
    doc = Doc()
    cover(doc, len(paths))
    rules(doc)
    gallery(doc, paths)
    tokens(doc)
    doc.save(PDF_OUT)
    print(f"  PDF ({len(doc.pages)} pagina's) -> {PDF_OUT}")


def main():
    tiles = list(csv.DictReader(TILES_CSV.open(encoding="utf-8")))
    print(f"KUDLAND build — {len(tiles)} tegels")
    paths = build_tiles(tiles)
    build_html(tiles)
    build_pdf(paths)
    print("Klaar.")


if __name__ == "__main__":
    main()
