#!/usr/bin/env python3
"""
render_cards.py — high-end concept cards voor KUD: DOORDRAAIEN (v0.4: koord & klik + quote-laag).

Toevoegingen t.o.v. v0.3:
  - QUOTE-ONDERTITEL op de art (als TV-ondertitel), met OPZET/PUNCHLINE-tag = de "voice"-laag.
  - RUNNING-GAG-tag (↺) linksboven = combo-mechaniek.
  - MAGNEET-poorten: elke draad-poort toont een magneetring + koord-kleur (fysiek concept).

Quoteregels hieronder zijn ORIGINEEL in KUD-stijl (placeholder) — GEEN echte serie-citaten.
Gebruikt de KUD-thumbnails uit ../../kud-kudland/print/assets/ als scene-art. Alleen Pillow.
"""
from __future__ import annotations
import csv
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = Path(__file__).resolve().parent
ASSETS = HERE.parent.parent / "kud-kudland" / "print" / "assets"
MANIFEST = HERE.parent.parent / "kud-kudland" / "framework" / "data" / "manifest.csv"
PNG = HERE / "png"; PNG.mkdir(exist_ok=True)

F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
_fc: dict = {}
def font(sz, bold=True):
    k=(sz,bold)
    if k not in _fc: _fc[k]=ImageFont.truetype(FB if bold else F, sz)
    return _fc[k]
def tw(d,t,f): l,_,r,_=d.textbbox((0,0),t,font=f); return r-l

THREADS = {
    "G": ("GROEN", (54,178,99)), "R": ("ROZE", (228,74,153)),
    "B": ("BLAUW", (52,140,224)), "Y": ("GEEL", (240,196,46)),
    "*": ("WILD", (170,174,186)),
}
INK=(22,25,31); PAPER=(248,248,246)
QTAG={"setup":("OPZET",(52,140,224)), "punch":("PUNCHLINE",(228,74,153))}

titles={}
if MANIFEST.exists():
    for r in csv.DictReader(MANIFEST.open(encoding="utf-8")): titles[r["videoId"]]=r["title"]

W,H=1120,760
ART=(70,150,W-70,H-150)

def rrect(d,box,r,**kw): d.rounded_rectangle(box,radius=r,**kw)

def shadow_card():
    pad=40
    base=Image.new("RGBA",(W+2*pad,H+2*pad),(0,0,0,0))
    sh=Image.new("RGBA",base.size,(0,0,0,0)); ds=ImageDraw.Draw(sh)
    ds.rounded_rectangle([pad+10,pad+16,pad+W+10,pad+H+16],radius=34,fill=(0,0,0,120))
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16)))
    card=Image.new("RGBA",(W,H),INK+(255,)); d=ImageDraw.Draw(card)
    rrect(d,[3,3,W-4,H-4],30,outline=(255,255,255,28),width=3)
    base.alpha_composite(card,(pad,pad)); return base,pad

def scene(card,vid,accent):
    d=ImageDraw.Draw(card); x0,y0,x1,y1=ART
    rrect(d,[x0-6,y0-6,x1+6,y1+6],14,fill=(8,9,11,255))
    if vid and (ASSETS/f"{vid}.jpg").exists():
        im=Image.open(ASSETS/f"{vid}.jpg").convert("RGB"); iw,ih=im.size
        tw_,th_=x1-x0,y1-y0; s=max(tw_/iw,th_/ih)
        im=im.resize((int(iw*s),int(ih*s)),Image.LANCZOS)
        im=im.crop(((im.width-tw_)//2,(im.height-th_)//2,(im.width-tw_)//2+tw_,(im.height-th_)//2+th_))
        card.paste(im,(x0,y0))
    else: d.rectangle([x0,y0,x1,y1],fill=(40,44,52,255))
    n=9
    for i in range(n):
        cx=x0+(i+0.5)*(x1-x0)/n
        for yy in (y0-34,y1+8):
            d.rounded_rectangle([cx-16,yy,cx+16,yy+26],radius=6,fill=(14,16,20,255),outline=(70,74,82,255),width=2)
    rrect(d,[x0,y0,x1,y1],10,outline=accent+(255,),width=5)

def subtitle(card,quote,qtag):
    if not quote: return
    d=ImageDraw.Draw(card,"RGBA"); x0,y0,x1,y1=ART
    bar=[x0+12,y1-112,x1-12,y1-12]
    rrect(d,bar,12,fill=(6,7,9,185))
    tx=x0+30; ty=bar[1]+16
    if qtag:
        lbl,col=QTAG[qtag]; f=font(18); wlab=tw(d,lbl,f)
        rrect(d,[tx,ty,tx+wlab+22,ty+30],8,fill=col+(255,))
        d.text((tx+11,ty+5),lbl,font=f,fill=(255,255,255,255)); ty+=40
    else: ty+=4
    f=font(26); maxw=x1-12-tx-18; words=quote.split(); line=""; yy=ty
    for wd in words:
        if tw(d,(line+" "+wd).strip(),f)<=maxw: line=(line+" "+wd).strip()
        else: d.text((tx,yy),"“"+line if yy==ty else line,font=f,fill=(246,246,246,255)); yy+=32; line=wd
    d.text((tx,yy),("“"+line+"”") if yy==ty else (line+"”"),font=f,fill=(246,246,246,255))

def port_tab(card,side,idx,total,color,capped=False):
    d=ImageDraw.Draw(card); th=120; gap=24; block=total*th+(total-1)*gap
    cy=H//2-block//2+idx*(th+gap)+th//2
    box=[-2,cy-th//2,64,cy+th//2] if side=="L" else [W-64,cy-th//2,W+2,cy+th//2]
    cxp=(box[0]+box[2])//2
    if capped or color=="CAP":
        rrect(d,box,14,fill=(60,64,72,255))
        d.text((cxp-tw(d,"■",font(40))//2,cy-26),"■",font=font(40),fill=(150,154,162,255)); return
    name,col=THREADS[color]
    rrect(d,box,14,fill=col+(255,))
    d.ellipse([cxp-18,cy-18,cxp+18,cy+18],fill=(228,230,235,255))            # magneet
    d.ellipse([cxp-18,cy-18,cxp+18,cy+18],outline=(120,124,132,255),width=3)
    d.ellipse([cxp-8,cy-8,cxp+8,cy+8],fill=col+(255,))                       # koord-kleur

def header(card,type_label,glyph,accent):
    d=ImageDraw.Draw(card)
    rrect(d,[36,34,W-36,118],18,fill=(255,255,255,16))
    d.text((58,52),"KUD",font=font(46),fill=(255,255,255,255))
    d.text((150,62),"DOORDRAAIEN",font=font(24),fill=(190,194,202,255))
    tl=type_label.upper(); f=font(30)
    d.text((W-58-tw(d,tl,f),60),tl,font=f,fill=accent+(255,))
    d.ellipse([W-150,128,W-78,200],fill=accent+(255,))
    g=font(38); d.text((W-114-tw(d,glyph,g)//2,146),glyph,font=g,fill=(20,22,28,255))

def gag_tag(card,gag):
    if not gag: return
    d=ImageDraw.Draw(card); t=f"↺ {gag}"; f=font(20); wdt=tw(d,t,f)
    rrect(d,[50,128,50+wdt+30,170],10,fill=(245,196,46,255))
    d.text((66,137),t,font=f,fill=(28,28,28,255))

def footer(card,title,rule):
    d=ImageDraw.Draw(card); y=H-128
    if title:
        f=font(30); t=title if len(title)<=34 else title[:33]+"…"
        d.text((70,y),t,font=f,fill=(255,255,255,255))
    if rule:
        f=font(22,bold=False); words=rule.split(); line=""; yy=y+44
        for w in words:
            if tw(d,(line+" "+w).strip(),f)<=W-140: line=(line+" "+w).strip()
            else: d.text((70,yy),line,font=f,fill=(206,210,218,255)); yy+=30; line=w
        d.text((70,yy),line,font=f,fill=(206,210,218,255))

def make(spec):
    base,pad=shadow_card(); card=Image.new("RGBA",(W,H),(0,0,0,0))
    accent=THREADS[spec.get("accent","*")][1]
    header(card,spec["type_label"],spec["glyph"],accent)
    scene(card,spec.get("vid"),accent)
    subtitle(card,spec.get("quote"),spec.get("qtag"))
    gag_tag(card,spec.get("gag"))
    for i,c in enumerate(spec.get("left",[])): port_tab(card,"L",i,len(spec["left"]),c)
    rights=spec.get("right",[])
    for i,c in enumerate(rights): port_tab(card,"R",i,len(rights),c,capped=(c=="CAP"))
    footer(card,spec.get("title",""),spec.get("rule",""))
    base.alpha_composite(card,(pad,pad))
    out=Image.new("RGB",base.size,PAPER); out.paste(base,(0,0),base)
    p=PNG/f'{spec["id"]}.png'; out.save(p); return p

# ---- showcase met quote-laag (placeholderregels, KUD-stijl, ORIGINEEL) -------
CARDS=[
 dict(id="01_splice_groen",type_label="Splice",glyph="→",accent="G",vid="HDFaY7Fbi28",
      title="Starfield",left=["G"],right=["G"],qtag="setup",
      quote="Even kijken of dit heelal ook stuk kan."),
 dict(id="02_splice_roze",type_label="Splice",glyph="→",accent="R",vid="1v4XZ8HKemo",
      title="Krols",left=["R"],right=["R"],qtag="setup",
      quote="Het is niet wat het lijkt. Het is erger."),
 dict(id="03_splice_switch_BY",type_label="Splice · kleurwissel",glyph="↘",accent="B",
      vid="v5aZ_qlpP2g",title="Watch Dogs",left=["B"],right=["Y"],qtag="setup",
      quote="Ik hack alles. Behalve mezelf.",
      rule="Wisselt de draad: blauw erin, geel eruit."),
 dict(id="04_splice_switch_GR",type_label="Splice · kleurwissel",glyph="↘",accent="G",
      vid="YYV_xLEXgHg",title="Te laat",left=["G"],right=["R"],qtag="punch",
      quote="Te laat is ook gewoon een tijd.",
      rule="Groen erin, roze eruit."),
 dict(id="05_vertakking",type_label="Vertakking",glyph="Y",accent="Y",vid="5w_lEzZNx_E",
      title="Verrassing!",left=["Y"],right=["Y","Y"],qtag="setup",gag="Konijntje",
      quote="Niemand verwacht het tweede konijntje.",
      rule="De strip splitst: +1 open uiteinde — meer plek om te lozen."),
 dict(id="06_samenkomst",type_label="Samenkomst",glyph="⋎",accent="G",vid="iGBzhqSgJUk",
      title="Mijnwerkers",left=["G","G"],right=["G"],
      quote="Dieper graven loste nog nooit iets op.",
      rule="Voegt twee draden samen: −1 open uiteinde."),
 dict(id="07_einde_roze",type_label="Aftiteling · KOP",glyph="⏹",accent="R",vid="boLkKd3W2sc",
      title="Drama",left=["R"],right=["CAP"],qtag="punch",
      quote="En scène. Niemand klapte.",
      rule="Einde-filmpje: sluit een roze uiteinde af. PUNCHLINE na een OPZET? Gooi 1 extra weg."),
 dict(id="08_einde_blauw",type_label="Aftiteling · KOP",glyph="⏹",accent="B",vid="tMGYPMJJm3o",
      title="Comazuipen",left=["B"],right=["CAP"],qtag="punch",
      quote="Morgen weten we nergens meer van.",
      rule="Einde-filmpje: cap een blauw uiteinde — ook eentje die de ander bouwde."),
 dict(id="09_pilon_wild",type_label="Pilon · wild",glyph="★",accent="*",vid="IpELRbaCzq8",
      title="Politieschets",left=["*"],right=["*"],gag="Pilon",
      quote="Past overal. Net als de pilon.",
      rule="Past op elke kleur."),
]
ACTIONS=[
 dict(id="10_knip",type_label="Actie · KNIP",glyph="✂",accent="*",vid="poJn09Ygm9c",
      title="Gebroken Zwaard",quote="Eén knip en het verhaal valt uiteen.",
      rule="Klik een koord los: +1 open draad van die kleur."),
 dict(id="11_cliffhanger",type_label="Actie · CLIFFHANGER",glyph="!",accent="R",vid="HCagkFYNTeQ",
      title="Fallout",quote="Wordt vervolgd. Of niet. We zien wel.",
      rule="Je tegenstander trekt 2 kaarten."),
 dict(id="12_voorvertoning",type_label="Actie · VOORVERTONING",glyph="◎",accent="B",vid="I0wGiWw_o6I",
      title="Nieuw!",quote="Nieuw! Precies als de vorige keer.",
      rule="Bekijk de top 3; herschik en hou er 1."),
 dict(id="13_herschrijven",type_label="Actie · HERSCHRIJVEN",glyph="⇄",accent="Y",vid="_DIjiWWm9IA",
      title="Assassin's Creed",quote="We schrijven het opnieuw. Niemand merkt het.",
      rule="Bekijk de hand van de ander en ruil 1 kaart."),
 dict(id="14_archief",type_label="Actie · ARCHIEF",glyph="⌕",accent="G",vid="ye_FqUM9sNI",
      title="Rommelmarkten",quote="Alles wat je zoekt ligt al in een doos.",
      rule="Trek 1 en gooi 1 weg."),
]

def make_leader():
    base,pad=shadow_card(); card=Image.new("RGBA",(W,H),(0,0,0,0))
    header(card,"Video-begin · INTRO","▶",THREADS["*"][1])
    scene(card,None,(240,196,46)); d=ImageDraw.Draw(card,"RGBA"); x0,y0,x1,y1=ART
    # grote play-knop (video-startscherm-look)
    cx,cy=(x0+x1)//2,(y0+y1)//2-10
    d.ellipse([cx-78,cy-78,cx+78,cy+78],fill=(255,255,255,40),outline=(255,255,255,235),width=6)
    d.polygon([(cx-26,cy-40),(cx-26,cy+40),(cx+44,cy)],fill=(255,255,255,245))
    d.text((x0+30,y0+24),"KUD — VIDEO BEGINT",font=font(30),fill=(255,255,255,255))
    subtitle(card,"Hier begint de ketting. Klik overal een koord aan.",None)
    port_tab(card,"L",0,1,"G"); port_tab(card,"R",0,1,"R")
    for cx2,c in [(W//2-120,"B"),(W//2+120,"Y")]:
        _,col=THREADS[c]; rrect(d,[cx2-46,138,cx2+46,196],14,fill=col+(255,))
    footer(card,"Video-begin (intro)","Vier open uiteinden — vanaf hier groeit de aflevering.")
    base.alpha_composite(card,(pad,pad))
    out=Image.new("RGB",base.size,PAPER); out.paste(base,(0,0),base)
    p=PNG/"00_leader.png"; out.save(p); return p

def make_anatomy():
    spec=dict(id="_anatomy_base",type_label="Splice",glyph="→",accent="G",vid="HDFaY7Fbi28",
              title="Starfield",left=["G"],right=["G"],qtag="setup",gag="Konijntje",
              quote="Even kijken of dit heelal ook stuk kan.")
    p=make(spec); base=Image.open(p).convert("RGB")
    cv=Image.new("RGB",(base.width+560,base.height),(252,252,250)); cv.paste(base,(0,0))
    d=ImageDraw.Draw(cv); x=base.width-40
    notes=[(150,"Type + glyph: wat de kaart doet"),
           (180,"Running-gag-tag ↺: combo-bron (zie regels)"),
           (300,"Sprocketgaten: filmstrip-look (tape→KUD)"),
           (base.height//2,"MAGNEET-poort: klik hier het gekleurde koord vast. Kleur = verhaaldraad."),
           (base.height-230,"QUOTE-ondertitel + OPZET/PUNCHLINE-tag = de voice/diepgang-laag"),
           (base.height-150,"Titel: de KUD-aflevering op deze scène"),
           (base.height-90,"Regeltekst (alleen special/actie)")]
    d.text((x+40,40),"ANATOMIE VAN EEN KAART (v0.4)",font=font(28),fill=INK); f=font(21,bold=False)
    for i,(yy,t) in enumerate(notes):
        ny=110+i*86; d.line([(x-10,yy),(x+30,ny+10)],fill=(120,124,132),width=3)
        d.ellipse([x-16,yy-6,x-4,yy+6],fill=(220,60,60))
        words=t.split(); line=""; ty=ny
        for w in words:
            if tw(d,(line+" "+w).strip(),f)<=500: line=(line+" "+w).strip()
            else: d.text((x+40,ty),line,font=f,fill=(40,44,52)); ty+=28; line=w
        d.text((x+40,ty),line,font=f,fill=(40,44,52))
    out=PNG/"anatomie.png"; cv.save(out); return out

def contact_sheet(paths):
    cols=4; tw_,th_=560,380; gap=18; rows=(len(paths)+cols-1)//cols
    sheet=Image.new("RGB",(cols*tw_+(cols+1)*gap,rows*th_+(rows+1)*gap),(236,236,232))
    for i,p in enumerate(paths):
        im=Image.open(p).convert("RGB"); im.thumbnail((tw_,th_)); r,c=divmod(i,cols)
        sheet.paste(im,(gap+c*(tw_+gap)+(tw_-im.width)//2,gap+r*(th_+gap)+(th_-im.height)//2))
    out=HERE/"overzicht.png"; sheet.save(out); return out

def main():
    paths=[make_leader()]+[make(s) for s in CARDS+ACTIONS]
    anat=make_anatomy(); sheet=contact_sheet(paths)
    pages=[Image.open(anat).convert("RGB")]
    for i in range(0,len(paths),4):
        grp=[Image.open(p).convert("RGB") for p in paths[i:i+4]]
        pg=Image.new("RGB",(1240,1754),(250,250,248))
        for j,im in enumerate(grp):
            im2=im.copy(); im2.thumbnail((1100,800)); pg.paste(im2,((1240-im2.width)//2,40+j*430))
        pages.append(pg)
    pdf=HERE/"KUD-Doordraaien-concept.pdf"
    pages[0].save(pdf,save_all=True,append_images=pages[1:],resolution=150.0)
    print(f"{len(paths)} kaarten + anatomie · contactvel {sheet.name} · PDF {pdf.name} ({len(pages)} pag.)")

if __name__=="__main__": main()
