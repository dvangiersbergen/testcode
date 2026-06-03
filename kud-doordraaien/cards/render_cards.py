#!/usr/bin/env python3
"""
render_cards.py — concept cards voor KUD: DOORDRAAIEN (v0.7: old-school YouTube-skin).

Layout per kaart:
  - bovenbalk met een HOMAGE aan het oude YouTube-logo (parodie, privégebruik) + speltype.
  - de scène-art als VIDEOSPELER (rode voortgangsbalk, play, tijd, logo-watermerk).
  - de KUD-aflevering als videotitel + nep-statistieken (weergaven / jaren geleden).
  - de QUOTE als REACTIE: random (verzonnen) gebruikersnaam + identicon-avatar + up/down votes.
  - spelfuncties blijven: magneet-poorten (koord-kleuren), type-glyph, running-gag-tag.

Quoteregels en gebruikersnamen zijn ORIGINEEL/fictief — geen echte serie-citaten of echte personen.
Gebruikt de KUD-thumbnails uit ../../kud-kudland/print/assets/. Alleen Pillow.
"""
from __future__ import annotations
import csv, hashlib, random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE=Path(__file__).resolve().parent
ASSETS=HERE.parent.parent/"kud-kudland"/"print"/"assets"
MANIFEST=HERE.parent.parent/"kud-kudland"/"framework"/"data"/"manifest.csv"
PNG=HERE/"png"; PNG.mkdir(exist_ok=True)

F="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"; FB="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
_fc={}
def font(s,b=True):
    k=(s,b)
    if k not in _fc: _fc[k]=ImageFont.truetype(FB if b else F,s)
    return _fc[k]
def tw(d,t,f): l,_,r,_=d.textbbox((0,0),t,font=f); return r-l

THREADS={"G":("GROEN",(54,178,99)),"R":("ROZE",(228,74,153)),"B":("BLAUW",(52,140,224)),
         "Y":("GEEL",(240,196,46)),"*":("WILD",(170,174,186))}
QTAG={"setup":("OPZET",(52,140,224)),"punch":("PUNCHLINE",(228,74,153))}
YT=(197,32,31); INK=(17,17,17); GREY=(99,99,99); LINE=(228,228,228)

NAMES=["KonijntjeFan2008","xX_DjingleDjengle_Xx","henk_de_3e","Roze4Lyfe","gamer_joost92",
 "anoniempje","PilonLover","ZwoeleMan68","kudsuperfan","mariekeNL","de_echte_groene",
 "wiebe_dr1nkt","TrampolineTim","cleeuwn_haat","walvis_werner","subscribe_pls","epicgamer2011",
 "nostalgiekindje","eerste_reactie","papegaai_praatt","koe_vliegtt","albatros_anna","putjes_piet",
 "seizoen1_isbeter","viewer_van_toen","kud_tot_ik_doodga","nietmachien","gola_gola_gola",
 "comazuipertje","ridder_zonder_zwaard"]

titles={}
if MANIFEST.exists():
    for r in csv.DictReader(MANIFEST.open(encoding="utf-8")): titles[r["videoId"]]=r["title"]

W,H=1120,760
VB=(104,128,W-104,466)        # videospeler — met zijmarges (gutters) voor de connectors

def rng_for(cid): return random.Random(int(hashlib.md5(cid.encode()).hexdigest(),16))
def rrect(d,b,r,**k): d.rounded_rectangle(b,radius=r,**k)
def fmt(n):
    s=str(n); out=""
    while len(s)>3: out="."+s[-3:]+out; s=s[:-3]
    return s+out

def shadow_card():
    pad=40
    base=Image.new("RGBA",(W+2*pad,H+2*pad),(0,0,0,0))
    sh=Image.new("RGBA",base.size,(0,0,0,0)); ds=ImageDraw.Draw(sh)
    ds.rounded_rectangle([pad+10,pad+16,pad+W+10,pad+H+16],radius=30,fill=(0,0,0,90))
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(15)))
    card=Image.new("RGBA",(W,H),(255,255,255,255)); d=ImageDraw.Draw(card)
    rrect(d,[2,2,W-3,H-3],26,outline=LINE+(255,),width=3)
    base.alpha_composite(card,(pad,pad)); return base,pad

def yt_logo(d,x,y):
    f=font(42); d.text((x,y),"You",font=f,fill=(28,28,28,255)); w=tw(d,"You",f)
    bx=x+w+6; f2=font(36); wt=tw(d,"Tube",f2)
    rrect(d,[bx,y+3,bx+wt+26,y+49],10,fill=YT+(255,))
    d.text((bx+13,y+5),"Tube",font=f2,fill=(255,255,255,255))
    return bx+wt+26

def type_badge(d,type_label,glyph,accent):
    gx=W-104-62; d.ellipse([gx,48,gx+62,110],fill=accent+(255,))
    g=font(36); d.text((gx+31-tw(d,glyph,g)//2,62),glyph,font=g,fill=(20,22,28,255))
    t=type_label.upper(); f=font(24); wt=tw(d,t,f)
    x1=gx-14; x0=x1-(wt+28)
    rrect(d,[x0,56,x1,102],10,fill=(28,28,28,255)); d.text((x0+14,64),t,font=f,fill=(255,255,255,255))

def player(card,vid,big_play=False):
    d=ImageDraw.Draw(card,"RGBA"); x0,y0,x1,y1=VB
    d.rectangle([x0,y0,x1,y1],fill=(8,8,9,255))
    if vid and (ASSETS/f"{vid}.jpg").exists():
        im=Image.open(ASSETS/f"{vid}.jpg").convert("RGB"); iw,ih=im.size
        tw_,th_=x1-x0,y1-y0; s=max(tw_/iw,th_/ih)
        im=im.resize((int(iw*s),int(ih*s)),Image.LANCZOS)
        im=im.crop(((im.width-tw_)//2,(im.height-th_)//2,(im.width-tw_)//2+tw_,(im.height-th_)//2+th_))
        card.paste(im,(x0,y0))
    r=rng_for((vid or "")+"plr")
    if big_play:
        cx,cy=(x0+x1)//2,(y0+y1)//2-6
        d.ellipse([cx-70,cy-70,cx+70,cy+70],fill=(255,255,255,45),outline=(255,255,255,235),width=6)
        d.polygon([(cx-24,cy-36),(cx-24,cy+36),(cx+40,cy)],fill=(255,255,255,245))
    # controls-strip donker
    d.rectangle([x0,y1-46,x1,y1],fill=(0,0,0,150))
    by=y1-14
    d.rectangle([x0+14,by,x1-14,by+5],fill=(120,120,120,255))
    pct=r.uniform(.18,.8); px=x0+14+(x1-x0-28)*pct
    d.rectangle([x0+14,by,px,by+5],fill=YT+(255,)); d.ellipse([px-7,by-4,px+7,by+10],fill=YT+(255,))
    d.polygon([(x0+18,by-26),(x0+18,by-8),(x0+34,by-17)],fill=(255,255,255,235))
    m1,s1=r.randint(0,3),r.randint(0,59); m2,s2=m1+r.randint(1,5),r.randint(0,59)
    d.text((x0+46,by-30),f"{m1}:{s1:02d} / {m2}:{s2:02d}",font=font(19),fill=(235,235,235,255))
    # logo-watermerk (oude YT-bug) rechtsonder
    wb=x1-92; wy=by-44
    rrect(d,[wb,wy,wb+72,wy+34],8,fill=YT+(230,))
    d.polygon([(wb+27,wy+9),(wb+27,wy+25),(wb+46,wy+17)],fill=(255,255,255,245))

def identicon(card,x,y,s,r):
    d=ImageDraw.Draw(card)
    col=(r.randint(30,205),r.randint(30,205),r.randint(30,205))
    rrect(d,[x,y,x+s,y+s],14,fill=(238,238,238,255))
    inner=s-16; cell=inner/5
    for gx in range(3):
        for gy in range(5):
            if r.random()<0.5:
                for cxg in {gx,4-gx}:
                    bx=x+8+cxg*cell; byy=y+8+gy*cell
                    d.rectangle([bx,byy,bx+cell,byy+cell],fill=col)

def chip(d,x,y,label,col,txtcol=(255,255,255)):
    f=font(18); w=tw(d,label,f)
    rrect(d,[x,y,x+w+22,y+30],8,fill=col+(255,)); d.text((x+11,y+5),label,font=f,fill=txtcol+(255,))
    return x+w+22

def comment_block(card,spec):
    d=ImageDraw.Draw(card,"RGBA"); r=rng_for(spec["id"]); L=104
    quote=spec.get("quote",""); pinned=spec.get("pinned")
    # videotitel + stats
    title=spec.get("title",""); f=font(33); t=title if len(title)<=40 else title[:39]+"…"
    d.text((L,476),t,font=f,fill=INK+(255,))
    views=r.randint(8000,3500000); yrs=r.randint(7,14)
    d.text((L,522),f"KUD ✓ · {fmt(views)} weergaven · {yrs} jaar geleden",font=font(21,False),fill=GREY+(255,))
    rule=spec.get("rule","")
    cy=562
    if rule:
        f=font(20,False); rt=rule
        while tw(d,rt,f)>W-2*L and len(rt)>8: rt=rt[:-2]
        if rt!=rule: rt=rt.rstrip()+"…"
        d.text((L,558),rt,font=f,fill=(120,120,120,255)); cy=592
    d.line([(L,cy),(W-L,cy)],fill=LINE+(255,),width=2); cy+=14
    ax=L; nx=L+92
    if pinned:
        d.text((nx,cy-2),"▦ Vastgezet door KUD",font=font(17,False),fill=GREY+(255,)); cy+=22
    name = "KUD ✓" if pinned else NAMES[r.randrange(len(NAMES))]
    identicon(card,ax,cy,72,r)
    f=font(25); d.text((nx,cy),name,font=f,fill=INK+(255,)); xx=nx+tw(d,name,f)+14
    qt=spec.get("qtag")
    if qt: lbl,col=QTAG[qt]; xx=chip(d,xx,cy+2,lbl,col)+10
    if spec.get("gag"): xx=chip(d,xx,cy+2,"↺ "+spec["gag"],(245,196,46),(28,28,28))+10
    d.text((xx,cy+3),f"· {r.randint(1,11)} jr",font=font(18,False),fill=GREY+(255,))
    # comment-tekst (= de quote)
    f=font(25,False); maxw=W-nx-L; words=quote.split(); line=""; yy=cy+38
    for w in words:
        if tw(d,(line+" "+w).strip(),f)<=maxw: line=(line+" "+w).strip()
        else: d.text((nx,yy),line,font=f,fill=(35,35,35,255)); yy+=32; line=w
    if quote: d.text((nx,yy),line,font=f,fill=(35,35,35,255)); yy+=40
    # votes
    f=font(20,False)
    d.text((nx,yy),"▲",font=font(20),fill=GREY+(255,))
    d.text((nx+28,yy),fmt(r.randint(40,9900)),font=f,fill=GREY+(255,))
    d.text((nx+150,yy),"▼",font=font(20),fill=GREY+(255,))
    d.text((nx+210,yy),"Beantwoorden",font=f,fill=GREY+(255,))

def make(spec,big_play=False):
    base,pad=shadow_card(); card=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(card,"RGBA")
    accent=THREADS[spec.get("accent","*")][1]
    yt_logo(d,104,52)
    type_badge(d,spec["type_label"],spec["glyph"],accent)
    player(card,spec.get("vid"),big_play)
    d.rectangle([VB[0],VB[1],VB[2],VB[3]],outline=accent+(255,),width=4)
    comment_block(card,spec)
    for i,c in enumerate(spec.get("left",[])): port_tab(card,"L",i,len(spec["left"]),c)
    rights=spec.get("right",[])
    for i,c in enumerate(rights): port_tab(card,"R",i,len(rights),c,capped=(c=="CAP"))
    base.alpha_composite(card,(pad,pad))
    out=Image.new("RGB",base.size,(247,247,245)); out.paste(base,(0,0),base)
    p=PNG/f'{spec["id"]}.png'; out.save(p); return p

def port_tab(card,side,idx,total,color,capped=False):
    """Schone koord-socket in de zijmarge: gekleurd plaatje (= koordkleur) + metalen magneet."""
    d=ImageDraw.Draw(card,"RGBA")
    top,bot=VB[1],VB[3]
    cy=int(top+(bot-top)*(idx+1)/(total+1))      # netjes verdeeld over de videohoogte
    ph=66; pw=44
    if side=="L": box=[0,cy-ph//2,pw,cy+ph//2]; mx=pw-15
    else: box=[W-pw,cy-ph//2,W,cy+ph//2]; mx=W-pw+15
    if capped or color=="CAP":
        rrect(d,box,12,fill=(124,128,136,255))
        d.text((mx-tw(d,"■",font(26))//2,cy-15),"■",font=font(26),fill=(245,245,247,255)); return
    _,col=THREADS[color]
    rrect(d,box,12,fill=col+(255,))
    d.ellipse([mx-12,cy-12,mx+12,cy+12],fill=(239,239,241,255),outline=(108,112,120,255),width=3)
    d.ellipse([mx-4,cy-4,mx+4,cy+4],fill=(92,96,104,255))

# ---- showcase ---------------------------------------------------------------
CARDS=[
 dict(id="01_splice_groen",type_label="Splice",glyph="→",accent="G",vid="HDFaY7Fbi28",
      title="Kud - Starfield",left=["G"],right=["G"],qtag="setup",
      quote="Even kijken of dit heelal ook stuk kan."),
 dict(id="02_splice_roze",type_label="Splice",glyph="→",accent="R",vid="1v4XZ8HKemo",
      title="Kud - Krols",left=["R"],right=["R"],qtag="setup",
      quote="Het is niet wat het lijkt. Het is erger."),
 dict(id="03_splice_switch_BY",type_label="Splice · kleurwissel",glyph="↘",accent="B",
      vid="v5aZ_qlpP2g",title="Kud - Watch Dogs",left=["B"],right=["Y"],qtag="setup",
      quote="Ik hack alles. Behalve mezelf.",rule="Wisselt de draad: blauw erin, geel eruit."),
 dict(id="04_splice_switch_GR",type_label="Splice · kleurwissel",glyph="↘",accent="G",
      vid="YYV_xLEXgHg",title="Kud - Te laat",left=["G"],right=["R"],qtag="punch",
      quote="Te laat is ook gewoon een tijd.",rule="Groen erin, roze eruit."),
 dict(id="05_vertakking",type_label="Vertakking",glyph="Y",accent="Y",vid="5w_lEzZNx_E",
      title="Kud - Verrassing!",left=["Y"],right=["Y","Y"],qtag="setup",gag="Konijntje",
      quote="Niemand verwacht het tweede konijntje.",rule="De strip splitst: +1 open uiteinde."),
 dict(id="06_samenkomst",type_label="Samenkomst",glyph="⋎",accent="G",vid="iGBzhqSgJUk",
      title="Kud - Mijnwerkers",left=["G","G"],right=["G"],
      quote="Dieper graven loste nog nooit iets op.",rule="Voegt twee draden samen: −1 open uiteinde."),
 dict(id="07_einde_roze",type_label="Aftiteling · KOP",glyph="⏹",accent="R",vid="boLkKd3W2sc",
      title="Kud - Drama",left=["R"],right=["CAP"],qtag="punch",
      quote="En scène. Niemand klapte.",rule="Einde-filmpje: sluit een roze uiteinde af."),
 dict(id="08_einde_blauw",type_label="Aftiteling · KOP",glyph="⏹",accent="B",vid="tMGYPMJJm3o",
      title="Kud - Comazuipen",left=["B"],right=["CAP"],qtag="punch",
      quote="Morgen weten we nergens meer van.",rule="Einde-filmpje: cap een blauw uiteinde."),
 dict(id="09_pilon_wild",type_label="Pilon · wild",glyph="★",accent="*",vid="IpELRbaCzq8",
      title="Kud - Politieschets",left=["*"],right=["*"],gag="Pilon",
      quote="Past overal. Net als de pilon.",rule="Past op elke kleur."),
]
ACTIONS=[
 dict(id="10_knip",type_label="Actie · KNIP",glyph="✂",accent="*",vid="poJn09Ygm9c",
      title="Kud - Gebroken Zwaard",quote="Eén knip en het verhaal valt uiteen.",
      rule="Klik een koord los: +1 open uiteinde van die kleur."),
 dict(id="11_cliffhanger",type_label="Actie · CLIFFHANGER",glyph="!",accent="R",vid="HCagkFYNTeQ",
      title="Kud - Fallout",quote="Wordt vervolgd. Of niet. We zien wel.",
      rule="Je tegenstander trekt 2 kaarten."),
 dict(id="12_voorvertoning",type_label="Actie · VOORVERTONING",glyph="◎",accent="B",vid="I0wGiWw_o6I",
      title="Kud - Nieuw!",quote="Nieuw! Precies als de vorige keer.",rule="Bekijk de top 3; hou er 1."),
 dict(id="13_herschrijven",type_label="Actie · HERSCHRIJVEN",glyph="⇄",accent="Y",vid="_DIjiWWm9IA",
      title="Kud - Assassin's Creed",quote="We schrijven het opnieuw. Niemand merkt het.",
      rule="Bekijk de hand van de ander en ruil 1 kaart."),
 dict(id="14_archief",type_label="Actie · ARCHIEF",glyph="⌕",accent="G",vid="ye_FqUM9sNI",
      title="Kud - Rommelmarkten",quote="Alles wat je zoekt ligt al in een doos.",
      rule="Trek 1 en gooi 1 weg."),
]

def make_leader():
    spec=dict(id="00_leader",type_label="Video-begin · INTRO",glyph="▶",accent="*",vid=None,
              title="Kud - INTRO (de aflevering begint)",left=["G"],right=["R"],
              pinned=True,quote="Hier begint de ketting. Klik overal een koord aan.",
              rule="Starttegel: vier open uiteinden — vanaf hier groeit de aflevering.")
    # top/onder extra kleuren tonen we via de tekst; links/rechts G/R poorten
    return make(spec,big_play=True)

def make_anatomy():
    p=make(dict(id="_anatomy_base",type_label="Splice",glyph="→",accent="G",vid="HDFaY7Fbi28",
        title="Kud - Starfield",left=["G"],right=["G"],qtag="setup",gag="Konijntje",
        quote="Even kijken of dit heelal ook stuk kan."))
    base=Image.open(p).convert("RGB")
    cv=Image.new("RGB",(base.width+560,base.height),(252,252,250)); cv.paste(base,(0,0)); d=ImageDraw.Draw(cv)
    x=base.width-40
    notes=[(80,"Homage oud YouTube-logo (parodie, privégebruik)"),(80,"Speltype + glyph"),
           (300,"Scène = videospeler: rode balk, play, tijd, logo-watermerk"),
           ((base.height)//2,"Magneet-poort: klik hier het gekleurde koord vast"),
           (base.height-260,"Videotitel = de KUD-aflevering + nep-stats"),
           (base.height-150,"QUOTE = reactie: random kijkernaam + identicon + up/down")]
    d.text((x+40,40),"ANATOMIE (v0.7 — YouTube-skin)",font=font(28),fill=INK); f=font(21,False)
    for i,(yy,t) in enumerate(notes):
        ny=120+i*92; d.line([(x-10,yy),(x+30,ny+10)],fill=(120,124,132),width=3)
        d.ellipse([x-16,yy-6,x-4,yy+6],fill=(220,60,60))
        words=t.split(); line=""; ty=ny
        for w in words:
            if tw(d,(line+" "+w).strip(),f)<=500: line=(line+" "+w).strip()
            else: d.text((x+40,ty),line,font=f,fill=(40,44,52)); ty+=28; line=w
        d.text((x+40,ty),line,font=f,fill=(40,44,52))
    out=PNG/"anatomie.png"; cv.save(out); return out

def contact_sheet(paths):
    cols=4; tw_,th_=560,400; gap=18; rows=(len(paths)+cols-1)//cols
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
            im2=im.copy(); im2.thumbnail((1100,820)); pg.paste(im2,((1240-im2.width)//2,40+j*430))
        pages.append(pg)
    pdf=HERE/"KUD-Doordraaien-concept.pdf"
    pages[0].save(pdf,save_all=True,append_images=pages[1:],resolution=150.0)
    print(f"{len(paths)} kaarten · contactvel {sheet.name} · PDF {pdf.name} ({len(pages)} pag.)")

if __name__=="__main__": main()
