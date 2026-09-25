#!/usr/bin/env python3
"""Top-down sim scenes, Working Theory line (Ep. 19 "muscle memory" is the reference episode) (engine lifted from xhs-pipeline/make_supermarket_sim.py).
  sim_shared  OLD HABIT: three clients walk into ONE big system (tenants +1 +2 +3)
  sim_build   COST OF NEW: 2015 bar crawls (6 MONTHS) vs 2026 bar snaps (3 DAYS)
  sim_own     NEW HABIT: three small houses, one client each, shared services 0
1080x1920, 2x supersampled, 30 fps, slow (6-8 s), everything above y=1340 (captions below)."""
import math, os, shutil, subprocess, sys
from multiprocessing import Pool
from PIL import Image, ImageDraw, ImageFont
W, H, S = 1080, 1920, 2
FB = "/System/Library/Fonts/Supplemental/Arial Black.ttf"; FR = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
OUT = os.path.expanduser("~/Movies/WT-videos/muscle-memory/inserts"); TMP = os.path.expanduser("~/Movies/WT-videos/muscle-memory/work/frames")
PAPER=(251,250,247); INK=(31,29,26); GOLD=(212,160,23); RED=(204,62,48); GREY=(138,133,122); GREEN=(72,146,98)
FLOOR=(244,240,230); TILE=(232,227,215); WALL=(52,48,44); SKIN=(236,200,168); HAIR=(40,32,28); WHITE=(255,255,255)
SHIRTS=[(46,92,150),(204,98,60),(88,140,96)]; NAMES=["BROKER","RESTAURANT","ACCOUNTANT"]
_fc={}
def font(sz,bold=True):
    k=(sz,bold)
    if k not in _fc: _fc[k]=ImageFont.truetype(FB if bold else FR, sz*S)
    return _fc[k]
class Cv:
    def __init__(s,bg=PAPER): s.im=Image.new("RGB",(W*S,H*S),bg); s.d=ImageDraw.Draw(s.im)
    def R(s,x0,y0,x1,y1,fill=None,outline=None,width=0,r=0):
        box=(x0*S,y0*S,x1*S,y1*S)
        if r: s.d.rounded_rectangle(box,radius=r*S,fill=fill,outline=outline,width=width*S)
        else: s.d.rectangle(box,fill=fill,outline=outline,width=width*S)
    def C(s,cx,cy,r,fill=None,outline=None,width=0): s.d.ellipse(((cx-r)*S,(cy-r)*S,(cx+r)*S,(cy+r)*S),fill=fill,outline=outline,width=width*S)
    def L(s,pts,fill,width): s.d.line([(x*S,y*S) for x,y in pts],fill=fill,width=width*S,joint="curve")
    def P(s,pts,fill,outline=None): s.d.polygon([(x*S,y*S) for x,y in pts],fill=fill,outline=outline)
    def T(s,x,y,t,sz,fill=INK,anchor="mm",bold=True,stroke=None): s.d.text((x*S,y*S),t,font=font(sz,bold),fill=fill,anchor=anchor,stroke_width=(4*S if stroke else 0),stroke_fill=stroke)
    def out(s): return s.im.resize((W,H),Image.LANCZOS)
def ease(t): return 0.5-0.5*math.cos(math.pi*max(0.0,min(1.0,t)))
class Path:
    def __init__(s,pts): s.pts=pts; s.seg=[math.dist(a,b) for a,b in zip(pts,pts[1:])]; s.len=sum(s.seg)
    def at(s,f):
        d=max(0.0,min(1.0,f))*s.len
        for (a,b),L in zip(zip(s.pts,s.pts[1:]),s.seg):
            if d<=L or (a,b)==(s.pts[-2],s.pts[-1]):
                k=0 if L==0 else min(1.0,d/L); return (a[0]+(b[0]-a[0])*k,a[1]+(b[1]-a[1])*k),math.atan2(b[1]-a[1],b[0]-a[0])
            d-=L
    def trail(s,f,step=34):
        n=int(max(0.0,min(1.0,f))*s.len/step); return [s.at(i*step/s.len)[0] for i in range(n+1)]
def ground(p):
    p.R(60,380,1020,1330,fill=FLOOR)
    for gx in range(60,1020,60): p.L([(gx,380),(gx,1330)],TILE,2)
    for gy in range(380,1330,60): p.L([(60,gy),(1020,gy)],TILE,2)
    p.R(60,380,1020,1330,outline=WALL,width=10)
def person(p,x,y,ang,n,i,bob=True,k=1.3):
    ca,sa=math.cos(ang)*k,math.sin(ang)*k
    def rot(dx,dy): return (x+dx*ca-dy*sa,y+dx*sa+dy*ca)
    b=1.5*math.sin(n/2.5) if bob else 0
    p.C(x+3,y+5,26*k,fill=(214,208,196)); p.C(x,y+b,24*k,fill=SHIRTS[i])
    hx,hy=rot(4,0); p.C(hx,hy+b,15*k,fill=SKIN); p.C(hx-3*ca,hy-3*sa+b,14*k,fill=HAIR)
    px,py=rot(26,-18)                       # the prop: briefcase / chef hat / calculator
    if i==0: p.R(px-12,py-9,px+12,py+9,fill=(90,60,40),r=3)
    elif i==1: p.C(px,py-4,11,fill=WHITE,outline=GREY,width=2); p.R(px-11,py+2,px+11,py+8,fill=WHITE,outline=GREY,width=2)
    else: p.R(px-10,py-13,px+10,py+13,fill=(60,60,70),r=3); p.R(px-7,py-10,px+7,py-3,fill=(180,220,200))
def footprints(p,pts,col=(196,186,168)):
    for x,y in pts: p.C(x,y,5,fill=col)
def hud(p,title,tcol,left,right,rcol=INK):
    p.T(W/2,120,title,60,tcol)
    p.R(60,220,1020,330,fill=WHITE,outline=(222,218,208),width=4,r=18)
    p.T(90,275,left,32,INK,anchor="lm"); p.T(990,275,right,32,rcol,anchor="rm")
def fly(p,n,t0,src,dst,label,col=RED,dur=26):
    k=(n-t0)/dur
    if 0<=k<=1:
        e=ease(k); x=src[0]+(dst[0]-src[0])*e; y=src[1]+(dst[1]-src[1])*e-70*math.sin(math.pi*e); p.C(x,y,13,fill=col,outline=WHITE,width=3)
    if 0<=k<=2.2:
        a=max(0.0,1-k/2.2); c=tuple(int(PAPER[i]+(col[i]-PAPER[i])*a) for i in range(3)); p.T(src[0],src[1]-50-40*k,label,30,c,stroke=WHITE)
# ---------------------------------------------------------------- scenes
DOOR=(540,1150); BLD=(300,560,780,1150)
STARTS=[(120,470),(120,860),(120,1250)]
def draw_building(p,n,glow=0):
    x0,y0,x1,y1=BLD
    if glow: g=8+4*math.sin(n/5.0); p.R(x0-g,y0-g,x1+g,y1+g,fill=(250,226,150),r=18)
    p.R(x0,y0,x1,y1,fill=(96,110,128),r=14)
    for r in range(4):
        for c in range(5): p.R(x0+40+c*90,y0+50+r*120,x0+95+c*90,y0+120+r*120,fill=(200,220,235) if (r+c)%3 else (240,190,90),r=4)
    p.R(DOOR[0]-50,y1-80,DOOR[0]+50,y1,fill=(60,44,36),r=6); p.T(W/2,y0-46,"THE SYSTEM",34,WALL)
def sim_shared(n,N=240):
    p=Cv(); ground(p); draw_building(p,n)
    paths=[Path([s,(220,s[1]),(220,DOOR[1]+60),(DOOR[0],DOOR[1]+60),(DOOR[0],DOOR[1]-30)]) for s in STARTS]
    inside=0
    for i,path in enumerate(paths):
        f=ease((n-i*40)/(N-100)); (x,y),ang=path.at(f); footprints(p,path.trail(f))
        if f<0.985: person(p,x,y,ang,n,i)
        else: inside+=1
        t0=next((k for k in range(N) if ease((k-i*40)/(N-100))>=0.985),N+99)
        fly(p,n,t0,(DOOR[0],DOOR[1]-40),(DOOR[0],BLD[1]+60),"+tenant")
        p.T(STARTS[i][0]+10,STARTS[i][1]-44,NAMES[i],22,GREY)
    hud(p,"OLD MUSCLE MEMORY",INK,"1 system, built to share",f"tenants +{inside}",RED if inside else GREY)
    return p.out()
HOUSES=[(150,700),(450,700),(750,700)]
def draw_house(p,x,y,i,lit):
    p.R(x,y+60,x+180,y+220,fill=(230,226,214),outline=WALL,width=6,r=8)
    p.P([(x-12,y+62),(x+90,y-10),(x+192,y+62)],fill=SHIRTS[i]); p.R(x+70,y+140,x+110,y+220,fill=(60,44,36) if not lit else GREEN,r=4)
    p.R(x+25,y+100,x+55,y+130,fill=(240,190,90) if lit else (200,220,235),r=3); p.R(x+125,y+100,x+155,y+130,fill=(240,190,90) if lit else (200,220,235),r=3)
    p.T(x+90,y+250,NAMES[i],22,GREY)
def sim_own(n,N=240):
    p=Cv(); ground(p)
    lit=[]
    for i,(hx,hy) in enumerate(HOUSES):
        path=Path([(hx+90,1290),(hx+90,hy+260)]); f=ease((n-i*30)/(N-110)); (x,y),ang=path.at(f)
        draw_house(p,hx,hy,i,f>=0.985); footprints(p,path.trail(f))
        if f<0.985: person(p,x,y,ang,n,i)
        else: lit.append(i)
    p.T(W/2,520,"ONE CLIENT = ONE SYSTEM",34,WALL)
    hud(p,"NEW MUSCLE MEMORY",GOLD,f"systems built: {len(lit)}","shared services: 0",GREEN)
    return p.out()
def sim_build(n,N=210):
    p=Cv(); ground(p)
    p.T(W/2,470,"TIME TO A WORKING SYSTEM",30,WALL)
    for j,(yr,label,col,full,speed) in enumerate([("2015","6 MONTHS",GREY,860,1.0),("2026","3 DAYS",GOLD,190,0.28)]):
        y=600+j*300; p.T(110,y,yr,44,INK,anchor="lm"); p.R(110,y+50,970,y+130,fill=WHITE,outline=(222,218,208),width=4,r=14)
        k=ease(n/(N*speed)); p.R(110,y+50,110+full*k,y+130,fill=col,r=14)
        if k>=1: p.T(110+full+30,y+90,label,40,col,anchor="lm")
        for m in range(1,12): p.L([(110+m*72,y+50),(110+m*72,y+130)],(240,236,226),2)
    if n>N*0.28+10: person(p,880,1240,-math.pi/2,n,0,bob=False)
    hud(p,"THE COST OF BUILDING NEW",INK,"same client, same app","DAYS, NOT MONTHS",GOLD)
    return p.out()
SCENES={"sim_shared":(sim_shared,240),"sim_build":(sim_build,210),"sim_own":(sim_own,240)}
def render(name):
    fn,N=SCENES[name]; d=f"{TMP}/{name}"; shutil.rmtree(d,ignore_errors=True); os.makedirs(d,exist_ok=True)
    for i in range(N): fn(i,N).save(f"{d}/f{i:04d}.png")
    for k in (0,N//2,N-1): fn(k,N).resize((270,480)).save(f"{TMP}/{name}_still{k}.png")
    subprocess.run(["ffmpeg","-y","-v","error","-framerate","30","-i",f"{d}/f%04d.png","-c:v","libx264","-preset","fast","-crf","18","-pix_fmt","yuv420p",f"{OUT}/{name}.mp4"],check=True)
    return name
if __name__=="__main__":
    os.makedirs(OUT,exist_ok=True); os.makedirs(TMP,exist_ok=True)
    names=sys.argv[1:] or list(SCENES)
    with Pool(3) as pool:
        for r in pool.imap_unordered(render,names): print("rendered",r,flush=True)
