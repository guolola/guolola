"""Generate original, code-drawn README motion graphics. Requires Pillow.

No character artwork is modified. All text and geometry below are editable.
Run: python scripts/build_motion.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

OUT = Path(__file__).resolve().parents[1] / 'assets'
OUT.mkdir(exist_ok=True)
FONTS = Path('C:/Windows/Fonts')
def font(size, kind='bold'):
    names = {'bold':'arialbd.ttf', 'mono':'consola.ttf', 'display':'impact.ttf', 'cn':'msyh.ttc'}
    path = FONTS / names[kind]
    if not path.exists():
        raise SystemExit('Set FONTS to a directory containing Arial, Consolas, Impact and Microsoft YaHei.')
    return ImageFont.truetype(str(path), size)

BG=(10,11,25); WHITE=(245,245,255); MUTED=(160,166,192)
PINK=(255,98,186); CYAN=(79,228,255); PURPLE=(154,104,255)
def blend(a,b,t):return tuple(round(x+(y-x)*t) for x,y in zip(a,b))
def background(w,h):
    im=Image.new('RGB',(w,h));d=ImageDraw.Draw(im)
    for y in range(h):d.line((0,y,w,y),fill=blend(BG,(30,17,49),y/h))
    for x in range(0,w,40):d.line((x,0,x,h),fill=(33,28,51))
    for y in range(0,h,40):d.line((0,y,w,y),fill=(33,28,51))
    return im
def text(d,xy,s,size=16,color=WHITE,kind='bold'):
    d.text(xy,s,font=font(size,kind),fill=color)
def star(d,x,y,r,c):
    d.polygon([(x,y-r),(x+r*.23,y-r*.23),(x+r,y),(x+r*.23,y+r*.23),(x,y+r),(x-r*.23,y+r*.23),(x-r,y),(x-r*.23,y-r*.23)],fill=c)
def save(frames,name,ms=80):
    # Shared palette prevents frame-to-frame color shimmer.
    palette=frames[0].quantize(colors=128)
    frames=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
    frames[0].save(OUT/f'{name}.gif',save_all=True,append_images=frames[1:],duration=ms,loop=0,optimize=True,disposal=1)
    frames[0].convert('RGB').save(OUT/f'{name}-still.png')
    print(name, len(frames), 'frames', (OUT/f'{name}.gif').stat().st_size, 'bytes')

def hero():
    frames=[];base=background(1000,360)
    for i in range(80):
        t=i/80;im=base.copy();d=ImageDraw.Draw(im)
        d.polygon([(735,0),(1000,0),(1000,305),(655,305)],fill=(32,20,57))
        d.polygon([(975,0),(1000,0),(1000,305),(880,305)],fill=(87,39,114))
        for n in range(22):
            x=(n*137+30)%980+10;y=47+(n*71)%230
            k=(math.sin(t*math.tau+n)+1)/2
            star(d,x,y,1.4+k*2.8,blend((65,55,83),PINK,k*.75))
        d.line((28,24,250,24),fill=CYAN,width=2)
        text(d,(28,32),'GUOLOLA   /   PERSONAL SPACE',13,CYAN,'mono')
        text(d,(732,27),'SYSTEM ONLINE',14,MUTED,'mono')
        d.ellipse((946,32,954,40),fill=blend((64,83,82),CYAN,(math.sin(t*math.tau)+1)/2))
        text(d,(44,78),'guolola',112,PURPLE,'display')
        text(d,(40,74),'guolola',112,WHITE,'display')
        # Thin moving highlight, never flashing or obscuring the title.
        d.line((43,209,575,209),fill=(78,51,104),width=2)
        x=43+int(t*480);d.line((x,209,x+50,209),fill=PINK,width=3)
        text(d,(46,229),'BUILD / CONNECT / CREATE',23,WHITE,'mono')
        text(d,(47,270),'IDEAS INTO SYSTEMS.',14,MUTED,'mono')
        # Orbital HUD uses one slow revolution per loop.
        cx,cy=823,165
        for r in (96,80,62):d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=(90,60,128),width=1)
        for n in range(3):
            a=t*math.tau+n*math.tau/3
            px=cx+math.cos(a)*96;py=cy+math.sin(a)*96
            d.ellipse((px-4,py-4,px+4,py+4),fill=[CYAN,PINK,PURPLE][n])
        d.arc((cx-80,cy-80,cx+80,cy+80),start=360*t,end=360*t+110,fill=PINK,width=4)
        text(d,(794,108),'G',66,WHITE,'display')
        text(d,(792,181),'001',21,CYAN,'mono')
        text(d,(772,264),'DENIA / 鸣潮',13,PINK,'cn')
        d.rectangle((0,315,1000,360),fill=CYAN)
        ticker='KURO  /  HOYOVERSE  /  HYPERGRYPH  /  PERSONA 03 · 04 · 05  /  '
        f=font(17,'mono');tw=d.textlength(ticker,font=f);shift=(t*tw)%tw
        for n in range(-1,3):d.text((n*tw-shift,328),ticker,font=f,fill=(11,23,36))
        frames.append(im)
    save(frames,'profile-hero')

def persona():
    frames=[];colors=[(55,180,255),(255,210,40),(255,62,91)]
    for i in range(90):
        t=i/90;im=Image.new('RGB',(1000,222),BG);d=ImageDraw.Draw(im)
        for n,(num,c,title,sub) in enumerate(zip(['03','04','05'],colors,['DARK HOUR','MIDNIGHT CHANNEL','PHANTOM THIEVES'],['月光馆学园','八十稻羽','东京'])):
            x=n*336;w=328;phase=(t*3-n)%3;active=phase<1
            d.rounded_rectangle((x,0,x+w-1,220),radius=12,fill=blend(BG,c,.12),outline=blend(BG,c,.85 if active else .4),width=2)
            d.polygon([(x+201,1),(x+326,1),(x+326,177),(x+142,177)],fill=blend(BG,c,.22))
            for k in range(5):
                yy=10+(k*34+int(t*68))%162
                d.line((x+240,yy,x+320,yy-20),fill=blend(BG,c,.3),width=2)
            text(d,(x+20,17),'PERSONA',15,c,'mono')
            text(d,(x+18,31),num,104,WHITE,'display')
            text(d,(x+22,146),title,16,c,'mono')
            text(d,(x+23,173),sub,16,WHITE,'cn')
            for k in range(12):
                d.rectangle((x+186+k*10,186,x+191+k*10,198),fill=c if k<int(phase*12)%13 and active else blend(BG,c,.23))
        frames.append(im)
    save(frames,'persona-select')

def footer():
    frames=[]
    for i in range(60):
        im=Image.new('RGB',(1000,105),BG);d=ImageDraw.Draw(im);t=i/60
        for n in range(62):
            h=8+int(27*(.5+.5*math.sin(n*.53+t*math.tau))*(.6+.4*math.cos(n*.31-t*math.tau)))
            c=blend(CYAN,PINK,n/61)
            d.rectangle((n*16+5,102-h,n*16+11,103),fill=c)
        text(d,(27,18),'SAVE POINT',16,PINK,'mono')
        text(d,(27,42),'SEE YOU NEXT TIME_',23,WHITE,'mono')
        text(d,(762,30),'CONTINUE  >',22,CYAN,'mono')
        frames.append(im)
    save(frames,'save-point')

if __name__=='__main__':
    hero();persona();footer()
