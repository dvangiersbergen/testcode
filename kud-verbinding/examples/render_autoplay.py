#!/usr/bin/env python3
"""
render_autoplay.py — KUD: AUTOPLAY (scene chaining op de YouTube-kaart).
Rendert: een hero-kaart (met fase-chapter + connectors + karakter-tags + een praatwolk),
een 4-kaart-tijdlijn (Opzet->Opbouw->Punchline->Nasleep), en 2 wolk-kaartjes.
Alleen Pillow. KUD-beelden (c) Peter Lub — privé prototype.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
HERE=Path(__file__).resolve().parent
ASSETS=HERE.parent.parent/"kud-kudland"/"print"/"assets"
SANS="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"; SANSB="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def fo(s,b=True): return ImageFont.truetype(SANSB if b else SANS,s)
def tw(d,t,f): l,_,r,_=d.textbbox((0,0),t,font=f); return r-l
YT=(197,32,31); INK=(20,20,20); GREY=(110,110,110)
PHASE={"OPZET":(47,168,74),"OPBOUW":(58,123,213),"PUNCHLINE":(226,74,160),"NASLEEP":(138,109,84)}
ORDER=["OPZET","OPBOUW","PUNCHLINE","NASLEEP"]
CHAR={"K":((47,168,74),"●","Konijntje"),"Z":((226,74,160),"◆","Zwoele Man"),
      "P":((58,123,213),"▲","Peter"),"L":((240,196,46),"★","Pilon")}

def still(vid,w,h):
    p=ASSETS/f"{vid}.jpg"
    if not p.exists(): return Image.new("RGB",(w,h),(40,44,52))
    im=Image.open(p).convert("RGB"); iw,ih=im.size; s=max(w/iw,h/ih)
    im=im.resize((int(iw*s),int(ih*s)),Image.LANCZOS)
    return im.crop(((im.width-w)//2,(im.height-h)//2,(im.width-w)//2+w,(im.height-h)//2+h))

def video(card,x,y,w,h,vid,phase,chapterlbl=True):
    d=ImageDraw.Draw(card,"RGBA")
    d.rectangle([x,y,x+w,y+h],fill=(8,8,9)); card.paste(still(vid,w,h),(x,y))
    d.rectangle([x,y+h-40,x+w,y+h],fill=(0,0,0,150))
    by=y+h-13; d.rectangle([x+12,by,x+w-12,by+5],fill=(120,120,120))
    pcol=PHASE[phase]; px=x+12+int((x+w-24-(x+12))*0.62)
    d.rectangle([x+12,by,px,by+5],fill=YT); d.ellipse([px-6,by-4,px+6,by+9],fill=YT)
    # chapter-marker (= de fase) op de balk
    d.ellipse([px-9,by-9,px+9,by+9],outline=pcol,width=4)
    if chapterlbl:
        d.polygon([(x+18,by-26),(x+18,by-10),(x+32,by-18)],fill=(255,255,255))
        d.text((x+44,by-30),phase,font=fo(18),fill=pcol)
    d.rectangle([x,y,x+w,y+h],outline=pcol,width=5)

def connector(d,x,y,color,label,side):
    pw,ph=42,70; box=[x-pw,y-ph//2,x,y+ph//2] if side=="L" else [x,y-ph//2,x+pw,y+ph//2]
    d.rounded_rectangle(box,radius=10,fill=color)
    cx=(box[0]+box[2])//2; d.ellipse([cx-9,y-9,cx+9,y+9],fill=(255,255,255))
    f=fo(17)
    if side=="L": d.text((x+12,y-30),"volgt op",font=fo(14,False),fill=GREY); d.text((x+12,y-10),label,font=f,fill=color)
    else: t1="leidt tot"; d.text((x-12-tw(d,t1,fo(14,False)),y-30),t1,font=fo(14,False),fill=GREY); d.text((x-12-tw(d,label,f),y-10),label,font=f,fill=color)

def bubble(card,x,y,kind,char,text):
    d=ImageDraw.Draw(card,"RGBA"); col,sym,nm=CHAR[char]
    f=fo(24); w=tw(d,text,f)+90; h=84
    if kind=="praat":
        d.rounded_rectangle([x,y,x+w,y+h],radius=16,fill=(255,255,255),outline=(20,20,20),width=4)
        d.polygon([(x+50,y+h-2),(x+70,y+h-2),(x+46,y+h+30)],fill=(255,255,255),outline=(20,20,20))
        d.line([(x+50,y+h),(x+47,y+h+27)],fill=(255,255,255),width=6)
    else:
        d.rounded_rectangle([x,y,x+w,y+h],radius=40,fill=(255,255,255),outline=(20,20,20),width=4)
        for i,r in enumerate([16,11,7]): d.ellipse([x+44-i*16,y+h+4+i*16,x+44-i*16+r,y+h+4+i*16+r],fill=(255,255,255),outline=(20,20,20),width=3)
    d.ellipse([x+14,y+22,x+50,y+58],fill=col,outline=(255,255,255),width=2); d.text((x+24,y+28),sym,font=fo(20),fill=(255,255,255))
    d.text((x+62,y+26),text,font=f,fill=(20,20,20))

def char_tags(d,x,y,chars):
    cx=x
    for ch in chars:
        col,sym,nm=CHAR[ch]; d.ellipse([cx,y,cx+30,y+30],fill=col); d.text((cx+8,y+4),sym,font=fo(18),fill=(255,255,255))
        d.text((cx+38,y+3),nm,font=fo(18,False),fill=INK); cx+=48+tw(d,nm,fo(18,False))

def hero():
    W,H=1020,760; c=Image.new("RGBA",(W,H),(255,255,255,255)); d=ImageDraw.Draw(c,"RGBA")
    d.text((40,30),"▶ KUD",font=fo(34),fill=INK); d.text((140,40),"AUTOPLAY",font=fo(22,False),fill=GREY)
    ph="PUNCHLINE"; pcol=PHASE[ph]
    chip=fo(24); t=f"FASE · {ph}"; d.rounded_rectangle([W-60-tw(d,t,chip)-28,32,W-60,76],radius=10,fill=pcol); d.text((W-60-tw(d,t,chip)-14,40),t,font=chip,fill=(255,255,255))
    video(c,90,110,W-180,400,"boLkKd3W2sc",ph)
    connector(d,90,310,PHASE["OPBOUW"],"OPBOUW","L"); connector(d,W-90,310,PHASE["NASLEEP"],"NASLEEP","R")
    bubble(c,150,150,"praat","Z","Niemand had dit zien aankomen.")
    d.text((90,530),"Kud - Drama",font=fo(32),fill=INK)
    d.text((90,576),"KUD ✓ · 1.204.880 weergaven · 9 jaar geleden",font=fo(20,False),fill=GREY)
    d.text((90,624),"In beeld:",font=fo(18,False),fill=GREY); char_tags(d,200,620,["K","Z"])
    d.text((90,684),"Leg aan als de vorige kaart eindigt op OPBOUW. Praatwolk mag: Zwoele Man staat erop + actieve fase.",font=fo(18,False),fill=(120,120,120))
    out=HERE/"autoplay_kaart.png"; c.convert("RGB").save(out); return out

def timeline():
    vids=["HDFaY7Fbi28","v5aZ_qlpP2g","boLkKd3W2sc","tMGYPMJJm3o"]
    cw,ch,gap=420,300,90; W=60*2+4*cw+3*gap; H=460
    c=Image.new("RGBA",(W,H),(244,244,242,255)); d=ImageDraw.Draw(c,"RGBA")
    d.rounded_rectangle([40,24,W-40,104],radius=14,fill=(20,23,29))
    d.text((60,38),"De tijdlijn speelt zich af: OPZET → OPBOUW → PUNCHLINE → NASLEEP",font=fo(30),fill=(255,255,255))
    for i,(ph,vid) in enumerate(zip(ORDER,vids)):
        x=60+i*(cw+gap); y=150; video(c,x,y,cw,ch,vid,ph,chapterlbl=False)
        col=PHASE[ph]; d.rounded_rectangle([x,y+ch+12,x+tw(d,ph,fo(26))+30,y+ch+54],radius=8,fill=col); d.text((x+15,y+ch+18),ph,font=fo(26),fill=(255,255,255))
        if i<3:
            ax=x+cw; ay=y+ch//2; d.line([(ax+10,ay),(ax+gap-10,ay)],fill=PHASE[ORDER[i+1]],width=10)
            d.polygon([(ax+gap-10,ay-14),(ax+gap-10,ay+14),(ax+gap+8,ay)],fill=PHASE[ORDER[i+1]])
    d.text((60,H-40),"Volgende kaart moet de volgende fase zijn (loopt rond: na Nasleep weer Opzet). Een Punchline mag splitsen in twee Nasleep-lijnen.",font=fo(19,False),fill=(90,90,92))
    out=HERE/"autoplay_tijdlijn.png"; c.convert("RGB").save(out); return out

def wolkjes():
    W,H=900,360; c=Image.new("RGBA",(W,H),(244,244,242,255)); d=ImageDraw.Draw(c,"RGBA")
    d.text((40,24),"WOLKJES (apart wegspelen)",font=fo(30),fill=INK)
    bubble(c,60,120,"praat","K","Konijntje? Konijntje.")
    bubble(c,60,260,"denk","P","…hier had iets moeten gebeuren.")
    d.text((470,130),"PRAATWOLK → alleen op",font=fo(22,False),fill=GREY); d.text((470,158),"actieve fasen (Opzet/Opbouw/Punchline)",font=fo(22),fill=INK)
    d.text((470,270),"DENKWOLK → alleen op",font=fo(22,False),fill=GREY); d.text((470,298),"NASLEEP (de stille gedachte)",font=fo(22),fill=INK)
    d.text((470,210),"én het karakter moet op de kaart staan.",font=fo(20,False),fill=(120,120,120))
    out=HERE/"autoplay_wolkjes.png"; c.convert("RGB").save(out); return out

if __name__=="__main__":
    for f in (hero(),timeline(),wolkjes()): print("->",f.name)
