#!/usr/bin/env python3
"""
render_kanalen.py — visuele voorbeelden van 'connected art' voor KUD: KANALEN.

Bouwt (a) een VIDEOWAND: KUD-stills als schermen, verbonden via 4-gekleurde kabel-poorten,
en (b) één losse scherm-kaart als detail. Toont hoe willekeurige, totaal verschillende stills
tóch verbinden: de kleur zit in de rand-poort, niet in het beeld.

Alleen Pillow. KUD-beelden (c) Peter Lub — privé prototype.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE=Path(__file__).resolve().parent
ASSETS=HERE.parent.parent/"kud-kudland"/"print"/"assets"
F="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"; FB="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def fo(s,b=True): return ImageFont.truetype(FB if b else F,s)
def tw(d,t,f): l,_,r,_=d.textbbox((0,0),t,font=f); return r-l

# 4 karakterenergieën = de 4 kleuren (kleur + kleurenblind-symbool)
PAL={"G":((54,178,99),"●","Konijntje"),"R":((228,74,153),"◆","Zwoele Man"),
     "B":((52,140,224),"▲","Peter"),"Y":((240,196,46),"★","Pilon")}

STILLS=["HDFaY7Fbi28","ptfF6yhWJ7c","pD9QbAmYUEU","IpELRbaCzq8","v5aZ_qlpP2g",
 "aFLiAI1dnV0","iGBzhqSgJUk","HCagkFYNTeQ","lfsucJq5L7k","HpLDbhAWiG8",
 "5w_lEzZNx_E","I0wGiWw_o6I","_DIjiWWm9IA","boLkKd3W2sc","tMGYPMJJm3o"]

def still(vid,w,h):
    p=ASSETS/f"{vid}.jpg"
    if not p.exists(): return Image.new("RGB",(w,h),(40,44,52))
    im=Image.open(p).convert("RGB"); iw,ih=im.size; s=max(w/iw,h/ih)
    im=im.resize((int(iw*s),int(ih*s)),Image.LANCZOS)
    return im.crop(((im.width-w)//2,(im.height-h)//2,(im.width-w)//2+w,(im.height-h)//2+h))

def screen(canvas,x,y,w,h,vid):
    d=ImageDraw.Draw(canvas)
    d.rounded_rectangle([x-8,y-8,x+w+8,y+h+8],radius=14,fill=(16,18,22))   # bezel
    canvas.paste(still(vid,w,h),(x,y))
    d.rounded_rectangle([x,y,x+w,y+h],radius=4,outline=(8,9,11),width=3)

def nub(d,cx,cy,color,open_=False):
    col,sym,_=PAL[color]
    if open_:
        d.ellipse([cx-22,cy-22,cx+22,cy+22],outline=(255,255,255,180),width=3)
    d.ellipse([cx-16,cy-16,cx+16,cy+16],fill=col,outline=(255,255,255),width=3)
    f=fo(18); d.text((cx-tw(d,sym,f)//2,cy-13),sym,font=f,fill=(255,255,255))

def cable(d,p1,p2,color):
    col=PAL[color][0]; d.line([p1,p2],fill=col,width=11)
    nub(d,p1[0],p1[1],color); nub(d,p2[0],p2[1],color)

def build_wall():
    cols,rows=5,3; w,h=380,280; gx,gy=92,96; mx,top=60,200
    W=mx*2+cols*w+(cols-1)*gx; H=top+rows*h+(rows-1)*gy+70
    cv=Image.new("RGB",(W,H),(244,244,242)); d=ImageDraw.Draw(cv,"RGBA")
    # banner
    d.rounded_rectangle([40,30,W-40,150],radius=18,fill=(20,23,29))
    d.text((64,46),"KUD: KANALEN",font=fo(46),fill=(255,255,255))
    d.text((66,108),"de videowand — zo verbindt de art (kleur zit in de poort, niet in het beeld)",
           font=fo(22,False),fill=(170,174,184))
    lx=W-40-560
    for i,(k,(col,sym,nm)) in enumerate(PAL.items()):
        x=lx+i*140; d.ellipse([x,64,x+30,94],fill=col,outline=(255,255,255),width=2)
        d.text((x+8,66),sym,font=fo(16),fill=(255,255,255)); d.text((x-2,100),nm,font=fo(15,False),fill=(180,184,194))
    def cell(c,r): return mx+c*(w+gx), top+r*(h+gy)
    for r in range(rows):
        for c in range(cols):
            x,y=cell(c,r); screen(cv,x,y,w,h,STILLS[r*cols+c])
    # horizontale kabels (elke rij verbonden)
    for r in range(rows):
        for c in range(cols-1):
            x,y=cell(c,r); col="GRBY"[(r+c)%4]
            cable(d,(x+w,y+h//2),(x+w+gx,y+h//2),col)
    # een paar verticale kabels
    for (c,r,col) in [(1,0,"B"),(3,0,"Y"),(2,1,"R")]:
        x,y=cell(c,r); cable(d,(x+w//2,y+h),(x+w//2,y+h+gy),col)
    # losse OPEN poorten aan de rand (waar je verder kunt bouwen)
    x,y=cell(0,0); nub(d,x-30,y+h//2,"R",open_=True)
    x,y=cell(2,0); nub(d,x+w//2,y-30,"G",open_=True)
    x,y=cell(4,2); nub(d,x+w+30,y+h//2,"Y",open_=True)
    x,y=cell(0,2); nub(d,x+w//2,y+h+30,"B",open_=True)
    d.text((64,H-52),"○ witte ring = OPEN poort: hier mag het volgende scherm aangeklikt worden.",
           font=fo(20,False),fill=(90,90,92))
    out=HERE/"kanalen_wand.png"; cv.save(out); return out

def build_card():
    w,h=820,560; W,H=w+160,h+300
    cv=Image.new("RGB",(W,H),(244,244,242)); d=ImageDraw.Draw(cv,"RGBA")
    x,y=80,80; screen(cv,x,y,w,h,"5w_lEzZNx_E")
    # 3 edge-poorten (smal, op de rand) — art blijft 90%
    nub(d,x-8,y+h//2,"G"); nub(d,x+w+8,y+h//2,"R"); nub(d,x+w//2,y-8,"B")
    # flavor-tekst onder de still (origineel, KUD-stijl)
    d.rounded_rectangle([x,y+h+16,x+w,y+h+96],radius=10,fill=(20,23,29))
    col,sym,nm=PAL["G"]
    d.ellipse([x+16,y+h+34,x+16+34,y+h+68],fill=col,outline=(255,255,255),width=2)
    d.text((x+24,y+h+38),sym,font=fo(20),fill=(255,255,255))
    d.text((x+68,y+h+30),f"{nm} — nog steeds aan het rennen.",font=fo(26),fill=(245,245,247))
    d.text((80,30),"KANAAL-KAART (scherm): de KUD-still vult ~90%, kleur leeft in de edge-poorten.",
           font=fo(22,False),fill=(70,70,72))
    out=HERE/"kanalen_kaart.png"; cv.save(out); return out

if __name__=="__main__":
    print("wand  ->",build_wall().name)
    print("kaart ->",build_card().name)
