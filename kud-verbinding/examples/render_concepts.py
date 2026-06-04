#!/usr/bin/env python3
"""
render_concepts.py — 3 grafische concept-richtingen voor KUD: KANALEN (brief: Joris Maes).
A "RUIS" (lo-fi VHS) · B "DRAGER" (Swiss editorial) · C "STICKER" (riso). Zelfde still, 3 looks.
Alleen Pillow. KUD-beeld (c) Peter Lub — privé prototype.
"""
from pathlib import Path
import random, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE=Path(__file__).resolve().parent
ASSETS=HERE.parent.parent/"kud-kudland"/"print"/"assets"
VID="boLkKd3W2sc"
SANS="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"; SANSB="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO="/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"; MONOB="/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
def fo(path,s): return ImageFont.truetype(path,s)
def tw(d,t,f): l,_,r,_=d.textbbox((0,0),t,font=f); return r-l
W,H=720,960
QUOTE="Konijntje — nog steeds aan het rennen."

def still(w,h):
    p=ASSETS/f"{VID}.jpg"
    if not p.exists(): return Image.new("RGB",(w,h),(40,44,52))
    im=Image.open(p).convert("RGB"); iw,ih=im.size; s=max(w/iw,h/ih)
    im=im.resize((int(iw*s),int(ih*s)),Image.LANCZOS)
    return im.crop(((im.width-w)//2,(im.height-h)//2,(im.width-w)//2+w,(im.height-h)//2+h))

def scanlines(card,box,alpha=60,step=3):
    ov=Image.new("RGBA",card.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
    for y in range(box[1],box[3],step): d.line([(box[0],y),(box[2],y)],fill=(0,0,0,alpha),width=1)
    card.alpha_composite(ov)

# ---------------- A · RUIS (lo-fi VHS) ----------------
def concept_A():
    c=Image.new("RGBA",(W,H),(13,13,13,255)); c.paste(still(W,H),(0,0))
    d=ImageDraw.Draw(c,"RGBA")
    scanlines(c,(0,0,W,H),55,3)
    GR=(57,255,20)
    # signaalbaan (horizontaal, scanline-stripe) op midden
    my=H//2; ov=Image.new("RGBA",c.size,(0,0,0,0)); od=ImageDraw.Draw(ov)
    od.rectangle([0,my-22,W,my-14],fill=GR+(110,)); od.rectangle([0,my+14,W,my+22],fill=GR+(110,))
    od.rectangle([0,my-7,W,my+7],fill=GR+(220,))
    c.alpha_composite(ov)
    # CRT-bezel
    d.rounded_rectangle([0,0,W-1,H-1],radius=22,outline=(42,31,0),width=30)
    d.rounded_rectangle([30,30,W-30,H-30],radius=10,outline=(0,0,0,160),width=4)
    # poort-nops links/rechts op baanhoogte
    for cx,sx in [(20,"⊕"),(W-20,"⊕")]:
        d.ellipse([cx-26,my-26,cx+26,my+26],fill=GR,outline=(255,255,255),width=3)
        d.text((cx-tw(d,"●",fo(SANSB,22))//2,my-15),"●",font=fo(SANSB,22),fill=(13,13,13))
    # VHS-bits
    d.text((44,40),"▶ PLAY",font=fo(MONOB,24),fill=(230,230,210,210))
    d.text((W-150,40),"SP  0:14",font=fo(MONO,22),fill=(230,230,210,180))
    # flavor-balk met scanlines
    by=int(H*0.82); d.rectangle([30,by,W-30,H-30],fill=(13,13,13,235)); scanlines(c,(30,by,W-30,H-30),70,3)
    d.text((48,by+18),"● KONIJNTJE",font=fo(MONOB,20),fill=GR)
    d.text((48,by+52),"NOG STEEDS AAN HET RENNEN.",font=fo(MONOB,26),fill=(232,232,208))
    return c.convert("RGB")

# ---------------- B · DRAGER (Swiss editorial) ----------------
def concept_B():
    c=Image.new("RGBA",(W,H),(245,240,232,255)); d=ImageDraw.Draw(c,"RGBA")
    GR=(60,180,75); BLK=(26,26,26)
    d.text((40,30),"KONIJNTJE",font=fo(SANSB,46),fill=BLK)
    d.text((40,86),"●",font=fo(SANSB,30),fill=GR)
    # still met harde zwarte rand
    sx,sy,sw,sh=40,150,W-80,620
    c.paste(still(sw,sh),(sx,sy)); d.rectangle([sx-8,sy-8,sx+sw+8,sy+sh+8],outline=BLK,width=8)
    # signaalbaan: enkele lijn + zwarte outline op midden still
    my=sy+sh//2
    d.line([(sx-8,my),(sx+sw+8,my)],fill=BLK,width=10); d.line([(sx-8,my),(sx+sw+8,my)],fill=GR,width=6)
    for cx in (sx-8,sx+sw+8):  # vierkante poorten in de rand
        d.rectangle([cx-12,my-12,cx+12,my+12],fill=GR,outline=BLK,width=2)
    # flavor onderaan, lowercase, rechts
    f=fo(SANS,24); t="nog steeds aan het rennen."
    d.text((W-40-tw(d,t,f),H-70),t,font=f,fill=BLK)
    d.text((40,H-72),"SIG-017",font=fo(SANS,18),fill=(120,120,120))
    d.rectangle([0,0,W-1,H-1],outline=BLK,width=4)
    return c.convert("RGB")

# ---------------- C · STICKER (riso) ----------------
def halftone(card,box,col,alpha=40,step=10):
    ov=Image.new("RGBA",card.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
    for y in range(box[1],box[3],step):
        for x in range(box[0],box[2],step): d.ellipse([x,y,x+2,y+2],fill=col+(alpha,))
    card.alpha_composite(ov)
def concept_C():
    c=Image.new("RGBA",(W,H),(255,251,240,255)); d=ImageDraw.Draw(c,"RGBA")
    OR=(255,107,53); GR=(92,187,142)
    halftone(c,(0,0,W,H),OR,26,12)
    d.rounded_rectangle([12,12,W-12,H-12],radius=20,outline=OR,width=10)
    # still als opgeplakte sticker met schaduw + witte rand
    sx,sy,sw,sh=70,150,W-140,560
    sh_off=Image.new("RGBA",c.size,(0,0,0,0)); ImageDraw.Draw(sh_off).rounded_rectangle([sx+10,sy+14,sx+sw+22,sy+sh+26],radius=14,fill=(0,0,0,70))
    c.alpha_composite(sh_off.filter(ImageFilter.GaussianBlur(8)))
    d.rounded_rectangle([sx-14,sy-14,sx+sw+14,sy+sh+14],radius=14,fill=(255,255,255,255))
    c.paste(still(sw,sh),(sx,sy))
    # brushy tape-baan, licht gedraaid
    my=sy+sh//2; tape=Image.new("RGBA",(W,120),(0,0,0,0)); td=ImageDraw.Draw(tape)
    td.rounded_rectangle([0,40,W,80],radius=8,fill=GR+(180,))
    for i in range(0,W,14): td.ellipse([i,36,i+8,44],fill=GR+(120,)); td.ellipse([i,76,i+8,84],fill=GR+(120,))
    tape=tape.rotate(-3,expand=False,center=(W//2,60)); c.alpha_composite(tape,(0,my-60))
    # ronde sticker-poorten met peel-schaduw
    for cx in (40,W-40):
        d.ellipse([cx-30,my-22,cx+34,my+38],fill=(0,0,0,50))
        d.ellipse([cx-26,my-26,cx+26,my+26],fill=GR,outline=(255,255,255),width=4)
        d.text((cx-tw(d,'●',fo(SANSB,22))//2,my-15),"●",font=fo(SANSB,22),fill=(255,255,255))
    # energie-badge (wit ovaal)
    d.ellipse([40,60,250,128],fill=(255,255,255),outline=GR,width=5); d.text((78,76),"Konijntje",font=fo(SANSB,30),fill=(26,10,0))
    d.text((70,H-90),"nog steeds aan het rennen.",font=fo(SANS,26),fill=(26,10,0))
    return c.convert("RGB")

def board():
    cards=[("A · RUIS","lo-fi VHS-grunge  —  AANRADER van Joris",concept_A()),
           ("B · DRAGER","Swiss editorial / grid",concept_B()),
           ("C · STICKER","riso / speels / handgemaakt",concept_C())]
    gap=60; mar=50; bw=W; BW=mar*2+3*bw+2*gap; BH=170+H+150
    bd=Image.new("RGB",(BW,BH),(238,238,236)); d=ImageDraw.Draw(bd)
    d.rounded_rectangle([40,30,BW-40,140],radius=16,fill=(20,23,29))
    d.text((64,46),"KUD: KANALEN — grafische concepten",font=fo(SANSB,42),fill=(255,255,255))
    d.text((66,104),"drie verbeterde richtingen door vormgever Joris Maes (zelfde still, andere grafische taal)",font=fo(SANS,22),fill=(170,174,184))
    for i,(name,mood,card) in enumerate(cards):
        x=mar+i*(bw+gap); y=170
        bd.paste(card,(x,y)); d.rectangle([x,y,x+bw,y+H],outline=(40,40,42),width=2)
        d.text((x,y+H+16),name,font=fo(SANSB,30),fill=(20,20,22))
        d.text((x,y+H+58),mood,font=fo(SANS,22),fill=(90,90,92))
    out=HERE/"concepten.png"; bd.save(out); return out

if __name__=="__main__":
    print("->",board().name)
