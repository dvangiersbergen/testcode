#!/usr/bin/env python3
"""
render_flow.py — mock van de art-richting "HET SIGNAAL": KUD-beelden die visueel DOORLOPEN
over de kaartranden, net als Tapeworms worm + aarde.

Twee doorlopende lagen (zoals Tapeworm: grond + worm):
  1) GROND — een doorlopende 'kapotte kabel-grond'-rand om elke kaart; raakt de buurkaart op elke
     rand → basis-continuïteit overal (zoals Tapeworms aarde).
  2) SIGNAAL — een gekleurde storings-/kabelbaan die elke rand op een VAST kruispunt (midden) kruist
     en zo NAADLOOS van kaart naar kaart vloeit (de worm-equivalent). Kleur = verbindingskleur.
De KUD-still is de 'uitzending' eronder. Alleen Pillow. KUD-beelden (c) Peter Lub — privé prototype.
"""
from pathlib import Path
import random
from PIL import Image, ImageDraw, ImageFont

HERE=Path(__file__).resolve().parent
ASSETS=HERE.parent.parent/"kud-kudland"/"print"/"assets"
F="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"; FB="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def fo(s,b=True): return ImageFont.truetype(FB if b else F,s)

GROUND=(150,98,55); GROUND_D=(120,76,40); ROZE=(228,120,170)
PAL={"R":((228,74,153),"◆")}

def still(vid,w,h):
    p=ASSETS/f"{vid}.jpg"
    if not p.exists(): return Image.new("RGB",(w,h),(40,44,52))
    im=Image.open(p).convert("RGB"); iw,ih=im.size; s=max(w/iw,h/ih)
    im=im.resize((int(iw*s),int(ih*s)),Image.LANCZOS)
    return im.crop(((im.width-w)//2,(im.height-h)//2,(im.width-w)//2+w,(im.height-h)//2+h))

def card(cv,x,y,w,h,vid,rng):
    d=ImageDraw.Draw(cv)
    d.rounded_rectangle([x,y,x+w,y+h],radius=16,fill=GROUND)           # doorlopende grond
    for _ in range(70):                                               # speckle
        sx,sy=rng.randint(x+6,x+w-6),rng.randint(y+6,y+h-6)
        d.ellipse([sx,sy,sx+3,sy+3],fill=GROUND_D)
    b=34; cv.paste(still(vid,w-2*b,h-2*b),(x+b,y+b))                  # still als 'uitzending'
    d.rounded_rectangle([x+b,y+b,x+w-b,y+h-b],radius=4,outline=(20,14,8),width=3)
    d.rounded_rectangle([x,y,x+w,y+h],radius=16,outline=(70,46,24),width=2)

def band(cv,pts,col,wd=84):
    ov=Image.new("RGBA",cv.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
    for a,b in zip(pts,pts[1:]): d.line([a,b],fill=col+(170,),width=wd)
    for p in pts: d.ellipse([p[0]-wd//2,p[1]-wd//2,p[0]+wd//2,p[1]+wd//2],fill=col+(170,))
    for a,b in zip(pts,pts[1:]): d.line([a,b],fill=(255,255,255,90),width=wd//3)
    cv.alpha_composite(ov)

def nub(d,cx,cy,col,sym,open_=False):
    if open_: d.ellipse([cx-26,cy-26,cx+26,cy+26],outline=(255,255,255,200),width=3)
    d.ellipse([cx-18,cy-18,cx+18,cy+18],fill=col,outline=(255,255,255),width=3)
    f=fo(20); l,_,r,_=d.textbbox((0,0),sym,font=f); d.text((cx-(r-l)//2,cy-14),sym,font=f,fill=(255,255,255))

def main():
    rng=random.Random(7)
    W,H=1320,1000
    cv=Image.new("RGBA",(W,H),(34,28,24,255)); d=ImageDraw.Draw(cv)
    d.rounded_rectangle([30,24,W-30,128],radius=16,fill=(20,23,29,255))
    d.text((54,40),"HET SIGNAAL",font=fo(42),fill=(255,255,255))
    d.text((56,100),"de KUD-beelden lopen door over de randen — grond + gekleurde signaalbaan, net als Tapeworm",
           font=fo(21,False),fill=(170,174,184))
    w,h,g=380,400,6; x1,y1=70,170
    C1=(x1,y1); C2=(x1+w+g,y1); C3=(x1+w+g,y1+h+g)                    # L-vorm (bocht, zoals de foto)
    for (x,y),v in [(C1,"boLkKd3W2sc"),(C2,"tMGYPMJJm3o"),(C3,"5w_lEzZNx_E")]:
        card(cv,x,y,w,h,v,rng)
    # SIGNAAL-baan: kruist randen op VASTE middenpunten -> naadloze flow
    my=y1+h//2; cxC2=C2[0]+w//2
    pts=[(x1-40,my),(cxC2,my),(cxC2,y1+2*h+g+40)]
    band(cv,pts,ROZE)
    # poort-noppen op de kruispunten (de 4-kleur-logica blijft op de rand)
    col,sym=PAL["R"]
    d=ImageDraw.Draw(cv)
    nub(d,C2[0],my,col,sym)                       # naad C1|C2
    nub(d,cxC2,C3[1],col,sym)                      # naad C2|C3
    nub(d,x1-40,my,col,sym,open_=True)            # open uiteinde links
    nub(d,cxC2,y1+2*h+g+40,col,sym,open_=True)    # open uiteinde onder
    d.text((54,H-44),"Vast kruispunt per rand (1 baan) = elke kaart sluit op elke kaart aan. Kleur blijft in de poort-nop.",
           font=fo(19,False),fill=(150,150,152))
    out=HERE/"flow_mock.png"; cv.convert("RGB").save(out); print("->",out.name)

if __name__=="__main__": main()
